# GitHub Issue 与评审评论机制

## 目标

把 GitHub Issue、评审评论和文档 Gate 绑定起来，确保线上协作轨迹可追溯、可审计。

## 主规则

- 一个正式交付流程必须有主 Issue。
- PRD / Tech / QA / Release 的结论必须能在 Issue 中找到。
- 评审评论不是聊天记录替代品，而是 Gate 留痕的一部分。
- 评论只有真正写入目标 Issue 后才算完成，本地草稿、pending 文件或聊天摘要都不算。

## Issue 最小结构

- 背景
- 目标
- 当前阶段
- 当前 owner
- 关联文档链接
- 最新 Gate 结论
- 打开的 Todo / blocker

## 评论写入时机

- PRD Review 结束
- Tech Review 结束
- QA 结论输出
- Release 决策输出
- Major / Breaking 变更发生
- 异常升级或恢复完成

## Gate 评论最小字段

- Gate 名称
- 决策人
- 结论
- 证据链接
- 待办与 owner
- 是否允许进入下游阶段

## 评论约束

- 禁止只写“LGTM”“通过”“看过了”之类无结构结论
- 禁止评论结论与正式文档状态不一致
- 条件通过必须写清条件和复核人
- 评论中只放结构化结论与链接摘要，不粘贴长篇设计正文
- Agent 默认不自行关闭主 Issue，除非项目策略显式允许
- 自动投递评论失败时，必须把当前动作标记为失败，不能伪装成成功

## 强制 Gate 要求

- PRD / Tech / QA / Release 阶段的正式结论，只有在 Issue Comment 成功落地后才算阶段完成
- 若阶段要求存在 Comment，但目标 Issue 下查不到该 Comment，则视为未完成
- 代码 PR 创建前，应确认上游必需 Comment 已存在
- 代码 PR 合并前，应确认当前阶段 Comment 和产物链接完整

## 失败处理

- 若当前阶段缺少必需 comment，则该阶段不能视为完成
- 若 comment 字段不完整，则必须补齐后重试
- 若 comment 与 issue / 文档状态不一致，则以更严格状态为准并触发纠正
- 必须指定修复 owner 和重试条件
- 若 comment 自动投递失败，必须返回非成功状态，阻断下游动作

## PR / Issue 关系

- PR 必须回链主 Issue
- 合并前必须确认主 Issue 的阶段状态与 PR 实际内容一致
- 若 PR 引入 Major / Breaking 变更，Issue 必须先完成重审记录
- 若 Issue Comment 缺失，不得把 PR 创建或合并视为合规完成
