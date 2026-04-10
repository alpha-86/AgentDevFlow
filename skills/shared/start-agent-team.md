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
