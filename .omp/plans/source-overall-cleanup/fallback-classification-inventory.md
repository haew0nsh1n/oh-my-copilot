# Fallback Classification Inventory - OMP Source-Overall Cleanup

This OMP readiness artifact mirrors OMC's source-overall-cleanup inventory surface for oh-my-copilot.

## Scope

- Review fallback-like code in `src/core`, `src/cli`, `src/domain`, and `src/skills` before deletion.
- Classify each fallback as masking, compatibility, fail-safe, or test-only.
- Preserve behavior with tests before simplifying.

## Current OMP anchors

- `src/core/provider_runtime.py` handles provider and AOAI fallback behavior.
- `src/cli/main.py` handles CLI compatibility fallbacks for OMC-style surfaces.
- `tests/e2e/test_runtime_parity.py` is the runtime parity smoke gate.
