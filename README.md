# MSPM0 CCS Agent Skill

面向 TI MSPM0 + CCS / CCS Theia + SysConfig + DriverLib 的 AI 编程助手规则包。

本项目主要服务于国内 MSPM0 开发、电赛备赛和立创天猛星 MSPM0G3507 使用场景，帮助 Claude Code、OpenCode、OpenClaw、Continue、Cursor、Codex 等 CLI / 编辑器 Agent 更安全地理解和修改 MSPM0 CCS 工程。

## 项目定位

这不是芯片库，也不是完整工程模板，而是一套给 Agent 使用的工程规则、参考片段和验证工具。

它关注几件事：

- 正确处理 `.syscfg`
- 避免手动修改 SysConfig 生成文件
- 使用 TI DriverLib 和生成宏
- 理解 CCS / CCS Theia 工程结构
- 固化已经实机验证过的命令行流程
- 记录时钟树和烧录复位相关经验

## 已验证环境

目前已实机验证的组合是：

- 开发板：立创天猛星 MSPM0G3507
- 开发环境：CCS / CCS Theia
- SDK：MSPM0 SDK 2.10.00.04
- SysConfig：1.26.2
- 编译器：TI Arm Clang 4.0.3 LTS
- 烧录器：J-Link
- 烧录工具：UniFlash / DSLite
- 验证外设：PB22 板载 LED，一秒闪烁
- 已验证时钟：80MHz CPUCLK，MFCLK 4MHz

其他开发板、芯片封装、SDK/CCS 版本、调试器或烧录方式可能也能使用本项目规则，但尚未百分百确认。迁移到其他组合时，应先运行静态检查和最小外设验证。

## 快速使用

根据你的 AI 编程工具选择入口文件：

```text
SKILL.md
AGENTS.md
CLAUDE.md
```

推荐用法：

- 通用 Agent：参考 `AGENTS.md`
- Claude Code：参考 `CLAUDE.md`
- 支持 skill 机制的工具：参考 `SKILL.md`

可以把对应文件复制到你的 MSPM0 CCS 工程根目录，让 Agent 先读取规则，再修改工程。

示例提示词：

```text
请先阅读 MSPM0 agent 规则，检查当前工程的 .syscfg 和 ti_msp_dl_config.h，
然后帮我安全地配置天猛星 PB22 板载 LED。
```

## 工具

静态检查当前 CCS 工程：

```powershell
python tools\check_syscfg.py C:\Users\3545\workspace_ccstheia\26testproject1
```

检查内容包括：

- 查找 `.syscfg`
- 检查 `@cliArgs`、`@v2CliArgs`、`@versions` 等元数据
- 检查 `Debug/Release` 下的 SysConfig 生成文件
- 检查 `assignedPin` 和 `$suggestSolution`
- 检查 `SYSCFG_DL_init()` / `SYSCFG_DL_Init()` 大小写是否和生成头文件一致
- 检查是否已有 `Debug/makefile`、`.out` 和 `targetConfigs/*.ccxml`
- 提示当前目标配置使用 J-Link、XDS110 或其他调试器
- 提醒不要手动修改 `ti_msp_dl_config.c/.h`
- 根据工程状态提示 SysConfig CLI、gmake、DSLite/J-Link 验证命令

完整命令行验证链路见 `docs/cli_validation.md`。

串口接收测试：

```powershell
python tools\serial_console.py --list
python tools\serial_console.py -p COM6 -b 115200 --timestamp --duration 10
```

如果 VOFA+ 或其他串口助手已经打开同一个 COM 口，Python 会无法打开该串口。测试 Python 工具前需要先关闭占用串口的软件。

## 使用前检查

如果希望 Agent 后续能直接通过命令行编译和烧录，建议先手动确认两件事：

1. 在 CCS / CCS Theia 里至少成功编译一次工程。

   这会生成 `Debug/makefile`、`Debug/subdir_rules.mk`、`Debug/ti_msp_dl_config.c/.h` 和 `.out`。没有这些文件时，Agent 仍然可以直接运行 SysConfig CLI 检查 `.syscfg`，但通常不能直接执行 `gmake -C Debug clean all`，也没有 `.out` 可以烧录。

