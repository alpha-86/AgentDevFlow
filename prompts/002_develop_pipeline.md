# 开发交付流程（Develop Pipeline）

## 目标

定义 AgentDevFlow 的完整开发交付流程，基于 hedge-ai V2.0/V2.2 双 PR 机制，作为所有 Agent 的核心必读流程文档。

本文档与 `004_delivery_gates.md`（Gate 合规检查定义）、`017_human_review_and_signoff.md`（Human Review 规范）配套使用。

## 流程概览

```
Agent Team 启动
        │
        ▼
扫描所有 open GitHub Issues（Human 随时可能创建新 Issue）
        │
        ▼
PM 领取 Issue → 与 Human 讨论问题（必须 Comment 到 Issue）
        │
        ▼
Gate 1: PRD Review — 需求评审（PM + Architect + QA 三方签字）
        │
        ▼
Gate 2: Tech Review — 技术评审（PM + QA 两签）
        │
        ▼
QA Case Design（三方：PM + Architect + Engineer 签字）
        │
        ▼
文档 PR（doc-{issue} 分支）— Human Review #1
        │
        ▼
文档 PR 合并 = 设计确认 ✅
        │
        ▼
Gate 3: Implementation — 开发实现（feature-{issue} 分支）
        │
        ▼
Gate 4: QA Validation — 质量验证
        │
        ▼
代码 PR（feature-{issue} 分支）— Human Review #2
        │
        ▼
代码 PR 合并 = 实现确认 ✅
        │
        ▼
Gate 5: Release / Issue Close — 发布 / 关闭
```

### 流程图 B：需求变更与打回流程（异常处理）

```
任意节点被 Human 打回
        │
        ▼
回滚到被打回节点的编写阶段
        │
        ▼
修改文档（版本+1，如 v1.0 → v1.1）
        │
        ▼
从该节点开始重新走完整流程（正向流程）
        │
        ▼
继续后续节点直到通过

特殊场景：
• PRD 变更 → Tech Spec 需同步变更（版本+1）→ Case Design 需同步变更（版本+1）
• Tech Spec 重大变更 → 回到 Gate 1 重新评审 PRD
• 需求变更 = 回到 PRD 编写流程 → 按顺序重新走完整个流程
```

### 流程图 C：Agent Team 启动后 Issue 扫描与路由（多 Issue 并行视角）

```
Agent Team 启动
        │
        ▼
扫描所有 open GitHub Issues
        │
        ▼
┌─────────────────────────────────────────────────┐
│  对每个 Issue 根据当前状态继续对应流程节点：      │
│                                                   │
│  • Issue 处于 Gate 1 阶段  →  继续 PRD Review    │
│  • Issue 处于 Gate 2 阶段  →  继续 Tech Review   │
│  • Issue 处于 QA Case Design →  继续 Case 签字  │
│  • Issue 处于文档 PR 阶段  →  继续 HR#1          │
│  • Issue 处于 Implementation →  继续开发         │
│  • Issue 处于 Gate 4 QA   →  继续 QA 验证       │
│  • Issue 处于代码 PR 阶段  →  继续 HR#2          │
│  • Issue 处于 Gate 5 Release →  继续发布         │
│                                                   │
│  Human 随时可能创建新 Issue                       │
│  新 Issue 从"PM 领取"开始，进入流程图 A          │
└─────────────────────────────────────────────────┘
        │
        ▼
Team Lead 协调多角色并行工作
```

**关键区分**：
- 流程图 A：单个 Issue 的完整生命周期（正向流程，从 PM 认领到 PM 关闭）
- 流程图 B：需求变更与打回的异常处理流程（被打回时触发）
- 流程图 C：Team 启动后的全局视角（多 Issue 并行调度）

## 关键原则

