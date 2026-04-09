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

## 步骤

1. Engineer 校验已批准输入。
2. Engineer 实现本次范围内的改动。
3. Engineer 补充单元测试和变更说明。
4. Engineer 记录偏差或 blocker。
5. Engineer 在 issue 中更新实现证据。
6. Engineer 把可追溯证据交接给 QA。

## 退出条件

- 代码改动已存在
- 单元测试已存在
- 实现说明已存在
- 已具备 QA 交接条件

## 必需签字

- Engineer：必需
- Tech Lead：实现一致性检查必需

## 回退规则

- 若实现偏离已批准 tech spec：回到 tech review
- 若验收映射断裂：回到 PRD review
