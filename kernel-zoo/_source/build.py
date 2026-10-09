"""Build data.js for the specimen-plate edition of Kernel Zoo.

Reads the original catalog (catalog.json, copied from the live site) and
re-files every entry onto a "plate" according to what kind of object the
kernel *is* -- its semantic family -- rather than which field uses it.

    python3 _source/build.py
"""
import json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from icons import svg  # noqa: E402

cat = json.loads((HERE / "catalog.json").read_text())

# Plate order follows the word outward from its literal sense.
PLATES = [
    dict(id="seed", roman="I", name="The Seed", kicker="the literal kernel",
         families=["physical"], color="#c9955a",
         gloss="The inner part of a layered physical object: what is left when the husk, shell or coating comes off.",
         sig=r"\text{kernel}\;\subset\;\text{shell}\;\subset\;\text{whole}"),
    dict(id="core", roman="II", name="The Core", kicker="the trusted center",
         families=["engine"], color="#e3b664",
         gloss="A small, privileged program that every request must pass through.",
         sig=r"\text{rest}\to\boxed{\text{kernel}}\to\text{hardware}"),
    dict(id="routine", roman="III", name="The Routine", kicker="one function, run in parallel",
         families=["compute"], color="#7095e6",
         gloss="A small function that runs many times at once, one copy per index, across a grid of data.",
         sig=r"\mathrm{kernel}(i)\;\;\forall\, i<n,\ \text{in parallel}"),
    dict(id="weighting", roman="IV", name="The Weighting", kicker="a function of two places",
         families=["influence"], color="#ee6a48",
         gloss="A function K(x, y) that says how much the value at y contributes to the result at x.",
         sig=r"(Tf)(x)\;=\;\int K(x,y)\,f(y)\,dy"),
    dict(id="similarity", roman="V", name="The Similarity", kicker="a function of two things",
         families=["similarity"], color="#e9bd4c",
         gloss="A function k(x, y) that scores how alike x and y are, computed as an inner product of features.",
         sig=r"k(x,y)\;=\;\langle\varphi(x),\,\varphi(y)\rangle"),
    dict(id="zero", roman="VI", name="The Vanishing", kicker="what a map sends to zero",
         families=["zero"], color="#e9e2d0",
         gloss="Everything a structure-preserving map sends to zero, or to the identity.",
         sig=r"\ker f\;=\;\{\,x \;:\; f(x)=0\,\}"),
    dict(id="remnant", roman="VII", name="The Remnant", kicker="what survives the pruning",
         families=["subset", "reduction"], color="#4fb3a0",
         gloss="The part of a set, problem or system that is left after everything removable is cut away.",
         sig=r"K=\bigcap_i\,\{\text{survives cut }i\}"),
    dict(id="odd", roman="?", name="The Odd One Out", kicker="fits no family",
         families=["space"], color="#9d947f",
         gloss="A SPICE kernel is simply a data file read by NASA's navigation software.",
         sig=r"\texttt{naif0012.tls}"),
]
fam_to_plate = {f: p["id"] for p in PLATES for f in p["families"]}

entries = []
for p in PLATES:
    group = [e for e in cat["entries"] if fam_to_plate[e["semanticFamily"]] == p["id"]]
    group.sort(key=lambda e: (e["rank"], e["name"].lower()))
    entries += group

# rewritten card text (American English, written for a STEM undergraduate) overrides the original
TEXT = {}
for f in sorted((HERE / "text").glob("out_*.json")):
    TEXT.update(json.loads(f.read_text()))
for e in entries:
    t = TEXT.get(e["id"], {})
    for k in ("short", "body", "tex", "read", "example", "why", "note", "variants"):
        if k in t:
            e[k] = t[k]
    e.setdefault("read", ""); e.setdefault("why", "")

visuals = {}
for no, e in enumerate(entries, 1):
    e["no"] = no
    e["plate"] = fam_to_plate[e["semanticFamily"]]
    visuals.setdefault(e["visual"], svg(e["visual"], e["visual"]))

fields = {f["id"]: f["name"] for f in cat["families"]}
data = dict(plates=PLATES, fields=fields, entries=entries, links=cat["links"],
            sources=cat["sources"], glyphs=visuals)

out = HERE.parent / "data.js"
out.write_text("window.KZ=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n")
print(f"wrote {out.name}: {len(entries)} entries, {len(visuals)} glyphs")
for p in PLATES:
    print(f"  {p['roman']:>4} {p['name']:<16} {sum(e['plate'] == p['id'] for e in entries)}")
