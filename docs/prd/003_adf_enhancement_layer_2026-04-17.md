---
name: AgentDevFlow gstack/superpower 增强层接入
description: 明确 gstack / superpower 作为 AgentDevFlow 能力增强层的接入方式、角色映射和边界约束
status: Approved
owner: Product Manager
date: 2026-04-17
update_date: 2026-04-17
issue: "#3"
---

# PRD #003 — AgentDevFlow gstack/superpower 能力增强层接入

## 1. 背景

AgentDevFlow 与 gstack、superpower 三个项目解决的问题层级不同：

- `gstack`：偏工具与任务工作流，增强单个 Agent 的执行能力
- `superpower`：偏通用方法论与执行模式，增强单个 Agent 的规划、拆解和协作能力
- `AgentDevFlow`：偏多 Agent 的交付流程层，定义 Issue / PRD / Tech / QA / Gate / Human Review / Release 的正式协作机制

当前 README.md 已明确三者差异，但尚未有正式决策：gstack / superpower 是否可以作为 AgentDevFlow 的能力增强层接入，以及如何接入。

关联讨论：`prompts/discuss/028_2026-04-14_gstack与superpower增强层接入方案.md`

## 2. 问题

当前 AgentDevFlow 缺少对 gstack / superpower 增强层的正式接入规范，导致：

- **接入决策模糊**：是否引入增强层、增强层与正式流程的关系未明确
- **边界不清晰**：增强层输出与正式交付物的关系未定义
- **各角色增强路径不明**：哪些角色在哪些阶段适合启用哪些增强能力未梳理

## 3. 目标

建立 AgentDevFlow 的"gstack/superpower 能力增强层"接入规范，包括定位声明、角色映射、边界约束，并落地到文档。

## 4. 范围

### 4.1 增强层定位声明

在 README.md 或平台接入文档中明确：

- `gstack / superpower` 作为 AgentDevFlow 的"能力插件层"，不替代 AgentDevFlow 本身的流程约束层
- 三者定位关系：工具层（gstack）+ 方法层（superpower）+ 流程层（AgentDevFlow）

### 4.2 角色增强映射

明确各角色在哪些阶段适合启用哪些增强能力：

| 角色 | 增强能力范围 | 适用阶段 | 来源 |
|------|------------|---------|------|
| Product Manager | brainstorming、方案评审增强 | 需求澄清、PRD 起草前 | superpower、gstack |
| Architect | 方案评审增强 | Tech Spec 起草前、技术方案评审前 | gstack、superpower |
| QA Engineer | 验证覆盖增强 | QA Case Design 后、QA 验证阶段 | gstack |
| Engineer | 代码审查增强、问题定位增强 | 开发前、修 Bug、代码 PR 前 | gstack |
| Team Lead | 流程改进增强 | 流程改进 | superpower、gstack |
| PMO | 流程审计增强 | 流程合规检查 | superpower、gstack |

### 4.3 增强层输出边界约束

明确增强层输出不能替代正式交付物：

- 增强能力生成的内容只能作为：分析过程、补充视角、评审建议、质量增强输入
- 不能替代以下正式交付物：PRD、Tech Spec、QA Case Design、QA Report、Issue Comment、正式评审结论

## 5. 非目标

- 不改造 AgentDevFlow 核心流程（Issue/Gate/PR/Human Review）
- 不将 gstack / superpower 作为 AgentDevFlow 的强依赖
- 不让增强能力输出替代正式 Gate 结论
- 不在本 PRD 中描述技术实现细节（技术选型、接口设计、代码方案）
- 不改造 AgentDevFlow 产生 gstack / superpower 之外的新流程能力边界

## 6. 用户故事

### US-1：谨慎接入者
> 作为 AgentDevFlow 用户，我希望在引入 gstack/superpower 增强能力前先了解它们与 AgentDevFlow 流程的关系，避免把增强工具当成流程替代品。

### US-2：渐进式启用者
> 作为 AgentDevFlow 用户，我希望安装 gstack/superpower 后自动获得增强能力，而不影响 AgentDevFlow 本体的独立运行能力。

### US-3：质量增强者
> 作为使用 AgentDevFlow 的 QA Engineer，我希望在 QA 阶段获得验证覆盖增强，同时不改变正式 QA 报告的约束。

## 7. 验收标准

### 7.1 定位声明

- [ ] README.md 或平台接入文档中明确增强层定位（三者定位关系已说明）
- [ ] 增强层"增强角色不替代角色"原则已声明

### 7.2 角色增强映射

- [ ] 各角色可选增强能力清单已梳理（6 个角色）
- [ ] 各角色增强能力的适用阶段已明确
- [ ] 各角色增强能力的来源（gstack/superpower）已标注

### 7.3 输出边界

- [ ] 增强层输出不能替代正式交付物的约束已声明
- [ ] "增强能力负责增强思考，正式文件负责流程留痕"的口径已明确

### 7.4 安装前置

- [ ] 增强层安装前置条件（gstack skill 包 + superpower skill 包）已写入平台接入文档

## 8. 风险

| 风险 | 影响 | 缓解 |
|------|------|------|
| 增强层输出被误当作正式交付物 | 高：Gate 检查被绕过 | 文档中明确边界约束，增强能力输出不计入 Gate 签字 |
| 文档口径与实际行为不一致 | 高：用户按文档操作后发现行为不符 | 文档变更需走 PR 评审 |

## 9. 依赖

- prompts/discuss/028_2026-04-14_gstack与superpower增强层接入方案.md（已有详细分析）
- README.md 当前内容（已包含三者差异 FAQ）

## 10. Gate 1 Review Record

| 日期 | 评审人 | 结论 | 关键意见 | 待办 |
|---|---|---|---|---|
| 2026-04-17 | PM | 起草完成，发起评审 | 符合新约束：禁止技术细节 | 等待 Architect + QA 签字 |
| 2026-04-17 | Architect | **Approved** ✅ | PRD v4 符合新约束：无技术选型/代码/接口/架构；Section 4 范围重构合理 | — |
| 2026-04-17 | QA | **Approved** ✅ | Section 7 验收标准覆盖完整，可测试性明确 | — |

### Gate 2 评审（跨文档追溯）

| 文档 | Tech Spec #003 v4 | QA Case #003 |
|------|-------------------|---------------|
| 状态 | Approved ✅ | Approved ✅ |
| Engineer 签字 | Approved | — |
| QA 签字 | Approved | Approved |
| PM 签字 | PM 确认 Tech Spec 覆盖 PRD v4 ✅ | PM 确认 QA Case 覆盖 PRD v4 ✅ |

---

## 11. 评审记录

| 日期 | 评审人 | 备注 | 决策 |
|---|---|---|---|
| 2026-04-17 | PM | PRD 起草（符合新约束：禁止技术细节）| Draft |
| 2026-04-17 | Architect | Gate 1 签字：Approved — 符合新约束，无技术选型/代码/接口/架构 | Approved |
| 2026-04-17 | QA | Gate 1 签字：Approved — Section 7 验收标准覆盖完整 | Approved |
