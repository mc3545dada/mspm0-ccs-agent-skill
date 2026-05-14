# Claude Code Instructions for MSPM0 CCS Projects

This repository contains rules for TI MSPM0 projects using Code Composer Studio, CCS Theia, SysConfig, and DriverLib.

Use `SKILL.md`, this file, and the detailed docs under `docs/` before editing a project.

## Main Rules

- Treat `.syscfg` as the source of truth for hardware configuration.
- Do not manually edit generated SysConfig files such as `ti_msp_dl_config.c` or `ti_msp_dl_config.h`.
- Inspect generated headers for macro names and function names, but make configuration changes in `.syscfg`.
- Preserve device, package, SDK, and SysConfig metadata in `.syscfg`.
- Rebuild or run SysConfig CLI after `.syscfg` changes.
- Ask before changing the target chip, package, board, SDK, compiler, or CCS version.

## Editing Flow

When asked to add or change GPIO, UART, PWM, I2C, SPI, ADC, Timer, interrupts, or clock setup:

1. Read the `.syscfg` file.
2. Read generated `ti_msp_dl_config.h` to understand existing names.
3. Modify `.syscfg` with minimal changes.
4. Update application code to use the generated DriverLib macros.
5. Run available validation, or tell the user exactly what build step remains.

## Important Naming Rule

Do not guess the generated init function name. Some MSPM0 projects use:

```c
SYSCFG_DL_init();
```

Use the spelling declared in `ti_msp_dl_config.h`.

## Docs To Read When Needed

- `docs/syscfg_rules.md` for `.syscfg` handling
- `docs/ccs_project_rules.md` for project layout and generated files
- `docs/driverlib_rules.md` for DriverLib and interrupt patterns
- `docs/common_mistakes.md` for known agent failure modes
- `docs/cli_validation.md` for SysConfig CLI, gmake, and DSLite/J-Link validation

When this repository is available, run `python tools/check_syscfg.py <project-dir>` before or after `.syscfg` edits to catch metadata, generated-file, assigned-pin, and init-function issues.
