# Packaging Strategy Research

**ID**: 000
**Status**: Draft
**Owner**: Researcher
**Date**: 2026-04-09

## Question

How should AgentDevPipeline package itself for Claude, Codex, and OpenCode while remaining self-contained?

## Options

- documentation + local skill pack + local plugin
- platform-specific duplicated packs
- external dependency-heavy thin layer

## Recommendation

Use one self-contained repository with a shared core plus thin platform adapters.

## Risks

- platform packaging formats may evolve independently

