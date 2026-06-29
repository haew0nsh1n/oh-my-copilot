"""Tests for hooks skill."""

import pytest
from skills import HooksSkill
from domain import HookEvent, HookType


class TestHooksSkillBasics:
    """Test basic hooks skill functionality."""
    
    def test_skill_can_be_created(self):
        """RED: Skill can be instantiated."""
        skill = HooksSkill()
        assert skill is not None
    
    def test_skill_has_name(self):
        """RED: Skill has a name."""
        skill = HooksSkill()
        assert skill.name == "hooks"


class TestHookRegistration:
    """Test hook registration."""
    
    def test_register_hook(self):
        """RED: Can register a hook."""
        skill = HooksSkill()
        
        def log_session_start(context):
            pass
        
        handler = skill.register_hook(
            "log_session_start",
            HookEvent.SESSION_STARTED,
            HookType.AFTER,
            log_session_start
        )
        
        assert handler.name == "log_session_start"
        assert handler.event == HookEvent.SESSION_STARTED
    
    def test_unregister_hook(self):
        """RED: Can unregister a hook."""
        skill = HooksSkill()
        
        def dummy(context):
            pass
        
        skill.register_hook("hook1", HookEvent.SESSION_STARTED, HookType.AFTER, dummy)
        
        hooks = skill.get_hooks_for_event(HookEvent.SESSION_STARTED)
        assert len(hooks) == 1
        
        skill.unregister_hook("hook1", HookEvent.SESSION_STARTED)
        
        hooks = skill.get_hooks_for_event(HookEvent.SESSION_STARTED)
        assert len(hooks) == 0


class TestHookExecution:
    """Test hook execution."""
    
    def test_execute_hooks(self):
        """RED: Can execute hooks."""
        skill = HooksSkill()
        
        execution_log = []
        
        def hook1(context):
            execution_log.append("hook1")
        
        def hook2(context):
            execution_log.append("hook2")
        
        skill.register_hook("h1", HookEvent.TASK_COMPLETED, HookType.AFTER, hook1, priority=1)
        skill.register_hook("h2", HookEvent.TASK_COMPLETED, HookType.AFTER, hook2, priority=2)
        
        executions = skill.execute_hooks(HookEvent.TASK_COMPLETED)
        
        assert len(executions) == 2
        assert execution_log[0] == "hook2"  # Higher priority runs first
        assert execution_log[1] == "hook1"
    
    def test_hook_with_context(self):
        """RED: Hooks receive context."""
        skill = HooksSkill()
        
        captured_context = {}
        
        def hook(context):
            captured_context.update(context)
        
        skill.register_hook("h", HookEvent.GOAL_COMPLETED, HookType.AFTER, hook)
        
        context = {"goal_id": "123", "status": "completed"}
        executions = skill.execute_hooks(HookEvent.GOAL_COMPLETED, context)
        
        assert captured_context["goal_id"] == "123"


class TestHookControl:
    """Test hook enable/disable."""
    
    def test_enable_disable_hook(self):
        """RED: Can enable/disable hooks."""
        skill = HooksSkill()
        
        execution_log = []
        
        def hook(context):
            execution_log.append("executed")
        
        skill.register_hook("h", HookEvent.SESSION_STARTED, HookType.AFTER, hook)
        
        # Execute with hook enabled
        skill.execute_hooks(HookEvent.SESSION_STARTED)
        assert len(execution_log) == 1
        
        # Disable and execute
        skill.disable_hook("h", HookEvent.SESSION_STARTED)
        skill.execute_hooks(HookEvent.SESSION_STARTED)
        assert len(execution_log) == 1  # Not executed again
        
        # Re-enable and execute
        skill.enable_hook("h", HookEvent.SESSION_STARTED)
        skill.execute_hooks(HookEvent.SESSION_STARTED)
        assert len(execution_log) == 2


class TestHookHistory:
    """Test execution history."""
    
    def test_get_execution_history(self):
        """RED: Can get execution history."""
        skill = HooksSkill()
        
        def hook(context):
            pass
        
        skill.register_hook("h", HookEvent.TASK_STARTED, HookType.BEFORE, hook)
        
        skill.execute_hooks(HookEvent.TASK_STARTED)
        skill.execute_hooks(HookEvent.TASK_STARTED)
        
        history = skill.get_execution_history(HookEvent.TASK_STARTED)
        assert len(history) == 2
    
    def test_get_failed_executions(self):
        """RED: Can track failed executions."""
        skill = HooksSkill()
        
        def failing_hook(context):
            raise Exception("Hook failed")
        
        def success_hook(context):
            pass
        
        skill.register_hook("fail", HookEvent.GOAL_BLOCKED, HookType.AFTER, failing_hook)
        skill.register_hook("success", HookEvent.GOAL_BLOCKED, HookType.AFTER, success_hook)
        
        skill.execute_hooks(HookEvent.GOAL_BLOCKED)
        
        failed = skill.get_failed_executions()
        assert len(failed) == 1
        assert "Hook failed" in failed[0].error


class TestHookMetadata:
    """Test hook metadata."""
    
    def test_get_all_hooks(self):
        """RED: Can get all hooks."""
        skill = HooksSkill()
        
        def hook(context):
            pass
        
        skill.register_hook("h1", HookEvent.SESSION_STARTED, HookType.AFTER, hook)
        skill.register_hook("h2", HookEvent.SESSION_COMPLETED, HookType.AFTER, hook)
        
        all_hooks = skill.get_all_hooks()
        
        assert HookEvent.SESSION_STARTED in all_hooks
        assert HookEvent.SESSION_COMPLETED in all_hooks
        assert len(all_hooks[HookEvent.SESSION_STARTED]) == 1
        assert len(all_hooks[HookEvent.SESSION_COMPLETED]) == 1
