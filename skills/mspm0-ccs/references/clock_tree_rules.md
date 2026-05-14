# MSPM0 Clock Tree Rules

This document records the clock-tree behavior verified on the LCKFB Tianmengxing MSPM0G3507 board.

## Validated 80 MHz Pattern

Validated environment:

- Board: LCKFB Tianmengxing MSPM0G3507
- SDK: MSPM0 SDK 2.10.00.04
- SysConfig: 1.26.2
- Toolchain: CCS / CCS Theia with TI Arm Clang 4.0.3 LTS
- Flash probe: J-Link through UniFlash / DSLite

The validated clock tree uses:

- HFXT enabled on PA5 / PA6
- HFXT input frequency: 40 MHz
- SYSPLL selected as the high-speed clock source
- CPUCLK: 80 MHz
- ULPCLK divider: 2
- MFCLK gate enabled
- MFCLK: 4 MHz from SYSOSC_4M

This pattern was checked by blinking the PB22 LED with `delay_cycles(80000000)`. After a proper system reset, the observed blink period was about one second.

## SysConfig Pattern

Add clock-tree changes in `.syscfg`, not in generated `ti_msp_dl_config.c`.

```js
const divider9       = system.clockTree["UDIV"];
divider9.divideValue = 2;

const gate7  = system.clockTree["MFCLKGATE"];
gate7.enable = true;

const multiplier2         = system.clockTree["PLL_QDIV"];
multiplier2.multiplyValue = 4;

const mux4       = system.clockTree["EXHFMUX"];
mux4.inputSelect = "EXHFMUX_XTAL";

const mux8       = system.clockTree["HSCLKMUX"];
mux8.inputSelect = "HSCLKMUX_SYSPLL0";

const mux12       = system.clockTree["SYSPLLMUX"];
mux12.inputSelect = "zSYSPLLMUX_HFCLK";

const pinFunction4        = system.clockTree["HFXT"];
pinFunction4.inputFreq    = 40;
pinFunction4.enable       = true;
pinFunction4.HFXTStartup  = 10;
pinFunction4.HFCLKMonitor = true;

SYSCTL.forceDefaultClkConfig = true;
SYSCTL.clockTreeEn           = true;

pinFunction4.peripheral.$suggestSolution           = "SYSCTL";
pinFunction4.peripheral.hfxInPin.$suggestSolution  = "PA5";
pinFunction4.peripheral.hfxOutPin.$suggestSolution = "PA6";
```

After rebuilding, inspect `Debug/ti_msp_dl_config.h` and `Debug/ti_msp_dl_config.c` for generated output similar to:

```c
#define CPUCLK_FREQ 80000000
DL_SYSCTL_setFlashWaitState(DL_SYSCTL_FLASH_WAIT_STATE_2);
DL_SYSCTL_setULPCLKDivider(DL_SYSCTL_ULPCLK_DIV_2);
DL_SYSCTL_enableMFCLK();
DL_SYSCTL_setMCLKSource(SYSOSC, HSCLK, DL_SYSCTL_HSCLK_SOURCE_SYSPLL);
```

## Delay Cycles

`delay_cycles(n)` depends on CPUCLK. For rough one-second LED tests:

- 32 MHz CPUCLK: `delay_cycles(32000000)`
- 80 MHz CPUCLK: `delay_cycles(80000000)`

If `delay_cycles(80000000)` produces about 2.5 seconds, the CPU is likely still running near 32 MHz.

Do not use `delay_cycles()` as a precise time base for production control loops. It is useful for smoke tests, but timers should be preferred for real timing.

## Flash / Reset Gotcha

A verified issue was observed with 80 MHz clock-tree testing:

- Manual flashing could start the program with a 2.5-second blink period.
- Pressing the board reset button after flashing changed the blink period to about one second.
- Automatic DSLite flashing with `-r 2 -u` started directly with the one-second blink period.

The likely cause is that loading and running the program after flash is not always equivalent to a full system reset. When automating flash, use System Reset after programming:

```powershell
C:\ti\uniflash_9.2.0\dslite.bat `
  -c path\to\MSPM0G3507.ccxml `
  -e `
  -r 2 `
  -u path\to\project.out
```

For manual flashing, press the board reset button after programming if the first run appears to use the wrong clock speed.

## MFCLK Note For UART

The LCKFB UART tutorial uses MFCLK for the serial peripheral clock. For UART work that follows that pattern, keep `MFCLKGATE` enabled and confirm generated UART clock settings after SysConfig regenerates output.

Do not assume MFCLK is enabled just because the CPU clock is 80 MHz; verify it in `.syscfg` and generated code.
