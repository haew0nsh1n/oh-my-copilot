"""Domain model for best practice research."""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime


class PracticeCategory(str, Enum):
    """Category of best practice."""
    ARCHITECTURE = "architecture"
    SECURITY = "security"
    PERFORMANCE = "performance"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    CODE_QUALITY = "code_quality"
    DEPLOYMENT = "deployment"
    MONITORING = "monitoring"


class EvidenceSource(str, Enum):
    """Official sources for evidence."""
    OFFICIAL_DOCS = "official_docs"
    RFC = "rfc"
    SPEC = "spec"
    PAPER = "paper"
    INDUSTRY_REPORT = "industry_report"
    FRAMEWORK_GUIDE = "framework_guide"


@dataclass
class BestPractice:
    """A documented best practice."""
    title: str
    category: PracticeCategory
    description: str
    rationale: str
    source: EvidenceSource
    source_url: str = ""
    adoption_level: int = 0  # 0-100: how widely adopted
    impact_score: int = 0  # 0-100: impact on quality
    examples: List[str] = field(default_factory=list)
    counter_examples: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    discovered_at: datetime = field(default_factory=datetime.now)


@dataclass
class PracticeEvidence:
    """Evidence supporting a practice."""
    practice: BestPractice
    finding: str
    verified: bool = False
    verification_source: str = ""
    verification_date: Optional[datetime] = None


@dataclass
class BestPracticeLibrary:
    """Library of best practices."""
    practices: Dict[str, BestPractice] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    
    def add_practice(self, practice: BestPractice) -> None:
        """Add a practice to the library."""
        self.practices[practice.title] = practice
        self.last_updated = datetime.now()
    
    def get_practice(self, title: str) -> Optional[BestPractice]:
        """Get a practice by title."""
        return self.practices.get(title)
    
    def get_by_category(self, category: PracticeCategory) -> List[BestPractice]:
        """Get practices by category."""
        return [
            p for p in self.practices.values()
            if p.category == category
        ]
    
    def get_by_source(self, source: EvidenceSource) -> List[BestPractice]:
        """Get practices by source."""
        return [
            p for p in self.practices.values()
            if p.source == source
        ]
    
    def get_high_impact_practices(self, threshold: int = 70) -> List[BestPractice]:
        """Get high-impact practices."""
        return [
            p for p in self.practices.values()
            if p.impact_score >= threshold
        ]
    
    def get_widely_adopted_practices(self, threshold: int = 70) -> List[BestPractice]:
        """Get widely adopted practices."""
        return [
            p for p in self.practices.values()
            if p.adoption_level >= threshold
        ]
