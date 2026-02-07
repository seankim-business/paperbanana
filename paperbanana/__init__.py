"""PaperBanana: Agentic framework for multimodal design generation."""

__version__ = "0.1.0"

from paperbanana.core.pipeline import PaperBananaPipeline
from paperbanana.core.types import DiagramType, GenerationInput, GenerationOutput
from paperbanana.fashion.orchestrator import run_fashion_pipeline

__all__ = [
    "PaperBananaPipeline",
    "DiagramType",
    "GenerationInput",
    "GenerationOutput",
    "run_fashion_pipeline",
]
