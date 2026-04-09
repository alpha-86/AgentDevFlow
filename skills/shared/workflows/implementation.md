# Implementation Workflow

## Goal

Convert an approved tech spec into code, tests, and implementation evidence.

## Required Traceability

- linked issue id
- approved PRD id
- approved tech spec id
- implementation commit links
- test evidence links

## Inputs

- approved PRD
- approved Tech Spec
- scoped todo items
- linked issue record

## Steps

1. Engineer verifies approved inputs.
2. Engineer implements the scoped change.
3. Engineer adds unit tests and change notes.
4. Engineer records any deviations or blockers.
5. Engineer updates issue with implementation evidence.
6. Engineer hands off traceable evidence to QA.

## Exit Criteria

- code change exists
- unit tests exist
- implementation notes exist
- QA handoff is possible

## Required Sign-off

- Engineer: required
- Tech Lead: required for implementation consistency check

## Re-entry Rules

- if implementation deviates from approved tech spec: return to tech review
- if acceptance criteria mapping is broken: return to PRD review
