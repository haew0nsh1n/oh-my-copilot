"""Tests for brainstorming skill - TDD approach."""

import pytest
from skills import BrainstormingSkill
from domain import BrainstormSession, BrainstormIdea, IdeaStatus, BrainstormOutcome


class TestBrainstormingSkillCreation:
    """Test creating and initializing the brainstorming skill."""
    
    def test_skill_can_be_created(self):
        """RED: BrainstormingSkill can be instantiated."""
        skill = BrainstormingSkill()
        assert skill is not None
    
    def test_skill_has_name(self):
        """RED: Skill has a descriptive name."""
        skill = BrainstormingSkill()
        assert skill.name == "brainstorming"
    
    def test_skill_has_description(self):
        """RED: Skill has a description."""
        skill = BrainstormingSkill()
        assert skill.description is not None
        assert len(skill.description) > 0


class TestSessionCreation:
    """Test creating brainstorm sessions."""
    
    def test_create_session_with_prompt(self, brainstorm_context):
        """RED: Can create a session with a prompt."""
        skill = BrainstormingSkill()
        prompt = "Design the architecture for agent skill system"
        
        session = skill.create_session(prompt, context=brainstorm_context)
        
        assert session.prompt == prompt
        assert session.context == brainstorm_context
        assert len(session.ideas) == 0
    
    def test_create_session_without_context(self):
        """RED: Can create session without context."""
        skill = BrainstormingSkill()
        
        session = skill.create_session("Some prompt")
        
        assert session.context == {}


class TestAddingIdeas:
    """Test adding ideas to a session."""
    
    def test_add_idea_to_session(self):
        """RED: Can add an idea to session."""
        skill = BrainstormingSkill()
        session = skill.create_session("Design architecture")
        
        idea = skill.add_idea(
            session,
            title="Modular design",
            description="Use deep modules with simple interfaces"
        )
        
        assert idea in session.ideas
        assert idea.title == "Modular design"
        assert idea.status == IdeaStatus.PROPOSED
    
    def test_add_multiple_ideas(self):
        """RED: Can add multiple ideas to a session."""
        skill = BrainstormingSkill()
        session = skill.create_session("Design architecture")
        
        idea1 = skill.add_idea(session, "Modular", "Modular approach")
        idea2 = skill.add_idea(session, "Layered", "Layered approach")
        
        assert len(session.ideas) == 2
        assert idea1 in session.ideas
        assert idea2 in session.ideas


class TestSelectingIdea:
    """Test selecting the best idea."""
    
    def test_select_idea_in_session(self):
        """RED: Can select an idea in session."""
        skill = BrainstormingSkill()
        session = skill.create_session("Design")
        idea = skill.add_idea(session, "Best approach", "This is the best")
        
        session.select_idea(idea)
        
        assert session.selected_idea == idea
        assert idea.status == IdeaStatus.SELECTED
    
    def test_cannot_select_idea_not_in_session(self):
        """RED: Cannot select idea not in session."""
        skill = BrainstormingSkill()
        session = skill.create_session("Design")
        other_idea = BrainstormIdea(title="Other", description="Not in session")
        
        with pytest.raises(ValueError, match="not part of this session"):
            session.select_idea(other_idea)


class TestBrainstormOutcome:
    """Test creating brainstorm outcomes."""
    
    def test_generate_outcome_with_selected_idea(self):
        """RED: Can generate outcome from session with selected idea."""
        skill = BrainstormingSkill()
        session = skill.create_session("Design architecture")
        idea = skill.add_idea(session, "Modular", "Use modular design")
        idea.rationale = "Reduces complexity and improves testability"
        session.select_idea(idea)
        
        outcome = skill.select_best_idea(session)
        
        assert outcome.session == session
        assert outcome.selected_title == "Modular"
        assert outcome.ideas_count == 1
        assert outcome.rationale == "Reduces complexity and improves testability"
    
    def test_cannot_generate_outcome_without_selection(self):
        """RED: Cannot generate outcome without selecting an idea."""
        skill = BrainstormingSkill()
        session = skill.create_session("Design")
        skill.add_idea(session, "Idea 1", "Description 1")
        
        with pytest.raises(ValueError, match="No idea selected"):
            skill.select_best_idea(session)
    
    def test_outcome_tracks_idea_count(self):
        """RED: Outcome tracks number of ideas explored."""
        skill = BrainstormingSkill()
        session = skill.create_session("Design")
        
        idea1 = skill.add_idea(session, "Option A", "Description A")
        idea2 = skill.add_idea(session, "Option B", "Description B")
        idea3 = skill.add_idea(session, "Option C", "Description C")
        
        session.select_idea(idea1)
        outcome = skill.select_best_idea(session)
        
        assert outcome.ideas_count == 3
