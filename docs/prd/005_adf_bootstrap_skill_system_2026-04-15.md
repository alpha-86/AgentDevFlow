---
name: ADF Bootstrap Skill System Enhancement
description: 完善 ADF 技能系统、文档与自动化流程，使 AgentDevFlow 作为多 Agent 协作框架具备完整的使用指南、自动化保障和角色协作接口
status: Approved
owner: Product Manager
date: 2026-04-15
update_date: 2026-04-15
issue: "#5"
---

# PRD #005 — AgentDevFlow Bootstrap: 完善 ADF 技能系统、文档与自动化流程

## 1. 背景

AgentDevFlow 项目已完成核心流程机制（Issue/Gate/PR/Human Review）的建立，并通过 bootstrap-sync 脚本将 `skills/shared/` 中的 skill 源文件同步到 `.claude/skills/` 下的 adf-prefixed 产物目录。但作为面向多 Agent 协作交付的可复用框架，当前存在四个系统性缺口：

1. **ADF 技能系统不完整**：bootstrap-sync 脚本有实现，但缺少面向用户的同步机制文档（映射表、安装前置、故障排查）
2. **文档与规范不完整**：现有 docs/ 目录以示例文件为主，缺少面向真实用户的接入指南和使用手册
3. **自动化流程不完整**：CI/CD 工作流缺少状态检查、错误处理和告警机制
4. **Agent 角色定义不够精细**：角色 prompt 与 skill 能力之间的配合关系、角色间协作接口缺少显式说明

这些缺口影响 AgentDevFlow 作为可复用框架的可信度和易用性，阻碍新用户接入和跨项目复用。

## 2. 问题

当前 AgentDevFlow 项目缺少系统性的"用户接入指南"，导致：

- **接入门槛高**：新用户或新项目无法快速理解如何使用 ADF 技能系统
- **维护不确定性**：开发者修改 `skills/shared/` 时不清楚哪些文件会被 bootstrap-sync 同步、如何验证同步结果
- **角色协作模糊**：各角色 Agent 的 prompt 约束与 skill 能力边界不够清晰，影响多 Agent 协作的可靠性
- **自动化覆盖不足**：CI 工作流缺少对关键交付节点（Gate 状态、Issue 链路、Doc PR 完整性）的自动检查

## 3. 目标

在 AgentDevFlow 仓库自身建立完整、可验证、可复用的 ADF 技能系统文档和自动化流程，作为其他项目接入 AgentDevFlow 的参考实现。

## 4. 范围

### 4.1 bootstrap-sync 机制文档

补充以下文档，使 bootstrap-sync 对用户可理解、可维护：

- **同步映射表**：列出 `skills/shared/` 源文件与 `.claude/skills/adf-*/` 产物的完整对应关系
- **安装与前置指南**：说明 bootstrap-sync 的依赖环境、触发条件（push to main）、预期行为
- **故障排查指南**：说明常见失败模式（如 YAML frontmatter 解析失败、commit message 引号问题）及修复方法
- **验证方法**：说明如何验证产物与源文件一致性（hash 对比、diff 核对）

### 4.2 AgentDevFlow 接入使用指南

补充面向用户的文档，覆盖三个主要场景：

- **新建项目**：如何在新项目中使用 AgentDevFlow 技能系统（skill 安装、角色初始化、Issue 机制建立）
- **接入已有项目**：如何将 AgentDevFlow 接入已有 Claude Code 项目
- **启动多 Agent 协作团队**：如何使用 `adf-start-agent-team` 启动团队，包含角色分配、Gate 流转规则

### 4.3 Agent 角色能力边界文档

补充以下说明，使角色间协作接口清晰：

- 各角色（PM/Architect/QA/Engineer/Team Lead）的 prompt 约束与 skill 能力对应关系
- 角色间协作的最小接口（Issue 评论格式、Gate 留痕要求、PRD/Tech/QA 文档追溯链）
- 角色协作的常见失败模式与纠正机制

### 4.4 CI/CD 自动化增强

CI/CD 自动化增强包含两类工作：

1. **代码修改**：修复 `doc-pr-checks.yml` 中 Gate 检查逻辑的缺陷（P0-1、P0-2）
2. **文档补充**：为 CI 工作流补充配置说明

