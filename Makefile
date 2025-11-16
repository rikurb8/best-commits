.PHONY: help install install-dev uninstall upgrade test clean format lint run-commit run-review

help:  ## Show this help message
	@echo "Best Commits - Development Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install the tools (uv tool install)
	./scripts/install-tool.sh

install-dev:  ## Install in editable mode for development
	./scripts/install-tool.sh --editable

uninstall:  ## Uninstall the tools
	./scripts/install-tool.sh --uninstall

upgrade:  ## Upgrade to latest version
	uv tool upgrade best-commits

list:  ## List installed uv tools
	uv tool list

run-commit:  ## Run commit tool without installation (using uvx)
	uvx --from . commit

run-review:  ## Run review tool without installation (using uvx)
	uvx --from . review

test-commit:  ## Test the commit module directly
	uv run -m tools.commit_changes

test-review:  ## Test the review module directly
	uv run -m tools.review_changes

clean:  ## Clean up build artifacts and caches
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

format:  ## Format code with black
	uvx black tools/

lint:  ## Lint code with ruff
	uvx ruff check tools/

check:  ## Run format and lint checks
	@echo "Running format check..."
	uvx black --check tools/
	@echo "Running lint check..."
	uvx ruff check tools/

build:  ## Build the package
	uv build

publish-test:  ## Publish to test PyPI
	uv publish --index-url https://test.pypi.org/legacy/

publish:  ## Publish to PyPI (use with caution!)
	uv publish
