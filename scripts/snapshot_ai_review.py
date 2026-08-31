import argparse
import contextlib
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


TECHNICAL_RETRY_STATES = {
    "TIMEOUT",
    "API_ERROR",
    "RATE_LIMIT",
    "EMPTY_RESPONSE",
    "INVALID_JSON",
    "SCHEMA_INVALID",
}


def read_bytes(path):
    return Path(path).read_bytes()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest().upper()


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def validate_instance(instance, schema, location="$"):
    schema_type = schema.get("type")
    type_checks = {
        "object": lambda value: isinstance(value, dict),
        "array": lambda value: isinstance(value, list),
        "string": lambda value: isinstance(value, str),
        "integer": lambda value: isinstance(value, int) and not isinstance(value, bool),
        "number": lambda value: isinstance(value, (int, float)) and not isinstance(value, bool),
        "boolean": lambda value: isinstance(value, bool),
        "null": lambda value: value is None,
    }
    if schema_type and not type_checks[schema_type](instance):
        raise ValueError(f"{location}: expected {schema_type}")

    if "enum" in schema and instance not in schema["enum"]:
        raise ValueError(f"{location}: value is outside the allowed enum")

    if isinstance(instance, dict):
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        missing = [name for name in required if name not in instance]
        if missing:
            raise ValueError(f"{location}: missing required properties: {', '.join(missing)}")
        if schema.get("additionalProperties") is False:
            extras = [name for name in instance if name not in properties]
            if extras:
                raise ValueError(f"{location}: unexpected properties: {', '.join(extras)}")
        for name, value in instance.items():
            if name in properties:
                validate_instance(value, properties[name], f"{location}.{name}")

    if isinstance(instance, list) and "items" in schema:
        for index, value in enumerate(instance):
            validate_instance(value, schema["items"], f"{location}[{index}]")

    if isinstance(instance, str) and len(instance) < schema.get("minLength", 0):
        raise ValueError(f"{location}: string is shorter than minLength")
    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            raise ValueError(f"{location}: value is below minimum")
        if "maximum" in schema and instance > schema["maximum"]:
            raise ValueError(f"{location}: value is above maximum")


def provider_response_schema(schema):
    supported = {
        "$id",
        "$defs",
        "$ref",
        "$anchor",
        "type",
        "properties",
        "required",
        "additionalProperties",
        "items",
        "prefixItems",
        "enum",
        "minItems",
        "maxItems",
        "minimum",
        "maximum",
        "anyOf",
        "oneOf",
        "title",
        "description",
        "format",
    }

    def project(value):
        if isinstance(value, dict):
            projected = {}
            for key, item in value.items():
                if key not in supported:
                    continue
                if key == "properties":
                    projected[key] = {name: project(subschema) for name, subschema in item.items()}
                else:
                    projected[key] = project(item)
            return projected
        if isinstance(value, list):
            return [project(item) for item in value]
        return value

    return project(schema)


