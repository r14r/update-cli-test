"""Record and verify results for the Update CLI integration fixture."""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / ".artifacts"
STAGES = ("bootstrap", "precommit", "test", "build", "install")
EXPECTED = {"bootstrap": "ready", "precommit": "clean", "test": "passed",
            "build": "built", "install": "installed"}


def run(*args):
    print("+", *map(str, args), flush=True)
    subprocess.run(list(map(str, args)), cwd=ROOT, check=True)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    ART.mkdir(exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def check_update():
    path = ART / "update.json"
    assert path.exists(), "No successful update receipt: run 'just update' first"
    data = json.loads(path.read_text())
    assert data["status"] == "success"
    assert data["version"] == (ROOT / "VERSION").read_text().strip()
    assert data["manifest_sha256"] == digest(ROOT / "update-cli.yaml")
    print("UPDATE RECEIPT OK", flush=True)


def ci_baseline():
    assert os.getenv("GITHUB_ACTIONS") == "true", "Synthetic receipts are for GitHub CI only"
    save(ART / "update.json", {"status": "success",
         "version": (ROOT / "VERSION").read_text().strip(),
         "manifest_sha256": digest(ROOT / "update-cli.yaml")})
    print("SYNTHETIC CI UPDATE BASELINE CREATED")


def update(cli):
    assert shutil.which(cli), f"Update CLI not found: {cli}"
    run(cli, "update", "--root", str(ROOT), "--no-setup", "--no-wait")
    save(ART / "update.json", {"status": "success",
         "version": (ROOT / "VERSION").read_text().strip(),
         "manifest_sha256": digest(ROOT / "update-cli.yaml")})
    print("UPDATE RECEIPT OK")


def stage(name):
    # Standalone lifecycle stages must work before the first update.
    # Only the complete verification command requires an update receipt.
    if name == "bootstrap":
        assert (ROOT / ".venv/bin/python").exists(), "Python virtualenv missing"
        assert (ROOT / "frontend/node_modules").exists(), "Node dependencies missing"
    elif name == "precommit":
        run("python3", "-m", "compileall", "-q", "backend", "cli/python")
        run(".venv/bin/python", "-m", "ruff", "check", "backend", "cli/python", "scripts")
    elif name == "test":
        run(".venv/bin/python", "-m", "pytest", "-q")
        run("node", "--test", "cli/node/main.test.mjs")
        run("npm", "test", "--prefix", "frontend")
        run(sys.executable, "scripts/assertions.py")
    elif name == "build":
        run("npm", "run", "build", "--prefix", "frontend")
        assert (ROOT / "frontend/.output/server/index.mjs").is_file(), "Nuxt SSR output missing"
    elif name == "install":
        target = ART / "install"
        target.mkdir(exist_ok=True)
        for source, output in (("cli/python/main.py", "fixture-py"), ("cli/node/main.mjs", "fixture-node")):
            dest = target / output
            shutil.copyfile(ROOT / source, dest)
            dest.chmod(0o755)
        assert (target / "fixture-py").exists()
        assert (target / "fixture-node").exists()
    ART.mkdir(parents=True, exist_ok=True)
    (ART / f"stage-{name}").write_text(EXPECTED[name] + "\n")
    print(f"{name.upper()} OK")


def verify():
    check_update()
    for name, expected in EXPECTED.items():
        assert (ART / f"stage-{name}").read_text() == expected + "\n", f"{name}: receipt mismatch"
    run(sys.executable, "scripts/assertions.py")
    print("ALL WORKFLOW STAGES VERIFIED")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("update", *STAGES, "verify", "check-update", "ci-baseline"))
    parser.add_argument("--cli", default=os.getenv("UPDATE_CLI_BIN", "update-cli"))
    options = parser.parse_args()
    if options.action == "update": update(options.cli)
    elif options.action == "ci-baseline": ci_baseline()
    elif options.action == "verify": verify()
    elif options.action == "check-update": check_update()
    else: stage(options.action)
