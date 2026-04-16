# 启动团队

## 目标

提供通用研发项目的团队启动统一入口，确保在任何平台里启动多 Agent 协作前，先把团队、角色、Issue、交付目录和首轮检查建立完整。

## 执行前必读

1. `skills/shared/team-setup.md`
2. `skills/shared/skill-protocol.md`
3. `skills/shared/event-bus.md`
4. `prompts/001_team_topology.md`
5. `prompts/010_team_setup_and_bootstrap.md`
6. `prompts/018_issue_routing_and_project_portfolio.md`

## 统一启动步骤

### 步骤 0. 确认团队上下文

- 确认当前项目标识 `project_id`
- 确认当前主 issue 或主工作索引
- 确认 团队负责人
- 确认本轮需要启用的角色

### 步骤 0.5. Team 创建检查

> **注**：每次执行 start-agent-team 时，**必须假设团队不存在**，从零开始检查和创建。上一个 session 的任何配置文件、日志、状态记录都与当前 session 无关。

**执行步骤**：

1. **检查全局 Team 注册表**：
   - 执行 `ls ~/.claude/teams/` 检查是否存在
   - 若存在，检查是否是当前项目的 Team
   - **禁止依赖** `agent-creation.log`、`TODO_REGISTRY.md`、`.claude/teams/` 等文件的历史状态

2. **若 Team 不存在，使用 TeamCreate 创建**：
   ```json
   TeamCreate(team_name="{project_id}", description="{项目描述}")
   ```

3. **Team 创建完成后，继续步骤 1**

**禁止行为**：
- 在 Team 未建立的情况下直接创建多个 Agent
- 将 `team-lead` 作为需要创建的 Agent（team-lead 是 Human 本身，见 `create-agent.md` 步骤 1.5）
- 每个项目只创建一个 Team，禁止重复创建

### 步骤 1. 建立项目骨架

- 初始化 `docs/prd/`
- 初始化 `docs/tech/`
- 初始化 `docs/qa/`
- 初始化 `docs/release/`
- 初始化 `docs/memo/`
- 初始化 `docs/todo/`

### 步骤 2. 建立共享状态

- 建立或确认主 issue
- 建立 todo registry
- 建立 启动会 纪要
- 建立项目状态板
- 建立 artifact linkage 主记录

### 步骤 3. 加载团队角色（显式 Skill 调用）

**⚠️ 关键原则：每次 start-agent-team 执行都是全新开始，不依赖历史配置**

以下文件/内容**不能**作为 Agent 存在的证明：
- `.claude/logs/agent-creation.log`
- `.claude/logs/agent-liveness.log`
- `.claude/teams/{team}/config.json`
- `docs/todo/TODO_REGISTRY.md` 中的角色状态列
- 任何 md 文件中的"已创建"、"active" 状态标记

**Agent 创建顺序**：

1. Team Lead（Human 本身，**不创建**）
2. Product Manager → `Skill("adf-product-manager")`
3. 架构师 → `Skill("adf-architect")`
4. 质量工程师 → `Skill("adf-qa-engineer")`
5. 工程师 → `Skill("adf-engineer")`
6. 平台与发布负责人 → `Skill("adf-platform-sre")`
7. PMO → `Skill("adf-pmo")`

**每个 Agent 创建后必须执行初始化确认**：
1. 读取对应的 `.claude/skills/adf-{role}/SKILL.md`
2. 读取必读文档列表中的第一个文档
3. 输出初始化确认（角色、project_id、issue_id、当前阶段、已读取文档、阻塞项、下一动作）

每个项目必须全量启用所有角色，不得以"临时承担"代替正式 Agent 实例化。

**原因**：`team-lead.md` 强制规则明确规定"团队负责人不得越权替其他角色做正式签字"。Team Lead 承担其他角色职责会导致：
1. 角色权责边界模糊，无法进行有效的流程合规审计
2. PMO 无法对"Team Lead 既当裁判又当运动员"进行独立检查
3. 缺失职责无正式 Agent 承担，任务路由失效

**正确做法**：
- 启动前必须创建 Engineer、Platform/SRE、PMO 的 Agent 实例
- 角色暂不需要实际工作时，Agent 处于"待命"状态（idle），但不分配给其他角色
- 所有角色都必须完成初始化检查（步骤 4），进入各自的角色循环

### 步骤 3.5. 发现并路由待处理任务

> **注**：启动团队前必须先拉取所有待处理任务，确保启动会覆盖完整的上下文。

**步骤 3.5.1. 发现 GitHub Open Issues**

调用 `scripts/github_issue_sync.py` 同步 open issues：

```bash
python scripts/github_issue_sync.py
```

- 该脚本从 GitHub 拉取所有 open issues，写入 `.claude/task_queue/issue_{number}.task`
- 对于命名格式不符的 issue，脚本会输出警告
- 每次运行自动去重，已处理的 issue 不会重复写入

**步骤 3.5.2. 读取任务队列**

读取 `.claude/task_queue/` 目录下所有 `.task` 文件：

- 统计当前待处理任务数量
- 按 type 分类（prd/tech/bug/qa 等）
- 按 priority 排序（critical > high > medium > low）

