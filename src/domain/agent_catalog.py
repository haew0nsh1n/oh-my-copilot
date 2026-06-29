"""Domain model for agent catalog — 33 specialist agent personas."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum


class AgentCategory(str, Enum):
    BUILD_ANALYSIS = "build_analysis"
    REVIEW = "review"
    DOMAIN_SPECIALIST = "domain_specialist"
    PRODUCT = "product"
    COORDINATION = "coordination"


class ModelTier(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class AgentSpec:
    name: str
    category: AgentCategory
    model_tier: ModelTier
    description: str
    example_usage: str
    is_internal: bool = False


# Full agent catalog — specialist personas for oh-my-copilot workflows
AGENT_CATALOG: List[AgentSpec] = [
    # Build & Analysis
    AgentSpec("explore", AgentCategory.BUILD_ANALYSIS, ModelTier.LOW,
              "Codebase discovery and symbol mapping.",
              'explore "map auth flow"'),
    AgentSpec("analyst", AgentCategory.BUILD_ANALYSIS, ModelTier.HIGH,
              "Clarifies requirements and acceptance criteria.",
              'analyst "define scope"'),
    AgentSpec("planner", AgentCategory.BUILD_ANALYSIS, ModelTier.HIGH,
              "Builds execution plans and sequencing.",
              'planner "plan migration"'),
    AgentSpec("architect", AgentCategory.BUILD_ANALYSIS, ModelTier.HIGH,
              "System boundaries and architecture design.",
              'architect "review service boundaries"'),
    AgentSpec("debugger", AgentCategory.BUILD_ANALYSIS, ModelTier.MEDIUM,
              "Root-cause and regression diagnosis.",
              'debugger "investigate flaky test"'),
    AgentSpec("executor", AgentCategory.BUILD_ANALYSIS, ModelTier.MEDIUM,
              "Implementation and refactoring work.",
              'executor "add validation"'),
    AgentSpec("verifier", AgentCategory.BUILD_ANALYSIS, ModelTier.MEDIUM,
              "Evidence-backed completion checks.",
              'verifier "verify release readiness"'),
    AgentSpec("parity-implementer", AgentCategory.BUILD_ANALYSIS, ModelTier.HIGH,
              "Ports oh-my-claudecode feature slices into oh-my-copilot implementation units.",
              'parity-implementer "implement team parity slice"'),
    # Review
    AgentSpec("style-reviewer", AgentCategory.REVIEW, ModelTier.LOW,
              "Formatting and naming conventions.",
              'style-reviewer "check style"'),
    AgentSpec("quality-reviewer", AgentCategory.REVIEW, ModelTier.MEDIUM,
              "Logic and maintainability defects.",
              'quality-reviewer "review PR"'),
    AgentSpec("api-reviewer", AgentCategory.REVIEW, ModelTier.MEDIUM,
              "API contracts and compatibility.",
              'api-reviewer "audit API changes"'),
    AgentSpec("security-reviewer", AgentCategory.REVIEW, ModelTier.MEDIUM,
              "Security boundaries and vulnerabilities.",
              'security-reviewer "security audit"'),
    AgentSpec("performance-reviewer", AgentCategory.REVIEW, ModelTier.MEDIUM,
              "Performance and complexity bottlenecks.",
              'performance-reviewer "profile hotspots"'),
    AgentSpec("code-reviewer", AgentCategory.REVIEW, ModelTier.HIGH,
              "Comprehensive multi-axis code review.",
              'code-reviewer "comprehensive review"'),
    # Domain Specialists
    AgentSpec("dependency-expert", AgentCategory.DOMAIN_SPECIALIST, ModelTier.MEDIUM,
              "External SDK/API/package evaluation.",
              'dependency-expert "compare SDK options"'),
    AgentSpec("test-engineer", AgentCategory.DOMAIN_SPECIALIST, ModelTier.MEDIUM,
              "Test strategy and coverage improvements.",
              'test-engineer "write test plan"'),
    AgentSpec("quality-strategist", AgentCategory.DOMAIN_SPECIALIST, ModelTier.MEDIUM,
              "Release quality and risk strategy.",
              'quality-strategist "assess release risk"'),
    AgentSpec("build-fixer", AgentCategory.DOMAIN_SPECIALIST, ModelTier.MEDIUM,
              "Build/toolchain/type issue resolution.",
              'build-fixer "fix CI failures"'),
    AgentSpec("designer", AgentCategory.DOMAIN_SPECIALIST, ModelTier.MEDIUM,
              "UI/UX architecture and interaction design.",
              'designer "improve onboarding UX"'),
    AgentSpec("writer", AgentCategory.DOMAIN_SPECIALIST, ModelTier.LOW,
              "Documentation and user guidance.",
              'writer "draft migration guide"'),
    AgentSpec("qa-tester", AgentCategory.DOMAIN_SPECIALIST, ModelTier.MEDIUM,
              "Interactive runtime QA validation.",
              'qa-tester "run manual QA pass"'),
    AgentSpec("git-master", AgentCategory.DOMAIN_SPECIALIST, ModelTier.MEDIUM,
              "Commit strategy and history hygiene.",
              'git-master "prepare clean commit plan"'),
    AgentSpec("code-simplifier", AgentCategory.DOMAIN_SPECIALIST, ModelTier.HIGH,
              "Post-stop code simplification and cleanup automation.",
              'code-simplifier "simplify touched files"',
              is_internal=True),
    AgentSpec("researcher", AgentCategory.DOMAIN_SPECIALIST, ModelTier.MEDIUM,
              "Reference and external documentation research.",
              'researcher "collect official API docs"'),
    AgentSpec("parity-analyst", AgentCategory.DOMAIN_SPECIALIST, ModelTier.HIGH,
              "Maps oh-my-claudecode features to oh-my-copilot parity gaps and acceptance checks.",
              'parity-analyst "map OMC team mode parity"'),
    # Product
    AgentSpec("product-manager", AgentCategory.PRODUCT, ModelTier.MEDIUM,
              "Problem framing and PRD definition.",
              'product-manager "define user outcomes"'),
    AgentSpec("ux-researcher", AgentCategory.PRODUCT, ModelTier.MEDIUM,
              "Usability and accessibility audits.",
              'ux-researcher "run heuristic audit"'),
    AgentSpec("information-architect", AgentCategory.PRODUCT, ModelTier.MEDIUM,
              "Navigation, taxonomy, and structure.",
              'information-architect "improve docs IA"'),
    AgentSpec("product-analyst", AgentCategory.PRODUCT, ModelTier.MEDIUM,
              "Metrics, funnels, and experiments.",
              'product-analyst "analyze onboarding funnel"'),
    # Coordination
    AgentSpec("critic", AgentCategory.COORDINATION, ModelTier.HIGH,
              "Critical challenge for plans and designs.",
              'critic "challenge this plan"'),
    AgentSpec("scholastic", AgentCategory.COORDINATION, ModelTier.HIGH,
              "Ontology-first review for category mistakes, assumptions, and minimal repairs.",
              'scholastic "check this spec ontology"'),
    AgentSpec("vision", AgentCategory.COORDINATION, ModelTier.MEDIUM,
              "Image/screenshot and diagram analysis.",
              'vision "review this screenshot"'),
    AgentSpec("parity-verifier", AgentCategory.COORDINATION, ModelTier.HIGH,
              "Confirms a parity slice is implemented, tested, documented, and free of regressions.",
              'parity-verifier "verify autopilot parity"'),
]


@dataclass
class AgentInvocation:
    agent_name: str
    prompt: str
    spec: Optional[AgentSpec] = None
    output: str = ""
    success: bool = False


class AgentRegistry:
    def __init__(self):
        self._catalog: Dict[str, AgentSpec] = {a.name: a for a in AGENT_CATALOG}

    def get(self, name: str) -> Optional[AgentSpec]:
        return self._catalog.get(name)

    def list_by_category(self, category: AgentCategory) -> List[AgentSpec]:
        return [a for a in self._catalog.values() if a.category == category]

    def list_all(self) -> List[AgentSpec]:
        return [a for a in self._catalog.values() if not a.is_internal]

    def list_all_names(self) -> List[str]:
        return [a.name for a in self.list_all()]

    def exists(self, name: str) -> bool:
        return name in self._catalog
