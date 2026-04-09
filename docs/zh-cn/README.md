# AgentDevPipeline 中文总览

## 定位

AgentDevPipeline 是一套自包含的通用产研 Agent 能力包，目标是把可复用的产品研发流程、角色约束、文档规范、会议与 Todo 机制沉淀为独立仓库，供 Claude、Codex、OpenCode 等环境复用。

## 项目定位

- AgentDevPipeline 是一个全新独立的项目
- 目标是提供完整的多 agent 研发流程编排能力
- 强调全流程自动化，同时保持过程可控、可追溯、可复盘
- 所有文档、prompts、skills、workflow、template 都维护在本仓库内

## 中文与英文的关系

- `docs/zh-cn/` 和 `prompts/zh-cn/` 是内部主版本。
- `docs/en/` 和 `prompts/en/` 是对外发布版本。
- 任何需求变更、prompt 调整、workflow 迭代，必须先修改中文，再翻译英文。
- 英文版只反映已发布内容，不抢跑内部设计。

## 核心能力范围

- Team Lead / Product Manager / Tech Lead / Engineer / QA / Researcher / SRE 的角色定义与协作边界
- PRD Gate、Tech Gate、QA Gate、Release Gate 组成的端到端交付流程
- 文档规范、会议纪要、Todo 闭环、Issue 驱动交付等过程治理机制
- Agent 创建规范、平台适配约束和跨平台接入方式
- 面向自动化编排的共享 prompts、workflows、templates、playbooks

## 与 hedge-ai 的边界

- hedge-ai 只作为流程参考样本，不是本项目运行依赖。
- 本项目严禁引入量化交易业务语义（角色、时段、报表、指标）。
- 保留通用研发日会机制，但日会内容必须使用通用产研语义。
- 详细约束见：[迁移边界（强约束）](/home/work/code/agentdevpipeline/docs/zh-cn/reference/migration-boundary-from-hedge-ai.md)

## 阅读顺序

1. [仓库结构图](/home/work/code/agentdevpipeline/docs/zh-cn/architecture/repository-map.md)
2. [依赖清单](/home/work/code/agentdevpipeline/docs/zh-cn/reference/dependencies.md)
3. [语言治理](/home/work/code/agentdevpipeline/docs/zh-cn/reference/localization-policy.md)
4. [外部复用调研](/home/work/code/agentdevpipeline/docs/zh-cn/reference/reuse-survey.md)
5. [与 hedge-ai 的迁移边界（强约束）](/home/work/code/agentdevpipeline/docs/zh-cn/reference/migration-boundary-from-hedge-ai.md)
6. [hedge-ai 源文档清单与迁移判定](/home/work/code/agentdevpipeline/docs/zh-cn/migration/hedge-ai-source-inventory.md)
7. [可迁移机制落地计划](/home/work/code/agentdevpipeline/docs/zh-cn/migration/portable-mechanism-rollout-plan.md)
8. 平台接入文档
9. `prompts/zh-cn/` 与 `skills/shared/`

## 可直接使用的交付目录

- [PRD](/home/work/code/agentdevpipeline/docs/prd/README.md)
- [Tech](/home/work/code/agentdevpipeline/docs/tech/README.md)
- [QA](/home/work/code/agentdevpipeline/docs/qa/README.md)
- [Memo](/home/work/code/agentdevpipeline/docs/memo/README.md)
- [Todo](/home/work/code/agentdevpipeline/docs/todo/README.md)
- [Research](/home/work/code/agentdevpipeline/docs/research/README.md)
- [Release](/home/work/code/agentdevpipeline/docs/release/README.md)
