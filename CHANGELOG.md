# 变更日志

本文件用于记录 AgentDevFlow 的正式版本变更。

## 维护规则

- 每次正式流程、插件入口、共享资产、规则层发生可追溯变更时，都必须更新本文件。
- 每个版本至少要写清：
  - 版本号
  - 日期
  - 标题
  - 状态
  - 变更原因
  - 核心内容
  - 涉及文件或落点
  - 详细记录链接
- 详细记录优先回链到：
  - `prompts/discuss/`
  - `docs/migration/`
- 没有进入 `CHANGELOG.md` 的重要变更，不应视为正式版本变更完成。
- 当前只维护中文单线仓库的正式版本记录。

## 版本主索引

| 版本 | 日期 | 标题 | 状态 |
|---|---|---|---|
| `0.3.1` | 2026-04-10 | 独立插件主线收口与 Phase 1-3.5 完整复核 | ✅ 已完成 |
| `0.3.0` | 2026-04-09 | 仓库主骨架与中文主版本初步建立 | ✅ 已完成 |
| `0.2.0` | 2026-04-09 | 中文规则层与共享执行层扩展 | ✅ 已完成 |
| `0.1.0` | 2026-04-09 | 初始自包含仓库骨架 | ✅ 已完成 |

## 0.3.1 - 2026-04-10

**标题**: 独立插件主线收口与 Phase 1-3.5 完整复核

**变更原因**:

- 仓库需要回到独立插件主线，确保插件入口、核心原则、README、插件 README、plugin 元数据均收口到位。
- 需要把源文档逐项复核并完成全链路收口。

**核心内容**:

- 完成 `prompts/V3.0`、`.claude/skills`、`change_record/`、`AGENTS/`、`WORKFLOWS/` 的 Phase 1 逐组复核
- 收口迁移矩阵，补齐 `github-issue.md`、`github-issue/SKILL.md`、`review-org/SKILL.md`
- 前置固化 `Issue First`、双阶段 PR、Issue Comment Gate、PMO 主动检查、核心原则和 README 主流程图
- 重写根 `README.md`，明确独立插件定位
- 重写 `plugins/agentdevflow/README.md`，作为插件入口
- 校准 `plugins/agentdevflow/.codex-plugin/plugin.json`
- 明确 `skills/shared/` 已基本构成插件核心资产层
- 明确 `prompts/` 已基本构成插件规则层

**涉及文件 / 落点**:

- `README.md`
- `plugins/agentdevflow/README.md`
- `plugins/agentdevflow/.codex-plugin/plugin.json`
- `docs/governance/core-principles.md`
- `docs/migration/hedge-ai-plugin-migration-matrix.md`
- `skills/shared/README.md`
- `prompts/README.md`
- `prompts/007_issue_driven_orchestration.md`
- `prompts/013_github_issue_and_review_comments.md`
- `prompts/014_process_compliance_and_audit.md`
- `prompts/017_human_review_and_signoff.md`
- `prompts/019_dual_stage_pr_and_three_layer_safeguard.md`
- `prompts/020_issue_comment_gate_and_artifact_linkage.md`

**详细记录**:

- `prompts/discuss/015_2026-04-10_独立插件目标总复核与纠偏.md`
- `prompts/discuss/016_2026-04-10_独立插件拆解执行计划.md`
- `prompts/discuss/016_phase_1_1_2026-04-10_README与CHANGELOG复核.md`
- `prompts/discuss/016_phase_1_2_2026-04-10_主文档001_016_019复核.md`
- `prompts/discuss/016_phase_1_3_2026-04-10_change_record复核.md`
- `prompts/discuss/016_phase_1_4_2026-04-10_skills顶层协议复核.md`
- `prompts/discuss/016_phase_1_5_2026-04-10_agents复核.md`
- `prompts/discuss/016_phase_1_6_2026-04-10_evaluation_checkers复核.md`
- `prompts/discuss/016_phase_1_7_2026-04-10_workflows复核.md`
- `prompts/discuss/016_phase_1_8_2026-04-10_逐文档迁移矩阵最终版收口.md`
- `prompts/discuss/016_phase_2_1_2026-04-10_issue机制复核.md`
- `prompts/discuss/016_phase_2_2_2026-04-10_双阶段PR机制复核.md`
- `prompts/discuss/016_phase_2_3_2026-04-10_issue_comment_gate复核.md`
- `prompts/discuss/016_phase_2_4_2026-04-10_PMO主动检查机制复核.md`
- `prompts/discuss/016_phase_2_5_2026-04-10_core_principles复核.md`
- `prompts/discuss/016_phase_2_6_2026-04-10_README流程图复核.md`
- `prompts/discuss/016_phase_3_1_2026-04-10_根README插件定位收口.md`
- `prompts/discuss/016_phase_3_2_2026-04-10_插件README收口.md`
- `prompts/discuss/016_phase_3_3_2026-04-10_plugin_json复核.md`
- `prompts/discuss/016_phase_3_4_2026-04-10_shared_skills核心资产复核.md`
- `prompts/discuss/016_phase_3_5_2026-04-10_prompt规则层复核.md`

## 0.3.0 - 2026-04-09

**标题**: 仓库主骨架与中文主版本初步建立

**变更原因**:

- 需要把仓库从零散文档整理成可继续迭代的中文主版本骨架。

**核心内容**:

- 建立交付目录骨架
- 建立共享角色与 playbook
- 建立 workflow 与 template 基础集合
- 建立中文 README 与中文治理文档

**涉及文件 / 落点**:

- `docs/prd/`
- `docs/tech/`
- `docs/qa/`
- `docs/memo/`
- `docs/todo/`
- `docs/release/`
- `skills/shared/agents/*`
- `skills/shared/workflows/*`
- `skills/shared/templates/*`
- `README.md`

## 0.2.0 - 2026-04-09

**标题**: 中文规则层与共享执行层扩展

**变更原因**:

- 需要把中文规则、角色约束和共享执行层从基础骨架扩展到可继续迁移的状态。

**核心内容**:

- 扩展共享角色规则
- 扩展交付阶段 workflow
- 扩展模板与追溯字段

## 0.1.0 - 2026-04-09

**标题**: 初始自包含仓库骨架

**变更原因**:

- 建立独立仓库和最初的目录结构。

**核心内容**:

- 初始化仓库结构
- 初始化中文主版本与适配层骨架
