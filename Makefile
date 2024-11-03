#include .env
export

app-dir = app


.PHONY help:
up:
	docker compose -f docker-compose.yml up -d --build --timeout 60

.PHONY down:
down:
	docker compose -f docker-compose.yml down --timeout 60

.PHONY pull:
pull:
	git pull origin master
	git submodule update --init --recursive


.PHONY lint:
lint:
	echo "Running ruff..."
	uv run ruff check --config pyproject.toml --diff $(app-dir)

.PHONY format:
format:
	echo "Running ruff check with --fix..."
	uv run ruff check --config pyproject.toml --fix --unsafe-fixes $(app-dir)

	echo "Running ruff..."
	uv run ruff format --config pyproject.toml $(app-dir)

	echo "Running isort..."
	uv run isort --settings-file pyproject.toml $(app-dir)

.PHONE mypy:
mypy:
	echo "Running MyPy..."
	uv run mypy --config-file pyproject.toml --package $(app-dir).$(bot-dir)

.PHONY show-outdated:
show-outdated:
	uv run pcu .\pyproject.toml --extra lint --extra dev --extra uvloop

.PHONY uv-sync:
uv-sync:
	uv sync --extra dev --extra lint --extra uvloop --link-mode=copy

.PHONY freeze: uv-sync
freeze:
	uv export --quiet --format requirements-txt --no-dev --extra uvloop --output-file app/requirements.txt

