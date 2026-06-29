"""Tests for CLI interface."""

import json
import tomllib

import pytest
from cli import CLI


class TestCLIBasics:
    """Test basic CLI functionality."""
    
    def test_cli_can_be_created(self):
        """RED: CLI can be instantiated."""
        cli = CLI()
        assert cli is not None
    
    def test_cli_has_name(self):
        """RED: CLI has a name."""
        cli = CLI()
        assert cli.name == "oh-my-copilot"
    
    def test_cli_has_version(self):
        """RED: CLI has a version."""
        cli = CLI()
        assert cli.version == "0.1.0"

    def test_public_omp_entry_point_targets_cli_main(self):
        """Public CLI parity exposes the omp command."""
        with open("pyproject.toml", "rb") as config_file:
            pyproject = tomllib.load(config_file)

        assert pyproject["project"]["scripts"]["omp"] == "cli:main"


class TestCLICommands:
    """Test CLI commands."""
    
    def test_help_command(self):
        """RED: Help command returns 0."""
        cli = CLI()
        result = cli.run(["help"])
        assert result == 0
    
    def test_version_command(self):
        """RED: Version command returns 0."""
        cli = CLI()
        result = cli.run(["version"])
        assert result == 0
    
    def test_brainstorm_command(self):
        """RED: Brainstorm command works."""
        cli = CLI()
        result = cli.run(["brainstorm", "How", "should", "we", "structure", "auth?"])
        assert result == 0
    
    def test_domain_command(self):
        """RED: Domain command works."""
        cli = CLI()
        result = cli.run(["domain", "PaymentSystem", "Process", "online", "payments"])
        assert result == 0
    
    def test_diagnose_command(self):
        """RED: Diagnose command works."""
        cli = CLI()
        result = cli.run(["diagnose", "Authentication", "fails", "intermittently"])
        assert result == 0
    
    def test_review_command(self):
        """RED: Review command works."""
        cli = CLI()
        result = cli.run(["review", "Add", "user", "authentication"])
        assert result == 0


class TestCLIErrorHandling:
    """Test CLI error handling."""
    
    def test_unknown_command(self):
        """RED: Unknown command returns error."""
        cli = CLI()
        result = cli.run(["unknown-command"])
        assert result != 0
    
    def test_no_args_shows_help(self):
        """RED: No arguments shows help."""
        cli = CLI()
        result = cli.run([])
        assert result == 0


class TestCanonicalWorkflowCommands:
    """Test canonical workflow CLI commands."""

    def test_interview_command(self):
        """interview command works."""
        cli = CLI()
        assert cli.run(["interview", "clarify the auth change"]) == 0

    def test_deep_interview_alias(self):
        """deep-interview alias works."""
        cli = CLI()
        assert cli.run(["deep-interview", "clarify scope"]) == 0

    def test_ralplan_command(self):
        """ralplan command works."""
        cli = CLI()
        assert cli.run(["ralplan", "OAuth2 redesign"]) == 0

    def test_prometheus_command(self):
        """prometheus command works."""
        cli = CLI()
        assert cli.run(["prometheus", "auth plan"]) == 0

    def test_prometheus_strict_alias(self):
        """prometheus-strict alias works."""
        cli = CLI()
        assert cli.run(["prometheus-strict", "auth plan"]) == 0

    def test_ultragoal_command(self):
        """ultragoal command works."""
        cli = CLI()
        assert cli.run(["ultragoal", "carry the approved plan"]) == 0

    def test_team_command(self):
        """team command works."""
        cli = CLI()
        assert cli.run(["team", "execute in parallel"]) == 0

    def test_team_provider_command(self, capsys):
        """team command prepares provider-backed workers."""
        cli = CLI()
        assert cli.run(["team", "2:codex", "review", "auth", "module"]) == 0
        output = capsys.readouterr().out
        assert "Provider: codex" in output
        assert "Workers: 2" in output
        assert "omp team 2:codex review auth module" in output

    def test_team_provider_check_command(self, capsys):
        """team --check reports provider-backed runtime requirements."""
        cli = CLI()
        assert cli.run(["team", "--check", "2:codex", "review", "auth", "module"]) == 0
        output = capsys.readouterr().out
        assert "Requirements:" in output
        assert "Provider executable:" in output
        assert "tmux executable:" in output

    def test_team_status_command(self, capsys):
        """team status prepares a provider team status request."""
        cli = CLI()
        assert cli.run(["team", "status", "auth-review"]) == 0
        output = capsys.readouterr().out
        assert "Control: status" in output
        assert "auth-review" in output
        assert "Saved:" in output

    def test_team_shutdown_command(self, capsys):
        """team shutdown prepares a provider team shutdown request."""
        cli = CLI()
        assert cli.run(["team", "shutdown", "auth-review"]) == 0
        output = capsys.readouterr().out
        assert "Control: shutdown" in output
        assert "auth-review" in output
        assert "Saved:" in output

    def test_ralph_command(self):
        """ralph command works."""
        cli = CLI()
        assert cli.run(["ralph", "complete the feature"]) == 0

    def test_code_review_alias(self):
        """code-review alias works."""
        cli = CLI()
        assert cli.run(["code-review", "auth feature"]) == 0

    def test_ultraqa_command(self):
        """ultraqa command works."""
        cli = CLI()
        assert cli.run(["ultraqa", "auth QA"]) == 0


