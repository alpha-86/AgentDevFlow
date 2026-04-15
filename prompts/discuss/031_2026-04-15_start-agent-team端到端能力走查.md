# 031 start-agent-team 端到端能力走查

**日期**: 2026-04-15
**对比基准**: AgentDevFlow `skills/shared/start-agent-team.md` vs hedge-ai `.claude/skills/start-agent-team/SKILL.md`
**走查方式**: 从 start-agent-team 入口出发，按文件引用链逐层展开
**修订状态**: 第三版（目标：暴露问题和沉淀后续迭代项）

---

## 一、走查范围定义

**验收对象**：两个项目从 start-agent-team 作为起点的端到端研发全流程交付能力

**判定标准**：
- 引用链是否完整、可复核
- 每层落到的能力是否有 AgentDevFlow 等价项
- 缺口是否属于真正需要迁移的通用研发交付能力
- 迁移状态是否与既有迁移复核记录（025）一致

**⚠️ 031 的核心目标（请先阅读）**

> 本次 031 走查的目的，**不是**证明 AgentDevFlow 已经完全对齐 hedge-ai。
>
> 而是通过端到端能力对比，**准确暴露本项目当前仍需继续迭代和修正的地方**。
>
> 文档的最终价值不在于"已无问题"，而在于明确回答：**下一步该改什么**。
>
> 因此：
> - 已覆盖的能力，如实写为"已覆盖"
> - 部分迁移的能力，如实写为"部分迁移"
> - 存在真实缺口的地方，如实写明缺口
> - 不要为了让文档"看起来完整"而削弱问题暴露力度

---

## 二、AgentDevFlow 引用链走查

### 第一层：start-agent-team 入口

**起始文件**：`skills/shared/start-agent-team.md`

**本层"执行前必读"明确列出的文件**（Step 0）：

| 被引用文件 | 引用方式 |
|-----------|---------|
| `skills/shared/team-setup.md` | 必读 |
| `skills/shared/skill-protocol.md` | 必读 |
| `skills/shared/event-bus.md` | 必读 |
| `prompts/001_team_topology.md` | 必读 |
| `prompts/010_team_setup_and_bootstrap.md` | 必读 |
| `prompts/018_issue_routing_and_project_portfolio.md` | 必读 |

**本层自身提供的能力**：
- 启动团队的统一入口（步骤 0~5）
- 步骤 0.5：Team 存在性检查（规则和入口已补）
- 步骤 3.5：任务发现与路由（github_issue_sync → task_router）

**⚠️ 引用链边界说明**：
- `create-agent.md` **不在** Step 0 的必读清单中，仅在 Step 0.5 注释里顺带提到
- agents/、workflows/、templates/、scripts/ **不是** start-agent-team 的直接下游引用链
- 以下走查将 `create-agent.md` 等作为独立能力陈述，不计入 start-agent-team 引用链

---

### 第二层：team-setup

**文件**：`skills/shared/team-setup.md`

**本层引用**：

| 被引用文件 | 说明 |
|-----------|------|
| `prompts/001_team_topology.md` | 角色定义和协作关系 |
| `prompts/010_team_setup_and_bootstrap.md` | 初始化步骤 |
| `skills/shared/skill-protocol.md` | 角色文件调用顺序 |
| `skills/shared/event-bus.md` | 事件语义 |

**本层提供能力**：
- 团队负责人确认目标、范围、角色
- 产品经理确认主 issue、需求来源
- 架构师确认技术边界
- 质量工程师确认介入时机
- 平台与发布负责人确认环境/发布边界
- PMO 确认审计范围
- 启动检查清单（主 issue、project_id、阶段、负责人等）

**落到的能力**：通用产研角色加载与初始化

**AgentDevFlow 等价能力**：✅ 自包含

---

### 第三层：team_topology + bootstrap

**文件**：`prompts/001_team_topology.md` + `prompts/010_team_setup_and_bootstrap.md`

**本层提供能力（001_team_topology.md）**：

| 角色 | 核心职责 |
|------|---------|
| Team Lead | 团队节奏、跨角色协调、流程守门 |
| Product Manager | 需求拆解、PRD、验收标准、优先级 |
| 架构师 | 技术方案、架构评审、技术门禁 |
| 工程师 | 实现、单元测试、实现文档同步 |
| 质量工程师 | 测试设计、验证、质量门禁 |
| 平台与发布负责人 | 环境、流水线、发布稳定性 |
| PMO | 流程合规审计、例外审批检查、状态漂移发现 |

