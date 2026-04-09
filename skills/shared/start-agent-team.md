# Start Agent Team

## 目标

提供通用研发项目的团队启动统一入口，确保在任何平台里启动多角色协作前，先把团队、角色、Issue、交付目录和首轮检查建立完整。

## 执行前必读

1. `skills/shared/team-setup.md`
2. `skills/shared/skill-protocol.md`
3. `skills/shared/event-bus.md`
4. `prompts/zh-cn/001_team_topology.md`
5. `prompts/zh-cn/010_team_setup_and_bootstrap.md`
6. `prompts/zh-cn/018_issue_routing_and_project_portfolio.md`

## 统一启动步骤

### Step 0. 确认团队上下文

- 确认当前项目标识 `project_id`
- 确认当前主 issue 或主工作索引
- 确认 Team Lead
- 确认本轮需要启用的角色

### Step 1. 建立项目骨架

- 初始化 `docs/prd/`
- 初始化 `docs/tech/`
- 初始化 `docs/qa/`
- 初始化 `docs/release/`
- 初始化 `docs/memo/`
- 初始化 `docs/todo/`

### Step 2. 建立共享状态

- 建立或确认主 issue
- 建立 todo registry
- 建立 kickoff memo
- 建立项目状态板
- 建立 artifact linkage 主记录

### Step 3. 加载团队角色

推荐顺序：

1. Team Lead
2. Product Manager
3. Tech Lead
4. QA Engineer
5. Engineer
6. Platform/SRE
7. Process Auditor
8. Researcher

不是每个项目都必须全量启用，但必须记录：

- 已启用角色
- 未启用角色
- 缺失职责的临时承担者

### Step 4. 执行首轮初始化检查

每个角色都必须完成：

- 读取角色主规范
- 读取角色 playbook
- 读取本阶段 workflow
- 读取必需模板
- 检查 issue / gate / todo / risk

### Step 5. 执行 kickoff

- 召开 kickoff 或首轮日会
- 形成 memo
- 明确首轮 Gate
- 明确 Human Review #1 是否需要
- 明确平台检查计划

## 启动完成判定

- 主 issue 已建立
- 角色加载完成
- kickoff memo 已形成
- 当前阶段已明确
- 下一个 Gate 已明确
- 项目状态板和 todo registry 可用
- 首轮平台检查与审计路径已明确

## 禁止行为

- 没有主 issue 就启动多角色并发
- 角色未读取必读文档就开始做正式判断
- kickoff 后没有 memo、owner、due 和下游 Gate
- 未声明缺失角色职责归属就默认“之后再说”
