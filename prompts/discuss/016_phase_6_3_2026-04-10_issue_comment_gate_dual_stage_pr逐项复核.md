# 016 Phase 6.3 - 2026-04-10 issue / comment / gate / dual-stage PR 逐项复核

## 复核范围

- `prompts/007_issue_driven_orchestration.md`
- `prompts/013_github_issue_and_review_comments.md`
- `prompts/019_dual_stage_pr_and_three_layer_safeguard.md`
- `prompts/020_issue_comment_gate_and_artifact_linkage.md`
- `skills/shared/workflows/issue-lifecycle.md`
- `skills/shared/workflows/human-review.md`

## 本轮结论

当前这一层的核心差距，是若单看单篇文档都“差不多有了”，但连起来仍有三处容易失真：

1. `in_tech -> in_impl` 的跃迁条件还不够硬
   - 文档 PR 合并
   - Human Review #1 留痕
   之前没有完全压进同一套规则

2. `in_qa -> in_release` 与 `done` 的闭环还不够硬
   - Human Review #2
   - Human 最终关闭 Issue
   之前虽然原则上提到，但还没有同时压进状态机和 comment gate

3. 文档 PR / 代码 PR / Issue / Comment / Human Review 的反查链还不够明确
   - 有规则，但不够统一

## 本轮修正

### 1. Issue 状态机收紧

- `in_tech -> in_impl`
  - 增加：文档 PR 已合并 + Human Review #1 已留痕
- `in_qa -> in_release`
  - 增加：Human Review #2 已留痕或风险已明确接受
- `in_release -> done`
  - 增加：Human 最终关闭确认

### 2. Comment Gate 收紧

- Gate 评论最小字段新增：
  - `project_id`
  - 当前 Issue 状态
- 文档 PR 合并前，必须检查：
  - 文档阶段 Comment
  - 产物链接
  - Human Review #1 结论
- 代码 PR 合并前，必须检查：
  - 实现阶段 Comment
  - 产物链接
  - Human Review #2 结论

### 3. 双阶段 PR 反查链补齐

- 文档 PR 最小要求新增主 Issue 链接
- 主 Issue 下必须能反查：
  - 文档 PR
  - 代码 PR
  - PRD / Tech / QA / Release

### 4. Human Review 留痕规则补齐

- Human Review #1 必须能从主 Issue 或文档 PR 反查
- Human Review #2 必须能从主 Issue 或代码 PR 反查
- 会议纪要不能替代 Issue / PR 上的正式评审结论

## 复核判断

`Phase 6.3` 可以落账，含义是：

- Issue / Comment / Gate / 双阶段 PR 已经形成更统一的硬约束链
- “设计确认”“实现确认”“最终关闭”三个节点都更明确地被压进主流程

后续 `6.4` 继续处理 evaluation checker 这一块，把评审维度从说明文档继续往更独立的检查能力推进。
