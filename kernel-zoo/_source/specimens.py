"""One specimen illustration per catalogue entry.

Each is a single tangible object (a natural specimen or an antique instrument),
drawn in the style of the seed plate, whose anatomy stands for the idea.
No people, no machines in use, no buildings.
"""

# the exact style that produced the seed specimens
SPEC_STYLE = (
    "A single specimen figure from a nineteenth-century natural-history or scientific-instrument plate, in the manner of Ernst Haeckel's 'Kunstformen der Natur': "
    "delicate, fine copperplate engraving linework with cross-hatching and stippling, printed on warm cream paper. "
    "The figure is shown as if neatly cut out of its printed page along its outline: wherever paper shows inside the figure "
    "(highlights, translucent parts, gaps between parts) it stays warm cream paper, and everything outside the outline is "
    "fully transparent (no backdrop, no glow, no halo, no ground shadow). Black ink with warm hand-tinted watercolour "
    "accents in two or three colours. {palette} Exactly one subject, centred, filling about 70% of the frame, with clear "
    "empty margins. Drawn accurately and coherently, as a careful naturalist would. No people, no hands, no buildings. "
    "Absolutely no text, letters, numbers, labels, borders or frames."
)


def prompt(pid, plate):
    return f"Subject: {SUBJECT[pid]}. " + SPEC_STYLE.format(palette=PALETTE[plate])


PALETTE = {
    "seed": "Tints of walnut brown, ochre and a touch of vermilion.",
    "core": "Tints of brass gold, steel blue and ruby red.",
    "routine": "Tints of cobalt blue, ochre and a touch of vermilion.",
    "weighting": "Tints of vermilion, coral and pale ochre.",
    "similarity": "Tints of chrome yellow, ochre and a touch of cobalt.",
    "zero": "Tints of pewter grey, pale blue and a single vermilion accent.",
    "remnant": "Tints of sea green, ochre and terracotta.",
    "odd": "Tints of brass, slate grey and prussian blue.",
}

