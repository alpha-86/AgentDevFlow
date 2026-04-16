# PMO — Project Management Office

## 目录结构

```
docs/pmo/
├── README.md                    # 本文件
├── audit/                       # 定期审计报告（按年份）
│   └── 2026-04-15_audit.md
├── issues/                      # 问题记录
│   └── {全局序号}_{日期}_{类别}_{简短描述}.md
└── resolutions/                 # 解决方案闭环记录
    └── {ID}_{日期}_{简短描述}_resolution.md
```

## 问题分类

| 分类 | 说明 |
|------|------|
| role-boundary | 角色越权、职责错配问题 |
| process | 流程顺序、合规性违规问题 |
| governance | 治理机制、文件规范问题 |

## 闭环流程

```
PMO 发现问题 → 记录到 docs/pmo/issues/
→ 通知 Team Lead（P0/P1 立即）
→ /pmo-review 讨论 → 记录到 docs/pmo/resolutions/
→ 发起 GitHub Issue 追踪修复
→ 执行修复
→ GitHub Issue 关闭 → 验收通过
→ 关闭 PMO issue
```

## 命名规范

| 文件类型 | 格式 | 示例 |
|---------|------|------|
| Issue 文件 | `{全局序号}_{日期}_{类别}_{简短描述}.md` | `001_2026-04-15_role-boundary_team_lead_follow_up.md` |
| Resolution 文件 | `{ID}_{日期}_{简短描述}_resolution.md` | `RB-001_2026-04-15_team_lead_follow_up_resolution.md` |

**ID 对应**：Resolution 文件的 ID 与 Issue 文件的 ID 一致。

## PMO 职责

1. **发现**：识别流程问题、角色越权、治理缺陷
2. **记录**：写入 `docs/pmo/issues/`
3. **升级**：P0/P1 问题立即通知 Team Lead
4. **推动**：通过 `/pmo-review` 与用户对齐解决方案
5. **追踪**：记录 GitHub Issue URL 到 resolution
6. **闭环**：GitHub Issue 关闭后，关闭 PMO issue

**PMO 只负责发现、记录、升级和推动改进，不代替签字人关闭问题。**

## 当前状态

| 类别 | Open | Closed |
|------|------|--------|
| role-boundary | 1 | 2 |
| process | 1 | 0 |
| governance | 3 | 1 |
| **合计** | **5** | **3** |

详见：
- [问题索引](./issues/README.md)
- [解决方案索引](./resolutions/README.md)
