"""Nano-Banana-Pro client wrapper (mockable)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from paperbanana.fashion.clients.vlm_client import VLMClient


@dataclass
class NanoBananaCredentials:
    api_key: str | None = None
    base_url: str | None = None


class NanoBananaClient(VLMClient):
    """Minimal Nano-Banana-Pro client wrapper.

    This implementation is intentionally mock-friendly. Replace the
    `generate_text` and `generate_image` methods with real API calls.
    """

    def __init__(self, credentials: NanoBananaCredentials | None = None) -> None:
        self.credentials = credentials or NanoBananaCredentials()

    def generate_text(self, prompt: str) -> str:
        return f"[NanoBananaMock:text] {prompt[:160]}"

    def generate_image(self, prompt: str, **kwargs: Any) -> str:
        preset = kwargs.get("preset", "lookbook")
        mode = kwargs.get("mode", "text_to_image")
        return f"mock://nano-banana/{preset}/{mode}/{hash(prompt) % 10000}"

    def text_to_image(self, prompt: str, preset: str = "lookbook") -> str:
        return self.generate_image(prompt, preset=preset, mode="text_to_image")

    def image_edit(
        self,
        prompt: str,
        base_image: str,
        preset: str = "virtual_tryon",
    ) -> str:
        return self.generate_image(
            prompt,
            preset=preset,
            mode="image_edit",
            base_image=base_image,
        )
