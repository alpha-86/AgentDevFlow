# PMO-2026-04-15-PROC-001 — PM 自行决定并行 Issue 处理顺序

## 基本信息

| 字段 | 内容 |
|------|------|
| 级别 | P1 / Warning |
| 日期 | 2026-04-15 |
| 类别 | process |
| 状态 | Open |

## 问题描述

Issue #3 和 Issue #5 同时处于活跃状态，PM 在 Gate 1 通过后自行选择先推进 Issue #5，Issue #3 被搁置。直到 Team Lead 追问才汇报 Issue #3 进展。PM 未主动向 Team Lead 确认并行 Issue 的优先级顺序。

## 规则确立

1. 当存在并行多 Issue 同时推进时，需 Human（Team Lead）确认任务优先级，不得由 Agent 自行决定任务顺序
2. 默认规则：issue 编号更小 = 更高优先级（如 Issue #3 < Issue #5，#3 先）
3. Agent 不得在无确认情况下自行决定多 Issue 间的处理顺序

## 纠正动作

| 动作 | 负责人 | 状态 |
|------|--------|------|
| PM 在发现多 Issue 并行时，主动向 Team Lead 确认优先级顺序 | PM | 已传达 |

## 机制改进建议

在 `prompts/002_product_engineering_roles.md` 或 `005_meeting_and_todo.md` 中补充多 Issue 并行处理规则。
