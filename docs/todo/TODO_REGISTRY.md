# TODO Registry

## 项目信息
- `project_id`: alpha-86-AgentDevFlow
- 当前主任务: #20
- 关联业务 issue: #3（暂停中，待 #20 完成后恢复）
- 当前阶段: #20 治理修复主体已完成，待同步正式留痕并验收；#3 Gate 2 Tech Review 暂停
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
| GOV-011 治理修复 | #20 | PM + PMO | 🔄 in_progress | 最高优先级，Issue #3 暂停 |

### #20 Action Items

| Action Item | Owner | Due | Evidence | Status |
|------------|-------|-----|----------|--------|
| 同步主线留痕：registry / kickoff / status board 口径一致 | PM | 2026-04-21 | `docs/todo/TODO_REGISTRY.md`, `docs/memo/kickoff_2026-04-21.md`, `docs/memo/project_status_2026-04-21.md` | ✅ 已完成 |
| 准备 PM 结构化评论草稿，待正式回写 Issue #20 | PM | 2026-04-21 | `docs/memo/issue_20_pm_structured_comment_draft_2026-04-21.md` | ✅ 已完成 |
| Team Lead / PMO 对治理修复结果执行验收确认 | Team Lead + PMO | 2026-04-21 | Issue #20 验收评论 / 后续验收留痕 | ⏳ 待完成 |

## 待处理 Issue (Open)

| Issue | 标题 | 类型 | 优先级 | 路由 | 状态 |
|-------|------|------|--------|------|------|
| #20 | GOV-011 HR#1 流程违规 | governance | medium | PM + PMO | 治理修复主体已完成，待同步正式留痕并验收 |
| #3 | gstack/superpower 增强层接入 | feature | high | PM | ⏸️ 暂停（关联业务 issue，等 #20 完成后恢复） |
| #5 | ADF 技能系统完善 | feature | medium | PM | pending |
| #8 | GOV-004 HR#1 被跳过 | process | medium | PMO | pending |
| #16 | GOV-009 职责归属矩阵缺失 | governance | medium | PM | pending |
| #17 | GOV-010 Skill 结构冲突 | governance | medium | PM | pending |
| #18 | Agent 获取 Issue Comment 不规范 | bug | medium | PM | pending |
| #19 | 安装脚本 bug 问题 | bug | medium | PM | pending |
| #21 | prompts 原则：禁止单一 pattern 式描述 | process | medium | PM | pending |

## Gate 状态 (Issue #3 — 暂停)

| Gate | 状态 | 说明 |
|------|------|------|
| Gate 0: Team Startup | ✅ 已完成 | 2026-04-21 重启 |
| Gate 1: PRD Review | ✅ 历史通过 | v4.1 (2026-04-17) |
| Gate 2: Tech Review | ⏸️ 暂停 | 待 Issue #20 完成后恢复 |
| QA Case Design | ⏸️ 暂停 | — |
| 文档 PR / HR#1 | ⏸️ 暂停 | — |
| Gate 3: Implementation | ⏸️ 暂停 | — |
| Gate 4: QA Validation | ⏸️ 暂停 | — |
| 代码 PR / HR#2 | ⏸️ 暂停 | — |
| Gate 5: Release | ⏸️ 暂停 | — |

## 启动会

- 时间: 2026-04-21
- 负责人: Team Lead
- 结论: 团队重启，6 个 Agent 初始化完成，当前聚焦 Issue #20 治理修复
- 纪要: `docs/memo/kickoff_2026-04-21.md`

## 历史审计记录（2026-04-17，Issue #3）

**触发原因**：Human 对 PM 工作严重不满，Team Lead 要求 PMO 紧急介入

| # | 违规项 | 违规归属 | 当前状态 |
|---|--------|---------|---------|
| 1 | PRD 命名不符合标准（`PRD-3_v3.md`） | PM（初次）→ Human（rename 已纠正） | ✅ 已纠正 |
| 2 | 直接 push 到 main 而非通过 PR | Human 操作，PMO 审计范围外 | ⚠️ 待规范 |
| 3 | 在 Human 确认前发起 Gate 1 评审（声称 v3 "Human 确认" 但缺乏独立证据） | PM | ⚠️ 待 PM 区分"Human 反馈"与"Human 确认" |
| 4 | PR #1 不存在（历史示例文件误解） | PM 误解 | ✅ 已澄清 |
| 5 | PM 发布 Issue 关闭评论（Issue 关闭是 Human 专属） | PM Agent（历史） | ✅ Human 已重新打开纠正 |

**纠正动作**：
- P0：PM 重新阅读 SKILL.md，明确 Issue 关闭 Human 专属边界（负责人：PM）
- P1：在 `003_document_contracts.md` 补充 PRD 命名反面示例（负责人：PMO）
- P1：在 `skills/workflows/prd-review.md` 明确"Human 确认"需独立 Issue 评论证据（负责人：PMO）
- P2：明确 Human 直接 push 与 PR 提交的边界（负责人：PMO/Team Lead）
