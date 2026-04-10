# 002 - 2026-04-09 双阶段 PR、Issue Gate 与多项目并行差距审计

## 目标

针对以下核心要求，对 AgentDevFlow 当前状态与 hedge-ai 中对应机制做严格对照：

1. 双阶段 PR / Human Review
2. 三层保障体系
3. Issue 驱动、多项目并行、Issue Comment Gate
4. README 对完整流程的形象化表达

## 一、对照结论

当前 AgentDevFlow 已经开始覆盖上述能力，但距离“相对完整、可执行、可长期运行”的状态仍有明显差距。更准确地说：

- 方法论层已开始建立
- 规则层正在成型
- 执行层仍不完整
- 平台检查层几乎还未建设

## 二、已落地部分

### 2.1 Human Review / 双阶段思路

已落地：

- `docs/zh-cn/governance/core-principles.md`
- `prompts/zh-cn/017_human_review_and_signoff.md`
- `prompts/zh-cn/019_dual_stage_pr_and_three_layer_safeguard.md`
- `skills/shared/workflows/human-review.md`
- `README_CN.md` 中的完整流程图

说明：

- 设计确认和实现确认已经被明确区分
- 但还没有完全下沉到所有 workflow 的准入准出条件中

### 2.2 Issue 驱动 / Issue Comment Gate

已落地：

- `prompts/zh-cn/007_issue_driven_orchestration.md`
- `prompts/zh-cn/013_github_issue_and_review_comments.md`
- `prompts/zh-cn/018_issue_routing_and_project_portfolio.md`
- `prompts/zh-cn/020_issue_comment_gate_and_artifact_linkage.md`
- `skills/shared/workflows/issue-lifecycle.md`
- `skills/shared/workflows/issue-routing.md`
- `skills/shared/templates/artifact-linkage-template.md`

说明：

- Issue 作为主索引的地位已经明确
- Comment Gate 已明确提出
- 但实际自动化检查机制仍未建设

## 三、仍然存在的关键差距

### P0. 平台检查层几乎没有落地

hedge-ai 对应机制：

- 双阶段 PR 检查
- Comment 检查
- Issue 状态同步检查

AgentDevFlow 现状：

- 只有规则，没有检查实现

影响：

- 当前流程依然高度依赖人工自觉
- 一旦团队规模上来，规则会漂移

### P0. Human Review 的对象和形式虽然被定义，但还没有被全面嵌入阶段 Gate

现状：

- README 和 prompt 里写清楚了
- 但 PRD / Tech / QA / Release workflow 还没有全部显式声明：
  - 哪些阶段必须 Human Review
  - 哪些阶段只是 Agent 内部 review
  - 哪些阶段的 reviewer 角色不可缺失

### P1. 多项目并行还没有统一的项目级视图

现状：

- 已有 Project ID / issue route 的规则
- 但缺少组合视图模板和 project registry

影响：

- 多项目同时运行时，Team Lead 仍然难以一眼看到组合健康度

### P1. README 已有流程图，但还缺“从用户视角的使用路径”

现状：

- 已有完整流程图

仍缺：

- 用户第一次接入时到底先配置什么
- 一个项目如何从 kickoff 到 done 跑起来
- Human Review 在用户实际使用中如何触发

### P1. 共享 agent 层虽然开始中文化，但还没有完全与新规则对齐

现状：

- 当前正在中文化和补充规则

仍缺：

- 每个角色在双阶段 PR / Human Review / Issue Comment Gate 中的明确责任

## 四、建议优先级

### 下一步 P0

1. 把 Human Review 节点明确写入 PRD / Tech / QA / Release workflow
2. 建立 project registry / project portfolio 模板
3. 在平台适配层定义最小自动化检查集合

### 下一步 P1

1. README 增加“如何从 0 到 1 使用”的用户路径
2. roles/playbook 全量对齐 Issue Gate / Human Review / 双阶段交付
3. docs/ 目录继续整理，减少治理类文档散落

## 五、结论

如果目标是“比现在更清楚”，当前已经前进了一大步。  
如果目标是“接近 hedge-ai 那种相对完整、可执行、可实时运转的多 agent 机制”，当前还远远不能收工，尤其缺：

- 平台检查层
- 项目组合视图
- Human Review 全面嵌入阶段 Gate
- 用户实际使用路径
