# oh-my-copilot Development

## Prerequisites

- Python 3.10+
- pip/venv

## Setup

```bash
# Navigate to project
cd oh-my-copilot

# Create virtual environment
python -m venv .venv

# Activate it
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test file
pytest tests/unit/skills/test_brainstorming.py -v

# Run with detailed output
pytest -vv
```

## Current Status

- [x] Domain model (`brainstorm_session.py`)
- [x] Skill implementation (`brainstorming.py`)
- [x] TDD tests (`test_brainstorming.py`)
- [x] All tests passing (295 tests, 100% pass rate)
- [x] Additional skills implementation (20 skills total)
