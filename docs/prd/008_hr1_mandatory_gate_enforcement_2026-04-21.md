---
name: Human Review #1 强制执行与 Gate 顺序固化
description: 将 HR#1 不可跳过及 Gate 2 到后续阶段的顺序约束重新固化为当前有效研发交付需求，作为 Issue #8 的 Gate 1 输入
status: Draft
owner: Product Manager
date: 2026-04-21
update_date: 2026-04-21
issue: "#8"
---

# PRD #008 — Human Review #1 强制执行与 Gate 顺序固化

## 1. 背景

Issue #8 指向的核心问题是：项目曾出现 Gate 2 通过后直接越过 Human Review #1 的违规推进，错误地把“纯文档交付”理解为可跳过 HR#1 的理由，导致正式研发交付流程断裂。

当前需要将该约束重新固化为当前有效产品输入，确保后续所有 issue 都按统一口径执行。

## 2. 问题

当前 AgentDevFlow 在流程认知与工作流文档上仍存在以下风险：

- **HR#1 强制性表达不足**：部分场景中仍可能被误读为可选环节
- **Gate 顺序约束不够统一**：Gate 2 后进入 HR#1，再进入下游阶段的顺序需要以当前有效输入重新确认
- **历史结论复用风险**：不能仅依赖历史治理结论，必须重新走严格研发交付流程形成当前有效产物

## 3. 目标

形成当前有效的 HR#1 强制执行需求定义，明确：

1. Human Review #1 是 Gate 2 后的强制环节
2. 不区分纯文档交付 / 纯代码交付 / 混合交付
3. Gate 顺序必须满足 Gate 2 → HR#1 → 下游阶段
4. 相关 prompts / workflow 文档需要按统一口径更新

## 4. 范围

### 4.1 HR#1 强制性口径

- 明确 HR#1 不可跳过
- 明确不存在因交付类型不同而跳过 HR#1 的分支
- 明确 HR#1 评审对象为文档阶段正式交付物

### 4.2 Gate 顺序固化

- 明确 Gate 2 完成后必须先进入 HR#1
- 明确未完成 HR#1 前不得推进到后续实现 / 验证 / 发布阶段
- 明确相关状态推进语义不能绕过 HR#1

### 4.3 文档与工作流更新范围

- `prompts/017_human_review_and_signoff.md`
- `prompts/004_delivery_gates.md`
- `skills/shared/workflows/human-review.md` 或其当前有效对应源文件

## 5. 非目标

- 不在本 PRD 中直接展开具体代码实现细节
- 不改造与 HR#1 无关的其他 Gate 机制
- 不把历史 GOV-004 留档直接视为本轮当前有效交付物

## 6. 用户故事

### US-1：流程执行者
> 作为 AgentDevFlow 使用者，我希望明确知道 HR#1 是 Gate 2 后的强制环节，这样就不会因为交付类型判断错误而跳过正式评审。

### US-2：Team Lead / 审核者
> 作为流程审核者，我希望状态推进规则明确，避免 Gate 状态被错误推进到下游阶段。

## 7. 验收标准

- [ ] 文档明确声明 HR#1 不可跳过
- [ ] 文档明确声明 HR#1 与交付类型无关
- [ ] 文档明确声明 Gate 2 → HR#1 → 下游阶段的强制顺序
- [ ] 相关 prompts / workflow 更新范围已被识别并可追溯
- [ ] 当前 issue 按严格研发交付流程重新进入 Gate 1，而非直接复用历史结论

## 8. 风险

| 风险 | 影响 | 缓解 |
|------|------|------|
| 团队继续引用历史治理结论替代当前交付 | 高 | 明确本 issue 必须重新走 PRD / Tech / QA / HR#1 链路 |
| HR#1 规则只在单一文档中更新 | 中 | 在 prompts 与 workflow 双侧同步固化 |
| 状态机仍可能被误推进 | 高 | 在 Gate 顺序文档中显式写入禁止绕过约束 |

## 9. 依赖

- `docs/pmo/issues/008_2026-04-16_governance_issue3_hr1_skipped.md`
- `docs/pmo/resolutions/GOV-004_2026-04-16_issue3_hr1_skipped_resolution.md`
- 当前有效流程文档与 human-review 工作流文档

## 10. 评审记录

| 日期 | 评审人 | 备注 | 决策 |
|---|---|---|---|
| 2026-04-21 | PM | 按 Team Lead 指令重新启动严格研发交付流程，起草当前有效 PRD | Draft |
