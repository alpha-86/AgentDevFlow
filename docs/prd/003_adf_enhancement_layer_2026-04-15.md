---
name: AgentDevFlow gstack/superpower 增强层接入
description: 明确 gstack / superpower 作为 AgentDevFlow 能力增强层的接入方式、开关语义、角色映射和边界约束
status: Draft
owner: Product Manager
date: 2026-04-15
update_date: 2026-04-15
version: v2
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
- **开关机制缺失**：无法按需开启/关闭增强能力
- **边界不清晰**：增强层输出与正式交付物的关系未定义
- **各角色增强路径不明**：哪些角色在哪些阶段适合启用哪些增强 skill 未梳理

## 3. 目标

建立 AgentDevFlow 的"gstack/superpower 能力增强层"接入规范，包括定位、开关语义、角色映射、边界约束，并落地到文档。

## 4. 范围

### 4.1 增强层定位声明

在 README.md 或平台接入文档中明确：

- `gstack / superpower` 作为 AgentDevFlow 的"能力插件层"，不替代 AgentDevFlow 本身的流程约束层
- 三者定位关系：工具层（gstack）+ 方法层（superpower）+ 流程层（AgentDevFlow）

### 4.2 增强层自动检测与回落机制

采用**自动检测 + 回落**机制，无需手动开关：

- **已安装 gstack**：AgentDevFlow 自动使用 gstack 相关 skill 进行能力增强
- **已安装 superpower**：AgentDevFlow 自动使用 superpower 相关 skill 进行能力增强
- **均未安装**：回落至 AgentDevFlow 原生机制，并提示用户建议安装 gstack 和 superpower

**技术语义**：
- 自动检测在角色 Agent 初始化时进行，无需用户手动配置
- 检测结果不写入配置文件，运行时判断，零持久化成本
- 回落到原生机制不影响任何核心流程运行
- 未安装时提示为建议性信息，不阻断任何操作

**设计理由**：自动检测比手动开关更符合"零配置接入"原则，降低用户认知负担，实现真正的渐进式增强。

### 4.3 角色增强映射

明确各角色在哪些阶段适合启用哪些增强 skill：

| 角色 | 可选增强 skill | 适用阶段 | 来源 |
|------|--------------|---------|------|
| Product Manager | brainstorming, plan-ceo-review | 需求澄清、PRD 起草前 | superpower / gstack |
| Architect | plan-eng-review, brainstorming | Tech Spec 起草前、技术方案评审前 | gstack / superpower |
| QA Engineer | qa-only, qa | QA Case Design 后、QA 验证阶段 | gstack |
| Engineer | review, investigate | 开发前、修 Bug、代码 PR 前 | gstack |
| Team Lead / PMO | brainstorming, plan-design-review, document-release | 流程改进、接入文档优化、发布后文档同步 | superpower / gstack |

> **注**：`plan-devex-review` 经 Engineer 验证不存在，已更正为 `plan-design-review`（gstack 中真实存在）。`brainstorming` 已在 PM 和 Architect 列表中（来自 superpower）。其他 skill 名称以 Engineer 最终验证为准。

### 4.4 增强层输出边界约束

明确增强层输出不能替代正式交付物：

- skill 生成的内容只能作为：分析过程、补充视角、评审建议、质量增强输入
- 不能替代以下正式交付物：PRD、Tech Spec、QA Case Design、QA Report、Issue Comment、正式评审结论

### 4.5 安装前置说明

在平台接入文档中补充增强层安装前置条件说明。

## 5. 非目标

- 不改造 AgentDevFlow 核心流程（Issue/Gate/PR/Human Review）
- 不将 gstack / superpower 作为 AgentDevFlow 1.0 的强依赖（未安装时必须回落）
- 不让 skill 输出替代正式 Gate 结论
- 不在本次实现手动配置的增强层开关（采用自动检测，无需用户配置）
- 不改造 AgentDevFlow 产生 gstack / superpower 之外的新流程能力边界

## 6. 用户故事

### US-1：谨慎接入者
> 作为 AgentDevFlow 用户，我希望在引入 gstack/superpower 增强能力前先了解它们与 AgentDevFlow 流程的关系，避免把增强工具当成流程替代品。

### US-2：分阶段启用者
> 作为 AgentDevFlow 用户，我希望能够按需开启增强层，而不影响 AgentDevFlow 本体的独立运行能力。

### US-3：质量增强者
> 作为使用 AgentDevFlow 的 QA Engineer，我希望在 QA 阶段获得 gstack-qa 的验证覆盖增强，同时不改变正式 QA 报告的约束。

## 7. 验收标准

### 7.1 定位声明

- [ ] README.md 或平台接入文档中明确增强层定位（三者定位关系已说明）
- [ ] 增强层"增强角色不替代角色"原则已声明

### 7.2 自动检测与回落机制

- [ ] 自动检测逻辑已实现（角色初始化时检测 gstack / superpower 是否已安装）
- [ ] gstack 已安装时，相关角色自动使用 gstack 增强 skill
- [ ] superpower 已安装时，相关角色自动使用 superpower 增强 skill
- [ ] 均未安装时，回落至原生机制，不报错不阻断
- [ ] 均未安装时，提示用户建议安装 gstack 和 superpower

### 7.3 角色增强映射

- [ ] 各角色可选增强 skill 清单已梳理（5 个角色的增强路径）
- [ ] 各角色增强 skill 的适用阶段已明确

### 7.4 输出边界

- [ ] 增强层输出不能替代正式交付物的约束已声明
- [ ] "skill 负责增强思考，正式文件负责流程留痕"的口径已明确

### 7.5 安装前置

- [ ] 增强层安装前置条件（gstack skill 包 + superpower skill 包）已写入平台接入文档

## 8. 风险

| 风险 | 影响 | 缓解 |
|------|------|------|
| 增强层输出被误当作正式交付物 | 高：Gate 检查被绕过 | 文档中明确边界约束，skill 输出不计入 Gate 签字 |
| 文档口径与实际行为不一致 | 高：用户按文档操作后发现行为不符 | 文档变更需走 PR 评审 |

## 9. 依赖

- prompts/discuss/028_2026-04-14_gstack与superpower增强层接入方案.md（已有详细分析）
- README.md 当前内容（已包含三者差异 FAQ）
- prompts/discuss/016_phase_5_3 和 016_phase_5_2（gstack/superpower 能力分析）

## 10. 评审记录

| 日期 | 评审人 | 备注 | 决策 |
|---|---|---|---|
| 2026-04-15 | PM | PRD 草稿 | Draft |
| 2026-04-15 | Team Lead | Gate 1 Review v1 — 5 个交付域边界清晰，输出边界约束合理 | **Approved** ✅ |
| 2026-04-15 | PM | PRD 迭代 v2 — Scope changed: 手动开关→自动检测，含代码实现 | v2 |
| 2026-04-15 | PM | Gate 1 重新评审请求 — v1→v2 性质变更，需三方重签 | 待评审 |
| 2026-04-15 | PM | Skill 名称修正：plan-devex-review → plan-design-review（Engineer 验证） | v2.1 |
| 2026-04-15 | QA Engineer | Gate 1 Re-review v2 — Section 4.2 自动检测+回落机制合理，零配置设计满足用户需求，Section 7.2 验收标准可测试 | **Approved** ✅ |
