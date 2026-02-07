# PaperBanana Fashion Fork

An agentic, PaperBanana-style pipeline for **fashion design image generation**. This fork adapts the original 5-agent architecture (Retriever → Planner → Stylist → Visualizer → Critic) to produce lookbooks, ecommerce shots, and virtual try-on imagery. The code is modular so you can swap out the underlying VLM/Image model (e.g., Nano‑Banana‑Pro, Gemini, or other providers).

> **Note**: The Nano‑Banana‑Pro client in this repo is **mock-only** for now. Plug in real endpoints/keys later by editing the client implementation.

---

## Architecture

```
User Brief
   │
   ▼
Retriever ──► Planner ──► Stylist ──► Visualizer ──► Critic
   ▲                                               │
   └────────────────── refinement loop (1–2x) ─────┘
```

### Agent Responsibilities (Fashion Domain)

1. **Retriever**: Pulls relevant fashion references (silhouettes, palettes, photography style).
2. **Planner**: Converts the brief into structured scene prompts (camera angle, pose, framing).
3. **Stylist**: Injects consistent brand or campaign style tokens into prompts.
4. **Visualizer**: Calls Nano‑Banana‑Pro (or another generator) to create images.
5. **Critic**: Scores fidelity and suggests prompt refinements for limited retries.

---

## Installation

```bash
pip install paperbanana
```

Or for local development:

```bash
git clone https://github.com/llmsresearch/paperbanana.git
cd paperbanana
pip install -e "[dev]"
```

---

## Quickstart

### Lookbook (text-only)

```bash
python examples/fashion_lookbook.py
```

### Virtual Try-On (image + text)

```bash
python examples/virtual_tryon.py
```

---

## JSON Schemas (per agent)

### Retriever

**Input**
```json
{
  "brief": {
    "text": "2026 S/S Paris editorial trench coat",
    "season": "2026 S/S",
    "target_audience": "luxury"
  }
}
```

**Output**
```json
{
  "summary": "Paris trench editorial: belted trench coat...",
  "references": [
    {
      "reference_id": "fw23_trench_001",
      "title": "Paris trench editorial",
      "silhouette": "belted trench coat with strong shoulders",
      "color_palette": ["beige", "charcoal"],
      "photography_style": "editorial street",
      "mood": "elegant, cinematic",
      "image_url": "https://example.com/reference/fw23_trench_001.jpg"
    }
  ]
}
```

### Planner

**Input**
```json
{
  "brief": {"text": "2026 S/S Paris editorial trench coat"},
  "retrieval": {"summary": "Paris trench editorial...", "references": []}
}
```

**Output**
```json
{
  "scenes": [
    {
      "scene_id": "front",
      "description": "Front-facing hero shot...",
      "camera_angle": "eye level",
      "pose": "neutral stance",
      "framing": "full_body",
      "background": "studio seamless",
      "lighting": "soft key light",
      "style_tokens": [],
      "negative_tokens": []
    }
  ]
}
```

### Stylist

**Input**
```json
{
  "scenes": [{"scene_id": "front", "description": "..."}],
  "brand_guidelines": "minimal, clean studio lighting"
}
```

**Output**
```json
{
  "scenes": [
    {
      "scene_id": "front",
      "style_tokens": ["minimal", "clean studio lighting"],
      "negative_tokens": ["blurry", "low quality"]
    }
  ]
}
```

### Visualizer

**Input**
```json
{
  "scenes": [{"scene_id": "front", "description": "..."}],
  "base_assets": ["assets/base_tshirt.png"],
  "preset": "virtual_tryon"
}
```

**Output**
```json
{
  "images": [
    {
      "scene_id": "front",
      "image_uri": "outputs/fashion/front_1.png",
      "metadata": {"preset": "virtual_tryon"}
    }
  ]
}
```

### Critic

**Input**
```json
{
  "brief": {"text": "2026 S/S Paris editorial trench coat"},
  "visualizer_output": {"images": [{"scene_id": "front"}]}
}
```

**Output**
```json
{
  "overall_score": 0.86,
  "feedback": [
    {
      "scene_id": "front",
      "score": 0.82,
      "issues": [],
      "suggestions": []
    }
  ],
  "approved_images": [{"scene_id": "front"}],
  "retry_scenes": []
}
```

---

## Swapping Nano‑Banana‑Pro or Other Models

The abstraction layer lives in:

- `paperbanana/fashion/clients/vlm_client.py` → base VLM interface
- `paperbanana/fashion/clients/nano_banana_client.py` → Nano‑Banana‑Pro mock

To plug in a real API:

1. Update `NanoBananaClient.generate_text` / `generate_image`.
2. Pass credentials via `NanoBananaCredentials`.
3. Keep the interface methods the same so the pipeline stays untouched.

---

## Extending to Other Domains

The fashion-specific logic is isolated to the agent implementations and reference data. To adapt this to interior design or product rendering, replace:

- `paperbanana/fashion/reference_data.py`
- `paperbanana/fashion/agents/*`

while keeping the `run_fashion_pipeline` orchestrator pattern intact.
