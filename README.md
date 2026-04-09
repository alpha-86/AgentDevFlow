# AgentDevPipeline

AgentDevPipeline is a self-contained product-engineering agent workflow package for Claude, Codex, and OpenCode.

## Documentation Policy

- Chinese docs under `docs/zh-cn/` and `prompts/zh-cn/` are the source of truth for all iterations.
- English docs under `docs/en/` and `prompts/en/` are release translations for external publication.
- Every functional change must land in Chinese first, then be translated to English in the same release.

## What This Repository Contains

- All prompts, skills, workflows, templates, and platform adapters required by this package
- Neutral agent roles for product and engineering delivery
- Stage-gated workflows for PRD, tech review, implementation, QA, and release
- Shared templates for PRD, tech spec, QA case, memo, and todo tracking
- Platform adapters for Claude, Codex, and OpenCode
- Dependency guidance, including reusable external skill/plugin packages
- A Chinese-first internal authoring model with an English release mirror

## Self-Contained Rule

- This repository must not require `hedge-ai` at runtime, install time, or review time.
- Historical migration notes may mention `hedge-ai` only as archival context.
- All future migrated product-engineering assets must be copied and maintained inside this repository.

## What Was Intentionally Removed

- Fund-manager operating roles
- CSO/CRO/FM and quant strategy governance
- Market-session schedules tied to A-share trading
- Backtest and investment-decision workflows

## Quick Start

1. Read [中文总览](/home/work/code/agentdevpipeline/docs/zh-cn/README.md).
2. Read [架构与迁移说明](/home/work/code/agentdevpipeline/docs/zh-cn/architecture/repository-map.md).
3. Pick a platform guide:
   - [Claude](/home/work/code/agentdevpipeline/docs/zh-cn/platforms/claude-code.md)
   - [Codex](/home/work/code/agentdevpipeline/docs/zh-cn/platforms/codex.md)
   - [OpenCode](/home/work/code/agentdevpipeline/docs/zh-cn/platforms/opencode.md)
4. Use the shared role and workflow assets under `skills/shared/`.

## Shared Workflow Pack

- `skills/shared/workflows/prd-review.md`
- `skills/shared/workflows/tech-review.md`
- `skills/shared/workflows/implementation.md`
- `skills/shared/workflows/qa-validation.md`
- `skills/shared/workflows/release-review.md`
- `skills/shared/workflows/daily-sync.md`
- `skills/shared/workflows/todo-review.md`

## Structure

```text
AgentDevPipeline/
├── adapters/           # Platform-specific entrypoints
├── docs/prd|tech|qa... # Ready-to-use delivery artifact directories
├── docs/               # Chinese source docs + English release docs
├── plugins/            # Codex plugin package
├── prompts/            # Chinese source prompts + English release prompts
└── skills/shared/      # Platform-neutral agent/workflow/templates
```

## Current Version

- Internal source version: `0.2.0`
- Public release version: `0.2.0`
