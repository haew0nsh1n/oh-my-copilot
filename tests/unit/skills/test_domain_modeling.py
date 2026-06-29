"""Tests for domain modeling skill - TDD approach."""

import pytest
from skills import DomainModelingSkill
from domain import DomainConcept, DomainModel, ConceptType


class TestDomainModelingSkillCreation:
    """Test creating and initializing the domain modeling skill."""
    
    def test_skill_can_be_created(self):
        """RED: DomainModelingSkill can be instantiated."""
        skill = DomainModelingSkill()
        assert skill is not None
    
    def test_skill_has_name(self):
        """RED: Skill has a descriptive name."""
        skill = DomainModelingSkill()
        assert skill.name == "domain-modeling"
    
    def test_skill_has_description(self):
        """RED: Skill has a description."""
        skill = DomainModelingSkill()
        assert skill.description is not None
        assert len(skill.description) > 0


class TestDomainConceptCreation:
    """Test creating domain concepts."""
    
    def test_create_concept_with_required_fields(self):
        """RED: Can create a domain concept."""
        concept = DomainConcept(
            name="User",
            description="A person using the system",
            concept_type=ConceptType.ENTITY
        )
        
        assert concept.name == "User"
        assert concept.description == "A person using the system"
        assert concept.concept_type == ConceptType.ENTITY
    
    def test_concept_name_cannot_be_empty(self):
        """RED: Concept name is required."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            DomainConcept(
                name="",
                description="A description",
                concept_type=ConceptType.ENTITY
            )
    
    def test_concept_requires_description(self):
        """RED: Concept description is required."""
        with pytest.raises(ValueError, match="description cannot be empty"):
            DomainConcept(
                name="User",
                description="",
                concept_type=ConceptType.ENTITY
            )


class TestDomainModelCreation:
    """Test creating domain models."""
    
    def test_create_domain_model(self):
        """RED: Can create a domain model."""
        model = DomainModel(
            project_name="Auth System",
            description="Authentication and authorization system"
        )
        
        assert model.project_name == "Auth System"
        assert model.description == "Authentication and authorization system"
        assert len(model.concepts) == 0
    
    def test_add_concept_to_model(self):
        """RED: Can add concepts to domain model."""
        model = DomainModel(
            project_name="Auth System",
            description="Auth system"
        )
        concept = DomainConcept(
            name="User",
            description="A user account",
            concept_type=ConceptType.ENTITY
        )
        
        model.add_concept(concept)
        
        assert concept in model.concepts
        assert len(model.concepts) == 1
    
    def test_cannot_add_duplicate_concept(self):
        """RED: Cannot add duplicate concept by name."""
        model = DomainModel(
            project_name="Auth System",
            description="Auth system"
        )
        concept = DomainConcept(
            name="User",
            description="A user",
            concept_type=ConceptType.ENTITY
        )
        
        model.add_concept(concept)
        
        duplicate = DomainConcept(
            name="User",
            description="Another user",
            concept_type=ConceptType.ENTITY
        )
        
        with pytest.raises(ValueError, match="Concept 'User' already exists"):
            model.add_concept(duplicate)
    
    def test_get_concept_by_name(self):
        """RED: Can retrieve concept by name."""
        model = DomainModel(
            project_name="Auth System",
            description="Auth system"
        )
        concept = DomainConcept(
            name="User",
            description="A user",
            concept_type=ConceptType.ENTITY
        )
        model.add_concept(concept)
        
        retrieved = model.get_concept("User")
        
        assert retrieved == concept
    
    def test_get_nonexistent_concept_raises_error(self):
        """RED: Retrieving nonexistent concept raises error."""
        model = DomainModel(
            project_name="Auth System",
            description="Auth system"
        )
        
        with pytest.raises(ValueError, match="Concept 'User' not found"):
            model.get_concept("User")


class TestDomainModelingSkillOperations:
    """Test domain modeling skill operations."""
    
    def test_skill_creates_domain_model(self):
        """RED: Skill can create a domain model."""
        skill = DomainModelingSkill()
        
        model = skill.create_model(
            project_name="E-Commerce",
            description="Online shopping platform"
        )
        
        assert model.project_name == "E-Commerce"
        assert isinstance(model, DomainModel)
    
    def test_skill_adds_concept_to_model(self):
        """RED: Skill can add concept to model."""
        skill = DomainModelingSkill()
        model = skill.create_model("E-Commerce", "Shopping platform")
        
        concept = skill.add_concept(
            model=model,
            name="Product",
            description="An item for sale",
            concept_type=ConceptType.ENTITY
        )
        
        assert concept in model.concepts
        assert concept.name == "Product"
    
    def test_skill_validates_ubiquitous_language(self):
        """RED: Skill can validate domain model completeness."""
        skill = DomainModelingSkill()
        model = skill.create_model("E-Commerce", "Shopping platform")
        
        # Add some concepts
        skill.add_concept(model, "Product", "Item for sale", ConceptType.ENTITY)
        skill.add_concept(model, "Order", "Customer purchase", ConceptType.ENTITY)
        skill.add_concept(model, "Payment", "Transaction", ConceptType.VALUE_OBJECT)
        
        # Validate
        validation = skill.validate_model(model)
        
        assert validation["is_valid"] is True
        assert validation["concept_count"] == 3
        assert len(validation["issues"]) == 0
    
    def test_skill_detects_incomplete_model(self):
        """RED: Skill detects models without enough concepts."""
        skill = DomainModelingSkill()
        model = skill.create_model("E-Commerce", "Shopping platform")
        
        # Model with no concepts
        validation = skill.validate_model(model)
        
        assert validation["is_valid"] is False
        assert "No concepts defined" in validation["issues"]
    
    def test_skill_generates_model_summary(self):
        """RED: Skill generates human-readable summary."""
        skill = DomainModelingSkill()
        model = skill.create_model("Auth System", "User authentication")
        
        skill.add_concept(model, "User", "System user", ConceptType.ENTITY)
        skill.add_concept(model, "Token", "Auth token", ConceptType.VALUE_OBJECT)
        
        summary = skill.generate_summary(model)
        
        assert model.project_name in summary
        assert "User" in summary
        assert "Token" in summary
        assert "2 total" in summary
