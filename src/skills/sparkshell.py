"""Sparkshell skill for shell command execution and validation."""

import subprocess
from typing import List, Tuple
from domain import (
    SparkshellSession,
    CommandExecution,
    CommandValidation,
    SparkshellReport,
    CommandStatus,
    CommandType,
)


class SparkshellSkill:
    """
    A skill for shell command execution with validation.
    
    This skill helps execute and validate shell commands safely,
    providing feedback on risks and outcomes.
    """
    
    def __init__(self):
        """Initialize the sparkshell skill."""
        self.name = "sparkshell"
        self.description = "Execute and validate shell commands with safety checks"
        
        # Dangerous command patterns that require approval
        self.dangerous_patterns = [
            "rm -rf",
            "git push",
            "git reset --hard",
            "git clean",
            "git branch -D",
            "git rebase",
            "dd if=",
            "> /dev/",
            "sudo",
            "chmod 777",
            "chown",
        ]
    
    def create_session(self, name: str) -> SparkshellSession:
        """
        Create a new sparkshell session.
        
        Args:
            name: Session name
            
        Returns:
            A new SparkshellSession
        """
        return SparkshellSession(name=name)
    
    def validate_command(
        self,
        command: str
    ) -> CommandValidation:
        """
        Validate a command before execution.
        
        Args:
            command: Command to validate
            
        Returns:
            A CommandValidation with safety assessment
        """
        validation = CommandValidation(
            command=command,
            is_safe=True,
            command_type=self._detect_command_type(command)
        )
        
        # Check for dangerous patterns
        for pattern in self.dangerous_patterns:
            if pattern in command:
                validation.is_safe = False
                validation.add_risk(f"Contains dangerous pattern: {pattern}")
                validation.requires_approval = True
        
        # Type-specific checks
        if validation.command_type == CommandType.WRITE:
            validation.add_risk("This command modifies the filesystem or repository")
            validation.requires_approval = True
        
        # Add suggestions
        if not validation.is_safe:
            validation.add_suggestion("Review the command carefully before execution")
            validation.add_suggestion("Ensure you have backups or can revert changes")
        
        return validation
    
    def _detect_command_type(self, command: str) -> CommandType:
        """Detect command type based on patterns."""
        write_commands = [
            "rm", "mv", "cp", "git push", "git reset",
            "git clean", "git branch -D", "git rebase",
            "dd", "chmod", "chown", "kill", "apt-get",
            "yum", "brew install", "npm install", "pip install"
        ]
        
        for write_cmd in write_commands:
            if write_cmd in command:
                return CommandType.WRITE
        
        return CommandType.READ
    
    def create_command(
        self,
        command: str,
        command_type: CommandType = CommandType.READ
    ) -> CommandExecution:
        """
        Create a command execution.
        
        Args:
            command: Command to execute
            command_type: Type of command
            
        Returns:
            A new CommandExecution
        """
        return CommandExecution(
            command=command,
            command_type=command_type
        )
    
    def execute_command(
        self,
        session: SparkshellSession,
        command: str,
        timeout: int = 30,
        cwd: str = None
    ) -> CommandExecution:
        """
        Execute a shell command.
        
        Args:
            session: Sparkshell session
            command: Command to execute
            timeout: Timeout in seconds
            cwd: Working directory
            
        Returns:
            CommandExecution with results
        """
        # Validate first
        validation = self.validate_command(command)
        session.add_validation(validation)
        
        # Create execution
        execution = self.create_command(command)
        session.add_command(execution)
        
        execution.start()
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd
            )
            
            execution.complete(
                exit_code=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr
            )
        except subprocess.TimeoutExpired:
            execution.timeout()
        except Exception as e:
            execution.complete(
                exit_code=-1,
                stderr=str(e)
            )
        
        return execution
    
    def execute_query(
        self,
        command: str,
        cwd: str = None
    ) -> str:
        """
        Execute a read-only query command and return output.
        
        Args:
            command: Query command (like git status, ls, etc.)
            cwd: Working directory
            
        Returns:
            Command output
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10,
                cwd=cwd
            )
            return result.stdout
        except Exception as e:
            return f"Error executing command: {str(e)}"
    
    def approve_command(
        self,
        validation: CommandValidation
    ) -> None:
        """
        Approve a dangerous command for execution.
        
        Args:
            validation: The validation to approve
        """
        validation.requires_approval = False
    
    def generate_report(self, session: SparkshellSession) -> SparkshellReport:
        """
        Generate a sparkshell session report.
        
        Args:
            session: The session
            
        Returns:
            A SparkshellReport
        """
        successful = len(session.get_successful_commands())
        failed = len(session.get_failed_commands())
        total = len(session.commands)
        
        summary = f"Executed {total} commands: "
        summary += f"{successful} successful, {failed} failed"
        
        # Build output summary
        output_parts = []
        for cmd in session.commands:
            if cmd.status == CommandStatus.SUCCESS:
                output_parts.append(f"✓ {cmd.command}")
                if cmd.stdout:
                    output_parts.append(f"  Output: {cmd.stdout[:100]}...")
            elif cmd.status == CommandStatus.FAILED:
                output_parts.append(f"✗ {cmd.command}")
                if cmd.stderr:
                    output_parts.append(f"  Error: {cmd.stderr[:100]}...")
        
        output_summary = "\n".join(output_parts)
        
        return SparkshellReport(
            session=session,
            total_commands=total,
            successful_commands=successful,
            failed_commands=failed,
            summary=summary,
            output_summary=output_summary
        )
