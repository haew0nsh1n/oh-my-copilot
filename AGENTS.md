<!-- OMX:AGENTS:START -->

# oh-my-copilot Agent Configuration

## Overview

oh-my-copilot은 Python으로 구현된 에이전트 주도 엔지니어링 스킬 프레임워크입니다.
이 패키지는 Matt Pocock식 엔지니어링 워크플로우를 재사용 가능한 도메인 모델,
스킬 오케스트레이터, CLI 명령으로 제공합니다.

## Parity Mission

최종 제품 목표는 https://github.com/Yeachan-Heo/oh-my-claudecode 의 공개 기능을
GitHub Copilot 환경에서 모두 동등하게 제공하는 것입니다. 새 기능, 리팩터링, 문서 작업은
가능하면 `oh-my-claudecode`의 기능 표면과 비교해 parity gap을 닫는 방향으로 해석합니다.

동등성은 이름을 그대로 복사하는 것이 아니라 사용자가 얻는 능력을 맞추는 것입니다. Claude Code
전용 플러그인, slash command, tmux/provider 런타임은 Copilot에서 실행 가능한 Python API,
CLI, 에이전트 스킬, 문서화된 검증 루프로 번역합니다.

CLI parity는 `oh-my-claudecode`의 `omc`에 대응하는 `omp` 명령을 기준으로 합니다.
`python -m cli ...`는 개발 중 smoke check와 fallback으로 사용할 수 있지만, 공개 사용자 문서와
최종 구현 목표는 `omp ...` 형태여야 합니다.

## Agent Skill Layer

현재 워크스페이스에서 에이전트가 사용할 Matt Pocock식 작업 스킬의 기준은
`.agents/skills/`입니다. `src/skills/`와 CLI 명령은 이 레포가 구현하는
제품 코드이므로, 에이전트 스킬 가용성의 기준으로 섞어 해석하지 않습니다.

로컬 스킬 디렉터리에 있는 `codebase-design`, `design-an-interface`, `diagnosing-bugs`,
`domain-modeling`, `grilling`, `request-refactor-plan`, `review`, `tdd` 등을 현재 디렉터리
기준의 단일 스킬 레이어로 사용합니다.

## Project Documents

- `BRIEF.md`: 프로젝트 목적, 사용자, 범위, 완료 정의
- `CONTEXT.md`: 공유 언어, 아키텍처 경계, 현재 가정
- `docs/adr/`: 이미 승인된 아키텍처 결정

작업을 시작할 때는 이 파일과 함께 `CONTEXT.md`를 읽고, 구조나 책임 경계를 바꾸는
변경은 관련 ADR을 확인한 뒤 진행합니다.

## Agent skills

### Issue tracker

Issues and PRDs are tracked in GitHub Issues; external PRs are not a triage surface by default. See `docs/agents/issue-tracker.md`.

### Triage labels

The canonical Matt Pocock triage roles map directly to matching GitHub label names. See `docs/agents/triage-labels.md`.

### Domain docs

This is a single-context repo with root `CONTEXT.md`, `BRIEF.md`, and `docs/adr/`. See `docs/agents/domain.md`.

## Canonical Workflow

```
interview -> ralplan -> prometheus -> ultragoal -> review -> ultraqa
```

자율 실행은 `autopilot`이 담당합니다. 검토나 QA에서 실패한 계획은 필요한 경우
`ralplan` 단계로 되돌려 다시 설계합니다.

## Autonomous Parity Execution

사용자가 기능 구현을 요청하거나 parity gap을 지적하면, 에이전트는 명시적으로 중단 요청을 받기 전까지
다음 루프를 유지합니다.

1. `parity-analyst` 관점으로 `oh-my-claudecode` 기준 기능과 현재 구현 차이를 식별합니다.
2. `planner` 또는 `architect` 관점으로 가장 작은 구현 단위와 검증 기준을 정합니다.
3. `parity-implementer` 또는 `executor` 관점으로 domain, skills, CLI, 문서를 필요한 만큼 수정합니다.
4. `test-engineer`, `verifier`, `parity-verifier` 관점으로 `uv run pytest`, 좁은 smoke check, `omp` 또는 `python -m cli` fallback 실행, 문서 일치 여부를 확인합니다.
5. 검증이 실패하면 `debugger` 또는 `build-fixer` 관점으로 같은 slice를 고치고 같은 검증을 다시 실행합니다.
6. 모든 관련 parity 항목이 구현, 검증, 문서화될 때까지 다음 gap으로 이동합니다.

