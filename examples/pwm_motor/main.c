#include "ti_msp_dl_config.h"

#define MOTOR_PWM_MAX (1000U)

static uint32_t clamp_duty(uint32_t duty)
{
    return (duty > MOTOR_PWM_MAX) ? MOTOR_PWM_MAX : duty;
}

static void motor_forward(uint32_t duty)
{
    duty = clamp_duty(duty);

    DL_GPIO_setPins(m1o1_PORT, m1o1_PIN_8_PIN);
    DL_GPIO_clearPins(m1o2_PORT, m1o2_PIN_9_PIN);
    DL_TimerA_setCaptureCompareValue(motor1_INST, duty, GPIO_motor1_C0_IDX);
}

static void motor_stop(void)
{
    DL_TimerA_setCaptureCompareValue(motor1_INST, 0U, GPIO_motor1_C0_IDX);
    DL_GPIO_clearPins(m1o1_PORT, m1o1_PIN_8_PIN);
    DL_GPIO_clearPins(m1o2_PORT, m1o2_PIN_9_PIN);
}

int main(void)
{
    SYSCFG_DL_init();
    DL_TimerA_startCounter(motor1_INST);

    while (1) {
        motor_forward(500U);
        delay_cycles(32000000U);
        motor_stop();
        delay_cycles(32000000U);
    }
}

