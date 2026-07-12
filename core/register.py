from __future__ import annotations

from typing import Any, Callable

from core.registry import Registry
from core.skill import Skill


def register(
    registry: Registry | None = None,
) -> Callable[[type[Skill]], type[Skill]]:
    """Decorator that registers a Skill class with the registry.

    Usage:
        @register()
        class MySkill(Skill):
            name = "my_skill"
            ...

        # Or with explicit registry:
        @register(my_registry)
        class MySkill(Skill):
            ...
    """
    def decorator(cls: type[Skill]) -> type[Skill]:
        instance = cls()
        if registry is not None:
            registry.register(instance)
        return cls

    return decorator
