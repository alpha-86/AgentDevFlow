# 双阶段 PR 与三层保障体系

## 目标

把“设计确认”和“实现确认”拆成两个明确的人机协同节点，并建立避免流程被绕过的三层保障体系。

## 为什么需要双阶段

如果文档设计和代码交付混在同一个模糊流程里，会出现三类问题：

- 设计是否被确认不清楚
- Human Review 到底 review 了什么不清楚
- QA 介入时机和验收边界不清楚

## 双阶段定义

### 阶段 1：文档阶段

- 分支：`doc-{issue}-{描述}`
- PR 类型：文档 PR
- 产物：PRD、Tech、QA Case Design
- 目标：锁定需求、方案、测试思路
- Human Review：确认设计可以进入实现
- 结果：文档 PR 合并 = 设计确认；之后才能正式开始开发

### 阶段 2：实现阶段

- 分支：`feature-{issue}-{描述}`
- PR 类型：代码 PR
- 前置：文档 PR 已合并
- 产物：代码、测试、测试报告、发布准备
- 目标：确认实现与设计一致且可交付
- Human Review：确认代码/交付物可以进入发布或验收完成
- 结果：代码 PR 合并 = 实现确认；之后才能关闭 Issue 或完成发布

## PR 内容最小要求

### 文档 PR

- PRD 链接
- Tech 链接
- QA Case Design 链接
- 主 Issue 链接
- 变更摘要
- 明确写出“合并即设计确认，可以进入开发”

### 代码 PR

- 已合并的文档 PR 链接
- 测试报告链接
- 代码变更摘要
- 关联 Issue
- 明确写出“合并即实现确认，可以进入关闭或发布”

## PR 合并前置条件

### 文档 PR 合并前

- PRD、Tech、QA Case Design 已齐备
- Human Review #1 结论已形成正式留痕
- 主 Issue 中已能反查文档 PR 和当前 Gate Comment

### 代码 PR 合并前

- 已合并的文档 PR 链接已存在
- 测试报告已齐备
- Human Review #2 结论已形成正式留痕
- 主 Issue 中已能反查代码 PR、测试报告和当前 Gate Comment

## Human Review 最小要求

- reviewer 身份明确
- 评审对象明确
- 结论明确（Approved / Conditional / Rejected）
- 证据链接明确
- 是否允许进入下游阶段明确

## 三层保障体系

### 第一层：流程规则

- Prompt / Workflow / Template 明确阶段、签字、退回条件
- Team Lead / PM / Architect / QA 持有强规则
- 没有当前阶段通过结论，不得推进下游
- 文档 PR 未合并，不得指派正式开发
- QA Case Design 必须作为文档 PR 组成部分前置确认

### 第二层：执行留痕

- Issue Comment
- Memo
- Review Record
- Change Record
- Todo Registry

要求：

- 所有关键结论都必须进入正式留痕对象
- 口头确认不具备流程效力

### 第三层：平台与自动化检查

- Branch Protection / PR Template / Merge Gate
- 文档 PR 完整性检查
- 代码 PR 前置条件检查
- Issue 状态一致性检查
- Comment / artifact linkage 检查

说明：

- AgentDevFlow 不绑定某个特定平台实现
- 但任何平台适配都应该提供等价的自动化保障

## 纯文档交付说明

纯文档交付与开发交付同等重要，其路径为：文档 PR → Human Review #1 → Release → Issue Close，不经过实现阶段（Gate 3）和代码 PR（Gate 4）。HR#1 的 Human review / merge decision 对纯文档交付仍然不可跳过。

## 强制规则

- 文档阶段未确认，不得正式进入实现阶段
- 实现阶段未确认，不得正式关闭 Issue 或发布
- 纯文档交付也必须完成 Human Review #1 后方可进入 Release
- 文档 PR 必须同时包含 PRD、Tech、QA Case Design
- 代码 PR 必须包含文档 PR 链接和测试报告
- QA 测试报告不得缺席实现阶段确认
- Major / Breaking 变更必须判断是否回退到文档阶段重新确认

## 失败信号

- 文档和代码混在一个无法区分的确认节点里
- Human Review 没有明确对象
- 设计未确认就开始实现
- 实现已变更但文档阶段结论未更新
- QA Case Design 未前置到文档阶段
- 代码 PR 与文档 PR 之间没有可追溯关联