- **Issue 是强制入口**：无 Issue 不进入正式交付流程
- **无 Issue 不进入 PRD**：PM 领取 Issue 后与 Human 讨论（必须 Comment）才能开始 PRD
- **讨论结果必须 Comment**：每次讨论结束必须将结论 Comment 到 Issue，**未 Comment 视为未完成**
- **方案不等于有效**：当 Issue 包含解决方案时，PM 必须回归问题本身讨论
- **PRD 不含技术实现**：PRD 只描述问题/产品设计/能力边界/方案，不含技术实现
- **无 PRD Review 不进入 Tech Review**
- **无 Human Review #1 不进入 Implementation**
- **双 PR 分支策略**：文档 PR（doc-{issue}）和代码 PR（feature-{issue}）分离
- **文档 PR 合并 = 设计确认**
- **代码 PR 合并 = 实现确认**
- **PR 合并是 Human 专属操作**，Agent 只负责推动流程，不执行合并
- **Issue 关闭是 Human 专属操作**，Agent 只负责发布关闭请求评论
- Human Review 结论未正式落地，不视为通过
- **打回 = 回滚 + 重新走流程**：任意节点被打回 → 回滚到该节点编写阶段 → 修改文档（版本+1）→ 从该节点重新走完整流程
- **变更级联效应**：PRD 发生变更 → Tech Spec 需同步变更（版本+1）→ Case Design 需同步变更（版本+1）；Tech Spec 发生 Major/Breaking 变更 → 回到 Gate 1 重新评审 PRD

---

## 前置阶段：PM 领取 Issue + 讨论

### 触发条件

- Agent Team 已启动，已扫描所有 open Issues
- Human 随时可能创建新 Issue

### 进入条件

- PM 从 open Issues 中领取 Issue
- PM 与 Human 讨论问题（每次讨论必须 Comment 到 Issue）
- 当 Issue 包含解决方案时，PM 必须回归问题本身讨论

### 角色职责矩阵

| 角色 | 职责 |
|------|------|
| PM | 领取 Issue、与 Human 讨论、每次讨论后 Comment 到 Issue |
| Team Lead | 跟踪 Issue 领取状态、推动讨论进展 |
| Human | 提出问题、确认讨论结论 |

### 强制 Comment 节点

| 节点 | 执行者 | Comment 内容 |
|------|--------|-------------|
| Issue 领取 | PM | "Issue #N 已领取，开始分析需求" |
| 问题讨论完成 | PM | 讨论结论（回归问题本质，而非方案） |
| PRD 产出 | PM | "PRD 已完成: [链接] - 概述..." |

### 通过标准

PM 在 Issue 下完成首次 Comment（领取说明或讨论结论），方可进入 PRD 起草。

### 回退条件

- Issue 描述模糊 → 退回 PM 要求 Human 补充问题描述
- 讨论未 Comment → **未 Comment 视为未完成**，不得进入下一阶段

---

## Gate 0: Team Startup — 团队初始化

### 触发条件

- Human 发起团队启动命令（`/adf-start-agent-team`）
- 或 Human 要求启动新项目/新阶段

### 进入条件

- Human 已明确项目目标或本轮交付目标
- Human 已指定 Team Lead
- 已确定本轮需要参与的角色
- 已明确项目标识 `project_id`
- 已明确当前阶段（新项目启动会、增量需求还是异常修复）

### 角色职责矩阵

| 角色 | 职责 |
|------|------|
| Team Lead | 主持启动、分配角色、确认优先级、确认并行可行性 |
| PM | 确认需求来源、澄清问题边界、确认交付范围 |
| Architect | 确认技术范围、识别技术风险和依赖 |
| QA | 确认验收路径、识别测试需求 |
| Engineer | 待命，准备接收已确认的设计输入 |
| Platform/SRE | 确认环境、发布、回滚和平台检查边界 |
| PMO | 记录启动状态、检查 Issue 命名规范、检查流程合规性 |

### 输出物

- Team 配置完成（`.claude/teams/{project_id}/config.json`）
- 角色分配确认
- 项目骨架初始化（`docs/prd/`、`docs/tech/`、`docs/qa/`、`docs/release/`、`docs/memo/`、`docs/todo/`）
- 启动会纪要（`docs/memo/`）

### 下一动作

- Team Lead 通知所有角色初始化完成
- PM 从已扫描的 open Issues 中领取任务
- Team 进入正常工作状态（PM 领取 Issue → 讨论 → PRD）

### 回退条件

- 角色未完成初始化检查 → 该角色不得进入 Gate 1
- 主 issue、状态板、todo registry 三者缺一 → 必须补齐后继续

---

## Gate 1: PRD Review — 需求评审

### 进入条件

- PM 已领取 Issue（已在 Issue 下 Comment）
- PM 已与 Human 完成问题讨论（已 Comment 讨论结论）
- PRD 文档已起草（`docs/prd/PRD-{issue}_v*.md`）
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

### 通过标准

PM + Architect + QA 三方签字完成，Issue Comment 已落地。

### Human 专属操作

