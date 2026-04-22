# TODO Registry

## 项目信息
- `project_id`: alpha-86-AgentDevFlow
- 当前主任务: #19（最高优先级）
- 关联治理 issue: #20（已关闭 / 已验收归档，作为返工背景保留）
- 当前阶段: #19 Gate 1 PRD v2.0 Approved（三方签字），推进 Gate 2: Tech Review
- 启动方式: 2026-04-21 团队重启（全新 session）
- 启动会纪要: `docs/memo/kickoff_2026-04-21.md`

## 角色分配

| 角色 | 状态 | Agent ID | 备注 |
|------|------|----------|------|
| Team Lead | ✅ | team-lead@alpha-86-AgentDevFlow | Human 保留角色 |
| Product Manager | ✅ | product-manager@alpha-86-AgentDevFlow | 启动文档已读 |
| 架构师 | ✅ | architect@alpha-86-AgentDevFlow | 启动文档+额外强制清单已读 |
| QA Engineer | ✅ | qa-engineer@alpha-86-AgentDevFlow | 启动文档已读 |
| Engineer | ✅ | engineer@alpha-86-AgentDevFlow | 启动文档已读 |
| Platform/SRE | ✅ | platform-sre@alpha-86-AgentDevFlow | 启动文档已读 |
| PMO | ✅ | pmo@alpha-86-AgentDevFlow | 启动文档已读 |

## 当前活跃任务

| 任务 | Issue | 负责人 | 状态 | 说明 |
|------|-------|--------|------|------|
| #3 PRD 返工并重进 Gate 1 | #3 | PM | 🔄 in_progress | 当前主任务，PRD v4.2 已产出，待重新发起 Gate 1 三方评审 |
| GOV-011 治理修复收口 | #20 | PM + PMO | ✅ completed | 已完成治理修复与正式留痕，作为 #3 返工背景保留 |

### #3 Action Items

| Action Item | Owner | Due | Evidence | Status |
|------------|-------|-----|----------|--------|
| 产出 PRD v4.2，作为回退后 Gate 1 正式输入 | PM | 2026-04-21 | `docs/prd/003_adf_enhancement_layer_2026-04-17.md` | ✅ 已完成 |
| 在 Issue #3 回写 PM 结构化 comment，声明回退到 Gate 1 | PM | 2026-04-21 | Issue #3 comment | ⏳ 待完成 |
| 组织 Gate 1 三方评审（PM + Architect + QA） | Team Lead | 2026-04-21 | Gate 1 评审结论 / Issue #3 comment | ⏳ 待完成 |

### #20 Action Items

> Issue #20 已关闭 / 已验收归档。本节仅保留归档说明，不再保留待验收 action item。

## 待处理 Issue (Open)

| Issue | 标题 | 类型 | 优先级 | 路由 | 状态 |
|-------|------|------|--------|------|------|
| #3 | gstack/superpower 增强层接入 | feature | high | PM | 已恢复，当前阶段 = Gate 1: PRD Review（返工输入 v4.2） |
| #5 | ADF 技能系统完善 | feature | medium | PM | pending |
| #8 | GOV-004 HR#1 被跳过 | process | medium | PM | ⏳ 待进入 Gate 1: PRD Review |
| #16 | GOV-009 职责归属矩阵缺失 | governance | medium | PM | pending |
| #17 | GOV-010 Skill 结构冲突 | governance | medium | PM | pending |
| #18 | Agent 获取 Issue Comment 不规范 | bug | medium | PM | pending |
| #19 | 安装脚本 bug 问题 | bug | **high** | PM | ✅ Gate 1 PRD v2.0 Approved，推进 Gate 2 Tech Review |
| #21 | prompts 原则：禁止单一 pattern 式描述 | process | medium | PM | pending |

## Gate 状态 (Issue #19 — 当前最高优先级主线)

| Gate | 状态 | 说明 |
|------|------|------|
| Gate 0: Team Startup | ✅ 已完成 | 2026-04-21 重启 |
| Gate 1: PRD Review | ✅ Approved | PRD v2.0 三方签字：PM[✅] Architect[✅] QA[✅ Conditional] |
| Gate 2: Tech Review | ✅ Approved | Tech Spec v2.0 已完成 Gate 2 收口，可作为当前有效输入 |
| QA Case Design | ✅ Approved | QA Case v2.0 已完成评审收口，可作为当前有效输入 |
| 文档 PR / HR#1 | 🔄 推进中 | PRD / Tech / QA 三份正式文档已齐备，进入文档 PR / HR#1 前置收敛 |
| Gate 3: Implementation | ⛔ 未开始 | — |
| Gate 4: QA Validation | ⛔ 未开始 | — |
| 代码 PR / HR#2 | ⛔ 未开始 | — |
| Gate 5: Release | ⛔ 未开始 | — |

## Gate 状态 (Issue #3)

| Gate | 状态 | 说明 |
|------|------|------|
| Gate 0: Team Startup | ✅ 已完成 | 2026-04-21 重启 |
| Gate 1: PRD Review | 🔄 in_progress | 已回退并重置为 PRD v4.2 输入，待重新三方评审 |
| Gate 2: Tech Review | ⛔ 未开始 | 旧 Tech Review 仅作历史留档，不作为当前有效前提 |
| QA Case Design | ⛔ 未开始 | 旧 QA Case 仅作历史留档，不作为当前有效前提 |
| 文档 PR / HR#1 | ⛔ 未开始 | 待 Gate 1 / Gate 2 / QA Case 重新完成 |
| Gate 3: Implementation | ⛔ 未开始 | — |
| Gate 4: QA Validation | ⛔ 未开始 | — |
| 代码 PR / HR#2 | ⛔ 未开始 | — |
| Gate 5: Release | ⛔ 未开始 | — |

## 启动会

- 时间: 2026-04-21
- 负责人: Team Lead
- 结论: 团队重启后，当前主线已切换为 Issue #3 的 PRD 返工与 Gate 1 重审
- 纪要: `docs/memo/kickoff_2026-04-21.md`

## 历史审计记录（2026-04-17，Issue #3）

**触发原因**：Human 对 PM 工作严重不满，Team Lead 要求 PMO 紧急介入

| # | 违规项 | 违规归属 | 当前状态 |
|---|--------|---------|---------|
| 1 | PRD 命名不符合标准（`PRD-3_v3.md`） | PM（初次）→ Human（rename 已纠正） | ✅ 已纠正 |
| 2 | 直接 push 到 main 而非通过 PR | Human 操作，PMO 审计范围外 | ⚠️ 待规范 |
| 3 | 在 Human 确认前发起 Gate 1 评审（声称 v3 "Human 确认" 但缺乏独立证据） | PM | ⚠️ 本轮 Gate 1 前仍需补齐证据 |
| 4 | PR #1 不存在（历史示例文件误解） | PM 误解 | ✅ 已澄清 |
| 5 | PM 发布 Issue 关闭评论（Issue 关闭是 Human 专属） | PM Agent（历史） | ✅ Human 已重新打开纠正 |

**纠正动作**：
- P0：PM 重新阅读 SKILL.md，明确 Issue 关闭 Human 专属边界（负责人：PM）
- P1：在 `003_document_contracts.md` 补充 PRD 命名反面示例（负责人：PMO）
- P1：在 `skills/workflows/prd-review.md` 明确"Human 确认"需独立 Issue 评论证据（负责人：PMO）
- P2：明确 Human 直接 push 与 PR 提交的边界（负责人：PMO/Team Lead）
