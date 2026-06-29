# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Layout

This is a single-context repo:

- `CONTEXT.md` at the repo root defines shared language.
- `docs/adr/` contains accepted architecture decisions.
- `BRIEF.md` defines product purpose, users, scope, and definition of done.

## Before exploring, read these

- `AGENTS.md`
- `CONTEXT.md`
- `BRIEF.md`
- Relevant ADRs under `docs/adr/`

If a future `CONTEXT-MAP.md` is added, treat the repo as multi-context and follow that map before reading context-specific documents.

## Use the glossary's vocabulary

When output names a domain concept in an issue title, refactor proposal, hypothesis, or test name, use the term as defined in `CONTEXT.md`.

If a concept is missing from the glossary, note it for `/domain-modeling` rather than inventing competing language.

## Flag ADR conflicts

If output contradicts an existing ADR, surface the conflict explicitly instead of silently overriding the decision.
