# Validated Workflow: Tianmengxing PB22 LED

This document records a real hardware validation of the project rules on a LCKFB Tianmengxing MSPM0G3507 board.

## Validation Summary

Result: passed.

Validated on:

- Board: LCKFB Tianmengxing MSPM0G3507
- IDE: CCS / CCS Theia
- SDK: MSPM0 SDK 2.10.00.04
- SysConfig: 1.26.2
- Compiler: TI Arm Clang 4.0.3 LTS
- Debug probe: J-Link, through UniFlash / DSLite
- Test peripheral: onboard LED on PB22

Confirmed workflow:

```text
edit empty.syscfg
-> run SysConfig
-> generate ti_msp_dl_config.c / ti_msp_dl_config.h
-> build with CCS generated makefile
-> flash with DSLite through J-Link
-> board LED blinks
```

## What Was Verified

This validation confirms that an agent can safely modify a real MSPM0 CCS project by editing `.syscfg` as text.

Specifically:

- `.syscfg` can be changed by an agent without using the GUI.
- SysConfig CLI accepts the edited `.syscfg`.
- Generated files include the expected LED macros:

```c
LED_PORT
LED_PIN_22_PIN
SYSCFG_DL_init()
```

- CCS generated makefiles can rebuild the project after the `.syscfg` edit.
- UniFlash / DSLite can flash the generated `.out` file through J-Link.
- The physical board behavior matches the source change.

## SysConfig Pattern

The validated `.syscfg` GPIO pattern:

```js
const GPIO   = scripting.addModule("/ti/driverlib/GPIO", {}, false);
const GPIO1  = GPIO.addInstance();
const SYSCTL = scripting.addModule("/ti/driverlib/SYSCTL");

GPIO1.$name                         = "LED";
GPIO1.port                          = "PORTB";
GPIO1.associatedPins[0].$name       = "PIN_22";
GPIO1.associatedPins[0].assignedPin = "22";

const Board = scripting.addModule("/ti/driverlib/Board", {}, false);

SYSCTL.forceDefaultClkConfig = true;

GPIO1.associatedPins[0].pin.$suggestSolution = "PB22";
Board.peripheral.$suggestSolution            = "DEBUGSS";
Board.peripheral.swclkPin.$suggestSolution   = "PA20";
Board.peripheral.swdioPin.$suggestSolution   = "PA19";
SYSCTL.peripheral.$suggestSolution           = "SYSCTL";
```

## Application Pattern

The validated application pattern:

```c
#include "ti_msp_dl_config.h"

int main(void)
{
    SYSCFG_DL_init();

    while (1)
    {
        DL_GPIO_clearPins(LED_PORT, LED_PIN_22_PIN);
        delay_cycles(32000000);
        DL_GPIO_setPins(LED_PORT, LED_PIN_22_PIN);
        delay_cycles(32000000);
    }
}
```

Use the generated init function spelling from the local project. In this validated project, it is `SYSCFG_DL_init()`.

## Commands Used

SysConfig CLI validation:

```powershell
C:\ti\sysconfig_1.26.2\sysconfig_cli.bat `
  --script C:\Users\3545\workspace_ccstheia\26testproject1\empty.syscfg `
  --product C:\ti\mspm0_sdk_2_10_00_04\.metadata\product.json `
  --compiler ticlang `
  --output <temp-output-dir>
```

Build with CCS generated makefile:

```powershell
C:\ti\ccs2020\ccs\utils\bin\gmake.exe `
  -C C:\Users\3545\workspace_ccstheia\26testproject1\Debug `
  clean all
```

List available debug cores:

```powershell
C:\ti\uniflash_9.2.0\dslite.bat `
  -c C:\Users\3545\workspace_ccstheia\26testproject1\targetConfigs\MSPM0G3507.ccxml `
  -N
```

Flash and run:

```powershell
C:\ti\uniflash_9.2.0\dslite.bat `
  -c C:\Users\3545\workspace_ccstheia\26testproject1\targetConfigs\MSPM0G3507.ccxml `
  -e `
  -u C:\Users\3545\workspace_ccstheia\26testproject1\Debug\26testproject1.out
```

Observed DSLite success output:

```text
Loading Program: ...\Debug\26testproject1.out
Setting PC to entry point.
Running...
Success
```

## Lessons For Agents

- Prefer a known-good board example when choosing pins. For Tianmengxing MSPM0G3507, the onboard LED uses PB22.
- Preserve SysConfig metadata and generated naming style.
- Read `ti_msp_dl_config.h` after generation instead of guessing macro names.
- Use generated makefiles when CCS server build commands are unavailable or version-dependent.
- List debug cores before flashing.
- Treat hardware observation as a separate validation layer after CLI success.

## Impact On This Project

This validation supports the core rules in this repository:

- `.syscfg` is the correct source of truth for hardware configuration.
- Generated `ti_msp_dl_config.*` files should be inspected, not hand-edited.
- CLI-based SysConfig, build, and flash workflows are practical for MSPM0 agent work.

