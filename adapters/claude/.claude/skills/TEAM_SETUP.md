# AgentDevFlow Team Setup

这是 Claude 侧的 AgentDevFlow 启动入口。

## 必须先读

1. `skills/shared/start-agent-team.md`
2. `skills/shared/create-agent.md`
3. `docs/governance/core-principles.md`

## Team Lead 语义说明

Claude 的 Agent Team 能力中，**Team Lead 是 human 用户本身，不是需要创建的 agent**。

`create-agent` 明确声明：`team-lead` is the human user themselves, not a separate agent。

Human 用户通过 Agent Team 能力承担 Team Lead 编排职责。其他角色才需要通过 `create-agent` 创建。

## 启动顺序

1. 先确认 `project_id`
2. 先确认主 issue 或当前主工作索引
3. 先建立：
   - 启动会纪要
   - `docs/todo/TODO_REGISTRY.md`
   - 项目状态板
   - 产物关联主记录
4. Human 用户作为 Team Lead，确认上述上下文
5. 通过 `create-agent` 创建其他角色
6. 最后通过 `start-agent-team` 完成团队启动

## 默认角色顺序

1. `team-lead`
2. `product-manager`
3. `architect`
4. `qa-engineer`
5. `engineer`
6. `platform-sre`
7. `pmo`

## 必须加载的共享资产

- `skills/shared/agents/`
- `skills/shared/workflows/`
- `skills/shared/templates/`
- `prompts/`

## 规则

- 所有角色和 workflow 内容都必须从当前仓库读取
- Team Lead 未完成初始化确认前，不得宣布团队已启动
- 文档阶段与实现阶段必须分离
