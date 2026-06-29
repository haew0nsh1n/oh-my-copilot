"""Tests for provider runtime adapters."""

from core import ProviderRuntime
from domain import ProviderAdvisorStatus, ProviderName


class TestProviderRuntime:
    """Test provider runtime execution behavior."""

    def test_runtime_blocks_missing_provider(self):
        """Provider runtime blocks when provider executable is missing."""
        runtime = ProviderRuntime(executable_resolver=lambda command: None)

        result = runtime.execute("codex", "review this patch")

        assert result.provider == ProviderName.CODEX
        assert result.status == ProviderAdvisorStatus.BLOCKED
        assert result.exit_code is None
        assert "missing" in result.error_summary

    def test_runtime_executes_available_provider(self):
        """Provider runtime executes available provider through an adapter."""
        commands = []

        def executor(command: list[str]) -> tuple[int, str, str]:
            commands.append(command)
            return 0, "looks good", ""

        runtime = ProviderRuntime(
            executable_resolver=lambda command: f"/bin/{command}",
            command_executor=executor,
        )

        result = runtime.execute("codex", "review this patch")

        assert result.provider == ProviderName.CODEX
        assert result.status == ProviderAdvisorStatus.COMPLETED
        assert result.exit_code == 0
        assert result.output_summary == "looks good"
        assert commands == [["/bin/codex", "review this patch"]]
