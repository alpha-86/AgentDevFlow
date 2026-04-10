# AgentDevPipeline

AgentDevPipeline 的核心目标，是把 `hedge-ai` 中可迁移的研发工作机制拆出来，沉淀成一个独立的研发流程插件包。它不是量化交易项目，也不应该继续携带 hedge-ai 的业务语义；它应该只保留可复用的研发编排机制。

这个仓库当前最重要的产物，不是单篇 prompt，也不是零散流程文档，而是一个中文单线的插件资产集合：

- 根 `README.md` 负责告诉用户插件解决什么问题、主线机制是什么
- `plugins/agentdevpipeline/` 负责承载插件入口
- `skills/shared/` 负责承载可复用的角色、workflow、template
- `prompts/` 负责承载中文规则层
- `docs/` 负责承载中文说明、迁移矩阵和治理边界

## 这个项目解决什么问题

很多团队已经能用 Agent 写代码、查资料、做评审，但真正卡住交付的往往不是“单点能力”，而是流程失控：

- 需求、方案、代码、测试之间断链
- 评审靠聊天推进，没有正式 Gate
- 任务有人做，但没人维护状态、风险和升级路径
- 会话一断、Agent 一换，整个上下文就丢了
- 同一套流程在 Claude、Codex、OpenCode 上重复造轮子

AgentDevPipeline 要解决的，是这些跨角色、跨阶段、跨工具的编排问题。

## 它如何解决

当前仓库主要在做三件事：

- 从 `hedge-ai/prompts/V3.0` 和 `.claude/skills` 逐文档拆出可迁移的研发机制
- 把这些机制重组为独立的角色、workflow、template 和治理规则
- 让这些资产能被 `plugins/agentdevpipeline/` 作为独立插件承载

不是所有“看起来合理”的流程概念都应该进入这个仓库。只有能从 hedge-ai 源文档中明确拆出来、且去掉业务语义后仍成立的机制，才应该保留。

## 这个仓库最终交付什么

对用户来说，这个仓库最终应该交付的是一个可装载、可阅读、可继续迭代的插件包，而不是一堆散落文档。

当前应按下面这条链理解它：

1. 根 `README.md`
   说明插件定位、问题、方法、主流程和阅读入口。

2. `plugins/agentdevpipeline/`
   说明插件自身入口、插件资产组成、插件如何装载共享资产。

3. `skills/shared/`
   提供真正可复用的角色定义、workflow、template 和共享协议。

4. `prompts/`
   提供中文规则层，约束角色、Gate、Issue、双阶段 PR、Comment Gate、PMO 主动检查等机制。

5. `docs/migration/hedge-ai-plugin-migration-matrix.md`
   提供“源文档 -> 当前落点 -> 插件落点”的审计依据。

## 内部逻辑

这个项目内部围绕五个核心对象运转：

1. `Issue`
   它是流程主索引。需求从这里开始，所有 PRD、Tech、QA、Release 记录都要回链到它。

2. `Gate`
   它是阶段切换阀门。没有通过当前 Gate，就不能安全进入下一阶段。

3. `Document`
   它是正式决策与交付证据。聊天记录不能替代 PRD、Tech Spec、QA Report、Release Record。

4. `Todo`
   它是行动项闭环机制。所有评审、会议、异常处理都必须落成 Todo 并跟踪到完成。

5. `Memo / Comment / Record`
   它们负责留痕。会议纪要、Issue 评论、变更记录、异常记录、恢复摘要共同保证过程可追溯。

## 核心原则

- Issue 是正式研发流程的强制入口
- PM 先回到问题本身，不直接把用户方案当结论
- 设计确认和实现确认都必须有 Human Review
- 文档阶段和代码阶段必须拆开
- 关键结论必须进入正式留痕对象
- Gate 缺产物、缺签字、缺 Comment 时不能视为完成
- 合规检查是独立治理职责，不替代正式签字角色
- 本项目只保留通用研发流程机制，不引入量化交易业务语义

完整定义见 [核心原则](./docs/governance/core-principles.md)。

## 完整流程图

```text
需求 / 问题 / 异常
        │
        ▼
创建主 Issue
        │
        ▼
PM 澄清问题
每轮讨论必须 Comment 到 Issue
        │
        ▼
PRD
不含技术实现
        │
        ▼
Tech Review + QA Gate
        │
        ▼
QA Case Design
        │
        ▼
文档 PR: doc-{issue}-{desc}
内容: PRD + Tech + QA Case Design
        │
        ▼
Human Review #1
合并 = 设计确认
        │
        ▼
开发与测试
代码 + 测试报告
        │
        ▼
代码 PR: feature-{issue}-{desc}
必须附文档 PR 链接
        │
        ▼
Human Review #2
合并 = 实现确认
        │
        ▼
Issue Comment Gate
产物与结论必须真实回链
        │
        ▼
Release / 验收 / Human 关闭 Issue
        │
        ▼
PMO 按 PR 主动检查
日汇总 / 周复盘 / 月复盘
```

## 三层保障体系

1. 流程规则层  
   prompt、workflow、template 和角色强规则定义阶段、签字、退回条件。

