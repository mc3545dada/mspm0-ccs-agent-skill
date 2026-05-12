# GPIO Input Key Interrupt SysConfig Snippet

## Use Case

Configure a push button or encoder input as a GPIO interrupt.

## Agent Notes

- Configure direction, resistor, interrupt enable, and polarity in `.syscfg`.
- Keep interrupt handlers short.
- For MSPM0 GPIO group interrupts, inspect the generated header for group IRQ names and per-pin IIDX macros.
- Do not assume a button is active-low or active-high. Check board wiring.

## Example `.syscfg` Pattern

```js
const GPIO = scripting.addModule("/ti/driverlib/GPIO", {}, false);
const GPIO1 = GPIO.addInstance();

GPIO1.$name                              = "key1";
GPIO1.port                               = "PORTB";
GPIO1.associatedPins[0].direction        = "INPUT";
GPIO1.associatedPins[0].$name            = "PIN_21";
GPIO1.associatedPins[0].assignedPin      = "21";
GPIO1.associatedPins[0].interruptEn      = true;
GPIO1.associatedPins[0].polarity         = "RISE";
GPIO1.associatedPins[0].internalResistor = "PULL_UP";
```

Use `FALL` instead of `RISE` when the board wiring requires a falling-edge interrupt.

## Expected Generated Macro Style

```c
#define GPIO_MULTIPLE_GPIOB_INT_IRQN  (GPIOB_INT_IRQn)
#define key1_PORT                     (GPIOB)
#define key1_PIN_21_PIN               (DL_GPIO_PIN_21)
#define key1_PIN_21_IIDX              (DL_GPIO_IIDX_DIO21)
```

## C-Side Usage

```c
#include "ti_msp_dl_config.h"

volatile bool gKeyPressed;

int main(void)
{
    SYSCFG_DL_init();
    NVIC_EnableIRQ(GPIO_MULTIPLE_GPIOB_INT_IRQN);

    while (1) {
        if (gKeyPressed) {
            gKeyPressed = false;
        }
    }
}

void GROUP1_IRQHandler(void)
{
    switch (DL_Interrupt_getPendingGroup(DL_INTERRUPT_GROUP_1)) {
        case DL_INTERRUPT_GROUP1_IIDX_GPIOB:
            if (DL_GPIO_getEnabledInterruptStatus(key1_PORT, key1_PIN_21_PIN) &
                key1_PIN_21_PIN) {
                gKeyPressed = true;
                DL_GPIO_clearInterruptStatus(key1_PORT, key1_PIN_21_PIN);
            }
            break;
        default:
            break;
    }
}
```

Confirm the actual group handler and IRQ names in the project startup file and generated header.

## Validation Checklist

- Pull-up or pull-down matches the board circuit.
- Interrupt polarity matches active edge.
- ISR clears the GPIO interrupt flag.
- Shared state is `volatile`.
- No long delay, OLED drawing, UART print loop, or sensor transaction is inside the ISR.

