"""Regression: standalone bootstrap must not require a prior update."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "workflow.py"
spec = importlib.util.spec_from_file_location("fixture_workflow", SCRIPT)
workflow = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workflow)


class WorkflowReceiptTests(unittest.TestCase):
    def test_bootstrap_works_without_update_receipt(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".venv" / "bin").mkdir(parents=True)
            (root / ".venv" / "bin" / "python").touch()
            (root / "frontend" / "node_modules").mkdir(parents=True)
            with patch.object(workflow, "ROOT", root), patch.object(workflow, "ART", root / ".artifacts"):
                workflow.stage("bootstrap")
                self.assertEqual((root / ".artifacts" / "stage-bootstrap").read_text(), "ready\n")
                with self.assertRaisesRegex(AssertionError, "No successful update receipt"):
                    workflow.check_update()

    def test_update_initializes_isolated_target_and_records_receipt(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "VERSION").write_text("0.1.2\n")
            (root / "update-cli.yaml").write_text("schemaVersion: 2\n")
            target = root / ".artifacts" / "managed-project"
            calls = []

            def fake_run(*args):
                calls.append(args)
                if args[1] == "init":
                    config = target / ".update-cli" / "config.json"
                    config.parent.mkdir(parents=True, exist_ok=True)
                    config.write_text('{"projectName":"update-cli-test"}')
                elif args[1] == "update":
                    deployed = target / "current" / "VERSION"
                    deployed.parent.mkdir(parents=True, exist_ok=True)
                    deployed.write_text("0.1.2\n")

            with patch.object(workflow, "ROOT", root), patch.object(workflow, "ART", root / ".artifacts"), patch.object(workflow, "UPDATE_TARGET", target), patch.object(workflow, "run", side_effect=fake_run), patch.object(workflow.shutil, "which", return_value="/usr/local/bin/update-cli"):
                workflow.update("update-cli")
                self.assertEqual([args[1] for args in calls], ["init", "update"])
                self.assertEqual(calls[1][3], str(target))
                workflow.check_update()


if __name__ == "__main__":
    unittest.main()
