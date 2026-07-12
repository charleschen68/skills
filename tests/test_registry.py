# tests/test_registry.py
import pytest
from core.skill import Skill, SkillResult
from core.registry import Registry, registry


class DemoSkill(Skill):
    name = "demo"
    description = "a demo skill"

    def execute(self, *args, **kwargs) -> SkillResult:
        return SkillResult(success=True, data="demo result", error=None)


class TestRegistry:
    def test_singleton(self):
        r1 = Registry()
        r2 = registry()
        assert r1 is r2

    def test_register_adds_skill(self):
        r = Registry()
        skill = DemoSkill()
        r.register(skill)
        assert r.get("demo") is skill

    def test_get_returns_none_for_unknown(self):
        r = Registry()
        assert r.get("nonexistent") is None

    def test_get_all_returns_registered_skills(self):
        r = Registry()
        r.register(DemoSkill())
        all_skills = r.get_all()
        assert len(all_skills) == 1
        assert all_skills[0].name == "demo"

    def test_invoke_calls_execute(self):
        r = Registry()
        r.register(DemoSkill())
        result = r.invoke("demo")
        assert isinstance(result, SkillResult)
        assert result.success is True
        assert result.data == "demo result"

    def test_invoke_unknown_skill_returns_error(self):
        r = Registry()
        result = r.invoke("unknown")
        assert result.success is False
        assert "not found" in result.error.lower()

    def test_validate_checks_preconditions(self):
        r = Registry()
        skill = DemoSkill()
        r.register(skill)
        assert r.validate("demo") is True

    def test_validate_returns_false_for_unknown(self):
        r = Registry()
        assert r.validate("unknown") is False
