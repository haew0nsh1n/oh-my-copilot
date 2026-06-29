"""Tests for swarm skill."""
import pytest
from skills import SwarmSkill
from domain import SwarmStatus


class TestSwarmBasics:
    def test_skill_created(self):
        assert SwarmSkill().name == "swarm"

    def test_create_session(self):
        skill = SwarmSkill()
        session = skill.create_session("Swarm execution", worker_count=3)
        assert session.goal == "Swarm execution"
        assert len(session.workers) == 3
        assert session.status == SwarmStatus.RUNNING

    def test_empty_goal_raises(self):
        with pytest.raises(ValueError):
            SwarmSkill().create_session("")


class TestSwarmTasks:
    def test_add_task(self):
        skill = SwarmSkill()
        session = skill.create_session("Goal")
        task = skill.add_task(session, "task-1", "Implement feature A")
        assert task.task_id == "task-1"
        assert len(session.tasks) == 1

    def test_assign_task(self):
        skill = SwarmSkill()
        session = skill.create_session("Goal")
        task = skill.add_task(session, "t1", "Task 1")
        worker = session.workers[0]
        skill.assign_task(task, worker)
        assert task.assigned_to == worker.worker_id

    def test_complete_task(self):
        skill = SwarmSkill()
        session = skill.create_session("Goal")
        task = skill.add_task(session, "t1", "Task 1")
        skill.complete_task(task, "Done")
        assert task.completed
        assert task.output == "Done"

    def test_completion_rate(self):
        skill = SwarmSkill()
        session = skill.create_session("Goal", worker_count=2)
        t1 = skill.add_task(session, "t1", "T1")
        t2 = skill.add_task(session, "t2", "T2")
        skill.complete_task(t1)
        assert session.completion_rate() == 0.5


class TestSwarmReport:
    def test_generate_report(self):
        skill = SwarmSkill()
        session = skill.create_session("Goal", worker_count=2)
        t1 = skill.add_task(session, "t1", "T1")
        skill.complete_task(t1, "OK")
        skill.complete_session(session)
        report = skill.generate_report(session)
        assert report.total_tasks == 1
        assert report.completed_tasks == 1
        assert report.status == SwarmStatus.COMPLETED
