# Event Bus

## 目标

定义 AgentDevPipeline 的共享事件语义、触发规则、状态流转和失败升级路径，让不同平台的自动化检查、Issue 同步、Gate 阻断都能围绕同一套事件模型工作。

## 适用边界

- 这里定义的是通用研发流程事件，不包含量化交易、盘前盘后、策略回测等业务语义。
- 平台适配层可以用 GitHub Action、Bot、脚本、Webhook、CI 或本地命令来实现，但不得改写这里的状态含义。

## 核心组件

- `Event Source`
  角色动作、文档更新、Issue 更新、评论更新、PR 状态变化、检查任务结果。
- `Event Bus`
  统一分发事件，驱动下游检查、通知、升级和留痕。
- `Workflow Engine`
  根据事件触发共享 workflow 的某一步或整条流程。
- `State Store`
  持久化 issue、gate、artifact linkage、todo、platform checks 的最近状态。
- `Audit Layer`
  记录自动化动作、失败原因、重试情况和人工接管结论。

## 标准事件

### 1. 文档事件

- `document.created`
- `document.updated`
- `document.review_requested`
- `document.review_completed`

最小字段：

- `project_id`
- `issue_id`
- `document_type`
- `document_path`
- `gate`
- `source_role`
- `timestamp`

### 2. Issue 事件

- `issue.created`
- `issue.routed`
- `issue.stage_changed`
- `issue.blocked`
- `issue.comment_posted`
- `issue.comment_missing`
- `issue.closed_requested`

最小字段：

- `project_id`
- `issue_id`
- `issue_type`
- `current_stage`
- `owner`
- `blocking_reason`
- `required_artifacts`

### 3. Review / Gate 事件

- `review.requested`
- `review.approved`
- `review.conditional`
- `review.rejected`
- `gate.enter_requested`
- `gate.enter_blocked`
- `gate.enter_approved`

最小字段：

- `project_id`
- `issue_id`
- `gate`
- `required_signoffs`
- `actual_signoffs`
- `required_comments`
- `artifact_links`

### 4. Human Review 事件

- `human_review.requested`
- `human_review.completed`
- `human_review.rejected`
- `human_review.timeout`

最小字段：

- `project_id`
- `issue_id`
- `review_slot`
- `review_scope`
- `reviewer`
- `decision`
- `decision_record`

### 5. 平台检查事件

- `platform_check.started`
- `platform_check.passed`
- `platform_check.failed`
- `platform_check.retried`

最小字段：

- `project_id`
- `issue_id`
- `check_name`
- `check_scope`
- `result`
- `evidence_path`

## 共享状态机

### Workflow 状态

`pending -> in_progress -> blocked -> completed`

### Review 状态

`requested -> approved | conditional | rejected | timeout`

### Platform Check 状态

`pending -> running -> pass | fail -> retried -> pass | fail`

## 触发规则

### 文档阶段

- PRD 创建后：
  - 触发 `document.created`
  - 触发 `review.requested`
  - 进入 `prd_review`

- Tech Spec 更新后：
  - 触发 `document.updated`
  - 检查是否需要 change record
  - 必要时回退到 `tech_review`

### 实现阶段

- Implementation 交付后：
  - 触发 `issue.stage_changed`
  - 触发 `review.requested`
  - 触发 `platform_check.started`
  - 自动要求 QA 接手

### 评论与留痕

- Gate 结论发出后：
  - 触发 `issue.comment_posted`
  - 校验 comment 是否包含最小字段和链接
  - 缺失时触发 `issue.comment_missing`
  - 阻断进入下游阶段

## 自动阻断规则

- 主 issue 缺失时，不允许进入任何正式 Gate。
- 必需文档链接缺失时，不允许进入下游阶段。
- Human Review 必需但未完成时，不允许进入 implementation 或 release。
- QA 未完成时，不允许进入 release。
- Issue comment 缺字段时，不允许把 gate 标为已完成。

## 失败与升级

### 失败类型

- `missing_input`
- `missing_comment`
- `state_drift`
- `timeout`
- `platform_error`
- `manual_override_required`

### 处理顺序

1. 记录失败结果。
2. 标记当前 issue 为 `blocked` 或 `needs_revalidation`。
3. 生成待办并指定 owner。
4. 必要时升级给 Team Lead 或 Process Auditor。
5. 只有补齐缺口后才允许重试。

## 平台实现要求

- 平台适配层至少要能观察 issue、comment、artifact linkage、gate 状态。
- 无法自动执行的步骤，也必须有结果模板和人工补录路径。
- 平台自动化只能推进状态，不能绕过人工签字和 Human Review。

## 推荐落地映射

- `issue.created` / `issue.routed`
  对应 `workflows/issue-routing.md`
- `review.requested` / `gate.enter_requested`
  对应 `workflows/prd-review.md`、`workflows/tech-review.md`
- `human_review.requested`
  对应 `workflows/human-review.md`
- `platform_check.*`
  对应 `templates/platform-checklist-template.md` 和 `templates/platform-check-result-template.md`
- `issue.comment_missing`
  对应 `prompts/zh-cn/020_issue_comment_gate_and_artifact_linkage.md`
