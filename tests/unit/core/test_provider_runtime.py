"""Tests for provider runtime adapters."""

from core import ProviderRuntime
from domain import ProviderAdvisorStatus, ProviderName


class TestProviderRuntime:
    """Test provider runtime execution behavior."""

    def test_runtime_blocks_missing_provider(self):
        """Provider runtime blocks when provider executable is missing."""
        runtime = ProviderRuntime(executable_resolver=lambda command: None, env={})

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

    def test_runtime_detects_aoai_codex_backend(self):
        """Provider runtime treats AOAI config as an available codex backend."""
        runtime = ProviderRuntime(
            executable_resolver=lambda command: None,
            env={
                "AZURE_OPENAI_ENDPOINT": "https://example.openai.azure.com",
                "AZURE_OPENAI_API_KEY": "test-key",
                "AZURE_OPENAI_CODEX_DEPLOYMENT": "codex-5-3",
            },
        )

        availability = runtime.check("codex")

        assert availability.provider == ProviderName.CODEX
        assert availability.status == ProviderAdvisorStatus.PREPARED
        assert availability.executable_path == "aoai://codex-5-3"

    def test_runtime_executes_aoai_codex_backend(self):
        """Provider runtime can execute codex through an AOAI deployment."""
        requests = []

        def aoai_request(url: str, headers: dict[str, str], payload: dict) -> tuple[int, str, str]:
            requests.append((url, headers, payload))
            return 0, "aoai looks good", ""

        runtime = ProviderRuntime(
            executable_resolver=lambda command: None,
            env={
                "AZURE_OPENAI_ENDPOINT": "https://example.openai.azure.com/",
                "AZURE_OPENAI_API_KEY": "test-key",
                "AZURE_OPENAI_CODEX_DEPLOYMENT": "codex-5-3",
                "AZURE_OPENAI_API_VERSION": "2025-04-01-preview",
            },
            aoai_request=aoai_request,
        )

        result = runtime.execute("codex", "review this patch")

        assert result.status == ProviderAdvisorStatus.COMPLETED
        assert result.output_summary == "aoai looks good"
        assert requests[0][0] == (
            "https://example.openai.azure.com/openai/deployments/"
            "codex-5-3/chat/completions?api-version=2025-04-01-preview"
        )
        assert requests[0][1]["api-key"] == "test-key"
        assert requests[0][2]["messages"][-1]["content"] == "review this patch"

    def test_runtime_detects_aoai_codex_with_azure_cli_token(self):
        """Provider runtime can use Azure CLI auth when API key is absent."""
        runtime = ProviderRuntime(
            executable_resolver=lambda command: None,
            env={
                "AZURE_OPENAI_ENDPOINT": "https://example.openai.azure.com",
                "AZURE_OPENAI_CODEX_DEPLOYMENT": "codex-5-3",
            },
            azure_token_provider=lambda: "azure-cli-token",
        )

        availability = runtime.check("codex")

        assert availability.status == ProviderAdvisorStatus.PREPARED
        assert availability.executable_path == "aoai://codex-5-3"

    def test_runtime_executes_aoai_codex_with_bearer_token(self):
        """Provider runtime sends Bearer auth when API key is absent."""
        requests = []

        def aoai_request(url: str, headers: dict[str, str], payload: dict) -> tuple[int, str, str]:
            requests.append((url, headers, payload))
            return 0, "aoai bearer looks good", ""

        runtime = ProviderRuntime(
            executable_resolver=lambda command: None,
            env={
                "AZURE_OPENAI_ENDPOINT": "https://example.openai.azure.com",
                "AZURE_OPENAI_CODEX_DEPLOYMENT": "codex-5-3",
            },
            azure_token_provider=lambda: "azure-cli-token",
            aoai_request=aoai_request,
        )

        result = runtime.execute("codex", "review this patch")

        assert result.status == ProviderAdvisorStatus.COMPLETED
        assert requests[0][1]["Authorization"] == "Bearer azure-cli-token"
        assert "api-key" not in requests[0][1]

    def test_runtime_executes_aoai_responses_endpoint(self):
        """Provider runtime supports Azure AI services OpenAI v1 responses endpoint."""
        requests = []

        def aoai_request(url: str, headers: dict[str, str], payload: dict) -> tuple[int, str, str]:
            requests.append((url, headers, payload))
            return 0, "responses looks good", ""

        runtime = ProviderRuntime(
            executable_resolver=lambda command: None,
            env={
                "AZURE_OPENAI_ENDPOINT": "https://example.services.ai.azure.com/openai/v1/responses",
                "AZURE_OPENAI_CODEX_DEPLOYMENT": "gpt-5.3-codex",
            },
            azure_token_provider=lambda: "azure-cli-token",
            aoai_request=aoai_request,
        )

        result = runtime.execute("codex", "review this patch")

        assert result.status == ProviderAdvisorStatus.COMPLETED
        assert result.output_summary == "responses looks good"
        assert requests[0][0] == "https://example.services.ai.azure.com/openai/v1/responses"
        assert requests[0][2] == {
            "model": "gpt-5.3-codex",
            "input": "review this patch",
        }
        assert requests[0][1]["Authorization"] == "Bearer azure-cli-token"

    def test_runtime_expands_foundry_project_endpoint_to_responses_endpoint(self):
        """Provider runtime expands Foundry project endpoint to OpenAI v1 responses."""
        requests = []

        def aoai_request(url: str, headers: dict[str, str], payload: dict) -> tuple[int, str, str]:
            requests.append((url, headers, payload))
            return 0, "project endpoint looks good", ""

        runtime = ProviderRuntime(
            executable_resolver=lambda command: None,
            env={
                "AZURE_OPENAI_ENDPOINT": "https://example.services.ai.azure.com/api/projects/demo",
                "AZURE_OPENAI_CODEX_DEPLOYMENT": "gpt-5.3-codex",
            },
            azure_token_provider=lambda: "azure-cli-token",
            aoai_request=aoai_request,
        )

        result = runtime.execute("codex", "review this patch")

        assert result.status == ProviderAdvisorStatus.COMPLETED
        assert requests[0][0] == (
            "https://example.services.ai.azure.com/api/projects/demo/openai/v1/responses"
        )

    def test_runtime_uses_ai_token_resource_for_services_endpoint(self):
        """Provider runtime requests ai.azure.com tokens for services.ai.azure.com endpoints."""
        commands = []

        def executor(command: list[str]) -> tuple[int, str, str]:
            commands.append(command)
            return 0, '{"accessToken":"azure-cli-token"}', ""

        runtime = ProviderRuntime(
            executable_resolver=lambda command: None,
            command_executor=executor,
            env={
                "AZURE_OPENAI_ENDPOINT": "https://example.services.ai.azure.com/openai/v1/responses",
                "AZURE_OPENAI_CODEX_DEPLOYMENT": "gpt-5.3-codex",
            },
            aoai_request=lambda url, headers, payload: (0, "ok", ""),
        )

        runtime.execute("codex", "review this patch")

        assert "https://ai.azure.com/" in commands[0]

    def test_runtime_responses_endpoint_prefers_bearer_when_api_key_is_set(self):
        """Responses endpoint uses Bearer auth because key auth can be disabled."""
        requests = []

        def aoai_request(url: str, headers: dict[str, str], payload: dict) -> tuple[int, str, str]:
            requests.append((url, headers, payload))
            return 0, "responses looks good", ""

        runtime = ProviderRuntime(
            executable_resolver=lambda command: None,
            env={
                "AZURE_OPENAI_ENDPOINT": "https://example.services.ai.azure.com/openai/v1/responses",
                "AZURE_OPENAI_API_KEY": "test-key",
                "AZURE_OPENAI_CODEX_DEPLOYMENT": "gpt-5.3-codex",
            },
            azure_token_provider=lambda: "azure-cli-token",
            aoai_request=aoai_request,
        )

        runtime.execute("codex", "review this patch")

        assert requests[0][1]["Authorization"] == "Bearer azure-cli-token"
        assert "api-key" not in requests[0][1]
