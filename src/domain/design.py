"""Domain model for design documentation management."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime


class DesignSectionType(str, Enum):
    OVERVIEW = "overview"
    ARCHITECTURE = "architecture"
    API = "api"
    DATA_MODEL = "data_model"
    DECISIONS = "decisions"
    DIAGRAMS = "diagrams"
    OPEN_QUESTIONS = "open_questions"


@dataclass
class DesignSection:
    title: str
    section_type: DesignSectionType
    content: str = ""
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class DesignDocument:
    """Represents DESIGN.md — kept in repo root."""
    project_name: str
    sections: List[DesignSection] = field(default_factory=list)
    last_updated: datetime = field(default_factory=datetime.now)
    version: str = "0.1.0"

    def __post_init__(self):
        if not self.project_name or not self.project_name.strip():
            raise ValueError("Project name cannot be empty")

    def add_section(self, section: DesignSection) -> None:
        self.sections.append(section)
        self.last_updated = datetime.now()

    def get_section(self, title: str) -> Optional[DesignSection]:
        for s in self.sections:
            if s.title.lower() == title.lower():
                return s
        return None

    def update_section(self, title: str, content: str) -> bool:
        section = self.get_section(title)
        if section:
            section.content = content
            section.updated_at = datetime.now()
            self.last_updated = datetime.now()
            return True
        return False

    def to_markdown(self) -> str:
        lines = [f"# {self.project_name} — Design", ""]
        for section in self.sections:
            lines.append(f"## {section.title}")
            lines.append(section.content)
            lines.append("")
        return "\n".join(lines)


@dataclass
class DesignReport:
    project_name: str
    sections_count: int = 0
    last_updated: Optional[datetime] = None
    has_architecture: bool = False
    has_decisions: bool = False
    summary: str = ""
