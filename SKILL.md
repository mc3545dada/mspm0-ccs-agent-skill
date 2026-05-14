---
name: mspm0-ccs-agent-skill
description: Tool-neutral CLI agent rules for TI MSPM0 development with Code Composer Studio, CCS Theia, SysConfig, and DriverLib. Use when an agent needs to inspect or modify MSPM0 CCS projects, edit .syscfg configuration, avoid generated SysConfig files, use DriverLib APIs, validate SysConfig output, or work on NUEDC-style MSPM0 embedded firmware.
---

# MSPM0 CCS Agent Skill

Use this skill when working on TI MSPM0 firmware projects that use CCS, CCS Theia, SysConfig, and DriverLib.

This skill is for Claude Code, OpenCode, OpenClaw, Continue, Cursor, Codex, and other skill-aware CLI or editor agents. It is not Codex-specific.

## First Steps

1. Locate the project `.syscfg` file.
2. Read the `.syscfg` metadata: device, package, SDK product, and SysConfig tool version.
3. Inspect generated `ti_msp_dl_config.h` for generated names, macros, IRQ names, and init function spelling.
4. Read the relevant docs under `docs/` before changing hardware configuration.
5. Make hardware configuration changes in `.syscfg`, not generated files.
6. Rebuild or run SysConfig CLI after `.syscfg` changes.

## Never Do This

- Do not manually edit `Debug/ti_msp_dl_config.c` or `Debug/ti_msp_dl_config.h`.
- Do not delete `.syscfg` metadata such as `@cliArgs`, `@v2CliArgs`, `@versions`, `--device`, `--package`, or `--product`.
- Do not guess pinmux validity from a package pin alone.
- Do not guess whether the generated init function is `SYSCFG_DL_init()` or `SYSCFG_DL_Init()`.
- Do not migrate device, package, board, SDK, compiler, or CCS version without asking.

## Read These References

- Use `docs/syscfg_rules.md` for safe `.syscfg` edits.
- Use `docs/ccs_project_rules.md` for CCS project layout and generated files.
- Use `docs/driverlib_rules.md` for DriverLib initialization, ISR, and API rules.
- Use `docs/common_mistakes.md` before finalizing changes.
- Use `docs/validated_workflow.md` for the verified Tianmengxing MSPM0G3507 PB22 LED workflow.
- Use `docs/cli_validation.md` for the SysConfig CLI -> gmake -> DSLite/J-Link command chain.
- Use `docs/clock_tree_rules.md` before changing CPUCLK, SYSPLL, HFXT, MFCLK, UART clocks, or delay-cycle assumptions.

## Tools

Run `python tools/check_syscfg.py <project-dir>` when this repository is available and you need a quick static check of a CCS project. The tool checks `.syscfg` metadata, generated SysConfig files, assigned pins, init-function spelling, and prints validation command hints when it can infer them from the project.

## Expected Validation

After modifying `.syscfg`, run the generated SysConfig CLI command if available, or rebuild the CCS project. If no local toolchain is available, clearly report that validation is pending and tell the user which command or IDE build action to run.

For automated DSLite flashing, prefer a system reset after programming: `-r 2 -u`. Manual flashing may require pressing the board reset button after programming, especially after clock-tree changes.
