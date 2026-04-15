# 030 start-agent-team 能力对比与缺失分析

**日期**: 2026-04-14
**分析来源**: `prompts/by-me/005_V5_start-agent-team能力分析.md`
**对比基准**: hedge-ai `.claude/skills/start-agent-team/SKILL.md`
**重要说明**: 本文档所有根因主体均为 `skills/shared/start-agent-team.md`，`.claude/skills/adf-start-agent-team/SKILL.md` 是 bootstrap-sync 生成的重命名产物，不是根因主体。

---

## 一、需求回顾

1. 安排创建 agent team，让每个 agent 按照规定的方式去创建
2. 检查所有任务清单包括 GitHub Issue、`.claude/task_queue/`、todo 等
3. 基于第 2 项内容，召集团队开日同步会

---

## 二、hedge-ai 能力清单

> **注**：以下对比项中，带 ~~删除线~~ 的为 hedge-ai 特定业务运营机制，不属于通用研发流程，不应作为 AgentDevFlow 的缺失项。

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
| ~~每日四次 DBR~~ | ~~08:00, 12:00, 16:00, 20:00~~（业务运营节奏） |
| 日会内容覆盖 | ✅ 进展 + 阻塞 + 优先级 + 决策 + Todo |
| ~~会议记录三合一~~ | ~~save + git push + Telegram 摘要~~（业务运营机制） |

### 2.3 Agent 触发机制

| Agent | 触发条件 | 关联文档 |
|-------|---------|---------|
| Team Lead | 每日08:00 | daily-standup.md |
| CSO | 每周一11:00 | strategy-review.md（业务） |
| CRO | 每日16:00 | risk-report.md（业务） |
| PM Agent | 辩论触发条件满足 | strategy-debate.md（业务） |
| Backtest Agent | 策略回测完成时 | backtest-review.md（业务） |
| SRE | 每日08:00/16:00 | daily-standup.md |

---

## 三、`skills/shared/start-agent-team.md` 能力现状分析

> **注**：根因主体为 `skills/shared/start-agent-team.md`。`.claude/skills/adf-start-agent-team/SKILL.md` 只是 bootstrap-sync 的重命名产物。

### 3.1 Agent 创建机制

| 能力项 | `skills/shared/start-agent-team.md` 现状 | 判断 |
|--------|----------------------------------------|------|
| Team 创建检查 | ⚠️ `skills/shared/create-agent.md` 定义了 `team-lead` 为 Human 本身并禁止重复创建，但这 **不等于** hedge-ai Step 1.5 的 Team 存在性检查 + Team 不存在时自动创建。当前既缺少 Team 存在性检查的规则明确定义，也缺少对应的统一 tooling。 | **规则缺口 + tooling缺口 + 编排缺失**（三重叠加，不能仅归为编排） |
| Agent 创建命令 | ⚠️ `skills/shared/create-agent.md` 已定义 `create-agent` skill，但 `start-agent-team` 只描述"加载团队角色"，未给出执行步骤 | 规则存在，**缺少自动编排** |
| Agent 必读文档分配 | ✅ `skills/shared/create-agent.md` 中每个角色有明确的必读文档要求 | 已完整 |
| Agent 创建日志 | ✅ `skills/shared/create-agent.md` 要求记录创建日志 | 已完整 |
| 创建后立即初始化 | ✅ `skills/shared/create-agent.md` 定义了激活后立即检查 | 已完整 |

### 3.2 任务发现机制

