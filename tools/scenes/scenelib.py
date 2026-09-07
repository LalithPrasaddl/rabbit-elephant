"""Painterly scene primitives for the story covers.

Same rules as the portraits (see tools/portraits/common.py): no outline strokes,
light from the upper-RIGHT, texture generated rather than drawn, and every blur
filter given a generous region so it never clips into a visible rectangle.

Coordinates are the cover viewBox: 0 0 500 300, horizon around y=170.
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'portraits'))

from furlib import fur_layers, render_fur, speckle  # noqa: E402

# The scene is authored in a 500x300 "safe frame" - that is what a desktop card
# shows, and every character and prop belongs inside it. The canvas is then bled
# past that frame (more sky above, more ground below) so the same SVG can cover
# a wide desktop card AND a tall phone card with `slice`, cropping only
# background. Keep anything that matters inside x 58..442 - that is what
# survives the horizontal crop on a phone.
W, H = 500, 300
# Asymmetric on purpose. A desktop card (960x540) shows a 281-unit-tall window
# centred on the canvas, so weighting the bleed downwards puts that window at
# y 54..335: the whole scene, plus ~60 units of open ground beneath the
# characters' feet for the title to sit on. A phone shows the full height.
BLEED_TOP, BLEED_BOT = 84, 173
CANVAS_Y = -BLEED_TOP
CANVAS_H = H + BLEED_TOP + BLEED_BOT
SAFE_X = (58, 442)


# ---------------------------------------------------------------- defs

def filters(P):
    """Blur filters at four radii. The region is deliberately huge - a tight
    region clips the blur into a visible box (portrait bug #5)."""
    reg = 'x="-150%" y="-150%" width="400%" height="400%"'
    return "".join(
        f'<filter id="{P}-b{i}" {reg}><feGaussianBlur stdDeviation="{sd}"/></filter>'
        for i, sd in [(1, 1.6), (2, 3.4), (3, 7), (4, 14)])


def lin(id_, stops, x1=0, y1=0, x2=0, y2=1):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"{"" if op is None else f" stop-opacity=\"{op}\""}/>'
                for o, c, op in stops)
    return f'<linearGradient id="{id_}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>'


def rad(id_, stops, cx="50%", cy="50%", r="50%"):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"{"" if op is None else f" stop-opacity=\"{op}\""}/>'
                for o, c, op in stops)
    return f'<radialGradient id="{id_}" cx="{cx}" cy="{cy}" r="{r}">{s}</radialGradient>'


# ---------------------------------------------------------------- sky

SKY_MOODS = {
    # top, upper-mid, horizon haze  - all warm and safe; never dark (audience is 2-4)
    'morning':  ("#8FC9EE", "#BFE4F7", "#F2FBFF"),
    'golden':   ("#F7C169", "#FFDEA0", "#FFF4DC"),
    'peach':    ("#F7B79A", "#FFD6BE", "#FFF2E8"),
    'winter':   ("#A8C6E8", "#CFE0F2", "#F6FAFF"),
    'noon':     ("#7FC3EA", "#B6E0F5", "#EEF9FF"),
    'dusk':     ("#E2A6C0", "#FFC9B6", "#FFEBD8"),
}


def sky(P, mood, horizon=170):
    top, mid, haze = SKY_MOODS[mood]
    d = lin(f"{P}-sky", [(0, top, None), (0.55, mid, None), (1, haze, None)])
    body = f'<rect y="{CANVAS_Y}" width="{W}" height="{horizon + 12 + BLEED_TOP}" fill="url(#{P}-sky)"/>'
    return d, body


def sun(P, x, y, r=34, warm="#FFF3CE", glow="#FFE6A2"):
    """A glow rather than a flat disc: three stacked falloffs plus a hot core."""
    d = (rad(f"{P}-sung", [(0, glow, "0.85"), (0.35, glow, "0.42"), (1, glow, "0")]) +
         rad(f"{P}-sunc", [(0, "#FFFFFF", "1"), (0.55, warm, "0.95"), (1, warm, "0.1")]))
    body = (f'<circle cx="{x}" cy="{y}" r="{r*4.2:.0f}" fill="url(#{P}-sung)" opacity=".55"/>'
            f'<circle cx="{x}" cy="{y}" r="{r*2.1:.0f}" fill="url(#{P}-sung)" opacity=".7"/>'
            f'<circle cx="{x}" cy="{y}" r="{r*0.62:.0f}" fill="url(#{P}-sunc)"/>')
    return d, body


