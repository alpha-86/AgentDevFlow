# Shared Skills 目录

`skills/shared/` 是 AgentDevPipeline 的平台无关执行资产层。

## 结构

- `team-setup.md`
  团队启动与 kickoff 共享入口。

- `skill-protocol.md`
  共享执行顺序、状态语义和恢复顺序。

- `agents/`
  角色定义与 playbook。每个角色至少由一个 `*.md` 主规范和一个 `*.playbook.md` 执行手册组成。

- `workflows/`
  阶段流程、准入准出条件、签字与回退规则。

- `templates/`
  正式留痕模板与交付物结构。

## 最近补充的关键资产

- `workflows/human-review.md`
- `workflows/issue-routing.md`
- `workflows/project-portfolio-review.md`
- `templates/artifact-linkage-template.md`
- `templates/project-portfolio-template.md`
- `templates/project-kickoff-checklist-template.md`
- `agents/process-auditor.md`
- `team-setup.md`
- `skill-protocol.md`
- `templates/agent-activation-template.md`
- `templates/audit-report-template.md`

## 使用原则

- 平台适配层只能包装入口，不得改写这里的核心语义。
- 角色、workflow、template 必须与中文主版本规则保持一致。
- 角色文件必须明确：必读文档、初始化动作、上下文恢复、Issue/Gate 责任、禁止行为、输出格式。
- 主持会议或执行评审前，必须先读取对应 workflow。
