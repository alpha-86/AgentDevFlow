# hedge-ai 源文档清单与迁移判定（中文主版本）

## 说明

- 本清单用于记录已阅读的 `hedge-ai` 文档，并给出迁移判定。
- 判定分为三类：
  - `可迁移`：可抽象为通用产研流程机制
  - `部分迁移`：仅迁移机制，必须剥离量化交易语义
  - `禁止迁移`：交易业务专属内容，禁止进入本仓库

---

## A. prompts/V3.0

| 源文件 | 判定 | 迁移说明 |
|---|---|---|
| `README.md` | 可迁移 | 迁移“目录编排与阅读入口”方法，不迁移业务术语 |
| `CHANGELOG.md` | 可迁移 | 迁移“流程变更记录机制” |
| `001_团队架构与角色职责.md` | 部分迁移 | 迁移角色协作框架，剥离量化角色语义 |
| `002_项目流程与文档规范.md` | 可迁移 | 迁移文档契约与流程阶段定义 |
| `003_PRD模板_提示词.md` | 可迁移 | 迁移 PRD 结构与验收约束 |
| `004_TechSpec模板_提示词.md` | 可迁移 | 迁移技术方案模板与评审约束 |
| `005_QA验证与发布流程.md` | 可迁移 | 迁移 QA/Release Gate |
| `006_辩论机制与案例.md` | 部分迁移 | 迁移“对抗式评审方法”，去交易策略语境 |
| `007_策略研究指南.md` | 禁止迁移 | 量化策略研究专属 |
| `008_因子研究与因子库.md` | 禁止迁移 | 因子体系专属 |
| `009_数据与回测规范.md` | 禁止迁移 | 回测范式与交易指标专属 |
| `010_日报迭代规范.md` | 部分迁移 | 仅迁移“日报迭代机制”，去交易字段 |
| `011_系统异常与响应机制.md` | 部分迁移 | 迁移异常响应机制，去交易监控口径 |
| `012_组织评审与升级机制.md` | 可迁移 | 迁移跨角色升级与评审治理 |
| `013_ai_driving_ai.md` | 可迁移 | 迁移多 agent 编排方法 |
| `014_回测报告模板.md` | 禁止迁移 | 回测报告专属 |
| `014_ClaudeSkills与Agent依赖.md` | 可迁移 | 迁移 agent 依赖治理方法 |
| `015_会议记录规范.md` | 可迁移 | 迁移会议纪要标准 |
| `016_Todo管理机制.md` | 可迁移 | 迁移 Todo 闭环机制 |
| `019_TeamLead职责边界.md` | 可迁移 | 迁移 Team Lead 边界约束 |

### A1. change_record（版本变更记录）

| 源文件 | 判定 | 迁移说明 |
|---|---|---|
| `V1.0_PRD_Tech_代码一致性变更管理规范.md` | 可迁移 | 迁移一致性变更管理 |
| `V1.2_review_org_支持subagent及change_record.md` | 可迁移 | 迁移 review + 变更记录联动 |
| `V1.3_review_org_强化文档阅读与系统性方案要求.md` | 可迁移 | 迁移“先读全量文档再决策”硬约束 |
| `V2.0_研发流程与GitHubIssue结合及QA角色引入.md` | 可迁移 | 迁移 Issue 驱动与 QA 介入 |
| `V2.1_P0修复_QA_V2.0_review_critical_rules强化.md` | 可迁移 | 迁移关键规则强制化 |
| `V2.1_V2.0变更review及Agent_Critical_Rules验证.md` | 可迁移 | 迁移 critical rules 验证机制 |
| `V2.2_双PR机制引入.md` | 部分迁移 | 迁移“双分支/双阶段验收思想”，去交易流程绑定 |
| `V2.2.5_Issue_Comment机制修复与强制Gate建立.md` | 可迁移 | 迁移 Issue 评论门禁 |
| `V2.3_Gate_流程保障机制.md` | 可迁移 | 迁移 Gate 防绕过保障 |
| `V2.3_Tech_Gate签字定义统一.md` | 可迁移 | 迁移签字口径统一 |
| `V2.5_DBR例会调整为每日4次.md` | 禁止迁移 | 交易运营节奏专属 |
| `V2.6_PMO-Agent引入_流程合规主动检查机制.md` | 可迁移 | 迁移流程合规主动检查机制 |

