#!/usr/bin/env python3
"""
detect-feedback-signal.py - Scan user message for correction keywords.
"""

import sys

SIGNALS = [
    "wrong", "incorrect", "not right", "你搞错了", "不是这样", "你又忘了",
    "missed", "forgot", "should be", "needs to be", "不对", "错了"
]


def main() -> int:
    text = sys.stdin.read().lower()
    if any(s in text for s in SIGNALS):
        print("📝 Feedback signal detected. Consider recording this correction.")
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
