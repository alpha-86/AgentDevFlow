# Create Agent

## 目标

提供共享的 Agent 创建统一入口，避免使用空白角色或泛化 prompt 创建关键流程角色，确保每个角色都带着完整的职责、必读文档、初始化动作和恢复顺序进入项目。

## 适用角色

- `team-lead`
- `product-manager`
- `tech-lead`
- `engineer`
- `qa-engineer`
- `researcher`
- `platform-sre`
- `process-auditor`

## 执行前必读

1. `prompts/zh-cn/006_agent_creation_contract.md`
2. `skills/shared/skill-protocol.md`
3. `skills/shared/event-bus.md`
4. 对应角色文件
5. 对应角色 playbook

## 创建步骤

### Step 0. 验证上下文

- 当前项目 `project_id` 已存在
- 主 issue 已存在
- 当前阶段已明确
- 当前角色是否真的需要启用

### Step 1. 解析角色类型

根据输入角色映射到：

- `skills/shared/agents/{role}.md`
- `skills/shared/agents/{role}.playbook.md`

### Step 2. 读取并提取关键内容

必须完整提取：

- Critical Rules
- 核心职责
- 必读文档
- 初始化后必做
- 上下文恢复
- 禁止行为
- 输出格式

### Step 3. 组装角色上下文

角色 prompt 中至少必须包含：

- 角色定义
- Critical Rules
- 必读文档清单
- 初始化动作
- 当前应读取的 workflow
- 当前应使用的 template
- Issue / Gate / Human Review 责任
- 禁止行为
- 恢复顺序

### Step 4. 激活后立即检查

角色激活后必须立即完成：

1. 读取主 issue
2. 读取最新 Gate 结论
3. 读取 todo registry
4. 读取当前阶段 workflow
5. 输出自己的初始化确认结果

## 初始化确认最小格式

- 角色
- project_id
- issue_id
- 当前阶段
- 已读取文档
- 当前 blocker
- 下一动作

## 创建日志要求

创建或激活后必须写入：

- agent 类型
- 读取的角色文件
- 读取的 playbook
- project_id
- issue_id
- 创建时间
- 创建者

推荐使用：

- `templates/agent-activation-template.md`
- `templates/agent-creation-log-template.md`

## 禁止行为

- 用通用空白 agent 执行正式角色职责
- 跳过角色文件或 playbook 直接开始工作
- 忽略初始化检查
- 未确认 issue / gate 状态就直接接任务
