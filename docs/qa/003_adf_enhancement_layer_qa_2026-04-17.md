---
name: AgentDevFlow 增强层接入 — QA Case Design v3
description: 基于 PRD v4.3 与 Tech Spec v5.2 的当前有效 QA Case Draft，定义增强层文档交付的测试用例（文档搜索型验收测试 + 脚本执行验证）
status: Draft
owner: QA Engineer
date: 2026-04-17
update_date: 2026-04-21
issue: "#3"
prd: docs/prd/003_adf_enhancement_layer_2026-04-17.md (v4.3)
tech: docs/tech/003_adf_enhancement_layer_tech_2026-04-17.md (v5.2)
---

# QA Case Design #003 — 增强层文档交付（v3 Draft）

---

## 当前有效状态

- **当前有效版本**：v3 Draft
- **当前有效输入**：PRD v4.3 + Tech Spec v5.2
- **当前阶段**：QA Case Design（等待 PM + Architect + Engineer 三方评审）
- **规则说明**：本文件为 Issue #3 在回退到 Gate 1 / Gate 2 并重新通过后的当前有效 QA Case Draft

## 历史结论说明（仅留档，不作为本轮有效前提）

- 2026-04-17 / 2026-04-20 的 QA Case 评审、Architect 补签与 Approved 结论仅用于追溯
- 这些历史结论基于 PRD v4.1 / Tech v5，不作为本轮 PRD v4.3 / Tech v5.2 的有效前提
- 本轮进入 QA Case 三方评审时，应仅以本文件当前 Draft 内容为准

---

## 追溯关系