SUBJECT = {
    # I · the seed: the literal kernel (kept from the first set)
    "atomic": "a sectioned mineral sphere like an onion-skin agate: a dense red centre wrapped in two thin shells, with a few loose beads orbiting far outside",
    "flame": "a sectioned seed pod bursting open at its heart, a small ochre spark-like core with fine radiating filaments",
    "grain": "a single wheat grain cut lengthwise, showing bran, starchy endosperm and the small germ",
    "fuel": "a tiny coated particle in cross-section, many concentric dark and grey layers around a small solid red kernel",
    "nut": "a walnut split in half, the convoluted edible kernel inside the woody shell",
    # II · the core: a small protected mechanism that everything passes through
    "linux": "an antique anatomical heart with its great vessels branching out to every side: the central organ through which everything flows and which supplies every part of the body",
    "lean": "an assayer's touchstone: a flat black slate with a bright gold streak rubbed across it, a small gold nugget beside it, and two thin reference needles of gold laid next to the streak for comparison",
    "jupyter": "an antique brass pinwheel calculating machine with its crank handle and a row of number wheels",
    "microkernel": "a watchmaker's tray: at its centre only the escapement and balance wheel on a small bridge, and the other wheels and parts of the movement laid out separately around it",
    "cgal": "an open case of brass drawing instruments: compass, ruling pen, protractor and set square in their fitted slots",
    "cad": "a set of carved boxwood geometric solids: a cylinder, a block with rounded edges, and a sphere cut cleanly by a plane",
    "exokernel": "a bare watch movement with no case and no dial at all, its plates and wheels fully exposed",
    "lcf": "a small locked iron strongbox with a single wax seal over its keyhole",
    "security": "an antique lever padlock drawn in cut-away, showing the levers and bolt that check the key",
    "simulation": "the pinned brass cylinder of a music box beside its steel comb, each pin a scheduled note",
    "wolfram": "a column of brass digit wheels from a difference engine",
    # III · the routine: one small program applied everywhere at once
    "cuda": "a wooden frame of honeycomb seen face-on, with one worker bee busy in every cell, all doing the same task at once",
    "triton": "a large carved wooden printing block, an object and not an animal, whose face prints a whole square tile of sixteen small rosettes at once, lying beside a sheet printed with several such tiles",
    "pallas": "a flat brass stencil plate, an object and not an animal, with a decorative geometric pattern cut through it, lying on a sheet of paper",
    "compute-cpu": "a small boxwood abacus",
    "metal": "a steel engraver's die stamp with its sharp relief face",
    "opencl": "a single brass key lying in front of three differently made padlocks it opens: one brass, one iron, one steel",
    "hip": "a double-ended brass key with a different bit at each end",
    "fusion": "an antique folding pocket knife with several blades and tools opened from one handle",
    "dispatch": "a ring of keys with one key turned outwards, chosen",
    "tf": "an opened plaster mould with the cast seashell it produced lying beside it",
    "shader": "a square mosaic panel of identical small square glass tiles in cobalt and gold, an object and not an animal, with a few loose tiles beside it waiting to be set",
    # IV · the weighting: how much each place contributes to another
    "cnn": "the compound eye of a fly seen close: a lattice of small identical lenses",
    "convolution": "a brass-rimmed magnifying glass lying over a printed row of dots of different sizes, the dots under the lens enlarged and softly blurred",
    "filter": "a square of fine brass sieve mesh in a wooden frame",
    "integral": "a small harp whose strings, of different thicknesses, join its two arms",
    "kde": "a row of small bell-shaped harebell flowers of different heights growing side by side",
    "heat": "a single coal ember with shimmering rings of heat spreading outward around it",
    "markov": "a pair of antique ivory dice",
    "probability": "a Galton board: a wooden board of pins with small balls piled into a bell-shaped heap in the slots below",
    "morphology": "a set of brass punches with cross, square and disc-shaped tips",
    "averaging": "a lens of frosted glass in a brass ring",
    "bethe": "two cherries joined on one stem",
    "cauchy": "a closed loop of brass wire encircling a single pearl",
    "collision": "two drops of quicksilver merging into one",
    "likelihood": "a glass bell jar",
    "dirichlet": "a ruffled cockle shell with a tall central crest and rippled edges",
    "dispersal": "a dandelion seed head releasing its seeds, which drift away: most stay close to the head, a few travel far",
    "xc": "a cluster of soap bubbles, each pressing a hollow into its neighbours",
    "fejer": "a smooth bell-shaped mushroom cap with fine gills beneath",
    "path-kernel": "a corner of a woven cane lattice, its strands making diagonal paths",
    "green": "a single drop of water falling into a shallow round dish, rings spreading out and reflecting from the rim",
    "hilbert": "a pair of mirror-image spiral seashells, one coiling left and one coiling right",
    "reconstruction": "a brass French curve drafting template",
    "kpm": "a steel tuning fork with fading rings of sound around its tines",
    "regression": "a draughtsman's flexible wooden spline, an object and not an animal: a thin wooden batten bent into a smooth curve and held in shape by four heavy grey lead spline weights resting against it",
    "memory": "a brass pendulum bob swinging inside a glass jar of honey",
    "mollifier": "a smooth, rounded river pebble beside the jagged rock fragment it was worn from",
    "poisson": "a round drum with a tensioned skin and a laced rim",
    "shield": "a thick lead brick with a small glass vial of radium glowing faintly behind it",
    "sensitivity": "an antique brass seismometer: a heavy pendulum with a fine stylus",
    "singular": "a single needle-sharp sea urchin spine",
    "sph": "a small heap of clear glass marbles",
    "stein-prob": "a brass balance scale resting in perfect equilibrium",
    "transform": "a glass prism splitting a ray of light into a spectrum",
    "volterra": "three nested glass handbells of graduated sizes",
    # V · the similarity: comparing two things
    "psd": "two scallop shells, one fitted perfectly over the other",
    "rbf": "two overlapping circular ripples spreading on still water",
    "gp": "a long string of pearls whose sizes change smoothly from one to the next",
    "ntk": "two leaves from the same tree laid side by side, their vein patterns matching",
    "rkhs": "a seashell and its exact reflection in a small hand mirror",
    "attention": "a spider's web with threads of different thickness running from the centre to dewdrops",
    "quantum": "two soap bubbles pressed together, their shared wall and iridescent interference colours where they overlap",
    "bergman": "a polished agate slice with smooth, flowing colour bands",
    "determinantal": "a pine cone with its scales evenly spaced",
    "fisher": "two feathers laid side by side, compared vane by vane",
    "graph-ml": "two sprigs of coral with similar branching, side by side",
    "mmd": "a brass balance with a small heap of shells on each pan",
    "kernel-families": "a tray of related seashells: a scallop, a cockle, a cowrie and a whelk",
    "nngp": "a fan of many fine feathers whose tips together trace a smooth bell-shaped outline",
    "stein-ml": "a magnetic compass with iron filings tracing field lines around it",
    "string": "two strings of coloured glass beads laid side by side, sharing several runs of the same colours",
    "szego": "a ring of small shells arranged around the rim of a round dish",
    # VI · the vanishing: what a map sends to zero
    "nullspace": "a single poppy pressed perfectly flat between two panes of glass, beside the same poppy fresh and upright: pressing has removed one whole direction, its depth",
    "group": "an antique clock dial",
    "ring": "a toothed brass wheel with every fourth tooth marked in vermilion",
    "category": "a compass rose whose arrows all meet at an empty ring at its centre",
    "congruence": "pairs of identical acorns tied together with thread",
    "operator": "an antique brass spirit level with its glass vial, the air bubble resting exactly at the centre mark",
    "isogeny": "a glass torus paperweight with a few gold flecks inside",
    "kernel-pair": "two identical keys tied together on one ring",
    "module": "a set of nested empty brass rings, like an armillary sphere without its globe",
    "code": "a strip of punched paper tape",
    # VII · the remnant: what survives the pruning
    "kernelization": "a small bonsai tree pruned back hard to a compact, dense core of branches, the cut twigs lying beside its pot",
    "lossy": "an apple core with a little flesh still left on it",
    "belief": "a small stone arch held up by its keystone",
    "game": "a round pie cut into equal, fair slices",
    "digraph": "a few separate limpets spaced apart on a stone",
    "discriminating": "a ship in a bottle",
    "kernel-search": "a prospector's gold pan with a few nuggets left after the gravel has been washed out",
    "perfect": "a single snowflake",
    "kern": "a cross-section of a stone column with a small diamond marked at its centre",
    "semigroup": "three overlapping soap films sharing one small common lens",
    "radical": "a cluster of crystals with exactly one of each kind: quartz, pyrite and amethyst",
    "saturation": "an onion cut in half, showing its nested layers",
    "viability": "a sea star sheltering in a shallow stone basin of seawater",
    "polygon": "a polished star sapphire cabochon whose six-rayed star meets in a small central hexagon; the stone is drawn crisply with no glow and no halo around it",
    # ? · incertae sedis
    "spice": "a stack of punched data cards beside a brass sextant",
}
