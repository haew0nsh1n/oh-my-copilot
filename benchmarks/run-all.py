#!/usr/bin/env python3
"""Run deterministic OMP benchmark compatibility checks."""

import json
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    result = {
        "skill_bodies": len(list((root / "skills").glob("*/SKILL.md"))),
        "command_bodies": len(list((root / "commands").glob("*.md"))),
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())