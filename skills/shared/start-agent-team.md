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

> **注**：此步骤确保项目级别的 Agent Team 已建立。TeamCreate 是 Claude Code 内置 tooling。若使用 `create-agent` skill 创建子 Agent（角色类型非 `team-lead`），该 skill 会处理 Agent 创建；但 Team 本身需提前确认存在。

**执行步骤**：

1. 检查当前项目是否已有 Team 定义：
   - 查找 `.claude/teams/{team_name}/config.json` 或 equivalent Team 配置文件
   - 若 Team 已存在，跳过此步
2. 若 Team 不存在，使用平台相关 TeamCreate tooling 建立项目级 Team：
   - 示意调用格式（按实际平台语法执行）：`TeamCreate(team_name="{project_id}", description="{项目描述}")`
   - 具体调用格式需参照所在平台的 TeamCreate tooling 文档
3. Team 创建完成后，继续步骤 1

**本仓库约定 fallback**：若平台 TeamCreate tooling 不可用，可改为创建本地配置文件 `.claude/teams/{project_id}/config.json`（team_id、description、created_at 字段）。此为 AgentDevFlow 仓库约定，非跨平台标准。

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

### 步骤 3. 加载团队角色

推荐顺序：

1. 团队负责人
2. 产品经理
3. 架构师
4. 质量工程师
5. 工程师
6. 平台与发布负责人
7. PMO

不是每个项目都必须全量启用，但必须记录：

- 已启用角色
- 未启用角色
- 缺失职责的临时承担者

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

### 步骤 4. 执行首轮初始化检查

每个角色都必须完成：

- 读取角色主规范
- 读取角色 playbook
- 读取本阶段 工作流
- 读取必需模板
- 检查 issue / gate / todo / risk

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

## 禁止行为

- 没有主 issue 就启动多角色并发
- 角色未读取必读文档就开始做正式判断
- 启动会 后没有 纪要、负责人、到期时间 和下游 Gate
- 未声明缺失角色职责归属就默认“之后再说”
