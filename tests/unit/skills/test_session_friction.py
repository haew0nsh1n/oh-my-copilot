"""Tests for session friction reporting skill."""

from skills import SessionFrictionSkill
from domain import FrictionSignalType


class TestSessionFrictionBasics:
    """Test local session friction reporting."""

    def test_skill_can_generate_empty_report(self):
        """Session friction report summarizes an empty time window."""
        skill = SessionFrictionSkill()

        report = skill.generate_report("24h")

        assert skill.name == "session-friction"
        assert report.since == "24h"
        assert report.total_signals == 0
        assert "0 friction signals" in report.summary

    def test_skill_can_add_context_bloat_signal(self):
        """Session friction report counts context bloat signals."""
        skill = SessionFrictionSkill()
        session = skill.create_session("24h")

        skill.add_signal(session, FrictionSignalType.CONTEXT_BLOAT, "large context summary")
        report = skill.generate_report_from_session(session)

        assert report.total_signals == 1
        assert report.signal_breakdown["context-bloat"] == 1
