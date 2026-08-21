# Skills

A collection of Claude Code skills for automated task execution and skill management.

## Structure

- `core/` — Core skill framework (registry, registration, base classes)
- `gowork/` — Skill implementations and utilities, including Claude Code agent skills as `gowork/<skill-name>/SKILL.md` (e.g. `gowork/blog-publish/`). Deploy an agent skill by copying its directory to `~/.claude/skills/`.
- `tests/` — Test files
- `docs/` — Documentation

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
