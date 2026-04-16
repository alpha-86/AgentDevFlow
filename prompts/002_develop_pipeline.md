# 开发交付流程（Develop Pipeline）

## 目标

定义 AgentDevFlow 的完整开发交付流程，基于 README 流程图（第 73-125 行），作为所有 Agent 的核心必读流程文档。

本文档与 `004_delivery_gates.md`（Gate 合规检查定义）、`017_human_review_and_signoff.md`（Human Review 规范）配套使用。

## 流程概览

```
需求 / 问题 / 异常
        │
        ▼
创建主 GitHub Issue
        │
        ▼
Gate 0: Team Startup — 团队初始化
        │
        ▼
Gate 1: PRD Review — 需求评审
        │
        ▼
Gate 2: Tech Review — 技术评审
        │
        ▼
Human Review #1 — 设计确认评审
        │
        ▼
文档 PR 合并 = 设计确认 ✅
        │
        ▼
Gate 3: Implementation — 开发实现
        │
        ▼
Gate 4: QA Validation — 质量验证
        │
        ▼
代码 PR + Human Review #2 — 实现确认评审
        │
        ▼
代码 PR 合并 = 实现确认 ✅
        │
        ▼
Gate 5: Release / Issue Close — 发布 / 关闭
```

## 关键原则

- 无 Issue 不进入正式交付流程
- 无 PRD Review 不进入 Tech Review
- 无 Human Review #1 不进入 Implementation
- 文档 PR 合并 = 设计确认
- 代码 PR 合并 = 实现确认
- **PR 合并是 Human 专属操作**，Agent 只负责推动流程，不执行合并
- **Issue 关闭是 Human 专属操作**，Agent 只负责发布关闭请求评论
- Human Review 结论未正式落地，不视为通过

---

## Gate 0: Team Startup — 团队初始化

### 触发条件

- 新 Issue 创建后，Team Lead 分配角色

### 进入条件

- 主 Issue 已创建且问题描述明确
- 角色已分配（PM、Architect、QA 等）
- 团队成员已了解需求背景

### 角色职责矩阵

| 角色 | 职责 |
|------|------|
| Team Lead | 主持启动、分配角色、确认优先级、确认并行可行性 |
| PM | 确认需求来源、澄清问题边界、确认交付范围 |
| Architect | 确认技术范围、识别技术风险和依赖 |
| QA | 确认验收路径、识别测试需求 |
| Engineer | 待命，准备接收已确认的设计输入 |
| PMO | 记录启动状态、检查 Issue 命名规范、检查流程合规性 |

### 输出物

- Issue 状态设为对应阶段
- 角色分配确认
- 项目组合视图更新

### 下一动作

- Team Lead 通知 PM 开始问题澄清
- PM 开始起草 PRD

### 回退条件

- Issue 描述模糊 → 退回 PM 补充问题描述
- 角色分配冲突 → Team Lead 协调

---

## Gate 1: PRD Review — 需求评审

### 进入条件

- PRD 文档已起草（`docs/prd/`）
- PRD 包含：问题、目标、非目标、范围边界、可测试验收标准
- PM 认为可进入评审

### 角色职责矩阵

| 角色 | 职责 |
|------|------|
| Team Lead | 主持评审、确认流转、判断是否需要重审 |
| PM | 主持评审、记录结论、PRD 签字 |
| Architect | 评审技术可行性、识别技术风险 |
| QA | 评审验收标准完整性、确认测试覆盖路径 |

### 签字要求

- **PM（必签）**：需求口径确认
- **Architect（必签）**：技术可行性确认
- **QA（确认）**：验收标准可测试性确认

### 输出物

- PRD 状态更新为 `Approved`
- Issue Comment 包含：Gate 1 结论、签字人、日期、PRD 链接
- 变更记录（如有）

### 通过标准

PM + Architect + QA 三方签字完成，Issue Comment 已落地。

### Human 专属操作

无（文档评审 Agent 可完成）

### 下一动作

- 通过 → PM 通知 Architect 开始 Tech Spec；QA 开始 QA Case Design
- 不通过 → 退回 PM 修订，Issue 状态保持 `in_prd`

### 回退条件

- PRD 缺少范围/非目标/验收标准 → 退回 PM 修订
- 评审结论为 `Rejected` → 修订后重新评审

---

## Gate 2: Tech Review — 技术评审

### 进入条件

- PRD `Approved`（Gate 1 通过）
- Tech Spec 文档已起草（`docs/tech/`）
- QA Case Design 已起草（`docs/qa/`）

### 角色职责矩阵

