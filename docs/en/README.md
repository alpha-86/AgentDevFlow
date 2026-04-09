# AgentDevPipeline Overview

AgentDevPipeline is a self-contained product-engineering agent workflow package.

## Source-of-Truth Policy

- Chinese files in `docs/zh-cn/` and `prompts/zh-cn/` are the internal source of truth.
- English files in `docs/en/` and `prompts/en/` are release translations.
- Every workflow or prompt change must be made in Chinese first.

## Scope

Included:

- Product and engineering agent roles
- Stage-gated delivery workflow
- Document, memo, and todo conventions
- Platform adapters for Claude, Codex, and OpenCode

Excluded:

- Quant fund operating roles
- Trading-session schedules
- Research, backtest, and risk workflows tied to fund operations

## Self-Contained Rule

- All prompts, skills, workflows, and templates required by AgentDevPipeline must live in this repository.
- `hedge-ai` may be referenced only as historical migration context.
- No installation or runtime flow may depend on reading another repository.

## Supporting References

- [Localization Policy](/home/work/code/agentdevpipeline/docs/en/reference/localization-policy.md)
- [External Reuse Survey](/home/work/code/agentdevpipeline/docs/en/reference/reuse-survey.md)
