"""Tests for visual verdict skill."""
import pytest
from skills import VisualVerdictSkill
from domain import VerdictStatus


class TestVisualVerdictBasics:
    def test_skill_created(self):
        assert VisualVerdictSkill().name == "visual_verdict"

    def test_create_session(self):
        skill = VisualVerdictSkill()
        session = skill.create_session("Match login page", threshold=90.0)
        assert session.task_description == "Match login page"
        assert session.threshold == 90.0

    def test_empty_task_raises(self):
        with pytest.raises(ValueError):
            VisualVerdictSkill().create_session("")


class TestVisualComparison:
    def test_comparison_pass(self):
        skill = VisualVerdictSkill()
        session = skill.create_session("Task")
        ref = skill.create_asset("ref", "reference", "/images/ref.png")
        ss = skill.create_asset("ss", "screenshot", "/images/ss.png")
        comparison = skill.compare(session, ref, ss, score=95.0)
        assert comparison.verdict == VerdictStatus.PASS
        assert comparison.passed()

    def test_comparison_fail(self):
        skill = VisualVerdictSkill()
        session = skill.create_session("Task")
        ref = skill.create_asset("ref", "reference", "/ref.png")
        ss = skill.create_asset("ss", "screenshot", "/ss.png")
        comparison = skill.compare(session, ref, ss, score=60.0)
        assert comparison.verdict == VerdictStatus.FAIL
        assert not comparison.passed()

    def test_needs_review_range(self):
        skill = VisualVerdictSkill()
        session = skill.create_session("Task")
        ref = skill.create_asset("ref", "reference", "/ref.png")
        ss = skill.create_asset("ss", "screenshot", "/ss.png")
        comparison = skill.compare(session, ref, ss, score=75.0)
        assert comparison.verdict == VerdictStatus.NEEDS_REVIEW


class TestVisualVerdictSession:
    def test_all_pass_when_all_pass(self):
        skill = VisualVerdictSkill()
        session = skill.create_session("Task")
        ref = skill.create_asset("r", "reference", "/r.png")
        ss = skill.create_asset("s", "screenshot", "/s.png")
        skill.compare(session, ref, ss, score=92.0)
        assert session.all_pass()

    def test_needs_retry_on_fail(self):
        skill = VisualVerdictSkill()
        session = skill.create_session("Task")
        ref = skill.create_asset("r", "reference", "/r.png")
        ss = skill.create_asset("s", "screenshot", "/s.png")
        skill.compare(session, ref, ss, score=50.0)
        assert skill.needs_retry(session)

    def test_average_score(self):
        skill = VisualVerdictSkill()
        session = skill.create_session("Task")
        ref = skill.create_asset("r", "reference", "/r.png")
        ss1 = skill.create_asset("s1", "screenshot", "/s1.png")
        ss2 = skill.create_asset("s2", "screenshot", "/s2.png")
        skill.compare(session, ref, ss1, score=80.0)
        skill.compare(session, ref, ss2, score=100.0)
        assert session.average_score() == 90.0

    def test_generate_report(self):
        skill = VisualVerdictSkill()
        session = skill.create_session("Task")
        ref = skill.create_asset("r", "reference", "/r.png")
        ss = skill.create_asset("s", "screenshot", "/s.png")
        skill.compare(session, ref, ss, score=95.0)
        skill.complete(session)
        report = skill.generate_report(session)
        assert report.passed
        assert report.average_score == 95.0
