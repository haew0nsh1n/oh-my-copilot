"""Local OMP bridge for Copilot-native workflow integrations."""

import json
from pathlib import Path
from typing import Any


class OmpBridge:
    """Read-only bridge over local OMP state and artifact surfaces."""

    def __init__(self, project_root: Path | str):
        self.project_root = Path(project_root)

    def status(self) -> dict[str, Any]:
        """Summarize local state, artifact, skill, and command surfaces."""
        state_root = self.project_root / ".omp" / "state"
        artifacts_root = self.project_root / ".omp" / "artifacts"
        skills_root = self.project_root / "skills"
        commands_root = self.project_root / "commands"
        ultragoal_root = self.project_root / ".omp" / "ultragoal"

        return {
            "project_root": str(self.project_root),
            "state_root_exists": state_root.exists(),
            "state_files": sorted(path.name for path in state_root.glob("*.json"))
            if state_root.exists()
            else [],
            "artifact_commands": sorted(path.name for path in artifacts_root.iterdir() if path.is_dir())
            if artifacts_root.exists()
            else [],
            "skill_bodies": len(list(skills_root.glob("*/SKILL.md"))) if skills_root.exists() else 0,
            "command_bodies": len(list(commands_root.glob("*.md"))) if commands_root.exists() else 0,
            "ultragoal_exists": ultragoal_root.exists(),
        }

    def read_state(self, name: str) -> dict[str, Any]:
        """Read a named JSON state file from .omp/state."""
        safe_name = name.removesuffix(".json")
        path = self.project_root / ".omp" / "state" / f"{safe_name}.json"
        if not path.exists():
            return {"status": "missing", "name": safe_name, "path": str(path)}
        return json.loads(path.read_text(encoding="utf-8"))

    def list_artifacts(self, command: str | None = None) -> list[str]:
        """List artifact file paths, optionally scoped to a command directory."""
        artifacts_root = self.project_root / ".omp" / "artifacts"
        if command:
            search_root = artifacts_root / command
            if not search_root.exists():
                return []
            paths = [path for path in search_root.rglob("*") if path.is_file()]
        elif artifacts_root.exists():
            paths = [path for path in artifacts_root.rglob("*") if path.is_file()]
        else:
            paths = []
        return sorted(str(path.relative_to(self.project_root)) for path in paths)