.PHONY: post-create init sync ensure-ipykernel test-tools \
        dev-tools lint format type-check gitignore freeze get-data \
        streamlit i18n-init i18n-extract i18n-update i18n-compile

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

test-tools:
	@bash scripts/test_tools.sh

dev-tools:
	@bash scripts/dev_tools.sh

lint:
	@uv run ruff check .

format:
	@uv run ruff format .

type-check:
	@uv run mypy .

gitignore:
	@bash scripts/gitignore.sh

freeze:
	@bash scripts/freeze.sh

get-data:
	@bash scripts/get_data.sh

streamlit:
	@uv run streamlit run /workspace/app/app.py --server.port 8501

i18n-init:
	uv run pybabel init -i /workspace/app/locales/messages.pot -d /workspace/app/locales -l pt_BR
	uv run pybabel init -i /workspace/app/locales/messages.pot -d /workspace/app/locales -l en_US

i18n-extract:
	uv run pybabel extract -F /workspace/app/babel.cfg -o /workspace/app/locales/messages.pot /workspace/app --project ChurnLab --version 0.1.0

i18n-update:
	uv run pybabel update -i /workspace/app/locales/messages.pot -d /workspace/app/locales

i18n-compile:
	uv run pybabel compile -d /workspace/app/locales
