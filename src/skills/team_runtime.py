"""Team runtime skill for coordinated parallel execution."""

import json
import re
from shutil import which
from pathlib import Path
from typing import List
from typing import Callable
from domain import (
    Team,
    Worker,
    WorkerTask,
    TeamReport,
    ProviderTeamRequest,
    ProviderTeamReadiness,
    TeamControlAction,
    TeamControlArtifact,
    TeamControlRequest,
    TeamProvider,
    TeamRequirementStatus,
    WorkerStatus,
    TeamStatus,
)
import uuid


class TeamRuntimeSkill:
    """
    A skill for coordinated parallel execution with multiple workers.
    
    This skill manages team creation, worker assignment, task distribution,
    and progress tracking for concurrent work.
    """
    
    def __init__(self, executable_resolver: Callable[[str], str | None] = which):
        """Initialize the team runtime skill."""
        self.name = "team-runtime"
        self.description = "Coordinate parallel execution with multiple workers"
        self.executable_resolver = executable_resolver
    
    def create_team(
        self,
        name: str,
        goal_description: str,
        worker_count: int = 3
    ) -> Team:
        """
        Create a new team.
        
        Args:
            name: Team name
            goal_description: Description of team's goal
            worker_count: Number of workers to create
            
        Returns:
            A new Team with workers
        """
        team = Team(
            team_id=str(uuid.uuid4()),
            name=name,
            goal_description=goal_description
        )
        
        # Create workers
        for i in range(worker_count):
            worker = Worker(
                worker_id=str(uuid.uuid4()),
                name=f"Worker-{i+1}",
                role="executor"
            )
            team.add_worker(worker)
        
        return team
    
    def create_worker(
        self,
        name: str,
        role: str = "executor"
    ) -> Worker:
        """
        Create a new worker.
        
        Args:
            name: Worker name
            role: Worker role (executor, reviewer, etc.)
            
        Returns:
            A new Worker
        """
        return Worker(
            worker_id=str(uuid.uuid4()),
            name=name,
            role=role
        )

    def prepare_provider_team(
        self,
        provider_spec: str,
        goal_description: str
    ) -> ProviderTeamRequest:
        """
        Prepare an OMP provider-backed team request.

        Args:
            provider_spec: Provider spec in the form N:provider
            goal_description: Goal for the provider team

        Returns:
            A prepared ProviderTeamRequest
        """
        if ":" not in provider_spec:
            raise ValueError("Provider spec must use N:provider format")

        count_text, provider_text = provider_spec.split(":", 1)
        worker_count = int(count_text)
        provider = TeamProvider(provider_text)
        return ProviderTeamRequest(
            worker_count=worker_count,
            provider=provider,
            goal_description=goal_description,
        )

    def check_provider_team_requirements(
        self,
        provider_spec: str,
        goal_description: str,
    ) -> ProviderTeamReadiness:
        """Check local requirements for provider-backed team execution."""
        request = self.prepare_provider_team(provider_spec, goal_description)
        provider_executable = self.executable_resolver(request.provider.value) or ""
        tmux_executable = self.executable_resolver("tmux") or ""
        status = (
            TeamRequirementStatus.READY
            if provider_executable and tmux_executable
            else TeamRequirementStatus.BLOCKED
        )
        return ProviderTeamReadiness(
            request=request,
            status=status,
            provider_executable=provider_executable,
            tmux_executable=tmux_executable,
        )

    def prepare_team_control(self, action: str, team_name: str) -> TeamControlRequest:
        """Prepare a provider team control request."""
        control_action = TeamControlAction(action)
        return TeamControlRequest(action=control_action, team_name=team_name)

    def save_team_control(
        self,
        control: TeamControlRequest,
        state_root: Path | str,
    ) -> TeamControlArtifact:
        """Persist provider team control state."""
        root = Path(state_root)
        root.mkdir(parents=True, exist_ok=True)
        safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "-", control.team_name).strip("-")
        path = root / f"team-{safe_name}.json"
        path.write_text(
            json.dumps(
                {
                    "action": control.action.value,
                    "team_name": control.team_name,
                    "command_preview": control.command_preview,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )
        return TeamControlArtifact(action=control.action, path=path)
    
    def create_task(
        self,
        description: str
    ) -> WorkerTask:
        """
        Create a new task.
        
        Args:
            description: Task description
            
        Returns:
            A new WorkerTask
        """
        return WorkerTask(
            task_id=str(uuid.uuid4()),
            description=description,
            worker_id=""  # Will be assigned when added to worker
        )
    
    def assign_task_to_worker(
        self,
        team: Team,
        task: WorkerTask,
        worker_id: str
    ) -> None:
        """
        Assign a task to a specific worker.
        
        Args:
            team: The team
            task: The task to assign
            worker_id: ID of the worker
        """
        worker = team.get_worker(worker_id)
        if not worker:
            raise ValueError(f"Worker {worker_id} not found")
        
        task.worker_id = worker_id
        worker.assign_task(task)
        team.add_task(task)
    
    def distribute_tasks(
        self,
        team: Team,
        tasks: List[WorkerTask]
    ) -> None:
        """
        Distribute tasks among workers round-robin style.
        
        Args:
            team: The team
            tasks: Tasks to distribute
        """
        if not team.workers:
            raise ValueError("Team has no workers")
        
        for i, task in enumerate(tasks):
            worker = team.workers[i % len(team.workers)]
            self.assign_task_to_worker(team, task, worker.worker_id)
    
    def start_team(self, team: Team) -> None:
        """
        Start the team execution.
        
        Args:
            team: The team to start
        """
        team.start()
    
    def start_task(self, task: WorkerTask) -> None:
        """
        Start executing a task.
        
        Args:
            task: The task to start
        """
        task.start()
    
    def complete_task(
        self,
        task: WorkerTask,
        result: str = ""
    ) -> None:
        """
        Mark a task as completed.
        
        Args:
            task: The task
            result: Task result/output
        """
        task.complete(result)
    
    def fail_task(
        self,
        task: WorkerTask,
        error: str = ""
    ) -> None:
        """
        Mark a task as failed.
        
        Args:
            task: The task
            error: Error message
        """
        task.fail(error)
    
    def update_task_progress(
        self,
        task: WorkerTask,
        progress: int
    ) -> None:
        """
        Update task progress.
        
        Args:
            task: The task
            progress: Progress percentage (0-100)
        """
        task.update_progress(progress)
    
    def complete_team(self, team: Team) -> None:
        """
        Mark team as completed.
        
        Args:
            team: The team
        """
        team.complete()
    
    def pause_team(self, team: Team) -> None:
        """
        Pause team execution.
        
        Args:
            team: The team
        """
        team.pause()
    
    def fail_team(self, team: Team) -> None:
        """
        Mark team as failed.
        
        Args:
            team: The team
        """
        team.fail()
    
    def generate_report(self, team: Team) -> TeamReport:
        """
        Generate a team execution report.
        
        Args:
            team: The team
            
        Returns:
            A TeamReport
        """
        completed = len(team.get_completed_tasks())
        in_progress = len(team.get_in_progress_tasks())
        pending = len(team.get_pending_tasks())
        failed = len(team.get_failed_tasks())
        total = len(team.tasks)
        
        completion_pct = team.completion_percentage()
        
        summary = f"Team '{team.name}': "
        summary += f"{completion_pct:.0f}% complete "
        summary += f"({completed}/{total} tasks done)"
        
        if failed > 0:
            summary += f", {failed} failed"
        
        if in_progress > 0:
            summary += f", {in_progress} in progress"
        
        return TeamReport(
            team=team,
            total_workers=len(team.workers),
            total_tasks=total,
            completed_tasks=completed,
            in_progress_tasks=in_progress,
            pending_tasks=pending,
            failed_tasks=failed,
            completion_percentage=completion_pct,
            summary=summary
        )
