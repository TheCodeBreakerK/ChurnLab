.PHONY: post-create init sync ensure-ipykernel test-tools \
        dev-tools lint format type-check gitignore freeze get-data

post-create:
	@bash scripts/test_tools.sh
	@bash scripts/init.sh
	@bash scripts/ensure_ipykernel.sh
	@bash scripts/sync.sh

init:
	@bash scripts/init.sh

sync:
	@bash scripts/sync.sh

ensure-ipykernel:
	@bash scripts/ensure_ipykernel.sh

lint:
	@uv run ruff check .

format:
	@uv run ruff format .

type-check:
	@uv run mypy .

test-tools:
	@bash scripts/test_tools.sh

dev-tools:
	@bash scripts/dev_tools.sh

gitignore:
	@bash scripts/gitignore.sh

freeze:
	@bash scripts/freeze.sh

get-data:
	@bash scripts/get_data.sh