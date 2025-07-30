.PHONY: env clean

.EXPORT_ALL_VARIABLES:
UI_REPO_DIR := ${PWD}/../sense-table-ui
URL_PREFIX := /demo

update-settings-schema:
	uv run datamodel-codegen \
	    --input ${UI_REPO_DIR}/src/settings.schema.yaml \
		--input-file-type jsonschema \
		--output sense_table/settings.py \
		--base-class sense_table.utils.models.ImmutableBaseModel

clean:
	rm -rf {.venv,dist,.pytest_cache,*.egg-info}


env:
	(rm -rf .venv)
	uv venv --seed && uv sync --all-groups
	uv run playwright install 



unit-test:
	uv run python -m unittest discover tests


build:
	(rm -rf dist)
	#uv version --bump rc
	uv build
	
publish:
	UV_PUBLISH_TOKEN=$(shell awk '/password/ { print $$3 }' ~/.pypirc) uv publish

integration-test:
	rm -rf tests_integration/{screenshots}
	uv run python -m unittest discover tests_integration/


test:
	make unit-test
	make build
	make integration-test

dev:
	FLASK_DEBUG=1 uv run sense_table/app.py