def clouds(P, specs):
    """specs: (cx, cy, rx, ry, opacity). Each cloud is a lit top and a shaded
    underside, both blurred - no hard ellipse edge anywhere."""
    out = []
    for (cx, cy, rx, ry, op) in specs:
        out.append(
            f'<g opacity="{op}">'
            f'<ellipse cx="{cx}" cy="{cy+ry*.35:.0f}" rx="{rx}" ry="{ry*.9:.0f}" fill="#C9D8E6" opacity=".55" filter="url(#{P}-b3)"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx*.95:.0f}" ry="{ry}" fill="#FFFFFF" filter="url(#{P}-b3)"/>'
            f'<ellipse cx="{cx+rx*.28:.0f}" cy="{cy-ry*.45:.0f}" rx="{rx*.5:.0f}" ry="{ry*.85:.0f}" fill="#FFFDF7" filter="url(#{P}-b3)"/>'
            f'</g>')
    return "".join(out)


def hills(P, rng, horizon=170, far="#9FC3A2", near="#7FAE72"):
    """Two hazed bands behind the meadow so the horizon has depth."""
    d = (lin(f"{P}-hillf", [(0, far, None), (1, "#B9D4B6", None)]) +
         lin(f"{P}-hilln", [(0, near, None), (1, "#8FBB7E", None)]))
    y = horizon
    a = (f'<path d="M0,{y-16} C70,{y-40} 130,{y-6} 210,{y-20} C290,{y-34} 360,{y-4} 500,{y-24} '
         f'L500,{y+40} L0,{y+40} Z" fill="url(#{P}-hillf)" opacity=".75" filter="url(#{P}-b2)"/>')
    b = (f'<path d="M0,{y-4} C90,{y-22} 150,{y+2} 250,{y-10} C340,{y-21} 420,{y+2} 500,{y-8} '
         f'L500,{y+40} L0,{y+40} Z" fill="url(#{P}-hilln)" opacity=".85" filter="url(#{P}-b1)"/>')
    return d, a + b


