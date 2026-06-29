"""Tests for provider advisor skill."""

from core import ProviderRuntime
from skills import ProviderAdvisorSkill
from domain import ProviderName, ProviderAdvisorStatus


class TestProviderAdvisorBasics:
    """Test provider advisor workflow behavior."""

    def test_skill_can_prepare_provider_advice_request(self):
        """Provider advisor prepares a request for a supported provider."""
        skill = ProviderAdvisorSkill()

        request = skill.ask("codex", "review this migration plan")

        assert skill.name == "provider-advisor"
        assert request.provider == ProviderName.CODEX
        assert request.prompt == "review this migration plan"
        assert request.status == ProviderAdvisorStatus.PREPARED
        assert "codex" in request.command_preview

    def test_skill_can_detect_available_provider_cli(self):
        """Provider advisor detects an installed provider CLI."""
        skill = ProviderAdvisorSkill(executable_resolver=lambda command: f"/bin/{command}")

        availability = skill.check_provider("codex")

        assert availability.provider == ProviderName.CODEX
        assert availability.status == ProviderAdvisorStatus.PREPARED
        assert availability.executable_path == "/bin/codex"

    def test_skill_blocks_missing_provider_cli(self):
        """Provider advisor blocks execution when provider CLI is missing."""
        skill = ProviderAdvisorSkill(
            provider_runtime=ProviderRuntime(executable_resolver=lambda command: None, env={})
        )

        availability = skill.check_provider("codex")

        assert availability.provider == ProviderName.CODEX
        assert availability.status == ProviderAdvisorStatus.BLOCKED
        assert availability.executable_path == ""

    def test_skill_can_execute_available_provider_cli(self):
        """Provider advisor executes an available provider CLI through an adapter."""
        executed_commands = []

        def executor(command: list[str]) -> tuple[int, str, str]:
            executed_commands.append(command)
            return 0, "looks good", ""

        skill = ProviderAdvisorSkill(
            executable_resolver=lambda command: f"/bin/{command}",
            command_executor=executor,
        )

        result = skill.execute("codex", "review this migration plan")

        assert result.provider == ProviderName.CODEX
        assert result.status == ProviderAdvisorStatus.COMPLETED
        assert result.exit_code == 0
        assert result.output_summary == "looks good"
        assert executed_commands == [["/bin/codex", "review this migration plan"]]

    def test_skill_blocks_execution_when_provider_cli_missing(self):
        """Provider advisor blocks execution when the provider executable is missing."""
        skill = ProviderAdvisorSkill(
            provider_runtime=ProviderRuntime(executable_resolver=lambda command: None, env={})
        )

        result = skill.execute("codex", "review this migration plan")

        assert result.provider == ProviderName.CODEX
        assert result.status == ProviderAdvisorStatus.BLOCKED
        assert result.exit_code is None
        assert "missing" in result.error_summary

    def test_skill_records_provider_result_artifact(self, tmp_path):
        """Provider advisor records a markdown artifact for execution results."""
        skill = ProviderAdvisorSkill(
            executable_resolver=lambda command: f"/bin/{command}",
            command_executor=lambda command: (0, "looks good", ""),
        )
        result = skill.execute("codex", "review this migration plan")

        artifact = skill.record_artifact(result, tmp_path)

        assert artifact.path == tmp_path / "codex.md"
        assert artifact.path.read_text().startswith("# Provider Advice: codex")
        assert "looks good" in artifact.path.read_text()
