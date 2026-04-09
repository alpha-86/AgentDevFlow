# 仓库结构与分层

## 分层原则

### L1. 中文源层

- 路径：`docs/zh-cn/`、`prompts/zh-cn/`
- 用途：内部持续迭代、评审、修订
- 约束：所有设计变更先落这里

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
    migration/
    platforms/
    reference/
  en/
    architecture/
    platforms/
    reference/
prompts/
  zh-cn/
  en/
skills/
  shared/
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

- 角色定义写在 `skills/shared/agents/`
- 流程定义写在 `skills/shared/workflows/`
- 模板写在 `skills/shared/templates/`
- 项目可直接使用的交付目录写在 `docs/prd/`、`docs/tech/`、`docs/qa/`、`docs/release/` 等路径
- 中文 prompt 文件编号稳定，不随英文文件名漂移
- 英文文件可以做术语归一，但不能擅自新增流程
