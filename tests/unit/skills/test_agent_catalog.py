"""Tests for agent catalog skill."""
import pytest
from skills import AgentCatalogSkill
from domain import AgentCategory


class TestAgentCatalogBasics:
    def test_skill_created(self):
        assert AgentCatalogSkill().name == "agent_catalog"

    def test_catalog_has_33_agents(self):
        skill = AgentCatalogSkill()
        agents = skill.list_agents()
        assert len(agents) == 32  # 33 total - 1 internal (code-simplifier)

    def test_all_agent_names(self):
        skill = AgentCatalogSkill()
        names = skill.list_agent_names()
        assert "explore" in names
        assert "critic" in names
        assert "architect" in names
        assert "parity-analyst" in names
        assert "parity-implementer" in names
        assert "parity-verifier" in names


class TestAgentRetrieval:
    def test_get_existing_agent(self):
        skill = AgentCatalogSkill()
        agent = skill.get_agent("explore")
        assert agent is not None
        assert agent.name == "explore"
        assert "discovery" in agent.description.lower()

    def test_get_missing_agent(self):
        skill = AgentCatalogSkill()
        assert skill.get_agent("nonexistent") is None

    def test_agent_exists(self):
        skill = AgentCatalogSkill()
        assert skill.agent_exists("architect")
        assert not skill.agent_exists("unicorn")


class TestAgentCategories:
    def test_list_build_analysis(self):
        skill = AgentCatalogSkill()
        agents = skill.list_by_category(AgentCategory.BUILD_ANALYSIS)
        names = [a.name for a in agents]
        assert "explore" in names
        assert "architect" in names
        assert "debugger" in names
        assert "parity-implementer" in names

    def test_list_review_agents(self):
        skill = AgentCatalogSkill()
        agents = skill.list_by_category(AgentCategory.REVIEW)
        assert len(agents) == 6

    def test_list_product_agents(self):
        skill = AgentCatalogSkill()
        agents = skill.list_by_category(AgentCategory.PRODUCT)
        names = [a.name for a in agents]
        assert "product-manager" in names

    def test_list_domain_specialist_agents(self):
        skill = AgentCatalogSkill()
        agents = skill.list_by_category(AgentCategory.DOMAIN_SPECIALIST)
        names = [a.name for a in agents]
        assert "parity-analyst" in names

    def test_list_coordination_agents(self):
        skill = AgentCatalogSkill()
        agents = skill.list_by_category(AgentCategory.COORDINATION)
        names = [a.name for a in agents]
        assert "critic" in names
        assert "scholastic" in names
        assert "vision" in names
        assert "parity-verifier" in names


class TestAgentInvocation:
    def test_invoke_known_agent(self):
        skill = AgentCatalogSkill()
        invocation = skill.invoke("explore", "map auth flow")
        assert invocation.success
        assert invocation.agent_name == "explore"
        assert len(invocation.output) > 0

    def test_invoke_unknown_agent(self):
        skill = AgentCatalogSkill()
        invocation = skill.invoke("unknown-agent", "do something")
        assert not invocation.success
        assert "not found" in invocation.output.lower()

    def test_invocation_history(self):
        skill = AgentCatalogSkill()
        skill.invoke("explore", "map flow")
        skill.invoke("critic", "challenge plan")
        history = skill.get_invocation_history()
        assert len(history) == 2