작업 완료를 선언하려면 최소 하나 이상의 실행 가능한 검증 증거가 있어야 합니다. 전체 테스트가 가능한 환경이면
`uv run pytest`를 우선 사용합니다.

## 스킬 목록 (34개)

### 핵심 워크플로우
| 스킬 | CLI | 설명 |
|------|-----|------|
| `DeepInterviewSkill` | `interview` | 요구사항 명확화 |
| `RalPlanSkill` | `ralplan` | Architect→Critic 합의 계획 |
| `PrometheusStrictSkill` | `prometheus` | 고위험 계획 강화 |
| `UltragoalSkill` | `ultragoal` | 다중 목표 체크포인트 실행 |
| `TeamRuntimeSkill` | `team` | 병렬 워커 조정 및 provider team 요청 준비 |
| `RalphSkill` | `ralph` | 단일 소유자 완료 루프 |
| `CodeReviewSkill` | `review` | 코드 품질 검토 |
| `UltraQASkill` | `ultraqa` | 테스트/검증/수정 루프 |

### 실행 모드
| 스킬 | CLI | 설명 |
|------|-----|------|
| `AutopilotSkill` | `autopilot` | 완전 자율 워크플로우 루프 |
| `UltraworkSkill` | `ultrawork` | 최대 병렬 실행 |
| `VisualVerdictSkill` | `visual-verdict` | 시각적 QA (threshold: 90+) |
| `EcomodeSkill` | `ecomode` | 토큰 효율 모델 라우팅 |
| `SwarmSkill` | `swarm` | 팀 호환 파사드 |

### 계획 & 연구
| 스킬 | CLI | 설명 |
|------|-----|------|
| `StrategicPlanSkill` | `plan` | 고수준 전략 계획 |
| `BestPracticeResearchSkill` | `best-practice` | 공식 문서 기반 베스트 프랙티스 |
| `AutoresearchSkill` | `autoresearch` | 검증 게이트 제한 연구 |
| `AutoresearchGoalSkill` | `autoresearch-goal` | 목표 모드 연구 |

### 특화 스킬
| 스킬 | CLI | 설명 |
|------|-----|------|
| `BrainstormingSkill` | `brainstorm` | 아이디어 생성 |
| `DomainModelingSkill` | `domain` | 도메인 개념 모델링 |
| `DiagnosticSkill` | `diagnose` | 버그 진단 |
| `SparkshellSkill` | `sparkshell` | 안전 셸 실행 |
| `WikiSkill` | `wiki` | 프로젝트 지식 관리 |
| `HooksSkill` | `hooks` | 라이프사이클 훅 |
| `GitHubIntegrationSkill` | `github` | GitHub 이슈 관리 |
| `ProviderAdvisorSkill` | `ask` | 외부 provider 자문 요청 준비 |
| `RateLimitWaitSkill` | `wait` | rate-limit wait 및 auto-resume 준비 |
| `SessionFrictionSkill` | `session` | 로컬 세션 friction report 요약 |
| `NotificationConfigSkill` | `config-stop-callback` | stop callback notification 설정 준비 |
| `ProjectSetupSkill` | `setup` | `.omp` 로컬 state root 초기화 |
| `StateSummarySkill` | `hud` | `.omp` 로컬 state 요약 |

### Agent Shortcuts
| 스킬 | CLI | 설명 |
|------|-----|------|
| `DeepSearchSkill` | `deepsearch` | 코드베이스 심층 검색 |
| `DesignSkill` | `design` | DESIGN.md 유지 |
| `VisualRalphSkill` | `visual-ralph` | 시각적 참조 구현 루프 |
| `AgentCatalogSkill` | `agent` / `agents` | 30개 전문가 에이전트 호출 |

## Agent Catalog (33개)

