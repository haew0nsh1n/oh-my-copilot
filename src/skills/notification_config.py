"""Notification callback configuration skill."""

import json
from pathlib import Path

from domain import (
    NotificationCallbackConfig,
    NotificationChannel,
    NotificationConfigArtifact,
)


class NotificationConfigSkill:
    """Prepare notification callback configuration without collecting secrets."""

    name = "notification-config"
    description = "Prepare stop-callback notification configuration for supported channels"

    def prepare_stop_callback(
        self,
        channel: str,
        tag_list: list[str] | None = None,
    ) -> NotificationCallbackConfig:
        """Prepare a notification callback configuration request."""
        notification_channel = NotificationChannel(channel)
        normalized_tags = [self._normalize_tag(tag) for tag in tag_list or []]
        return NotificationCallbackConfig(
            channel=notification_channel,
            tag_list=normalized_tags,
            command_preview=f"omp config-stop-callback {notification_channel.value}",
        )

    def _normalize_tag(self, tag: str) -> str:
        """Normalize human tag input without channel-specific secrets."""
        if tag.startswith("@") or tag.startswith("<"):
            return tag
        return f"@{tag}"

    def save_config(
        self,
        config: NotificationCallbackConfig,
        state_root: Path | str,
    ) -> NotificationConfigArtifact:
        """Persist non-secret notification callback settings."""
        root = Path(state_root)
        root.mkdir(parents=True, exist_ok=True)
        path = root / "notifications.json"
        path.write_text(
            json.dumps(
                {
                    "channel": config.channel.value,
                    "status": config.status.value,
                    "tag_list": config.tag_list,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )
        return NotificationConfigArtifact(channel=config.channel, path=path)
