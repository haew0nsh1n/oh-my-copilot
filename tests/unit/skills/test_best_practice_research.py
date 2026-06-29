"""Tests for best-practice-research skill."""

import pytest
from skills import BestPracticeResearchSkill
from domain import PracticeCategory, EvidenceSource


class TestBestPracticeResearchBasics:
    """Test basic best-practice-research skill functionality."""
    
    def test_skill_can_be_created(self):
        """RED: Skill can be instantiated."""
        skill = BestPracticeResearchSkill()
        assert skill is not None
    
    def test_skill_has_name(self):
        """RED: Skill has a name."""
        skill = BestPracticeResearchSkill()
        assert skill.name == "best_practice_research"


class TestPracticeCreation:
    """Test practice creation."""
    
    def test_create_practice(self):
        """RED: Can create a best practice."""
        skill = BestPracticeResearchSkill()
        
        practice = skill.create_practice(
            "API Versioning",
            PracticeCategory.ARCHITECTURE,
            "Use semantic versioning for APIs",
            "Prevents breaking changes for clients",
            EvidenceSource.OFFICIAL_DOCS,
            adoption_level=85,
            impact_score=90
        )
        
        assert practice.title == "API Versioning"
        assert practice.adoption_level == 85


class TestPracticeMetadata:
    """Test practice metadata."""
    
    def test_add_example(self):
        """RED: Can add examples to practices."""
        skill = BestPracticeResearchSkill()
        
        practice = skill.create_practice(
            "Practice",
            PracticeCategory.TESTING,
            "Desc",
            "Rationale",
            EvidenceSource.RFC
        )
        
        skill.add_example_to_practice(practice, "Example 1")
        
        assert "Example 1" in practice.examples
    
    def test_add_counter_example(self):
        """RED: Can add counter-examples."""
        skill = BestPracticeResearchSkill()
        
        practice = skill.create_practice(
            "Practice",
            PracticeCategory.SECURITY,
            "Desc",
            "Rationale",
            EvidenceSource.SPEC
        )
        
        skill.add_counter_example_to_practice(practice, "Bad practice")
        
        assert "Bad practice" in practice.counter_examples
    
    def test_add_prerequisite(self):
        """RED: Can add prerequisites."""
        skill = BestPracticeResearchSkill()
        
        practice = skill.create_practice(
            "Practice",
            PracticeCategory.DEPLOYMENT,
            "Desc",
            "Rationale",
            EvidenceSource.OFFICIAL_DOCS
        )
        
        skill.add_prerequisite_to_practice(practice, "Docker installed")
        
        assert "Docker installed" in practice.prerequisites


class TestEvidence:
    """Test evidence collection."""
    
    def test_add_evidence_to_practice(self):
        """RED: Can add evidence to practices."""
        skill = BestPracticeResearchSkill()
        
        practice = skill.create_practice(
            "TLS 1.3",
            PracticeCategory.SECURITY,
            "Use TLS 1.3",
            "Better security",
            EvidenceSource.RFC
        )
        
        evidence = skill.add_evidence_to_practice(
            practice,
            "TLS 1.3 is faster",
            verified=True,
            verification_source="Official Benchmark"
        )
        
        assert evidence.verified is True
    
    def test_get_evidence(self):
        """RED: Can retrieve evidence."""
        skill = BestPracticeResearchSkill()
        
        practice = skill.create_practice(
            "Practice",
            PracticeCategory.CODE_QUALITY,
            "D",
            "R",
            EvidenceSource.PAPER
        )
        
        skill.add_evidence_to_practice(practice, "Finding 1", verified=True)
        skill.add_evidence_to_practice(practice, "Finding 2", verified=False)
        
        evidence = skill.get_evidence_for_practice(practice)
        assert len(evidence) == 2


class TestSearchAndFilter:
    """Test searching and filtering practices."""
    
    def test_get_practices_by_category(self):
        """RED: Can filter by category."""
        skill = BestPracticeResearchSkill()
        
        skill.create_practice("P1", PracticeCategory.SECURITY, "D", "R", EvidenceSource.OFFICIAL_DOCS)
        skill.create_practice("P2", PracticeCategory.SECURITY, "D", "R", EvidenceSource.OFFICIAL_DOCS)
        skill.create_practice("P3", PracticeCategory.TESTING, "D", "R", EvidenceSource.OFFICIAL_DOCS)
        
        security = skill.get_practices_by_category(PracticeCategory.SECURITY)
        assert len(security) == 2
    
    def test_get_practices_by_source(self):
        """RED: Can filter by source."""
        skill = BestPracticeResearchSkill()
        
        skill.create_practice("P1", PracticeCategory.TESTING, "D", "R", EvidenceSource.RFC)
        skill.create_practice("P2", PracticeCategory.TESTING, "D", "R", EvidenceSource.RFC)
        skill.create_practice("P3", PracticeCategory.TESTING, "D", "R", EvidenceSource.SPEC)
        
        rfc_practices = skill.get_practices_by_source(EvidenceSource.RFC)
        assert len(rfc_practices) == 2
    
    def test_get_high_impact_practices(self):
        """RED: Can filter by impact."""
        skill = BestPracticeResearchSkill()
        
        skill.create_practice("P1", PracticeCategory.CODE_QUALITY, "D", "R", EvidenceSource.OFFICIAL_DOCS, impact_score=90)
        skill.create_practice("P2", PracticeCategory.CODE_QUALITY, "D", "R", EvidenceSource.OFFICIAL_DOCS, impact_score=40)
        
        high_impact = skill.get_high_impact_practices(threshold=70)
        assert len(high_impact) == 1


class TestAll:
    """Test getting all practices."""
    
    def test_get_all_practices(self):
        """RED: Can get all practices."""
        skill = BestPracticeResearchSkill()
        
        skill.create_practice("P1", PracticeCategory.MONITORING, "D", "R", EvidenceSource.OFFICIAL_DOCS)
        skill.create_practice("P2", PracticeCategory.PERFORMANCE, "D", "R", EvidenceSource.SPEC)
        
        all_practices = skill.get_all_practices()
        assert len(all_practices) == 2
