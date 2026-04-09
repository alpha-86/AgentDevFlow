# 实现 Workflow

## 目标

把已批准的技术方案转化为代码、测试和实现证据。

## 必需追溯字段

- 关联 issue id
- 已批准 PRD id
- 已批准 tech spec id
- 实现 commit 链接
- 测试证据链接

## 输入

- 已批准的 PRD
- 已批准的 Tech Spec
- 已切分的 todo items
- 关联 issue 记录
- 文档阶段 Human Review 已完成的证据

## 推荐模板与输出目录

- Review Comment：`skills/shared/templates/review-comment-template.md`
- Artifact Linkage：`skills/shared/templates/artifact-linkage-template.md`
- 推荐输出目录：代码仓库实现位置、`docs/memo/`

## 步骤

1. Engineer 校验已批准输入。
2. Engineer 实现本次范围内的改动。
3. Engineer 补充单元测试和变更说明。
4. Engineer 记录偏差或 blocker。
5. Engineer 在 issue 中更新实现证据。
6. Engineer 把可追溯证据交接给 QA。

## 阶段最小产物集合

- 实现代码
- 测试证据
- implementation 交接摘要
- issue comment 中的实现证据链接

## 退出条件

- 代码改动已存在
- 单元测试已存在
- 实现说明已存在
- 已具备 QA 交接条件
- 文档阶段 Human Review 已明确允许进入实现

## 必需签字

- Engineer：必需
- Tech Lead：实现一致性检查必需

## 回退规则

- 若实现偏离已批准 tech spec：回到 tech review
- 若验收映射断裂：回到 PRD review
- 若发现文档阶段 Human Review 未完成：停止实现并回到对应上游 Gate
