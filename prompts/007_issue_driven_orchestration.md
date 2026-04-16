# Issue 驱动编排机制

## 目标

把交付流程统一收敛到 Issue 主线，确保每个 Gate 的输入、输出、结论、行动项都可追溯，并把 `Issue First` 从一般性建议提升为正式入口约束。

## 核心原则

- 无 Issue 不进入正式交付流程。
- Issue 是唯一流程主索引，PRD/Tech/QA/Release 都必须回链到该 Issue。
- Gate 结论必须写入 Issue 评论或关联记录，不允许口头通过。
- 一个需求、一个问题、一次异常，都必须有自己的 Issue 主线。
- Issue 可以包含用户给出的方案，但流程必须先回到问题本身，而不是直接把方案当结论执行。

## 强制入口规则

### 1. 哪些事项必须先建 Issue

- 新需求
- 缺陷
- 异常
- 流程纠偏
- 发布后问题

### 2. 没有 Issue 时禁止的动作

- 进入 PRD
- 进入 Tech Review
- 安排正式开发
- 安排正式 QA
- 给出发布放行结论

### 3. 谁负责维护 Issue 主线

- PM 负责需求类 / 问题类 Issue 的问题澄清与主线维护。
- Team Lead 负责检查流程是否已经回到对应 Issue。
- 其他角色负责把各自阶段的正式结论回写到同一个 Issue。

## PM Issue 讨论规则

- Issue 中如果已经包含“用户建议的解决方案”，PM 也不能直接接受，必须先澄清问题、目标、约束和边界。
- 每轮正式讨论结束后，必须把结论写成 Issue Comment，不能只留在聊天窗口。
- PRD 完成后，必须在 Issue Comment 中给出摘要和 PRD 链接。
- PRD 只描述问题、目标、范围、产品方案和边界，不写技术实现细节。

## Issue 状态机（最小）

- `open`：已创建，待需求澄清
- `in_prd`：PRD 编写/评审中
- `in_tech`：Tech 方案编写/评审中
- `in_impl`：开发实现中
- `in_qa`：验证中
- `in_release`：发布评审中
- `done`：完成
- `blocked`：阻塞
- `canceled`：取消

## 产物绑定规则

- PRD 必须回链到对应 Issue。
- Tech Spec 必须回链到对应 Issue。
- QA Case / QA Report 必须回链到对应 Issue。
- Release Record 必须回链到对应 Issue。
- Todo、Memo、Change Record、Review Record 如与当前事项有关，也必须回链到对应 Issue。
- 只有当上游产物已经完整挂接到 Issue，才能进入最终关闭动作。

## Gate 与 Issue 的绑定规则

### Gate 1 PRD Review

- 入场条件：Issue 有明确问题描述、目标、范围，且 PM 已完成问题澄清。
- 出场条件：PRD 状态 `Approved`，Issue 留下评审结论、action items、PRD 链接。

### Gate 2 Tech Review

- 入场条件：PRD `Approved`。
- 出场条件：Tech Spec `Approved`，Issue 留下风险、依赖、重审条件；若属于双阶段 PR，则必须同时具备文档 PR 合并前置条件。

### Gate 3 Implementation

- 入场条件：Tech Spec `Approved`，文档 PR 已合并，Human Review #1 已完成，**Team Lead 已通知 Human 执行文档 PR 合并**。
- 出场条件：实现证据（代码、测试、说明）回链 Issue，并明确是否具备 Human Review #2 条件。

> Team Lead 通知 Human 执行 PR 合并是 Human Review #1 通过后的强制步骤。见 `prompts/002_develop_pipeline.md`。

### Gate 4 QA Validation

- 入场条件：实现证据完整。
- 出场条件：测试报告与缺陷结论回链 Issue，给出放行或阻断意见；阻塞性缺陷未清除时不得进入关闭。

### Gate 5 Release Review

- 入场条件：QA 无阻塞缺陷或风险已明确接受。
- 出场条件：发布结论、回滚方案、值守安排回链 Issue；Issue 是否关闭由 Human 最终确认。

## 强制评论模板（Issue 内）

每次 Gate 完成后必须包含：

- Gate 名称与日期
- 结论（Approved / Conditional / Rejected）
- 关键证据链接
- 待办清单（负责人 + 截止时间）
- 下一 Gate 的入场条件
- 当前 Issue 状态是否需要更新

## 关闭规则

- Issue 关闭前必须确认：
  - 关键产物已全部回链
  - 当前 Gate 已正式完成
  - 阻塞性缺陷已清除或有明确例外批准
- Issue 默认不由 Agent 私自关闭，应由 Human 或明确授权的人类操作完成最终关闭。

## 禁止行为

- 跳过 Issue 直接开工
- 把用户给出的方案直接当成 PRD 结论
- 讨论结束不写 Issue Comment
- Gate 结论不留痕
- 用聊天记录替代正式评审结论
- 状态与实际阶段不一致且不修正
- 产物未回链就关闭 Issue
