import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from score import build_summary, load_dataset, validate_dataset, weighted_score  # noqa: E402


class BenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataset = load_dataset()
        cls.rows = validate_dataset(cls.dataset)

    def test_dataset_is_explicitly_synthetic(self):
        self.assertTrue(self.dataset["metadata"]["synthetic"])

    def test_weights_sum_to_100(self):
        self.assertEqual(sum(self.dataset["weights"].values()), 100)

    def test_contains_twelve_unique_cases(self):
        ids = [case["id"] for case in self.dataset["cases"]]
        self.assertEqual(len(ids), 12)
        self.assertEqual(len(ids), len(set(ids)))

    def test_all_scores_use_one_to_five_scale(self):
        for case in self.dataset["cases"]:
            for candidate in ("A", "B"):
                for score in case["scores"][candidate].values():
                    self.assertIn(score, range(1, 6))

    def test_weighted_score_bounds(self):
        weights = self.dataset["weights"]
        self.assertEqual(weighted_score({key: 1 for key in weights}, weights), 20.0)
        self.assertEqual(weighted_score({key: 5 for key in weights}, weights), 100.0)

    def test_candidate_labels_are_balanced(self):
        summary = build_summary(self.rows)
        self.assertEqual(summary["a_wins"], 6)
        self.assertEqual(summary["b_wins"], 6)
        self.assertEqual(summary["ties"], 0)

    def test_json_round_trip(self):
        encoded = json.dumps(self.dataset, ensure_ascii=False)
        decoded = json.loads(encoded)
        self.assertEqual(decoded["metadata"]["locale"], "zh-TW")


if __name__ == "__main__":
    unittest.main()
