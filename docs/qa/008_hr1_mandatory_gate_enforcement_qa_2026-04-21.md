---
name: Human Review #1 强制执行与 Gate 顺序固化 — QA Case Design v1
description: 基于 PRD #008 与 Tech-8_v1 的当前有效 QA Case Draft，定义 HR#1 不可跳过与 Gate 顺序固化在 prompts/workflow 中的验证用例
status: Draft
owner: QA Engineer
date: 2026-04-22
update_date: 2026-04-22
issue: "#8"
prd: docs/prd/008_hr1_mandatory_gate_enforcement_2026-04-21.md
tech: docs/tech/008_hr1_mandatory_gate_enforcement_tech_2026-04-21.md
---

# QA Case Design #008 — Human Review #1 强制执行与 Gate 顺序固化

---

## 当前有效状态

- **当前有效版本**：v1 Draft
- **当前有效输入**：PRD #008 + Tech Spec #008 v1
- **当前阶段**：QA Case Design（待 PM + Architect + Engineer 三方评审）
- **规则说明**：本文件为 Issue #8 的当前有效 QA Case Draft，仅绑定当前仓库内已落地的 PRD 与 Tech 输入

## 追溯关系

- **PRD**: `docs/prd/008_hr1_mandatory_gate_enforcement_2026-04-21.md`
- **Tech Spec**: `docs/tech/008_hr1_mandatory_gate_enforcement_tech_2026-04-21.md`

### PRD #008 → QA Case 追溯矩阵

| PRD Section | 对应 TC | 覆盖状态 |
|-------------|---------|---------|
| 7.1 HR#1 不可跳过 | TC-8-01, TC-8-02, TC-8-03 | ✅ |
| 7.2 HR#1 与交付类型无关 | TC-8-02, TC-8-04 | ✅ |
| 7.3 Gate 2 → HR#1 → 下游阶段 | TC-8-03, TC-8-05 | ✅ |
| 7.4 文档与工作流更新范围 | TC-8-06, TC-8-07, TC-8-08 | ✅ |
| 7.5 历史治理结论隔离 | TC-8-09 | ✅ |

### Tech Spec #008 → QA Case 追溯矩阵

| Tech Spec Section | 对应 TC | 覆盖状态 |
|-------------------|---------|---------|
| 规则固化范围 | TC-8-06, TC-8-07, TC-8-08 | ✅ |
| 统一技术语义 | TC-8-01, TC-8-02, TC-8-03, TC-8-04, TC-8-05 | ✅ |
| 文件级技术责任 | TC-8-06, TC-8-07, TC-8-08 | ✅ |
| 最小修改原则 | TC-8-10 | ✅ |

---

## TC-8-01：HR#1 不可跳过 — 主规则验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-8-01 |
| 标题 | HR#1 不可跳过主规则验证 |
| 追溯 | PRD 7.1 HR#1 强制性；Tech Spec 统一技术语义 |
| 前置条件 | `prompts/017_human_review_and_signoff.md`、`skills/workflows/human-review.md` 已更新 |
| 测试步骤 | 在上述两份文件中搜索“不可跳过”“强制”“不得跳过”“不存在跳过”等关键词 |
| 预期结果 | 文件明确写出 Human Review #1 不可跳过的强制规则 |
| 验证方法 | 文档搜索 |
| 优先级 | P1 |

---

## TC-8-02：HR#1 与交付类型无关 — 纯文档交付分支验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-8-02 |
| 标题 | HR#1 与交付类型无关验证 |
| 追溯 | PRD 7.2 / 不区分交付类型；Tech Spec 统一语义 |
| 前置条件 | `prompts/017_human_review_and_signoff.md`、`skills/workflows/human-review.md` 已更新 |
| 测试步骤 | 1. 搜索“纯文档交付”“与交付方式无关”“*md 文档是实现层”“不是跳过理由”等关键词<br>2. 检查是否存在按交付类型决定是否跳过 HR#1 的分支描述 |
| 预期结果 | 文档明确说明 HR#1 评审对象与交付方式无关，纯文档交付也必须经过 HR#1；不存在“纯文档可跳过”的分支 |
| 验证方法 | 文档搜索 + 反例排除 |
| 优先级 | P1 |

---

## TC-8-03：开发交付路径顺序验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-8-03 |
| 标题 | 开发交付路径 Gate 2 → HR#1 → 下游阶段顺序验证 |
| 追溯 | PRD 7.3 Gate 顺序固化；Tech Spec 统一技术语义 |
| 前置条件 | 目标文档已更新 |
| 测试步骤 | 在三份目标文档中搜索 Gate 顺序描述：检查是否包含 Gate 2 → Human Review #1 → Gate 3 的链式推进描述 |
| 预期结果 | 开发交付路径明确为 Gate 2 → HR#1 → Gate 3 → Gate 4 → HR#2 → Gate 5，无跳过或颠倒顺序的描述 |
| 验证方法 | 文档搜索 |
| 优先级 | P1 |

---

## TC-8-04：纯文档交付路径顺序验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-8-04 |
| 标题 | 纯文档交付路径 Gate 2 → HR#1 → Release 验证 |
| 追溯 | PRD 7.3 纯文档交付路径；Tech Spec 统一技术语义 |
| 前置条件 | 目标文档已更新 |
| 测试步骤 | 在三份目标文档中搜索纯文档交付路径：检查 Gate 2 → HR#1 → Release / Issue Close 的链式描述 |
| 预期结果 | 纯文档交付路径明确为 Gate 2 → HR#1 → Release / Issue Close，不走 Gate 3/Gate 4/HR#2，但 HR#1 环节不可省略 |
| 验证方法 | 文档搜索 |
| 优先级 | P1 |

