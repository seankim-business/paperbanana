"""Abstract VLM client interface for fashion generation."""

from __future__ import annotations

from abc import ABC, abstractmethod


class VLMClient(ABC):
    """Abstract VLM/LLM client."""

    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        """Generate text for planning or critique."""
        raise NotImplementedError

    @abstractmethod
    def generate_image(self, prompt: str, **kwargs: object) -> str:
        """Generate an image and return a URI."""
        raise NotImplementedError


class MockVLMClient(VLMClient):
    """Mock client for local testing."""

    def generate_text(self, prompt: str) -> str:
        return f"[MockVLM] {prompt[:160]}"

    def generate_image(self, prompt: str, **kwargs: object) -> str:
        return f"mock://image/{hash(prompt) % 10000}"
