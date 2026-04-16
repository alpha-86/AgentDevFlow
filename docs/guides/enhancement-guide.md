# Enhancement Guide — 能力增强层使用指南

## 概述

本文档说明如何在 AgentDevFlow 中启用和使用 gstack / superpower 能力增强层。

## 默认状态

**增强层默认关闭**。

AgentDevFlow 本体保持可独立运行，不安装 gstack / superpower 时，所有流程正常运行。

## 启用增强层

### 前提条件

1. **安装 gstack skill 包**
   ```bash
   # 确认 gstack 已安装并可被发现
   ```

2. **安装 superpower skill 包**
   ```bash
   # 确认 superpower 已安装并可被发现
   ```

### 自动检测

增强层采用自动检测机制：

- 当 AgentDevFlow 初始化角色 Agent 时，自动检测 gstack / superpower 是否已安装
- 如已安装，自动启用对应增强能力
- 如未安装，自动回落至原生机制

**无需手动配置开关。**

## 各角色增强说明

### Product Manager

**可选增强 skill**：`brainstorming`, `plan-ceo-review`

**适用阶段**：
- 需求澄清
- PRD 起草前
- PRD 文档评审前

**使用方式**：增强层开启后，PM 在上述阶段自动获得 gstack/superpower 增强能力。

### Architect

**可选增强 skill**：`plan-eng-review`, `brainstorming`

**适用阶段**：
- Tech Spec 起草前
- 技术方案评审前

**使用方式**：增强层开启后，Architect 在上述阶段自动获得增强能力。

### QA Engineer

**可选增强 skill**：`qa-only`, `qa`

**适用阶段**：
- QA Case Design 后
- QA 验证阶段

**使用方式**：增强层开启后，QA Engineer 在上述阶段自动获得增强能力。

### Engineer

**可选增强 skill**：`review`, `investigate`

**适用阶段**：
- 开发前
- 修 Bug 时
- 代码 PR 前

**使用方式**：增强层开启后，Engineer 在上述阶段自动获得增强能力。

### Team Lead / PMO

**可选增强 skill**：`brainstorming`, `plan-design-review`, `document-release`

**适用阶段**：
- 流程改进
- 接入文档优化
- 发布后文档同步

**使用方式**：增强层开启后，Team Lead / PMO 在上述阶段自动获得增强能力。

## 边界约束

### 可以做的

- 在角色文档中说明"如增强层开启，可调用哪些 skill"
- 在平台文档中说明"启用增强层需要哪些安装前置"
- 在流程文档中说明"哪些阶段适合启用能力增强"

### 不能做的

- 不能让 AgentDevFlow 强依赖 gstack / superpower
- 不能把 skill 输出当作正式 Gate 结论
- 不能让 skill 替代正式角色职责
- 不能为了接 skill 而改造出 AgentDevFlow 之外的新流程能力边界

## 增强层输出边界

skill 生成的内容只能作为：

- 分析过程
- 补充视角
- 评审建议
- 质量增强输入

**不能替代**以下正式交付物：

- PRD
- Tech Spec
- QA Case Design
- QA Report
- Issue Comment
- 正式评审结论

**核心原则**：skill 负责"增强思考和执行质量"，正式文件负责"形成流程留痕与交付依据"。

## 故障排除

### 增强层未生效

1. 确认 gstack 和 superpower skill 包已正确安装
2. 确认运行环境能够发现并调用这些 skill
3. 检查 Agent 初始化日志

### 回落至原生机制

如果未安装 gstack/superpower，AgentDevFlow 会：
- 自动回落至原生机制
- 不报错不阻断任何操作
- 提示用户建议安装 gstack 和 superpower 以获得增强能力

这是正常行为，不代表功能缺失。
