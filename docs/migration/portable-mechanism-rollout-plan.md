# 可迁移机制落地计划（中文主版本）

## 目标

将 hedge-ai 中“可迁移/部分迁移”的流程机制，按通用产研语义落地到 AgentDevPipeline，形成完整闭环：

`Issue -> PRD -> Tech -> Implementation -> QA -> Release -> 复盘 -> 改进`

## 当前状态

- 中文主版本主干机制已完成首轮落地。
- 后续如有新增机制，继续直接在当前仓库迭代，不再保留其他语言镜像前提。

## 落地范围（第一阶段）

### 1. 流程治理

- 引入 Issue 驱动交付规则（Issue 状态、评论门禁、跨 Gate 追溯）
- 强化 Gate 防绕过机制（未通过不得进入下游）
- 引入签字一致性规则（每个 Gate 的必签角色）

### 2. 文档治理

- 文档状态机（Draft/In Review/Approved/Blocked/Archived）
- Review Record 的最小结构统一
- 变更级别定义（Minor/Major/Breaking）与重审规则

### 3. 会议与执行节奏

- 日会机制（通用研发语义）
- 周度流程复盘（关注交付效率与流程违规）
- Todo 关闭证据标准（链接、截图、提交、报告）

### 4. Agent 编排治理

- Agent 创建前置检查（角色、必读、边界）
- 任务切分与 handoff 契约
- 上下文恢复与断点续作规范（`codex resume` 等）

## 里程碑

### M1：治理骨架

- 输出：Issue/Gate/文档状态机规则
- 位置：`prompts/*` 与 `skills/shared/workflows/*`

### M2：执行模板

- 输出：日会、周会、变更记录、阻塞升级模板
- 位置：`docs/memo/`、`skills/shared/templates/*`

### M3：流程合规

- 输出：合规检查清单、违规升级路径、例外审批机制
- 位置：`prompts/*` 与 `docs/reference/*`

## 不在范围（明确排除）

- 任何交易策略、因子、回测、仓位、盘前盘后机制
- 任何基金组织角色与交易风险口径字段

## 验收标准

- 中文主版本具备完整流程文档，且可独立运行（不依赖 hedge-ai 仓库）。
- 任意流程文档中不出现交易业务语义。
- 每个 Gate 的输入、输出、签字角色、退回路径可追溯。
