# MSPM0 CCS Agent Skill

面向 TI MSPM0 + Code Composer Studio / CCS Theia + SysConfig + DriverLib 的 AI 编程助手规则包。

这个项目主要给国内做 MSPM0、参加电赛、使用立创天猛星 MSPM0G3507 或 TI LaunchPad 的同学使用。它不是传统意义上的芯片库，也不是完整工程模板，而是一套给 AI 编程助手看的规则、说明和后续工具，让 Claude Code、OpenCode、OpenClaw、Continue、Cursor 等工具更懂 MSPM0 CCS 工程。

普通 AI 编程助手通常能看懂 C 语言，但不一定理解 TI CCS + SysConfig 的工程规则。最常见的问题是：

- 直接手改 `ti_msp_dl_config.c` / `ti_msp_dl_config.h` 这类生成文件
- 不改 `.syscfg`，却自己乱写引脚初始化代码
- 猜错 SysConfig 生成的宏名、外设名、中断名
- 忽略 `.syscfg` 里的芯片型号、封装、SDK 版本信息
- 把 `SYSCFG_DL_init()` / `SYSCFG_DL_Init()` 大小写写错

这个仓库的目标就是：让 AI 在修改 MSPM0 工程时，先理解 SysConfig，再安全地改代码。

## 适合谁

- 全国大学生电子设计竞赛相关项目
- MSPM0G3507 / MSPM0L 系列用户
- 立创天猛星 MSPM0G3507 用户
- TI LaunchPad 用户
- 使用 CCS / CCS Theia 的同学
- 使用 Claude Code、OpenCode、OpenClaw、Continue、Cursor 等 AI 编程助手的人
- 想让 AI 帮忙改 GPIO、UART、PWM、电机、舵机、OLED、ADC、定时器、PID 控制代码的人

Codex 等支持 skill 风格规则的工具也可以使用本仓库，但本项目不是 Codex 专属。

## 为什么 MSPM0 需要专门的 Agent 规则

很多 MSPM0 CCS 工程使用 SysConfig。

在这类工程里，`.syscfg` 文件才是引脚、外设、时钟和初始化代码的源配置文件。`ti_msp_dl_config.c` 和 `ti_msp_dl_config.h` 通常是 SysConfig 自动生成的输出文件，不应该手动修改。

正确思路是：

```text
修改 .syscfg
-> 运行 SysConfig 或重新构建 CCS 工程
-> 生成 ti_msp_dl_config.c / ti_msp_dl_config.h
-> 应用代码调用生成的宏和 DriverLib API
```

这个仓库就是把这套规则明确告诉 AI，避免它像改普通 C 工程那样乱改生成文件。

## 快速使用

根据你使用的工具，把下面一个或多个入口文件放进你的 MSPM0 CCS 工程：

```text
SKILL.md
AGENTS.md
CLAUDE.md
```

推荐最少放：

```text
AGENTS.md
```

如果你用 Claude Code，也建议放：

```text
CLAUDE.md
```

如果你的工具支持 skill 风格规则，也可以使用：

```text
SKILL.md
```

然后让 AI 先阅读规则，再开始改工程。例如：

```text
请先阅读 MSPM0 agent 规则，检查当前工程的 .syscfg 和生成的 ti_msp_dl_config.h，然后帮我安全地增加一个 UART 调试串口。
```

如果修改了 `.syscfg`，一定要重新构建 CCS 工程，或者运行 CCS 生成的 SysConfig CLI 命令。

## 当前阶段

当前是 Phase 1：文档和规则 MVP。

本阶段不需要手头有 MSPM0 板子，主要解决“AI 能不能正确理解工程结构”和“AI 会不会乱改生成文件”的问题。

已经包含：

- `SKILL.md`：面向 skill-aware CLI agent 的通用入口
- `AGENTS.md`：通用 AI agent 规则
- `CLAUDE.md`：面向 Claude Code 的说明
- `docs/syscfg_rules.md`：`.syscfg` 安全修改规则
- `docs/ccs_project_rules.md`：CCS 工程结构规则
- `docs/driverlib_rules.md`：DriverLib 使用规则
- `docs/common_mistakes.md`：常见错误清单

## 核心规则

- `.syscfg` 是引脚和外设配置的源头。
- 不要手动修改 `Debug/ti_msp_dl_config.c` 或 `Debug/ti_msp_dl_config.h`。
- 不要随便删除 `.syscfg` 头部的 device、package、product、version 信息。
- GPIO、UART、PWM、I2C、ADC、Timer 等配置优先改 `.syscfg`。
- 应用代码优先使用 SysConfig 生成的宏和 TI DriverLib API。
- 修改 `.syscfg` 后必须重新运行 SysConfig 或重新构建工程。
- 不要猜生成函数名，先看 `ti_msp_dl_config.h`。有些工程是 `SYSCFG_DL_init()`，不是 `SYSCFG_DL_Init()`。
- 不要随便更换芯片型号、封装、SDK、编译器或 CCS 版本。

## 后续计划

后续会继续加入：

- 常见 `.syscfg` 片段：GPIO、按键中断、UART、PWM、电机、I2C OLED、ADC、定时器
- 最小例程：点灯、串口回显、PWM 电机
- `tools/check_syscfg.py`：静态检查 `.syscfg` 和工程结构
- SysConfig CLI / CCS 构建验证工具
- 自动烧录流程
- Python 串口收发工具
- 基于串口的 PID / 电机 / 舵机 / 云台参数自动调整工具

前几阶段主要做不需要硬件的工作。烧录、串口通信和自动调参会放到后面有板子时再做。

## 参考资料

- TI SysConfig: https://www.ti.com/tool/SYSCONFIG
- TI MSPM0 SDK: https://www.ti.com/tool/MSPM0-SDK
- TI MSPM0 SysConfig Guide: https://software-dl.ti.com/msp430/esd/MSPM0-SDK/2_05_01_00/docs/english/tools/sysconfig_guide/doc_guide/doc_guide-srcs/sysconfig_guide.html
- 立创天猛星 MSPM0G3507 文档: https://wiki.lckfb.com/zh-hans/tmx-mspm0g3507/

