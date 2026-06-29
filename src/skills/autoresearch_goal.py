"""Autoresearch-Goal skill for goal-mode research missions."""

from typing import List, Optional
from datetime import datetime
from domain import (
    ResearchMission,
    ResearchGoalStatus,
    ProfessorReview,
    CriticReview,
    ResearchGoalReport,
)


class AutoresearchGoalSkill:
    """
    A skill for goal-mode research missions with Professor/Critic validation.
    
    Unlike regular Autoresearch (bounded artifact), this focuses on durable
    goal-driven research with continuing validation pressure.
    """
    
    def __init__(self):
        """Initialize the skill."""
        self.name = "autoresearch_goal"
        self.description = "Goal-mode research with Professor/Critic validation"
        self.missions: dict = {}
    
    def create_research_mission(
        self,
        title: str,
        research_focus: str,
        professor_prompt: str = "",
        critic_prompt: str = ""
    ) -> ResearchMission:
        """
        Create a research mission.
        
        Args:
            title: Mission title
            research_focus: What to research
            professor_prompt: Professor-style guidance
            critic_prompt: Critic-style challenge
            
        Returns:
            A ResearchMission
        """
        mission = ResearchMission(
            title=title,
            research_focus=research_focus,
            professor_prompt=professor_prompt,
            critic_prompt=critic_prompt
        )
        self.missions[title] = mission
        return mission
    
    def start_mission(self, mission: ResearchMission) -> None:
        """
        Start a research mission.
        
        Args:
            mission: The mission
        """
        mission.status = ResearchGoalStatus.IN_PROGRESS
    
    def add_finding(
        self,
        mission: ResearchMission,
        finding: str
    ) -> None:
        """
        Add a research finding.
        
        Args:
            mission: The mission
            finding: The finding
        """
        mission.add_finding(finding)
    
    def validate_finding(
        self,
        mission: ResearchMission,
        validation: str
    ) -> None:
        """
        Validate a finding.
        
        Args:
            mission: The mission
            validation: Validation result
        """
        mission.add_validation(validation)
    
    def get_professor_review(
        self,
        mission: ResearchMission,
        guidance: str,
        next_steps: List[str] = None
    ) -> ProfessorReview:
        """
        Get professor review.
        
        Args:
            mission: The mission
            guidance: Professor guidance
            next_steps: Recommended next steps
            
        Returns:
            A ProfessorReview
        """
        review = ProfessorReview(
            mission=mission,
            guidance=guidance,
            recommended_next_steps=next_steps or []
        )
        return review
    
    def get_critic_review(
        self,
        mission: ResearchMission,
        challenges: List[str] = None,
        weaknesses: List[str] = None
    ) -> CriticReview:
        """
        Get critic review.
        
        Args:
            mission: The mission
            challenges: Critical challenges
            weaknesses: Identified weaknesses
            
        Returns:
            A CriticReview
        """
        review = CriticReview(
            mission=mission,
            challenges=challenges or [],
            weaknesses=weaknesses or []
        )
        return review
    
    def is_research_sufficient(self, mission: ResearchMission) -> bool:
        """
        Check if research is sufficient.
        
        Args:
            mission: The mission
            
        Returns:
            True if findings and validations exist
        """
        return (
            mission.get_findings_count() > 0 and
            mission.get_validations_count() > 0
        )
    
    def complete_mission(self, mission: ResearchMission) -> None:
        """
        Mark mission as complete.
        
        Args:
            mission: The mission
        """
        mission.status = ResearchGoalStatus.COMPLETED
        mission.completed_at = datetime.now()
    
    def fail_mission(self, mission: ResearchMission) -> None:
        """
        Mark mission as failed.
        
        Args:
            mission: The mission
        """
        mission.status = ResearchGoalStatus.FAILED
        mission.completed_at = datetime.now()
    
    def generate_report(self, mission: ResearchMission) -> ResearchGoalReport:
        """
        Generate research report.
        
        Args:
            mission: The mission
            
        Returns:
            A ResearchGoalReport
        """
        summary = (
            f"Research Complete: {mission.get_findings_count()} findings, "
            f"{mission.get_validations_count()} validations"
        )
        
        report = ResearchGoalReport(
            title=mission.title,
            status=mission.status,
            findings_count=mission.get_findings_count(),
            validations_count=mission.get_validations_count(),
            completed_at=mission.completed_at,
            summary=summary,
            is_complete=mission.is_complete()
        )
        
        return report
    
    def get_mission(self, title: str) -> Optional[ResearchMission]:
        """Get a mission by title."""
        return self.missions.get(title)
    
    def get_all_missions(self) -> List[ResearchMission]:
        """Get all missions."""
        return list(self.missions.values())
