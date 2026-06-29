"""Hooks skill for lifecycle management."""

from typing import Callable, List, Dict, Any
from datetime import datetime
from domain import (
    HookRegistry,
    HookHandler,
    HookExecution,
    HookEvent,
    HookType,
)


class HooksSkill:
    """
    A skill for managing lifecycle hooks.
    
    This skill allows registering and executing hooks at various lifecycle
    points (session start, task complete, goal failed, etc.).
    """
    
    def __init__(self):
        """Initialize the hooks skill."""
        self.name = "hooks"
        self.description = "Manage lifecycle hooks and event handlers"
        self.registry = HookRegistry()
        self._hook_actions: Dict[str, Callable] = {}  # Store actual callables
    
    def register_hook(
        self,
        name: str,
        event: HookEvent,
        handler_type: HookType,
        action: Callable,
        priority: int = 0
    ) -> HookHandler:
        """
        Register a new hook.
        
        Args:
            name: Hook name
            event: Event to hook into
            handler_type: Type of hook (before/after/etc.)
            action: Callable to execute
            priority: Execution priority
            
        Returns:
            The registered HookHandler
        """
        handler = HookHandler(
            name=name,
            event=event,
            handler_type=handler_type,
            action=name,  # Store name, actual callable in separate dict
            priority=priority
        )
        
        self.registry.register_hook(handler)
        self._hook_actions[name] = action
        
        return handler
    
    def unregister_hook(
        self,
        handler_name: str,
        event: HookEvent
    ) -> None:
        """
        Unregister a hook.
        
        Args:
            handler_name: Name of the handler
            event: Event the hook was registered for
        """
        self.registry.unregister_hook(handler_name, event)
        if handler_name in self._hook_actions:
            del self._hook_actions[handler_name]
    
    def enable_hook(
        self,
        handler_name: str,
        event: HookEvent
    ) -> None:
        """
        Enable a hook.
        
        Args:
            handler_name: Name of the handler
            event: Hook event
        """
        for handler in self.registry.get_hooks(event):
            if handler.name == handler_name:
                handler.enabled = True
                break
    
    def disable_hook(
        self,
        handler_name: str,
        event: HookEvent
    ) -> None:
        """
        Disable a hook.
        
        Args:
            handler_name: Name of the handler
            event: Hook event
        """
        for handler in self.registry.get_hooks(event):
            if handler.name == handler_name:
                handler.enabled = False
                break
    
    def execute_hooks(
        self,
        event: HookEvent,
        context: Dict[str, Any] = None
    ) -> List[HookExecution]:
        """
        Execute all hooks for an event.
        
        Args:
            event: The event
            context: Context to pass to hooks
            
        Returns:
            List of HookExecution records
        """
        context = context or {}
        executions = []
        
        for handler in self.registry.get_enabled_hooks(event):
            execution = self._execute_hook(handler, event, context)
            executions.append(execution)
            self.registry.record_execution(execution)
        
        return executions
    
    def _execute_hook(
        self,
        handler: HookHandler,
        event: HookEvent,
        context: Dict[str, Any]
    ) -> HookExecution:
        """
        Execute a single hook.
        
        Args:
            handler: The handler
            event: The event
            context: Context
            
        Returns:
            HookExecution record
        """
        execution = HookExecution(
            handler=handler,
            event=event,
            context=context
        )
        
        try:
            start_time = datetime.now()
            
            # Get the actual callable
            if handler.action in self._hook_actions:
                action = self._hook_actions[handler.action]
                action(context)
            
            end_time = datetime.now()
            execution.duration_ms = (end_time - start_time).total_seconds() * 1000
            
        except Exception as e:
            execution.mark_failed(str(e))
        
        return execution
    
    def get_hooks_for_event(self, event: HookEvent) -> List[HookHandler]:
        """
        Get all hooks for an event.
        
        Args:
            event: The event
            
        Returns:
            List of HookHandlers
        """
        return self.registry.get_hooks(event)
    
    def get_all_hooks(self) -> Dict[HookEvent, List[HookHandler]]:
        """
        Get all registered hooks.
        
        Returns:
            Dictionary of event -> handlers
        """
        return self.registry.hooks
    
    def get_execution_history(self, event: HookEvent = None) -> List[HookExecution]:
        """
        Get execution history.
        
        Args:
            event: Optional event to filter by
            
        Returns:
            List of HookExecutions
        """
        if event:
            return self.registry.get_executions_for_event(event)
        return self.registry.executions
    
    def get_failed_executions(self) -> List[HookExecution]:
        """
        Get all failed hook executions.
        
        Returns:
            List of failed HookExecutions
        """
        return self.registry.get_failed_executions()
