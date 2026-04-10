# 交付 Gate

## Gate 1: PRD Review

- 输入：明确需求
- 输出：通过评审的 PRD
- 参与：PM、Tech Lead、必要的业务评审人
- 签字：PM（必签）、Tech Lead（必签）
- 检查点：
  - 范围是否清晰
  - 非范围是否清晰
  - 验收标准是否可测
  - 风险和依赖是否识别
- 未通过处理：退回 PM 修订

## Gate 2: Tech Review

- 输入：通过的 PRD
- 输出：通过评审的 Tech Spec
- 参与：Tech Lead、PM、QA
- 签字：Tech Lead（必签）、QA（必签）、PM（确认）
- 检查点：
  - 是否完整覆盖 PRD
  - 是否可实现
  - 是否可测试
  - 是否说明风险、监控、回滚点
- 未通过处理：退回 Tech Lead 修订

## Gate 3: Implementation

- 输入：通过的 Tech Spec
- 输出：代码、单测、变更说明
- 参与：Engineer
- 签字：Engineer（必签）、Tech Lead（实现一致性确认）
- 检查点：
  - 实现是否符合 Tech
  - 单测是否覆盖关键路径
  - 文档和配置是否同步
- 未通过处理：补实现或补证据

## Gate 4: QA Validation

- 输入：实现结果
- 输出：QA 报告、阻塞问题、验收意见
- 参与：QA、Engineer、PM
- 签字：QA（必签）、PM（验收口径确认）
- 检查点：
  - Case 是否覆盖关键验收项
  - 是否有阻塞缺陷
  - 结果是否有证据
  - 残留风险是否明确
- 未通过处理：回到 Implementation 或 Tech Review

## Gate 5: Release

- 输入：通过验证的交付物
- 输出：上线决定、发布记录、回滚信息
- 参与：PM、Tech Lead、Platform/SRE
- 签字：PM（业务放行）、Tech Lead（技术放行）、Platform/SRE（发布放行）
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

## Gate 退回与重进规则

- `Rejected`：必须回到当前 Gate 输入文档修订后再提交
- `Conditional`：必须先完成条件项并补证据，才可进入下游 Gate
- `Blocked`：必须升级到 Team Lead 协调并给出解除阻塞动作
