# Source-Overall Cleanup Ownership Matrix - OMP

This matrix mirrors OMC's cleanup ownership surface for oh-my-copilot.

## Lane 0 - Baseline and inventory

| Target | Owner | Purpose |
| --- | --- | --- |
| `.omp/plans/source-overall-cleanup/*` | planner/verifier | Readiness evidence |
| `tests/unit/test_omc_structure_parity.py` | verifier | Structure parity lock |
| `tests/e2e/test_runtime_parity.py` | verifier | Runtime parity lock |

## Lane 1 - Public surfaces

| Target | Owner | Purpose |
| --- | --- | --- |
| `skills/*/SKILL.md` | writer/executor | OMC-compatible skill bodies |
| `commands/*.md` | writer/executor | OMC-compatible command wrappers |
| `agents/*.md` | writer/executor | OMC-compatible agent prompts |

## Lane 2 - Python product API

| Target | Owner | Purpose |
| --- | --- | --- |
| `src/domain/*` | architect/executor | Domain invariants |
| `src/skills/*` | executor/test-engineer | Product skill API |
| `src/cli/main.py` | executor/verifier | OMP CLI adapter |
| `src/core/*` | executor/verifier | Runtime integrations |

## Rule

Do not edit multiple lanes in parallel unless tests prove the interfaces are independent.