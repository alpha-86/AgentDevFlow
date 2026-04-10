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
| `prompts/V3.0/README.md` | 启动指南、阅读顺序、角色必读分配、双阶段流程总览、恢复入口 | 可迁移 | `README.md`、`docs/README.md` | `plugins/agentdevflow/README.md` | 已复核；主入口已成型，仍可继续收紧插件装载说明 |
| `prompts/V3.0/CHANGELOG.md` | 版本化变更记录主索引，联动 change_record 明细 | 可迁移 | 根 `CHANGELOG.md` | 根 `CHANGELOG.md` | 已在 Phase 3.6 建立中文主版本 CHANGELOG 方案与主索引联动 |
| `prompts/V3.0/014_ClaudeSkills与Agent依赖.md` | 平台 Skills 依赖矩阵、角色依赖关系 | 可迁移 | `docs/reference/dependencies.md`、`skills/shared/README.md` | `plugins/agentdevflow/README.md` | 已复核；依赖边界已收口，安装说明仍可继续强化 |
| `.claude/skills/TEAM_SETUP.md` | 团队初始化顺序、前置条件、恢复入口 | 可迁移 | `skills/shared/team-setup.md` | `plugins/agentdevflow/README.md` + 共享入口 | 已复核；属于插件启动主干 |
| `.claude/skills/start-agent-team/SKILL.md` | 团队启动统一入口 | 可迁移 | `skills/shared/start-agent-team.md` | 插件内启动入口说明 | 已初步落地 |
| `.claude/skills/create-agent/SKILL.md` | 角色统一创建入口 | 可迁移 | `skills/shared/create-agent.md` | 插件内角色激活入口 | 已初步落地 |
| `.claude/skills/SKILL_PROTOCOL.md` | 角色 / workflow / template 使用顺序、状态机、失败恢复 | 可迁移 | `skills/shared/skill-protocol.md` | 插件共享协议主干 | 已复核；属于插件协议主干 |
| `.claude/skills/EVENT_BUS.md` | 事件总线架构、事件格式、触发与订阅 | 可迁移 | `skills/shared/event-bus.md` | 插件共享编排协议 | 已复核；只能保留抽象结构 |
| `.claude/skills/ANOMALY_LOOP.md` | 异常闭环、优先级、case 状态机 | 部分迁移 | `prompts/012_anomaly_and_escalation_loop.md`、`skills/shared/workflows/anomaly-response.md` | 插件异常闭环能力 | 已复核；需持续去业务语义 |
| `.claude/skills/github-issue.md` | GitHub Issue 流程约束、字段要求、流转规范 | 可迁移 | `prompts/007_issue_driven_orchestration.md`、`013_github_issue_and_review_comments.md` | 插件 Issue 主线规则 | 已复核；Phase 2 深化 |
| `.claude/skills/github-issue/SKILL.md` | Issue skill 调用入口、执行顺序、约束包装 | 可迁移 | 当前缺严格对应共享入口 | 插件 Issue skill 入口说明 | 已复核；仍缺更明确插件承载位置 |
| `.claude/skills/review-org/SKILL.md` | 组织化评审入口、全量阅读、系统性输出约束 | 可迁移 | `prompts/discuss/` 当前执行口径、`prompts/009_review_rigor_and_context_recovery.md` | 插件评审入口约束 | 已复核；仍缺更明确插件承载位置 |

## A1. 主文档 001-016, 019

