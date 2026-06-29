# oh-my-copilot

Agent-driven engineering skills for Python using Matt Pocock's harness engineering patterns.

## Quick Start

```bash
# Install in development mode
pip install -e ".[dev]"

# Initialize project configuration
omp setup

# Verify the public CLI entry point
omp doctor

# Run tests
pytest

# Run with coverage
pytest --cov
```

## 🚀 Usage

### 방법 1: CLI 인터페이스

프로젝트 루트에서 다음 명령어를 실행합니다:

```bash
# 도움말 보기
omp help

# 전체 스킬 목록
omp skills

# 헬스체크 (전체 34개 스킬 확인)
omp doctor

# 버전 확인
omp version

# ── 정규 워크플로우 ──
# 1. 심층 인터뷰 - 요구사항 명확화
omp interview "우리 앱의 인증 구조를 어떻게 개선할까?"

# 2. 아키텍처 계획 - Architect/Critic 승인
omp ralplan "OAuth2 인증 재설계"

# 3. 계획 강화 - 고위험 계획 검증
omp prometheus "인증 시스템 계획"

# 4. 목표 실행 - 다중 목표 추적
omp ultragoal "승인된 계획 실행"

# 병렬 provider team 요청 준비
omp team --check 2:codex "인증 모듈 리뷰"
omp team 2:codex "인증 모듈 리뷰"
omp team status auth-review
omp team shutdown auth-review

# 5. 코드 리뷰
omp review "사용자 인증 기능 추가"

# 6. QA 루프 - 병합 준비 확인
omp ultraqa "인증 기능 QA"

# ── 완전 자동 모드 ──
omp autopilot "OAuth2 인증 end-to-end 구현"

# ── 기타 스킬 ──
# 브레인스토밍
omp brainstorm "우리 앱의 인증 구조를 어떻게 설계할까?"

# 도메인 모델링
omp domain PaymentSystem "온라인 결제 처리"

# 버그 진단
omp diagnose "로그인이 간헐적으로 실패함"

# 베스트 프랙티스 연구
omp best-practice "OAuth2 토큰 저장"

# Provider advisor 요청 준비
omp ask --check codex
omp ask codex "인증 패치 리뷰"
omp ask --execute codex "인증 패치 리뷰"

# Rate-limit wait 상태 확인 및 auto-resume 준비
omp wait
omp wait --start
omp wait --stop

# 로컬 세션 friction report 요약
omp session friction report --since 24h

# 로컬 OMP state HUD 요약
omp hud

# Stop callback notification 설정 준비
omp config-stop-callback telegram --tag-list "@alice,bob"

# 보안 리뷰
omp security-review "인증 모듈"

# TDD
omp tdd "refresh token 기능"
```

개발 중 editable install 전에는 `PYTHONPATH=src python -m cli <command>`를 fallback으로 사용할 수 있습니다.

### 방법 2: Python 코드에서 직접 사용

Python 파일에서 스킬을 직접 import하여 사용합니다:

