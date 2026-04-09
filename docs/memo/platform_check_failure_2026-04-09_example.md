# 平台检查失败示例

**平台**: Codex
**日期**: 2026-04-09
**Issue**: #0
**当前 Gate**: Release
**结论**: fail
**执行人**: Platform/SRE

## 检查项结果

- Gate 前置检查: pass
- Issue 检查: warning
- 产物关联检查: fail
- 状态一致性检查: pass

## 失败原因

- Release Record 已存在，但主 Issue 下缺少对应 release 决策 comment
- 产物关联表缺少 PR / merge 链接与 release comment 链接

## 阻断范围

- 当前 release 不能继续推进
- issue 不能进入 `done`

## 修复 Owner

- Platform/SRE：补 release 决策 comment
- Team Lead：确认 issue 状态未被提前关闭

## 重试条件

- 主 Issue 已补齐 release 决策 comment
- 产物关联表已补齐缺失链接
- Release 状态与 QA 结论保持一致

## 重试结果

- 待重试

## 相关链接

- `docs/release/000_release_record_2026-04-09.md`
- `docs/memo/artifact_linkage_2026-04-09_example.md`
