# 023 Phase 1.7 WORKFLOWS 复核

## 复核范围

- `prd-review.md`
- `tech-review.md`
- `daily-standup.md`
- `todo-management.md`
- `weekly-review.md`
- `monthly-review.md`
- `anomaly-iteration.md`
- `debate.md`
- `strategy-review.md`
- `strategy-debate.md`
- `factor-review.md`
- `backtest-review.md`
- `risk-report.md`
- `daily-report.md`

## 复核结论

### 插件 workflow 主干来源

以下 workflow 可以作为插件主干来源：

- `prd-review.md`
- `tech-review.md`
- `daily-standup.md`
- `todo-management.md`
- `weekly-review.md`
- `monthly-review.md`

原因：

- 这些流程描述的是通用研发阶段评审、日会、Todo 闭环、周期复盘。

### 部分迁移的 workflow

- `anomaly-iteration.md`
  - 保留异常发现、分级、修复、验证闭环
  - 去掉交易事故、信号异常等业务口径
- `debate.md`
  - 保留对抗式评审框架
  - 不保留策略 / 因子辩论业务语境
- `daily-report.md`
  - 只保留通用进展日报结构，不作为插件主干 workflow
- `risk-report.md`
  - 只可参考工程风险汇报结构，不作为插件主干 workflow

### 禁止进入插件主干的 workflow

- `strategy-review.md`
- `strategy-debate.md`
- `factor-review.md`
- `backtest-review.md`

原因：

- 这些流程直接绑定量化交易研究、因子、回测、策略辩论语义。

## 对插件目标的直接影响

后续 `skills/shared/workflows/` 的主干应继续围绕：

- 启动
- PRD
- Tech
- 日会
- Todo
- 异常
- 周/月复盘

而不是回到策略研究或回测语义。

## 回写到计划

- `1.7` 已完成
