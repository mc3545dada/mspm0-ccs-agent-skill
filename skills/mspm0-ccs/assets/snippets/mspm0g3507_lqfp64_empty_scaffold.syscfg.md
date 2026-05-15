# MSPM0G3507 LQFP-64 Empty SysConfig Scaffold

Use this as a reference scaffold for MSPM0G3507 LQFP-64 projects when the user does not yet have a richer `.syscfg`.

Prefer the user's existing `.syscfg`, a local MSPM0 SDK example, or a SysConfig GUI-generated file over this hardcoded scaffold.

```js
/**
 * These arguments were validated with MSPM0 SDK 2.10.00.04 and SysConfig 1.26.2.
 * Do not copy them to a different device, package, SDK, or board without validation.
 *
 * @cliArgs --device "MSPM0G350X" --part "Default" --package "LQFP-64(PM)" --product "mspm0_sdk@2.10.00.04"
 * @v2CliArgs --device "MSPM0G3507" --package "LQFP-64(PM)" --product "mspm0_sdk@2.10.00.04"
 * @versions {"tool":"1.26.2+4477"}
 */

const SYSCTL = scripting.addModule("/ti/driverlib/SYSCTL");
const Board  = scripting.addModule("/ti/driverlib/Board", {}, false);

SYSCTL.forceDefaultClkConfig = true;

Board.peripheral.$suggestSolution          = "DEBUGSS";
Board.peripheral.swclkPin.$suggestSolution = "PA20";
Board.peripheral.swdioPin.$suggestSolution = "PA19";
SYSCTL.peripheral.$suggestSolution         = "SYSCTL";
```

For Tianmengxing PB22 LED or UART0 patterns, prefer the full examples under:

```text
examples/led_blink/
examples/uart_blocking_tx/
```
