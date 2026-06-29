"""Tests for sparkshell skill."""

import pytest
from skills import SparkshellSkill
from domain import CommandType, CommandStatus


class TestSparkshellSkillBasics:
    """Test basic sparkshell skill functionality."""
    
    def test_skill_can_be_created(self):
        """RED: Skill can be instantiated."""
        skill = SparkshellSkill()
        assert skill is not None
    
    def test_skill_has_name(self):
        """RED: Skill has a name."""
        skill = SparkshellSkill()
        assert skill.name == "sparkshell"


class TestSessionCreation:
    """Test session creation."""
    
    def test_create_session(self):
        """RED: Can create a session."""
        skill = SparkshellSkill()
        session = skill.create_session("Git operations")
        assert session.name == "Git operations"
        assert len(session.commands) == 0


class TestCommandValidation:
    """Test command validation."""
    
    def test_validate_safe_command(self):
        """RED: Can validate safe commands."""
        skill = SparkshellSkill()
        validation = skill.validate_command("git status")
        assert validation.is_safe is True
        assert validation.requires_approval is False
        assert validation.command_type == CommandType.READ
    
    def test_validate_dangerous_command(self):
        """RED: Can identify dangerous commands."""
        skill = SparkshellSkill()
        validation = skill.validate_command("rm -rf /")
        assert validation.is_safe is False
        assert validation.requires_approval is True
        assert len(validation.risks) > 0
    
    def test_write_command_detection(self):
        """RED: Detects write commands."""
        skill = SparkshellSkill()
        validation = skill.validate_command("git push origin main")
        assert validation.command_type == CommandType.WRITE
        assert validation.requires_approval is True
    
    def test_command_approval(self):
        """RED: Can approve dangerous commands."""
        skill = SparkshellSkill()
        validation = skill.validate_command("git reset --hard")
        assert validation.requires_approval is True
        
        skill.approve_command(validation)
        assert validation.requires_approval is False


class TestCommandExecution:
    """Test command execution."""
    
    def test_create_command(self):
        """RED: Can create a command."""
        skill = SparkshellSkill()
        cmd = skill.create_command("ls -la", CommandType.READ)
        assert cmd.command == "ls -la"
        assert cmd.status == CommandStatus.PENDING
    
    def test_query_execution(self):
        """RED: Can execute query commands."""
        skill = SparkshellSkill()
        # Execute a simple, safe query
        output = skill.execute_query("echo 'test'")
        assert "test" in output
    
    def test_session_validation(self):
        """RED: Commands are validated in sessions."""
        skill = SparkshellSkill()
        session = skill.create_session("Test")
        
        # Simulate a command execution
        execution = skill.create_command("echo 'hello'")
        session.add_command(execution)
        
        validation = skill.validate_command("echo 'hello'")
        session.add_validation(validation)
        
        assert len(session.validations) > 0


class TestReporting:
    """Test report generation."""
    
    def test_generate_report(self):
        """RED: Can generate session report."""
        skill = SparkshellSkill()
        session = skill.create_session("Test")
        
        # Create mock commands
        cmd1 = skill.create_command("echo 'test'")
        cmd1.status = CommandStatus.SUCCESS
        cmd1.stdout = "test"
        session.add_command(cmd1)
        
        cmd2 = skill.create_command("invalid command")
        cmd2.status = CommandStatus.FAILED
        cmd2.stderr = "command not found"
        session.add_command(cmd2)
        
        report = skill.generate_report(session)
        assert report.total_commands == 2
        assert report.successful_commands == 1
        assert report.failed_commands == 1
