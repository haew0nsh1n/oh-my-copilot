"""Tests for deep search skill."""
import pytest
from skills import DeepSearchSkill
from domain import SearchScope


class TestDeepSearchBasics:
    def test_skill_created(self):
        assert DeepSearchSkill().name == "deepsearch"

    def test_create_session(self):
        skill = DeepSearchSkill()
        session = skill.create_session("auth flow", scope=SearchScope.SYMBOLS)
        assert session.query == "auth flow"
        assert session.scope == SearchScope.SYMBOLS

    def test_empty_query_raises(self):
        with pytest.raises(ValueError):
            DeepSearchSkill().create_session("")


class TestSearchResults:
    def test_add_result(self):
        skill = DeepSearchSkill()
        session = skill.create_session("login")
        result = skill.add_result(session, "auth.py", 42, "def login(user):", relevance_score=0.9)
        assert result.file_path == "auth.py"
        assert result.line_number == 42
        assert len(session.results) == 1

    def test_max_results_limit(self):
        skill = DeepSearchSkill()
        session = skill.create_session("query", max_results=2)
        skill.add_result(session, "f1.py", 1, "match1", 0.9)
        skill.add_result(session, "f2.py", 2, "match2", 0.8)
        skill.add_result(session, "f3.py", 3, "match3", 0.7)  # Should be ignored
        assert len(session.results) == 2

    def test_get_top_results_sorted(self):
        skill = DeepSearchSkill()
        session = skill.create_session("query")
        skill.add_result(session, "low.py", 1, "low", 0.3)
        skill.add_result(session, "high.py", 2, "high", 0.9)
        skill.add_result(session, "mid.py", 3, "mid", 0.6)
        top = skill.get_top_results(session, 2)
        assert top[0].file_path == "high.py"
        assert top[1].file_path == "mid.py"

    def test_has_results(self):
        skill = DeepSearchSkill()
        session = skill.create_session("query")
        assert not session.has_results()
        skill.add_result(session, "f.py", 1, "content", 0.5)
        assert session.has_results()


class TestDeepSearchReport:
    def test_generate_report(self):
        skill = DeepSearchSkill()
        session = skill.create_session("auth", scope=SearchScope.CODEBASE)
        skill.add_result(session, "auth.py", 10, "login", 0.9)
        skill.add_result(session, "user.py", 5, "user model", 0.7)
        report = skill.generate_report(session)
        assert report.total_results == 2
        assert "auth.py" in report.top_files