无（文档评审 Agent 可完成）

### 下一动作

- 通过 → PM 通知 Architect 开始 Tech Spec；QA 开始 QA Case Design 准备
- 不通过 → 退回 PM 修订，Issue 状态保持 `in_prd`

### 回退条件

- PRD 缺少范围/非目标/验收标准 → 退回 PM 修订
- 评审结论为 `Rejected` → 修订后重新评审

---

## Gate 2: Tech Review — 技术评审

### 进入条件

- PRD `Approved`（Gate 1 通过）
- Tech Spec 文档已起草（`docs/tech/Tech-{issue}_v*.md`）

### 角色职责矩阵

| 角色 | 职责 |
|------|------|
| Team Lead | 主持评审、确认流转 |
| PM | 确认 PRD 覆盖完整性 |
| Architect | 主持评审、识别风险和依赖（不签自己的 Tech Spec）|
| QA | 评审技术方案可行性（必签）|
| Engineer | 评审 Tech Spec 可实现性（必签）|

### 签字要求

- **QA（必签）**：技术方案可行性确认
- **Engineer（必签）**：技术方案可实现性确认
- **PM（确认）**：需求覆盖确认

### 输出物

- Tech Spec 状态更新为 `Approved`
- Issue Comment 包含：Gate 2 结论、两方签字、日期、Tech Spec 链接

### 通过标准

QA + Engineer + PM 三方签字完成，Issue Comment 已落地。

### Human 专属操作

无（文档评审 Agent 可完成）

### 下一动作

- 通过 → QA 开始 QA Case Design（三方签字）
- 不通过 → 退回修订

### 回退条件

- Tech 未完整覆盖 PRD → 退回 Architect 修订
- PRD 发生 Major/Breaking 变更 → 回到 Gate 1 重新评审

---

## QA Case Design — 测试用例设计

### 进入条件

- Tech Spec `Approved`（Gate 2 通过）
- QA 已开始基于 Tech Spec 设计测试用例

### 角色职责矩阵

| 角色 | 职责 |
|------|------|
| QA | 基于 Tech 方案设计测试 Case（按组件 + E2E）|
| PM | 确认测试覆盖范围 |
| Architect | 确认测试设计完整性 |
| Engineer | 评审测试 Case 可实现性 |

### 签字要求

- **PM（必签）**：测试覆盖范围确认
- **Architect（必签）**：测试设计完整性确认
- **Engineer（必签）**：测试 Case 可实现性确认

### 输出物

- QA Case Design 文档（`docs/qa/QA-Case-{issue}_v*.md`）
- Issue Comment 包含：Case Design 完成通知、签字人、文档链接

### 通过标准

PM + Architect + Engineer 三方签字完成，Issue Comment 已落地。

### 下一动作

- 通过 → PM 创建 `doc-{issue}` 分支，提交文档 PR
- 不通过 → 退回 QA 修订

---

## 文档 PR（doc-{issue}）— Human Review #1

### 进入条件

- PRD `Approved`（Gate 1）
- Tech Spec `Approved`（Gate 2）
- QA Case Design `Approved`
- 所有 Gate 签字已落地
- PM 已创建 `doc-{issue}-{简短描述}` 分支
- PM 已提交：PRD + Tech + QA Case Design 到该分支

### 分支命名规范

```
doc-{issue_number}-{简短描述}
示例：doc-3-gstack-superpower
```

### 角色职责矩阵

| 角色 | 职责 |
|------|------|
| PM | 创建分支、提交文档、创建 PR、推动 Human Review |
| Architect | 提供评审意见、签字 |
| QA | 提供评审意见、签字 |
| Team Lead | 确认评审完成、推动 Human 执行 PR 合并 |
| Human | Review 文档 PR、执行合并 |

### Human 专属操作

- **文档 PR 合并**（Human 执行，Agent 不执行）

### 通过标准

- Human Review 完成并决定合并
- 文档 PR 合并完成

### PM 发布 HR#1 通过评论后的下一动作

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

### 下一动作

- 通过 → Human 执行文档 PR 合并（PR 合并 = 设计确认）
- Conditional → 完成条件项后重新 Review
- 不通过 → 退回修订

---

## 文档 PR 合并 = 设计确认 ✅

文档 PR 合并后，设计正式确认，进入实现阶段。Engineer 收到 Human 的实现通知后，基于已确认的 PRD + Tech Spec 开发。

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

