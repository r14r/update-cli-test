"""Verify exact expected CLI results and configuration contracts."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent


def output(*args):
    return json.loads(subprocess.check_output(args, cwd=ROOT, text=True))


def main():
    assert output(sys.executable, "cli/python/main.py", "health") == {"runtime": "python", "status": "ok"}
    assert output(sys.executable, "cli/python/main.py", "add", "20", "22") == {"result": 42}
    assert output("node", "cli/node/main.mjs", "health") == {"runtime": "node", "status": "ok"}
    assert output("node", "cli/node/main.mjs", "add", "20", "22") == {"result": 42}
    assert "services:" in (ROOT / "compose.yaml").read_text()
    assert "schemaVersion: 2" in (ROOT / "update-cli.yaml").read_text()
    print("EXPECTED OUTPUTS OK")


if __name__ == "__main__":
    main()
