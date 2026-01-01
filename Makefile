.DEFAULT: help

.PHONY: help
help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: setup
setup: ## Setup the development environment
	@uv venv --clear
	@uv sync --all-extras

.PHONY: check
check: ## Checks formatting, linting and type errors.
	@uv run ruff format .
	@uv run ruff check --fix .
	@uv run mypy .
	@hadolint Dockerfile

.PHONY: test
test: ## Run tests.
	@uv run pytest

.PHONY: test-in-ci
test-in-ci: ## Run tests and generate coverage report for CI.
	@rm -rf .coverage
	@rm -rf coverage
	@mkdir -p coverage
	@uv run pytest --cov=. --cov-report=xml:coverage/cobertura-coverage.xml
	@echo "Coverage report generated in coverage/cobertura-coverage.xml"

.PHONY: clean
clean: ## Clean up temporary files and directories.
	@rm -rf .coverage
	@rm -rf coverage
	@find . -type d -name "__pycache__" -exec rm -r {} +
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf .venv
	@rm -rf .ruff_cache
	@docker stop smartplaylist || true
	@docker rm smartplaylist || true

.PHONY: docker-run
docker-run: ## Build and run the Docker container.
	@docker stop smartplaylist || true
	@docker rm smartplaylist || true
	@docker build -t smartplaylist:latest .
	@docker run -d --name smartplaylist -p 8000:8000 -v $$(pwd)/_tmp:/app/data smartplaylist:latest

.PHONY: update-version
update-version: ## Bump version in pyproject.toml.
	@LATEST_TAG=$$(git describe --tags --abbrev=0 | sed 's/^v//') && \
	echo "Updating version to $$LATEST_TAG" && \
	sed -i '' "s/^version = \".*\"/version = \"$$LATEST_TAG\"/" pyproject.toml

