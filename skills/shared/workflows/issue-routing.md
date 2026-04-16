# Issue 路由与项目组合管理工作流

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

- `feature` -> 产品经理
- `bug` -> Engineer
- `research` -> 研究员
- `process` -> 团队负责人
- `release` -> 平台与发布负责人 或 团队负责人
- `anomaly` -> 当前阶段 负责人，必要时升级 团队负责人

## 项目组合字段

- project id
- issue type
- current 负责人
- current gate
- priority
- linked artifacts

## 推荐模板与输出目录

- 项目组合视图：`skills/shared/templates/project-portfolio-template.md`
- 审计报告：`skills/shared/templates/audit-report-template.md`
- 推荐输出目录：`docs/memo/` 或项目治理目录

## 路由步骤

1. 创建 issue 时补齐项目组合字段。
2. 按 issue type 指派默认 负责人。
3. 由 团队负责人 在日会或周度复盘中检查 负责人 和优先级是否合理。
4. 若 issue 需要跨角色协同，记录次级 负责人 和 交接 计划。

## 阶段最小产物集合

- 一份项目组合视图或等价状态表
- 当前 负责人 和 current gate 记录
- 必要时的一份审计结论

## 组合管理检查点

- 每个项目当前打开 issue 数量
- 每个 负责人 当前活跃 issue 数量
- 阻塞 issue 数量
- 超期 issue 数量

## 失败信号

- issue 无法归类
- 负责人 不明确
- 多项目并行时缺少 project id
- issue 已跨阶段推进，但 route 未更新