- **PRD**: `docs/prd/003_adf_enhancement_layer_2026-04-17.md` (v4.3, Issue #3)
- **Tech Spec**: `docs/tech/003_adf_enhancement_layer_tech_2026-04-17.md` (v5.2)

### PRD v4.3 → QA Case 追溯矩阵

| PRD v4.3 Section 7 | 对应 TC | 覆盖状态 |
|---------------------|---------|---------|
| 7.1 定位声明 — 三者定位关系 | TC-3-01 | ✅ |
| 7.1 定位声明 — 安装后强制依赖、未安装时回落原生机制 | TC-3-02, TC-3-04 | ✅ |
| 7.2 角色增强映射 — 6角色清单 / 适用 Gate / 来源 | TC-3-05, TC-3-11 | ✅ |
| 7.2 角色增强映射 — 已安装增强层时按强制执行处理 | TC-3-05, TC-3-11 | ✅ |
| 7.3 输出边界 — 不能替代正式交付物 | TC-3-06 | ✅ |
| 7.3 输出边界 — 流程留痕口径 | TC-3-07 | ✅ |
| 7.4 安装前置 — 安装前置条件 | TC-3-08, TC-3-09 | ✅ |
| 7.4 安装前置 — 安装后行为 / 回落方式 / 未安装不阻断主流程 | TC-3-03, TC-3-04, TC-3-09 | ✅ |

### Tech Spec v5.2 → QA Case 追溯矩阵

| Tech Spec v5.2 Section | 对应 TC | 覆盖状态 |
|------------------------|---------|---------|
| 检测机制（统一检测一次、结果共享、强制依赖/回落） | TC-3-02, TC-3-03, TC-3-04 | ✅ |
| Python 检测脚本实现逻辑 | TC-3-10 | ✅ |
| Gate × 角色增强能力映射矩阵 | TC-3-11 | ✅ |
| 输出边界与回落机制说明 | TC-3-06, TC-3-07 | ✅ |

---

## TC-3-01：增强层定位声明验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-01 |
| 标题 | 增强层定位声明验证 |
| 追溯 | PRD #003 v4.3 / 7.1 定位声明 |
| 前置条件 | `docs/platforms/enhancement-layer.md` 存在于当前分支 |
| 测试步骤 | 1. 读取 `docs/platforms/enhancement-layer.md`<br>2. 搜索关键词“能力插件层”“工具层”“方法层”“流程层” |
| 预期结果 | 文档包含三者定位关系（gstack/工具层、superpower/方法层、AgentDevFlow/流程层），且明确增强层不替代正式流程约束层 |
| 验证方法 | 文档搜索 |
| 优先级 | P1 |

---

## TC-3-02：安装后强制依赖 / 强制执行语义验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-02 |
| 标题 | 安装后强制依赖 / 强制执行语义验证 |
| 追溯 | PRD #003 v4.3 / 7.1 定位声明；7.2 角色增强映射 |
| 前置条件 | `docs/platforms/enhancement-layer.md` 或当前 Tech Spec 存在 |
| 测试步骤 | 搜索“强制依赖”“强制执行”“不支持安装后再选择性关闭”等关键词 |
| 预期结果 | 文档明确说明：安装增强层后按强制依赖 / 强制执行处理，不存在“安装后可选启用”或“推荐执行”分支 |
| 验证方法 | 文档搜索 |
| 优先级 | P1 |

---

## TC-3-03：检测结果共享验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-03 |
| 标题 | 检测结果共享验证 |
| 追溯 | Tech Spec #003 v5.2 / 检测机制、结果共享 |
| 前置条件 | Tech Spec 存在 |
| 测试步骤 | 搜索“统一检测一次”“Team config”“metadata”“共享”等关键词 |
| 预期结果 | 文档明确说明：`start-agent-team` 统一检测一次，结果通过 Team config 持久化并供各 Agent 共享读取 |
| 验证方法 | 文档搜索 |
| 优先级 | P1 |

---

## TC-3-04：未安装时回落原生机制验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-04 |
| 标题 | 未安装时回落原生机制验证 |
| 追溯 | PRD #003 v4.3 / 7.1、7.4；Tech Spec #003 v5.2 / 回落保障 |
| 前置条件 | `docs/platforms/enhancement-layer.md` 或当前 Tech Spec 存在 |
| 测试步骤 | 搜索“回落”“未安装”“不阻断主流程”“建议安装”等关键词 |
| 预期结果 | 文档明确说明：未安装时自动回落 AgentDevFlow 原生机制，不阻断主流程，并给出建议安装提示 |
| 验证方法 | 文档搜索 |
| 优先级 | P1 |

---

## TC-3-05：角色增强映射表验证（6 角色）

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-05 |
| 标题 | 角色增强映射表验证（6 角色） |
| 追溯 | PRD #003 v4.3 / 7.2 角色增强映射 |
| 前置条件 | `docs/platforms/enhancement-layer.md` 或 PRD/Tech 中映射表存在 |
| 测试步骤 | 读取角色增强映射表，检查 6 个角色 |
| 预期结果 | 每个角色（PM/Architect/QA/Engineer/Team Lead/PMO）都有对应增强能力范围、适用 Gate、来源；并明确已安装时按强制执行处理 |
| 验证方法 | 文档内容验证 |
| 优先级 | P1 |

---

## TC-3-06：输出边界验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-06 |
| 标题 | 增强层输出边界验证 |
| 追溯 | PRD #003 v4.3 / 7.3 输出边界；Tech Spec #003 v5.2 / 输出边界 |
| 前置条件 | `docs/platforms/enhancement-layer.md` 或当前 Tech Spec 存在 |
| 测试步骤 | 搜索“不能替代”“正式交付物”“PRD”“Tech Spec”“QA Case Design”“QA Report”“Issue Comment”“正式评审结论”等关键词 |
| 预期结果 | 文档明确说明增强能力输出不能替代正式交付物与正式 Gate 结论 |
| 验证方法 | 文档搜索 |
| 优先级 | P1 |

---

## TC-3-07：流程留痕口径验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-07 |
| 标题 | 流程留痕口径验证 |
| 追溯 | PRD #003 v4.3 / 7.3 输出边界 |
| 前置条件 | `docs/platforms/enhancement-layer.md` 或当前 Tech Spec 存在 |
| 测试步骤 | 搜索“增强能力负责增强思考”“正式文件负责流程留痕”等关键词 |
| 预期结果 | 文档明确说明增强能力仅增强思考与分析，正式文件负责流程留痕 |
| 验证方法 | 文档搜索 |
| 优先级 | P2 |

---

## TC-3-08：角色文档增强 skill 引用验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-08 |
| 标题 | 6 个角色 SKILL.md 包含增强能力说明验证 |
| 追溯 | PRD #003 v4.3 / 7.2 角色增强映射 |
| 前置条件 | `skills/*/SKILL.md` 存在于当前分支 |
| 测试步骤 | 检查每个角色 SKILL.md 中是否包含增强能力说明及来源标注 |
| 预期结果 | 每个角色文档至少有一条增强能力说明，并标注来源（gstack/superpower） |
| 验证方法 | 文件内容验证 |
| 优先级 | P2 |

---

## TC-3-09：安装前置条件说明验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-09 |
| 标题 | 安装前置条件说明验证 |
| 追溯 | PRD #003 v4.3 / 7.4 安装前置 |
| 前置条件 | `docs/guides/enhancement-guide.md` 存在 |
| 测试步骤 | 读取增强层使用指南，确认安装前置说明 |
| 预期结果 | 文档包含 gstack + superpower skill 包的安装前置条件，并说明未安装时按原生机制运行 |
| 验证方法 | 文档内容验证 |
| 优先级 | P2 |

---

## TC-3-10：检测脚本实现验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-10 |
| 标题 | 检测脚本实现验证 |
| 追溯 | Tech Spec #003 v5.2 / Python 检测脚本实现 |
| 前置条件 | `scripts/detect_enhancement_layer.py` 存在且可执行 |
| 测试步骤 | 1. 确认脚本存在于 `scripts/detect_enhancement_layer.py`<br>2. 运行 `python scripts/detect_enhancement_layer.py`<br>3. 验证脚本输出（gstack/superpower 安装状态）<br>4. 对比脚本输出与实际 skill 目录状态 |
| 预期结果 | 脚本正确识别 gstack/superpower 安装状态，返回码正确（0=任一已安装，1=均未安装），输出与实际 skill 目录一致 |
| 验证方法 | 脚本执行验证 |
| 优先级 | P1 |
| 注意事项 | 若 gstack/superpower 均未安装，脚本返回码应为 1 且输出提示建议安装 |

---

## TC-3-11：Gate 增强映射一致性验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-11 |
| 标题 | 各 Gate 增强能力映射一致性验证 |
| 追溯 | PRD #003 v4.3 / 7.2；Tech Spec #003 v5.2 / Gate × 角色增强映射矩阵 |
| 前置条件 | Tech Spec Gate 增强映射矩阵存在 |
| 测试步骤 | 对照 PRD v4.3 与 Tech Spec v5.2，逐一验证：1. 每个 Gate 的增强能力有 PRD 角色映射作为依据<br>2. 各角色在各 Gate 的增强能力不超出 PRD 范围<br>3. 空白（不使用增强）的 Gate 阶段与 PRD 一致 |
| 预期结果 | Tech Spec 的 Gate × 角色增强映射有 PRD v4.3 作为依据，无超出 PRD 范围的增强能力定义 |
| 验证方法 | 文档交叉验证 |
| 优先级 | P1 |

---

## 当前评审状态

- **当前状态**：Draft
- **下一动作**：进入 QA Case Design 三方评审（PM + Architect + Engineer）
- **评审前提**：以本文件当前 Draft 为准，不沿用历史 Approved 结论

## 历史评审记录（仅留档，不作为本轮有效前提）

| 日期 | 评审人 | 历史结论 | 说明 |
|---|---|---|---|
| 2026-04-17 | PM | 发起评审 | 基于旧版 PRD / Tech 的历史记录，仅留档 |
| 2026-04-17 | Engineer | Approved | 基于历史版本，仅留档 |
| 2026-04-17 | QA | Approved | 基于历史版本，仅留档 |
| 2026-04-20 | QA | Approved（v2迭代） | 基于 PRD v4.1 / Tech v5，仅留档 |
| 2026-04-20 | Architect | Approved（补签） | 基于 PRD v4.1 / Tech v5，仅留档 |

## v3 Draft 变更说明（2026-04-21）

| 变更项 | 说明 |
|--------|------|
| 当前有效输入重置 | 从 PRD v4.1 / Tech v5 重置为 PRD v4.3 / Tech v5.2 |
| frontmatter 重置 | 状态改为 Draft，绑定当前有效 PRD / Tech 版本 |
| 追溯矩阵重置 | 清理 PRD v4.1 / Tech v5 旧追溯矩阵，改为 PRD v4.3 / Tech v5.2 |
| 历史结论降格 | 历史 Approved 记录仅保留留档，不作为当前有效前提 |
| 语义对齐 | 所有测试用例统一对齐“安装后强制依赖 / 强制执行，未安装时回落原生机制” |
