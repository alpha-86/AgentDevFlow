# PMO-2026-04-15-RB-001 — Team Lead 深度介入具体 Issue 跟踪

## 基本信息

| 字段 | 内容 |
|------|------|
| 级别 | P1 / Warning |
| 日期 | 2026-04-15 |
| 类别 | role-boundary |
| 状态 | Open（重复发生） |

## 问题描述

Team Lead 在本次启动中亲自跟进特定 Agent 的进展（如询问 product-manager 初始化状态、architect tech spec 进展等），而非仅在更高层面把控节奏和 blocker 升级。违反 Team Lead "负责团队节奏、跨角色协调、流程守门"的职责定义。

## 重复发生记录

### 发生 #2（2026-04-15，同日）

**触发**：Team Lead 直接处理具体问题——确认 PRD #003 v2 是否需要重新 Gate 1，而非将任务路由给相应角色（PM 或 Architect）。

**规则重申**：Team Lead 的首要职责是**路由/分发任务**，遇到具体问题应路由给对应 Agent，不应直接回答。

**PMO 判断**：这是 RB-001 的第二次发生。Team Lead 仍需学习："遇到具体问题 → 路由给对应 Agent，而不是直接回答"。

## 影响范围

Team Lead 角色边界模糊，可能压缩其他角色的自主决策空间，长期导致 Agent 习惯性等待 Team Lead 确认而非自主负责。

## 纠正动作

| 动作 | 负责人 | 截止时间 |
|------|--------|----------|
| Team Lead 明确"跟进进展"与"协调节奏"的边界：只处理跨角色 blocker，不跟进单角色内部状态 | Team Lead | 下次启动节点 |

## 机制改进建议

在 `prompts/001_team_topology.md` 或 `002_product_engineering_roles.md` 中明确 Team Lead 的"跟进"范围（仅限 blocker 和 gate 状态，不含单角色进度询问）。
