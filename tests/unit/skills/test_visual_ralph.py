"""Tests for visual ralph skill."""
import pytest
from skills import VisualRalphSkill
from domain import VisualRalphStatus


class TestVisualRalphBasics:
    def test_skill_created(self):
        assert VisualRalphSkill().name == "visual_ralph"

    def test_create_session(self):
        skill = VisualRalphSkill()
        session = skill.create_session("Build login UI", "Reference design doc", threshold=90.0)
        assert session.task_description == "Build login UI"
        assert session.threshold == 90.0

    def test_empty_task_raises(self):
        with pytest.raises(ValueError):
            VisualRalphSkill().create_session("", "ref")


class TestIterations:
    def test_start_iteration(self):
        skill = VisualRalphSkill()
        session = skill.create_session("Task", "Ref")
        iteration = skill.start_iteration(session, "First attempt")
        assert iteration.iteration_number == 1
        assert session.status == VisualRalphStatus.IMPLEMENTING

    def test_score_passing_iteration(self):
        skill = VisualRalphSkill()
        session = skill.create_session("Task", "Ref")
        iteration = skill.start_iteration(session, "Attempt")
        skill.score_iteration(session, iteration, score=92.0, notes="Looks good")
        assert iteration.passed
        assert iteration.score == 92.0

    def test_score_failing_iteration(self):
        skill = VisualRalphSkill()
        session = skill.create_session("Task", "Ref")
        iteration = skill.start_iteration(session, "Attempt")
        skill.score_iteration(session, iteration, score=60.0)
        assert not iteration.passed
        assert session.status == VisualRalphStatus.REFINING

    def test_multiple_iterations_best_score(self):
        skill = VisualRalphSkill()
        session = skill.create_session("Task", "Ref")
        i1 = skill.start_iteration(session, "Attempt 1")
        skill.score_iteration(session, i1, score=70.0)
        i2 = skill.start_iteration(session, "Attempt 2")
        skill.score_iteration(session, i2, score=95.0)
        assert session.best_score() == 95.0


class TestCompletion:
    def test_is_passing(self):
        skill = VisualRalphSkill()
        session = skill.create_session("Task", "Ref")
        iteration = skill.start_iteration(session, "Attempt")
        skill.score_iteration(session, iteration, score=91.0)
        assert skill.is_passing(session)

    def test_complete_session(self):
        skill = VisualRalphSkill()
        session = skill.create_session("Task", "Ref")
        skill.complete(session)
        assert session.status == VisualRalphStatus.COMPLETED

    def test_fail_session(self):
        skill = VisualRalphSkill()
        session = skill.create_session("Task", "Ref")
        skill.fail(session)
        assert session.status == VisualRalphStatus.FAILED


class TestVisualRalphReport:
    def test_generate_report(self):
        skill = VisualRalphSkill()
        session = skill.create_session("Task", "Ref", threshold=90.0)
        i = skill.start_iteration(session, "Attempt")
        skill.score_iteration(session, i, score=95.0)
        skill.complete(session)
        report = skill.generate_report(session)
        assert report.passed
        assert report.best_score == 95.0
        assert report.total_iterations == 1