| 源文件 | 机制摘要 | 判定 | 当前仓库落点 | 插件落点 | 状态 |
|---|---|---|---|---|---|
| `001_Agent团队架构.md` | 团队协作结构、评审链路、人机协作关系 | 部分迁移 | `prompts/001_team_topology.md` | 插件组织结构规则 | 已复核；需持续去业务语义 |
| `002_Agent工具设计.md` | 量化数据/研究/回测工具接口 | 禁止迁移 | 不进入主干 | 不进入插件主干 | 已复核 |
| `003_产品工程师Agent.md` | PM / Engineer 职责、PRD 生命周期、需求到开发主链路 | 可迁移 | `prompts/002_product_engineering_roles.md`、`skills/shared/agents/product-manager.md`、`skills/shared/agents/engineer.md` | 插件角色主干 | 已复核；仍需逐项细化 |
| `004_工作流程规范.md` | 工作流节奏、评审与异常处理主链路 | 部分迁移 | `prompts/004_delivery_gates.md`、`005_meeting_and_todo.md` | 插件 workflow 主干 | 已复核；需持续去交易节奏 |
| `005_人机交互规范.md` | 人与 Agent 协作约束 | 部分迁移 | `prompts/006_agent_creation_contract.md`、`013_github_issue_and_review_comments.md` | 插件交互约束 | 已复核；需排除 Telegram 语义 |
| `006_辩论机制与案例.md` | 对抗式评审方法 | 部分迁移 | `prompts/015_review_evaluation_dimensions.md` | 插件评审补充能力 | 已复核；方法可保留，案例不迁移 |
| `007_策略研究指南.md` | 量化策略研究 | 禁止迁移 | 不进入主干 | 不进入插件主干 | 已复核 |
| `008_因子研究与因子库.md` | 因子研究体系 | 禁止迁移 | 不进入主干 | 不进入插件主干 | 已复核 |
| `009_回测报告设计.md` | 回测设计与指标 | 禁止迁移 | 不进入主干 | 不进入插件主干 | 已复核 |
| `010_日报迭代规范.md` | 日报与迭代复盘结构 | 部分迁移 | `prompts/005_meeting_and_todo.md` | 插件进展日报结构 | 已复核；只保留通用日报机制 |
| `011_文档规范.md` | 文档契约、命名、状态、变更等级 | 可迁移 | `prompts/003_document_contracts.md` | 插件规则主干 | 已复核 |
| `012_交付物Checklist.md` | 交付检查与 Gate 检查思路 | 部分迁移 | `prompts/004_delivery_gates.md` | 插件交付检查能力 | 已复核；需持续去业务口径 |
| `013_ai_driving_ai.md` | 多 agent 编排与自动协作方法 | 部分迁移 | `prompts/011_event_bus_and_handoff.md`、`014_process_compliance_and_audit.md` | 插件编排方法 | 已复核；需持续去业务上下文 |
| `014_ClaudeSkills与Agent依赖.md` | Skills 依赖治理 | 可迁移 | `docs/reference/dependencies.md` | 插件依赖说明 | 已复核；Phase 4 深化 |
| `014_回测报告模板.md` | 回测模板 | 禁止迁移 | 不进入主干 | 不进入插件主干 | 已复核 |
| `015_会议记录规范.md` | Memo 强制留痕、目录与命名规则 | 可迁移 | `prompts/005_meeting_and_todo.md`、`docs/memo/README.md` | 插件会议留痕主干 | 已复核 |
| `016_Todo管理机制.md` | Todo 闭环与 Review | 可迁移 | `prompts/005_meeting_and_todo.md`、`docs/todo/TODO_REGISTRY.md` | 插件 Todo 主干 | 已复核 |
| `019_TeamLead职责边界.md` | Team Lead 边界、AI 驱动 AI、Agent 创建规范 | 可迁移 | `skills/shared/agents/team-lead.md`、`prompts/006_agent_creation_contract.md` | 插件协调与创建主干 | 已复核 |

## B. 角色机制

