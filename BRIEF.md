# BRIEF - oh-my-copilot

## One Sentence

oh-my-copilot은 `oh-my-claudecode`가 제공하는 에이전트 오케스트레이션 경험을 GitHub Copilot 환경에서 동일하게 제공하는 것을 목표로 하며, 요구사항 탐색, 계획, 구현, 리뷰, QA를 반복 가능한 Python 스킬로 수행하게 하는 엔지니어링 워크플로우 프레임워크입니다.

## Product Goal

최종 목표는 https://github.com/Yeachan-Heo/oh-my-claudecode 를 기준 제품으로 삼아, `oh-my-claudecode`의 모든 공개 기능을 `oh-my-copilot`에서도 동등하게 제공하는 것입니다. 기능 이름이나 내부 구현은 Copilot 환경에 맞게 조정할 수 있지만, 사용자가 얻는 워크플로우 능력, 검증 루프, 에이전트 협업 경험은 빠짐없이 대응되어야 합니다.

`oh-my-claudecode`가 터미널 CLI 표면으로 `omc`를 제공하듯이, `oh-my-copilot`의 공개 터미널 CLI 표면은 `omp`를 목표로 합니다. `python -m cli ...`는 로컬 개발과 테스트를 위한 fallback으로 유지할 수 있지만, 사용자 문서와 parity 구현은 최종적으로 `omp ...` 명령을 기준으로 설계합니다.

## Users

- 에이전트 기반 개발 워크플로우를 실험하거나 교육하는 개발자
- TDD, 진단, 코드 리뷰, 도메인 모델링 같은 작업을 재사용 가능한 스킬로 분리하려는 팀
- CLI와 Python API 양쪽에서 동일한 엔지니어링 루프를 실행하려는 도구 작성자

## Core Scenarios

최종 사용자-facing CLI 시나리오는 `omp`를 기준으로 합니다. `omp` entry point가 구현되기 전까지 로컬 개발에서는 같은 명령을 `python -m cli ...`로 검증할 수 있습니다.

```bash
$ omp skills
# 사용 가능한 스킬 목록을 확인한다.

$ omp interview "결제 리팩터링 요구사항 정리"
# 구현 전 요구사항과 모호한 지점을 명확히 한다.

$ omp ralplan "결제 모듈 리팩터링 계획"
# Architect/Critic 검토를 거친 계획을 만든다.

$ omp ultraqa "결제 모듈 QA"
# 테스트, 검증, 수정 루프로 병합 준비 상태를 점검한다.
```

## Requirements

- `oh-my-claudecode`의 공개 README, 문서, CLI/스킬 표면을 기준으로 parity backlog를 유지해야 합니다.
- 각 parity 항목은 `not-started`, `implemented`, `verified`, `documented` 같은 관찰 가능한 상태를 가져야 합니다.
- 공개 CLI parity는 `omc`에 대응하는 `omp` 명령을 기준으로 구현하고 문서화해야 합니다.
- 각 스킬은 명확한 domain model과 skill orchestrator를 가져야 합니다.
- 스킬 public API는 Python 코드에서 직접 사용할 수 있어야 합니다.
- CLI 명령은 스킬 public API 위의 얇은 어댑터여야 합니다.
- 도메인 모델은 자체 검증과 명확한 상태 표현을 제공해야 합니다.
- 테스트는 도메인 불변식, 스킬 워크플로우, CLI 라우팅을 분리해서 검증해야 합니다.
- 아키텍처 결정은 `docs/adr/`에 남기고, 공유 언어는 `CONTEXT.md`에 유지해야 합니다.

## Non-Goals

- 실제 AI 모델 호출 런타임을 구현하는 것
- 외부 서비스에 강하게 결합된 프로덕션 오케스트레이션 플랫폼을 만드는 것
- Claude Code 전용 UI나 플러그인 동작을 그대로 복제하느라 Copilot 환경의 제약을 무시하는 것
- 모든 스킬을 하나의 거대한 실행 엔진으로 합치는 것
- CLI 편의를 위해 도메인 규칙을 중복 구현하는 것
- 문서에만 존재하고 테스트되지 않는 public workflow를 늘리는 것

## Implementation Constraints

- Python 3.10+를 지원합니다.
- 패키지 코드는 `src/` 아래에 둡니다.
- 도메인 모델은 `src/domain/`에, 스킬 오케스트레이터는 `src/skills/`에 둡니다.
- 테스트는 `tests/unit/`과 `tests/integration/`에 둡니다.
- 새 의존성은 명확한 이유가 있을 때만 `pyproject.toml`에 추가합니다.

## Definition of Done

- 관련 `oh-my-claudecode` 기능과의 parity 항목이 구현, 검증, 문서화됩니다.
- 공개 CLI를 건드린 변경은 `omp ...` 동작 또는 아직 entry point가 없을 경우 `python -m cli ...` fallback과 `omp` 구현 계획을 함께 검증합니다.
- 새 동작이나 public API는 테스트로 검증됩니다.
- 관련 CLI 명령이 있다면 CLI 테스트나 좁은 smoke check가 통과합니다.
- 도메인 용어가 `CONTEXT.md`, 코드, 테스트에서 같은 의미로 쓰입니다.
- 계층 경계를 바꾸는 결정은 ADR로 기록됩니다.
- `pytest` 또는 변경 범위에 맞는 좁은 테스트가 통과합니다.