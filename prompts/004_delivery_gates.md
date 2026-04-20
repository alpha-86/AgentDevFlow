# 交付 Gate CI 检查逻辑（参考附录）

> **本文档已废弃 Gate 定义。Gate 定义以 `prompts/002_develop_pipeline.md` 为唯一源。**
>
> 本文件仅保留 CI 检查相关逻辑，供 CI/CD pipeline 参考。

## README 流程节点 vs Gate 编号映射表

| README 流程节点 | Gate 编号 | 说明 |
|---------------|-----------|------|
| Agent Team 启动 → 扫描 Issue | Gate 0 | Team Startup |
| PM 领取 Issue + 讨论 Comment | - | Issue 是强制入口，未 Comment 视为未完成 |
| PRD Review | Gate 1 | PRD Review（PM + Architect + QA 三方签字）|
| Tech Review | Gate 2 | Tech Review（QA + Engineer + PM 三签）|
| QA Case Design | - | QA Case Design（PM + Architect + Engineer 三签）|
| 文档 PR 合并（doc-{issue} 分支）| Human Review #1 | HR#1 通过后 Human 合并 = 设计确认 |
| Engineer 实现（feature-{issue} 分支）| Gate 3 | Implementation |
| QA 验证 | Gate 4 | QA Validation |
| 代码 PR 合并（feature-{issue} 分支）| Human Review #2 | HR#2 通过后 Human 合并 = 实现确认 |
| Release / Issue Close | Gate 5 | Release |

---

## Gate 签字矩阵（CI 检查参考）

> 以下签字矩阵与 `prompts/002_develop_pipeline.md` 保持一致，CI 检查基于此矩阵验证。

| Gate | 文档类型 | 必需签字 | CI 检查位置 |
|------|---------|----------|------------|
| Gate 1 | PRD | PM + Architect + QA | PRD 文档头部 Gate 块 |
| Gate 2 | Tech Spec | QA + Engineer + PM | Tech 文档头部 Gate 块 |
| QA Case Design | QA Case | PM + Architect + Engineer | QA Case 文档头部 Gate 块 |
| Gate 3 | Implementation | 代码 + 单测 | 代码 PR |
| Gate 4 | QA Test Report | QA + PM + Engineer | QA Test Report 文档头部 |
| Gate 5 | Release | PM + Architect + Platform/SRE | Release 文档头部 |

---

## CI Gate 检查流程

```
文档 PR 创建
     │
     ▼
doc-pr-checks.yml 执行
     │
     ├── 检查 PRD Gate 1 (PM + Architect + QA)
     ├── 检查 Tech Gate 2 (QA + Engineer + PM)
     └── 检查 QA Case Design (PM + Architect + Engineer)
          │
          ├── 全部通过 → 允许提交
          └── 任一失败 → 显示友好错误，阻止提交
```

### 友好错误信息示例

```
[Gate Check] 前置条件未满足

问题: 文档 PR 提交时，关联的 Gate 尚未全部签字

要求:
  □ Gate 1 PRD (PM + Architect + QA): 未通过
  □ Gate 2 Tech (QA + Engineer + PM): 未通过
  □ QA Case Design (PM + Architect + Engineer): 未通过

解决方案:
  1. 完成所有 Gate 签字后再提交 PR
  2. 参考: prompts/002_develop_pipeline.md
```

---

## 三层保障体系

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         三层保障体系                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  【第一层：GitHub 原生能力】                                                │
│  ├── Branch Protection Rules → 强制 PR 才能合并到 main                      │
│  ├── PR Template → 强制信息完整                                             │
│  └── Merge Gate → 条件满足才能合并                                         │
│                                                                             │
│  【第二层：CI/CD 自动检查】                                                 │
│  ├── doc-pr-checks.yml → 文档 PR 完整性检查 + Gate 状态检查                │
│  ├── code-pr-checks.yml → 代码 PR 前置条件检查                            │
│  └── issue-status-sync.yml → Issue 状态同步检查                            │
│                                                                             │
│  【第三层：Agent Critical Rules】                                            │
│  ├── PM: 禁止跳过文档 PR 指派开发                                          │
│  ├── Engineer: 开发前必须确认文档 PR 已合并                                 │
│  └── QA: Case Design 必须前置到文档 PR                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Agent Critical Rules（V2.3 参考）

**QA Agent Critical Rules**:
- QA-15: Gate 保障强制配合 - QA 在 Tech Review 中必须完成 Gate 签字，未签字的 Tech 不得进入开发
- QA-16: Gate 签字记录必须准确 - QA 签字前必须验证 Tech 文档质量，签字后承担相应责任
- QA-17: 三方签字 Gate 强制执行 - QA Case Design 的三方签字必须在文档 PR 提交前完成

**Engineer Agent Critical Rules**:
- ENG-12: Gate 签字前置条件 - 开发前必须确认相关 Gate 文档已满足所有签字要求
- ENG-13: Gate 保障不满足时的正确处理 - 拒绝开发，指出缺失的 Gate 签字，提供解决方案
- ENG-14: 开发前 CI/hook 检查配合 - pre-commit hook 会自动检查 Gate 签字状态

---

## Gate 退回与重进规则

- `Rejected`：必须回到当前 Gate 输入文档修订后再提交
- `Conditional`：必须先完成条件项并补证据，才可进入下游 Gate
- `Blocked`：必须升级到 Team Lead 协调并给出解除阻塞动作

---

*GOV-009 执行产物 | Gate 定义已统一至 `prompts/002_develop_pipeline.md` | 2026-04-20 更新 v2.0 流程修复：Gate 2 细分为 Tech Review 和 QA Case Design，双 PR 分支策略，PM 领取 Issue + 讨论 Comment 规则*
