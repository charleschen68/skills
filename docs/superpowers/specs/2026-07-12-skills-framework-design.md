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
├── gowork/         # User skill directory
│   ├── __init__.py
│   ├── blog_summarize.py  # Skill 1: summarize content → blog
│   └── create_skill_demo.py  # Skill 2: generate new skill template
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

## Skill 1: BlogSummarizeSkill

### Trigger

Activated when user says "总结XX内容提交到blog" or skill is invoked directly.

### Content analysis (all conditional)

- **原因及背景** — included if present in content
- **个人思考** — included if content has relevant elements
  - 发现问题 / 解决 / 措施 / 量化 / 预防 / 架构升级
- **专业性发现** — always included, first-person voice (not AI voice)
- **总结** — always included, first-person voice
- **建议** — always included, first-person voice

### Output flow

1. Analyze content — include what's present, skip what's not
2. Generate `.mdx` file → `~/app/cocomoon/data/blog/`
3. Execute `npm run pub "文章标题"` in `~/app/cocomoon/`

### Output format

```mdx
---
title: '文章标题'
date: '2026-07-12'
tags: ['AI Builders Digest']
draft: false
summary: 'AI Builders Digest'
images: ['static/images/avatar_bak.png']
---
```

## Skill 2: CreateSkillDemoSkill

### Purpose

Generates a new skill template that agents can directly imitate when writing new skills.

### Behavior

1. Creates new skill file in `gowork/`
2. Includes `@register()` decorator
3. Includes standard Skill base class implementation
4. Example code comments for direct modification

### Relationship

- `BlogSummarizeSkill` — handles content summarization → .mdx → npm pub
- `CreateSkillDemoSkill` — generates new skill templates → agent imitation

## Error Handling

- `execute()` exceptions caught → `SkillResult(success=False, error=...)`
- File write failures return error info without raising
- `npm run pub` failures recorded but skill marked as success (publishing is auxiliary)
- New skills added by creating files in `gowork/` with `@register()` decorator

## Design Decisions

1. **Central registry** — simple, explicit, single source of truth, minimal abstraction
2. **Python** — aligns with Claude Code ecosystem
3. **Class-based** — explicit interfaces, clear structure
4. **Runtime registry** — skills register themselves on import
5. **No forced structure** — content analysis is flexible, not rigid
