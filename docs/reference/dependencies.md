# 依赖清单

## 当前盘点结论

当前仓库是“文档与共享资产自包含、平台能力外接”的结构。

- 仓库内已直接承载的核心资产：
  - `README.md`
  - `prompts/`
  - `docs/`
  - `skills/`
  - `plugins/agentdevflow/.codex-plugin/plugin.json`
- 仓库内目前没有语言运行时依赖清单：
  - 无 `package.json`
  - 无 `pyproject.toml`
  - 无 `requirements.txt`
  - 无 `go.mod`
- 当前外部依赖主要是“研发协作环境依赖”，而不是“应用运行时依赖”。

## 必需基础依赖

这些依赖缺失时，插件主流程无法真正落地：

- `git`
  - 用途：提交、分支、PR 对应的版本管理
- `rg` 或等价全文检索工具
  - 用途：全文检索 prompt、workflow、模板和历史记录
- Markdown 文件系统工作流
  - 用途：承载 PRD、Tech、QA、Memo、Todo、Release 等正式交付物
- Issue 跟踪系统
  - 用途：作为“Issue 优先”主索引
- Pull Request 工作流
  - 用途：承载双阶段 PR 机制

## 推荐工程依赖

这些依赖不是插件主干的一部分，但强烈建议接入：

- `gh`
  - 用途：Issue / PR 自动化和评论回写
- Stacked PR 工具
  - 推荐：`git-stack`、`gstack` 或团队已有等价方案
  - 用途：承接文档 PR / 代码 PR 的双阶段协作
- 测试运行器
  - 用途：在代码阶段输出真实测试证据
- CI 平台
  - 推荐：GitHub Actions 或等价系统
  - 用途：承接平台检查层

## 当前已发现的仓库内建入口

当前仓库实际内建且已可作为装载入口的只有：

- `plugins/agentdevflow/.codex-plugin/plugin.json`
  - 当前唯一正式插件元数据入口
- `skills/`
  - 当前唯一共享角色、工作流、模板入口
- `prompts/`
  - 当前唯一规则层入口
- `docs/`
  - 当前唯一说明、治理、迁移审计入口

## 插件自身资产与外部依赖资产的边界

### 一、插件自身资产

这些内容必须由本仓库自己承载，不能外包给外部能力包：

- `plugins/agentdevflow/.codex-plugin/plugin.json`
- `README.md`
- `prompts/`
- `docs/`
- `skills/agents/`
- `skills/workflows/`
- `skills/templates/`
- `skills/team-setup.md`
- `skills/start-agent-team.md`
- `skills/create-agent.md`
- `skills/skill-protocol.md`
- `skills/event-bus.md`

这些资产共同构成：

- 插件入口
- 研发流程规则
- 角色职责与执行手册
- 交付模板与留痕规范
- 迁移边界与审计依据

### 二、外部依赖资产

这些内容可以接入，但不能替代插件自身资产：

- `superpowers`
  - 定位：执行方法与结构组织参考
- `gstack`
  - 定位：可选宿主环境
- `gh`
  - 定位：GitHub 自动化接入工具
- CI / PR / Issue 平台能力
  - 定位：平台检查层与流程自动化承载

### 三、边界规则

- 外部依赖只能增强执行效率，不能定义核心流程规则。
- 任何平台或工具接入都不得改写 `prompts/` 与 `skills/` 的核心语义。
- 若移除外部依赖，插件自身资产仍必须可以被阅读、审计和手动执行。
- 若某个流程只有依赖外部宿主才能成立，则它不应被写成插件主干规则。

## 推荐复用的外部能力

### 1. `superpowers`

- 级别：可选依赖
- 当前作用：作为目录组织、技能拆分和执行方式的参考来源
- 当前结论：可以复用思路，但本仓库核心资产不能依赖其在线存在

### 2. `gstack`

