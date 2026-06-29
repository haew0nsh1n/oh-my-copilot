"""Wiki skill for knowledge management."""

from typing import List
from domain import (
    WikiPage,
    WikiIndex,
    WikiPageStatus,
)


class WikiSkill:
    """
    A skill for managing project knowledge as wiki pages.
    
    This skill helps store, organize, and retrieve project documentation,
    decisions, patterns, and lessons learned.
    """
    
    def __init__(self):
        """Initialize the wiki skill."""
        self.name = "wiki"
        self.description = "Store and manage project knowledge as wiki pages"
        self.index = WikiIndex()
    
    def create_page(
        self,
        title: str,
        content: str,
        category: str = "general",
        author: str = ""
    ) -> WikiPage:
        """
        Create a new wiki page.
        
        Args:
            title: Page title
            content: Page content (markdown)
            category: Page category
            author: Page author
            
        Returns:
            A new WikiPage
        """
        page = WikiPage(
            title=title,
            content=content,
            category=category,
            author=author
        )
        return page
    
    def add_page(self, page: WikiPage) -> None:
        """
        Add a page to the wiki.
        
        Args:
            page: The page to add
        """
        self.index.add_page(page)
    
    def publish_page(self, page: WikiPage) -> None:
        """
        Publish a page.
        
        Args:
            page: The page to publish
        """
        page.publish()
    
    def archive_page(self, page: WikiPage) -> None:
        """
        Archive a page.
        
        Args:
            page: The page to archive
        """
        page.archive()
    
    def get_page(self, title: str) -> WikiPage:
        """
        Get a page by title.
        
        Args:
            title: Page title
            
        Returns:
            The WikiPage or None
        """
        return self.index.get_page(title)
    
    def add_tag_to_page(self, page: WikiPage, tag: str) -> None:
        """
        Add a tag to a page.
        
        Args:
            page: The page
            tag: The tag to add
        """
        page.add_tag(tag)
        # Update the index with the new tag
        self.index.update_page_tags_index(page)
    
    def add_reference_to_page(
        self,
        page: WikiPage,
        reference: str
    ) -> None:
        """
        Add a reference to another page.
        
        Args:
            page: The page
            reference: Reference to another page
        """
        page.add_reference(reference)
    
    def add_related_topic_to_page(
        self,
        page: WikiPage,
        topic: str
    ) -> None:
        """
        Add a related topic.
        
        Args:
            page: The page
            topic: Related topic
        """
        page.add_related_topic(topic)
    
    def search_by_title(self, query: str) -> List[WikiPage]:
        """
        Search pages by title.
        
        Args:
            query: Search query
            
        Returns:
            Matching WikiPages
        """
        return self.index.search_by_title(query)
    
    def search_by_tag(self, tag: str) -> List[WikiPage]:
        """
        Search pages by tag.
        
        Args:
            tag: Tag to search
            
        Returns:
            Matching WikiPages
        """
        return self.index.search_by_tag(tag)
    
    def search_by_category(self, category: str) -> List[WikiPage]:
        """
        Search pages by category.
        
        Args:
            category: Category to search
            
        Returns:
            Matching WikiPages
        """
        return self.index.search_by_category(category)
    
    def get_published_pages(self) -> List[WikiPage]:
        """
        Get all published pages.
        
        Returns:
            List of published WikiPages
        """
        return self.index.get_published_pages()
    
    def get_all_pages(self) -> List[WikiPage]:
        """
        Get all pages.
        
        Returns:
            All WikiPages
        """
        return list(self.index.pages.values())
    
    def get_categories(self) -> List[str]:
        """
        Get all categories.
        
        Returns:
            List of category names
        """
        return list(self.index.categories.keys())
    
    def get_tags(self) -> List[str]:
        """
        Get all tags.
        
        Returns:
            List of tag names
        """
        return list(self.index.tags.keys())
