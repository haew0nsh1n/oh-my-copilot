# First Safe Cleanup Batch: Behavior-Locked Fallback Resolution

This OMP plan mirrors the OMC first-safe-cleanup-batch method: choose one low-risk batch, lock behavior first, edit second, and stop immediately when validation changes meaning.

The batch is intentionally conservative. It exists to prevent “cleanup” from becoming silent parity regression.

## Scope and stop rule

- Scope: generated source artifacts, markdown parity depth, CLI placeholder-like behavior, and source-parity reporting.
- Do not edit unrelated lanes in the same batch.
- Stop after the first failed validation that changes understanding of the behavior.
- Stop if an OMC reference behavior is unclear and capture the missing comparison as a gap.
- Stop if a cleanup would remove a compatibility fallback without a replacement test.
- Do not use `git reset --hard`, `git checkout --`, or destructive cleanup to hide failures.

## Batch objective

- Keep source trees free of generated artifacts.
- Ensure OMP markdown files mirror OMC method and instruction depth, not only filenames.
- Ensure `source-parity` reports implementation/adaptation/partial/gap status with mapped OMP source paths.
- Ensure strict doctor distinguishes executable, artifact, state, external, and placeholder surfaces.
- Make autopilot/full-audit prompts require full-surface evidence before completion.

## Target file ownership for this batch

| Target | Owner | Edit type | Required lock |
| --- | --- | --- | --- |
| `src/` generated artifacts | executor/verifier | deletion only | full pytest plus no generated remnants |
| `skills/*/SKILL.md` | writer/verifier | instruction depth | markdown skill tests |
| `commands/*.md` | writer/verifier | wrapper depth | markdown command tests |
| `agents/*.md` | writer/verifier | prompt depth | structure parity tests |
| `.github/prompts/*.prompt.md` | planner/verifier | workflow guidance | Copilot workflow tests |
| `.omp/plans/source-overall-cleanup/*.md` | planner/verifier | OMC-method parity | structure parity tests |
| `src/domain/source_parity.py` | architect/test-engineer | domain contract | source parity tests |

## Existing behavior locks to run before editing

```bash
.venv/bin/python -m pytest tests/unit/test_copilot_native_workflow.py -q
.venv/bin/python -m pytest tests/unit/test_omc_structure_parity.py -q
.venv/bin/python -m pytest tests/unit/skills/test_markdown_skill_bodies.py tests/unit/skills/test_markdown_commands.py -q
.venv/bin/python -m pytest tests/unit/skills/test_source_parity.py -q
.venv/bin/python -m cli source-parity --json
.venv/bin/python -m cli doctor --strict
```

## Tests to add before cleanup edits

- Add a structure test before changing any shared markdown surface shape.
- Add a CLI test before changing a command route, alias, output, state write, or artifact write.
- Add a domain test before changing source-parity status, source path mapping, or count logic.
- Add a core test before changing provider runtime, bridge, session recorder, or websocket helpers.
- Add a documentation contract test when autopilot instructions, full-audit prompts, or completion policy changes.

## Source-contract change rules

- Domain objects must keep stable public contracts through dataclasses/enums.
- Skills orchestrate domain models and should not duplicate CLI output rules.
- CLI remains a thin adapter and should not own domain invariants.
- Core owns runtime integration only.
- Markdown root surfaces are product surfaces and must stay OMC-style enough for agent use.
- A file may be moved from OMC `.omx` naming to OMP `.omp` only when contents and tests explain the translation.

## Recommended first implementation order

1. Remove generated `src` artifacts and prove no source modules are unreferenced.
2. Expand skill, agent, and command markdown bodies to OMC-style depth while preserving OMP terminology.
3. Add source-parity reporting for OMC runtime families and mapped OMP source paths.
4. Strengthen autopilot/full-audit prompt and completion policy to prevent early stops.
5. Expand `.omp/plans/source-overall-cleanup` to mirror the OMC reference method and sections.
6. Run the full-surface audit manifest and record remaining gaps as partial/gap rather than pretending completion.

## Verification commands after edits

```bash
.venv/bin/python -m cli source-parity --json
.venv/bin/python -m cli doctor --strict
.venv/bin/python -m cli skills
.venv/bin/python -m cli agents
.venv/bin/python -m pytest tests/unit/skills/test_markdown_skill_bodies.py tests/unit/skills/test_markdown_commands.py tests/unit/test_omc_structure_parity.py -q
.venv/bin/python -m pytest -q
find src \( -type d -name '__pycache__' -o -type d -name '*.egg-info' -o -type f -name '*.pyc' \) -print
```

## Concrete source/test anchors used

- `tests/unit/test_omc_structure_parity.py` locks root OMC-compatible structures and cleanup plan shape.
- `tests/unit/test_copilot_native_workflow.py` locks autopilot/full-audit guidance and VS Code tasks.
- `tests/unit/skills/test_markdown_skill_bodies.py` locks root skill body depth.
- `tests/unit/skills/test_markdown_commands.py` locks command wrapper depth and dispatch targets.
- `tests/unit/skills/test_source_parity.py` locks source family counts, mapped OMP paths, and missing path reporting.
- `.github/prompts/omc-full-audit.prompt.md` is the default prompt for full-surface parity work.

## Exit criteria

- The first batch has no failing focused tests.
- Strict doctor reports operational with zero placeholders and zero external blocked local surfaces.
- Source-parity reports known family count and no missing mapped OMP source paths.
- Full pytest passes or unrelated failures are documented with evidence.
- Generated `src` artifacts are absent after validation.
