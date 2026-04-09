# hedge-ai 历史迁移映射

## 总体策略

本文仅用于记录历史迁移映射。

当前原则：

- AgentDevPipeline 是独立主仓库。
- 所有已迁移能力必须在本仓库内自维护。
- 不允许要求使用者回到 `hedge-ai` 查阅运行所需文档。

## 保留并抽象的资产

| hedge-ai 历史来源 | AgentDevPipeline 落点 | 处理方式 |
|---|---|---|
| `prompts/V3.0/003_产品工程师Agent.md` | `prompts/zh-cn/002_product_engineering_roles.md` | 抽象为 PM / Tech Lead / Engineer / QA |
| `prompts/V3.0/011_文档规范.md` | `prompts/zh-cn/003_document_contracts.md` | 保留目录、命名、评审、签审思想 |
| `prompts/V3.0/012_交付物Checklist.md` | `prompts/zh-cn/004_delivery_gates.md` | 保留 Gate 机制，移除量化收益指标 |
| `prompts/V3.0/015_会议记录规范.md` | `prompts/zh-cn/005_meeting_and_todo.md` | 保留会议留痕和归档要求 |
| `prompts/V3.0/016_Todo管理机制.md` | `prompts/zh-cn/005_meeting_and_todo.md` | 保留 Todo 生命周期 |
| `.claude/skills/create-agent/SKILL.md` | `adapters/claude/.claude/skills/create-agent/SKILL.md` | 改成中立角色类型 |
| `.claude/skills/start-agent-team/SKILL.md` | `adapters/claude/.claude/skills/start-agent-team/SKILL.md` | 改成通用团队启动 |
| `AGENTS/*.md` | `skills/shared/agents/*.md` | 仅保留产研角色 |
| `WORKFLOWS/prd-review.md` | `skills/shared/workflows/prd-review.md` | 保留 |
| `WORKFLOWS/tech-review.md` | `skills/shared/workflows/tech-review.md` | 保留 |
| `WORKFLOWS/todo-management.md` | `skills/shared/workflows/todo-review.md` | 合并精简 |

## 明确移除的资产

| hedge-ai 角色/流程 | 原因 |
|---|---|
| FM / CSO / CRO | 属于量化基金业务运营，不属于通用产研 |
| Bull / Bear / Risk 辩论角色 | 强绑定策略辩论场景 |
| Backtest Agent | 强绑定量化研究和回测能力 |
| 盘前盘后 DBR/WBR/MBR 时间切片 | 强绑定市场交易节奏 |
| 实盘信号、回测、风险日报 | 非通用研发流程 |

## 新的中立角色映射

| 原角色 | 新角色 |
|---|---|
| PM Agent | Product Manager |
| CTO Agent | Tech Lead |
| Engineer Agent | Engineer |
| QA Agent | QA Engineer |
| Team Lead | Team Lead |
| Research Agent | Product/Technical Researcher |
| SRE Agent | Platform/SRE |
