# Timer Interrupt SysConfig Snippet

## Use Case

Configure a periodic timer interrupt for scheduling, control loops, LED heartbeat, sensor polling ticks, or software timing.

## Agent Notes

- Configure timer mode, period, prescaler, interrupts, and peripheral assignment in `.syscfg`.
- Keep timer ISRs short.
- Do not put PID math, OLED refresh, or blocking serial output directly in a high-frequency timer ISR unless the user explicitly wants that design.
- Confirm TimerA vs TimerG generated instance before using DriverLib calls.

## Example `.syscfg` Pattern

```js
const TIMER = scripting.addModule("/ti/driverlib/TIMER", {}, false);
const TIMER1 = TIMER.addInstance();

TIMER1.$name              = "TIMER_0";
TIMER1.timerClkPrescale   = 256;
TIMER1.timerMode          = "PERIODIC";
TIMER1.interrupts         = ["ZERO"];
TIMER1.timerStartTimer    = true;
TIMER1.timerPeriod        = "10ms";
TIMER1.peripheral.$assign = "TIMG0";
```

## Expected Generated Macro Style

```c
#define TIMER_0_INST            (TIMG0)
#define TIMER_0_INST_IRQHandler TIMG0_IRQHandler
#define TIMER_0_INST_INT_IRQN   (TIMG0_INT_IRQn)
#define TIMER_0_INST_LOAD_VALUE (1249U)
```

## C-Side Usage

```c
#include "ti_msp_dl_config.h"

volatile uint32_t gTick10ms;

int main(void)
{
    SYSCFG_DL_init();
    NVIC_EnableIRQ(TIMER_0_INST_INT_IRQN);
    DL_TimerG_startCounter(TIMER_0_INST);

    while (1) {
        if (gTick10ms) {
            gTick10ms = 0;
        }
    }
}

void TIMER_0_INST_IRQHandler(void)
{
    switch (DL_TimerG_getPendingInterrupt(TIMER_0_INST)) {
        case DL_TIMER_IIDX_ZERO:
            gTick10ms++;
            break;
        default:
            break;
    }
}
```

Use the actual generated handler name and TimerA/TimerG API for the project.

## Validation Checklist

- Timer period and clock prescaler produce the intended interval.
- NVIC IRQ is enabled in application code if SysConfig does not do it.
- ISR uses volatile shared state.
- ISR does not contain long blocking work.
- DriverLib TimerA/TimerG API matches generated instance.

