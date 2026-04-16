# TODO Registry

## 项目信息
- `project_id`: alpha-86/AgentDevFlow
- 主 issue: #1
- 当前阶段: Team Startup (2026-04-16 补充缺失角色)
- 启动方式: 补充创建 Engineer、Platform/SRE、PMO Agent 实例

## 角色分配

| 角色 | 状态 | Agent ID | 说明 |
|------|------|----------|------|
| Team Lead | ✅ | - | Claude Code (本会话，Human) |
| Product Manager | ✅ 已创建 | product-manager@alpha-86-AgentDevFlow | 子 Agent，初始化中 |
| 架构师 | ✅ 已创建 | architect@alpha-86-AgentDevFlow | 子 Agent，初始化中 |
| QA Engineer | ✅ 已创建 | qa-engineer@alpha-86-AgentDevFlow | 子 Agent，初始化中 |
| Engineer | 🔴 待创建 | - | 必须在推进前创建正式 Agent 实例 |
| Platform/SRE | 🔴 待创建 | - | 必须在推进前创建正式 Agent 实例 |
| PMO | 🔴 待创建 | - | 必须在推进前创建正式 Agent 实例 |

## 当前 Gate

- Gate 0: Team Startup (当前，2026-04-15 重新启动)
- Gate 1: PRD Review
- Gate 2: Tech Doc Review
- Gate 3: QA Case Review
- Gate 4: Doc PR Merge
- Gate 5: Code PR Merge
- Gate 6: Issue Close

## 启动会

- 时间: 2026-04-15
- 负责人: Team Lead
- 结论: 详见 docs/memo/2026-04-15-kickoff-memo.md

## 角色补充说明

**2026-04-16 修订**：根据 `skills/shared/start-agent-team.md` 规则，严禁 Team Lead 承担其他 Agent 职责。
- 所有角色必须正式实例化，不得以"临时承担"代替
- Engineer、Platform/SRE、PMO Agent 实例待创建
