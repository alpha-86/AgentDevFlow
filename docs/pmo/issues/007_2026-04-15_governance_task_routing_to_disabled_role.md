# PMO-2026-04-15-GOV-003 — Task Router 路由到未启用的角色

## 基本信息

| 字段 | 内容 |
|------|------|
| 级别 | P1 / Warning |
| 日期 | 2026-04-15 |
| 类别 | governance |
| 状态 | Open |

## 问题描述

Issue #3 的任务被路由到 `Engineer`，但 Engineer 在 TODO_REGISTRY 中状态为 "暂未启用"（职责由 Team Lead 临时承担）。Task Router 未检查角色启用状态，导致路由目标实际不存在。

## 影响范围

- 路由任务落空，任务无人接收
- 团队成员不清楚实际负责人
- 可能在其他未启用角色上同样存在问题

## 根因分析

Task Router (`scripts/task_router.py`) 在路由时未校验目标角色的当前启用状态。

## 纠正动作

| 动作 | 负责人 | 截止时间 | 状态 |
|------|--------|----------|------|
| Task Router 增加角色启用状态校验，跳过未启用角色 | Team Lead | 下次启动前 | Pending |

## 机制改进建议

在 `scripts/task_router.py` 中：
1. 读取 `docs/todo/TODO_REGISTRY.md` 获取角色启用状态
2. 仅路由到状态为"已创建"的 Agent
3. 对 "暂未启用" 的角色，路由到临时承担者（Team Lead）

## 状态

- [ ] 问题已记录
- [ ] Task Router 改进
- [ ] 验证路由逻辑
