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


if __name__ == "__main__":
    unittest.main()
