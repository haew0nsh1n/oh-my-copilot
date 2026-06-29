# Sandbox

Use this sandbox to test Copilot-native runtime changes.

## Checks

```bash
omp bridge status --json
omp doctor --strict
.venv/bin/python -m pytest tests/e2e/test_runtime_parity.py -q
```

Record failures as parity gaps and fix them with the smallest test-backed change.