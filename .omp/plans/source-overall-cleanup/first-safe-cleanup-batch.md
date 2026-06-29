# First Safe Cleanup Batch - OMP Source-Overall Cleanup

This plan defines the first safe cleanup batch for oh-my-copilot.

## Candidate cleanup order

1. Remove generated caches and local-only artifacts from `src/` and `tests/`.
2. Tighten README structure and parity claims when tests prove behavior.
3. Keep Python product APIs in `src/skills/*.py` and Markdown skill bodies in root `skills/*/SKILL.md`.
4. Only simplify CLI compatibility branches after a focused CLI smoke test exists.

## Required checks

```bash
.venv/bin/python -m pytest tests/unit/test_omc_structure_parity.py -q
.venv/bin/python -m pytest tests/e2e/test_runtime_parity.py -q
omp doctor --strict
```
