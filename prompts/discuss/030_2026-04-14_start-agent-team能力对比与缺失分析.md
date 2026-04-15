# 030 start-agent-team 能力对比与缺失分析

**日期**: 2026-04-14
**分析来源**: `prompts/by-me/005_V5_start-agent-team能力分析.md`
**对比基准**: hedge-ai `.claude/skills/start-agent-team/SKILL.md`

---

## 一、需求回顾

1. 安排创建 agent team，让每个 agent 按照规定的方式去创建
2. 检查所有任务清单包括 github issue、`.claude/task_queue/`、todo 等
3. 基于 2 的内容，召集团队开 DBR 日会

---

## 二、hedge-ai 能力清单

### 2.1 Agent 创建机制

| 能力项 | hedge-ai 现状 |
|--------|---------------|
| Team 创建检查 | ✅ 有 Step 1.5，强制检查 Team 是否存在，不存在则创建 |
| Agent 创建命令 | ✅ 明确使用 TeamCreate tooling，按顺序创建 |
| Agent 必读文档分配 | ✅ 每个 Agent 有明确的必读文档速查表 |
| Agent 创建日志 | ✅ 记录到 `.claude/agent-creation-log.md` |
| 创建后立即初始化 | ✅ 创建完下一个 Agent 后直接继续，无确认环节 |

### 2.2 任务发现机制

| 能力项 | hedge-ai 现状 |
|--------|---------------|
| GitHub Issue 列表 | ✅ Agent 有触发条件关联 GitHub Issue |
| Todo 管理 | ✅ `WORKFLOWS/todo-management.md` |
| 每日四次 DBR | ✅ 08:00, 12:00, 16:00, 20:00 |
| 日会内容覆盖 | ✅ 进展 + 阻塞 + 优先级 + 决策 + Todo |
| 会议记录三合一 | ✅ 保存到 docs/MEMO + git push + Telegram 摘要 |

### 2.3 Agent 触发机制

| Agent | 触发条件 | 关联文档 |
|-------|---------|---------|
| Team Lead | 每日08:00 | daily-standup.md |
| CSO | 每周一11:00 | strategy-review.md |
| CRO | 每日16:00 | risk-report.md |
| PM Agent | 辩论触发条件满足 | strategy-debate.md |
| Backtest Agent | 策略回测完成时 | backtest-review.md |
| SRE | 每日08:00/16:00 | daily-standup.md |

---

## 三、AgentDevFlow 能力清单

### 3.1 Agent 创建机制

| 能力项 | AgentDevFlow 现状 | 差距 |
|--------|-------------------|------|
| Team 创建检查 | ❌ 无，只有文字描述"确认团队负责人" | 缺失 tooling |
| Agent 创建命令 | ❌ 无，只有文字描述"加载团队角色" | 缺失 tooling |
| Agent 必读文档分配 | ⚠️ 有提及，但不具体到每个 Agent | 部分缺失 |
| Agent 创建日志 | ❌ 无 | 缺失 |
| 创建后立即初始化 | ❌ 无流程约束 | 缺失 |

### 3.2 任务发现机制

| 能力项 | AgentDevFlow 现状 | 差距 |
|--------|-------------------|------|
| GitHub Issue 自动发现 | ❌ 无，skill 文本说"确认主 issue"但无执行能力 | **严重缺失** |
| `.claude/task_queue/` 读取 | ❌ 无集成 | 缺失 |
| Todo 管理 | ⚠️ 有 `workflows/todo-review.md`，但无定时触发 | 部分缺失 |
| 每日 DBR 定时 | ❌ 无 schedule | 缺失 |
| 日会内容覆盖 | ⚠️ 有 `daily-sync.md`，但缺少 DBR #1/#2/#3 差异化 | 部分缺失 |
| 会议记录三合一 | ❌ 无 save + git push + Telegram 集成 | 缺失 |

### 3.3 Agent 触发机制

| 能力项 | AgentDevFlow 现状 | 差距 |
|--------|-------------------|------|
| 按触发条件激活 Agent | ❌ 无 | **严重缺失** |
| Issue 触发 Workflow | ⚠️ 有 `issue-lifecycle.md` 设计，但无触发机制 | 缺失 |
| 定时任务 | ❌ 无 | 缺失 |

