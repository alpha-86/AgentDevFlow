# 项目状态板 — AgentDevFlow (2026-04-21)

## 项目概览

| 字段 | 值 |
|------|-----|
| project_id | alpha-86-AgentDevFlow |
| 当前主任务 | Issue #20 (GOV-011 治理修复) |
| 暂停任务 | Issue #3 (gstack/superpower) — 关联业务 issue，待 #20 完成后恢复 |
| Team Lead | Human (alpha-86) |
| 最后更新 | 2026-04-21 |

## 活跃任务

| Issue | 标题 | 阶段 | Owner | 状态 | 阻塞项 |
|-------|------|------|-------|------|--------|
| #20 | GOV-011 HR#1 流程违规 | 治理修复 | PM + PMO | 治理修复主体已完成，待同步正式留痕并验收 | 待 Team Lead / PMO 验收确认 |
| #3 | gstack/superpower 增强层接入 | ⏸️ 暂停 | PM | ⏸️ 暂停 | 等 Issue #20 完成 |

## Open Issues 队列 (9 个)

| Issue | 标题 | 类型 | 优先级 | 状态 |
|-------|------|------|--------|------|
| #20 | GOV-011 HR#1 流程违规 | governance | medium | 🔄 in_progress |
| #3 | gstack/superpower 增强层接入 | feature | high | ⏸️ 暂停 |
| #5 | AgentDevFlow bootstrap 完善 | feature | medium | pending |
| #8 | GOV-004 HR#1 被跳过 | process | medium | pending |
| #16 | GOV-009 职责归属矩阵缺失 | governance | medium | pending |
| #17 | GOV-010 Skill 结构冲突 | governance | medium | pending |
| #18 | Agent 获取 Issue Comment 不规范 | bug | medium | pending |
| #19 | 安装脚本 bug 问题 | bug | medium | pending |
| #21 | prompts 原则：禁止单一 pattern 式描述 | process | medium | pending |

## 团队状态

| 角色 | 初始化 | 当前工作 |
|------|--------|---------|
| Product Manager | ✅ | 等待分派 #20 正式检查范围 |
| PMO | ✅ | 等待分派 #20 正式审计范围 |
| 架构师 | ✅ | 可执行 #20 架构合规审查 |
| QA Engineer | ✅ | 可执行 #20 QA 验证清单核查 |
| Engineer | ✅ | 可执行 #20 实现前置条件核查 |
| Platform/SRE | ✅ | GOV-011 平台侧现状核查 |

## 风险与阻塞

| # | 风险 | 级别 | Owner | 缓解措施 |
|---|------|------|-------|---------|
| 1 | Issue #3 曾发生 PRD 变更未重新走 Gate 1 | P1 | PM + PMO | Issue #20 产出修复方案 |
| 2 | Issue #3 各 Agent 状态判断不一致 | P2 | PMO | Issue #20 完成后统一审计 |
| 3 | 9 个 open issues 堆积 | P2 | Team Lead | 按优先级逐个处理 |

## 产物关联

- 启动会纪要: `docs/memo/kickoff_2026-04-21.md`
- 待办注册: `docs/todo/TODO_REGISTRY.md`
- 项目状态板: `docs/memo/project_status_2026-04-21.md` (本文件)
- PM 结构化评论草稿: `docs/memo/issue_20_pm_structured_comment_draft_2026-04-21.md`
- GOV-011 治理决议: `docs/pmo/resolutions/GOV-011_2026-04-20_change_propagation_gate_violation_resolution.md`
- PMO Issue 011: `docs/pmo/issues/011_2026-04-20_governance_hr1_rejected_and_gate_violation.md`
