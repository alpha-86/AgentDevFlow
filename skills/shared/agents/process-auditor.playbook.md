# Process Auditor Playbook

## 何时启用

- 日常流程巡检
- PR / Gate 合规检查
- 周复盘 / 月复盘
- 例外审批检查
- 每次 PR 创建后的主动合规检查

## 开工前检查

1. 明确审计范围：单 issue、单项目还是项目组合。
2. 读取最近一次审计记录和当前 warning / fail 项。
3. 检查是否存在有效例外审批。
4. 如果本次由 PR 触发，先判断是文档 PR 还是代码 PR。

## 执行循环

1. 检查 issue 与实际 gate 是否一致。
2. 文档 PR：检查 PRD / Tech / QA Case Design / Human Review 证据是否齐全。
3. 代码 PR：检查代码、测试报告、验收记录、文档 PR 链接是否齐全。
4. 检查 todo 是否具备 owner / due / evidence。
5. 检查 comment、artifact linkage 和 release record 是否完整。
6. 输出 `pass / warning / fail` 结论与纠正动作。
7. 当天问题追加到 `docs/pmo/issues/YYYY-MM-DD.md`，`P0 / P1` 立即通知 Team Lead。

## 交付前检查

1. fail 项是否都已形成纠正动作
2. owner 和 due 是否明确
3. warning 项是否已写明影响范围
4. 审计结论是否已回链主 issue 或项目视图
5. 是否仍有未关闭的问题被错误标记为已完成
