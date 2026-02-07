"""Orchestrator for the fashion multi-agent pipeline."""

from __future__ import annotations

from paperbanana.fashion.agents import (
    CriticAgent,
    PlannerAgent,
    RetrieverAgent,
    StylistAgent,
    VisualizerAgent,
)
from paperbanana.fashion.clients.nano_banana_client import NanoBananaClient
from paperbanana.fashion.schemas import (
    FashionBrief,
    FashionPipelineConfig,
    FashionPipelineResult,
    VisualizerOutput,
)


def run_fashion_pipeline(
    brief: FashionBrief | str,
    assets: list[str] | None = None,
    config: FashionPipelineConfig | None = None,
    client: NanoBananaClient | None = None,
) -> FashionPipelineResult:
    """Run the full fashion pipeline end-to-end."""

    config = config or FashionPipelineConfig()
    if isinstance(brief, str):
        brief = FashionBrief(text=brief)

    retriever = RetrieverAgent()
    planner = PlannerAgent()
    stylist = StylistAgent()
    client = client or NanoBananaClient()
    visualizer = VisualizerAgent(client=client, output_dir=config.output_dir)
    critic = CriticAgent()

    retrieval = retriever.run(brief)
    plan = planner.run(brief, retrieval.summary)
    styled = stylist.run(plan.scenes, config.brand_guidelines)
    visuals = visualizer.run(styled.scenes, assets, config.preset)
    critique = critic.run(brief, visuals)

    for _ in range(config.max_refinement_rounds):
        if not critique.retry_scenes:
            break
        refined_visuals = visualizer.run(critique.retry_scenes, assets, config.preset)
        visuals = _merge_visuals(visuals, refined_visuals)
        critique = critic.run(brief, visuals)

    return FashionPipelineResult(
        retrieval=retrieval,
        plan=plan,
        styled=styled,
        visuals=visuals,
        critique=critique,
    )


def _merge_visuals(
    current: VisualizerOutput,
    refined: VisualizerOutput,
) -> VisualizerOutput:
    image_map = {image.scene_id: image for image in current.images}
    for image in refined.images:
        image_map[image.scene_id] = image
    return VisualizerOutput(images=list(image_map.values()))
