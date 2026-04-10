# Issue Comment 缺失阻断示例

**平台**: Claude
**日期**: 2026-04-09
**Issue**: #0
**当前阶段门**: QA
**结论**: fail
**执行人**: 流程审计员

## 失败原因

- QA 测试报告已存在，但主 Issue 下缺少 QA 结论评论
- 当前 issue 状态已尝试进入 `in_release`，与缺失的 QA 评论不一致

## 阻断范围

- 当前阶段不得进入发布评审
- issue 状态不得继续推进到 `in_release`

## 修复负责人

- 质量工程师：补 QA 结论评论
- 团队负责人：纠正 issue 状态并重新检查阶段一致性

## 重试条件

- QA 评论已写入主 Issue
- 评论字段齐全且与测试报告状态一致
- issue 状态回到与 QA 阶段一致的值

## 相关链接

- `docs/qa/000_user_notification_center_qa_2026-04-09.md`
- `skills/shared/templates/review-comment-template.md`
