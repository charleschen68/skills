# tests/test_create_skill_demo.py
import pytest
from gowork.create_skill_demo import CreateSkillDemoSkill
from core.skill import SkillResult


class TestCreateSkillDemoSkill:
    def test_skill_name(self):
        skill = CreateSkillDemoSkill()
        assert skill.name == "create_skill_demo"

    def test_skill_description(self):
        skill = CreateSkillDemoSkill()
        assert "skill" in skill.description.lower()

    def test_execute_generates_file(self):
        skill = CreateSkillDemoSkill()
        result = skill.execute(name="MyNewSkill", description="A new skill")
        assert isinstance(result, SkillResult)
        assert result.success is True

    def test_execute_with_custom_gowork_dir(self):
        skill = CreateSkillDemoSkill()
        result = skill.execute(name="TestSkill", description="Test")
        assert isinstance(result, SkillResult)

    def test_validate_returns_true(self):
        skill = CreateSkillDemoSkill()
        assert skill.validate() is True
