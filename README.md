# AgentDevFlow

AgentDevFlow 是一套面向 AI Coding 研发交付的多 Agent 流程资产包。它关注的不是“单个 Agent 会不会写代码”，而是如何把 GitHub Issue 驱动、双阶段 PR 引入的人类评审、文件化交付物，以及两条彼此配合但职责不同的 AI 驱动 AI 闭环串成可执行流程：一条是 QA 与 Engineer 围绕 QA Case 的交付质量闭环，另一条是 PMO 驱动的流程改进闭环。

## 它解决什么问题

很多团队已经在用 Claude、Codex 或其他 Agent 工具，但真正容易失控的往往不是编码本身，而是协作过程：

- 对话式安排任务，很难确保 Agent 真正理解需求、边界和验收标准
- 关键信息如果停留在聊天里，上下文恢复成本很高，还会占用宝贵的上下文空间并干扰 AI
- 多个问题并行推进时，状态、依赖、优先级和责任边界的复杂性会快速爆炸，过程会越来越不可控
- 如果没有前置确认的 QA Case Design、设计确认和 QA 与 Engineer 的验证修复闭环，AI Coding 很容易持续偏离预期
- 人与 Agent Team 的桌面端主入口通常只有 Claude 或 Codex，离开电脑后移动端实时沟通和状态跟进容易断掉
- 不同平台各写一套规则，流程越做越碎，重复造轮子

AgentDevFlow 的目标，是把这些问题沉淀成一套可复用的 Agent、workflow、template 和平台入口约束：让 Agent 基于文件交付物协作，让人只在关键节点把关，一方面通过 QA 与 Engineer 的验证-修复循环提升交付质量，另一方面通过 PMO 持续发现流程问题并回写机制，持续优化整个 Agent 团队，使研发交付过程更可控、更符合预期、更高质量。

## 它怎么工作

AgentDevFlow 的主线不是“让 Agent 自己跑完一切”，而是建立一条 **以 Claude / Codex 为桌面端编排入口**、**以 GitHub Issue 为正式主线**、**以文件交付物为上下游唯一交接物**、**以双阶段 PR 引入 Human Review**、**以 QA Case Design 前置定义验证路径**、**以交付质量闭环和流程改进闭环并行运转** 的研发链路：

- `GitHub Issue 全流程`：从主 Issue 启动，所有关键产物和结论持续回链，最终也在 Issue 上完成验收与关闭
- `问题先于方案`：先澄清目标、边界、约束，再写 PRD，而不是让 Agent 直接根据聊天内容开工
- `文件交付物与文件交接`：PRD、Tech Spec、QA Case Design 是任务交付物，也是下游新任务的正式启动输入；Agent 与 Agent 之间的正式交接只认文件和结构化评论，不靠聊天接力
- `双阶段 PR`：文档 PR 合并代表设计确认，代码 PR 合并代表实现确认；两次确认都通过 Human Review 引入明确的人类判断
- `Case Design 先行的 TDD`：本项目语境的 TDD 指 QA Case Design 前置，并在 PR#1 / Human Review #1 中完成确认。它先定义测试覆盖和验收路径，但不等于 Engineer 按 QA Case Design 写实现；Engineer 的 coding 以已确认的 PRD 和 Tech Spec 为主输入
- `交付质量闭环`：QA 基于 PRD 和 Tech 设计或维护 QA Case Design，并在代码阶段按 case 验证实现、反馈缺陷、产出测试报告；Engineer 根据 QA 反馈修复问题，直到约定 case 通过并形成可审阅证据
- `Issue Comment Gate`：关键结论必须真正回写到 Issue，而不是停留在聊天里
- `PMO 流程改进闭环`：由于上下文干扰、执行漂移和幻觉，不能假设每个 Agent 都会 100% 按 prompt 执行；PMO 按 PR / Gate / 复盘主动检查流程、沉淀重复性协同问题，并把问题回写到 agent 描述、workflow、template、prompt 和文档要求
- `多通道沟通`：Claude / Codex 负责桌面端编排，GitHub Issue 承担正式流程主线，Telegram 提供移动端实时沟通能力，后续可扩展飞书 CLI、Discord 等更多沟通通道

换句话说，这里要区分两条并行闭环：一条是 `QA Case Design -> Engineer 实现 -> QA 验证 -> Engineer 修复 -> 测试报告` 的交付质量闭环；另一条是 `PMO 审计 -> 发现重复问题 -> 回写角色 / workflow / template / prompt / 文档要求 -> 下轮再执行` 的流程改进闭环。

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
Tech Spec + QA Case Design
文档阶段交付物
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
Issue Comment Gate
        │
        ▼
