#!/usr/bin/env bash
# Test script for doc-pr-checks.yml Gate regex pattern
# Validates Pattern A: table row with role + date + decision
# Usage: ./scripts/test_gate_regex.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PASS=0
FAIL=0

# Pattern A regex (same as doc-pr-checks.yml)
check_sig() {
    local DOC_FILE="$1"; local ROLE="$2"; local GATE_NAME="$3"
    local SIG_LINE
    SIG_LINE=$(grep "^|" "${DOC_FILE}" | grep "| ${ROLE} |" | grep -E "\| [0-9]{4}-[0-9]{2}-[0-9]{2} \|.*\| (Approved|Conditional|Rejected|Draft|通过|待评审|驳回)" 2>/dev/null || true)
    if [ -n "$SIG_LINE" ]; then
        echo "  ✓ [${GATE_NAME}] ${ROLE}: MATCH"
        return 0
    else
        echo "  ✗ [${GATE_NAME}] ${ROLE}: NO MATCH"
        return 1
    fi
}

run_test() {
    local DOC_FILE="$1"
    local TEST_NAME="$2"
    shift 2
    while [ $# -gt 0 ]; do
        local ROLE="$1"; shift
        local EXPECTED="$1"; shift
        if check_sig "$DOC_FILE" "$ROLE" "$TEST_NAME" 2>/dev/null; then
            local ACTUAL="match"
        else
            local ACTUAL="no match"
        fi
        if [ "$EXPECTED" = "$ACTUAL" ]; then
            echo "  ✓ ${ROLE}: expected=$EXPECTED actual=$ACTUAL"
            ((PASS++))
        else
            echo "  ✗ ${ROLE}: expected=$EXPECTED actual=$ACTUAL"
            ((FAIL++))
        fi
    done
    echo ""
}

echo "=========================================="
echo "Gate Regex Pattern Tests"
echo "=========================================="
echo ""

# --- Test 1: Synthetic valid signatures ---
echo "[Test 1] Synthetic valid signatures"
TMPFILE=$(mktemp)
cat > "$TMPFILE" << 'EOF'
## 评审记录

| 日期 | 评审人 | 备注 | 决策 |
|---|---|---|---|
| 2026-04-15 | PM | OK | Approved |
| 2026-04-15 | 架构师 | Good | Approved |
| 2026-04-15 | 技术负责人 | LGTM | Conditional |
| 2026-04-15 | QA | Pass | Approved |
| 2026-04-15 | Engineer | Done | Rejected |
EOF
run_test "$TMPFILE" "Test1" "PM" "match" "架构师" "match" "技术负责人" "match" "QA" "match" "Engineer" "match"
rm "$TMPFILE"

# --- Test 2: Pseudo-signatures should NOT match ---
echo "[Test 2] Pseudo-signatures (should NOT match)"
TMPFILE=$(mktemp)
cat > "$TMPFILE" << 'EOF'
## Notes
需要 PM review 完成签字
| 2026-04-15 | Architect | OK | Approved |
| | QA | OK | Approved |
| 2026-04-15 | PM | OK | 待评审 |
| 2026-04-15 | 架构 | OK | Approved |
EOF
run_test "$TMPFILE" "Test2" "PM" "match" "架构师" "no match" "QA" "no match"
rm "$TMPFILE"

# --- Test 3: Existing documents (PRD-1, Tech-1, QA-1) - no Gate blocks ---
echo "[Test 3] Existing docs without Gate blocks (should have no sigs)"
for pair in "prd:PRD-1_v1:prd" "tech:Tech-1_v1:tech"; do
    DIR="${pair%%:*}"; pair="${pair#*:}"
    DOC="${pair%%:*}"; TEST="${pair#*:}"
    FILE="$SCRIPT_DIR/../docs/${DIR}/${DOC}.md"
    if [ -f "$FILE" ]; then
        RESULT=$(grep "^|" "${FILE}" | grep "| PM |" | grep -E "\| [0-9]{4}-[0-9]{2}-[0-9]{2} \|.*\| (Approved|Conditional|Rejected|Draft|通过|待评审|驳回)" 2>/dev/null || true)
        if [ -n "$RESULT" ]; then
            echo "  ? [Test3] ${DOC}: Has PM signature (review record found)"
        else
            echo "  ✓ [Test3] ${DOC}: no PM signature (no Gate block)"
        fi
    fi
done
FILE="$SCRIPT_DIR/../docs/qa/QA-1_v1.md"
if [ -f "$FILE" ]; then
    RESULT=$(grep "^|" "${FILE}" | grep "| PM |" | grep -E "\| [0-9]{4}-[0-9]{2}-[0-9]{2} \|.*\| (Approved|Conditional|Rejected|Draft|通过|待评审|驳回)" 2>/dev/null || true)
    if [ -n "$RESULT" ]; then
        echo "  ? [Test3] QA-1_v1: Has PM signature (review record found)"
    else
        echo "  ✓ [Test3] QA-1_v1: no PM signature (no Gate block)"
    fi
fi
echo ""

# --- Test 4: PRD-5 review records ---
# Actual decisions in file: "通过", "待评审", "已纳入...", "**Approved**", "v2", "**Approved**", "v3 — Approved"
# Rows with valid decisions: Team Lead(通过), PM(待评审)
# Rows with non-standard decisions: Architect(已纳入...), Team Lead(**Approved**), PM(v2), Team Lead(**Approved**), PM(v3 — Approved)
echo "[Test 4] PRD-5 review record table"
FILE="$SCRIPT_DIR/../docs/prd/005_adf_bootstrap_skill_system_2026-04-15.md"
if [ -f "$FILE" ]; then
    run_test "$FILE" "Test4" "Team Lead" "match" "PM" "match" "Architect" "no match"
else
    echo "  ! PRD-5 file not found"
fi
echo ""

# --- Test 5: Tech-5 review records ---
# All rows have standard decisions: Draft, Approved, Approved, Conditional, Approved
echo "[Test 5] Tech-5 review record table"
FILE="$SCRIPT_DIR/../docs/tech/Tech-5_v1.md"
if [ -f "$FILE" ]; then
    run_test "$FILE" "Test5" "架构师" "match" "PM" "match" "QA Engineer" "match" "Team Lead" "match"
else
    echo "  ! Tech-5 file not found"
fi
echo ""

# --- Test 6: QA-5 review records ---
# Only QA Engineer row has a decision value; PM/Architect/Engineer rows are placeholders
echo "[Test 6] QA-5 review record table"
FILE="$SCRIPT_DIR/../docs/qa/QA-5_v1.md"
if [ -f "$FILE" ]; then
    run_test "$FILE" "Test6" "QA Engineer" "match" "PM" "no match" "Architect" "no match" "Engineer" "no match"
else
    echo "  ! QA-5 file not found"
fi
echo ""

# --- Summary ---
echo "=========================================="
echo "Results: PASS=$PASS FAIL=$FAIL"
if [ "$FAIL" -eq 0 ]; then
    echo "All tests PASSED ✓"
    exit 0
else
    echo "Some tests FAILED ✗"
    exit 1
fi