```python
from skills import (
    BrainstormingSkill,
    DomainModelingSkill,
    DiagnosticSkill,
    CodeReviewSkill,
    GitHubIntegrationSkill,
)
from domain import (
    ConceptType,
    ErrorSeverity,
    ErrorLocation,
    FindingSeverity,
    ReviewAspect,
)

# 1️⃣ 브레인스토밍 - 아이디어 생성
brainstorm = BrainstormingSkill()
session = brainstorm.create_session("인증 구조 설계")
idea1 = brainstorm.add_idea(session, "OAuth2", "OAuth2 프로토콜 기반 인증")
idea2 = brainstorm.add_idea(session, "JWT", "JWT 토큰 기반 상태 비저장 인증")
session.select_idea(idea1)  # 최고의 아이디어 선택
outcome = brainstorm.select_best_idea(session)

# 2️⃣ 도메인 모델링 - 도메인 개념 정의
domain = DomainModelingSkill()
model = domain.create_model("PaymentSystem", "온라인 결제 처리")
domain.add_concept(
    model,
    "Payment",
    "결제 트랜잭션. 고객이 상품 구매 시 만들어지는 핵심 개체",
    ConceptType.AGGREGATE
)
domain.add_concept(
    model,
    "Invoice",
    "청구서. 지불할 항목을 추적하는 문서",
    ConceptType.ENTITY
)
is_valid = domain.validate_model(model)

# 3️⃣ 진단 - 버그 조사 및 근본 원인 분석
diagnostic = DiagnosticSkill()
diag_session = diagnostic.create_session("로그인 실패", ErrorSeverity.HIGH)

# 증거 수집
location = ErrorLocation(
    file_path="auth.py",
    function_name="login()",
    line_number=45
)
diagnostic.add_evidence(
    diag_session,
    "503 Service Unavailable",
    "ServiceUnavailableError",
    location
)

# 가설 생성
diagnostic.add_hypothesis(diag_session, "DB 연결 오류", 0.8)
diagnostic.add_hypothesis(diag_session, "캐시 레이어 문제", 0.5)

# 해결 단계 추가
diagnostic.add_resolution_step(diag_session, "데이터베이스 연결 풀 재시작")
diagnostic.add_resolution_step(diag_session, "캐시 레이어 로그 확인")

# 보고서 생성
report = diagnostic.generate_report(
    diag_session,
    root_cause="데이터베이스 연결 타임아웃",
    affected_components=["Auth Service", "User DB"],
    permanent_fix="DB 연결 풀 설정 최적화"
)

# 4️⃣ 코드 리뷰 - 코드 품질 검토
review = CodeReviewSkill()
code_review = review.create_review("사용자 인증 기능")

# 검토 섹션 추가
review.add_section(
    code_review,
    "Authentication",
    files=["auth.py", "auth_handler.py"],
    lines_changed=150,
    description="사용자 인증 구현"
)

# 발견 사항 추가
review.add_finding(
    code_review,
    location="auth.py:45",
    description="암호가 평문으로 저장됨",
    severity=FindingSeverity.CRITICAL,
    aspect=ReviewAspect.STANDARDS,
    suggestion="bcrypt 또는 argon2로 해싱하세요"
)

# 리뷰 보고서 생성
report = review.generate_report(code_review)

# 5️⃣ GitHub 통합 - GitHub 이슈 생성
github = GitHubIntegrationSkill()

# 버그 리포트 생성
issue = github.create_bug_report(
    title="로그인 인증 실패",
    description="사용자가 간헐적으로 로그인할 수 없음",
    root_cause="데이터베이스 연결 타임아웃",
    reproduction_steps=[
        "로그인 페이지 접속",
        "이메일과 암호 입력",
        "로그인 버튼 클릭",
        "503 에러 발생"
    ]
)

# 기능 요청 생성
feature = github.create_feature_request(
    title="다크 모드 지원",
    description="사용자가 다크 모드로 UI를 사용할 수 있도록 합니다",
    acceptance_criteria=[
        "모든 페이지에서 다크 모드 지원",
        "사용자 선택 사항 저장",
        "시스템 테마 감지 지원"
    ]
)

# 저장소 참조 생성
repo = github.create_repository(
    "myteam",
    "auth-service",
    "인증 서비스"
)
```

## Project Structure

- `src/` - Main package
  - `domain/` - 도메인 모델 (보편 언어 / ubiquitous language)
  - `skills/` - 스킬 구현 (아이디어 생성, 도메인 정의, 버그 진단, 코드 리뷰, GitHub 통합)
  - `cli/` - 명령어 인터페이스
- `tests/` - TDD 기반 테스트
  - `unit/skills/` - 각 스킬 테스트
  - `unit/cli/` - CLI 테스트
  - `integration/` - 스킬 통합 테스트
- `docs/` - 아키텍처 결정 기록 (ADR)

## 📚 Skills

34가지 엔지니어링 스킬이 구현되어 있습니다 (oh-my-claudecode parity 진행 중):

### Phase 1: 기본 스킬 (5개)

