# hedge-ai 可迁移机制落地完成度审计

## 结论

截至当前版本，hedge-ai 中大量“可迁移”和“部分迁移”的通用产研机制已经在 `agentdevpipeline` 当前仓库中形成主干，但不能再表述为“已基本完成拆解”。更准确的状态是：

- 主干机制已经形成可执行主线
- 边界已经明确
- 逐文档到插件落点的覆盖检查已经推进到 `Phase 7`
- 仍有少量插件入口与安装承载细节未完全收口

## 已落地的主干机制

### 组织与角色

- 团队拓扑与角色边界：`prompts/001_*`、`002_*`
- Team Lead 边界与角色强规则：`skills/shared/agents/*`
- 团队启动机制：`prompts/010_team_setup_and_bootstrap.md`

### 流程与 Gate

- 文档契约：`prompts/003_document_contracts.md`
- Gate 机制：`prompts/004_delivery_gates.md`
- 双轨交付：`prompts/016_dual_track_delivery_mechanism.md`
- 双阶段 PR 与 Comment Gate：`prompts/019_*`、`020_*`

### Issue / 评论 / 变更

- Issue 驱动：`prompts/007_issue_driven_orchestration.md`
- GitHub Issue 评论门禁：`prompts/013_github_issue_and_review_comments.md`
- 变更记录与重审：`prompts/008_change_record_and_revalidation.md`
- Issue 生命周期 workflow：`skills/shared/workflows/issue-lifecycle.md`

### 会议 / Todo / 异常 / 恢复

- 日会与 Todo：`prompts/005_meeting_and_todo.md`
- 异常升级闭环：`prompts/012_anomaly_and_escalation_loop.md`
- 上下文恢复：`prompts/009_review_rigor_and_context_recovery.md`
- 对应 workflows：`daily-sync.md`、`todo-review.md`、`anomaly-response.md`、`context-recovery.md`

### 合规与审计

- 流程合规：`prompts/014_process_compliance_and_audit.md`
- 周/月复盘：`skills/shared/workflows/weekly-review.md`、`monthly-review.md`
- Skill 协议：`docs/governance/skill-protocol.md`

### 评审评估

- 评审维度：`prompts/015_review_evaluation_dimensions.md`
- 检查器类型与模板字段：`prompts/015_*`、`review-comment-checklist-template.md`、`audit-report-template.md`
- Review Comment / Change Record / Handoff / Recovery / Anomaly 模板：`skills/shared/templates/*`

## 当前仍未完成的主缺口

- `github-issue/SKILL.md` 与 `review-org/SKILL.md` 仍缺更明确的插件落点
- 插件安装/装载说明仍可继续收紧
- 完成度审计仍需随着后续插件入口收口继续同步

## 明确排除

以下内容仍然保持禁止迁移状态：

- 基金经理、交易员、CRO/CSO（量化语境）
- 盘前、盘后、DBR、异常日报（交易运营语境）
- 因子研究、回测评审、策略辩论、持仓与回撤指标

详见：

- [迁移边界（强约束）](/home/work/code/agentdevpipeline/docs/governance/migration-boundary-from-hedge-ai.md)
- [源文档清单与迁移判定](/home/work/code/agentdevpipeline/docs/migration/hedge-ai-source-inventory.md)

## 审计口径

本审计当前表示“主干已成型，但仍未彻底收口为最终插件成品”。更严格的检查请以：

- [hedge-ai 研发机制拆解到独立插件的迁移矩阵](/home/work/code/agentdevpipeline/docs/migration/hedge-ai-plugin-migration-matrix.md)
- [围绕独立插件目标的总复核与纠偏](/home/work/code/agentdevpipeline/prompts/discuss/015_2026-04-10_围绕独立插件目标的总复核与纠偏.md)

为准。

本审计只覆盖当前中文单线仓库，不再包含其他语言镜像维度。
