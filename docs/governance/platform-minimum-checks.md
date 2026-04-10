# 平台最小检查规范

## 目标

定义 Claude、Codex、OpenCode 等平台适配层必须具备的最小检查能力，保证共享流程规则能够被真正执行。

## 最小检查集合

### 1. Gate 前置检查

- 文档阶段应有产物是否存在
- 当前阶段应有签字是否存在
- 当前阶段应有 Human Review 是否存在

### 2. Issue 检查

- 是否存在主 Issue
- 当前 issue 状态是否与 gate 一致
- 是否存在必需的 issue comment

### 3. 产物关联检查

- PRD / Tech / QA / Release 是否能回链 issue
- 产物关联表是否完整

### 4. 状态一致性检查

- issue、todo、memo、review record 的状态是否一致
- release 前 QA 结论是否已存在

## 平台实现要求

- 平台可以通过 PR 检查、CI、Bot、Hook、API 校验等方式实现
- 只要检查效果等价，即视为符合 AgentDevFlow 标准
- 平台实现不得绕过共享流程规则

## 检查结果最小字段

- 平台
- 日期
- issue
- 当前 gate
- 结论（`pass / warning / fail`）
- 失败原因
- 阻断范围
- 修复 owner
- 重试条件
- 相关链接

## 失败处理要求

- 检查失败必须阻断当前阶段继续推进
- 必须给出明确失败原因
- 必须指出由谁修复、修复后如何重试

## 失败处理流程

1. 记录平台检查结果。
2. 将结论写为 `warning` 或 `fail`。
3. 若为 `fail`，立即阻断当前阶段继续推进。
4. 指定修复 owner 和重试条件。
5. 修复完成后重新执行平台检查。

## 重试完成判定

- 失败项已关闭
- 当前 gate 可继续推进
- issue、artifact linkage、review 结论已恢复一致
