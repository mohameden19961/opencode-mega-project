#!/bin/bash
set -e

echo "Running CodeGuard checks..."

cd "$(dirname "$0")/.."

python -m codeguard analyze src/ --format terminal
python -m codeguard analyze src/ --format json --output report.json
python -m codeguard analyze src/ --severity high

echo "Checks complete!"