```
oh-my-copilot agents  # 전체 목록 조회
oh-my-copilot <agent-name> <prompt>  # 직접 호출
oh-my-copilot agent <name> <prompt>  # 범용 호출
```

| 카테고리 | 에이전트 |
|---------|---------|
| Build & Analysis | explore, analyst, planner, architect, debugger, executor, verifier, parity-implementer |
| Review | style-reviewer, quality-reviewer, api-reviewer, security-reviewer, performance-reviewer, code-reviewer |
| Domain Specialists | dependency-expert, test-engineer, quality-strategist, build-fixer, designer, writer, qa-tester, git-master, researcher, parity-analyst |
| Product | product-manager, ux-researcher, information-architect, product-analyst |
| Coordination | critic, scholastic, vision, parity-verifier |

## Architecture Rules

### Domain Layer (`src/domain/`)

- 파일당 하나의 주요 도메인 개념을 둡니다.
- 도메인 모델은 스킬이나 CLI에 의존하지 않습니다.
- 입력 검증은 가능한 한 `__post_init__` 또는 명시적 도메인 메서드에서 수행합니다.
- 상태는 문자열보다 Enum으로 표현합니다.
- 도메인 객체는 스킬에서 반환할 수 있는 안정적인 public contract입니다.

### Skill Layer (`src/skills/`)

- 각 스킬은 도메인 모델을 오케스트레이션합니다.
- 스킬은 `name`, `description` 같은 간단한 식별 속성을 유지합니다.
- public 메서드는 워크플로우 동사를 사용합니다. 예: `create_session`, `add_evidence`, `generate_report`.
- 서로 다른 스킬 간 직접 결합은 피하고, 공유 의미는 도메인 모델로 올립니다.

### CLI Layer (`src/cli/`)

- CLI는 thin adapter입니다.
- CLI 명령은 스킬 public API를 호출하고 사용자 출력/종료코드만 책임집니다.
- 스킬이나 도메인 규칙을 CLI에 중복 구현하지 않습니다.

### Core Layer (`src/core/`)

- 런타임/에이전트 통합을 위한 경계입니다.
- 도메인 규칙이나 개별 스킬 로직을 이 계층으로 끌어올리지 않습니다.

## Coding Rules

- Python 3.10+를 기준으로 작성합니다.
- 표준 라이브러리만으로 충분한 곳에는 새 런타임 의존성을 추가하지 않습니다.
- 타입 힌트를 유지하고, public API 변경은 테스트와 문서를 함께 갱신합니다.
- 새 스킬을 추가할 때는 `domain/`, `skills/`, `tests/unit/skills/`, 필요한 경우 `cli/commands/`를 함께 검토합니다.
- 기존 공개 클래스명과 CLI 명령명은 호환성을 깨지 않도록 변경합니다.

## Testing Rules

- 도메인 모델은 불변식과 검증 실패 경로를 테스트합니다.
- 스킬 테스트는 도메인 모델을 통해 관찰 가능한 워크플로우 결과를 검증합니다.
- CLI 테스트는 명령 라우팅, 출력, 종료코드를 검증합니다.
- 좁은 변경에는 좁은 테스트를 먼저 실행하고, 계층 경계를 건드린 변경에는 전체 `pytest`를 실행합니다.

## Utility Commands

```bash
omp doctor            # 공개 CLI 목표: 스킬 헬스체크
omp skills            # 공개 CLI 목표: 스킬 목록
omp agents            # 공개 CLI 목표: 에이전트 목록
omp help              # 공개 CLI 목표: 전체 도움말

python -m cli doctor   # 34개 스킬 헬스체크
python -m cli skills   # 스킬 목록
python -m cli agents   # 에이전트 목록
python -m cli help     # 전체 도움말
pytest tests/                         # 전체 테스트
```

## Change Checklist

- `CONTEXT.md`의 용어와 맞는 이름을 사용했는가?
- 관련 ADR과 충돌하지 않는가?
- 도메인 규칙이 CLI나 테스트 fixture에만 숨어 있지 않은가?
- public API 변경이면 README, BRIEF, 테스트가 함께 갱신되었는가?

<!-- OMX:AGENTS:END -->

