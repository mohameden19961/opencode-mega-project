#!/bin/bash
set -e

echo "Setting up CodeGuard development environment..."

python -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -e ".[dev]"
pip install pre-commit

echo "Development environment ready!"
echo "Run 'source venv/bin/activate' to activate it."
