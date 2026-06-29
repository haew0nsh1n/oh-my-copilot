# Sandbox

Use this mission sandbox for small parity slices.

## Loop

1. Compare one OMC public behavior against OMP.
2. Choose the relevant Matt Pocock skill (`tdd`, `diagnosing-bugs`, `codebase-design`, or `review`).
3. Add the smallest failing test that captures the parity gap.
4. Implement the smallest OMP adaptation.
5. Run focused tests, `omp doctor --strict`, and broader validation when public surfaces changed.

## Evidence

- `tests/e2e/test_runtime_parity.py`
- `tests/unit/test_omc_structure_parity.py`
- `tests/unit/skills/test_markdown_skill_bodies.py`
- `tests/unit/skills/test_markdown_commands.py`