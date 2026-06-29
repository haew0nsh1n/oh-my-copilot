# ADR 0001: Skill Interface and Domain Model Separation

**Date**: 2026-06-19
**Status**: ACCEPTED
**Context**: Designing the core architecture for oh-my-copilot

## Problem

How should we structure the oh-my-copilot framework to support:
1. Reusable engineering skills
2. Clear domain models
3. Test-driven development
4. Easy agent integration

## Decision

We separate the architecture into three layers:

### 1. Domain Layer (`domain/`)
- **Purpose**: Define ubiquitous language
- **Responsibility**: Domain concepts, validation, state management
- **Example**: `BrainstormSession`, `BrainstormIdea`, `BrainstormOutcome`
- **Constraint**: No dependencies on skills or runtime

### 2. Skill Layer (`skills/`)
- **Purpose**: Reusable engineering workflows
- **Responsibility**: Orchestrate domain operations, business logic
- **Example**: `BrainstormingSkill` uses domain models
- **Constraint**: Depends on domain, not on other skills

### 3. Core/Runtime Layer (`core/`)
- **Purpose**: Agent integration and execution
- **Responsibility**: Agent callbacks, execution context
- **Future**: Skill registration, lifecycle management

## Benefits

✅ **Testability** - Domain models can be tested without skills
✅ **Reusability** - Skills can be used in multiple contexts
✅ **Clarity** - Separation of concerns is explicit
✅ **Extensibility** - Easy to add new skills without modifying core

## Trade-offs

❌ **Slight overhead** - Data flows through three layers
❌ **More files** - More complex project structure than monolithic design

## Implementation

### Example: Brainstorming Skill

**Domain** (`BrainstormSession`):
```python
@dataclass
class BrainstormSession:
    prompt: str
    ideas: List[BrainstormIdea] = field(default_factory=list)
    
    def add_idea(self, idea: BrainstormIdea) -> None: ...
    def select_idea(self, idea: BrainstormIdea) -> None: ...
```

**Skill** (`BrainstormingSkill`):
```python
class BrainstormingSkill:
    def create_session(self, prompt: str) -> BrainstormSession: ...
    def add_idea(self, session: BrainstormSession, ...) -> BrainstormIdea: ...
    def select_best_idea(self, session: BrainstormSession) -> BrainstormOutcome: ...
```

**Testing**:
- Domain models have unit tests (no dependencies)
- Skills have integration tests (with domain)
- Runtime has end-to-end tests (with agents)

## Related Decisions

- ADR 0002: TDD as Standard Practice (coming)
- ADR 0003: Skill Registration and Discovery (coming)

## References

- "A Philosophy of Software Design" by John Ousterhout (Deep Modules)
- Domain-Driven Design by Eric Evans
- Matt Pocock's codebase-design skill
