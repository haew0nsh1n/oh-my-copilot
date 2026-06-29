"""Best-Practice-Research skill for gathering official evidence."""

from typing import List, Dict
from domain import (
    BestPractice,
    PracticeCategory,
    EvidenceSource,
    BestPracticeLibrary,
    PracticeEvidence,
)


class BestPracticeResearchSkill:
    """
    A skill for researching and documenting best practices.
    
    This skill helps gather official upstream evidence and document
    industry-standard best practices.
    """
    
    def __init__(self):
        """Initialize the skill."""
        self.name = "best_practice_research"
        self.description = "Research and document best practices from official sources"
        self.library = BestPracticeLibrary()
        self.evidence: Dict[str, List[PracticeEvidence]] = {}
    
    def create_practice(
        self,
        title: str,
        category: PracticeCategory,
        description: str,
        rationale: str,
        source: EvidenceSource,
        source_url: str = "",
        adoption_level: int = 0,
        impact_score: int = 0
    ) -> BestPractice:
        """
        Create a best practice entry.
        
        Args:
            title: Practice title
            category: Practice category
            description: Description
            rationale: Why this practice matters
            source: Official source
            source_url: URL to source
            adoption_level: 0-100 adoption percentage
            impact_score: 0-100 impact score
            
        Returns:
            A BestPractice
        """
        practice = BestPractice(
            title=title,
            category=category,
            description=description,
            rationale=rationale,
            source=source,
            source_url=source_url,
            adoption_level=adoption_level,
            impact_score=impact_score
        )
        
        self.library.add_practice(practice)
        self.evidence[title] = []
        
        return practice
    
    def add_evidence_to_practice(
        self,
        practice: BestPractice,
        finding: str,
        verified: bool = False,
        verification_source: str = ""
    ) -> PracticeEvidence:
        """
        Add evidence supporting a practice.
        
        Args:
            practice: The practice
            finding: The evidence finding
            verified: Whether verified
            verification_source: Source of verification
            
        Returns:
            A PracticeEvidence
        """
        evidence = PracticeEvidence(
            practice=practice,
            finding=finding,
            verified=verified,
            verification_source=verification_source
        )
        
        if practice.title not in self.evidence:
            self.evidence[practice.title] = []
        
        self.evidence[practice.title].append(evidence)
        
        return evidence
    
    def add_example_to_practice(
        self,
        practice: BestPractice,
        example: str
    ) -> None:
        """
        Add an example to a practice.
        
        Args:
            practice: The practice
            example: Example implementation
        """
        practice.examples.append(example)
    
    def add_counter_example_to_practice(
        self,
        practice: BestPractice,
        counter_example: str
    ) -> None:
        """
        Add a counter-example to a practice.
        
        Args:
            practice: The practice
            counter_example: What NOT to do
        """
        practice.counter_examples.append(counter_example)
    
    def add_prerequisite_to_practice(
        self,
        practice: BestPractice,
        prerequisite: str
    ) -> None:
        """
        Add a prerequisite to a practice.
        
        Args:
            practice: The practice
            prerequisite: A prerequisite
        """
        practice.prerequisites.append(prerequisite)
    
    def get_practices_by_category(
        self,
        category: PracticeCategory
    ) -> List[BestPractice]:
        """
        Get practices by category.
        
        Args:
            category: The category
            
        Returns:
            List of BestPractices
        """
        return self.library.get_by_category(category)
    
    def get_practices_by_source(
        self,
        source: EvidenceSource
    ) -> List[BestPractice]:
        """
        Get practices by source.
        
        Args:
            source: The source
            
        Returns:
            List of BestPractices
        """
        return self.library.get_by_source(source)
    
    def get_high_impact_practices(
        self,
        threshold: int = 70
    ) -> List[BestPractice]:
        """
        Get high-impact practices.
        
        Args:
            threshold: Impact threshold
            
        Returns:
            List of BestPractices
        """
        return self.library.get_high_impact_practices(threshold)
    
    def get_widely_adopted_practices(
        self,
        threshold: int = 70
    ) -> List[BestPractice]:
        """
        Get widely adopted practices.
        
        Args:
            threshold: Adoption threshold
            
        Returns:
            List of BestPractices
        """
        return self.library.get_widely_adopted_practices(threshold)
    
    def get_evidence_for_practice(
        self,
        practice: BestPractice
    ) -> List[PracticeEvidence]:
        """
        Get evidence for a practice.
        
        Args:
            practice: The practice
            
        Returns:
            List of PracticeEvidence
        """
        return self.evidence.get(practice.title, [])
    
    def get_verified_evidence_for_practice(
        self,
        practice: BestPractice
    ) -> List[PracticeEvidence]:
        """
        Get verified evidence for a practice.
        
        Args:
            practice: The practice
            
        Returns:
            List of verified PracticeEvidence
        """
        all_evidence = self.get_evidence_for_practice(practice)
        return [e for e in all_evidence if e.verified]
    
    def get_all_practices(self) -> List[BestPractice]:
        """Get all practices."""
        return list(self.library.practices.values())
