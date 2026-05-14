# MSPM0 CCS Agent Skill

面向 TI MSPM0 + CCS / CCS Theia + SysConfig + DriverLib 的 AI 编程助手规则包。

本项目主要服务于国内 MSPM0 开发和电赛场景，帮助 Claude Code、OpenCode、OpenClaw、Continue、Cursor、Codex 等 AI 编程助手更安全地理解和修改 MSPM0 CCS 工程。

## 项目定位

这不是芯片库，也不是完整工程模板，而是一套面向 AI Agent 的工程规则与参考文档。

它用于约束 Agent 在 MSPM0 CCS 工程中的行为，尤其是：

- 正确处理 `.syscfg`
- 避免手动修改 SysConfig 生成文件
- 使用 TI DriverLib 和生成的宏
- 理解 CCS / CCS Theia 工程结构
- 为电赛常见外设和控制代码提供后续参考

## 适用场景

- 全国大学生电子设计竞赛
- 立创天猛星 MSPM0G3507
- TI MSPM0 LaunchPad
- MSPM0G3507 / MSPM0L 系列工程
- GPIO、UART、PWM、I2C、ADC、Timer 等外设配置
- 电机、舵机、OLED、PID、云台、小车等常见电赛模块

## 快速使用

根据你的 AI 编程工具选择入口文件：

```text
SKILL.md
AGENTS.md
CLAUDE.md
```

推荐用法：

- 通用 Agent：使用 `AGENTS.md`
- Claude Code：使用 `CLAUDE.md`
- 支持 skill 机制的工具：使用 `SKILL.md`

可以把对应文件复制到你的 MSPM0 CCS 工程根目录，然后让 Agent 先阅读规则再修改工程。

示例提示词：

```text
请先阅读 MSPM0 agent 规则，检查当前工程的 .syscfg 和 ti_msp_dl_config.h，然后帮我安全地增加 UART 调试功能。
```

## 核心规则

- `.syscfg` 是引脚、外设、时钟和生成代码的源配置文件。
- 不要手动修改 `ti_msp_dl_config.c` / `ti_msp_dl_config.h`。
- 修改 GPIO、UART、PWM、I2C、ADC、Timer 等配置时，优先修改 `.syscfg`。
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
snippets/
  gpio_output_led.syscfg.md
  gpio_input_key_interrupt.syscfg.md
  uart_115200.syscfg.md
  pwm_motor.syscfg.md
  i2c_oled.syscfg.md
  adc_sampling.syscfg.md
  timer_interrupt.syscfg.md
examples/
  led_blink/
  uart_echo/
  pwm_motor/
```

当前阶段以规则、`.syscfg` 片段和最小参考例程为主，不需要连接 MSPM0 硬件。

`examples/` 目录不是完整 CCS 导入工程，而是给 Agent 和用户参考的最小结构：`README.md`、`main.c` 和 `example.syscfg`。

`docs/validated_workflow.md` 记录了一次已通过实机验证的流程：在立创天猛星 MSPM0G3507 上通过修改 `.syscfg` 配置 PB22 板载 LED，命令行生成、编译、J-Link 烧录后实现闪灯。

## 后续计划

- `.syscfg` 静态检查工具
- SysConfig CLI / CCS 构建验证工具
- 自动烧录流程
- Python 串口收发工具
- 基于串口的 PID / 电机 / 舵机 / 云台参数调试工具

## 参考资料

- TI SysConfig: https://www.ti.com/tool/SYSCONFIG
- TI MSPM0 SDK: https://www.ti.com/tool/MSPM0-SDK
- TI MSPM0 SysConfig Guide: https://software-dl.ti.com/msp430/esd/MSPM0-SDK/2_05_01_00/docs/english/tools/sysconfig_guide/doc_guide/doc_guide-srcs/sysconfig_guide.html
- 立创天猛星 MSPM0G3507 文档: https://wiki.lckfb.com/zh-hans/tmx-mspm0g3507/
