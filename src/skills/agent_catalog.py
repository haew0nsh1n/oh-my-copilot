"""AgentCatalog skill — invoke specialist agent personas."""

from typing import Optional, List
from domain import (
    AgentRegistry, AgentSpec, AgentCategory, AgentInvocation,
)


class AgentCatalogSkill:
    name = "agent_catalog"
    description = "Invoke specialist agent personas from the oh-my-copilot catalog (33 agents)"

    def __init__(self):
        self.registry = AgentRegistry()
        self.invocations: List[AgentInvocation] = []

    def get_agent(self, name: str) -> Optional[AgentSpec]:
        return self.registry.get(name)

    def invoke(self, agent_name: str, prompt: str) -> AgentInvocation:
        spec = self.registry.get(agent_name)
        invocation = AgentInvocation(
            agent_name=agent_name,
            prompt=prompt,
            spec=spec,
            success=spec is not None
        )
        if spec:
            invocation.output = (
                f"[{spec.model_tier.value.upper()} model] {spec.description} "
                f"→ Processing: {prompt}"
            )
        else:
            invocation.output = f"Agent '{agent_name}' not found in catalog."
        self.invocations.append(invocation)
        return invocation

    def list_agents(self) -> List[AgentSpec]:
        return self.registry.list_all()

    def list_by_category(self, category: AgentCategory) -> List[AgentSpec]:
        return self.registry.list_by_category(category)

    def agent_exists(self, name: str) -> bool:
        return self.registry.exists(name)

    def list_agent_names(self) -> List[str]:
        return self.registry.list_all_names()

    def get_invocation_history(self) -> List[AgentInvocation]:
        return self.invocations
