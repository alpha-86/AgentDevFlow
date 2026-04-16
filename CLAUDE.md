# AgentDevFlow CLAUDE.md

## ADF 命名空间的核心认知（本项目最关键的架构设计）

### adf- 前缀的真正含义

`adf-` 是 AgentDevFlow 的**开发版命名空间**，用于区分本项目自举用的开发版和外部用户安装的稳定版。

| 环境 | 路径 | 命名空间 | Skill 调用 |
|------|------|---------|-----------|
| 本项目 (`~/code/AgentDevFlow`) | `.claude/skills/adf-*/` | adf- 开发版 | `Skill("adf-product-manager")` |
| 外部用户 (`~/.claude/skills/`) | `skills/product-manager/` | 稳定版（无前缀） | `Skill("product-manager")` |

### 核心规则

1. **`skills/` 是唯一源文件**，所有 Skill 调用在源文件中**不带 adf- 前缀**
2. **bootstrap-sync** 在生成 `.claude/skills/adf-*/` 时，自动把 Skill 调用加上 adf- 前缀
3. **禁止在 `skills/` 源文件中写 adf- 前缀**（会导致双重前缀或外部用户无法使用）

### bootstrap-sync 替换规则

当 `skills/start-agent-team/SKILL.md` 包含 `Skill("product-manager")` 时：
- bootstrap-sync 生成 `.claude/skills/adf-start-agent-team/SKILL.md` 时自动替换为 `Skill("adf-product-manager")`

### 错误示例（我曾经犯过的错）

❌ **错误**：`skills/start-agent-team/SKILL.md` 里写 `Skill("adf-product-manager")`
- 原因：外部用户安装后没有 `adf-product-manager` 这个 skill，会导致调用失败

✅ **正确**：`skills/start-agent-team/SKILL.md` 里写 `Skill("product-manager")`
- bootstrap-sync 会自动在生成的目标文件中替换为 `Skill("adf-product-manager")`

### 判断依据

- `prompts/by-me/005_V1_如何在本项目中使用.md` — 明确说明 adf- 是命名空间隔离机制
- `prompts/discuss/024_2026-04-10_adf-prefix自举部署方案.md` — 说明 bootstrap-sync 的替换逻辑

---

## ADF Bootstrap Skill 架构：真实源 vs 重命名产物

### 核心概念：禁止直接修改 bootstrap 产物

`.claude/skills/adf-*/SKILL.md` 文件是 `bootstrap-sync` 脚本的**自动生成产物**，不是源文件。

- **真实源文件**在 `skills/` 下
- **bootstrap-sync** 做的是：路径替换（`skills/` → `.claude/skills/adf-*`）+ frontmatter 注入
- **禁止直接修改** `.claude/skills/adf-*/SKILL.md`，这些文件会被 bootstrap-sync 覆盖

### bootstrap-sync 自动同步机制

bootstrap-sync.yml 在 `skills/**/*.md` 变更时自动触发（push to main）。

**注意**：commit message 中多行 shell 字符串引号可能导致 YAML 解析失败（`[skip ci]"` 结尾问题），需保持 commit message 简洁。

| 真实源 (`skills/`) | bootstrap 产物 (`.claude/skills/`) |
|---------------------------|-------------------------------------|
| `start-agent-team.md` | `adf-start-agent-team/SKILL.md` |
| `team-setup.md` | `adf-team-setup/SKILL.md` |
| `agent-bootstrap.md` | `adf-agent-bootstrap/SKILL.md` |

### 当前差异

bootstrap-sync 修复后，产物与源文件的差异仅为 frontmatter 注入和路径重写（预期行为），无内容滞后。

### 判断依据

详见：`prompts/discuss/030_2026-04-14_start-agent-team能力对比与缺失分析.md`
迭代 Review：`prompts/discuss/033_2026-04-15_031迭代review_start-agent-team实现补齐.md`

### 工作流原则

1. **只修改源 skill**：`skills/*.md` 是唯一的真实来源，禁止直接修改 `.claude/skills/adf-*/SKILL.md`
2. **验证后才发布**：PR 合并前 diff 对照表中的对应文件对，确保产物与源一致

### GitHub Issue 操作规范

**禁止直接使用 `gh issue create`、`gh issue close` 等 raw gh 命令操作 GitHub Issue。**

所有 GitHub Issue 操作必须通过统一封装脚本：

```bash
# 创建 Issue
python scripts/github_issue_sync.py --create-issue --title "..." --body "..." --labels "..."

# 关闭 Issue
python scripts/github_issue_sync.py --close-issue --issue N --reason completed --close-comment "..."

# 评论 Issue（通过 GitHub Actions）
python scripts/github_issue_sync.py --post-comment --issue N --body "..." --agent "..."

# 同步 Issues 到 TaskQueue
python scripts/github_issue_sync.py
```

**原因**：`github_issue_sync.py` 提供标准化封装，包含：断点续传、命名格式校验、TaskQueue 写入、GitHub Actions 集成、processed_issues 记录。直接用 gh 命令会绕过这些保障。

### PR 关联 Issue 规范

**PMO / 治理类 Issue 必须使用 `Refs #N`，禁止使用 `Fixes #N` 或 `Closes #N`。**

- `Fixes #N` / `Closes #N`：PR 合并后**自动关闭** Issue
- `Refs #N`：仅关联，不自动关闭

**原因**：PMO Issue 需要验收确认后才关闭，不能依赖 PR 合并自动关闭。验收人是 Human，不是机器。

**PR 标题格式**：
```
<type>: <short description> (Refs #N)
```

示例：`pmo: GOV-004 HR#1 强制不可跳过 (Refs #8)`

### 相关文件位置

- bootstrap-sync 脚本：`.github/workflows/bootstrap-sync.py`
- 源 skill：`skills/`
- bootstrap 产物：`.claude/skills/adf-*/SKILL.md`
- issue-poll workflow：`.github/workflows/issue-poll.yml`
- task_router 脚本：`scripts/task_router.py`
- github_issue_sync 脚本：`scripts/github_issue_sync.py`
- task_update 脚本：`scripts/task_update.py`
