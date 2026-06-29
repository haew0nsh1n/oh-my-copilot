"""Rate-limit wait skill for OMP wait parity."""

import json
from pathlib import Path

from domain import RateLimitWaitResult, RateLimitWaitStateArtifact, WaitAction, WaitStatus


class RateLimitWaitSkill:
    """Prepare rate-limit wait and auto-resume guidance."""

    name = "rate-limit-wait"
    description = "Check rate-limit wait state and prepare auto-resume actions"

    def check_status(self) -> RateLimitWaitResult:
        """Report rate-limit wait guidance for the current session."""
        return RateLimitWaitResult(
            action=WaitAction.CHECK,
            status=WaitStatus.READY,
            guidance="No local rate limit daemon state is active; wait for the rate limit reset before resuming.",
        )

    def start_auto_resume(self) -> RateLimitWaitResult:
        """Prepare auto-resume daemon startup guidance."""
        return RateLimitWaitResult(
            action=WaitAction.START,
            status=WaitStatus.PREPARED,
            guidance="Auto-resume start prepared; run inside a tmux-capable session when provider credentials are available.",
        )

    def stop_auto_resume(self) -> RateLimitWaitResult:
        """Prepare auto-resume daemon shutdown guidance."""
        return RateLimitWaitResult(
            action=WaitAction.STOP,
            status=WaitStatus.PREPARED,
            guidance="Auto-resume stop prepared; disable any active wait daemon for this workspace.",
        )

    def save_state(
        self,
        result: RateLimitWaitResult,
        state_root: Path | str,
    ) -> RateLimitWaitStateArtifact:
        """Persist local rate-limit wait state."""
        root = Path(state_root)
        root.mkdir(parents=True, exist_ok=True)
        path = root / "wait.json"
        path.write_text(
            json.dumps(
                {
                    "action": result.action.value,
                    "status": result.status.value,
                    "tmux_required": result.tmux_required,
                    "guidance": result.guidance,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )
        return RateLimitWaitStateArtifact(path=path)

    def load_state(self, state_root: Path | str) -> RateLimitWaitResult:
        """Restore local rate-limit wait state."""
        path = Path(state_root) / "wait.json"
        data = json.loads(path.read_text())
        return RateLimitWaitResult(
            action=WaitAction(data["action"]),
            status=WaitStatus(data["status"]),
            guidance=data["guidance"],
            tmux_required=data.get("tmux_required", True),
        )
