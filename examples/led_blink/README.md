# LED Blink Example

Minimal reference for blinking one GPIO LED in an MSPM0 CCS + SysConfig project.

This is not a complete CCS import project. It is an agent-readable reference showing which parts belong in `.syscfg` and which parts belong in application code.

## Files

- `example.syscfg`: GPIO output configuration pattern
- `main.c`: DriverLib application code using generated macros

## Agent Notes

- Configure the LED pin in `.syscfg`.
- Do not manually edit generated `ti_msp_dl_config.c` or `ti_msp_dl_config.h`.
- After changing `example.syscfg`, run SysConfig or rebuild the real CCS project.
- Confirm the generated init function and macro names in the local generated header.

## Expected Generated Names

The example expects generated names similar to:

```c
led_PORT
led_PIN_22_PIN
SYSCFG_DL_init()
```

Real projects may generate different names.

