"""UltraQA skill for test/verify/fix loops."""

from typing import List, Optional
from domain import (
    UltraQA,
    TestCase,
    QALoopStatus,
    FixAttempt,
    UltraQAReport,
)


class UltraQASkill:
    """
    A skill for test/verify/fix loops with merge readiness gates.
    
    This skill helps ensure code is merge-ready through comprehensive
    testing, verification, and automated fix cycles.
    """
    
    def __init__(self):
        """Initialize the skill."""
        self.name = "ultraqa"
        self.description = "Test/verify/fix loop for merge readiness"
        self.qa_sessions: dict = {}
    
    def create_qa_session(
        self,
        title: str,
        description: str = ""
    ) -> UltraQA:
        """
        Create a QA session.
        
        Args:
            title: Session title
            description: Session description
            
        Returns:
            An UltraQA session
        """
        qa = UltraQA(title=title, description=description)
        self.qa_sessions[title] = qa
        return qa
    
    def add_test_case(
        self,
        qa: UltraQA,
        name: str,
        description: str
    ) -> TestCase:
        """
        Add a test case.
        
        Args:
            qa: The QA session
            name: Test name
            description: Test description
            
        Returns:
            A TestCase
        """
        return qa.add_test_case(name, description)
    
    def add_test_step(
        self,
        test_case: TestCase,
        step: str
    ) -> None:
        """
        Add a test step.
        
        Args:
            test_case: The test case
            step: The test step
        """
        test_case.test_steps.append(step)
    
    def set_expected_result(
        self,
        test_case: TestCase,
        expected: str
    ) -> None:
        """
        Set expected result.
        
        Args:
            test_case: The test case
            expected: Expected result
        """
        test_case.expected_result = expected
    
    def verify_test(
        self,
        qa: UltraQA,
        test_case: TestCase,
        passed: bool,
        evidence: str = ""
    ) -> None:
        """
        Verify a test.
        
        Args:
            qa: The QA session
            test_case: The test case
            passed: Whether test passed
            evidence: Verification evidence
        """
        qa.add_verification_result(test_case, passed, evidence)
        qa.status = QALoopStatus.VERIFYING
    
    def add_fix(
        self,
        qa: UltraQA,
        description: str,
        fixes: List[str] = None
    ) -> FixAttempt:
        """
        Add a fix attempt.
        
        Args:
            qa: The QA session
            description: Fix description
            fixes: List of fixes applied
            
        Returns:
            A FixAttempt
        """
        qa.status = QALoopStatus.FIXING
        attempt = qa.add_fix_attempt(description)
        
        if fixes:
            attempt.fixes_applied = fixes
        
        return attempt
    
    def mark_fix_successful(
        self,
        attempt: FixAttempt,
        tests_to_retry: List[str] = None
    ) -> None:
        """
        Mark fix as successful.
        
        Args:
            attempt: The fix attempt
            tests_to_retry: Tests to retry
        """
        attempt.success = True
        if tests_to_retry:
            attempt.tests_to_retry = tests_to_retry
    
    def is_merge_ready(self, qa: UltraQA) -> bool:
        """
        Check if merge ready.
        
        Args:
            qa: The QA session
            
        Returns:
            True if all tests pass
        """
        return qa.is_merge_ready()
    
    def mark_qa_complete(self, qa: UltraQA) -> None:
        """
        Mark QA as complete.
        
        Args:
            qa: The QA session
        """
        qa.mark_completed()
    
    def generate_report(self, qa: UltraQA) -> UltraQAReport:
        """
        Generate QA report.
        
        Args:
            qa: The QA session
            
        Returns:
            An UltraQAReport
        """
        passed = qa.get_passed_tests()
        failed = qa.get_failed_tests()
        
        summary = (
            f"QA Complete: {len(passed)} passed, {len(failed)} failed. "
            f"{'✓ Merge Ready' if qa.is_merge_ready() else '✗ Not Merge Ready'}"
        )
        
        report = UltraQAReport(
            title=qa.title,
            status=qa.status,
            total_tests=len(qa.verification_results),
            passed_tests=len(passed),
            failed_tests=len(failed),
            merge_ready=qa.is_merge_ready(),
            completed_at=qa.completed_at,
            summary=summary
        )
        
        return report
    
    def get_qa_session(self, title: str) -> Optional[UltraQA]:
        """Get a QA session by title."""
        return self.qa_sessions.get(title)
    
    def get_all_qa_sessions(self) -> List[UltraQA]:
        """Get all QA sessions."""
        return list(self.qa_sessions.values())
