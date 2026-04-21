# 开发交付流程（Develop Pipeline）

## 目标

定义 AgentDevFlow 的完整开发交付流程，基于 V2.0/V2.2 双 PR 机制，作为所有 Agent 的核心必读流程文档。

本文档与 `004_delivery_gates.md`（Gate 合规检查定义）、`017_human_review_and_signoff.md`（Human Review 规范）配套使用。

## 关键原则（Critical Rules）

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
- **纯文档交付与开发交付同等重要**：只要是正式交付，无论是否包含代码变更，都必须严格按照 Issue 主线、文档交付物、Human Review 和关闭边界执行
- **PR 合并是 Human 专属操作**，Agent 只负责推动流程，不执行合并
- **Issue 关闭是 Human 专属操作**，Agent 只负责发布关闭请求评论
- Human Review 结论未正式落地，不视为通过
- **打回 = 回滚 + 重新走流程**：任意节点被打回 → 回滚到该节点编写阶段 → 修改文档（版本+1）→ 从该节点重新走完整流程
- **变更级联效应**：PRD 变更 → Tech Spec 版本+1 → Case Design 版本+1；Tech Spec 发生 Major/Breaking 变更 → 回到 Gate 1 重新评审 PRD

---

## 三个流程图

本文档包含三个独立的流程图，从不同视角描述开发交付流程：

### 流程图 A：完整 Issue 交付流程（正向流程，从认领到关闭）

```
PM 领取 Issue → 与 Human 讨论问题（每次讨论后必须 Comment 到 Issue）
        │
        ▼
PRD 产出 → Comment 到 Issue（含 PRD 链接）
        │
        ▼
Gate 1: PRD Review — 需求评审（PM + Architect + QA 三方签字）
        │
        ▼
Gate 2: Tech Review — 技术评审（QA + Engineer + PM 三签）
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
        ├── QA 根据 Case Design 开发测试代码（case 代码）
        ├── QA 运行 case 验证 Engineer 完成的代码质量
        ├── 不合格 → 排查问题来源：
        │   • 代码问题 → Engineer 修复 → 重新验证
        │   • Case 问题 → QA 修复 case → 重新验证
        ├── 验证通过 → QA 编写测试报告（QA Report）
        │
        ├── PM + Architect + Engineer 三方评审测试报告并签字
        │
        ▼ (通过)
代码 PR（feature-{issue} 分支）— Human Review #2
        │
        ▼
代码 PR 合并 = 实现确认 ✅
        │
        ▼
Gate 5: Release — 发布
        │
        ▼
PM 通过 github_issue_sync.py 发布关闭请求 → Human 执行关闭
```

**强制 Comment 规则**：`PM 领取 Issue` 后每次与 Human 讨论结束必须 Comment 到 Issue。**未 Comment 视为未完成**，不得进入下一阶段。

**Human Review 绑定**：Human Review #1 = 文档 PR（doc-{issue}）合并 = 设计确认；Human Review #2 = 代码 PR（feature-{issue}）合并 = 实现确认。

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

---

## 双 PR 分支策略

### 分支命名

| 阶段 | 分支名 | 内容 | Human Review |
|------|--------|------|--------------|
| 设计确认 | `doc-{issue_number}-{简短描述}` | PRD + Tech + QA Case Design | **HR#1** |
| 实现确认 | `feature-{issue_number}-{简短描述}` | 代码 + 测试报告 | **HR#2** |

### 文档 PR 创建条件（必须同时满足）

```
✅ PRD 文档完成（docs/prd/PRD-XXX_v*.md）
✅ Tech 文档完成（docs/tech/Tech-XXX_v*.md）
✅ Gate 2 Tech Review 三签通过（QA + Engineer + PM）
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
| Tech Review 完成 | Architect | 评审结论 + 签署人 | "Tech Review 通过 - PM[✅] QA[✅] Engineer[✅]" |
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

## 阶段详解

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
- **QA（必签）**：验收标准可测试性确认

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
- **PM（必签）**：需求覆盖确认

### 输出物

- Tech Spec 状态更新为 `Approved`
- Issue Comment 包含：Gate 2 结论、三方签字、日期、Tech Spec 链接

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
| Architect | 提供评审意见，响应 Human Review 中的技术问题 |
| QA | 提供评审意见，响应 Human Review 中的质量问题 |
| Team Lead | 确认评审完成、推动 Human 执行 PR 合并 |
| Human | Review 文档 PR、执行合并 |

### Human 专属操作

- **文档 PR 合并**（Human 执行，Agent 不执行）

### 通过标准

- Human Review 完成并决定合并
- 文档 PR 合并完成

### 文档 PR 通过后的下一动作

```
PM 确认 HR#1 前置材料齐备
        │
        ▼
