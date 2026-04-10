---
name: create-agent
description: Create a product-engineering agent using AgentDevFlow shared role files.
user-invocable: true
---

# create-agent

Supported types:

- team-lead
- product-manager
- tech-lead
- engineer
- qa-engineer
- researcher
- platform-sre

The created agent must load its shared role file under `skills/shared/agents/` and the required Chinese source prompts under `prompts/zh-cn/`.

## Creation Rules

1. load the selected shared role file first
2. load the required Chinese source prompts
3. inject critical rules, responsibilities, required reading, and standard actions
4. do not create a generic fallback role for a gated delivery responsibility
