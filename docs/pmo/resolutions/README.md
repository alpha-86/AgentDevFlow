# PMO Resolutions 问题解决方案闭环记录

## 目录结构

```
docs/pmo/
├── issues/                     # 问题记录
│   └── {全局序号}_{日期}_{类别}_{简短描述}.md
└── resolutions/                # 解决方案闭环记录
    ├── README.md              # 本文件
    └── {ID}_{日期}_{简短描述}_resolution.md
```

## 命名规范

| 文件类型 | 格式 | 示例 |
|---------|------|------|
| Issue 文件 | `{全局序号}_{日期}_{类别}_{简短描述}.md` | `001_2026-04-15_role-boundary_team_lead_follow_up.md` |
| Resolution 文件 | `{ID}_{日期}_{简短描述}_resolution.md` | `RB-001_2026-04-15_team_lead_follow_up_resolution.md` |

**ID 对应**：Resolution 文件的 ID 与 Issue 文件的 ID 一致。

## 闭环流程

```
PMO 发现问题 → 记录到 docs/pmo/issues/
→ 通知 Team Lead
→ /pmo-review 讨论
→ 记录到 docs/pmo/resolutions/（记录 GitHub Issue URL）
→ 执行修复（通过 GitHub Issue 追踪）
→ GitHub Issue 关闭 → 验收通过
→ 关闭 PMO issue
```

## Resolution 文件结构

```markdown
# {ID} {问题标题}

## 基本信息

| 字段 | 内容 |
|------|------|
| Issue 文件 | `../issues/{filename}.md` |
| GitHub Issue | {URL} |
| 讨论日期 | {YYYY-MM-DD} |
| 验收日期 | {待填} |
| 状态 | ⏳ 待执行 → ✅ 已验收 → Closed |

---

## 一、问题回顾

{简述核心问题}

## 二、根因分析

{深入分析根因}

## 三、讨论对齐结论

### 修复方案

| 动作 | 涉及文件 | 验收标准 | 负责人 |
|------|---------|---------|--------|
| ... | ... | ... | ... |

---

## 四、GitHub Issue 追踪

| 字段 | 内容 |
|------|------|
| GitHub Issue URL | {URL} |
| 责任人 | {GitHub Issue Assignee} |
| 关联 PR | {PR URL} |

---

## 五、验收结论

| 字段 | 内容 |
|------|------|
| 最终验收人 | Team Lead |
| 验收日期 | {YYYY-MM-DD} |
| GitHub Issue 状态 | ✅ Closed |
| PMO Issue 状态 | ✅ Closed |

---

*由 pmo-review Skill 生成 | {YYYY-MM-DD}*
```

## 解决方案索引

| ID | 问题标题 | GitHub Issue | Resolution 文件 | PMO Issue 状态 |
|----|---------|-------------|----------------|----------------|
| RB-001 | Team Lead 深度介入具体 Issue 跟踪 | — | `RB-001_..._resolution.md` | Open |
| RB-002 | Architect 被分配代码实现任务 | — | `RB-002_..._resolution.md` | Closed |
| GOV-004 | Issue #3 Human Review #1 被跳过 | https://github.com/alpha-86/AgentDevFlow/issues/8 | `GOV-004_2026-04-16_issue3_hr1_skipped_resolution.md` | Open |
| GOV-011 | 变更追溯规则缺失 + Gate 流程并行化违规 | https://github.com/alpha-86/AgentDevFlow/issues/20 | `GOV-011_2026-04-20_change_propagation_gate_violation_resolution.md` | Open |
