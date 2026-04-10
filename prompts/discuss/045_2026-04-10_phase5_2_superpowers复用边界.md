# 045 Phase 5.2 superpowers 复用边界

## 结论

`superpowers` 对当前仓库的价值，主要在“执行方法复用”，不在“核心规则承载”。

本轮复核后，将其分成三类：

### 一、适合直接复用的方法类能力

- `writing-plans`
- `dispatching-parallel-agents`
- `verification-before-completion`
- `using-git-worktrees`
- `executing-plans`

这些能力的共同点是：

- 不改写本仓库的角色、Gate、Issue、双阶段 PR 语义
- 只提升执行效率、隔离性和验证强度

### 二、只应参考、不应强绑定的能力

- `using-superpowers`
- `brainstorming`
- `test-driven-development`

这些能力可以借鉴，但不应成为插件成立前提。

### 三、当前结论

- `superpowers` 适合做“执行方法宿主”
- `agentdevpipeline` 必须继续做“流程规则宿主”
- 两者是互补关系，不是依赖替代关系

## 本轮落点

- 更新 `docs/reference/reuse-survey.md`
- 在执行计划中勾选 `5.2`

## 下一步

- `5.3` 继续梳理 `gstack` 中哪些能力适合写成可选依赖说明
