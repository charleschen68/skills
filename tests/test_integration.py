# tests/test_integration.py
import pytest
from core.registry import Registry
from core.skill import SkillResult
from gowork.blog_summarize import BlogSummarizeSkill
from gowork.create_skill_demo import CreateSkillDemoSkill


class TestIntegration:
    def test_registry_discovers_all_skills(self):
        """All skills are discoverable via registry."""
        registry = Registry()
        registry.register(BlogSummarizeSkill())
        registry.register(CreateSkillDemoSkill())

        all_skills = registry.get_all()
        assert len(all_skills) == 2
        names = {s.name for s in all_skills}
        assert "blog_summarize" in names
        assert "create_skill_demo" in names

    def test_blog_summarize_execute_returns_result(self):
        """BlogSummarizeSkill.execute returns a valid SkillResult."""
        registry = Registry()
        registry.register(BlogSummarizeSkill())

        result = registry.invoke("blog_summarize", content="test")
        assert isinstance(result, SkillResult)
        assert result.success is True

    def test_create_skill_demo_execute_returns_result(self):
        """CreateSkillDemoSkill.execute returns a valid SkillResult."""
        registry = Registry()
        registry.register(CreateSkillDemoSkill())

        result = registry.invoke("create_skill_demo", "TestSkill")
        assert isinstance(result, SkillResult)
        assert result.success is True

    def test_skill_validation_chain(self):
        """Skills validate correctly before invocation."""
        registry = Registry()
        blog = BlogSummarizeSkill()
        demo = CreateSkillDemoSkill()
        registry.register(blog)
        registry.register(demo)

        assert registry.validate("blog_summarize") is True
        assert registry.validate("create_skill_demo") is True
        assert registry.validate("nonexistent") is False