> **注意**：本节修改仅限于 `doc-pr-checks.yml` 的 Gate 签字检查逻辑。`bootstrap-sync.yml` 触发条件和 `bootstrap-sync.py` 脚本逻辑不在本次修改范围内。

#### 4.4.1 CI Gate 检查逻辑修复（P0，最高优先级）

**P0-1：Gate 守门失效**

当前 `doc-pr-checks.yml` 的 Gate 签字检查使用 grep keyword 匹配（如 `grep -i "PM" | grep -i "sign"`），存在两类问题：

- **假阳性**：Review Record 中任意包含 "PM" 或 "sign" 字样的行都会被匹配到，非正式签字（如备注、说明文字）也会通过
- **不完整**：仅检查 Review Record 行中是否包含关键字，无法验证签字的语义完整性（如缺少日期或签名字段）

**修复要求**：
- 签字检查应使用结构化模式（正则表达式）匹配 Review Record 表格行，验证角色名、日期、结论字段同时存在
- 检查结果必须 `exit 1`（不是 WARNING），真正阻断不合规 PR

**P0-2：Gate 角色口径分叉**

当前 CI 检查中的角色名与 Gate 文档（prompts/004_delivery_gates.md）存在不一致：

| Gate | Gate 文档要求 | CI 原检查 | 差异 |
|------|-------------|----------|------|
| Gate 1 | PM + 架构评审人 | PM + 架构 | 角色名不一致 |
| Gate 3 | PM + 架构评审人 + Engineer（三方） | PM + 架构评审人 + Engineer | 一致 |

> **C4 决策（2026-04-15）**：Gate 1 标准角色名统一为"架构评审人"（与 Gate 文档一致）。

**修复要求**：
- 统一 Gate 1 角色检查使用"架构评审人"作为标准角色名（与 Gate 文档一致）
- 确保 Gate 3 三方签字（PM + 架构评审人 + Engineer）检查逻辑正确

#### 4.4.2 CI/CD 配置说明文档

在 4.4.1 修复完成后，补充以下 CI 工作流的配置说明：

- **doc-pr-checks.yml**：正确的 Gate 签字检查逻辑（含正则模式说明）、友好错误输出格式
- **issue-poll.yml**：GitHub Issue 同步与路由触发条件
- **bootstrap-sync.yml**：skill 同步触发条件和预期行为

## 5. 非目标

- 不修改 `skills/shared/` 中的 skill 源文件内容本身
- 不实现新的 bootstrap-sync 功能（如增量同步、版本回滚）
- 不为非 GitHub 平台（Claude Code Web App 等）提供等价的 CI/CD 适配
- 不改变 AgentDevFlow 核心流程机制（Issue/Gate/PR/Human Review 语义不变）
- 不建立完整的 API 或 SDK
- 不修改 `bootstrap-sync.py` 脚本逻辑
- CI 修改仅限于 `doc-pr-checks.yml` 的 Gate 签字检查逻辑，不修改 `bootstrap-sync.yml` 触发条件

## 6. 用户故事

### US-1：项目接入者
> 作为新加入 AgentDevFlow 的开发者，我希望能快速理解 ADF 技能系统的使用方法，在 30 分钟内完成新项目的初始化接入。

### US-2：维护者
> 作为 AgentDevFlow 的维护者，我希望在修改 `skills/shared/` 后能清晰预见同步结果，并有自动化保障确保产物一致性。

### US-3：多 Agent 协作参与者
> 作为使用 AgentDevFlow 启动多 Agent 团队的用户，我希望各角色的能力边界和协作接口清晰，减少协作中的歧义和返工。

### US-4：CI 运营者
> 作为 CI 运营者，我希望 Gate 检查失败时能立即知道缺失的签字和修复方法，而不是收到晦懂的错误信息。

## 7. 验收标准

### 7.1 bootstrap-sync 机制文档

- [ ] 同步映射表存在，覆盖 `skills/shared/` 下所有被同步的源文件和 `.claude/skills/adf-*/` 下对应的产物文件
- [ ] 安装前置指南说明 bootstrap-sync.py 的依赖（Python 3.x）和触发条件（push to main）
- [ ] 故障排查指南覆盖至少 3 种已知失败模式（含 commit message YAML 解析失败的处理方法）
- [ ] 验证方法说明可通过 hash 对比确认产物与源文件一致性

