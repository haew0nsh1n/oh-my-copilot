"""Tests for design skill."""
import pytest
from skills import DesignSkill
from domain import DesignSectionType


class TestDesignBasics:
    def test_skill_created(self):
        assert DesignSkill().name == "design"

    def test_create_document(self):
        skill = DesignSkill()
        doc = skill.create_document("AuthService")
        assert doc.project_name == "AuthService"
        assert len(doc.sections) == 0

    def test_empty_project_raises(self):
        with pytest.raises(ValueError):
            DesignSkill().create_document("")


class TestSections:
    def test_add_section(self):
        skill = DesignSkill()
        doc = skill.create_document("Project")
        section = skill.add_section(doc, "Architecture", DesignSectionType.ARCHITECTURE, "System overview")
        assert section.title == "Architecture"
        assert len(doc.sections) == 1

    def test_get_section(self):
        skill = DesignSkill()
        doc = skill.create_document("Project")
        skill.add_section(doc, "Overview", DesignSectionType.OVERVIEW, "Content here")
        section = skill.get_section(doc, "Overview")
        assert section is not None
        assert section.content == "Content here"

    def test_get_missing_section(self):
        skill = DesignSkill()
        doc = skill.create_document("Project")
        assert skill.get_section(doc, "Missing") is None

    def test_update_section(self):
        skill = DesignSkill()
        doc = skill.create_document("Project")
        skill.add_section(doc, "API", DesignSectionType.API, "Old content")
        result = skill.update_section(doc, "API", "New content")
        assert result is True
        section = skill.get_section(doc, "API")
        assert section.content == "New content"

    def test_update_missing_returns_false(self):
        skill = DesignSkill()
        doc = skill.create_document("Project")
        result = skill.update_section(doc, "Missing", "Content")
        assert result is False


class TestMarkdown:
    def test_to_markdown(self):
        skill = DesignSkill()
        doc = skill.create_document("MyProject")
        skill.add_section(doc, "Overview", DesignSectionType.OVERVIEW, "This is the overview.")
        md = skill.to_markdown(doc)
        assert "# MyProject" in md
        assert "## Overview" in md
        assert "This is the overview." in md


class TestDesignReport:
    def test_generate_report(self):
        skill = DesignSkill()
        doc = skill.create_document("Project")
        skill.add_section(doc, "Architecture", DesignSectionType.ARCHITECTURE, "Arch content")
        skill.add_section(doc, "Decisions", DesignSectionType.DECISIONS, "Decision log")
        report = skill.generate_report(doc)
        assert report.sections_count == 2
        assert report.has_architecture
        assert report.has_decisions
