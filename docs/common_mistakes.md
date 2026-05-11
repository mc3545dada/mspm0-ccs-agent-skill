# Common MSPM0 Agent Mistakes

Use this checklist before finalizing changes to an MSPM0 CCS project.

## Mistake 1: Editing Generated Files

Wrong:

```text
Debug/ti_msp_dl_config.c
Debug/ti_msp_dl_config.h
```

Correct:

Edit `.syscfg`, then rebuild or run SysConfig.

Generated files may be inspected, not patched by hand.

## Mistake 2: Removing SysConfig Metadata

Do not remove:

```text
@cliArgs
@v2CliArgs
@versions
--device
--package
--product
```

Without this metadata, SysConfig may reopen or regenerate with the wrong assumptions.

## Mistake 3: Guessing Init Function Capitalization

Do not assume:

```c
SYSCFG_DL_Init();
```

Many MSPM0 projects generate:

```c
SYSCFG_DL_init();
```

Inspect `ti_msp_dl_config.h` and use the local declaration.

## Mistake 4: Assuming Any Pin Can Do Any Function

MSPM0 package pins and peripheral functions are constrained. A pin being present on the chip does not mean it can be used for a selected UART, PWM, I2C, ADC, or timer channel.

Use SysConfig, `$assign`, `$suggestSolution`, and generated headers to verify pinmux.

## Mistake 5: Renaming Generated Instances Casually

Changing a SysConfig `$name` can change generated macros and break application code.

Before renaming, search the project for the old generated names.

## Mistake 6: Mixing SysConfig With Manual Peripheral Setup

If SysConfig configures a peripheral, do not reinitialize the same peripheral by hand in application code unless there is a clear reason.

Use application code for runtime actions such as:

- Start or stop a timer
- Set PWM duty cycle
- Read ADC result
- Send UART data
- Toggle GPIO

## Mistake 7: Long Work Inside ISR

Avoid:

- Long delays
- Complex parsing
- OLED drawing
- Blocking UART prints
- Slow sensor transactions

Inside an ISR, record state, clear flags, and return.

## Mistake 8: Editing CCS Metadata Without Need

Avoid unnecessary edits to:

```text
.cproject
.ccsproject
.project
.settings/
targetConfigs/
```

These files can change compiler, SDK, debugger, and build behavior.

## Mistake 9: Forgetting To Rebuild

After `.syscfg` changes, generated files are stale until SysConfig runs again.

Always rebuild or run SysConfig CLI before trusting generated macros.

## Mistake 10: Treating Hardware Tests As Available

If no MSPM0 board is connected, do not claim that flashing, UART, motor, servo, or sensor behavior was verified.

Report source-level and build-level validation separately from hardware validation.

