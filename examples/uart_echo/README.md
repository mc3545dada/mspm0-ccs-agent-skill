# UART Echo Example

Minimal reference for UART 115200 RX interrupt echo in an MSPM0 CCS + SysConfig project.

This is not a complete CCS import project. It is intended as a pattern for agents and users.

## Files

- `example.syscfg`: UART0 configuration pattern
- `main.c`: DriverLib UART echo handler

## Agent Notes

- Configure UART pins and baud rate in `.syscfg`.
- Confirm TX/RX pins match the board USB-to-UART or debugger backchannel.
- Use generated macros from `ti_msp_dl_config.h`.
- Keep UART ISR short. Do not put complex parsing in the ISR.

## Expected Generated Names

The example expects generated names similar to:

```c
UART_0_INST
UART_0_INST_INT_IRQN
UART_0_INST_IRQHandler
SYSCFG_DL_init()
```

Real projects may generate different names.

