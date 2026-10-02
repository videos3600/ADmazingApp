"""
End-to-end fase-1 demo: build the EDL from the concept doc's worked example
(Suriname Kitchen restaurant ad) and render it to a real MP4 with the
FFmpeg-only render engine.

Run:
    python3 scripts/make_demo_assets.py   # once, generates placeholder assets
    python3 main.py                       # builds the EDL and renders samples/output.mp4
"""

from __future__ import annotations

from pathlib import Path

from edl.generator import build_edl
from render.pipeline import render_edl, edl_to_json

ROOT = Path(__file__).resolve().parent
ASSETS_DIR = ROOT / "assets"
SAMPLES_DIR = ROOT / "samples"


def main() -> None:
    edl = build_edl(
        sector="restaurant",
        business_name="Suriname Kitchen",
        headline="Surinaamse smaken in hartje Almere",
        cta="Bestel vandaag",
        tagged_sources={
            "exterior": "exterior.mp4",
            "owner": "owner.mp4",
            "food-closeup": "food-closeup.mp4",
            "customer": "customer.mp4",
        },
        music_style="upbeat tropical / urban",
        music_bpm=105,
        music_file="music_placeholder.m4a",
        logo="logo.png",
        output_format="9:16",
    )

    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    edl_to_json(edl, SAMPLES_DIR / "edl_example.json")
    print(f"EDL written to {SAMPLES_DIR / 'edl_example.json'} ({edl.duration:.1f}s, {len(edl.clips)} clips)")

    output_path = render_edl(edl, assets_dir=ASSETS_DIR, output_path=SAMPLES_DIR / "output.mp4")
    print(f"Rendered ad: {output_path}")


if __name__ == "__main__":
    main()
