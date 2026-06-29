---
name: skill
description: Use when listing, checking, or managing root Markdown skill bodies.
---

# Skill

Use when listing, checking, or managing root Markdown skill bodies.

This body is intentionally written as an OMC-style operating guide for an agent. It should tell the agent when to use the skill, how to proceed, what to produce, and how to verify completion without exposing internal Python file paths.

## When To Use

- Use this skill when the user asks for skill work or when the current task naturally falls into engineering workflow.
- Use it when a workflow needs a repeatable set of steps instead of a one-off answer.
- Use it when evidence, state, or artifacts should survive beyond a single chat response.
- Prefer this skill over ad hoc reasoning when it can make the next action explicit and testable.
- If another Matt Pocock skill is more specific, use that skill first and treat this one as the product-facing OMP surface.

## Inputs

- User request or task description.
- Relevant repository files, current diagnostics, command output, or prior artifacts.
- Any OMC reference behavior that should be translated to OMP behavior.
- Constraints from `AGENTS.md`, `CONTEXT.md`, and nearby tests.
- The intended public surface: CLI command, markdown instruction, artifact, state file, or report.

## Workflow

1. Restate the concrete goal in OMP terms and identify the nearest public interface.
2. Gather only the local evidence needed to decide the next safe action.
3. Check whether this task is an OMC parity surface, an OMP-native product skill, or both.
4. Execute the smallest useful step through the documented OMP surface.
5. Record any durable output as state, artifact, markdown, or test coverage when the workflow calls for it.
6. Validate with the narrowest command that can disconfirm the result, then broaden only when the surface changed.
7. Report remaining gaps as explicit follow-up work instead of implying full parity.

## Outputs

- A concise result that names the completed work and any remaining gap.
- Updated markdown, state, artifact, test, or CLI output when the workflow requires it.
- Evidence from commands, tests, or review notes that the work is complete.
- A clear distinction between implemented, adapted, partial, and intentionally unsupported OMC behavior.
- No references to private implementation paths inside the root markdown skill body.

## OMP Mapping

- Primary OMP command: `omp skill <input>`.
- Reference alignment: OMC public skill surface.
- Runtime target: Copilot-friendly Python, CLI, markdown, `.omp` state, and repository artifacts.
- This skill preserves the OMC-style markdown instruction surface for Copilot use.
- Translate Claude Code-only assumptions into OMP equivalents rather than copying provider-specific mechanics.

## Guardrails

- Keep the skill body as agent-facing instructions, not implementation documentation.
- Do not claim OMC parity unless tests, smoke checks, or source-parity evidence support it.
- Do not hide uncertainty: mark incomplete behavior as partial or gap.
- Preserve existing user work and avoid broad rewrites unrelated to the requested workflow.
- Keep command examples executable in this repository, preferring `omp` or `python -m cli` fallback.
- When editing code, follow the Matt Pocock workflow skill appropriate to the task type.

## Verification

- Run the focused pytest file for the touched skill, command, or markdown contract.
- Run `python -m cli skills` when skill availability or descriptions changed.
- Run `python -m cli doctor --strict` when CLI, skill registration, or parity evidence changed.
- Run `python -m cli source-parity --json` when the change affects OMC-to-OMP source parity.
- Run the full test suite when shared contracts, public surfaces, or many skill bodies changed.
- Confirm generated caches under `src/` are not left behind after validation.

## Handoff Notes

- Keep follow-up tasks small and named after the missing OMC capability or OMP surface.
- Link the next action to a failing test, strict doctor item, source-parity gap, or documented artifact.
- If this skill is invoked by a command wrapper, keep the wrapper lightweight and put durable instructions here.
