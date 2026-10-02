"""
Generates placeholder assets so the pipeline can be run end to end without
a real client upload. NONE of this is meant to ship: the "clips" are solid-
colour cards with a label (no real footage, no license concerns), the
"logo" is a generated placeholder mark, and the "music" is a plain
synthesised tone loop — not a real track. Swap all three for a client's
real upload + a licensed music bed once the funnel exists.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
FONT_FILE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# (filename, label, hex colour) — stand-ins for exterior / owner / food-closeup / customer
CLIPS = [
    ("exterior.mp4", "EXTERIOR", "0x2B3A55"),
    ("owner.mp4", "OWNER", "0x3E5C43"),
    ("food-closeup.mp4", "FOOD CLOSE-UP", "0x8C3B2E"),
    ("customer.mp4", "CUSTOMER", "0x4A3B6B"),
]

CLIP_SECONDS = 3  # longer than any single EDL segment needs; renderer trims it
RESOLUTION = "1080x1920"


def make_placeholder_clips() -> None:
    for filename, label, color in CLIPS:
        out_path = ASSETS_DIR / filename
        drawtext = (
            f"drawtext=fontfile={FONT_FILE}:text='{label}':"
            "fontcolor=white@0.85:fontsize=64:"
            "x=(w-text_w)/2:y=(h-text_h)/2"
        )
        subprocess.run(
            [
                "ffmpeg", "-y",
                "-f", "lavfi",
                "-i", f"color=c={color}:s={RESOLUTION}:d={CLIP_SECONDS}:r=30",
                "-vf", drawtext,
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                str(out_path),
            ],
            check=True,
            capture_output=True,
        )
        print(f"  wrote {out_path.name}")


def make_placeholder_logo() -> None:
    out_path = ASSETS_DIR / "logo.png"
    size = 480
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([40, 40, size - 40, size - 40], fill=(255, 90, 46, 235))
    font = ImageFont.truetype(FONT_FILE, 150)
    text = "A"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((size - tw) / 2 - bbox[0], (size - th) / 2 - bbox[1]), text, font=font, fill=(10, 10, 13, 255))
    img.save(out_path)
    print(f"  wrote {out_path.name}")


# (filename, [frequencies], label) — two distinct placeholder beds so
# "Change music" has something real to swap to. Neither is a real track;
# both are just enough signal to prove the mix/duck/fade steps.
MUSIC_BEDS = [
    ("music_placeholder.m4a", [220, 330], "upbeat tropical / urban"),
    ("music_placeholder_alt.m4a", [147, 196, 294], "warmer / lo-fi"),
]


def make_placeholder_music(duration: int = 12) -> None:
    for filename, freqs, _label in MUSIC_BEDS:
        out_path = ASSETS_DIR / filename
        inputs = []
        for f in freqs:
            inputs += ["-f", "lavfi", "-i", f"sine=frequency={f}:duration={duration}"]
        mix_inputs = "".join(f"[{i}:a]" for i in range(len(freqs)))
        subprocess.run(
            [
                "ffmpeg", "-y",
                *inputs,
                "-filter_complex", f"{mix_inputs}amix=inputs={len(freqs)}:duration=first,volume=0.5[a]",
                "-map", "[a]",
                "-c:a", "aac", "-b:a", "128k",
                str(out_path),
            ],
            check=True,
            capture_output=True,
        )
        print(f"  wrote {out_path.name}")


if __name__ == "__main__":
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    print("Generating placeholder clips...")
    make_placeholder_clips()
    print("Generating placeholder logo...")
    make_placeholder_logo()
    print("Generating placeholder music bed...")
    make_placeholder_music()
    print("Done.")
