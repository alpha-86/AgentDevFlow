---
name: AgentDevFlow gstack/superpower 增强层接入
description: 明确 gstack / superpower 作为 AgentDevFlow 能力增强层的接入方式、角色映射和边界约束
status: In Review
owner: Product Manager
date: 2026-04-17
update_date: 2026-04-21
issue: "#3"
---

# PRD #003 v4.3 — AgentDevFlow gstack/superpower 能力增强层接入

> **当前状态说明**：Issue #3 已按用户要求从暂停恢复，并正式回退到 **Gate 1: PRD Review**。本版本为 GOV-011 后、结合 Human 最新确认的返工修订版本；旧 Gate 2 / QA Case 状态仅作为历史记录，不再作为当前有效前提。

## 0. 本轮 Gate 1 当前确认口径

### D1. 增强层依赖语义

本轮 Gate 1 的当前唯一口径如下：

- **安装增强层后 = 强制依赖**
  - 一旦用户安装增强层，即默认开启并在适用 Gate 强制使用 gstack / superpower
  - 不存在“安装后仍按场景选择是否启用”的可选分支
- **未安装增强层时 = 回落 AgentDevFlow 原生机制**
  - 未安装时不阻断主流程
  - 仍按 AgentDevFlow 原生机制运行

### D2. 角色增强映射执行强度

本轮 Gate 1 的当前唯一口径如下：

- 在适用 Gate 中，已安装增强层的相关角色按 **强制执行** 处理
- 不再保留“推荐使用”分支作为当前需求口径

> 在新的 Gate 1 评审结论完成前，当前阶段仍仅限 **Gate 1: PRD Review**，不得进入 Gate 2 Tech Review / QA Case Design。

## 1. 背景

AgentDevFlow 与 gstack、superpower 三个项目解决的问题层级不同：

- `gstack`：偏工具与任务工作流，增强单个 Agent 的执行能力
- `superpower`：偏通用方法论与执行模式，增强单个 Agent 的规划、拆解和协作能力
- `AgentDevFlow`：偏多 Agent 的交付流程层，定义 Issue / PRD / Tech / QA / Gate / Human Review / Release 的正式协作机制

当前 README.md 已明确三者差异，但尚未有正式接入规范，来定义 gstack / superpower 作为 AgentDevFlow 能力增强层时的定位、强制语义与边界约束。

关联讨论：`prompts/discuss/028_2026-04-14_gstack与superpower增强层接入方案.md`

## 2. 问题

当前 AgentDevFlow 缺少对 gstack / superpower 增强层的正式接入规范，导致：

- **接入语义不清**：安装后是否必须启用、未安装时如何回落未被正式定义
- **边界不清晰**：增强层输出与正式交付物的关系未定义
- **各角色增强路径不明**：哪些角色在哪些阶段必须使用哪些增强能力未梳理

## 3. 目标

建立 AgentDevFlow 的“gstack/superpower 能力增强层”接入规范，包括定位声明、角色映射、边界约束，并落地到文档。

## 4. 范围

### 4.1 增强层定位声明

在 README.md 或平台接入文档中明确：

- `gstack / superpower` 作为 AgentDevFlow 的“能力插件层”，不替代 AgentDevFlow 本身的流程约束层
- 三者定位关系：工具层（gstack）+ 方法层（superpower）+ 流程层（AgentDevFlow）
- **开关语义**：安装增强层后按强制依赖处理；未安装时回落 AgentDevFlow 原生机制
- 在新的 Gate 1 评审结论完成前，不得据此进入 Gate 2

### 4.2 角色增强映射

明确各角色在哪些 Gate 阶段使用增强能力；已安装增强层时，在适用 Gate 中按强制执行处理：

| 角色 | 增强能力范围 | 适用 Gate | 来源 |
|------|------------|---------|------|
| Product Manager | brainstorming、方案评审增强 | Gate 0（启动）/ Gate 1（PRD 评审前）| superpower、gstack |
| Architect | 方案评审增强 | Gate 2（Tech Spec 起草前）/ HR#1（设计评审）| gstack、superpower |
| QA Engineer | 验证覆盖增强 | Gate 4（QA 验证阶段）/ HR#2（实现确认）| gstack |
| Engineer | 代码审查增强、问题定位增强 | Gate 3（开发阶段）/ 修 Bug / 代码 PR 前 | gstack |
| Team Lead | 流程改进增强 | Gate 0（团队启动）/ Gate 5（发布评审）| superpower、gstack |
| PMO | 流程审计增强 | Gate 0 / Gate 5 / 流程合规检查 | superpower、gstack |

