"""Generate a handful of sample specimens for review before any batch run.
    python3 _source/samples.py
Writes _source/samples/<id>.png and a labelled contact sheet."""
import concurrent.futures as cf, pathlib, sys
from PIL import Image, ImageDraw
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from gen_images import generate  # noqa: E402

from specimens import prompt, SUBJECT  # noqa: E402
# one-off alternatives to compare against the main list
SUBJECT["lean-loupe"] = "a brass jeweler's loupe seen from directly above, held flat over a single cut ruby; through the round lens the same ruby appears magnified, exactly centered and aligned with the stone beneath, as real optics would show it"
SUBJECT["lean-touchstone"] = "an assayer's touchstone: a flat black slate with a bright gold streak rubbed across it, a small gold nugget beside it, and two thin reference needles of gold laid next to the streak for comparison"
SUBJECT["cuda-bees"] = "a wooden frame of honeycomb seen face-on, with one worker bee busy in every cell, all doing the same task at once"
import json
PLATE = {"cuda-bees": "routine", "lean-loupe": "core", "lean-touchstone": "core"} | {e["id"]: e["plate"] for e in json.loads((HERE.parent / "data.js").read_text()[len("window.KZ="):-2])["entries"]}
IDS = sys.argv[1:] or ["linux", "cuda", "opencl", "nullspace", "convolution", "psd", "regression", "security"]
SAMPLES = IDS

if __name__ == "__main__":
    out = HERE / "samples"; out.mkdir(exist_ok=True)
    for k in SAMPLES: (out / f"{k}.png").unlink(missing_ok=True)
    jobs = [(k, (out / f"{k}.png", prompt(k, PLATE[k]), "medium")) for k in SAMPLES]
    with cf.ThreadPoolExecutor(4) as ex:
        for name, status in ex.map(generate, jobs):
            print(name, status, flush=True)
    T = 340; sheet = Image.new("RGB", (4 * T, 2 * (T + 26)), "#ece2c7"); d = ImageDraw.Draw(sheet)
    for i, k in enumerate(SAMPLES):
        im = Image.open(out / f"{k}.png"); im.thumbnail((T, T)); x, y = (i % 4) * T, (i // 4) * (T + 26)
        sheet.paste(im, (x, y)); d.text((x + 10, y + T + 6), k, fill="#1d1a15")
    sheet.save(out / "_sheet.jpg", quality=90)
