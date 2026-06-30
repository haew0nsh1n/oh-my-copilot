---
applyTo:
  - "**/*.py"
  - "pyproject.toml"
  - "README.md"
  - "AGENTS.md"
  - "BRIEF.md"
  - "CONTEXT.md"
  - "docs/**/*.md"
  - ".github/prompts/**/*.md"
  - ".github/instructions/**/*.md"
  - "agents/**/*.md"
  - "commands/**/*.md"
  - "skills/**/*.md"
---

# Matt Pocock Harness Engineering

When changing this repository, use the local Matt Pocock-style agent skills in `.agents/skills/` as the working discipline.

Read these project documents before implementation work that changes behavior, public CLI surface, skill contracts, or architecture:

- `AGENTS.md`
- `BRIEF.md`
- `CONTEXT.md`
- relevant ADRs under `docs/adr/`

Use `.agents/skills/` as the agent-facing skill layer. Do not treat `src/skills/` as the assistant skill registry; `src/skills/` is product code that implements oh-my-copilot's Python skill API.

Choose the implementation skill by task type:

- Bug, failure, regression, or slow behavior: read `.agents/skills/diagnosing-bugs/SKILL.md` and build a tight repro before editing.
- New behavior or feature work: read `.agents/skills/tdd/SKILL.md` and drive the change with a failing test when a test seam exists.
- Module/interface design or architecture changes: read `.agents/skills/codebase-design/SKILL.md`; use `.agents/skills/design-an-interface/SKILL.md` when comparing API shapes.
- Domain terminology or ubiquitous-language changes: read `.agents/skills/domain-modeling/SKILL.md` and update `CONTEXT.md` when terms are resolved.
- Review work: read `.agents/skills/review/SKILL.md` and lead with findings.
- Refactor planning: read `.agents/skills/request-refactor-plan/SKILL.md` before broad rewrites.

Keep the product architecture intact:

- `src/domain/` owns domain models and invariants.
- `src/skills/` orchestrates domain models through a Python API.
- `src/cli/` is a thin adapter over skills and runtime helpers.
- `src/core/` holds runtime integrations, not individual skill rules.

Before declaring work complete, run the narrowest meaningful validation first, then broader validation when public surfaces changed. For CLI or skill changes, prefer:

1. Focused pytest for the touched unit.
2. Relevant `omp ...` smoke command.
3. `omp doctor --strict` when CLI surface or skill availability changed.
4. Full `.venv/bin/python -m pytest -q` when shared contracts changed.

For autopilot/parity work, do not stop after a single passing test or a successful smoke command. First run the full-surface audit gates named in `AGENTS.md` and `.github/prompts/autocopilot.prompt.md`, including `python -m cli source-parity --json`, strict doctor, focused tests for changed surfaces, and the full test suite when public contracts changed.