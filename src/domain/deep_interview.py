"""Domain model for deep interview sessions."""

from dataclasses import dataclass, field
from typing import List
from enum import Enum
from datetime import datetime


class QuestionType(str, Enum):
    """Type of interview question."""
    CLARIFICATION = "clarification"
    SCOPE = "scope"
    CONSTRAINT = "constraint"
    ASSUMPTION = "assumption"
    TRADEOFF = "tradeoff"
    RISK = "risk"


class InterviewPhase(str, Enum):
    """Phase of the interview."""
    INITIAL = "initial"
    EXPLORING = "exploring"
    VALIDATING = "validating"
    COMPLETED = "completed"


@dataclass
class InterviewQuestion:
    """A question asked during deep interview."""
    question: str
    question_type: QuestionType
    context: str = ""
    priority: int = 1  # 1-5, higher is more important
    
    def __post_init__(self):
        """Validate question."""
        if not self.question or not self.question.strip():
            raise ValueError("Question cannot be empty")
        if self.priority < 1 or self.priority > 5:
            raise ValueError("Priority must be between 1 and 5")


@dataclass
class InterviewAnswer:
    """An answer to an interview question."""
    question: InterviewQuestion
    answer: str
    confidence: float = 0.5  # 0.0-1.0 confidence in answer
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate answer."""
        if not self.answer or not self.answer.strip():
            raise ValueError("Answer cannot be empty")
        if self.confidence < 0.0 or self.confidence > 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")


@dataclass
class DeepInterviewSession:
    """A deep interview session to clarify requirements."""
    prompt: str
    questions: List[InterviewQuestion] = field(default_factory=list)
    answers: List[InterviewAnswer] = field(default_factory=list)
    phase: InterviewPhase = InterviewPhase.INITIAL
    goals: List[str] = field(default_factory=list)  # Clarified goals
    non_goals: List[str] = field(default_factory=list)  # What's NOT in scope
    assumptions: List[str] = field(default_factory=list)  # Key assumptions
    risks: List[str] = field(default_factory=list)  # Identified risks
    constraints: List[str] = field(default_factory=list)  # Technical/business constraints
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate session."""
        if not self.prompt or not self.prompt.strip():
            raise ValueError("Prompt cannot be empty")
    
    def add_question(self, question: InterviewQuestion) -> None:
        """Add a question to the interview."""
        if question in self.questions:
            raise ValueError("Question already exists")
        self.questions.append(question)
    
    def add_answer(self, answer: InterviewAnswer) -> None:
        """Add an answer to the interview."""
        if answer in self.answers:
            raise ValueError("Answer already exists")
        self.answers.append(answer)
    
    def get_unanswered_questions(self) -> List[InterviewQuestion]:
        """Get all questions that haven't been answered."""
        answered_questions = {a.question for a in self.answers}
        return [q for q in self.questions if q not in answered_questions]
    
    def add_goal(self, goal: str) -> None:
        """Add a clarified goal."""
        if goal not in self.goals:
            self.goals.append(goal)
    
    def add_non_goal(self, non_goal: str) -> None:
        """Add a non-goal (out of scope)."""
        if non_goal not in self.non_goals:
            self.non_goals.append(non_goal)
    
    def add_assumption(self, assumption: str) -> None:
        """Add a key assumption."""
        if assumption not in self.assumptions:
            self.assumptions.append(assumption)
    
    def add_risk(self, risk: str) -> None:
        """Add an identified risk."""
        if risk not in self.risks:
            self.risks.append(risk)
    
    def add_constraint(self, constraint: str) -> None:
        """Add a constraint."""
        if constraint not in self.constraints:
            self.constraints.append(constraint)


@dataclass
class DeepInterviewReport:
    """Report from a deep interview session."""
    session: DeepInterviewSession
    clarified_prompt: str
    goals: List[str]
    non_goals: List[str]
    assumptions: List[str]
    risks: List[str]
    constraints: List[str]
    next_steps: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate report."""
        if not self.clarified_prompt or not self.clarified_prompt.strip():
            raise ValueError("Clarified prompt cannot be empty")
