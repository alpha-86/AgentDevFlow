# 周度复盘 Workflow

## 目标

复盘周度交付健康度、流程合规情况和重复 blocker。

## 输入

- 所有活跃 issues
- 本周 gate 结果
- todo 老化报告
- blocker 和升级记录

## 步骤

1. Team Lead 汇总本周 issue 流转和 gate 结果。
2. PM 和 Tech Lead 评估范围漂移和重审事件。
3. QA 评估 defect 趋势和残留风险模式。
4. Platform/SRE 评估发布稳定性和 rollback 事件。
5. 团队把纠正动作写入 memo 和 todo registry。

## 复盘检查清单

- 是否发生 gate 绕过
- 是否存在 major / breaking 变更未重审
- 超过一个工作日的 blocked todo 是否已升级
- 重复 blocker 是否已有 owner 和修复计划

## 输出

- 周度复盘 memo
- 优先级明确的流程改进动作
- 更新后的 owner 和 due date
