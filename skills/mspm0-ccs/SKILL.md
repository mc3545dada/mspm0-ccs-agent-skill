---
name: mspm0-ccs
description: Tool-neutral CLI agent rules for TI MSPM0 development with Code Composer Studio, CCS Theia, SysConfig, and DriverLib. Use when an agent needs to inspect or modify MSPM0 CCS projects, edit .syscfg configuration, avoid generated SysConfig files, use DriverLib APIs, validate SysConfig output, or work on NUEDC-style MSPM0 embedded firmware.
---

# MSPM0 CCS Agent Skill

Use this skill when working on TI MSPM0 firmware projects that use CCS, CCS Theia, SysConfig, and DriverLib.

This skill is for Claude Code, OpenCode, OpenClaw, Continue, Cursor, Codex, and other skill-aware CLI or editor agents. It is not Codex-specific.

## First Steps

1. Locate the project `.syscfg` file.
2. Read the `.syscfg` metadata: device, package, SDK product, and SysConfig tool version.
3. Inspect generated `ti_msp_dl_config.h` for generated names, macros, IRQ names, and init function spelling.
4. Inspect existing module instances, such as GPIO, UART, PWM, I2C, ADC, TIMER, SYSCTL, DMA, and interrupts.
5. If the needed SysConfig field or enum is unclear, read `references/syscfg_schema_sources.md` and inspect local SDK examples or `.meta/*.syscfg.js` before editing.
6. Read the relevant docs under `references/` before changing hardware configuration.
7. Modify the smallest relevant `.syscfg` section and follow the local naming style.
8. Update application code to use generated DriverLib macros.
9. Rebuild or run SysConfig CLI after `.syscfg` changes.

## Core Rules

1. Treat `.syscfg` as the source of truth for pinmux, peripherals, clocks, and generated initialization.
2. For GPIO, UART, PWM, I2C, SPI, ADC, Timer, clock, DMA, and interrupt setup, prefer changing `.syscfg` rather than hand-written register or generated-code edits.
3. Read `ti_msp_dl_config.h` to confirm macro names, IRQ names, instance names, and init function spelling.
4. Application code must call the generated SysConfig init function before using generated peripherals.
5. If a pin or peripheral conflict occurs, fix `.syscfg` first.
6. Do not assume a pin is valid only because it exists on the package. Verify pinmux through SysConfig or generated output.
7. Follow the existing project naming style for modules, pins, macros, and interrupt handlers.
8. Ask before changing device, package, board, SDK, compiler, CCS version, or debug probe.
9. Do not freehand new SysConfig fields. If unsure, search the local MSPM0 SDK examples and module metadata first.
10. Preserve unrelated user code, comments, license headers, and `.syscfg` settings. If a requested feature requires removing or rewriting existing project logic, call that out before making the change when possible.

## Safe Edit Scope

Usually safe to edit:

- Application source files such as `main.c`, `empty.c`, `app/*.c`, `bsp/*.c`, and matching headers.
- `.syscfg`.
- Project documentation.
- User-owned board support files.

Keep edits focused on the requested behavior. If a file already has a TI or user copyright header, leave it in place unless the user explicitly asks for cleanup. If a file has no header, do not add one just for style.

Avoid hand-editing generated or build output files:

- `Debug/ti_msp_dl_config.c`
- `Debug/ti_msp_dl_config.h`
- `Release/ti_msp_dl_config.c`
- `Release/ti_msp_dl_config.h`
- `Debug/device.opt`
- `Debug/device_linker.cmd`
- `Debug/device.cmd.genlibs`
- `Debug/*.mk`
- Object files, maps, `.out`, and other build outputs.

Generated files may be inspected, but changes should be made in source files or `.syscfg`.

## DriverLib Rules

- Prefer `DL_GPIO_*`, `DL_UART_*`, `DL_Timer*`, `DL_I2C_*`, and `DL_ADC12_*` APIs.
- Keep interrupt handlers short.
- Clear interrupt flags correctly.
- Use `volatile` for variables shared with interrupt handlers.
- Avoid long blocking delays inside high-frequency interrupts.
- Do not mix register-level configuration with SysConfig-generated setup unless the user explicitly requests it and the reason is documented.

## Validation Workflow

1. Run `python scripts/check_syscfg.py <project-dir>` when this skill is available.
2. After `.syscfg` changes, look for the CCS-generated SysConfig command in `Debug/subdir_rules.mk`.
3. Run SysConfig CLI directly or rebuild through the CCS-generated makefile.
4. If CLI validation is unavailable, ask the user to rebuild in CCS and paste SysConfig or compiler errors.
5. If flashing, confirm `targetConfigs/*.ccxml` matches the physical debug probe.
6. For automated DSLite flashing, prefer `-r 2 -u` so the target receives a System Reset after programming.

For manual flashing, press the board reset button after programming if the first run appears to use the wrong clock speed.

## Never Do This

- Do not manually edit `Debug/ti_msp_dl_config.c` or `Debug/ti_msp_dl_config.h`.
- Do not delete `.syscfg` metadata such as `@cliArgs`, `@v2CliArgs`, `@versions`, `--device`, `--package`, or `--product`.
- Do not guess pinmux validity from a package pin alone.
- Do not guess whether the generated init function is `SYSCFG_DL_init()` or `SYSCFG_DL_Init()`.
- Do not migrate device, package, board, SDK, compiler, CCS version, or debug probe without asking.
- Do not invent `.syscfg` field names, enum values, `@cliArgs`, `@v2CliArgs`, device, package, product, or version metadata.

## Reference Selection

- `references/syscfg_rules.md`: safe `.syscfg` edits.
- `references/ccs_project_rules.md`: CCS project layout and generated files.
- `references/driverlib_rules.md`: DriverLib initialization, ISR, and API rules.
- `references/common_mistakes.md`: known agent failure modes.
- `references/validated_workflow.md`: verified Tianmengxing MSPM0G3507 PB22 LED workflow.
- `references/cli_validation.md`: SysConfig CLI -> gmake -> DSLite/J-Link command chain.
- `references/clock_tree_rules.md`: CPUCLK, SYSPLL, HFXT, MFCLK, UART clocks, and `delay_cycles()` assumptions.
- `references/uart_blocking_tx.md`: verified UART0 blocking transmit smoke test before DMA or variable-length receive.
- `references/pwm_breath_led.md`: verified PB22 PWM breathing LED baseline, failed duty-cycle attempts, and CCS linker-file build gotcha.
- `references/syscfg_schema_sources.md`: how to use local MSPM0 SDK examples and `.meta/*.syscfg.js` instead of guessing `.syscfg` fields.

## Tools

Run `python scripts/check_syscfg.py <project-dir>` when this skill is available and you need a quick static check of a CCS project. The tool checks `.syscfg` metadata, generated SysConfig files, assigned pins, init-function spelling, and prints validation command hints when it can infer them from the project.

Run `python scripts/serial_console.py --list` to list PC serial ports. For the verified CH340 setup, use `python scripts/serial_console.py -p COM6 -b 115200 --timestamp --duration 10` after closing other serial tools such as VOFA+.

Run `python scripts/index_syscfg_examples.py <mspm0-sdk-root> --board LP_MSPM0G3507 --module UART` to index local TI SDK `.syscfg` examples and `source/ti/driverlib/.meta/*.syscfg.js` module metadata before authoring unfamiliar SysConfig fields.
