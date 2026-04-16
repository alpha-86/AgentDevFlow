# 待办评审工作流

## 目标

跟踪 action item 从创建到关闭的完整生命周期。

## 规则

- 每次 评审 或讨论都必须产生可跟踪 action
- 每个 todo 都必须有 issue id、gate、负责人、priority、到期日 和 state
- 阻塞 项必须包含升级路径
- 已关闭项必须包含证据

## 状态模型

- open
- in_progress
- 阻塞
- done
- canceled

## 必需关闭证据

- 已合并改动链接或文档更新链接
- 验证记录链接（测试报告、评审 纪要 或 release record）

## 升级规则

- 若 item 被阻塞超过一个工作日，必须在日会中升级并指定升级 负责人

## 每轮 review 最小输出

- 更新后的 todo 状态
- 新增或补齐的关闭证据
- 被升级项及其负责人
- 需回写 issue 的关键结论
