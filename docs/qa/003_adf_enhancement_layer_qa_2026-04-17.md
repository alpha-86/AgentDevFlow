---
name: AgentDevFlow 增强层接入 — QA Case Design
description: 定义增强层文档交付的 QA 测试用例（文档搜索型验收测试 + 脚本执行验证）
status: In Review
owner: QA Engineer
date: 2026-04-17
update_date: 2026-04-20
issue: "#3"
prd: docs/prd/003_adf_enhancement_layer_2026-04-17.md (v4.1)
tech: docs/tech/003_adf_enhancement_layer_tech_2026-04-17.md (v5)
---

# QA Case Design #003 — 增强层文档交付

---

## 追溯关系

- **PRD**: `docs/prd/003_adf_enhancement_layer_2026-04-17.md` (v4.1, Issue #3)
- **Tech Spec**: `docs/tech/003_adf_enhancement_layer_tech_2026-04-17.md` (v5)

### PRD v4.1 → QA Case 追溯矩阵

| PRD v4.1 Section 7 | 对应 TC | 覆盖状态 |
|---------------------|---------|---------|
| 7.1 定位声明 — 三者定位关系 | TC-3-01, TC-3-02 | ✅ |
| 7.1 定位声明 — 开关语义（开关打开=强制依赖）| TC-3-02 | ✅ |
| 7.2 角色增强映射 — 6角色清单 | TC-3-05 | ✅ |
| 7.2 角色增强映射 — 适用Gate阶段 | TC-3-04, TC-3-11 | ✅ |
| 7.2 角色增强映射 — 来源标注 | TC-3-05 | ✅ |
| 7.3 输出边界 — 不能替代 | TC-3-06 | ✅ |
| 7.3 输出边界 — 流程留痕口径 | TC-3-07 | ✅ |
| 7.4 安装前置 — 安装前置条件 | TC-3-08, TC-3-09 | ✅ |
| 7.4 安装前置 — 强制依赖语义 | TC-3-02 | ✅ |

### Tech Spec v5 新增验证项追溯

| Tech Spec v5 Section | 对应 TC | 覆盖状态 |
|-----------------------|---------|---------|
| Section 3 检测脚本实现逻辑 | TC-3-10 | ✅ |
| Section 4.3 各Gate增强能力映射矩阵 | TC-3-11 | ✅ |

---

## TC-3-01：增强层定位声明验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-01 |
| 标题 | 增强层定位声明验证 |
| 追溯 | PRD #003 v4.1 / 7.1 定位声明 |
| 前置条件 | `docs/platforms/enhancement-layer.md` 存在于 main 分支 |
| 测试步骤 | 1. 读取 `docs/platforms/enhancement-layer.md`<br>2. 搜索关键词"能力插件层"或"增强层" |
| 预期结果 | 文档包含三者定位关系（gstack/工具层、superpower/方法层、AgentDevFlow/流程层），且明确增强层"增强角色不替代角色"原则 |
| 验证方法 | 文档搜索 |
| 优先级 | P1 |

---

## TC-3-02：开关语义与强制依赖验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-02 |
| 标题 | 开关语义与强制依赖验证 |
| 追溯 | PRD #003 v4.1 / 7.1 定位声明（开关语义）、7.4 安装前置（强制依赖） |
| 前置条件 | `docs/platforms/enhancement-layer.md` 存在 |
| 测试步骤 | 搜索"强制依赖"、"开关打开"或"强制增强" |
| 预期结果 | 文档明确说明：开关打开 = 强制依赖 gstack/superpower，不支持选择性关闭；增强能力在适用 Gate 阶段自动触发 |
| 验证方法 | 文档搜索 |
| 优先级 | P1 |

---

## TC-3-03：结果共享验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-03 |
| 标题 | 检测结果共享验证 |
| 追溯 | PRD #003 v4.1 / Tech Spec #003 v5 / Section 3 检测脚本实现 |
| 前置条件 | `docs/platforms/enhancement-layer.md` 或 Tech Spec 存在 |
| 测试步骤 | 搜索关键词"共享"或"Team config" |
| 预期结果 | 文档明确说明：检测结果通过 Team config 持久化，各 Agent 读取配置，无需重复检测 |
| 验证方法 | 文档搜索 |
| 优先级 | P1 |

---

## TC-3-04：回落机制验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-04 |
| 标题 | 回落机制验证 |
| 追溯 | PRD #003 v4.1 / Tech Spec #003 v5 / Section 3 回落行为 |
| 前置条件 | `docs/platforms/enhancement-layer.md` 或 Tech Spec 存在 |
| 测试步骤 | 搜索关键词"回落" |
| 预期结果 | 文档明确说明：均未安装时自动回落 AgentDevFlow 原生机制 + 提示建议安装，回落不影响核心流程 |
| 验证方法 | 文档搜索 |
| 优先级 | P1 |

---

## TC-3-05：角色增强映射表验证（6 角色）

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-05 |
| 标题 | 角色增强映射表验证（6 角色）|
| 追溯 | PRD #003 v4.1 / 7.2 角色增强映射 |
| 前置条件 | `docs/platforms/enhancement-layer.md` 存在 |
| 测试步骤 | 读取角色增强映射表，检查 6 个角色 |
| 预期结果 | 每个角色（PM/Architect/QA/Engineer/Team Lead/PMO）都有对应增强能力范围、适用 Gate 阶段和来源（gstack/superpower）|
| 验证方法 | 文档内容验证 |
| 优先级 | P1 |

---

## TC-3-06：输出边界验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-06 |
| 标题 | 增强层输出边界验证 |
| 追溯 | PRD #003 v4.1 / 7.3 输出边界 |
| 前置条件 | `docs/platforms/enhancement-layer.md` 存在 |
| 测试步骤 | 搜索关键词"不能替代"或"边界" |
| 预期结果 | 文档明确说明增强能力输出不能替代 PRD/Tech/QA/Gate 结论 |
| 验证方法 | 文档搜索 |
| 优先级 | P1 |

---

## TC-3-07：流程留痕口径验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-07 |
| 标题 | 流程留痕口径验证 |
| 追溯 | PRD #003 v4.1 / 7.3 输出边界 |
| 前置条件 | `docs/platforms/enhancement-layer.md` 存在 |
| 测试步骤 | 搜索"流程留痕"或"正式文件负责" |
| 预期结果 | 文档明确说明"增强能力负责增强思考，正式文件负责流程留痕" |
| 验证方法 | 文档搜索 |
| 优先级 | P2 |

---

## TC-3-08：角色文档增强 skill 引用验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-08 |
| 标题 | 6 个角色 SKILL.md 包含增强 skill 引用验证 |
| 追溯 | PRD #003 v4.1 / 7.2 角色增强映射（来源标注）|
| 前置条件 | `skills/*/SKILL.md` 存在于 main 分支 |
| 测试步骤 | 检查每个角色 SKILL.md 中是否包含增强层 skill 引用（含来源标注） |
| 预期结果 | 每个角色文档至少有一条增强 skill 引用，并标注来源（gstack/superpower）|
| 验证方法 | 文件内容验证 |
| 优先级 | P2 |

---

## TC-3-09：安装前置条件验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-09 |
| 标题 | 安装前置条件说明验证 |
| 追溯 | PRD #003 v4.1 / 7.4 安装前置 |
| 前置条件 | `docs/guides/enhancement-guide.md` 存在 |
| 测试步骤 | 读取增强层使用指南，确认安装前置说明 |
| 预期结果 | 文档包含 gstack + superpower skill 包的安装前置条件 |
| 验证方法 | 文档内容验证 |
| 优先级 | P2 |

---

## TC-3-10：检测脚本实现验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-10 |
| 标题 | 检测脚本实现验证 |
| 追溯 | Tech Spec #003 v5 / Section 3 检测脚本实现 |
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
| 追溯 | Tech Spec #003 v5 / Section 4.3 Gate×角色增强映射矩阵 |
| 前置条件 | Tech Spec Section 4.3 Gate 增强映射矩阵存在 |
| 测试步骤 | 对照 Tech Spec Section 4.3 Gate×角色矩阵，逐一验证：1. 每个 Gate 的增强能力有 PRD v4.1 Section 4.2 作为依据<br>2. 各角色在各 Gate 的增强能力不超出 PRD v4.1 Section 4.2 定义范围<br>3. 空白（不使用增强）的 Gate 阶段与 PRD 一致 |
| 预期结果 | Tech Spec Section 4.3 的每个 Gate×角色增强映射有 PRD v4.1 Section 4.2 作为依据，无超出 PRD 范围的增强能力定义 |
| 验证方法 | 文档交叉验证 |
| 优先级 | P1 |

---

## Gate 2 Review Record

| 日期 | 评审人 | 结论 | 关键意见 | 待办 |
|---|---|---|---|---|
| 2026-04-17 | PM | 发起评审 | Tech + QA Case 均已起草，追溯关系完整 | 等待 Engineer + QA 签字 |
| 2026-04-17 | Engineer | **Approved** ✅ | skill 名称映射准确，检测机制语义可实现，文档交付流程可行 | — |
| 2026-04-17 | QA | **Approved** ✅ | TC-3-01~TC-3-09 完整覆盖 PRD v4 Section 7，验证方法可执行，无覆盖缺口 | — |
| 2026-04-20 | QA | **Approved** ✅（v2迭代）| TC-3-10（检测脚本实现）+ TC-3-11（Gate映射一致性）新增覆盖 Tech Spec v5；PRD v4.1 追溯矩阵更新；TC-3-01~TC-3-09 按 v4.1 重映射 | 待 Human Review #1 签字 |

## v2 变更说明（2026-04-20）

基于 PRD v4.1 + Tech Spec v5 迭代 QA Case Design：

| 变更项 | 说明 |
|--------|------|
| 新增 TC-3-10 | 检测脚本实现验证（Python脚本执行验证，对应 Tech Spec v5 Section 3）|
| 新增 TC-3-11 | Gate 增强映射一致性验证（Tech Spec v5 Section 4.3 × PRD v4.1 Section 4.2 交叉验证）|
| 更新 TC-3-02 | 原"统一检测机制"→"开关语义与强制依赖"，新增开关打开=强制依赖语义验证 |
| 更新 TC-3-03 | 新增"结果通过 Team config 共享"验证，对应 Tech Spec v5 检测脚本共享机制 |
| 更新 TC-3-05 | 增强映射验证增加"适用 Gate 阶段"检查 |
| 更新 TC-3-07 | 原"零配置语义"→"流程留痕口径"，PRD v4.1 Section 7.3 对应 |
| 更新 TC-3-08 | 增强 skill 引用验证增加来源标注检查 |
| 新增追溯矩阵 | PRD v4.1 Section 7 → TC 覆盖状态 + Tech Spec v5 → TC 追溯 |
| 状态更新 | In Review（等待 Human Review #1 签字）|