PM 通知 Team Lead：文档 PR 可以进入 Human Review #1
        │
        ▼
Team Lead 推动 Human 执行文档 PR Review / 合并
        │
        ▼
Human 执行 PR 合并（PR 合并是 Human 专属操作）
        │
        ▼
文档 PR 合并 = 设计确认
        │
        ▼
Engineer 可进入 Implementation
```

### 下一动作

- 通过 → Human 执行文档 PR 合并（PR 合并 = 设计确认）
- Conditional → 完成条件项后重新 Review
- 不通过 → 退回修订

---

## 文档 PR 合并 = 设计确认 ✅

文档 PR 合并后，设计正式确认，进入实现阶段。Engineer 基于已确认的 PRD + Tech Spec 开发。

### Human 专属操作

- **文档 PR 合并**（Human 执行，Agent 不执行）

### 下一动作

文档 PR 合并后，Engineer 进入 Implementation。

---

## Gate 3: Implementation — 开发实现

### 进入条件

- 文档 PR 已合并（设计确认）
- Human Review #1 已通过

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

无（QA 验证 Agent 可完成）

### 下一动作

- 通过 → 确认是否需要代码 PR（纯文档交付跳过）
- 不通过 → Engineer 修复 → QA 重新验证

### 回退条件

- 发现阻塞性缺陷 → 退回 Engineer 修复 → 回到 QA 验证

---

## 代码 PR（feature-{issue}）— Human Review #2

### 进入条件

- QA 测试报告已完成
- PM + Architect + Engineer 已完成测试报告评审并签字
- 代码 PR 已创建（包含代码 + 测试报告）
- 测试报告和代码 PR 链接已回链 Issue

### 角色职责矩阵

| 角色 | 职责 |
|------|------|
| PM | 确认进入 Human Review #2 的前置材料已齐备，推动 Human Review |
| Architect | 提供技术背景说明，响应 Human Review 中的技术问题 |
| QA | 提供测试报告与质量结论，响应 Human Review 中的质量问题 |
| Engineer | 创建代码 PR，补充实现说明，响应 Human Review 中的实现问题 |
| Team Lead | 确认前置条件完成、推动 Human 合并代码 PR |
| Human | Review 代码 PR、执行合并 |

### 通过标准

- Human Review #2 完成
- Human 决定合并代码 PR
- 代码 PR 合并完成

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

- 已完成正式交付确认：
  - 开发交付场景：Human Review #2 通过，代码 PR 已合并
  - 纯文档交付场景：Human Review #1 通过，文档 PR 已合并
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
- Human 执行 Issue 关闭

### 回退条件

- 发布风险未明确 → 回到 Gate 4
- 回滚方案缺失 → 补充回滚方案


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

## 纯文档交付说明

在 AgentDevFlow 中，纯文档交付不是例外场景，而是与开发交付同等重要的正式交付场景。很多 Agent 编排项目本身的交付物就是 prompts、spec、workflow、review 记录等 Markdown 文档。

因此：

- 纯文档变更也必须创建并绑定 GitHub Issue
- 纯文档变更也必须产出正式交付文档并回链 Issue
- 纯文档变更也必须经过文档 PR 和 Human Review #1
- 纯文档交付完成后，仍然必须通过 Issue Comment 回写结论，并由 Human 执行 Issue 关闭

区别只在于：

- 开发交付场景：`文档 PR -> Human Review #1 -> Implementation -> QA Validation -> 代码 PR -> Human Review #2`
- 纯文档交付场景：`文档 PR -> Human Review #1 -> Release / Issue Close`

两者在 Issue 主线、文档交付物、Human Review 边界和关闭要求上同样严格。

---

## 完成标准矩阵

每个角色在每个 Gate 的"完成标准"：

