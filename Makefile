.PHONY: install dev test lint clean build

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=src/codeguard --cov-report=term-missing

lint:
	black src/codeguard tests/
	ruff check src/codeguard/ tests/

typecheck:
	mypy src/codeguard/

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

build: clean
	python -m build

release: lint test build
	echo "Ready for release"
