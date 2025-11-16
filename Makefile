.PHONY: help install install-dev uninstall upgrade list run-commit run-review test-commit test-review clean format lint check build-commit build-review

help:  ## Show this help message
	@echo "Best Commits Monorepo - Development Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install all tools
	./scripts/install-tool.sh

install-commit:  ## Install only commit tool
	./scripts/install-tool.sh commit

install-review:  ## Install only review tool
	./scripts/install-tool.sh review

install-dev:  ## Install all tools in editable mode
	./scripts/install-tool.sh --editable

install-commit-dev:  ## Install commit tool in editable mode
	./scripts/install-tool.sh --editable commit

install-review-dev:  ## Install review tool in editable mode
	./scripts/install-tool.sh --editable review

uninstall:  ## Uninstall all tools
	./scripts/install-tool.sh --uninstall

uninstall-commit:  ## Uninstall commit tool only
	./scripts/install-tool.sh --uninstall commit

uninstall-review:  ## Uninstall review tool only
	./scripts/install-tool.sh --uninstall review

upgrade-commit:  ## Upgrade commit tool
	uv tool upgrade best-commits-commit

upgrade-review:  ## Upgrade review tool
	uv tool upgrade best-commits-review

list:  ## List installed uv tools
	uv tool list

run-commit:  ## Run commit tool without installation
	uvx --from ./tools/commit_changes commit

run-review:  ## Run review tool without installation
	uvx --from ./tools/review_changes review

test-commit:  ## Test the commit module directly
	cd tools/commit_changes && uv run -m commit_changes

test-review:  ## Test the review module directly
	cd tools/review_changes && uv run -m review_changes

clean:  ## Clean up build artifacts and caches
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find tools -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	find tools -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true

format:  ## Format code with black
	uvx black tools/

lint:  ## Lint code with ruff
	uvx ruff check tools/

check:  ## Run format and lint checks
	@echo "Running format check..."
	uvx black --check tools/
	@echo "Running lint check..."
	uvx ruff check tools/

build-commit:  ## Build commit tool package
	cd tools/commit_changes && uv build

build-review:  ## Build review tool package
	cd tools/review_changes && uv build

build-all:  ## Build all tool packages
	@echo "Building commit tool..."
	cd tools/commit_changes && uv build
	@echo "Building review tool..."
	cd tools/review_changes && uv build
