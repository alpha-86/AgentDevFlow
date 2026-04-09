# AgentDevPipeline

[English](./README.md) | 中文

AgentDevPipeline 是一个面向 Claude、Codex、OpenCode 等环境的独立产研流程编排项目。它不是单个 Agent 的 prompt 包，也不是某个业务系统的脚手架，而是一套把“需求、设计、开发、测试、发布、复盘”串成闭环的通用研发流程系统。

## 这个项目解决什么问题

很多团队已经能用 Agent 写代码、查资料、做评审，但真正卡住交付的往往不是“单点能力”，而是流程失控：

- 需求、方案、代码、测试之间断链
- 评审靠聊天记录推进，没有正式 Gate
- 任务有人做，但没人维护状态、风险和升级路径
- 会话一断、Agent 一换，整个上下文就丢了
- 同一套流程在 Claude、Codex、OpenCode 上重复造轮子

AgentDevPipeline 要解决的，是这些跨角色、跨阶段、跨工具的编排问题。

## 它如何解决

项目把完整研发流程拆成一组可复用的通用机制：

- 角色层：定义 Team Lead、PM、Tech Lead、Engineer、QA、Researcher、Platform/SRE 的职责边界、禁止越权规则和交付物
- 流程层：定义 PRD、Tech、Implementation、QA、Release 的阶段 Gate，以及日会、周会、月会、Todo Review 等节奏机制
- 留痕层：统一 PRD、Tech Spec、QA Case、Memo、Todo、Change Record、Review Comment、Release Record 的结构
- 编排层：用 Issue 驱动整个流程，把文档、评审结论、阻塞、异常、恢复动作全部串起来
- 适配层：把共享角色、workflow、template 封装成平台无关资产，再由 Claude/Codex/OpenCode 入口接入

项目的目标不是让 Agent “更聪明”，而是让 Agent 参与的研发过程更稳定、更可控、更可审计。

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

把这五类对象连接起来后，项目形成的是一条完整研发链路，而不是一堆分散的提示词文件。

## 核心原则

- 不允许跳过 Gate 直接推进下游阶段
- 代码、文档、测试、发布结论必须一致
- 所有关键判断都要有正式留痕，而不是只留在聊天里
- 上下文恢复必须先读状态、再继续执行
- 关键交付物必须支持 Human Review，而不是只在 Agent 内部流转
- Issue 是流程主索引，必须能承载多项目并行和项目内问题追踪
- 中文是内部主版本，英文是发布镜像
- 本项目只保留通用研发流程机制，不引入量化交易业务语义

完整定义见 [核心原则](./docs/zh-cn/reference/core-principles.md)。

## 完整流程图

```text
需求 / 问题 / 异常
        │
        ▼
   创建主 Issue
        │
        ▼
Research / PRD
        │
        ▼
Tech Spec + QA Case Design
        │
        ▼
Human Review #1
设计确认 / 退回重审
        │
        ▼
Implementation
        │
        ▼
QA Validation + 测试报告
        │
        ▼
Human Review #2
代码/交付确认
        │
        ▼
Release Decision
        │
        ▼
Todo Closure / Weekly Review / Monthly Review
```

这张图强调三件事：

- Issue 是主线，所有交付物都要回链
- 设计确认和代码确认是两个不同的人机协同节点
- 发布不是终点，异常、Todo、复盘还要继续闭环

## 整体架构

可以把 AgentDevPipeline 理解为四层结构：

### 1. 中文源层

- `docs/zh-cn/`
- `prompts/zh-cn/`

这是内部设计和迭代主版本。所有流程、规则、机制先在这里演进。

### 2. 共享能力层

- `skills/shared/agents/`
- `skills/shared/workflows/`
- `skills/shared/templates/`

这是平台无关的核心资产层。角色边界、workflow、模板都放在这里，供不同平台复用。

### 3. 交付目录层

- `docs/prd/`
- `docs/tech/`
- `docs/qa/`
- `docs/memo/`
- `docs/todo/`
- `docs/research/`
- `docs/release/`

这是项目实际产物落地的位置，用来承接每个阶段的正式交付物。

### 4. 平台适配层

- `adapters/`
- `plugins/`

这里只做接入和包装，不改写核心流程语义。

## 关键机制

目前项目已经沉淀的关键机制包括：

- 团队拓扑与角色边界
- Issue 驱动编排
- Issue 路由与项目组合管理
- 文档契约与状态机
- PRD / Tech / QA / Release Gate
- Human Review 与双阶段交付
- 研发日会、周复盘、月复盘
- Todo 闭环
- 变更记录与重审
- 异常升级闭环
- 上下文恢复
- 双轨交付机制
- 流程合规与审计

如果你要找“这套流程具体怎么跑”，核心入口在：

- [中文总览](./docs/zh-cn/README.md)
- [Prompt 索引](./prompts/zh-cn/README.md)
- [仓库结构图](./docs/zh-cn/architecture/repository-map.md)
- [核心原则](./docs/zh-cn/reference/core-principles.md)

## 适用场景

- 你已经在用 Agent 做研发，但缺统一的交付流程
- 你希望把多角色协作做成可复用的标准资产
- 你需要跨 Claude、Codex、OpenCode 复用同一套研发方法
- 你希望需求、设计、开发、QA、发布之间形成正式闭环

## 不适用场景

- 只想找一个代码生成 prompt
- 只需要单角色自动化，不需要流程治理
- 想直接复用 hedge-ai 的量化交易业务角色和业务流程

本项目明确排除基金、交易、回测、因子、盘前盘后、DBR 等量化交易语义。相关边界见 [迁移边界（强约束）](./docs/zh-cn/reference/migration-boundary-from-hedge-ai.md)。

## 快速开始

1. 先读 [中文总览](./docs/zh-cn/README.md)，理解项目范围和阅读顺序。
2. 再读 [Prompt 索引](./prompts/zh-cn/README.md)，理解流程机制。
3. 按平台选择入口：
   - [Claude Code](./docs/zh-cn/platforms/claude-code.md)
   - [Codex](./docs/zh-cn/platforms/codex.md)
   - [OpenCode](./docs/zh-cn/platforms/opencode.md)
4. 在你的项目中落地 `skills/shared/` 里的角色、workflow、template，并把正式产物写入 `docs/prd/`、`docs/tech/`、`docs/qa/`、`docs/release/` 等目录。
5. 对需要人类确认的节点，显式使用 `human-review` workflow，并把结论写回 Issue / PR / Memo。

## 仓库结构

```text
AgentDevPipeline/
├── adapters/           # 平台适配入口
├── docs/               # 中文源文档、英文发布文档、交付目录
├── plugins/            # 插件与平台包装
├── prompts/            # 流程机制与规则定义
├── registry/           # 依赖元数据
└── skills/shared/      # 角色、workflow、template、playbook
```

## 文档治理

- `docs/zh-cn/` 和 `prompts/zh-cn/` 是内部主版本
- `docs/en/` 和 `prompts/en/` 是英文发布版本
- 所有流程和规则变更必须先更新中文，再同步英文
- 与 hedge-ai 的关系是“参考流程样本”，不是运行依赖

## 当前版本

- 内部主版本：`0.3.0`
- 对外发布版本：`0.3.0`