def foliage(P, rng, x, y, r, dark="#3E6B3C", base="#5C9150", light="#8FC46A"):
    """A tree/bush clump: overlapping blobs, speckled leaf texture, lit upper-right."""
    gid = f"{P}-fol{int(x)}{int(y)}"
    d = rad(gid, [(0, light, None), (0.45, base, None), (1, dark, None)], cx="66%", cy="24%", r="88%")
    blobs = []
    zones = []
    for (dx, dy, rr) in [(0, 0, 1.0), (-r*.62, r*.18, .72), (r*.58, r*.22, .68), (-r*.2, -r*.5, .66), (r*.24, -r*.44, .6)]:
        cx, cy, R = x+dx, y+dy, r*rr
        blobs.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{R:.0f}" ry="{R*.88:.0f}" fill="url(#{gid})"/>')
        zones.append(dict(ell=(cx, cy, R*.82, R*.72), n=int(R*2.0),
                          tones=[(dark, .16), (light, .17), (base, .14)], r=(1.4, 3.2)))
    tex = speckle(zones, rng)
    shade = (f'<ellipse cx="{x-r*.5:.0f}" cy="{y+r*.45:.0f}" rx="{r*.8:.0f}" ry="{r*.55:.0f}" '
             f'fill="#25452A" opacity=".30" filter="url(#{P}-b3)"/>')
    rim = (f'<ellipse cx="{x+r*.5:.0f}" cy="{y-r*.48:.0f}" rx="{r*.46:.0f}" ry="{r*.3:.0f}" '
           f'fill="#D9F0A8" opacity=".38" filter="url(#{P}-b2)"/>')
    return d, "".join(blobs) + shade + tex + rim


def trunk(x, ytop, ybot, w=7, col="#6B4A2E", light="#8E6842"):
    return (f'<path d="M{x-w/2:.0f},{ybot} C{x-w/2:.0f},{(ytop+ybot)/2:.0f} {x-w*.9:.0f},{ytop+8} {x-w*.4:.0f},{ytop} '
            f'L{x+w*.6:.0f},{ytop} C{x+w:.0f},{ytop+10} {x+w/2:.0f},{(ytop+ybot)/2:.0f} {x+w/2:.0f},{ybot} Z" fill="{col}"/>'
            f'<path d="M{x+w*.1:.0f},{ybot} C{x+w*.1:.0f},{(ytop+ybot)/2:.0f} {x+w*.4:.0f},{ytop+10} {x+w*.5:.0f},{ytop+2}" '
            f'stroke="{light}" stroke-width="2" fill="none" opacity=".5"/>')


# ---------------------------------------------------------------- ground

FLOWERS = ["#FF6B6B", "#FFD166", "#C77DFF", "#74C8E4", "#FF9BAE", "#FFFFFF"]


def meadow(P, rng, horizon=170, top="#8CC163", bot="#3F7237", warm=True, avoid=(), flowers=24):
    """Grass: a gradient body, a sun-warmed band near the horizon, generated
    blade strokes on a slight lean, then flowers.

    Returns (defs, back, front). `front` is the handful of foreground flowers and
    tall blades that belong IN FRONT of the characters - drawing a few blades over
    the feet is what stops a placed figure reading as pasted onto the grass.
    `avoid` is a list of (x, y, rx, ry) ellipses that flowers keep out of.
    """
    d = lin(f"{P}-grd", [(0, top, None), (0.45, "#6CA24B", None), (1, bot, None)])
    y = horizon
    ground = (f'<path d="M0,{y} C110,{y-9} 180,{y+6} 260,{y+1} C340,{y-4} 420,{y+7} 500,{y-2} '
              f'L500,{H+BLEED_BOT} L0,{H+BLEED_BOT} Z" fill="url(#{P}-grd)"/>')
    haze = (f'<path d="M0,{y+2} C110,{y-7} 180,{y+8} 260,{y+3} C340,{y-2} 420,{y+9} 500,{y} '
            f'L500,{y+26} L0,{y+26} Z" fill="#D8EFAE" opacity="{.5 if warm else .3}" filter="url(#{P}-b3)"/>')
    # blades: shorter and sparser near the horizon, longer in the foreground
    bands = [
        dict(ell=(250, y + 16, 265, 14), n=100, len=(3, 7), w=(.7, .16)),
        dict(ell=(250, y + 48, 265, 24), n=130, len=(5, 11), w=(.9, .20)),
        dict(ell=(250, y + 92, 265, 28), n=130, len=(7, 15), w=(1.1, .22)),
        dict(ell=(250, y + 126, 265, 20), n=110, len=(9, 19), w=(1.4, .24)),
        dict(ell=(250, H + BLEED_BOT * .55, 265, BLEED_BOT * .5), n=110, len=(11, 24), w=(1.6, .26)),
    ]
    layers = []
    for b in bands:
        tones = [("#B4DE7E", b["w"][0], b["w"][1] + .06), ("#4E8340", b["w"][0], b["w"][1]),
                 ("#8FC46A", b["w"][0], b["w"][1] + .04), ("#2F5C2B", b["w"][0] * .8, b["w"][1] - .04)]
        layers += fur_layers([dict(ell=b["ell"], n=b["n"], flow=lambda x, y: -math.pi/2 + 0.22,
                                   tones=tones, len=b["len"], curve=1.6, jitter=0.34)], rng)
    blades = render_fur(layers)

    back, front = _flowers(rng, y, avoid, flowers)
    tall = render_fur(fur_layers([dict(ell=(250, H + BLEED_BOT - 6, 250, 22), n=80,
                                       flow=lambda x, y: -math.pi/2 + 0.2,
                                       tones=[("#4E8340", 1.5, .5), ("#8FC46A", 1.4, .55), ("#2F5C2B", 1.3, .42)],
                                       len=(14, 30), curve=2.2, jitter=0.3)], rng))
    return d, ground + haze + blades + back, tall + front


def _flowers(rng, horizon, avoid, count):
    """Stratified so they scatter evenly instead of clumping into a stripe."""
    back, front = [], []
    cols, rows = 8, 4
    for r in range(rows):
        for c in range(cols):
            if rng.random() > count / float(cols * rows):
                continue
            fx = (c + rng.uniform(.15, .85)) * (W / cols)
            fy = horizon + 16 + (r + rng.uniform(.1, .9)) * ((H + BLEED_BOT - horizon - 22) / rows)
            if any(((fx-ax)/arx)**2 + ((fy-ay)/ary)**2 < 1 for (ax, ay, arx, ary) in avoid):
                continue
            # cap the perspective growth - the bled foreground runs far past the
            # safe frame, and an uncapped scale turns those flowers into blobs
            s = min(2.0, 1.0 + (fy - horizon) / 130.0 * 1.4)
            col = FLOWERS[rng.randrange(len(FLOWERS))]
            g = (f'<g opacity="{rng.uniform(.7, .95):.2f}">'
                 f'<path d="M{fx:.0f},{fy+5*s:.0f} q{-1.5*s:.1f},{-4*s:.1f} 0,{-7*s:.1f}" stroke="#4E8340" '
                 f'stroke-width="{1.1*s:.1f}" fill="none" opacity=".8"/>'
                 f'<circle cx="{fx:.0f}" cy="{fy:.0f}" r="{2.4*s:.1f}" fill="{col}"/>'
                 f'<circle cx="{fx-.5*s:.1f}" cy="{fy-.6*s:.1f}" r="{1.0*s:.1f}" fill="#FFF8E0" opacity=".9"/></g>')
            (front if r == rows - 1 else back).append(g)
    return "".join(back), "".join(front)


def sunwash(P, x, y):
    """One warm pass over the whole frame from the sun's side, and a cool one
    opposite. This is what makes a placed figure share the scene's light instead
    of reading as a sticker."""
    d = (rad(f"{P}-wash", [(0, "#FFEFC4", "0.30"), (0.42, "#FFDF9E", "0.10"), (1, "#FFDF9E", "0")],
             cx=f"{x/W*100:.0f}%", cy=f"{y/H*100:.0f}%", r="78%") +
         rad(f"{P}-cool", [(0, "#3E5F80", "0.07"), (1, "#3E5F80", "0")],
             cx=f"{100-x/W*100:.0f}%", cy="98%", r="62%"))
    r = f'y="{CANVAS_Y}" width="{W}" height="{CANVAS_H}"'
    return d, (f'<rect {r} fill="url(#{P}-cool)"/><rect {r} fill="url(#{P}-wash)"/>')


def cast_shadow(P, x, ybase, w, h=None, op=.46, col="#1F4020", stretch=1.5):
    """A real cast shadow, thrown down-LEFT because the light is upper-right:
    a long soft pool plus a tight dark contact patch right under the feet."""
    h = h or w * 0.24
    return (f'<ellipse cx="{x - w*stretch*.36:.0f}" cy="{ybase + h*.30:.0f}" rx="{w*stretch:.0f}" ry="{h*1.1:.0f}" '
            f'fill="{col}" opacity="{op*.45:.2f}" filter="url(#{P}-b4)"/>'
            f'<ellipse cx="{x - w*.22:.0f}" cy="{ybase + h*.12:.0f}" rx="{w*.92:.0f}" ry="{h*.82:.0f}" '
            f'fill="{col}" opacity="{op*.8:.2f}" filter="url(#{P}-b3)"/>'
            f'<ellipse cx="{x - w*.08:.0f}" cy="{ybase:.0f}" rx="{w*.58:.0f}" ry="{h*.46:.0f}" '
            f'fill="#17331A" opacity="{op:.2f}" filter="url(#{P}-b2)"/>')


def contact_shadow(P, x, y, rx, ry, op=.34, col="#2B4A22"):
    return f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="{col}" opacity="{op}" filter="url(#{P}-b3)"/>'


def vignette(P):
    """A touch of warmth in the corners so the frame feels painted, not cropped."""
    d = rad(f"{P}-vig", [(0.6, "#000000", "0"), (1, "#4A2E12", "0.13")], cx="50%", cy="46%", r="74%")
    return d, f'<rect y="{CANVAS_Y}" width="{W}" height="{CANVAS_H}" fill="url(#{P}-vig)"/>'


def wrap(P, defs, body):
    return (f'<svg viewBox="0 {CANVAS_Y} {W} {CANVAS_H}" preserveAspectRatio="xMidYMid slice" '
            f'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
            f'<defs>{filters(P)}{defs}</defs>'
            f'<clipPath id="{P}-frame"><rect y="{CANVAS_Y}" width="{W}" height="{CANVAS_H}"/></clipPath>'
            f'<g clip-path="url(#{P}-frame)">{body}</g></svg>')


# ---------------------------------------------------------------- winter

def snowfield(P, rng, horizon=170, avoid=()):
    """Snow-covered ground. Snow is never pure white: it takes a warm tint where
    the sun hits and a cool blue in the hollows, or it reads as a paper cut-out."""
    d = (lin(f"{P}-snow", [(0, "#FFFFFF", None), (0.4, "#F2F7FF", None), (1, "#D3E2F2", None)]) +
         lin(f"{P}-snow2", [(0, "#FFF6E2", "0.85"), (1, "#FFF6E2", "0")]))
    y = horizon
    ground = (f'<path d="M0,{y} C110,{y-10} 180,{y+5} 260,{y} C340,{y-5} 420,{y+6} 500,{y-3} '
              f'L500,{H+BLEED_BOT} L0,{H+BLEED_BOT} Z" fill="url(#{P}-snow)"/>')
    warm = (f'<path d="M0,{y+2} C110,{y-8} 180,{y+7} 260,{y+2} C340,{y-3} 420,{y+8} 500,{y-1} '
            f'L500,{y+34} L0,{y+34} Z" fill="url(#{P}-snow2)" opacity=".8" filter="url(#{P}-b3)"/>')
    drifts = []
    for (cx, cy, rx, ry) in [(70, y + 44, 90, 20), (300, y + 30, 120, 16), (440, y + 62, 110, 22),
                             (180, y + 92, 130, 26), (390, y + 110, 140, 28)]:
        drifts.append(f'<ellipse cx="{cx}" cy="{cy+7}" rx="{rx}" ry="{ry}" fill="#B9CFE6" opacity=".40" filter="url(#{P}-b3)"/>'
                      f'<ellipse cx="{cx+8}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#FFFFFF" opacity=".85" filter="url(#{P}-b3)"/>')
    sparkle = "".join(
        f'<circle cx="{rng.uniform(6, W-6):.0f}" cy="{rng.uniform(y+12, H+BLEED_BOT-4):.0f}" r="{rng.uniform(.7, 1.5):.1f}" '
        f'fill="#FFFFFF" opacity="{rng.uniform(.5, 1):.2f}"/>' for _ in range(90))
    return d, ground + warm + "".join(drifts) + sparkle


def snowfall(P, rng, n=70):
    out = []
    for _ in range(n):
        x, y = rng.uniform(0, W), rng.uniform(CANVAS_Y, H + BLEED_BOT)
        r = rng.uniform(1.0, 3.4)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#FFFFFF" opacity="{rng.uniform(.45, .95):.2f}"'
                   f'{f" filter=\"url(#{P}-b1)\"" if r > 2.4 else ""}/>')
    return "".join(out)


