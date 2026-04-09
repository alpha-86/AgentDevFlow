# PRD Review Workflow

## Goal

Approve or reject a PRD before technical design begins.

## Required Traceability

- linked issue id
- PRD document id and status
- review memo link
- action items in todo registry

## Inputs

- current requirement statement
- PRD draft
- known constraints or dependencies
- linked issue record

## Steps

1. PM prepares PRD and acceptance criteria.
2. Tech Lead reviews feasibility, dependencies, and risks.
3. Optional domain reviewer validates business fit.
4. PM and Tech Lead record sign-off decision in PRD review record.
5. Review outcome is recorded in memo and linked issue comment.
6. Action items enter todo tracking with owner and due date.

## Review Checklist

- scope is explicit
- non-goals are explicit
- acceptance criteria are testable
- dependencies are identified
- unresolved risks are visible

## Required Sign-off

- PM: required
- Tech Lead: required

## Outcomes

- approved
- conditionally approved
- rejected with rework items

## Re-entry Rules

- conditionally approved: all conditions must be closed with evidence before tech review
- rejected: PRD must be revised and reviewed again
- blocked: escalate to Team Lead and keep issue state at `blocked`
