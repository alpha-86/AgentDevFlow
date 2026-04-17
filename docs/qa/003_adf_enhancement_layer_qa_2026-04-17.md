---
name: AgentDevFlow 增强层接入 — QA Case Design
description: 定义增强层文档交付的 QA 测试用例（文档搜索型验收测试）
status: Approved
owner: QA Engineer
date: 2026-04-17
update_date: 2026-04-17
issue: "#3"
prd: docs/prd/003_adf_enhancement_layer_2026-04-17.md
tech: docs/tech/003_adf_enhancement_layer_tech_2026-04-17.md
---

# QA Case Design #003 — 增强层文档交付

---

## 追溯关系

- **PRD**: `docs/prd/003_adf_enhancement_layer_2026-04-17.md`（Issue #3）
- **Tech Spec**: `docs/tech/003_adf_enhancement_layer_tech_2026-04-17.md`

---

## TC-1：增强层定位声明验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-01 |
| 标题 | 增强层定位声明验证 |
| 前置条件 | `docs/platforms/enhancement-layer.md` 存在于 main 分支 |
| 测试步骤 | 1. 读取 `docs/platforms/enhancement-layer.md`<br>2. 搜索关键词"能力插件层"或"增强层" |
| 预期结果 | 文档包含三者定位关系（gstack/工具层、superpower/方法层、AgentDevFlow/流程层）|
| 验证方法 | 文档搜索 |
| 优先级 | P1 |

---

## TC-2：统一检测机制验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-02 |
| 标题 | 统一检测机制验证 |
| 前置条件 | `docs/platforms/enhancement-layer.md` 存在 |
| 测试步骤 | 搜索关键词"统一检测" |
| 预期结果 | 文档明确说明：start-agent-team 入口统一检测 gstack/superpower 是否已安装（只检测一次）|
| 验证方法 | 文档搜索 |
| 优先级 | P1 |

---

## TC-3：结果共享验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-03 |
| 标题 | 检测结果共享验证 |
| 前置条件 | `docs/platforms/enhancement-layer.md` 存在 |
| 测试步骤 | 搜索关键词"共享" |
| 预期结果 | 文档明确说明：检测结果在各 Agent 间共享，无需重复检测 |
| 验证方法 | 文档搜索 |
| 优先级 | P1 |

---

## TC-4：回落机制验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-04 |
| 标题 | 回落机制验证 |
| 前置条件 | `docs/platforms/enhancement-layer.md` 存在 |
| 测试步骤 | 搜索关键词"回落" |
| 预期结果 | 文档明确说明：均未安装时自动回落原生机制 + 提示建议安装 |
| 验证方法 | 文档搜索 |
| 优先级 | P1 |

---

## TC-5：角色增强映射验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-05 |
| 标题 | 角色增强映射表验证（6 角色）|
| 前置条件 | `docs/platforms/enhancement-layer.md` 存在 |
| 测试步骤 | 读取角色增强映射表，检查 6 个角色 |
| 预期结果 | 每个角色（PM/Architect/QA/Engineer/Team Lead/PMO）都有对应增强 skill、适用阶段和来源 |
| 验证方法 | 文档内容验证 |
| 优先级 | P1 |

---

## TC-6：输出边界验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-06 |
| 标题 | 增强层输出边界验证 |
| 前置条件 | `docs/platforms/enhancement-layer.md` 存在 |
| 测试步骤 | 搜索关键词"不能替代"或"边界" |
| 预期结果 | 文档明确说明 skill 输出不能替代 PRD/Tech/QA/Gate 结论 |
| 验证方法 | 文档搜索 |
| 优先级 | P1 |

---

## TC-7：零配置语义验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-07 |
| 标题 | 零配置语义验证 |
| 前置条件 | `docs/platforms/enhancement-layer.md` 存在 |
| 测试步骤 | 搜索"零配置"或"无需配置" |
| 预期结果 | 文档明确说明用户无需手动配置增强层 |
| 验证方法 | 文档搜索 |
| 优先级 | P2 |

---

## TC-8：角色文档增强 skill 引用验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-08 |
| 标题 | 6 个角色文档包含增强 skill 引用 |
| 前置条件 | `skills/*/SKILL.md` 存在于 main 分支 |
| 测试步骤 | 检查每个角色 SKILL.md 中是否包含增强层 skill 引用 |
| 预期结果 | 每个角色文档至少有一条增强 skill 引用 |
| 验证方法 | 文件内容验证 |
| 优先级 | P2 |

---

## TC-9：安装前置条件验证

| 字段 | 内容 |
|------|------|
| 用例 ID | TC-3-09 |
| 标题 | 安装前置条件说明验证 |
| 前置条件 | `docs/guides/enhancement-guide.md` 存在 |
| 测试步骤 | 读取增强层使用指南，确认安装前置说明 |
| 预期结果 | 文档包含 gstack + superpower skill 包的安装前置条件 |
| 验证方法 | 文档内容验证 |
| 优先级 | P2 |

---

## Gate 2 Review Record

| 日期 | 评审人 | 结论 | 关键意见 | 待办 |
|---|---|---|---|---|
| 2026-04-17 | PM | 发起评审 | Tech + QA Case 均已起草，追溯关系完整 | 等待 Engineer + QA 签字 |
| 2026-04-17 | Engineer | **Approved** ✅ | skill 名称映射准确，检测机制语义可实现，文档交付流程可行 | — |
| 2026-04-17 | QA | **Approved** ✅ | TC-1~TC-9 完整覆盖 PRD v4 Section 7，验证方法可执行，无覆盖缺口 | — |