**步骤 3.5.3. 读取 Todo Registry**

读取 `docs/todo/TODO_REGISTRY.md`：

- 获取当前阶段 gate 状态
- 检查是否有 overdue 任务
- 确认启动会前的未完成任务

**步骤 3.5.4. 路由任务到角色**

调用 `scripts/task_router.py` 将待处理任务路由到对应角色：

```bash
python scripts/task_router.py --verbose
```

- 该脚本读取 `.claude/task_queue/` 下的 `.task` 文件
- 按 type 标签路由到 Product Manager / 架构师 / Engineer / QA Engineer
- 输出路由日志到 `.claude/results/routing.log`
- 每个任务生成 pending comment 文件到 `.claude/results/pending_{issue_id}.md`

**步骤 3.5.5. 汇总启动上下文**

整合以上结果，生成启动前任务摘要：

- GitHub open issues 数量
- 待路由任务数量
- 当前 todo 状态（overdue / 正常）
- 关键阻塞项（如有）

此摘要将作为启动会议程的依据。

## Agent 必读文档速查表

| Agent | 必读文档 |
|-------|---------|
| Team Lead | prompts/001_team_topology.md, prompts/010_team_setup_and_bootstrap.md, prompts/018_issue_routing_and_project_portfolio.md |
| Product Manager | prompts/001_team_topology.md, prompts/003_document_contracts.md, prompts/004_delivery_gates.md |
| 架构师 | prompts/001_team_topology.md, prompts/004_delivery_gates.md, skills/shared/workflows/tech-review.md |
| 质量工程师 | prompts/001_team_topology.md, prompts/004_delivery_gates.md, skills/shared/workflows/qa-validation.md |
| 工程师 | prompts/001_team_topology.md, prompts/004_delivery_gates.md, prompts/019_dual_stage_pr_and_three_layer_safeguard.md |
| Platform/SRE | prompts/001_team_topology.md, prompts/019_dual_stage_pr_and_three_layer_safeguard.md, skills/shared/workflows/release-review.md |
| PMO | prompts/001_team_topology.md, prompts/005_meeting_and_todo.md, docs/governance/core-principles.md |

### 步骤 4. 执行首轮初始化检查

每个角色都必须完成：

- 读取角色主规范
- 读取角色 playbook
- 读取本阶段 工作流
- 读取必需模板
- 检查 issue / gate / todo / risk

### 步骤 4.5. Agent 工作触发条件

每个 Agent 的触发条件：

| Agent | 触发时间 | 执行 Workflow | 关联文档 |
|-------|---------|--------------|----------|
| Team Lead | 每日启动时 | skills/shared/workflows/weekly-review.md | 启动会纪要 |
| Product Manager | PRD Gate 完成后 | skills/shared/workflows/prd-review.md | PRD 文档 |
| 架构师 | PRD Gate 通过后 | skills/shared/workflows/tech-review.md | Tech Spec |
| 质量工程师 | Tech Gate 通过后 | skills/shared/workflows/qa-validation.md | QA Case |
| 工程师 | QA Case Design 通过后 | prompts/019_dual_stage_pr_and_three_layer_safeguard.md | 代码 PR |
| Platform/SRE | Release 前 | skills/shared/workflows/release-review.md | 发布检查单 |
| PMO | 每周定期 | skills/shared/workflows/weekly-review.md | 审计报告 |

### 步骤 5. 执行 启动会

- 召开 启动会 或首轮日会
- 形成 纪要
- 明确首轮 Gate
- 明确 人工评审 #1 是否需要
- 明确平台检查计划

## 启动完成判定

- 主 issue 已建立
- 角色加载完成
- 启动会 纪要 已形成
- 当前阶段已明确
- 下一个 Gate 已明确
- 项目状态板和 todo registry 可用
- 首轮平台检查与审计路径已明确

## 启动输出去向

- 启动会 纪要：`docs/memo/`
- 待办注册：`docs/todo/TODO_REGISTRY.md`
- 项目状态板：`docs/memo/`
- 产物关联主记录：`docs/memo/`

## 启动失败规则

- 若任一关键角色未完成初始化检查，不得宣布启动完成。
- 若主 issue、状态板、todo registry 三者缺一，必须回到步骤 1 或步骤 2 补齐。
- 若首轮 Gate 或 人工评审 #1 判定不明确，必须补会议结论后再继续。
- **若有任何角色未经正式 Agent 实例化即以"临时承担"方式运作，必须补充创建该角色 Agent 并重新完成初始化检查。**

## 禁止行为

- **严禁 Team Lead 承担其他 Agent 的职责**：Team Lead 不得以”临时承担””暂由 Team Lead 代管”等理由，实际履行 Engineer、PMO、Platform/SRE 等角色的决策权、签字权和工作触发权。违反此规则等同于绕开角色分离机制，PMO 应立即标记为 P0 级 governance 问题。
- 没有主 issue 就启动多角色并发
- 角色未读取必读文档就开始做正式判断
- 启动会 后没有 纪要、负责人、到期时间 和下游 Gate
- 未启用全部角色就宣布启动完成
