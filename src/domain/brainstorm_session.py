"""Domain model for brainstorming sessions."""

from dataclasses import dataclass, field
from typing import List
from enum import Enum


class IdeaStatus(str, Enum):
    """Status of an idea in a brainstorm session."""
    PROPOSED = "proposed"
    EXPLORED = "explored"
    SELECTED = "selected"
    REJECTED = "rejected"


@dataclass
class BrainstormIdea:
    """A single idea proposed during a brainstorm session."""
    
    title: str
    description: str
    rationale: str = ""
    status: IdeaStatus = IdeaStatus.PROPOSED
    metadata: dict = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate idea on creation."""
        if not self.title or not self.title.strip():
            raise ValueError("Idea title cannot be empty")
        if not self.description or not self.description.strip():
            raise ValueError("Idea description cannot be empty")


@dataclass
class BrainstormSession:
    """A brainstorming session with multiple ideas and outcomes."""
    
    prompt: str
    ideas: List[BrainstormIdea] = field(default_factory=list)
    selected_idea: BrainstormIdea | None = None
    context: dict = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate session on creation."""
        if not self.prompt or not self.prompt.strip():
            raise ValueError("Prompt cannot be empty")
    
    def add_idea(self, idea: BrainstormIdea) -> None:
        """Add an idea to the session."""
        if idea in self.ideas:
            raise ValueError("Idea already exists in session")
        self.ideas.append(idea)
    
    def select_idea(self, idea: BrainstormIdea) -> None:
        """Mark an idea as selected."""
        if idea not in self.ideas:
            raise ValueError("Idea is not part of this session")
        self.selected_idea = idea
        idea.status = IdeaStatus.SELECTED
    
    def get_selected_idea(self) -> BrainstormIdea:
        """Get the selected idea."""
        if self.selected_idea is None:
            raise ValueError("No idea has been selected yet")
        return self.selected_idea


@dataclass
class BrainstormOutcome:
    """The outcome of a brainstorm session."""
    
    session: BrainstormSession
    ideas_count: int
    selected_title: str
    rationale: str
    next_steps: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate outcome on creation."""
        if self.ideas_count <= 0:
            raise ValueError("Ideas count must be positive")
        if not self.selected_title or not self.selected_title.strip():
            raise ValueError("Selected title cannot be empty")
