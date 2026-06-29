"""Tests for VS Code Copilot-native workflow configuration."""

import json
from pathlib import Path


def test_vscode_tasks_cover_omp_runtime_workflow():
    """Workspace tasks expose repeatable OMP validation and bridge commands."""
    tasks_path = Path(".vscode/tasks.json")

    assert tasks_path.exists()
    tasks = json.loads(tasks_path.read_text(encoding="utf-8"))
    labels = {task["label"] for task in tasks["tasks"]}

    assert {
        "omp: doctor strict",
        "omp: pytest",
        "omp: hud",
        "omp: bridge status",
        "omp: ultragoal status",
        "omp: e2e runtime parity",
    } <= labels


def test_autocopilot_prompt_uses_bridge_and_tasks():
    """Autocopilot prompt tells Copilot to use bridge state and VS Code tasks."""
    prompt = Path(".github/prompts/autocopilot.prompt.md").read_text(encoding="utf-8")

    assert "omp bridge status --json" in prompt
    assert ".vscode/tasks.json" in prompt
    assert "repeat until" in prompt.lower()