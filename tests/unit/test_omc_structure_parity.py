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

OMC_WORKFLOW_FILES = {
    "auto-label.yml",
    "ci.yml",
    "cleanup.yml",
    "pr-check.yml",
    "release.yml",
    "stale.yml",
    "upgrade-test.yml",
}

OMC_SOURCE_CLEANUP_PLAN_FILES = {
    "fallback-classification-inventory.md",
    "first-safe-cleanup-batch.md",
    "generated-artifact-policy.md",
    "ownership-matrix.md",
}

OMC_SOURCE_CLEANUP_REQUIRED_SECTIONS = {
    "fallback-classification-inventory.md": {
        "## Inputs and method",
        "## Classification legend",
        "## High-priority inventory",
        "## Required test-locks before Lane 2 edits",
        "## Lane ownership / handoff notes",
    },
    "first-safe-cleanup-batch.md": {
        "## Scope and stop rule",
        "## Batch objective",
        "## Target file ownership for this batch",
        "## Existing behavior locks to run before editing",
        "## Verification commands after edits",
    },
    "generated-artifact-policy.md": {
        "## Scope and source anchors",
        "## Package/build evidence",
        "## Decision",
        "## Artifact classes and required action",
        "## Final verification procedure",
    },
    "ownership-matrix.md": {
        "## Rules",
        "## Lane 0 — Baseline / inventory lock",
        "## Lane 1 — Test contract hardening",
        "## Lane 2 — Fallback / state-contract cleanup",
        "## Hand-off rule",
    },
}


def test_root_agents_include_omc_public_agents():
    """Root agents mirror OMC's public agent prompt surface."""
    local_agents = {path.stem for path in Path("agents").glob("*.md")}

    assert OMC_AGENT_NAMES <= local_agents
    for agent_name in OMC_AGENT_NAMES:
        content = (Path("agents") / f"{agent_name}.md").read_text(encoding="utf-8")
        assert content.startswith("---\n"), agent_name
        assert "description:" in content, agent_name


def test_root_agents_are_substantial_omc_style_prompts():
    """Root agents include OMC-style role, workflow, output, and verification guidance."""
    required_sections = (
        "## Role",
        "## When To Use",
        "## Operating Workflow",
        "## Expected Outputs",
        "## OMP Guardrails",
        "## Verification",
    )

    for agent_name in OMC_AGENT_NAMES:
        path = Path("agents") / f"{agent_name}.md"
        content = path.read_text(encoding="utf-8")
        line_count = len(content.splitlines())
        assert line_count >= 48, f"{path} is too shallow with {line_count} lines"
        for section in required_sections:
            assert section in content, f"{path} is missing {section}"


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


def test_github_workflows_mirror_omc_ci_surface():
    """GitHub workflows provide OMC-compatible CI, PR, release, cleanup, and upgrade surfaces."""
    workflow_root = Path(".github/workflows")
    local_workflows = {path.name for path in workflow_root.glob("*.yml")}

    assert OMC_WORKFLOW_FILES <= local_workflows

    ci = (workflow_root / "ci.yml").read_text(encoding="utf-8")
    assert "omp doctor --strict" in ci
    assert ".venv/bin/python -m pytest -q" in ci

    release = (workflow_root / "release.yml").read_text(encoding="utf-8")
    assert "omp doctor --strict" in release
    assert "MANIFEST.in" in release

    cleanup = (workflow_root / "cleanup.yml").read_text(encoding="utf-8")
    assert "retention-days" in cleanup


def test_source_overall_cleanup_plan_surface_exists():
    """OMP source-overall-cleanup readiness artifacts exist under .omp/plans."""
    assert not Path(".omx").exists()

    plan_root = Path(".omp/plans/source-overall-cleanup")
    local_files = {path.name for path in plan_root.glob("*.md")}

    assert OMC_SOURCE_CLEANUP_PLAN_FILES <= local_files
    for file_name in OMC_SOURCE_CLEANUP_PLAN_FILES:
        content = (plan_root / file_name).read_text(encoding="utf-8")
        assert content.startswith("# ")
        assert "OMP" in content or "oh-my-copilot" in content
        assert len(content.splitlines()) >= 70, file_name
        for section in OMC_SOURCE_CLEANUP_REQUIRED_SECTIONS[file_name]:
            assert section in content, f"{file_name} missing {section}"