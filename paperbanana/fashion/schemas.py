"""Pydantic schemas for the fashion-focused PaperBanana pipeline."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class FashionBrief(BaseModel):
    """Top-level fashion request provided by a user."""

    text: str = Field(..., description="User brief describing the fashion imagery.")
    season: str | None = Field(default=None, description="Optional season/year tag.")
    target_audience: str | None = Field(
        default=None, description="Optional target audience or market segment."
    )


class ReferenceItem(BaseModel):
    """Reference metadata retrieved for inspiration."""

    reference_id: str
    title: str
    silhouette: str
    color_palette: list[str]
    photography_style: str
    mood: str
    image_url: str


class RetrieverInput(BaseModel):
    brief: FashionBrief


class RetrieverOutput(BaseModel):
    summary: str
    references: list[ReferenceItem]


class ScenePrompt(BaseModel):
    """Structured prompt for one fashion scene."""

    scene_id: str
    description: str
    camera_angle: str
    pose: str
    framing: Literal["full_body", "half_body", "detail"]
    background: str
    lighting: str
    style_tokens: list[str] = Field(default_factory=list)
    negative_tokens: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class PlannerInput(BaseModel):
    brief: FashionBrief
    retrieval: RetrieverOutput


class PlannerOutput(BaseModel):
    scenes: list[ScenePrompt]


class StylistInput(BaseModel):
    scenes: list[ScenePrompt]
    brand_guidelines: str | None = None


class StylistOutput(BaseModel):
    scenes: list[ScenePrompt]


class VisualizerInput(BaseModel):
    scenes: list[ScenePrompt]
    base_assets: list[str] | None = None
    preset: Literal[
        "lookbook",
        "ecommerce_white_bg",
        "lifestyle",
        "virtual_tryon",
    ] = "lookbook"


class GeneratedImage(BaseModel):
    scene_id: str
    image_uri: str
    prompt: ScenePrompt
    metadata: dict[str, Any] = Field(default_factory=dict)


class VisualizerOutput(BaseModel):
    images: list[GeneratedImage]


class CriticInput(BaseModel):
    brief: FashionBrief
    visualizer_output: VisualizerOutput


class CriticFeedback(BaseModel):
    scene_id: str
    score: float = Field(..., ge=0, le=1)
    issues: list[str]
    suggestions: list[str]


class CriticOutput(BaseModel):
    overall_score: float = Field(..., ge=0, le=1)
    feedback: list[CriticFeedback]
    approved_images: list[GeneratedImage]
    retry_scenes: list[ScenePrompt] = Field(default_factory=list)


class FashionPipelineConfig(BaseModel):
    """Configuration for the fashion pipeline."""

    brand_guidelines: str | None = None
    preset: Literal[
        "lookbook",
        "ecommerce_white_bg",
        "lifestyle",
        "virtual_tryon",
    ] = "lookbook"
    max_refinement_rounds: int = 2
    output_dir: str = "outputs/fashion"


class FashionPipelineResult(BaseModel):
    retrieval: RetrieverOutput
    plan: PlannerOutput
    styled: StylistOutput
    visuals: VisualizerOutput
    critique: CriticOutput
