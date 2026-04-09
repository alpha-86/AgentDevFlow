# Context Recovery Workflow

## Goal

Recover execution context after session loss, environment switch, or role handoff without reducing review rigor.

## Triggers

- cleared conversation history
- agent restart
- ownership handoff
- stale task resumed after a long pause

## Inputs

- linked issue id
- latest gate state
- latest memo and todo links
- latest change record links

## Steps

1. Read issue status and latest decision record.
2. Read current-stage documents and their status.
3. Read open blockers, todos, and anomaly records.
4. Produce a recovery summary.
5. Confirm next action is still valid before execution.

## Recovery Summary Fields

- current issue
- current gate
- latest decision
- open blockers
- open todos
- next action
- required approver or owner

## Exit Criteria

- recovery summary exists
- execution stage is unambiguous
- no required upstream record is missing
