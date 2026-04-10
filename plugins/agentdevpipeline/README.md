# AgentDevPipeline 插件入口

## 定位

`agentdevpipeline` 不是重新发明一套流程，而是把 `hedge-ai` 中可迁移的研发工作机制拆出来，沉淀成可被不同 Agent 入口加载的独立插件资产。

这个插件只保留通用研发语义，不保留量化交易业务语义。

## 当前阶段交付什么

当前插件入口主要承载四类资产：

1. 共享角色、workflow、template  
   来自 `skills/shared/`

2. 中文规则层  
   来自 `prompts/`

3. 中文说明与治理文档  
   来自 `docs/`

4. 迁移审计依据  
   来自 `docs/migration/hedge-ai-plugin-migration-matrix.md`

当前插件入口只面向中文单线仓库。

## 插件主线机制

本插件当前收口的主线机制是：

- Issue First
- 问题先于方案
- 双阶段 PR
- Human Review
- Issue Comment Gate
- PMO / Process Auditor 主动检查
- Memo / Todo / Change Record 正式留痕

这些机制都必须能回溯到 `hedge-ai/prompts/V3.0` 或 `.claude/skills` 源文件。

## 插件资产装载关系

从插件视角，当前仓库的核心装载关系如下：

1. 根 [README.md](/home/work/code/agentdevpipeline/README.md)
   负责说明插件解决什么问题、主流程是什么。

2. [docs/README.md](/home/work/code/agentdevpipeline/docs/README.md)
   负责中文总览。

3. [skills/shared/README.md](/home/work/code/agentdevpipeline/skills/shared/README.md)  
   负责共享角色、workflow、template 的入口。

4. [hedge-ai-plugin-migration-matrix.md](/home/work/code/agentdevpipeline/docs/migration/hedge-ai-plugin-migration-matrix.md)
   负责记录源文档、当前落点和插件落点。

## 当前插件最重要的共享资产

### 1. 共享协议与入口

- [team-setup.md](/home/work/code/agentdevpipeline/skills/shared/team-setup.md)
- [start-agent-team.md](/home/work/code/agentdevpipeline/skills/shared/start-agent-team.md)
- [create-agent.md](/home/work/code/agentdevpipeline/skills/shared/create-agent.md)
- [skill-protocol.md](/home/work/code/agentdevpipeline/skills/shared/skill-protocol.md)

### 2. 共享角色

- [team-lead.md](/home/work/code/agentdevpipeline/skills/shared/agents/team-lead.md)
- [product-manager.md](/home/work/code/agentdevpipeline/skills/shared/agents/product-manager.md)
- [tech-lead.md](/home/work/code/agentdevpipeline/skills/shared/agents/tech-lead.md)
- [engineer.md](/home/work/code/agentdevpipeline/skills/shared/agents/engineer.md)
- [qa-engineer.md](/home/work/code/agentdevpipeline/skills/shared/agents/qa-engineer.md)
- [platform-sre.md](/home/work/code/agentdevpipeline/skills/shared/agents/platform-sre.md)
- [process-auditor.md](/home/work/code/agentdevpipeline/skills/shared/agents/process-auditor.md)

### 3. 共享 workflow

- [prd-review.md](/home/work/code/agentdevpipeline/skills/shared/workflows/prd-review.md)
- [tech-review.md](/home/work/code/agentdevpipeline/skills/shared/workflows/tech-review.md)
- [human-review.md](/home/work/code/agentdevpipeline/skills/shared/workflows/human-review.md)
- [daily-sync.md](/home/work/code/agentdevpipeline/skills/shared/workflows/daily-sync.md)
- [todo-review.md](/home/work/code/agentdevpipeline/skills/shared/workflows/todo-review.md)
- [weekly-review.md](/home/work/code/agentdevpipeline/skills/shared/workflows/weekly-review.md)
- [monthly-review.md](/home/work/code/agentdevpipeline/skills/shared/workflows/monthly-review.md)

### 4. 中文规则层

- [007_issue_driven_orchestration.md](/home/work/code/agentdevpipeline/prompts/007_issue_driven_orchestration.md)
- [014_process_compliance_and_audit.md](/home/work/code/agentdevpipeline/prompts/014_process_compliance_and_audit.md)
- [017_human_review_and_signoff.md](/home/work/code/agentdevpipeline/prompts/017_human_review_and_signoff.md)
- [019_dual_stage_pr_and_three_layer_safeguard.md](/home/work/code/agentdevpipeline/prompts/019_dual_stage_pr_and_three_layer_safeguard.md)
- [020_issue_comment_gate_and_artifact_linkage.md](/home/work/code/agentdevpipeline/prompts/020_issue_comment_gate_and_artifact_linkage.md)

## 规则边界

- 不得新增 `hedge-ai` 源文档中不存在的核心流程概念
- 不得把量化交易角色、交易节奏、策略研究、因子、回测等内容带入插件主干
- 不得由插件层改写 `skills/shared/` 的核心语义
- 当前阶段不保留任何其他语言镜像入口规划

## 当前仍未完成的部分

- `github-issue/SKILL.md`、`review-org/SKILL.md` 还需要更明确的插件承载方式
- evaluation checker 还未形成更接近 `hedge-ai` 的独立检查子能力
