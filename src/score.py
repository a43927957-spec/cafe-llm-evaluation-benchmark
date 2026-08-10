#!/usr/bin/env python3
"""Validate and summarize the synthetic café LLM evaluation dataset."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = ROOT / "data" / "evaluations.json"


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
    weights = dataset.get("weights", {})
    cases = dataset.get("cases", [])

    if dataset.get("metadata", {}).get("synthetic") is not True:
        errors.append("metadata.synthetic must be true")
    if sum(weights.values()) != 100:
        errors.append("rubric weights must sum to 100")
    if len(cases) < 10:
        errors.append("benchmark must contain at least 10 cases")

    seen_ids: set[str] = set()
    rows: list[dict[str, Any]] = []

    for case in cases:
        case_id = case.get("id", "<missing>")
        if case_id in seen_ids:
            errors.append(f"duplicate case id: {case_id}")
        seen_ids.add(case_id)

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
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--json", action="store_true", help="Print summary as JSON")
    args = parser.parse_args()

    rows = validate_dataset(load_dataset(args.dataset))
    summary = build_summary(rows)
    if args.json:
        print(json.dumps({"summary": summary, "rows": rows}, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(rows, summary))


if __name__ == "__main__":
    main()
