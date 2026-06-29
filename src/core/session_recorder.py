"""Sanitized local session recorder."""

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class SessionRecordArtifact:
    """Persisted session record artifact."""

    path: Path


class SessionRecorder:
    """Record sanitized CLI execution summaries under .omp/sessions."""

    def __init__(self, sessions_root: Path | str):
        """Initialize recorder with a sessions root."""
        self.sessions_root = Path(sessions_root)

    def record_command(
        self,
        command: str,
        status: str,
        exit_code: int | None,
        friction_type: str = "",
        friction_summary: str = "",
        raw_prompt: str = "",
        raw_output: str = "",
    ) -> SessionRecordArtifact:
        """Record sanitized command metadata without raw prompts or raw tool output."""
        self.sessions_root.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
        path = self.sessions_root / f"{timestamp}.json"
        friction_signals = []
        if friction_type and friction_summary:
            friction_signals.append({"type": friction_type, "summary": friction_summary})

        path.write_text(
            json.dumps(
                {
                    "command": command,
                    "status": status,
                    "exit_code": exit_code,
                    "friction_signals": friction_signals,
                    "recorded_at": timestamp,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )
        return SessionRecordArtifact(path=path)
