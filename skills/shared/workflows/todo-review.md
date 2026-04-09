# Todo Review Workflow

## Goal

Track action items from creation through closure.

## Rules

- every review or discussion creates tracked actions
- every todo has issue id, gate, owner, priority, due date, and state
- blocked items must include escalation
- closed items must include evidence

## Status Model

- open
- in_progress
- blocked
- done
- canceled

## Required Closure Evidence

- merged change link or document update link
- verification record link (test report, review memo, or release record)

## Escalation Rule

- if item is blocked for more than one working day, escalate in daily sync and assign escalation owner
