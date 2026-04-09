# Release Review Workflow

## Goal

Decide whether the current delivery package is safe and complete enough to release.

## Required Traceability

- linked issue id
- approved QA result link
- release plan and rollback plan links
- release decision record link

## Inputs

- approved QA result
- deployment plan
- rollback plan
- release notes
- linked issue record

## Steps

1. PM confirms business readiness.
2. Tech Lead confirms technical readiness.
3. Platform/SRE confirms deployment and rollback readiness.
4. Known risks are reviewed explicitly.
5. PM, Tech Lead, and Platform/SRE record sign-off decision.
6. Release decision and follow-up actions are written to linked issue.

## Outcomes

- approved for release
- approved with known risk
- blocked pending actions

## Required Sign-off

- PM: required
- Tech Lead: required
- Platform/SRE: required

## Re-entry Rules

- blocked pending actions: keep issue state at `in_release` or `blocked`
- release scope changed materially: return to QA validation or tech review
