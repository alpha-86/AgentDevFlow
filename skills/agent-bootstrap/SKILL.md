# AgentDevFlow 自举

## 目标

让 AgentDevFlow 仓库自身能够像任何目标项目一样，先建立完整的项目骨架、团队、Issue 和交付目录，再启动 Agent 协作开发。这是 AgentDevFlow 的"自举"——项目吃自己的狗粮。

## 与 /start-agent-team 的区别

| | `/start-agent-team` | `/agent-bootstrap` |
|---|---|---|
| 适用场景 | 任意目标项目启动 AgentDevFlow | AgentDevFlow 自身初始化 |
| 起点 | 目标项目已有骨架 | 项目骨架待建立或待复核 |
| 重点 | 建立交付目录、Issue、团队 | 建立 AgentDevFlow 自身治理 + 交付机制 |
| 角色来源 | `skills/{role}.md` | `skills/{role}.md` (自身) |

## 执行前必读

1. `skills/start-agent-team.md`
2. `skills/skill-protocol.md`
3. `skills/event-bus.md`
4. `prompts/001_team_topology.md`
5. `prompts/010_team_setup_and_bootstrap.md`
6. `docs/governance/core-principles.md`
7. `README.md`

## 自举步骤

### 步骤 0. 确认 AgentDevFlow 自身状态

- 当前是否已有骨架？（`docs/prd/`、`docs/tech/`、`docs/qa/`、`docs/memo/`、`docs/todo/`、`docs/release/`）
- 当前仓库版本（`CHANGELOG.md` 最新版本）
- 当前主 issue 或本轮工作目标
- 本轮 AgentDevFlow 自身需要迭代什么？

### 步骤 1. 确认或建立项目骨架

检查以下目录是否存在，若缺失则建立：

- `docs/prd/` - 需求文档
- `docs/tech/` - 技术设计
- `docs/qa/` - QA 相关
- `docs/release/` - 发布记录
- `docs/memo/` - 纪要
- `docs/todo/` - 待办注册
- `skills/` - 共享资产层
- `prompts/` - 规则层
- `adapters/` - 平台适配

### 步骤 2. 确认或建立启动会纪要

- 若 `docs/memo/` 下无启动会纪要，创建首轮启动会纪要
- 纪要包含：本轮目标、交付范围、团队成员、Gate 计划

### 步骤 3. 确认或建立 Todo Registry

- 确认 `docs/todo/TODO_REGISTRY.md` 存在
- 登记本轮 AgentDevFlow 自举任务

### 步骤 4. 加载 AgentDevFlow 交付团队

加载顺序（参考 `/start-agent-team`）：

1. `team-lead` - 负责自举规划和协调
2. `architect` - 负责架构规范
3. `qa-engineer` - 负责质量规范
4. `engineer` - 负责具体实现任务
5. `pmo` - 负责检查流程合规与协同问题

### 步骤 5. 执行首轮检查

每个角色必须完成：

- 读取角色主规范
- 读取角色 playbook
- 读取本阶段工作流
- 读取必要模板
- 检查 issue / gate / todo / risk

### 步骤 6. 明确 AgentDevFlow 自身交付 Gate

- Gate 1: 自举骨架和团队就绪
- Gate 2: 本轮功能实现完成
- Gate 3: 文档 PR 合并（Human Review #1）
- Gate 4: 代码 PR 合并（Human Review #2）
- Gate 5: Issue Comment Gate + 发布

## AgentDevFlow 自举完成判定

- 项目骨架完整
- 启动会纪要已建立
- Todo Registry 可用
- 交付团队已建立
- 首个 Gate 已明确
- 本轮 AgentDevFlow 迭代目标已记录

## 自举输出去向

- 启动会纪要：`docs/memo/`
- 待办注册：`docs/todo/TODO_REGISTRY.md`
- 项目状态板：`docs/memo/`
- AgentDevFlow 自举记录：`docs/memo/agent-bootstrap.md`

## 禁止行为

- 在骨架不完整时启动并发角色
- 跳过角色初始化检查
- 没有明确的 Gate 就开始实现
- 未声明缺失职责归属就默认"之后再说"
