# AgentDevFlow

AgentDevFlow 是一套面向软件研发交付的多 Agent 流程资产包。它解决的不是“单个 Agent 会不会写代码”，而是多角色协作时经常失控的那部分：需求澄清、方案评审、实现、测试、发布、留痕、恢复和人机协同 Gate。

## 它解决什么问题

很多团队已经在用 Claude、Codex 或其他 Agent 工具，但真正容易失控的是流程层：

- 需求、方案、实现、测试之间断链
- 评审靠聊天推进，没有正式 Gate
- 问题并行时 owner、状态、证据混乱
- 会话切换后上下文恢复成本高
- 不同平台各写一套编排规则，重复造轮子

AgentDevFlow 提供的是一套可复用的共享角色、workflow、template 和平台入口约束，让这些问题可以被系统化处理。

## 主线机制

AgentDevFlow 当前的主干机制是：

- Issue First
- 问题先于方案
- 双阶段 PR
- Human Review #1 / #2
- Issue Comment Gate
- Todo / Memo / Change Record 正式留痕
- Process Auditor 主动检查
- 上下文恢复优先从 issue / gate / todo / risk 开始

完整定义见 [核心原则](./docs/governance/core-principles.md)。

## 完整流程

```text
需求 / 问题 / 异常
        │
        ▼
创建主 Issue
        │
        ▼
PM 澄清问题
每轮讨论必须回链
        │
        ▼
PRD
不含技术实现
        │
        ▼
架构评审 + QA Gate
        │
        ▼
QA Case Design
        │
        ▼
文档 PR
PRD + Tech + QA Case
        │
        ▼
Human Review #1
合并 = 设计确认
        │
        ▼
实现与验证
        │
        ▼
代码 PR
代码 + 测试报告
        │
        ▼
Human Review #2
合并 = 实现确认
        │
        ▼
Issue Comment Gate
        │
        ▼
Release / 验收 / Human 关闭
```

## 默认角色

默认团队：

- Team Lead
- Product Manager
- 架构师
- Engineer
- QA Engineer
- Platform/SRE
- Process Auditor

按需启用：

- 研究支持

说明：

- `架构师` 是 1.0 的正式角色口径，对应 `skills/shared/agents/architect.md`
- 遗留的 `tech-lead` 文件已标记为兼容层，仅供遗留引用

## 如何开始

如果你要在当前仓库里直接启动 AgentDevFlow，按这个顺序读：

1. [插件入口](./plugins/agentdevflow/README.md)
2. [文档总览](./docs/README.md)
3. [核心原则](./docs/governance/core-principles.md)
4. [依赖清单](./docs/reference/dependencies.md)
5. [Claude 接入](./docs/platforms/claude-code.md) 或 [Codex 接入](./docs/platforms/codex.md)
6. [共享技能目录](./skills/shared/README.md)
7. [启动团队](./skills/shared/start-agent-team.md)
8. [创建角色实例](./skills/shared/create-agent.md)

## Telegram Bot 部署

AgentDevFlow 支持通过 Telegram Bot 向用户发送状态通知。

### 配置步骤

1. **获取 Bot Token**
   - 在 Telegram 中搜索 @BotFather
   - 发送 `/newbot` 创建新 Bot
   - 复制获得的 Bot Token

2. **配置环境变量**

   ```bash
   export TELEGRAM_BOT_TOKEN=<your-bot-token>
   export TELEGRAM_CHAT_ID=<your-chat-id>
   ```

3. **部署 systemd Service**

   ```bash
   # 复制 service 文件
   sudo cp scripts/telegram_bot.service /etc/systemd/system/

   # 编辑 token
   sudo vim /etc/systemd/system/telegram_bot.service
   # 在 [Service] 段的 Environment= 中设置 TELEGRAM_BOT_TOKEN

   # 启用并启动
   sudo systemctl daemon-reload
   sudo systemctl enable telegram_bot
   sudo systemctl start telegram_bot
   ```

4. **验证连接状态**

   ```bash
   # 检查服务状态
   sudo systemctl status telegram_bot

   # 查看日志
   journalctl -u telegram_bot -f

   # 发送测试消息
   python scripts/send_telegram.py --test
   ```

### 相关文件

- `scripts/telegram_bot.service` - systemd service 配置
- `scripts/send_telegram.py` - 消息发送 CLI 工具
- `hedge_ai/telegram/` - Bot 服务端实现

## 资产结构

- `plugins/agentdevflow/`
  平台入口与插件装载说明
- `skills/shared/`
  共享角色、workflow、template、启动协议
- `prompts/`
  规则层和阶段机制
- `docs/`
  说明、治理、示例、验收与审计
- `adapters/`
  平台适配入口

## 复用原则

AgentDevFlow 不重复实现平台已经具备的能力。

优先复用：

- Claude 现有 Agent Team 能力
- Codex 现有多 agent 调度能力
- Git / Issue / PR / CI / `gh`
- 已有 skills、plugin、agents 包

只有当现成能力不能承载主干机制时，才在本仓库补充自己的入口或约束。

## 问题反馈

如果你发现问题或有改进建议，欢迎通过 GitHub Issue 反馈。
