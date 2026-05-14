@AGENTS.md

# Claude Code Notes

`AGENTS.md` is the canonical source for developing this repository.

Claude Code users should install only:

```text
skills/mspm0-ccs/
```

Typical install path:

```text
~/.claude/skills/mspm0-ccs/
```

Keep this file as a thin compatibility entrypoint. Put shared repository rules in `AGENTS.md`, and put actual MSPM0 skill behavior in `skills/mspm0-ccs/SKILL.md`.
