# 日会 Workflow

## 目标

同步状态、阻塞、优先级和下一步动作。

## 触发时机

- 每个工作日开始时
- 关键 Gate 前
- 出现 blocker、范围变更或状态漂移时
- 上下文恢复后重新接手时

## 输入

- `project_id`
- 当前 todos
- 打开的 reviews
- 当前交付阶段
- 进行中的关联 issues
- 当前项目状态板

## 议程

1. 昨日进展
2. 今日计划
3. blockers
4. gate 或 review 风险
5. todo 跟进
6. 当日需要决策的事项

## 输出

- 日会 memo
- 更新后的 owner 和 due date
- 必要的升级动作
- 必要的 issue comment 或 gate 纠偏动作

## 日会 Memo 必填字段

- project_id
- 关联 issue IDs
- 每个 issue 当前 gate
- blocker owner 和升级路径
- 下一次 review 或 gate 准入条件

## 会前必做

1. 读取本 workflow。
2. 检查主 issue 与项目状态板是否一致。
3. 检查最近一次 memo、todo registry 和 blocker。
4. 检查是否有 overdue review、缺失 comment、缺失 signoff。

## 禁止行为

- 不读取 workflow 就主持日会
- 只汇报进展，不同步 gate 风险和阻断项
- 发现 issue / gate / todo 状态漂移却不纠正
