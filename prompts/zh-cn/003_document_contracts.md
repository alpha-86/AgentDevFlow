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
