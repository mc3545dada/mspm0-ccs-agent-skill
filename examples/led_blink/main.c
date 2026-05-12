#include "ti_msp_dl_config.h"

#define LED_DELAY_CYCLES (3200000U)

int main(void)
{
    SYSCFG_DL_init();

    while (1) {
        DL_GPIO_togglePins(led_PORT, led_PIN_22_PIN);
        delay_cycles(LED_DELAY_CYCLES);
    }
}

