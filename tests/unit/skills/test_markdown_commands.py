"""Tests for OMC-compatible root command bodies."""

from pathlib import Path


OMC_PUBLIC_COMMANDS = {
    "ask",
    "autoresearch",
    "ccg",
    "compact",
    "configure-notifications",
    "debug",
    "deep-dive",
    "deepinit",
    "external-context",
    "hud",
    "learner",
    "mcp-setup",
    "omc-doctor",
    "omc-setup",
    "omc-teams",
    "project-session-manager",
    "psm",
    "release",
    "remember",
    "sciomc",
    "self-improve",
    "skill",
    "skillify",
    "trace",
    "verify",
    "visual-verdict",
    "wiki",
    "writer-memory",
}


def test_omc_public_command_markdown_surface_is_present():
    """Root commands include OMC-compatible public command names."""
    local_commands = {
        path.stem
        for path in Path("commands").glob("*.md")
    }

    assert OMC_PUBLIC_COMMANDS <= local_commands


def test_omc_public_commands_dispatch_to_matching_skills():
    """Compatibility commands dispatch to root skills without embedding long instructions."""
    for command_name in OMC_PUBLIC_COMMANDS:
        command_file = Path("commands") / f"{command_name}.md"
        content = command_file.read_text(encoding="utf-8")
        if command_name == "compact":
            assert "native /compact" in content
            assert "$ARGUMENTS" in content
            continue
        skill_name = "project-session-manager" if command_name == "psm" else command_name
        assert content.startswith("---\n"), command_name
        assert f"skills/{skill_name}/SKILL.md" in content, command_name
        assert "$ARGUMENTS" in content, command_name


def test_root_commands_are_included_in_source_distribution():
    """Root command Markdown bodies are included in source distributions."""
    manifest = Path("MANIFEST.in")

    assert manifest.exists()
    assert "recursive-include commands *.md" in manifest.read_text(encoding="utf-8")