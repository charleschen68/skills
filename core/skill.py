from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class SkillResult:
    success: bool
    data: Any = None
    error: str | None = None


class Skill:
    """Base class for all skills.

    Subclasses define name, description, and implement execute().
    """

    name: str = ""
    description: str = ""

    def __init__(self) -> None:
        if not self.name:
            self.name = self.__class__.__name__

    def execute(self, *args: Any, **kwargs: Any) -> SkillResult:
        """Execute the skill. Override in subclass."""
        raise NotImplementedError

    def validate(self) -> bool:
        """Pre-execution validation. Override for custom checks."""
        return True
