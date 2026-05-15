# PWM Breathing LED Baseline

This document records the verified PB22 PWM breathing LED test on the LCKFB Tianmengxing MSPM0G3507 board.

## Validated Setup

- Board: LCKFB Tianmengxing MSPM0G3507
- Project: CCS / CCS Theia MSPM0G3507 empty project
- CPUCLK: 80 MHz
- PWM timer: TIMG8
- PWM output: CCP1
- LED pin: PB22
- SDK: MSPM0 SDK 2.10.00.04
- SysConfig: 1.26.2
- Flash probe: J-Link
- Flash command: DSLite with `-e -r 2 -u`

## SysConfig Pattern

Relevant `.syscfg` lines:

```js
const PWM    = scripting.addModule("/ti/driverlib/PWM", {}, false);
const PWM1   = PWM.addInstance();

PWM1.$name                      = "PWM_0";
PWM1.clockPrescale              = 16;
PWM1.peripheral.$assign         = "TIMG8";
PWM1.peripheral.ccp1Pin.$assign = "PB22";
PWM1.PWM_CHANNEL_1.$name        = "ti_driverlib_pwm_PWMTimerCC1";
PWM1.PWM_CHANNEL_1.dutyCycle    = 50;
PWM1.ccp1PinConfig.$name        = "ti_driverlib_gpio_GPIOPinGeneric1";
```

Keep the 80 MHz / HFXT clock-tree setup from `references/clock_tree_rules.md` when reproducing this exact test.

Generated header output confirmed:

```c
#define PWM_0_INST          TIMG8
#define PWM_0_INST_CLK_FREQ 2500000
#define GPIO_PWM_0_C1_PIN   DL_GPIO_PIN_22
#define GPIO_PWM_0_C1_IDX   DL_TIMER_CC_1_INDEX
```

## C Pattern

Use the generated channel macro for PB22:

```c
DL_TimerG_setCaptureCompareValue(PWM_0_INST, duty, GPIO_PWM_0_C1_IDX);
```

Start with a known compare value before starting the timer:

```c
SYSCFG_DL_init();
DL_TimerG_setCaptureCompareValue(PWM_0_INST, PWM_MAX, GPIO_PWM_0_C1_IDX);
DL_TimerG_startCounter(PWM_0_INST);
```

For the verified smoke test:

```c
#define PWM_PERIOD     1000
#define PWM_MIN        1
#define PWM_MAX        (PWM_PERIOD - 1)
#define FADE_STEP      10
#define FADE_DELAY_CYC 800000
```

At 80 MHz, `delay_cycles(800000)` is roughly 10 ms. With about 100 steps, each fade direction is roughly one second.

## Failed And Corrected Behavior

Failure 1: too slow.

The first implementation used a one-second delay per brightness step:

```c
#define STEP_SIZE  100
#define DELAY_CYC  80000000
```

This made the fade very slow.

Failure 2: LED appeared off.

A later implementation used exact edge values `0` and `1000` for a timer period of `1000`. On the verified board, this produced an apparent off/glitchy result.

Successful correction:

- Avoid exact compare boundaries.
- Use `1..999`.
- Set the first compare value before starting the timer.
- Use smaller delays per step.

## Build Issue Observed

One CCS project generated a `Debug/makefile` that linked both:

```text
../device_linker.cmd
-l"./device_linker.cmd"
```

SysConfig generated `Debug/device_linker.cmd`, but `../device_linker.cmd` did not exist. Copying the generated linker file to the project root caused duplicate memory range linker errors.

Treat this as a CCS generated build-file state problem. Do not edit generated `Debug/makefile` as the default fix. Prefer regenerating/rebuilding in CCS. For one-off CLI validation, remove the duplicate root linker input from the manual link command and keep `-l"./device_linker.cmd"`.

## Flash Issue Observed

After a failed J-Link connection, stale `DSLite`, `JLink`, or `JLinkGUIServer` processes could keep the next flash attempt from connecting. Stopping stale processes and retrying DSLite succeeded:

```powershell
Get-Process DSLite,JLink,JLinkGUIServer -ErrorAction SilentlyContinue | Stop-Process -Force
dslite.bat -c path\to\MSPM0G3507.ccxml -e -r 2 -u path\to\project.out
```

Do not report hardware flashing as verified until DSLite reaches `Running... Success`.
