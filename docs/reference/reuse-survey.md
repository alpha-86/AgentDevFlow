# 外部能力复用调研

> 调研日期：2026-04-09

## 1. Superpowers

参考仓库：

- GitHub: https://github.com/obra/superpowers
- Marketplace: https://github.com/obra/superpowers-marketplace

### 值得复用的点

- 同时覆盖 `.claude-plugin`、`.codex`、`.opencode`，说明其本身已经验证了跨平台分发思路
- 把能力拆成 skills、commands、agents、hooks，层次清晰
- 安装方式区分 Claude 插件安装与 Codex/OpenCode 手动安装，适合直接借鉴到本项目

### 对 AgentDevPipeline 的建议

- 不重复造一个“大而全”的开发工作流全集
- 直接把 AgentDevPipeline 定位为“产研流程治理包”
- 与 Superpowers 形成互补：Superpowers 负责通用开发方法，AgentDevPipeline 负责角色、Gate、文档和交付治理

## 2. gitstack / gstack / stacked PR 工具

参考仓库：

- gitstack: https://github.com/stevearc/gitstack
- spr: https://github.com/ejoffe/spr

### 值得复用的点

- 小步提交、分层 PR、顺序合并，非常适合文档 PR 和代码 PR 分离
- 可以自然映射 AgentDevPipeline 的“双阶段交付”：先设计文档，再实现代码
- 降低大 PR 的评审负担，提升多 agent 协作稳定性

### 对 AgentDevPipeline 的建议

- 不强绑定某一个工具实现
- 在依赖层声明“支持 git-stack / gstack 等价工作流”
- 在具体接入项目中，由团队选定一种命令约定

## 3. 结论

- `Superpowers` 适合作为跨平台分发结构和通用开发 skill 依赖
- `gitstack/spr/gstack` 适合作为 stacked PR 协作依赖
- AgentDevPipeline 应专注于“产研组织能力”和“交付流程契约”，避免与这些项目功能重叠