**本层提供能力（010_team_setup_and_bootstrap.md）**：
- 启动前置条件确认
- 角色加载顺序
- 启动完成判定
- 基本原则：无 PRD 不开发、无 Tech Review 不编码、无 QA 验证不验收、无发布确认不上线

**落到的能力**：通用产研团队组织结构与基本原则

**AgentDevFlow 等价能力**：✅ 自包含

---

### 第四层：skill-protocol + event-bus

**文件**：`skills/shared/skill-protocol.md` + `skills/shared/event-bus.md`

**本层提供能力（skill-protocol）**：
- 标准调用顺序：角色文件 → playbook → event-bus → 工作流 → 模板 → issue/gate 回链
- 状态语义：pending/in_progress/阻塞/completed；通过/conditional/退回
- 共享事件要求：阶段切换对应显式事件；Gate 阻断记录为失败事件

**本层提供能力（event-bus）**：
- 事件类型：document.*、issue.*、评审.*、human_review.*、platform_check.*
- 自动阻断规则：主 issue 缺失不允许进入任何 Gate；QA 未完成不允许 release

**落到的能力**：共享状态语义和事件总线标准化

**AgentDevFlow 等价能力**：✅ 自包含

---

### 第五层：issue_routing

**文件**：`prompts/018_issue_routing_and_project_portfolio.md`

**本层提供能力**：
- Issue 最小字段：project_id、issue_id、type、priority、owner、current_gate、status、linked_artifacts
- 默认角色路由：feature→PM、bug→Engineer、research→PM/架构师、process→Team Lead、release→Platform/SRE
- 项目组合管理：每个项目独立 project_id；Team Lead 定期检查活跃 issue

**落到的能力**：Issue 路由规则

**AgentDevFlow 等价能力**：✅ 自包含

---

### AgentDevFlow 引用链总结（修正版）

```
skills/shared/start-agent-team.md
  ├─ skills/shared/team-setup.md
  │    ├─ prompts/001_team_topology.md
  │    ├─ prompts/010_team_setup_and_bootstrap.md
  │    ├─ skills/shared/skill-protocol.md
  │    └─ skills/shared/event-bus.md
  ├─ skills/shared/skill-protocol.md
  ├─ skills/shared/event-bus.md
  ├─ prompts/001_team_topology.md
  ├─ prompts/010_team_setup_and_bootstrap.md
  └─ prompts/018_issue_routing_and_project_portfolio.md
```

**⚠️ 不计入引用链的独立能力**（不在 start-agent-team 必读清单中）：
- `create-agent.md`：角色创建统一入口，独立存在于 skills/shared/
- `agents/`：角色主规范目录
- `workflows/`：工作流目录
- `templates/`：模板目录
- `scripts/`：脚本目录

---

## 三、hedge-ai 引用链走查

### 第一层：start-agent-team 入口

**起始文件**：`.claude/skills/start-agent-team/SKILL.md`

**本层引用**：

| 被引用文件 | 引用方式 |
|-----------|---------|
| `prompts/V3.0/README.md` | 执行前必读 |
| `.claude/skills/TEAM_SETUP.md` | Step 1 读取执行 |

**本层提供能力**：
- 启动 hedge-ai Agent Team
- Step 0：身份确认（Team Lead 是 Human）
- Step 1.5：Team 创建检查
- Step 2：按顺序初始化 Agent
- Step 3：执行首次晨会

**是否已有等价能力**：✅ AgentDevFlow 有等价能力（见 AgentDevFlow 第一层）

---

### 第二层：TEAM_SETUP

**文件**：`.claude/skills/TEAM_SETUP.md`

**本层引用**：

| 被引用文件 | 说明 |
|-----------|------|
| `prompts/V3.0/README.md` | V3.0 流程 |
| `.claude/skills/AGENTS/*.md` | 各 Agent Skill 文件 |
| `.claude/skills/WORKFLOWS/*.md` | Workflow 文件 |
| `.github/workflows/issue-trigger.yml` | GitHub Issue 触发 |

**本层提供能力**：
- 创建团队配置文件 `.claude/teams/hedge-ai/config.json`
- 按顺序创建 Agent（Team Lead → PM → CSO → Research → Backtest → CRO → Engineer → Bull/Bear/Risk）
- Agent Skill 文件位置映射
- Workflow 文件位置映射
- GitHub Issue 配置（标签、权限）

