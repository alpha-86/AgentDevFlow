# Codex 平台最小检查样例

## 目标

说明在 Codex 插件或本地入口下，如何以最小实现满足 AgentDevFlow 的平台检查要求。

## 最小自动化链路

1. 读取主 issue、当前 gate 和关联产物。
2. 确认主会话是否已经完成启动前置条件。
3. 检查当前阶段所需 PRD / Tech / QA / Release 文档是否存在。
4. 检查对应 issue comment 是否存在且字段完整。
5. 检查 artifact linkage 是否完整。
6. 失败时输出平台检查结果并阻断继续推进。

## 最小落地物

- `skills/shared/templates/platform-checklist-template.md`
- `skills/shared/templates/platform-check-result-template.md`
- `docs/memo/platform_check_failure_2026-04-09_example.md`

## 常见失败

- 缺 Human Review 结论
- 缺 QA comment
- artifact linkage 缺失
- issue 状态提前推进
- 还没建立主 issue / Gate / Todo 就开始创建 subagent
