# tests/test_blog_summarize.py
import pytest
from gowork.blog_summarize import BlogSummarizeSkill
from core.skill import SkillResult


class TestBlogSummarizeSkill:
    def test_skill_name(self):
        skill = BlogSummarizeSkill()
        assert skill.name == "blog_summarize"

    def test_skill_description(self):
        skill = BlogSummarizeSkill()
        assert "blog" in skill.description.lower()

    def test_execute_with_content(self):
        skill = BlogSummarizeSkill()
        content = "This is a test article about AI development."
        result = skill.execute(content)
        assert isinstance(result, SkillResult)

    def test_execute_with_title(self):
        skill = BlogSummarizeSkill()
        content = "Test content"
        result = skill.execute(content, title="My Article")
        assert isinstance(result, SkillResult)

    def test_execute_with_empty_content(self):
        skill = BlogSummarizeSkill()
        result = skill.execute("")
        assert isinstance(result, SkillResult)
        assert result.success is True

    def test_validate_returns_true(self):
        skill = BlogSummarizeSkill()
        assert skill.validate() is True
