---
name: agents
description: AgentDevFlow 角色定义与协作边界
---

# AgentDevFlow 角色定义

本目录包含 AgentDevFlow 的正式角色定义与对应 playbook。

## 正式角色集

| 角色 | 文件 | 一句话职责 |
|------|------|-----------|
| Team Lead | `team-lead.md` | 流程编排与升级协调的唯一负责人 |
| Product Manager | `product-manager.md` | 把需求转成可评审、可实现、可验收的正式交付物 |
| Architect | `architect.md` | 技术可行性判断、架构收敛和 Tech Spec 产出 |
| QA Engineer | `qa-engineer.md` | QA Case Design、验证执行和 QA Report 产出 |
| Engineer | `engineer.md` | 把已确认设计转成代码、测试和实现证据 |
| Platform / SRE | `platform-sre.md` | 环境稳定性、CI/CD 和发布风险控制 |
| PMO | `pmo.md` | 流程合规检查和改进闭环驱动 |

## 角色协作原则

1. 各角色只通过文件交付物协作，不靠口头或聊天传递关键结论
2. 角色间正式交接必须通过 Issue Comment 或结构化文件
3. PMO 不代替任何正式签字角色
4. Team Lead 是唯一编排者和升级协调人

## 禁止行为

- 不得用空白 agent 执行正式角色职责
- 不得跳过角色文件直接开始工作
- 不得忽略初始化确认就接任务
