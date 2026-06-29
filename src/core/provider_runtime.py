"""Provider CLI runtime adapters."""

import subprocess
from shutil import which
from typing import Callable

from domain import ProviderAvailability, ProviderAdvisorStatus, ProviderExecutionResult, ProviderName


def run_provider_command(command: list[str]) -> tuple[int, str, str]:
    """Run a provider command and capture text output."""
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    return completed.returncode, completed.stdout.strip(), completed.stderr.strip()


class ProviderRuntime:
    """Check and execute local provider CLI commands."""

    def __init__(
        self,
        executable_resolver: Callable[[str], str | None] = which,
        command_executor: Callable[[list[str]], tuple[int, str, str]] = run_provider_command,
    ):
        """Initialize provider runtime adapters."""
        self.executable_resolver = executable_resolver
        self.command_executor = command_executor

    def check(self, provider: str) -> ProviderAvailability:
        """Check whether a provider CLI is available locally."""
        provider_name = ProviderName(provider)
        executable_path = self.executable_resolver(provider_name.value) or ""
        status = (
            ProviderAdvisorStatus.PREPARED
            if executable_path
            else ProviderAdvisorStatus.BLOCKED
        )
        return ProviderAvailability(
            provider=provider_name,
            status=status,
            executable_path=executable_path,
        )

    def execute(self, provider: str, prompt: str) -> ProviderExecutionResult:
        """Execute a provider CLI command if available."""
        provider_name = ProviderName(provider)
        availability = self.check(provider)
        if availability.status == ProviderAdvisorStatus.BLOCKED:
            return ProviderExecutionResult(
                provider=provider_name,
                status=ProviderAdvisorStatus.BLOCKED,
                error_summary=f"Provider executable missing: {provider_name.value}",
            )

        exit_code, stdout, stderr = self.command_executor([
            availability.executable_path,
            prompt,
        ])
        status = (
            ProviderAdvisorStatus.COMPLETED
            if exit_code == 0
            else ProviderAdvisorStatus.FAILED
        )
        return ProviderExecutionResult(
            provider=provider_name,
            status=status,
            exit_code=exit_code,
            output_summary=stdout,
            error_summary=stderr,
        )
