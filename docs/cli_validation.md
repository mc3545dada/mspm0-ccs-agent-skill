# CLI Validation for MSPM0 CCS Projects

This document records the command-line chain verified on a LCKFB Tianmengxing MSPM0G3507 board with CCS / CCS Theia, MSPM0 SDK 2.10.00.04, SysConfig 1.26.2, TI Arm Clang 4.0.3 LTS, and J-Link through UniFlash / DSLite.

The exact paths are environment-specific. Treat these commands as a pattern and adjust `C:\ti\...`, project name, and `.ccxml` paths for the local machine.

## 1. Static Check

Run the repository checker first:

```powershell
python tools\check_syscfg.py C:\Users\3545\workspace_ccstheia\26testproject1
```

The checker looks for:

- `.syscfg` files and metadata such as `@cliArgs`, `@v2CliArgs`, and `@versions`
- generated `Debug/ti_msp_dl_config.c` and `Debug/ti_msp_dl_config.h`
- `assignedPin` entries and `$suggestSolution` pin hints
- `SYSCFG_DL_init()` / `SYSCFG_DL_Init()` spelling mismatches
- reminder that generated SysConfig files should be inspected, not edited

## 2. SysConfig CLI

Run SysConfig directly when you want fast configuration validation without a full compile:

```powershell
C:\ti\sysconfig_1.26.2\sysconfig_cli.bat `
  --script C:\Users\3545\workspace_ccstheia\26testproject1\empty.syscfg `
  --product C:\ti\mspm0_sdk_2_10_00_04\.metadata\product.json `
  --compiler ticlang `
  --output <temp-output-dir>
```

If the project has already been built by CCS, `Debug\subdir_rules.mk` usually contains the exact SysConfig command that CCS generated.

## 3. CCS Generated Makefile Build

Build through the generated makefile:

```powershell
C:\ti\ccs2020\ccs\utils\bin\gmake.exe `
  -C C:\Users\3545\workspace_ccstheia\26testproject1\Debug `
  clean all
```

This regenerates `ti_msp_dl_config.c/.h`, compiles application code, and links the `.out` file.

If a project has never been built by CCS / CCS Theia, `Debug\subdir_rules.mk` may not exist yet. In that case:

- SysConfig CLI can still validate `.syscfg` by writing to a temporary output directory.
- `gmake -C Debug clean all` is not available until CCS has generated the build files.
- Ask the user to build once in CCS / CCS Theia, or use the local CCS command-line build interface if it is configured for that installation.

On one tested CCS installation, `ccs-serverc.exe` exposed the following build application help:

```text
ccs-serverc -nosplash -data '<eclipse-metadata-dir>' -application com.ti.ccs.apps.buildProject
  (-ccs.projects [<name> ]+ | -ccs.locations [<path> ]+ | -ccs.workspace) [<options>]
```

This interface can vary by CCS version, so prefer the already generated makefile when it is present.

## 4. J-Link / DSLite Flash

List the available debug cores before flashing:

```powershell
C:\ti\uniflash_9.2.0\dslite.bat `
  -c C:\Users\3545\workspace_ccstheia\26testproject1\targetConfigs\MSPM0G3507.ccxml `
  -N
```

The `.ccxml` must match the physical debug probe. In the verified Tianmengxing setup, the file references `SEGGER J-Link Emulator_0`.

If the project is still configured for XDS110 while the board is connected through J-Link, DSLite can fail before flashing with:

```text
An attempt to connect to the XDS110 failed.
```

Flash, issue System Reset, and run:

```powershell
C:\ti\uniflash_9.2.0\dslite.bat `
  -c C:\Users\3545\workspace_ccstheia\26testproject1\targetConfigs\MSPM0G3507.ccxml `
  -e `
  -r 2 `
  -u C:\Users\3545\workspace_ccstheia\26testproject1\Debug\26testproject1.out
```

Expected success ends with:

```text
Loading Program: ...\Debug\26testproject1.out
Setting PC to entry point.
Resetting...
System Reset is issued.
Running...
Success
```

The `-r 2` argument selects System Reset from DSLite's reset list. This matters for clock-tree changes. A verified 80 MHz test could blink at about 2.5 seconds immediately after a load-and-run flash, then blink at about one second after pressing the board reset button. Adding `-r 2 -u` made automatic flashing start directly with the one-second blink.

If you flash manually through CCS / UniFlash and the first run appears to use the wrong clock speed, press the board reset button after programming.

If `dslite -N` hangs or times out, do not continue to flash blindly. Close stale DSLite/CCS debug sessions, check that the board and J-Link are still connected, and retry the core listing before running `-e -u`.

## Notes

- Passing SysConfig and build validation does not replace hardware observation.
- In the verified Tianmengxing PB22 LED workflow, the final check was the physical board LED blinking once per second.
- Other boards, debug probes, SDK versions, CCS versions, and pin mappings may require adjustment.
- A freshly created CCS project may need one manual IDE build before generated makefiles exist.
- A successfully built project can still fail to flash if `targetConfigs/*.ccxml` uses the wrong debug probe.
- For automated flashing after clock-tree work, use DSLite System Reset (`-r 2`) before running.