| 能力项 | `skills/shared/start-agent-team.md` 现状 | 判断 |
|--------|----------------------------------------|------|
| GitHub Issue 发现 | ⚠️ `scripts/github_issue_sync.py` 已存在并可用于发现 / 同步 open issues，但 `start-agent-team` 尚未将其纳入启动步骤 | **工具已存在，缺少启动流程集成 / 编排** |
| `.claude/task_queue/` 读取 | ⚠️ 目录存在，但 `start-agent-team` 未编排读取步骤 | **缺少流程编排** |
| Todo 管理 | ✅ `skills/shared/workflows/todo-review.md` 已定义，但无定时触发 | 规则存在，缺少触发 |
| 日同步会 | ✅ `skills/shared/workflows/daily-sync.md` 已定义，但 `start-agent-team` 未编排为启动步骤 | **缺少流程编排** |
| 会议记录 | ✅ `skills/shared/templates/memo-template.md` 等已定义，但三合一机制为业务运营语义 | 不适用于通用研发 |

### 3.3 Agent 触发机制

| 能力项 | `skills/shared/start-agent-team.md` 现状 | 判断 |
|--------|----------------------------------------|------|
| Issue 触发 Workflow | ✅ `skills/shared/workflows/issue-lifecycle.md` 已定义，但无触发集成 | 规则存在，**缺少触发编排** |
| 统一触发/编排闭环 | ⚠️ `scripts/task_router.py` 存在，但 `start-agent-team` 未编排路由步骤 | 工具存在，**缺少流程编排** |

---

## 四、核心差距总结

### 4.1 问题根因

**根因主体**：`skills/shared/start-agent-team.md`

```
问题：`skills/shared/start-agent-team.md` 需要"先检查 open issues"，
但源文件里没有任何 tooling 调用指令，只是告诉人类"去检查"。

bootstrap-sync 只做路径替换和 SKILL.md 生成，不会补全 tooling 调用。
```

### 4.2 tooling 能力现状

| tooling | 用途 | 现状 |
|---------|------|------|
| `scripts/github_issue_sync.py` | 发现/同步 GitHub Issues | ✅ 工具存在，`start-agent-team` 未集成 |
| `.claude/task_queue/` | 读取待处理任务 | ✅ 目录存在，未编排读取步骤 |
| `docs/todo/TODO_REGISTRY.md` | 读取 todo | ✅ 文档存在，未编排读取步骤 |
| `scripts/task_router.py` | 任务路由 | ✅ 工具存在，未编排触发 |
| `skills/shared/create-agent.md` | Agent 创建规则 | ✅ 规则存在，启动流程未编排 |
| **Team 创建/检查 tooling** | Team 存在性检查 + 不存在时自动创建（对应 hedge-ai Step 1.5） | ⚠️ 尚未被证明存在，等价性未验证 |

### 4.3 编排缺失的 workflow 能力

| workflow | 现状 |
|-----------|------|
| GitHub Issue 发现 -> 启动流程 | ❌ `start-agent-team` 未编排 github_issue_sync.py 调用 |
| task_queue 读取 -> 启动流程 | ❌ `start-agent-team` 未编排 task_queue 读取步骤 |
| todo 读取 -> 启动流程 | ❌ `start-agent-team` 未编排 todo 读取步骤 |
| issue -> Agent 路由闭环 | ⚠️ 已有 issue-routing.md 和 task_router.py，但缺少统一触发/编排闭环 |

---

## 五、GitHub Issue 能力迁移完整性检查

### 5.1 已迁移

| 文件 | 状态 |
|------|------|
| `skills/shared/workflows/issue-lifecycle.md` | ✅ 已迁移，有状态机设计 |
| `skills/shared/workflows/issue-routing.md` | ✅ 已迁移，有角色路由规则 |
| `scripts/task_router.py` | ✅ 已迁移，有路由脚本 |
| `.github/workflows/issue-status-sync.yml` | ✅ 已迁移 |
| `scripts/post_comments.py` | ✅ 已迁移 |

### 5.2 需补充编排

| 能力 | 现状 | 修复方向 |
|------|------|---------|
| Issue 发现 -> 启动流程 | ⚠️ github_issue_sync.py 存在，但 start-agent-team 未集成 | 在 `start-agent-team.md` 中编排调用 |
| 统一触发/编排闭环 | ⚠️ 已有路由规则和 task_router.py，但缺少触发层 | 设计触发机制 |