### 分支命名规范

```
feature-{issue_number}-{简短描述}
示例：feature-3-gstack-superpower
```

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

- QA 测试报告（`docs/qa/qa-report-{issue}_v*.md`）
- 缺陷清单（如有）
- 质量结论（Approved/Conditional/Rejected）
- Issue Comment 包含：测试完成通知、测试报告链接

### 通过标准

- 所有关键测试用例通过
- 无阻塞性缺陷（或阻塞缺陷有明确例外批准）
- QA 发布质量结论，Issue Comment 已落地

### Human 专属操作

无（QA 验证 Agent 可完成，但最终结论由 Human 确认）

### 下一动作

- 通过 → 确认是否需要代码 PR（纯文档交付跳过）
- 不通过 → Engineer 修复 → QA 重新验证

### 回退条件

- 发现阻塞性缺陷 → 退回 Engineer 修复 → 回到 QA 验证

---

## 代码 PR（feature-{issue}）— Human Review #2

### 进入条件

- QA 测试报告已完成
- 代码 PR 已创建（包含代码 + 测试报告）
- 测试报告和代码 PR 链接已回链 Issue

### 角色职责矩阵

| 角色 | 职责 |
|------|------|
| PM | 评审实现满足 PRD 验收标准、出具意见、确认签字 |
| Architect | 评审代码与 Tech Spec 一致性、出具意见、确认签字 |
| QA | 评审 QA 报告完整性、出具意见、确认签字 |
| Team Lead | 确认评审完成、推动 Human 合并代码 PR |
| Human | Review 代码 PR、执行合并 |

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

- 发布记录（`docs/release/release-{issue}_v*.md`）
- 回滚方案
- 值守安排
- Issue Comment 包含：发布结论、参与者、日期

### 通过标准

PM + Architect + Platform/SRE 三方放行。

### Human 专属操作

- **Issue 关闭**（Human 执行，Agent 发布"关闭请求"评论）

### 下一动作

- PM 通过 `scripts/github_issue_sync.py` 发布"Issue 关闭请求"评论
- Human 执行 Issue 关闭（或通知 Team Lead 代为操作）

### 回退条件

- 发布风险未明确 → 回到 Gate 4
- 回滚方案缺失 → 补充回滚方案

---

## 双 PR 分支策略

### 分支类型

| 阶段 | 分支名 | 内容 | 生命周期 |
|------|--------|------|---------|
| 文档 PR | `doc-{issue}-{描述}` | PRD + Tech + QA Case Design | 创建 → Review → 合并/关闭 |
| 代码 PR | `feature-{issue}-{描述}` | 代码 + 测试报告 | 创建 → 开发 → Test → Review → 合并 |

### 分支依赖关系

```
main
  └── doc-13-xxx (创建，提交设计文档)
        └── [Human 合并] → main
              └── feature-13-xxx (基于 main，创建开发分支)
                    └── [Human 合并] → main
```

### 文档 PR 创建条件（必须同时满足）

```
✅ PRD 文档完成（docs/prd/PRD-XXX_v*.md）
✅ Tech 文档完成（docs/tech/Tech-XXX_v*.md）
✅ Gate 2 Tech Review 两签通过（PM + QA）
✅ QA Case Design 完成（docs/qa/QA-Case-XXX_v*.md）
```

### 代码 PR 创建条件（必须同时满足）

```
✅ 文档 PR 已合并（设计已确认）
✅ 代码开发完成
✅ QA 测试报告完成（docs/qa/qa-report-XXX_v*.md）
✅ 三方签字验收完成（Architect + Engineer + PM）
```

---

## Issue Comment 强制要求（V2.2.4）

**⚠️ 强制规则**：未 Comment 视为未完成。每个角色完成工作后必须在 Issue 下 Comment。

