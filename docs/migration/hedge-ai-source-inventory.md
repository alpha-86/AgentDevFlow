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
| `001_Agent团队架构.md` | 部分迁移 | 迁移团队协作框架，剥离量化角色语义 |
| `002_Agent工具设计.md` | 禁止迁移 | 量化数据/研究/回测工具接口专属 |
| `003_产品工程师Agent.md` | 可迁移 | 迁移 PM / Engineer 主链路、PRD 生命周期与 Gate 约束 |
| `004_工作流程规范.md` | 部分迁移 | 迁移流程阶段与治理方法，去交易时间切片 |
| `005_人机交互规范.md` | 部分迁移 | 迁移人机交互约束，去 Telegram / 交易命令语义 |
| `006_辩论机制与案例.md` | 部分迁移 | 迁移“对抗式评审方法”，去交易策略语境 |
| `007_策略研究指南.md` | 禁止迁移 | 量化策略研究专属 |
| `008_因子研究与因子库.md` | 禁止迁移 | 因子体系专属 |
| `009_回测报告设计.md` | 禁止迁移 | 回测范式与交易指标专属 |
| `010_日报迭代规范.md` | 部分迁移 | 仅迁移“进展/问题/复盘”的日报机制，去交易字段 |
| `011_文档规范.md` | 可迁移 | 迁移文档契约、命名规范、状态与变更等级 |
| `012_交付物Checklist.md` | 部分迁移 | 迁移交付检查思路，去交易上线口径 |
| `013_ai_driving_ai.md` | 可迁移 | 迁移多 agent 编排方法 |
| `014_回测报告模板.md` | 禁止迁移 | 回测报告专属 |
| `014_ClaudeSkills与Agent依赖.md` | 可迁移 | 迁移 agent 依赖治理方法 |
| `015_会议记录规范.md` | 可迁移 | 迁移会议纪要标准 |
| `016_Todo管理机制.md` | 可迁移 | 迁移 Todo 闭环机制 |
| `019_TeamLead职责边界.md` | 可迁移 | 迁移 Team Lead 边界、AI 驱动 AI 与 Agent 创建规范 |

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
| `github-issue/SKILL.md` | 可迁移 | 迁移 Issue skill 入口与调用约束 |
| `create-agent/SKILL.md` | 可迁移 | 迁移 agent 创建契约 |
| `start-agent-team/SKILL.md` | 可迁移 | 迁移团队启动流程 |
| `review-org/SKILL.md` | 可迁移 | 迁移组织评审机制 |

### B1. AGENTS

| 源文件 | 判定 | 迁移说明 |
|---|---|---|
| `team-lead.md` | 可迁移 | 通用管理边界可迁移 |
| `pm-agent.md` | 可迁移 | 通用 PM / 文档阶段 owner 可迁移 |
| `cto-agent.md` | 可迁移 | 通用技术评审 owner 可迁移 |
| `engineer-agent.md` | 可迁移 | 通用开发交付角色可迁移 |
| `qa-agent.md` | 可迁移 | 通用 QA Gate 与测试验收角色可迁移 |
| `pmo-agent.md` | 可迁移 | 流程合规主动检查机制可迁移 |
| `research-agent.md` | 部分迁移 | 仅保留通用研究流程 |
| `sre-agent.md` | 可迁移 | 运行保障机制可迁移 |
| `backtest-agent.md` | 禁止迁移 | 回测业务专属 |
| `bull-agent.md` | 禁止迁移 | 交易策略辩论专属 |
| `bear-agent.md` | 禁止迁移 | 交易策略辩论专属 |
| `risk-agent.md` | 部分迁移 | 仅迁移工程风险控制方法 |
| `cso.md` | 部分迁移 | 不作为插件主干角色，仅参考通用治理方法 |
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

- 当前仓库只保留中文单线版本，不再规划其他语言镜像。
- 先固化边界，再迁移机制，再补模板与 workflow。
- 任何出现量化交易语义的内容，一律退回重写。

## D. Phase 7 复核摘要

- 已复核根 `README.md`、插件入口、共享角色、共享 workflow。
- 当前未发现新的交易业务语义混入插件主干。
- 当前仓库中保留的交易相关词汇，均用于：
  - 源文档分类
  - 禁止迁移说明
  - 边界审计

详见：

- [与 hedge-ai 的迁移边界（强约束）](/home/work/code/AgentDevFlow/docs/governance/migration-boundary-from-hedge-ai.md)
