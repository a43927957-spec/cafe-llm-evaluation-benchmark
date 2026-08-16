#!/usr/bin/env python3
"""Validate and summarize the Gemini Traditional Chinese semantic audit."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = ROOT / "data" / "gemini_zh_semantics.json"

EVIDENCE_LEVELS = {
    "confirmed_gemini_structured_output",
    "end_to_end_system_output",
}
DIAGNOSIS_LAYERS = {
    "model_extraction",
    "semantic_representation",
    "evidence_coverage",
    "answer_realization",
}
SEVERITIES = {"low", "medium", "high", "critical"}
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
CJK_PATTERN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
ENGLISH_WORD_PATTERN = re.compile(r"\b[A-Za-z]+(?:[-'][A-Za-z]+)*\b")


def load_dataset(path: Path = DEFAULT_DATASET) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def english_word_count(text: str) -> int:
    return len(ENGLISH_WORD_PATTERN.findall(text))


def validate_dataset(dataset: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[str] = []
    metadata = dataset.get("metadata", {})
    sources = dataset.get("sources", [])
    iterations = dataset.get("iteration_evidence", [])
    product_gate = dataset.get("product_gate", {})
    cases = dataset.get("cases", [])

    validate_metadata(metadata, errors)
    source_map = validate_sources(sources, errors)
    validate_iterations(iterations, source_map, errors)
    rows = validate_cases(cases, source_map, errors)
    validate_product_gate(product_gate, source_map, errors)

    if errors:
        raise ValueError("Semantic audit validation failed:\n- " + "\n- ".join(errors))
    return rows


def validate_metadata(metadata: dict[str, Any], errors: list[str]) -> None:
    if metadata.get("schema_version") != "gemini-zh-semantic-audit-v1":
        errors.append("metadata.schema_version must be gemini-zh-semantic-audit-v1")
    if metadata.get("locale") != "zh-TW":
        errors.append("metadata.locale must be zh-TW")
    if metadata.get("input_prompts") != "synthetic_evaluation_prompts":
        errors.append("input prompts must be labeled as synthetic evaluation prompts")
    if metadata.get("output_evidence") != "archived_real_inference_artifacts":
        errors.append("output evidence must be labeled as archived real inference artifacts")

    attribution = metadata.get("provider_attribution", {})
    if attribution.get("confirmed_provider") != "Gemini API":
        errors.append("confirmed provider must be Gemini API")
    if attribution.get("exact_model_id") != "not_recorded_in_artifacts":
        errors.append("exact model ID must remain not_recorded_in_artifacts")
    if attribution.get("end_to_end_reply_attribution") != "system_output_not_direct_provider_quote":
        errors.append("end-to-end replies must not be presented as direct provider quotes")

    privacy = metadata.get("privacy", {})
    for field in ("real_customer_data", "production_customer_messages", "merchant_identity_published"):
        if privacy.get(field) is not False:
            errors.append(f"privacy.{field} must be false")
    if privacy.get("source_prompt_type") != "synthetic_test_cases":
        errors.append("privacy.source_prompt_type must be synthetic_test_cases")

    language = metadata.get("language_policy", {})
    if language.get("primary") != "Traditional Chinese":
        errors.append("Traditional Chinese must be the primary analysis language")
    if language.get("english") != "one concise conclusion per case":
        errors.append("English must be limited to one concise conclusion per case")


def validate_sources(
    sources: list[dict[str, Any]], errors: list[str]
) -> dict[str, dict[str, Any]]:
    source_map: dict[str, dict[str, Any]] = {}
    for source in sources:
        source_id = source.get("source_id")
        if not source_id:
            errors.append("every source requires a source_id")
            continue
        if source_id in source_map:
            errors.append(f"duplicate source id: {source_id}")
        source_map[source_id] = source

        if not source.get("artifact"):
            errors.append(f"{source_id}: artifact name is required")
        if not str(source.get("generated_at", "")).endswith("Z"):
            errors.append(f"{source_id}: generated_at must be a UTC timestamp")
        if not SHA256_PATTERN.fullmatch(str(source.get("sha256", ""))):
            errors.append(f"{source_id}: sha256 must contain 64 lowercase hex characters")
        if not isinstance(source.get("direct_gemini_runner"), bool):
            errors.append(f"{source_id}: direct_gemini_runner must be boolean")
        if not CJK_PATTERN.search(str(source.get("attribution_zh", ""))):
            errors.append(f"{source_id}: Traditional Chinese attribution is required")

    if len(source_map) < 2:
        errors.append("at least two evidence sources are required")
    return source_map


def validate_iterations(
    iterations: list[dict[str, Any]],
    source_map: dict[str, dict[str, Any]],
    errors: list[str],
) -> None:
    stages: set[str] = set()
    for item in iterations:
        stage = item.get("stage")
        if not stage:
            errors.append("every iteration requires a stage")
        elif stage in stages:
            errors.append(f"duplicate iteration stage: {stage}")
        stages.add(stage)

        source_id = item.get("source_id")
        if source_id not in source_map:
            errors.append(f"{stage}: iteration source does not resolve")
        elif source_map[source_id].get("direct_gemini_runner") is not True:
            errors.append(f"{stage}: iteration metrics must use a direct Gemini runner source")

        total = item.get("total_runs")
        metrics = {
            "valid_runs": item.get("valid_runs"),
            "exact_frame_runs": item.get("exact_frame_runs"),
            "core_semantic_runs": item.get("core_semantic_runs"),
        }
        if not isinstance(total, int) or total <= 0:
            errors.append(f"{stage}: total_runs must be a positive integer")
            continue
        for label, value in metrics.items():
            if not isinstance(value, int) or not 0 <= value <= total:
                errors.append(f"{stage}: {label} must be between 0 and total_runs")


def validate_cases(
    cases: list[dict[str, Any]],
    source_map: dict[str, dict[str, Any]],
    errors: list[str],
) -> list[dict[str, str]]:
    if len(cases) != 6:
        errors.append("the primary audit must contain exactly six cases")

    seen_ids: set[str] = set()
    rows: list[dict[str, str]] = []
    required_fields = {
        "id",
        "source_id",
        "source_case_id",
        "evidence_level",
        "diagnosis_layer",
        "failure_type",
        "severity",
        "input_zh",
        "expected_semantics",
        "observed_output",
        "analysis_zh",
        "conclusion_en",
        "remediation_zh",
    }

    for case in cases:
        case_id = case.get("id", "<missing>")
        if case_id in seen_ids:
            errors.append(f"duplicate case id: {case_id}")
        seen_ids.add(case_id)

        missing = sorted(required_fields - set(case))
        if missing:
            errors.append(f"{case_id}: missing fields: {', '.join(missing)}")

        evidence_level = case.get("evidence_level")
        if evidence_level not in EVIDENCE_LEVELS:
            errors.append(f"{case_id}: unsupported evidence level")
        diagnosis_layer = case.get("diagnosis_layer")
        if diagnosis_layer not in DIAGNOSIS_LAYERS:
            errors.append(f"{case_id}: unsupported diagnosis layer")
        severity = case.get("severity")
        if severity not in SEVERITIES:
            errors.append(f"{case_id}: unsupported severity")

        source_id = case.get("source_id")
        source = source_map.get(source_id)
        if source is None:
            errors.append(f"{case_id}: source does not resolve")
        elif evidence_level == "confirmed_gemini_structured_output":
            if source.get("direct_gemini_runner") is not True:
                errors.append(f"{case_id}: confirmed Gemini output must use a direct runner source")
        elif evidence_level == "end_to_end_system_output":
            if source.get("direct_gemini_runner") is not False:
                errors.append(f"{case_id}: system output must use an end-to-end source")

        if not case.get("source_case_id"):
            errors.append(f"{case_id}: source_case_id is required")
        if not CJK_PATTERN.search(str(case.get("input_zh", ""))):
            errors.append(f"{case_id}: input_zh must contain Traditional Chinese content")
        if not isinstance(case.get("expected_semantics"), dict) or not case.get("expected_semantics"):
            errors.append(f"{case_id}: expected_semantics must be a non-empty object")
        if not isinstance(case.get("observed_output"), dict) or not case.get("observed_output"):
            errors.append(f"{case_id}: observed_output must be a non-empty object")

        analysis_zh = str(case.get("analysis_zh", ""))
        if len(analysis_zh) < 80 or not CJK_PATTERN.search(analysis_zh):
            errors.append(f"{case_id}: analysis_zh must contain at least 80 characters of Chinese analysis")
        if not CJK_PATTERN.search(str(case.get("remediation_zh", ""))):
            errors.append(f"{case_id}: remediation_zh must contain Chinese guidance")

        conclusion_en = str(case.get("conclusion_en", ""))
        word_count = english_word_count(conclusion_en)
        if not 8 <= word_count <= 45:
            errors.append(f"{case_id}: conclusion_en must contain 8 to 45 English words")
        if CJK_PATTERN.search(conclusion_en):
            errors.append(f"{case_id}: conclusion_en must not contain CJK characters")

        rows.append(
            {
                "id": str(case_id),
                "failure_type": str(case.get("failure_type", "")),
                "diagnosis_layer": str(diagnosis_layer),
                "severity": str(severity),
                "evidence_level": str(evidence_level),
            }
        )

    return rows


def validate_product_gate(
    gate: dict[str, Any],
    source_map: dict[str, dict[str, Any]],
    errors: list[str],
) -> None:
    source_id = gate.get("source_id")
    if source_id not in source_map:
        errors.append("product gate source does not resolve")
    elif source_map[source_id].get("direct_gemini_runner") is not False:
        errors.append("product gate must use an end-to-end source")
    if gate.get("verdict") != "NO-GO":
        errors.append("archived product verdict must remain NO-GO")

    fields = (
        "total_cases",
        "customer_visible_replies",
        "silent_cases",
        "answerable_cases",
        "answerable_replied",
        "qualifier_coverage_leaks",
    )
    values = {field: gate.get(field) for field in fields}
    if any(not isinstance(value, int) or value < 0 for value in values.values()):
        errors.append("all product gate counts must be non-negative integers")
        return
    if values["customer_visible_replies"] + values["silent_cases"] != values["total_cases"]:
        errors.append("visible and silent product cases must sum to total_cases")
    if values["answerable_replied"] > values["answerable_cases"]:
        errors.append("answerable_replied cannot exceed answerable_cases")
    if not CJK_PATTERN.search(str(gate.get("interpretation_zh", ""))):
        errors.append("product gate requires a Traditional Chinese interpretation")


def render_markdown(dataset: dict[str, Any], rows: list[dict[str, str]]) -> str:
    evidence_counts = Counter(row["evidence_level"] for row in rows)
    lines = [
        "# Gemini zh-TW semantic audit",
        "",
        f"Cases: {len(rows)} | Confirmed Gemini structured outputs: "
        f"{evidence_counts['confirmed_gemini_structured_output']} | End-to-end system outputs: "
        f"{evidence_counts['end_to_end_system_output']}",
        "",
        "| Case | Failure | Layer | Severity | Evidence |",
        "|---|---|---|:---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['id']} | {row['failure_type']} | {row['diagnosis_layer']} | "
            f"{row['severity']} | {row['evidence_level']} |"
        )

    lines.extend(
        [
            "",
            "## Iteration evidence",
            "",
            "| Stage | Valid | Exact frame | Core semantics |",
            "|---|---:|---:|---:|",
        ]
    )
    for item in dataset["iteration_evidence"]:
        total = item["total_runs"]
        lines.append(
            f"| {item['stage']} | {item['valid_runs']}/{total} | "
            f"{item['exact_frame_runs']}/{total} | {item['core_semantic_runs']}/{total} |"
        )

    gate = dataset["product_gate"]
    lines.extend(
        [
            "",
            f"Product gate: {gate['verdict']} | Visible: {gate['customer_visible_replies']}/"
            f"{gate['total_cases']} | Answerable replied: {gate['answerable_replied']}/"
            f"{gate['answerable_cases']} | Qualifier leaks: {gate['qualifier_coverage_leaks']}",
            "Dataset validation: PASS",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--json", action="store_true", help="Print validated rows as JSON")
    args = parser.parse_args()

    dataset = load_dataset(args.dataset)
    rows = validate_dataset(dataset)
    if args.json:
        print(json.dumps({"cases": rows, "product_gate": dataset["product_gate"]}, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(dataset, rows))


if __name__ == "__main__":
    main()
