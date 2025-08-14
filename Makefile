.PHONY: env clean install-hooks build

.EXPORT_ALL_VARIABLES:
UI_REPO_DIR := ${PWD}/../sense-table-ui

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
	uv run python -m unittest discover tests/


build:
	(rm -rf dist)
	#uv version --bump rc
	uv build
	
publish:
	UV_PUBLISH_TOKEN=$(shell awk '/password/ { print $$3 }' ~/.pypirc) uv publish

integration-test:
	uv run python -m unittest discover tests_integration -p "test_*.py"

update-screenshots:
	uv run python -m unittest discover tests_integration -p "doc_*.py"

test:
	make unit-test
	make build
	make integration-test

dev:
	FLASK_DEBUG=1 uv run sense_table/app.py

install-hooks:
	./scripts/install-hooks.sh

update-videos:
	(rm -rf docs/public/videos)
	uv run python tests_integration/update_videos.py
	for video in docs/public/videos/*.webm; do \
		ffmpeg -ss 1 -i "$$video" -c:v libvpx-vp9 -c:a libopus "$$video.2.webm"; \
		mv "$$video.2.webm" "$$video"; \
	done
