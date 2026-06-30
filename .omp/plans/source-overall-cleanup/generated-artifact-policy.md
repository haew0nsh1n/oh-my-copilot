# Generated Artifact Policy and Static/Security Gate

This policy mirrors the OMC generated-artifact cleanup method while translating paths and runtime expectations to OMP. It defines what is source, what is generated, and which gates must run before cleanup is accepted.

## Scope and source anchors

- Source anchors: `src/`, `tests/`, `skills/`, `commands/`, `agents/`, `hooks/`, `templates/`, `bridge/`, `benchmark/`, `benchmarks/`, `missions/`, `.github/`, `.vscode/tasks.json`, `.omp/plans/`.
- Runtime anchors: `.omp/state`, `.omp/artifacts`, `.omp/sessions`, provider credentials, local virtualenvs, cache directories.
- Reference anchor: OMC `.omx/plans/source-overall-cleanup/generated-artifact-policy.md`.
- Translation rule: OMC `.omx` shared plan artifacts become OMP `.omp/plans`; local runtime state remains ignored.
- Security rule: generated artifacts must not hide secrets, provider tokens, local paths that imply credentials, or stale execution outputs.

## Package/build evidence

- `MANIFEST.in` includes root markdown surfaces that are intended source distribution inputs.
- `.gitignore` ignores `.omp/*` by default but explicitly allows `.omp/plans/**` and `.omp/skills/**`.
- `.gitignore` ignores generated Python caches and editable install metadata.
- `.vscode/tasks.json` is a shared validation surface and must remain trackable.
- Full pytest regenerates `src/**/__pycache__`; cleanup must remove those after validation.
- `src/oh_my_copilot.egg-info` is editable-install metadata and must not be committed.

## Decision

- Commit source files that describe product behavior, parity surfaces, tests, prompts, workflows, and reusable validation tasks.
- Do not commit local runtime state, caches, virtual environments, build output, or provider-specific artifacts.
- Keep `.omp/plans/source-overall-cleanup/*.md` as source because these files are shared cleanup plans, not runtime logs.
- Keep `.omp/state`, `.omp/artifacts`, and `.omp/sessions` ignored because those are machine/session-local outputs.
- Keep root `skills/`, `commands/`, and `agents/` committed because they are OMC-compatible public surfaces.

## Artifact classes and required action

| Artifact class | Examples | Required action |
| --- | --- | --- |
| Python cache | `__pycache__`, `*.pyc` | Delete after tests; never commit. |
| Editable metadata | `src/*.egg-info` | Delete after install/test runs; never commit. |
| Runtime state | `.omp/state/**`, `.omp/artifacts/**`, `.omp/sessions/**` | Ignore by default; inspect through bridge when needed. |
| Shared OMP plans | `.omp/plans/**/*.md` | Commit when they define repeatable workflow or policy. |
| Public markdown surfaces | `skills/`, `commands/`, `agents/` | Commit and lock with structure tests. |
| Hook templates | `hooks/hooks.json`, `templates/hooks/*.mjs` | Commit and lock with structure tests. |
| Benchmark sources | `benchmark/`, `benchmarks/` | Commit deterministic smoke sources and baselines. |
| Credentials | `.env`, provider tokens, cloud auth output | Never commit; document setup only. |

## Final verification procedure

```bash
.venv/bin/python -m cli source-parity --json
.venv/bin/python -m cli doctor --strict
.venv/bin/python -m pytest tests/unit/test_omc_structure_parity.py -q
.venv/bin/python -m pytest tests/unit/test_copilot_native_workflow.py -q
.venv/bin/python -m pytest -q
find src \( -type d -name '__pycache__' -o -type d -name '*.egg-info' -o -type f -name '*.pyc' \) -print
git status --short --untracked-files=all
```

The final `find` command must print nothing for `src` generated remnants. If tests recreate caches, delete them and rerun only the generated-artifact check.

## Static/security gate decision

- `omp doctor --strict` is the local static gate for CLI surface depth and placeholder detection.
- `source-parity --json` is the source-family gate for OMC-to-OMP implementation mapping.
- Markdown structure tests are the static gate for skill, command, agent, plan, workflow, hook, mission, and prompt surfaces.
- Full pytest is the regression gate for shared contracts.
- A security-sensitive cleanup must also check that `.env`, credentials, and provider outputs remain ignored.

## Public-surface and release-note rule

- Any cleanup that changes user-visible commands, skill bodies, agent prompts, or full-audit behavior must update README or project docs.
- Any cleanup that changes OMC parity status must update source-parity data or the relevant plan artifact.
- Any cleanup that removes a compatibility behavior must state whether the behavior was masking slop, obsolete OMC coupling, or an intentional breaking change.
- Any release note should mention only user-visible changes, not cache deletion.

## OMP-specific generated artifact examples

- Commit: `.github/prompts/omc-full-audit.prompt.md` because it is a reusable prompt.
- Commit: `.vscode/tasks.json` because it is a shared validation task list.
- Commit: `.omp/plans/source-overall-cleanup/*.md` because these are shared plans.
- Ignore/delete: `src/**/__pycache__`, `src/**/*.pyc`, `src/oh_my_copilot.egg-info`.
- Ignore: `.omp/artifacts/**` unless a future ADR explicitly promotes a deterministic artifact to source.