### 7.2 接入使用指南

- [ ] 新建项目场景指南存在，包含 skill 安装、角色初始化、Issue 机制建立步骤
- [ ] 接入已有项目场景指南存在，包含最小配置清单和验证步骤
- [ ] 启动多 Agent 协作团队指南存在，包含 `adf-start-agent-team` 使用说明、角色分配规则、Gate 流转规则
- [ ] 三份指南的交叉引用完整（新建 → 接入 → 启动团队形成链路）

### 7.3 Agent 角色能力边界文档

- [ ] 6 个角色（PM/Architect/QA/Engineer/Team Lead/Platform-SRE）的 prompt 约束与 skill 能力映射关系已文档化
- [ ] 角色间协作最小接口已文档化（Issue 评论格式、Gate 留痕要求、文档追溯链）
- [ ] 角色协作常见失败模式不少于 3 个，已附纠正机制

### 7.4 CI/CD 自动化增强

#### 7.4.1 CI 检查逻辑修复（P0）

- [ ] **P0-1 修复**：doc-pr-checks.yml Gate 签字检查在缺签字时 `exit 1`（非 WARNING），真正阻断不合规 PR
- [ ] **P0-1 修复**：签字检查使用结构化正则模式，验证角色名 + 日期 + 结论字段同时存在于 Review Record 行中
- [ ] **P0-2 修复**：Gate 1 角色检查统一使用"架构评审人"作为标准角色名（C4 决策）
- [ ] **P0-2 修复**：Gate 3 QA Case Design 三方签字（PM + 架构评审人 + Engineer）检查逻辑正确

#### 7.4.2 CI/CD 配置说明文档

- [ ] doc-pr-checks.yml 的 Gate 签字检查逻辑有配置说明文档（含正则模式说明）
- [ ] CI 工作流在 Gate 缺失时输出友好错误（指出缺失的签字角色和修复方法）
- [ ] bootstrap-sync.yml 的触发条件和预期行为有配置说明
- [ ] CI 配置可通过文档说明在 30 分钟内完成等效部署

## 8. 风险

| 风险 | 影响 | 缓解 |
|------|------|------|
| bootstrap-sync 行为与文档描述不一致 | 高：用户按文档操作后同步失败 | 每次同步后自动验证产物 hash，文档与脚本同步更新 |
| CI 检查逻辑修复破坏现有通过的 doc PR | 高：修复上线后历史合规 PR 被误判 | 修复仅针对未来 PR，不对历史合并回溯 |
| 文档过度详细导致维护成本上升 | 中：文档与实现漂移 | 文档变更必须与对应代码变更在同一个 PR 中 |

## 9. 依赖

- `skills/shared/` 中的 skill 源文件结构和命名保持稳定
- bootstrap-sync.py 脚本逻辑不变（本 PRD 不修改脚本）
- docs/ 目录结构不变（本次补充在现有目录下创建文档）
- CI 工作流需修改 Gate 检查逻辑（4.4.1 P0 修复），但不影响 bootstrap-sync.yml 触发条件

## 10. 评审记录

| 日期 | 评审人 | 备注 | 决策 |
|---|---|---|---|
| 2026-04-15 | Team Lead | Problem Statement Approved | 通过 |
| 2026-04-15 | PM | PRD Draft v1 | 待评审 |
| 2026-04-15 | Architect | 预评估发现 2 个 P0 blockers | 已纳入 PRD（Section 4.4.1）|
| 2026-04-15 | Team Lead | Gate 1 Review | **Approved** ✅（备注：CI P0 修复明确为代码修改，非"配置不变"）|
| 2026-04-15 | PM | PRD 更新 — Section 4.4 重构，明确 P0 为代码修改 | v2 |
| 2026-04-15 | Team Lead | Gate 1 Review 复审 | **Approved** ✅ |
| 2026-04-15 | PM | PRD 状态更新 | v3 — Approved |
| 2026-04-15 | Architect / PM / QA / Team Lead | Tech Spec #5 Tech Review | **Approved** ✅ |
| 2026-04-15 | Team Lead | C4 决策：Gate 1 标准角色名统一为"架构评审人" | 已更新 Section 4.4.1 P0-2 + 验收标准 |