def winter_tree(P, x, ybase, h=90, w=8):
    """A bare tree: branches spring UP and OUT from points along the trunk, with
    a ridge of snow sitting on top of each one."""
    top = ybase - h
    br = []
    for (deg, ln, lev) in [(-48, .46, .42), (46, .43, .50), (-34, .36, .62),
                           (38, .34, .70), (-16, .28, .84), (20, .26, .88)]:
        sx, sy = x, ybase - lev * h
        a = math.radians(deg - 90)
        ex, ey = sx + math.cos(a) * ln * h, sy + math.sin(a) * ln * h
        mx, my = (sx + ex) / 2 + math.cos(a) * 4, (sy + ey) / 2 - 6
        wid = max(1.5, w * .46 * (1 - lev * .6))
        br.append(f'<path d="M{sx:.0f},{sy:.0f} Q{mx:.0f},{my:.0f} {ex:.0f},{ey:.0f}" '
                  f'stroke="#6B5140" stroke-width="{wid:.1f}" fill="none" stroke-linecap="round"/>')
        br.append(f'<path d="M{sx:.0f},{sy-wid*.7:.0f} Q{mx:.0f},{my-wid*.9:.0f} {ex:.0f},{ey-wid*.6:.0f}" '
                  f'stroke="#FFFFFF" stroke-width="{wid*.55:.1f}" fill="none" stroke-linecap="round" opacity=".9"/>')
    return (trunk(x, top, ybase, w, "#6B5140", "#8E6E52") + "".join(br) +
            f'<ellipse cx="{x-4:.0f}" cy="{ybase+2:.0f}" rx="{w*2.8:.0f}" ry="{w*1.0:.0f}" '
            f'fill="#FFFFFF" opacity=".92" filter="url(#{P}-b2)"/>')


