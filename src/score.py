#!/usr/bin/env python3
"""Validate and summarize both synthetic zh-TW LLM evaluation tracks."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CAFE_DATASET = ROOT / "data" / "evaluations.json"
PERSONALIZATION_DATASET = ROOT / "data" / "personalization_sxs.json"
DEFAULT_DATASET = CAFE_DATASET


def load_dataset(path: Path = DEFAULT_DATASET) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def weighted_score(scores: dict[str, int], weights: dict[str, int]) -> float:
    return round(sum((scores[name] / 5) * weight for name, weight in weights.items()), 1)


def choose_winner(score_a: float, score_b: float) -> str:
    if score_a > score_b:
        return "A"
    if score_b > score_a:
        return "B"
    return "TIE"


def validate_dataset(dataset: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[str] = []
    metadata = dataset.get("metadata", {})
    weights = dataset.get("weights", {})
    cases = dataset.get("cases", [])
    is_personalization = "primary_dimensions" in metadata

    if metadata.get("synthetic") is not True:
        errors.append("metadata.synthetic must be true")
    if sum(weights.values()) != 100:
        errors.append("rubric weights must sum to 100")
    if len(cases) < 10:
        errors.append("benchmark must contain at least 10 cases")
    if is_personalization:
        primary_dimensions = set(metadata.get("primary_dimensions", []))
        required_primary = {"grounding", "integration", "helpfulness"}
        if primary_dimensions != required_primary:
            errors.append("personalization primary dimensions must be grounding, integration, and helpfulness")
        if not required_primary.issubset(weights):
            errors.append("personalization weights must include every primary dimension")
        hygiene = metadata.get("data_hygiene", {})
        if hygiene.get("source_data") != "synthetic_and_anonymized":
            errors.append("personalization source data must be synthetic and anonymized")
        if hygiene.get("evaluation_conversations") != "delete_after_scoring":
            errors.append("personalization conversations must be deleted after scoring")

    seen_ids: set[str] = set()
    rows: list[dict[str, Any]] = []

    for case in cases:
        case_id = case.get("id", "<missing>")
        if case_id in seen_ids:
            errors.append(f"duplicate case id: {case_id}")
        seen_ids.add(case_id)

        if is_personalization:
            validate_personalization_case(case, errors)

        candidate_scores: dict[str, float] = {}
        for candidate in ("A", "B"):
            scores = case.get("scores", {}).get(candidate, {})
            if set(scores) != set(weights):
                errors.append(f"{case_id}/{candidate}: score dimensions do not match weights")
                continue
            for dimension, value in scores.items():
                if not isinstance(value, int) or not 1 <= value <= 5:
                    errors.append(f"{case_id}/{candidate}/{dimension}: score must be an integer from 1 to 5")
            candidate_scores[candidate] = weighted_score(scores, weights)

        if set(candidate_scores) == {"A", "B"}:
            computed_winner = choose_winner(candidate_scores["A"], candidate_scores["B"])
            expected_winner = case.get("expected_winner")
            if computed_winner != expected_winner:
                errors.append(
                    f"{case_id}: expected {expected_winner}, computed {computed_winner} "
                    f"({candidate_scores['A']} vs {candidate_scores['B']})"
                )
            rows.append(
                {
                    "id": case_id,
                    "category": case.get("category"),
                    "score_a": candidate_scores["A"],
                    "score_b": candidate_scores["B"],
                    "winner": computed_winner,
                }
            )

    if errors:
        raise ValueError("Dataset validation failed:\n- " + "\n- ".join(errors))
    return rows


def validate_personalization_case(case: dict[str, Any], errors: list[str]) -> None:
    """Validate turn, source, rationale, Debug Info, and cleanup evidence."""

    case_id = case.get("id", "<missing>")
    sources = case.get("sources", [])
    conversation = case.get("conversation", [])
    source_ids = {source.get("source_id") for source in sources}
    turn_ids = {turn.get("turn_id") for turn in conversation}

    if not sources:
        errors.append(f"{case_id}: source bundle is required")
    if not 1 <= len(conversation) <= 5:
        errors.append(f"{case_id}: conversation must contain 1 to 5 turns")
    if None in source_ids or len(source_ids) != len(sources):
        errors.append(f"{case_id}: source IDs must be present and unique")
    if None in turn_ids or len(turn_ids) != len(conversation):
        errors.append(f"{case_id}: turn IDs must be present and unique")

    turn_references = set(case.get("turn_references", []))
    source_references = set(case.get("source_references", []))
    if not turn_references or not turn_references.issubset(turn_ids):
        errors.append(f"{case_id}: rationale turn references must resolve to conversation turns")
    if not source_references or not source_references.issubset(source_ids):
        errors.append(f"{case_id}: rationale source references must resolve to source bundle")

    rationale = case.get("rationale_zh", "")
    if len(rationale) < 80:
        errors.append(f"{case_id}: rationale must contain at least 80 zh-TW characters")
    for reference in turn_references | source_references:
        if reference not in rationale:
            errors.append(f"{case_id}: rationale does not explicitly cite {reference}")

    if not case.get("feedback_zh"):
        errors.append(f"{case_id}: constructive feedback is required")
    if case.get("cleanup_required") is not True:
        errors.append(f"{case_id}: cleanup_required must be true")

    debug_check = case.get("debug_check", {})
    for candidate in ("A", "B"):
        debug = debug_check.get(candidate, {})
        verified = set(debug.get("verified_sources", []))
        claimed = set(debug.get("claimed_sources", []))
        issues = debug.get("issues", [])
        if not verified.issubset(source_ids):
            errors.append(f"{case_id}/{candidate}: verified Debug Info source does not exist")
        if not claimed.issubset(source_ids) and not issues:
            errors.append(f"{case_id}/{candidate}: missing claimed source must be recorded as an issue")


def build_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    winners = Counter(row["winner"] for row in rows)
    return {
        "cases": len(rows),
        "a_wins": winners["A"],
        "b_wins": winners["B"],
        "ties": winners["TIE"],
        "average_a": round(sum(row["score_a"] for row in rows) / len(rows), 1),
        "average_b": round(sum(row["score_b"] for row in rows) / len(rows), 1),
    }


def render_markdown(rows: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    lines = [
        "| Case | Category | A | B | Winner |",
        "|---|---|---:|---:|:---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['id']} | {row['category']} | {row['score_a']:.1f} | "
            f"{row['score_b']:.1f} | {row['winner']} |"
        )
    lines.extend(
        [
            "",
            f"Cases: {summary['cases']} | A wins: {summary['a_wins']} | "
            f"B wins: {summary['b_wins']} | Ties: {summary['ties']}",
            "Dataset validation: PASS",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, help="Validate one custom dataset instead of a built-in track")
    parser.add_argument(
        "--track",
        choices=("all", "cafe", "personalization"),
        default="all",
        help="Choose a built-in evaluation track (default: all)",
    )
    parser.add_argument("--json", action="store_true", help="Print summary as JSON")
    args = parser.parse_args()

    if args.dataset:
        datasets = [("custom", args.dataset)]
    elif args.track == "cafe":
        datasets = [("cafe-grounding", CAFE_DATASET)]
    elif args.track == "personalization":
        datasets = [("personalization-sxs", PERSONALIZATION_DATASET)]
    else:
        datasets = [
            ("cafe-grounding", CAFE_DATASET),
            ("personalization-sxs", PERSONALIZATION_DATASET),
        ]

    results: dict[str, Any] = {}
    rendered: list[str] = []
    for label, path in datasets:
        rows = validate_dataset(load_dataset(path))
        summary = build_summary(rows)
        results[label] = {"summary": summary, "rows": rows}
        rendered.extend([f"## {label}", "", render_markdown(rows, summary), ""])

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print("\n".join(rendered).rstrip())


if __name__ == "__main__":
    main()