class TestPlanningCLICommands:
    """Test planning CLI commands."""

    def test_plan_command(self):
        """plan command works."""
        cli = CLI()
        assert cli.run(["plan", "Q3-Roadmap", "Build scalable auth"]) == 0

    def test_plan_command_missing_vision(self):
        """plan command fails without vision."""
        cli = CLI()
        assert cli.run(["plan", "OnlyTitle"]) != 0


class TestResearchCLICommands:
    """Test research CLI commands."""

    def test_best_practice_command(self):
        """best-practice command works."""
        cli = CLI()
        assert cli.run(["best-practice", "OAuth2 token storage"]) == 0

    def test_best_practice_research_alias(self):
        """best-practice-research alias works."""
        cli = CLI()
        assert cli.run(["best-practice-research", "OAuth2"]) == 0

    def test_autoresearch_command(self):
        """autoresearch command works."""
        cli = CLI()
        assert cli.run(["autoresearch", "PKCE standard"]) == 0

    def test_autoresearch_goal_command(self):
        """autoresearch-goal command works."""
        cli = CLI()
        assert cli.run(["autoresearch-goal", "OAuth2 best practices"]) == 0


class TestExecutionModeCLICommands:
    """Test execution mode CLI commands."""

    def test_autopilot_command(self):
        """autopilot command works."""
        cli = CLI()
        assert cli.run(["autopilot", "implement auth end-to-end"]) == 0


class TestSpecializedCLICommands:
    """Test specialized CLI commands."""

    def test_sparkshell_command(self):
        """sparkshell command works."""
        cli = CLI()
        assert cli.run(["sparkshell", "ls -la"]) == 0

    def test_shell_alias(self):
        """shell alias works."""
        cli = CLI()
        assert cli.run(["shell", "ls -la"]) == 0

    def test_wiki_command(self):
        """wiki command works."""
        cli = CLI()
        assert cli.run(["wiki", "Auth Architecture"]) == 0

    def test_hooks_command(self):
        """hooks command works."""
        cli = CLI()
        assert cli.run(["hooks", "TASK_COMPLETED"]) == 0

    def test_github_command(self):
        """github command works."""
        cli = CLI()
        assert cli.run(["github", "Fix auth token expiry"]) == 0


class TestAgentShortcutCLICommands:
    """Test agent shortcut CLI commands."""

    def test_analyze_command(self):
        """analyze command works."""
        cli = CLI()
        assert cli.run(["analyze", "map auth flow"]) == 0

    def test_tdd_command(self):
        """tdd command works."""
        cli = CLI()
        assert cli.run(["tdd", "OAuth2 refresh token"]) == 0

    def test_security_review_command(self):
        """security-review command works."""
        cli = CLI()
        assert cli.run(["security-review", "auth module"]) == 0

    def test_build_fix_command(self):
        """build-fix command works."""
        cli = CLI()
        assert cli.run(["build-fix", "failing CI tests"]) == 0

    def test_git_master_command(self):
        """git-master command works."""
        cli = CLI()
        assert cli.run(["git-master", "clean commit history"]) == 0


