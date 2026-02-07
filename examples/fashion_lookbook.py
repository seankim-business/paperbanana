"""Generate a 4-shot fashion lookbook from a text brief."""

from __future__ import annotations

from paperbanana.fashion.orchestrator import run_fashion_pipeline
from paperbanana.fashion.schemas import FashionPipelineConfig


def main() -> None:
    brief = (
        "2026 S/S Paris runway-inspired trench coat lookbook, "
        "beige palette, elegant editorial mood"
    )
    config = FashionPipelineConfig(
        brand_guidelines="minimal, clean studio lighting, slightly desaturated, high-end editorial look",
        preset="lookbook",
    )

    result = run_fashion_pipeline(brief=brief, assets=None, config=config)

    print("Retrieval summary:\n", result.retrieval.summary)
    print("Generated images:")
    for image in result.visuals.images:
        print(f"- {image.scene_id}: {image.image_uri} ({image.metadata.get('preset')})")


if __name__ == "__main__":
    main()
