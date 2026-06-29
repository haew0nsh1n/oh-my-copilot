"""Provider CLI runtime adapters."""

import json
import os
import subprocess
from shutil import which
from typing import Callable, Mapping
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from domain import ProviderAvailability, ProviderAdvisorStatus, ProviderExecutionResult, ProviderName


def run_provider_command(command: list[str]) -> tuple[int, str, str]:
    """Run a provider command and capture text output."""
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    return completed.returncode, completed.stdout.strip(), completed.stderr.strip()


def request_aoai_chat_completion(
    url: str,
    headers: dict[str, str],
    payload: dict,
) -> tuple[int, str, str]:
    """Call Azure OpenAI chat completions and return summarized text."""
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urlopen(request, timeout=60) as response:
            body = json.loads(response.read().decode("utf-8"))
            content = body.get("choices", [{}])[0].get("message", {}).get("content", "")
            return response.status, content, ""
    except HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        return error.code, "", body or str(error)
    except Exception as error:
        return 1, "", str(error)


class ProviderRuntime:
    """Check and execute local provider CLI commands."""

    def __init__(
        self,
        executable_resolver: Callable[[str], str | None] = which,
        command_executor: Callable[[list[str]], tuple[int, str, str]] = run_provider_command,
        env: Mapping[str, str] | None = None,
        aoai_request: Callable[[str, dict[str, str], dict], tuple[int, str, str]] = request_aoai_chat_completion,
        azure_token_provider: Callable[[], str] | None = None,
    ):
        """Initialize provider runtime adapters."""
        self.executable_resolver = executable_resolver
        self.command_executor = command_executor
        self.env = env if env is not None else os.environ
        self.aoai_request = aoai_request
        self.azure_token_provider = azure_token_provider
        self._cached_azure_token = ""

    def check(self, provider: str) -> ProviderAvailability:
        """Check whether a provider CLI is available locally."""
        provider_name = ProviderName(provider)
        executable_path = self.executable_resolver(provider_name.value) or ""
        if not executable_path and provider_name == ProviderName.CODEX:
            deployment = self._aoai_deployment()
            if self._aoai_endpoint() and self._aoai_auth_available() and deployment:
                executable_path = f"aoai://{deployment}"
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

        if availability.executable_path.startswith("aoai://"):
            exit_code, stdout, stderr = self._execute_aoai(prompt)
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

    def _aoai_endpoint(self) -> str:
        return self.env.get("AZURE_OPENAI_ENDPOINT", "").rstrip("/")

    def _aoai_responses_endpoint(self) -> str:
        endpoint = self._aoai_endpoint()
        if endpoint.endswith("/openai/v1/responses"):
            return endpoint
        if ".services.ai.azure.com" in endpoint and "/api/projects/" in endpoint:
            return f"{endpoint}/openai/v1/responses"
        return ""

    def _aoai_api_key(self) -> str:
        return self.env.get("AZURE_OPENAI_API_KEY", "")

    def _aoai_bearer_token(self) -> str:
        if self._cached_azure_token:
            return self._cached_azure_token
        if self.azure_token_provider:
            self._cached_azure_token = self.azure_token_provider()
            return self._cached_azure_token

        exit_code, stdout, _stderr = self.command_executor([
            "az",
            "account",
            "get-access-token",
            "--resource",
            self._azure_token_resource(),
            "--output",
            "json",
        ])
        if exit_code != 0 or not stdout:
            return ""
        try:
            self._cached_azure_token = json.loads(stdout).get("accessToken", "")
        except json.JSONDecodeError:
            self._cached_azure_token = ""
        return self._cached_azure_token

    def _azure_token_resource(self) -> str:
        if ".services.ai.azure.com" in self._aoai_endpoint():
            return "https://ai.azure.com/"
        return "https://cognitiveservices.azure.com/"

    def _aoai_auth_available(self) -> bool:
        return bool(self._aoai_api_key() or self._aoai_bearer_token())

    def _aoai_deployment(self) -> str:
        return (
            self.env.get("AZURE_OPENAI_CODEX_DEPLOYMENT", "")
            or self.env.get("AZURE_OPENAI_DEPLOYMENT", "")
        )

    def _aoai_api_version(self) -> str:
        return self.env.get("AZURE_OPENAI_API_VERSION", "2025-04-01-preview")

    def _execute_aoai(self, prompt: str) -> tuple[int, str, str]:
        endpoint = self._aoai_endpoint()
        deployment = self._aoai_deployment()
        api_version = self._aoai_api_version()
        responses_endpoint = self._aoai_responses_endpoint()
        if responses_endpoint:
            url = responses_endpoint
            headers = self._aoai_headers(prefer_bearer=True)
            payload = {
                "model": deployment,
                "input": prompt,
            }
            status_code, stdout, stderr = self.aoai_request(url, headers, payload)
            exit_code = 0 if 200 <= status_code < 300 else status_code
            return exit_code, stdout, stderr

        url = (
            f"{endpoint}/openai/deployments/{deployment}/chat/completions"
            f"?api-version={api_version}"
        )
        headers = self._aoai_headers()
        payload = {
            "messages": [
                {"role": "system", "content": "You are a concise code review advisor."},
                {"role": "user", "content": prompt},
            ],
        }
        status_code, stdout, stderr = self.aoai_request(url, headers, payload)
        exit_code = 0 if 200 <= status_code < 300 else status_code
        return exit_code, stdout, stderr

    def _aoai_headers(self, prefer_bearer: bool = False) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        api_key = self._aoai_api_key()
        if api_key and not prefer_bearer:
            headers["api-key"] = api_key
        else:
            headers["Authorization"] = f"Bearer {self._aoai_bearer_token()}"
        return headers
