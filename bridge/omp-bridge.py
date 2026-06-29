#!/usr/bin/env python3
"""Command-line bridge wrapper for local OMP state."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core import OmpBridge  # noqa: E402


def main() -> int:
    command = sys.argv[1] if len(sys.argv) > 1 else "status"
    bridge = OmpBridge(Path.cwd())
    if command == "status":
        payload = bridge.status()
    elif command == "state" and len(sys.argv) > 2:
        payload = bridge.read_state(sys.argv[2])
    elif command == "artifacts":
        payload = {"artifacts": bridge.list_artifacts(sys.argv[2] if len(sys.argv) > 2 else None)}
    else:
        print("Usage: omp-bridge.py status|state <name>|artifacts [command]", file=sys.stderr)
        return 1
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())