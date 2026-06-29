---
description: "Prepare context for a manual native /compact handoff."
---

# OMP Compact

Prepare context for a manual native /compact handoff.

## Purpose

Prepare a manual native `/compact` handoff while preserving the user-provided note.

Command files stay intentionally lighter than skill bodies. They identify the dispatch target, preserve user input, and keep command behavior aligned with OMC-style slash command wrappers.

## Dispatch

This command cannot trigger native `/compact` directly from a markdown wrapper. Preserve `$ARGUMENTS`, explain the limitation, and tell the user to run native `/compact $ARGUMENTS` directly.

No root skill body is required for this command because it is a native host handoff.

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
