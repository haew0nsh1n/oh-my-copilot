"""End-to-end runtime parity smoke tests for OMP CLI surfaces."""

import json
import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def run_omp(workspace: Path, *args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    """Run OMP through the public module entry point in an isolated workspace."""
    process_env = os.environ.copy()
    process_env.update(
        {
            "PYTHONPATH": str(REPO_ROOT / "src"),
        }
    )
    for key in [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_CODEX_DEPLOYMENT",
        "AZURE_OPENAI_API_VERSION",
        "AZURE_OPENAI_DEPLOYMENT",
    ]:
        process_env.pop(key, None)
    if env:
        process_env.update(env)

    return subprocess.run(
        [sys.executable, "-m", "cli", *args],
        cwd=workspace,
        env=process_env,
        text=True,
        capture_output=True,
        check=False,
    )


def assert_success(result: subprocess.CompletedProcess[str]) -> None:
    """Assert command success with useful failure output."""
    assert result.returncode == 0, result.stdout + result.stderr


def test_omp_runtime_surfaces_create_real_state_and_artifacts(tmp_path):
    """OMP runtime surfaces create inspectable state, artifacts, and generated code."""
    assert_success(run_omp(tmp_path, "setup"))

    doctor = run_omp(tmp_path, "doctor", "--strict", "--json")
    assert_success(doctor)
    doctor_report = json.loads(doctor.stdout)
    assert doctor_report["status"] == "operational"
    assert not [item for item in doctor_report["commands"] if item["status"] == "placeholder"]

    ask = run_omp(tmp_path, "ask", "--execute", "codex", "review", "runtime", "surface")
    assert_success(ask)
    assert (tmp_path / ".omp" / "artifacts" / "ask" / "codex.md").exists()
    assert list((tmp_path / ".omp" / "sessions").glob("*.json"))

    assert_success(run_omp(tmp_path, "wait", "daemon", "start"))
    assert json.loads((tmp_path / ".omp" / "state" / "wait.json").read_text())["action"] == "start"

    assert_success(run_omp(tmp_path, "team", "status", "runtime-check"))
    assert (tmp_path / ".omp" / "state" / "team-runtime-check.json").exists()

    assert_success(run_omp(tmp_path, "ultragoal", "웹소켓", "클라이언트", "생성"))
    assert_success(run_omp(tmp_path, "ultragoal", "execute"))
    assert (tmp_path / "src" / "core" / "websocket_client.py").exists()
    goals = json.loads((tmp_path / ".omp" / "ultragoal" / "goals.json").read_text())
    execute_goal = [goal for goal in goals["goals"] if goal["title"] == "Execute implementation work"][0]
    assert execute_goal["status"] == "completed"

    assert_success(run_omp(tmp_path, "ralph", "finish", "runtime"))
    assert_success(run_omp(tmp_path, "autopilot", "finish", "runtime"))
    assert_success(run_omp(tmp_path, "ultrawork", "finish", "runtime"))
    for mode in ["ralph", "autopilot", "ultrawork"]:
        state = json.loads((tmp_path / ".omp" / "state" / f"{mode}.json").read_text())
        assert state["status"] == "completed"

    command_wrapper = REPO_ROOT / "commands" / "verify.md"
    assert command_wrapper.exists()
    assert "skills/verify/SKILL.md" in command_wrapper.read_text(encoding="utf-8")