---
name: adf-workflows
description: 在技术设计开始前，批准或退回 PRD。
user-invocable: true
---

# PRD 评审 工作流

## 目标

在技术设计开始前，批准或退回 PRD。

## 必需追溯字段

- 关联 issue id
- PRD 文档 id 和状态
- 评审 纪要 链接
- todo registry 中的 行动项

## 输入

- 当前需求描述
- PRD 草稿
- 已知约束或依赖
- 关联 issue 记录
- 必要时的 人工评审 安排

## 推荐模板与输出目录

- PRD：`.claude/skills/adf-templates/prd-template.md`
- 评审评论：`.claude/skills/adf-templates/review-comment-template.md`
- Memo：`.claude/skills/adf-templates/memo-template.md`
- 推荐输出目录：`docs/prd/`、`docs/memo/`

## 步骤

1. PM 准备 PRD 和验收标准。
2. 技术负责人 评估可行性、依赖和风险。
3. 必要时由领域 reviewer 验证业务匹配。
4. PM 和 技术负责人 在 PRD 评审 record 中记录签字结论。
5. 若本次 PRD 属于关键需求或高风险需求，执行 人工评审。
6. 在 纪要 和关联 Issue 评论 中记录 评审 结论。
7. 把 行动项 写入 todo 跟踪，并补充 负责人 和 到期日。

## 阶段最小产物集合

- 一份 PRD 文档
- 一份 评审 结论
- 必要时的一份 人工评审 结论
- 一份 纪要 或等价纪要

## 评审检查清单

- 范围是否明确
- 非目标是否明确
- 验收标准是否可测试
- 依赖是否已识别
- 未解决风险是否可见

## 必需签字

- PM：必需
- 技术负责人：必需

## 人工评审规则

- 高风险或关键需求的 PRD，必须进入 人工评审。
- 人工评审 未完成时，不得进入 技术评审。
- 人工评审 结论必须写回 Issue 评论 或 评审 record。

## 结果

- 通过
- conditionally 通过
- 退回并附返工项

## 回退规则

- conditionally 通过：所有条件关闭并补齐证据后，才能进入 tech 评审
- 退回：PRD 必须修订后重新 评审
- 阻塞：升级给 团队负责人，并把 issue 状态保持为 `阻塞`
- 若 人工评审 退回：PRD 必须修订后重新执行当前阶段 评审

