"""Session friction reporting skill."""

from domain import (
    FrictionSignal,
    FrictionSignalType,
    SessionFrictionReport,
    SessionFrictionSession,
)


class SessionFrictionSkill:
    """Summarize local session friction without exposing raw session content."""

    name = "session-friction"
    description = "Summarize context-bloat and operator-friction signals from local sessions"

    def create_session(self, since: str) -> SessionFrictionSession:
        """Create a friction reporting session."""
        return SessionFrictionSession(since=since)

    def add_signal(
        self,
        session: SessionFrictionSession,
        signal_type: FrictionSignalType,
        summary: str,
    ) -> FrictionSignal:
        """Add a sanitized friction signal to a report session."""
        signal = FrictionSignal(signal_type=signal_type, summary=summary)
        session.add_signal(signal)
        return signal

    def generate_report(self, since: str) -> SessionFrictionReport:
        """Generate an empty local session friction report for a time window."""
        return self.generate_report_from_session(self.create_session(since))

    def generate_report_from_session(
        self,
        session: SessionFrictionSession,
    ) -> SessionFrictionReport:
        """Generate a report from a populated friction session."""
        breakdown: dict[str, int] = {}
        for signal in session.signals:
            key = signal.signal_type.value
            breakdown[key] = breakdown.get(key, 0) + 1

        total = len(session.signals)
        return SessionFrictionReport(
            since=session.since,
            total_signals=total,
            signal_breakdown=breakdown,
            summary=f"Found {total} friction signals since {session.since}.",
        )
