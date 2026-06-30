---
description: "Run a full OMC parity audit for oh-my-copilot surfaces, then implement and re-test gaps until green."
mode: agent
---

# OMC Full Audit

Use this prompt when you want Copilot to keep working through Matt Pocock-style implementation loops until OMP surfaces are checked against OMC parity expectations.

## Always Read First

- `AGENTS.md`
- `BRIEF.md`
- `CONTEXT.md`
- `.github/instructions/matt-pocock-harness.instructions.md`
- `.github/prompts/autocopilot.prompt.md`
- relevant `.agents/skills/*/SKILL.md` for the task type

## Required Loop

1. Run the Full-Surface Audit Manifest from `AGENTS.md` and `.github/prompts/autocopilot.prompt.md`.
2. Compare OMC implementation method, not only filenames: section shape, state path semantics, command behavior, lane ownership, stop rules, and verification commands.
3. Use Matt Pocock skills as the work discipline: `tdd` for feature slices, `diagnosing-bugs` for failures, `codebase-design` for module boundaries, `review` before completion.
4. Pick the smallest failing or incomplete parity slice.
5. Add or update the focused test/contract first when a test seam exists.
6. Implement the smallest change that makes the focused check pass.
7. Rerun the same focused check.
8. Rerun the relevant manifest checks: `python -m cli source-parity --json`, `python -m cli doctor --strict`, markdown structure tests, CLI smoke, and full pytest when public contracts changed.
9. Continue until no requested surface is unclassified or failing.

## Stop Conditions

Do not stop after a single green test. Stop only when every requested surface is implemented/adapted/partial/gap with evidence, all required checks pass, or a real blocker is documented with the next command or file to inspect.

If a file exists locally with an OMC-matching name but a weaker implementation method, treat it as partial until its structure, behavior, and verification procedure are either matched or explicitly adapted.

## Default Validation Commands

```bash
python -m cli source-parity --json
python -m cli doctor --strict
python -m cli skills
python -m cli agents
python -m pytest tests/unit/skills/test_markdown_skill_bodies.py tests/unit/skills/test_markdown_commands.py tests/unit/test_omc_structure_parity.py -q
python -m pytest -q
```

Report exact command results in the final answer.