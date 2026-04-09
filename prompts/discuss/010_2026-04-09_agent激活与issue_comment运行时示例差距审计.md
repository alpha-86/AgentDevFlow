# 010 - 2026-04-09 Agent 激活与 Issue Comment 运行时示例差距审计

## 结论

当前 AgentDevPipeline 已经有：

- `agent-activation-template.md`
- `review-comment-template.md`
- `issue comment gate` 相关 prompt

但仍缺少两类关键运行时示例：

- 角色激活后的初始化记录示例
- 阶段 comment 的正式示例

没有这两类示例时，用户虽然知道“应该写”，但不容易判断“应该写到什么粒度”。

## 本轮决策

1. 增加 agent 激活记录示例
2. 增加 issue comment gate 示例
3. 在 README 和中文总览中把这两类示例挂出来
