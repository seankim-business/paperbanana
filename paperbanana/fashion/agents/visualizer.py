"""Visualizer agent to call Nano-Banana-Pro (mock) for images."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from paperbanana.fashion.clients.nano_banana_client import NanoBananaClient
from paperbanana.fashion.schemas import (
    GeneratedImage,
    ScenePrompt,
    VisualizerInput,
    VisualizerOutput,
)


@dataclass
class VisualizerAgent:
    """Generate fashion images via Nano-Banana-Pro."""

    client: NanoBananaClient
    output_dir: str = "outputs/fashion"

    def _serialize_prompt(self, scene: ScenePrompt) -> str:
        style = ", ".join(scene.style_tokens)
        negative = ", ".join(scene.negative_tokens)
        return (
            f"{scene.description}\n"
            f"Camera: {scene.camera_angle}; Pose: {scene.pose}; Framing: {scene.framing}.\n"
            f"Background: {scene.background}; Lighting: {scene.lighting}.\n"
            f"Style: {style}.\n"
            f"Avoid: {negative}."
        )

    def run(
        self,
        scenes: list[ScenePrompt],
        base_assets: list[str] | None = None,
        preset: str = "lookbook",
    ) -> VisualizerOutput:
        output_path = Path(self.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        images: list[GeneratedImage] = []
        base_assets = base_assets or []

        for idx, scene in enumerate(scenes, start=1):
            prompt = self._serialize_prompt(scene)
            if base_assets:
                image_uri = self.client.image_edit(prompt, base_assets[0], preset=preset)
            else:
                image_uri = self.client.text_to_image(prompt, preset=preset)

            file_name = output_path / f"{scene.scene_id}_{idx}.png"
            file_name.write_text(f"Mock image for {scene.scene_id}: {image_uri}")

            images.append(
                GeneratedImage(
                    scene_id=scene.scene_id,
                    image_uri=str(file_name),
                    prompt=scene,
                    metadata={"preset": preset, "source_uri": image_uri},
                )
            )

        return VisualizerOutput(images=images)

    def run_from_input(self, data: VisualizerInput) -> VisualizerOutput:
        return self.run(data.scenes, data.base_assets, data.preset)
