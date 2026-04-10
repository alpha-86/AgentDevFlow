# hedge-ai 研发机制拆解到独立插件的迁移矩阵

## 说明

- 本矩阵只服务一个目标：把 `hedge-ai` 中可迁移的研发机制拆出来，形成独立插件。
- 每一行都必须能回答：
  - 源文件是什么
  - 可迁移机制是什么
  - 在本仓库落到哪里
  - 在插件层如何承载
- “禁止迁移”表示该源文件主要属于量化交易业务语义，不能进入插件主干。

## A. 顶层入口与依赖

| 源文件 | 机制摘要 | 判定 | 当前仓库落点 | 插件落点 | 状态 |
|---|---|---|---|---|---|
| `prompts/V3.0/README.md` | 启动指南、阅读顺序、角色必读分配、双阶段流程总览、恢复入口 | 可迁移 | `README.md`、`docs/zh-cn/README.md` | `plugins/agentdevpipeline/README.md` | 已复核；插件入口仍偏薄，需在 Phase 3 收口 |
| `prompts/V3.0/CHANGELOG.md` | 版本化变更记录主索引，联动 change_record 明细 | 可迁移 | 当前缺严格对应落点 | 根 `CHANGELOG.md` | 已复核；需在 Phase 3 建立正式 CHANGELOG |
| `prompts/V3.0/014_ClaudeSkills与Agent依赖.md` | 平台 Skills 依赖矩阵、角色依赖关系 | 可迁移 | `docs/zh-cn/reference/dependencies.md`、`skills/shared/README.md` | `plugins/agentdevpipeline/README.md` | 未充分插件化 |
| `.claude/skills/TEAM_SETUP.md` | 团队初始化顺序、前置条件、恢复入口 | 可迁移 | `skills/shared/team-setup.md` | `plugins/agentdevpipeline/README.md` + 共享入口 | 已初步落地 |
| `.claude/skills/start-agent-team/SKILL.md` | 团队启动统一入口 | 可迁移 | `skills/shared/start-agent-team.md` | 插件内启动入口说明 | 已初步落地 |
| `.claude/skills/create-agent/SKILL.md` | 角色统一创建入口 | 可迁移 | `skills/shared/create-agent.md` | 插件内角色激活入口 | 已初步落地 |
| `.claude/skills/SKILL_PROTOCOL.md` | 角色 / workflow / template 使用顺序 | 可迁移 | `skills/shared/skill-protocol.md` | 插件共享协议 | 已初步落地 |

## B. 角色机制

| 源文件 | 机制摘要 | 判定 | 当前仓库落点 | 插件落点 | 状态 |
|---|---|---|---|---|---|
| `.claude/skills/AGENTS/team-lead.md` | 团队协调、会议前读 workflow、QA 触发、评论约束 | 可迁移 | `skills/shared/agents/team-lead.md` | 插件角色包 | 已迁移，但还需继续细化 |
| `.claude/skills/AGENTS/pm-agent.md` | 文档阶段 owner、Issue 主线、双阶段交付、Gate 前置 | 可迁移 | `skills/shared/agents/product-manager.md` | 插件角色包 | 已迁移，但还需继续细化 |
| `.claude/skills/AGENTS/cto-agent.md` | 技术评审 owner、架构边界、签字机制 | 可迁移 | `skills/shared/agents/tech-lead.md` | 插件角色包 | 已迁移，但需逐项再核 |
| `.claude/skills/AGENTS/engineer-agent.md` | 前置检查、开发拒绝机制、实现后交 QA | 可迁移 | `skills/shared/agents/engineer.md` | 插件角色包 | 已迁移，但需逐项再核 |
| `.claude/skills/AGENTS/qa-agent.md` | QA 介入、测试报告、验收约束 | 可迁移 | `skills/shared/agents/qa-engineer.md` | 插件角色包 | 已迁移，但需逐项再核 |
| `.claude/skills/AGENTS/sre-agent.md` | 平台保障、发布/回滚、平台检查 | 可迁移 | `skills/shared/agents/platform-sre.md` | 插件角色包 | 已迁移 |
| `.claude/skills/AGENTS/pmo-agent.md` | 流程合规主动检查机制 | 可迁移 | `skills/shared/agents/process-auditor.md` | 插件治理角色包 | 已迁移，但需继续对齐源文档 |
| `.claude/skills/AGENTS/research-agent.md` | 通用研究支持、信息澄清与前期调研 | 部分迁移 | `skills/shared/agents/researcher.md` | 插件角色包 | 已部分迁移 |
| `.claude/skills/AGENTS/evaluation/*.md` | 完整性 / 一致性 / 逻辑 / 证据检查 | 可迁移 | `prompts/zh-cn/015_review_evaluation_dimensions.md` | 插件评审子能力 | 尚未充分产品化 |

## C. Workflow 机制

