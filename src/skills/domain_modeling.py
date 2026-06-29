"""Domain modeling skill for defining ubiquitous language."""

from typing import Dict, Any, List
from domain import DomainConcept, DomainModel, ConceptType


class DomainModelingSkill:
    """
    A skill for defining and refining domain models.
    
    This skill helps define ubiquitous language and domain concepts,
    validate domain model completeness, and generate documentation.
    """
    
    def __init__(self):
        """Initialize the domain modeling skill."""
        self.name = "domain-modeling"
        self.description = "Define and refine ubiquitous language and domain concepts"
    
    def create_model(self, project_name: str, description: str) -> DomainModel:
        """
        Create a new domain model.
        
        Args:
            project_name: Name of the project
            description: Project description
            
        Returns:
            A new DomainModel
        """
        return DomainModel(
            project_name=project_name,
            description=description
        )
    
    def add_concept(
        self,
        model: DomainModel,
        name: str,
        description: str,
        concept_type: ConceptType,
        examples: List[str] | None = None,
        invariants: List[str] | None = None,
    ) -> DomainConcept:
        """
        Add a concept to the domain model.
        
        Args:
            model: The domain model
            name: Concept name (ubiquitous language term)
            description: What the concept means
            concept_type: Type of concept (Entity, Value Object, etc.)
            examples: Optional examples of the concept
            invariants: Optional business rules/invariants
            
        Returns:
            The created DomainConcept
        """
        concept = DomainConcept(
            name=name,
            description=description,
            concept_type=concept_type,
            examples=examples or [],
            invariants=invariants or []
        )
        model.add_concept(concept)
        return concept
    
    def validate_model(self, model: DomainModel) -> Dict[str, Any]:
        """
        Validate a domain model for completeness.
        
        Args:
            model: The domain model to validate
            
        Returns:
            Dictionary with validation results:
            - is_valid: Whether model is valid
            - concept_count: Number of concepts
            - issues: List of any issues found
        """
        issues: List[str] = []
        
        if len(model.concepts) == 0:
            issues.append("No concepts defined")
        
        # Check for concepts with incomplete documentation
        for concept in model.concepts:
            if not concept.description or len(concept.description) < 10:
                issues.append(f"Concept '{concept.name}' has insufficient description")
        
        return {
            "is_valid": len(issues) == 0,
            "concept_count": len(model.concepts),
            "issues": issues
        }
    
    def generate_summary(self, model: DomainModel) -> str:
        """
        Generate a human-readable summary of the domain model.
        
        Args:
            model: The domain model
            
        Returns:
            A formatted summary string
        """
        lines = [
            f"# Domain Model: {model.project_name}",
            f"\n{model.description}\n",
            f"## Concepts ({len(model.concepts)} total)\n",
        ]
        
        # Group by type
        by_type: Dict[ConceptType, List[DomainConcept]] = {}
        for concept in model.concepts:
            if concept.concept_type not in by_type:
                by_type[concept.concept_type] = []
            by_type[concept.concept_type].append(concept)
        
        # Format by type
        for concept_type, concepts in sorted(by_type.items()):
            lines.append(f"### {concept_type.value.replace('_', ' ').title()}s\n")
            for concept in concepts:
                lines.append(f"- **{concept.name}**: {concept.description}")
                if concept.examples:
                    lines.append(f"  - Examples: {', '.join(concept.examples)}")
                if concept.invariants:
                    lines.append(f"  - Rules: {', '.join(concept.invariants)}")
            lines.append("")
        
        return "\n".join(lines)