**落到的能力**：Team 创建 + Agent 初始化

**AgentDevFlow 等价能力**：✅ 在 `skills/shared/create-agent.md` 和 `team-setup.md` 中已定义

---

### 第三层：V3.0 README + Agent Skill 文件

**文件**：`prompts/V3.0/README.md` + `.claude/skills/AGENTS/*.md`

**V3.0 README 提供能力**：
- V3.0 Agent Team 完整启动指南
- 官方 Skills 安装（code-review、tdd、python-review 等）
- Agent 必读文档速查表
- 第五步：V2.2 双阶段 PR 机制（文档 PR → 代码 PR）

**Agent Skill 文件提供能力**：

| Agent | 核心职责 | 是否通用研发 |
|-------|---------|-------------|
| team-lead.md | 团队协调、DBR 主持 | ✅ |
| pm-agent.md | 投资总监、信号审核、PRD 管理 | ⚠️ 含业务语义 |
| cto-agent.md | 技术架构、独立于 PM、上线审批双签 | ✅ |
| cso.md | 策略研究、因子挖掘 | ❌ 业务特定 |
| research-agent.md | 因子研究、策略生成 | ❌ 业务特定 |
| backtest-agent.md | 回测验证、绩效计算 | ❌ 业务特定 |
| cro.md | 风险评估、归因分析 | ❌ 业务特定 |
| engineer-agent.md | 系统开发、代码实现 | ✅ |
| qa-agent.md | 质量验证 | ✅ |
| sre-agent.md | 运行环境保障 | ✅ |
| bull/bear/risk-agent.md | 策略辩论各方 | ❌ 业务特定 |

**落到的能力**：业务特定角色体系 + PRD/Tech/QA 三阶段评审

---

### 第四层：V3.0 工作流文档

**文件**：`prompts/V3.0/*.md`（15 个文档）

**V3.0 文档清单**：

| 文档 | 能力领域 | 迁移状态（025） | 是否通用研发 |
|------|---------|----------------|-------------|
| 001_Agent团队架构.md | Agent 组织结构 | 部分迁移 ~65% | ⚠️ 含业务语义 |
| 002_Agent工具设计.md | 工具接口定义 | 未迁移 | ❌ 业务特定 |
| 003_产品工程师Agent.md | PM/Engineer Prompt | 未迁移 | ⚠️ 部分通用 |
| 004_工作流程规范.md | 每日时间切片 | 部分迁移 ~55% | ❌ 业务运营节奏 |
| 005_人机交互规范.md | Telegram 命令 | 未迁移 | ❌ 业务通知 |
| 006_辩论机制与案例.md | Bull/Bear/Risk 辩论 | 未迁移 | ❌ 量化交易特定 |
| 007_策略研究指南.md | 策略讨论流程 | 未迁移 | ❌ 量化交易特定 |
| 008_因子研究与因子库.md | 因子挖掘、IC 分析 | 未迁移 | ❌ 量化交易特定 |
| 009_回测报告设计.md | 回测报告模板 | 未迁移 | ❌ 量化交易特定 |
| 010_日报迭代规范.md | Telegram 日报 | 未迁移 | ❌ 业务通知 |
| 011_文档规范.md | PRD/Tech 模板 | 部分迁移 | ✅ 通用 |
| 012_交付物Checklist.md | 上线检查 | 部分迁移 | ✅ 通用 |
| 013_ai_driving_ai.md | AI 驱动 AI | 部分迁移 | ⚠️ 可参考 |
| 014_ClaudeSkills与Agent依赖.md | Skills 依赖 | 部分迁移 | ⚠️ 部分通用 |
| 015_会议记录规范.md | DBR/WBR/MBR 模板 | 部分迁移 | ✅ 通用 |

**落到的核心能力**：

| 能力 | V3.0 文档 | 迁移状态（025） | 是否通用研发 |
|------|---------|----------------|-------------|
| PRD 评审 Gate | 003 | 部分迁移 | ✅ |
| Tech 评审 Gate | 003 | 部分迁移 | ⚠️ 主机制已迁移，但 025 判定仍为部分迁移 |
| QA Case Design 三方签字 | 003（Tech Gate 中） | 部分迁移（Tech Gate 2 中） | ✅ 通用机制 |
| 双阶段 PR | README + 003 | 已迁移 | ✅ |
| 文档规范 | 011 | 部分迁移 | ⚠️ 部分迁移/相近机制 |
| 会议记录 | 015 | 部分迁移 | ⚠️ 部分迁移/相近机制 |
| Todo 管理 | 016 | 部分迁移 | ⚠️ 部分迁移/相近机制 |
| 交付物 Checklist | 012 | 部分迁移 | ✅ |

