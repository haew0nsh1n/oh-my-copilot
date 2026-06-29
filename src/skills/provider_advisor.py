"""Provider advisor skill for OMP ask parity."""

import subprocess
from pathlib import Path
from shutil import which
from typing import Callable

from domain import (
    ProviderAdviceArtifact,
    ProviderAdviceRequest,
    ProviderAvailability,
    ProviderAdvisorStatus,
    ProviderExecutionResult,
    ProviderName,
)


def _run_provider_command(command: list[str]) -> tuple[int, str, str]:
    """Run a provider command and capture text output."""
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    return completed.returncode, completed.stdout.strip(), completed.stderr.strip()


class ProviderAdvisorSkill:
    """Prepare provider advisor requests for external review workflows."""

    name = "provider-advisor"
    description = "Prepare ask-provider advice requests for Claude, Codex, Gemini, and peers"

    def __init__(
        self,
        executable_resolver: Callable[[str], str | None] = which,
        command_executor: Callable[[list[str]], tuple[int, str, str]] = _run_provider_command,
    ):
        """Initialize with a provider executable resolver."""
        self.executable_resolver = executable_resolver
        self.command_executor = command_executor

    def ask(self, provider: str, prompt: str) -> ProviderAdviceRequest:
        """Prepare an advice request for a supported provider."""
        provider_name = ProviderName(provider)
        return ProviderAdviceRequest(
            provider=provider_name,
            prompt=prompt,
            command_preview=f"omp ask {provider_name.value} {prompt}",
        )

    def check_provider(self, provider: str) -> ProviderAvailability:
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
        """Execute a provider CLI request when the provider is available."""
        provider_name = ProviderName(provider)
        availability = self.check_provider(provider)
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

    def record_artifact(
        self,
        result: ProviderExecutionResult,
        artifact_root: Path | str,
    ) -> ProviderAdviceArtifact:
        """Record a sanitized markdown artifact for a provider result."""
        root = Path(artifact_root)
        root.mkdir(parents=True, exist_ok=True)
        artifact_path = root / f"{result.provider.value}.md"
        artifact_path.write_text(
            "\n".join([
                f"# Provider Advice: {result.provider.value}",
                "",
                f"Status: {result.status.value}",
                f"Exit code: {result.exit_code if result.exit_code is not None else 'n/a'}",
                "",
                "## Output Summary",
                result.output_summary or "",
                "",
                "## Error Summary",
                result.error_summary or "",
                "",
            ])
        )
        return ProviderAdviceArtifact(provider=result.provider, path=artifact_path)
