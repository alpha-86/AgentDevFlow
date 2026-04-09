# AgentDevPipeline

[English](./README.md) | 中文

AgentDevPipeline 是一套自包含的通用产研 Agent 能力包，面向 Claude、Codex、OpenCode 等环境使用。

## 概览

本项目提供：

- 面向产研协作的 agent 角色定义
- PRD、Tech Review、开发、QA、Release 的分阶段 Gate 流程
- PRD、Tech Spec、QA Case、Memo、Todo 等可复用模板
- Claude、Codex、OpenCode 适配入口
- 中文内部主版本、英文发布镜像的文档治理模型

## 核心理念

- 建立一套全流程自动化的多 agent 研发流程编排能力
- 通过明确的阶段、Gate、负责人、评审记录，让过程始终可控
- 通过 prompts、workflows、templates、memo、todo 等资产，让关键交付步骤可追溯、可复盘
- 作为独立项目，为 Claude、Codex、OpenCode 提供完整的多 agent 研发流程能力

## 文档治理

- `docs/zh-cn/` 和 `prompts/zh-cn/` 是内部主版本
- `docs/en/` 和 `prompts/en/` 是英文发布版本
- 所有功能和流程变更必须先更新中文，再同步英文
- 与 hedge-ai 的迁移必须遵循强约束边界，见 [迁移边界（强约束）](./docs/zh-cn/reference/migration-boundary-from-hedge-ai.md)

## 快速开始

1. 阅读 [中文总览](./docs/zh-cn/README.md)
2. 阅读 [仓库结构图](./docs/zh-cn/architecture/repository-map.md)
3. 按平台选择接入文档：
   - [Claude Code](./docs/zh-cn/platforms/claude-code.md)
   - [Codex](./docs/zh-cn/platforms/codex.md)
   - [OpenCode](./docs/zh-cn/platforms/opencode.md)
4. 使用 `skills/shared/` 下的共享资产

## 共享 Workflow 包

- `skills/shared/workflows/prd-review.md`
- `skills/shared/workflows/tech-review.md`
- `skills/shared/workflows/implementation.md`
- `skills/shared/workflows/qa-validation.md`
- `skills/shared/workflows/release-review.md`
- `skills/shared/workflows/daily-sync.md`
- `skills/shared/workflows/todo-review.md`

## 项目结构

```text
AgentDevPipeline/
├── adapters/           # 平台适配入口
├── docs/               # 源文档、发布文档、交付目录
├── plugins/            # Codex 插件包
├── prompts/            # 中文源 prompts + 英文发布 prompts
├── registry/           # 依赖元数据
└── skills/shared/      # 平台无关角色、流程、模板、playbook
```

## 可直接使用的交付目录

- `docs/prd/`
- `docs/tech/`
- `docs/qa/`
- `docs/memo/`
- `docs/todo/`
- `docs/research/`
- `docs/release/`

## 当前版本

- 内部主版本：`0.3.0`
- 对外发布版本：`0.3.0`
