"""Tests for ultraqa skill."""

import pytest
from skills import UltraQASkill
from domain import QALoopStatus


class TestUltraQABasics:
    """Test basic ultraqa skill functionality."""
    
    def test_skill_can_be_created(self):
        """RED: Skill can be instantiated."""
        skill = UltraQASkill()
        assert skill is not None
    
    def test_skill_has_name(self):
        """RED: Skill has a name."""
        skill = UltraQASkill()
        assert skill.name == "ultraqa"


class TestQASessionCreation:
    """Test QA session creation."""
    
    def test_create_qa_session(self):
        """RED: Can create a QA session."""
        skill = UltraQASkill()
        
        qa = skill.create_qa_session("Auth Feature QA", "Test authentication feature")
        
        assert qa.title == "Auth Feature QA"
        assert qa.status == QALoopStatus.STARTING


class TestTestCases:
    """Test case management."""
    
    def test_add_test_case(self):
        """RED: Can add test cases."""
        skill = UltraQASkill()
        qa = skill.create_qa_session("QA", "Desc")
        
        test = skill.add_test_case(qa, "Login Test", "Test basic login")
        
        assert test.name == "Login Test"
        assert len(qa.test_cases) == 1
    
    def test_add_test_steps(self):
        """RED: Can add test steps."""
        skill = UltraQASkill()
        qa = skill.create_qa_session("QA", "Desc")
        test = skill.add_test_case(qa, "Test", "Desc")
        
        skill.add_test_step(test, "Navigate to login page")
        skill.add_test_step(test, "Enter credentials")
        skill.add_test_step(test, "Click login")
        
        assert len(test.test_steps) == 3
    
    def test_set_expected_result(self):
        """RED: Can set expected result."""
        skill = UltraQASkill()
        qa = skill.create_qa_session("QA", "Desc")
        test = skill.add_test_case(qa, "Test", "Desc")
        
        skill.set_expected_result(test, "User logged in successfully")
        
        assert test.expected_result == "User logged in successfully"


class TestVerification:
    """Test verification."""
    
    def test_verify_passing_test(self):
        """RED: Can verify passing test."""
        skill = UltraQASkill()
        qa = skill.create_qa_session("QA", "Desc")
        test = skill.add_test_case(qa, "Login", "Test login")
        
        skill.verify_test(qa, test, True, "Login successful")
        
        assert len(qa.get_passed_tests()) == 1
        assert qa.status == QALoopStatus.VERIFYING
    
    def test_verify_failing_test(self):
        """RED: Can verify failing test."""
        skill = UltraQASkill()
        qa = skill.create_qa_session("QA", "Desc")
        test = skill.add_test_case(qa, "Login", "Test login")
        
        skill.verify_test(qa, test, False, "Login failed")
        
        assert len(qa.get_failed_tests()) == 1


class TestFixing:
    """Test fix attempts."""
    
    def test_add_fix(self):
        """RED: Can add fix attempt."""
        skill = UltraQASkill()
        qa = skill.create_qa_session("QA", "Desc")
        
        fix = skill.add_fix(qa, "Fix OAuth2 token issue", ["Update OAuth2 lib"])
        
        assert len(fix.fixes_applied) == 1
        assert qa.status == QALoopStatus.FIXING
    
    def test_mark_fix_successful(self):
        """RED: Can mark fix as successful."""
        skill = UltraQASkill()
        qa = skill.create_qa_session("QA", "Desc")
        fix = skill.add_fix(qa, "Fix issue")
        
        skill.mark_fix_successful(fix, ["test_login"])
        
        assert fix.success
        assert len(fix.tests_to_retry) == 1


class TestMergeReadiness:
    """Test merge readiness."""
    
    def test_merge_ready_when_all_pass(self):
        """RED: Merge ready when all tests pass."""
        skill = UltraQASkill()
        qa = skill.create_qa_session("QA", "Desc")
        test1 = skill.add_test_case(qa, "Test1", "Desc")
        test2 = skill.add_test_case(qa, "Test2", "Desc")
        
        skill.verify_test(qa, test1, True)
        skill.verify_test(qa, test2, True)
        
        assert skill.is_merge_ready(qa)
    
    def test_not_merge_ready_with_failures(self):
        """RED: Not merge ready with failures."""
        skill = UltraQASkill()
        qa = skill.create_qa_session("QA", "Desc")
        test1 = skill.add_test_case(qa, "Test1", "Desc")
        test2 = skill.add_test_case(qa, "Test2", "Desc")
        
        skill.verify_test(qa, test1, True)
        skill.verify_test(qa, test2, False)
        
        assert not skill.is_merge_ready(qa)


class TestCompletion:
    """Test QA completion."""
    
    def test_mark_qa_complete(self):
        """RED: Can mark QA as complete."""
        skill = UltraQASkill()
        qa = skill.create_qa_session("QA", "Desc")
        test = skill.add_test_case(qa, "Test", "Desc")
        
        skill.verify_test(qa, test, True)
        skill.mark_qa_complete(qa)
        
        assert qa.status == QALoopStatus.COMPLETED
        assert qa.merge_ready


class TestReporting:
    """Test reporting."""
    
    def test_generate_report(self):
        """RED: Can generate report."""
        skill = UltraQASkill()
        qa = skill.create_qa_session("QA", "Desc")
        test1 = skill.add_test_case(qa, "Test1", "Desc")
        test2 = skill.add_test_case(qa, "Test2", "Desc")
        
        skill.verify_test(qa, test1, True)
        skill.verify_test(qa, test2, True)
        skill.mark_qa_complete(qa)
        
        report = skill.generate_report(qa)
        
        assert report.total_tests == 2
        assert report.passed_tests == 2
        assert report.merge_ready
