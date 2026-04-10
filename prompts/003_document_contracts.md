# 文档契约

## 目录

- `docs/prd/`
- `docs/tech/`
- `docs/qa/`
- `docs/memo/`
- `docs/todo/`
- `docs/research/`
- `docs/release/`

## 命名

- PRD：`{id}_{name}_{date}.md`
- Tech：`{id}_{name}_tech_{date}.md`
- QA：`{id}_{name}_qa_{date}.md`
- Memo：`{type}_{date}_{topic}.md`

## 强制项

- 每个文档必须有状态、负责人、评审记录
- PRD/Tech/QA 文档必须能互相追溯
- 禁止临时命名和歧义目录
- 所有关键文档必须写明创建日期和最近更新日期
- 所有正式文档必须在文末保留 Review Record

## 文档状态机（统一）

- `Draft`：起草中，未进入正式评审
- `In Review`：评审中，可能带 action items
- `Approved`：通过当前阶段 Gate
- `Blocked`：存在阻塞项，禁止进入下游
- `Archived`：归档，只读保留

状态变更必须记录“变更人、日期、原因”。

## 文档追溯关系

```text
Research -> PRD -> Tech Spec -> QA Case -> Test Report -> Release Record
```

## Gate 签审最小要求

### PRD

- 需求背景
- 范围
- 非范围
- 验收标准
- Gate 1 Review Record

### Tech Spec

- 架构
- 接口
- 数据流
- 风险
- 测试路径
- Gate 2 Review Record

### QA Case / Test Report

- 追溯到 PRD 和 Tech
- 环境说明
- 执行结果
- 缺陷结论

### Release Record

- 发布内容
- 风险说明
- 回滚方式
- 发布结论

## Review Record 最小字段

- 日期
- 阶段（PRD/Tech/QA/Release）
- 评审人
- 结论（Approved/Conditional/Rejected）
- 关键意见
- 待办与负责人
- 下次复审时间（如有）

## 重审触发条件

出现以下任一情况，必须触发重审：

- 需求范围或验收标准变化
- 核心接口、数据结构、发布策略变化
- 关键测试路径变化
- 阻塞缺陷跨阶段传播
