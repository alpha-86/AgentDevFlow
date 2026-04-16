# Enhancement Layer — 能力增强层

## 定位

AgentDevFlow 的"能力增强层"由 `gstack` 和 `superpower` 提供，用于在特定阶段增强各角色的分析、评审与执行能力。

**核心原则**：增强角色，不替代角色。

| 项目 | 定位 |
|------|------|
| `gstack` | 偏工具与任务工作流，增强单个 Agent 的执行能力 |
| `superpower` | 偏通用方法论与执行模式，增强单个 Agent 的规划、拆解和协作能力 |
| `AgentDevFlow` | 偏多 Agent 交付流程层，定义 Issue / PRD / Tech / QA / Gate / Human Review / Release 的正式协作机制 |

## 增强层与核心流程的关系

- `gstack / superpower` 是**能力插件层**，增强 Agent 的工作质量
- AgentDevFlow 核心流程（Gate / PR / Human Review）是**流程约束层**，确保交付确定性
- **增强层输出不能替代正式交付物**：skill 生成的内容只能作为分析过程、补充视角、评审建议，不能替代 PRD、Tech Spec、QA Case Design 等正式文件

## 开关机制

采用**自动检测 + 回落**机制：

- **已安装 gstack**：AgentDevFlow 自动使用 gstack 相关 skill 进行能力增强
- **已安装 superpower**：AgentDevFlow 自动使用 superpower 相关 skill 进行能力增强
- **均未安装**：回落至 AgentDevFlow 原生机制，提示用户建议安装

> 自动检测在角色 Agent 初始化时进行，无需用户手动配置。回落到原生机制不影响任何核心流程运行。

## 角色增强映射

| 角色 | 可选增强 skill | 适用阶段 | 来源 |
|------|--------------|---------|------|
| Product Manager | brainstorming, plan-ceo-review | 需求澄清、PRD 起草前 | superpower / gstack |
| Architect | plan-eng-review, brainstorming | Tech Spec 起草前、技术方案评审前 | gstack / superpower |
| QA Engineer | qa-only, qa | QA Case Design 后、QA 验证阶段 | gstack |
| Engineer | review, investigate | 开发前、修 Bug、代码 PR 前 | gstack |
| Team Lead / PMO | brainstorming, plan-design-review, document-release | 流程改进、接入文档优化、发布后文档同步 | superpower / gstack |

> **注**：`plan-devex-review` 已在 gstack/superpower 中验证为 `plan-design-review`。

## 安装前置条件

如需启用增强层，需满足以下前置条件：

1. 已安装 `gstack` skill 包
2. 已安装 `superpower` skill 包
3. 对应运行环境能够正确发现并调用这些 skill

如未满足安装前置条件，AgentDevFlow 自动回落至原生机制，不报错不阻断。

## 相关文档

- [PRD #003 — AgentDevFlow gstack/superpower 能力增强层接入](../prd/003_adf_enhancement_layer_2026-04-15.md)
- [讨论文档 #028 — gstack 与 superpower 增强层接入方案](../prompts/discuss/028_2026-04-14_gstack与superpower增强层接入方案.md)
- [增强层使用指南](../guides/enhancement-guide.md)
