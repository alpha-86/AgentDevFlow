# 团队拓扑

## 目标

定义 AgentDevPipeline 的通用产研协作结构，确保任何项目都能在不依赖特定业务领域角色的前提下完成需求澄清、方案评审、开发、测试和发布。

## 核心角色

### Team Lead

- 负责团队节奏、跨角色协调、流程守门
- 负责会议主持、blocker 升级、交付推进

### Product Manager

- 负责需求拆解、PRD、验收标准、优先级
- 负责需求边界和交付目标的最终口径

### Tech Lead

- 负责技术方案、架构评审、技术门禁
- 负责确认方案的可实现性、可测试性、可维护性

### Engineer

- 负责实现、单元测试、实现文档同步
- 负责把通过评审的方案落成可交付资产

### QA Engineer

- 负责测试设计、验证、质量门禁
- 负责将 PRD/Tech 的要求转换为验证证据

### Researcher

- 负责需求调研、技术调研、方案探索
- 负责在正式立项前提供比较、风险和建议

### Platform/SRE

- 负责环境、流水线、发布稳定性
- 负责上线前后的运行保障与回滚能力

## 推荐组织关系

```text
Team Lead
├── Product Manager
├── Tech Lead
├── Engineer
├── QA Engineer
├── Researcher
└── Platform/SRE
```

## 角色协作关系

| 角色 | 上游输入 | 下游输出 |
|---|---|---|
| Team Lead | 项目目标、当前状态 | 节奏、分工、升级决策 |
| Product Manager | 需求、调研、反馈 | PRD、优先级、验收标准 |
| Tech Lead | 已通过的 PRD | Tech Spec、架构约束、实现切分 |
| Engineer | 已通过的 Tech Spec | 代码、单测、实现说明 |
| QA Engineer | PRD + Tech + 实现 | QA Case、测试报告、缺陷列表 |
| Researcher | 模糊问题或方向 | 调研报告、选项比较、建议 |
| Platform/SRE | 发布需求、运行约束 | 部署方案、发布记录、回滚方案 |

## 基本原则

- 无 PRD 不开发
- 无 Tech Review 不编码
- 无 QA 验证不验收
- 无发布确认不上线
- 所有会议必须留痕
- 所有行动项必须进入 Todo
- 所有关键文档必须可追溯

## 升级原则

- 评审超时由 Team Lead 升级
- 范围冲突由 Product Manager 定口径
- 技术不可行由 Tech Lead 退回
- 质量阻塞由 QA Engineer 持有 gate
- 发布风险由 Platform/SRE 提出阻塞意见
