# AgentDevFlow

AgentDevFlow 是一套面向 AI Coding 的多 Agent 研发交付机制与协作框架。它关注的不是单个 Agent 会不会写代码，而是如何通过编排多 Agent 协作的研发 pipeline，把 harness 一类能力落到真实的产研协作、角色分工和交付约束中，并在高需求吞吐下并行、可控地跟进多个研发任务。

它解决的核心问题有三个：需求和结论如何留痕，设计和实现如何防漂移，多个 Agent 与人如何在关键节点形成可阻断、可追溯、可恢复且可并行编排的协作链路。

## 两个入口

如果你第一次接触 AgentDevFlow，建议按目标进入：

### 我想理解这套机制

先读：

1. [核心机制](#核心机制)
2. [完整流程](#完整流程)
3. [默认角色与边界](#默认角色与边界)
4. [流程如何被保障](#流程如何被保障)

### 我想快速接入试用

先读：

1. [快速接入](#快速接入)
2. [协作通道与入口](#协作通道与入口)
3. [继续阅读](#继续阅读)

## 为什么需要 AgentDevFlow

很多团队已经在用 Claude、Codex 或其他 Agent 工具，但真正容易失控的往往不是编码本身，而是协作过程：需求靠聊天传递、结论停留在会话里、PRD/Tech/代码容易漂移、测试和验收缺少前置约束，而且一旦同时推进多个任务，传统聊天式安排很难并行、可控地持续跟进。

AgentDevFlow 的目标，是把这些问题收敛成一套可复用的交付机制：用 GitHub Issue 串主线，用文件交付物做正式交接，用双阶段 PR、QA 闭环和 Human Review 把关键节点固定下来，并让多个研发任务能够并行推进而不互相串线。

## 核心机制

### 1. GitHub Issue 是正式主线

主 Issue 是每个需求、变更或异常的正式入口。关键产物、阶段结论、Gate 门控状态、QA 结论和最终验收都要回链到 Issue，而不是只停留在聊天记录里。

更重要的是，Issue 不只是留痕容器，也是多任务并行的基本单位。通过 GitHub Issue 作为正式主线，AgentDevFlow 可以并行、可控地跟进多个研发任务，而不是把多个任务混在同一条聊天上下文里推进。这也是它支持高需求吞吐、多 Agent 协作和稳定交付质量的基础。

### 2. 文件交付物是唯一正式交接物

PRD、Tech Spec、QA Case Design、QA Report 不是顺手写的文档，而是上下游的正式交接物。Agent 与 Agent 之间的正式接力只认文件和结构化评论，不靠口头补充。

### 3. 双阶段 PR + Human Review

AgentDevFlow 将研发链路拆成两个明确阶段：

- 文档 PR：PRD + Tech + QA Case Design，合并代表设计确认
- 代码 PR：代码 + 测试证据 + QA 结论，合并代表实现确认

两次 PR 都通过 Human Review 在关键节点引入人的判断。

### 4. 交付质量闭环

质量闭环不是开发完再测，而是：

`QA Case Design -> Engineer 实现 -> QA 验证 -> Engineer 修复 -> QA Report`

QA 负责把 PRD 和 Tech 的承诺转成可验证路径，Engineer 负责按已确认输入实现并交付证据，两者围绕 case 循环直到形成可审阅结果。

### 5. 流程改进闭环

除了交付主线，AgentDevFlow 还有一条并行的流程改进线：

`PMO 审计 -> 发现重复问题 -> 回写 roles / workflows / templates / prompts -> 下轮执行`

它的目的不是替代交付，而是持续修正多 Agent 协作中的重复性偏差和机制漏洞。

完整原则见 [核心原则](./docs/governance/core-principles.md)。

## 完整流程

```text
需求 / 问题 / 异常
        │
        ▼
创建主 GitHub Issue
        │
        ▼
PM 澄清问题与边界
        │
        ▼
PRD
        │
        ▼
Gate 门控 1: PRD Review
        │
        ▼
Tech Spec + QA Case Design
文档阶段交付物
        │
        ▼
Gate 门控 2: Tech Review
        │
        ▼
文档 PR
PRD + Tech + QA Case Design
Human Review #1
合并 = 设计确认
        │
        ▼
Engineer 基于已确认 PRD + Tech 实现
        │
        ▼
QA 基于已确认 QA Case Design 验证 / 回归
        │
        ├── 未通过：反馈缺陷给 Engineer 修复并回到 QA 验证
        │
        ▼
全部约定 case 通过 + 测试报告
        │
        ▼
代码 PR
代码 + 测试证据 + 测试报告 / QA 结论
Human Review #2
合并 = 实现确认
        │
        ▼
Issue Comment Gate 门控
        │
        ▼
Release / 验收 / Human 关闭
```

上图展示的是最核心的交付主线。几个常见场景可以这样理解：

- `PMO`：并行做流程审计和机制改进，不代替正式签字和交付闭环
- `已有人工 PRD`：PM Agent 不重写需求，而是把人类 PRD 整理成其他 Agent 可稳定读取和评审的正式输入
- `修 Bug`：也建议先写清问题现象、影响范围、预期行为和修复边界，再进入后续流程

在真实使用中，这条主线通常不是只跑一条。Team Lead 会围绕多个 GitHub Issue 管理任务队列、阶段状态、阻塞升级和角色协同，让多个任务可以并行推进，同时保持每条链路各自可追踪、可恢复、可验收。

## 默认角色与边界

Team Lead 是流程编排与升级协调的唯一负责人，不是一个可以重复创建的普通 Agent。QA Engineer 不只负责测试，还负责把 PRD 验收标准和 Tech 验证路径转成可追溯的 QA Case，并在关键 Gate 门控环节持有质量结论。

| 启用方式 | 角色 | 一句话职责 | 定义文档 |
| --- | --- | --- | --- |
| 默认 | 团队负责人（Team Lead） | 负责团队节奏、流程完整性、多个 Issue 的并行编排、跨角色协同和升级协调。 | [team-lead.md](./skills/shared/agents/team-lead.md) |
| 默认 | 产品经理（Product Manager） | 负责把用户问题、业务目标或既有人类 PRD，转成可评审、可实现、可验收且可供其他 Agent 读取的正式交付物。 | [product-manager.md](./skills/shared/agents/product-manager.md) |
| 默认 | 架构师（Architect） | 负责技术可行性判断、架构与接口收敛、Tech Spec 产出以及技术 Gate 门控守门。 | [architect.md](./skills/shared/agents/architect.md) |
| 默认 | 质量工程师（QA Engineer） | 负责 QA Case Design、验证执行、测试报告、PRD 追溯和质量 Gate 门控。 | [qa-engineer.md](./skills/shared/agents/qa-engineer.md) |
| 默认 | 工程师（Engineer） | 负责把已确认的设计转成代码、测试和实现证据。 | [engineer.md](./skills/shared/agents/engineer.md) |
| 默认 | 平台与发布负责人（Platform / SRE） | 负责环境稳定性、CI 与自动化检查、部署准备、回滚能力和发布风险控制。 | [platform-sre.md](./skills/shared/agents/platform-sre.md) |
| 默认 | PMO | 负责流程合规检查、协同问题沉淀和机制改进，驱动流程改进闭环，但不代替正式签字角色。 | [pmo.md](./skills/shared/agents/pmo.md) |

## 协作通道与入口

当前桌面端的主入口通常是 Claude 或 Codex。这样做适合同步编排，但用户一旦离开电脑，移动端实时沟通和状态跟进就容易断掉。

因此，AgentDevFlow 把 `Claude / Codex`、`GitHub Issue`、`Telegram`，以及未来可扩展的 `飞书 CLI`、`Discord` 等能力统一看作协作入口，而不是孤立工具。

其中：

- `Claude / Codex`：桌面端主会话编排、角色启动和同步推进入口
- `GitHub Issue`：正式流程主线，负责挂接过程产出物、状态、评论、Gate 门控结论和最终验收关闭
- `Telegram`：移动端实时沟通与 Team Lead 回复闭环入口
- `飞书 CLI / Discord`：后续可扩展的更多协作通道

Telegram 配置与接入说明见 [Telegram 通道接入](./docs/channels/telegram.md)。

## 流程如何被保障

当你已经理解了主线流程，再看这一节会更容易明白 AgentDevFlow 的差异点：它不只描述一套协作方法，也尽量把关键约束落到自动化、检查点和闭环里。

### Gate 门控已自动化

- 文档 PR 会检查 PRD、Tech、QA 文档是否包含 Gate 门控块和签字状态
- 本地 `.githooks/pre-commit` 会对受保护文档目录执行 Gate 门控检查
- 缺少关键签字时，流程会被直接阻断

### 代码 PR 有前置约束

- 是否关联对应 Issue
- 是否包含文档 PR 链接
- 是否满足 `Fixes #N` 或 `Closes #N`
- Issue 下是否已有关键 Agent Comment 和产物留痕

### 一致性有专门约束

- 仓库已有 PRD / Tech / 代码一致性变更管理规范
- Issue 标题执行命名格式校验
- 变更等级与是否需要重新触发 Gate 门控评审被明确化

### Telegram 已形成闭环

- 用户消息进入 `.claude/task_queue`
- `task_router` 将 Telegram 任务路由给 Team Lead
- Team Lead 回复可通过 `response_forwarder` 回传原始用户

## 快速接入

### 1. 安装

当前仓库提供安装脚本：

```bash
./scripts/install.sh --dry-run
./scripts/install.sh --channel dev --target ~/.claude
```

说明：

- `scripts/install.sh` 当前主要用于安装 Claude 本地技能包
- `--channel stable` 安装稳定版本
- `--channel dev` 安装当前仓库中的开发版本
- 默认目标目录是 `~/.claude`
- 如果要先预览改动，先执行 `--dry-run`

### 2. 最少必读

如果你想先跑通一遍最小流程，至少先读：

1. [核心原则](./docs/governance/core-principles.md)
2. [交付 Gate 门控](./prompts/004_delivery_gates.md)
3. [Issue 与评审评论机制](./prompts/013_github_issue_and_review_comments.md)
4. [双阶段 PR 与三层保障](./prompts/019_dual_stage_pr_and_three_layer_safeguard.md)

### 3. 跑通最小路径

建议第一次试用按这条最短路径走：

1. 创建一个主 GitHub Issue
2. 产出 PRD、Tech Spec、QA Case Design
3. 提交文档 PR，并完成 Human Review #1
4. 由 Engineer 基于已确认输入实现
5. 由 QA 按 case 验证并形成 QA 结论
6. 提交代码 PR，并完成 Human Review #2
7. 在 Issue 上完成结论回写与关闭

## FAQ

### AgentDevFlow 和 gstack / superpower 有什么区别？

三者解决的不是同一层问题。

- `gstack` / `superpower` 更偏 **单个 Agent 的能力增强层**
- `AgentDevFlow` 更偏 **多 Agent 的交付流程层**

从技术分层看：

- `gstack`：偏工具与任务工作流，增强单个 Agent 的执行能力
- `superpower`：偏通用方法论与执行模式，增强单个 Agent 的规划、拆解和协作能力
- `AgentDevFlow`：定义多 Agent 围绕 `Issue / PRD / Tech / QA / Gate / Human Review / Release` 的正式协作机制

所以它们不是简单替代关系，而是不同层级、可以叠加：

- 前者负责让 **单个 Agent 更强**
- 后者负责让 **多个 Agent 真正像研发团队一样协作交付**

如果只用一句话概括：

**`gstack / superpower` 解决“Agent 怎么更会做事”，`AgentDevFlow` 解决“多个 Agent 怎么稳定交付”。`**

## 继续阅读

### 理解机制必读

1. [核心原则](./docs/governance/core-principles.md)
2. [交付 Gate 门控](./prompts/004_delivery_gates.md)
3. [Issue 与评审评论机制](./prompts/013_github_issue_and_review_comments.md)
4. [双阶段 PR 与三层保障](./prompts/019_dual_stage_pr_and_three_layer_safeguard.md)

### 接入平台必读

1. [Claude 接入](./docs/platforms/claude-code.md)
2. [能力增强层](./docs/platforms/enhancement-layer.md)
3. [插件入口](./plugins/agentdevflow/README.md)
3. [共享技能目录](./skills/shared/README.md)

### 通道接入

1. [Telegram 通道接入](./docs/channels/telegram.md)

## 问题反馈

如果你发现问题或有改进建议，欢迎通过 GitHub Issue 反馈。