# ---------------------------------------------------------------- path, water, props

def dirt_path(P, rng, horizon=170, xtop=280, xbot=250, wtop=22, wbot=210):
    """A worn track running from the horizon to the bottom of the frame."""
    d = lin(f"{P}-dirt", [(0, "#C7A075", None), (0.55, "#B18C63", None), (1, "#8E6B47", None)])
    y = horizon
    body = (f'<path d="M{xtop-wtop/2:.0f},{y} L{xbot-wbot*.72:.0f},{H+BLEED_BOT} L{xbot+wbot*.72:.0f},{H+BLEED_BOT} L{xtop+wtop/2:.0f},{y} Z" '
            f'fill="url(#{P}-dirt)" opacity=".95" filter="url(#{P}-b1)"/>')
    edge = (f'<path d="M{xtop-wtop/2-3:.0f},{y} L{xbot-wbot*.72-6:.0f},{H+BLEED_BOT}" stroke="#5E8A44" stroke-width="7" '
            f'fill="none" opacity=".35" filter="url(#{P}-b2)"/>'
            f'<path d="M{xtop+wtop/2+3:.0f},{y} L{xbot+wbot*.72+6:.0f},{H+BLEED_BOT}" stroke="#5E8A44" stroke-width="7" '
            f'fill="none" opacity=".35" filter="url(#{P}-b2)"/>')
    grit = "".join(
        f'<ellipse cx="{(lambda t: xtop + (xbot-xtop)*t + rng.uniform(-1,1)*(wtop + (wbot-wtop)*t)/2*.85)(t):.0f}" '
        f'cy="{y + (H+BLEED_BOT-y)*t:.0f}" rx="{rng.uniform(1.2, 4)*(0.4+t):.1f}" ry="{rng.uniform(.8, 2.4)*(0.4+t):.1f}" '
        f'fill="{rng.choice(["#8E6B47", "#DCBE97", "#7A5A3C"])}" opacity="{rng.uniform(.2, .5):.2f}"/>'
        for t in [rng.random() for _ in range(60)])
    return d, body + edge + grit


