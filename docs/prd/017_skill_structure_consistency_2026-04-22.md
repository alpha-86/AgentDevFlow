---
name: SKILL 结构冲突与不一致治理
description: 治理 AgentDevFlow 7 个核心角色 SKILL.md 的结构冲突与不一致，统一命名、章节、强制规则与章节顺序，作为 Issue #17 的当前有效 Gate 1 输入
status: Draft
owner: Product Manager
date: 2026-04-22
update_date: 2026-04-22
issue: "#17"
---

# PRD #017 — SKILL 结构冲突与不一致治理

## 1. 背景

Issue #17 指向的核心问题是：AgentDevFlow 的 7 个核心角色 SKILL.md 存在结构冲突与不一致，包括命名混乱、章节缺失、强制规则未声明、章节顺序异常。这些不一致会导致角色行为预期模糊、流程合规性降低，并可能继续扩散为新的治理问题。

## 2. 问题

当前存在以下三个优先级的问题：

### P0（必须立即修复）
- **Architect 强制规则未声明"不签自己的交付物"**：`skills/architect/SKILL.md` 缺少 self-review 禁止规则
- **QA "三方签字"定义错误**：`skills/qa-engineer/SKILL.md` L23 使用 "CTO" 而非 "架构评审人"

### P1（结构不一致）
- **HR#1 命名混乱**：7 个 SKILL 中存在三种不同写法，需统一为 "Human Review #1"
- **Architect 缺少"职责边界"章节**：唯一缺失该章节的核心角色
- **Platform/SRE 缺少"职责边界"和"输出格式"章节**

### P2（原则缺失）
- **"产出者不评审自己"原则未显式声明**：需在禁止行为章节补充
- **PMO 章节顺序异常**："何时启用"在"必读文档"之后

## 3. 目标

形成当前有效的产品层需求定义，明确：

1. 7 个核心角色 SKILL.md 的结构必须统一
2. P0 冲突必须按当前有效需求修复
3. P1/P2 不一致必须按统一口径治理
4. 修复后的 SKILL 结构必须可追溯、可验证

## 4. 范围

### 4.1 强制规则补齐（P0）

- `skills/architect/SKILL.md`：在禁止行为章节显式声明"不签自己的交付物"
- `skills/qa-engineer/SKILL.md`：将 L23 "CTO" 更正为 "架构评审人"

### 4.2 命名统一（P1）

- 7 个 SKILL 中的 "HR#1" 相关表述统一为 "Human Review #1"
- 确保同一 issue 中不出现三种以上不同写法

### 4.3 章节补齐（P1）

- `skills/architect/SKILL.md`：补充"职责边界"章节
- `skills/platform-sre/SKILL.md`：补充"职责边界"和"输出格式"章节

### 4.4 原则显式声明（P2）

- 在 7 个 SKILL 的禁止行为章节统一补充："产出者不评审自己"
- `skills/pmo/SKILL.md`：调整章节顺序，使"何时启用"在"必读文档"之前

### 4.5 涉及文件

- `skills/architect/SKILL.md`
- `skills/qa-engineer/SKILL.md`
- `skills/product-manager/SKILL.md`
- `skills/engineer/SKILL.md`
- `skills/team-lead/SKILL.md`
- `skills/pmo/SKILL.md`
- `skills/platform-sre/SKILL.md`

## 5. 非目标

- 不在本 PRD 中直接修改 skill 源文件
- 不新增与 SKILL 结构无关的流程机制
- 不把 GOV-010 历史治理留档直接当作当前有效交付物

## 6. 用户故事

### US-1：角色使用者
> 作为使用 AgentDevFlow 角色的用户，我希望同一角色的 SKILL 结构与其他角色一致，这样可以减少理解成本和操作歧义。

### US-2：流程审核者
> 作为流程审核者，我希望所有核心角色的强制规则都已显式声明，避免 self-review 等违规行为。

## 7. 验收标准

- [ ] Architect SKILL 已显式声明"不签自己的交付物"
- [ ] QA Engineer SKILL 的"三方签字"已统一为"架构评审人"
- [ ] 7 个 SKILL 中 HR#1 相关表述已统一为"Human Review #1"
- [ ] Architect SKILL 已补充"职责边界"章节
- [ ] Platform/SRE SKILL 已补充"职责边界"和"输出格式"章节
- [ ] 7 个 SKILL 的禁止行为章节已统一补充"产出者不评审自己"
- [ ] PMO SKILL 章节顺序已调整为"何时启用"在"必读文档"之前
- [ ] 本 issue 已按严格研发交付流程重新进入 Gate 1，而非直接复用历史治理结论

## 8. 风险

| 风险 | 影响 | 缓解 |
|------|------|------|
| 修复只改文本、不改结构，后续继续漂移 | 高 | 在 PRD 中明确章节模板与命名规则 |
| 命名统一后与其他引用文档冲突 | 中 | 统一回链当前有效流程文档，触发后续文档修订 |
| 强制规则声明后实际行为未变 | 中 | 在 QA Case 中验证文本存在性，并在后续 issue 中验证执行 |

## 9. 依赖

- `docs/pmo/issues/010_2026-04-17_governance_skill_structure_consistency.md`
- `docs/pmo/resolutions/010_2026-04-17_governance_skill_structure_consistency_resolution.md`
- 当前有效 skill 源文件状态
- Issue #17 当前讨论上下文

## 10. 评审记录

| 日期 | 评审人 | 备注 | 决策 |
|---|---|---|---|
| 2026-04-22 | PM | 按严格研发交付流程重新启动 #17，起草当前有效 PRD | Draft |
