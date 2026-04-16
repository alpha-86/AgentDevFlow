# PMO-2026-04-15-GOV-001 — PMO 文档目录结构不规范

## 基本信息

| 字段 | 内容 |
|------|------|
| 级别 | P1 / Fail |
| 日期 | 2026-04-15 |
| 类别 | governance |
| 状态 | Open |

## 问题描述

PMO 的治理文档未统一存放在 `docs/pmo/` 目录下，而是散落在：
- `docs/memo/governance_audit_2026-04-15.md`（应在 `docs/pmo/audit/`）
- `docs/pmo/issues/2026-04-15.md`（daily tracker 应按分类存放）

违反了"所有 PMO 文档统一存放在 `docs/pmo/` 目录下，按问题分类组织"的原则。

## 影响范围

- 治理文档难以追溯
- 新成员难以快速定位相关文件
- 问题记录与审计报告的关联关系不清晰

## 纠正动作

| 动作 | 负责人 | 截止时间 | 状态 |
|------|--------|----------|------|
| 将 `docs/memo/governance_audit_2026-04-15.md` 迁移至 `docs/pmo/audit/2026-04-15_audit.md` | PMO | 2026-04-15 | ✅ 已完成 |
| 将原 `docs/pmo/issues/2026-04-15.md` 内容按分类拆分至 `docs/pmo/issues/role-boundary/`、`docs/pmo/issues/process/`、`docs/pmo/issues/governance/` | PMO | 2026-04-15 | ✅ 已完成 |
| 更新 `docs/pmo/issues/README.md` | PMO | 2026-04-15 | ✅ 已完成 |
| 清理旧文件 | PMO | 2026-04-15 | ✅ 已完成 |

## 状态

- [x] 目录结构已建立
- [x] 文件迁移完成
- [x] README 更新完成
- [x] 旧文件清理完成
- **Closed ✅**
