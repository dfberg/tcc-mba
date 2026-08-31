"""Offline concurrency regression tests for snapshot_ai_review.py.

These tests use only temporary directories and a process-local provider mock.
They never construct a request through urllib and never access experiment paths.
"""
import importlib.util
import io
import json
import multiprocessing
import os
import tempfile
import time
import unittest
import urllib.error
from pathlib import Path


ADAPTER_PATH = Path(__file__).with_name("snapshot_ai_review.py")
VALID_RAW = json.dumps({"candidates": [{"content": {"parts": [{"text": '{"decision":"ok"}'}]}}]}).encode()
SCHEMA = {"type": "object", "properties": {"decision": {"type": "string"}}, "required": ["decision"], "additionalProperties": False}


def load_adapter():
    spec = importlib.util.spec_from_file_location("snapshot_ai_review_tested", ADAPTER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def config():
    return {
        "configurationId": "CONFIG-GEMINI-02", "modelRequested": "gemini-3.6-flash",
        "authentication": {"environmentVariable": "GEMINI_API_KEY"},
        "api": {"endpointTemplate": "https://offline.invalid/{model}"},
        "http": {"timeoutSeconds": 1},
        "retryPolicy": {"maximumTechnicalAttempts": 3, "backoffSeconds": [0, 0, 0]},
    }


def worker(output, attempts, mode, counter, entered, release, result):
    adapter = load_adapter()
    os.environ["GEMINI_API_KEY"] = "offline-test-key"

    def fake_call(*_args):
        with counter.get_lock():
            counter.value += 1
        if entered is not None:
            entered.set()
        if release is not None:
            release.wait(5)
        if mode == "timeout":
            raise TimeoutError()
        if mode == "429":
            raise urllib.error.HTTPError("offline", 429, "rate", {}, io.BytesIO(b'{"error":"rate"}'))
        if mode == "exception":
            raise RuntimeError("offline provider failure")
        return 200, VALID_RAW

    adapter.call_gemini = fake_call
    try:
        adapter.run_inference(config(), b"offline prompt", SCHEMA, Path(output), Path(attempts))
        result.put("ok")
    except Exception as error:  # expected for technical/exception paths
        result.put(type(error).__name__)


class ConcurrencyTests(unittest.TestCase):
    def setUp(self):
        self.context = multiprocessing.get_context("spawn")

    def start(self, root, mode, counter, entered=None, release=None, rerun=False):
        execution = root / "reruns" / "rerun-01" if rerun else root
        result = self.context.Queue()
        process = self.context.Process(target=worker, args=(execution / "llm-output.json", execution / "attempts", mode, counter, entered, release, result))
        process.start()
        return process, result

    def join(self, process, result):
        process.join(10)
        self.assertEqual(process.exitcode, 0)
        return result.get(timeout=2)

    def test_c1_c2_c3_same_namespace_and_resume(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "execution"
            counter = self.context.Value("i", 0)
            entered, release = self.context.Event(), self.context.Event()
            first, first_result = self.start(root, "valid", counter, entered, release, rerun=True)
            self.assertTrue(entered.wait(5))
            second, second_result = self.start(root, "valid", counter, rerun=True)
            time.sleep(.2)
            release.set()
            self.assertEqual(self.join(first, first_result), "ok")
            self.assertEqual(self.join(second, second_result), "RuntimeError")
            self.assertEqual(counter.value, 1)
            self.assertTrue((root / "reruns" / "rerun-01" / "llm-output.json").is_file())

            # A preserved retryable attempt resumes exclusively at attempt-02.
            resume_root = Path(temporary) / "resume"
            adapter = load_adapter()
            adapter.preserve_attempt(resume_root / "attempts" / "attempt-01", {"attempt": 1, "status": "RATE_LIMIT"}, b"{}")
            counter = self.context.Value("i", 0)
            first, first_result = self.start(resume_root, "valid", counter)
            second, second_result = self.start(resume_root, "valid", counter)
            self.assertEqual(self.join(first, first_result), "ok")
            self.assertEqual(self.join(second, second_result), "RuntimeError")
            self.assertEqual(counter.value, 1)
            self.assertTrue((resume_root / "attempts" / "attempt-02" / "attempt.json").is_file())

    def test_c4_budget_c5_exception_c6_c7_isolation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            adapter = load_adapter()
            budget_root = root / "budget"
            adapter.preserve_attempt(budget_root / "attempts" / "attempt-01", {"attempt": 1, "status": "TIMEOUT"})
            counter = self.context.Value("i", 0)
            first, first_result = self.start(budget_root, "timeout", counter)
            self.assertEqual(self.join(first, first_result), "RuntimeError")
            second, second_result = self.start(budget_root, "valid", counter)
            self.assertEqual(self.join(second, second_result), "RuntimeError")
            self.assertEqual(counter.value, 2)

            exception_root = root / "exception"
            counter = self.context.Value("i", 0)
            first, first_result = self.start(exception_root, "exception", counter)
            self.assertEqual(self.join(first, first_result), "RuntimeError")
            second, second_result = self.start(exception_root, "valid", counter)
            self.assertEqual(self.join(second, second_result), "ok")
            self.assertEqual(counter.value, 2)

            # Separate execution roots—including original vs rerun—do not share locks.
            counter = self.context.Value("i", 0)
            a, ar = self.start(root / "a", "valid", counter)
            b, br = self.start(root / "b", "valid", counter)
            self.assertEqual(self.join(a, ar), "ok")
            self.assertEqual(self.join(b, br), "ok")
            self.assertEqual(counter.value, 2)
            counter = self.context.Value("i", 0)
            original, original_result = self.start(root / "same-exp", "valid", counter)
            rerun, rerun_result = self.start(root / "same-exp", "valid", counter, rerun=True)
            self.assertEqual(self.join(original, original_result), "ok")
            self.assertEqual(self.join(rerun, rerun_result), "ok")
            self.assertEqual(counter.value, 2)

    def test_timeout_and_429_preserve_expected_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "timeout"
            counter = self.context.Value("i", 0)
            process, result = self.start(root, "timeout", counter)
            self.assertEqual(self.join(process, result), "RuntimeError")
            self.assertFalse((root / "attempts" / "attempt-01" / "response.raw.json").exists())
            root = Path(temporary) / "rate-limit"
            counter = self.context.Value("i", 0)
            process, result = self.start(root, "429", counter)
            self.assertEqual(self.join(process, result), "RuntimeError")
            self.assertTrue((root / "attempts" / "attempt-01" / "response.raw.json").is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)
