# Human Review Workflow

## 目标

在关键交付节点引入明确的人类评审与确认，避免流程只在 Agent 内部自循环。

## 适用对象

- PRD
- Tech Spec
- QA Case Design
- 代码 PR
- 发布决策
- Major / Breaking 变更

## Review 形式

- 文档 review
- Pull Request review
- Issue comment confirm
- 发布放行确认
- 例外审批确认

## 输入

- 关联 issue
- 当前 gate
- 待评审交付物链接
- 上一阶段结论
- 已知风险

## 推荐模板与输出目录

- Review Comment：`skills/shared/templates/review-comment-template.md`
- Memo：`skills/shared/templates/memo-template.md`
- 推荐输出目录：`docs/memo/` 或关联 PR / issue

## 步骤

1. 明确本次 review 的对象、目的和通过条件。
2. 准备结构化 review 摘要和交付物链接。
3. 由 Human 给出 `approved`、`conditional` 或 `rejected`。
4. 在 issue、memo 或 PR 中留下正式结论。
5. 若为 `conditional` 或 `rejected`，生成 action items 和回退路径。

## 阶段最小产物集合

- 一份结构化 review 结论
- reviewer 身份
- 证据链接
- 是否允许进入下游阶段

## 必需输出

- reviewer 身份
- 决策结论
- 关键意见
- 证据链接
- 下游是否允许继续推进

## 失败信号

- 没有明确 reviewer
- 只有口头结论，没有正式留痕
- 没有条件项却标记为条件通过
- Human Review 未完成却继续推进下游阶段
