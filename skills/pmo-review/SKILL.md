# PMO Review

## 目标

PMO 系统化地逐个解决 `docs/pmo/issues/` 下的 Open 问题：分析根因、与用户对齐方案、推动机制改进落地。

## 适用场景

- PMO 定期 Review（每周/每阶段）
- 多个 Open Issue 需要系统性解决
- 用户发起 PMO Review 请求

## 执行流程

### Step 1: 阅读核心规则（强制）

**PMO Review 必须先建立对标准流程的理解，才能判断问题是否合规。**

#### A. 阅读 `skills/` 目录

**必须全部读完：**
- [ ] `skills/skill-protocol.md` — 共享技能协议
- [ ] `skills/team-setup.md` — 团队启动协议
- [ ] `skills/event-bus.md` — 事件总线语义
- [ ] `skills/start-agent-team.md` — 团队启动 Skill
- [ ] `skills/agent-bootstrap.md` — Agent 激活协议
- [ ] `pmo/SKILL.md` — PMO 角色定义（必读）
- [ ] `team-lead/SKILL.md` — Team Lead 角色定义
- [ ] `product-manager/SKILL.md` — PM 角色定义
- [ ] `architect/SKILL.md` — Architect 角色定义
- [ ] `qa-engineer/SKILL.md` — QA Engineer 角色定义
- [ ] `engineer/SKILL.md` — Engineer 角色定义

#### B. 阅读核心流程文件

**必须全部读完：**
- [ ] `prompts/001_team_topology.md` — 团队拓扑
- [ ] `prompts/002_product_engineering_roles.md` — 角色职责
- [ ] `prompts/004_delivery_gates.md` — 交付 Gate 门控
- [ ] `prompts/017_human_review_and_signoff.md` — Human Review 规范
- [ ] `prompts/014_process_compliance_and_audit.md` — 流程合规与审计
- [ ] `prompts/007_issue_driven_orchestration.md` — Issue 驱动编排

#### 阅读完成标志

```
Step 1 阅读完成：
- skills/ 核心文件：已全部通读
- prompts/ 核心流程文件：已全部通读
- 已建立流程合规判断基准
```

---

### Step 2: 读取所有 Open 问题

**⚠️ 必须逐个分析每个 Open 问题，不能遗漏。**

读取 `docs/pmo/issues/` 下的所有 Open 问题文件（扁平结构）：

```
docs/pmo/issues/
├── README.md
├── 001_2026-04-15_role-boundary_team_lead_follow_up_boundary.md  (Open)
├── 002_2026-04-15_role-boundary_architect_assigned_code_task.md  (Closed)
├── 003_2026-04-15_role-boundary_minimal_role_sequence.md  (Closed)
├── 004_2026-04-15_process_parallel_issue_priority.md  (Open)
├── 005_2026-04-15_governance_file_organization_non_standard.md  (Closed)
├── 006_2026-04-15_governance_hr1_gate3_circular_dependency.md  (Open)
└── ...
```

对每个 Open 问题，分析：

| 分析维度 | 内容 |
|---------|------|
| **问题描述** | 简述核心问题 |
| **根因** | 直接原因 + 根因（机制/流程/规范缺陷） |
| **关联问题** | 是否与其他 Open 问题有共同根因 |
| **纠正动作现状** | 已有动作 vs. 待执行动作 |
| **优先级** | P0 > P1 > P2 |

---

### Step 3: 逐个发起讨论

**⚠️ 对每个 Open 问题，使用 `/plan-ceo-review` 与用户讨论该问题的解决方案。**

按优先级排序处理：

#### Issue 处理模式

对每个问题，汇报：

```
### {问题 ID}: {问题标题}

**问题简述**：{一句话描述}
**根因分析**：{根因是什么}
**当前状态**：{已有纠正动作}
**待定事项**：{需要用户对齐的问题}

**讨论议题**：
1. {具体问题 1}
2. {具体问题 2}
```

使用 `/plan-ceo-review` 发起讨论。

**用户对齐后**：
- 如果需要修改文件 → 记录到变更清单
- 如果只是确认 → 更新该 issue 状态为 Closed/Mitigated

#### PMO 状态机

| 状态 | 说明 | 退出条件 |
|------|------|---------|
| **Review 进行中** | PMO 正在分析问题、与用户对齐 | 用户对齐后进入下一状态 |
| **追踪中** | Resolution 已归档，GitHub Issue 已创建，等待执行 | 执行完成 + Human Review 通过 |
| **验收待确认** | 机制改进已合并，等待 Human 验收 | Human 确认验收后关闭 PMO Issue |

**PMO 退出规则**：Resolution 归档 + GitHub Issue 评论分配完动作后，PMO 立即退出追踪状态。后续由 Human（Team Lead）负责验收，PMO 收到通知后再确认关闭。

---

### Step 4: 创建 Resolution

讨论对齐后，为每个 Open 问题创建 Resolution 文件：

文件路径：`docs/pmo/resolutions/{ID}_{日期}_{简短描述}_resolution.md`

Resolution 包含：
- 问题回顾
- 根因分析
- 讨论对齐结论（修复方案）
- **GitHub Issue URL**（追踪修复进度）

### Step 5: 发起 GitHub Issue

**一个 PMO Issue = 一个 GitHub Issue。**

Resolution 创建后，发起 GitHub Issue 追踪修复：

1. 在 Resolution 中记录 GitHub Issue URL
2. GitHub Issue 作为项目级追踪，关联相关 PR
3. **在同一个 Issue 下评论分配所有动作，不创建多个 Issue**
4. 执行人在该 Issue 下回复认领，提交 PR（Refs #N），不自动关闭
5. Human Review 通过 PR 后，Human 验收，Issue 才关闭

**禁止**：为每个子动作创建独立的 GitHub Issue。

### Step 6: 跟踪与验收

- 跟踪 GitHub Issue 进度（通过 Issue 评论）
- GitHub Issue 关闭后，更新 Resolution 中的验收记录
- PMO issue 状态更新为 Closed

**GitHub Issue 操作规范**：必须使用 `python scripts/github_issue_sync.py`，禁止直接使用 `gh issue create/close` 等 raw gh 命令。详见 CLAUDE.md。

### Step 7: 更新索引

变更完成后，更新：
- `docs/pmo/issues/README.md`
- `docs/pmo/resolutions/README.md`

---

### Step 8: Commit + Push

```bash
git add docs/pmo/issues/ docs/pmo/resolutions/ {涉及的其他文件}
git commit -m "pmo: review 变更 - {本期解决的问题摘要}"
git push
```

**所有工作完成后，汇报本期 Review 结论摘要。**

---

## 关键输出

### Review 阶段输出

1. **问题分析表**：所有 Open 问题的根因、优先级、处理顺序
2. **逐问题讨论结论**：每个 Open 问题的对齐结论
3. **Resolution 文件**：每个 Open 问题对应的解决方案记录（含 GitHub Issue URL）

### 闭环阶段输出

1. **Resolution 文件更新**：GitHub Issue 关闭后更新验收记录
2. **PMO Issue 关闭**：状态变更为 Closed
3. **Git 提交**：包含所有变更的 commit

---

## 注意事项

- **Step 1 阅读是强制性的**，确保 PMO 有足够的上下文判断问题
- **必须逐个处理每个 Open 问题**，不能跳过
- **PMO 只负责发现、记录、升级和推动改进，不代替签字人关闭问题**
- **涉及规范变更必须先与用户对齐，才能执行**
- **按 P0 > P1 > P2 优先级处理问题**
