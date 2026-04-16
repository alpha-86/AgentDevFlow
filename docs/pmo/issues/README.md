# PMO Issues 问题记录

## 目录结构

```
docs/pmo/issues/
├── README.md
└── {全局序号}_{日期}_{类别}_{简短描述}.md
```

## 命名规范

- 文件命名：`{全局序号}_{日期}_{类别}_{简短描述}.md`
- 类别标签：`_role-boundary_`, `_process_`, `_governance_`
- ID 保留在文件内容中（如 RB-001）

## 问题索引

| 序号 | ID | 类别 | 问题 | 状态 |
|------|----|------|------|------|
| 001 | RB-001 | role-boundary | Team Lead 深度介入具体 Issue 跟踪 | Open |
| 002 | RB-002 | role-boundary | Architect 被分配代码实现任务 | Closed |
| 003 | RB-003 | role-boundary | 最小角色集未按 Gate 顺序启用 | Closed |
| 004 | PROC-001 | process | PM 自行决定并行 Issue 处理顺序 | Open |
| 005 | GOV-001 | governance | PMO 文档目录结构不规范 | **Closed** |
| 006 | GOV-002 | governance | Human Review #1 与 Gate 3 循环依赖 | Mitigated |
| 007 | GOV-003 | governance | Task Router 路由到未启用的角色 | Open |
| 008 | GOV-004 | governance | Issue #3 Human Review #1 被跳过 | **Open ⚠️ P0** |

## 记录规则

- 每个问题一个文件，全局顺序编号
- P0/P1 问题记录后，必须立即通知 Team Lead
- PMO 只负责发现、记录、升级和推动改进，不代替签字人关闭问题
- 问题关闭后，解决方案记录到 `../resolutions/`

## 闭环流程

```
发现问题 → 记录到 docs/pmo/issues/
→ 通知 Team Lead
→ /pmo-review 讨论 → 记录到 ../resolutions/
→ 发起 GitHub Issue 追踪修复
→ GitHub Issue 关闭 → 验收通过
→ 关闭 PMO issue
```
