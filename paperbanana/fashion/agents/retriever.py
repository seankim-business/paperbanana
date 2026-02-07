"""Retriever agent for fashion references."""

from __future__ import annotations

from dataclasses import dataclass

from paperbanana.fashion.reference_data import FASHION_REFERENCES
from paperbanana.fashion.schemas import FashionBrief, RetrieverInput, RetrieverOutput


@dataclass
class RetrieverAgent:
    """Select relevant fashion references based on the brief."""

    max_results: int = 3

    def run(self, brief: FashionBrief) -> RetrieverOutput:
        scored = []
        lower_text = brief.text.lower()
        for ref in FASHION_REFERENCES:
            score = 0
            for token in ref.color_palette + [ref.silhouette, ref.photography_style, ref.mood]:
                if token.lower() in lower_text:
                    score += 1
            scored.append((score, ref))

        scored.sort(key=lambda item: item[0], reverse=True)
        selected = [ref for score, ref in scored[: self.max_results]]
        summary_lines = [
            f"{ref.title}: {ref.silhouette}, palette {', '.join(ref.color_palette)}, style {ref.photography_style}."
            for ref in selected
        ]
        summary = " ".join(summary_lines) if summary_lines else "No references matched; use generic editorial look."
        return RetrieverOutput(summary=summary, references=selected)

    def run_from_input(self, data: RetrieverInput) -> RetrieverOutput:
        return self.run(data.brief)
