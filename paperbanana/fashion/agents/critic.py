"""Critic agent for quality assessment."""

from __future__ import annotations

from dataclasses import dataclass

from paperbanana.fashion.schemas import (
    CriticFeedback,
    CriticInput,
    CriticOutput,
    FashionBrief,
    ScenePrompt,
    VisualizerOutput,
)


@dataclass
class CriticAgent:
    """Assess fidelity and propose refinements."""

    score_threshold: float = 0.72

    def _score_scene(self, brief: FashionBrief, scene: ScenePrompt) -> CriticFeedback:
        brief_terms = {term.strip(".,") for term in brief.text.lower().split()}
        scene_terms = {term.strip(".,") for term in scene.description.lower().split()}
        overlap = brief_terms & scene_terms
        score = min(1.0, 0.6 + 0.02 * len(overlap))
        issues = []
        suggestions = []
        if score < self.score_threshold:
            issues.append("Prompt may not fully reflect the brief keywords.")
            suggestions.append("Reinforce garment type and color palette in the prompt.")
        return CriticFeedback(
            scene_id=scene.scene_id,
            score=round(score, 2),
            issues=issues,
            suggestions=suggestions,
        )

    def run(self, brief: FashionBrief, output: VisualizerOutput) -> CriticOutput:
        feedback: list[CriticFeedback] = []
        retry_scenes: list[ScenePrompt] = []

        for image in output.images:
            scene_feedback = self._score_scene(brief, image.prompt)
            feedback.append(scene_feedback)
            if scene_feedback.score < self.score_threshold:
                scene = image.prompt
                scene.style_tokens = [*scene.style_tokens, "emphasize garment details", "accurate color"]
                retry_scenes.append(scene)

        overall_score = sum(item.score for item in feedback) / len(feedback) if feedback else 0.0
        approved = [image for image, item in zip(output.images, feedback) if item.score >= self.score_threshold]
        return CriticOutput(
            overall_score=round(overall_score, 2),
            feedback=feedback,
            approved_images=approved,
            retry_scenes=retry_scenes,
        )

    def run_from_input(self, data: CriticInput) -> CriticOutput:
        return self.run(data.brief, data.visualizer_output)
