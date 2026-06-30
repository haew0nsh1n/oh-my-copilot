# Source-Overall Aggressive Cleanup — Exclusive Ownership Matrix

This matrix mirrors the OMC source-overall cleanup lane model while translating ownership to OMP roles, Python modules, markdown surfaces, and Copilot-native validation.

No lane owns the whole repository. Each lane owns a narrow source family and its tests. Parallel work is allowed only when lanes do not share files or public contracts.

## Rules

- One lane owns a file at a time.
- A lane cannot merge cleanup without its focused validation gate.
- A lane cannot mark OMC parity complete by matching filenames alone.
- A lane must compare OMC implementation method, section shape, CLI behavior, or runtime surface before claiming parity.
- If two lanes need the same file, the earlier lane must finish and document handoff notes first.
- Generated artifacts are never a lane output unless explicitly listed as shared source under `.omp/plans` or `.omp/skills`.

## Lane 0 — Baseline / inventory lock

| Target | Owner | Purpose | Gate |
| --- | --- | --- | --- |
| `.omp/plans/source-overall-cleanup/*` | planner/verifier | Keep OMC cleanup method translated to OMP | `test_source_overall_cleanup_plan_surface_exists` |
| `AGENTS.md`, `BRIEF.md`, `CONTEXT.md` | planner/writer | Maintain completion policy and shared language | `test_copilot_native_workflow.py` |
| `.github/prompts/*`, `.github/instructions/*` | planner/verifier | Prevent early autopilot completion | `test_copilot_native_workflow.py` |
| `.vscode/tasks.json` | verifier | Keep repeatable validation commands | `test_vscode_tasks_cover_omp_runtime_workflow` |

## Lane 1 — Test contract hardening

| Target | Owner | Purpose | Gate |
| --- | --- | --- | --- |
| `tests/unit/skills/test_markdown_skill_bodies.py` | test-engineer | Lock skill body depth and no internal paths | focused pytest |
| `tests/unit/skills/test_markdown_commands.py` | test-engineer | Lock command wrapper dispatch and depth | focused pytest |
| `tests/unit/test_omc_structure_parity.py` | test-engineer | Lock agents, hooks, workflows, plans | focused pytest |
| `tests/unit/test_copilot_native_workflow.py` | test-engineer | Lock autopilot/full-audit guidance | focused pytest |
| `tests/unit/skills/test_source_parity.py` | test-engineer | Lock source family mapping and missing paths | focused pytest |

## Lane 2 — Fallback / state-contract cleanup

| Target | Owner | Purpose | Gate |
| --- | --- | --- | --- |
| `src/core/provider_runtime.py` | debugger/executor | Preserve provider auth and fallback semantics | provider runtime tests |
| `src/core/omp_bridge.py` | executor/verifier | Preserve `.omp` read-only state bridge | bridge tests and bridge smoke |
| `src/core/session_recorder.py` | executor/verifier | Preserve session artifact recording | session recorder tests |
| `src/cli/main.py` | executor/verifier | Preserve command routing and strict audit | CLI tests and strict doctor |
| `.gitignore` | verifier | Preserve generated/source artifact boundary | generated-artifact policy checks |

## Lane 3 — Orchestrator seam extraction

| Target | Owner | Purpose | Gate |
| --- | --- | --- | --- |
| `src/skills/*` | architect/executor | Keep workflow orchestration behind skill APIs | unit skill tests |
| `src/domain/*` | architect/test-engineer | Keep invariants and report contracts pure | domain/skill tests |
| `src/core/*` | architect/executor | Keep runtime integration separate from skill rules | core tests |
| `src/cli/main.py` | architect/executor | Keep CLI a thin adapter | CLI tests |

## Lane 4 — Duplication / boundary cleanup

| Target | Owner | Purpose | Gate |
| --- | --- | --- | --- |
| `skills/*/SKILL.md` | writer/verifier | Preserve OMC-style skill instructions | markdown skill tests |
| `commands/*.md` | writer/verifier | Preserve lightweight dispatch wrappers | markdown command tests |
| `agents/*.md` | writer/verifier | Preserve role prompt depth | structure parity tests |
| `README.md` | writer/verifier | Keep public docs aligned with implemented behavior | docs tests / strict doctor |

## Lane 5 — Dead code / warning cleanup

| Target | Owner | Purpose | Gate |
| --- | --- | --- | --- |
| `src/**/__pycache__`, `src/**/*.pyc` | executor | Remove generated caches | generated artifact check prints nothing |
| `src/*.egg-info` | executor | Remove editable install metadata | generated artifact check prints nothing |
| stale plan artifacts | planner/verifier | Keep only shared `.omp/plans` source | structure parity tests |
| stale CLI aliases | architect/verifier | Remove only after compatibility decision | CLI tests and README update |

## Hand-off rule

- Handoff must name lane, files touched, validation run, and remaining gap.
- If a lane leaves a partial/gap status, it must update the relevant markdown plan or source-parity output expectation.
- If a lane changes public behavior, it must include writer/verifier review before completion.
- If validation fails, ownership stays with the lane until the same validation passes or a blocker is documented.
- If OMC reference behavior differs from OMP adaptation, the handoff must explain the translation rather than hiding the mismatch.

## Current OMP cleanup ownership snapshot

- Lane 0 currently owns the full-audit prompt, source-overall cleanup plans, and completion policy docs.
- Lane 1 currently owns structure tests that prevent shallow markdown parity.
- Lane 2 currently owns source artifact cleanup and strict doctor evidence.
- Lane 3 currently owns source-parity implementation mapping.
- Lane 4 currently owns expanded skill, command, and agent markdown surfaces.
- Lane 5 currently owns cache/egg-info removal after every full pytest run.