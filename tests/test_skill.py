# tests/test_skill.py
import pytest
from core.skill import Skill, SkillResult


class TestSkillResult:
    def test_success_result(self):
        result = SkillResult(success=True, data="hello", error=None)
        assert result.success is True
        assert result.data == "hello"
        assert result.error is None

    def test_failure_result(self):
        result = SkillResult(success=False, data=None, error="something broke")
        assert result.success is False
        assert result.error == "something broke"

    def test_default_error_is_none(self):
        result = SkillResult(success=True, data=42)
        assert result.error is None


class DummySkill(Skill):
    name = "dummy"
    description = "a dummy skill"

    def execute(self, *args, **kwargs) -> SkillResult:
        return SkillResult(success=True, data="executed", error=None)


class TestSkill:
    def test_default_name_is_class_name(self):
        class MySkill(Skill):
            def execute(self, *args, **kwargs) -> SkillResult:
                return SkillResult(success=True, data=None, error=None)

        skill = MySkill()
        assert skill.name == "MySkill"

    def test_execute_returns_skill_result(self):
        skill = DummySkill()
        result = skill.execute()
        assert isinstance(result, SkillResult)
        assert result.success is True

    def test_validate_returns_true_by_default(self):
        skill = DummySkill()
        assert skill.validate() is True
