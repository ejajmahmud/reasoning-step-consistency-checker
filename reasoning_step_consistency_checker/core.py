"""Core evidence-grounding verifier checking summary claims against tool outputs."""
import re
from typing import Any, Dict, List


class ConsistencyChecker:
    """Verifies that numeric metrics and file paths in agent summaries appear in tool outputs."""

    NUM_RE = re.compile(r"\b\d+(?:\.\d+)?\b")
    PATH_RE = re.compile(r"\b[A-Za-z0-9_/-]+\.[a-z]{1,5}\b")

    def verify(self, summary: str, tool_outputs: List[str]) -> Dict[str, Any]:
        evidence = "\n".join(tool_outputs)
        ev_nums = set(self.NUM_RE.findall(evidence))
        ev_paths = set(self.PATH_RE.findall(evidence))

        claimed_nums = self.NUM_RE.findall(summary)
        claimed_paths = self.PATH_RE.findall(summary)

        bad_nums = sorted(n for n in set(claimed_nums) if n not in ev_nums)
        bad_paths = sorted(p for p in set(claimed_paths) if p not in ev_paths)

        contradiction = ("passed" in summary.lower() and "fail" in evidence.lower() and "0 failed" not in evidence.lower())

        return {
            "grounded": not bad_nums and not bad_paths and not contradiction,
            "ungrounded_numbers": bad_nums,
            "ungrounded_paths": bad_paths,
            "status_contradiction": contradiction,
        }
