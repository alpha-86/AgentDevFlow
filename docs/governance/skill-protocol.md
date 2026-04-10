# Shared Skill 使用协议

## 目标

统一 `skills/shared/` 中角色、workflow、template 的使用方式，避免平台适配时各自发散。

## 基本原则

- 角色文件定义“职责边界与强规则”。
- playbook 定义“执行顺序与常见失误”。
- workflow 定义“阶段流程、输入、输出、准入准出”。
- template 定义“留痕格式与最小字段”。

## 使用顺序

1. 先读取角色文件
2. 再读取对应 playbook
3. 再读取当前阶段 workflow
4. 最后选择对应 template 生成或更新交付物

## 强制要求

- 任何关键动作都必须能回链到 Issue、Gate 和文档。
- 若角色文件与 workflow 冲突，以 workflow 和 Gate 规则为准。
- 若 template 字段缺失，不得直接省略，必须显式标注 `N/A` 或补齐输入。

## 平台适配要求

- Claude / Codex / OpenCode 只能包装入口，不得篡改共享协议含义。
- 平台层新增能力时，必须保持 `skills/shared/` 语义不变。

## 违规信号

- 只使用角色 prompt，不读取 workflow
- 只做执行，不更新 template 与留痕
- 平台层私自改写 Gate 或签字规则
