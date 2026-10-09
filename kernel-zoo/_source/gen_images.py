"""Generate every illustration with the OpenAI Images API, on black.

Reads OPENAI_API_KEY, or an API_KEY file next to index.html (git-ignored, never printed). Writes PNGs to _source/raw/;
run _source/optimize.py afterwards to make the web files.

    python3 _source/gen_images.py plates      # title + 8 plate engravings
    python3 _source/gen_images.py specimens   # one engraving per catalogue entry
    python3 _source/gen_images.py sprites     # small pieces the diagrams are built from
    python3 _source/gen_images.py cuda husk   # regenerate particular items
Add --force to overwrite existing files.
"""
import base64, concurrent.futures as cf, json, os, pathlib, sys, time, urllib.error, urllib.request

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from specimens import SPEC_STYLE, prompt as spec_prompt  # noqa: E402
from sprites import SPRITES  # noqa: E402

RAW = HERE / "raw"
def api_key():
    """OPENAI_API_KEY from the environment, or an API_KEY file in the project folder (git-ignored)."""
    key = os.environ.get("OPENAI_API_KEY") or ((HERE.parent / "API_KEY").read_text() if (HERE.parent / "API_KEY").exists() else "")
    if not key.strip():
        sys.exit("Set OPENAI_API_KEY or put the key in an API_KEY file next to index.html.")
    return key.strip()
MODEL = "gpt-image-2.5-flare"

STYLE = (
    "A hand-coloured copperplate engraving, as a plate from Diderot's Encyclopédie or a nineteenth-century natural-philosophy "
    "treatise, with the delicacy of Haeckel's Kunstformen der Natur: fine engraved linework, cross-hatching and stipple, and "
    "transparent watercolour washes applied by hand in a few colours. The subject is drawn literally and legibly, so the idea "
    "is understood at a glance. Printed on warm cream paper that fills the whole frame (solid #ECE2C7), no vignette, no border, no frame. "
)
SPRITE_STYLE = (
    "A single small figure cut from a hand-coloured copperplate engraving of the same series: fine engraved linework, "
    "cross-hatching and stipple with transparent hand-applied watercolour washes. Exactly one isolated object, centred, "
    "filling about 80% of the frame, on plain warm cream paper (solid #ECE2C7), no shadow, no vignette, no frame. "
)
NO_TEXT = "Absolutely no text, letters, numbers, labels, signatures, borders or frames."

FOUR = "Four specimens arranged symmetrically on one plate, each drawn whole and separately: "
PLATES = {
    "title": "a single walnut split open, its golden kernel exposed, resting on its two cracked shell halves",
    "seed": FOUR + "a wheat grain cut lengthwise; a walnut split in half; a hazelnut cut open; a maize kernel sliced through, each showing husk, shell or coat around its kernel",
    "odd": "an antique brass orrery with a small sun and two planets on elliptical rings, beside a neat stack of punched data cards",
    "core": FOUR + "an antique anatomical heart with its great vessels; an assayer's touchstone with a gold streak, a gold nugget and reference needles; an antique lever padlock in cut-away; a brass pinwheel calculating machine",
    "routine": FOUR + "a honeycomb frame with a worker bee in every cell; a carved printing block beside a sheet printed in a grid of its rosette; one brass key before three different padlocks; an antique folding pocket knife with several blades open",
    "weighting": FOUR + "a magnifying glass over a row of dots of different sizes; a dandelion releasing its seeds; a Galton board with balls heaped in a bell shape; a glass prism splitting a ray into a spectrum",
    "similarity": FOUR + "two scallop shells fitted one over the other; two soap bubbles pressed together; two strings of coloured beads sharing runs of colour; a brass balance with a heap of shells on each pan",
    "zero": FOUR + "a poppy pressed flat between glass beside a fresh poppy; an antique clock dial; a brass spirit level with its bubble centred; a strip of punched paper tape",
    "remnant": FOUR + "a bonsai pruned to a compact core with its clippings beside it; an apple core; a small stone arch held by its keystone; a gold pan with a few nuggets left",
}
PALETTES = {"seed": "walnut brown, ochre and a touch of vermilion", "odd": "brass, slate grey and prussian blue", "title": "walnut brown and ochre with a touch of vermilion", "core": "brass gold, steel blue and ruby red",
            "routine": "golden honey, cobalt blue and a touch of vermilion", "weighting": "vermilion, coral and pale ochre",
            "similarity": "chrome yellow, ochre and a touch of cobalt", "zero": "pewter grey, pale blue and vermilion",
            "remnant": "sea green, ochre and terracotta"}


def jobs():
    out = {}
    for k, subj in PLATES.items():
        out[k] = (RAW / "plates" / f"{k}.png", f"Subject: {subj}. " + SPEC_STYLE.replace("Exactly one subject, centred, filling about 70% of the frame", "A balanced plate composition filling about 80% of the frame").format(palette=f"Tints of {PALETTES[k]}."), "high")
    entries = json.loads((HERE.parent / "data.js").read_text()[len("window.KZ="):-2])["entries"]
    for e in entries:
        out[e["id"]] = (RAW / "sp" / f"{e['id']}.png", spec_prompt(e["id"], e["plate"]), "medium")
    for k, subj in SPRITES.items():
        p = (f"Subject: {subj}. " + SPEC_STYLE.format(palette="")) if not k.startswith("tex-") else f"{subj}. {STYLE}{NO_TEXT}"
        out[k] = (RAW / "sprites" / f"{k}.png", p, "medium")
    return out, entries


def generate(item):
    name, (path, prompt, quality) = item
    # everything but the full-bleed textures is generated on a transparent background
    bg = "opaque" if name.startswith("tex-") else "transparent"
    body = json.dumps({"model": MODEL, "prompt": prompt, "n": 1, "size": "1024x1024", "quality": quality,
                       "background": bg, "output_format": "png"}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=body,
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key()}"})
    for attempt in range(10):  # the endpoint allows ~20 images a minute
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                data = json.load(r)
            break
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 9:
                return name, f"HTTP {e.code}: {e.read().decode()[:200]}"
            time.sleep(8 + 6 * attempt)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(base64.b64decode(data["data"][0]["b64_json"]))
    return name, "ok"


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--force"]
    force = "--force" in sys.argv
    all_jobs, entries = jobs()
    groups = {"plates": list(PLATES), "specimens": [e["id"] for e in entries], "sprites": list(SPRITES)}
    names = [n for a in args for n in groups.get(a, [a])]
    todo = [(n, all_jobs[n]) for n in names if force or not all_jobs[n][0].exists()]
    with cf.ThreadPoolExecutor(4) as ex:
        for name, status in ex.map(generate, todo):
            print(name, status, flush=True)
