# GOV-011 变更追溯规则缺失 + Gate 流程并行化违规

## 基本信息

| 字段 | 内容 |
|------|------|
| PMO Issue | `../issues/011_2026-04-20_governance_hr1_rejected_and_gate_violation.md` |
| GitHub Issue | https://github.com/alpha-86/AgentDevFlow/issues/20 |
| 关联 Issue | #3 (gstack/superpower 增强层接入) |
| 讨论日期 | 2026-04-20 |
| 验收日期 | 2026-04-21 |
| 状态 | ✅ 已执行，待验收 |

---

## 一、问题回顾

Issue #3 在 PRD v3 → v4.1 迭代过程中，**PRD 变更后未重新走 Gate 1 → Gate 2 流程就并行更新了 Tech Spec 和 QA Case**，导致 Tech Spec v5 的"可选"语义与 PRD v4.1 的"强制依赖"语义不一致，Architect 在 HR#1 阶段发现并 Reject。

### 违规事实

1. **PRD v3 → v4.1 发生重大语义变更**（可选增强 → 强制依赖），未重新触发 Gate 1 评审
2. **Gate 流程被并行化**：Tech Spec v4 和 QA Case v2 在 Gate 1（v3）还未最终确认时就开始并行迭代
3. **Gate 2 未完成就起草 QA Case**：违反 `prompts/002_develop_pipeline.md` 的 Gate 顺序约束

### 时间线

| 日期 | 事件 | 合规性 |
|------|------|--------|
| 2026-04-17 | PRD v3 Gate 1 三方签字完成 | ✅ |
| 2026-04-17 | **Tech Spec v4 + QA Case v2 在 Gate 1（v3）未最终确认时并行迭代** | ❌ 违规 |
| 2026-04-17 | QA Case Design 在 Gate 2 未完成前开始起草 | ❌ 违规 |
| 2026-04-20 | PRD v3 → v4.1（可选→强制，重大语义变更） | — |
| 2026-04-20 | Tech Spec v5 完成，但 Section 4.3 仍写"可选" | ❌ 与 PRD v4.1 语义冲突 |
| 2026-04-20 | HR#1：Architect Rejected（语义冲突）| — 发现问题 |
| 2026-04-20 | Tech Spec v5.1 修复（可选→强制对齐）| ✅ 纠正 |
| 2026-04-20 | HR#1 重新评审：QA + Architect Approved | ✅ 流程恢复 |

---

## 二、根因分析

### 直接原因

PRD v3 → v4.1 发生"可选→强制依赖"重大语义变更后，Gate 1 重新评审未完成，Tech Spec 和 QA Case 就开始并行更新。

### 根因

1. **变更追溯规则虽有但不够显式**：`prompts/002_develop_pipeline.md` 虽有"变更级联效应"章节，但未明确声明 **"Gate 流程必须串行，禁止并行迭代"**
2. **重大变更 vs 小幅变更缺乏定义标准**：Agent 无法判断一次 PRD 变更是否触发完整 Gate 重审
3. **Gate 阶段边界模糊**：Tech Spec 在 PRD Gate 1 评审期间就开始更新，QA Case 在 Gate 2 完成前就开始起草

### 深层原因

Agent 在迭代过程中倾向于"并行推进多个文档"以加速交付，但忽略了 Gate 流程的串行约束。流程文档中的"变更级联效应"被当作"建议"而非"强制规则"执行。

---

## 三、讨论对齐结论

### 结论 1：Gate 流程串行约束（强制）

**决定**：Gate 流程 **必须串行执行，禁止并行迭代**。

**理由**：下游文档依赖上游文档的评审结论，并行迭代会导致文档间语义不一致，最终只能在 HR#1 阶段发现（代价高）。

**正确流程**：
```
PRD 变更
  │
  ▼
Gate 1（PRD Review）重新评审 → 三方签字 Approved
  │
  ▼
Tech Spec 更新 → Gate 2（Tech Review）→ 三方签字 Approved
  │
  ▼
QA Case Design 更新 → 三方签字 Approved
  │
  ▼
文档 PR → Human Review #1
```

**禁止行为**：
- PRD 在 Gate 1 评审期间，Tech Spec 不得更新
- Tech Spec 在 Gate 2 评审期间，QA Case 不得起草
- 任何 Gate 未 Approved 前，不得进入下游 Gate 的文档编写

### 结论 2：变更等级定义标准

**决定**：明确"重大变更"和"小幅变更"的定义，作为是否触发完整 Gate 重审的判断依据。

**重大变更**（必须触发完整 Gate 重审）：
| 类型 | 示例 |
|------|------|
| 语义变化 | 可选→强制、单一→多个、范围扩大/缩小 |
| 新增/删除交付域 | 新增文档类型、删除验收标准章节 |
| 角色数量变化 | 5 角色→6 角色 |
| 关键验收标准变更 | 验收标准新增/删除/修改判定条件 |
| 架构决策变更 | 技术选型改变、检测方式改变 |

