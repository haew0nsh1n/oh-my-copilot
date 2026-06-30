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
        "omp: source parity",
    } <= labels


def test_autocopilot_prompt_uses_bridge_and_tasks():
    """Autocopilot prompt tells Copilot to use bridge state and VS Code tasks."""
    prompt = Path(".github/prompts/autocopilot.prompt.md").read_text(encoding="utf-8")

    assert "omp bridge status --json" in prompt
    assert ".vscode/tasks.json" in prompt
    assert "repeat until" in prompt.lower()


def test_autocopilot_prompt_defines_full_surface_audit_loop():
    """Autocopilot prompt prevents early stops by requiring exhaustive surface checks."""
    prompt = Path(".github/prompts/autocopilot.prompt.md").read_text(encoding="utf-8")

    assert "Full-Surface Audit Manifest" in prompt
    assert "Do not stop after a single green test" in prompt
    assert "Surface parity is not filename parity" in prompt
    assert "implementation method" in prompt
    assert "skills/" in prompt
    assert "commands/" in prompt
    assert "agents/" in prompt
    assert "hooks/" in prompt
    assert "templates/hooks/" in prompt
    assert "missions/" in prompt
    assert "python -m cli source-parity --json" in prompt
    assert "python -m cli doctor --strict" in prompt


def test_project_docs_define_autopilot_completion_policy():
    """Core docs explain how autopilot must continue until full parity evidence is green."""
    docs = {
        "AGENTS.md": Path("AGENTS.md").read_text(encoding="utf-8"),
        "BRIEF.md": Path("BRIEF.md").read_text(encoding="utf-8"),
        "CONTEXT.md": Path("CONTEXT.md").read_text(encoding="utf-8"),
    }

    assert "Full-Surface Audit Manifest" in docs["AGENTS.md"]
    assert "파일 이름이 같다는 사실만으로 parity를 선언하지 않습니다" in docs["AGENTS.md"]
    assert "Autopilot Completion Policy" in docs["BRIEF.md"]
    assert "Full-surface audit" in docs["CONTEXT.md"]
    assert "Implementation-method parity" in docs["CONTEXT.md"]
    assert "source-parity" in docs["CONTEXT.md"]


def test_omc_full_audit_prompt_is_available():
    """Workspace includes a reusable prompt for full OMC parity audits."""
    prompt = Path(".github/prompts/omc-full-audit.prompt.md")

    assert prompt.exists()
    content = prompt.read_text(encoding="utf-8")
    assert "mode: agent" in content
    assert "Always Read First" in content
    assert "Full-Surface Audit Manifest" in content
    assert "Compare OMC implementation method" in content
    assert "python -m cli source-parity --json" in content