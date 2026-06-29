# Sandbox

Use this sandbox for Markdown skill and command parity checks.

## Checks

```bash
.venv/bin/python -m pytest tests/unit/skills/test_markdown_skill_bodies.py -q
.venv/bin/python -m pytest tests/unit/skills/test_markdown_commands.py -q
```

If OMC adds or removes public surfaces, update the tests first, then update `skills/`, `commands/`, `README.md`, and `MANIFEST.in`.