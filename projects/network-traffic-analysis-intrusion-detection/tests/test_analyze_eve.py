import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "scripts" / "analyze_eve.py"
FIXTURE = PROJECT / "data" / "sample-eve.jsonl"


class AnalyzeEveTests(unittest.TestCase):
    def test_synthetic_fixture_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "summary.json"
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), str(FIXTURE), "--out", str(out)],
                capture_output=True, text=True, check=True,
            )
            summary = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(summary["alert_count"], 2)
            self.assertEqual(summary["event_type_counts"]["flow"], 1)
            self.assertEqual(summary["top_alert_source_ips"][0]["ip"], "192.0.2.10")
            self.assertIn("Wrote summary", proc.stdout)


if __name__ == "__main__":
    unittest.main()
