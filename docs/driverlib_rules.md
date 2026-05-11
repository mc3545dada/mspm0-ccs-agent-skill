# MSPM0 DriverLib Rules

MSPM0 CCS projects commonly use TI DriverLib with SysConfig-generated setup code. Agents should preserve that model.

## Initialization

Application code must call the generated SysConfig initialization function before using generated peripherals.

Do not guess the function spelling. Inspect `ti_msp_dl_config.h`.

Common generated spelling:

```c
SYSCFG_DL_init();
```

Some examples or discussions may use different capitalization. Use the local generated declaration.

## Use Generated Macros

Generated headers define names for instances, pins, IRQs, and indexes. Prefer these names over hard-coded registers or pin numbers.

Examples:

```c
DL_GPIO_togglePins(led_PORT, led_PIN_22_PIN);
NVIC_EnableIRQ(UART_0_INST_INT_IRQN);
DL_UART_Main_receiveData(UART_0_INST);
DL_TimerG_setCaptureCompareValue(motor1_INST, value, GPIO_motor1_C0_IDX);
```

Read the generated header for the actual names in the project.

## GPIO

Use DriverLib GPIO APIs such as:

```c
DL_GPIO_setPins(port, pin);
DL_GPIO_clearPins(port, pin);
DL_GPIO_togglePins(port, pin);
DL_GPIO_readPins(port, pin);
DL_GPIO_clearInterruptStatus(port, pin);
```

Configure direction, pull-up, polarity, and interrupts in `.syscfg` when possible.

## UART

Configure UART instance, TX/RX pins, baud rate, and RX interrupts in `.syscfg`.

Use generated names and DriverLib APIs in application code:

```c
DL_UART_Main_transmitData(UART_0_INST, ch);
uint8_t data = DL_UART_Main_receiveData(UART_0_INST);
```

Keep ISR work short. Move parsing or protocol work into the main loop when possible.

## Timers and PWM

Configure timer instance, clock, period, PWM mode, channels, and pins in `.syscfg`.

Use application code for runtime operations:

```c
DL_TimerG_startCounter(TIMER_0_INST);
DL_TimerG_setCaptureCompareValue(motor1_INST, duty, GPIO_motor1_C0_IDX);
```

Confirm whether the generated instance is a TimerA or TimerG peripheral and use compatible DriverLib calls.

## ADC

Configure ADC instance, input pin, sample time, memory index, repeat mode, and trigger behavior in `.syscfg`.

Use generated ADC memory names:

```c
DL_ADC12_startConversion(ADC1_INST);
uint16_t value = DL_ADC12_getMemResult(ADC1_INST, ADC1_ADCMEM_ADC_Channel0);
```

## Interrupts

Rules for interrupt handlers:

- Keep handlers short.
- Clear interrupt status.
- Avoid long blocking delays.
- Use `volatile` for variables shared with main code.
- Confirm IRQ handler names from generated macros and startup files.
- For grouped GPIO interrupts, check the group pending interrupt before checking individual pins.

## Register-Level Code

Avoid direct register configuration when SysConfig and DriverLib already own a peripheral. Direct register writes may conflict with generated initialization.

Use register-level code only when:

- The user explicitly requested it.
- DriverLib does not expose the required operation.
- The code is isolated and documented.
- The generated SysConfig setup remains consistent.