---

## TC-8-05：HR#1 后推进路径完整性验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-8-05 |
| 标题 | HR#1 后推进路径完整性验证 |
| 追溯 | PRD 7.3 Gate 顺序；Tech Spec 规则固化范围 |
| 前置条件 | `prompts/017_human_review_and_signoff.md` 已更新 |
| 测试步骤 | 检查 HR#1 通过后下游推进路径的描述是否完整，是否存在“HR#1 未完成即进入实现阶段”的遗漏 |
| 预期结果 | 文档明确说明：HR#1 未完成前不得推进到下游阶段，并给出 Human 合并文档 PR 后 Engineer 可进入 Implementation 的清晰路径 |
| 验证方法 | 文档内容验证 |
| 优先级 | P1 |

---

## TC-8-06：`prompts/017_human_review_and_signoff.md` 更新验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-8-06 |
| 标题 | Human Review 与签字机制文档更新验证 |
| 追溯 | PRD 4.3 文档更新范围；Tech Spec 文件级技术责任 |
| 前置条件 | `prompts/017_human_review_and_signoff.md` 已更新 |
| 测试步骤 | 1. 检查文档是否明确 HR#1 不可跳过<br>2. 检查文档是否明确纯文档交付不能跳过 HR#1<br>3. 检查文档是否定义 Gate 2 → HR#1 → 下游阶段的顺序 |
| 预期结果 | 上述三条语义均已写入且表述一致 |
| 验证方法 | 文档内容验证 |
| 优先级 | P1 |

---

## TC-8-07：`skills/workflows/human-review.md` 更新验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-8-07 |
| 标题 | 人工评审工作流文档更新验证 |
| 追溯 | PRD 4.3 文档更新范围；Tech Spec 文件级技术责任 |
| 前置条件 | `skills/workflows/human-review.md` 已更新 |
| 测试步骤 | 1. 检查文档是否明确 HR#1 不可跳过<br>2. 检查文档是否列出开发交付路径和纯文档交付路径<br>3. 检查文档是否将“HR#1 未完成却继续推进下游阶段”列为失败信号 |
| 预期结果 | 上述三条语义均已写入且表述一致 |
| 验证方法 | 文档内容验证 |
| 优先级 | P1 |

---

## TC-8-08：`prompts/004_delivery_gates.md` 更新验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-8-08 |
| 标题 | 交付 Gate CI 参考文档更新验证 |
| 追溯 | PRD 4.3 文档更新范围；Tech Spec 文件级技术责任 |
| 前置条件 | `prompts/004_delivery_gates.md` 已更新 |
| 测试步骤 | 1. 检查 Gate 2 → HR#1 → Gate 3 的映射是否清晰<br>2. 检查 HR#1 是否被明确定义为 Gate 2 后的强制环节<br>3. 检查文档是否未将 GOV-004 结论写成当前自动前提 |
| 预期结果 | Gate 顺序映射清晰，HR#1 为强制环节，历史结论仅追溯 |
| 验证方法 | 文档内容验证 |
| 优先级 | P1 |

---

## TC-8-09：历史治理结论隔离验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-8-09 |
| 标题 | 历史治理结论仅留档、不替代当前交付验证 |
| 追溯 | PRD 5.3 非目标 / 历史治理结论隔离；Tech Spec 风险 |
| 前置条件 | 全部目标文档已更新 |
| 测试步骤 | 1. 检查文档是否将 GOV-004 结论自动视为当前已通过<br>2. 检查 #8 的 QA Case / Tech / PRD 是否独立起草，而非直接引用历史结论 |
| 预期结果 | GOV-004 仅作为背景追溯，Issue #8 仍需按 PRD / Tech / QA / HR#1 链路完成交付；文档文本中不得出现“因 GOV-004 已通过”或类似表述 |
| 验证方法 | 文档内容验证 + 追溯矩阵检查 |
| 优先级 | P1 |

---

## TC-8-10：最小修改原则验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-8-10 |
| 标题 | 最小修改原则验证 |
| 追溯 | Tech Spec 最小修改原则 |
| 前置条件 | 文档与 workflow 修改已完成 |
| 测试步骤 | 1. 检查本次修改是否只涉及 HR#1 强制性与 Gate 顺序相关的文本<br>2. 检查是否未引入与 #8 无关的新 workflow 新脚本新机制 |
| 预期结果 | 改动面严格限定在三份目标文件，未扩散到 bootstrap-sync、CI 核心逻辑等无关领域 |
| 验证方法 | 文档范围验证 / diff 检查 |
| 优先级 | P2 |

---

## 当前评审状态

- **当前状态**：Draft
- **下一动作**：发起 QA Case Design 三方评审（PM + Architect + Engineer）
- **评审前提**：以本文件当前 Draft 为准，后续实现与文档修改不得绕过 QA Case 评审

## v1 Draft 变更说明（2026-04-22）

| 变更项 | 说明 |
|--------|------|
| 首次建立 QA Case | 基于 PRD #008 + Tech Spec #008 v1 建立当前有效 QA Case Draft |
| 覆盖范围建立 | 对 HR#1 强制性、交付类型无关性、Gate 顺序固化、三文件一致性建立追溯矩阵与测试用例 |
| 历史结论隔离 | 将 GOV-004 仅留档、不替代当前交付纳入验证范围 |
