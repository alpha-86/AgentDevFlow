# Issue 路由与项目组合管理

## 目标

让 Issue 机制支持：

- 多项目并行
- 单项目内多问题并行
- 不同类型任务的默认角色路由
- 项目级优先级和阻塞管理

## 为什么这是核心能力

如果一个团队同时推进多个项目，或者一个项目内同时存在功能、缺陷、异常、流程改进等多条主线，没有清晰 Issue 机制，就会出现：

- 当前主线不清
- owner 冲突
- blocker 无法升级
- 交付物挂错位置
- 会话恢复时不知道该从哪个问题继续

## Issue 最小字段

- Project ID
- Issue ID
- Type
- Priority
- Owner
- Current Gate
- Status
- Linked Artifacts

## Issue 类型

- `feature`
- `bug`
- `research`
- `process`
- `release`
- `anomaly`

## 默认角色路由

- `feature` -> Product Manager
- `bug` -> Engineer
- `research` -> Researcher
- `process` -> Team Lead
- `release` -> Platform/SRE 或 Team Lead
- `anomaly` -> 当前阶段 owner，必要时升级 Team Lead

## 项目组合管理规则

- 每个项目必须有独立 Project ID
- 每个 issue 必须属于某个 project
- Team Lead 必须定期检查每个 project 的活跃 issue 数量、blocked 数量、超期数量
- 多项目并行时必须控制总体并发预算

## 路由失败信号

- issue 无法分类
- owner 缺失
- 没有 Project ID
- 交付物与 issue 不匹配
- issue 已经跨阶段推进但 route 未更新

## 交付要求

- README 和 docs 要能让用户理解 issue 在整个体系里的作用
- workflow 和 template 要能直接承接 issue 路由、产物关联和状态追踪
