# Anomaly Response Workflow

## Goal

Contain, escalate, and close delivery anomalies without losing traceability.

## Inputs

- anomaly description
- linked issue id
- impacted gate or document
- current owner

## Steps

1. Record anomaly type, time, and impact.
2. Classify severity as A1, A2, or A3.
3. Assign owner and target resolution time.
4. Link anomaly to issue, memo, and todo registry.
5. Escalate according to severity.
6. Verify closure evidence and update affected gate state.

## Escalation Rules

- A1: owner resolves within one working day.
- A2: review in daily sync or dedicated review.
- A3: stop downstream gate progression until explicit release.

## Exit Criteria

- root cause is documented
- immediate fix is documented
- follow-up prevention action exists
- issue and gate state are synchronized
