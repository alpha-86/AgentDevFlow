# Issue 生命周期工作流

## 目标

用单个 issue 作为 PRD、Tech、实现、QA、发布和后续动作的统一追溯主线。

## 状态

- open
- in_prd
- in_tech
- in_impl
- in_qa
- in_release
- 阻塞
- done
- canceled

## 必需字段

- project_id
- issue 负责人
- current gate
- linked documents
- linked prs
- latest 评审 decision
- open 阻塞项
- open todo items

## 状态流转规则

1. `open` -> `in_prd`：只有在范围 负责人 已分配后才能进入。
2. `in_prd` -> `in_tech`：只有在 PRD 批准已记录后才能进入。
3. `in_tech` -> `in_impl`：只有在 tech sign-off 完成、文档 PR 已合并且 Human Review #1 已留痕后才能进入。
4. `in_impl` -> `in_qa`：只有在实现证据已链接后才能进入。
5. `in_qa` -> `in_release`：只有在 QA sign-off 完成、Human Review #2 已留痕或已明确接受已知风险后才能进入。
6. 任意状态 -> `阻塞`：当下游动作无法安全继续时进入。
7. `in_release` -> `done`：只有在发布决策已记录且 Human 完成最终关闭确认后才能进入。

## 必需记录

- gate 决策评论
- 关联 纪要 或 评审 note
- todo 跟进更新
- 文档 PR / 代码 PR 链接（如适用）
- Human Review 结论（如适用）

## 常见失败模式

- issue 状态和实际交付阶段漂移
- 关联文档缺失或已过期
- 状态变化没有决策证据
