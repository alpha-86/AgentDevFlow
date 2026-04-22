---
name: 职责归属矩阵与 Gate 2 签字规范补齐
description: 补齐 AgentDevFlow 正式交付物职责归属矩阵，收敛 Gate 2 签字规则与 Gate 定义口径，作为 Issue #16 的当前有效 Gate 1 输入
status: Draft
owner: Product Manager
date: 2026-04-21
update_date: 2026-04-21
issue: "#16"
---

# PRD #016 — 职责归属矩阵与 Gate 2 签字规范补齐

## 1. 背景

Issue #16 指向的核心问题是：AgentDevFlow 当前缺少一份可直接执行的正式交付物职责归属矩阵，导致 PRD、Tech Spec、QA Case、代码与测试报告等交付物的产出者、评审者、签字边界不够清晰，并进一步暴露出 Gate 2 self-review 与 Gate 定义分叉问题。

## 2. 问题

当前项目存在以下三个直接问题：

- **职责归属矩阵缺失**：交付物的产出角色、评审角色与评审立场未形成统一矩阵
- **Gate 2 签字规范不清**：Architect 评审自己产出的 Tech Spec，造成 self-review 风险
- **Gate 定义不一致**：不同文档中 Gate 口径存在分叉，影响流程一致性

## 3. 目标

形成当前有效的产品层需求定义，明确：

1. 正式交付物职责归属矩阵必须存在且可追溯
2. Gate 2 签字规则必须避免产出者自评审
3. Gate 定义口径必须统一到当前有效流程文档
4. 后续文档与 workflow 修订应以该 PRD 为上游输入

## 4. 范围

### 4.1 职责归属矩阵

明确以下交付物的职责边界：
- PRD
- Tech Spec
- QA Case Design
- 代码实现
- QA Report / 测试报告
- Gate 结论 / Human Review 结论

对每类交付物至少明确：
- 产出角色
- 必需评审角色
- 是否允许产出者自评审
- 结论留痕位置

### 4.2 Gate 2 签字规范

- 明确 Gate 2 的合法评审组合与签字边界
- 明确 Tech Spec 产出者不得作为自己的独立评审签字人
- 明确 PM / QA / Engineer 在 Gate 2 中的评审职责边界

### 4.3 Gate 定义口径统一

- 收敛不同文档中的 Gate 定义冲突
- 统一到当前有效流程文档口径
- 保证后续 issue 按同一 Gate 语义推进

## 5. 非目标

- 不在本 PRD 中展开具体实现 diff
- 不一次性改造所有 workflow 细节
- 不把历史治理留档直接当作当前有效 PRD / Tech / QA 输入

## 6. 用户故事

### US-1：交付参与者
> 作为项目成员，我希望知道每类交付物由谁产出、谁评审、谁签字，这样可以避免责任混乱和返工。

### US-2：流程审核者
> 作为流程审核者，我希望 Gate 2 的合法签字边界清晰，避免 self-review 被误当作合规。

## 7. 验收标准

- [ ] 至少覆盖 PRD / Tech / QA Case / 代码 / QA Report / Gate 结论六类正式交付物的职责矩阵
- [ ] 每类交付物都明确产出角色、评审角色与是否允许自评审
- [ ] Gate 2 的合法签字边界已明确，且禁止 Tech Spec 产出者自评审
- [ ] Gate 定义冲突已识别，并明确统一到当前有效流程口径
- [ ] 本 issue 已按严格研发交付流程重新进入 Gate 1，而非直接复用历史治理结论

## 8. 风险

| 风险 | 影响 | 缓解 |
|------|------|------|
| 职责矩阵只写原则、不具可执行性 | 高 | 以交付物维度列出明确角色与留痕位置 |
| Gate 2 规范修复不彻底 | 高 | 在 PRD 中显式禁止 self-review，并在 Tech / QA 继续细化 |
| Gate 定义统一后与现有文档冲突 | 中 | 统一回链当前有效流程文档，触发后续文档修订 |

## 9. 依赖

- `docs/pmo/resolutions/009_2026-04-17_governance_role_attribution_and_gate2_signatory_resolution.md`
- 当前有效流程文档与 Gate 定义文档
- Issue #16 当前讨论上下文

## 10. 评审记录

| 日期 | 评审人 | 备注 | 决策 |
|---|---|---|---|
| 2026-04-21 | PM | 按严格研发交付流程重新启动 #16，起草当前有效 PRD | Draft |
