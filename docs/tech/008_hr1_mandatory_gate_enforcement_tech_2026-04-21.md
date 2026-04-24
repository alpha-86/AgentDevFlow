---
name: Human Review #1 强制执行与 Gate 顺序固化 — Tech Spec v1
description: 基于 PRD #008 的当前有效 Tech Spec，定义 HR#1 不可跳过与 Gate 2 后顺序固化在 prompts / workflow / CI 参考文档中的技术落点与验证路径
status: Draft
owner: Architect
date: 2026-04-21
update_date: 2026-04-21
issue: "#8"
prd: docs/prd/008_hr1_mandatory_gate_enforcement_2026-04-21.md
---

# Tech Spec #008 — Human Review #1 强制执行与 Gate 顺序固化（v1）

---

**ID**: Tech-8_v1
**状态**: Draft
**负责人**: Architect
**日期**: 2026-04-21
**更新日期**: 2026-04-21
**基于**: PRD #008（Draft 已经通过 Gate 1，2026-04-21）
**当前评审状态**: 待发起 Gate 2 Tech Review（PM + QA + Engineer）

---

## 上下文

Issue #8 的目标不是新增流程能力，而是把已经被证明不可缺失的 HR#1 约束重新固化为当前有效研发交付输入，防止以下错误再次发生：

1. 把“纯文档交付”误解为可以跳过 Human Review #1
2. 在 Gate 2 后直接推进到下游实现 / 验证 / 发布阶段
3. 只引用历史治理结论，而不形成当前有效交付物

本 Tech Spec 将 PRD #008 的产品层需求落到当前仓库的规则文件、工作流文件和 CI 参考文档更新面。

## 架构

### 1. 规则固化范围

本次技术落点限定在以下当前有效源文件：

- `prompts/017_human_review_and_signoff.md`
- `prompts/004_delivery_gates.md`
- `skills/workflows/human-review.md`

如发现 bootstrap 产物存在对应镜像文件，仅通过源文件更新，不直接修改产物文件。

### 2. 需要固化的统一技术语义

所有目标文件必须统一承接以下语义：

- **HR#1 不可跳过**
- **HR#1 与交付类型无关**；纯文档交付不是跳过 HR#1 的理由
- **开发交付强制顺序**：Gate 2 → Human Review #1 → Gate 3 / Gate 4 / HR#2 / Gate 5
- **纯文档交付强制顺序**：Gate 2 → Human Review #1 → Release / Issue Close
- **历史治理结论仅能作为背景，不得替代当前 Issue 的正式交付物**

### 3. 文件级技术责任

| 文件 | 技术责任 |
|---|---|
| `prompts/017_human_review_and_signoff.md` | 定义 HR#1 的对象、强制性、禁止绕过规则、HR#1 后的正式推进路径 |
| `skills/workflows/human-review.md` | 固化工作流步骤、失败信号、开发交付路径与纯文档交付路径 |
| `prompts/004_delivery_gates.md` | 作为 CI 参考附录，明确 Gate 2、HR#1、下游阶段的映射和检查口径 |

### 4. 最小修改原则

本次只做 #8 所需的最小收口，不扩展到：

- 其他与 HR#1 无关的 Gate 机制
- 新 workflow 新脚本
- 额外 CI 自动化能力

## 接口

### 输入

- PRD #008：`docs/prd/008_hr1_mandatory_gate_enforcement_2026-04-21.md`
- 当前 human-review 相关 prompts / workflow 文本
- GOV-004 背景留档（仅作追溯，不作当前结论替代）

### 输出

- 当前有效 Tech Spec #008
- 后续 QA Case Design #008
- 三个目标文件中的统一规则修订

## 数据流

```text
PRD #008 Gate 1 Approved
    ↓
Tech Spec #008 Draft / Gate 2 Review
    ↓
QA Case Design #008
    ↓
更新 prompts/017 + prompts/004 + skills/workflows/human-review
    ↓
文档 PR（HR#1）
```

## 可测试性

QA 可基于本 Tech Spec 直接派生以下验证面：

1. **强制性验证**
   - 文档明确写出 HR#1 不可跳过
   - 不存在按交付类型跳过 HR#1 的分支描述

2. **顺序验证**
   - 开发交付路径明确为 Gate 2 → HR#1 → 下游阶段
   - 纯文档交付路径明确为 Gate 2 → HR#1 → Release / Issue Close

3. **一致性验证**
   - `prompts/017_human_review_and_signoff.md`
   - `skills/workflows/human-review.md`
   - `prompts/004_delivery_gates.md`
   三处口径一致，无互相冲突

4. **历史结论隔离验证**
   - 文本中未将 GOV-004 历史结论写成当前自动通过前提
   - 当前 Issue 仍需走完整 PRD / Tech / QA / HR#1 链路

## 风险

| 风险 | 级别 | 缓解 |
|---|---|---|
| 规则只在单一文件更新，其他文件继续漂移 | 高 | 将 3 个目标文件纳入同一交付范围 |
| “纯文档交付”语义再次被误读 | 高 | 在 prompts 与 workflow 中同时写明“纯文档交付也必须经过 HR#1” |
| CI 参考附录与主规则口径不一致 | 中 | `prompts/004_delivery_gates.md` 仅保留与唯一源一致的参考描述 |
| 历史治理结论再次被误当作当前有效输入 | 中 | 在 QA Case 与后续评审中单独验证“历史仅留档” |

## 发布推进

1. Gate 2 通过后，QA 起草 #8 QA Case Design
2. QA Case 通过后，修改目标 prompts / workflow 源文件
3. 形成文档 PR，进入 Human Review #1
4. HR#1 通过并合并后，按交付类型进入下游 Release 或后续阶段

## 回滚

- 若发现三文件口径不一致，回退到文档修订阶段重新统一
- 若某条规则会影响其他现行主线，以 `prompts/002_develop_pipeline.md` 的唯一源定义为裁决基准
- 若 CI 参考附录表述超出主规则定义，删除扩展表达，仅保留引用性说明

## 评审记录

| 日期 | 评审人 | 备注 | 决策 |
|---|---|---|---|
| 2026-04-21 | Architect | 基于已通过 Gate 1 的 PRD #008 起草当前有效 Tech Draft | Draft |

## 版本历史

| 版本 | 日期 | 变更说明 | 变更人 |
|------|------|---------|-------|
| v1 | 2026-04-21 | 首次起草 #8 当前有效 Tech Spec Draft | Architect |

## 前序文档追溯链

基于：`docs/prd/008_hr1_mandatory_gate_enforcement_2026-04-21.md`
Tech Spec 依赖：PRD #008 Gate 1 Approved

## 评审记录表

| 评审日期 | 评审节点 | 评审结果 | 评审人 | 意见/打回原因 | 修改后版本 |
|----------|---------|---------|-------|-------------|-----------|
| 2026-04-21 | Gate 2 | 待评审 | PM + QA + Engineer | — | v1 |
