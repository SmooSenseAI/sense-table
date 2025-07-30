#!/usr/bin/env bash

set -o pipefail  # To change the default behavior of Bash so that it treats any non-zero status in a pipeline like a total pipeline failure
set -e  # to exit on non-zero status
set -x  # to print out the command executed
set -u  # to exit if you use an unbound variable


docker run --rm --platform=linux/amd64 \
  -v "$PWD"/sense_table:/var/task/sense_table \
  -v "$PWD"/zappa/lambda.py:/var/task/lambda.py \
  -v "$PWD"/zappa/zappa_settings.json:/var/task/zappa_settings.json \
  -v "$PWD"/.python-version:/var/task/.python-version \
  -v "$PWD"/pyproject.toml:/var/task/pyproject.toml \
  -v "$PWD"/data:/var/task/data \
  -v ${HOME}/.aws:/root/.aws:ro \
  public.ecr.aws/sam/build-python3.9 \
  bash -c "
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ~/.local/bin/uv venv --seed
    ~/.local/bin/uv pip install . --pre
    ~/.local/bin/uv pip install zappa --pre
    . .venv/bin/activate && zappa update dev 

"

