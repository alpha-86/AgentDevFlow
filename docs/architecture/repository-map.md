# 仓库结构与分层

## 分层原则

### L1. 中文源层

- 路径：`docs/`、`prompts/`
- 用途：内部持续迭代、评审、修订
- 约束：所有设计变更先落这里

### L1.1 中文治理层

- 路径：`docs/governance/`
- 用途：维护顶层原则、边界、协议和平台检查约束
- 约束：所有方法论和边界性调整先落这里

### L2. 共享能力层

- 路径：`skills/`
- 用途：平台无关的智能体角色、工作流、模板
- 约束：尽量不写平台私有语法

### L3. 平台适配层

- 路径：`adapters/`、`plugins/`
- 用途：Claude/Codex/OpenCode 接入说明或适配文件
- 约束：只做入口和平台绑定，不改写核心流程

## 目录结构

```text
docs/
  architecture/
  governance/
  migration/
  platforms/
  reference/
  prd/
  tech/
  qa/
  memo/
  todo/
  research/
  release/
prompts/
  discuss/
skills/
  shared/
    team-setup.md
    start-agent-team.md
    create-agent.md
    skill-protocol.md
    event-bus.md
    agents/
    workflows/
    templates/
adapters/
  claude/
  codex/
  opencode/
plugins/
  agentdevflow/
```

## 约束

- 角色定义写在 `skills/agents/`，执行手册使用同名 `*.playbook.md`
- 团队启动入口写在 `skills/team-setup.md` 与 `skills/start-agent-team.md`
- Agent 统一创建入口写在 `skills/create-agent.md`
- 事件与状态同步语义写在 `skills/event-bus.md`
- 流程定义写在 `skills/workflows/`
- 模板写在 `skills/templates/`
- 顶层原则、边界和协议写在 `docs/governance/`
- 迁移复核与对照材料写在 `docs/migration/` 和 `prompts/discuss/`
- 项目可直接使用的交付目录写在 `docs/prd/`、`docs/tech/`、`docs/qa/`、`docs/release/` 等路径
- prompt 文件编号稳定，不随目录重组漂移
