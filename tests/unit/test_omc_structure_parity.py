"""Tests for OMC-compatible repository structure surfaces."""

import json
import subprocess
import sys
from pathlib import Path


OMC_AGENT_NAMES = {
    "analyst",
    "architect",
    "code-reviewer",
    "code-simplifier",
    "critic",
    "debugger",
    "designer",
    "document-specialist",
    "executor",
    "explore",
    "git-master",
    "planner",
    "qa-tester",
    "scientist",
    "security-reviewer",
    "test-engineer",
    "tracer",
    "verifier",
    "writer",
}


def test_root_agents_include_omc_public_agents():
    """Root agents mirror OMC's public agent prompt surface."""
    local_agents = {path.stem for path in Path("agents").glob("*.md")}

    assert OMC_AGENT_NAMES <= local_agents
    for agent_name in OMC_AGENT_NAMES:
        content = (Path("agents") / f"{agent_name}.md").read_text(encoding="utf-8")
        assert content.startswith("---\n"), agent_name
        assert "description:" in content, agent_name


def test_hook_and_template_surfaces_exist():
    """Root hooks and hook templates provide OMC-compatible lifecycle surfaces."""
    hooks_config = Path("hooks/hooks.json")

    assert hooks_config.exists()
    data = json.loads(hooks_config.read_text(encoding="utf-8"))
    assert "hooks" in data
    assert "SessionStart" in data["hooks"]
    assert "Stop" in data["hooks"]

    for template in [
        "session-start.mjs",
        "pre-tool-use.mjs",
        "post-tool-use.mjs",
        "post-tool-use-failure.mjs",
        "persistent-mode.mjs",
        "workflow-drift-guard.mjs",
        "stop-continuation.mjs",
    ]:
        path = Path("templates/hooks") / template
        assert path.exists(), template
        assert "OMP" in path.read_text(encoding="utf-8"), template


def test_bridge_script_reports_status():
    """Root bridge script exposes OMP bridge status as JSON."""
    script = Path("bridge/omp-bridge.py")

    assert script.exists()
    result = subprocess.run(
        [sys.executable, str(script), "status"],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert "skill_bodies" in data
    assert "command_bodies" in data


def test_benchmark_surfaces_run_quick_smoke():
    """Benchmark compatibility scripts exist and run a quick deterministic smoke."""
    for path in [
        Path("benchmark/README.md"),
        Path("benchmark/quick_test.py"),
        Path("benchmarks/run-all.py"),
        Path("benchmarks/baselines/omp-baseline.json"),
    ]:
        assert path.exists(), str(path)

    result = subprocess.run(
        [sys.executable, "benchmark/quick_test.py"],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "benchmark_smoke=ok" in result.stdout


def test_mission_surfaces_exist():
    """Root missions mirror OMC's mission/sandbox planning surface."""
    mission_roots = sorted(path for path in Path("missions").iterdir() if path.is_dir())

    assert mission_roots
    for mission_root in mission_roots:
        mission = mission_root / "mission.md"
        sandbox = mission_root / "sandbox.md"
        assert mission.exists(), mission_root.name
        assert sandbox.exists(), mission_root.name
        assert mission.read_text(encoding="utf-8").startswith("# Mission")
        assert sandbox.read_text(encoding="utf-8").startswith("# Sandbox")