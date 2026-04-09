# 004 - 2026-04-09 Team Setup 与 Skill Protocol 对照审计

## 目标

对照 `hedge-ai` 的以下来源，审计 AgentDevPipeline 在“团队启动”和“共享协议”两块的落地完整度：

- `.claude/skills/TEAM_SETUP.md`
- `.claude/skills/SKILL_PROTOCOL.md`
- `.claude/skills/start-agent-team/SKILL.md`
- `.claude/skills/create-agent/SKILL.md`

## 一、结论

当前 AgentDevPipeline 已有：

- `prompts/zh-cn/010_team_setup_and_bootstrap.md`
- `docs/zh-cn/governance/skill-protocol.md`
- `prompts/zh-cn/006_agent_creation_contract.md`

但它们大多仍属于“治理规则”，还没有像 `hedge-ai` 那样形成可直接执行的共享启动资产。

## 二、对照后的主要差距

### P0. 缺共享启动入口

当前只有 prompt 规则，没有共享层的 `team-setup` 手册。

后果：

- 项目 kickoff 时只能回看 prompt
- 角色加载顺序、首轮检查、kickoff 产物没有共享入口

### P0. 缺共享 skill protocol 执行版

当前 `docs/zh-cn/governance/skill-protocol.md` 只说明原则，没有进一步下沉到：

- 事件
- 状态
- 输出字段
- 失败和恢复动作

### P1. 缺统一 agent 创建/恢复操作清单

`hedge-ai` 的 `create-agent` 虽然带有平台实现细节，但它有一个通用价值：

- 角色必须通过统一入口创建
- 角色文件必须是第一份必读文档
- 创建后必须立即做初始化检查

本项目当前只在契约层表达，还没形成执行入口。

## 三、本轮落地决策

1. 新增 `skills/shared/team-setup.md`
2. 新增 `skills/shared/skill-protocol.md`
3. 在 `skills/shared/README.md`、`docs/zh-cn/README.md`、`README.md` 中增加入口
4. 继续保持不引入任何量化交易业务角色或自动创建策略类 agent 的语义

## 四、后续项

- 后续还需要补“项目 kickoff 示例目录”
- 后续还需要补“角色创建日志模板”与“首次日会模板”
- 后续还需要补平台侧对 `skill-protocol` 的最小自动化映射示例