2. 执行留痕层  
   Issue Comment、Memo、Review Record、Change Record、Todo Registry 负责把关键结论正式落地。

3. 平台检查层  
   PR、Issue、CI、自动化脚本等负责检查文档 PR / 代码 PR 前置条件、Comment 成功落地、状态一致性和产物完整性。

## 角色与结构

项目当前沉淀的共享角色包括：

- Team Lead
- Product Manager
- Tech Lead
- Engineer
- QA Engineer
- Researcher
- Platform/SRE
- Process Auditor

其中每个角色都应至少包含：

- 角色主规范
- playbook 执行手册
- 必读文档
- 初始化动作
- 上下文恢复
- Issue / Gate / Human Review 责任
- 禁止行为
- 输出格式

## 整体架构

### 1. 中文源层

- `docs/`
- `prompts/`

### 2. 共享能力层

- `skills/shared/agents/`
- `skills/shared/workflows/`
- `skills/shared/templates/`
- `skills/shared/team-setup.md`
- `skills/shared/start-agent-team.md`
- `skills/shared/create-agent.md`
- `skills/shared/skill-protocol.md`
- `skills/shared/event-bus.md`

核心阶段应优先按 workflow 绑定的模板产出正式文件，而不是自由发挥。

### 3. 交付目录层

- `docs/prd/`
- `docs/tech/`
- `docs/qa/`
- `docs/memo/`
- `docs/todo/`
- `docs/research/`
- `docs/release/`

### 4. 插件与适配层

- `adapters/`
- `plugins/`

这里的目标不是扩展一堆平台私有机制，而是让插件资产可以被不同入口装载。

其中当前最重要的是：

- `plugins/agentdevpipeline/`
- `skills/shared/`
- `prompts/`

## 从哪里开始读

1. [根 README](./README.md)
2. [插件入口说明](./plugins/agentdevpipeline/README.md)
3. [中文总览](./docs/README.md)
4. [核心原则](./docs/governance/core-principles.md)
5. [hedge-ai 迁移矩阵](./docs/migration/hedge-ai-plugin-migration-matrix.md)
6. [Prompt 索引](./prompts/README.md)
7. `skills/shared/`

## 最小接入路径

如果你现在就要把它接到一个项目里，按这个顺序即可：

1. 阅读 [插件入口说明](./plugins/agentdevpipeline/README.md)
2. 阅读 [依赖清单](./docs/reference/dependencies.md)
3. 让团队先按 `prompts/` 和 `skills/shared/` 运行手动流程
4. 再逐步补 `gh`、stacked PR、CI 等增强能力

## 最小可运行示例

- [Kickoff 示例纪要](./docs/memo/kickoff_2026-04-09_agentdevpipeline_execution_example.md)
- [项目组合视图示例](./docs/memo/project_portfolio_2026-04-09_example.md)
- [上下文恢复示例](./docs/memo/context_recovery_2026-04-09_example.md)
- [审计报告示例](./docs/memo/audit_2026-04-09_example.md)
- [产物关联表示例](./docs/memo/artifact_linkage_2026-04-09_example.md)
- [平台检查失败示例](./docs/memo/platform_check_failure_2026-04-09_example.md)
- [Agent 激活记录示例](./docs/memo/agent_activation_2026-04-09_example.md)
- [Agent 创建日志示例](./docs/memo/agent_creation_log_2026-04-09_example.md)
- [Issue Comment Gate 示例](./docs/memo/issue_comment_gate_2026-04-09_example.md)
- [Issue Comment 缺失阻断示例](./docs/memo/issue_comment_failure_2026-04-09_example.md)
- [项目状态板示例](./docs/memo/project_status_board_2026-04-09_example.md)
- [平台检查清单示例](./docs/memo/platform_checklist_2026-04-09_example.md)
- [QA Report 示例](./docs/qa/001_user_notification_center_qa_report_2026-04-09.md)
- [Release Record 示例](./docs/release/001_release_record_example_2026-04-09.md)
- [Todo Registry](./docs/todo/TODO_REGISTRY.md)

## 现在还缺什么

- 还缺把 `github-issue/SKILL.md` 与 `review-org/SKILL.md` 的插件落点写得更明确
- 还缺把插件安装/装载说明继续收紧到更接近可直接接入
- 还缺把剩余完成度审计继续同步到迁移矩阵和插件入口

当前第一优先级不是继续发明新机制，而是把 hedge-ai 的可迁移研发机制拆干净、落准确。

## 适用场景

- 你已经在用 Agent 做研发，但缺统一的交付流程
- 你希望把多角色协作做成可复用的标准资产
- 你需要跨 Claude、Codex、OpenCode 复用同一套研发方法
- 你希望需求、设计、开发、QA、发布之间形成正式闭环

## 不适用场景

- 只想找一个代码生成 prompt
- 只需要单角色自动化，不需要流程治理
- 想直接复用 hedge-ai 的量化交易业务角色和业务流程

相关边界见 [迁移边界（强约束）](./docs/governance/migration-boundary-from-hedge-ai.md)。

## 当前版本

- 内部主版本：`0.3.0`
- 对外发布版本：`0.3.0`