---

## 四、核心差距总结

### 4.1 自举悖论

```
问题：/adf-start-agent-team 本身需要"先检查 open issues"，
但 skill 定义里没有任何 tooling 调用指令，只是告诉人类"去检查"。

hedge-ai 的 skill 包含 TeamCreate 等 tooling 调用，
AgentDevFlow 的 skill 只有 markdown 描述。
```

### 4.2 tooling 能力现状（需修正确认）

| tooling | 用途 | 现状 |
|---------|------|------|
| `scripts/github_issue_sync.py` | 发现/同步 GitHub Issues | ✅ 工具存在，但 skill 未调用 |
| `.claude/task_queue/` | 读取待处理任务 | ✅ 目录存在，无 skill 集成 |
| `docs/todo/TODO_REGISTRY.md` | 读取 todo | ✅ 文档存在，无 skill 集成 |
| TeamCreate | 创建 Agent Team | ⚠️ Claude Agent Team 内置，skill 文本未调用 |
| create-agent | 创建具体 Agent | ⚠️ 有 skill 文档，无 skill 集成 |

### 4.3 缺失的 workflow 能力

| workflow | 现状 |
|-----------|------|
| DBR 日会定时触发 | ❌ 无 |
| 日会记录三合一（save + git push + Telegram） | ❌ 无 |
| Agent 按触发条件激活 | ❌ 无 |
| GitHub Issue -> Agent 路由 | ❌ 无 |

---

## 五、GitHub Issue 能力迁移完整性检查

### 5.1 已迁移

| 文件 | 状态 |
|------|------|
| `issue-lifecycle.md` | ✅ 已迁移，有状态机设计 |
| `issue-routing.md` | ✅ 已迁移，有角色路由 |
| `issue-status-sync.yml` | ✅ 已迁移 |
| `post_comments.py` | ✅ 已迁移 |

### 5.2 未迁移或缺失

| 能力 | 现状 | 优先级 |
|------|------|--------|
| Issue 自动发现 | ⚠️ github_issue_sync.py 存在，但 skill 未集成调用 | P0 |
| Issue 触发 Agent | ❌ 无触发机制 | P1 |
| Issue 评论自动留痕 | ⚠️ 部分有，无完整集成 | P1 |
| Issue 状态变更 -> Workflow | ❌ 无 | P2 |

---

## 六、建议修复方向

### P0（立即修复）

1. **修改 `skills/shared/start-agent-team.md` 源文件，加入 tooling 调用**
   - `scripts/github_issue_sync.py` 发现 open issues
   - 读取 `.claude/task_queue/` 目录
   - 读取 `docs/todo/TODO_REGISTRY.md`

2. **实现 `adf-daily-standup` workflow**
   - 定时触发（可选，依赖平台能力）
   - 自动收集 open issues、task_queue、todo
   - 生成日会内容

### P1（短期修复）

3. **Agent 触发机制设计**
   - 定义 Agent 激活触发条件
   - 与 issue lifecycle 集成

4. **会议记录三合一**
   - save + git push + Telegram 摘要

### P2（中期修复）

5. **TeamCreate tooling 集成**
   - 参照 hedge-ai 的 Step 1.5
   - 检查 Team 状态，不存在则创建

---

## 七、结论

`/adf-start-agent-team` 当前状态：

- **设计层面**：有完整的流程描述和文档结构
- **执行层面**：tooling 存在（github_issue_sync.py），但 skill 未调用
- **自举悖论**：要求"检查 open issues"但 skill 文本里没有调用指令

**根因**：`skills/shared/start-agent-team.md` 本身是纯 markdown 描述，bootstrap-sync 只做路径替换和 SKILL.md 生成，没有能力补全 tooling 调用。

**真正的修复点**：`skills/shared/start-agent-team.md` 源文件需要加入 `scripts/github_issue_sync.py` 调用指令，bootstrap-sync 生成的 `.claude/skills/adf-start-agent-team/SKILL.md` 才能继承 tooling 能力。
