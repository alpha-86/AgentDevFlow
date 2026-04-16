# PMO-2026-04-15-RB-002 — Architect 被分配代码实现任务

## 基本信息

| 字段 | 内容 |
|------|------|
| 级别 | P1 / Fail |
| 日期 | 2026-04-15 |
| 类别 | role-boundary |
| 状态 | Closed |

## 问题描述

Architect 在启动初期被直接分配了 P0 修复任务（doc-pr-checks.yml 代码变更），该任务属于 Engineer 职责范围。Architect 的正确职责是技术方案评审和技术门禁，而非编码实现。

## 影响范围

Architect 角色职责被扩大至实现层，双阶段交付机制中的代码阶段形同虚设。

## 纠正动作

| 动作 | 负责人 | 截止时间 |
|------|--------|----------|
| 将 doc-pr-checks.yml 修复重新分配给 Engineer | Team Lead | 已完成 |
| Architect 退回代码任务，重新聚焦 Tech Spec 评审 | Architect | 已完成 |

## 机制改进建议

在 `002_product_engineering_roles.md` 中增加 Architect 的"禁止行为"清单，明确 Architect 不做代码实现。
