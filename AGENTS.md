# MSPM0 CCS Agent Rules

You are working in a TI MSPM0 project that may use Code Composer Studio, CCS Theia, SysConfig, and DriverLib.

Follow these rules before editing code.

## Golden Rules

1. Treat `.syscfg` as the source of truth for pinmux, peripheral, clock, and generated initialization configuration.
2. Do not manually edit generated SysConfig outputs, including `Debug/ti_msp_dl_config.c`, `Debug/ti_msp_dl_config.h`, `Release/ti_msp_dl_config.c`, and `Release/ti_msp_dl_config.h`.
3. Preserve `.syscfg` header metadata such as `@cliArgs`, `@v2CliArgs`, `@versions`, `--device`, `--package`, and `--product`.
4. For GPIO, UART, PWM, I2C, SPI, ADC, Timer, and clock changes, prefer modifying `.syscfg` rather than generated C code.
5. Read the generated header to confirm macro names, IRQ names, peripheral instance names, and init function spelling.
6. Do not assume the init function is `SYSCFG_DL_Init()`. Many MSPM0 projects generate `SYSCFG_DL_init()`. Use the spelling declared in `ti_msp_dl_config.h`.
7. Application code must call the generated SysConfig init function before using generated peripherals.
8. After modifying `.syscfg`, rebuild the project or run SysConfig CLI to regenerate output.
9. If a pin conflict or peripheral conflict occurs, fix `.syscfg` first.
10. Do not assume a pin is valid only because it exists on the chip package. Verify pinmux through SysConfig or generated output.
11. Follow the existing project naming style for modules, pins, macros, and interrupt handlers.
12. Ask before migrating device, package, board, SDK version, compiler, or CCS version.

## Recommended Workflow

Before changing hardware configuration:

1. Locate the `.syscfg` file.
2. Read its metadata to identify device, package, SDK product, and SysConfig tool version.
3. Inspect existing module instances, such as GPIO, UART, PWM, I2C, ADC, TIMER, and SYSCTL.
4. Inspect generated `ti_msp_dl_config.h` only to learn generated names and macros.
5. Modify the smallest relevant section of `.syscfg`.
6. Run SysConfig or rebuild.
7. Update application code to use generated DriverLib macros.
8. Do not commit generated build artifacts unless the project already tracks them intentionally.

## Files Usually Safe To Edit

- Application source files, such as `main.c`, `empty.c`, `app/*.c`, `bsp/*.c`, and matching headers
- `.syscfg`
- Project documentation
- User-owned board support files

## Files To Avoid Editing By Hand

- `Debug/ti_msp_dl_config.c`
- `Debug/ti_msp_dl_config.h`
- `Release/ti_msp_dl_config.c`
- `Release/ti_msp_dl_config.h`
- `Debug/device.opt`
- `Debug/device_linker.cmd`
- `Debug/device.cmd.genlibs`
- `Debug/*.mk`
- Object files, maps, `.out`, and other build outputs

Generated files may be inspected, but changes should be made in source files or `.syscfg`.

## DriverLib Rules

- Prefer `DL_GPIO_*`, `DL_UART_*`, `DL_Timer*`, `DL_I2C_*`, and `DL_ADC12_*` APIs.
- Keep interrupt handlers short.
- Clear interrupt flags correctly.
- Use `volatile` for variables shared with interrupt handlers.
- Avoid long blocking delays inside high-frequency interrupts.
- Do not mix register-level configuration with SysConfig-generated setup unless the user explicitly requests it and the reason is documented.

## Validation

After changing `.syscfg`, look for a CCS-generated SysConfig command in a build makefile such as `Debug/subdir_rules.mk`. A typical command calls `sysconfig_cli` with:

```text
--script path/to/project.syscfg
-o output-directory
-s path/to/mspm0_sdk/.metadata/product.json
--compiler ticlang
```

If CLI validation is not available, ask the user to rebuild in CCS and paste any SysConfig or compiler errors.

