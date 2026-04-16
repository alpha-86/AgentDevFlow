# 交付 Gate

## README 流程节点 vs Gate 编号映射表

| README 流程节点 | Gate 编号 | 说明 |
|---------------|-----------|------|
| 创建主 GitHub Issue | Gate 0 | Team Startup |
| PRD | Gate 1 | PRD Review |
| Tech Spec + QA Case | Gate 2 | Tech Review |
| Human Review #1 + 文档PR合并 | - | HR#1 通过后 Human 合并 |
| Engineer 实现 | Gate 3 | Implementation |
| QA 验证 | Gate 4 | QA Validation |
| Human Review #2 + 代码PR合并 | - | HR#2 通过后 Human 合并 |
| Release / Issue Close | Gate 5 | Release |

> 详细流程定义见 `prompts/002_develop_pipeline.md`。

## Gate 1: PRD Review

- 输入：明确需求
- 输出：通过评审的 PRD
- 参与：PM、架构师、必要的业务评审人
- 签字：PM（必签）、架构师（必签）
- 检查点：
  - 范围是否清晰
  - 非范围是否清晰
  - 验收标准是否可测
  - 风险和依赖是否识别
- 未通过处理：退回 PM 修订

## Gate 2: Tech Review

- 输入：通过的 PRD
- 输出：通过评审的 Tech Spec
- 参与：架构师、PM、QA
- 签字：架构师（必签）、QA（必签）、PM（确认）
- 检查点：
  - 是否完整覆盖 PRD
  - 是否可实现
  - 是否可测试
  - 是否说明风险、监控、回滚点
- 未通过处理：退回 架构师 修订

## Gate 3: QA Case Design

- 输入：通过 Tech Review 的 Tech Spec
- 输出：通过三方签字的 QA Case Design 文档
- 参与：PM、架构师/QA、Engineer
- 签字：PM（必签）、架构师（必签）、Engineer（必签）
- 检查点：
  - Case 覆盖关键验收项
  - Case 覆盖边界条件
  - Case 覆盖异常路径
- 未通过处理：退回修订

## QA Case Design 独立文档要求

- **QA Case Design 必须是有独立文件的文档**（`docs/qa/QA-{issue}-v{n}.md`）
- **不得以内嵌形式存在于 Tech Spec 中**（Tech Spec 中的 TC 仅为设计说明，不能替代正式 QA Case Design 文档）
- 纯文档交付场景下，Engineer 角色由架构师代理签字（需在文档中注明原因）

## Gate 4: Implementation

- 输入：通过的 Tech Spec
- 输出：代码、单测、变更说明
- 参与：Engineer
- 签字：Engineer（必签）、架构师（技术一致性确认）
- 检查点：
  - 实现是否符合 Tech
  - 单测是否覆盖关键路径
  - 文档和配置是否同步
- 未通过处理：补实现或补证据

## Gate 5: QA Validation

- 输入：实现结果
- 输出：QA 报告、阻塞问题、验收意见
- 参与：QA、Engineer、PM
- 签字：QA（必签）、PM（验收口径确认）、Engineer（必签）
- 检查点：
  - Case 是否覆盖关键验收项
  - 是否有阻塞缺陷
  - 结果是否有证据
  - 残留风险是否明确
- 未通过处理：回到 Implementation 或 Tech Review

## Gate 6: Release

- 输入：通过验证的交付物
- 输出：上线决定、发布记录、回滚信息
- 参与：PM、架构师、Platform/SRE
- 签字：PM（业务放行）、架构师（技术放行）、Platform/SRE（发布放行）
- 检查点：
  - 发布内容是否明确
  - 回滚方案是否存在
  - 监控和值守是否明确
  - 已知风险是否被接受
- 未通过处理：阻止发布

## Gate 之间的流转原则

- 任一 Gate 不通过，禁止直接跳到后续 Gate
- 如果上游文档发生大变更，后续 Gate 必须重新评审
- Team Lead 负责监督 Gate 不被绕过
- 任一必签角色缺失，当前 Gate 视为未完成

## 强制顺序（不可跳过）

```
Gate 1 (PRD) → Gate 2 (Tech) → Human Review #1（强制）→ Gate 3 → Gate 4 (Implementation) → Gate 5 → Gate 6
```

**Human Review #1 是 Gate 2 之后的强制环节，不可跳过。** HR#1 评审 PRD + Tech Spec + Case 设计文档，与交付方式无关。

## Gate 退回与重进规则

- `Rejected`：必须回到当前 Gate 输入文档修订后再提交
- `Conditional`：必须先完成条件项并补证据，才可进入下游 Gate
- `Blocked`：必须升级到 Team Lead 协调并给出解除阻塞动作

## Gate 流程保障机制 (V2.3)

### Gate 定义

| Gate | 文档类型 | 必需签字 | 检查位置 |
|------|---------|----------|----------|
| **PRD Gate 1** | PRD | PM + 架构评审人 | PRD 文档头部 Gate 块 |
| **Tech Gate 2** | Tech | PM + 技术评审人 + QA | Tech 文档头部 Gate 块 |
| **QA Case Design Gate 3** | QA Case | PM + 架构师 + Engineer (三方签字) | QA Case 文档头部 Gate 块 |
| **Implementation Gate 4** | 代码/单测 | Engineer + 架构师 | 代码 PR 或交付记录 |
| **QA Test Report Gate 5** | QA Test Report | QA + PM + Engineer (三方签字验收) | QA Test Report 文档头部 Gate 块 |
| **Release Gate 6** | 发布记录 | PM + 架构师 + Platform/SRE | 发布文档头部 Gate 块 |

### CI Gate 检查流程

```
文档 PR 创建
     │
     ▼
doc-pr-checks.yml 执行
     │
     ├── 检查 PRD Gate 1 (PM + 架构评审人)
     ├── 检查 Tech Gate 2 (PM + 技术评审人 + QA)
     └── 检查 QA Case Design Gate 3 (PM + 架构师 + Engineer)
          │
          ├── 全部通过 → 允许提交
          └── 任一失败 → 显示友好错误，阻止提交
```

### 友好错误信息示例

```
[Gate Check] 前置条件未满足

问题: 文档 PR 提交时，关联的 Tech Gate 2 尚未全部签字

要求:
  □ PM 签字: 未通过
  □ 技术评审人签字: 已通过
  □ QA 签字: 未通过

解决方案:
  1. 完成所有 Gate 签字后再提交 PR
  2. 参考: prompts/004_delivery_gates.md
  3. 参考: skills/shared/workflows/tech-review.md
```

### 三层保障体系

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

### Agent Critical Rules 强化 (V2.3)

**QA Agent Critical Rules 新增**:
- QA-15: Gate 保障强制配合 - QA 在 Tech Review 中必须完成 Gate 签字，未签字的 Tech 不得进入开发
- QA-16: Gate 签字记录必须准确 - QA 签字前必须验证 Tech 文档质量，签字后承担相应责任
- QA-17: 三方签字 Gate 强制执行 - QA Case Design 的三方签字必须在文档 PR 提交前完成

**Engineer Agent Critical Rules 新增**:
- ENG-12: Gate 签字前置条件 - 开发前必须确认相关 Gate 文档已满足所有签字要求
- ENG-13: Gate 保障不满足时的正确处理 - 拒绝开发，指出缺失的 Gate 签字，提供解决方案
- ENG-14: 开发前 CI/hook 检查配合 - pre-commit hook 会自动检查 Gate 签字状态