### 4.3 增强层输出边界约束

明确增强层输出不能替代正式交付物：

- 增强能力生成的内容只能作为：分析过程、补充视角、评审建议、质量增强输入
- 不能替代以下正式交付物：PRD、Tech Spec、QA Case Design、QA Report、Issue Comment、正式评审结论

## 5. 非目标

- 不改造 AgentDevFlow 核心流程（Issue/Gate/PR/Human Review）
- 不在本 PRD 中描述技术实现细节（技术选型、接口设计、代码方案）
- 不改造 AgentDevFlow 产生 gstack / superpower 之外的新流程能力边界
- 不引入“安装后可选启用”或“推荐执行”作为本轮已确认需求分支

## 6. 用户故事

### US-1：增强语义确认者
> 作为 AgentDevFlow 用户，我希望明确增强层安装后的真实语义是强制依赖 / 强制执行，未安装时才回落原生机制，以避免文档与实际行为不一致。

### US-2：无缝回落者
> 作为 AgentDevFlow 用户，我希望在未安装增强层时自动回落 AgentDevFlow 原生机制，不需要任何配置即可正常运行。

### US-3：质量增强者
> 作为使用 AgentDevFlow 的 QA Engineer，我希望在 QA 阶段获得验证覆盖增强，同时不改变正式 QA 报告的约束。

## 7. 验收标准

### 7.1 定位声明

- [ ] README.md 或平台接入文档中明确增强层定位（三者定位关系已说明）
- [ ] 增强层“增强角色不替代角色”原则已声明
- [ ] 增强层依赖语义已明确：安装后强制依赖，未安装时回落原生机制，且表达一致

### 7.2 角色增强映射

- [ ] 各角色增强能力清单已梳理（6 个角色）
- [ ] 各角色增强能力的适用 Gate 阶段已明确
- [ ] 各角色增强能力的来源（gstack/superpower）已标注
- [ ] 已明确这些增强能力在已安装增强层时按“强制执行”处理

### 7.3 输出边界

- [ ] 增强层输出不能替代正式交付物的约束已声明
- [ ] “增强能力负责增强思考，正式文件负责流程留痕”的口径已明确

### 7.4 安装前置

- [ ] 增强层安装前置条件（gstack skill 包 + superpower skill 包）已写入平台接入文档
- [ ] 已说明安装后行为、回落方式与失败场景
- [ ] 已说明未安装时按原生机制运行，不阻断主流程

## 8. 风险

| 风险 | 影响 | 缓解 |
|------|------|------|
| 增强层输出被误当作正式交付物 | 高：Gate 检查被绕过 | 文档中明确边界约束，增强能力输出不计入 Gate 签字 |
| 用户误解安装后仍可选择关闭增强层 | 高：安装后行为与预期不符 | 在 Gate 1 明确唯一口径，并同步 README / 平台文档 |
| 文档口径与实际行为不一致 | 高：用户按文档操作后发现行为不符 | 文档变更需走 PRD Review，不允许跳过 Gate 1 |

## 9. 依赖

- `prompts/discuss/028_2026-04-14_gstack与superpower增强层接入方案.md`
- README.md 当前内容（已包含三者差异 FAQ）
- Issue #3 当前讨论上下文与 Human 最新确认

## 10. Gate 1 Review Record

| 日期 | 评审人 | 结论 | 关键意见 | 待办 |
|---|---|---|---|---|
| 2026-04-17 | PM | 起草完成，发起评审 | 符合新约束：禁止技术细节 | 等待 Architect + QA 签字 |
| 2026-04-17 | Architect | **Approved** ✅ | PRD v4 符合新约束：无技术选型/代码/接口/架构；Section 4 范围重构合理 | — |
| 2026-04-17 | QA | **Approved** ✅ | Section 7 验收标准覆盖完整，可测试性明确 | — |
| 2026-04-20 | PM | HR#1 迭代 — v4.1 | 引入 Gate 0~5 增强映射及“强制依赖/强制增强”口径 | 该版本因 GOV-011 回退，不作为当前有效前提 |
| 2026-04-21 | PM | PRD 返工 — v4.2 | 正式回退到 Gate 1；将依赖语义与增强强制性列为本轮核心决策点 | 等待 PM + Architect + QA 重新评审 |
| 2026-04-21 | PM | PRD 最小修订 — v4.3 | 已按 Human 最新确认统一为“安装后强制依赖 / 强制执行，未安装时回落原生机制” | 等待重新发起 Gate 1 三方评审 |

