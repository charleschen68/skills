# Skills

A collection of Claude Code skills for automated task execution and skill management.

## Structure

- `core/` — Core skill framework (registry, registration, base classes)
- `gowork/` — Skill implementations and utilities
- `tests/` — Test files
- `docs/` — Documentation
- `<skill-name>/SKILL.md` — Claude Code agent skills, one top-level directory per skill (e.g. `blog-publish/`). Deploy by copying the directory to `~/.claude/skills/`.

## Features

- Skill registration and discovery
- Blog content summarization
- Dynamic skill generation

## Getting Started

```bash
# Install dependencies
pip install -e .

# Run tests
pytest
```
