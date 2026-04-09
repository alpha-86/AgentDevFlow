# Issue 路由与项目组合管理 Workflow

## 目标

让 issue 机制不仅能支撑单项目交付，还能支撑多项目并行、项目内问题拆分和角色路由。

## 适用场景

- 同时推进多个项目
- 单个项目中并行多个需求或问题
- 异常、流程改进、功能需求混合存在

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

## 项目组合字段

- project id
- issue type
- current owner
- current gate
- priority
- linked artifacts

## 路由步骤

1. 创建 issue 时补齐项目组合字段。
2. 按 issue type 指派默认 owner。
3. 由 Team Lead 在日会或周度复盘中检查 owner 和优先级是否合理。
4. 若 issue 需要跨角色协同，记录次级 owner 和 handoff 计划。

## 组合管理检查点

- 每个项目当前打开 issue 数量
- 每个 owner 当前活跃 issue 数量
- blocked issue 数量
- 超期 issue 数量

## 失败信号

- issue 无法归类
- owner 不明确
- 多项目并行时缺少 project id
- issue 已跨阶段推进，但 route 未更新