### 历史 Gate 2 / QA Case 记录（仅留档，不作为当前有效前提）

| 文档 | 历史状态 | 说明 |
|------|---------|------|
| Tech Spec #003 v4 | Approved（历史） | 因 Issue #3 已回退到 Gate 1，本记录仅保留追溯，不作为当前 Tech Review 准入依据 |
| QA Case #003 | Approved（历史） | 因 Issue #3 已回退到 Gate 1，本记录仅保留追溯，不作为当前 QA Case Design 准入依据 |

## 11. 评审记录

| 日期 | 评审人 | 备注 | 决策 |
|---|---|---|---|
| 2026-04-17 | PM | PRD 起草（符合新约束：禁止技术细节） | Draft |
| 2026-04-17 | Architect | Gate 1 签字：Approved — 符合新约束，无技术选型/代码/接口/架构 | Approved |
| 2026-04-17 | QA | Gate 1 签字：Approved — Section 7 验收标准覆盖完整 | Approved |
| 2026-04-20 | PM | PRD v4.1 迭代（HR#1 反馈）：补 Gate 映射与强制依赖口径 | In Review |
| 2026-04-21 | PM | GOV-011 后返工：Issue #3 正式回退到 Gate 1，重置 PRD Review 输入；旧 Gate 2 / QA Case 仅作历史留档 | In Review |
| 2026-04-21 | PM | Gate 1 Rejected 后最小修订：删除可选增强 / 推荐执行分支，统一为唯一已确认口径 | In Review |

## 12. 本轮 Gate 1 进入条件

- [x] PRD 当前版本已作为本轮正式评审输入回写到 Issue #3
- [x] PM 已在 Issue #3 评论中声明：当前阶段 = Gate 1: PRD Review
- [x] Human 最新确认已明确：安装后按强制依赖 / 强制执行处理，未安装时回落原生机制
- [x] 旧 Gate 2 / QA Case 状态已明确不作为当前有效前提
- [ ] 待重新发起新的 Gate 1 三方评审入口（PM + Architect + QA）

## 13. 当前阻塞

- 缺新的 Gate 1 三方评审结论
- 在新的 Gate 1 评审结论完成前，不进入 Tech Review / QA Case Design

## 14. Review Record

- 2026-04-21：本版本为 Gate 1 返工后的最小修订版本（v4.3），用于重新进入 PRD Review。当前不具备进入 Gate 2 的条件。

## 15. 版本历史

| 版本 | 日期 | 变更说明 | 变更人 |
|------|------|---------|-------|
| v4.0 | 2026-04-17 | Gate 1 首轮通过版本 | PM |
| v4.1 | 2026-04-20 | HR#1 反馈后迭代，补 Gate 映射与强制依赖口径 | PM |
| v4.2 | 2026-04-21 | 因 GOV-011 回退到 Gate 1，重置为返工评审输入，显式列出核心待决策点 | PM |
| v4.3 | 2026-04-21 | 按 Rejected 意见做最小修订，统一为“安装后强制依赖 / 强制执行，未安装时回落原生机制” | PM |

前序文档追溯链：
`PRD v4.3 -> Tech Spec（待重置） -> QA Case（待重置）`

后续 Gate 1 通过后，Tech Spec 与 QA Case 必须基于 v4.3 重新确认，不得直接沿用历史 Approved 结果。

## 16. Review Record 表

| 日期 | 阶段 | 评审人 | 结论 | 关键意见 | 待办与负责人 | 下次复审时间 |
|------|------|--------|------|---------|-------------|-------------|
| 2026-04-21 | PRD | PM | In Review | 已按拒绝意见完成最小修订，待重新发起 PM+Architect+QA 三方评审 | 组织 Gate 1 重审（Team Lead） | 待定 |

## 17. 文档状态机记录

- 当前有效 PRD 输入版本：v4.3
- 当前有效阶段：Gate 1: PRD Review
- 旧 Gate 2 / QA Case 结论：历史留档，不得作为当前下游阶段输入
- 当前禁止进入：Tech Review、QA Case Design、Implementation

## 18. 本轮待确认问题

1. 在当前唯一确认口径下，README / 平台接入文档应如何准确表达安装前置、强制启用与原生回落机制？
2. 在当前唯一确认口径下，边界约束与正式交付物替代限制是否表达充分，可供 Gate 1 通过后进入下游重置？

这些问题仅作为 Gate 1 当前评审关注点；在新的 Gate 1 评审结论完成前，仍不进入下一阶段。
