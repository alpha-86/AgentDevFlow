# Human Review Workflow

## 目标

在关键交付节点引入明确的人类评审与确认，避免流程只在 Agent 内部自循环。

## 适用对象

- 文档 PR（PRD + Tech Spec + QA Case Design）
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
- 若为代码 PR，必须附已合并的文档 PR 链接
- 上一阶段结论
- 已知风险

## 推荐模板与输出目录

- Review Comment：`skills/shared/templates/review-comment-template.md`
- Memo：`skills/shared/templates/memo-template.md`
- 推荐输出目录：`docs/memo/` 或关联 PR / issue

## 步骤

1. 明确本次 review 的对象、目的和通过条件。
2. 准备结构化 review 摘要和交付物链接。
3. 若为文档 PR，确认 PRD、Tech、QA Case Design 是否齐备。
4. 若为代码 PR，确认文档 PR 已合并且测试报告已附齐。
5. 由 Human 给出 `approved`、`conditional` 或 `rejected`。
6. 在 issue、memo 或 PR 中留下正式结论。
7. 若为 `conditional` 或 `rejected`，生成 action items 和回退路径。

## 阶段最小产物集合

- 一份结构化 review 结论
- reviewer 身份
- 证据链接
- 是否允许进入下游阶段
- 若为双阶段 PR，必须能区分“设计确认”还是“实现确认”

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
- 文档 PR 缺 PRD / Tech / QA Case Design
- 代码 PR 缺文档 PR 链接或测试报告
