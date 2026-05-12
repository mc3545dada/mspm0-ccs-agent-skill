# PWM Motor Example

Minimal reference for one PWM timer with two direction GPIO pins in an MSPM0 CCS + SysConfig project.

This is not a complete CCS import project. It shows how an agent should separate SysConfig hardware setup from application-level motor control.

## Files

- `example.syscfg`: PWM and direction GPIO configuration pattern
- `main.c`: DriverLib motor duty and direction helpers

## Agent Notes

- Configure PWM channels and direction pins in `.syscfg`.
- Use application code only to set direction and duty.
- Confirm TimerA vs TimerG generated instance before choosing `DL_TimerA_*` or `DL_TimerG_*`.
- Clamp duty cycle before writing capture compare values.

## Expected Generated Names

The example expects generated names similar to:

```c
motor1_INST
GPIO_motor1_C0_IDX
m1o1_PORT
m1o1_PIN_8_PIN
SYSCFG_DL_init()
```

Real projects may generate different names.