| 节点 | 执行者 | Comment 内容 | 示例 |
|------|--------|-------------|------|
| Issue 领取 | PM | 说明领取，开始分析 | "Issue #N 已领取，开始分析需求" |
| 问题讨论完成 | PM | 讨论结论（回归问题本质）| "讨论完成：问题根源是 X，方案 Y 已被否决" |
| PRD 产出 | PM | PRD 链接 + 概述 | "PRD 已完成: [链接] - 概述..." |
| PRD 评审完成 | PM | 评审结论 + 签署人 | "PRD 评审通过 - PM[✅] Architect[✅] QA[✅]" |
| Tech 产出 | Architect | Tech 链接 + 概述 | "Tech 已完成: [链接] - 概述..." |
| Tech Review 完成 | Architect | 评审结论 + 签署人 | "Tech Review 通过 - PM[✅] QA[✅]" |
| QA Case Design 完成 | QA | Case 链接 + 概述 | "QA Case Design 完成: [链接]" |
| 文档 PR 创建 | PM | PR 链接 + 文档清单 | "文档 PR 已创建: [链接] - PRD/Tech/QA Case" |
| 文档 PR 合并 | PM | 合并确认 | "文档 PR 已合并，设计确认完毕" |
| 开发完成 | Engineer | 开发报告 | "开发完成 - [组件列表] - 待测试" |
| 测试完成 | QA | 测试报告链接 | "测试完成 - [报告链接]" |
| 代码 PR 创建 | Engineer | PR 链接 + 测试报告 | "代码 PR 已创建: [链接] - Fixes #N" |
| 代码 PR 合并 | Engineer | 合并确认 | "代码 PR 已合并 - 等待 Issue 关闭" |
| Issue 关闭 | PM | 关闭原因 + 关闭请求 | "Issue #N 请求关闭 - 完成/重复/无法复现" |

**必须通过 `scripts/github_issue_sync.py` 发布 Comment**：
```bash
python scripts/github_issue_sync.py \
  --post-comment \
  --issue N \
  --body "$(cat comment.md)" \
  --agent "Agent名称"
```

---

## 角色职责矩阵总览

| 节点 | Team Lead | PM | Architect | QA | Engineer | Platform/SRE | PMO |
|------|-----------|-----|-----------|-----|----------|-------------|-----|
| 领取 Issue | 跟踪 | **领取/讨论** | — | — | — | — | 审计 |
| Gate 0: Startup | 主持/分配 | 确认来源 | 确认范围 | 确认路径 | 待命 | 确认环境 | 记录 |
| Gate 1: PRD Review | 主持/流转 | 主持/签字 | 评审可行性 | 评审完整性 | — | — | 审计 |
| Gate 2: Tech Review | 主持/流转 | 确认覆盖 | 主持（不签自己的）| 评审/签字 | 评审可实现性/签字 | — | 审计 |
| QA Case Design | — | 签字 | 签字 | **设计** | 签字 | — | 审计 |
| **文档PR合并** | **—** | **通知TL** | **—** | **—** | **—** | **—** | **—** |
| Gate 3: Impl | 跟踪 | 跟踪 | 确认一致性 | 跟踪 | **实现** | — | 审计 |
| Gate 4: QA | 跟踪 | 确认口径 | — | **验证/报告** | 修复 | — | 审计 |
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
| PM | 领取 Issue | 在 Issue 下完成首次 Comment（领取说明或讨论结论）|
| PM | Gate 1 | PRD 起草完成、Gate 1 三方签字完成、Issue Comment 落地 |
| PM | Gate 2 | 确认 Tech 覆盖 PRD、Gate 2 两方签字完成 |
| PM | QA Case Design | 三方签字完成、Issue Comment 落地 |
| PM | 文档 PR | HR#1 评审意见已落地、发布结论评论、**通知 Team Lead 合并** |
| PM | Gate 3-4 | 跟踪进度、确认口径（不执行实现/验证）|
| PM | Gate 5 | 业务放行签字 |
| PM | **Issue Close** | **发布"Issue 关闭请求"评论，不自行关闭** |
| Architect | Gate 1 | 评审技术可行性、签字 |
| Architect | Gate 2 | 主持 Tech Spec 评审、确认 QA + Engineer 签字（不签自己的）|
| Architect | QA Case Design | 确认测试设计完整性、签字 |
| Architect | HR#1/2 | 独立评审意见、签字 |
| Architect | Gate 3 | 确认实现与 Tech 一致性 |
| Architect | Gate 5 | 技术放行签字 |
| QA | Gate 1 | 评审验收标准完整性、签字 |
| QA | Gate 2 | 评审技术方案可行性、签字 |
| QA | QA Case Design | 测试 Case 设计、签字 |
| QA | HR#1/2 | 独立评审意见、签字 |
| QA | Gate 4 | 测试执行完成、报告已发布、质量结论已落地 |
| Engineer | Gate 2 | 评审 Tech Spec 可实现性、签字 |
| Engineer | QA Case Design | 评审测试 Case 可实现性、签字 |
| Engineer | Gate 3 | 代码实现完成、单元测试通过、实现文档同步、通知 QA |
| Engineer | Gate 4 | 缺陷修复、响应 QA 反馈 |
| Engineer | 代码 PR | 创建 PR、通知 Human Review |
| Platform/SRE | Gate 5 | 发布准备清单完成、回滚方案确认、值守安排确认 |
| Team Lead | 全流程 | 主持评审、确认流转、推动 Human 合并、推动升级 |
| PMO | 全流程 | 记录问题、推动纠正、审计合规性 |

