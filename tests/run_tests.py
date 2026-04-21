#!/usr/bin/env python3
"""
Unified test runner for harness exit-check tests.

Usage:
    python3 tests/run_tests.py              # Run all tests
    python3 tests/run_tests.py -v           # Verbose mode
    python3 tests/run_tests.py -k release   # Filter by keyword
"""

import argparse
import sys
import time
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).parent

# Ensure tests/ can be imported by adding parent dir to path
if str(TESTS_DIR.parent) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR.parent))


def discover_tests(pattern: str = "test_*.py") -> unittest.TestSuite:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for test_file in sorted(TESTS_DIR.glob(pattern)):
        if test_file.name == "run_tests.py":
            continue
        module_name = f"tests.{test_file.stem}"
        try:
            module = __import__(module_name, fromlist=["tests"])
            suite.addTests(loader.loadTestsFromModule(module))
        except Exception as e:
            print(f"⚠️  Failed to load {module_name}: {e}")
    return suite


def main() -> int:
    parser = argparse.ArgumentParser(description="Run harness exit-check tests")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-k", "--keyword", default="", help="Filter test names by keyword")
    args = parser.parse_args()

    print("═══ Harness Exit-Check Test Suite ═══\n")

    suite = discover_tests()

    if args.keyword:
        filtered = unittest.TestSuite()
        for test in suite:
            if args.keyword.lower() in str(test).lower():
                filtered.addTest(test)
        suite = filtered
        print(f"Filtered by '{args.keyword}': {suite.countTestCases()} test(s)\n")

    if suite.countTestCases() == 0:
        print("No tests found.")
        return 1

    verbosity = 2 if args.verbose else 1
    runner = unittest.TextTestRunner(verbosity=verbosity)

    start = time.time()
    result = runner.run(suite)
    elapsed = time.time() - start

    print(f"\n{'─' * 50}")
    print(f"Ran {result.testsRun} test(s) in {elapsed:.2f}s")

    if result.wasSuccessful():
        print("✅ All tests passed.")
        return 0
    else:
        print("❌ Some tests failed.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
