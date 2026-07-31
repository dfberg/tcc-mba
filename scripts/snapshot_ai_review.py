import json
import os
import re
import subprocess
import sys

import requests

API_KEY = "AIzaSyAKJ0LC12xIdTyfs6EBNMrJWWKyMmqZ1v8" #os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("Missing GEMINI_API_KEY")
    sys.exit(1)

TEST_OUTPUT_FILE = "target/snapshot-test-output.txt"
PROMPT_LOG_FILE = "target/snapshot-prompt-log.txt"


def read_test_output():
    with open(TEST_OUTPUT_FILE, "r", encoding="utf-8") as f:
        return f.read()


def normalize_text(text):
    text = re.sub(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.*?Z",
        "<TIMESTAMP>",
        text,
    )

    text = re.sub(
        r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
        "<UUID>",
        text,
        flags=re.IGNORECASE,
    )

    return text


def get_git_diff():
    try:
        result = subprocess.run(
            ["git", "diff", "origin/main...HEAD"],
            capture_output=True,
            text=True,
            check=False,
        )

        return result.stdout[:20000]

    except Exception as ex:
        return f"Unable to collect git diff: {ex}"


def extract_snapshot_failure(output):
    lines = output.splitlines()

    relevant = []

    capture = False

    for line in lines:
        lower = line.lower()

        if (
            "expected:" in lower
            or "but was:" in lower
            or "snapshot" in lower
            or "comparisonfailure" in lower
        ):
            capture = True

        if capture:
            relevant.append(line)

        if capture and len(relevant) > 200:
            break

    return "\n".join(relevant)


def build_prompt(git_diff, snapshot_failure):
    return f"""
You are an automated reviewer for snapshot test failures.

Analyze:
1. Git diff
2. Snapshot test failure

Determine:
- Is the snapshot change intentional?
- Should the snapshot be updated?
- Is there evidence of regression?

Be conservative.

Return ONLY valid JSON.

JSON format:
{{
  "shouldUpdateSnapshot": true|false,
  "confidence": 0-100,
  "reason": "short explanation"
}}

GIT DIFF:
{git_diff}

SNAPSHOT FAILURE:
{snapshot_failure}
"""


def call_gemini(prompt):
    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-2.5-flash:generateContent"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(
        url,
        params={"key": API_KEY},
        json=payload,
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    text = data["candidates"][0]["content"]["parts"][0]["text"]

    return text


def parse_response(text):
    text = text.strip()

    text = re.sub(r"^```json", "", text)
    text = re.sub(r"```$", "", text)

    return json.loads(text)


def append_prompt_log(prompt):
    os.makedirs(os.path.dirname(PROMPT_LOG_FILE), exist_ok=True)
    with open(PROMPT_LOG_FILE, "a", encoding="utf-8") as f:
        f.write("=" * 80)
        f.write("\n")
        f.write("Prompt generated at: ")
        f.write("\n")
        f.write("\n")
        f.write(prompt)
        f.write("\n")
        f.write("\n")


def main():
    test_output = read_test_output()

    normalized_output = normalize_text(test_output)

    snapshot_failure = extract_snapshot_failure(normalized_output)

    git_diff = normalize_text(get_git_diff())

    prompt = build_prompt(git_diff, snapshot_failure)
    append_prompt_log(prompt)

    print("Reviewing snapshot with AI...")
    print("")

    raw_response = call_gemini(prompt)

    print("AI RESPONSE:")
    print(raw_response)
    print("")

    parsed = parse_response(raw_response)

    should_update = parsed.get("shouldUpdateSnapshot", False)
    confidence = parsed.get("confidence", 0)
    reason = parsed.get("reason", "")

    print(f"Should update snapshot: {should_update}")
    print(f"Confidence: {confidence}")
    print(f"Reason: {reason}")
    print("")

    if should_update and confidence >= 80:
        sys.exit(0)

    sys.exit(1)


if __name__ == "__main__":
    main()