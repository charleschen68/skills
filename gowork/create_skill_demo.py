# gowork/create_skill_demo.py
from __future__ import annotations

import os

from core.register import register
from core.skill import Skill, SkillResult


@register()
class CreateSkillDemoSkill(Skill):
    """Generate a new skill template for agent imitation.

    Creates a new skill file in gowork/ with @register() decorator
    and standard Skill base class implementation.
    """

    name = "create_skill_demo"
    description = "Generate a new skill template file"

    def execute(
        self,
        name: str,
        description: str = "",
    ) -> SkillResult:
        """Execute skill demo generation.

        Args:
            name: Name of the new skill (used for class name and filename).
            description: Description of the new skill.

        Returns:
            SkillResult with the generated file path.
        """
        try:
            gowork_dir = os.path.join(os.path.dirname(__file__))
            os.makedirs(gowork_dir, exist_ok=True)

            filename = name.lower() + ".py"
            filepath = os.path.join(gowork_dir, filename)

            template = self._generate_template(name, description)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(template)

            return SkillResult(
                success=True,
                data={"filepath": filepath, "class_name": name},
                error=None,
            )
        except Exception as exc:
            return SkillResult(
                success=False,
                data=None,
                error=str(exc),
            )

    def _generate_template(self, name: str, description: str) -> str:
        """Generate a skill template string."""
        return (
            f'from __future__ import annotations\n'
            f'\n'
            f'from core.register import register\n'
            f'from core.skill import Skill, SkillResult\n'
            f'\n'
            f'\n'
            f'@register()\n'
            f'class {name}(Skill):\n'
            f'    """{description}."""\n'
            f'\n'
            f'    name = "{name.lower()}"\n'
            f'    description = "{description}"\n'
            f'\n'
            f'    def execute(self, *args, **kwargs) -> SkillResult:\n'
            f'        """Execute the skill.\n'
            f'\n'
            f'        TODO: Implement your skill logic here.\n'
            f'        Use first-person voice for findings and suggestions.\n'
            f'        """\n'
            f'\n'
            f'        # Example:\n'
            f'        # result = process(some_input)\n'
            f'        # return SkillResult(success=True, data=result)\n'
            f'\n'
            f'        return SkillResult(\n'
            f'            success=True,\n'
            f'            data=None,\n'
            f'            error=None,\n'
            f'        )\n'
            f'\n'
            f'    def validate(self) -> bool:\n'
            f'        """Pre-execution validation."""\n'
            f'        return True\n'
        )

    def validate(self) -> bool:
        """Validate skill prerequisites."""
        return True
