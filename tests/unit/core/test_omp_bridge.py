"""Tests for the local OMP bridge used by Copilot-native workflows."""

import json

from core import OmpBridge


def test_bridge_reports_workspace_status(tmp_path):
    """Bridge status summarizes local OMP state, artifacts, skills, and commands."""
    (tmp_path / ".omp" / "state").mkdir(parents=True)
    (tmp_path / ".omp" / "artifacts" / "ask").mkdir(parents=True)
    (tmp_path / "skills" / "verify").mkdir(parents=True)
    (tmp_path / "commands").mkdir()
    (tmp_path / ".omp" / "state" / "wait.json").write_text('{"action":"start"}\n')
    (tmp_path / ".omp" / "artifacts" / "ask" / "codex.md").write_text("# ask\n")
    (tmp_path / "skills" / "verify" / "SKILL.md").write_text("---\nname: verify\n---\n")
    (tmp_path / "commands" / "verify.md").write_text("---\ndescription: verify\n---\n")

    status = OmpBridge(tmp_path).status()

    assert status["state_root_exists"] is True
    assert status["state_files"] == ["wait.json"]
    assert status["artifact_commands"] == ["ask"]
    assert status["skill_bodies"] == 1
    assert status["command_bodies"] == 1


def test_bridge_reads_named_state(tmp_path):
    """Bridge can read a named .omp/state JSON file."""
    state_root = tmp_path / ".omp" / "state"
    state_root.mkdir(parents=True)
    (state_root / "autopilot.json").write_text(json.dumps({"status": "completed"}))

    state = OmpBridge(tmp_path).read_state("autopilot")

    assert state == {"status": "completed"}


def test_bridge_lists_artifacts(tmp_path):
    """Bridge lists artifacts for all commands or one command."""
    artifact_root = tmp_path / ".omp" / "artifacts" / "ask"
    artifact_root.mkdir(parents=True)
    (artifact_root / "codex.md").write_text("# ask\n")

    artifacts = OmpBridge(tmp_path).list_artifacts("ask")

    assert artifacts == [".omp/artifacts/ask/codex.md"]