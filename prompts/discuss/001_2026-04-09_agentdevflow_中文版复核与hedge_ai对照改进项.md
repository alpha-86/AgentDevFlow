# 001 - 2026-04-09 AgentDevFlow 中文版复核与 hedge-ai 对照改进项

## 背景

本轮复核基于以下输入：

1. 对当前 AgentDevFlow 中文主版本的全面 review
2. 对 hedge-ai 中可迁移流程机制的再次对照
3. 用户新增强调的两项核心诉求：
   - 人机协同必须成为方法论核心，而不是附属补充
   - Issue 机制必须能支撑多项目并行与项目内问题追踪

## 结论摘要

当前项目已经具备主干流程，但在以下四个方面仍然不够：

1. Human Review 机制还没有被提升到顶层原则
2. Issue 机制已经有状态机，但还没有把“多项目并行 / 多问题并行”讲透
3. README 对完整流程的形象化解释还不够
4. 顶层方法论没有独立文件，导致后续演进容易继续碎片化

## 对照 hedge-ai 后确认应吸收的通用机制

### A. 双阶段 PR 机制的通用抽象

来源：

- `prompts/V3.0/change_record/V2.2_双PR机制引入.md`

可迁移的不是“GitHub 分支名细节”，而是两条原则：

1. 设计确认和代码确认是两个不同的 Human Review 节点
2. 设计轨和实现轨必须明确边界，防止代码推进裹挟设计确认

对应到 AgentDevFlow：

- 需要在方法论层面明确 `Human In The Loop`
- 需要在 README 和核心流程中解释“双阶段交付”
- 需要在后续 workflow 中继续细化文档阶段与代码阶段的人机协同门禁

### B. GitHub Issue 驱动与评论门禁

来源：

- `prompts/V3.0/change_record/V2.0_研发流程与GitHubIssue结合及QA角色引入.md`
- `prompts/V3.0/change_record/V2.2.5_Issue_Comment机制修复与强制Gate建立.md`

可迁移的核心是：

1. Issue 是流程主线，不是可有可无的补充字段
2. Issue Comment 是 Gate 留痕的一部分，不是随手备注
3. Issue 能承载多项目并行和单项目问题拆分

对应到 AgentDevFlow：

- 要把 `Issue First` 上升为核心原则
- 要在 README 里明确 Issue 的角色
- 要继续补 Issue 路由、产物关联表、关闭权限策略

## 本轮决定落地的改进

### 1. 新增核心原则文件

文件：

- `docs/zh-cn/governance/core-principles.md`

目的：

- 把 `Issue First`
- `Human In The Loop`
- `设计先于实现`
- `双阶段交付`
- `Gate 不可绕过`

这些原则提升到方法论层。

### 2. README 增强完整流程图

目标：

- 用简洁流程图解释：
  - Issue 主线
  - 文档设计阶段
  - Human Review
  - 实现与 QA
  - 发布与复盘

要求：

- 不臃肿
- 能让第一次打开仓库的用户快速理解整个系统

### 3. 后续高优先级改进

#### P1. Issue 机制补强

- 增加 Issue 类型到角色的路由规则
- 增加产物关联表模板
- 增加 Human / Agent 关闭权限策略

#### P1. Human Review 机制补强

- 明确哪些交付物必须经过 Human Review
- 明确 Review 形式：PR / 文档确认 / Issue 评论确认 / 发布确认
- 明确哪些节点只允许 Agent 内部评估，哪些必须引入 Human

#### P1. 共享资产中文化

- `skills/shared/agents/*`
- `skills/shared/workflows/*`
- `skills/shared/templates/*`

当前仍有较多英文正文，与“中文主版本”定位不完全一致。

## 不做的事情

- 不迁移 hedge-ai 中量化交易业务角色
- 不迁移盘前盘后、DBR、交易日报、回测因子等业务流程
- 不把 AgentDevFlow 绑定到 GitHub 单一平台实现细节

## 下一步建议

1. 完成 README 的完整流程图和核心原则入口
2. 补一轮 Issue 路由与 Human Review 细则
3. 系统性中文化共享资产正文
