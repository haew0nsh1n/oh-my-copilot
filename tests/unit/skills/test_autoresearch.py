"""Tests for autoresearch skill."""

import pytest
from skills import AutoresearchSkill
from domain import EvidenceType, ResearchStatus


class TestAutoresearchBasics:
    """Test basic autoresearch skill functionality."""
    
    def test_skill_can_be_created(self):
        """RED: Skill can be instantiated."""
        skill = AutoresearchSkill()
        assert skill is not None
    
    def test_skill_has_name(self):
        """RED: Skill has a name."""
        skill = AutoresearchSkill()
        assert skill.name == "autoresearch"


class TestResearchTarget:
    """Test research target creation."""
    
    def test_create_research_target(self):
        """RED: Can create a research target."""
        skill = AutoresearchSkill()
        
        target = skill.create_research_target(
            "OAuth2 Security",
            "Best practices for OAuth2 security",
            keywords=["oauth2", "security", "tokens"]
        )
        
        assert target.topic == "OAuth2 Security"
        assert len(target.keywords) == 3


class TestResearchTask:
    """Test research task creation."""
    
    def test_create_research_task(self):
        """RED: Can create a research task."""
        skill = AutoresearchSkill()
        
        target = skill.create_research_target("Topic", "Query")
        task = skill.create_research_task(target, max_items=5)
        
        assert task.target.topic == "Topic"
        assert task.status == ResearchStatus.PENDING
    
    def test_task_is_stored(self):
        """RED: Task is stored in skill."""
        skill = AutoresearchSkill()
        
        target = skill.create_research_target("Topic", "Query")
        task = skill.create_research_task(target)
        
        retrieved = skill.get_task(task.task_id)
        assert retrieved.task_id == task.task_id


class TestEvidence:
    """Test evidence collection."""
    
    def test_add_evidence_to_task(self):
        """RED: Can add evidence to a task."""
        skill = AutoresearchSkill()
        
        target = skill.create_research_target("Topic", "Query")
        task = skill.create_research_task(target)
        
        success = skill.add_evidence(
            task,
            "OAuth2 RFC",
            EvidenceType.REFERENCE,
            "https://tools.ietf.org/html/rfc6749",
            "OAuth 2.0 Authorization Framework",
            0.95
        )
        
        assert success is True
        assert len(task.evidence) == 1
    
    def test_evidence_respects_relevance_threshold(self):
        """RED: Low relevance evidence is rejected."""
        skill = AutoresearchSkill()
        
        target = skill.create_research_target("Topic", "Query")
        task = skill.create_research_task(target, min_relevance=0.6)
        
        success = skill.add_evidence(
            task,
            "Low relevance",
            EvidenceType.REFERENCE,
            "source",
            "content",
            0.3  # Below threshold
        )
        
        assert success is False
        assert len(task.evidence) == 0
    
    def test_evidence_respects_max_items(self):
        """RED: Task respects max items limit."""
        skill = AutoresearchSkill()
        
        target = skill.create_research_target("Topic", "Query")
        task = skill.create_research_task(target, max_items=2)
        
        # Add 2 items
        skill.add_evidence(task, "Ev1", EvidenceType.REFERENCE, "s1", "c1", 0.9)
        skill.add_evidence(task, "Ev2", EvidenceType.REFERENCE, "s2", "c2", 0.9)
        
        # Try to add 3rd
        success = skill.add_evidence(task, "Ev3", EvidenceType.REFERENCE, "s3", "c3", 0.9)
        
        assert success is False
        assert len(task.evidence) == 2


class TestValidationGates:
    """Test validation gates."""
    
    def test_create_validation_gate(self):
        """RED: Can create validation gates."""
        skill = AutoresearchSkill()
        
        gate = skill.create_validation_gate(
            "min_evidence",
            "Must have at least 3 evidence items",
            "Check evidence count"
        )
        
        assert gate.name == "min_evidence"
        assert gate.required is True


class TestResearch:
    """Test research workflow."""
    
    def test_start_and_complete_research(self):
        """RED: Can start and complete research."""
        skill = AutoresearchSkill()
        
        target = skill.create_research_target("Topic", "Query")
        task = skill.create_research_task(target)
        
        skill.start_research(task)
        assert task.status == ResearchStatus.IN_PROGRESS
        
        skill.complete_research(task)
        assert task.status == ResearchStatus.COMPLETED
    
    def test_fail_research(self):
        """RED: Can fail research."""
        skill = AutoresearchSkill()
        
        target = skill.create_research_target("Topic", "Query")
        task = skill.create_research_task(target)
        
        skill.fail_research(task)
        assert task.status == ResearchStatus.FAILED


class TestReporting:
    """Test research reporting."""
    
    def test_generate_report(self):
        """RED: Can generate research report."""
        skill = AutoresearchSkill()
        
        target = skill.create_research_target("Topic", "Query")
        task = skill.create_research_task(target)
        
        skill.add_evidence(task, "Ev1", EvidenceType.REFERENCE, "s", "c", 0.9)
        skill.complete_research(task)
        
        report = skill.generate_report(task)
        
        assert report.topic == "Topic"
        assert report.evidence_count == 1
        assert "Ev1" in report.evidence_summary
