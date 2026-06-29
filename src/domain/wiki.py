"""Domain model for wiki and knowledge management."""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime


class WikiPageStatus(str, Enum):
    """Status of a wiki page."""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"


@dataclass
class WikiPage:
    """A wiki page for knowledge storage."""
    title: str
    content: str
    category: str = "general"
    tags: List[str] = field(default_factory=list)
    status: WikiPageStatus = WikiPageStatus.DRAFT
    author: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    references: List[str] = field(default_factory=list)  # Links to other pages
    related_topics: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate page."""
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")
        if not self.content or not self.content.strip():
            raise ValueError("Content cannot be empty")
    
    def add_tag(self, tag: str) -> None:
        """Add a tag."""
        if tag not in self.tags:
            self.tags.append(tag)
    
    def add_reference(self, reference: str) -> None:
        """Add a reference to another page."""
        if reference not in self.references:
            self.references.append(reference)
    
    def add_related_topic(self, topic: str) -> None:
        """Add a related topic."""
        if topic not in self.related_topics:
            self.related_topics.append(topic)
    
    def publish(self) -> None:
        """Publish the page."""
        self.status = WikiPageStatus.PUBLISHED
        self.updated_at = datetime.now()
    
    def archive(self) -> None:
        """Archive the page."""
        self.status = WikiPageStatus.ARCHIVED
        self.updated_at = datetime.now()


@dataclass
class WikiIndex:
    """Index of wiki pages for search."""
    pages: Dict[str, WikiPage] = field(default_factory=dict)
    categories: Dict[str, List[str]] = field(default_factory=dict)  # category -> page titles
    tags: Dict[str, List[str]] = field(default_factory=dict)  # tag -> page titles
    created_at: datetime = field(default_factory=datetime.now)
    
    def add_page(self, page: WikiPage) -> None:
        """Add a page to the index."""
        self.pages[page.title] = page
        
        # Add to category
        if page.category not in self.categories:
            self.categories[page.category] = []
        if page.title not in self.categories[page.category]:
            self.categories[page.category].append(page.title)
        
        # Add to tags
        for tag in page.tags:
            if tag not in self.tags:
                self.tags[tag] = []
            if page.title not in self.tags[tag]:
                self.tags[tag].append(page.title)
    
    def update_page_tags_index(self, page: WikiPage) -> None:
        """Update the tags index for a page (used when tags are added after page creation)."""
        for tag in page.tags:
            if tag not in self.tags:
                self.tags[tag] = []
            if page.title not in self.tags[tag]:
                self.tags[tag].append(page.title)
    
    def get_page(self, title: str) -> Optional[WikiPage]:
        """Get a page by title."""
        return self.pages.get(title)
    
    def search_by_title(self, query: str) -> List[WikiPage]:
        """Search pages by title."""
        results = []
        query_lower = query.lower()
        for page in self.pages.values():
            if query_lower in page.title.lower():
                results.append(page)
        return results
    
    def search_by_tag(self, tag: str) -> List[WikiPage]:
        """Search pages by tag."""
        if tag not in self.tags:
            return []
        page_titles = self.tags[tag]
        return [self.pages[title] for title in page_titles]
    
    def search_by_category(self, category: str) -> List[WikiPage]:
        """Search pages by category."""
        if category not in self.categories:
            return []
        page_titles = self.categories[category]
        return [self.pages[title] for title in page_titles]
    
    def get_published_pages(self) -> List[WikiPage]:
        """Get all published pages."""
        return [p for p in self.pages.values() if p.status == WikiPageStatus.PUBLISHED]