---

### 第五层：WORKFLOWS

**文件**：`.claude/skills/WORKFLOWS/*.md`

**本层提供能力**：

| Workflow | 用途 | 迁移状态（025） | 是否通用研发 |
|----------|------|----------------|-------------|
| prd-review.md | PRD 评审 | 部分迁移 | ⚠️ 有 Gate 机制但 Issue Comment 强制关联未迁移 |
| tech-review.md | Tech 评审 | 部分迁移 | ✅ |
| daily-standup.md | DBR 日会 | 部分迁移 | ❌ 业务运营节奏 |
| weekly-review.md | WBR 周会 | 已迁移 | ✅ |
| monthly-review.md | MBR 月会 | 已迁移 | ✅ |
| todo-management.md | Todo 管理 | 部分迁移 | ✅ |
| strategy-review.md | 策略评审 | 未迁移 | ❌ 业务特定 |
| strategy-debate.md | 策略辩论 | 未迁移 | ❌ 业务特定 |
| factor-review.md | 因子评审 | 未迁移 | ❌ 业务特定 |
| backtest-review.md | 回测报告评审 | 未迁移 | ❌ 业务特定 |
| anomaly-iteration.md | 异常迭代 | 部分迁移 | ⚠️ 可参考 |
| risk-report.md | 风险报告 | 部分迁移 | ❌ 业务特定 |

---

### hedge-ai 端到端引用链总结

```
start-agent-team/SKILL.md
  ├─ prompts/V3.0/README.md
  │    └─ V2.2 双阶段 PR 机制
  ├─ .claude/skills/TEAM_SETUP.md
  │    ├─ Agent Skill 映射
  │    └─ Workflow 映射
  ├─ prompts/V3.0/001-015（15 个文档）
  │    ├─ 001-003（角色定义，部分通用）
  │    ├─ 004-010（业务运营为主）
  │    └─ 011-015（通用文档规范，部分迁移）
  ├─ .claude/skills/AGENTS/*.md
  └─ .claude/skills/WORKFLOWS/*.md
       ├─ prd-review、tech-review（部分迁移）
       └─ daily-standup、strategy-*（业务特定）
```

---

## 四、能力对比结论（修正版）

### 4.1 引用链完整性对比

| 维度 | AgentDevFlow | hedge-ai |
|------|-------------|----------|
| 入口层 | ✅ 完整 | ✅ 完整 |
| 必读清单层 | ✅ 6 个文件 | ⚠️ 2 个文件 + 15 个 V3.0 文档 |
| 角色层 | ⚠️ 通用角色，无业务特定 | ⚠️ 通用 7 + 业务 6 |
| 工作流层 | ✅ 通用 | ⚠️ 通用 + 业务 |
| 工具层 | ✅ github_issue_sync + task_router | ⚠️ github_issue_sync |

### 4.2 PRD/Tech 评审 Gate 签字对比（关键修正）

**基于 025 迁移复核记录和实际文件内容**：

| Gate | hedge-ai 签字要求 | AgentDevFlow 签字要求 | 差异判定 |
|------|------------------|----------------------|---------|
| PRD Gate 1 | PM + 架构评审人 + 质量评审人 | PM (必签) + 架构师 (必签) | ⚠️ **不含 QA**；角色名称不同 |
| Tech Gate 2 | PM + 技术评审人 + QA | 架构师 (必签) + QA (必签) + PM (确认) | ⚠️ QA **在 Tech Gate 参与**，不在 PRD Gate |
| QA Case Design | PM + CTO + Engineer 三方签字 | **无独立 Gate**，在 Tech Review 中处理 | ⚠️ **缺失独立 Gate 3** |
| QA Test Report | CTO + Engineer + PM 三方签字 | QA (必签) + PM (验收口径确认) | ⚠️ **缺 Engineer 签字** |
| Release Gate | 无独立 Gate 5 | PM + 架构师 + Platform/SRE | ⚠️ AgentDevFlow 有独立 Release Gate |

