# UART0 Blocking TX SysConfig Snippet

## Use Case

Tianmengxing MSPM0G3507 UART0 smoke test at 115200 baud, using PA10 as TX and PA11 as RX. This was validated by sending `Hello World! <n>` lines to a PC through a CH340 USB serial adapter.

This is a blocking TX baseline, not the final DMA receive design.

## Snippet

```js
const UART   = scripting.addModule("/ti/driverlib/UART", {}, false);
const UART1  = UART.addInstance();

UART1.$name                    = "UART_0";
UART1.targetBaudRate           = 115200;
UART1.peripheral.rxPin.$assign = "PA11";
UART1.peripheral.txPin.$assign = "PA10";
UART1.txPinConfig.$name        = "ti_driverlib_gpio_GPIOPinGeneric0";
UART1.rxPinConfig.$name        = "ti_driverlib_gpio_GPIOPinGeneric1";

UART1.peripheral.$suggestSolution = "UART0";
```

## Generated Names Observed

```c
#define UART_0_INST            UART0
#define UART_0_INST_FREQUENCY  40000000
#define GPIO_UART_0_RX_PIN     DL_GPIO_PIN_11
#define GPIO_UART_0_TX_PIN     DL_GPIO_PIN_10
#define UART_0_BAUD_RATE       (115200)
```

Always inspect the local generated `ti_msp_dl_config.h`; generated names can change if SysConfig instance names change.
