"""Load a generated character portrait and place it into a cover scene.

The portrait generators in tools/portraits are the single source of truth for
what a character looks like. Rather than redrawing them at cover scale, this
runs a generator at reduced fur density (a cover figure is ~half portrait size,
so half the hairs keeps the apparent density the same) and lifts its <defs> and
body out of the standalone <svg> so a scene can drop the figure in.

Every id inside a portrait is already prefixed per character (r-, e-, b-, ...),
so several figures coexist in one scene without collisions.
"""
import os, re, runpy, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PORTRAITS = os.path.abspath(os.path.join(HERE, '..', 'portraits'))
sys.path.insert(0, PORTRAITS)
import furlib  # noqa: E402

# The portrait box. Feet sit on y=330; the figure is centred on x=160.
BOX_W, BOX_H, BASELINE = 320, 360, 330

_cache = {}


def load(name, density=0.5):
    """Returns (defs, body) for a character, generated at `density`."""
    key = (name, density)
    if key in _cache:
        return _cache[key]

    out = os.path.join(PORTRAITS, 'out', name + '.svg')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    saved = open(out).read() if os.path.exists(out) else None

    prev = furlib.DENSITY
    furlib.DENSITY = density
    try:
        globs = runpy.run_path(os.path.join(PORTRAITS, name + '.py'), run_name='__main__')
        svg = globs['svg']
    finally:
        furlib.DENSITY = prev
        # the generator just clobbered the full-density portrait; put it back so
        # tools/portraits/out stays the portrait build's, not ours
        if saved is not None:
            open(out, 'w').write(saved)
        elif os.path.exists(out):
            os.remove(out)

    m = re.search(r'<defs>(.*?)</defs>(.*)</svg>', svg, re.S)
    if not m:
        raise SystemExit(f'{name}: could not split defs/body out of the generated SVG')
    _cache[key] = (m.group(1), m.group(2))
    return _cache[key]


def place(body, x, ybase, height, flip=False, rot=0.0, opacity=None, clip=None, extra=""):
    """Drop a figure into the scene.

    x       - horizontal centre of the figure
    ybase   - scene y the feet stand on
    height  - rendered height of the whole 360-unit portrait box
    flip    - mirror it (the portraits all face right by default)
    rot     - degrees, pivoting on the feet
    """
    s = height / float(BOX_H)
    sx = -s if flip else s
    tx = x + (BOX_W / 2.0) * s * (1 if flip else -1)
    ty = ybase - BASELINE * s
    t = f'translate({tx:.2f},{ty:.2f}) scale({sx:.4f},{s:.4f})'
    if rot:
        t = f'rotate({rot} {x:.1f} {ybase:.1f}) ' + t
    attrs = t and f' transform="{t}"'
    if opacity is not None:
        attrs += f' opacity="{opacity}"'
    if clip:
        attrs += f' clip-path="url(#{clip})"'
    return f'<g{attrs}{extra}>{body}</g>'


def to_scene(px, py, x, ybase, height, flip=False):
    """Map a point in the GENERATOR's coordinates to scene coordinates.

    The generators author facing viewer-left and let common.svg wrap everything
    in the mirror, so a feature written at px shows up at (320 - px) in the box.
    Use this to hang a prop (a scarf, a bandage) on an actual feature instead of
    eyeballing it against the rendered figure.
    """
    s = height / float(BOX_H)
    bx = BOX_W - px
    if flip:
        bx = BOX_W - bx
    return x + (bx - BOX_W / 2.0) * s, ybase - (BASELINE - py) * s


def head_top(ybase, height, top=14):
    """Scene y of the top of a placed figure's bounding box."""
    s = height / float(BOX_H)
    return ybase - (BASELINE - top) * s
