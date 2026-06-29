"""Domain model for ubiquitous language and domain concepts."""

from dataclasses import dataclass, field
from typing import List
from enum import Enum


class ConceptType(str, Enum):
    """Types of domain concepts."""
    ENTITY = "entity"
    VALUE_OBJECT = "value_object"
    AGGREGATE = "aggregate"
    SERVICE = "service"
    EVENT = "event"
    REPOSITORY = "repository"


@dataclass
class DomainConcept:
    """A single concept in the ubiquitous language."""
    
    name: str
    description: str
    concept_type: ConceptType
    related_concepts: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    invariants: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate concept on creation."""
        if not self.name or not self.name.strip():
            raise ValueError("Concept name cannot be empty")
        if not self.description or not self.description.strip():
            raise ValueError("Concept description cannot be empty")


@dataclass
class DomainModel:
    """A domain model containing ubiquitous language concepts."""
    
    project_name: str
    description: str
    concepts: List[DomainConcept] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate model on creation."""
        if not self.project_name or not self.project_name.strip():
            raise ValueError("Project name cannot be empty")
        if not self.description or not self.description.strip():
            raise ValueError("Description cannot be empty")
    
    def add_concept(self, concept: DomainConcept) -> None:
        """
        Add a concept to the domain model.
        
        Args:
            concept: The concept to add
            
        Raises:
            ValueError: If concept with same name already exists
        """
        if any(c.name == concept.name for c in self.concepts):
            raise ValueError(f"Concept '{concept.name}' already exists in model")
        self.concepts.append(concept)
    
    def get_concept(self, name: str) -> DomainConcept:
        """
        Retrieve a concept by name.
        
        Args:
            name: The concept name
            
        Returns:
            The DomainConcept
            
        Raises:
            ValueError: If concept not found
        """
        for concept in self.concepts:
            if concept.name == name:
                return concept
        raise ValueError(f"Concept '{name}' not found in model")
    
    def get_concepts_by_type(self, concept_type: ConceptType) -> List[DomainConcept]:
        """Get all concepts of a specific type."""
        return [c for c in self.concepts if c.concept_type == concept_type]
