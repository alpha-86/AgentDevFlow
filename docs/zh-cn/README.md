# AgentDevPipeline 中文总览

## 定位

AgentDevPipeline 是一套自包含的通用产研 Agent 能力包，目标是把可复用的产品研发流程、角色约束、文档规范、会议与 Todo 机制沉淀为独立仓库，供 Claude、Codex、OpenCode 等环境复用。

## 自包含原则

- 所有文档、prompts、skills、workflow、template 都必须存在于本仓库内。
- 不允许在使用、安装、初始化或评审时依赖 `hedge-ai` 仓库。
- `hedge-ai` 只作为历史迁移来源说明，不作为当前能力依赖。
- 后续从 `hedge-ai` 迁移来的产研能力，必须直接并入本仓库维护。

## 中文与英文的关系

- `docs/zh-cn/` 和 `prompts/zh-cn/` 是内部主版本。
- `docs/en/` 和 `prompts/en/` 是对外发布版本。
- 任何需求变更、prompt 调整、workflow 迭代，必须先修改中文，再翻译英文。
- 英文版只反映已发布内容，不抢跑内部设计。

## 核心抽取范围

保留：

- Team Lead / Product Manager / Tech Lead / Engineer / QA / Researcher / SRE 的通用职责
- PRD Gate、Tech Gate、QA Gate、Release Gate
- 文档规范、会议纪要、Todo 闭环、Issue 驱动交付
- Agent 创建规范与平台适配约束

移除：

- 基金经理、CSO、CRO、Bull/Bear/Risk 等量化业务角色
- A 股盘前盘后作息、实盘信号、回测评审、策略辩论
- 量化基金特定的日报和研究语义

## 阅读顺序

1. [仓库结构图](/home/work/code/agentdevpipeline/docs/zh-cn/architecture/repository-map.md)
2. [迁移映射](/home/work/code/agentdevpipeline/docs/zh-cn/migration/hedge-ai-migration-map.md)
3. [依赖清单](/home/work/code/agentdevpipeline/docs/zh-cn/reference/dependencies.md)
4. [语言治理](/home/work/code/agentdevpipeline/docs/zh-cn/reference/localization-policy.md)
5. [外部复用调研](/home/work/code/agentdevpipeline/docs/zh-cn/reference/reuse-survey.md)
6. 平台接入文档
5. `prompts/zh-cn/` 与 `skills/shared/`

## 可直接使用的交付目录

- [PRD](/home/work/code/agentdevpipeline/docs/prd/README.md)
- [Tech](/home/work/code/agentdevpipeline/docs/tech/README.md)
- [QA](/home/work/code/agentdevpipeline/docs/qa/README.md)
- [Memo](/home/work/code/agentdevpipeline/docs/memo/README.md)
- [Todo](/home/work/code/agentdevpipeline/docs/todo/README.md)
- [Research](/home/work/code/agentdevpipeline/docs/research/README.md)
- [Release](/home/work/code/agentdevpipeline/docs/release/README.md)
