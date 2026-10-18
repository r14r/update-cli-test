set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

default:
    @just --list

update:
    python3 scripts/workflow.py update

bootstrap:
    python3 -m venv .venv
    .venv/bin/python -m pip install -q -r backend/requirements.txt
    npm install --prefix frontend --no-audit --no-fund --silent
    python3 scripts/workflow.py bootstrap

precommit:
    python3 scripts/workflow.py precommit

test:
    python3 scripts/workflow.py test

build:
    python3 scripts/workflow.py build

install:
    python3 scripts/workflow.py install

verify:
    python3 scripts/workflow.py check-update
    just bootstrap
    just precommit
    just test
    just build
    just install
    python3 scripts/workflow.py verify

# CI validation independent from external Update CLI and its update receipt.
verify-local:
    python3 -m venv .venv
    .venv/bin/python -m pip install -q -r backend/requirements.txt
    npm install --prefix frontend --no-audit --no-fund --silent
    .venv/bin/python -m pytest -q
    node --test cli/node/main.test.mjs
    npm test --prefix frontend
    npm run build --prefix frontend
    python3 scripts/assertions.py

up:
    docker compose up --build -d

down:
    docker compose down --remove-orphans

smoke:
    python3 scripts/smoke.py

clean:
    rm -rf .artifacts .venv frontend/node_modules frontend/.nuxt frontend/.output
