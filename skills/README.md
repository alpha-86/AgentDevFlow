# 共享技能目录

`skills/` 是 AgentDevFlow 的平台无关执行资产层。

## 结构

- `team-setup.md`
  团队启动与 启动会 共享入口。

- `start-agent-team.md`
  更接近执行入口的团队启动步骤，约束项目骨架、角色加载和首轮检查。

- `skill-protocol.md`
  共享执行顺序、状态语义和恢复顺序。

- `event-bus.md`
  共享事件、触发规则、阻断条件和失败升级路径。

- `workflows/`
  阶段流程、准入准出条件、签字与回退规则。

- `templates/`
  正式留痕模板与交付物结构。

## 最近补充的关键资产

- `workflows/human-review.md`
- `workflows/issue-routing.md`
- `workflows/project-portfolio-review.md`
- `templates/artifact-linkage-template.md`
- `templates/project-portfolio-template.md`
- `templates/project-kickoff-checklist-template.md`
- `team-setup.md`
- `start-agent-team.md`
- `skill-protocol.md`
- `event-bus.md`
- `templates/agent-activation-template.md`
- `templates/audit-report-template.md`
- `templates/qa-report-template.md`
- `templates/release-record-template.md`
- `templates/platform-checklist-template.md`
- `templates/platform-check-result-template.md`
- `templates/agent-creation-log-template.md`
- `templates/评审-评论-checklist-template.md`
- `templates/project-status-board-template.md`

## 使用原则

- 平台适配层只能包装入口，不得改写这里的核心语义。
- 角色、工作流、template 必须与中文主版本规则保持一致。
- 角色文件必须明确：必读文档、初始化动作、上下文恢复、Issue/Gate 责任、禁止行为、输出格式。
- 主持会议或执行评审前，必须先读取对应 工作流。
- 团队启动、Agent 创建、事件分发都必须优先复用共享入口，而不是在平台层各写一套。
- **强制 Comment 规则**：每个角色完成工作后必须在对应 Issue 下 Comment。**未 Comment 视为未完成**，不得进入下一阶段。

## 流程入口规则

完整流程见 `prompts/002_develop_pipeline.md`。以下是与 `skills/` 资产强关联的流程节点：

### 流程启动顺序

完整流程见 `prompts/002_develop_pipeline.md`（包含流程图 A/B/C）。

以下是与 `skills/` 资产强关联的流程节点：

#### 团队启动视角（流程图 C）

```
Agent Team 启动
        │
        ▼
扫描所有 open GitHub Issues
        │
        ▼
对每个 Issue 根据当前状态继续对应流程节点：
        │
        ├── Issue 处于 Gate 1 阶段  →  继续 PRD Review
        ├── Issue 处于 Gate 2 阶段  →  继续 Tech Review
        ├── Issue 处于 QA Case Design →  继续 Case 签字
        ├── Issue 处于文档 PR 阶段  →  继续 Human Review #1
        ├── Issue 处于 Implementation →  继续开发
        ├── Issue 处于 Gate 4 QA   →  继续 QA 验证
        ├── Issue 处于代码 PR 阶段  →  继续 Human Review #2
        └── Issue 处于 Gate 5 Release →  继续发布
        │
        ▼
Human 随时可能创建新 Issue
        │
        └── 新 Issue 从"PM 领取"开始，进入单个 Issue 流程
        │
        ▼
Team Lead 协调多角色并行工作
```

#### 单个 Issue 流程（流程图 A）

```
PM 领取 Issue → 与 Human 讨论问题（每次讨论后必须 Comment 到 Issue）
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
        ├── QA 根据 Case Design 开发测试代码（case 代码），不是 Engineer 开发
        ├── QA 运行 case 验证 Engineer 完成的代码质量
        ├── 不合格 → 排查问题来源：
        │   • 代码问题 → Engineer 修复 → 重新验证
        │   • Case 问题 → QA 修复 case → 重新验证
        ├── 验证通过 → QA 编写测试报告（QA Report）
        │
        ├── PM + Architect + Engineer 三方评审测试报告并签字
        │   • PM: 是否满足 PRD 需求
        │   • Architect: 是否满足 Case Design 和 Tech Spec
        │   • Engineer: 修复情况如何修复的
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

### 双 PR 分支策略

| 阶段 | 分支名 | 内容 | Human Review |
|------|--------|------|--------------|
| 设计确认 | `doc-{issue_number}-{简短描述}` | PRD + Tech + QA Case Design | **HR#1** |
| 实现确认 | `feature-{issue_number}-{简短描述}` | 代码 + 测试报告 | **HR#2** |

分支创建条件：
- 文档 PR：PRD `Approved` + Tech Spec `Approved` + QA Case Design `Approved` + Gate 2 三签通过
- 代码 PR：文档 PR 已合并 + 代码开发完成 + QA 测试报告完成 + 三方签字验收完成

仅文档 PR 已创建不代表可进入 Implementation；必须文档 PR 已合并且 Human Review #1 已完成。

### PM 领取 Issue + Comment 规则

> 完整 Comment 节点表格见 `prompts/002_develop_pipeline.md`「Issue Comment 强制要求」章节。以下为关键节点：

| 节点 | 执行者 | Comment 内容 |
|------|--------|-------------|
| Issue 领取 | PM | "Issue #N 已领取，开始分析需求" |
| 问题讨论完成 | PM | 讨论结论（回归问题本质）|
| PRD 产出 | PM | "PRD 已完成: [链接] - 概述..." |
| PRD 评审完成 | PM | "PRD 评审通过 - PM[×] Architect[×] QA[×]" |
| Tech 产出 | Architect | "Tech 已完成: [链接] - 概述..." |
| Tech Review 完成 | Architect | "Tech Review 通过 - PM[×] QA[×] Engineer[×]" |
| QA Case Design 完成 | QA | "QA Case Design 完成: [链接]" |
| 文档 PR 创建 | PM | "文档 PR 已创建: [链接] - PRD/Tech/QA Case" |
| 文档 PR 合并 | PM | "文档 PR 已合并，设计确认完毕" |
| 开发完成 | Engineer | "开发完成 - [组件列表] - 待测试" |
| 测试完成 | QA | "测试完成 - [报告链接]" |
| 代码 PR 创建 | Engineer | "代码 PR 已创建: [链接] - Fixes #N" |
| 代码 PR 合并 | Engineer | "代码 PR 已合并 - 等待 Issue 关闭" |
| Issue 关闭 | PM | "Issue #N 请求关闭 - 完成/重复/无法复现" |

**必须通过 `scripts/github_issue_sync.py` 发布 Comment**，未 Comment 视为未完成，不得进入下一阶段。

## 当前判定

`skills/` 现在已经基本构成插件核心资产层，原因是它已经具备：

- 共享启动入口：`team-setup.md`、`start-agent-team.md`
- 共享协议：`skill-protocol.md`
- 共享角色：主角色 + playbook
- 共享 工作流：PRD / Tech / 人工评审 / 日会 / 待办 / 周月复盘
- 共享 template：PRD、Tech、QA、Release、Memo、待办、评审评论 等正式留痕模板

但它还不是完全收口状态，当前主要缺口仍然是：

- `github-issue/SKILL.md` 对应的共享入口还不够明确
- `review-org/SKILL.md` 对应的共享入口还不够明确
- evaluation checker 还没有沉到 `skills/` 形成更独立的检查子能力