| 角色 | 职责 |
|------|------|
| Team Lead | 主持评审、确认流转 |
| PM | 评审 PRD 覆盖完整性、Tech 满足需求、确认签字 |
| Architect | 主持评审、Tech Spec 签字、识别风险和依赖 |
| QA | 评审 QA Case 覆盖 Tech Spec、风险和回滚路径、QA 签字 |
| Engineer | 评审 Tech Spec 可实现性（纯文档交付场景可由 Architect 代理）|

### 签字要求

- **Architect（必签）**：技术方案确认
- **QA（必签）**：测试路径确认
- **PM（确认）**：需求覆盖确认

### 输出物

- Tech Spec 状态更新为 `Approved`
- QA Case Design 状态更新为 `Approved`
- Issue Comment 包含：Gate 2 结论、三方签字、日期、文档链接

### 通过标准

Architect + QA + PM 三方签字完成，Issue Comment 已落地。

### Human 专属操作

无（文档评审 Agent 可完成）

### 下一动作

- 通过 → PM 发起 Human Review #1
- 不通过 → 退回修订

### 回退条件

- Tech 未完整覆盖 PRD → 退回 Architect 修订
- QA Case 未覆盖关键路径 → 退回 QA 修订
- PRD 发生 Major/Breaking 变更 → 回到 Gate 1 重新评审

---

## Human Review #1 — 设计确认评审

### 进入条件

- PRD `Approved`（Gate 1）
- Tech Spec `Approved`（Gate 2）
- QA Case Design `Approved`（Gate 2）
- 所有 Gate 签字已落地

### 角色职责矩阵

| 角色 | 职责 |
|------|------|
| PM | 发起 Human Review #1、整理评审材料、记录结论、协调修订 |
| Architect | 评审设计文档、出具独立评审意见、签字 |
| QA | 评审测试设计、出具独立评审意见、签字 |
| Team Lead | 确认评审完成、推动 Human 合并文档 PR |

### 评审形式

文档 Review / Issue Comment Confirm / PR Review

### 通过标准

- Architect 评审意见已落地（Approved/Conditional/Rejected）
- QA 评审意见已落地（Approved/Conditional/Rejected）
- PM 发布 HR#1 结论总结

### Human 专属操作

无（文档评审 Agent 可完成，但 PR 合并是 Human 专属）

### PM 发布 HR#1 通过评论后的下一动作（关键）

```
PM 发布 HR#1 通过评论
        │
        ▼
PM 通知 Team Lead：文档 PR 可以合并（HR#1 已通过）
        │
        ▼
Team Lead 推动 Human 执行文档 PR 合并
        │
        ▼
Human 执行 PR 合并（PR 合并是 Human 专属操作）
        │
        ▼
Human 合并完成后，Human 通知 Engineer 开始实现
        │
        ▼
Engineer 收到通知，开始 Implementation
```

**PM 的职责到此结束（文档阶段交付完整）**，后续是 Human 和 Engineer 的工作。

### 下一动作

- 通过 → Human 执行文档 PR 合并（PR 合并 = 设计确认）
- Conditional → 完成条件项后重新评审
- 不通过 → 退回修订

### 回退条件

- 文档质量不满足评审标准 → 退回修订
- 发现新的技术风险 → 回到 Gate 2 重新评审

---

## 文档 PR 合并 = 设计确认 ✅

文档 PR 合并后，设计正式确认，进入实现阶段。

### Human 专属操作

- **文档 PR 合并**（Human 执行，Agent 不执行）

### 下一动作

Human 合并文档 PR 后，通知 Engineer 开始实现。

---

## Gate 3: Implementation — 开发实现

### 进入条件

- 文档 PR 已合并（设计确认）
- Human Review #1 已通过
- Engineer 收到 Human 的实现通知

### 角色职责矩阵

| 角色 | 职责 |
|------|------|
| Engineer | 基于已确认的 PRD + Tech Spec 实现、编写单元测试、同步实现文档 |
| Architect | 确认实现符合 Tech Spec、技术一致性确认 |
| PM | 跟踪进度、澄清需求细节 |
| QA | 跟踪进度、准备 QA 验证 |
| Team Lead | 跟踪进度、协调阻塞、确认 QA 验证时机 |

### 输出物

- 代码变更
- 单元测试
- 实现说明
- Issue Comment 包含：实现进度、阻塞项（如有）

### 通过标准

代码实现完成、单元测试通过、实现文档同步、通知 QA 开始验证。

### Human 专属操作

无（实现工作由 Agent 完成）

### 下一动作

- 实现完成 → Engineer 通知 QA 开始验证
- 遇到文档缺失/冲突 → 回退到评审环节

