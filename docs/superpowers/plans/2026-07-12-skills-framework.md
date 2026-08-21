# Core Skills Framework Implementation Plan

> This plan covers the generic Python registry only. User-authored agent skills
> live in `gowork/<skill-name>/SKILL.md` directories and are deployed separately.

**Goal:** Provide a small, tested Python framework for registering, discovering,
validating, and invoking Python-native skills without coupling it to particular
user skills.

**Architecture:** `core/` owns the base interface, result type, central registry,
and registration decorator. `gowork/` is also the source tree for filesystem-based
agent skills, so its package initializer must not import those directories.

**Tech stack:** Python 3.13+, pytest, dataclasses, typing.

## Constraints

- Keep the core dependency-free.
- Develop framework behavior test-first.
- Do not register user skills as an import side effect of `gowork`.
- Keep filesystem-based agent skills self-contained in their own directories.

## Task 1: Project configuration

Maintain `pyproject.toml` with Python 3.13+ metadata, setuptools package discovery,
and `tests/` as the pytest test path.

Validation:

```bash
python3 -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb'))"
```

## Task 2: Base interface and result type

Maintain `core/skill.py` with:

- `SkillResult(success, data, error)`;
- a `Skill` base class with `execute()` and `validate()`;
- explicit failure behavior for unimplemented execution.

Cover success, failure, default values, validation, and abstract execution behavior
in `tests/test_skill.py`.

## Task 3: Registry

Maintain `core/registry.py` with deterministic registration, lookup, listing,
validation, and invocation behavior. Reject duplicate names and return a clear
failure result for unknown or invalid skills.

Cover the public behavior in `tests/test_registry.py`.

## Task 4: Registration decorator

Maintain `core/register.py` so decorated Python-native skill classes register an
instance with the selected registry. Test direct and parameterized decorator use in
`tests/test_register.py`.

## Task 5: Package APIs

`core/__init__.py` exports the supported framework API. `gowork/__init__.py` remains
import-safe and does not import filesystem-based agent skills.

Validation:

```bash
python3 -c "from core import Registry, Skill, SkillResult, register, registry; import gowork"
```

## Task 6: Final verification

Run the complete framework suite and verify package imports:

```bash
python3 -m pytest -q
python3 -c "import core, gowork"
git diff --check
```

The change is complete only when all commands pass and documentation contains no
references to removed Python skill implementations.
