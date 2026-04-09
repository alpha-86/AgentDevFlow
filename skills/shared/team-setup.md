# Team Setup

## 目标

为 AgentDevPipeline 的真实项目 kickoff 提供统一的共享启动入口，确保团队在进入正式交付前，先完成角色加载、主 issue 建立、交付目录初始化和首轮状态检查。

## 启动前置条件

1. 已明确项目目标或本轮交付目标。
2. 已指定 Team Lead。
3. 已确定本轮需要参与的角色。
4. 已创建主 issue 或等价的工作主索引。
5. 已明确本轮并发预算。
6. 已明确项目标识 `project_id`。
7. 已明确当前阶段是新项目 kickoff、增量需求还是异常修复。

## 推荐角色集合

- Team Lead
- Product Manager
- Tech Lead
- Engineer
- QA Engineer
- Researcher
- Platform/SRE
- Process Auditor

不是每个项目都必须启用所有角色，但必须明确：

- 哪些角色已启用
- 哪些角色暂不启用
- 缺失角色的职责由谁临时承担

## 启动顺序

1. Team Lead 确认目标、范围、角色、节奏和评审 SLA。
2. Product Manager 确认主 issue、需求来源和 PRD 入口。
3. Tech Lead 确认技术边界、依赖和 Tech Review 边界。
4. QA Engineer 确认介入时机、验证路径和 QA 资产要求。
5. Platform/SRE 确认环境、发布、回滚和平台检查边界。
6. Process Auditor 确认审计范围、例外审批和首轮检查计划。
7. 所有角色完成必读文档加载和初始化检查。

## 统一启动命令视角

如果平台支持统一命令或入口，应把团队启动视为以下固定顺序：

1. 读取 `team-setup.md`
2. 读取 `skill-protocol.md`
3. 读取 `event-bus.md`
4. 确认主 issue、todo registry、项目状态板
5. 激活角色
6. 执行 kickoff 或首轮日会

## 角色加载顺序

1. 角色主规范
2. 角色 playbook
3. 团队拓扑
4. 文档契约
5. 交付 Gate
6. Issue / Todo / Comment 规则
7. 当前需要使用的 workflow
8. 当前阶段需要的 template

## 启动检查清单

- 主 issue 已存在
- `project_id` 已存在
- 当前阶段已明确
- 当前 owner 已明确
- 首轮 PRD / Tech / QA / Release 路径已明确
- Todo registry 已存在并可使用
- 项目状态板已存在并可使用
- kickoff memo 已创建
- 例外审批需求已判断
- 审计范围已明确

## 启动完成判定

- 每个角色都知道自己的输入、输出、禁止越权边界
- 当前 issue 已建立并可回链文档
- 当前阶段与下一 Gate 已明确
- 首次 kickoff memo 已完成
- 首轮审计计划已存在
- 平台检查入口和人工补录路径已明确

## 禁止行为

- 未建立主 issue 就直接开始多角色并行
- 角色未加载必读文档就开始做关键判断
- kickoff 后没有 memo 和 action items
- 不明确缺失角色由谁承担其职责
