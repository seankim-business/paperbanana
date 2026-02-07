"""Generate virtual try-on shots using base garment images."""

from __future__ import annotations

from paperbanana.fashion.orchestrator import run_fashion_pipeline
from paperbanana.fashion.schemas import FashionPipelineConfig


def main() -> None:
    brief = (
        "Studio ecommerce shots for a cropped denim jacket, "
        "clean white background, accurate texture"
    )
    base_assets = [
        "assets/fashion/base_top.png",
        "assets/fashion/base_bottom.png",
    ]
    config = FashionPipelineConfig(
        brand_guidelines="ecommerce-ready, true-to-color, balanced lighting",
        preset="virtual_tryon",
    )

    result = run_fashion_pipeline(brief=brief, assets=base_assets, config=config)

    print("Virtual try-on outputs:")
    for image in result.visuals.images:
        print(f"- {image.scene_id}: {image.image_uri}")


if __name__ == "__main__":
    main()
