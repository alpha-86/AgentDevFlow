# 发布评审 Workflow

## 目标

判断当前交付包是否足够安全、完整，可以进入发布。

## 必需追溯字段

- 关联 issue id
- 已批准 QA 结果链接
- release plan 和 rollback plan 链接
- release decision record 链接

## 输入

- 已批准的 QA 结果
- 部署计划
- 回滚计划
- release notes
- 关联 issue 记录

## 步骤

1. PM 确认业务准备情况。
2. Tech Lead 确认技术准备情况。
3. Platform/SRE 确认部署和回滚准备情况。
4. 明确 review 已知风险。
5. PM、Tech Lead 和 Platform/SRE 记录签字结论。
6. 把发布决定和后续动作写入关联 issue。

## 结果

- approved for release
- approved with known risk
- blocked pending actions

## 必需签字

- PM：必需
- Tech Lead：必需
- Platform/SRE：必需

## 回退规则

- blocked pending actions：把 issue 状态保持在 `in_release` 或 `blocked`
- 发布范围发生重大变化：回到 QA validation 或 tech review
