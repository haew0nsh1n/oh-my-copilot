# Fallback Classification Inventory — G001 Source-Overall Cleanup

This OMP readiness artifact mirrors the OMC source-overall-cleanup method, translated from `.omx/plans` to `.omp/plans` and from Claude Code runtime assumptions to OMP Python/CLI surfaces.

The goal is not to delete every fallback. The goal is to classify each fallback-like behavior before cleanup so that masking slop is removed, compatibility behavior is protected, and tests lock the difference.

## Inputs and method

- Compare the OMC reference plan shape before editing this file.
- Search OMP source with `rg 'fallback|compat|default|except|try:|TODO|pass|NotImplemented|placeholder' src tests`.
- Group findings by owner: `src/core`, `src/cli`, `src/domain`, `src/skills`, root markdown surfaces, and tests.
- Classify each fallback as masking slop, grounded compatibility, fail-safe, test-only scaffolding, or unknown.
- Require a behavior lock before deleting, narrowing, or replacing any fallback.
- Use Matt Pocock `diagnosing-bugs` for suspicious behavior and `tdd` for cleanup slices that change public behavior.

## Classification legend

- Masking slop: hides missing implementation, swallows errors, or makes a command appear successful without evidence.
- Grounded compatibility: intentionally preserves OMC-compatible CLI, markdown, or state behavior for users.
- Fail-safe: prevents destructive behavior, preserves local work, or keeps external-provider failures non-fatal.
- Test-only scaffolding: exists only to make isolated tests possible and must not leak into public runtime behavior.
- Unknown: cannot be classified without a focused test, source-parity evidence, or a nearby code read.

## High-priority inventory

| Area | Anchor | Current class | Required action |
| --- | --- | --- | --- |
| Provider runtime | `src/core/provider_runtime.py` | fail-safe / compatibility | Keep Azure auth and provider fallback behavior locked with provider runtime tests. |
| CLI compatibility | `src/cli/main.py` | grounded compatibility | Preserve OMC-compatible command names while avoiding placeholder success. |
| Bridge state | `src/core/omp_bridge.py` | grounded compatibility | Keep read-only bridge behavior verified by bridge tests and CLI smoke. |
| Source parity | `src/domain/source_parity.py`, `src/skills/source_parity.py` | compatibility / audit | Use this as the default src-family comparison gate before cleanup. |
| Markdown surfaces | `skills/`, `commands/`, `agents/` | grounded compatibility | Keep OMC-style depth tests before changing generated wording. |
| Local runtime | `.omp/state`, `.omp/artifacts`, `.omp/sessions` | fail-safe | Keep runtime artifacts ignored except explicitly shared `.omp/plans` and `.omp/skills`. |

## Masking-slop candidates to prioritize first

- CLI commands that print guidance but do not create state, artifacts, or executable evidence.
- Broad `except Exception` paths that erase failure details needed by tests or users.
- Fallback values that claim a provider, agent, command, or skill exists without checking local files.
- Markdown parity files that match OMC filenames but omit OMC method, stop rules, or verification steps.
- Any generated artifact committed under `src/`, including `__pycache__`, `.pyc`, or editable-install metadata.
- Any source-parity item marked implemented without mapped OMP source paths.

## Grounded fallbacks to protect from deletion

- `python -m cli` fallback remains valid for local development even when public docs prefer `omp`.
- Provider fallback to non-live advice remains valid when external credentials or RBAC are unavailable.
- `.omp` state/artifact fallback remains valid as the Copilot-native translation of Claude Code runtime state.
- `compact` command wrapper must remain a native host handoff because markdown commands cannot trigger `/compact` directly.
- Strict doctor may classify external provider behavior separately from local executable behavior.
- Source-parity gap labels are allowed when the gap is explicit and backed by report output.

## Required test-locks before Lane 2 edits

- Run `.venv/bin/python -m pytest tests/unit/core/test_provider_runtime.py -q` before provider fallback cleanup.
- Run `.venv/bin/python -m pytest tests/unit/cli/test_cli.py -q` before CLI compatibility cleanup.
- Run `.venv/bin/python -m pytest tests/unit/core/test_omp_bridge.py -q` before bridge cleanup.
- Run `.venv/bin/python -m pytest tests/unit/skills/test_source_parity.py -q` before source-parity cleanup.
- Run `.venv/bin/python -m pytest tests/unit/skills/test_markdown_skill_bodies.py tests/unit/skills/test_markdown_commands.py tests/unit/test_omc_structure_parity.py -q` before markdown surface cleanup.
- Run `.venv/bin/python -m cli doctor --strict` after any public command or skill availability change.

## Lane ownership / handoff notes

- `planner` owns classification changes and must keep this inventory ordered by cleanup risk.
- `architect` owns changes that alter module boundaries or domain concepts.
- `executor` owns small cleanup patches only after a test lock exists.
- `test-engineer` owns missing behavior locks and should add tests before deletion.
- `verifier` owns rerunning the exact failing check and the relevant full-surface manifest item.
- `writer` owns README, prompt, command, skill, and agent wording when cleanup changes public behavior.

## OMP-specific acceptance criteria

- Every listed fallback has a class and a required action.
- No cleanup issue is accepted if it only says “same filename as OMC”; it must name the OMC method being mirrored.
- The inventory itself stays under `.omp/plans/source-overall-cleanup` and `.omx` must not exist in this repo.
- Tests fail if required OMC-style sections are removed from this plan.
- Full cleanup completion requires strict doctor, source-parity, markdown structure tests, and full pytest evidence.
