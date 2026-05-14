# Claude Code Repository Notes

This repository contains an installable skill for MSPM0 CCS / CCS Theia projects.

Use this file only when developing this repository. The actual skill to install is:

```text
skills/mspm0-ccs/
```

For Claude Code users, copy that directory to:

```text
~/.claude/skills/mspm0-ccs/
```

## Editing Rules

- Keep `skills/mspm0-ccs/SKILL.md` concise.
- Keep detailed docs in `skills/mspm0-ccs/references/`.
- Keep scripts in `skills/mspm0-ccs/scripts/`.
- Keep snippets in `skills/mspm0-ccs/assets/snippets/`.
- Keep examples in `skills/mspm0-ccs/examples/`.
- Do not treat root `AGENTS.md` or root `CLAUDE.md` as installable MSPM0 project rules.

## Test Commands

```text
python -m py_compile skills/mspm0-ccs/scripts/check_syscfg.py skills/mspm0-ccs/scripts/serial_console.py
python skills/mspm0-ccs/scripts/check_syscfg.py .
```