class TestUtilityCLICommands:
    """Test utility CLI commands."""

    def test_skills_command(self):
        """skills command works."""
        cli = CLI()
        assert cli.run(["skills"]) == 0

    def test_doctor_command(self):
        """doctor command works."""
        cli = CLI()
        assert cli.run(["doctor"]) == 0

    def test_hud_command_summarizes_state(self, tmp_path, monkeypatch, capsys):
        """hud command summarizes persisted OMP state."""
        state_root = tmp_path / ".omp" / "state"
        state_root.mkdir(parents=True)
        (state_root / "wait.json").write_text(json.dumps({"action": "start"}))
        monkeypatch.chdir(tmp_path)

        cli = CLI()
        assert cli.run(["hud"]) == 0
        output = capsys.readouterr().out
        assert "Wait state: start" in output
        assert "State files: 1" in output

    def test_setup_command(self):
        """setup command works as the public OMP setup entry point."""
        cli = CLI()
        assert cli.run(["setup"]) == 0

    def test_ask_command(self):
        """ask command prepares a provider advisor request."""
        cli = CLI()
        assert cli.run(["ask", "codex", "review", "this", "patch"]) == 0

    def test_ask_check_command(self):
        """ask --check reports provider CLI availability."""
        cli = CLI()
        assert cli.run(["ask", "--check", "codex"]) == 0

    def test_ask_execute_command(self, capsys):
        """ask --execute runs or blocks provider CLI execution."""
        cli = CLI()
        assert cli.run(["ask", "--execute", "codex", "review", "this", "patch"]) == 0
        output = capsys.readouterr().out
        assert "Artifact:" in output

    def test_ask_execute_records_sanitized_session(self, tmp_path, monkeypatch):
        """ask --execute records sanitized session metadata."""
        monkeypatch.chdir(tmp_path)

        cli = CLI()
        assert cli.run(["ask", "--execute", "codex", "review", "this", "secret", "patch"]) == 0

        session_files = list((tmp_path / ".omp" / "sessions").glob("*.json"))
        assert len(session_files) == 1
        data = json.loads(session_files[0].read_text())
        assert data["command"] == "omp ask --execute codex"
        assert data["status"] == "blocked"
        assert data["friction_signals"] == [
            {"type": "operator-friction", "summary": "provider executable missing"}
        ]
        assert "secret patch" not in session_files[0].read_text()

    def test_wait_command(self, capsys):
        """wait command checks rate-limit wait state."""
        cli = CLI()
        assert cli.run(["wait"]) == 0
        output = capsys.readouterr().out
        assert "Wait:" in output

    def test_wait_command_restores_saved_state(self, tmp_path, monkeypatch, capsys):
        """wait command restores persisted wait state when present."""
        state_root = tmp_path / ".omp" / "state"
        state_root.mkdir(parents=True)
        (state_root / "wait.json").write_text(json.dumps({
            "action": "start",
            "status": "prepared",
            "tmux_required": True,
            "guidance": "Auto-resume start prepared",
        }))
        monkeypatch.chdir(tmp_path)

        cli = CLI()
        assert cli.run(["wait"]) == 0
        output = capsys.readouterr().out
        assert "Restored:" in output
        assert "Wait: start" in output

    def test_wait_start_command(self, capsys):
        """wait --start prepares auto-resume startup."""
        cli = CLI()
        assert cli.run(["wait", "--start"]) == 0
        output = capsys.readouterr().out
        assert "Saved:" in output

    def test_wait_stop_command(self, capsys):
        """wait --stop prepares auto-resume shutdown."""
        cli = CLI()
        assert cli.run(["wait", "--stop"]) == 0
        output = capsys.readouterr().out
        assert "Saved:" in output

    def test_session_friction_report_command(self):
        """session friction report command summarizes local friction."""
        cli = CLI()
        assert cli.run(["session", "friction", "report", "--since", "24h"]) == 0

    def test_session_friction_report_reads_session_files(self, tmp_path, monkeypatch, capsys):
        """session friction report reads local OMP session signal files."""
        sessions_root = tmp_path / ".omp" / "sessions"
        sessions_root.mkdir(parents=True)
        (sessions_root / "session-1.json").write_text(json.dumps({
            "friction_signals": [
                {"type": "context-bloat", "summary": "large context summary"}
            ]
        }))
        monkeypatch.chdir(tmp_path)

        cli = CLI()
        assert cli.run(["session", "friction", "report", "--since", "24h"]) == 0
        output = capsys.readouterr().out
        assert "Signals: 1" in output
        assert "context-bloat" in output

    def test_config_stop_callback_command(self, capsys):
        """config-stop-callback prepares notification configuration."""
        cli = CLI()
        assert cli.run([
            "config-stop-callback",
            "telegram",
            "--tag-list",
            "@alice,bob",
        ]) == 0
        output = capsys.readouterr().out
        assert "Saved:" in output

    def test_config_stop_callback_show_command(self, tmp_path, monkeypatch, capsys):
        """config-stop-callback --show restores notification configuration."""
        state_root = tmp_path / ".omp" / "state"
        state_root.mkdir(parents=True)
        (state_root / "notifications.json").write_text(
            '{"channel":"telegram","status":"prepared","tag_list":["@alice"]}'
        )
        monkeypatch.chdir(tmp_path)

        cli = CLI()
        assert cli.run(["config-stop-callback", "--show"]) == 0
        output = capsys.readouterr().out
        assert "Restored:" in output
        assert "telegram" in output

    def test_brainstorm_without_prompt(self):
        """RED: Brainstorm without prompt fails."""
        cli = CLI()
        result = cli.run(["brainstorm"])
        assert result == 1
    
    def test_domain_without_args(self):
        """RED: Domain without arguments fails."""
        cli = CLI()
        result = cli.run(["domain"])
        assert result == 1