---

## 六、建议修复方向

### P0（立即修复）

1. **修改 `skills/shared/start-agent-team.md`，编排 GitHub Issue 发现步骤**
   - 调用 `scripts/github_issue_sync.py` 发现 open issues（默认行为即为 sync issues，无 --sync-issues 参数）
   - 编排读取 `.claude/task_queue/` 目录
   - 编排读取 `docs/todo/TODO_REGISTRY.md`

2. **修改 `skills/shared/start-agent-team.md`，编排任务发现步骤**
   - 将 todo review 作为启动会前检查项

### P1（短期修复）

3. **补充 Team 创建检查步骤**
   - 在 `start-agent-team.md` 中编排 Team 状态检查
   - 参照 hedge-ai Step 1.5
   - 此项为启动前置条件，提升优先级至 P1

4. **补充 issue -> Agent 触发编排**
   - 在 `start-agent-team.md` 或独立 workflow 中定义触发机制
   - 与 `task_router.py` 集成
   - **当前状态**：⚠️ 部分完成 — poll workflow 已新增，但下游触发链（与 post-comment.yml 的集成）尚未验证

---

## 七、结论

**根因主体**：`skills/shared/start-agent-team.md`

| 维度 | 判断 |
|------|------|
| **规则层面** | 大部分规则已定义（`create-agent.md`、`issue-lifecycle.md`、`issue-routing.md` 等），但 Team 创建检查层仍有规则缺口 |
| **工具层面** | 部分工具已存在（`github_issue_sync.py`、`task_router.py` 等），但 Team 级统一 tooling 尚未被证明完整迁移 |
| **编排层面** | P0 启动流程已补齐（github_issue_sync、task_queue、todo、task_router 已编排），但启动后持续触发层仍有缺口 |
| **触发层面** | issue-poll.yml 已新增（cron 每 15 分钟），当前未与 post-comment.yml 集成，未设计为自动触发下游 |

**缺失性质分类**：
- 规则缺失：⚠️ 少量存在（尤其 Team 创建检查层 — `create-agent.md` 的 team-lead is Human 规则不等于 Team 存在性检查规则）
- tooling 缺失：⚠️ 少量存在（尤其缺少 Team 级统一 tooling 证据，无法证明等价于 hedge-ai Step 1.5 的 Team 创建能力）
- **编排缺失**：✅ 已补齐（启动流程五步已编排）
- **触发缺失**：⚠️ 部分存在（poll workflow 已建立，下游触发链待验证）

**不属于通用研发缺失项**（业务运营语义）：
- 每日四次 DBR（hedge-ai 特定业务节奏）
- DBR #1/#2/#3 差异化（A股市场特定）
- save + git push + Telegram 摘要三合一（Telegram 业务通知）

---

## 八、Codex Review 补充审计（2026-04-15）

### 8.1 本轮确认已修正的问题

1. **GitHub Issue 检查入口口径已修正**
   - 不应直接写成调用 `gh issue list`。
   - 本项目已经有统一脚本 `scripts/github_issue_sync.py`，`start-agent-team` 若要补齐 issue 检查能力，应优先通过该脚本发现 / 同步 open issues。

2. **真正应修改的对象是共享源 skill，不是别名产物**
   - `/adf-start-agent-team` 只是 `/start-agent-team` 在本项目 `.claude/skills/` 下的重命名产物。
   - 真正的源定义位于 `skills/shared/start-agent-team.md`。
   - 能力缺口、修复点、设计责任都应首先落在 `skills/shared/start-agent-team.md`。

3. **问题主体已统一为 `skills/shared/start-agent-team.md`**
   - 前文 4.1"自举悖论"和第七部分结论的主语已统一修正。

4. **缺失判断已区分三类**
   - 规则缺失
   - tooling 缺失
   - 编排 / 自动触发缺失

