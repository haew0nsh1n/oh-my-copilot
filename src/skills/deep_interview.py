"""Deep interview skill for clarifying requirements."""

from typing import List
from domain import (
    DeepInterviewSession,
    InterviewQuestion,
    InterviewAnswer,
    DeepInterviewReport,
    QuestionType,
    InterviewPhase,
)


class DeepInterviewSkill:
    """
    A skill for conducting deep interviews.
    
    This skill helps clarify scope, identify assumptions, risks, and constraints
    before planning or execution.
    """
    
    def __init__(self):
        """Initialize the deep interview skill."""
        self.name = "deep-interview"
        self.description = "Clarify scope, goals, and constraints through systematic questioning"
    
    def create_session(self, prompt: str) -> DeepInterviewSession:
        """
        Create a new deep interview session.
        
        Args:
            prompt: The initial prompt or request to clarify
            
        Returns:
            A new DeepInterviewSession
        """
        session = DeepInterviewSession(prompt=prompt)
        self._generate_initial_questions(session)
        return session
    
    def _generate_initial_questions(self, session: DeepInterviewSession) -> None:
        """Generate initial clarifying questions."""
        initial_questions = [
            InterviewQuestion(
                question="What are the primary goals of this task?",
                question_type=QuestionType.SCOPE,
                priority=5
            ),
            InterviewQuestion(
                question="What is explicitly NOT in scope?",
                question_type=QuestionType.SCOPE,
                priority=5
            ),
            InterviewQuestion(
                question="What are the key constraints (time, budget, technical)?",
                question_type=QuestionType.CONSTRAINT,
                priority=4
            ),
            InterviewQuestion(
                question="What are the main risks or challenges?",
                question_type=QuestionType.RISK,
                priority=4
            ),
            InterviewQuestion(
                question="What assumptions are we making?",
                question_type=QuestionType.ASSUMPTION,
                priority=3
            ),
        ]
        
        for question in initial_questions:
            session.add_question(question)
        
        session.phase = InterviewPhase.EXPLORING
    
    def ask_question(
        self,
        session: DeepInterviewSession,
        question: str,
        question_type: QuestionType = QuestionType.CLARIFICATION
    ) -> InterviewQuestion:
        """
        Ask a new question during the interview.
        
        Args:
            session: The interview session
            question: The question text
            question_type: Type of question
            
        Returns:
            The created InterviewQuestion
        """
        q = InterviewQuestion(
            question=question,
            question_type=question_type,
            priority=3
        )
        session.add_question(q)
        return q
    
    def answer_question(
        self,
        session: DeepInterviewSession,
        question: InterviewQuestion,
        answer: str,
        confidence: float = 0.8
    ) -> InterviewAnswer:
        """
        Record an answer to a question.
        
        Args:
            session: The interview session
            question: The question being answered
            answer: The answer text
            confidence: Confidence level (0.0-1.0)
            
        Returns:
            The created InterviewAnswer
        """
        answer_obj = InterviewAnswer(
            question=question,
            answer=answer,
            confidence=confidence
        )
        session.add_answer(answer_obj)
        return answer_obj
    
    def clarify_goals(
        self,
        session: DeepInterviewSession,
        *goals: str
    ) -> None:
        """
        Add clarified goals to the session.
        
        Args:
            session: The interview session
            goals: Goals to add
        """
        for goal in goals:
            session.add_goal(goal)
    
    def clarify_non_goals(
        self,
        session: DeepInterviewSession,
        *non_goals: str
    ) -> None:
        """
        Add clarified non-goals to the session.
        
        Args:
            session: The interview session
            non_goals: Non-goals to add
        """
        for non_goal in non_goals:
            session.add_non_goal(non_goal)
    
    def identify_assumptions(
        self,
        session: DeepInterviewSession,
        *assumptions: str
    ) -> None:
        """
        Identify key assumptions.
        
        Args:
            session: The interview session
            assumptions: Assumptions to add
        """
        for assumption in assumptions:
            session.add_assumption(assumption)
    
    def identify_risks(
        self,
        session: DeepInterviewSession,
        *risks: str
    ) -> None:
        """
        Identify risks.
        
        Args:
            session: The interview session
            risks: Risks to add
        """
        for risk in risks:
            session.add_risk(risk)
    
    def identify_constraints(
        self,
        session: DeepInterviewSession,
        *constraints: str
    ) -> None:
        """
        Identify constraints.
        
        Args:
            session: The interview session
            constraints: Constraints to add
        """
        for constraint in constraints:
            session.add_constraint(constraint)
    
    def generate_report(self, session: DeepInterviewSession) -> DeepInterviewReport:
        """
        Generate a deep interview report.
        
        Args:
            session: The interview session
            
        Returns:
            A DeepInterviewReport summarizing the findings
        """
        session.phase = InterviewPhase.VALIDATING
        
        # Compile clarified prompt from answers
        clarified_parts = [session.prompt]
        high_confidence_answers = [
            a for a in session.answers
            if a.confidence >= 0.8
        ]
        
        if high_confidence_answers:
            clarified_parts.append("\nKey Clarifications:")
            for answer in high_confidence_answers:
                clarified_parts.append(f"- {answer.answer}")
        
        clarified_prompt = "\n".join(clarified_parts)
        
        report = DeepInterviewReport(
            session=session,
            clarified_prompt=clarified_prompt,
            goals=session.goals,
            non_goals=session.non_goals,
            assumptions=session.assumptions,
            risks=session.risks,
            constraints=session.constraints,
            next_steps=["Review clarifications", "Move to planning phase"]
        )
        
        session.phase = InterviewPhase.COMPLETED
        return report
