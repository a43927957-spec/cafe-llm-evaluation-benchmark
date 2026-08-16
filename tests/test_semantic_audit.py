import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from semantic_audit import (  # noqa: E402
    DEFAULT_DATASET,
    DIAGNOSIS_LAYERS,
    load_dataset,
    validate_dataset,
)


class GeminiZhSemanticAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataset = load_dataset(DEFAULT_DATASET)
        cls.rows = validate_dataset(cls.dataset)
        cls.sources = {source["source_id"]: source for source in cls.dataset["sources"]}

    def test_contains_six_unique_cases(self):
        ids = [case["id"] for case in self.dataset["cases"]]
        self.assertEqual(len(ids), 6)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(self.rows), 6)

    def test_source_provenance_has_valid_sha256(self):
        for source in self.dataset["sources"]:
            self.assertRegex(source["sha256"], re.compile(r"^[0-9a-f]{64}$"))
            self.assertTrue(source["generated_at"].endswith("Z"))

    def test_exact_model_id_is_not_fabricated(self):
        attribution = self.dataset["metadata"]["provider_attribution"]
        self.assertEqual(attribution["confirmed_provider"], "Gemini API")
        self.assertEqual(attribution["exact_model_id"], "not_recorded_in_artifacts")
        self.assertEqual(
            attribution["end_to_end_reply_attribution"],
            "system_output_not_direct_provider_quote",
        )

    def test_evidence_levels_match_source_provenance(self):
        counts = {"confirmed_gemini_structured_output": 0, "end_to_end_system_output": 0}
        for case in self.dataset["cases"]:
            source = self.sources[case["source_id"]]
            counts[case["evidence_level"]] += 1
            if case["evidence_level"] == "confirmed_gemini_structured_output":
                self.assertTrue(source["direct_gemini_runner"])
            else:
                self.assertFalse(source["direct_gemini_runner"])
        self.assertEqual(counts["confirmed_gemini_structured_output"], 3)
        self.assertEqual(counts["end_to_end_system_output"], 3)

    def test_chinese_analysis_and_concise_english_conclusion(self):
        cjk = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
        english_word = re.compile(r"\b[A-Za-z]+(?:[-'][A-Za-z]+)*\b")
        for case in self.dataset["cases"]:
            self.assertGreaterEqual(len(case["analysis_zh"]), 80)
            self.assertRegex(case["analysis_zh"], cjk)
            self.assertNotRegex(case["conclusion_en"], cjk)
            self.assertIn(len(english_word.findall(case["conclusion_en"])), range(8, 46))

    def test_root_cause_layers_cover_the_full_diagnostic_chain(self):
        layers = {case["diagnosis_layer"] for case in self.dataset["cases"]}
        self.assertEqual(layers, DIAGNOSIS_LAYERS)

    def test_iteration_metrics_match_archived_evidence(self):
        metrics = {
            item["stage"]: (
                item["total_runs"],
                item["valid_runs"],
                item["exact_frame_runs"],
                item["core_semantic_runs"],
            )
            for item in self.dataset["iteration_evidence"]
        }
        self.assertEqual(metrics["initial_30x3"], (90, 27, 15, 27))
        self.assertEqual(metrics["canonical_prompt_30x3"], (90, 72, 45, 63))
        self.assertEqual(metrics["final_v2_30x3"], (90, 90, 90, 90))
        self.assertEqual(metrics["final_v2_full_96"], (96, 96, 86, 96))

    def test_privacy_boundary_and_product_gate_are_explicit(self):
        privacy = self.dataset["metadata"]["privacy"]
        self.assertFalse(privacy["real_customer_data"])
        self.assertFalse(privacy["production_customer_messages"])
        self.assertFalse(privacy["merchant_identity_published"])

        gate = self.dataset["product_gate"]
        self.assertEqual(gate["verdict"], "NO-GO")
        self.assertEqual(
            gate["customer_visible_replies"] + gate["silent_cases"],
            gate["total_cases"],
        )
        self.assertLessEqual(gate["answerable_replied"], gate["answerable_cases"])


if __name__ == "__main__":
    unittest.main()