| 源文件 | 机制摘要 | 判定 | 当前仓库落点 | 插件落点 | 状态 |
|---|---|---|---|---|---|
| `.claude/skills/AGENTS/team-lead.md` | 团队协调、会议前读 workflow、QA 触发、评论约束 | 可迁移 | `skills/shared/agents/team-lead.md` | 插件主干角色包 | 已复核；属于插件主干角色 |
| `.claude/skills/AGENTS/pm-agent.md` | 文档阶段 owner、Issue 主线、双阶段交付、Gate 前置 | 可迁移 | `skills/shared/agents/product-manager.md` | 插件主干角色包 | 已复核；属于插件主干角色 |
| `.claude/skills/AGENTS/cto-agent.md` | 技术评审 owner、架构边界、签字机制 | 可迁移 | `skills/shared/agents/tech-lead.md` | 插件主干角色包 | 已复核；属于插件主干角色 |
| `.claude/skills/AGENTS/engineer-agent.md` | 前置检查、开发拒绝机制、实现后交 QA | 可迁移 | `skills/shared/agents/engineer.md` | 插件主干角色包 | 已复核；属于插件主干角色 |
| `.claude/skills/AGENTS/qa-agent.md` | QA 介入、测试报告、验收约束 | 可迁移 | `skills/shared/agents/qa-engineer.md` | 插件主干角色包 | 已复核；属于插件主干角色 |
| `.claude/skills/AGENTS/sre-agent.md` | 平台保障、发布/回滚、平台检查 | 可迁移 | `skills/shared/agents/platform-sre.md` | 插件主干角色包 | 已复核；属于插件主干角色 |
| `.claude/skills/AGENTS/pmo-agent.md` | 流程合规主动检查机制 | 可迁移 | `skills/shared/agents/process-auditor.md` | 插件治理主干角色包 | 已复核；属于插件主干角色 |
| `.claude/skills/AGENTS/research-agent.md` | 通用研究支持、信息澄清与前期调研 | 部分迁移 | `skills/shared/agents/researcher.md` | 插件补充角色包 | 已复核；仅保留通用研究方法 |
| `.claude/skills/AGENTS/risk-agent.md` | 风险识别与缓解建议 | 部分迁移 | 当前无严格对应主角色 | 插件补充风险方法 | 已复核；仅保留工程风险方法 |
| `.claude/skills/AGENTS/cso.md` | 量化策略负责人角色 | 部分迁移 | 当前无直接主干对应 | 不作为插件主角色主干 | 已复核；仅可参考通用治理方法 |
| `.claude/skills/AGENTS/backtest-agent.md` | 回测执行与回测报告生成 | 禁止迁移 | 不进入主干 | 不进入插件主干 | 已复核 |
| `.claude/skills/AGENTS/bull-agent.md` | 策略辩论看多方 | 禁止迁移 | 不进入主干 | 不进入插件主干 | 已复核 |
| `.claude/skills/AGENTS/bear-agent.md` | 策略辩论看空方 | 禁止迁移 | 不进入主干 | 不进入插件主干 | 已复核 |
| `.claude/skills/AGENTS/cro.md` | 交易风险负责人角色 | 禁止迁移 | 不进入主干 | 不进入插件主干 | 已复核 |
| `.claude/skills/AGENTS/evaluation/*.md` | 完整性 / 一致性 / 逻辑 / 证据检查 | 可迁移 | `prompts/015_review_evaluation_dimensions.md`、`skills/shared/templates/review-comment-checklist-template.md`、`skills/shared/templates/audit-report-template.md` | 插件评审子能力 | 已复核；已从维度说明推进到更明确的检查器类型与模板字段 |

## C. Workflow 机制

