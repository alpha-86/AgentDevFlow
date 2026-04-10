# Issue Comment Gate 与产物关联机制

## 目标

把 Issue Comment 从“可有可无的备注”提升为流程 Gate 的组成部分，并让多项目并行、多问题并行时的产物挂载关系保持清晰。

## 核心原则

- Issue Comment 是正式留痕，不是聊天补充
- 没有关键 Comment 的阶段，默认视为未完成
- 所有关键产物都必须能从 Issue 反查
- Comment 只有真正落到目标 Issue 上才算完成，生成待发送文件不算完成

## 必须存在 Comment 的时机

- PRD Review 结束
- Tech Review 结束
- Human Review #1 结束
- Implementation 交接 QA
- QA 结论输出
- Human Review #2 结束
- Release 决策输出
- Major / Breaking 变更
- 异常升级与关闭

## Comment 最小字段

- Gate / 阶段名称
- 决策人
- 结论
- 关键证据链接
- Action Items
- 下游是否允许推进

## 产物关联要求

每个主 Issue 下至少应能反查：

- PRD
- Tech
- QA Case
- Test Report
- Release Record
- Change Record（如有）
- 相关 PR / Merge 链接

建议使用统一的产物关联表模板。

## 多项目并行要求

- 每个 issue 必须挂到明确的 Project ID
- 每个项目必须可统计活跃 issue、blocked issue、超期 issue
- Team Lead 必须能在日会或周度复盘中读取项目组合视图

## 强制 Gate 规则

- 若当前阶段应有 Comment 但缺失，则该阶段不能视为完成
- 若 Comment 与正式文档状态不一致，则以较严格状态为准，并触发纠正
- 若产物链接缺失，则该阶段默认不能放行
- 若自动投递 Comment 失败，必须返回失败状态并阻断下游动作
- 代码 PR 创建前，必须确认主 Issue 已存在要求的上游 Comment
- 代码 PR 合并前，必须确认当前阶段 Comment 与产物链接完整

## 失败信号

- issue 有文档，但没有阶段 Comment
- comment 有结论，但没有证据链接
- PR / 文档 / 测试报告 无法回链主 issue
- 多项目并行时 issue 无法归属到 project
- 系统显示成功，但目标 Issue 下实际没有 Comment
