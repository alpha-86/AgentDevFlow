# Claude Code 接入

本文档不是“最小安装说明”，而是 Claude 侧的 **自举入口**。

## Claude 侧目标

Claude 已有 Agent Team 能力。AgentDevFlow 在 Claude 中要做的是：

1. 复用现有 Team 能力
2. 约束 Team Lead 的启动顺序
3. 让每个角色先读共享规则再开始工作
4. 保证文档阶段、实现阶段、Human Review 和 Issue Comment Gate 都可追溯

## Team Lead 语义说明

Claude 的 Agent Team 能力中，**Team Lead 是 human 用户本身，不是需要创建的 agent**。

- `create-agent` 明确声明：`team-lead` is the human user themselves, not a separate agent
- Human 用户通过 Agent Team 能力承担 Team Lead 编排职责
- 其他角色（Product Manager、Architect、QA Engineer 等）才需要通过 `create-agent` 创建

## 启动顺序

1. 加载 `adapters/claude/.claude/skills/`
2. 先读 `TEAM_SETUP.md`
3. Human 用户作为 Team Lead，确认项目上下文：
   - `project_id`
   - 主 issue 或当前主工作索引
   - 当前 Gate
   - 启动会纪要、Todo Registry、状态板、产物关联主记录
4. 通过 `create-agent` 按顺序创建其他角色：
   - Product Manager
   - 架构师
   - QA Engineer
   - Engineer
   - Platform/SRE
   - PMO
5. 最后通过 `start-agent-team` 完成团队启动

## Team Lead 必须先做什么

Human 用户作为 Team Lead，在创建其他角色前，必须先确认：

1. `project_id`
2. 主 issue 或当前主工作索引
3. 当前 Gate
4. 已启用角色与未启用角色
5. 启动会纪要、Todo Registry、状态板、产物关联主记录

没有这些前置条件，不得宣称团队已启动。

## Claude 侧最小通过标准

1. Team Lead 先读共享入口，不直接开工
2. 默认角色顺序正确
3. 文档阶段与实现阶段分离
4. Human Review #1 / #2 可追溯
5. Issue Comment Gate 生效

## 必读文件

- `adapters/claude/.claude/skills/TEAM_SETUP.md`
- `skills/shared/start-agent-team.md`
- `skills/shared/create-agent.md`
- `docs/governance/core-principles.md`
- `prompts/004_delivery_gates.md`
- `prompts/013_github_issue_and_review_comments.md`
- `prompts/019_dual_stage_pr_and_three_layer_safeguard.md`
