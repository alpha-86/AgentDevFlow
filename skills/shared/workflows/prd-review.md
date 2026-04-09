# PRD Review Workflow

## 目标

在技术设计开始前，批准或退回 PRD。

## 必需追溯字段

- 关联 issue id
- PRD 文档 id 和状态
- review memo 链接
- todo registry 中的 action items

## 输入

- 当前需求描述
- PRD 草稿
- 已知约束或依赖
- 关联 issue 记录
- 必要时的 Human Review 安排

## 推荐模板与输出目录

- PRD：`skills/shared/templates/prd-template.md`
- Review Comment：`skills/shared/templates/review-comment-template.md`
- Memo：`skills/shared/templates/memo-template.md`
- 推荐输出目录：`docs/prd/`、`docs/memo/`

## 步骤

1. PM 准备 PRD 和验收标准。
2. Tech Lead 评估可行性、依赖和风险。
3. 必要时由领域 reviewer 验证业务匹配。
4. PM 和 Tech Lead 在 PRD review record 中记录签字结论。
5. 若本次 PRD 属于关键需求或高风险需求，执行 Human Review。
6. 在 memo 和关联 issue comment 中记录 review 结论。
7. 把 action items 写入 todo 跟踪，并补充 owner 和 due date。

## 阶段最小产物集合

- 一份 PRD 文档
- 一份 review 结论
- 必要时的一份 Human Review 结论
- 一份 memo 或等价纪要

## Review 检查清单

- 范围是否明确
- 非目标是否明确
- 验收标准是否可测试
- 依赖是否已识别
- 未解决风险是否可见

## 必需签字

- PM：必需
- Tech Lead：必需

## Human Review 规则

- 高风险或关键需求的 PRD，必须进入 Human Review。
- Human Review 未完成时，不得进入 Tech Review。
- Human Review 结论必须写回 issue comment 或 review record。

## 结果

- approved
- conditionally approved
- rejected with rework items

## 回退规则

- conditionally approved：所有条件关闭并补齐证据后，才能进入 tech review
- rejected：PRD 必须修订后重新 review
- blocked：升级给 Team Lead，并把 issue 状态保持为 `blocked`
- 若 Human Review 退回：PRD 必须修订后重新执行当前阶段 review
