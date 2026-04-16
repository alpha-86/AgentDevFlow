# 发布评审 工作流

## 目标

判断当前交付包是否足够安全、完整，可以进入发布。

## 必需追溯字段

- 关联 issue id
- 已批准 QA 结果链接
- release plan 和 回滚 plan 链接
- release decision record 链接

## 输入

- 已批准的 QA 结果
- 部署计划
- 回滚计划
- release notes
- 关联 issue 记录
- 需要时的 Human 放行安排

## 推荐模板与输出目录

- Release 记录：`skills/shared/templates/release-record-template.md`
- 评审评论：`skills/shared/templates/review-comment-template.md`
- 推荐输出目录：`docs/release/`

## 步骤

1. PM 确认业务准备情况。
2. 技术负责人 确认技术准备情况。
3. 平台与发布负责人 确认部署和回滚准备情况。
4. 明确 评审 已知风险。
5. PM、技术负责人 和 平台与发布负责人 记录签字结论。
6. 若项目策略要求 Human 放行，则执行最终 Human Release Approval。
7. 把发布决定和后续动作写入关联 issue。

## 阶段最小产物集合

- 一份 release record
- 一份 release 决策评论
- 必要时的一份 Human Release Approval 结论

## 结果

- 通过 for release
- 通过 with known risk
- 阻塞 pending actions

## 必需签字

- PM：必需
- 技术负责人：必需
- 平台与发布负责人：必需

## 人工评审规则

- 对高风险发布、重大变更发布或需要外部确认的发布，必须执行最终 Human Release Approval。
- Human Release Approval 未完成时，不得标记发布完成。

## 回退规则

- 阻塞 pending actions：把 issue 状态保持在 `in_release` 或 `阻塞`
- 发布范围发生重大变化：回到 QA validation 或 tech 评审
- 若最终 Human Release Approval 退回：继续保持 `in_release` 或回退到 QA validation
