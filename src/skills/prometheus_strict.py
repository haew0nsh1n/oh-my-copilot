"""Prometheus-Strict skill for plan validation."""

from typing import Callable, List, Dict
from datetime import datetime
from domain import (
    ValidationRule,
    ValidationRuleType,
    ValidationResult,
    RiskLevel,
    StressTest,
    StressTestResult,
    ValidationReport,
)


class PrometheusStrictSkill:
    """
    A skill for validating and hardening plans.
    
    This skill helps ensure plans are robust by validating against rules
    and stress-testing scenarios.
    """
    
    def __init__(self):
        """Initialize the skill."""
        self.name = "prometheus_strict"
        self.description = "Validate and harden plans with strict validation rules"
        self.rules: Dict[str, ValidationRule] = {}
        self.stress_tests: Dict[str, StressTest] = {}
    
    def create_rule(
        self,
        name: str,
        description: str,
        rule_type: ValidationRuleType = ValidationRuleType.REQUIREMENT,
        checker: str = "",
        error_message: str = ""
    ) -> ValidationRule:
        """
        Create a validation rule.
        
        Args:
            name: Rule name
            description: Rule description
            rule_type: Type of rule
            checker: How to check the rule
            error_message: Error message if failed
            
        Returns:
            A ValidationRule
        """
        rule = ValidationRule(
            name=name,
            description=description,
            rule_type=rule_type,
            checker=checker,
            error_message=error_message
        )
        self.rules[name] = rule
        return rule
    
    def create_stress_test(
        self,
        name: str,
        description: str,
        scenario: str,
        expected_outcome: str
    ) -> StressTest:
        """
        Create a stress test.
        
        Args:
            name: Test name
            description: Test description
            scenario: The scenario to test
            expected_outcome: Expected outcome
            
        Returns:
            A StressTest
        """
        test = StressTest(
            name=name,
            description=description,
            scenario=scenario,
            expected_outcome=expected_outcome
        )
        self.stress_tests[name] = test
        return test
    
    def validate_plan(
        self,
        plan_title: str,
        rule_names: List[str] = None,
        custom_validator: Callable = None
    ) -> ValidationReport:
        """
        Validate a plan against rules.
        
        Args:
            plan_title: Title of the plan
            rule_names: Specific rules to check (all if None)
            custom_validator: Custom validation function
            
        Returns:
            A ValidationReport
        """
        report = ValidationReport(plan_title=plan_title)
        
        # Get rules to check
        rules_to_check = self.rules.values()
        if rule_names:
            rules_to_check = [self.rules[r] for r in rule_names if r in self.rules]
        
        # Run validations
        for rule in rules_to_check:
            result = self._validate_rule(rule, custom_validator)
            report.validation_results.append(result)
            
            if not result.passed and rule.rule_type == ValidationRuleType.REQUIREMENT:
                report.critical_issues.append(rule.name)
                report.overall_passed = False
            
            if not result.passed and rule.rule_type == ValidationRuleType.WARNING:
                report.warnings.append(rule.name)
        
        return report
    
    def _validate_rule(
        self,
        rule: ValidationRule,
        custom_validator: Callable = None
    ) -> ValidationResult:
        """
        Validate a single rule.
        
        Args:
            rule: The rule to validate
            custom_validator: Custom validator function
            
        Returns:
            A ValidationResult
        """
        result = ValidationResult(
            rule=rule,
            passed=True  # Default to pass
        )
        
        if custom_validator:
            try:
                passed = custom_validator(rule)
                result.passed = passed
                if not passed:
                    result.details = rule.error_message
            except Exception as e:
                result.passed = False
                result.details = str(e)
        
        return result
    
    def stress_test_plan(
        self,
        plan_title: str,
        test_names: List[str] = None,
        scenario_validator: Callable = None
    ) -> List[StressTestResult]:
        """
        Stress test a plan with scenarios.
        
        Args:
            plan_title: Title of the plan
            test_names: Specific tests to run
            scenario_validator: Custom validator for scenarios
            
        Returns:
            List of StressTestResults
        """
        results = []
        
        # Get tests to run
        tests_to_run = self.stress_tests.values()
        if test_names:
            tests_to_run = [self.stress_tests[t] for t in test_names if t in self.stress_tests]
        
        # Run stress tests
        for test in tests_to_run:
            result = self._run_stress_test(test, scenario_validator)
            results.append(result)
        
        return results
    
    def _run_stress_test(
        self,
        test: StressTest,
        scenario_validator: Callable = None
    ) -> StressTestResult:
        """
        Run a single stress test.
        
        Args:
            test: The test to run
            scenario_validator: Custom validator
            
        Returns:
            A StressTestResult
        """
        result = StressTestResult(
            test=test,
            passed=True  # Default to pass
        )
        
        if scenario_validator:
            try:
                passed = scenario_validator(test)
                result.passed = passed
            except Exception as e:
                result.passed = False
                result.failure_points.append(str(e))
        
        return result
    
    def get_rule(self, name: str) -> ValidationRule:
        """Get a rule by name."""
        return self.rules.get(name)
    
    def get_all_rules(self) -> List[ValidationRule]:
        """Get all rules."""
        return list(self.rules.values())
    
    def get_stress_test(self, name: str) -> StressTest:
        """Get a stress test by name."""
        return self.stress_tests.get(name)
    
    def get_all_stress_tests(self) -> List[StressTest]:
        """Get all stress tests."""
        return list(self.stress_tests.values())
