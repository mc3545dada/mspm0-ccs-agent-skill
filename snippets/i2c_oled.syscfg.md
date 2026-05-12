# I2C OLED SysConfig Snippet

## Use Case

Configure an I2C controller for OLED display modules, IMU sensors, EEPROMs, or other I2C devices.

## Agent Notes

- Configure I2C peripheral, SDA/SCL pins, controller mode, and bus speed in `.syscfg`.
- Check whether the board has external pull-up resistors on SDA/SCL.
- Do not mix software I2C GPIO bit-banging with hardware I2C on the same pins.
- Keep display drawing out of fast interrupts.

## Example `.syscfg` Pattern

```js
const I2C = scripting.addModule("/ti/driverlib/I2C", {}, false);
const I2C1 = I2C.addInstance();

I2C1.$name                             = "I2C_OLED";
I2C1.basicEnableController             = true;
I2C1.basicControllerBusSpeed           = 400000;
I2C1.basicClockSourceDivider           = 4;
I2C1.peripheral.sdaPin.$assign         = "PA28";
I2C1.peripheral.sclPin.$assign         = "PA31";
I2C1.sdaPinConfig.passedPeripheralType = scripting.forceWrite("Digital");
I2C1.sdaPinConfig.$name                = "ti_driverlib_gpio_GPIOPinGeneric0";
I2C1.sclPinConfig.passedPeripheralType = scripting.forceWrite("Digital");
I2C1.sclPinConfig.$name                = "ti_driverlib_gpio_GPIOPinGeneric1";
```

## Expected Generated Macro Style

```c
#define I2C_OLED_INST          I2C0
#define I2C_OLED_BUS_SPEED_HZ  400000
#define GPIO_I2C_OLED_SDA_PIN  DL_GPIO_PIN_28
#define GPIO_I2C_OLED_SCL_PIN  DL_GPIO_PIN_31
```

## C-Side Usage

```c
#include "ti_msp_dl_config.h"

static void i2c_write_oled(uint8_t addr, const uint8_t *data, uint32_t len)
{
    DL_I2C_fillControllerTXFIFO(I2C_OLED_INST, data, len);
    while (!(DL_I2C_getControllerStatus(I2C_OLED_INST) &
             DL_I2C_CONTROLLER_STATUS_IDLE)) {
    }
    DL_I2C_startControllerTransfer(I2C_OLED_INST, addr,
        DL_I2C_CONTROLLER_DIRECTION_TX, len);
}
```

## Validation Checklist

- SDA/SCL pins match the board wiring.
- Pull-ups are present or configured appropriately.
- Bus speed is supported by the connected device.
- Hardware I2C and software I2C do not share the same pins.
- I2C transactions are not run inside time-critical ISRs.

