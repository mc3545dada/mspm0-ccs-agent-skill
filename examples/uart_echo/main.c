#include "ti_msp_dl_config.h"

static void uart0_putc(uint8_t ch)
{
    while (DL_UART_isBusy(UART_0_INST)) {
    }
    DL_UART_Main_transmitData(UART_0_INST, ch);
}

int main(void)
{
    SYSCFG_DL_init();
    NVIC_ClearPendingIRQ(UART_0_INST_INT_IRQN);
    NVIC_EnableIRQ(UART_0_INST_INT_IRQN);

    uart0_putc('>');

    while (1) {
    }
}

void UART_0_INST_IRQHandler(void)
{
    switch (DL_UART_getPendingInterrupt(UART_0_INST)) {
        case DL_UART_IIDX_RX: {
            uint8_t data = DL_UART_Main_receiveData(UART_0_INST);
            uart0_putc(data);
            break;
        }
        default:
            break;
    }
}

