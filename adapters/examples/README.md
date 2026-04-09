# Adapter Examples

这里集中放跨平台可复用的自动化检查骨架，而不是分散写在每个平台说明里。

适用原则：

- 只表达共享流程检查，不表达平台私有业务逻辑
- 只作为样例和骨架，不默认代表当前仓库已启用真实自动化
- 所有检查语义必须对齐 `skills/shared/event-bus.md` 和 `docs/zh-cn/governance/platform-minimum-checks.md`

当前样例：

- `gate-check-workflow.example.yml`
- `issue-comment-check.example.yml`
