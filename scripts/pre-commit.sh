#!/bin/bash
echo "Running CodeGuard pre-commit check..."
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$' || true)
if [ -z "$FILES" ]; then exit 0; fi
python -m codeguard check $FILES --severity medium
STATUS=$?
if [ $STATUS -ne 0 ]; then
    echo "CodeGuard found violations. Use git commit --no-verify to bypass"
    exit 1
fi
echo "CodeGuard check passed!"
