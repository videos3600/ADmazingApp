"""
Test met echt materiaal (John's eigen upload) in plaats van placeholder-clips.
Geen sector-heuristiek nodig (het is geen restaurant/contractor) — EDL hier
direct opgebouwd, exact zoals de AI-laag dat straks voor een willekeurige
sector zou doen.
"""

from pathlib import Path

from edl.schema import EDL, ClipRef, TextCue, MusicCue
from render.pipeline import render_edl, edl_to_json

ROOT = Path(__file__).resolve().parent
ASSETS_DIR = ROOT / "assets" / "client_test"
SAMPLES_DIR = ROOT / "samples"

edl = EDL(
    template="Papercut",
    format="9:16",
    clips=[
        ClipRef(start=0.0, end=2.0, source="back_workout.mp4", tag="grind"),
        ClipRef(start=2.0, end=4.2, source="bicep_curl.mp4", tag="action"),
        ClipRef(start=4.2, end=6.8, source="standing_pose.mp4", tag="hero"),
    ],
    text_cues=[
        TextCue(content="Discipline builds results.", start=0.5, end=6.2, kind="headline"),
        TextCue(content="Train today", start=5.2, end=6.8, kind="cta"),
    ],
    music=MusicCue(style="upbeat tropical / urban", bpm=105, file="../music_placeholder.m4a"),
    logo="../logo.png",
    business_name="MisterMuscleMan (test)",
)

SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
edl_to_json(edl, SAMPLES_DIR / "edl_real_footage.json")
print(f"EDL: {edl.duration:.1f}s, {len(edl.clips)} clips")

output_path = render_edl(edl, assets_dir=ASSETS_DIR, output_path=SAMPLES_DIR / "output_real_footage.mp4")
print(f"Rendered: {output_path}")
