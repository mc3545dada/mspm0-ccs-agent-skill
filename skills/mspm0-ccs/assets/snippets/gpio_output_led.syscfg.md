# Tianmengxing PB22 LED SysConfig Snippet

## Use Case

Configure the onboard LED on the LCKFB Tianmengxing MSPM0G3507 board.

This pattern was validated on real hardware. The board LED uses PB22.

## Agent Notes

- Add or edit GPIO in `.syscfg`; do not write pinmux setup by hand in generated C files.
- Use the exact generated names from the current project.
- The validated pattern uses `LED_PORT` and `LED_PIN_22_PIN`.
- Confirm the generated macro names in `ti_msp_dl_config.h` after rebuilding.

## Example `.syscfg` Pattern

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

## Expected Generated Macro Style

```c
#define LED_PORT        (GPIOB)
#define LED_PIN_22_PIN  (DL_GPIO_PIN_22)
```

The exact names depend on `$name` and pin `$name`.

## C-Side Usage

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

Use the generated init function spelling from the local project.

## Validation Checklist

- `.syscfg` metadata is unchanged.
- No generated `ti_msp_dl_config.*` file was manually edited.
- The generated header contains `LED_PORT` and `LED_PIN_22_PIN`.
- The application calls `SYSCFG_DL_init()` before touching GPIO.
- The LED is observed blinking on the board after flashing.

