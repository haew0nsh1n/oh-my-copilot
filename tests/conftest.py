"""Pytest configuration and shared fixtures."""

import pytest


@pytest.fixture
def brainstorm_context():
    """Fixture providing brainstorm session context."""
    return {
        "project": "oh-my-copilot",
        "domain": "agent-engineering"
    }
