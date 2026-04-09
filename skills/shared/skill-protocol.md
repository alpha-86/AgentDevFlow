# Shared Skill Protocol

## 目标

统一 `skills/shared/` 中角色、playbook、workflow、template 的调用顺序和状态语义，避免不同平台各自发散。

## 基本原则

1. 角色文件定义职责边界与强规则。
2. playbook 定义执行顺序与常见失误。
3. workflow 定义阶段输入、输出、准入、准出和回退。
4. template 定义正式留痕的最小字段。
5. event bus 定义共享事件、触发条件、阻断条件和失败升级路径。

## 标准使用顺序

1. 读取角色主规范。
2. 读取角色 playbook。
3. 读取 `event-bus.md` 中与当前阶段相关的事件语义。
4. 读取当前阶段 workflow。
5. 选择并填写对应 template。
6. 把结论回链到 issue、gate 和正式文档。

## 状态语义

### 执行状态

- `pending`
- `in_progress`
- `blocked`
- `completed`

### 审核状态

- `approved`
- `conditional`
- `rejected`

### 审计状态

- `pass`
- `warning`
- `fail`

## 结构化输出最小字段

- `project_id`
- 当前对象
- 当前阶段
- 当前结论
- 证据链接
- 待办动作
- owner
- 是否允许进入下游阶段

## 共享事件要求

- 任何阶段切换都必须对应一个显式事件，而不是只修改文档内容。
- 任何 Gate 阻断都必须记录为失败事件或阻断事件。
- 任何 Human Review 结论都必须记录为可追踪事件。
- 任何平台检查失败都必须能回链到 issue 和证据文件。

## 失败与恢复

### 失败信号

- 只读取角色文件，不读取 workflow
- 执行后不更新正式留痕
- issue、gate、文档状态不一致
- Human Review 未完成却继续推进

### 恢复顺序

1. 读取主 issue
2. 读取最近一次 Gate 结论
3. 读取最近一次 memo / comment / change record
4. 读取 todo registry
5. 再继续当前阶段动作

## 平台适配要求

- Claude / Codex / OpenCode 只能包装入口，不得改写共享语义。
- 平台层若引入自动化检查，必须保持与共享状态语义一致。
- 平台层若无法实现某个自动化能力，必须明确说明缺口，而不是悄悄降级流程。
- 平台层应优先实现 `issue`、`comment`、`gate`、`platform_check` 四类事件观察能力。