---

## B. .claude/skills

| 源文件 | 判定 | 迁移说明 |
|---|---|---|
| `TEAM_SETUP.md` | 可迁移 | 迁移团队初始化步骤 |
| `SKILL_PROTOCOL.md` | 可迁移 | 迁移 skill 使用协议 |
| `EVENT_BUS.md` | 可迁移 | 迁移事件触发/订阅机制 |
| `ANOMALY_LOOP.md` | 部分迁移 | 迁移异常闭环机制，去交易告警语义 |
| `github-issue.md` | 可迁移 | 迁移 Issue 流程约束 |
| `create-agent/SKILL.md` | 可迁移 | 迁移 agent 创建契约 |
| `start-agent-team/SKILL.md` | 可迁移 | 迁移团队启动流程 |
| `review-org/SKILL.md` | 可迁移 | 迁移组织评审机制 |

### B1. AGENTS

| 源文件 | 判定 | 迁移说明 |
|---|---|---|
| `team-lead.md` | 可迁移 | 通用管理边界可迁移 |
| `research-agent.md` | 部分迁移 | 仅保留通用研究流程 |
| `sre-agent.md` | 可迁移 | 运行保障机制可迁移 |
| `backtest-agent.md` | 禁止迁移 | 回测业务专属 |
| `bull-agent.md` | 禁止迁移 | 交易策略辩论专属 |
| `bear-agent.md` | 禁止迁移 | 交易策略辩论专属 |
| `risk-agent.md` | 部分迁移 | 仅迁移工程风险控制方法 |
| `cso.md` | 部分迁移 | 仅迁移通用安全治理机制 |
| `cro.md` | 禁止迁移 | 交易风险角色专属 |

### B2. AGENTS/evaluation

| 源文件 | 判定 | 迁移说明 |
|---|---|---|
| `logic-checker.md` | 可迁移 | 逻辑审查机制 |
| `consistency-checker.md` | 可迁移 | 一致性审查机制 |
| `data-verifier.md` | 部分迁移 | 仅迁移“数据证据核验”机制 |
| `completeness-checker.md` | 可迁移 | 完整性审查机制 |

### B3. WORKFLOWS

| 源文件 | 判定 | 迁移说明 |
|---|---|---|
| `prd-review.md` | 可迁移 | 已纳入通用 PRD Gate |
| `tech-review.md` | 可迁移 | 已纳入通用 Tech Gate |
| `daily-standup.md` | 可迁移 | 已纳入研发日会机制 |
| `todo-management.md` | 可迁移 | 已纳入 Todo 闭环机制 |
| `weekly-review.md` | 可迁移 | 迁移周度复盘机制 |
| `monthly-review.md` | 可迁移 | 迁移月度改进机制 |
| `strategy-review.md` | 禁止迁移 | 策略业务专属 |
| `strategy-debate.md` | 禁止迁移 | 策略业务专属 |
| `factor-review.md` | 禁止迁移 | 因子业务专属 |
| `backtest-review.md` | 禁止迁移 | 回测业务专属 |
| `risk-report.md` | 部分迁移 | 仅迁移工程风险报告结构 |
| `daily-report.md` | 部分迁移 | 仅迁移通用进展日报结构 |
| `debate.md` | 部分迁移 | 迁移对抗式评审方法，不迁移交易内容 |
| `anomaly-iteration.md` | 部分迁移 | 迁移异常迭代机制，不迁移交易告警字段 |

---

## C. 本仓库落地原则（摘要）

- 中文主版本优先，英文只做后续镜像。
- 先固化边界，再迁移机制，再补模板与 workflow。
- 任何出现量化交易语义的内容，一律退回重写。

详见：

- [与 hedge-ai 的迁移边界（强约束）](/home/work/code/agentdevpipeline/docs/zh-cn/reference/migration-boundary-from-hedge-ai.md)
