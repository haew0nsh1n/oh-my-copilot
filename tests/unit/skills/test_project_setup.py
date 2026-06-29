"""Tests for project setup skill."""

from skills import ProjectSetupSkill
from domain import ProjectSetupStatus


class TestProjectSetupBasics:
    """Test project setup workflow."""

    def test_skill_initializes_omp_state_root(self, tmp_path):
        """Project setup creates the local OMP state root."""
        skill = ProjectSetupSkill()

        result = skill.initialize(tmp_path)

        assert skill.name == "project-setup"
        assert result.status == ProjectSetupStatus.INITIALIZED
        assert result.state_root == tmp_path / ".omp"
        assert (tmp_path / ".omp" / "artifacts" / "ask").is_dir()
        assert (tmp_path / ".omp" / "sessions").is_dir()
        assert (tmp_path / ".omp" / "state").is_dir()
        assert (tmp_path / ".omp" / "skills").is_dir()
