"""Tests for rate limit wait skill."""

from skills import RateLimitWaitSkill
from domain import WaitAction, WaitStatus


class TestRateLimitWaitBasics:
    """Test rate-limit wait workflow behavior."""

    def test_skill_can_check_wait_status(self):
        """Rate limit wait can report a check result."""
        skill = RateLimitWaitSkill()

        result = skill.check_status()

        assert skill.name == "rate-limit-wait"
        assert result.action == WaitAction.CHECK
        assert result.status == WaitStatus.READY
        assert "rate limit" in result.guidance.lower()

    def test_skill_can_prepare_auto_resume_start(self):
        """Rate limit wait can prepare auto-resume start."""
        skill = RateLimitWaitSkill()

        result = skill.start_auto_resume()

        assert result.action == WaitAction.START
        assert result.status == WaitStatus.PREPARED
        assert "auto-resume" in result.guidance.lower()

    def test_skill_can_prepare_auto_resume_stop(self):
        """Rate limit wait can prepare auto-resume stop."""
        skill = RateLimitWaitSkill()

        result = skill.stop_auto_resume()

        assert result.action == WaitAction.STOP
        assert result.status == WaitStatus.PREPARED

    def test_skill_can_save_wait_state(self, tmp_path):
        """Rate limit wait persists local wait state."""
        skill = RateLimitWaitSkill()
        result = skill.start_auto_resume()

        saved = skill.save_state(result, tmp_path)

        assert saved.path == tmp_path / "wait.json"
        text = saved.path.read_text()
        assert '"action": "start"' in text
        assert '"status": "prepared"' in text

    def test_skill_can_load_wait_state(self, tmp_path):
        """Rate limit wait restores local wait state."""
        skill = RateLimitWaitSkill()
        result = skill.start_auto_resume()
        skill.save_state(result, tmp_path)

        loaded = skill.load_state(tmp_path)

        assert loaded.action == WaitAction.START
        assert loaded.status == WaitStatus.PREPARED
        assert "auto-resume" in loaded.guidance.lower()
