"""Skill implementations for oh-my-copilot."""

from .brainstorming import BrainstormingSkill
from .domain_modeling import DomainModelingSkill
from .diagnostics import DiagnosticSkill
from .code_review import CodeReviewSkill
from .github_integration import GitHubIntegrationSkill
from .deep_interview import DeepInterviewSkill
from .ultragoal import UltragoalSkill
from .team_runtime import TeamRuntimeSkill
from .sparkshell import SparkshellSkill
from .wiki import WikiSkill
from .hooks import HooksSkill
from .prometheus_strict import PrometheusStrictSkill
from .autoresearch import AutoresearchSkill
from .best_practice_research import BestPracticeResearchSkill
from .ralplan import RalPlanSkill
from .ralph import RalphSkill
from .ultraqa import UltraQASkill
from .autoresearch_goal import AutoresearchGoalSkill
from .autopilot import AutopilotSkill
from .strategic_plan import StrategicPlanSkill
from .ultrawork import UltraworkSkill
from .visual_verdict import VisualVerdictSkill
from .ecomode import EcomodeSkill
from .swarm import SwarmSkill
from .deep_search import DeepSearchSkill
from .design import DesignSkill
from .visual_ralph import VisualRalphSkill
from .agent_catalog import AgentCatalogSkill
from .provider_advisor import ProviderAdvisorSkill
from .rate_limit_wait import RateLimitWaitSkill
from .session_friction import SessionFrictionSkill
from .notification_config import NotificationConfigSkill
from .project_setup import ProjectSetupSkill

__all__ = [
    "BrainstormingSkill",
    "DomainModelingSkill",
    "DiagnosticSkill",
    "CodeReviewSkill",
    "GitHubIntegrationSkill",
    "DeepInterviewSkill",
    "UltragoalSkill",
    "TeamRuntimeSkill",
    "SparkshellSkill",
    "WikiSkill",
    "HooksSkill",
    "PrometheusStrictSkill",
    "AutoresearchSkill",
    "BestPracticeResearchSkill",
    "RalPlanSkill",
    "RalphSkill",
    "UltraQASkill",
    "AutoresearchGoalSkill",
    "AutopilotSkill",
    "StrategicPlanSkill",
    "UltraworkSkill",
    "VisualVerdictSkill",
    "EcomodeSkill",
    "SwarmSkill",
    "DeepSearchSkill",
    "DesignSkill",
    "VisualRalphSkill",
    "AgentCatalogSkill",
    "ProviderAdvisorSkill",
    "RateLimitWaitSkill",
    "SessionFrictionSkill",
    "NotificationConfigSkill",
    "ProjectSetupSkill",
]