def pool(P, rng, ytop=196, ybot=None, cx=250, rx=330):
    """A garden pool: tiled rim, gradient water, ripple rings and caustic glints."""
    ybot = ybot or H + BLEED_BOT
    d = (lin(f"{P}-water", [(0, "#7FD3E8", None), (0.45, "#3FAFD6", None), (1, "#1B7FB0", None)]) +
         lin(f"{P}-rim", [(0, "#FFF6E6", None), (1, "#D9C6AB", None)]))
    cy = (ytop + ybot) / 2 + 22
    ry = (ybot - ytop) / 2 + 30
    body = (f'<ellipse cx="{cx}" cy="{cy:.0f}" rx="{rx}" ry="{ry:.0f}" fill="url(#{P}-rim)"/>'
            f'<ellipse cx="{cx}" cy="{cy-3:.0f}" rx="{rx}" ry="{ry:.0f}" fill="#FFFDF6" opacity=".55" filter="url(#{P}-b2)"/>'
            f'<ellipse cx="{cx}" cy="{cy+4:.0f}" rx="{rx-28}" ry="{ry-16:.0f}" fill="url(#{P}-water)"/>'
            f'<ellipse cx="{cx}" cy="{ytop+16:.0f}" rx="{rx-32}" ry="20" fill="#0E6690" opacity=".22" filter="url(#{P}-b3)"/>')
    ripples = "".join(
        f'<ellipse cx="{rng.uniform(cx-rx+70, cx+rx-70):.0f}" cy="{rng.uniform(ytop+10, ybot-8):.0f}" '
        f'rx="{rng.uniform(10, 30):.0f}" ry="{rng.uniform(2, 5):.0f}" fill="none" stroke="#DFF6FF" '
        f'stroke-width="{rng.uniform(.8, 1.6):.1f}" opacity="{rng.uniform(.14, .34):.2f}"/>' for _ in range(20))
    glint = (f'<ellipse cx="330" cy="{ytop+16:.0f}" rx="120" ry="16" fill="#EAFBFF" opacity=".35" filter="url(#{P}-b3)"/>')
    return d, body + glint + ripples


