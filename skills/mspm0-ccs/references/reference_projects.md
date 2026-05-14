# Reference Projects Used For Validation

This repository avoids using unverified contest code as a source of rules. Current references are limited to TI-generated empty CCS projects, the LCKFB Tianmengxing documentation pattern, and workflows verified on real hardware.

## 26testproject1

- Role: CCS project used for command-line SysConfig, build, J-Link flash, and real-board PB22 LED validation.
- State observed: generated/compiled project after the LED workflow was applied.
- Important lesson: after editing `empty.syscfg` as text, CCS generated makefiles regenerated `ti_msp_dl_config.c/.h`, compiled the application, and DSLite flashed the `.out` successfully through J-Link.
- Not committed here: build artifacts such as `.out`, `.o`, `.d`, generated makefiles, and generated SysConfig output.

## 26testproject2

- Role: CCS project manually configured according to the LCKFB Tianmengxing MSPM0G3507 LED tutorial.
- State observed: PB22 onboard LED blinked successfully after GUI configuration, build, and flash.
- Important lesson: this project provided the known-good PB22 SysConfig pattern used to cross-check the agent-edited project.

## 26testproject3

- Role: fresh empty CCS project reserved for tool and workflow testing.
- State observed before tests: target configuration was set to J-Link, but `Debug` did not contain generated makefiles or `.out`.
- Important lesson: static tools should handle both generated projects and not-yet-generated empty projects.
- Additional lesson: a fresh project can pass direct SysConfig CLI validation before CCS has generated `Debug\subdir_rules.mk`; `gmake -C Debug clean all` is only available after that build structure exists.
- Real failure observed during testing: invalid metadata comment syntax such as `* @cliArgs` outside a block comment causes SysConfig to fail with `SyntaxError: Unexpected token '*'`.
- Probe result: `dslite -N` can list `SEGGER J-Link Emulator_0/CORTEX_M0P` when the `.ccxml` is configured for J-Link, even if the project has not produced a `.out` yet.

## 26testproject4

- Role: project built once in CCS, but left on the default XDS110 target configuration.
- State observed: `Debug/makefile`, `Debug/subdir_rules.mk`, generated SysConfig files, and `.out` existed; `gmake -C Debug clean all` succeeded.
- Important lesson: successful build output is not enough for flashing. The target configuration must match the connected probe.
- Probe result: `dslite -N` failed because the project tried to connect to XDS110 while the physical setup used J-Link.

See `examples/empty_project/` for the empty-project baseline and `examples/led_blink/` for the verified PB22 LED pattern.
