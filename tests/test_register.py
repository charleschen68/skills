# tests/test_register.py
import pytest
from core.skill import Skill, SkillResult
from core.registry import Registry
from core.register import register


class TestRegisterDecorator:
    def test_decorator_registers_class(self):
        registry = Registry()

        @register(registry)
        class MySkill(Skill):
            name = "my_skill"
            description = "test"

            def execute(self, *args, **kwargs) -> SkillResult:
                return SkillResult(success=True, data=None, error=None)

        assert registry.get("my_skill") is not None

    def test_decorator_returns_class(self):
        registry = Registry()

        @register(registry)
        class MySkill(Skill):
            name = "my_skill2"
            description = "test"

            def execute(self, *args, **kwargs) -> SkillResult:
                return SkillResult(success=True, data=None, error=None)

        assert MySkill is not None

    def test_decorator_with_instance(self):
        registry = Registry()

        @register(registry)
        class MySkill(Skill):
            name = "my_skill3"
            description = "test"

            def execute(self, *args, **kwargs) -> SkillResult:
                return SkillResult(success=True, data=None, error=None)

        skill = registry.get("my_skill3")
        assert isinstance(skill, MySkill)
