"""Domain model for lifecycle hooks."""

from dataclasses import dataclass, field
from typing import List, Callable, Dict, Any
from enum import Enum
from datetime import datetime


class HookEvent(str, Enum):
    """Lifecycle hook events."""
    PRE_SESSION = "pre_session"
    SESSION_STARTED = "session_started"
    TASK_STARTED = "task_started"
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"
    PRE_GOAL = "pre_goal"
    GOAL_STARTED = "goal_started"
    GOAL_COMPLETED = "goal_completed"
    GOAL_BLOCKED = "goal_blocked"
    SESSION_COMPLETED = "session_completed"
    SESSION_FAILED = "session_failed"
    POST_SESSION = "post_session"


class HookType(str, Enum):
    """Type of hook."""
    BEFORE = "before"
    AFTER = "after"
    ON_SUCCESS = "on_success"
    ON_ERROR = "on_error"


@dataclass
class HookHandler:
    """A handler for a lifecycle event."""
    name: str
    event: HookEvent
    handler_type: HookType
    action: str = ""  # Description of what the hook does
    priority: int = 0  # Higher priority runs first
    enabled: bool = True
    
    def __post_init__(self):
        """Validate handler."""
        if not self.name or not self.name.strip():
            raise ValueError("Handler name cannot be empty")
        if self.priority < -100 or self.priority > 100:
            raise ValueError("Priority must be between -100 and 100")


@dataclass
class HookExecution:
    """Execution record of a hook."""
    handler: HookHandler
    event: HookEvent
    executed_at: datetime = field(default_factory=datetime.now)
    duration_ms: float = 0.0
    success: bool = True
    error: str = ""
    output: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    
    def mark_failed(self, error: str) -> None:
        """Mark execution as failed."""
        self.success = False
        self.error = error


@dataclass
class HookRegistry:
    """Registry of all lifecycle hooks."""
    hooks: Dict[HookEvent, List[HookHandler]] = field(default_factory=dict)
    executions: List[HookExecution] = field(default_factory=list)
    
    def register_hook(self, handler: HookHandler) -> None:
        """Register a hook handler."""
        if handler.event not in self.hooks:
            self.hooks[handler.event] = []
        
        # Add hook in priority order
        hooks_list = self.hooks[handler.event]
        hooks_list.append(handler)
        hooks_list.sort(key=lambda h: h.priority, reverse=True)
    
    def unregister_hook(self, handler_name: str, event: HookEvent) -> None:
        """Unregister a hook handler."""
        if event not in self.hooks:
            return
        
        self.hooks[event] = [
            h for h in self.hooks[event]
            if h.name != handler_name
        ]
    
    def get_hooks(self, event: HookEvent) -> List[HookHandler]:
        """Get all hooks for an event."""
        return self.hooks.get(event, [])
    
    def get_enabled_hooks(self, event: HookEvent) -> List[HookHandler]:
        """Get all enabled hooks for an event."""
        return [h for h in self.get_hooks(event) if h.enabled]
    
    def record_execution(self, execution: HookExecution) -> None:
        """Record a hook execution."""
        self.executions.append(execution)
    
    def get_executions_for_event(self, event: HookEvent) -> List[HookExecution]:
        """Get all executions for an event."""
        return [e for e in self.executions if e.event == event]
    
    def get_failed_executions(self) -> List[HookExecution]:
        """Get all failed executions."""
        return [e for e in self.executions if not e.success]