def build_request_payload(prompt_text, output_schema):
    return {
        "contents": [{"parts": [{"text": prompt_text}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseJsonSchema": provider_response_schema(output_schema),
        },
    }


def extract_model_text(provider_body):
    data = json.loads(provider_body.decode("utf-8"))
    candidates = data.get("candidates") or []
    if not candidates:
        return ""
    parts = candidates[0].get("content", {}).get("parts", [])
    return "".join(part.get("text", "") for part in parts).strip()


def classify_http_error(error):
    if error.code == 429:
        return "RATE_LIMIT", True
    if error.code in {408, 500, 502, 503, 504}:
        return "API_ERROR", True
    return "API_ERROR", False


def call_gemini(url, api_key, payload, timeout_seconds):
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        return response.status, response.read()


def preserve_attempt(attempt_dir, metadata, raw_body=None):
    attempt_dir.mkdir(parents=True, exist_ok=False)
    if raw_body is not None:
        (attempt_dir / "response.raw.json").write_bytes(raw_body)
        metadata["rawResponseSha256"] = sha256_bytes(raw_body)
    (attempt_dir / "attempt.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


@contextlib.contextmanager
def execution_lock(execution_root):
    """Hold an OS-level lock for one complete execution namespace."""
    execution_root.mkdir(parents=True, exist_ok=True)
    lock_path = execution_root / ".execution.lock"
    descriptor = os.open(lock_path, os.O_CREAT | os.O_RDWR)
    acquired = False
    try:
        # Both APIs lock one existing byte. This marker is not the exclusion.
        os.lseek(descriptor, 0, os.SEEK_SET)
        os.write(descriptor, b"\0")
        os.lseek(descriptor, 0, os.SEEK_SET)
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(descriptor, msvcrt.LK_LOCK, 1)
        else:
            import fcntl

            fcntl.flock(descriptor, fcntl.LOCK_EX)
        acquired = True
        yield
    finally:
        if acquired:
            if os.name == "nt":
                import msvcrt

                os.lseek(descriptor, 0, os.SEEK_SET)
                msvcrt.locking(descriptor, msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)
        try:
            lock_path.unlink()
        except (FileNotFoundError, PermissionError):
            # A waiting Windows process can still have the artifact open and
            # takes over cleanup after it releases the same OS lock.
            pass


def write_output_exclusively(output_path, model_text):
    """Publish normative output bytes without silent replacement."""
    descriptor = os.open(output_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
    try:
        with os.fdopen(descriptor, "wb") as output_file:
            output_file.write(model_text.encode("utf-8"))
    except BaseException:
        try:
            output_path.unlink()
        except FileNotFoundError:
            pass
        raise


def _run_inference_locked(config, prompt_bytes, output_schema, output_path, attempts_dir):
    api_key = os.getenv(config["authentication"]["environmentVariable"])
    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY environment variable")

    model = config["modelRequested"]
    url = config["api"]["endpointTemplate"].format(model=model)
    prompt_text = prompt_bytes.decode("utf-8")
    prompt_hash = sha256_bytes(prompt_bytes)
    payload = build_request_payload(prompt_text, output_schema)
    timeout_seconds = config["http"]["timeoutSeconds"]
    maximum_attempts = config["retryPolicy"]["maximumTechnicalAttempts"]
    backoff_seconds = config["retryPolicy"]["backoffSeconds"]

    existing_attempts = sorted(path for path in attempts_dir.glob("attempt-*") if path.is_dir()) if attempts_dir.exists() else []
    expected_names = [f"attempt-{index:02d}" for index in range(1, len(existing_attempts) + 1)]
    if [path.name for path in existing_attempts] != expected_names:
        raise RuntimeError("Attempt namespace is not contiguous")
    for path in existing_attempts:
        if not (path / "attempt.json").is_file():
            raise RuntimeError(f"Incomplete preserved attempt: {path}")
    if output_path.exists():
        raise RuntimeError(f"Valid output already exists: {output_path}")
    start_attempt = len(existing_attempts) + 1
    if start_attempt > maximum_attempts:
        raise RuntimeError("Technical attempt budget already exhausted")

    for attempt_number in range(start_attempt, maximum_attempts + 1):
        attempt_path = attempts_dir / f"attempt-{attempt_number:02d}"
        if attempt_path.exists():
            raise RuntimeError(f"Attempt slot already exists before provider call: {attempt_path}")
        metadata = {
            "attempt": attempt_number,
            "timestamp": utc_now(),
            "configurationId": config["configurationId"],
            "modelRequested": model,
            "renderedPromptSha256": prompt_hash,
            "status": None,
        }
        raw_body = None
        retryable = False
        try:
            http_status, raw_body = call_gemini(url, api_key, payload, timeout_seconds)
            metadata["httpStatus"] = http_status
            model_text = extract_model_text(raw_body)
            if not model_text:
                metadata["status"] = "EMPTY_RESPONSE"
                retryable = True
            else:
                try:
                    parsed = json.loads(model_text)
                except json.JSONDecodeError:
                    metadata["status"] = "INVALID_JSON"
                    retryable = True
                else:
                    try:
                        validate_instance(parsed, output_schema)
                    except ValueError as error:
                        metadata["status"] = "SCHEMA_INVALID"
                        metadata["validationError"] = str(error)
                        retryable = True
                    else:
                        metadata["status"] = "VALID_RESPONSE"
                        metadata["modelOutputSha256"] = sha256_bytes(model_text.encode("utf-8"))
                        preserve_attempt(attempt_path, metadata, raw_body)
                        write_output_exclusively(output_path, model_text)
                        return parsed
        except TimeoutError:
            metadata["status"] = "TIMEOUT"
            retryable = True
        except urllib.error.HTTPError as error:
            raw_body = error.read()
            metadata["httpStatus"] = error.code
            metadata["status"], retryable = classify_http_error(error)
        except urllib.error.URLError:
            metadata["status"] = "API_ERROR"
            retryable = True

        preserve_attempt(attempt_path, metadata, raw_body)
        if not retryable or metadata["status"] not in TECHNICAL_RETRY_STATES:
            break
        if attempt_number < maximum_attempts:
            time.sleep(backoff_seconds[attempt_number - 1])

    raise RuntimeError("No valid response was obtained within the technical retry policy")


def run_inference(config, prompt_bytes, output_schema, output_path, attempts_dir):
    # Acquire before inspecting any execution state. The lock is deliberately
    # held across provider calls, persistence, and retry decisions.
    with execution_lock(output_path.parent):
        return _run_inference_locked(
            config, prompt_bytes, output_schema, output_path, attempts_dir
        )


def validate_configuration(config):
    required = {
        "configurationId",
        "provider",
        "modelRequested",
        "promptTemplate",
        "promptTemplateSha256",
        "api",
        "authentication",
        "structuredOutput",
        "explicitlyConfigured",
        "providerDefaults",
        "unsupportedOrObsolete",
        "http",
        "retryPolicy",
        "validResponsesPerExperiment",
        "preparedAt",
    }
    missing = sorted(required - set(config))
    if missing:
        raise ValueError(f"Configuration is missing fields: {', '.join(missing)}")
    if config["configurationId"] != "CONFIG-GEMINI-02":
        raise ValueError("Unexpected configurationId")
    if config["modelRequested"] != "gemini-3.6-flash":
        raise ValueError("Unexpected Gemini model")
    if config["promptTemplate"] != "PROMPT_TEMPLATE_V1":
        raise ValueError("Unexpected prompt template")
    if config["retryPolicy"]["maximumTechnicalAttempts"] != 3:
        raise ValueError("Technical retry policy must allow exactly three attempts")
    if config["validResponsesPerExperiment"] != 1:
        raise ValueError("The main round requires one valid response per EXP/configuration")


def dry_run_summary(config, prompt_path, prompt_hash, schema_path):
    return {
        "mode": "DRY_RUN",
        "configurationId": config["configurationId"],
        "provider": config["provider"],
        "modelRequested": config["modelRequested"],
        "promptTemplate": config["promptTemplate"],
        "renderedPromptPath": str(prompt_path),
        "renderedPromptSha256": prompt_hash,
        "responseSchema": str(schema_path),
        "structuredOutput": config["structuredOutput"],
        "explicitlyConfigured": config["explicitlyConfigured"],
        "providerDefaults": config["providerDefaults"],
        "unsupportedOrObsolete": config["unsupportedOrObsolete"],
        "maximumTechnicalAttempts": config["retryPolicy"]["maximumTechnicalAttempts"],
        "apiCalls": 0,
        "groundTruthLoaded": False,
    }


def parse_args():
    parser = argparse.ArgumentParser(description="Benchmark V2 Gemini inference adapter")
    parser.add_argument("--configuration", required=True, type=Path)
    parser.add_argument("--prompt", required=True, type=Path)
    parser.add_argument("--response-schema", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--attempts-dir", type=Path)
    parser.add_argument("--execution-id", choices=("original", "rerun-01"), default="original")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    config = read_json(args.configuration)
    validate_configuration(config)
    prompt_bytes = read_bytes(args.prompt)
    prompt_hash = sha256_bytes(prompt_bytes)
    output_schema = read_json(args.response_schema)

    if args.dry_run:
        print(json.dumps(dry_run_summary(config, args.prompt, prompt_hash, args.response_schema), indent=2))
        return 0

    if args.output is None or args.attempts_dir is None:
        raise ValueError("--output and --attempts-dir are required outside dry-run mode")

    if args.execution_id == "rerun-01":
        execution_root = args.output.parent / "reruns" / args.execution_id
        output_path = execution_root / "llm-output.json"
        attempts_dir = execution_root / "attempts"
    else:
        output_path = args.output
        attempts_dir = args.attempts_dir
    run_inference(config, prompt_bytes, output_schema, output_path, attempts_dir)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(2)
