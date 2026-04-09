# Tech Review Workflow

## Goal

Approve or reject a tech spec before implementation begins.

## Required Traceability

- linked issue id
- approved PRD id
- tech spec id and status
- review memo link
- todo links for follow-up actions

## Inputs

- approved PRD
- tech spec draft
- dependency and rollout notes
- linked issue record

## Steps

1. Tech Lead publishes tech spec.
2. PM checks requirement coverage.
3. QA checks testability and validation path.
4. Tech Lead and QA record sign-off decision in tech review record.
5. Review outcome is recorded in memo and linked issue comment.
6. Action items enter todo tracking with owner and due date.

## Review Checklist

- every major PRD requirement is covered
- interfaces and data flow are clear
- rollout and rollback points exist
- validation path is feasible
- risks and assumptions are explicit

## Required Sign-off

- Tech Lead: required
- QA: required
- PM: confirmation required for scope consistency

## Outcomes

- approved
- conditionally approved
- rejected with rework items

## Re-entry Rules

- conditionally approved: all conditions must be closed and rechecked before implementation
- rejected: tech spec must be revised and reviewed again
- if PRD changed materially: return to PRD review first
