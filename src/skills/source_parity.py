"""Source parity skill for OMC-to-OMP implementation audits."""

from pathlib import Path

from domain.source_parity import (
    SourceParityItem,
    SourceParityReport,
    SourceParityStatus,
    count_reference_source_families,
)


REFERENCE_SOURCE_FAMILIES: tuple[SourceParityItem, ...] = (
    SourceParityItem("AGENTS.md", 1, SourceParityStatus.ADAPTED, ("AGENTS.md",), "Root agent guidance is translated for Copilot."),
    SourceParityItem("agents", 22, SourceParityStatus.ADAPTED, ("agents/", "src/domain/agent_catalog.py"), "Agent prompts and catalog entries are represented."),
    SourceParityItem("autoresearch", 3, SourceParityStatus.IMPLEMENTED, ("src/skills/autoresearch.py", "src/skills/autoresearch_goal.py"), "Autoresearch workflows have Python skill surfaces."),
    SourceParityItem("cli", 23, SourceParityStatus.IMPLEMENTED, ("src/cli/main.py",), "Public OMP CLI mirrors OMC command value through Python adapters."),
    SourceParityItem("commands", 1, SourceParityStatus.IMPLEMENTED, ("commands/",), "Root command markdown wrappers are present."),
    SourceParityItem("config", 4, SourceParityStatus.PARTIAL, ("src/core/provider_runtime.py", "src/domain/notification_config.py"), "Provider and notification config exist, but OMC model/config loader parity is incomplete."),
    SourceParityItem("constants", 2, SourceParityStatus.ADAPTED, ("src/cli/main.py", "src/domain/"), "Constants are folded into Python domain and CLI modules."),
    SourceParityItem("features", 61, SourceParityStatus.PARTIAL, ("src/skills/", "src/core/"), "Core workflow features exist; background tasks, context injection, model routing, and verification hooks remain partial."),
    SourceParityItem("goal-workflows", 1, SourceParityStatus.ADAPTED, ("src/skills/ultragoal.py",), "Goal snapshot behavior maps to OMP ultragoal artifacts."),
    SourceParityItem("hooks", 169, SourceParityStatus.PARTIAL, ("hooks/", "templates/hooks/", "src/skills/hooks.py"), "Lifecycle surfaces exist; Claude Code hook runtime is translated only partially."),
    SourceParityItem("hud", 42, SourceParityStatus.ADAPTED, ("src/skills/state_summary.py", "skills/hud/SKILL.md"), "HUD is represented as local OMP state summary."),
    SourceParityItem("index.ts", 1, SourceParityStatus.ADAPTED, ("src/cli/__init__.py", "src/cli/__main__.py"), "Package entrypoint is Python CLI-based."),
    SourceParityItem("installer", 3, SourceParityStatus.PARTIAL, ("src/skills/project_setup.py", "src/cli/main.py"), "Setup/install commands exist, but full Node installer behavior is not ported."),
    SourceParityItem("interop", 3, SourceParityStatus.ADAPTED, ("src/core/omp_bridge.py", "bridge/omp-bridge.py"), "Shared state interop maps to the OMP bridge."),
    SourceParityItem("lib", 22, SourceParityStatus.PARTIAL, ("src/core/",), "Some runtime helpers exist; file locks, job DB, memory merge, and release helpers are gaps."),
    SourceParityItem("mcp", 13, SourceParityStatus.GAP, ("bridge/omp-bridge.py",), "MCP server/tool runtime is not implemented in Python yet."),
    SourceParityItem("notifications", 16, SourceParityStatus.PARTIAL, ("src/skills/notification_config.py",), "Notification config exists without dispatcher/listener parity."),
    SourceParityItem("openclaw", 6, SourceParityStatus.GAP, (), "OpenClaw dispatcher/signal runtime has no OMP implementation yet."),
    SourceParityItem("planning", 2, SourceParityStatus.ADAPTED, (".omp/plans/", "src/domain/strategic_plan.py"), "Planning artifacts are represented through OMP plans and strategic plan domain models."),
    SourceParityItem("platform", 2, SourceParityStatus.ADAPTED, ("src/core/",), "Platform utilities are folded into Python runtime helpers."),
    SourceParityItem("providers", 7, SourceParityStatus.PARTIAL, ("src/core/provider_runtime.py", "src/skills/provider_advisor.py"), "AOAI/provider advice exists; Git hosting provider adapters are not complete."),
    SourceParityItem("ralphthon", 5, SourceParityStatus.ADAPTED, ("src/skills/ralph.py", "src/skills/deep_interview.py"), "Ralphthon planning maps to Ralph plus deep interview flows."),
    SourceParityItem("shared", 3, SourceParityStatus.ADAPTED, ("src/domain/",), "Shared contracts are modeled as Python domain objects."),
    SourceParityItem("team", 61, SourceParityStatus.PARTIAL, ("src/domain/team_runtime.py", "src/skills/team_runtime.py"), "Team domain and CLI exist; tmux/worktree/MCP worker runtime remains partial."),
    SourceParityItem("tools", 32, SourceParityStatus.PARTIAL, ("src/skills/", "src/core/"), "Skill tools and trace/wiki surfaces exist; AST/LSP/Python REPL tools are gaps."),
    SourceParityItem("types", 1, SourceParityStatus.ADAPTED, ("src/domain/",), "Type contracts are represented by dataclasses and enums."),
    SourceParityItem("ultragoal", 1, SourceParityStatus.IMPLEMENTED, ("src/skills/ultragoal.py",), "Artifact-only ultragoal flow is implemented."),
    SourceParityItem("utils", 14, SourceParityStatus.ADAPTED, ("src/core/", "src/cli/main.py"), "General utilities are folded into Python helpers and adapters."),
    SourceParityItem("verification", 2, SourceParityStatus.ADAPTED, ("src/skills/ultraqa.py", "src/skills/code_review.py"), "Verification maps to UltraQA and review flows."),
)


class SourceParitySkill:
    """Audit OMC src implementation families against OMP source surfaces."""

    name = "source_parity"
    description = "Compare OMC src implementation families with OMP translated source surfaces."

    def audit(
        self,
        reference_src: str | Path | None = None,
        workspace_root: str | Path | None = None,
    ) -> SourceParityReport:
        """Create a source parity report, optionally checking OMC and OMP source trees."""
        observed_counts: dict[str, int] = {}
        if reference_src is not None:
            observed_counts = count_reference_source_families(Path(reference_src))

        return SourceParityReport(
            reference="oh-my-claudecode/src",
            items=REFERENCE_SOURCE_FAMILIES,
            observed_reference_counts=observed_counts,
            workspace_root=Path(workspace_root) if workspace_root is not None else Path.cwd(),
        )