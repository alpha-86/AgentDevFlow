# 017 Phase 1.1 README 与 CHANGELOG 复核

## 复核范围

- `hedge-ai/prompts/V3.0/README.md`
- `hedge-ai/prompts/V3.0/CHANGELOG.md`

## 复核结论

### 1. `README.md` 可迁移的部分

可迁移的不是量化业务流程本身，而是以下研发机制组织方式：

- 以“启动指南”作为顶层阅读入口
- 明确团队初始化顺序
- 明确角色必读文档分配关系
- 把双阶段 PR 机制放在入口文档中作为主流程总览
- 给出上下文恢复和文件结构总览

当前问题：

- 本项目根 `README.md` 已转向“独立插件”口径，但还没有完全达到 hedge-ai 入口文档那种“启动步骤 + 阅读顺序 + 关键机制总览”强度
- 插件入口 `plugins/agentdevpipeline/README.md` 仍然偏薄，无法承担真正的插件启动指南角色

### 2. `CHANGELOG.md` 可迁移的部分

可迁移的是以下机制：

- 变更必须分版本记录
- 每条变更要写：原因、核心内容、涉及文件、详细记录
- `CHANGELOG.md` 与 `change_record/` 要形成主索引与详情联动

当前问题：

- 本项目当前缺严格意义上的根 `CHANGELOG.md`
- 变更记录分散在 `prompts/discuss/`、migration 审计和提交历史中，还没有形成和 hedge-ai 对应的正式主索引

## 对插件目标的影响

`README.md` 和 `CHANGELOG.md` 不是外围文档，而是插件能否独立使用的两个入口：

- `README.md` 解决“怎么理解和开始使用插件”
- `CHANGELOG.md` 解决“插件到底演进了什么、当前到哪个版本”

因此它们应在后续 Phase 3 中作为插件资产收口的重点对象，而不是普通补充文档。

## 回写到计划

- `1.1` 已完成
- 其结果已回写到迁移矩阵
