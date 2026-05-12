# GPIO Output LED SysConfig Snippet

## Use Case

Configure one digital output pin for an LED or simple enable signal.

## Agent Notes

- Add or edit GPIO in `.syscfg`; do not write pinmux setup by hand in generated C files.
- Check whether the board LED is active-high or active-low.
- Reuse the local naming style. Many MSPM0 projects generate names like `led_PORT` and `led_PIN_22_PIN`.
- Confirm the generated macro names in `ti_msp_dl_config.h` after rebuilding.

## Example `.syscfg` Pattern

```js
const GPIO = scripting.addModule("/ti/driverlib/GPIO", {}, false);
const GPIO1 = GPIO.addInstance();

GPIO1.$name                         = "led";
GPIO1.port                          = "PORTB";
GPIO1.associatedPins[0].$name       = "PIN_22";
GPIO1.associatedPins[0].assignedPin = "22";
GPIO1.associatedPins[0].direction   = "OUTPUT";
```

If the project already has a `const GPIO = ...` declaration, add only a new instance:

```js
const GPIO2 = GPIO.addInstance();
```

## Expected Generated Macro Style

```c
#define led_PORT        (GPIOB)
#define led_PIN_22_PIN  (DL_GPIO_PIN_22)
```

The exact names depend on `$name` and pin `$name`.

## C-Side Usage

```c
#include "ti_msp_dl_config.h"

int main(void)
{
    SYSCFG_DL_init();

    while (1) {
        DL_GPIO_togglePins(led_PORT, led_PIN_22_PIN);
        delay_cycles(3200000);
    }
}
```

Use the generated init function spelling from the local project.

## Validation Checklist

- `.syscfg` metadata is unchanged.
- No generated `ti_msp_dl_config.*` file was manually edited.
- The selected package pin is valid for GPIO.
- The generated header contains the expected port and pin macros.
- The application calls the generated SysConfig init function before toggling the pin.

