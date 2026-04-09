# QA Validation Workflow

## Goal

Validate the delivered implementation against PRD and Tech requirements.

## Required Traceability

- linked issue id
- approved PRD and tech spec ids
- QA case link
- test report link
- defect list and residual risk links

## Inputs

- approved PRD
- approved Tech Spec
- implementation evidence
- QA cases
- linked issue record

## Steps

1. QA derives or validates the case set.
2. QA executes validation.
3. QA records defects and residual risks.
4. PM reviews acceptance impact.
5. QA and PM record sign-off decision.
6. Release readiness is approved or blocked and written to linked issue.

## Exit Criteria

- test report exists
- blockers are explicit
- residual risk is explicit
- release recommendation is clear

## Required Sign-off

- QA: required
- PM: required for acceptance scope confirmation

## Re-entry Rules

- blocker defects: return to implementation
- missing testability or coverage mapping: return to tech review
- changed acceptance criteria: return to PRD review