| 源文件 | 机制摘要 | 判定 | 当前仓库落点 | 插件落点 | 状态 |
|---|---|---|---|---|---|
| `.claude/skills/WORKFLOWS/prd-review.md` | PRD Gate | 可迁移 | `skills/shared/workflows/prd-review.md` | 插件主干 workflow 包 | 已复核；属于插件主干 workflow |
| `.claude/skills/WORKFLOWS/tech-review.md` | Tech Gate | 可迁移 | `skills/shared/workflows/tech-review.md` | 插件主干 workflow 包 | 已复核；属于插件主干 workflow |
| `.claude/skills/WORKFLOWS/daily-standup.md` | 研发日会、Todo Review、Blocker 升级 | 可迁移 | `skills/shared/workflows/daily-sync.md` | 插件主干 workflow 包 | 已复核；需继续去交易议程字段 |
| `.claude/skills/WORKFLOWS/todo-management.md` | Todo 全局管理 | 可迁移 | `skills/shared/workflows/todo-review.md` | 插件主干 workflow 包 | 已复核；属于插件主干 workflow |
| `.claude/skills/WORKFLOWS/weekly-review.md` | 周复盘 | 可迁移 | `skills/shared/workflows/weekly-review.md` | 插件主干 workflow 包 | 已复核；属于插件主干 workflow |
| `.claude/skills/WORKFLOWS/monthly-review.md` | 月复盘 | 可迁移 | `skills/shared/workflows/monthly-review.md` | 插件主干 workflow 包 | 已复核；属于插件主干 workflow |
| `.claude/skills/WORKFLOWS/anomaly-iteration.md` | 异常闭环 | 部分迁移 | `skills/shared/workflows/anomaly-response.md` | 插件异常 workflow | 已复核；仅保留通用异常闭环 |
| `.claude/skills/WORKFLOWS/debate.md` | 对抗式评审 | 部分迁移 | `prompts/015_review_evaluation_dimensions.md`、`005/014` 相关文档 | 插件评审补充能力 | 已复核；只保留方法框架 |
| `.claude/skills/WORKFLOWS/daily-report.md` | 日报生成 | 部分迁移 | 当前无主干 workflow 对应 | 不作为插件主干 workflow | 已复核；只可参考通用日报结构 |
| `.claude/skills/WORKFLOWS/risk-report.md` | 风险日报 | 部分迁移 | 当前无主干 workflow 对应 | 不作为插件主干 workflow | 已复核；只可参考工程风险汇报结构 |
| `.claude/skills/WORKFLOWS/strategy-review.md` | 策略评审 | 禁止迁移 | 不进入主干 | 不进入插件主干 | 已复核 |
| `.claude/skills/WORKFLOWS/strategy-debate.md` | 策略辩论 | 禁止迁移 | 不进入主干 | 不进入插件主干 | 已复核 |
| `.claude/skills/WORKFLOWS/factor-review.md` | 因子评审 | 禁止迁移 | 不进入主干 | 不进入插件主干 | 已复核 |
| `.claude/skills/WORKFLOWS/backtest-review.md` | 回测评审 | 禁止迁移 | 不进入主干 | 不进入插件主干 | 已复核 |

## D. 文档与变更机制

