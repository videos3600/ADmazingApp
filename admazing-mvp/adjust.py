"""
Simulates a click on one of the Result screen's quick-adjust buttons:
loads the last rendered EDL, applies the requested adjustment, saves the
new EDL and re-renders it. This is exactly the loop the real Result
screen will trigger server-side once it exists — see edl/adjustments.py
for what each button actually changes.

Run:
    python3 adjust.py more_energetic
    python3 adjust.py make_cleaner
    python3 adjust.py change_music
    python3 adjust.py rewrite_text

Each run reads samples/edl_example.json (the current state), writes
samples/edl_<adjustment>.json and samples/output_<adjustment>.mp4, and
leaves the original untouched so you can compare before/after.
"""

from __future__ import annotations

import sys
from pathlib import Path

from edl.schema import EDL
from edl.adjustments import ADJUSTMENTS
from render.pipeline import render_edl, edl_to_json

ROOT = Path(__file__).resolve().parent
ASSETS_DIR = ROOT / "assets"
SAMPLES_DIR = ROOT / "samples"
CURRENT_EDL_PATH = SAMPLES_DIR / "edl_example.json"


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in ADJUSTMENTS:
        print(f"Usage: python3 adjust.py <{'|'.join(ADJUSTMENTS)}>")
        sys.exit(1)

    name = sys.argv[1]
    adjustment_fn = ADJUSTMENTS[name]

    if not CURRENT_EDL_PATH.exists():
        print(f"No current EDL at {CURRENT_EDL_PATH} — run main.py first.")
        sys.exit(1)

    import json
    current_edl = EDL.from_dict(json.loads(CURRENT_EDL_PATH.read_text()))

    print(f"Applying '{name}' to the current EDL ({current_edl.duration:.1f}s)...")
    adjusted_edl = adjustment_fn(current_edl)
    print(f"  -> new duration: {adjusted_edl.duration:.1f}s, text_style={adjusted_edl.text_style}, "
          f"music={adjusted_edl.music.file if adjusted_edl.music else None}")

    edl_json_path = SAMPLES_DIR / f"edl_{name}.json"
    edl_to_json(adjusted_edl, edl_json_path)

    output_path = render_edl(adjusted_edl, assets_dir=ASSETS_DIR, output_path=SAMPLES_DIR / f"output_{name}.mp4")
    print(f"Rendered: {output_path}")


if __name__ == "__main__":
    main()
