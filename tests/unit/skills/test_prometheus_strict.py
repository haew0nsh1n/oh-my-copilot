"""Tests for prometheus-strict skill."""

import pytest
from skills import PrometheusStrictSkill
from domain import ValidationRuleType, RiskLevel


class TestPrometheusStrictBasics:
    """Test basic prometheus-strict skill functionality."""
    
    def test_skill_can_be_created(self):
        """RED: Skill can be instantiated."""
        skill = PrometheusStrictSkill()
        assert skill is not None
    
    def test_skill_has_name(self):
        """RED: Skill has a name."""
        skill = PrometheusStrictSkill()
        assert skill.name == "prometheus_strict"


class TestRuleCreation:
    """Test validation rule creation."""
    
    def test_create_rule(self):
        """RED: Can create a validation rule."""
        skill = PrometheusStrictSkill()
        
        rule = skill.create_rule(
            "security_check",
            "All endpoints must use HTTPS",
            rule_type=ValidationRuleType.REQUIREMENT,
            error_message="HTTPS is mandatory"
        )
        
        assert rule.name == "security_check"
        assert rule.rule_type == ValidationRuleType.REQUIREMENT
    
    def test_get_rule(self):
        """RED: Can retrieve a rule."""
        skill = PrometheusStrictSkill()
        rule = skill.create_rule("test_rule", "Test")
        
        retrieved = skill.get_rule("test_rule")
        assert retrieved.name == "test_rule"


class TestStressTests:
    """Test stress test creation."""
    
    def test_create_stress_test(self):
        """RED: Can create a stress test."""
        skill = PrometheusStrictSkill()
        
        test = skill.create_stress_test(
            "high_load_test",
            "Test plan under high load",
            "1000 concurrent requests",
            "System remains responsive"
        )
        
        assert test.name == "high_load_test"
        assert test.scenario == "1000 concurrent requests"
    
    def test_get_stress_test(self):
        """RED: Can retrieve a stress test."""
        skill = PrometheusStrictSkill()
        test = skill.create_stress_test("test", "desc", "scenario", "outcome")
        
        retrieved = skill.get_stress_test("test")
        assert retrieved.name == "test"


class TestValidation:
    """Test plan validation."""
    
    def test_validate_plan(self):
        """RED: Can validate a plan."""
        skill = PrometheusStrictSkill()
        
        skill.create_rule("rule1", "Test rule 1", ValidationRuleType.REQUIREMENT)
        
        report = skill.validate_plan("My Plan", rule_names=["rule1"])
        
        assert report.plan_title == "My Plan"
        assert len(report.validation_results) == 1
    
    def test_custom_validator(self):
        """RED: Can use custom validators."""
        skill = PrometheusStrictSkill()
        
        skill.create_rule("exists", "Must exist")
        
        def always_pass(rule):
            return True
        
        report = skill.validate_plan("Plan", custom_validator=always_pass)
        
        assert report.overall_passed


class TestReporting:
    """Test validation reporting."""
    
    def test_report_shows_failed_rules(self):
        """RED: Report shows failed rules."""
        skill = PrometheusStrictSkill()
        
        skill.create_rule("must_pass", "Required", ValidationRuleType.REQUIREMENT)
        
        def always_fail(rule):
            return False
        
        report = skill.validate_plan("Plan", custom_validator=always_fail)
        
        assert not report.overall_passed
        assert "must_pass" in report.critical_issues
    
    def test_separate_warnings_and_requirements(self):
        """RED: Can distinguish warnings from requirements."""
        skill = PrometheusStrictSkill()
        
        skill.create_rule("req1", "Required", ValidationRuleType.REQUIREMENT)
        skill.create_rule("warn1", "Warning", ValidationRuleType.WARNING)
        
        def always_fail(rule):
            return False
        
        report = skill.validate_plan("Plan", custom_validator=always_fail)
        
        assert len(report.critical_issues) == 1  # Only requirement
        assert len(report.warnings) == 1  # Only warning
