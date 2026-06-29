# Generated Artifact Policy - OMP Source-Overall Cleanup

OMP keeps generated and local runtime artifacts out of source control by default.

## Commit as source

- Root Markdown surfaces: `skills/*/SKILL.md`, `commands/*.md`, `agents/*.md`.
- Compatibility templates: `hooks/hooks.json`, `templates/hooks/*.mjs`.
- Source distribution manifest: `MANIFEST.in`.
- Benchmark compatibility sources under `benchmark/` and `benchmarks/`.

## Do not commit as source

- `.omp/state/**`, `.omp/artifacts/**`, `.omp/sessions/**`, except explicitly shared `.omp/skills/**`.
- Python caches, coverage outputs, virtual environments, and build outputs.

## Verification

Run these checks after source cleanup work:

```bash
.venv/bin/python -m pytest -q
omp doctor --strict
python benchmark/quick_test.py
python bridge/omp-bridge.py status
```
