# ADR 0002: Codebase Design - Deep Module Architecture

**Date**: 2026-06-19
**Status**: ACCEPTED
**Context**: Designing module interfaces for oh-my-copilot

## Problem

How should we structure modules in oh-my-copilot to:
1. Hide complexity in internal implementations
2. Provide simple, expressive public interfaces
3. Make code easy for agents to navigate
4. Reduce dependencies and coupling

## Decision

We follow the **Deep Module** principle from "A Philosophy of Software Design":
- **Interface should be simple** - Few public methods/concepts
- **Implementation can be complex** - Hide details behind the interface
- **Functionality is large relative to interface complexity** - Good depth ratio

### Module Structure

```
oh-my-copilot/
├── domain/          # Domain models (simple, focused)
│   ├── brainstorm_session.py  # One concept per file
│   └── domain_model.py
│
├── skills/          # Skill orchestrators (moderate complexity)
│   ├── brainstorming.py       # Uses domain models
│   └── domain_modeling.py
│
└── core/            # Runtime (to be designed)
    └── (Future: agent integration)
```

## Module Design Principles

### 1. Domain Module (`domain/`)

**Principle**: Domain models should be **pure** and **self-contained**.

```python
# ✅ GOOD: Simple interface, clear responsibility
@dataclass
class BrainstormSession:
    prompt: str
    ideas: List[BrainstormIdea]
    
    def add_idea(self, idea: BrainstormIdea) -> None: ...
    def select_idea(self, idea: BrainstormIdea) -> None: ...

# ❌ BAD: Too complex, mixes concerns
class Session:
    def add_idea_and_notify_agents(self): ...
    def execute_ai_service(self): ...
    def log_to_database(self): ...
```

**Module Characteristics**:
- ✅ Represents one domain concept
- ✅ Has clear validation in `__post_init__`
- ✅ No dependencies on skills or runtime
- ✅ Easy to test (no mocking needed)
- ✅ Clear error messages on invalid state

**Depth Ratio**: High
- Small interface (3-5 public methods)
- Contains business logic and validation

### 2. Skill Module (`skills/`)

**Principle**: Skills are **orchestrators** that use domain models to implement workflows.

```python
# ✅ GOOD: Orchestrates domain operations
class BrainstormingSkill:
    def create_session(self, prompt: str) -> BrainstormSession: ...
    def add_idea(self, session, ...) -> BrainstormIdea: ...
    def select_best_idea(self, session) -> BrainstormOutcome: ...

# ❌ BAD: Reinvents domain logic
class BrainstormingSkill:
    def create_session_and_add_idea(self): ...  # Too specific
    def execute_all_brainstorm_flow(self): ...  # Does too much
```

**Module Characteristics**:
- ✅ Depends only on domain models
- ✅ Provides workflow-oriented methods
- ✅ Each skill is independent
- ✅ Easy to compose skills
- ✅ Clear method documentation

**Depth Ratio**: Moderate-to-High
- 5-10 public methods
- Uses domain models internally

### 3. Runtime Module (`core/` - Future)

**Principle**: Runtime should be **thin** and focused on agent integration.

**Expected Interface**:
```python
class Agent:
    async def run_skill(self, skill: Skill, context: ExecutionContext) -> Result: ...
    def register_skill(self, skill: Skill) -> None: ...
```

## Design Patterns

### Pattern 1: Domain Model Factory
Use skills to create domain models rather than exposing constructors:

```python
# ✅ GOOD: Factory method in skill
skill = BrainstormingSkill()
session = skill.create_session("prompt")

# ❌ BAD: Direct constructor usage (mixes concerns)
session = BrainstormSession(prompt="...", context={})
```

### Pattern 2: Immutable Value Objects
Value objects should be immutable after creation:

```python
# ✅ GOOD: Dataclass with frozen=True
@dataclass(frozen=True)
class BrainstormIdea:
    title: str
    description: str
```

### Pattern 3: Validation at Boundaries
Always validate input at module boundaries:

```python
# ✅ GOOD: Validate in __post_init__
@dataclass
class DomainConcept:
    name: str
    
    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Name cannot be empty")

# ❌ BAD: Validate in caller code
concept = DomainConcept(name="")  # No error
if not concept.name:  # Caller must check
    handle_error()
```

## Navigation for Agents

Design module interfaces to help agents understand code:

### Clear Method Names
```python
# ✅ GOOD: What does it do?
add_idea()
select_best_idea()
validate_model()

# ❌ BAD: Unclear intent
process_input()
execute()
run()
```

### Clear Docstrings
```python
# ✅ GOOD: Purpose, args, returns, exceptions
def add_concept(
    self,
    model: DomainModel,
    name: str,
    description: str,
    concept_type: ConceptType,
) -> DomainConcept:
    """
    Add a concept to the domain model.
    
    Args:
        model: The domain model to update
        name: Concept name (ubiquitous language term)
        description: What the concept means
        concept_type: Type of concept
        
    Returns:
        The created DomainConcept
        
    Raises:
        ValueError: If concept name already exists
    """
```

### Type Hints
```python
# ✅ GOOD: Full type hints
def add_concept(
    self,
    model: DomainModel,
    name: str,
) -> DomainConcept: ...

# ❌ BAD: Missing types
def add_concept(self, model, name):  # Type unclear
```

## Testing Strategy

Each module layer has different test focus:

### Domain Tests
- Focus on **invariants** and **validation**
- No external dependencies
- Test all edge cases

```python
def test_session_rejects_invalid_prompt():
    with pytest.raises(ValueError):
        BrainstormSession(prompt="")
```

### Skill Tests
- Focus on **orchestration** and **workflows**
- Mock/use real domain models
- Test happy path and error cases

```python
def test_skill_can_add_multiple_ideas():
    skill = BrainstormingSkill()
    session = skill.create_session("prompt")
    idea1 = skill.add_idea(session, ...)
    idea2 = skill.add_idea(session, ...)
    assert len(session.ideas) == 2
```

### Integration Tests (Future)
- Test skills working together
- Test with runtime/agents

## Trade-offs

### Benefits
✅ Modules are **easy to understand** (clear interfaces)
✅ Changes are **well-contained** (high cohesion)
✅ **Easy to test** (dependencies are clear)
✅ **Agent-friendly** (clear method names, full docstrings)
✅ **Reusable** (skills can be composed)

### Costs
❌ More files (domain + skill for each feature)
❌ Initial setup overhead
❌ Requires discipline (easy to violate)

## Related Decisions

- ADR 0001: Skill Interface and Domain Separation
- ADR 0003: TDD as Standard Practice (coming)

## References

- "A Philosophy of Software Design" by John Ousterhout (Chapter 5: Designing Classes)
- Clean Architecture by Robert C. Martin
- Domain-Driven Design by Eric Evans (Entities, Value Objects)
- Matt Pocock's "codebase-design" skill