| 源文件 | 机制摘要 | 判定 | 当前仓库落点 | 插件落点 | 状态 |
|---|---|---|---|---|---|
| `prompts/V3.0/011_文档规范.md` | 文档契约、命名、状态、变更等级 | 可迁移 | `prompts/003_document_contracts.md` | 插件规则层 | 已迁移 |
| `prompts/V3.0/015_会议记录规范.md` | Memo 结构、目录和命名规则 | 可迁移 | `prompts/005_meeting_and_todo.md`、`docs/memo/README.md` | 插件模板与目录约束 | 已迁移 |
| `prompts/V3.0/016_Todo管理机制.md` | Todo 注册表、闭环、跟踪 | 可迁移 | `prompts/005_meeting_and_todo.md`、`docs/todo/TODO_REGISTRY.md` | 插件模板与 workflow | 已迁移 |
| `change_record/V1.0_*.md` | PRD / Tech / 代码一致性变更管理 | 可迁移 | `prompts/008_change_record_and_revalidation.md` | 插件变更管理能力 | 已迁移 |
| `change_record/V1.2_review_org_支持subagent及change_record.md` | review 结果必须沉淀 change_record，并与 CHANGELOG 联动 | 可迁移 | 当前仅部分散落在 `prompts/discuss/` | 插件变更记录规范 | 已复核；需在 Phase 3 建立正式 CHANGELOG 联动 |
| `change_record/V1.3_review_org_强化文档阅读与系统性方案要求.md` | 先读全量文档，再输出系统性方案 | 可迁移 | `prompts/discuss/` 当前执行口径 | 插件审计 / review 约束 | 已复核；需继续固化为插件规则 |
| `change_record/V2.0_研发流程与GitHubIssue结合及QA角色引入.md` | Issue First + QA 正式进入研发主链路 | 可迁移 | `prompts/007_issue_driven_orchestration.md`、`004/005/013` 相关文档、`docs/governance/core-principles.md` | 插件 Issue / QA 主骨架 | Issue First 已在 Phase 2.1 深化；QA Gate 继续在后续项深化 |
| `change_record/V2.1_P0修复_QA_V2.0_review_critical_rules强化.md` | 流程变更后，Critical Rules 必须同步修正 | 可迁移 | `skills/shared/agents/*` | 插件角色规则校验 | 已复核；Phase 5 深化 |
| `change_record/V2.1_V2.0变更review及Agent_Critical_Rules验证.md` | 流程变更需要复核并验证角色规则是否一致 | 可迁移 | `prompts/discuss/`、`skills/shared/agents/*` | 插件复核机制 | 已复核 |
| `change_record/V2.2_双PR机制引入.md` | 文档阶段 + 代码阶段双阶段 PR 机制 | 可迁移 | `prompts/019_dual_stage_pr_and_three_layer_safeguard.md`、`017_human_review_and_signoff.md`、`skills/shared/workflows/human-review.md`、`docs/governance/core-principles.md` | 插件双阶段交付能力 | 双阶段 PR 与三层保障体系已在 Phase 2.2 深化；README 流程图仍需后续校准 |
| `change_record/V2.2.5_Issue_Comment机制修复与强制Gate建立.md` | 评论门禁、结构化评论、Gate 不可绕过 | 可迁移 | `prompts/013_github_issue_and_review_comments.md`、`020_issue_comment_gate_and_artifact_linkage.md`、`skills/shared/templates/review-comment-checklist-template.md`、`docs/governance/core-principles.md` | 插件评论 / Gate 能力 | Issue Comment Gate 已在 Phase 2.3 深化；后续仍需补更明确的插件入口约束 |
| `change_record/V2.3_Gate_流程保障机制.md` | Gate 保障、三层保障体系、友好错误信息 | 可迁移 | `prompts/019_dual_stage_pr_and_three_layer_safeguard.md`、`021_platform_checks_and_gate_automation.md` | 插件 Gate 保障能力 | 已复核；需继续校准与源文档一致性 |
| `change_record/V2.3_Tech_Gate签字定义统一.md` | Tech Gate 签字口径统一 | 可迁移 | `prompts/004_delivery_gates.md` | 插件签字规则统一 | 已复核 |
| `change_record/V2.5_DBR例会调整为每日4次.md` | DBR 交易运营节奏调整 | 禁止迁移 | 不进入主干 | 不进入插件主干 | 已复核 |
| `change_record/V2.6_PMO-Agent引入_流程合规主动检查机制.md` | 流程合规主动检查 | 可迁移 | `prompts/014_process_compliance_and_audit.md`、`skills/shared/agents/process-auditor.md`、`skills/shared/agents/process-auditor.playbook.md`、`docs/pmo/issues/README.md`、`docs/governance/core-principles.md` | 插件治理能力 | PMO 主动检查机制已在 Phase 2.4 深化；仍需在插件入口层说明触发方式 |

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

1. `github-issue/SKILL.md` 与 `review-org/SKILL.md` 已纳入矩阵，但当前仓库仍缺更明确的插件落点。
2. 插件安装/装载说明已建立，但仍可继续收紧到更接近直接接入。
3. evaluation checker 已从评审维度说明推进到检查器类型与模板字段，但仍未形成更完整的独立子入口。

## Phase 1 收口结论

- `hedge-ai/prompts/V3.0` 顶层文档、`change_record/`、`.claude/skills` 顶层协议、`AGENTS/`、`AGENTS/evaluation/`、`WORKFLOWS/` 已完成逐组复核。
- 本阶段已经明确哪些内容属于插件主干，哪些只能部分迁移，哪些必须禁止迁移。
- 本阶段未做“补新机制”扩展，只做源覆盖、迁移判定、当前落点与插件落点的收口。
- 下一阶段进入 `Phase 2`，只围绕双阶段 PR、Issue First、Issue Comment Gate、PMO 合规检查和 README 流程图继续深化。
