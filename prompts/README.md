# AgentDevFlow Prompt 索引

这些文件是仓库当前使用的规则层。

## 文件列表

- `001_team_topology.md`
- `002_develop_pipeline.md` — **核心流程文档**，定义完整开发交付流程（Gate 0~5）、角色职责矩阵、Human 专属操作
- `002_product_engineering_roles.md`
- `003_document_contracts.md`
- `004_delivery_gates.md`
- `005_meeting_and_todo.md`
- `006_agent_creation_contract.md`
- `007_issue_driven_orchestration.md`
- `008_change_record_and_revalidation.md`
- `009_review_rigor_and_context_recovery.md`
- `010_team_setup_and_bootstrap.md`
- `011_event_bus_and_handoff.md`
- `012_anomaly_and_escalation_loop.md`
- `013_github_issue_and_review_comments.md`
- `014_process_compliance_and_audit.md`
- `015_review_evaluation_dimensions.md`
- `016_dual_track_delivery_mechanism.md`
- `017_human_review_and_signoff.md`
- `018_issue_routing_and_project_portfolio.md`
- `019_dual_stage_pr_and_three_layer_safeguard.md`
- `020_issue_comment_gate_and_artifact_linkage.md`
- `021_platform_checks_and_gate_automation.md`

## 配套共享能力

角色定义位于：

- `skills/`（如 `skills/product-manager/SKILL.md`）

当前角色包括：

- `product-manager/SKILL.md`
- `architect/SKILL.md`
- `engineer/SKILL.md`
- `qa-engineer/SKILL.md`
- `platform-sre/SKILL.md`
- `pmo/SKILL.md`
- `team-lead/SKILL.md`
- `agent-bootstrap/SKILL.md`
- `pmo-review/SKILL.md`
- `start-agent-team/SKILL.md`
- `team-setup/SKILL.md`

工作流位于：

- `skills/workflows/issue-lifecycle.md`
- `skills/workflows/human-review.md`
- `skills/workflows/project-portfolio-review.md`
- `skills/workflows/prd-review.md`
- `skills/workflows/tech-review.md`
- `skills/workflows/qa-validation.md`

模板位于：

- `skills/templates/prd-template.md`
- `skills/templates/tech-spec-template.md`
- `skills/templates/qa-case-template.md`
- `skills/templates/qa-report-template.md`
- `skills/templates/audit-report-template.md`
- `skills/templates/review-comment-template.md`

## 当前判定

`prompts/` 现在已经基本构成插件规则层，原因是它已经覆盖了插件主干所需的关键规则：

- 团队结构与角色边界
- 文档契约与交付 Gate
- 会议 / Todo / Agent 创建约束
- Issue First 与 Comment Gate
- 流程合规主动检查
- Human Review 与双阶段 PR
- 平台最小检查集合

但它还不是完全收口状态，当前主要缺口仍然是：

- 还缺更明确的 `github-issue/SKILL.md` 插件入口映射
- 还缺更明确的 `review-org/SKILL.md` 插件入口映射
- `015_review_evaluation_dimensions.md` 目前更像维度说明，还不是更独立的 checker 规则层承载
