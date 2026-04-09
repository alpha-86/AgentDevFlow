# Issue Lifecycle Workflow

## Goal

Use a single issue as the traceability spine across PRD, tech, implementation, QA, release, and follow-up actions.

## States

- open
- in_prd
- in_tech
- in_impl
- in_qa
- in_release
- blocked
- done
- canceled

## Required Fields

- issue owner
- current gate
- linked documents
- latest review decision
- open blockers
- open todo items

## Transition Rules

1. `open` -> `in_prd` only after scope owner is assigned.
2. `in_prd` -> `in_tech` only after PRD approval is recorded.
3. `in_tech` -> `in_impl` only after tech sign-off is complete.
4. `in_impl` -> `in_qa` only after implementation evidence is linked.
5. `in_qa` -> `in_release` only after QA sign-off or explicit known-risk acceptance.
6. Any state -> `blocked` when downstream work cannot safely continue.
7. `in_release` -> `done` only after release decision is recorded.

## Required Records

- gate decision comment
- linked memo or review note
- todo updates for follow-up work

## Failure Modes

- issue state drifts from actual delivery stage
- linked documents are missing or outdated
- state changes without recorded decision evidence
