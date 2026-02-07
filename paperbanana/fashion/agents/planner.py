"""Planner agent for fashion scenes."""

from __future__ import annotations

from dataclasses import dataclass

from paperbanana.fashion.schemas import (
    FashionBrief,
    PlannerInput,
    PlannerOutput,
    ScenePrompt,
)


@dataclass
class PlannerAgent:
    """Convert a brief and references into scene prompts."""

    def run(self, brief: FashionBrief, retrieval_summary: str) -> PlannerOutput:
        base_description = f"{brief.text}. Reference cues: {retrieval_summary}"
        scenes = [
            ScenePrompt(
                scene_id="front",
                description=f"Front-facing hero shot. {base_description}",
                camera_angle="eye level",
                pose="neutral stance, hands relaxed",
                framing="full_body",
                background="studio seamless or urban street",
                lighting="soft key light with gentle fill",
                metadata={"shot_type": "front"},
            ),
            ScenePrompt(
                scene_id="back",
                description=f"Back view showing garment structure. {base_description}",
                camera_angle="eye level",
                pose="slight turn to show back silhouette",
                framing="full_body",
                background="studio seamless",
                lighting="even diffuse lighting",
                metadata={"shot_type": "back"},
            ),
            ScenePrompt(
                scene_id="half",
                description=f"Half-body editorial crop. {base_description}",
                camera_angle="slight high angle",
                pose="soft movement, editorial gaze",
                framing="half_body",
                background="minimalist interior",
                lighting="directional window light",
                metadata={"shot_type": "half"},
            ),
            ScenePrompt(
                scene_id="detail",
                description=f"Detail shot of fabric and trims. {base_description}",
                camera_angle="macro close-up",
                pose="focus on textile texture",
                framing="detail",
                background="neutral",
                lighting="specular highlights for texture",
                metadata={"shot_type": "detail"},
            ),
        ]
        return PlannerOutput(scenes=scenes)

    def run_from_input(self, data: PlannerInput) -> PlannerOutput:
        return self.run(data.brief, data.retrieval.summary)
