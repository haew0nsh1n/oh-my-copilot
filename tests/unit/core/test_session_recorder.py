"""Tests for session recording."""

import json

from core import SessionRecorder


class TestSessionRecorder:
    """Test sanitized session recording."""

    def test_records_sanitized_command_summary(self, tmp_path):
        """Session recorder stores command metadata without raw prompt or output."""
        recorder = SessionRecorder(tmp_path)

        record = recorder.record_command(
            command="omp ask --execute codex",
            status="blocked",
            exit_code=None,
            friction_type="operator-friction",
            friction_summary="provider executable missing",
            raw_prompt="review this secret patch",
            raw_output="very long raw provider output",
        )

        data = json.loads(record.path.read_text())
        assert data["command"] == "omp ask --execute codex"
        assert data["status"] == "blocked"
        assert data["exit_code"] is None
        assert data["friction_signals"] == [
            {"type": "operator-friction", "summary": "provider executable missing"}
        ]
        assert "raw_prompt" not in data
        assert "raw_output" not in data
