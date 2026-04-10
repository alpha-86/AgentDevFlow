# Codex Adapter

这是 Codex 侧的 AgentDevFlow 适配入口。它的职责不是再发明一套规则，而是把 Codex 的多 Agent 调度能力接到 AgentDevFlow 的共享角色、workflow 和 Gate 主线。

## 启动顺序

1. 读取根 `README.md`
2. 读取 `plugins/agentdevflow/README.md`
3. 读取 `docs/platforms/codex.md`
4. 读取 `skills/shared/start-agent-team.md`
5. 读取 `skills/shared/create-agent.md`
6. 由主会话建立：
   - `project_id`
   - 主 issue 或当前主工作索引
   - 当前 Gate
   - Todo / 状态板 / 产物关联主记录
7. 再创建 Product Manager、架构师、QA、Engineer、PMO 等角色 Agent

## 主会话职责

Codex 中的主会话承担 `Team Lead 等效编排者` 职责：

- 先建立启动前置条件，再决定是否创建角色
- 决定默认团队和可选角色
- 给每个子 Agent 注入角色读物、职责边界和写入范围
- 控制文档阶段先于实现阶段
- 把守 Issue / Comment / Human Review / Gate
- 统一收口验证结果和下一步动作

## 子 Agent 最小约束

每个 Codex 侧子 Agent 在创建时至少必须带上：

1. 角色定义
2. 必读文档
3. 当前 Gate
4. 当前主 issue / `project_id`
5. 明确职责边界
6. 允许写入的文件范围
7. 初始化确认格式

没有这些内容，不应创建正式的 gated delivery 角色。

## 最小通过标准

1. 主会话先完成启动前置条件，再创建任何子 Agent
2. 每个子 Agent 都带着明确读物、职责边界和写入范围启动
3. 文档阶段先于实现阶段
4. Issue / Comment / Human Review / Gate 全部可追溯
5. 发现检查失败时，当前阶段会被阻断，而不是继续推进

## 最小检查建议

接入 Codex 时，至少检查：

1. 当前阶段所需文档是否存在
2. 当前阶段所需 Issue Comment 是否存在
3. artifact linkage 是否完整
4. 当前 Gate 状态是否与实际产物一致
5. Human Review 结论是否已正式落地

参考：

- `docs/governance/platform-minimum-checks.md`
- `skills/shared/templates/platform-checklist-template.md`
- `skills/shared/templates/platform-check-result-template.md`
- `adapters/codex/platform-check-example.md`
