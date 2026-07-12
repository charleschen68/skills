from __future__ import annotations

from typing import Any

from core.skill import Skill, SkillResult

# Module-level singleton
_registry: Registry | None = None


class Registry:
    """Central registry for skills.

    Collects Skill instances and provides discovery and invocation.
    Uses singleton pattern via __new__.
    """

    _instance: Registry | None = None

    def __new__(cls) -> "Registry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_skills"):
            self._skills: dict[str, Skill] = {}

    def register(self, skill: Skill) -> None:
        """Register a skill instance."""
        self._skills[skill.name] = skill

    def get(self, name: str) -> Skill | None:
        """Get a skill by name."""
        return self._skills.get(name)

    def get_all(self) -> list[Skill]:
        """Get all registered skills."""
        return list(self._skills.values())

    def invoke(self, name: str, *args: Any, **kwargs: Any) -> SkillResult:
        """Invoke a skill by name."""
        skill = self._skills.get(name)
        if skill is None:
            return SkillResult(
                success=False,
                data=None,
                error=f"Skill '{name}' not found",
            )
        if not skill.validate():
            return SkillResult(
                success=False,
                data=None,
                error=f"Skill '{name}' validation failed",
            )
        try:
            return skill.execute(*args, **kwargs)
        except Exception as exc:
            return SkillResult(
                success=False,
                data=None,
                error=str(exc),
            )

    def validate(self, name: str) -> bool:
        """Validate a skill by name."""
        skill = self._skills.get(name)
        if skill is None:
            return False
        return skill.validate()


# Module-level singleton accessor
def registry() -> Registry:
    """Get or create the singleton registry."""
    global _registry
    if _registry is None:
        _registry = Registry()
    return _registry
