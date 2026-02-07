"""Stylist agent injects brand and campaign styling."""

from __future__ import annotations

from dataclasses import dataclass

from paperbanana.fashion.schemas import ScenePrompt, StylistInput, StylistOutput


@dataclass
class StylistAgent:
    """Apply consistent style tokens across prompts."""

    default_style: str = "minimal, clean studio lighting, slightly desaturated, high-end editorial look"

    def run(self, scenes: list[ScenePrompt], brand_guidelines: str | None = None) -> StylistOutput:
        style_note = brand_guidelines or self.default_style
        for scene in scenes:
            scene.style_tokens = [*scene.style_tokens, *style_note.split(", ")]
            scene.negative_tokens = list({*scene.negative_tokens, "blurry", "low quality"})
        return StylistOutput(scenes=scenes)

    def run_from_input(self, data: StylistInput) -> StylistOutput:
        return self.run(data.scenes, data.brand_guidelines)