### 回退条件

- 实现与 Tech Spec 严重偏离 → 退回 Engineer 修订
- 上游文档发生变更 → 回到 Gate 2 重新评审

---

## Gate 4: QA Validation — 质量验证

### 进入条件

- Engineer 通知 QA 验证
- 实现证据完整（代码、单测、实现说明）
- QA Case Design 已确认

### 角色职责矩阵

| 角色 | 职责 |
|------|------|
| QA | 执行测试、记录结果、报告缺陷、出具验收意见 |
| Engineer | 修复缺陷、响应 QA 反馈 |
| PM | 确认验收口径 |
| Team Lead | 跟踪质量结论、确认是否具备 Human Review #2 条件 |

### 输出物

- QA 测试报告（`docs/qa/`）
- 缺陷清单（如有）
- 质量结论（Approved/Conditional/Rejected）

### 通过标准

- 所有关键测试用例通过
- 无阻塞性缺陷（或阻塞缺陷有明确例外批准）
- QA 发布质量结论

### Human 专属操作

无（QA 验证 Agent 可完成，但最终结论由 Human 确认）

### 下一动作

- 通过 → 确认是否需要代码 PR（纯文档交付跳过）
- 不通过 → Engineer 修复 → QA 重新验证

### 回退条件

- 发现阻塞性缺陷 → 退回 Engineer 修复 → 回到 QA 验证

---

## Human Review #2 — 实现确认评审

### 进入条件

- QA 测试报告已完成
- 代码 PR 已创建（如有代码交付）
- 测试报告和代码 PR 链接已回链 Issue

### 角色职责矩阵

| 角色 | 职责 |
|------|------|
| PM | 评审实现满足 PRD 验收标准、出具意见、确认签字 |
| Architect | 评审代码与 Tech Spec 一致性、出具意见、确认签字 |
| QA | 评审 QA 报告完整性、出具意见、确认签字 |
| Team Lead | 确认评审完成、推动 Human 合并代码 PR |

### 通过标准

PM + Architect + QA 三方签字完成，Issue Comment 已落地。

### Human 专属操作

- **代码 PR 合并**（Human 执行，Agent 不执行）

### 下一动作

- 通过 → Human 执行代码 PR 合并（PR 合并 = 实现确认）
- Conditional → 完成条件项
- 不通过 → 退回 Engineer 修复

---

## 代码 PR 合并 = 实现确认 ✅

代码 PR 合并后，实现正式确认。

### Human 专属操作

- **代码 PR 合并**（Human 执行，Agent 不执行）

### 下一动作

Human 合并代码 PR 后，确认是否可以关闭 Issue 或进入 Release。

---

## Gate 5: Release / Issue Close — 发布 / 关闭

### 进入条件

- 实现确认完成（Human Review #2 通过，或纯文档交付场景下 Human Review #1 通过）
- 所有关键产物已回链 Issue
- 无未关闭的阻塞性缺陷

### 角色职责矩阵

| 角色 | 职责 |
|------|------|
| Team Lead | 确认发布准备、主持发布评审 |
| PM | 确认业务放行、验收签字 |
| Architect | 确认技术放行 |
| Platform/SRE | 确认部署准备、回滚方案、监控值守 |
| QA | 确认测试覆盖、缺陷已处理 |
| PMO | 审计流程完整性 |

### 输出物

- 发布记录（`docs/release/`）
- 回滚方案
- 值守安排
- Issue Comment 包含：发布结论、参与者、日期

### 通过标准

PM + Architect + Platform/SRE 三方放行。

### Human 专属操作

- **Issue 关闭**（Human 执行，Agent 发布"关闭请求"评论）

### 下一动作

- Human 发布 Release 记录
- Human 关闭 Issue（或通知 Team Lead 代为操作）

### 回退条件

- 发布风险未明确 → 回到 QA 验证
- 回滚方案缺失 → 补充回滚方案

---

## 角色职责矩阵总览

