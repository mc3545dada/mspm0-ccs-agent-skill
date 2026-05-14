# UART Blocking TX Baseline

This document records the first verified UART smoke test on the LCKFB Tianmengxing MSPM0G3507 board.

It is intentionally simple: blocking UART string transmit plus PB22 LED blink. It is not the final DMA / variable-length receive design.

## Validated Setup

- Board: LCKFB Tianmengxing MSPM0G3507
- Project: CCS / CCS Theia MSPM0G3507 empty project
- CPUCLK: 80 MHz
- UART instance: UART0
- UART pins: PA10 TX, PA11 RX
- Baud rate: 115200
- Data format: 8 data bits, no parity, 1 stop bit
- PC adapter observed: CH340 on COM6
- PC tool observed: VOFA+ raw data view
- Python tool observed: `tools/serial_console.py`

Current generated output showed:

```c
#define UART_0_INST            UART0
#define UART_0_INST_FREQUENCY  40000000
#define GPIO_UART_0_TX_PIN     DL_GPIO_PIN_10
#define GPIO_UART_0_RX_PIN     DL_GPIO_PIN_11
#define UART_0_BAUD_RATE       (115200)
```

The generated UART clock config used BUSCLK:

```c
.clockSel    = DL_UART_MAIN_CLOCK_BUSCLK,
.divideRatio = DL_UART_MAIN_CLOCK_DIVIDE_RATIO_1
```

Do not describe this baseline as the final MFCLK/DMA receive design. If a future UART project intentionally uses MFCLK, verify the generated UART clock config again.

## SysConfig Pattern

Relevant `.syscfg` lines:

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

Keep the 80 MHz / clock-tree setup from `docs/clock_tree_rules.md` when reproducing this exact test.

## C Pattern

Minimal blocking transmit helpers:

```c
#include <stdint.h>
#include <stdarg.h>
#include <stdio.h>
#include "ti_msp_dl_config.h"

#define UART_TX_BUF_SIZE 256

int UART0_sendStr(const char *str)
{
    int cnt = 0;
    while (*str) {
        DL_UART_transmitDataBlocking(UART_0_INST, (uint8_t) *str);
        str++;
        cnt++;
    }
    return cnt;
}

int UART0_printf(char *fmt, ...)
{
    static char buf[UART_TX_BUF_SIZE];
    int len;
    va_list args;
    va_start(args, fmt);
    len = vsprintf(buf, fmt, args);
    va_end(args);
    UART0_sendStr(buf);
    return len;
}
```

Observed application behavior:

```c
UART0_printf("Hello World! %d\n", n);
```

The board sent one line about every two seconds while blinking PB22.

## PC-Side Test

Use the Python serial console:

```powershell
python tools\serial_console.py --list
python tools\serial_console.py -p COM6 -b 115200 --timestamp --duration 10
```

Expected output is repeated text similar to:

```text
Hello World! 48
Hello World! 49
```

Verified Python receive output:

```text
Opened COM6 at 115200 8N1
[23:47:59.931] Hello World! 316
[23:48:01.923] Hello World! 317

Done. RX 34 bytes.
```

If the port is already open in VOFA+, Python will fail to open it. Close VOFA+ before running the script.

## Notes For Future DMA Work

- Keep this blocking TX example as a smoke test only.
- For bidirectional control, add RX handling and a framing strategy.
- For variable-length receive, prefer DMA or interrupt-driven receive with an explicit frame delimiter or timeout policy.
- Re-check UART clock source, generated baud divisors, IRQ names, DMA trigger names, and generated init function names after each SysConfig change.
