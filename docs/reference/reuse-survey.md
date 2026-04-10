# 外部能力复用调研

> 调研日期：2026-04-10

## 1. Superpowers

参考仓库：

- GitHub: https://github.com/obra/superpowers
- Marketplace: https://github.com/obra/superpowers-marketplace

### 当前仓库可直接复用的点

- 同时覆盖 `.claude-plugin`、`.codex`、`.opencode`，说明其本身已经验证了跨平台分发思路
- 把能力拆成 skills、commands、agents、hooks，层次清晰
- 安装方式区分 Claude 插件安装与 Codex/OpenCode 手动安装，适合直接借鉴到本项目

### 适合直接复用的方法类能力

这些能力与 `agentdevflow` 的研发机制不冲突，可以作为执行辅助能力直接接入：

- `writing-plans`
  - 用途：把多阶段任务拆成可执行计划
- `dispatching-parallel-agents`
  - 用途：在无共享写集时并行清点、审计、分目录处理
- `verification-before-completion`
  - 用途：避免在未验证前宣称完成
- `using-git-worktrees`
  - 用途：在复杂迁移或并行任务中隔离工作区
- `executing-plans`
  - 用途：在已有计划时按任务逐项执行

### 只应参考、不应强绑定的点

这些内容可以借鉴，但不应成为本仓库成立的前提：

- `using-superpowers`
  - 可借鉴其“先确认方法、再执行”的纪律
  - 不应要求最终用户必须安装 superpowers 才能使用本仓库
- `brainstorming`
  - 可借鉴其在大改动前先明确范围和意图的做法
  - 不应把它写成 AgentDevFlow 的强制依赖
- `test-driven-development`
  - 可作为代码阶段的推荐工程方法
  - 不应替代本项目自己的 Gate、Issue、Human Review 机制

### 对 AgentDevFlow 的建议

- 不重复造一个“大而全”的开发工作流全集
- 直接把 AgentDevFlow 定位为“产研流程治理包”
- 与 Superpowers 形成互补：Superpowers 负责通用开发方法，AgentDevFlow 负责角色、Gate、文档和交付治理

### Phase 5.2 结论

- `superpowers` 适合复用“执行方法”，不适合承载本项目的核心流程规则
- 本项目必须保持：即使没有 `superpowers`，核心角色、workflow、template、prompt 仍可独立成立

## 2. gitstack / gstack / stacked PR 工具

参考仓库：

- gitstack: https://github.com/stevearc/gitstack
- spr: https://github.com/ejoffe/spr

### 值得复用的点

- 小步提交、分层 PR、顺序合并，非常适合文档 PR 和代码 PR 分离
- 可以自然映射 AgentDevFlow 的“双阶段交付”：先设计文档，再实现代码
- 降低大 PR 的评审负担，提升多 agent 协作稳定性

### 对 AgentDevFlow 的建议

- 不强绑定某一个工具实现
- 在依赖层声明“支持 git-stack / gstack 等价工作流”
- 在具体接入项目中，由团队选定一种命令约定

### `gstack` 当前建议接入范围

优先作为“可选宿主能力”接入的有：

- `gstack-review`
  - 适合承接代码阶段的预落地评审
- `gstack-ship`
  - 适合承接双阶段 PR 后半段的提交、推送和 PR 创建
- `gstack-document-release`
  - 适合承接发布后的文档同步
- `gstack-qa` / `gstack-qa-only`
  - 适合承接 QA Gate 前后的质量验证
- `gstack-health`
  - 适合承接仓库健康检查

不应进入插件主干依赖的有：

- 浏览器控制类能力
- 视觉设计类能力
- 部署平台类能力
- 安全深审类能力

### Phase 5.3 结论

- `gstack` 适合作为可选宿主环境，不适合作为插件唯一运行前提
- 本项目只应声明与研发主流程直接相关的 `gstack` 能力
- 其余能力保持“可扩展接入”，不进入核心依赖清单

## 3. 结论

- `Superpowers` 适合作为执行方法与结构组织参考
- `gitstack/spr/gstack` 适合作为 stacked PR 和研发协作宿主依赖
- AgentDevFlow 应专注于“产研组织能力”和“交付流程契约”，避免与这些项目功能重叠
