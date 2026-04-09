# Tech Review Workflow

## 目标

在实现开始前，批准或退回 tech spec。

## 必需追溯字段

- 关联 issue id
- 已批准 PRD id
- tech spec id 和状态
- review memo 链接
- 后续动作的 todo 链接

## 输入

- 已批准的 PRD
- tech spec 草稿
- 依赖和 rollout 说明
- 关联 issue 记录
- 必要时的 Human Review 安排

## 推荐模板与输出目录

- Tech Spec：`skills/shared/templates/tech-spec-template.md`
- Review Comment：`skills/shared/templates/review-comment-template.md`
- Artifact Linkage：`skills/shared/templates/artifact-linkage-template.md`
- 推荐输出目录：`docs/tech/`、`docs/memo/`

## 步骤

1. Tech Lead 发布 tech spec。
2. PM 检查需求覆盖情况。
3. QA 检查可测试性和验证路径。
4. Tech Lead 和 QA 在 tech review record 中记录签字结论。
5. 对关键方案、复杂方案或高风险改动执行 Human Review。
6. 在 memo 和关联 issue comment 中记录 review 结果。
7. 把 action items 写入 todo 跟踪，并补充 owner 和 due date。

## 阶段最小产物集合

- 一份 Tech Spec
- 一份 Tech Review 结论
- 必要时的一份 Human Review #1 结论
- 一份产物关联表或等价链接清单

## Review 检查清单

- 每项关键 PRD 需求是否都有覆盖
- 接口和数据流是否清晰
- rollout 和 rollback 点是否存在
- 验证路径是否可执行
- 风险和假设是否明确

## 必需签字

- Tech Lead：必需
- QA：必需
- PM：范围一致性确认必需

## Human Review 规则

- 关键方案、复杂方案和高风险改动，必须进入 Human Review。
- Human Review 未完成时，不得进入 Implementation。
- Human Review 结论必须说明是否允许开始实现。

## 结果

- approved
- conditionally approved
- rejected with rework items

## 回退规则

- conditionally approved：所有条件关闭并复核后，才能进入 implementation
- rejected：tech spec 必须修订后重新 review
- 若 PRD 发生重大变化：先回到 PRD review
- 若 Human Review 退回：tech spec 必须修订并重新执行 Tech Review
