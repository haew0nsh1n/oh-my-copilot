"""Tests for ultrawork skill."""
import pytest
from skills import UltraworkSkill
from domain import UltraworkStatus, LaneStatus


class TestUltraworkBasics:
    def test_skill_created(self):
        assert UltraworkSkill().name == "ultrawork"

    def test_create_session(self):
        skill = UltraworkSkill()
        session = skill.create_session("Build auth in parallel")
        assert session.goal == "Build auth in parallel"
        assert session.status == UltraworkStatus.RUNNING

    def test_empty_goal_raises(self):
        skill = UltraworkSkill()
        with pytest.raises(ValueError):
            skill.create_session("")


class TestLanes:
    def test_add_lane(self):
        skill = UltraworkSkill()
        session = skill.create_session("Goal")
        lane = skill.add_lane(session, "lane-1", "Implement backend", worker_hint="executor")
        assert lane.lane_id == "lane-1"
        assert len(session.lanes) == 1

    def test_start_lane(self):
        skill = UltraworkSkill()
        session = skill.create_session("Goal")
        lane = skill.add_lane(session, "lane-1", "Task")
        skill.start_lane(lane)
        assert lane.status == LaneStatus.ACTIVE

    def test_complete_lane(self):
        skill = UltraworkSkill()
        session = skill.create_session("Goal")
        lane = skill.add_lane(session, "lane-1", "Task")
        skill.start_lane(lane)
        skill.complete_lane(lane, "Done")
        assert lane.status == LaneStatus.DONE
        assert lane.output == "Done"

    def test_fail_lane(self):
        skill = UltraworkSkill()
        session = skill.create_session("Goal")
        lane = skill.add_lane(session, "lane-1", "Task")
        skill.fail_lane(lane, "Error occurred")
        assert lane.status == LaneStatus.FAILED

    def test_completion_rate(self):
        skill = UltraworkSkill()
        session = skill.create_session("Goal")
        l1 = skill.add_lane(session, "l1", "T1")
        l2 = skill.add_lane(session, "l2", "T2")
        skill.complete_lane(l1)
        assert session.completion_rate() == 0.5


class TestUltraworkReport:
    def test_generate_report(self):
        skill = UltraworkSkill()
        session = skill.create_session("Goal")
        l1 = skill.add_lane(session, "l1", "T1")
        l2 = skill.add_lane(session, "l2", "T2")
        skill.complete_lane(l1)
        skill.complete_session(session)
        report = skill.generate_report(session)
        assert report.total_lanes == 2
        assert report.completed_lanes == 1
        assert report.status == UltraworkStatus.COMPLETED
