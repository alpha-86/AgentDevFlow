# 事件总线与交接机制

## 目标

用统一的事件模型连接角色、文档、Todo 和 Gate，减少信息丢失与跨角色误解。

## 事件定义

事件是流程中发生的、需要被其他角色消费的结构化状态变化。

## 事件最小字段

- 事件 ID
- 事件类型
- 来源角色
- 关联 Issue
- 关联文档或 Gate
- 发生时间
- 当前状态
- 下一动作

## 核心事件类型

- `prd_submitted`
- `prd_approved`
- `tech_submitted`
- `tech_approved`
- `implementation_ready`
- `qa_blocked`
- `qa_approved`
- `release_blocked`
- `release_approved`
- `todo_blocked`
- `context_recovered`

## 事件使用规则

- 每个 Gate 完成时，必须至少产生一个可追溯事件。
- 事件必须能够回链到 Issue 和文档，不允许孤立存在。
- 阻塞事件必须携带“阻塞原因 + 负责人 + 升级路径”。

## Handoff 契约

任何角色把工作交给下游角色时，必须交付：

- 当前阶段
- 已完成证据
- 未完成事项
- 风险与阻塞
- 下游角色可直接使用的链接

## 标准 Handoff 模板

- From:
- To:
- Issue:
- Current Gate:
- Completed Evidence:
- Open Risks:
- Open Todos:
- Expected Next Action:

## 失败信号

出现以下任一情况，视为交接失败：

- 下游角色无法判断当前阶段
- 证据链接缺失
- Todo 与交接内容不一致
- 风险已知但未显式传递
