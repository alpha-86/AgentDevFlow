---
name: Prompts 描述规范 — pattern + 枚举原则
description: 禁止 prompts 中仅使用单一 pattern 式描述，要求采用"pattern + 枚举"组合方式，作为 Issue #21 的当前有效 Gate 1 输入
status: Draft
owner: Product Manager
date: 2026-04-22
update_date: 2026-04-22
issue: "#21"
---

# PRD #021 — Prompts 描述规范：pattern + 枚举原则

## 1. 背景

Issue #21 指向的核心问题是：AgentDevFlow 中 prompts 存在大量单一 pattern 式描述（如"读取你的 skill 文件：`.claude/skills/adf-{role}/SKILL.md`"），缺乏枚举式具体映射内容，导致 Agent 在实际执行时无法准确理解具体映射关系。

## 2. 问题

当前存在以下直接问题：

- **仅有 pattern 式描述**：如"读取 `.claude/skills/adf-{role}/SKILL.md`"，但下面没有枚举每个 role 对应的具体文件
- **Agent 理解歧义**：Agent 无法从 pattern 中准确推断所有具体映射
- **缺乏具体映射内容**：没有表格或其他枚举形式列出每个 agent 及其对应 skill 文件

## 3. 目标

形成当前有效的产品层需求定义，明确：

1. prompts 中禁止仅使用单一 pattern 式描述
2. 必须采用"pattern + 枚举"组合方式
3. pattern 作为说明，下方必须放枚举式具体映射内容
4. 该规范需要在 CLAUDE.md 中沉淀，并落实到所有 skills

## 4. 范围

### 4.1 原则定义

- 在 CLAUDE.md 中沉淀"pattern + 枚举"原则
- 明确 pattern 式描述与枚举式描述的组合要求
- 明确枚举形式（表格、列表等）

### 4.2 Skill 文件更新范围

- 修改所有 skills 中仅使用单一 pattern 式描述的地方
- 补充枚举式具体映射内容
- 确保所有 skill 调用、文档引用都遵循该规范

### 4.3 验证方式

- 定义如何验证 skill 文件是否符合该规范
- 定义检查清单或自动化验证方式

## 5. 非目标

- 不在本 PRD 中直接修改所有 skill 文件
- 不扩展到与描述规范无关的其他流程改造
- 不把历史讨论直接作为当前有效交付物

## 6. 用户故事

### US-1：Agent 执行者
> 作为 Agent，我希望 prompts 中不仅有 pattern 说明，还有具体枚举，这样我就能准确知道每个角色对应的具体文件和路径。

### US-2：流程设计者
> 作为流程设计者，我希望所有 prompts 的描述方式统一，减少 Agent 执行时的歧义和试错。

## 7. 验收标准

- [ ] CLAUDE.md 中已沉淀"pattern + 枚举"原则
- [ ] 所有 skills 中已消除仅使用单一 pattern 式描述的情况
- [ ] 每个 pattern 下方都有枚举式具体映射内容
- [ ] 已定义验证方式，可检查 skill 文件是否符合规范
- [ ] 本 issue 已按严格研发交付流程重新进入 Gate 1

## 8. 风险

| 风险 | 影响 | 缓解 |
|------|------|------|
| 规范过于严格导致维护成本上升 | 中 | 明确最小合规标准，不过度要求 |
| 枚举内容随项目变化需要频繁更新 | 中 | 建立枚举内容的同步机制 |
| Agent 仍无法正确理解枚举内容 | 低 | 采用表格等结构化形式提高可读性 |

## 9. 依赖

- Issue #21 当前讨论上下文
- 当前有效 CLAUDE.md
- 当前有效所有 skills 文件

## 10. 评审记录

| 日期 | 评审人 | 备注 | 决策 |
|---|---|---|---|
| 2026-04-22 | PM | 按严格研发交付流程重新启动 #21，起草当前有效 PRD | Draft |