| 节点 | Team Lead | PM | Architect | QA | Engineer | Platform/SRE | PMO |
|------|-----------|-----|-----------|-----|----------|-------------|-----|
| Gate 0: Startup | 主持/分配 | 确认来源 | 确认范围 | 确认路径 | 待命 | 确认环境 | 记录 |
| Gate 1: PRD Review | 主持/流转 | 主持/签字 | 评审可行性 | 评审完整性 | — | — | 审计 |
| Gate 2: Tech Review | 主持/流转 | 确认覆盖 | 主持/签字 | 评审路径/签字 | 评审可实现性 | — | 审计 |
| HR#1 | 推动合并 | 发起/整理 | 评审/签字 | 评审/签字 | — | — | 审计 |
| **文档PR合并** | **—** | **通知TL** | **—** | **—** | **—** | **—** | **—** |
| Gate 3: Impl | 跟踪 | 跟踪 | 确认一致性 | 跟踪 | **实现** | — | 审计 |
| Gate 4: QA | 跟踪 | 确认口径 | — | **验证/报告** | 修复 | — | 审计 |
| HR#2 | 推动合并 | 评审/签字 | 评审/签字 | 评审/签字 | — | — | 审计 |
| **代码PR合并** | **—** | **—** | **—** | **—** | **—** | **—** | **—** |
| Gate 5: Release | 主持/确认 | 业务放行 | 技术放行 | 测试覆盖 | — | **部署/回滚** | 审计 |

> **注**：表格中 **加粗** 为该节点的核心执行角色，**—** 为不参与，**文档PR合并** 和 **代码PR合并** 为 Human 专属操作。

---

## Human 专属操作清单

以下操作是 Human 的专属权限，Agent 不得执行：

| 操作 | 理由 |
|------|------|
| **文档 PR 合并** | 设计正式确认，代表团队决策 |
| **代码 PR 合并** | 实现正式确认，代表交付完成 |
| **Issue 关闭** | 交付验收确认，代表流程闭环 |
| **Human Review 正式签字** | 人工判断，必须由人做出 |
| **例外审批** | 流程豁免，必须由人批准 |

Agent 在这些操作完成后的正确行为：发布通知评论，推动 Human 执行，而不是替代 Human 操作。

---

## 完成标准矩阵

每个角色在每个 Gate 的"完成标准"：

| 角色 | Gate | 完成标准 |
|------|------|---------|
| PM | Gate 0 | Issue 已创建、角色已分配 |
| PM | Gate 1 | PRD 起草完成、Gate 1 三方签字完成、Issue Comment 落地 |
| PM | Gate 2 | 确认 Tech + QA Case 覆盖 PRD、Gate 2 三方签字完成 |
| PM | HR#1 | HR#1 评审意见已落地、发布结论评论、**通知 Team Lead 合并** |
| PM | Gate 3-4 | 跟踪进度、确认口径（不执行实现/验证）|
| PM | Gate 5 | 业务放行签字 |
| PM | **Issue Close** | **发布"Issue 关闭请求"评论，不自行关闭** |
| Architect | Gate 1 | 评审技术可行性、签字 |
| Architect | Gate 2 | Tech Spec 起草完成、签字 |
| Architect | HR#1/2 | 独立评审意见、签字 |
| Architect | Gate 3 | 确认实现与 Tech 一致性 |
| Architect | Gate 5 | 技术放行签字 |
| QA | Gate 1 | 评审验收标准完整性、签字 |
| QA | Gate 2 | QA Case Design 起草完成、签字 |
| QA | HR#1/2 | 独立评审意见、签字 |
| QA | Gate 4 | 测试执行完成、报告已发布、质量结论已落地 |
| Engineer | Gate 3 | 代码实现完成、单元测试通过、实现文档同步、通知 QA |
| Engineer | Gate 4 | 缺陷修复、响应 QA 反馈 |
| Platform/SRE | Gate 5 | 发布准备清单完成、回滚方案确认、值守安排确认 |
| Team Lead | 全流程 | 主持评审、确认流转、推动 Human 合并、推动升级 |
| PMO | 全流程 | 记录问题、推动纠正、审计合规性 |

---

## 流程异常处理

### 回退规则

| 场景 | 回退到 |
|------|--------|
| PRD 缺少必要项 | Gate 1 → 退回 PM 修订 |
| Tech 未覆盖 PRD | Gate 2 → 退回 Architect 修订 |
| PRD 发生 Major/Breaking 变更 | Gate 1 → 重新评审 |
| Tech 发生 Major/Breaking 变更 | Gate 2 → 重新评审 |
| HR#1 未通过 | HR#1 → 修订后重新评审 |
| 实现与 Tech 严重偏离 | Gate 3 → 退回 Engineer 修订 |
| QA 发现阻塞性缺陷 | Gate 4 → 退回 Engineer 修复 |
| 发布风险未明确 | Gate 5 → 回到 Gate 4 |

### 升级规则

- 评审超时 → Team Lead 升级
- 范围冲突 → PM 定口径
- 技术不可行 → Architect 退回
- 质量阻塞 → QA 持有 gate
- 发布风险 → Platform/SRE 提出阻塞意见
- 流程违规 → PMO 记录并推动纠正