def splash(P, rng, x, y, s=1.0):
    """A crown of water plus flying droplets."""
    d = lin(f"{P}-spl", [(0, "#FFFFFF", None), (0.55, "#CFF1FB", None), (1, "#7FD3E8", None)])
    arms = []
    for i in range(9):
        a = math.pi + (i / 8.0) * math.pi          # upward fan
        ln = s * (34 + rng.uniform(-10, 18))
        ex, ey = x + math.cos(a) * ln * 1.5, y + math.sin(a) * ln
        w = s * rng.uniform(5, 11)
        arms.append(f'<path d="M{x - w:.0f},{y:.0f} Q{(x+ex)/2:.0f},{(y+ey)/2 - 6:.0f} {ex:.0f},{ey:.0f} '
                    f'Q{(x+ex)/2 + 5:.0f},{(y+ey)/2 + 2:.0f} {x + w:.0f},{y:.0f} Z" fill="url(#{P}-spl)" opacity=".82"/>')
    drops = []
    for _ in range(13):
        a = math.pi + rng.random() * math.pi
        r = rng.uniform(34, 70) * s
        dx, dy = x + math.cos(a) * r * 1.35, y + math.sin(a) * r * .78
        rr = rng.uniform(1.8, 4.4) * s
        drops.append(f'<ellipse cx="{dx:.0f}" cy="{dy:.0f}" rx="{rr:.1f}" ry="{rr*1.7:.1f}" '
                     f'fill="#EAF9FF" opacity="{rng.uniform(.55, .95):.2f}"/>')
    drops = "".join(drops)
    base = (f'<ellipse cx="{x:.0f}" cy="{y+4:.0f}" rx="{62*s:.0f}" ry="{14*s:.0f}" fill="#FFFFFF" opacity=".55" filter="url(#{P}-b2)"/>')
    return d, base + "".join(arms) + drops


def thorn(P, x, ybase, h=46, flip=False):
    """A long needle-thorn stuck point-up in the ground: narrow base, hard taper,
    a lit edge on the sunward side and a dark seat where it enters the soil."""
    gid = f"{P}-thorn{int(x)}{int(ybase)}"
    d = lin(gid, [(0, "#A9713F", None), (0.35, "#6B3D22", None), (1, "#22120A", None)], x1=1, y1=0, x2=0, y2=0.5)
    w = h * 0.155
    lean = h * (0.20 if not flip else -0.20)
    tipx, tipy = x + lean, ybase - h
    body = (f'<path d="M{x - w:.1f},{ybase:.1f} '
            f'C{x - w*.75:.1f},{ybase - h*.45:.1f} {tipx - w*.30:.1f},{ybase - h*.80:.1f} {tipx:.1f},{tipy:.1f} '
            f'C{x + w*.62:.1f},{ybase - h*.72:.1f} {x + w*.92:.1f},{ybase - h*.36:.1f} {x + w:.1f},{ybase:.1f} Z" '
            f'fill="url(#{gid})"/>'
            f'<path d="M{x + w*.42:.1f},{ybase - h*.06:.1f} C{x + w*.55:.1f},{ybase - h*.42:.1f} '
            f'{tipx + w*.12:.1f},{ybase - h*.74:.1f} {tipx:.1f},{tipy + h*.04:.1f}" '
            f'stroke="#E0AE7C" stroke-width="{max(.9, w*.34):.1f}" fill="none" opacity=".55" stroke-linecap="round"/>'
            f'<ellipse cx="{x-1:.0f}" cy="{ybase+1:.0f}" rx="{w*1.7:.1f}" ry="{w*.55:.1f}" fill="#24461F" '
            f'opacity=".50" filter="url(#{P}-b2)"/>')
    return d, body


