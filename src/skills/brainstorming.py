"""Brainstorming skill for idea generation and exploration."""

from typing import List
from domain import BrainstormSession, BrainstormIdea, BrainstormOutcome


class BrainstormingSkill:
    """
    A skill for conducting brainstorming sessions.
    
    This skill helps explore multiple ideas around a given prompt,
    compare their merits, and select the best approach.
    """
    
    def __init__(self):
        """Initialize the brainstorming skill."""
        self.name = "brainstorming"
        self.description = "Generate and explore multiple ideas around a prompt"
    
    def create_session(self, prompt: str, context: dict | None = None) -> BrainstormSession:
        """
        Create a new brainstorming session.
        
        Args:
            prompt: The brainstorming prompt
            context: Optional execution context
            
        Returns:
            A new BrainstormSession
        """
        return BrainstormSession(
            prompt=prompt,
            context=context or {}
        )
    
    def add_idea(self, session: BrainstormSession, title: str, description: str) -> BrainstormIdea:
        """
        Add a new idea to the session.
        
        Args:
            session: The brainstorm session
            title: Short title of the idea
            description: Detailed description
            
        Returns:
            The created BrainstormIdea
        """
        idea = BrainstormIdea(title=title, description=description)
        session.add_idea(idea)
        return idea
    
    def select_best_idea(self, session: BrainstormSession) -> BrainstormOutcome:
        """
        Finalize the session by selecting the best idea.
        
        Args:
            session: The brainstorm session to finalize
            
        Returns:
            A BrainstormOutcome with the selected idea
        """
        if not session.selected_idea:
            raise ValueError("No idea selected. Call select_idea() first.")
        
        selected = session.selected_idea
        outcome = BrainstormOutcome(
            session=session,
            ideas_count=len(session.ideas),
            selected_title=selected.title,
            rationale=selected.rationale,
            next_steps=[]
        )
        return outcome
