#!/bin/bash
set -e
cd "$(dirname "$0")"

echo "================================================"
echo "  CI Test Fixer Playground — Verification"
echo "================================================"
echo ""

# Check main passes
echo "Checking main branch..."
git stash --quiet 2>/dev/null || true
git checkout main --quiet 2>/dev/null
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
main_result=$(python -m pytest -q --tb=no 2>&1 | tail -1)
echo "  main: $main_result"

if echo "$main_result" | grep -q "failed"; then
    echo "  ❌ ERROR: Tests failing on main!"
    exit 1
fi
echo "  ✅ All tests pass on main"
echo ""

# Check each break branch
echo "Checking break branches..."
total_branches=0
total_failures=0

for branch in $(git branch | grep break/ | sort); do
    git checkout "$branch" --quiet 2>/dev/null
    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
    result=$(python -m pytest -q --tb=no 2>&1 | tail -1)
    failures=$(echo "$result" | grep -oP '\d+ failed' | grep -oP '\d+' || echo "0")
    total_branches=$((total_branches + 1))
    total_failures=$((total_failures + failures))
    printf "  %-40s %s\n" "$branch" "$result"
done

git checkout main --quiet 2>/dev/null

echo ""
echo "================================================"
echo "  Summary: $total_branches branches, $total_failures total test failures"
echo "================================================"
