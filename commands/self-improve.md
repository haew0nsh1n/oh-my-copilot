---
description: "Dispatch to the OMP self-improve skill."
---

# OMP Self Improve

Dispatch to the OMP self-improve skill.

## Purpose

Dispatch `self-improve` command requests to the matching OMP skill body without embedding long instructions here.

Command files stay intentionally lighter than skill bodies. They identify the dispatch target, preserve user input, and keep command behavior aligned with OMC-style slash command wrappers.

## Dispatch

Read `skills/self-improve/SKILL.md`, follow its workflow, and pass the preserved argument block as the user request.

Target skill body: `skills/self-improve/SKILL.md`.

## Arguments

Preserve the user arguments exactly:

```text
$ARGUMENTS
```

Treat the block above as the task input. Do not reinterpret missing arguments unless the target skill asks for clarification.

## OMP Notes

- Keep this wrapper short and put durable operating instructions in the target skill body.
- Prefer public `omp` terminology when explaining behavior to the user.
- If the command maps to an OMC-only runtime detail, translate it to the closest OMP CLI, `.omp` state, markdown, or artifact surface.
- Do not claim execution happened unless the target skill or CLI command produced evidence.

## Verification

- Confirm the target skill body exists unless this command explicitly delegates to native `/compact`.
- For command surface changes, run `python -m pytest tests/unit/skills/test_markdown_commands.py -q`.
- For broad command or skill changes, run `python -m cli doctor --strict`.
- When command output or dispatch behavior changes, run the relevant `omp` or `python -m cli` smoke command.