---

## 流程异常处理

### 回退规则

| 场景 | 回退到 |
|------|--------|
| PM 未领取 Issue 或未 Comment | 退回 PM 领取 + 讨论 |
| PRD 缺少必要项 | Gate 1 → 退回 PM 修订 |
| Tech 未覆盖 PRD | Gate 2 → 退回 Architect 修订 |
| PRD 发生 Major/Breaking 变更 | Gate 1 → 重新评审 |
| Tech 发生 Major/Breaking 变更 | Gate 2 → 重新评审 |
| QA Case Design 未通过 | QA Case Design → 退回 QA 修订 |
| HR#1 未通过 | 文档 PR → 修订后重新 Review |
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

### 变更级联效应

当上游文档发生变更时，下游文档必须同步更新：

| 变更来源 | 影响范围 | 处理方式 |
|----------|---------|---------|
| PRD 变更 | Tech Spec、Case Design | Tech Spec 版本+1 → Case Design 版本+1 → 重新评审受影响文档 |
| Tech Spec 发生 Major/Breaking 变更 | PRD、Case Design | 回到 Gate 1 重新评审 PRD → 按顺序重新走完整个流程 |
| Case Design 变更 | 测试报告 | 测试报告版本+1 → 重新评审测试报告 |

---

## 文档版本规范

每个交付文档（PRD、Tech Spec、Case Design、测试报告）必须包含以下三个部分：

### 1. 版本历史表

每个文档必须记录版本变更历史：

```
| 版本 | 日期 | 变更说明 | 变更人 |
|------|------|---------|-------|
| v1.0 | 2026-04-20 | 初始版本 | PM |
| v1.1 | 2026-04-21 | 需求变更：xxx，评审打回后修改 | PM |
```

### 2. 前序文档追溯链

每个文档必须明确标注依赖的前序文档版本号，形成可追溯的依赖链：

```
PRD v3.1 → Tech Spec v2.3 → Case Design v1.4 → 测试报告 v1.2
```

### 3. 评审记录表

每次评审必须记录完整过程：

```
| 评审日期 | 评审节点 | 评审结果 | 评审人 | 意见/打回原因 | 修改后版本 |
|----------|---------|---------|-------|-------------|-----------|
| 2026-04-20 | Gate 1 | 打回 | Human | 缺少非目标定义 | v1.1 |
| 2026-04-21 | Gate 1 | 通过 | PM+Architect+QA | — | v1.1 |
```

### 变更传播规则

- PRD 变更 → Tech Spec 需同步变更（版本+1）→ Case Design 需同步变更（版本+1）
- Tech Spec 发生 Major/Breaking 变更 → 回到 Gate 1 重新评审 PRD
- 任意文档变更 → 对应下游文档版本+1 → 重新评审

### 评审过程记录要求

- 每次评审必须记录：评审结果（通过/打回）、具体意见、打回原因
- 打回后修改必须记录：修改了什么、为什么这样改
- 重新评审必须记录：相比上次修改了什么、新的评审意见

---

## 版本与参考

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v2.0 | 2026-04-20 | 修正流程概览起点、重写 Gate 0、增加 PM 领取 Issue + 讨论 Comment 规则、增加双 PR 分支策略、增加 V2.2.4 Issue Comment 强制要求 |
| v2.1 | 2026-04-20 | 增加流程图 B（打回机制）、流程图 C（Agent Team 启动后 Issue 扫描与路由）、增加文档版本规范（版本历史表、前序追溯链、评审记录表）、增加变更级联效应规则 |

**参考文档**：
- `hedge-ai/prompts/V3.0/change_record/V2.0_研发流程与GitHubIssue结合及QA角色引入.md`
- `hedge-ai/prompts/V3.0/change_record/V2.2_双PR机制引入.md`
- `prompts/discuss/032_2026-04-20_002流程错误复核.md`