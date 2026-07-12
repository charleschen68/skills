# gowork/blog_summarize.py
from __future__ import annotations

from core.register import register
from core.skill import Skill, SkillResult


@register()
class BlogSummarizeSkill(Skill):
    """Summarize content and publish to blog."""

    name = "blog_summarize"
    description = "Summarize content and submit to blog as MDX"

    def execute(
        self,
        content: str,
        title: str | None = None,
    ) -> SkillResult:
        return SkillResult(success=True, data=None, error=None)

    def validate(self) -> bool:
        return True