2. 在 CCS 工程属性或 target configuration 中选择实际使用的烧录器。

   如果你实际连接的是 J-Link，但工程仍然是默认 XDS110 配置，编译可能完全正常，但 DSLite 会在连接阶段失败。实测错误类似：

   ```text
   An attempt to connect to the XDS110 failed.
   ```

当前实测结论：首次编译和烧录器配置是两个独立条件。首次编译决定命令行构建文件和 `.out` 是否存在；烧录器配置决定 DSLite 是否能连接真实硬件。

## 时钟树和烧录复位

立创天猛星 MSPM0G3507 已验证过一组 80MHz CPUCLK 配置：HFXT 40MHz、SYSPLL、CPUCLK 80MHz、MFCLK 4MHz。相关规则见 `docs/clock_tree_rules.md`，片段见 `snippets/clock_80mhz_mfclk.syscfg.md`。

`delay_cycles()` 和 CPU 主频相关。粗略闪灯测试中：

- 32MHz：`delay_cycles(32000000)` 约 1 秒
- 80MHz：`delay_cycles(80000000)` 约 1 秒

实测发现：普通手动烧录后第一次运行可能仍表现得像 32MHz，`delay_cycles(80000000)` 会变成约 2.5 秒。按一次开发板 reset 后恢复为 1 秒。自动烧录时建议使用 DSLite System Reset：

```powershell
dslite.bat -c path\to\MSPM0G3507.ccxml -e -r 2 -u path\to\project.out
```

手动烧录时如果遇到第一次运行频率不对，烧录后按一次 reset。

## 核心规则

- `.syscfg` 是引脚、外设、时钟和生成代码的源配置文件。
- 不要手动修改 `ti_msp_dl_config.c` / `ti_msp_dl_config.h`。
- 修改硬件配置时，优先修改 `.syscfg`。
- 修改 `.syscfg` 后，需要重新运行 SysConfig 或重新构建 CCS 工程。
- 应用代码应使用 SysConfig 生成的宏和 TI DriverLib API。
- 不要猜生成函数和宏名，先查看生成的 `ti_msp_dl_config.h`。
- 不要随意更换芯片型号、封装、SDK、编译器或 CCS 版本。

## 当前内容

```text
README.md
SKILL.md
AGENTS.md
CLAUDE.md
docs/
  syscfg_rules.md
  ccs_project_rules.md
  driverlib_rules.md
  common_mistakes.md
  validated_workflow.md
  cli_validation.md
  reference_projects.md
  clock_tree_rules.md
  uart_blocking_tx.md
tools/
  check_syscfg.py
  serial_console.py
snippets/
  clock_80mhz_mfclk.syscfg.md
  gpio_output_led.syscfg.md
  uart0_blocking_tx.syscfg.md
examples/
  empty_project/
  led_blink/
```

`examples/empty_project/` 记录未编译空工程的最小基线。

`examples/led_blink/` 记录已经在立创天猛星 MSPM0G3507 + PB22 上实机验证过的 LED 闪烁模式。

## 后续计划

- 继续增强 `.syscfg` 静态检查
- 将 SysConfig CLI、gmake、DSLite/J-Link 流程做成更完整的命令行验证工具
- 增加自动烧录封装
- 增强 Python 串口收发工具
- 记录 UART 阻塞发送基线，后续扩展到 DMA / 不定长收发
- 在串口工具稳定后，探索 PID / 舵机 / 云台等参数自动调整流程
- 增加更多外设示例，但只在官方资料或实测验证后加入

## 参考资料

- TI SysConfig: https://www.ti.com/tool/SYSCONFIG
- TI MSPM0 SDK: https://www.ti.com/tool/MSPM0-SDK
- TI MSPM0 SysConfig Guide: https://software-dl.ti.com/msp430/esd/MSPM0-SDK/2_05_01_00/docs/english/tools/sysconfig_guide/doc_guide/doc_guide-srcs/sysconfig_guide.html
- 立创天猛星 MSPM0G3507 文档: https://wiki.lckfb.com/zh-hans/tmx-mspm0g3507/
