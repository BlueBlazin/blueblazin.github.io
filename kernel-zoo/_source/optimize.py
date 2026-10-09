"""Turn the generated PNGs in _source/raw into WebP files for the page.

Illustrations are generated with transparent backgrounds, so this only resizes
and keeps the alpha. Specimens and plates keep their generated margins (which set
their size on the page); sprites are trimmed. Full-bleed textures stay opaque.
    python3 _source/optimize.py [--all]
"""
import pathlib, sys
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "_source" / "raw"
OUT = {"plates": (ROOT / "img", 1200), "sp": (ROOT / "img" / "sp", 520), "sprites": (ROOT / "img" / "sprites", 360)}


def convert(src, dst_dir, size):
    im = Image.open(src)
    if src.stem.startswith("tex-"):
        im, size = im.convert("RGB"), 900
    elif src.parent.name != "sprites":
        im = im.convert("RGBA")  # keep the generated framing: the margins set each figure's size on the page
    else:
        im = im.convert("RGBA")  # sprites are trimmed so the figures can place them exactly
        bbox = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
        if bbox:
            pad = 6
            im = im.crop((max(0, bbox[0] - pad), max(0, bbox[1] - pad), min(im.width, bbox[2] + pad), min(im.height, bbox[3] + pad)))
    im.thumbnail((size, size), Image.LANCZOS)
    dst_dir.mkdir(parents=True, exist_ok=True)
    im.save(dst_dir / f"{src.stem}.webp", "WEBP", quality=86, method=6)


if __name__ == "__main__":
    force = "--all" in sys.argv
    n = 0
    for sub, (dst, size) in OUT.items():
        for f in sorted((RAW / sub).glob("*.png")):
            out = dst / f"{f.stem}.webp"
            if not force and out.exists() and out.stat().st_mtime > f.stat().st_mtime:
                continue
            convert(f, dst, size); n += 1
    print(f"converted {n}")
