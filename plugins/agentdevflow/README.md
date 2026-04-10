# AgentDevFlow 插件入口

这个目录提供的是 **Codex 侧的 AgentDevFlow 启动入口**。目标不是复制整套规则，而是把 Codex 的多 agent 能力接到本仓库的共享资产上。

## 插件启动顺序

在 Codex 中接入 AgentDevFlow 时，按这个顺序执行：

1. 读取 [README.md](/home/work/code/AgentDevFlow/README.md)
2. 读取 [docs/README.md](/home/work/code/AgentDevFlow/docs/README.md)
3. 读取 [core-principles.md](/home/work/code/AgentDevFlow/docs/governance/core-principles.md)
4. 读取 [start-agent-team.md](/home/work/code/AgentDevFlow/skills/shared/start-agent-team.md)
5. 读取 [create-agent.md](/home/work/code/AgentDevFlow/skills/shared/create-agent.md)
6. 决定默认团队和本轮主 issue
7. 再创建 Product Manager / 架构师 / QA / Engineer 等角色 subagent

## Codex 侧运行模型

Codex 侧的主会话承担 `Team Lead 等效编排者` 职责：

- 建立主 issue、当前 Gate、Todo 和状态板
- 决定本轮需要哪些角色
- 用 `spawn_agent` 创建角色 subagent
- 控制文档阶段和实现阶段的先后顺序
- 在关键节点统一把守 Human Review 和 Issue Comment Gate

这不是新增角色，而是 Codex 宿主差异下的承载方式。

## 默认角色

默认启用：

- Team Lead 等效编排者（主会话承担）
- Product Manager
- 架构师
- QA Engineer
- Engineer
- Platform/SRE
- Process Auditor

按需启用：

- 研究支持

## 必读共享资产

共享入口：

- [team-setup.md](/home/work/code/AgentDevFlow/skills/shared/team-setup.md)
- [start-agent-team.md](/home/work/code/AgentDevFlow/skills/shared/start-agent-team.md)
- [create-agent.md](/home/work/code/AgentDevFlow/skills/shared/create-agent.md)
- [skill-protocol.md](/home/work/code/AgentDevFlow/skills/shared/skill-protocol.md)

关键角色：

- [team-lead.md](/home/work/code/AgentDevFlow/skills/shared/agents/team-lead.md)
- [product-manager.md](/home/work/code/AgentDevFlow/skills/shared/agents/product-manager.md)
- [architect.md](/home/work/code/AgentDevFlow/skills/shared/agents/architect.md)
- [qa-engineer.md](/home/work/code/AgentDevFlow/skills/shared/agents/qa-engineer.md)
- [engineer.md](/home/work/code/AgentDevFlow/skills/shared/agents/engineer.md)
- [platform-sre.md](/home/work/code/AgentDevFlow/skills/shared/agents/platform-sre.md)
- [process-auditor.md](/home/work/code/AgentDevFlow/skills/shared/agents/process-auditor.md)

关键规则：

- [004_delivery_gates.md](/home/work/code/AgentDevFlow/prompts/004_delivery_gates.md)
- [013_github_issue_and_review_comments.md](/home/work/code/AgentDevFlow/prompts/013_github_issue_and_review_comments.md)
- [019_dual_stage_pr_and_three_layer_safeguard.md](/home/work/code/AgentDevFlow/prompts/019_dual_stage_pr_and_three_layer_safeguard.md)

## 最小通过标准

一个 Codex 项目只有同时满足下列条件，才能算“已接入 AgentDevFlow”：

1. 主会话先读共享入口再创建角色
2. 文档阶段先于实现阶段
3. 默认团队与可选团队边界明确
4. Issue / Gate / Comment / Human Review 主线可追溯
5. subagent 都有清晰职责和写入范围

## 依赖原则

AgentDevFlow 优先复用现成能力，不重复造轮子。

直接复用：

- Codex 多 agent 调度能力
- Git / Issue / PR / CI / `gh`
- 已有 skills、plugin、agents 包

完整依赖说明见 [dependencies.md](/home/work/code/AgentDevFlow/docs/reference/dependencies.md)。
