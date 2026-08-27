---
name: cohelper-project
description: Develop, configure, validate, or operate the local-only macOS CoHelper assistant. Use for work in app/cohelper; not for unrelated macOS automation or Dofi/Hermes changes.
metadata:
  short-description: Work safely in the CoHelper project
---

# CoHelper Project

Use this skill for `/Users/ad/app/cohelper`, a macOS Apple-Silicon local AI
assistant. Treat it as a PyObjC/AppKit application with separately launched
local services, not as a generic web or cloud-agent project.

## Establish the current state

Before changing or claiming behavior, inspect `README.md`, `pyproject.toml`,
`config.example.yaml`, `docs/architecture.md`, `docs/security-model.md`, and
the relevant implementation and tests. Check `git status --short --branch`;
preserve unrelated work. The project can evolve independently of this skill,
so do not use this document as a substitute for current source.

For local development, install the dev extra and launch from the repository:

```sh
python3 -m pip install -e '.[dev]'
python3 -m pytest -q
python3 cohelper.py
```

The runtime configuration is
`~/Library/Application Support/cohelper/config.yaml`; copy
`config.example.yaml` there only when it does not already exist or the user
explicitly asks to replace it. Never commit that user configuration, automation
rules/templates, screenshots, logs, or Keychain material.

## Navigate by responsibility

- `cohelper_app.py` is the AppKit composition root and settings UI;
  `cohelper_core.py` owns configuration validation and shared orchestration.
- `apps/clipboard_helper/` handles clipboard translation and source-grounded
  QMD answers; it must preserve cancellation so stale work cannot overwrite a
  later clipboard item.
- `src/ai_drive/` holds reusable contracts and capabilities. Keep platform UI
  code in `apps/`; do not import or execute Dofi skills from CoHelper.
- `apps/overlay/` consumes bounded output events over a current-user Unix
  socket. It is output-only, never an action endpoint.
- `src/ai_drive/vision/` and `src/ai_drive/actions/` implement screenshot
  analysis and guarded one-time clicking. Read the security model before
  changing either.
- `apps/automation_runtime.py` is a separate declarative screen-monitor
  process. For lifecycle or live operation, load `cohelper-screen-automation`.
- `apps/telegram_bridge/` is a separate manual process, not a menu-bar thread
  and not a general remote-command interface.

## Preserve non-negotiable boundaries

- CoHelper is local-first. Visual and OCR endpoints must remain loopback;
  `privacy.allow_external_api` controls OpenAI-compatible use. Do not add a
  cloud fallback silently.
- A false feature flag must prevent its module, diagnostics, model calls, and
  QMD calls from starting. Keep dependency validation explicit (for example,
  knowledge answers require knowledge search).
- Credentials are macOS Keychain entries under service
  `com.charleschen68.cohelper`; never put secrets in YAML, source, command
  arguments, logs, test fixtures, or chat output.
- Screen recording, microphone, and Accessibility permissions belong to the
  launching Terminal/iTerm or packaged app. A sandbox or non-authorized agent
  cannot prove the real GUI runtime is permitted.
- Do not broaden visual actions into arbitrary shell, keyboard, drag,
  double-click, or blind-click execution. Preserve application/capability
  allowlists, fresh capture and desktop identity checks, one-time confirmation,
  and fail-closed behavior. `AXWebArea` must not impersonate a native allowed
  control.
- Telegram previews leave the Mac. Its supported click protocol is only
  `/click`, `/confirm <id>`, and `/cancel <id>`; identity checks and token
  expiry are security controls, not UI conveniences.

## Change and verify deliberately

Place logic behind the narrowest applicable feature or service boundary. Add
or update focused tests for safety-sensitive behavior, config validation,
cancellation, and failure paths. Run at least:

```sh
python3 -m pytest -q
python3 -m compileall -q apps src cohelper.py cohelper_app.py cohelper_core.py cohelper_setup.py
git diff --check
```

Use a real authorized macOS session for live checks involving AppKit, TCC,
audio, Quartz capture/input, global hotkeys, or the frontmost application.
Report those separately from unit-test results. For release artifacts, also
run the documented PyInstaller, code-signature, and DMG verification steps;
an ad-hoc-signed local app is not a notarized public distribution.

## Configuration and model operations

Inspect `config.example.yaml` and `Config._validate()` before changing config
schema. Use the in-app advanced configuration editor or validated config path
where possible. Do not download Ollama models, create/rebuild QMD indexes, or
alter a user's knowledge source unless they explicitly authorize it. A model
listed in config or returned by `ollama list` does not prove the service is
usable from the actual runtime.

When reporting, distinguish source-backed implementation, automated validation,
and live macOS acceptance. State any missing permission, service, model, or
human confirmation as a blocker rather than inferring success.
