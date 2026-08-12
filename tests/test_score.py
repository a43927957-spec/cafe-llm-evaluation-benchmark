import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from score import (  # noqa: E402
    PERSONALIZATION_DATASET,
    build_summary,
    load_dataset,
    validate_dataset,
    weighted_score,
)


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


class PersonalizationBenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataset = load_dataset(PERSONALIZATION_DATASET)
        cls.rows = validate_dataset(cls.dataset)

    def test_contains_ten_unique_cases(self):
        ids = [case["id"] for case in self.dataset["cases"]]
        self.assertEqual(len(ids), 10)
        self.assertEqual(len(ids), len(set(ids)))

    def test_primary_dimensions_match_role(self):
        self.assertEqual(
            set(self.dataset["metadata"]["primary_dimensions"]),
            {"grounding", "integration", "helpfulness"},
        )

    def test_candidate_labels_are_balanced(self):
        summary = build_summary(self.rows)
        self.assertEqual(summary["a_wins"], 5)
        self.assertEqual(summary["b_wins"], 5)
        self.assertEqual(summary["ties"], 0)

    def test_conversations_use_one_to_five_turns(self):
        for case in self.dataset["cases"]:
            self.assertIn(len(case["conversation"]), range(1, 6))

    def test_rationales_reference_turns_and_sources(self):
        for case in self.dataset["cases"]:
            rationale = case["rationale_zh"]
            self.assertGreaterEqual(len(rationale), 80)
            for reference in case["turn_references"] + case["source_references"]:
                self.assertIn(reference, rationale)

    def test_every_case_requires_cleanup(self):
        self.assertTrue(all(case["cleanup_required"] for case in self.dataset["cases"]))

    def test_verified_debug_sources_exist(self):
        for case in self.dataset["cases"]:
            source_ids = {source["source_id"] for source in case["sources"]}
            for candidate in ("A", "B"):
                verified = set(case["debug_check"][candidate]["verified_sources"])
                self.assertTrue(verified.issubset(source_ids))

    def test_missing_debug_source_is_explicitly_flagged(self):
        target = next(case for case in self.dataset["cases"] if case["id"] == "PERS-008")
        debug = target["debug_check"]["B"]
        self.assertIn("C_missing", debug["claimed_sources"])
        self.assertTrue(debug["issues"])


if __name__ == "__main__":
    unittest.main()