- 级别：可选依赖
- 当前作用：适合作为 stacked PR、评审、发布、检查类能力的宿主环境
- 当前结论：可接入，不应成为仓库核心规则的唯一承载
- 当前建议接入范围：
  - `gstack-review`
    - 适用：代码变更前的预落地评审
  - `gstack-ship`
    - 适用：需要把双阶段 PR 落地到实际提交流程时
  - `gstack-document-release`
    - 适用：发布后同步 README、CHANGELOG、说明文档
  - `gstack-qa` / `gstack-qa-only`
    - 适用：代码阶段和发布前的质量验证
  - `gstack-health`
    - 适用：做仓库体检和持续质量检查
- 当前不建议写成插件强前置：
  - 浏览器类能力
  - 设计类能力
  - 部署类能力
  - 安全审计类能力
  - 它们可以作为扩展接入，但不属于插件主干依赖

### 3. GitHub CLI 与 GitHub 平台能力

- 级别：推荐依赖
- 当前作用：Issue、PR、Comment、检查器接入
- 当前结论：是当前最贴近插件主流程的外部协作平台依赖

## 依赖治理规则

- 本项目的核心资产不得依赖其他仓库中的 prompts、skills 或文档才能成立。
- 核心流程文档必须说明依赖来源、安装方式、是否必需。
- 外部依赖优先“引用和适配”，避免重复造轮子。
- 若团队已有 `gstack` 约定，则在平台接入文档中明确其命令约定。
- 若外部依赖缺失，必须说明哪些流程可降级执行，哪些流程不可执行。
- 插件自身资产与外部依赖资产的边界，必须优先以本文件定义为准。

## Phase 5.1 结论

`Phase 5.1` 的结论是：当前仓库没有复杂的语言运行时依赖，真正需要收口的是研发协作依赖和插件装载依赖。下一步应继续区分哪些能力直接复用 `superpowers` / `gstack`，哪些必须由本仓库自己承载。

## 中文依赖接入说明

### 1. 最小可用接入

如果只想先把插件主流程跑起来，至少准备：

1. `git`
2. `rg`
3. 一个支持 Issue 的代码托管平台
4. 一个支持 Pull Request 的协作流程
5. 当前仓库本身

对应动作：

- 克隆当前仓库
- 让项目成员先阅读 `README.md`
- 再阅读 `plugins/agentdevflow/README.md`
- 再按 `docs/README.md` 和 `prompts/README.md` 进入规则层与共享资产层

### 2. 推荐增强接入

如果要让流程更接近可执行状态，建议再准备：

- `gh`
- 一套 stacked PR 工具
- CI 平台
- 目标项目自己的测试运行器

对应作用：

- `gh`：承接 Issue / PR / Comment 回写
- stacked PR 工具：承接文档 PR / 代码 PR 双阶段交付
- CI：承接平台检查层
- 测试运行器：承接 QA 与发布前验证

### 3. 可选宿主接入

如果你的团队已经在用下列环境，可按需接入：

- `superpowers`
- `gstack`

接入原则：

- 它们只能增强执行效率
- 它们不能替代本仓库的规则层和共享资产层
- 即使不接入，它们也不应阻止当前仓库被阅读和手动执行

### 4. 推荐接入顺序

1. 先接入仓库自身资产：
   - `README.md`
   - `plugins/agentdevflow/README.md`
   - `prompts/`
   - `skills/`
   - `docs/`
2. 再接入协作依赖：
   - `git`
   - Issue / PR 平台
   - `gh`
3. 最后按团队成熟度接入：
   - stacked PR 工具
   - CI
   - `gstack`
   - `superpowers`

### 5. 不建议的接入方式

- 先接平台自动化，再补规则层
- 只装外部宿主能力，不读本仓库规则
- 把 `gstack`、`superpowers` 当成插件本体
- 未建立 Issue / PR 流程就直接声称已接入双阶段 PR

## Phase 5.5 结论

当前仓库的中文依赖安装说明，应该理解为“中文接入说明”，而不是语言运行时安装手册。核心是先接入仓库自身资产，再逐层接入协作环境和可选宿主能力。
