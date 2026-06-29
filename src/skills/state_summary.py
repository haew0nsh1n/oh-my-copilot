"""State summary skill for local OMP runtime state."""

import json
from pathlib import Path

from domain import StateSummary


class StateSummarySkill:
    """Summarize persisted local OMP state without exposing raw session content."""

    name = "state-summary"
    description = "Summarize persisted .omp state for HUD and diagnostics"

    def summarize(self, state_root: Path | str) -> StateSummary:
        """Summarize known OMP state files from a state root."""
        root = Path(state_root)
        files = list(root.glob("*.json")) if root.exists() else []
        wait_state = "missing"
        notification_channel = "missing"
        team_controls: list[str] = []

        wait_path = root / "wait.json"
        if wait_path.exists():
            wait_state = json.loads(wait_path.read_text()).get("action", "unknown")

        notifications_path = root / "notifications.json"
        if notifications_path.exists():
            notification_channel = json.loads(notifications_path.read_text()).get(
                "channel", "unknown"
            )

        for path in sorted(root.glob("team-*.json")) if root.exists() else []:
            data = json.loads(path.read_text())
            team_controls.append(f"{data.get('team_name', 'unknown')}:{data.get('action', 'unknown')}")

        return StateSummary(
            total_files=len(files),
            wait_state=wait_state,
            notification_channel=notification_channel,
            team_controls=team_controls,
        )
