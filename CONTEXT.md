# oh-my-copilot Context

## Shared Language

- Skill: 하나의 엔지니어링 작업 흐름을 캡슐화한 재사용 가능한 오케스트레이터.
- Domain model: 스킬이 다루는 핵심 개념, 상태, 불변식을 표현하는 Python 객체.
- Ubiquitous language: 문서, 테스트, 코드에서 같은 의미로 쓰는 프로젝트 용어 집합.
- Workflow: 여러 스킬이 순서대로 연결되어 하나의 개발 작업을 완수하는 흐름.
- Canonical workflow: `interview -> ralplan -> prometheus -> ultragoal -> review -> ultraqa`.
- Autopilot: canonical workflow를 가능한 한 자동으로 진행하는 자율 실행 스킬.
- Agent catalog: 특화된 에이전트 페르소나와 호출 방식을 정의하는 목록.
- Reference product: 기능 동등성의 기준으로 삼는 `oh-my-claudecode` 공개 README, 문서, CLI/스킬 표면.
- Feature parity: 기준 제품의 기능이 Copilot 환경에서 동일한 사용자 가치를 제공하도록 구현, 검증, 문서화된 상태.
- Parity gap: 기준 제품에는 있지만 oh-my-copilot에는 아직 구현 또는 검증되지 않은 기능 차이.
- OMP CLI: `oh-my-claudecode`의 `omc`에 대응하는 `oh-my-copilot`의 공개 터미널 CLI 명령 이름. 개발 중에는 `python -m cli` fallback을 사용할 수 있지만, 공개 사용자 표면은 `omp`를 기준으로 설계합니다.
- Thin CLI adapter: 도메인 규칙을 직접 갖지 않고 스킬 API를 호출해 출력과 종료코드만 담당하는 CLI 계층.
- Deep module: public interface는 작고 명확하지만 내부 구현이 충분한 책임을 감추는 모듈.
- Validation gate: 계획, 연구, QA 같은 흐름에서 다음 단계로 넘어가기 전에 충족해야 하는 검증 조건.

## Architecture Model

oh-my-copilot은 세 계층을 기준으로 설계합니다.

### Domain

`src/domain/`은 프로젝트의 보편 언어와 상태 전이를 담습니다. 이 계층은 skills, CLI, runtime에 의존하지 않습니다.

도메인 모델은 다음을 책임집니다.

- 입력 검증
- 상태 표현
- 도메인 불변식 유지
- 테스트하기 쉬운 순수 동작 제공

### Skills

`src/skills/`는 도메인 모델을 사용해 작업 흐름을 제공합니다. 스킬은 외부 사용자에게 가장 중요한 Python API입니다.

스킬은 다음을 책임집니다.

- 도메인 객체 생성
- 워크플로우 단계 실행
- 도메인 결과 반환
- public API를 작고 예측 가능하게 유지

### CLI

`src/cli/`는 스킬을 명령어로 노출합니다. CLI는 사용자의 입력을 파싱하고, 스킬을 호출하고, 사람이 읽을 수 있는 출력을 만듭니다.

CLI는 도메인 규칙을 소유하지 않습니다. 같은 규칙이 Python API와 CLI에서 모두 필요하면 domain 또는 skill 계층에 둡니다.

공개 CLI 이름은 `omp`입니다. `python -m cli`는 테스트와 로컬 개발에서 사용할 수 있는 모듈 실행 경로이며, parity backlog에서 사용자-facing CLI 기능을 정의할 때는 `omp <command>` 형태를 기준으로 삼습니다.

### Core

`src/core/`는 런타임 통합을 위한 자리입니다. 개별 스킬의 도메인 규칙을 이 계층에 넣지 않습니다.

## Current Skill Families

- Discovery and planning: `DeepInterviewSkill`, `RalPlanSkill`, `StrategicPlanSkill`, `PrometheusStrictSkill`
- Execution and coordination: `UltragoalSkill`, `TeamRuntimeSkill`, `RalphSkill`, `UltraworkSkill`, `AutopilotSkill`, `SwarmSkill`
- Quality and verification: `CodeReviewSkill`, `UltraQASkill`, `VisualVerdictSkill`, `VisualRalphSkill`, `DiagnosticSkill`
- Knowledge and research: `DomainModelingSkill`, `WikiSkill`, `AutoresearchSkill`, `AutoresearchGoalSkill`, `BestPracticeResearchSkill`, `DeepSearchSkill`, `DesignSkill`
- Tooling and integration: `SparkshellSkill`, `HooksSkill`, `GitHubIntegrationSkill`, `ProviderAdvisorSkill`, `RateLimitWaitSkill`, `SessionFrictionSkill`, `NotificationConfigSkill`, `ProjectSetupSkill`, `EcomodeSkill`, `AgentCatalogSkill`

## Parity Model

`oh-my-copilot`의 장기 로드맵은 `oh-my-claudecode`와의 기능 동등성입니다. 기능을 추가하거나 리팩터링할 때는 먼저 기준 제품의 공개 동작을 작은 parity 항목으로 쪼개고, 각 항목을 domain model, skill orchestrator, CLI/문서, 검증 증거로 연결합니다.

Parity 항목은 다음 질문에 답해야 합니다.

- 기준 제품의 어떤 기능, 명령, 스킬, 상태, 문서 동작에 대응하는가?
- Copilot 환경에서 동일한 사용자 가치를 제공하려면 이름, UX, 런타임 경계가 어떻게 달라져야 하는가?
- 구현 완료를 어떤 테스트, smoke check, 문서 링크, 또는 에이전트 검토 결과로 증명하는가?
- 남은 차이가 의도된 Copilot 적응인지, 아직 닫지 않은 parity gap인지 구분했는가?

## Current Assumptions

- `oh-my-claudecode`의 공개 기능 표면은 parity backlog의 기준입니다.
- Claude Code 전용 기능은 그대로 복제하지 않고 Copilot에서 같은 작업 능력을 제공하는 방향으로 번역합니다.
- `omc` CLI에 대응하는 공개 명령 이름은 `omp`입니다.
- The Python API is the stable center; the CLI is an adapter over it.
- Domain models are allowed to be rich enough to protect invariants.
- Skills should compose through explicit inputs and outputs rather than hidden global state.
- Tests should make behavior visible through domain objects, not only through printed CLI output.
- Documentation should describe the workflow language agents need before they touch code.

## Naming Guidance

- Use `Session` for ongoing interactive or iterative work.
- Use `Report` for generated summaries of completed or inspected work.
- Use `Status` enums for lifecycle state.
- Use `Finding`, `Evidence`, `Hypothesis`, `Checkpoint`, and `Review` with their domain-specific meanings from existing modules.
- Prefer explicit workflow verbs: `create_*`, `add_*`, `validate_*`, `generate_*`, `complete_*`.

## Design Pressure Points

- If a skill needs many unrelated public methods, split the domain concept or introduce a smaller workflow object.
- If CLI tests duplicate domain validation, move the validation downward.
- If two skills need the same concept, put the concept in `domain/` rather than importing one skill from another.
- If a module boundary changes, update or add an ADR before the reasoning is lost.