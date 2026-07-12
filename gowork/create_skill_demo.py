# gowork/create_skill_demo.py
from __future__ import annotations

from core.register import register
from core.skill import Skill, SkillResult


@register()
class CreateSkillDemoSkill(Skill):
    """Generate a new skill template for agent imitation."""

    name = "create_skill_demo"
    description = "Generate a new skill template file"

    def execute(
        self,
        name: str,
        description: str = "",
    ) -> SkillResult:
        return SkillResult(success=True, data=None, error=None)

    def validate(self) -> bool:
        return True
