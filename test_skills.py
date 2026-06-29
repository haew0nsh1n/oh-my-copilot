"""Test script to verify oh-my-copilot skills work correctly."""

from skills import (
    BrainstormingSkill,
    DomainModelingSkill,
    DiagnosticSkill,
    CodeReviewSkill,
    GitHubIntegrationSkill,
)
from domain import (
    FindingSeverity, 
    ReviewAspect,
    ConceptType,
    ErrorSeverity,
    ErrorLocation,
)

print("=" * 60)
print("Testing oh-my-copilot Skills")
print("=" * 60)

# Test 1: Brainstorming Skill
print("\n1️⃣  Testing BrainstormingSkill...")
brainstorm = BrainstormingSkill()
session = brainstorm.create_session("인증 구조 설계")
idea1 = brainstorm.add_idea(session, "OAuth2", "OAuth2 프로토콜 기반 인증")
idea2 = brainstorm.add_idea(session, "JWT", "JWT 토큰 기반 상태 비저장 인증")
idea3 = brainstorm.add_idea(session, "세션", "서버 세션 쿠키 기반 인증")
session.select_idea(idea1)  # Select the best idea
best = brainstorm.select_best_idea(session)
print(f"   ✅ Created session with {len(session.ideas)} ideas")
print(f"   ✅ Selected best idea: {best.selected_title}")

# Test 2: Domain Modeling Skill
print("\n2️⃣  Testing DomainModelingSkill...")
domain = DomainModelingSkill()
model = domain.create_model("PaymentSystem", "온라인 결제 처리")
domain.add_concept(model, "Payment", "결제 트랜잭션", ConceptType.AGGREGATE)
domain.add_concept(model, "Invoice", "청구서", ConceptType.ENTITY)
domain.add_concept(model, "Customer", "고객 정보", ConceptType.ENTITY)
summary = domain.generate_summary(model)
print(f"   ✅ Created domain model with {len(model.concepts)} concepts")
print(f"   ✅ Model is valid: {domain.validate_model(model)}")

# Test 3: Diagnostic Skill
print("\n3️⃣  Testing DiagnosticSkill...")
diagnostic = DiagnosticSkill()
diag_session = diagnostic.create_session("로그인 실패 문제", ErrorSeverity.HIGH)
location1 = ErrorLocation(file_path="auth.py", function_name="login()", line_number=45)
location2 = ErrorLocation(file_path="db.py", function_name="get_connection()", line_number=102)
diagnostic.add_evidence(
    diag_session,
    "에러 메시지: 503 Service Unavailable",
    "ServiceUnavailableError",
    location1
)
diagnostic.add_evidence(
    diag_session,
    "발생 시간: 오후 2-3시 사이",
    "TimeoutError",
    location2
)
diagnostic.add_hypothesis(diag_session, "DB 연결 오류", 0.8)
diagnostic.add_hypothesis(diag_session, "캐시 레이어 문제", 0.5)
diagnostic.add_resolution_step(diag_session, "데이터베이스 연결 풀 재시작")
diagnostic.add_resolution_step(diag_session, "캐시 레이어 로그 확인")
report = diagnostic.generate_report(
    diag_session,
    root_cause="데이터베이스 연결 타임아웃",
    affected_components=["Auth Service", "User DB"],
    permanent_fix="DB 연결 풀 설정 최적화"
)
print(f"   ✅ Collected {len(diag_session.evidence)} evidence items")
print(f"   ✅ Generated {len(diag_session.hypotheses)} hypotheses")
print(f"   ✅ Most likely cause: {report.root_cause}")

# Test 4: Code Review Skill
print("\n4️⃣  Testing CodeReviewSkill...")
review = CodeReviewSkill()
code_review = review.create_review("사용자 인증 기능")
review.add_section(code_review, "Authentication", ["auth.py", "auth_handler.py"], 150)
review.add_finding(
    code_review,
    location="auth.py:45",
    description="암호가 평문으로 저장됨",
    severity=FindingSeverity.CRITICAL,
    aspect=ReviewAspect.STANDARDS,
    suggestion="bcrypt 또는 argon2로 해싱하세요"
)
review.add_finding(
    code_review,
    location="auth.py:67",
    description="CSRF 토큰 검증 누락",
    severity=FindingSeverity.MAJOR,
    aspect=ReviewAspect.STANDARDS,
)
report = review.generate_report(code_review)
print(f"   ✅ Review contains {report.total_findings} findings")
print(f"   ✅ Critical issues: {report.critical_findings}")
print(f"   ✅ Major issues: {report.major_findings}")
print(f"   ✅ Recommendation: {report.recommendation}")

# Test 5: GitHub Integration Skill
print("\n5️⃣  Testing GitHubIntegrationSkill...")
github = GitHubIntegrationSkill()
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
repo = github.create_repository("myteam", "auth-service", "인증 서비스")
print(f"   ✅ Created issue: {issue.title}")
print(f"   ✅ Issue type: {issue.issue_type.value}")
print(f"   ✅ Labels: {', '.join(issue.labels)}")
print(f"   ✅ Repository: {repo.full_name}")

print("\n" + "=" * 60)
print("✅ All skills tested successfully!")
print("=" * 60)
