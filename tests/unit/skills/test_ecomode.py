"""Tests for ecomode skill."""
import pytest
from skills import EcomodeSkill
from domain import ModelTier, TaskComplexity


class TestEcomodeBasics:
    def test_skill_created(self):
        assert EcomodeSkill().name == "ecomode"

    def test_create_session(self):
        skill = EcomodeSkill()
        session = skill.create_session("Minimize costs")
        assert session.goal == "Minimize costs"

    def test_empty_goal_raises(self):
        with pytest.raises(ValueError):
            EcomodeSkill().create_session("")


class TestRouting:
    def test_route_simple_to_low(self):
        skill = EcomodeSkill()
        session = skill.create_session("Goal")
        tier = skill.route(session, "format code", TaskComplexity.SIMPLE)
        assert tier == ModelTier.LOW

    def test_route_moderate_to_medium(self):
        skill = EcomodeSkill()
        session = skill.create_session("Goal")
        tier = skill.route(session, "write unit test", TaskComplexity.MODERATE)
        assert tier == ModelTier.MEDIUM

    def test_route_complex_to_high(self):
        skill = EcomodeSkill()
        session = skill.create_session("Goal")
        tier = skill.route(session, "design architecture", TaskComplexity.COMPLEX)
        assert tier == ModelTier.HIGH


class TestRules:
    def test_add_rule(self):
        skill = EcomodeSkill()
        session = skill.create_session("Goal")
        rule = skill.add_rule(session, "format*", ModelTier.LOW, "Formatting is cheap")
        assert rule.recommended_tier == ModelTier.LOW
        assert len(session.routing_rules) == 1


class TestTokenUsage:
    def test_record_usage(self):
        skill = EcomodeSkill()
        session = skill.create_session("Goal")
        usage = skill.record_usage(session, "format file", ModelTier.LOW, 100)
        assert usage.model_tier == ModelTier.LOW
        assert usage.cost_saving_vs_high == 90.0  # 1.0 - 0.1 = 0.9 = 90%

    def test_record_medium_savings(self):
        skill = EcomodeSkill()
        session = skill.create_session("Goal")
        usage = skill.record_usage(session, "write test", ModelTier.MEDIUM, 500)
        assert usage.cost_saving_vs_high == 60.0  # 1.0 - 0.4 = 0.6 = 60%

    def test_generate_report(self):
        skill = EcomodeSkill()
        session = skill.create_session("Goal")
        skill.record_usage(session, "task1", ModelTier.LOW, 100)
        skill.record_usage(session, "task2", ModelTier.MEDIUM, 300)
        report = skill.generate_report(session)
        assert report.total_tasks == 2
        assert report.total_estimated_tokens == 400
