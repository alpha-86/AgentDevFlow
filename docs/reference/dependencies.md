# 依赖清单

## 必需基础依赖

- `git`
- `rg` 或等价全文检索工具
- Markdown 文件系统工作流
- Issue 跟踪系统
- Pull Request 工作流

## 推荐工程依赖

- `gh`：GitHub CLI
- Stacked PR 工具：推荐 `git-stack` 或团队已有 `gstack` 等价方案
- 测试运行器：按项目语言选择
- CI 平台：GitHub Actions / 等价系统

## 推荐外部 Skill / Plugin 复用

### Claude 官方 Skills

- `planner`
- `architect`
- `code-review`
- `tdd`
- `verification-loop`
- `docs-lookup`
- `deep-research`

### 可复用社区包

- `Superpowers`：适合作为多平台目录组织和插件分发参考
- Stacked PR 工具链：适合承接文档 PR / 代码 PR 的双阶段协作

## 依赖治理规则

- 本项目的核心资产不得依赖其他仓库中的 prompts、skills 或文档。
- 核心流程文档必须说明依赖来源、安装方式、是否必需
- 外部依赖优先“引用和适配”，避免重复造轮子
- 若团队已有 `gstack` 约定，则在平台接入文档中明确其命令约定

## 当前建议

| 依赖 | 级别 | 用途 |
|---|---|---|
| Claude 官方 Skills | 推荐 | 规划、架构、评审、验证 |
| Superpowers | 可选 | 参考其跨平台打包方式与现成能力 |
| git-stack / gstack | 推荐 | Stacked PR 协作 |
| GitHub CLI | 推荐 | Issue / PR 自动化 |
