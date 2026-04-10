# AgentDevPipeline 文档总览

## 定位

AgentDevPipeline 是一套自包含的通用产研 Agent 能力包，目标是把可复用的产品研发流程、角色约束、文档规范、会议与 Todo 机制沉淀为独立仓库，供 Claude、Codex、OpenCode 等环境复用。

## 项目定位

- AgentDevPipeline 是一个全新独立的项目
- 目标是提供完整的多 agent 研发流程编排能力
- 强调全流程自动化，同时保持过程可控、可追溯、可复盘
- 所有文档、prompts、skills、workflow、template 都维护在本仓库内

## 文档组织方式

- `docs/` 只保留中文单线文档。
- 目录按内容语义组织，不再按语言组织。
- 所有需求变更、prompt 调整、workflow 迭代都直接回写到当前目录结构。
- 历史上的多语言镜像策略已停止使用。

## 核心能力范围

- Team Lead / Product Manager / Tech Lead / Engineer / QA / Researcher / Platform/SRE / Process Auditor 的角色定义与协作边界
- PRD Gate、Tech Gate、QA Gate、Release Gate 组成的端到端交付流程
- 文档规范、会议纪要、Todo 闭环、Issue 驱动交付等过程治理机制
- Agent 创建规范、平台适配约束和跨平台接入方式
- 面向自动化编排的共享 prompts、workflows、templates、playbooks

## 与 hedge-ai 的边界

- hedge-ai 只作为流程参考样本，不是本项目运行依赖。
- 本项目严禁引入量化交易业务语义（角色、时段、报表、指标）。
- 保留通用研发日会机制，但日会内容必须使用通用产研语义。
- 详细约束见：[迁移边界（强约束）](/home/work/code/agentdevpipeline/docs/governance/migration-boundary-from-hedge-ai.md)

## 阅读顺序

1. [仓库结构图](/home/work/code/agentdevpipeline/docs/architecture/repository-map.md)
2. [依赖清单](/home/work/code/agentdevpipeline/docs/reference/dependencies.md)
3. [外部复用调研](/home/work/code/agentdevpipeline/docs/reference/reuse-survey.md)
4. [与 hedge-ai 的迁移边界（强约束）](/home/work/code/agentdevpipeline/docs/governance/migration-boundary-from-hedge-ai.md)
5. [hedge-ai 源文档清单与迁移判定](/home/work/code/agentdevpipeline/docs/migration/hedge-ai-source-inventory.md)
6. [可迁移机制落地计划](/home/work/code/agentdevpipeline/docs/migration/portable-mechanism-rollout-plan.md)
7. [完成度审计](/home/work/code/agentdevpipeline/docs/migration/completion-audit.md)
8. [与 hedge-ai 的对照审计](/home/work/code/agentdevpipeline/docs/migration/review-vs-hedge-ai.md)
9. [治理目录](/home/work/code/agentdevpipeline/docs/governance/README.md)
10. [核心原则](/home/work/code/agentdevpipeline/docs/governance/core-principles.md)
11. [Shared Skill 使用协议](/home/work/code/agentdevpipeline/docs/governance/skill-protocol.md)
12. `prompts/discuss/` 中的复核与讨论记录
13. 平台接入文档
14. `prompts/` 中的 Issue / 变更 / 异常 / 合规机制
15. `skills/shared/` 中的角色、workflow、template
16. `skills/shared/team-setup.md`
17. `skills/shared/start-agent-team.md`
18. `skills/shared/create-agent.md`
19. `skills/shared/skill-protocol.md`
20. `skills/shared/event-bus.md`
21. `skills/shared/agents/process-auditor.md` 与其他角色文件

## 可直接使用的交付目录

- [PRD](/home/work/code/agentdevpipeline/docs/prd/README.md)
- [Tech](/home/work/code/agentdevpipeline/docs/tech/README.md)
- [QA](/home/work/code/agentdevpipeline/docs/qa/README.md)
- [Memo](/home/work/code/agentdevpipeline/docs/memo/README.md)
- [Todo](/home/work/code/agentdevpipeline/docs/todo/README.md)
- [Research](/home/work/code/agentdevpipeline/docs/research/README.md)
- [Release](/home/work/code/agentdevpipeline/docs/release/README.md)

## 最小可运行示例

- [Kickoff 示例纪要](/home/work/code/agentdevpipeline/docs/memo/kickoff_2026-04-09_agentdevpipeline_execution_example.md)
- [项目组合视图示例](/home/work/code/agentdevpipeline/docs/memo/project_portfolio_2026-04-09_example.md)
- [上下文恢复示例](/home/work/code/agentdevpipeline/docs/memo/context_recovery_2026-04-09_example.md)
- [审计报告示例](/home/work/code/agentdevpipeline/docs/memo/audit_2026-04-09_example.md)
- [产物关联表示例](/home/work/code/agentdevpipeline/docs/memo/artifact_linkage_2026-04-09_example.md)
- [平台检查失败示例](/home/work/code/agentdevpipeline/docs/memo/platform_check_failure_2026-04-09_example.md)
- [Agent 激活记录示例](/home/work/code/agentdevpipeline/docs/memo/agent_activation_2026-04-09_example.md)
- [Agent 创建日志示例](/home/work/code/agentdevpipeline/docs/memo/agent_creation_log_2026-04-09_example.md)
- [Issue Comment Gate 示例](/home/work/code/agentdevpipeline/docs/memo/issue_comment_gate_2026-04-09_example.md)
- [Issue Comment 缺失阻断示例](/home/work/code/agentdevpipeline/docs/memo/issue_comment_failure_2026-04-09_example.md)
- [项目状态板示例](/home/work/code/agentdevpipeline/docs/memo/project_status_board_2026-04-09_example.md)
- [平台检查清单示例](/home/work/code/agentdevpipeline/docs/memo/platform_checklist_2026-04-09_example.md)
- [QA Report 示例](/home/work/code/agentdevpipeline/docs/qa/001_user_notification_center_qa_report_2026-04-09.md)
- [Release Record 示例](/home/work/code/agentdevpipeline/docs/release/001_release_record_example_2026-04-09.md)
- [Todo Registry](/home/work/code/agentdevpipeline/docs/todo/TODO_REGISTRY.md)