**小幅变更**（仅需原 Gate 签字人确认，无需完整 Gate 重审）：
| 类型 | 示例 |
|------|------|
| 文档格式调整 | 表格对齐、标题层级调整 |
| 错别字修正 | 不影响语义的文字修正 |
| 描述文字澄清 | 不改变语义的范围澄清 |
| 补充遗漏内容 | 不改变范围的补充说明 |
| 链接修正 | 文档链接更新 |

### 结论 3：变更追溯规则增强

**决定**：将变更追溯规则增强后写入 `prompts/002_develop_pipeline.md`，作为强制规则而非建议。

**增强规则**：

| 变更来源 | 变更等级 | 需重新通过的 Gate | 下游文档处理 |
|---------|---------|------------------|-------------|
| PRD | 重大 | Gate 1 → Gate 2 → QA Case Design → 重新评审全部 | Tech Spec 版本+1 → Case Design 版本+1 |
| PRD | 小幅 | 原 Gate 1 签字人确认即可 | Tech Spec 版本+0.1 → 确认无影响后无需 Case Design 变更 |
| Tech Spec | Major/Breaking | Gate 2 → QA Case Design → 重新评审 | Case Design 版本+1 |
| Tech Spec | 小幅 | 原 Gate 2 签字人确认即可 | Case Design 确认无影响 |
| QA Case | 任意 | QA Case Design 重新评审 | 测试报告版本+1（如有）|
| 多环节同时变更 | — | 从头重新走 Gate 1 → Gate 2 → QA Case | 全部文档版本+1 |

### 结论 4：Gate 阶段准入检查清单

**决定**：每个 Gate 的"进入条件"增加"上游 Gate 已 Approved"的显式检查。

| Gate | 进入条件（新增/强化） |
|------|---------------------|
| Gate 1 | PRD 已起草，无未完成的下游文档更新 |
| Gate 2 | **PRD Gate 1 已 Approved**（新增显式检查），Tech Spec 已起草 |
| QA Case Design | **Gate 2 已 Approved**（新增显式检查），QA Case 已起草 |
| 文档 PR | 所有 Gate 签字已落地，无未完成的文档变更 |

---

## 四、修复方案

### 本次已完成修复

| 动作 | 涉及文件 | 验收标准 | 负责人 | 状态 |
|------|---------|---------|--------|------|
| 增强"变更级联效应"章节：新增串行约束、变更等级定义、增强追溯规则 | `prompts/002_develop_pipeline.md` | 文档已更新，规则明确为强制 | PM | ✅ 已完成 |
| 补充 Gate 准入强化说明：显式要求上游 Gate 已 Approved | `prompts/002_develop_pipeline.md` | 文档中存在 Gate 进入条件强化表 | PM | ✅ 已完成 |
| 产出 GOV-011 治理决议文档 | `docs/pmo/resolutions/GOV-011_2026-04-20_change_propagation_gate_violation_resolution.md` | 根因、决议、修复建议完整留痕 | PM | ✅ 已完成 |

### 后续建议修复

| 动作 | 涉及位置 | 验收标准 | 负责人 | 状态 |
|------|---------|---------|--------|------|
| 同步更新 `prompts/004_delivery_gates.md` 的 CI 检查参考口径 | `prompts/004_delivery_gates.md` | 与 `002_develop_pipeline.md` 保持一致 | PM / Team Lead | ⏳ 建议跟进 |
| PMO 检查清单增加"Gate 并行化"检查项 | `docs/pmo/issues/` 模板 | PMO Issue 模板包含 Gate 顺序检查 | PMO | ⏳ 建议跟进 |
| 各角色 SKILL.md 补充"禁止在下游 Gate 并行迭代文档" | `skills/*/SKILL.md` | 角色规范与流程规则一致 | Team Lead | ⏳ 建议跟进 |

### Issue #3 已修复项
'}
| 修复项 | Commit | 状态 |
|--------|--------|------|
| Tech Spec v5.1 修复可选→强制语义 | 73028fe | ✅ 已修复 |
| HR#1 重新评审 Approved | — | ✅ 已通过 |

---

## 五、GitHub Issue 追踪

| 字段 | 内容 |
|------|------|
| GitHub Issue URL | https://github.com/alpha-86/AgentDevFlow/issues/20 |
| 责任人 | PM |
| 关联 PMO Issue | `../issues/011_2026-04-20_governance_hr1_rejected_and_gate_violation.md` |
| 关联 GOV | GOV-004（Issue #3 HR#1 被跳过） |

---

## 六、验收结论

| 字段 | 内容 |
|------|------|
| 最终验收人 | Team Lead |
| 验收日期 | 2026-04-21 |
| GitHub Issue 状态 | ⏳ Open |
| PMO Issue 状态 | ⏳ Open |
| 文档更新状态 | ✅ 已完成（002_develop_pipeline.md 变更级联效应增强） |

---

*由 Product Manager 基于 PMO 检查记录生成 | 2026-04-21*