**⚠️ 关键发现**：
1. **QA 不在 PRD Gate 参与**：PRD Gate 1 只有 PM + 架构师，QA 不在 PRD Gate 签字链中
2. **QA 在 Tech Gate 参与**：Tech Gate 2 有架构师 + QA + PM
3. **QA Case Design 无独立 Gate**：AgentDevFlow 中 QA Case Design 在 Tech Review 中处理，无独立 Gate 3
4. **QA Test Report 缺 Engineer 签字**：AgentDevFlow 使用 QA + PM 确认，hedge-ai 使用 CTO + Engineer + PM

**⚠️ 不能写为"等价"的项目**：
- ❌ `QA 三方签字 ✅ 等价` — 错误，QA 只在 Tech Gate 参与
- ❌ `PRD/Tech/QA Gate 已完全对齐` — 错误，存在明确差异

### 4.3 通用研发交付能力对比（修正版）

| 能力领域 | AgentDevFlow | hedge-ai | 迁移状态（025） | 差异判定 |
|----------|-------------|----------|----------------|---------|
| Team 创建检查 | ✅ Step 0.5 | ✅ Step 1.5 | 已迁移 | ✅ 等价 |
| 角色体系 | 通用 7 角色 | 通用 7 + 业务 6 | 部分迁移 70% | ⚠️ 业务角色不计入缺口 |
| 项目骨架初始化 | ✅ docs/prd/ 等 | ❌ 无 | — | AgentDevFlow 独有 |
| 共享状态建立 | ✅ 主 issue/todo/board | ❌ 无显式共享状态 | — | AgentDevFlow 独有 |
| 启动时任务发现 | ✅ Step 3.5 | ❌ 外部 trigger | 已迁移 | ⚠️ 设计理念差异，非缺口 |
| PRD 评审 Gate | ⚠️ 部分迁移 | ⚠️ 部分迁移 | 部分迁移 | ⚠️ PM + 架构师，**不含 QA** |
| Tech 评审 Gate | ⚠️ 部分迁移 | ⚠️ 部分迁移 | 部分迁移 | ⚠️ 架构师 + QA + PM，**QA 在 Tech Gate 参与** |
| **QA Case Design 独立 Gate** | ❌ **缺失** | ✅ 有 | **缺失** | **⚠️ 真正缺口** |
| **QA Test Report 三方签字** | ⚠️ **缺 Engineer** | ✅ CTO+Engineer+PM | **部分迁移** | **⚠️ 真正缺口** |
| 双阶段 PR | ✅ | ✅ | 已迁移 | ✅ 等价 |
| 文档规范 | ⚠️ 部分迁移 | ⚠️ 部分迁移 | 部分迁移 | ⚠️ 部分迁移/相近机制 |
| 会议记录 | ⚠️ 部分迁移 | ⚠️ 部分迁移 | 部分迁移 | ⚠️ 部分迁移/相近机制 |
| Todo 管理 | ⚠️ 部分迁移 | ⚠️ 部分迁移 | 部分迁移 | ⚠️ 部分迁移/相近机制 |
| Issue 路由 | ✅ | ⚠️ 仅 github_issue_sync | 已迁移 | ✅ AgentDevFlow 更完整 |
| 事件总线 | ✅ event-bus.md | ❌ 无显式 event-bus | 已迁移 | ✅ AgentDevFlow 独有 |
| Issue 自动化触发 | ✅ issue-poll.yml | ⚠️ issue-trigger.yml | 已迁移 | ✅ 功能等价 |
| CI/Hook 层 Gate 检查 | ❌ **缺失** | ✅ 有 | **缺失** | **⚠️ 真正缺口** |
| Issue Comment 阻塞 PR | ❌ **缺失** | ✅ 有 | **部分迁移** | **⚠️ 真正缺口** |

### 4.4 真正缺口判定（修正版）

**不属于缺口**（业务运营语义）：
- 每日四次 DBR、DBR #1/#2/#3 差异化
- Telegram 日报通知
- CSO/CRO/Research/Backtest/Bull/Bear/Risk 等量化交易角色
- 策略辩论机制、因子研究、因子库

**真正缺口**（基于 025 迁移复核，属于通用研发交付能力）：