| 角色 | Gate | 完成标准 |
|------|------|---------|
| PM | 领取 Issue | 在 Issue 下完成首次 Comment（领取说明或讨论结论）|
| PM | Gate 1 | PRD 起草完成、Gate 1 三方签字完成、Issue Comment 落地 |
| PM | Gate 2 | 确认 Tech 覆盖 PRD、Gate 2 三方签字完成 |
| PM | QA Case Design | 三方签字完成、Issue Comment 落地 |
| PM | 文档 PR | HR#1 评审意见已落地、发布结论评论、**通知 Team Lead 合并** |
| PM | Gate 3-4 | 跟踪进度、确认口径（不执行实现/验证）|
| PM | Gate 5 | 业务放行签字 |
| PM | **Issue Close** | **发布"Issue 关闭请求"评论，不自行关闭** |
| Architect | Gate 1 | 评审技术可行性、签字 |
| Architect | Gate 2 | 主持 Tech Spec 评审、确认 QA + Engineer 签字（不签自己的）|
| Architect | QA Case Design | 确认测试设计完整性、签字 |
| Architect | HR#1 | 独立评审意见、签字 |
| Architect | Gate 3 | 确认实现与 Tech 一致性 |
| Architect | Gate 5 | 技术放行签字 |
| QA | Gate 1 | 评审验收标准完整性、签字 |
| QA | Gate 2 | 评审技术方案可行性、签字 |
| QA | QA Case Design | 测试 Case 设计、签字 |
| QA | HR#1 | 独立评审意见、签字 |
| QA | Gate 4 | 测试执行完成、报告已发布、质量结论已落地 |
| Engineer | Gate 2 | 评审 Tech Spec 可实现性、签字 |
| Engineer | QA Case Design | 评审测试 Case 可实现性、签字 |
| Engineer | Gate 3 | 代码实现完成、单元测试通过、实现文档同步、通知 QA |
| Engineer | Gate 4 | 缺陷修复、响应 QA 反馈 |
| Engineer | 代码 PR | 创建 PR、补充实现说明、响应 Human Review |
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

**核心原则：Gate 流程必须串行执行，禁止并行迭代。**

下游文档依赖上游文档的评审结论。任何 Gate 未 Approved 前，不得进入下游 Gate 的文档编写。并行迭代会导致文档间语义不一致，最终只能在 HR#1 阶段以高代价发现。

**禁止行为**：
- PRD 在 Gate 1 评审期间，Tech Spec 不得更新
- Tech Spec 在 Gate 2 评审期间，QA Case 不得起草
- 任何 Gate 未 Approved 前，不得进入下游 Gate

#### 变更等级定义

**重大变更**（必须触发完整 Gate 重审）：
- 语义发生变化（可选→强制、单一→多个、范围扩大/缩小）
- 新增或删除交付域
- 角色数量变化
- 关键验收标准变更
- 架构决策变更（技术选型改变、检测方式改变）

**小幅变更**（仅需原 Gate 签字人确认，无需完整 Gate 重审）：
- 文档格式调整
- 错别字修正
- 描述文字澄清（不改变语义）
- 补充遗漏内容（不改变范围）
- 链接修正

#### 变更追溯规则

| 变更来源 | 变更等级 | 需重新通过的 Gate | 下游文档处理 |
|---------|---------|------------------|-------------|
| PRD | 重大 | Gate 1 → Gate 2 → QA Case Design → 重新评审全部 | Tech Spec 版本+1 → Case Design 版本+1 |
| PRD | 小幅 | 原 Gate 1 签字人确认即可 | Tech Spec 确认无影响后无需变更 |
| Tech Spec | Major/Breaking | Gate 2 → QA Case Design → 重新评审 | 如影响 PRD，回到 Gate 1；Case Design 版本+1 |
| Tech Spec | 小幅 | 原 Gate 2 签字人确认即可 | Case Design 确认无影响 |
| QA Case | 任意 | QA Case Design 重新评审 | 测试报告版本+1（如有）|
| 多环节同时变更 | — | 从头重新走 Gate 1 → Gate 2 → QA Case | 全部文档版本+1 |

#### Gate 进入条件强化（新增上游确认检查）

| Gate | 进入条件（强化） |
|------|-----------------|
| Gate 1 | PRD 已起草；当前无未完成的下游文档更新在并行进行 |
| Gate 2 | **PRD Gate 1 已 Approved**；Tech Spec 已起草；无 QA Case 并行起草 |
| QA Case Design | **Gate 2 已 Approved**；QA Case 已起草 |
| 文档 PR | 所有 Gate 签字已落地；无未完成的文档变更在评审中 |

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
| v2.2 | 2026-04-20 | 删除重复章节（双 PR 分支策略/Issue Comment）、统一 Gate 1/2 签字描述（全部"必签"）、Gate 2 输出物改为三方签字、精简文档结构（-74 行） |

**参考文档**：
- `hedge-ai/prompts/V3.0/change_record/V2.0_研发流程与GitHubIssue结合及QA角色引入.md`
- `hedge-ai/prompts/V3.0/change_record/V2.2_双PR机制引入.md`
- `prompts/discuss/032_2026-04-20_002流程错误复核.md`
