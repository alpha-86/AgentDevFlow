# AgentDevFlow CLAUDE.md

## ADF Bootstrap Skill 架构：真实源 vs 重命名产物

### 核心概念：禁止直接修改 bootstrap 产物

`.claude/skills/adf-*/SKILL.md` 文件是 `bootstrap-sync` 脚本的**自动生成产物**，不是源文件。

- **真实源文件**在 `skills/shared/` 下
- **bootstrap-sync** 做的是：路径替换（`skills/shared/` → `.claude/skills/adf-*`）+ frontmatter 注入
- **禁止直接修改** `.claude/skills/adf-*/SKILL.md`，这些文件会被 bootstrap-sync 覆盖

### bootstrap-sync 自动同步机制

bootstrap-sync.yml 在 `skills/shared/**/*.md` 变更时自动触发（push to main）。

**注意**：commit message 中多行 shell 字符串引号可能导致 YAML 解析失败（`[skip ci]"` 结尾问题），需保持 commit message 简洁。

| 真实源 (`skills/shared/`) | bootstrap 产物 (`.claude/skills/`) |
|---------------------------|-------------------------------------|
| `start-agent-team.md` | `adf-start-agent-team/SKILL.md` |
| `team-setup.md` | `adf-team-setup/SKILL.md` |
| `create-agent.md` | `adf-create-agent/SKILL.md` |
| `agent-bootstrap.md` | `adf-agent-bootstrap/SKILL.md` |

### 当前差异

bootstrap-sync 修复后，产物与源文件的差异仅为 frontmatter 注入和路径重写（预期行为），无内容滞后。

### 判断依据

详见：`prompts/discuss/030_2026-04-14_start-agent-team能力对比与缺失分析.md`
迭代 Review：`prompts/discuss/033_2026-04-15_031迭代review_start-agent-team实现补齐.md`

### 工作流原则

1. **只修改源 skill**：`skills/shared/*.md` 是唯一的真实来源，禁止直接修改 `.claude/skills/adf-*/SKILL.md`
2. **验证后才发布**：PR 合并前 diff 对照表中的对应文件对，确保产物与源一致

### 相关文件位置

- bootstrap-sync 脚本：`.github/workflows/bootstrap-sync.py`
- 源 skill：`skills/shared/`
- bootstrap 产物：`.claude/skills/adf-*/SKILL.md`
- issue-poll workflow：`.github/workflows/issue-poll.yml`
- task_router 脚本：`scripts/task_router.py`
- github_issue_sync 脚本：`scripts/github_issue_sync.py`
