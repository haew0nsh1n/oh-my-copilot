"""Tests for autoresearch-goal skill."""

import pytest
from skills import AutoresearchGoalSkill
from domain import ResearchGoalStatus


class TestAutoresearchGoalBasics:
    """Test basic autoresearch-goal skill functionality."""
    
    def test_skill_can_be_created(self):
        """RED: Skill can be instantiated."""
        skill = AutoresearchGoalSkill()
        assert skill is not None
    
    def test_skill_has_name(self):
        """RED: Skill has a name."""
        skill = AutoresearchGoalSkill()
        assert skill.name == "autoresearch_goal"


class TestMissionCreation:
    """Test mission creation."""
    
    def test_create_mission(self):
        """RED: Can create a research mission."""
        skill = AutoresearchGoalSkill()
        
        mission = skill.create_research_mission(
            "OAuth2 Best Practices",
            "Research current OAuth2 security best practices",
            professor_prompt="Guide the research process",
            critic_prompt="Challenge assumptions"
        )
        
        assert mission.title == "OAuth2 Best Practices"
        assert mission.status == ResearchGoalStatus.STARTING
    
    def test_start_mission(self):
        """RED: Can start a mission."""
        skill = AutoresearchGoalSkill()
        mission = skill.create_research_mission("Mission", "Focus")
        
        skill.start_mission(mission)
        
        assert mission.status == ResearchGoalStatus.IN_PROGRESS


class TestFindings:
    """Test finding collection."""
    
    def test_add_finding(self):
        """RED: Can add findings."""
        skill = AutoresearchGoalSkill()
        mission = skill.create_research_mission("Mission", "Focus")
        
        skill.add_finding(mission, "OAuth2 RFC recommends refresh token rotation")
        
        assert mission.get_findings_count() == 1
    
    def test_multiple_findings(self):
        """RED: Can add multiple findings."""
        skill = AutoresearchGoalSkill()
        mission = skill.create_research_mission("Mission", "Focus")
        
        skill.add_finding(mission, "Finding 1")
        skill.add_finding(mission, "Finding 2")
        skill.add_finding(mission, "Finding 3")
        
        assert mission.get_findings_count() == 3


class TestValidation:
    """Test validation."""
    
    def test_validate_finding(self):
        """RED: Can validate findings."""
        skill = AutoresearchGoalSkill()
        mission = skill.create_research_mission("Mission", "Focus")
        
        skill.add_finding(mission, "Finding 1")
        skill.validate_finding(mission, "Validated by official docs")
        
        assert mission.get_validations_count() == 1
    
    def test_multiple_validations(self):
        """RED: Can add multiple validations."""
        skill = AutoresearchGoalSkill()
        mission = skill.create_research_mission("Mission", "Focus")
        
        skill.add_finding(mission, "Finding 1")
        skill.validate_finding(mission, "Validation 1")
        skill.validate_finding(mission, "Validation 2")
        
        assert mission.get_validations_count() == 2


class TestProfessorReview:
    """Test professor review."""
    
    def test_get_professor_review(self):
        """RED: Can get professor review."""
        skill = AutoresearchGoalSkill()
        mission = skill.create_research_mission("Mission", "Focus")
        
        review = skill.get_professor_review(
            mission,
            "Your research is on the right track",
            ["Explore more sources", "Validate findings"]
        )
        
        assert "right track" in review.guidance
        assert len(review.recommended_next_steps) == 2


class TestCriticReview:
    """Test critic review."""
    
    def test_get_critic_review(self):
        """RED: Can get critic review."""
        skill = AutoresearchGoalSkill()
        mission = skill.create_research_mission("Mission", "Focus")
        
        review = skill.get_critic_review(
            mission,
            challenges=["Need more official sources"],
            weaknesses=["Limited scope"]
        )
        
        assert len(review.challenges) == 1
        assert len(review.weaknesses) == 1


class TestCompletion:
    """Test research completion."""
    
    def test_is_research_sufficient(self):
        """RED: Can check if research is sufficient."""
        skill = AutoresearchGoalSkill()
        mission = skill.create_research_mission("Mission", "Focus")
        
        assert not skill.is_research_sufficient(mission)
        
        skill.add_finding(mission, "Finding 1")
        skill.validate_finding(mission, "Validation 1")
        
        assert skill.is_research_sufficient(mission)
    
    def test_complete_mission(self):
        """RED: Can complete mission."""
        skill = AutoresearchGoalSkill()
        mission = skill.create_research_mission("Mission", "Focus")
        
        skill.add_finding(mission, "Finding 1")
        skill.validate_finding(mission, "Validation 1")
        skill.complete_mission(mission)
        
        assert mission.status == ResearchGoalStatus.COMPLETED
        assert mission.is_complete()
    
    def test_fail_mission(self):
        """RED: Can fail mission."""
        skill = AutoresearchGoalSkill()
        mission = skill.create_research_mission("Mission", "Focus")
        
        skill.fail_mission(mission)
        
        assert mission.status == ResearchGoalStatus.FAILED


class TestReporting:
    """Test reporting."""
    
    def test_generate_report(self):
        """RED: Can generate report."""
        skill = AutoresearchGoalSkill()
        mission = skill.create_research_mission("Mission", "Focus")
        
        skill.add_finding(mission, "Finding 1")
        skill.add_finding(mission, "Finding 2")
        skill.validate_finding(mission, "Validation 1")
        skill.complete_mission(mission)
        
        report = skill.generate_report(mission)
        
        assert report.findings_count == 2
        assert report.validations_count == 1
        assert report.is_complete
