"""Provider advisor skill for OMP ask parity."""

from pathlib import Path
from shutil import which
from typing import Callable

from core import ProviderRuntime, run_provider_command

from domain import (
    ProviderAdviceArtifact,
    ProviderAdviceRequest,
    ProviderAvailability,
    ProviderAdvisorStatus,
    ProviderExecutionResult,
    ProviderName,
)


class ProviderAdvisorSkill:
    """Prepare provider advisor requests for external review workflows."""

    name = "provider-advisor"
    description = "Prepare ask-provider advice requests for Claude, Codex, Gemini, and peers"

    def __init__(
        self,
        executable_resolver: Callable[[str], str | None] = which,
        command_executor: Callable[[list[str]], tuple[int, str, str]] = run_provider_command,
        provider_runtime: ProviderRuntime | None = None,
    ):
        """Initialize with a provider executable resolver."""
        self.provider_runtime = provider_runtime or ProviderRuntime(
            executable_resolver=executable_resolver,
            command_executor=command_executor,
        )

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
        return self.provider_runtime.check(provider)

    def execute(self, provider: str, prompt: str) -> ProviderExecutionResult:
        """Execute a provider CLI request when the provider is available."""
        return self.provider_runtime.execute(provider, prompt)

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
