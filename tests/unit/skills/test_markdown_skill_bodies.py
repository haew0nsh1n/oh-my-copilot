"""Tests for OMC-style markdown skill bodies."""

from pathlib import Path
import tomllib


OMC_PUBLIC_SKILLS = {
    "ai-slop-cleaner",
    "ask",
    "autopilot",
    "autoresearch",
    "cancel",
    "ccg",
    "configure-notifications",
    "debug",
    "deep-dive",
    "deep-interview",
    "deepinit",
    "external-context",
    "hud",
    "learner",
    "local-build-reminder",
    "mcp-setup",
    "omc-doctor",
    "omc-reference",
    "omc-setup",
    "omc-teams",
    "plan",
    "project-session-manager",
    "ralph",
    "ralplan",
    "release",
    "remember",
    "sciomc",
    "self-improve",
    "setup",
    "skill",
    "skillify",
    "team",
    "trace",
    "ultragoal",
    "ultraqa",
    "ultrawork",
    "verify",
    "visual-verdict",
    "wiki",
    "writer-memory",
}


def test_each_python_skill_has_markdown_skill_body():
    """Every product skill module has a matching root-level OMC-style SKILL.md body."""
    python_skills_root = Path("src/skills")
    markdown_skills_root = Path("skills")
    skill_modules = sorted(
        path.stem
        for path in python_skills_root.glob("*.py")
        if path.name != "__init__.py" and not path.name.startswith("_")
    )

    assert len(skill_modules) == 34

    for module_name in skill_modules:
        skill_body = markdown_skills_root / module_name.replace("_", "-") / "SKILL.md"
        assert skill_body.exists(), f"Missing markdown body for {module_name}"
        content = skill_body.read_text(encoding="utf-8")
        assert content.startswith("---\n"), f"Missing frontmatter for {module_name}"
        assert "name:" in content, f"Missing name frontmatter for {module_name}"
        assert "description:" in content, f"Missing description frontmatter for {module_name}"
        assert "# " in content, f"Missing heading for {module_name}"


def test_markdown_skill_bodies_are_not_nested_inside_python_package():
    """OMC-style Markdown skill bodies live in the repository-root skills directory."""
    nested_bodies = list(Path("src/skills").glob("*/SKILL.md"))

    assert nested_bodies == []


def test_markdown_skill_bodies_are_included_in_source_distribution():
    """Root-level Markdown skill bodies are included in source distributions."""
    manifest = Path("MANIFEST.in")

    assert manifest.exists()
    assert "recursive-include skills SKILL.md" in manifest.read_text(encoding="utf-8")


def test_omc_public_markdown_skill_surface_is_present():
    """Root skills include OMC-compatible public Markdown skill names."""
    local_skills = {
        path.parent.name
        for path in Path("skills").glob("*/SKILL.md")
    }

    assert OMC_PUBLIC_SKILLS <= local_skills