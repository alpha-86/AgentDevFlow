# start-agent-team P0/P1 补齐 & issue-poll 闭环 — Codex Review

## 背景

本次工作响应 `prompts/discuss/030_2026-04-14_start-agent-team能力对比与缺失分析.md` 的 audit findings，补齐 P0 编排缺失和两项 P1 缺口。

## 变更文件

### 1. `skills/shared/start-agent-team.md`

**步骤 0.5 Team 创建检查（重写）**：
- 补全 TeamCreate tooling 显式调用：`TeamCreate(team_name="{project_id}", description="{项目描述}")`
- 指定 Team 配置文件检查路径：`.claude/teams/{team_name}/config.json`
- 新增平台无关 fallback：创建本地 `.claude/teams/{project_id}/config.json`
- 新增禁止重复创建规则

**步骤 3.5 发现并路由待处理任务（新增）**：
- 3.5.1：`python scripts/github_issue_sync.py` 同步 open issues
- 3.5.2：读取 `.claude/task_queue/` 下所有 `.task` 文件
- 3.5.3：读取 `docs/todo/TODO_REGISTRY.md`
- 3.5.4：`python scripts/task_router.py --verbose` 路由到角色
- 3.5.5：汇总启动上下文作为启动会议程依据

### 2. `.github/workflows/issue-poll.yml`（新建）

定时触发 workflow，实现持续触发闭环：
- `on: schedule` cron 每 15 分钟触发
- `on: workflow_dispatch` 支持手动触发
- 完整链路：`cron/workflow_dispatch → github_issue_sync.py → task_router.py → .claude/results/pending_*.md → post-comment workflow`
- 自动 git push 触发 post-comment workflow

### 3. `prompts/discuss/030_2026-04-14_start-agent-team能力对比与缺失分析.md`

- 修正 `--sync-issues` 为 `python scripts/github_issue_sync.py`（与实现一致）
- 第六部分 P1-item4 标注「❌ 未完成」→ 「✅ 完成」
- 新增 8.4 本轮修复记录，含三项完成状态和最终结论「**030 全部完成**」

## 请审查

1. **步骤 0.5 TeamCreate tooling 调用** — 格式和逻辑是否正确？平台无关 fallback 是否合理？
2. **步骤 3.5 编排** — 五步顺序和描述是否准确？是否有遗漏？
3. **issue-poll.yml** — cron 15min 频率是否合理？触发链路是否完整？permissions 是否正确？
4. **整体一致性** — start-agent-team.md、030 文档、issue-poll.yml 三者是否相互印证、无矛盾？
