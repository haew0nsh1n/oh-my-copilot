"""Domain model for sparkshell shell command execution."""

from dataclasses import dataclass, field
from typing import List, Dict
from enum import Enum
from datetime import datetime


class CommandStatus(str, Enum):
    """Status of a shell command."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"


class CommandType(str, Enum):
    """Type of shell command."""
    READ = "read"  # Non-destructive (git status, ls, etc.)
    WRITE = "write"  # Potentially destructive (rm, git push, etc.)
    QUERY = "query"  # Information gathering


@dataclass
class CommandExecution:
    """Execution of a shell command."""
    command: str
    status: CommandStatus = CommandStatus.PENDING
    command_type: CommandType = CommandType.READ
    exit_code: int = None
    stdout: str = ""
    stderr: str = ""
    started_at: datetime = None
    completed_at: datetime = None
    duration_seconds: float = 0.0
    
    def __post_init__(self):
        """Validate execution."""
        if not self.command or not self.command.strip():
            raise ValueError("Command cannot be empty")
    
    def start(self) -> None:
        """Mark command as started."""
        self.status = CommandStatus.RUNNING
        self.started_at = datetime.now()
    
    def complete(
        self,
        exit_code: int,
        stdout: str = "",
        stderr: str = ""
    ) -> None:
        """Mark command as completed."""
        self.exit_code = exit_code
        self.stdout = stdout
        self.stderr = stderr
        self.completed_at = datetime.now()
        
        if self.started_at:
            self.duration_seconds = (self.completed_at - self.started_at).total_seconds()
        
        if exit_code == 0:
            self.status = CommandStatus.SUCCESS
        else:
            self.status = CommandStatus.FAILED
    
    def timeout(self) -> None:
        """Mark command as timed out."""
        self.status = CommandStatus.TIMEOUT
        self.completed_at = datetime.now()
        if self.started_at:
            self.duration_seconds = (self.completed_at - self.started_at).total_seconds()


@dataclass
class CommandValidation:
    """Validation result for a command."""
    command: str
    is_safe: bool
    risks: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    command_type: CommandType = CommandType.READ
    requires_approval: bool = False
    
    def add_risk(self, risk: str) -> None:
        """Add a risk."""
        if risk not in self.risks:
            self.risks.append(risk)
    
    def add_suggestion(self, suggestion: str) -> None:
        """Add a suggestion."""
        if suggestion not in self.suggestions:
            self.suggestions.append(suggestion)


@dataclass
class SparkshellSession:
    """A sparkshell session for command execution."""
    name: str
    commands: List[CommandExecution] = field(default_factory=list)
    validations: Dict[str, CommandValidation] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    environment: dict = field(default_factory=dict)  # env vars, cwd, etc.
    
    def __post_init__(self):
        """Validate session."""
        if not self.name or not self.name.strip():
            raise ValueError("Session name cannot be empty")
    
    def add_command(self, command: CommandExecution) -> None:
        """Add a command to the session."""
        if command in self.commands:
            raise ValueError("Command already in session")
        self.commands.append(command)
    
    def add_validation(self, validation: CommandValidation) -> None:
        """Add a validation to the session."""
        self.validations[validation.command] = validation
    
    def get_validation(self, command: str) -> CommandValidation:
        """Get validation for a command."""
        return self.validations.get(command)
    
    def get_successful_commands(self) -> List[CommandExecution]:
        """Get all successful commands."""
        return [c for c in self.commands if c.status == CommandStatus.SUCCESS]
    
    def get_failed_commands(self) -> List[CommandExecution]:
        """Get all failed commands."""
        return [c for c in self.commands if c.status == CommandStatus.FAILED]


@dataclass
class SparkshellReport:
    """Report on sparkshell session."""
    session: SparkshellSession
    total_commands: int
    successful_commands: int
    failed_commands: int
    summary: str = ""
    output_summary: str = ""
    
    def __post_init__(self):
        """Validate report."""
        if self.total_commands < 0:
            raise ValueError("Total commands cannot be negative")