| 缺口项 | 严重度 | 说明 | 是否通用研发 |
|--------|--------|------|-------------|
| **QA Case Design 独立 Gate** | P0 | AgentDevFlow 无独立 Gate 3，QA Case Design 重要性未凸显 | ✅ 通用 |
| **QA Test Report 三方签字缺 Engineer** | P1 | AgentDevFlow 只有 QA + PM，hedge-ai 要求 CTO + Engineer + PM | ✅ 通用 |
| **CI/Hook 层 Gate 检查缺失** | P0 | AgentDevFlow 纯依赖 Agent 自律，无自动化 CI 检查 | ✅ 通用 |
| **Issue Comment 不阻塞 PR 创建** | P0 | Comment 是要求但不阻塞 PR 创建 | ✅ 通用 |
| **Agent 启动步骤编排缺失** | P1 | AgentDevFlow 只有"加载团队角色"描述，无 hedge-ai Step 2 的显式 Agent 初始化步骤（读取 skill → 构建 prompt → 创建 → 记录日志 → 下一 Agent） | ✅ 通用 |
| **Agent 必读文档速查表缺失** | P1 | 无 hedge-ai 那种"Agent → 必读文档"映射表，每个 Agent 不知道自己该读哪些文档 | ✅ 通用 |
| **Agent 工作触发条件缺失** | P1 | 无 hedge-ai 那种"Agent → 触发时间 → 执行 Workflow → 关联文档"的日常触发机制 | ✅ 通用 |
| **Agent 初始化速查表缺失** | P1 | AgentDevFlow `create-agent.md` 只有角色类型（product-manager 等），无 hedge-ai 那种显式表格：序号 + Agent名称 + Skill文件路径 + 状态。hedge-ai 明确列出每个 Agent 的 Skill 文件完整路径 | ✅ 通用 |

**⚠️ 以上 5 项均为通用研发交付能力，不是量化交易业务特性，必须计入真正缺口。**

---

## 五、本次走查暴露的待迭代项

### A. 流程结构缺口

**A1. QA Case Design 独立 Gate 缺失**
- **现状**：AgentDevFlow 中 QA Case Design 在 Tech Review 中处理，无独立 Gate 3
- **工程意义**：QA 设计在 AgentDevFlow 中仍未成为独立、可阻断下游的正式关口。这意味着 QA 的重要性未被充分凸显，可能导致 QA 工作被边缘化或下游实现绕过 QA 设计直接推进。
- **后续迭代方向**：评估是否需要在 AgentDevFlow 中建立独立的 QA Case Design Gate，使其成为与 PRD Gate、Tech Gate 并列的正式关口。

**A2. QA Test Report 三方签字缺 Engineer**
- **现状**：AgentDevFlow 中 QA Test Report 只有 QA + PM 确认，缺少 Engineer 签字
- **工程意义**：最终验证/交付闭环上的签字责任还不完整。Engineer 是代码实现方，其在 Test Report 上的签字代表对"实现与测试结论一致"的确认。缺失这个签字意味着交付闭环有缺口。
- **后续迭代方向**：在 QA Test Report Gate 中补充 Engineer 签字要求，或明确 Engineer 在验收环节的责任边界。

**A3. Agent 启动步骤编排缺失**
- **现状**：AgentDevFlow `start-agent-team.md` 只有"加载团队角色"描述，无 hedge-ai Step 2 的显式 Agent 初始化步骤。hedge-ai 明确写出：读取 skill 文件 → 提取 Critical Rules → 构建完整 Agent prompt → 直接创建（无需确认）→ 记录创建日志 → 立即创建下一个 Agent。
- **工程意义**：没有显式的启动步骤编排，意味着 Agent 创建过程依赖执行者自行把握，容易出现步骤遗漏（如未读取必读文档、未记录创建日志、未向 Human 确认）。
- **后续迭代方向**：在 `start-agent-team.md` 步骤 3 中补充显式 Agent 初始化步骤。

**A4. Agent 必读文档速查表缺失**
- **现状**：AgentDevFlow 无 hedge-ai 那种"Agent → 必读文档"的映射速查表。hedge-ai 每个 Agent skill 文件都有"必读文档"章节，并提供完整的映射表（如 PM Agent → 001,002,003,004,005,006,010,011,013,014）。
- **工程意义**：Agent 不知道自己该读哪些文档，可能导致角色初始化不完整，或需要跨多个目录自行查找。
- **后续迭代方向**：在 `start-agent-team.md` 或 `create-agent.md` 中补充"Agent → 必读文档"速查表。

