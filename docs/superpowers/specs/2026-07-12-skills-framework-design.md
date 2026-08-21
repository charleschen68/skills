---
title: "Skills Framework Design"
date: "2026-07-12"
tags: ["skills", "framework", "design"]
draft: false
---

# Skills Framework Design

## Overview

A Python skills framework for agent discovery and invocation. The project lives in `/Users/ad/app/skills/` — a greenfield project with a single initial commit.

## Architecture

```
skills/
├── core/           # Framework core
│   ├── __init__.py
│   ├── skill.py      # Skill base class + SkillResult
│   ├── registry.py   # Central registry (singleton)
│   └── register.py   # @register() decorator
├── gowork/         # Source directories for user-authored agent skills
│   ├── __init__.py
│   └── <skill-name>/
│       ├── SKILL.md
│       └── references/    # Optional supporting instructions
└── pyproject.toml
```

## Core Components

### `Skill` base class

- `name: str` — unique identifier
- `description: str` — what the skill does
- `execute(*args, **kwargs) -> SkillResult` — main execution
- `validate() -> bool` — pre-execution validation hook

### `Registry` class

- Singleton pattern, globally accessible
- Methods: `register()`, `get()`, `get_all()`, `invoke()`

### `@register()` decorator

- Auto-registers skill on import via `registry.register()`

### `SkillResult` dataclass

- `success: bool`
- `data: Any`
- `error: str | None`

### Agent workflow

1. `registry.get_all()` — discover available skills
2. `registry.get(name)` — get specific skill
3. `registry.invoke(name, ...)` — invoke skill

## Agent skill sources

User-authored agent skills live under `gowork/<skill-name>/`. Each skill has a
`SKILL.md` entrypoint and may add focused `references/`, `scripts/`, or `assets/`
when those resources materially improve the workflow. The complete directory is
copied to each applicable agent runtime during deployment.

The Python registry remains available for Python-native extensions, but the
`gowork` package does not import agent-skill directories.

## Error Handling

- Python-native `execute()` exceptions should return `SkillResult(success=False, error=...)`
- Agent skills define their own failure boundaries and stopping conditions in `SKILL.md`
- Deployment must copy the complete skill directory so supporting resources are not omitted

## Design Decisions

1. **Central registry** — simple, explicit, single source of truth, minimal abstraction
2. **Python core** — provides a small optional runtime for Python-native extensions
3. **Class-based** — explicit interfaces, clear structure
4. **Runtime registry** — skills register themselves on import
5. **Filesystem agent skills** — keep user-authored instructions portable across agent runtimes
