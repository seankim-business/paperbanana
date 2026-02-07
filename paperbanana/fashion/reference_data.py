"""Sample fashion reference metadata for retrieval."""

from __future__ import annotations

from paperbanana.fashion.schemas import ReferenceItem

FASHION_REFERENCES: list[ReferenceItem] = [
    ReferenceItem(
        reference_id="fw23_trench_001",
        title="Paris trench editorial",
        silhouette="belted trench coat with strong shoulders",
        color_palette=["beige", "charcoal", "warm white"],
        photography_style="editorial street",
        mood="elegant, cinematic",
        image_url="https://example.com/reference/fw23_trench_001.jpg",
    ),
    ReferenceItem(
        reference_id="ss26_suit_002",
        title="Minimalist suiting lookbook",
        silhouette="relaxed tailored suit with wide-leg trousers",
        color_palette=["stone", "sand", "soft gray"],
        photography_style="clean studio",
        mood="calm, premium",
        image_url="https://example.com/reference/ss26_suit_002.jpg",
    ),
    ReferenceItem(
        reference_id="athleisure_003",
        title="Performance capsule",
        silhouette="oversized hoodie with tapered leggings",
        color_palette=["midnight", "ice blue"],
        photography_style="lifestyle gym",
        mood="energetic, sporty",
        image_url="https://example.com/reference/athleisure_003.jpg",
    ),
]
