"""Domain model for QA and verification loops."""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime


class TestStatus(str, Enum):
    """Status of a test."""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"


class QALoopStatus(str, Enum):
    """Status of QA loop."""
    STARTING = "starting"
    TESTING = "testing"
    VERIFYING = "verifying"
    FIXING = "fixing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class TestCase:
    """A test case."""
    name: str
    description: str
    test_steps: List[str] = field(default_factory=list)
    expected_result: str = ""
    status: TestStatus = TestStatus.PENDING
    error: str = ""
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class VerificationResult:
    """Result of verification."""
    test_case: TestCase
    passed: bool
    evidence: str = ""
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class FixAttempt:
    """An attempt to fix failures."""
    description: str
    fixes_applied: List[str] = field(default_factory=list)
    tests_to_retry: List[str] = field(default_factory=list)
    success: bool = False
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class UltraQA:
    """Test/Verify/Fix loop for merge readiness."""
    title: str
    description: str = ""
    status: QALoopStatus = QALoopStatus.STARTING
    test_cases: List[TestCase] = field(default_factory=list)
    verification_results: List[VerificationResult] = field(default_factory=list)
    fix_attempts: List[FixAttempt] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    merge_ready: bool = False
    
    def __post_init__(self):
        """Validate QA."""
        if not self.title or not self.title.strip():
            raise ValueError("QA title cannot be empty")
    
    def add_test_case(self, name: str, description: str) -> TestCase:
        """Add a test case."""
        test = TestCase(
            name=name,
            description=description
        )
        self.test_cases.append(test)
        return test
    
    def add_verification_result(self, test_case: TestCase, passed: bool, evidence: str = "") -> VerificationResult:
        """Add verification result."""
        result = VerificationResult(
            test_case=test_case,
            passed=passed,
            evidence=evidence
        )
        self.verification_results.append(result)
        return result
    
    def add_fix_attempt(self, description: str) -> FixAttempt:
        """Add a fix attempt."""
        attempt = FixAttempt(description=description)
        self.fix_attempts.append(attempt)
        return attempt
    
    def get_failed_tests(self) -> List[VerificationResult]:
        """Get failed test results."""
        return [r for r in self.verification_results if not r.passed]
    
    def get_passed_tests(self) -> List[VerificationResult]:
        """Get passed test results."""
        return [r for r in self.verification_results if r.passed]
    
    def is_merge_ready(self) -> bool:
        """Check if merge ready (all tests pass)."""
        if not self.verification_results:
            return False
        return all(r.passed for r in self.verification_results)
    
    def mark_completed(self) -> None:
        """Mark QA as completed."""
        self.status = QALoopStatus.COMPLETED
        self.completed_at = datetime.now()
        self.merge_ready = self.is_merge_ready()


@dataclass
class UltraQAReport:
    """Report from QA."""
    title: str
    status: QALoopStatus
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    merge_ready: bool = False
    completed_at: Optional[datetime] = None
    summary: str = ""
