# 仓库结构与分层

## 分层原则

### L1. 中文源层

- 路径：`docs/zh-cn/`、`prompts/zh-cn/`
- 用途：内部持续迭代、评审、修订
- 约束：所有设计变更先落这里

### L1.1 中文治理层

- 路径：`docs/zh-cn/governance/`
- 用途：维护顶层原则、边界、协议、语言治理
- 约束：所有方法论和边界性调整先落这里

### L2. 英文发布层

- 路径：`docs/en/`、`prompts/en/`
- 用途：对外公开、安装说明、发布材料
- 约束：只能从中文源层翻译同步

### L3. 共享能力层

- 路径：`skills/shared/`
- 用途：平台无关的 agent role、workflow、template
- 约束：尽量不写平台私有语法

### L4. 平台适配层

- 路径：`adapters/`、`plugins/`
- 用途：Claude/Codex/OpenCode 接入说明或适配文件
- 约束：只做入口和平台绑定，不改写核心流程

## 目录结构

```text
docs/
  prd/
  tech/
  qa/
  memo/
  todo/
  research/
  release/
  zh-cn/
    architecture/
    governance/
    migration/
    platforms/
    reference/
  en/
    architecture/
    platforms/
    reference/
prompts/
  discuss/
  zh-cn/
  en/
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
  agentdevpipeline/
```

## 约束

- 角色定义写在 `skills/shared/agents/`，执行手册使用同名 `*.playbook.md`
- 团队启动入口写在 `skills/shared/team-setup.md` 与 `skills/shared/start-agent-team.md`
- Agent 统一创建入口写在 `skills/shared/create-agent.md`
- 事件与状态同步语义写在 `skills/shared/event-bus.md`
- 流程定义写在 `skills/shared/workflows/`
- 模板写在 `skills/shared/templates/`
- 顶层原则、边界和协议写在 `docs/zh-cn/governance/`
- 迁移复核与对照材料写在 `docs/zh-cn/migration/` 和 `prompts/discuss/`
- 项目可直接使用的交付目录写在 `docs/prd/`、`docs/tech/`、`docs/qa/`、`docs/release/` 等路径
- 中文 prompt 文件编号稳定，不随英文文件名漂移
- 英文文件可以做术语归一，但不能擅自新增流程
