"""Tests for OMP state summary skill."""

import json

from skills import StateSummarySkill


class TestStateSummaryBasics:
    """Test local OMP state summary."""

    def test_skill_summarizes_empty_state_root(self, tmp_path):
        """State summary handles an empty state root."""
        skill = StateSummarySkill()

        summary = skill.summarize(tmp_path)

        assert skill.name == "state-summary"
        assert summary.total_files == 0
        assert summary.wait_state == "missing"
        assert summary.notification_channel == "missing"
        assert summary.team_controls == []

    def test_skill_summarizes_saved_state_files(self, tmp_path):
        """State summary reads saved wait, notification, and team state."""
        (tmp_path / "wait.json").write_text(json.dumps({"action": "start"}))
        (tmp_path / "notifications.json").write_text(json.dumps({"channel": "telegram"}))
        (tmp_path / "team-auth-review.json").write_text(json.dumps({
            "action": "shutdown",
            "team_name": "auth-review",
        }))

        summary = StateSummarySkill().summarize(tmp_path)

        assert summary.total_files == 3
        assert summary.wait_state == "start"
        assert summary.notification_channel == "telegram"
        assert summary.team_controls == ["auth-review:shutdown"]
