# PWM Motor SysConfig Snippet

## Use Case

Configure timer PWM output for DC motor speed control, servo output, buzzer output, or other duty-cycle control.

## Agent Notes

- Configure timer instance, PWM mode, channels, period, clock divider, and pins in `.syscfg`.
- Keep motor direction GPIOs as separate GPIO outputs when using an H-bridge driver.
- Confirm whether the generated peripheral is TimerA or TimerG before choosing DriverLib calls.
- For motor control, application code should update duty cycle, not reinitialize pinmux.

## Example `.syscfg` Pattern

```js
const PWM = scripting.addModule("/ti/driverlib/PWM", {}, false);
const PWM1 = PWM.addInstance();

PWM1.$name                              = "motor1";
PWM1.timerStartTimer                    = true;
PWM1.pwmMode                            = "EDGE_ALIGN_UP";
PWM1.clockDivider                       = 2;
PWM1.peripheral.$assign                 = "TIMA0";
PWM1.peripheral.ccp0Pin.$assign         = "PA0";
PWM1.peripheral.ccp1Pin.$assign         = "PA1";
PWM1.PWM_CHANNEL_0.$name                = "ti_driverlib_pwm_PWMTimerCC0";
PWM1.PWM_CHANNEL_1.$name                = "ti_driverlib_pwm_PWMTimerCC1";
PWM1.ccp0PinConfig.direction            = scripting.forceWrite("OUTPUT");
PWM1.ccp0PinConfig.passedPeripheralType = scripting.forceWrite("Digital");
PWM1.ccp0PinConfig.$name                = "ti_driverlib_gpio_GPIOPinGeneric0";
PWM1.ccp1PinConfig.direction            = scripting.forceWrite("OUTPUT");
PWM1.ccp1PinConfig.passedPeripheralType = scripting.forceWrite("Digital");
PWM1.ccp1PinConfig.$name                = "ti_driverlib_gpio_GPIOPinGeneric1";
```

## Expected Generated Macro Style

```c
#define motor1_INST       TIMA0
#define GPIO_motor1_C0_IDX DL_TIMER_CC_0_INDEX
#define GPIO_motor1_C1_IDX DL_TIMER_CC_1_INDEX
```

## C-Side Usage

```c
#include "ti_msp_dl_config.h"

static void motor_set_left(uint32_t duty)
{
    if (duty > 1000U) {
        duty = 1000U;
    }

    DL_TimerA_setCaptureCompareValue(motor1_INST, duty, GPIO_motor1_C0_IDX);
}

int main(void)
{
    SYSCFG_DL_init();
    DL_TimerA_startCounter(motor1_INST);

    while (1) {
        motor_set_left(500U);
    }
}
```

Use `DL_TimerG_*` instead when the generated instance is TimerG.

## Validation Checklist

- Timer peripheral and channel support the selected pin.
- Duty-cycle range matches the generated timer period.
- Direction GPIOs are configured separately if required.
- DriverLib TimerA/TimerG API matches the generated instance.
- Motor cannot start unexpectedly at full duty after reset.

