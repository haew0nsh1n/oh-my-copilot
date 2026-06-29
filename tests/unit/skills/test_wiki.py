"""Tests for wiki skill."""

import pytest
from skills import WikiSkill
from domain import WikiPageStatus


class TestWikiSkillBasics:
    """Test basic wiki skill functionality."""
    
    def test_skill_can_be_created(self):
        """RED: Skill can be instantiated."""
        skill = WikiSkill()
        assert skill is not None
    
    def test_skill_has_name(self):
        """RED: Skill has a name."""
        skill = WikiSkill()
        assert skill.name == "wiki"


class TestPageCreation:
    """Test page creation."""
    
    def test_create_page(self):
        """RED: Can create a wiki page."""
        skill = WikiSkill()
        page = skill.create_page(
            "Authentication Patterns",
            "# Authentication\n\nUse OAuth2 for external users.",
            category="patterns",
            author="Alice"
        )
        assert page.title == "Authentication Patterns"
        assert page.category == "patterns"
        assert page.author == "Alice"
    
    def test_add_page_to_wiki(self):
        """RED: Can add page to wiki."""
        skill = WikiSkill()
        page = skill.create_page("Topic", "Content", category="tech")
        skill.add_page(page)
        
        retrieved = skill.get_page("Topic")
        assert retrieved.title == "Topic"


class TestPageManagement:
    """Test page management."""
    
    def test_publish_page(self):
        """RED: Can publish a page."""
        skill = WikiSkill()
        page = skill.create_page("Page", "Content")
        assert page.status == WikiPageStatus.DRAFT
        
        skill.publish_page(page)
        assert page.status == WikiPageStatus.PUBLISHED
    
    def test_archive_page(self):
        """RED: Can archive a page."""
        skill = WikiSkill()
        page = skill.create_page("Page", "Content")
        skill.publish_page(page)
        
        skill.archive_page(page)
        assert page.status == WikiPageStatus.ARCHIVED
    
    def test_add_tags(self):
        """RED: Can add tags to pages."""
        skill = WikiSkill()
        page = skill.create_page("Page", "Content")
        
        skill.add_tag_to_page(page, "important")
        skill.add_tag_to_page(page, "security")
        
        assert len(page.tags) == 2


class TestSearch:
    """Test search functionality."""
    
    def test_search_by_title(self):
        """RED: Can search by title."""
        skill = WikiSkill()
        page1 = skill.create_page("Authentication Flow", "Content 1")
        page2 = skill.create_page("Authorization Setup", "Content 2")
        page3 = skill.create_page("User Management", "Content 3")
        
        skill.add_page(page1)
        skill.add_page(page2)
        skill.add_page(page3)
        
        results = skill.search_by_title("Auth")
        assert len(results) == 2
    
    def test_search_by_category(self):
        """RED: Can search by category."""
        skill = WikiSkill()
        page1 = skill.create_page("Page 1", "Content", category="patterns")
        page2 = skill.create_page("Page 2", "Content", category="patterns")
        page3 = skill.create_page("Page 3", "Content", category="howto")
        
        skill.add_page(page1)
        skill.add_page(page2)
        skill.add_page(page3)
        
        results = skill.search_by_category("patterns")
        assert len(results) == 2
    
    def test_search_by_tag(self):
        """RED: Can search by tag."""
        skill = WikiSkill()
        page1 = skill.create_page("Page 1", "Content")
        page2 = skill.create_page("Page 2", "Content")
        page3 = skill.create_page("Page 3", "Content")
        
        skill.add_page(page1)
        skill.add_page(page2)
        skill.add_page(page3)
        
        skill.add_tag_to_page(page1, "security")
        skill.add_tag_to_page(page2, "security")
        
        results = skill.search_by_tag("security")
        assert len(results) == 2


class TestMetadata:
    """Test metadata and organization."""
    
    def test_get_categories(self):
        """RED: Can get all categories."""
        skill = WikiSkill()
        page1 = skill.create_page("Page 1", "Content", category="patterns")
        page2 = skill.create_page("Page 2", "Content", category="howto")
        
        skill.add_page(page1)
        skill.add_page(page2)
        
        categories = skill.get_categories()
        assert "patterns" in categories
        assert "howto" in categories
    
    def test_get_tags(self):
        """RED: Can get all tags."""
        skill = WikiSkill()
        page = skill.create_page("Page", "Content")
        skill.add_page(page)
        
        skill.add_tag_to_page(page, "important")
        skill.add_tag_to_page(page, "security")
        
        tags = skill.get_tags()
        assert "important" in tags
        assert "security" in tags


class TestPublishedPages:
    """Test published pages."""
    
    def test_get_published_pages(self):
        """RED: Can get published pages."""
        skill = WikiSkill()
        page1 = skill.create_page("Page 1", "Content")
        page2 = skill.create_page("Page 2", "Content")
        
        skill.add_page(page1)
        skill.add_page(page2)
        
        skill.publish_page(page1)
        
        published = skill.get_published_pages()
        assert len(published) == 1
        assert published[0].title == "Page 1"
