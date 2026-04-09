# AgentDevPipeline

English | [中文](./README_CN.md)

AgentDevPipeline is a self-contained product-engineering agent workflow package for Claude, Codex, and OpenCode.

## Overview

AgentDevPipeline provides:

- product and engineering agent roles
- stage-gated workflows for PRD, tech review, implementation, QA, and release
- reusable templates for PRD, tech spec, QA case, memo, and todo tracking
- platform adapters for Claude, Codex, and OpenCode
- a Chinese-first internal authoring model with an English release mirror

## Core Principles

- Build an end-to-end automated multi-agent delivery workflow.
- Keep the process controllable through explicit stages, gates, owners, and review records.
- Make every critical delivery step traceable through prompts, workflows, templates, memos, and todo tracking.
- Keep the package reusable across Claude, Codex, and OpenCode without depending on another project repository.

## Documentation Policy

- Chinese docs under `docs/zh-cn/` and `prompts/zh-cn/` are the internal source of truth.
- English docs under `docs/en/` and `prompts/en/` are release translations.
- Functional changes must land in Chinese first, then be translated to English for release.

## Quick Start

1. Read the internal overview in [docs/zh-cn/README.md](./docs/zh-cn/README.md).
2. Read the repository map in [docs/zh-cn/architecture/repository-map.md](./docs/zh-cn/architecture/repository-map.md).
3. Pick a platform guide:
   - [Claude Code](./docs/zh-cn/platforms/claude-code.md)
   - [Codex](./docs/zh-cn/platforms/codex.md)
   - [OpenCode](./docs/zh-cn/platforms/opencode.md)
4. Use the shared assets under `skills/shared/`.

## Shared Workflow Pack

- `skills/shared/workflows/prd-review.md`
- `skills/shared/workflows/tech-review.md`
- `skills/shared/workflows/implementation.md`
- `skills/shared/workflows/qa-validation.md`
- `skills/shared/workflows/release-review.md`
- `skills/shared/workflows/daily-sync.md`
- `skills/shared/workflows/todo-review.md`

## Project Structure

```text
AgentDevPipeline/
├── adapters/           # Platform-specific entrypoints
├── docs/               # Source docs, release docs, and starter delivery directories
├── plugins/            # Codex plugin package
├── prompts/            # Chinese source prompts + English release prompts
├── registry/           # Dependency metadata
└── skills/shared/      # Platform-neutral roles, workflows, templates, and playbooks
```

## Starter Delivery Directories

- `docs/prd/`
- `docs/tech/`
- `docs/qa/`
- `docs/memo/`
- `docs/todo/`
- `docs/research/`
- `docs/release/`

## Current Version

- Internal source version: `0.3.0`
- Public release version: `0.3.0`
