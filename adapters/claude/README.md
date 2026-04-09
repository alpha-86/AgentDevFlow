# Claude Adapter

这个适配层负责把 AgentDevPipeline 包装成 Claude 可使用的本地 skill pack。

## 最小要求

- 不改写 `skills/shared/` 的核心语义
- 支持读取中文主版本规则
- 至少具备 issue / gate / artifact linkage 的最小检查能力

## 接入清单

1. 读取 `README.md`、`docs/zh-cn/README.md` 和 `skills/shared/README.md`
2. 确认共享角色、workflow、template 可被 Claude 入口读取
3. 对照 `docs/zh-cn/governance/platform-minimum-checks.md` 实现最小检查
4. 至少落一份 `skills/shared/templates/platform-checklist-template.md`
5. 明确检查失败时如何阻断当前阶段

## 最小输出物

- 一份平台最小检查清单
- 一份平台检查结果
- 一份接入说明
- 一份失败处理说明

## 接入完成判定

- 能读取中文主版本规则
- 不改写共享语义
- 能做最小 Gate / Issue / Artifact / 状态一致性检查
- 检查失败时能阻断并给出修复路径

参考：

- `docs/zh-cn/governance/platform-minimum-checks.md`
- `skills/shared/templates/platform-checklist-template.md`
- `skills/shared/templates/platform-check-result-template.md`
- `adapters/claude/platform-check-example.md`