| 스킬 | 설명 | 메인 메서드 |
|------|------|-----------|
| **BrainstormingSkill** | 여러 아이디어 생성 및 탐색 | `create_session()`, `add_idea()`, `select_best_idea()` |
| **DomainModelingSkill** | 도메인 개념 및 보편 언어 정의 | `create_model()`, `add_concept()`, `validate_model()` |
| **DiagnosticSkill** | 버그 조사 및 근본 원인 분석 | `create_session()`, `add_evidence()`, `add_hypothesis()` |
| **CodeReviewSkill** | 코드 품질 및 명세 준수 검토 | `create_review()`, `add_finding()`, `generate_report()` |
| **GitHubIntegrationSkill** | GitHub 이슈 생성 및 관리 | `create_issue()`, `create_bug_report()`, `create_feature_request()` |

### Phase 2: 고급 스킬 (5개)

| 스킬 | 설명 | 메인 메서드 |
|------|------|-----------|
| **DeepInterviewSkill** | 요구사항 명확화를 위한 심층 인터뷰 | `create_session()`, `ask_question()`, `clarify_goals()` |
| **UltragoalSkill** | 승인된 계획을 다중 목표 실행으로 변환 | `create_ultragoal()`, `create_goal()`, `add_checkpoint()` |
| **TeamRuntimeSkill** | 여러 워커를 통한 병렬 실행 조정 | `create_team()`, `create_worker()`, `distribute_tasks()` |
| **SparkshellSkill** | 안전 검증을 통한 셸 명령어 실행 | `create_session()`, `validate_command()`, `execute_command()` |
| **WikiSkill** | 프로젝트 지식 관리 및 검색 | `create_page()`, `search_by_tag()`, `publish_page()` |

### Phase 3: 검증 및 연구 스킬 (4개) 

| 스킬 | 설명 | 메인 메서드 |
|------|------|-----------|
| **HooksSkill** | 라이프사이클 훅 및 이벤트 관리 | `register_hook()`, `execute_hooks()`, `get_execution_history()` |
| **PrometheusStrictSkill** | 계획 검증 및 강화 | `create_rule()`, `validate_plan()`, `stress_test_plan()` |
| **AutoresearchSkill** | 검증 게이트가 있는 제한된 연구 | `create_research_task()`, `add_evidence()`, `validate_research()` |
| **BestPracticeResearchSkill** | 공식 소스 증거 수집 | `create_practice()`, `add_evidence_to_practice()`, `get_high_impact_practices()` |

### Phase 4: oh-my-codex 호환 스킬 (6개)

| 스킬 | 설명 | 메인 메서드 | oh-my-codex 대응 |
|------|------|-----------|------------------|
| **RalPlanSkill** | 아키텍처 승인 계획 (Architect→Critic 합의) | `create_plan()`, `submit_architect_review()`, `submit_critic_review()` | `$ralplan` |
| **RalphSkill** | 단일 소유자 영구 완료 루프 | `create_completion()`, `start_iteration()`, `mark_complete()` | `$ralph` |
| **UltraQASkill** | 테스트/검증/수정 루프 (병합 준비) | `create_qa_session()`, `add_test_case()`, `verify_test()` | `$ultraqa` |
| **AutoresearchGoalSkill** | 목표 모드 연구 (Professor/Critic 검증) | `create_research_mission()`, `add_finding()`, `validate_finding()` | `$autoresearch-goal` |
| **AutopilotSkill** | 자율 전체 워크플로우 루프 | `create_workflow()`, `complete_phase()`, `trigger_replan()` | `$autopilot` |
| **StrategicPlanSkill** | 고수준 전략 계획 | `create_plan()`, `add_goal()`, `add_objective()` | `$plan` |

## Development

This project follows TDD (Test-Driven Development) and uses Matt Pocock's engineering skills:

- **domain-modeling** - Ubiquitous language
- **tdd** - Test-first development
- **codebase-design** - Deep module patterns
- **diagnosing-bugs** - Systematic debugging

## 테스트

```bash
# 모든 테스트 실행
pytest

# 테스트 + 커버리지 보고서
pytest --cov

# 특정 스킬 테스트
pytest tests/unit/skills/test_brainstorming.py -v

# CLI 테스트
pytest tests/unit/cli/ -v
```

## 예제

프로젝트에 포함된 `test_skills.py` 파일에서 모든 스킬의 사용 예제를 확인할 수 있습니다:

```bash
python test_skills.py
```
