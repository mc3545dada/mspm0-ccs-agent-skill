# SysConfig Rules for MSPM0

`.syscfg` is the editable SysConfig source file for many MSPM0 CCS projects. It is a text-based configuration script that describes devices, packages, pins, peripherals, clocks, and generated initialization output.

For MSPM0 agent work, `.syscfg` should be treated as the source of truth.

## Preserve Metadata

Do not remove or casually modify the header block containing fields like:

```text
@cliArgs
@v2CliArgs
@versions
--device
--package
--product
```

These fields let SysConfig reopen the project with the correct device, package, SDK product, and tool version assumptions.

Changing any of these can effectively migrate the project. Ask the user first.

## Common Structure

MSPM0 `.syscfg` files often include module imports and instances:

```js
const GPIO = scripting.addModule("/ti/driverlib/GPIO", {}, false);
const GPIO1 = GPIO.addInstance();
```

Instances then set names, ports, pins, clock settings, and generated configuration names. The validated Tianmengxing LED workflow uses:

```js
GPIO1.$name = "LED";
GPIO1.port = "PORTB";
GPIO1.associatedPins[0].$name = "PIN_22";
GPIO1.associatedPins[0].assignedPin = "22";
```

## Editing Strategy

When adding or changing a peripheral:

1. Find an existing similar instance in the same `.syscfg`.
2. Copy the local style rather than inventing a new style.
3. Change only the required fields.
4. Keep instance names stable unless the user asked for a rename.
5. Assign peripheral instances and pins carefully.
6. Preserve `$suggestSolution` lines unless you understand the solver impact.
7. Run SysConfig or rebuild.
8. Fix SysConfig errors in `.syscfg`.

## Generated Files Are Outputs

Do not manually edit:

```text
Debug/ti_msp_dl_config.c
Debug/ti_msp_dl_config.h
Release/ti_msp_dl_config.c
Release/ti_msp_dl_config.h
```

These files are regenerated and may be overwritten.

It is fine to read generated headers to learn macro names such as:

```c
LED_PORT
LED_PIN_22_PIN
SYSCFG_DL_init
```

But configuration changes belong in `.syscfg`.

## Pinmux Rules

- Do not assume all package pins can serve all peripheral functions.
- Use SysConfig assignments or generated output to confirm the selected pin function.
- Watch for conflicts between GPIO use and peripheral use.
- Be careful with debug pins such as SWDIO and SWCLK.
- Ask before changing board-level pin maps from examples or development boards.

## Validation

A CCS project may generate a build rule similar to:

```text
sysconfig_cli --script project.syscfg -o . -s path/to/mspm0_sdk/.metadata/product.json --compiler ticlang
```

Run this through the project build when possible. If direct CLI use is not configured, rebuild in CCS.

## Agent Checklist

Before finalizing a `.syscfg` change:

- Confirm the metadata block is still present.
- Confirm only intended instances changed.
- Confirm no generated files were manually edited.
- Confirm application code uses generated names from `ti_msp_dl_config.h`.
- Confirm SysConfig or CCS build has been run, or clearly report that it still needs to be run.
