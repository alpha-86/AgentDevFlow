# 033 - 2026-04-10 Phase 3.3 plugin.json 复核

## 目标

校准 `plugins/agentdevflow/.codex-plugin/plugin.json`，使其与当前仓库的插件定位和版本状态一致。

## 当前项目原有问题

旧版 `plugin.json` 的问题很直接：

- 版本号仍是 `0.1.0`
- 描述太泛，只写成了一般性的 agent workflow package
- `author.name` 仍是占位值

这和当前仓库已经明确的插件定位不一致。

## 本次落地调整

### 1. 版本号同步

将插件版本从：

- `0.1.0`

调整为：

- `0.3.0`

与当前根 README 中的版本口径保持一致。

### 2. 描述收紧

将描述改成更贴当前目标的表述：

- 不是泛指任意 workflow package
- 而是明确写成：从 `hedge-ai` 拆出可复用研发机制，形成独立 agent development pipeline 插件包

### 3. 作者字段去占位

将：

- `[TODO: maintainer]`

替换为：

- `alpha-86`

至少先去掉明显未完成的占位值。

## 结论

`plugin.json` 现在至少和当前仓库状态一致了：

- 版本一致
- 描述一致
- 作者字段不再是占位符

下一步进入 `Phase 3.4`，检查 `skills/shared/` 是否已经足以构成插件核心资产。
