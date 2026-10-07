import json
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from run_detections import load_events, RULES


class DetectionLabTests(unittest.TestCase):
    def test_dataset_contains_events(self):
        self.assertGreater(len(load_events()), 0)

    def test_all_events_have_required_fields(self):
        for event in load_events():
            self.assertIn("event_id", event)
            self.assertIn("timestamp", event)
            self.assertIn("host", event)
            self.assertIn("event_type", event)

    def test_rules_have_attack_mapping(self):
        for rule in RULES:
            self.assertRegex(rule["technique"], r"^T\d{4}(\.\d{3})?$")
            self.assertIn("tactic", rule)
            self.assertIn("severity", rule)


if __name__ == "__main__":
    unittest.main()
