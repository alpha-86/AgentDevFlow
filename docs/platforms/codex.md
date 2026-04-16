# Codex 接入

本文档是 Codex 侧的 **自举入口**。

## Codex 侧目标

Codex 没有现成的 Team 产品壳，但已有多 Agent 调度能力。AgentDevFlow 在 Codex 中的目标是：

1. 复用 `spawn_agent / send_input / wait_agent / close_agent`
2. 让主会话承担 Team Lead 等效编排职责
3. 让每个角色子 Agent 先读共享规则再做正式工作
4. 保持与 Claude 侧相同的 Gate、Comment 和 Human Review 主线

## 启动顺序

1. 读取 `plugins/agentdevflow/README.md`
2. 读取 `skills/start-agent-team.md`
3. 读取 `skills/create-agent.md`
4. 读取 `docs/governance/core-principles.md`
5. 主会话建立主 issue、当前 Gate、Todo 和状态板
6. 再创建：
   - Product Manager
   - 架构师
   - QA Engineer
   - Engineer
   - Platform/SRE
   - PMO

## 主会话职责

主会话在 Codex 中承担 `Team Lead 等效编排者` 职责：

- 决定哪些角色需要启用
- 给子 Agent 分配清晰职责和写入范围
- 统一判断何时进入下一个 Gate
- 统一把守 Human Review 和 Issue Comment Gate

## Codex 侧最小通过标准

1. 主会话先完成启动前置条件，再创建子 Agent
2. 每个子 Agent 都有明确读物、职责和写入范围
3. 文档阶段先于实现阶段
4. Human Review #1 / #2 可追溯
5. Issue / Comment / Gate 闭环成立