Release / 验收 / Human 关闭
```

上图展示的是交付主线。实际项目落地时，还需要把它和现实中的人类角色衔接起来：

- `已有人工 PRD 时`：如果现实中已经由人类 PM 完成了 PRD，PM Agent 的职责不是重新发明需求，而是与当前人类 PM 和工程师讨论对齐，把人类 PRD 整理成其他 Agent 可稳定读取、可评审、可追溯的正式 PRD，确保后续 Tech Spec、QA Case Design、实现和验证基于同一份语义
- `修 Bug 时`：即使只是修复一个 bug，也建议先由 PM Agent 把问题现象、影响范围、预期行为、复现线索和修复边界写清楚，再进入后续的 Tech、QA、Engineer 和 Review 流程，避免 Engineer 直接凭聊天和零散上下文开工
- `PMO 的位置`：PMO 不代替签字，也不替代交付质量闭环；它在文档 PR、代码 PR 和周期复盘中并行运行，持续主动检查流程、沉淀协同问题并推动机制改进

## 默认角色

| 启用方式 | 角色 | 一句话职责 | 定义文档 |
| --- | --- | --- | --- |
| 默认 | 团队负责人（Team Lead） | 负责团队节奏、流程完整性、跨角色协同和升级协调。 | [team-lead.md](./skills/shared/agents/team-lead.md) |
| 默认 | 产品经理（Product Manager） | 负责把用户问题、业务目标或既有人类 PRD，转成可评审、可实现、可验收且可供其他 Agent 读取的正式交付物。 | [product-manager.md](./skills/shared/agents/product-manager.md) |
| 默认 | 架构师（Architect） | 负责技术可行性判断、架构与接口收敛、Tech Spec 产出以及技术 Gate 守门。 | [architect.md](./skills/shared/agents/architect.md) |
| 默认 | 质量工程师（QA Engineer） | 负责测试设计、验证执行、测试报告和质量 Gate。 | [qa-engineer.md](./skills/shared/agents/qa-engineer.md) |
| 默认 | 工程师（Engineer） | 负责把已确认的设计转成代码、测试和实现证据。 | [engineer.md](./skills/shared/agents/engineer.md) |
| 默认 | 平台与发布负责人（Platform / SRE） | 负责环境稳定性、CI 与自动化检查、部署准备、回滚能力和发布风险控制。 | [platform-sre.md](./skills/shared/agents/platform-sre.md) |
| 默认 | PMO | 负责流程合规检查、协同问题沉淀和机制改进，驱动流程改进闭环，但不代替正式签字角色。 | [pmo.md](./skills/shared/agents/pmo.md) |

## 人与 Agent 的沟通通道

当前桌面端的主入口通常是 Claude 或 Codex。这样做适合同步编排，但用户一旦离开电脑，移动端实时沟通和状态跟进就容易断掉。

因此，AgentDevFlow 把 `Claude / Codex`、`GitHub Issue`、`Telegram`，以及未来可扩展的 `飞书 CLI`、`Discord` 等沟通通道统一看作协作通道，而不是孤立工具。

其中：

- `Claude / Codex` 负责桌面端主会话编排、角色启动和同步推进
- `GitHub Issue` 不只是沟通通道，还是 GitHub Issue 全流程的正式主线，负责挂接过程产出物、状态、评论、Gate 结论以及最终验收关闭
- `Telegram` 提供移动端实时沟通和状态跟进能力
- 后续可继续扩展 `飞书 CLI`、`Discord` 等更多沟通通道

Telegram 配置与接入说明见 [Telegram 通道接入](./docs/channels/telegram.md)。

## 如何安装

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

## 继续阅读

如果你要接入平台入口，可继续阅读：

1. [Claude 接入](./docs/platforms/claude-code.md)
2. [插件入口](./plugins/agentdevflow/README.md)
3. [共享技能目录](./skills/shared/README.md)

如果你想先理解这套机制，至少先读：

1. [核心原则](./docs/governance/core-principles.md)
2. [交付 Gate](./prompts/004_delivery_gates.md)
3. [Issue 与评审评论机制](./prompts/013_github_issue_and_review_comments.md)
4. [双阶段 PR 与三层保障](./prompts/019_dual_stage_pr_and_three_layer_safeguard.md)
5. [Telegram 通道接入](./docs/channels/telegram.md)

## 问题反馈

如果你发现问题或有改进建议，欢迎通过 GitHub Issue 反馈。