| 源文件 | 机制摘要 | 判定 | 当前仓库落点 | 插件落点 | 状态 |
|---|---|---|---|---|---|
| `.claude/skills/WORKFLOWS/prd-review.md` | PRD Gate | 可迁移 | `skills/shared/workflows/prd-review.md` | 插件 workflow 包 | 已迁移 |
| `.claude/skills/WORKFLOWS/tech-review.md` | Tech Gate | 可迁移 | `skills/shared/workflows/tech-review.md` | 插件 workflow 包 | 已迁移 |
| `.claude/skills/WORKFLOWS/daily-standup.md` | 研发日会、Todo Review、Blocker 升级 | 可迁移 | `skills/shared/workflows/daily-sync.md` | 插件 workflow 包 | 已迁移，但还需逐项对齐 |
| `.claude/skills/WORKFLOWS/todo-management.md` | Todo 全局管理 | 可迁移 | `skills/shared/workflows/todo-review.md` | 插件 workflow 包 | 已迁移 |
| `.claude/skills/WORKFLOWS/weekly-review.md` | 周复盘 | 可迁移 | `skills/shared/workflows/weekly-review.md` | 插件 workflow 包 | 已迁移 |
| `.claude/skills/WORKFLOWS/monthly-review.md` | 月复盘 | 可迁移 | `skills/shared/workflows/monthly-review.md` | 插件 workflow 包 | 已迁移 |
| `.claude/skills/WORKFLOWS/anomaly-iteration.md` | 异常闭环 | 部分迁移 | `skills/shared/workflows/anomaly-response.md` | 插件 workflow 包 | 已部分迁移 |
| `.claude/skills/WORKFLOWS/debate.md` | 对抗式评审 | 部分迁移 | `prompts/zh-cn/015_review_evaluation_dimensions.md`、`005/014` 相关文档 | 插件评审补充能力 | 仍偏弱 |

## D. 文档与变更机制

| 源文件 | 机制摘要 | 判定 | 当前仓库落点 | 插件落点 | 状态 |
|---|---|---|---|---|---|
| `prompts/V3.0/011_文档规范.md` | 文档契约、命名、状态、变更等级 | 可迁移 | `prompts/zh-cn/003_document_contracts.md` | 插件规则层 | 已迁移 |
| `prompts/V3.0/015_会议记录规范.md` | Memo 结构、目录和命名规则 | 可迁移 | `prompts/zh-cn/005_meeting_and_todo.md`、`docs/memo/README.md` | 插件模板与目录约束 | 已迁移 |
| `prompts/V3.0/016_Todo管理机制.md` | Todo 注册表、闭环、跟踪 | 可迁移 | `prompts/zh-cn/005_meeting_and_todo.md`、`docs/todo/TODO_REGISTRY.md` | 插件模板与 workflow | 已迁移 |
| `change_record/V1.0_*.md` | PRD / Tech / 代码一致性变更管理 | 可迁移 | `prompts/zh-cn/008_change_record_and_revalidation.md` | 插件变更管理能力 | 已迁移 |
| `change_record/V2.2_双PR机制引入.md` | 文档阶段 + 代码阶段双阶段 PR 机制 | 可迁移 | `prompts/zh-cn/019_dual_stage_pr_and_three_layer_safeguard.md`、`017_human_review_and_signoff.md` | 插件双阶段交付能力 | 已迁移，但 README 仍需改为插件口径 |
| `change_record/V2.2.5_Issue_Comment机制修复与强制Gate建立.md` | 评论门禁、结构化评论、Gate 不可绕过 | 可迁移 | `prompts/zh-cn/013_github_issue_and_review_comments.md`、`020_issue_comment_gate_and_artifact_linkage.md` | 插件评论 / Gate 能力 | 已迁移 |
| `change_record/V2.6_PMO-Agent引入_流程合规主动检查机制.md` | 流程合规主动检查 | 可迁移 | `prompts/zh-cn/014_process_compliance_and_audit.md`、`skills/shared/agents/process-auditor.md` | 插件治理能力 | 已迁移 |

## E. 禁止进入插件主干的源

| 源文件 | 原因 |
|---|---|
| `007_策略研究指南.md` | 量化策略研究专属 |
| `008_因子研究与因子库.md` | 因子体系专属 |
| `009_回测报告设计.md` / `014_回测报告模板.md` | 回测专属 |
| `WORKFLOWS/strategy-review.md` / `strategy-debate.md` / `factor-review.md` / `backtest-review.md` | 交易业务专属 |
| `AGENTS/backtest-agent.md` / `bull-agent.md` / `bear-agent.md` / `cro.md` | 交易业务专属 |
| `change_record/V2.5_DBR例会调整为每日4次.md` | 交易运营节奏专属 |

## 当前最关键缺口

1. 根 `README.md` 仍未完全达到 hedge-ai 顶层启动指南的插件化强度。
2. `plugins/agentdevpipeline/README.md` 太薄，尚未成为真正的插件入口。
3. 根 `CHANGELOG.md` 尚未建立，无法对应 hedge-ai 的版本变更主索引机制。
4. 还缺更严格的“逐源文件 -> 当前文件”映射覆盖检查。
5. 个别迁移资产已经存在，但需要回到源文件逐项复核，防止混入自我发挥。
