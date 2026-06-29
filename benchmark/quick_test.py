#!/usr/bin/env python3
"""Deterministic benchmark smoke for OMP runtime surfaces."""

from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    assert (root / "skills").exists()
    assert (root / "commands").exists()
    print("benchmark_smoke=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())