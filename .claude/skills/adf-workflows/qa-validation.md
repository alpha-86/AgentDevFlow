# QA 验证 工作流

## 目标

依据已在文档阶段确认的 QA Case Design、PRD 和 Tech 要求，验证已交付的实现。

## 必需追溯字段

- 关联 issue id
- 已批准的 PRD 和 tech spec ids
- QA case design 链接
- 测试报告链接
- defect 列表和残留风险链接

## 输入

- 已批准的 PRD
- 已批准的 Tech Spec
- 已批准的 QA Case Design
- 实现证据
- 关联 issue 记录
- 必要时的 人工评审 #2 安排

## 推荐模板与输出目录

- QA Case：`.claude/skills/adf-templates/qa-case-template.md`
- QA Report：`.claude/skills/adf-templates/qa-report-template.md`
- 评审评论：`.claude/skills/adf-templates/review-comment-template.md`
- 推荐输出目录：`docs/qa/`

## 步骤

1. QA 校验当前实现是否覆盖文档阶段已确认的 QA Case Design。
2. QA 执行验证。
3. QA 记录 defects 和残留风险。
4. PM 评估对验收的影响。
5. QA 和 PM 记录签字结论。
6. 对关键交付或高风险发布前内容执行 人工评审 #2。
7. 把发布准备状态写入关联 issue，给出 通过 或 阻塞 结论。

## 阶段最小产物集合

- 一份 QA Case 或覆盖映射
- 一份已确认的 QA Case Design 或覆盖映射
- 一份 QA 测试报告
- 一份 QA 结论评论
- 必要时的一份 人工评审 #2 结论

## 退出条件

- 测试报告已存在
- 阻塞项 已明确
- 残留风险已明确
- 发布建议已清晰

## 必需签字

- QA：必需
- PM：确认验收范围时必需

## 人工评审规则

- 关键交付、高风险改动或用户要求确认的交付物，必须执行 人工评审 #2。
- 人工评审 #2 未完成时，不得进入 发布评审 或 Issue 完成状态。

## 回退规则

- 阻塞项 defects：回到 实现阶段
- 可测试性或覆盖映射缺失：回到 tech 评审
- 验收标准变化：回到 PRD 评审
- 若 人工评审 #2 退回：回到 实现阶段 或 tech 评审，取决于退回原因
