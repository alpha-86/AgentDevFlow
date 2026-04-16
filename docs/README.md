# AgentDevFlow 文档总览

## 定位

AgentDevFlow 是一套自包含的通用产研 Agent 能力包，目标是把可复用的产品研发流程、角色约束、文档规范、会议与 Todo 机制沉淀为独立仓库，供 Claude、Codex、OpenCode 等环境复用。

## 项目定位

- AgentDevFlow 是一个全新独立的项目
- 目标是提供完整的多 Agent 研发流程编排能力
- 强调全流程自动化，同时保持过程可控、可追溯、可复盘
- 所有文档、提示词、技能、工作流、模板都维护在本仓库内

## 文档组织方式

- `docs/` 只保留中文单线文档。
- 目录按内容语义组织，不再按语言组织。
- 所有需求变更、提示词调整、工作流迭代都直接回写到当前目录结构。
- 历史上的多语言镜像策略已停止使用。

## 核心能力范围

- 团队负责人 / 产品经理 / 架构师 / 工程师 / 质量工程师 / 平台与发布负责人 / PMO 的角色定义与协作边界
- PRD Gate、Tech Gate、QA Gate、Release Gate 组成的端到端交付流程
- 文档规范、会议纪要、Todo 闭环、Issue 驱动交付等过程治理机制
- Agent 创建规范、平台适配约束和跨平台接入方式
- 面向自动化编排的共享 prompts、workflows、templates、playbooks

## 阅读顺序

1. [仓库结构图](./architecture/repository-map.md)
2. [依赖清单](./reference/dependencies.md)
3. [外部复用调研](./reference/reuse-survey.md)
4. [治理目录](./governance/README.md)
5. [核心原则](./governance/core-principles.md)
6. [共享技能使用协议](./governance/skill-protocol.md)
7. `prompts/discuss/` 中的复核与讨论记录
8. 平台与沟通通道接入文档
9. `prompts/` 中的 Issue / 变更 / 异常 / 合规机制
10. `skills/` 中的角色、workflow、template
11. `skills/team-setup.md`
12. `skills/start-agent-team.md`
13. `skills/create-agent.md`
14. `skills/skill-protocol.md`
15. `skills/event-bus.md`
16. `skills/agents/pmo.md` 与其他角色文件

## 可直接使用的交付目录

- [PRD](/home/work/code/AgentDevFlow/docs/prd/README.md)
- [Tech](/home/work/code/AgentDevFlow/docs/tech/README.md)
- [QA](/home/work/code/AgentDevFlow/docs/qa/README.md)
- [Memo](/home/work/code/AgentDevFlow/docs/memo/README.md)
- [Todo](/home/work/code/AgentDevFlow/docs/todo/README.md)
- [Release](/home/work/code/AgentDevFlow/docs/release/README.md)

## 最小可运行示例

- [Kickoff 示例纪要](/home/work/code/AgentDevFlow/docs/memo/kickoff_2026-04-09_agentdevflow_execution_example.md)
- [项目组合视图示例](/home/work/code/AgentDevFlow/docs/memo/project_portfolio_2026-04-09_example.md)
- [上下文恢复示例](/home/work/code/AgentDevFlow/docs/memo/context_recovery_2026-04-09_example.md)
- [审计报告示例](/home/work/code/AgentDevFlow/docs/memo/audit_2026-04-09_example.md)
- [产物关联表示例](/home/work/code/AgentDevFlow/docs/memo/artifact_linkage_2026-04-09_example.md)
- [平台检查失败示例](/home/work/code/AgentDevFlow/docs/memo/platform_check_failure_2026-04-09_example.md)
- [Agent 激活记录示例](/home/work/code/AgentDevFlow/docs/memo/agent_activation_2026-04-09_example.md)
- [Agent 创建日志示例](/home/work/code/AgentDevFlow/docs/memo/agent_creation_log_2026-04-09_example.md)
- [Issue Comment Gate 示例](/home/work/code/AgentDevFlow/docs/memo/issue_comment_gate_2026-04-09_example.md)
- [Issue Comment 缺失阻断示例](/home/work/code/AgentDevFlow/docs/memo/issue_comment_failure_2026-04-09_example.md)
- [项目状态板示例](/home/work/code/AgentDevFlow/docs/memo/project_status_board_2026-04-09_example.md)
- [平台检查清单示例](/home/work/code/AgentDevFlow/docs/memo/platform_checklist_2026-04-09_example.md)
- [QA 报告示例](/home/work/code/AgentDevFlow/docs/qa/001_user_notification_center_qa_report_2026-04-09.md)
- [发布记录示例](/home/work/code/AgentDevFlow/docs/release/001_release_record_example_2026-04-09.md)
- [待办注册表示例](/home/work/code/AgentDevFlow/docs/todo/TODO_REGISTRY.md)
