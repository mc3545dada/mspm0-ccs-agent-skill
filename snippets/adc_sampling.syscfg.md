# ADC Sampling SysConfig Snippet

## Use Case

Configure ADC sampling for sensors, battery voltage, potentiometers, gray sensors, current sensing, or analog feedback.

## Agent Notes

- Configure ADC instance, input channel, sample time, reference, memory name, and conversion mode in `.syscfg`.
- Confirm the selected package pin supports ADC input.
- Keep ADC result names from the generated header.
- Avoid changing analog reference assumptions without asking.

## Example `.syscfg` Pattern

```js
const ADC12 = scripting.addModule("/ti/driverlib/ADC12", {}, false);
const ADC121 = ADC12.addInstance();

ADC121.$name                             = "ADC1";
ADC121.sampClkDiv                        = "DL_ADC12_CLOCK_DIVIDE_8";
ADC121.repeatMode                        = true;
ADC121.powerDownMode                     = "DL_ADC12_POWER_DOWN_MODE_MANUAL";
ADC121.sampleTime0                       = "1 us";
ADC121.adcMem0_name                      = "ADC_Channel0";
ADC121.adcPin0Config.hideOutputInversion = scripting.forceWrite(false);
ADC121.adcPin0Config.$name               = "ti_driverlib_gpio_GPIOPinGeneric0";
ADC121.adcPin0Config.enableConfig        = true;
ADC121.peripheral.$suggestSolution       = "ADC1";
ADC121.peripheral.adcPin0.$suggestSolution = "PA15";
```

## Expected Generated Macro Style

```c
#define ADC1_INST                 ADC1
#define ADC1_ADCMEM_ADC_Channel0  DL_ADC12_MEM_IDX_0
#define GPIO_ADC1_C0_PIN          DL_GPIO_PIN_15
```

## C-Side Usage

```c
#include "ti_msp_dl_config.h"

uint16_t adc_read_once(void)
{
    DL_ADC12_enableConversions(ADC1_INST);
    DL_ADC12_startConversion(ADC1_INST);

    while (DL_ADC12_getStatus(ADC1_INST) !=
           DL_ADC12_STATUS_CONVERSION_IDLE) {
    }

    DL_ADC12_stopConversion(ADC1_INST);
    DL_ADC12_disableConversions(ADC1_INST);

    return DL_ADC12_getMemResult(ADC1_INST, ADC1_ADCMEM_ADC_Channel0);
}
```

## Validation Checklist

- Selected pin supports ADC for the target package.
- ADC reference voltage matches the circuit.
- Sample time is suitable for sensor impedance.
- Memory index name matches generated header.
- Blocking ADC read is not used inside high-frequency ISRs.

