# Issue 生命周期 Workflow

## 目标

用单个 issue 作为 PRD、Tech、实现、QA、发布和后续动作的统一追溯主线。

## 状态

- open
- in_prd
- in_tech
- in_impl
- in_qa
- in_release
- blocked
- done
- canceled

## 必需字段

- issue owner
- current gate
- linked documents
- latest review decision
- open blockers
- open todo items

## 状态流转规则

1. `open` -> `in_prd`：只有在范围 owner 已分配后才能进入。
2. `in_prd` -> `in_tech`：只有在 PRD 批准已记录后才能进入。
3. `in_tech` -> `in_impl`：只有在 tech sign-off 完成后才能进入。
4. `in_impl` -> `in_qa`：只有在实现证据已链接后才能进入。
5. `in_qa` -> `in_release`：只有在 QA sign-off 完成或已明确接受已知风险后才能进入。
6. 任意状态 -> `blocked`：当下游动作无法安全继续时进入。
7. `in_release` -> `done`：只有在发布决策已记录后才能进入。

## 必需记录

- gate 决策评论
- 关联 memo 或 review note
- todo 跟进更新

## 常见失败模式

- issue 状态和实际交付阶段漂移
- 关联文档缺失或已过期
- 状态变化没有决策证据
