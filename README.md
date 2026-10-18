# Update CLI Test

A fully working integration fixture for [Update CLI](https://github.com/r14r/update-cli).

It includes a **FastAPI backend**, a **Vue/Nuxt UI frontend**, independent **Python and Node CLIs**, **Docker Compose**, automated tests, and a receipt-based **five-stage lifecycle verifier**.

## Full update workflow

Install Update CLI, just, Python 3.11+, Node 20+, npm, and Docker Compose. From the test repository checkout, run:

```sh
just update
just verify
```

`just update` creates an isolated managed project in `.artifacts/managed-project/` using `update-cli init` (only on first run), then invokes the real `update-cli update` command without automatic setup or interactive waiting. The Git checkout under `current/` is never treated as the updater's runtime root. The downloaded release version is checked against the checkout before writing the receipt. On success it records an update receipt containing the project version and a SHA-256 checksum of the update manifest. If the update fails, no success receipt is written.

`just verify` **requires that update receipt** before running:

1. **Bootstrap:** create `.venv`, install Python and Node dependencies quietly, verify the environment.
2. **Precommit:** compile and lint Python sources with Ruff.
3. **Test:** pytest FastAPI, Node CLI tests, Nuxt tests and exact output assertions.
4. **Build:** compile the Nuxt SSR frontend and verify the expected server bundle.
5. **Install:** install sample Python and Node CLI programs under `.artifacts/install/`, never overwriting system executables.

Individual stages (including `update-cli bootstrap` and `just bootstrap`) can be run before the first update. Only `just verify` requires a successful update receipt. Each stage writes an independently checked status receipt, and the verifier asserts all five stages plus the expected outputs. A failure stops execution immediately.

> Run both commands from your Git checkout. Update CLI's runtime configuration is created separately in `.artifacts/managed-project/.update-cli/config.json`; do not initialize `.update-cli` inside your `current/` checkout.

## CI

```sh
just verify-local
```

This validates Python, Node and Nuxt without needing an installed Update CLI or a prior update receipt. GitHub Actions also validates `docker compose config`.

## Docker Compose

```sh
just up
just smoke
just down
```

Backend: http://localhost:18080/api/health

Frontend: http://localhost:13000/

The frontend reverse-proxies `/api/*` requests to FastAPI.

## CLI examples

```sh
python3 cli/python/main.py add 20 22
node cli/node/main.mjs add 20 22
```

Both must return JSON equivalent to `{"result": 42}`. Tests compare parsed JSON values, not only exit codes.
