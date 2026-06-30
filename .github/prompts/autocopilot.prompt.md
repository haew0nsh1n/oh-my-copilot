---
description: "Run autonomous oh-my-claudecode parity engineering for oh-my-copilot until the requested feature set is implemented, tested, and documented."
mode: agent
---

# Autocopilot

You are running autonomous harness engineering for `oh-my-copilot`.

Goal: implement `oh-my-copilot` feature parity with `oh-my-claudecode` for the requested scope, and do not stop until the scope is implemented, tested, and documented, unless blocked by missing credentials, unavailable upstream information, or an explicit user stop.

## Required Context

Before editing code, read these repo documents and use their terminology:

- `AGENTS.md`
- `CONTEXT.md`
- `BRIEF.md`
- `docs/adr/`

Use the local `.agents/skills/` directory as the agent-facing Matt Pocock skill layer. Treat `src/skills/` and the CLI as the product being built, not as the source of available assistant skills.

## Environment Gate

Start every run by checking whether the repo can execute the harness loop:

```bash
git remote -v
command -v gh || true
command -v uv || true
PYTHONPATH=src .venv/bin/python -m cli doctor
PYTHONPATH=src .venv/bin/python -m cli autopilot "environment readiness smoke"
PYTHONPATH=src .venv/bin/python -m cli bridge status --json
.venv/bin/python -m pytest -q
```

When running inside VS Code, prefer the workspace tasks in `.vscode/tasks.json` for repeatable validation:

- `omp: bridge status`
- `omp: doctor strict`
- `omp: pytest`
- `omp: e2e runtime parity`

Use `omp bridge status --json`, `omp bridge state <name> --json`, and `omp bridge artifacts [command] --json` to inspect local `.omp` state before deciding whether a workflow is genuinely complete. If a validation fails, fix the smallest failing slice and repeat until the bridge state, strict doctor, focused tests, and relevant smoke command all pass.

If `.venv` is missing, use the repo's documented setup path. Prefer `uv` when available; otherwise use `python3 -m venv .venv` and install `.[dev]`.

If `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, or `docs/agents/domain.md` is missing, follow `/setup-matt-pocock-skills` before issue-driven flows. Default assumptions for this repo are GitHub Issues, default triage labels, and a single root `CONTEXT.md` plus `docs/adr/`, but confirm with the user before writing those setup files.

## Parity Loop

For the requested scope:

1. Use a parity-analyst posture to compare the target behavior against `oh-my-claudecode` public behavior and identify the smallest parity gap.
2. Use Matt Pocock-style engineering skills where they fit:
   - `/codebase-design` for module boundaries and deep-module pressure.
   - `/design-an-interface` when an API shape is unclear.
   - `/diagnosing-bugs` for failing behavior.
   - `/domain-modeling` when terminology or invariants are unclear.
   - `/request-refactor-plan` for broad refactors.
   - `/review` before declaring completion.
   - `/tdd` for feature work and regression fixes.
3. Convert the gap into a narrow implementation slice with a falsifiable check.
4. Write or update tests first when behavior changes.
5. Implement the smallest code change that closes the gap.
6. Run the narrow test for the touched slice immediately after the first substantive edit.
7. Iterate until the narrow tests pass.
8. Run broader validation before moving to the next gap.
9. Update README, AGENTS, CONTEXT, ADRs, or docs when user-facing behavior, public APIs, or workflow assumptions change.

Continue through adjacent parity gaps in the requested scope. Do not stop at a plan when code can be implemented. Do not declare completion without executable validation evidence.

For Copilot-native execution, repeat until all requested checks are green: inspect bridge state, run the narrow failing command/test, repair locally, then rerun `omp bridge status --json`, `omp doctor --strict`, and the relevant VS Code task or pytest command.

## Full-Surface Audit Manifest

Do not stop after a single green test, a single CLI smoke, or one implemented slice. For OMC parity work, an autopilot run must inspect every public surface in the requested scope and keep looping until each surface is either implemented, adapted, explicitly partial, or documented as a gap with evidence.

Surface parity is not filename parity. When OMP adds a file that corresponds to an OMC file, compare the OMC implementation method as well: section structure, ownership model, state path semantics, command behavior, stop rules, verification commands, and generated-artifact policy. If OMP intentionally adapts the implementation, document the translation and lock it with tests.

Use this manifest as the default full-pass checklist:

- `src/` Python implementation: domain models, skills, CLI adapters, and core runtime helpers.
- `skills/`: root OMC-style `SKILL.md` bodies with substantial operating instructions.
- `commands/`: root OMC-style lightweight command wrappers that dispatch to matching skills.
- `agents/`: root OMC-style agent prompts with role, workflow, output, guardrail, and verification sections.
- `hooks/` and `templates/hooks/`: lifecycle hook surfaces and OMP translation templates.
- `bridge/`: OMP bridge script and `.omp` state/artifact inspection surfaces.
- `benchmark/` and `benchmarks/`: deterministic compatibility smoke surfaces.
- `missions/`: mission/sandbox surfaces that explain parity work and validation.
- `.github/workflows/`, `.github/instructions/`, `.github/prompts/`, and `.vscode/tasks.json`.
- `README.md`, `AGENTS.md`, `BRIEF.md`, `CONTEXT.md`, and relevant ADRs.
- `.omp/plans/source-overall-cleanup/*.md`: OMC cleanup-plan method, lane model, section shape, and verification procedure translated from `.omx` to `.omp`.

Minimum full-surface commands for parity work:

```bash
.venv/bin/python -m cli source-parity --json
.venv/bin/python -m cli doctor --strict
.venv/bin/python -m cli skills
.venv/bin/python -m cli agents
.venv/bin/python -m pytest tests/unit/skills/test_markdown_skill_bodies.py tests/unit/skills/test_markdown_commands.py tests/unit/test_omc_structure_parity.py -q
.venv/bin/python -m pytest -q
```

When a check fails, repair the smallest local slice and rerun the same check. After it passes, rerun the manifest item that originally exposed the gap. Only move to the next surface after the current surface has evidence.

## Architecture Rules

Respect the existing layering:

- `src/domain/`: domain models, enums, invariants, pure state transitions.
- `src/skills/`: skill orchestrators over domain models.
- `src/cli/`: thin adapter over skills; no duplicated domain rules.
- `src/core/`: runtime integration only.

Public CLI parity should target `omp` as the final public surface. `python -m cli` or `PYTHONPATH=src .venv/bin/python -m cli` is acceptable as a development smoke path.

## Validation Standards

Use the cheapest relevant validation after each edit, then broaden:

```bash
.venv/bin/python -m pytest tests/unit/skills/<touched_skill_test>.py -q
.venv/bin/python -m pytest tests/unit/cli/test_cli.py -q
.venv/bin/python -m pytest -q
PYTHONPATH=src .venv/bin/python -m cli doctor
```

If the environment supports the public CLI entry point, also run the equivalent `omp` smoke command. If it does not, record that as a parity gap or setup gap instead of pretending it passed.

## Completion Bar

A run is complete only when all of these are true:

- The requested parity scope is implemented.
- Relevant domain, skill, CLI, and documentation surfaces are consistent.
- Narrow tests for touched areas pass.
- The full test suite passes, or any failure is clearly unrelated and documented.
- A CLI smoke check proves the user-facing workflow still runs.
- The Full-Surface Audit Manifest has been run for the requested scope, or each skipped item is named with a blocker and next action.
- The final response lists changed files and exact validation commands/results.

If blocked, stop only after documenting the blocker, the evidence gathered, and the next concrete action.
