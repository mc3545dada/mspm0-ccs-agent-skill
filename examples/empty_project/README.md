# Empty CCS Project Baseline

Minimal reference captured from a newly created MSPM0G3507 CCS / CCS Theia empty project before the first build.

This is useful for agents because a fresh project may not yet have generated `Debug/ti_msp_dl_config.c` or `Debug/ti_msp_dl_config.h`. In that state, the agent can still inspect `empty.syscfg` and application source, but it cannot confirm generated macro names until SysConfig or CCS build runs.

## Files

- `empty.syscfg`: initial SYSCTL + Board configuration
- `empty.c`: initial application loop calling `SYSCFG_DL_init()`

Do not treat this as a complete importable CCS project. It is a small reference snapshot.
