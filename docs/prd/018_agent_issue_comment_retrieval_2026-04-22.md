---
name: Agent 获取 Issue Comment 统一规范
description: 统一 AgentDevFlow 中 Agent 获取 Issue Comment 的标准方式、责任边界与统一接口，消除多次试错问题
status: Draft
owner: Product Manager
date: 2026-04-22
update_date: 2026-04-22
issue: "#18"
---

# PRD #018 — Agent 获取 Issue Comment 统一规范

## 1. 背景

Issue #18 指向的核心问题是：AgentDevFlow 中的 Agent 在获取 GitHub Issue Comment 时缺乏统一规范，导致多次试错、命令失败、状态混乱。例如在 #3 的 HR#1 环节中，Agent 连续尝试了 `gh api`、`gh issue view`、`gh issue view --json comments` 等多种方式，均未成功获取 comment 内容，最终需要 Human 介入。

## 2. 问题

当前存在以下直接问题：

- **Agent 获取 comment 方式不统一**：不同 Agent 使用不同命令组合，缺乏统一标准
- **试错成本高**：Agent 会连续尝试多种方式，每次失败都产生新的 bash 调用和错误输出
- **错误恢复不清晰**：当一种方式失败后，Agent 不知道应该 fallback 到什么方式
- **脚本封装不足**：已有的 `github_issue_sync.py` 提供评论功能，但 Agent skill 中未明确指导如何使用

## 3. 目标

形成当前有效的产品层需求定义，明确：

1. Agent 获取 issue comment 必须有统一标准方式
2. 统一方式必须在 prompts/skill 中显式声明
3. 当统一方式不可用时，必须有明确的 fallback 路径
4. 避免 Agent 自行探索多种命令组合

## 4. 范围

### 4.1 统一获取方式定义

- 明确 Agent 获取 issue comment 的首选方式
- 明确命令参数、输出格式、错误处理
- 明确何时使用脚本、何时使用 raw gh 命令

### 4.2 Prompt / Skill 更新范围

- 在相关角色的 SKILL.md 中补充 issue comment 获取规范
- 在 workflow 文档中明确 issue comment 获取步骤
- 确保所有角色使用同一套获取方式

### 4.3 Fallback 机制

- 当首选方式失败时，明确 fallback 路径
- 避免无限试错循环
- 明确何时应该停止尝试并上报 blocker

## 5. 非目标

- 不在本 PRD 中直接修改 `github_issue_sync.py` 脚本
- 不扩展到 issue 创建、关闭等其他操作
- 不把历史试错记录直接作为当前有效交付物

## 6. 用户故事

### US-1：Agent 执行者
> 作为 AgentDevFlow 中的 Agent，我希望明确知道获取 issue comment 的标准方式，这样就不会浪费时间在多次试错上。

### US-2：流程设计者
> 作为流程设计者，我希望所有 Agent 使用统一的 issue comment 获取方式，这样可以减少执行差异和错误恢复成本。

## 7. 验收标准

- [ ] Agent 获取 issue comment 的统一方式已在 prompts/skill 中声明
- [ ] 统一方式包含明确的命令、参数和预期输出格式
- [ ] 已定义当统一方式失败时的 fallback 路径
- [ ] 已明确避免 Agent 自行探索多种命令组合
- [ ] 相关角色 SKILL 中已补充 issue comment 获取规范
- [ ] 本 issue 已按严格研发交付流程重新进入 Gate 1，而非直接复用历史试错记录

## 8. 风险

| 风险 | 影响 | 缓解 |
|------|------|------|
| 统一方式在某些场景下不可用 | 高 | 明确 fallback 路径和终止条件 |
| 不同角色对统一方式理解不一致 | 中 | 在 SKILL 中统一写法，避免歧义 |
| 统一方式随 gh CLI 版本变化失效 | 低 | 定期验证统一方式可用性 |

## 9. 依赖

- Issue #18 当前讨论上下文
- 当前有效 `github_issue_sync.py` 脚本功能
- 当前有效角色 SKILL 文档

## 10. 评审记录

| 日期 | 评审人 | 备注 | 决策 |
|---|---|---|---|
| 2026-04-22 | PM | 按严格研发交付流程重新启动 #18，起草当前有效 PRD | Draft |
