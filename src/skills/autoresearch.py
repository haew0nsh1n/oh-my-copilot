"""Autoresearch skill for bounded research with validation gates."""

from typing import List, Callable, Dict, Optional
from uuid import uuid4
from datetime import datetime
from domain import (
    ResearchTask,
    ResearchTarget,
    ResearchStatus,
    Evidence,
    EvidenceType,
    ValidationGate,
    ResearchReport,
)


class AutoresearchSkill:
    """
    A skill for bounded research with validation gates.
    
    This skill helps conduct focused research on specific topics with
    built-in validation checkpoints.
    """
    
    def __init__(self):
        """Initialize the skill."""
        self.name = "autoresearch"
        self.description = "Conduct bounded research with validation gates"
        self.tasks: Dict[str, ResearchTask] = {}
        self.gates: Dict[str, ValidationGate] = {}
    
    def create_research_target(
        self,
        topic: str,
        query: str,
        keywords: List[str] = None
    ) -> ResearchTarget:
        """
        Create a research target.
        
        Args:
            topic: Research topic
            query: Research query
            keywords: Keywords to search for
            
        Returns:
            A ResearchTarget
        """
        return ResearchTarget(
            topic=topic,
            query=query,
            keywords=keywords or []
        )
    
    def create_research_task(
        self,
        target: ResearchTarget,
        max_items: int = 10,
        min_relevance: float = 0.5
    ) -> ResearchTask:
        """
        Create a research task.
        
        Args:
            target: The research target
            max_items: Maximum evidence items
            min_relevance: Minimum relevance score
            
        Returns:
            A ResearchTask
        """
        task = ResearchTask(
            task_id=str(uuid4()),
            target=target,
            max_items=max_items,
            min_relevance=min_relevance
        )
        self.tasks[task.task_id] = task
        return task
    
    def add_evidence(
        self,
        task: ResearchTask,
        title: str,
        evidence_type: EvidenceType,
        source: str,
        content: str,
        relevance_score: float
    ) -> bool:
        """
        Add evidence to a research task.
        
        Args:
            task: The research task
            title: Evidence title
            evidence_type: Type of evidence
            source: Source of the evidence
            content: Evidence content
            relevance_score: Relevance score (0.0-1.0)
            
        Returns:
            True if added, False otherwise
        """
        evidence = Evidence(
            title=title,
            evidence_type=evidence_type,
            source=source,
            content=content,
            relevance_score=relevance_score
        )
        return task.add_evidence(evidence)
    
    def create_validation_gate(
        self,
        name: str,
        description: str,
        validator: str = "",
        required: bool = True
    ) -> ValidationGate:
        """
        Create a validation gate.
        
        Args:
            name: Gate name
            description: Gate description
            validator: Description of validation
            required: Whether gate is required
            
        Returns:
            A ValidationGate
        """
        gate = ValidationGate(
            name=name,
            description=description,
            validator=validator,
            required=required
        )
        self.gates[name] = gate
        return gate
    
    def validate_research(
        self,
        task: ResearchTask,
        gate_names: List[str] = None,
        custom_validator: Callable = None
    ) -> bool:
        """
        Validate research results at a gate.
        
        Args:
            task: The research task
            gate_names: Specific gates to validate
            custom_validator: Custom validator function
            
        Returns:
            True if validation passes
        """
        # Check if research is complete
        if not task.is_complete():
            return False
        
        # Get gates to check
        gates_to_check = self.gates.values()
        if gate_names:
            gates_to_check = [self.gates[g] for g in gate_names if g in self.gates]
        
        # Run validations
        for gate in gates_to_check:
            if custom_validator:
                if not custom_validator(task, gate):
                    return False
        
        task.status = ResearchStatus.COMPLETED
        task.completed_at = datetime.now()
        return True
    
    def start_research(self, task: ResearchTask) -> None:
        """
        Start a research task.
        
        Args:
            task: The task to start
        """
        task.status = ResearchStatus.IN_PROGRESS
    
    def complete_research(self, task: ResearchTask) -> None:
        """
        Mark research as complete.
        
        Args:
            task: The task to complete
        """
        task.status = ResearchStatus.COMPLETED
        task.completed_at = datetime.now()
    
    def fail_research(self, task: ResearchTask) -> None:
        """
        Mark research as failed.
        
        Args:
            task: The task to fail
        """
        task.status = ResearchStatus.FAILED
        task.completed_at = datetime.now()
    
    def generate_report(self, task: ResearchTask) -> ResearchReport:
        """
        Generate a research report.
        
        Args:
            task: The research task
            
        Returns:
            A ResearchReport
        """
        summary = [e.title for e in task.evidence]
        
        report = ResearchReport(
            task_id=task.task_id,
            topic=task.target.topic,
            status=task.status,
            evidence_count=len(task.evidence),
            completed_at=task.completed_at,
            evidence_summary=summary,
            validated=(task.status == ResearchStatus.COMPLETED)
        )
        
        return report
    
    def get_task(self, task_id: str) -> Optional[ResearchTask]:
        """Get a research task by ID."""
        return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> List[ResearchTask]:
        """Get all research tasks."""
        return list(self.tasks.values())
