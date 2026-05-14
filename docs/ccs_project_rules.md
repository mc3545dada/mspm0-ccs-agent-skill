# CCS Project Rules for MSPM0

MSPM0 projects created from TI examples often use Code Composer Studio or CCS Theia. They may look like ordinary C projects, but SysConfig and generated build files are part of the workflow.

## Common Files

Common editable files:

```text
.syscfg
main.c
empty.c
README.md
```

Common project metadata:

```text
.project
.cproject
.ccsproject
.settings/
targetConfigs/*.ccxml
```

Common build output:

```text
Debug/
Release/
```

## Generated SysConfig Files

SysConfig commonly generates:

```text
ti_msp_dl_config.c
ti_msp_dl_config.h
device.opt
device_linker.cmd
device.cmd.genlibs
Event.dot
```

These are often placed under `Debug/` or `Release/` depending on the active build configuration.

Agents may inspect generated files to understand the project, but should not manually edit them.

## Build Rules

CCS generated makefiles may include a SysConfig rule in files such as:

```text
Debug/subdir_rules.mk
```

The rule normally invokes `sysconfig_cli` with the project `.syscfg`, SDK product metadata, and compiler target. This is useful for validation because it shows the exact SysConfig command CCS expects.

## Project Metadata Rules

Do not casually edit:

- `.cproject`
- `.ccsproject`
- `.project`
- `.settings/*`
- `targetConfigs/*.ccxml`

These files can affect SDK discovery, compiler settings, debug probes, include paths, linker settings, and files opened by CCS.

Only edit project metadata when the task explicitly requires it, and describe the reason.

## Build Artifacts

Do not add or modify build artifacts unless the repository already tracks them intentionally:

```text
*.o
*.d
*.out
*.map
*_linkInfo.xml
Debug/
Release/
```

For an open-source rules repository, examples should prefer source files and docs over generated binaries.

## Validation Without Hardware

Many Phase 1 tasks can be validated without a board:

- Parse or inspect `.syscfg`.
- Run SysConfig CLI if available.
- Build the project with CCS tooling if installed.
- Check generated headers for expected macros.
- Check application code compiles against generated headers.

Flashing and serial testing require hardware and should be documented only after validation on a real board.
