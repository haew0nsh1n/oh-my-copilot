"""Project setup skill for local OMP state."""

from pathlib import Path

from domain import ProjectSetupResult, ProjectSetupStatus


class ProjectSetupSkill:
    """Initialize local OMP state directories for a workspace."""

    name = "project-setup"
    description = "Initialize .omp local state directories for OMP workflows"

    def initialize(self, project_root: Path | str) -> ProjectSetupResult:
        """Create the local .omp state root and standard subdirectories."""
        root = Path(project_root)
        state_root = root / ".omp"
        paths = [
            state_root,
            state_root / "artifacts" / "ask",
            state_root / "sessions",
            state_root / "state",
            state_root / "skills",
        ]
        for path in paths:
            path.mkdir(parents=True, exist_ok=True)

        return ProjectSetupResult(
            status=ProjectSetupStatus.INITIALIZED,
            state_root=state_root,
            created_paths=paths,
        )
