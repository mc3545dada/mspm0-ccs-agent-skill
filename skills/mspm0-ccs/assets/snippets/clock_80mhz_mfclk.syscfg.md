# Tianmengxing 80 MHz CPUCLK + MFCLK SysConfig Snippet

## Use Case

Configure the LCKFB Tianmengxing MSPM0G3507 clock tree for an 80 MHz CPU clock and enabled MFCLK. This was validated with PB22 LED blinking and is intended as a reference before UART work that uses MFCLK.

## SysConfig Snippet

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

## Checks

After rebuilding, confirm generated output includes:

```c
#define CPUCLK_FREQ 80000000
DL_SYSCTL_setFlashWaitState(DL_SYSCTL_FLASH_WAIT_STATE_2);
DL_SYSCTL_setULPCLKDivider(DL_SYSCTL_ULPCLK_DIV_2);
DL_SYSCTL_enableMFCLK();
DL_SYSCTL_setMCLKSource(SYSOSC, HSCLK, DL_SYSCTL_HSCLK_SOURCE_SYSPLL);
```

## LED Timing Smoke Test

For a rough one-second delay at 80 MHz:

```c
delay_cycles(80000000);
```

If the board blinks at about 2.5 seconds, the CPU may still be running at about 32 MHz. Press reset after manual flashing, or use DSLite with System Reset:

```powershell
dslite.bat -c path\to\MSPM0G3507.ccxml -e -r 2 -u path\to\project.out
```
