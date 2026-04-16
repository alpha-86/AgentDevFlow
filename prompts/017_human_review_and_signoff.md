# Human Review 与签字机制

## 目标

明确哪些交付物必须进入 Human Review，谁来 review，以什么形式 review，以及 review 结论如何影响后续流程。

## 核心原则

- Agent 可以起草、整理、预审，但关键交付物不能只在 Agent 内部自循环。
- Human Review 的对象、时机、形式、结论必须显式定义。
- 没有正式签字或确认记录，不视为已通过。

## 必须进入 Human Review 的对象

- 文档 PR 中的 PRD
- 文档 PR 中的 Tech Spec
- 文档 PR 中的 QA Case Design
- 代码 PR
- 发布放行
- Major / Breaking Change
- 例外审批

## 双阶段 Human Review 主线

### 阶段 1：设计确认

- 载体：文档 PR
- 最小内容：PRD + Tech + QA Case Design
- **Human Review #1 通过后，才允许进入开发阶段（强制，不可跳过）**
- 文档 PR 合并，代表设计正式确认

### 阶段 2：实现确认

- 载体：代码 PR
- 最小内容：代码变更 + 测试报告 + 文档 PR 链接
- Human Review 通过后，才允许进入关闭或发布阶段
- 代码 PR 合并，代表实现正式确认

## 推荐 Review 形式

- 文档 Review
- Pull Request Review
- Issue Comment Confirm
- Release Approval

## 结论类型

- `Approved`
- `Conditional`
- `Rejected`

## 结论处理规则

### Approved

- 可以进入下游阶段
- 必须记录 reviewer、日期、证据链接

### Conditional

- 必须记录条件项、owner、due date
- 条件项关闭前不得进入下游

### Rejected

- 必须回到当前阶段修订
- 必须说明最关键失败原因

## 签字最小要求

- PRD：PM + Tech Lead
- Tech：Tech Lead + QA + PM 确认
- QA Case Design：QA 产出，PM + Tech Lead + Engineer 确认
- QA：QA + PM
- Release：PM + Tech Lead + Platform/SRE

## 双阶段 PR 的最小确认条件

### 文档 PR

- PRD 已完成
- Tech 已完成
- QA Case Design 已完成
- Review 结论已写回 PR / Issue / Memo

### 代码 PR

- 文档 PR 已合并
- 代码实现已完成
- 测试报告已完成
- Review 结论已写回 PR / Issue / Memo

## 禁止行为

- 口头说通过但不留正式记录
- 只让 Agent 自评就视为通过
- Conditional 未关闭就进入下游
- 用聊天摘要替代签字记录
- 文档 PR 未合并就启动正式开发
- 代码 PR 不附文档 PR 链接或测试报告
- **Human Review #1 未完成就进入实现阶段（强制禁止）**

## Human Review #1 强制规范

Human Review #1 评审 **PRD、Tech Spec、Case 设计文档** 三类文档，与交付方式无关：

| 文档类型 | 评审重点 | 与实现方式的关系 |
|---------|---------|----------------|
| PRD | 问题描述、期望达成的能力和效果 | 独立于实现方式 |
| Tech Spec | 如何拆解和实现 PRD 要求的能力，解决 PRD 的问题 | 独立于实现方式 |
| Case 设计文档 | 如何验证是否达成效果 | 独立于实现方式 |

**关键原则**：`*.md` 文档是本项目的实现层。"纯文档交付"不是可以跳过 HR#1 的理由。

**不存在任何可以跳过 Human Review #1 的情况。**

Gate 2 → Human Review #1 → Gate 3 → Gate 4 是强制顺序，不得颠倒或跳过。

## Human Review #1 之后的路径

HR#1 通过后，流程按以下顺序推进：

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
Engineer 收到通知，开始 Implementation（Gate 3）
```

**PM 的职责到此结束（文档阶段交付完整）**，后续是 Human 和 Engineer 的工作。

> 详细流程定义见 `prompts/002_develop_pipeline.md`。
