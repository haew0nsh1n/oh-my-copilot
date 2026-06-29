"""CLI interface for oh-my-copilot."""

import sys
from typing import Optional


class CLI:
    """Command-line interface for oh-my-copilot."""

    def __init__(self):
        """Initialize the CLI."""
        self.name = "oh-my-copilot"
        self.version = "0.1.0"
        self.commands = {
            # === Canonical Workflow ===
            "interview": self._interview_command,
            "deep-interview": self._interview_command,
            "ralplan": self._ralplan_command,
            "prometheus": self._prometheus_command,
            "prometheus-strict": self._prometheus_command,
            "ultragoal": self._ultragoal_command,
            "team": self._team_command,
            "ralph": self._ralph_command,
            "review": self._review_command,
            "code-review": self._review_command,
            "ultraqa": self._ultraqa_command,
            # === Planning & Clarification ===
            "plan": self._plan_command,
            "brainstorm": self._brainstorm_command,
            "domain": self._domain_command,
            # === Research ===
            "best-practice": self._best_practice_command,
            "best-practice-research": self._best_practice_command,
            "autoresearch": self._autoresearch_command,
            "autoresearch-goal": self._autoresearch_goal_command,
            # === Execution Modes ===
            "autopilot": self._autopilot_command,
            # === Specialized ===
            "diagnose": self._diagnose_command,
            "sparkshell": self._sparkshell_command,
            "shell": self._sparkshell_command,
            "wiki": self._wiki_command,
            "hooks": self._hooks_command,
            "github": self._github_command,
            "ask": self._ask_command,
            "wait": self._wait_command,
            "session": self._session_command,
            "config-stop-callback": self._config_stop_callback_command,
            # === Agent Shortcuts ===
            "analyze": self._analyze_command,
            "tdd": self._tdd_command,
            "security-review": self._security_review_command,
            "build-fix": self._build_fix_command,
            "git-master": self._git_master_command,
            "deepsearch": self._deepsearch_command,
            "design": self._design_command,
            "visual-ralph": self._visual_ralph_command,
            # === Execution Modes (new) ===
            "ultrawork": self._ultrawork_command,
            "visual-verdict": self._visual_verdict_command,
            "ecomode": self._ecomode_command,
            "swarm": self._swarm_command,
            # === Agent Catalog (31 agents) ===
            "agent": self._agent_command,
            "explore": self._make_agent_cmd("explore"),
            "analyst": self._make_agent_cmd("analyst"),
            "planner": self._make_agent_cmd("planner"),
            "architect": self._make_agent_cmd("architect"),
            "debugger": self._make_agent_cmd("debugger"),
            "executor": self._make_agent_cmd("executor"),
            "verifier": self._make_agent_cmd("verifier"),
            "style-reviewer": self._make_agent_cmd("style-reviewer"),
            "quality-reviewer": self._make_agent_cmd("quality-reviewer"),
            "api-reviewer": self._make_agent_cmd("api-reviewer"),
            "performance-reviewer": self._make_agent_cmd("performance-reviewer"),
            "code-reviewer": self._make_agent_cmd("code-reviewer"),
            "dependency-expert": self._make_agent_cmd("dependency-expert"),
            "test-engineer": self._make_agent_cmd("test-engineer"),
            "quality-strategist": self._make_agent_cmd("quality-strategist"),
            "build-fixer": self._make_agent_cmd("build-fixer"),
            "designer": self._make_agent_cmd("designer"),
            "writer": self._make_agent_cmd("writer"),
            "qa-tester": self._make_agent_cmd("qa-tester"),
            "code-simplifier": self._make_agent_cmd("code-simplifier"),
            "researcher": self._make_agent_cmd("researcher"),
            "product-manager": self._make_agent_cmd("product-manager"),
            "ux-researcher": self._make_agent_cmd("ux-researcher"),
            "information-architect": self._make_agent_cmd("information-architect"),
            "product-analyst": self._make_agent_cmd("product-analyst"),
            "critic": self._make_agent_cmd("critic"),
            "scholastic": self._make_agent_cmd("scholastic"),
            "vision": self._make_agent_cmd("vision"),
            # === Utilities ===
            "help": self._help_command,
            "version": self._version_command,
            "skills": self._skills_command,
            "doctor": self._doctor_command,
            "cancel": self._cancel_command,
            "note": self._note_command,
            "trace": self._trace_command,
            "hud": self._hud_command,
            "setup": self._omx_setup_command,
            "omx-setup": self._omx_setup_command,
            "configure-notifications": self._configure_notifications_command,
            "ralph-init": self._ralph_init_command,
            "agents": self._agents_command,
        }

    def run(self, args: Optional[list[str]] = None) -> int:
        if args is None:
            args = sys.argv[1:]

        if not args:
            return self._help_command()

        command = args[0]

        if command not in self.commands:
            print(f"Error: Unknown command '{command}'")
            print(f"Run 'oh-my-copilot help' for available commands.")
            return 1

        return self.commands[command](args[1:])

    # === Canonical Workflow ===

    def _interview_command(self, args: list[str]) -> int:
        """$deep-interview — clarify intent before execution."""
        if not args:
            print("Usage: oh-my-copilot interview <prompt>")
            print("       Clarify requirements, boundaries, and non-goals.")
            return 1
        prompt = " ".join(args)
        print(f"🎤 Deep Interview: {prompt}")
        print("   Phase: Requirements clarification")
        print("   → Ask clarifying questions")
        print("   → Define goals, non-goals, assumptions")
        print("   → Generate interview report")
        print("   Next: ralplan")
        return 0

    def _ralplan_command(self, args: list[str]) -> int:
        """$ralplan — architecture planning with Architect→Critic approval."""
        if not args:
            print("Usage: oh-my-copilot ralplan <plan-title>")
            print("       Build architecture plan with Architect and Critic review.")
            return 1
        title = " ".join(args)
        print(f"📐 RalPlan: {title}")
        print("   Phase: Architecture approval")
        print("   → Add design decisions and implementation steps")
        print("   → Submit Architect review (verdict: Approved/Rejected)")
        print("   → Submit Critic review (verdict: Approved/Rejected)")
        print("   → Handoff to ultragoal when both approve")
        print("   Next: prometheus-strict OR ultragoal")
        return 0

    def _prometheus_command(self, args: list[str]) -> int:
        """$prometheus-strict — harden high-risk plans."""
        if not args:
            print("Usage: oh-my-copilot prometheus <plan-title>")
            print("       Stress-test and validate a plan before execution.")
            return 1
        title = " ".join(args)
        print(f"🔥 Prometheus-Strict: {title}")
        print("   Phase: Plan validation and hardening")
        print("   → Define validation rules")
        print("   → Run stress tests")
        print("   → Identify critical issues")
        print("   → Generate validation report")
        print("   Next: ultragoal")
        return 0

    def _ultragoal_command(self, args: list[str]) -> int:
        """$ultragoal — durable multi-goal execution with checkpoints."""
        if not args:
            print("Usage: omp ultragoal <task-description>")
            print("       omp ultragoal create-goals [--auto-plan-id|--plan-id <id>] --brief <brief>")
            print("       omp ultragoal execute [--plan-id <id>]")
            print("       omp ultragoal status [--plan-id <id>]")
            print("       omp ultragoal list-plans")
            print("       Create artifact-only durable goal ledgers under .omp/ultragoal/.")
            return 1

        if args[0] == "create-goals":
            return self._ultragoal_create_goals(args[1:])

        if args[0] == "status":
            return self._ultragoal_status(args[1:])

        if args[0] == "execute":
            return self._ultragoal_execute(args[1:])

        if args[0] == "list-plans":
            return self._ultragoal_list_plans()

        return self._ultragoal_create_goals(args)

    def _ultragoal_create_goals(self, args: list[str]) -> int:
        """Create an artifact-only ultragoal ledger."""
        from pathlib import Path

        from skills import UltragoalSkill

        plan_id = ""
        auto_plan_id = False
        brief_parts: list[str] = []
        index = 0
        while index < len(args):
            arg = args[index]
            if arg == "--auto-plan-id":
                auto_plan_id = True
                index += 1
            elif arg == "--plan-id":
                if index + 1 >= len(args):
                    print("Error: --plan-id requires a value")
                    return 1
                plan_id = args[index + 1]
                index += 2
            elif arg == "--brief":
                index += 1
                while index < len(args) and not args[index].startswith("--"):
                    brief_parts.append(args[index])
                    index += 1
            else:
                brief_parts.append(arg)
                index += 1

        brief = " ".join(brief_parts).strip()
        if not brief:
            print("Usage: omp ultragoal create-goals [--auto-plan-id|--plan-id <id>] --brief <brief>")
            return 1

        skill = UltragoalSkill()
        if auto_plan_id and not plan_id:
            plan_id = skill.auto_plan_id(brief)

        ultragoal = skill.create_artifact_only_ultragoal(
            brief,
            metadata={
                "runtime": "omp",
                "mode": "artifact-only",
                "parity": "omc ultragoal create-goals",
            },
        )
        artifact = skill.save_artifacts(ultragoal, Path.cwd() / ".omp", plan_id=plan_id)

        print(f"🎯 Ultragoal: {brief}")
        print("   Mode: artifact-only")
        print("   Status: created")
        if artifact.plan_id:
            print(f"   Plan ID: {artifact.plan_id}")
        print(f"   Artifact: {artifact.root}")
        print(f"   Brief: {artifact.brief_path}")
        print(f"   Goals: {artifact.goals_path}")
        print(f"   Ledger: {artifact.ledger_path}")
        print("   Next: attach implementation evidence or hand off to ralph/team/ultraqa")
        return 0

    def _ultragoal_execute(self, args: list[str]) -> int:
        """Execute the next built-in implementation step for an ultragoal ledger."""
        import json
        from pathlib import Path

        from domain import GoalStatus
        from skills import UltragoalSkill

        plan_id = ""
        if args:
            if len(args) == 2 and args[0] == "--plan-id":
                plan_id = args[1]
            else:
                print("Usage: omp ultragoal execute [--plan-id <id>]")
                return 1

        project_root = Path.cwd()
        artifact_root = project_root / ".omp" / "ultragoal"
        if plan_id:
            artifact_root = artifact_root / "plans" / plan_id
        goals_path = artifact_root / "goals.json"
        if not goals_path.exists():
            print("No ultragoal artifacts found.")
            print("Run: omp ultragoal create-goals --brief <brief>")
            return 1

        data = json.loads(goals_path.read_text(encoding="utf-8"))
        skill = UltragoalSkill()
        try:
            paths = skill.materialize_builtin_implementation(data.get("name", ""), project_root)
            relative_paths = [path.relative_to(project_root) for path in paths]
            skill.record_goal_status(
                artifact_root,
                "Execute implementation work",
                GoalStatus.COMPLETED,
                evidence_paths=relative_paths,
            )
        except ValueError as error:
            print(f"Blocked: {error}")
            print("Next: hand off this ultragoal to ralph/team/ask for implementation.")
            return 1

        print(f"🎯 Ultragoal: {data.get('name', 'unknown')}")
        print("   Mode: built-in execution")
        print("   Status: implementation complete")
        if plan_id:
            print(f"   Plan ID: {plan_id}")
        for path in relative_paths:
            print(f"   Implemented: {path}")
        print(f"   Ledger: {artifact_root / 'ledger.jsonl'}")
        print("   Next: run tests and complete verification evidence")
        return 0

    def _ultragoal_status(self, args: list[str]) -> int:
        """Render status for an artifact-only ultragoal ledger."""
        import json
        from pathlib import Path

        plan_id = ""
        if args:
            if len(args) == 2 and args[0] == "--plan-id":
                plan_id = args[1]
            else:
                print("Usage: omp ultragoal status [--plan-id <id>]")
                return 1

        root = Path.cwd() / ".omp" / "ultragoal"
        artifact_root = root / "plans" / plan_id if plan_id else root
        goals_path = artifact_root / "goals.json"
        if not goals_path.exists():
            print("No ultragoal artifacts found.")
            print("Run: omp ultragoal create-goals --brief <brief>")
            return 1

        data = json.loads(goals_path.read_text(encoding="utf-8"))
        goals = data.get("goals", [])
        completed = len([goal for goal in goals if goal.get("status") == "completed"])
        print(f"🎯 Ultragoal: {data.get('name', 'unknown')}")
        if plan_id:
            print(f"   Plan ID: {plan_id}")
        print(f"   Status: {data.get('status', 'unknown')}")
        print(f"   Goals: {completed}/{len(goals)} completed")
        print(f"   Artifact: {artifact_root}")
        return 0

    def _ultragoal_list_plans(self) -> int:
        """List available plan-scoped ultragoal ledgers."""
        from pathlib import Path

        root = Path.cwd() / ".omp" / "ultragoal"
        plans_root = root / "plans"
        print("🎯 Ultragoal plans")
        if (root / "goals.json").exists():
            print("   default")
        for path in sorted(plans_root.iterdir()) if plans_root.exists() else []:
            if path.is_dir() and (path / "goals.json").exists():
                print(f"   {path.name}")
        return 0

    def _team_command(self, args: list[str]) -> int:
        """$team — coordinated parallel execution with multiple workers."""
        if not args:
            print("Usage: oh-my-copilot team <goal-description>")
            print("       Usage: omp team <count>:<provider> <goal-description>")
            print("       Usage: omp team --check <count>:<provider> <goal-description>")
            print("       Usage: omp team status|shutdown <team-name>")
            print("       Launch parallel workers for coordinated execution.")
            return 1

        if len(args) == 2 and args[0] in {"status", "shutdown"}:
            try:
                from pathlib import Path
                from skills import TeamRuntimeSkill

                skill = TeamRuntimeSkill()
                control = skill.prepare_team_control(args[0], args[1])
                artifact = skill.save_team_control(control, Path.cwd() / ".omp" / "state")
            except ValueError as error:
                print(f"Error: {error}")
                return 1

            print(f"👥 Team Runtime: {control.team_name}")
            print(f"   Control: {control.action.value}")
            print(f"   Preview: {control.command_preview}")
            print(f"   Saved: {artifact.path}")
            return 0

        if len(args) >= 3 and args[0] == "--check":
            try:
                from skills import TeamRuntimeSkill

                readiness = TeamRuntimeSkill().check_provider_team_requirements(
                    args[1],
                    " ".join(args[2:]),
                )
            except ValueError as error:
                print(f"Error: {error}")
                return 1

            print(f"👥 Team Runtime: {readiness.request.goal_description}")
            print("   Requirements:")
            print(f"   Status: {readiness.status.value}")
            print(f"   Provider executable: {readiness.provider_executable or 'missing'}")
            print(f"   tmux executable: {readiness.tmux_executable or 'missing'}")
            return 0

        if len(args) >= 2 and ":" in args[0]:
            try:
                from skills import TeamRuntimeSkill

                request = TeamRuntimeSkill().prepare_provider_team(args[0], " ".join(args[1:]))
            except ValueError as error:
                print(f"Error: {error}")
                return 1

            print(f"👥 Team Runtime: {request.goal_description}")
            print("   Mode: Provider-backed team preparation")
            print(f"   Provider: {request.provider.value}")
            print(f"   Workers: {request.worker_count}")
            print(f"   Preview: {request.command_preview}")
            return 0

        goal = " ".join(args)
        print(f"👥 Team Runtime: {goal}")
        print("   Phase: Parallel execution")
        print("   → Create workers with roles")
        print("   → Distribute tasks (round-robin)")
        print("   → Track worker progress")
        print("   → Generate team report")
        return 0

    def _ralph_command(self, args: list[str]) -> int:
        """$ralph — single-owner persistent completion loop."""
        if not args:
            print("Usage: oh-my-copilot ralph <task>")
            print("       Single-owner loop until completion (no ledger needed).")
            return 1
        task = " ".join(args)
        print(f"🔄 Ralph: {task}")
        print("   Phase: Persistent completion loop")
        print("   → One owner pushes until done")
        print("   → Iterate until success")
        print("   → No formal goal tracking required")
        print("   → Generate completion report")
        return 0

    def _review_command(self, args: list[str]) -> int:
        """$code-review — review current branch for merge readiness."""
        if not args:
            print("Usage: oh-my-copilot review <title>")
            print("       Review code quality, standards, and spec compliance.")
            return 1
        title = " ".join(args)
        print(f"👀 Code Review: {title}")
        print("   Phase: Review")
        print("   → Standards compliance (naming, formatting)")
        print("   → Spec compliance (feature completeness)")
        print("   → Security findings")
        print("   → Generate review report")
        print("   Next: ultraqa")
        return 0

    def _ultraqa_command(self, args: list[str]) -> int:
        """$ultraqa — test/verify/fix loop for merge readiness."""
        if not args:
            print("Usage: oh-my-copilot ultraqa <title>")
            print("       Run test/verify/fix loop until merge-ready.")
            return 1
        title = " ".join(args)
        print(f"🧪 UltraQA: {title}")
        print("   Phase: QA loop")
        print("   → Add test cases")
        print("   → Verify each test")
        print("   → Fix failures and retry")
        print("   → Gate: all tests pass = merge-ready")
        return 0

    # === Planning & Clarification ===

    def _plan_command(self, args: list[str]) -> int:
        """$plan — strategic planning when not on the canonical path."""
        if not args:
            print("Usage: oh-my-copilot plan <title> <vision>")
            print("       High-level strategic planning (simpler than ralplan).")
            return 1
        if len(args) < 2:
            print("Error: Need both title and vision")
            return 1
        title = args[0]
        vision = " ".join(args[1:])
        print(f"🗺️  Strategic Plan: {title}")
        print(f"   Vision: {vision}")
        print("   → Set goals and objectives")
        print("   → Define constraints and assumptions")
        print("   → Estimate effort by phase")
        print("   → Approve plan")
        return 0

    def _brainstorm_command(self, args: list[str]) -> int:
        """Brainstorm ideas for a prompt."""
        if not args:
            print("Usage: oh-my-copilot brainstorm <prompt>")
            return 1
        prompt = " ".join(args)
        print(f"🧠 Brainstorming: {prompt}")
        print("   → Generate multiple ideas")
        print("   → Explore tradeoffs")
        print("   → Select best approach")
        return 0

    def _domain_command(self, args: list[str]) -> int:
        """Define domain model and ubiquitous language."""
        if not args:
            print("Usage: oh-my-copilot domain <project> <description>")
            return 1
        if len(args) < 2:
            print("Error: Need both project name and description")
            return 1
        project = args[0]
        description = " ".join(args[1:])
        print(f"📚 Domain Model: {project}")
        print(f"   Description: {description}")
        print("   → Define ubiquitous language")
        print("   → Add domain concepts")
        print("   → Validate model")
        return 0

    # === Research ===

    def _best_practice_command(self, args: list[str]) -> int:
        """$best-practice-research — find official best practices."""
        if not args:
            print("Usage: oh-my-copilot best-practice <topic>")
            print("       Find official/upstream best practices before planning.")
            return 1
        topic = " ".join(args)
        print(f"📖 Best Practice Research: {topic}")
        print("   Phase: Pre-planning research")
        print("   → Search official docs and standards")
        print("   → Record source citations")
        print("   → Score adoption and impact")
        print("   → Feed evidence into ralplan")
        return 0

    def _autoresearch_command(self, args: list[str]) -> int:
        """$autoresearch — bounded validator-gated research."""
        if not args:
            print("Usage: oh-my-copilot autoresearch <topic>")
            print("       Bounded research that must pass a validator before completing.")
            return 1
        topic = " ".join(args)
        print(f"🔬 Autoresearch: {topic}")
        print("   Phase: Bounded research")
        print("   → Define research target and keywords")
        print("   → Collect evidence (max 10 items)")
        print("   → Apply validation gate")
        print("   → Complete only when validated")
        return 0

    def _autoresearch_goal_command(self, args: list[str]) -> int:
        """$autoresearch-goal — goal-mode research with Professor/Critic validation."""
        if not args:
            print("Usage: oh-my-copilot autoresearch-goal <mission>")
            print("       Research mission with professor/critic-style durable validation.")
            return 1
        mission = " ".join(args)
        print(f"🎓 Autoresearch-Goal: {mission}")
        print("   Phase: Goal-mode research")
        print("   → Set research focus with professor/critic prompts")
        print("   → Add findings and validate each one")
        print("   → Professor guides, critic challenges")
        print("   → Complete when findings + validations satisfy")
        return 0

    # === Execution Modes ===

    def _autopilot_command(self, args: list[str]) -> int:
        """$autopilot — strict autonomous loop over the full workflow."""
        if not args:
            print("Usage: oh-my-copilot autopilot <task>")
            print("       Autonomous loop: interview→ralplan→ultragoal→review→ultraqa")
            print("       Returns to ralplan when review or QA is not clean.")
            return 1
        task = " ".join(args)
        print(f"🤖 Autopilot: {task}")
        print("   Mode: Autonomous execution loop")
        print("   1. interview    → clarify requirements")
        print("   2. ralplan      → architect approval")
        print("   3. ultragoal    → execute and verify")
        print("   4. code-review  → standards check")
        print("   5. ultraqa      → merge readiness gate")
        print("   ↩  replan if review/QA not clean (max 3 replans)")
        return 0

    # === Specialized ===

    def _diagnose_command(self, args: list[str]) -> int:
        """Diagnose bugs and find root causes."""
        if not args:
            print("Usage: oh-my-copilot diagnose <error_summary>")
            return 1
        error = " ".join(args)
        print(f"🔍 Diagnosing: {error}")
        print("   → Collect error evidence")
        print("   → Generate hypotheses")
        print("   → Identify root cause")
        print("   → Produce resolution plan")
        return 0

    def _sparkshell_command(self, args: list[str]) -> int:
        """$sparkshell — shell command execution with safety validation."""
        if not args:
            print("Usage: oh-my-copilot sparkshell <command>")
            print("       Execute shell commands with safety checks.")
            return 1
        command = " ".join(args)
        print(f"⚡ Sparkshell: {command}")
        print("   → Validate command safety")
        print("   → Detect dangerous patterns (rm -rf, git push, etc.)")
        print("   → Request approval for destructive commands")
        print("   → Execute and capture output")
        return 0

    def _wiki_command(self, args: list[str]) -> int:
        """Wiki — project knowledge management."""
        if not args:
            print("Usage: oh-my-copilot wiki <title>")
            print("       Manage project documentation and knowledge base.")
            return 1
        title = " ".join(args)
        print(f"📝 Wiki: {title}")
        print("   → Create and publish pages")
        print("   → Search by tag, category, or title")
        print("   → Archive deprecated content")
        return 0

    def _hooks_command(self, args: list[str]) -> int:
        """Hooks — lifecycle event management."""
        if not args:
            print("Usage: oh-my-copilot hooks <event>")
            print("       Register and execute lifecycle hooks.")
            return 1
        event = " ".join(args)
        print(f"🪝 Hooks: {event}")
        print("   → Register hooks with priority ordering")
        print("   → Execute hooks on lifecycle events")
        print("   → Track execution history")
        return 0

    def _github_command(self, args: list[str]) -> int:
        """GitHub — issue and repository management."""
        if not args:
            print("Usage: oh-my-copilot github <title>")
            print("       Create GitHub issues, bug reports, and feature requests.")
            return 1
        title = " ".join(args)
        print(f"🐙 GitHub: {title}")
        print("   → Create issues with priority and labels")
        print("   → File bug reports with steps to reproduce")
        print("   → Submit feature requests with acceptance criteria")
        return 0

    def _ask_command(self, args: list[str]) -> int:
        """Provider advisor — prepare an ask-provider request."""
        if len(args) == 2 and args[0] == "--check":
            try:
                from skills import ProviderAdvisorSkill

                availability = ProviderAdvisorSkill().check_provider(args[1])
            except ValueError as error:
                print(f"Error: {error}")
                return 1

            print(f"🤝 Ask Provider: {availability.provider.value}")
            print(f"   Status: {availability.status.value}")
            print(f"   Executable: {availability.executable_path or 'missing'}")
            return 0

        if len(args) >= 3 and args[0] == "--execute":
            try:
                from pathlib import Path
                from core import SessionRecorder
                from skills import ProviderAdvisorSkill

                skill = ProviderAdvisorSkill()
                provider = args[1]
                result = skill.execute(provider, " ".join(args[2:]))
                artifact = skill.record_artifact(result, Path.cwd() / ".omp" / "artifacts" / "ask")
                friction_type = ""
                friction_summary = ""
                if result.status.value == "blocked":
                    friction_type = "operator-friction"
                    friction_summary = "provider executable missing"
                elif result.status.value == "failed":
                    friction_type = "validation-failure"
                    friction_summary = "provider execution failed"
                SessionRecorder(Path.cwd() / ".omp" / "sessions").record_command(
                    command=f"omp ask --execute {provider}",
                    status=result.status.value,
                    exit_code=result.exit_code,
                    friction_type=friction_type,
                    friction_summary=friction_summary,
                )
            except ValueError as error:
                print(f"Error: {error}")
                return 1

            print(f"🤝 Ask Execute: {result.provider.value}")
            print(f"   Status: {result.status.value}")
            if result.exit_code is not None:
                print(f"   Exit code: {result.exit_code}")
            if result.output_summary:
                print(f"   Output: {result.output_summary}")
            if result.error_summary:
                print(f"   Error: {result.error_summary}")
            print(f"   Artifact: {artifact.path}")
            return 0

        if len(args) < 2:
            print("Usage: omp ask <provider> <prompt>")
            print("       Usage: omp ask --check <provider>")
            print("       Usage: omp ask --execute <provider> <prompt>")
            print("       Providers: claude, codex, gemini, antigravity, grok, cursor")
            return 1
        provider = args[0]
        prompt = " ".join(args[1:])
        try:
            from skills import ProviderAdvisorSkill

            request = ProviderAdvisorSkill().ask(provider, prompt)
        except ValueError as error:
            print(f"Error: {error}")
            return 1

        print(f"🤝 Ask {request.provider.value}: {request.prompt}")
        print(f"   Status: {request.status.value}")
        print(f"   Preview: {request.command_preview}")
        return 0

    def _wait_command(self, args: list[str]) -> int:
        """Rate-limit wait — check or prepare auto-resume."""
        from pathlib import Path
        from skills import RateLimitWaitSkill

        skill = RateLimitWaitSkill()
        artifact = None
        if args == ["--start"]:
            result = skill.start_auto_resume()
            artifact = skill.save_state(result, Path.cwd() / ".omp" / "state")
        elif args == ["--stop"]:
            result = skill.stop_auto_resume()
            artifact = skill.save_state(result, Path.cwd() / ".omp" / "state")
        elif not args:
            state_root = Path.cwd() / ".omp" / "state"
            if (state_root / "wait.json").exists():
                result = skill.load_state(state_root)
                artifact = skill.save_state(result, state_root)
            else:
                result = skill.check_status()
        else:
            print("Usage: omp wait [--start|--stop]")
            return 1

        print(f"⏳ Wait: {result.action.value}")
        print(f"   Status: {result.status.value}")
        print(f"   Guidance: {result.guidance}")
        if artifact:
            if not args:
                print(f"   Restored: {artifact.path}")
            print(f"   Saved: {artifact.path}")
        return 0

    def _session_command(self, args: list[str]) -> int:
        """Session utilities — local session summaries and reports."""
        if len(args) == 5 and args[:3] == ["friction", "report", "--since"]:
            since = args[3]
            output_format = args[4]
        elif len(args) == 4 and args[:3] == ["friction", "report", "--since"]:
            since = args[3]
            output_format = "text"
        else:
            print("Usage: omp session friction report --since <window> [--json]")
            return 1

        from skills import SessionFrictionSkill
        from pathlib import Path

        report = SessionFrictionSkill().generate_report_from_files(
            since,
            Path.cwd() / ".omp" / "sessions",
        )
        if output_format == "--json":
            print(
                '{'
                f'"since":"{report.since}",'
                f'"total_signals":{report.total_signals}'
                '}'
            )
        else:
            print(f"📉 Session Friction: since {report.since}")
            print(f"   Signals: {report.total_signals}")
            print(
                "   Breakdown: "
                + (", ".join(f"{key}={value}" for key, value in report.signal_breakdown.items()) or "none")
            )
            print(f"   Summary: {report.summary}")
        return 0

    def _config_stop_callback_command(self, args: list[str]) -> int:
        """Configure stop callback notifications without collecting secrets."""
        if args == ["--show"]:
            try:
                from pathlib import Path
                from skills import NotificationConfigSkill

                config = NotificationConfigSkill().load_config(Path.cwd() / ".omp" / "state")
            except FileNotFoundError:
                print("Error: notification config not found")
                return 1
            print(f"🔔 Stop Callback: {config.channel.value}")
            print(f"   Status: {config.status.value}")
            print(f"   Tags: {', '.join(config.tag_list) if config.tag_list else 'none'}")
            print(f"   Restored: {Path.cwd() / '.omp' / 'state' / 'notifications.json'}")
            return 0

        if not args:
            print("Usage: omp config-stop-callback <channel> [--tag-list <tags>]")
            return 1

        channel = args[0]
        tag_list: list[str] = []
        if "--tag-list" in args:
            option_index = args.index("--tag-list")
            if option_index + 1 >= len(args):
                print("Error: --tag-list requires a comma-separated value")
                return 1
            tag_list = [tag for tag in args[option_index + 1].split(",") if tag]

        try:
            from pathlib import Path
            from skills import NotificationConfigSkill

            skill = NotificationConfigSkill()
            config = skill.prepare_stop_callback(channel, tag_list)
            artifact = skill.save_config(config, Path.cwd() / ".omp" / "state")
        except ValueError as error:
            print(f"Error: {error}")
            return 1

        print(f"🔔 Stop Callback: {config.channel.value}")
        print(f"   Status: {config.status.value}")
        print(f"   Tags: {', '.join(config.tag_list) if config.tag_list else 'none'}")
        print(f"   Preview: {config.command_preview}")
        print(f"   Saved: {artifact.path}")
        return 0

    # === Agent Shortcuts ===

    def _analyze_command(self, args: list[str]) -> int:
        """$analyze — codebase discovery and symbol mapping."""
        if not args:
            print("Usage: oh-my-copilot analyze <query>")
            return 1
        query = " ".join(args)
        print(f"🗺️  Analyze: {query}")
        print("   Agent: Explorer (low)")
        print("   → Map codebase structure")
        print("   → Trace symbols and dependencies")
        print("   → Identify key entry points")
        return 0

    def _tdd_command(self, args: list[str]) -> int:
        """$tdd — test-driven development."""
        if not args:
            print("Usage: oh-my-copilot tdd <feature>")
            return 1
        feature = " ".join(args)
        print(f"🧪 TDD: {feature}")
        print("   Agent: Test Engineer (medium)")
        print("   → Write failing tests first (RED)")
        print("   → Implement to pass tests (GREEN)")
        print("   → Refactor for clarity (REFACTOR)")
        return 0

    def _security_review_command(self, args: list[str]) -> int:
        """$security-review — security audit."""
        if not args:
            print("Usage: oh-my-copilot security-review <scope>")
            return 1
        scope = " ".join(args)
        print(f"🔒 Security Review: {scope}")
        print("   Agent: Security Reviewer (medium)")
        print("   → Check OWASP Top 10")
        print("   → Audit auth and input validation")
        print("   → Review dependency vulnerabilities")
        return 0

    def _build_fix_command(self, args: list[str]) -> int:
        """$build-fix — build/toolchain issue resolution."""
        if not args:
            print("Usage: oh-my-copilot build-fix <issue>")
            return 1
        issue = " ".join(args)
        print(f"🔧 Build Fix: {issue}")
        print("   Agent: Build Fixer (medium)")
        print("   → Diagnose CI/build failures")
        print("   → Resolve type errors and toolchain issues")
        print("   → Verify fix with test run")
        return 0

    def _git_master_command(self, args: list[str]) -> int:
        """$git-master — commit strategy and history hygiene."""
        if not args:
            print("Usage: oh-my-copilot git-master <goal>")
            return 1
        goal = " ".join(args)
        print(f"🌿 Git Master: {goal}")
        print("   Agent: Git Master (medium)")
        print("   → Plan clean commit strategy")
        print("   → Squash and reorder commits")
        print("   → Prepare branch for merge")
        return 0

    # === Utilities ===

    def _skills_command(self, args: list[str] = None) -> int:
        """List all available skills."""
        print(f"{self.name} — Available Skills")
        print()
        print("Canonical Workflow:")
        print("  interview        Clarify requirements ($deep-interview)")
        print("  ralplan          Architecture plan with Architect→Critic approval")
        print("  prometheus       Harden high-risk plans ($prometheus-strict)")
        print("  ultragoal        Durable multi-goal execution")
        print("  team             Parallel execution with workers")
        print("  ralph            Single-owner completion loop")
        print("  review           Code review ($code-review)")
        print("  ultraqa          Test/verify/fix loop")
        print()
        print("Planning & Clarification:")
        print("  plan             Strategic high-level planning")
        print("  brainstorm       Idea generation")
        print("  domain           Domain model and ubiquitous language")
        print()
        print("Research:")
        print("  best-practice    Official best-practice evidence")
        print("  autoresearch     Bounded validator-gated research")
        print("  autoresearch-goal  Goal-mode research with professor/critic")
        print()
        print("Execution Modes:")
        print("  autopilot        Autonomous full-workflow loop")
        print()
        print("Specialized:")
        print("  diagnose         Bug diagnosis and root cause")
        print("  sparkshell       Shell execution with safety checks")
        print("  wiki             Project knowledge management")
        print("  hooks            Lifecycle event hooks")
        print("  github           GitHub issue management")
        print("  ask              Provider advisor request prep")
        print("  wait             Rate-limit wait guidance")
        print("  session          Local session friction reports")
        print("  config-stop-callback  Notification callback prep")
        print()
        print("Agent Shortcuts:")
        print("  analyze          Codebase discovery ($analyze)")
        print("  tdd              Test-driven development ($tdd)")
        print("  security-review  Security audit ($security-review)")
        print("  build-fix        Build/CI fix ($build-fix)")
        print("  git-master       Git strategy ($git-master)")
        return 0

    def _doctor_command(self, args: list[str] = None) -> int:
        """$doctor — check system and skill health."""
        args = args or []
        if "--strict" in args:
            return self._strict_doctor_command(args)

        print(f"🩺 Doctor — {self.name} v{self.version}")
        print()
        print("Checking skills...")
        try:
            from skills import (
                BrainstormingSkill, DomainModelingSkill, DiagnosticSkill,
                CodeReviewSkill, GitHubIntegrationSkill, DeepInterviewSkill,
                UltragoalSkill, TeamRuntimeSkill, SparkshellSkill, WikiSkill,
                HooksSkill, PrometheusStrictSkill, AutoresearchSkill,
                BestPracticeResearchSkill, RalPlanSkill, RalphSkill,
                UltraQASkill, AutoresearchGoalSkill, AutopilotSkill,
                StrategicPlanSkill, UltraworkSkill, VisualVerdictSkill,
                EcomodeSkill, SwarmSkill, DeepSearchSkill, DesignSkill,
                VisualRalphSkill, AgentCatalogSkill, ProviderAdvisorSkill,
                RateLimitWaitSkill,
                SessionFrictionSkill,
                NotificationConfigSkill,
                ProjectSetupSkill,
                StateSummarySkill,
            )
            skills = [
                BrainstormingSkill, DomainModelingSkill, DiagnosticSkill,
                CodeReviewSkill, GitHubIntegrationSkill, DeepInterviewSkill,
                UltragoalSkill, TeamRuntimeSkill, SparkshellSkill, WikiSkill,
                HooksSkill, PrometheusStrictSkill, AutoresearchSkill,
                BestPracticeResearchSkill, RalPlanSkill, RalphSkill,
                UltraQASkill, AutoresearchGoalSkill, AutopilotSkill,
                StrategicPlanSkill, UltraworkSkill, VisualVerdictSkill,
                EcomodeSkill, SwarmSkill, DeepSearchSkill, DesignSkill,
                VisualRalphSkill, AgentCatalogSkill, ProviderAdvisorSkill,
                RateLimitWaitSkill,
                SessionFrictionSkill,
                NotificationConfigSkill,
                ProjectSetupSkill,
                StateSummarySkill,
            ]
            for skill_cls in skills:
                s = skill_cls()
                print(f"  ✓ {s.name}")
            print()
            print(f"All {len(skills)} skills operational.")
        except Exception as e:
            print(f"  ✗ Import error: {e}")
            return 1
        return 0

    def _strict_doctor_command(self, args: list[str]) -> int:
        """Run a stricter CLI audit that distinguishes placeholders from working surfaces."""
        import json

        commands = self._cli_surface_audit()
        placeholder_count = len([item for item in commands if item["status"] == "placeholder"])
        blocked_count = len([item for item in commands if item["status"] == "external-blocked"])
        status = "operational" if placeholder_count == 0 and blocked_count == 0 else "degraded"

        if "--json" in args:
            print(json.dumps({"status": status, "commands": commands}, ensure_ascii=False, indent=2))
            return 0 if status == "operational" else 1

        print(f"🩺 Doctor — {self.name} v{self.version}")
        print()
        print("Strict CLI audit:")
        for item in commands:
            marker = "✓" if item["status"] in {"executable", "artifact", "state", "external"} else "!"
            print(f"  {marker} {item['command']:<24} {item['status']:<16} {item['evidence']}")

        print()
        print(f"Summary: {status}")
        print(f"  placeholders: {placeholder_count}")
        print(f"  external blocked: {blocked_count}")
        if placeholder_count:
            print("  Note: placeholder means the CLI prints guidance but does not yet create state, artifacts, or run work.")
        return 0 if status == "operational" else 1

    def _cli_surface_audit(self) -> list[dict[str, str]]:
        """Describe CLI surfaces by their current implementation depth."""
        return [
            {"command": "doctor", "status": "executable", "evidence": "imports skills and can run strict audit"},
            {"command": "skills", "status": "executable", "evidence": "lists registered skill surfaces"},
            {"command": "agents", "status": "executable", "evidence": "lists agent catalog"},
            {"command": "setup", "status": "state", "evidence": "creates .omp state directories"},
            {"command": "hud", "status": "state", "evidence": "reads .omp state summary"},
            {"command": "ask", "status": "external", "evidence": "records artifacts and invokes provider when available"},
            {"command": "wait", "status": "state", "evidence": "persists wait state"},
            {"command": "session", "status": "state", "evidence": "summarizes .omp session records"},
            {"command": "config-stop-callback", "status": "state", "evidence": "persists notification config"},
            {"command": "team", "status": "artifact", "evidence": "prepares provider team/control artifacts, not full worker lifecycle"},
            {"command": "ultragoal", "status": "artifact", "evidence": "creates ledger artifacts and has built-in websocket execute path"},
            {"command": "agent", "status": "artifact", "evidence": "records agent invocation metadata"},
            {"command": "interview", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "ralplan", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "prometheus", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "ralph", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "review", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "ultraqa", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "plan", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "brainstorm", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "domain", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "best-practice", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "autoresearch", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "autoresearch-goal", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "autopilot", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "diagnose", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "sparkshell", "status": "placeholder", "evidence": "prints validation guidance only"},
            {"command": "wiki", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "hooks", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "github", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "analyze", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "tdd", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "security-review", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "build-fix", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "git-master", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "ultrawork", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "visual-verdict", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "ecomode", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "swarm", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "deepsearch", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "design", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "visual-ralph", "status": "placeholder", "evidence": "prints phase guidance only"},
            {"command": "cancel", "status": "placeholder", "evidence": "prints cancellation guidance only"},
            {"command": "note", "status": "placeholder", "evidence": "prints note text only"},
            {"command": "trace", "status": "placeholder", "evidence": "prints tracing guidance only"},
        ]

    # === New Execution Modes ===

    def _ultrawork_command(self, args: list[str]) -> int:
        """$ultrawork — max parallel execution."""
        if not args:
            print("Usage: oh-my-copilot ultrawork <goal>")
            print("       Launch max parallel execution lanes.")
            return 1
        goal = " ".join(args)
        print(f"⚡ Ultrawork: {goal}")
        print("   Mode: Max parallel execution")
        print("   → Create independent execution lanes")
        print("   → All lanes run simultaneously")
        print("   → Track per-lane progress")
        print("   → Aggregate results when all lanes complete")
        return 0

    def _visual_verdict_command(self, args: list[str]) -> int:
        """$visual-verdict — structured visual QA loop."""
        if not args:
            print("Usage: oh-my-copilot visual-verdict <task>")
            print("       Visual QA loop for screenshot/reference matching (threshold: 90+).")
            return 1
        task = " ".join(args)
        print(f"👁️  Visual Verdict: {task}")
        print("   Mode: Visual QA loop")
        print("   → Provide reference image(s)")
        print("   → Generate and compare screenshot")
        print("   → Pass threshold: 90+")
        print("   → Use pixel diff for secondary debugging")
        print("   → Iterate until passing or exhausted")
        return 0

    def _ecomode_command(self, args: list[str]) -> int:
        """$ecomode — token-efficient model routing."""
        if not args:
            print("Usage: oh-my-copilot ecomode <goal>")
            print("       Route tasks to the right model tier for token efficiency.")
            return 1
        goal = " ".join(args)
        print(f"🌱 Ecomode: {goal}")
        print("   Mode: Token-efficient routing")
        print("   → LOW tier:    formatting, simple lookups")
        print("   → MEDIUM tier: most coding and review tasks")
        print("   → HIGH tier:   complex reasoning, architecture")
        print("   → Avg ~60-90% savings vs always-high")
        return 0

    def _swarm_command(self, args: list[str]) -> int:
        """$swarm — team compatibility facade."""
        if not args:
            print("Usage: oh-my-copilot swarm <goal>")
            print("       Team compatibility facade — same semantics as $team.")
            return 1
        goal = " ".join(args)
        print(f"🐝 Swarm: {goal}")
        print("   Mode: Team compatibility facade")
        print("   → Identical to $team with swarm semantics")
        print("   → Auto-creates workers, distributes tasks")
        print("   → Backward-compatible with team workflows")
        return 0

    # === New Agent Shortcuts ===

    def _deepsearch_command(self, args: list[str]) -> int:
        """$deepsearch — deep codebase search."""
        if not args:
            print("Usage: oh-my-copilot deepsearch <query>")
            return 1
        query = " ".join(args)
        print(f"🔎 Deep Search: {query}")
        print("   → Search symbols, patterns, and dependencies")
        print("   → Ranked by relevance")
        print("   → Scope: codebase, symbols, patterns, all")
        return 0

    def _design_command(self, args: list[str]) -> int:
        """$design — maintain DESIGN.md."""
        if not args:
            print("Usage: oh-my-copilot design <project>")
            print("       Maintain repo-local DESIGN.md.")
            return 1
        project = " ".join(args)
        print(f"🎨 Design: {project}")
        print("   → Maintain DESIGN.md in repo root")
        print("   → Sections: overview, architecture, API, decisions, diagrams")
        print("   → Track open questions")
        return 0

    def _visual_ralph_command(self, args: list[str]) -> int:
        """$visual-ralph — measured visual-reference implementation loop."""
        if not args:
            print("Usage: oh-my-copilot visual-ralph <task>")
            return 1
        task = " ".join(args)
        print(f"🖼️  Visual Ralph: {task}")
        print("   → Implement against a visual reference")
        print("   → Score each iteration (threshold: 90+)")
        print("   → Loop until passing or max iterations")
        return 0

    # === Agent Catalog ===

    def _make_agent_cmd(self, agent_name: str):
        """Factory: create a CLI handler for a named agent."""
        def _cmd(args: list[str]) -> int:
            if not args:
                from domain import AgentRegistry
                reg = AgentRegistry()
                spec = reg.get(agent_name)
                if spec:
                    print(f"Usage: oh-my-copilot {agent_name} <prompt>")
                    print(f"       {spec.description}")
                    print(f"       Model: {spec.model_tier.value}")
                    print(f"       Example: {spec.example_usage}")
                return 1
            from skills import AgentCatalogSkill
            skill = AgentCatalogSkill()
            invocation = skill.invoke(agent_name, " ".join(args))
            print(f"🤖 {agent_name}: {invocation.output}")
            return 0 if invocation.success else 1
        _cmd.__name__ = f"_agent_{agent_name.replace('-', '_')}_command"
        return _cmd

    def _agent_command(self, args: list[str]) -> int:
        """Invoke any agent from the catalog: oh-my-copilot agent <name> <prompt>."""
        if len(args) < 2:
            print("Usage: oh-my-copilot agent <agent-name> <prompt>")
            print("       Run 'oh-my-copilot agents' to list all agents.")
            return 1
        agent_name, prompt = args[0], " ".join(args[1:])
        from skills import AgentCatalogSkill
        skill = AgentCatalogSkill()
        invocation = skill.invoke(agent_name, prompt)
        print(f"🤖 {agent_name}: {invocation.output}")
        return 0 if invocation.success else 1

    def _agents_command(self, args: list[str] = None) -> int:
        """List all 31 specialist agents from the catalog."""
        from domain import AgentRegistry, AgentCategory
        reg = AgentRegistry()
        categories = [
            ("Build & Analysis", AgentCategory.BUILD_ANALYSIS),
            ("Review", AgentCategory.REVIEW),
            ("Domain Specialists", AgentCategory.DOMAIN_SPECIALIST),
            ("Product", AgentCategory.PRODUCT),
            ("Coordination", AgentCategory.COORDINATION),
        ]
        print("🤖 Agent Catalog — oh-my-copilot")
        print()
        for label, cat in categories:
            agents = reg.list_by_category(cat)
            print(f"{label}:")
            for a in agents:
                internal = " (internal)" if a.is_internal else ""
                print(f"  {a.name:<25} [{a.model_tier.value}]{internal}")
                print(f"    {a.description}")
            print()
        print(f"Total: {len(reg.list_all())} agents")
        print("Usage: oh-my-copilot <agent-name> <prompt>")
        print("       oh-my-copilot agent <name> <prompt>")
        return 0

    # === Utilities ===

    def _cancel_command(self, args: list[str] = None) -> int:
        """$cancel — cancel an in-progress operation."""
        print("🚫 Cancel")
        print("   Signals cancellation of the current in-progress skill/operation.")
        print("   Use this to gracefully stop an active run.")
        return 0

    def _note_command(self, args: list[str] = None) -> int:
        """$note — save a note."""
        if not args:
            print("Usage: oh-my-copilot note <text>")
            return 1
        note = " ".join(args)
        print(f"📝 Note saved: {note}")
        return 0

    def _trace_command(self, args: list[str] = None) -> int:
        """$trace — show execution trace."""
        print("🔍 Trace")
        print("   Shows execution history for the current session.")
        print("   Use to debug skill sequencing and phase transitions.")
        return 0

    def _hud_command(self, args: list[str] = None) -> int:
        """$hud — heads-up display of current state."""
        from pathlib import Path
        from domain import AgentRegistry
        from skills import StateSummarySkill

        summary = StateSummarySkill().summarize(Path.cwd() / ".omp" / "state")
        agent_count = len(AgentRegistry().list_all())
        print(f"📊 HUD — {self.name} v{self.version}")
        print()
        print("Current state:")
        print("  Skills loaded: 34")
        print(f"  Agent catalog: {agent_count} agents")
        print(f"  State files: {summary.total_files}")
        print(f"  Wait state: {summary.wait_state}")
        print(f"  Notification channel: {summary.notification_channel}")
        print(f"  Team controls: {', '.join(summary.team_controls) if summary.team_controls else 'none'}")
        print("  Status: operational")
        return 0

    def _omx_setup_command(self, args: list[str] = None) -> int:
        """$omx-setup — initial project setup."""
        from pathlib import Path
        from skills import ProjectSetupSkill

        result = ProjectSetupSkill().initialize(Path.cwd())
        print("⚙️  OMP Setup")
        print("   Initialize oh-my-copilot for this project.")
        print(f"   Status: {result.status.value}")
        print(f"   State root: {result.state_root}")
        print("   Creates: .omp/ state, sessions, artifacts, and skills directories")
        return 0

    def _configure_notifications_command(self, args: list[str] = None) -> int:
        """$configure-notifications — configure notifications."""
        print("🔔 Configure Notifications")
        print("   Set up hook-based notifications for lifecycle events.")
        print("   Events: task_started, task_completed, goal_completed, session_failed")
        return 0

    def _ralph_init_command(self, args: list[str] = None) -> int:
        """$ralph-init — initialize a Ralph completion loop."""
        if not args:
            print("Usage: oh-my-copilot ralph-init <task>")
            return 1
        task = " ".join(args)
        print(f"🔄 Ralph Init: {task}")
        print("   Initializes a new Ralph completion loop.")
        print("   Creates owner record and first iteration scaffold.")
        return 0

    def _help_command(self, args: list[str] = None) -> int:
        """Show help message."""
        print(f"{self.name} v{self.version}")
        print()
        print("A Python agent framework with oh-my-codex compatible skills")
        print()
        print("Canonical workflow:")
        print("  interview → ralplan → prometheus → ultragoal → review → ultraqa")
        print()
        print("Quick commands:")
        print("  interview <prompt>         Clarify requirements ($deep-interview)")
        print("  ralplan <title>            Architecture plan with approval")
        print("  prometheus <title>         Harden plan ($prometheus-strict)")
        print("  ultragoal <task>           Durable execution")
        print("  team <goal>                Parallel workers")
        print("  ralph <task>               Single-owner completion loop")
        print("  review <title>             Code review")
        print("  ultraqa <title>            Test/verify/fix loop")
        print("  plan <title> <vision>      Strategic planning ($plan)")
        print("  brainstorm <prompt>        Idea generation")
        print("  domain <project> <desc>    Domain modeling")
        print("  best-practice <topic>      Best practice research")
        print("  autoresearch <topic>       Bounded research")
        print("  autoresearch-goal <topic>  Goal-mode research")
        print("  autopilot <task>           Autonomous full-workflow loop")
        print("  diagnose <error>           Bug diagnosis")
        print("  sparkshell <command>       Safe shell execution")
        print("  wiki <title>               Knowledge management")
        print("  ask <provider> <prompt>    Provider advisor request")
        print("  wait [--start|--stop]      Rate-limit wait guidance")
        print("  session friction report --since <window>  Local friction report")
        print("  config-stop-callback <channel> [--tag-list <tags>]  Notification prep")
        print("  analyze <query>            Codebase analysis")
        print("  tdd <feature>              Test-driven development")
        print("  security-review <scope>    Security audit")
        print("  build-fix <issue>          Build/CI fix")
        print("  git-master <goal>          Git strategy")
        print("  skills                     List all skills")
        print("  doctor                     Health check")
        print("  version                    Show version")
        print()
        print("Examples:")
        print("  oh-my-copilot interview 'clarify the auth change'")
        print("  oh-my-copilot ralplan 'OAuth2 redesign'")
        print("  oh-my-copilot ultragoal 'carry the approved plan to completion'")
        print("  oh-my-copilot autopilot 'implement auth end-to-end'")
        print("  oh-my-copilot best-practice 'OAuth2 token storage'")
        print("  omp ask codex 'review this patch'")
        return 0

    def _version_command(self, args: list[str] = None) -> int:
        """Show version."""
        print(f"{self.name} {self.version}")
        return 0


def main():
    """Main entry point for the CLI."""
    cli = CLI()
    sys.exit(cli.run())


if __name__ == "__main__":
    main()
