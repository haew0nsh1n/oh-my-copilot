"""Tests for notification callback configuration skill."""

from skills import NotificationConfigSkill
from domain import NotificationChannel, NotificationConfigStatus


class TestNotificationConfigBasics:
    """Test notification callback configuration."""

    def test_skill_can_prepare_stop_callback_config(self):
        """Notification config prepares a stop callback target."""
        skill = NotificationConfigSkill()

        config = skill.prepare_stop_callback("telegram", ["@alice", "bob"])

        assert skill.name == "notification-config"
        assert config.channel == NotificationChannel.TELEGRAM
        assert config.status == NotificationConfigStatus.PREPARED
        assert config.tag_list == ["@alice", "@bob"]
        assert "telegram" in config.command_preview

    def test_skill_can_save_stop_callback_config_without_secrets(self, tmp_path):
        """Notification config persists non-secret callback settings."""
        skill = NotificationConfigSkill()
        config = skill.prepare_stop_callback("telegram", ["@alice", "bob"])

        saved = skill.save_config(config, tmp_path)

        assert saved.path == tmp_path / "notifications.json"
        text = saved.path.read_text()
        assert '"channel": "telegram"' in text
        assert '"@bob"' in text
        assert "token" not in text

    def test_skill_can_load_stop_callback_config(self, tmp_path):
        """Notification config restores non-secret callback settings."""
        skill = NotificationConfigSkill()
        config = skill.prepare_stop_callback("telegram", ["@alice", "bob"])
        skill.save_config(config, tmp_path)

        loaded = skill.load_config(tmp_path)

        assert loaded.channel == NotificationChannel.TELEGRAM
        assert loaded.tag_list == ["@alice", "@bob"]
        assert loaded.status == NotificationConfigStatus.PREPARED