5. **hedge-ai 业务语境项已排除**
   - 每日四次 DBR、DBR #1/#2/#3 差异化、save+git push+Telegram 摘要已标注为业务运营语义，不列为通用研发缺失。

### 8.2 保留的争议点（已在前文修正）

以下争议点已在前文修正，保持记录以供追溯：

1. **规则缺失和 tooling 缺失不能直接归零** ✅ 已修正
   - 前版文档第七部分将”规则缺失”和”tooling 缺失”均写作”❌ 无”。
   - 经审计认定：此结论过满，不能排除少量规则缺口与 tooling 缺口。
   - 已修正为：规则缺失 ⚠️ 少量存在，tooling 缺失 ⚠️ 少量存在，编排/触发缺失 ✅ 主要缺失。

2. **Team 创建检查不只是编排问题** ✅ 已修正
   - 前版文档 3.1 将”Team 创建检查”仅判断为”规则存在，缺少自动编排”。
   - 经审计认定：`create-agent.md` 的 team-lead is Human 规则 ≠ hedge-ai Step 1.5 的 Team 存在性检查 + TeamCreate。
   - 已修正为：Team 创建检查 = 规则缺口 + tooling 缺口 + 编排缺失（三重叠加）。

3. **”已存在 toolings”不等于”start-agent-team 所需 tooling 已完整”** ✅ 已修正
   - 前版文档默认 tooling 缺失为零。
   - 经审计认定：部分脚本存在不能推出 tooling 完整，尤其是 Team 级 tooling 尚无证据。
   - 已体现在第七部分判断中。

### 8.3 最终判断

文档前七节与第八节 Codex Review 补充审计已对齐：
- 根因主体：`skills/shared/start-agent-team.md`
- GitHub Issue 入口：`scripts/github_issue_sync.py`
- 缺失定性：**主要为编排/触发缺失，但不能排除少量规则缺口与 tooling 缺口**
- 业务运营语义项已排除
- 口径已统一：结论与第七部分完全一致，无自我矛盾

### 8.4 本轮修复（2026-04-15）

**已完成的修复**：

1. **P0 启动流程编排已补齐**
   - 步骤 3.5.1：`python scripts/github_issue_sync.py` 同步 open issues
   - 步骤 3.5.2：读取 `.claude/task_queue/`
   - 步骤 3.5.3：读取 `docs/todo/TODO_REGISTRY.md`
   - 步骤 3.5.4：`python scripts/task_router.py --verbose` 路由任务
   - 步骤 3.5.5：汇总启动上下文
   - 注：030 原写作 `--sync-issues` 与实现不符，已修正为默认调用

2. **P1 Team 创建检查 — 规则与入口已补**
   - 步骤 0.5 已添加 Team 存在性检查规则和调用入口
   - TeamCreate 调用格式已标注为示意写法（平台相关）
   - 已补本仓库约定 fallback（`.claude/teams/{project_id}/config.json`）
   - 已补禁止重复创建规则
   - ⚠️ 等价性待验证：具体调用格式和 hedge-ai Step 1.5 等价性尚未被平台文档或仓库内证据证明

3. **issue-poll.yml 已新增**
   - 新建 `.github/workflows/issue-poll.yml`：cron 每 15 分钟触发
   - 本 workflow 产出 `.md` 文件（pending_*.md），与 `post-comment.yml` 监听的 `.json` 文件类型不一致，当前未与 post-comment.yml 集成，未设计为自动触发下游
   - git push 已移除（permissions 改为 contents: read，无需写权限）

**030 验收结论**：
- P0：✅ 完成
- P1-Team 创建检查：⚠️ 部分完成（规则入口已补，调用格式和等价性待平台验证）
- P1-issue -> Agent 触发编排：⚠️ 部分完成（poll workflow 已新增，当前未与 post-comment.yml 集成）