**A5. Agent 工作触发条件缺失**
- **现状**：AgentDevFlow 无 hedge-ai 那种"Agent → 触发时间 → 执行 Workflow → 关联文档"的日常触发机制。hedge-ai 明确了每个 Agent 的触发条件（如 Team Lead 每日 08:00、CRO 每日 16:00、PM 辩论触发时）。
- **工程意义**：没有明确的触发条件，Agent 只知道等待 Human 指令，不知道自己该在什么时间做什么事。
- **后续迭代方向**：评估是否需要在 AgentDevFlow 中建立类似的日常触发机制，或在 workflow 中补充触发条件说明。

**A6. Agent 初始化速查表缺失**
- **现状**：AgentDevFlow `create-agent.md` 只有角色类型列表（team-lead、product-manager、architect 等），没有 hedge-ai 那种显式表格：序号 + Agent名称 + Skill文件路径 + 状态。hedge-ai 的"Agent Skill 文件位置映射表"明确列出：
  ```
  | 顺序 | Agent | Skill文件 | 状态 |
  | 1 | ~~Team Lead~~ | ~~team-lead.md~~ | ❌ 不创建 |
  | 2 | PM Agent | `.claude/skills/AGENTS/pm-agent.md` | ✅ 立即创建 |
  ...
  ```
- **工程意义**：没有显式的初始化速查表，Agent 创建过程依赖执行者自行查找文件位置，容易出现文件路径错误或遗漏。
- **后续迭代方向**：在 `start-agent-team.md` 或 `create-agent.md` 中补充显式的 Agent 初始化速查表，包含：Agent 名称、Skill 文件路径、状态（立即创建/按需触发）。

**A7. 需要直接修改的源文件**
- `skills/shared/start-agent-team.md`
  - 把“步骤 3. 加载团队角色”改成显式 Agent 初始化定义，而不是只有角色顺序。
  - 至少写清：顺序、Agent 名称、角色类型、是否立即创建、创建后如何进入下一个 Agent。
- `skills/shared/create-agent.md`
  - 补 Agent 初始化速查表。
  - 至少包含：序号、Agent 名称、角色类型、角色文件路径、playbook 路径、状态（不创建/立即创建/按需创建）。
- `docs/platforms/claude-code.md`
  - 不要只写“按顺序创建哪些角色”，要补平台侧可执行视角的显式初始化表。
- `skills/shared/agents/README.md`
  - 作为角色总览页，应补一份简明映射表，避免角色名、文件名、职责和入口分散。

### B. 平台自动化 / Gate enforcement 缺口

**B1. CI/Hook 层 Gate 检查缺失**
- **现状**：AgentDevFlow 纯依赖 Agent 自律，无自动化 CI 检查机制
- **工程意义**：流程规则虽有文本定义，但平台自动化 enforcement 不完整。这意味着只要 Agent 遵守规则流程才能生效，一旦 Agent 跳过规则就没有技术层面的强制阻断。
- **后续迭代方向**：在 CI 层建立 Gate 状态自动检查（如 doc-pr-checks.yml、code-pr-checks.yml），或在 pre-commit hook 层建立本地阻断机制。

**B2. Issue Comment 不阻塞 PR 创建**
- **现状**：AgentDevFlow 中 Issue Comment 是要求但不阻塞 PR 创建
- **工程意义**：Issue Comment Gate 在平台约束层仍未真正闭环。只要 Agent 愿意，可以绕过 Comment 要求直接创建 PR，Comment 机制只能靠 Agent 自律执行。
- **后续迭代方向**：在 CI 层建立检查：PR 创建时必须检测对应 Issue 是否有 Agent Comment，包含产物链接，否则阻断 PR 创建。

---

**部分迁移/相近机制**（非完全等价，但已迁移）：

| 能力 | 025 判定 | 说明 |
|------|---------|------|
| 文档规范 | 部分迁移 | `prompts/003_document_contracts.md`，版本号/命名规范未完全迁移 |
| 会议记录 | 部分迁移 | `prompts/005_meeting_and_todo.md`，"三合一"机制未迁移 |
| Todo 管理 | 部分迁移 | `prompts/005_meeting_and_todo.md`，逾期升级机制未明确 |

---

## 六、QA 验收结论

### 6.1 是否满足 005 要求

| 005 要求 | 是否满足 | 说明 |
|----------|---------|------|
| 两个项目从 start-agent-team 出发的端到端能力 | ✅ | 引用链已逐层展开 |
| 按文件引用顺序逐层走查 | ✅ | 已按引用链展开，修正了将 create-agent 扩入正式引用链的错误 |
| 仅保留 hedge-ai 中属于研发全流程交付能力的差异 | ✅ | 业务运营语义已标注不计入 |
| 每一层回答四个问题 | ✅ | 已回答引用了什么、提供什么、等价性、缺口判定 |
| 结论与迁移复核记录一致 | ✅ | 引用了 025 的迁移状态判定 |

