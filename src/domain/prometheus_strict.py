"""Domain model for plan validation and hardening."""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime


class ValidationRuleType(str, Enum):
    """Type of validation rule."""
    REQUIREMENT = "requirement"  # Must be satisfied
    CONSTRAINT = "constraint"  # Must not be violated
    WARNING = "warning"  # Should be addressed
    SUGGESTION = "suggestion"  # Nice to have


class RiskLevel(str, Enum):
    """Risk severity level."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class ValidationRule:
    """A validation rule for plans."""
    name: str
    description: str
    rule_type: ValidationRuleType
    checker: str = ""  # Description of how to check
    error_message: str = ""
    
    def __post_init__(self):
        """Validate rule."""
        if not self.name or not self.name.strip():
            raise ValueError("Rule name cannot be empty")


@dataclass
class ValidationResult:
    """Result of validating a plan against a rule."""
    rule: ValidationRule
    passed: bool
    details: str = ""
    risk_level: RiskLevel = RiskLevel.LOW
    suggestions: List[str] = field(default_factory=list)


@dataclass
class StressTest:
    """A stress test for a plan."""
    name: str
    description: str
    scenario: str  # The scenario to test
    expected_outcome: str  # What should happen
    failure_modes: List[str] = field(default_factory=list)


@dataclass
class StressTestResult:
    """Result of a stress test."""
    test: StressTest
    passed: bool
    failure_points: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class ValidationReport:
    """Report from validating a plan."""
    plan_title: str
    validated_at: datetime = field(default_factory=datetime.now)
    validation_results: List[ValidationResult] = field(default_factory=list)
    stress_test_results: List[StressTestResult] = field(default_factory=list)
    overall_passed: bool = True
    critical_issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def get_passed_rules(self) -> List[ValidationResult]:
        """Get all passing validation results."""
        return [r for r in self.validation_results if r.passed]
    
    def get_failed_rules(self) -> List[ValidationResult]:
        """Get all failing validation results."""
        return [r for r in self.validation_results if not r.passed]
    
    def get_critical_issues(self) -> List[str]:
        """Get critical issues."""
        return self.critical_issues
    
    def passed_all_requirements(self) -> bool:
        """Check if all requirements are met."""
        failed = self.get_failed_rules()
        for result in failed:
            if result.rule.rule_type == ValidationRuleType.REQUIREMENT:
                return False
        return True
