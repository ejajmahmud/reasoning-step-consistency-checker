"""CLI for Reasoning Step Consistency Checker."""
import argparse
import json
from .core import ConsistencyChecker


def main():
    parser = argparse.ArgumentParser(description="Reasoning Step Consistency Checker CLI")
    parser.add_argument("--summary", default="Updated app.py and all 10 tests passed.")
    parser.add_argument("--evidence", default="Modified app.py. Ran 10 tests, 0 failed.")
    args = parser.parse_args()

    chk = ConsistencyChecker()
    print(json.dumps(chk.verify(args.summary, [args.evidence]), indent=2))


if __name__ == "__main__":
    main()
