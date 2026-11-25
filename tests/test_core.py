"""Tests for Reasoning Step Consistency Checker."""
import unittest
from reasoning_step_consistency_checker.core import ConsistencyChecker


class TestConsistencyChecker(unittest.TestCase):
    def setUp(self):
        self.chk = ConsistencyChecker()

    def test_grounded_summary_passes(self):
        res = self.chk.verify(
            "Edited router.py and verified 14 tests with 0 failed.",
            ["Modified router.py", "Ran 14 tests in 0.02s - 0 failed"],
        )
        self.assertTrue(res["grounded"])

    def test_catches_invented_numbers_paths_and_fake_pass(self):
        res = self.chk.verify(
            "Fixed phantom.py and 99 tests passed.",
            ["Modified real.py. Ran 5 tests: 2 failed."],
        )
        self.assertFalse(res["grounded"])
        self.assertIn("99", res["ungrounded_numbers"])
        self.assertIn("phantom.py", res["ungrounded_paths"])
        self.assertTrue(res["status_contradiction"])