def car(P, x, ybase, w=210, body_col="#E85D5D", dark="#A32F35", light="#FF9A8E", plate=None):
    """A little round car, drawn IN FRONT of its passengers so they sit in it."""
    gid = f"{P}-car{int(x)}"
    d = (rad(gid, [(0, light, None), (0.42, body_col, None), (1, dark, None)], cx="66%", cy="22%", r="92%") +
         lin(f"{gid}-w", [(0, "#DCF2FA", None), (1, "#8FBACB", None)]) +
         rad(f"{gid}-t", [(0, "#5B5B62", None), (0.6, "#2E2E33", None), (1, "#141416", None)], cx="60%", cy="30%", r="80%"))
    h = w * 0.30
    r_ = w * 0.115
    wheel = lambda cx: (f'<circle cx="{cx:.0f}" cy="{ybase - r_*.28:.0f}" r="{r_:.1f}" fill="url(#{gid}-t)"/>'
                        f'<circle cx="{cx:.0f}" cy="{ybase - r_*.28:.0f}" r="{r_*.42:.1f}" fill="#C9CDD4"/>'
                        f'<circle cx="{cx - r_*.12:.0f}" cy="{ybase - r_*.38:.0f}" r="{r_*.2:.1f}" fill="#EEF1F5"/>')
    body = (
        f'<ellipse cx="{x - w*.06:.0f}" cy="{ybase + 4:.0f}" rx="{w*.62:.0f}" ry="{h*.30:.0f}" fill="#1F4020" opacity=".40" filter="url(#{P}-b3)"/>'
        + wheel(x - w*.30) + wheel(x + w*.30) +
        f'<path d="M{x - w/2:.0f},{ybase - h*.30:.0f} Q{x - w*.52:.0f},{ybase - h*1.05:.0f} {x - w*.30:.0f},{ybase - h*1.12:.0f} '
        f'L{x + w*.28:.0f},{ybase - h*1.12:.0f} Q{x + w*.53:.0f},{ybase - h*1.02:.0f} {x + w/2:.0f},{ybase - h*.30:.0f} '
        f'Q{x + w*.5:.0f},{ybase - h*.02:.0f} {x + w*.40:.0f},{ybase - h*.02:.0f} '
        f'L{x - w*.40:.0f},{ybase - h*.02:.0f} Q{x - w*.5:.0f},{ybase - h*.02:.0f} {x - w/2:.0f},{ybase - h*.30:.0f} Z" fill="url(#{gid})"/>'
        f'<path d="M{x - w*.44:.0f},{ybase - h*.52:.0f} Q{x:.0f},{ybase - h*.30:.0f} {x + w*.44:.0f},{ybase - h*.52:.0f}" '
        f'stroke="{dark}" stroke-width="{w*.012:.1f}" fill="none" opacity=".45"/>'
        f'<ellipse cx="{x + w*.18:.0f}" cy="{ybase - h*.92:.0f}" rx="{w*.22:.0f}" ry="{h*.18:.0f}" fill="#FFFFFF" opacity=".35" filter="url(#{P}-b2)"/>'
        f'<ellipse cx="{x - w*.30:.0f}" cy="{ybase - h*.30:.0f}" rx="{w*.24:.0f}" ry="{h*.34:.0f}" fill="{dark}" opacity=".35" filter="url(#{P}-b3)"/>'
        f'<circle cx="{x + w*.44:.0f}" cy="{ybase - h*.55:.0f}" r="{w*.045:.1f}" fill="#FFF3C4"/>'
        f'<circle cx="{x + w*.44:.0f}" cy="{ybase - h*.55:.0f}" r="{w*.022:.1f}" fill="#FFFFFF"/>'
        # door seam, wheel arches and bumper - the details that say "car"
        f'<path d="M{x - w*.02:.0f},{ybase - h*1.10:.0f} L{x - w*.06:.0f},{ybase - h*.16:.0f}" '
        f'stroke="{dark}" stroke-width="{w*.010:.1f}" fill="none" opacity=".45"/>'
        f'<circle cx="{x - w*.02:.0f}" cy="{ybase - h*.62:.0f}" r="{w*.022:.1f}" fill="#FFF0C8" opacity=".9"/>'
        f'<path d="M{x - w*.44:.0f},{ybase - h*.30:.0f} q{w*.14:.0f},{-h*.34:.0f} {w*.28:.0f},0" '
        f'stroke="{dark}" stroke-width="{w*.014:.1f}" fill="none" opacity=".40"/>'
        f'<path d="M{x + w*.16:.0f},{ybase - h*.30:.0f} q{w*.14:.0f},{-h*.34:.0f} {w*.28:.0f},0" '
        f'stroke="{dark}" stroke-width="{w*.014:.1f}" fill="none" opacity=".40"/>'
        f'<path d="M{x - w*.42:.0f},{ybase - h*.16:.0f} L{x + w*.42:.0f},{ybase - h*.16:.0f}" '
        f'stroke="#F3F5F7" stroke-width="{w*.030:.1f}" opacity=".6" stroke-linecap="round"/>')
    return d, body
