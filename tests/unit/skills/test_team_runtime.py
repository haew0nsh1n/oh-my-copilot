"""Tests for team runtime skill."""

import pytest
from skills import TeamRuntimeSkill
from domain import (
    TeamControlAction,
    TeamStatus,
    WorkerStatus,
    TeamProvider,
    TeamRequirementStatus,
)


class TestTeamRuntimeSkillBasics:
    """Test basic team runtime skill functionality."""
    
    def test_skill_can_be_created(self):
        """RED: Skill can be instantiated."""
        skill = TeamRuntimeSkill()
        assert skill is not None
    
    def test_skill_has_name(self):
        """RED: Skill has a name."""
        skill = TeamRuntimeSkill()
        assert skill.name == "team-runtime"


class TestTeamCreation:
    """Test team creation."""
    
    def test_create_team(self):
        """RED: Can create a team."""
        skill = TeamRuntimeSkill()
        team = skill.create_team(
            "Auth Team",
            "Implement authentication",
            worker_count=3
        )
        assert team.name == "Auth Team"
        assert len(team.workers) == 3
        assert team.status == TeamStatus.IDLE
    
    def test_create_worker(self):
        """RED: Can create a worker."""
        skill = TeamRuntimeSkill()
        worker = skill.create_worker("Alice", "executor")
        assert worker.name == "Alice"
        assert worker.role == "executor"

    def test_prepare_provider_team(self):
        """Can prepare an OMP provider team request."""
        skill = TeamRuntimeSkill()

        request = skill.prepare_provider_team("2:codex", "review auth module")

        assert request.worker_count == 2
        assert request.provider == TeamProvider.CODEX
        assert request.goal_description == "review auth module"
        assert request.command_preview == "omp team 2:codex review auth module"

    def test_check_provider_team_requirements_ready(self):
        """Provider team requirements are ready when provider and tmux exist."""
        skill = TeamRuntimeSkill(executable_resolver=lambda command: f"/bin/{command}")

        readiness = skill.check_provider_team_requirements("2:codex", "review auth module")

        assert readiness.status == TeamRequirementStatus.READY
        assert readiness.provider_executable == "/bin/codex"
        assert readiness.tmux_executable == "/bin/tmux"

    def test_check_provider_team_requirements_blocked_without_tmux(self):
        """Provider team requirements block when tmux is missing."""
        skill = TeamRuntimeSkill(
            executable_resolver=lambda command: f"/bin/{command}" if command == "codex" else None
        )

        readiness = skill.check_provider_team_requirements("2:codex", "review auth module")

        assert readiness.status == TeamRequirementStatus.BLOCKED
        assert readiness.provider_executable == "/bin/codex"
        assert readiness.tmux_executable == ""

    def test_prepare_team_status_control(self):
        """Can prepare a provider team status control request."""
        skill = TeamRuntimeSkill()

        control = skill.prepare_team_control("status", "auth-review")

        assert control.action == TeamControlAction.STATUS
        assert control.team_name == "auth-review"
        assert control.command_preview == "omp team status auth-review"

    def test_prepare_team_shutdown_control(self):
        """Can prepare a provider team shutdown control request."""
        skill = TeamRuntimeSkill()

        control = skill.prepare_team_control("shutdown", "auth-review")

        assert control.action == TeamControlAction.SHUTDOWN
        assert control.team_name == "auth-review"
        assert control.command_preview == "omp team shutdown auth-review"

    def test_save_team_control_state(self, tmp_path):
        """Can persist provider team control state."""
        skill = TeamRuntimeSkill()
        control = skill.prepare_team_control("status", "auth-review")

        saved = skill.save_team_control(control, tmp_path)

        assert saved.path == tmp_path / "team-auth-review.json"
        text = saved.path.read_text()
        assert '"action": "status"' in text
        assert '"team_name": "auth-review"' in text


class TestTaskManagement:
    """Test task management."""
    
    def test_create_task(self):
        """RED: Can create a task."""
        skill = TeamRuntimeSkill()
        task = skill.create_task("Implement login endpoint")
        assert task.description == "Implement login endpoint"
        assert task.status == WorkerStatus.IDLE
    
    def test_assign_task_to_worker(self):
        """RED: Can assign tasks to workers."""
        skill = TeamRuntimeSkill()
        team = skill.create_team("Team", "Goal", worker_count=2)
        task = skill.create_task("Task 1")
        
        worker_id = team.workers[0].worker_id
        skill.assign_task_to_worker(team, task, worker_id)
        
        assert task.worker_id == worker_id
        assert len(team.workers[0].assigned_tasks) == 1
        assert len(team.tasks) == 1
    
    def test_distribute_tasks(self):
        """RED: Can distribute tasks round-robin."""
        skill = TeamRuntimeSkill()
        team = skill.create_team("Team", "Goal", worker_count=3)
        
        tasks = [
            skill.create_task("Task 1"),
            skill.create_task("Task 2"),
            skill.create_task("Task 3"),
        ]
        
        skill.distribute_tasks(team, tasks)
        
        assert len(team.tasks) == 3
        assert len(team.workers[0].assigned_tasks) == 1
        assert len(team.workers[1].assigned_tasks) == 1
        assert len(team.workers[2].assigned_tasks) == 1


class TestTaskExecution:
    """Test task execution."""
    
    def test_execute_task_lifecycle(self):
        """RED: Can track task lifecycle."""
        skill = TeamRuntimeSkill()
        team = skill.create_team("Team", "Goal")
        task = skill.create_task("Task")
        
        skill.assign_task_to_worker(team, task, team.workers[0].worker_id)
        
        skill.start_task(task)
        assert task.status == WorkerStatus.WORKING
        
        skill.complete_task(task, "Done")
        assert task.status == WorkerStatus.COMPLETED
        assert task.result == "Done"
    
    def test_task_failure(self):
        """RED: Can track task failures."""
        skill = TeamRuntimeSkill()
        task = skill.create_task("Task")
        
        skill.start_task(task)
        skill.fail_task(task, "Connection timeout")
        
        assert task.status == WorkerStatus.FAILED
        assert task.error == "Connection timeout"
    
    def test_task_progress(self):
        """RED: Can update task progress."""
        skill = TeamRuntimeSkill()
        task = skill.create_task("Task")
        
        skill.start_task(task)
        skill.update_task_progress(task, 50)
        assert task.progress == 50
        
        skill.update_task_progress(task, 100)
        assert task.progress == 100


class TestTeamExecution:
    """Test team execution."""
    
    def test_team_lifecycle(self):
        """RED: Can track team lifecycle."""
        skill = TeamRuntimeSkill()
        team = skill.create_team("Team", "Goal")
        
        skill.start_team(team)
        assert team.status == TeamStatus.RUNNING
        
        skill.complete_team(team)
        assert team.status == TeamStatus.COMPLETED


class TestReporting:
    """Test report generation."""
    
    def test_generate_team_report(self):
        """RED: Can generate team report."""
        skill = TeamRuntimeSkill()
        team = skill.create_team("Team", "Goal", worker_count=2)
        
        task1 = skill.create_task("Task 1")
        task2 = skill.create_task("Task 2")
        
        skill.distribute_tasks(team, [task1, task2])
        skill.complete_task(task1)
        
        report = skill.generate_report(team)
        assert report.total_tasks == 2
        assert report.completed_tasks == 1
        assert report.completion_percentage == 50.0