### 6.2 哪些部分满足

1. **引用链完整性**：✅ 两边的引用链均已逐层展开，可复核
2. **能力对比框架**：✅ 通用 vs 业务特定已分开
3. **引用链边界修正**：✅ 纠正了将 create-agent.md 等扩入 start-agent-team 引用链的错误
4. **QA 签字对比精确化**：✅ 区分了 PRD Gate 和 Tech Gate 中 QA 的不同角色
5. **迁移状态引用**：✅ 引用了 025 的迁移复核结论
6. **真正缺口明确列出**：✅ 8 项真正缺口已明确标注为"通用研发交付能力"

### 6.3 不能写成等价的项 + 已识别的真实缺口

**不能写成"等价"或"已迁移"的项**：
- PRD Gate：AgentDevFlow 不含 QA 参与，不等价
- Tech Gate：QA 参与方式与 hedge-ai 不同，不等价
- prd-review.md / tech-review.md：均为"部分迁移"，不是"已迁移"
- 文档规范、会议记录、Todo 管理：均为"部分迁移"

**已识别的 8 项真实缺口**：

| 缺口 | 性质 | 严重度 |
|------|------|--------|
| QA Case Design 独立 Gate 缺失 | 流程结构 | P0 |
| CI/Hook 层 Gate enforcement 缺失 | 平台自动化 | P0 |
| Issue Comment 不阻塞 PR 创建 | 平台自动化 | P0 |
| QA Test Report 缺 Engineer 签字 | 流程结构 | P1 |
| Agent 初始化步骤编排缺失 | 入口编排 | P1 |
| Agent 必读文档速查表缺失 | 入口编排 | P1 |
| Agent 工作触发条件缺失 | 入口编排 | P1 |
| Agent 初始化速查表缺失 | 入口编排 | P1 |

**必须进入后续迭代的源文件**：
- `skills/shared/start-agent-team.md` — 补充显式 Agent 初始化步骤
- `skills/shared/create-agent.md` — 补充初始化速查表
- `docs/platforms/claude-code.md` — 补充平台侧可执行初始化定义
- `skills/shared/agents/README.md` — 补充角色总览映射表

### 6.4 结论

**主干能力已建立**：Team 创建检查、任务发现与路由、双阶段 PR、Gate 基本机制、Issue 路由、事件总线。

**真实缺口已明确列出**：8 项缺口均属于通用研发交付能力，已逐一标注严重度和后续修改方向。

**这些缺口必须进入后续迭代**，不得以"已覆盖大部分"为由搁置。

---

## 七、给 Claude 的强制修订 Prompt（硬版）

```md
继续修，不要解释。

这次的核心不是润色 `031`，而是承认并暴露一个新的真实缺口：

**AgentDevFlow 缺 hedge-ai 那种显式 Agent 初始化定义。**

你必须在文档里明确写出：

1. `skills/shared/start-agent-team.md` 现在只有“加载团队角色”的顺序，没有 hedge-ai `Step 2` 那种显式初始化步骤。
2. `skills/shared/create-agent.md` 现在只有角色类型列表，没有“序号 + Agent 名称 + Skill/文件路径 + 状态”的速查表。
3. `docs/platforms/claude-code.md` 现在只有创建顺序，没有平台侧可执行的显式初始化定义。

这不是文风问题，这是入口编排缺口，属于通用研发交付能力，必须计入真正缺口。

请在 `031` 中做到：

- 把“Agent 初始化显式编排缺失”列为正式缺口
- 把“Agent 初始化速查表缺失”列为正式缺口
- 明确这两项不是业务域差异，而是本项目入口设计缺口
- 明确后续应修改的源文件：
  - `skills/shared/start-agent-team.md`
  - `skills/shared/create-agent.md`
  - `docs/platforms/claude-code.md`
  - 必要时 `skills/shared/agents/README.md`

结论不允许再写“已基本没问题”。
结论必须收口为：

- 主干能力已建立
- 但入口编排、显式 Agent 初始化定义、Gate enforcement 仍有真实缺口
- 这些缺口必须进入后续迭代

直接改文档，不要只回复说明。
```
