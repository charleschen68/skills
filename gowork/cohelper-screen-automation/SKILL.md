---
name: cohelper-screen-automation
description: Operate and verify CoHelper's guarded local screen automation.
metadata:
  short-description: Safely operate CoHelper screen automation
---

# CoHelper Screen Automation

Operate the separately launched, local CoHelper screen-automation service. Use
the existing socket control surface; do not replace it with direct GUI tooling,
old scripts, shell actions, or arbitrary Python actions.

## When to use

Use this skill to start, inspect, arm, stop, acknowledge, resume, or acceptance-test
the CoHelper template monitor. Do not use it to change Dofi or Hermes itself,
to automate an unreviewed UI workflow, or to control a service not owned by the
current user.

## Authority boundaries

- Require a named group for start. Never use or emulate `start all`.
- The service must be launched manually from the macOS app that has both Screen
  Recording and Accessibility permission. It does not register login startup.
- Treat `accept` as click-capable and `auto666666` as click-and-type-capable.
  Do not arm either merely to test service availability. Start with `info-alarm`.
- Do not read, print, write, or move Keychain secrets. `auto666666` obtains its
  configured value by Keychain reference at execution time.
- Do not edit the user-private YAML or templates without explicit authorization.
  They belong under the user Application Support directory and must never be
  committed, copied into the repository, or sent to Telegram.
- A config change stops the service. Validate it and require a manual restart;
  do not silently restart or re-arm groups.

## Discover the installation

1. Confirm the current workspace is the CoHelper repository by locating
   `apps/automation_runtime.py` and `src/ai_drive/automation/`. If it is not,
   ask for the repository location rather than guessing.
2. Use `terminal` to set the repository root for this operation. The default
   config is `~/Library/Application Support/cohelper/automation/rules.yaml`.
3. Check the socket status before changing anything:

   ```sh
   cd "$COHELPER_ROOT"
   PYTHONPATH=src:. python3 -m apps.automation_control status
   ```

   If the socket is absent, report that the service is not running. Do not
   claim monitoring is active.

## Manual service lifecycle

Ask the human to run this in the same authorized Terminal session and leave it
open:

```sh
cd "$COHELPER_ROOT"
PYTHONPATH=src:. python3 -m apps.automation_runtime \
  --config "$HOME/Library/Application Support/cohelper/automation/rules.yaml"
```

It starts with every group disarmed. In a second terminal, control it only via:

```sh
cd "$COHELPER_ROOT"
PYTHONPATH=src:. python3 -m apps.automation_control status
PYTHONPATH=src:. python3 -m apps.automation_control start <group>
PYTHONPATH=src:. python3 -m apps.automation_control stop <group|all>
PYTHONPATH=src:. python3 -m apps.automation_control ack
PYTHONPATH=src:. python3 -m apps.automation_control emergency-stop
PYTHONPATH=src:. python3 -m apps.automation_control resume
```

After every control mutation, query `status` and report the exact armed or
suspended state. `resume` restores only ready state; it never re-arms a group.

## Safe acceptance sequence

1. Verify the service is `ready` and every group is `disarmed`.
2. Arm `info-alarm`. Show its template on the main display and confirm alert
   behavior. For latched sound, run `ack`; then `stop info-alarm` and confirm
   it is disarmed.
3. Arm `accept` only when the human is prepared for one guarded click. Confirm
   the template appears, a single action occurs, and it does not replay until
   two absent scans. Stop it after the test.
4. Test emergency stop by moving the pointer to the main-display top-left
   corner. Confirm `service: suspended` and all groups disarmed. Require
   `resume` before any future start.
5. Test `auto666666` only after the human explicitly confirms the Keychain
   reference is configured and accepts click/type/Enter behavior. Never expose
   the value in output or logs.

## Telegram control

Telegram controls are optional and must remain identity-bound to the configured
private chat. Use only the supported `/automation_status`, `/automation_start`,
`/automation_confirm`, `/automation_stop`, `/automation_ack`,
`/automation_emergency_stop`, and `/automation_resume` commands. A start needs
its one-time confirmation; stop and emergency stop must take effect immediately.
Do not accept forwarded commands or broaden chat/user access.

## Completion report

State separately: service/socket status, each armed group, whether the action
was live-tested, the result of emergency-stop verification, and any blocker
(permissions, missing config/template, missing Keychain reference, or Telegram
transport). Do not call the system running merely because its process exists.
