"""Flat character library for the in-story page illustrations.

Every story page currently redraws its characters from scratch, so they drift: the
rabbit in story 01 has pink inner ears, blush and a highlight in each eye, and the
rabbit in story 06 is a plain shape with a dot for a mouth. Same character, six
stories, no shared source. These functions are that shared source.

The characters are drawn FRONT-FACING, which is what the existing pages do and what
reads best for a two-year-old - a face pointed at the reader. So there is no mirror
and no lighting direction to respect: attention is directed with `look` (which way
the pupils go) and the limbs are swung wherever the scene needs them. That is also
why this is the right fidelity for interior pages - a character of twenty flat shapes
can be re-posed, seated in a car or laid in a bed for a few hundred bytes, which the
generated-texture portraits in tools/portraits cannot do at any price.

Coordinates are local to each character: the origin is the point on the GROUND
between its feet, and y runs negative upwards. `s` scales around that point, so a
character always stands on the ground line you place it on.

    rabbit(138, 350, expr='cross', arm=(-40, -46), look=(.4, 0))
"""
import math

INK = "#2D3748"
R_BODY, R_LINE, R_EAR, R_NOSE = "#F0E8DC", "#D0C8B8", "#FFB3C6", "#FF9BAE"
E_BODY, E_LINE, E_EAR = "#A8C0CC", "#88A0AC", "#C5D8E0"
B_BODY, B_LINE, B_MUZZ, B_NOSE = "#C89A72", "#A87A52", "#EAD1B0", "#5C3A21"
# Squirrel and Giraffe take their colours from the portrait generators, which are the
# canonical palettes (tools/portraits/squirrel.py, giraffe.py) - so the flat pages and
# the characters.html portraits stay the same animal.
Q_BODY, Q_LINE, Q_LIGHT, Q_COAT = "#A2683F", "#5A3A1E", "#D4956C", "#FAF8F4"
N_BODY, N_LINE, N_PATCH, N_MUZ = "#E8C078", "#B98B3E", "#B0762F", "#FFEFC4"
# Dr. Sheep: cream fleece, slate face/ears/legs (tools/portraits/sheep.py). Her face is
# too dark for INK features, so her brows and mouth are drawn in pale wool instead.
S_WOOL, S_WLINE, S_WSHADE, S_FACE, S_FLINE, S_DARK = "#F6F2EA", "#CFC6B2", "#E4DCCB", "#4A5364", "#333A47", "#2A313D"
S_SCOPE = "#3C90AE"   # stethoscope: blue, so it never reads as one of her slate arms
MEDRED = "#E4453F"
BLUSH = "#FFB3C6"


# ---------------------------------------------------------------- expressions
# Each entry is (brow, mouth, lid) where brow and mouth are drawn relative to the
# muzzle centre and scaled to the character's eye spacing, so one table serves every
# character regardless of how big its head is.
EXPR = {
    'calm':      dict(brow=None,       mouth='smile',  lid=0),
    'happy':     dict(brow=None,       mouth='grin',   lid=0,   blush=True),
    'cross':     dict(brow='cross',    mouth='flat',   lid=.18),
    'shout':     dict(brow='cross',    mouth='open',   lid=0),
    'surprised': dict(brow='raised',   mouth='oh',     lid=-.2),
    'sad':       dict(brow='worried',  mouth='frown',  lid=.12),
    'worried':   dict(brow='worried',  mouth='wavy',   lid=.1),
    'sleepy':    dict(brow=None,       mouth='smile',  lid=.9),
    'hurt':      dict(brow='worried',  mouth='open',   lid=.3),
    # story 01 turns on these two: Elephant is sly, then caught
    'excited':   dict(brow='raised',   mouth='open',   lid=-.12, blush=True),
    'sneaky':    dict(brow='cross',    mouth='grin',   lid=.26),
    'guilty':    dict(brow='worried',  mouth='flat',   lid=.16, blush=True),
}


def _eyes(cy, dx, r, expr, look):
    """Both eyes, with the pupil steered by `look` so characters can attend to
    each other or to the thing the sentence is about."""
    e = EXPR[expr]
    lx, ly = look
    out = []
    for sx in (-1, 1):
        x = sx * dx
        if e['lid'] >= .85:                                  # asleep: a lash line
            out.append(f'<path d="M{x-r:.1f},{cy:.1f} q{r:.1f},{r*.9:.1f} {r*2:.1f},0" '
                       f'stroke="{INK}" stroke-width="{max(1.6, r*.34):.1f}" fill="none" stroke-linecap="round"/>')
            continue
        out.append(f'<circle cx="{x:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="#fff" stroke="{INK}" stroke-width="1"/>'
                   f'<circle cx="{x + lx*r*.42:.1f}" cy="{cy + ly*r*.42:.1f}" r="{r*.8:.1f}" fill="{INK}"/>'
                   f'<circle cx="{x + lx*r*.42 + r*.24:.1f}" cy="{cy + ly*r*.42 - r*.26:.1f}" '
                   f'r="{r*.26:.1f}" fill="#fff"/>')
        if e['lid'] > 0:
            # `lid` is the fraction of the eye the upper lid covers. It used to be a
            # half-disc bulging downwards, which ate 60% of the eye at lid=.18 and
            # turned every cross or sad face into a squint.
            yt = cy - r + 2*r*e['lid']
            out.append(f'<path d="M{x-r-1:.1f},{cy-r-1:.1f} L{x-r-1:.1f},{yt:.1f} '
                       f'Q{x:.1f},{yt + r*.42:.1f} {x+r+1:.1f},{yt:.1f} L{x+r+1:.1f},{cy-r-1:.1f} Z" '
                       f'fill="{INK}" opacity=".92"/>')
    return "".join(out)


def _brow(kind, cy, dx, r, ink=INK):
    if not kind:
        return ""
    w, lift = r * 1.15, r * .55
    d = []
    for sx in (-1, 1):
        x = sx * dx
        inner, outer = (x - sx*w, x + sx*w)   # inner = the end nearer the muzzle
        if kind == 'raised':
            a, b = cy - lift*1.7, cy - lift*1.7
        elif kind == 'worried':
            a, b = cy - lift*2.0, cy - lift*.5      # inner end up
        else:                                        # cross: inner end down
            a, b = cy - lift*.4, cy - lift*2.0
        d.append(f'M{inner:.1f},{a:.1f} Q{x:.1f},{min(a, b)-lift*.7:.1f} {outer:.1f},{b:.1f}')
    return (f'<path d="{" ".join(d)}" stroke="{ink}" stroke-width="{max(1.8, r*.38):.1f}" '
            f'fill="none" stroke-linecap="round"/>')


def _mouth(kind, cy, w, ink=INK):
    return _mouth_ink(kind, cy, w).replace(INK, ink)


def _mouth_ink(kind, cy, w):
    if kind == 'smile':
        return f'<path d="M{-w*.5:.1f},{cy:.1f} Q0,{cy+w*.42:.1f} {w*.5:.1f},{cy:.1f}" stroke="{INK}" stroke-width="2.3" fill="none" stroke-linecap="round"/>'
    if kind == 'grin':
        return (f'<path d="M{-w*.5:.1f},{cy-w*.06:.1f} Q0,{cy+w*.54:.1f} {w*.5:.1f},{cy-w*.06:.1f} Z" fill="#4A3A44"/>'
                f'<path d="M{-w*.24:.1f},{cy+w*.26:.1f} Q0,{cy+w*.46:.1f} {w*.24:.1f},{cy+w*.26:.1f} Z" fill="{R_NOSE}" opacity=".8"/>')
    if kind == 'flat':
        return f'<path d="M{-w*.42:.1f},{cy:.1f} L{w*.42:.1f},{cy:.1f}" stroke="{INK}" stroke-width="2.3" stroke-linecap="round"/>'
    if kind == 'frown':
        return f'<path d="M{-w*.5:.1f},{cy+w*.3:.1f} Q0,{cy-w*.22:.1f} {w*.5:.1f},{cy+w*.3:.1f}" stroke="{INK}" stroke-width="2.3" fill="none" stroke-linecap="round"/>'
    if kind == 'wavy':
        return f'<path d="M{-w*.5:.1f},{cy:.1f} q{w*.25:.1f},{-w*.24:.1f} {w*.5:.1f},0 q{w*.25:.1f},{w*.24:.1f} {w*.5:.1f},0" stroke="{INK}" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
    if kind == 'oh':
        return f'<ellipse cx="0" cy="{cy+w*.16:.1f}" rx="{w*.24:.1f}" ry="{w*.3:.1f}" fill="{INK}"/>'
    # open - a shout, a wail, or an excited "I'm SO hungry!". A tall pure-black
    # oval reads as horror, so keep it wider than it is tall and warm it up.
    return (f'<ellipse cx="0" cy="{cy+w*.18:.1f}" rx="{w*.34:.1f}" ry="{w*.32:.1f}" fill="#4A3A44"/>'
            f'<ellipse cx="0" cy="{cy+w*.30:.1f}" rx="{w*.22:.1f}" ry="{w*.16:.1f}" fill="{R_NOSE}" opacity=".85"/>')


def _limb(x0, y0, dx, dy, color, line, w, bow=.28):
    """A rolled arm, trunk or leg: one stroked curve with a thinner outline over it,
    which is how the existing pages draw every limb."""
    mx, my = x0 + dx*.5 - dy*bow, y0 + dy*.5 + dx*bow
    d = f'M{x0:.1f},{y0:.1f} Q{mx:.1f},{my:.1f} {x0+dx:.1f},{y0+dy:.1f}'
    return (f'<path d="{d}" stroke="{color}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="{line}" stroke-width="1.5" fill="none" stroke-linecap="round"/>')



def _wrap(x, y, s, inner):
    t = f'translate({x},{y})' + (f' scale({s})' if s != 1 else '')
    return f'<g transform="{t}">{inner}</g>'


# ---------------------------------------------------------------- poses
# A pose is geometry, not a new drawing. `seated` drops the legs and shortens the
# body so a car door or a desk crops it; `lie` swings the body out sideways and rests
# the head where a pillow goes, ears flopped back. Between them, `stand`, `sit`,
# `seated` and `lie` cover every staging the six stories actually use.
#
#   body = (cx, cy, rx, ry)   head = (cx, cy)   ear = y of the ear centres
# Each character keeps its own table: an elephant and a rabbit are different shapes,
# and one shared table for both would only be a table of exceptions.
R_POSE = {
    'stand':  dict(body=(0, -46, 30, 38), head=(0, -110), ear=-154, feet=True,  ears=(-10, 12)),
    'sit':    dict(body=(0, -40, 32, 34), head=(0, -100), ear=-144, feet=False, ears=(-10, 12)),
    'seated': dict(body=(0, -30, 27, 31), head=(0, -86),  ear=-128, feet=False, ears=(-9, 11)),
    'lie':    dict(body=(50, -26, 54, 26), head=(0, -38), ear=-72,  feet=False, ears=(-72, -46)),
}
E_POSE = {
    'stand':  dict(body=(0, -48, 42, 38), head=(0, -100), ear=-110, feet=True),
    'sit':    dict(body=(0, -42, 44, 34), head=(0, -92),  ear=-102, feet=False),
    'seated': dict(body=(0, -32, 36, 32), head=(0, -84),  ear=-94,  feet=False),
    'lie':    dict(body=(58, -28, 58, 28), head=(0, -44), ear=-54,  feet=False),
}
B_POSE = {
    'stand':  dict(body=(0, -46, 32, 38), head=(0, -108), ear=-126, feet=True),
    'sit':    dict(body=(0, -40, 34, 34), head=(0, -98),  ear=-116, feet=False),
    'seated': dict(body=(0, -30, 28, 31), head=(0, -86),  ear=-104, feet=False),
    'lie':    dict(body=(54, -26, 56, 26), head=(0, -38), ear=-56,  feet=False),
}
Q_POSE = {
    'stand':  dict(body=(0, -40, 26, 32), head=(0, -88), ear=-104, feet=True),
    'sit':    dict(body=(0, -34, 28, 29), head=(0, -80), ear=-96,  feet=False),
    'seated': dict(body=(0, -26, 23, 27), head=(0, -70), ear=-86,  feet=False),
}
N_POSE = {
    'stand':  dict(body=(0, -52, 33, 40), head=(9, -142), ear=-162, feet=True),
    'sit':    dict(body=(0, -46, 35, 36), head=(9, -130), ear=-150, feet=False),
    'seated': dict(body=(0, -32, 28, 31), head=(7, -110), ear=-130, feet=False),
}
S_POSE = {
    'stand':  dict(body=(0, -58, 38, 32), head=(0, -104), ear=-108, feet=True),
    'sit':    dict(body=(0, -36, 40, 30), head=(0, -84),  ear=-88,  feet=False),
    'seated': dict(body=(0, -30, 32, 28), head=(0, -76),  ear=-80,  feet=False),
}


# ---------------------------------------------------------------- characters
def rabbit(x, y, s=1.0, expr='calm', look=(0, 0), arm=None, arm2=None,
           ears=None, pose='stand', extra=""):
    """Rabbit. `arm`/`arm2` are (dx, dy) offsets from the shoulder in local units:
    (-32, -46) throws a paw up and back, (46, -10) reaches forward."""
    e, g = EXPR[expr], R_POSE[pose]
    (bx, by, brx, bry), (hx, hy) = g['body'], g['head']
    ears = ears or g['ears']
    p = []
    for sx, rot in zip((-1, 1), ears):
        ex = hx + sx * 8
        p.append(f'<g transform="rotate({rot} {ex} {g["ear"]+16})">'
                 f'<ellipse cx="{ex}" cy="{g["ear"]}" rx="9" ry="27" fill="{R_BODY}" stroke="{R_LINE}" stroke-width="1.5"/>'
                 f'<ellipse cx="{ex}" cy="{g["ear"]+3}" rx="5" ry="21" fill="{R_EAR}"/></g>')
    # body first, then the limbs OVER it - a paw or a foot drawn behind the belly
    # simply disappears
    p.append(f'<ellipse cx="{bx}" cy="{by}" rx="{brx}" ry="{bry}" fill="{R_BODY}" stroke="{R_LINE}" stroke-width="1.5"/>')
    for i, a in enumerate((arm, arm2)):
        if a:
            p.append(_limb(bx + (-24 if i == 0 else 24), by - 14, a[0], a[1], R_BODY, R_LINE, 11))
    if g['feet']:
        p += [f'<ellipse cx="-18" cy="-8" rx="16" ry="10" fill="{R_BODY}" stroke="{R_LINE}" stroke-width="1.5" transform="rotate(-16 -18 -8)"/>',
              f'<ellipse cx="18" cy="-6" rx="16" ry="10" fill="{R_BODY}" stroke="{R_LINE}" stroke-width="1.5" transform="rotate(10 18 -6)"/>']
    p.append(f'<circle cx="{hx}" cy="{hy}" r="28" fill="{R_BODY}" stroke="{R_LINE}" stroke-width="1.5"/>')
    if e.get('blush'):
        p += [f'<ellipse cx="{hx+sx*19}" cy="{hy+8}" rx="7" ry="4.5" fill="{BLUSH}" opacity=".55"/>' for sx in (-1, 1)]
    p += [f'<g transform="translate({hx},{hy})">',
          _brow(e['brow'], -14, 11, 6), _eyes(-6, 11, 6, expr, look),
          f'<ellipse cx="0" cy="6" rx="4" ry="3" fill="{R_NOSE}"/>',
          _mouth(e['mouth'], 18, 18), '</g>']
    return _wrap(x, y, s, "".join(p) + extra)


def elephant(x, y, s=1.0, expr='calm', look=(0, 0), trunk=(-30, 40), arm=None,
             pose='stand', extra=""):
    """Elephant. `trunk` is where the tip of the trunk lands, from under the head."""
    e, g = EXPR[expr], E_POSE[pose]
    (bx, by, brx, bry), (hx, hy) = g['body'], g['head']
    p = [f'<ellipse cx="{hx+sx*30}" cy="{g["ear"]}" rx="23" ry="33" fill="{E_EAR}" stroke="{E_LINE}" stroke-width="1.5"/>'
         for sx in (-1, 1)]
    p.append(f'<ellipse cx="{bx}" cy="{by}" rx="{brx}" ry="{bry}" fill="{E_BODY}" stroke="{E_LINE}" stroke-width="1.5"/>')
    if arm:
        p.append(_limb(bx + 26, by - 10, arm[0], arm[1], E_BODY, E_LINE, 14))
    if g['feet']:
        p += [f'<ellipse cx="{sx*24}" cy="-12" rx="20" ry="12" fill="{E_BODY}" stroke="{E_LINE}" stroke-width="1.5"/>'
              for sx in (-1, 1)]
    p.append(f'<circle cx="{hx}" cy="{hy}" r="40" fill="{E_BODY}" stroke="{E_LINE}" stroke-width="1.5"/>')
    if e.get('blush'):
        p += [f'<ellipse cx="{hx+sx*27}" cy="{hy+10}" rx="8" ry="5" fill="{BLUSH}" opacity=".45"/>' for sx in (-1, 1)]
    p += [f'<g transform="translate({hx},{hy})">',
          _brow(e['brow'], -18, 12, 7), _eyes(-8, 12, 7, expr, look),
          _limb(trunk[0]*.42, 20, trunk[0]*.72, trunk[1], E_BODY, E_LINE, 15, bow=.2),
          _mouth(e['mouth'], 16, 22), '</g>']
    return _wrap(x, y, s, "".join(p) + extra)


def bear(x, y, s=1.0, expr='calm', look=(0, 0), arm=None, arm2=None,
         pose='stand', extra=""):
    """Bear. Round ears on top of the head and a pale muzzle carrying the nose."""
    e, g = EXPR[expr], B_POSE[pose]
    (bx, by, brx, bry), (hx, hy) = g['body'], g['head']
    p = [f'<ellipse cx="{hx+sx*15}" cy="{g["ear"]}" rx="10" ry="9.5" fill="{B_BODY}" stroke="{B_LINE}" stroke-width="1.5"/>'
         for sx in (-1, 1)]
    p.append(f'<ellipse cx="{bx}" cy="{by}" rx="{brx}" ry="{bry}" fill="{B_BODY}" stroke="{B_LINE}" stroke-width="1.5"/>')
    for i, a in enumerate((arm, arm2)):
        if a:
            p.append(_limb(bx + (-26 if i == 0 else 26), by - 12, a[0], a[1], B_BODY, B_LINE, 12))
    if g['feet']:
        p += [f'<ellipse cx="{sx*19}" cy="-8" rx="17" ry="11" fill="{B_BODY}" stroke="{B_LINE}" stroke-width="1.5"/>'
              for sx in (-1, 1)]
    p.append(f'<circle cx="{hx}" cy="{hy}" r="28" fill="{B_BODY}" stroke="{B_LINE}" stroke-width="1.5"/>')
    if e.get('blush'):
        p += [f'<ellipse cx="{hx+sx*20}" cy="{hy+8}" rx="7" ry="4.5" fill="{BLUSH}" opacity=".45"/>' for sx in (-1, 1)]
    p += [f'<g transform="translate({hx},{hy})">',
          _brow(e['brow'], -13, 11, 6), _eyes(-6, 11, 6, expr, look),
          f'<ellipse cx="0" cy="9" rx="12" ry="8.5" fill="{B_MUZZ}" stroke="{B_LINE}" stroke-width="1.3"/>',
          f'<ellipse cx="0" cy="5.5" rx="3.6" ry="3" fill="{B_NOSE}"/>',
          _mouth(e['mouth'], 15, 16), '</g>']
    return _wrap(x, y, s, "".join(p) + extra)


def _pose_of(table, pose, who):
    try:
        return table[pose]
    except KeyError:
        raise ValueError(f"{who} has no {pose!r} pose; it has {sorted(table)}") from None


def squirrel(x, y, s=1.0, expr='calm', look=(0, 0), arm=None, arm2=None,
             pose='stand', coat=True, extra=""):
    """Dr. Squirrel - small, big tail, and a white coat when she is on duty."""
    e, g = EXPR[expr], _pose_of(Q_POSE, pose, 'squirrel')
    (bx, by, brx, bry), (hx, hy) = g['body'], g['head']
    body_fill = Q_COAT if coat else Q_BODY
    p = [  # tail: a fat curl behind her, drawn first so it reads as further away
        f'<path d="M{bx+brx*.62:.0f},{by+14:.0f} '
        f'C{bx+brx+34:.0f},{by+10:.0f} {bx+brx+40:.0f},{by-56:.0f} {bx+8:.0f},{by-64:.0f} '
        f'C{bx+brx+24:.0f},{by-44:.0f} {bx+brx+22:.0f},{by-4:.0f} {bx+brx*.62:.0f},{by+14:.0f} Z" '
        f'fill="{Q_LIGHT}" stroke="{Q_LINE}" stroke-width="1.5"/>']
    p += [f'<path d="M{hx+sx*13},{g["ear"]+8} q{sx*3},-16 {sx*11},-14 q-2,10 -4,16 Z" '
          f'fill="{Q_BODY}" stroke="{Q_LINE}" stroke-width="1.4"/>' for sx in (-1, 1)]
    p.append(f'<ellipse cx="{bx}" cy="{by}" rx="{brx}" ry="{bry}" fill="{body_fill}" stroke="{Q_LINE}" stroke-width="1.5"/>')
    if coat:
        p.append(f'<path d="M{bx-6},{by-bry+4} l0,{bry*1.4:.0f}" stroke="{Q_LINE}" stroke-width="1.2" opacity=".55"/>'
                 f'<circle cx="{bx+brx*.52:.0f}" cy="{by-6}" r="5" fill="{MEDRED}" opacity=".9"/>')
    for i, a in enumerate((arm, arm2)):
        if a:
            p.append(_limb(bx + (-19 if i == 0 else 19), by - 10, a[0], a[1], body_fill, Q_LINE, 9))
    if g['feet']:
        p += [f'<ellipse cx="{sx*13}" cy="-6" rx="12" ry="8" fill="{Q_BODY}" stroke="{Q_LINE}" stroke-width="1.4"/>'
              for sx in (-1, 1)]
    p.append(f'<circle cx="{hx}" cy="{hy}" r="24" fill="{Q_BODY}" stroke="{Q_LINE}" stroke-width="1.5"/>')
    if e.get('blush'):
        p += [f'<ellipse cx="{hx+sx*16}" cy="{hy+7}" rx="6" ry="4" fill="{BLUSH}" opacity=".5"/>' for sx in (-1, 1)]
    p += [f'<g transform="translate({hx},{hy})">',
          _brow(e['brow'], -12, 9, 5.4), _eyes(-5, 9, 5.4, expr, look),
          f'<ellipse cx="0" cy="8" rx="10" ry="7" fill="{Q_LIGHT}" stroke="{Q_LINE}" stroke-width="1.2"/>',
          f'<ellipse cx="0" cy="4.5" rx="3" ry="2.5" fill="{Q_LINE}"/>',
          _mouth(e['mouth'], 14, 14), '</g>']
    return _wrap(x, y, s, "".join(p) + extra)


def giraffe(x, y, s=1.0, expr='calm', look=(0, 0), arm=None, pose='stand',
            cap=True, extra=""):
    """Nurse Giraffe - the neck is the character, so it is a limb, not an ellipse."""
    e, g = EXPR[expr], _pose_of(N_POSE, pose, 'giraffe')
    (bx, by, brx, bry), (hx, hy) = g['body'], g['head']
    p = [f'<ellipse cx="{bx}" cy="{by}" rx="{brx}" ry="{bry}" fill="{N_BODY}" stroke="{N_LINE}" stroke-width="1.5"/>']
    p += [f'<ellipse cx="{bx+dx}" cy="{by+dy}" rx="9" ry="7" fill="{N_PATCH}" opacity=".55"/>'
          for dx, dy in ((-14, -8), (10, 4), (-4, 16), (18, -12))]
    if arm:
        p.append(_limb(bx + 18, by - 8, arm[0], arm[1], N_BODY, N_LINE, 11))
    if g['feet']:
        p += [f'<ellipse cx="{sx*15}" cy="-7" rx="12" ry="9" fill="{N_BODY}" stroke="{N_LINE}" stroke-width="1.4"/>'
              for sx in (-1, 1)]
    neck_y = by - bry + 6
    p.append(_limb(bx, neck_y, hx - bx, hy - neck_y - 4, N_BODY, N_LINE, 24, bow=.05))
    p += [f'<ellipse cx="{bx + (hx-bx)*t:.0f}" cy="{neck_y + (hy-neck_y)*t:.0f}" rx="6" ry="5" '
          f'fill="{N_PATCH}" opacity=".5"/>' for t in (.24, .52, .78)]
    p += [f'<path d="M{hx+sx*7},{g["ear"]+6} l{sx*2},-11" stroke="{N_LINE}" stroke-width="2.6" stroke-linecap="round"/>'
          f'<circle cx="{hx+sx*9}" cy="{g["ear"]-6}" r="3.4" fill="{N_PATCH}"/>' for sx in (-1, 1)]
    p.append(f'<ellipse cx="{hx}" cy="{hy}" rx="20" ry="22" fill="{N_BODY}" stroke="{N_LINE}" stroke-width="1.5"/>')
    if cap:
        p.append(f'<path d="M{hx-18},{hy-17} q18,-13 36,0 l0,-9 q-18,-11 -36,0 Z" fill="#fff" stroke="#DCD2C0" stroke-width="1.3"/>'
                 f'<rect x="{hx-2.5:.0f}" y="{hy-25}" width="5" height="10" rx="1" fill="{MEDRED}"/>'
                 f'<rect x="{hx-6:.0f}" y="{hy-21.5}" width="12" height="4.5" rx="1" fill="{MEDRED}"/>')
    if e.get('blush'):
        p += [f'<ellipse cx="{hx+sx*14}" cy="{hy+7}" rx="6" ry="4" fill="{BLUSH}" opacity=".5"/>' for sx in (-1, 1)]
    p += [f'<g transform="translate({hx},{hy})">',
          _brow(e['brow'], -11, 8, 5), _eyes(-4, 8, 5, expr, look),
          f'<ellipse cx="0" cy="11" rx="11" ry="8" fill="{N_MUZ}" stroke="{N_LINE}" stroke-width="1.2"/>',
          f'<ellipse cx="-4" cy="9" rx="1.8" ry="1.4" fill="{N_LINE}"/><ellipse cx="4" cy="9" rx="1.8" ry="1.4" fill="{N_LINE}"/>',
          _mouth(e['mouth'], 16, 13), '</g>']
    return _wrap(x, y, s, "".join(p) + extra)


def bandage(x, y, rx=18, ry=12):
    """A wrapped limb - the prop these stories keep needing."""
    return (f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="white" stroke="#D0D0D0" stroke-width="1.5"/>'
            f'<line x1="{x-rx*.8:.0f}" y1="{y-ry*.5:.0f}" x2="{x+rx*.8:.0f}" y2="{y+ry*.5:.0f}" stroke="#B8B8B8" stroke-width="1.5"/>'
            f'<line x1="{x-rx*.8:.0f}" y1="{y+ry*.5:.0f}" x2="{x+rx*.8:.0f}" y2="{y-ry*.5:.0f}" stroke="#B8B8B8" stroke-width="1.5"/>')


def sheep(x, y, s=1.0, expr='calm', look=(0, 0), arm=None, arm2=None, pose='stand',
          scope=True, extra=""):
    """Dr. Sheep - a fleece cloud on slate legs, a slate face under a woolly fringe,
    and a stethoscope, which is what says DOCTOR when the coat is already white.
    Her arms are slate like her legs: hooves, poking out of the fleece."""
    e, g = EXPR[expr], _pose_of(S_POSE, pose, 'sheep')
    (bx, by, brx, bry), (hx, hy) = g['body'], g['head']
    p = []
    if g['feet']:   # legs first, so the fleece overlaps their tops
        p += [f'<rect x="{sx*15-5}" y="{by+bry-16}" width="10" height="{-(by+bry)+10}" rx="5" fill="{S_FACE}"/>'
              f'<ellipse cx="{sx*15}" cy="-5" rx="8.5" ry="5.5" fill="{S_DARK}"/>' for sx in (-1, 1)]
    # the fleece: a core ellipse ringed with puffs, outline on the puffs only so the
    # silhouette reads as scalloped wool rather than one smooth egg
    ring = [(bx + math.cos(a)*(brx-5), by + math.sin(a)*(bry-5))
            for a in (2*math.pi*i/13 + .2 for i in range(13))]
    p += [f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{bry*.42:.1f}" fill="{S_WOOL}" stroke="{S_WLINE}" stroke-width="1.5"/>'
          for cx, cy in ring]
    p.append(f'<ellipse cx="{bx}" cy="{by}" rx="{brx-2}" ry="{bry-2}" fill="{S_WOOL}"/>')
    p += [f'<circle cx="{bx+dx}" cy="{by+dy}" r="{r}" fill="none" stroke="{S_WSHADE}" stroke-width="2.2"/>'
          for dx, dy, r in ((-16, 4, 7), (12, 12, 6), (18, -8, 5), (-4, 16, 5))]
    if scope:   # hangs from the neck, drawn before the head so the head covers the top
        p.append(f'<path d="M{hx-17},{hy+18} Q{hx-20},{by+6} {hx-3},{by+10} Q{hx+14},{by+12} {hx+14},{by-6}" '
                 f'stroke="{S_SCOPE}" stroke-width="3" fill="none" stroke-linecap="round"/>'
                 f'<path d="M{hx+17},{hy+18} Q{hx+19},{by-12} {hx+14},{by-6}" stroke="{S_SCOPE}" stroke-width="3" '
                 f'fill="none" stroke-linecap="round"/>'
                 f'<circle cx="{hx+14}" cy="{by-4}" r="6.5" fill="#C9D3DC" stroke="#7D8A96" stroke-width="2"/>'
                 f'<circle cx="{bx-brx*.46:.0f}" cy="{by+bry*.1:.0f}" r="5.5" fill="{MEDRED}" opacity=".9"/>')
    for i, a in enumerate((arm, arm2)):
        if a:
            ax = bx + (-28 if i == 0 else 28)
            p.append(_limb(ax, by - 6, a[0], a[1], S_FACE, S_FLINE, 9)
                     + f'<ellipse cx="{ax+a[0]:.0f}" cy="{by-6+a[1]:.0f}" rx="5.5" ry="5" fill="{S_DARK}"/>')
    # ears stick out sideways below the fringe, as in the portrait
    p += [f'<ellipse cx="{hx+sx*27}" cy="{g["ear"]}" rx="14" ry="6.5" fill="{S_FACE}" stroke="{S_FLINE}" '
          f'stroke-width="1.4" transform="rotate({sx*16} {hx+sx*27} {g["ear"]})"/>'
          f'<ellipse cx="{hx+sx*29}" cy="{g["ear"]+.5}" rx="8" ry="3" fill="#8C6F7A" opacity=".55" '
          f'transform="rotate({sx*16} {hx+sx*29} {g["ear"]})"/>' for sx in (-1, 1)]
    p.append(f'<ellipse cx="{hx}" cy="{hy}" rx="22" ry="27" fill="{S_FACE}" stroke="{S_FLINE}" stroke-width="1.5"/>')
    if e.get('blush'):
        p += [f'<ellipse cx="{hx+sx*14}" cy="{hy+8}" rx="6" ry="4" fill="{BLUSH}" opacity=".5"/>' for sx in (-1, 1)]
    # woolly fringe across the top of the head
    p += [f'<circle cx="{hx+dx}" cy="{hy+dy}" r="{r}" fill="{S_WOOL}" stroke="{S_WLINE}" stroke-width="1.3"/>'
          for dx, dy, r in ((-14, -24, 10), (14, -24, 10), (0, -30, 11), (-6, -23, 8), (6, -23, 8))]
    p += [f'<g transform="translate({hx},{hy})">',
          _brow(e['brow'], -4, 8.5, 5.2, ink=S_WOOL), _eyes(3, 8.5, 5.2, expr, look),
          # a paler muzzle, so an open mouth or a grin still shows on the slate face
          f'<ellipse cx="0" cy="18" rx="12" ry="8.5" fill="#6B7589"/>',
          f'<ellipse cx="0" cy="13" rx="4.5" ry="3" fill="{S_DARK}"/>',
          _mouth(e['mouth'], 19, 13, ink=S_WOOL), '</g>']
    return _wrap(x, y, s, "".join(p) + extra)


# ---------------------------------------------------------------- the patients
# Story 03's hospital is full of walk-on patients. They each appear once or twice,
# mostly in bed, so they share one body plan - the bear's - and differ only in colour,
# ears, muzzle and one signature feature (antlers, a mane, a brush of a tail). That
# is enough for a two-year-old to say "fox!", and it keeps them visibly the same
# family of drawings as the main cast.
CRITTERS = {
    #          body       line       muzzle     nose       ears
    'pig':  ("#FFC2D1", "#E892AA", "#FF9FB8", "#D8708E", 'flop'),
    'deer': ("#C8905E", "#9A6A3E", "#F0DCC0", "#3A2A20", 'leaf'),
    'fox':  ("#F0873A", "#C0622A", "#FFF6EC", "#2D2A2A", 'point'),
    'wolf': ("#A3ACB6", "#707A86", "#E6EAEE", "#2D3748", 'point'),
    'lion': ("#E8B454", "#B8862E", "#FBE3AE", "#8A4A2A", 'round'),
}


def _critter_ears(kind, style, hx, ey, body, line):
    out = []
    for sx in (-1, 1):
        x = hx + sx*17
        if style == 'flop':        # pig: triangles folded forward over the brow
            out.append(f'<path d="M{x-sx*9},{ey+10} L{x+sx*12},{ey-6} L{x+sx*8},{ey+16} Z" fill="{body}" '
                       f'stroke="{line}" stroke-width="1.5" stroke-linejoin="round"/>')
        elif style == 'leaf':      # deer: long ears straight out to the side
            out.append(f'<ellipse cx="{x+sx*14}" cy="{ey+8}" rx="15" ry="7" fill="{body}" stroke="{line}" '
                       f'stroke-width="1.5" transform="rotate({sx*-20} {x+sx*14} {ey+8})"/>'
                       f'<ellipse cx="{x+sx*15}" cy="{ey+8}" rx="9" ry="3.5" fill="#F0C8B0" '
                       f'transform="rotate({sx*-20} {x+sx*15} {ey+8})"/>')
        elif style == 'point':     # fox and wolf: tall triangles, dark tips on the fox
            tip = "#3A2A22" if kind == 'fox' else line
            out.append(f'<path d="M{x-sx*8},{ey+14} L{x+sx*6},{ey-20} L{x+sx*14},{ey+10} Z" fill="{body}" '
                       f'stroke="{line}" stroke-width="1.5" stroke-linejoin="round"/>'
                       f'<path d="M{x+sx*3},{ey-11} L{x+sx*6},{ey-20} L{x+sx*9},{ey-10} Z" fill="{tip}"/>')
        else:                      # lion: little round ears poking out of the mane
            out.append(f'<circle cx="{x}" cy="{ey}" r="8" fill="{body}" stroke="{line}" stroke-width="1.5"/>')
    return "".join(out)


def critter(kind, x, y, s=1.0, expr='calm', look=(0, 0), arm=None, arm2=None,
            pose='stand', extra=""):
    """A walk-on patient: kind is pig | deer | fox | wolf | lion."""
    body, line, muzz, nose, ears = CRITTERS[kind]
    e, g = EXPR[expr], _pose_of(B_POSE, pose, kind)
    (bx, by, brx, bry), (hx, hy) = g['body'], g['head']
    p = []
    if kind == 'fox':      # the brush, behind everything, white-tipped
        p.append(f'<path d="M{bx+brx*.6:.0f},{by+bry*.5:.0f} q46,-6 40,-54 q-4,-10 -14,-4 q2,34 -30,40 Z" '
                 f'fill="{body}" stroke="{line}" stroke-width="1.5"/>'
                 f'<path d="M{bx+brx*.6+40:.0f},{by+bry*.5-54:.0f} q-4,-10 -14,-4 l2,10 Z" fill="#FFF6EC"/>')
    if kind == 'lion':     # the mane is the lion
        p += [f'<circle cx="{hx + 36*math.cos(a):.1f}" cy="{hy + 36*math.sin(a):.1f}" r="15" fill="#C8702C"/>'
              for a in (2*math.pi*i/12 for i in range(12))]
        p.append(f'<circle cx="{hx}" cy="{hy}" r="38" fill="#C8702C"/>')
    p.append(_critter_ears(kind, ears, hx, g['ear'] + 6, body, line))
    p.append(f'<ellipse cx="{bx}" cy="{by}" rx="{brx}" ry="{bry}" fill="{body}" stroke="{line}" stroke-width="1.5"/>')
    if kind in ('fox', 'wolf'):
        p.append(f'<ellipse cx="{bx}" cy="{by+6}" rx="{brx*.55:.0f}" ry="{bry*.6:.0f}" fill="{muzz}" opacity=".9"/>')
    if kind == 'deer':
        p += [f'<circle cx="{bx+dx}" cy="{by+dy}" r="3.4" fill="#FFF6EC" opacity=".85"/>'
              for dx, dy in ((-14, -10), (-4, -16), (10, -8), (16, 2), (-12, 6))]
    for i, a in enumerate((arm, arm2)):
        if a:
            p.append(_limb(bx + (-26 if i == 0 else 26), by - 12, a[0], a[1], body, line, 12))
    if g['feet']:
        p += [f'<ellipse cx="{sx*19}" cy="-8" rx="15" ry="10" fill="{body}" stroke="{line}" stroke-width="1.5"/>'
              for sx in (-1, 1)]
    if kind == 'deer':     # antlers first, so the head sits over their roots
        p.append(f'<path d="' + " ".join(
            f'M{hx+sx*9},{hy-22} q{sx*4},-16 {sx*14},-26 M{hx+sx*13},{hy-34} q{sx*8},-2 {sx*14},-10 '
            f'M{hx+sx*18},{hy-42} q{-sx*4},-8 {-sx*2},-14' for sx in (-1, 1))
                 + f'" stroke="#8A5A2E" stroke-width="4" fill="none" stroke-linecap="round"/>')
    p.append(f'<circle cx="{hx}" cy="{hy}" r="28" fill="{body}" stroke="{line}" stroke-width="1.5"/>')
    if kind in ('fox', 'wolf'):   # pale cheeks sweeping down to the muzzle
        p.append(f'<path d="M{hx-26},{hy+4} Q{hx-12},{hy+2} {hx},{hy+12} Q{hx+12},{hy+2} {hx+26},{hy+4} '
                 f'Q{hx+18},{hy+26} {hx},{hy+28} Q{hx-18},{hy+26} {hx-26},{hy+4} Z" fill="{muzz}"/>')
    if e.get('blush'):
        p += [f'<ellipse cx="{hx+sx*20}" cy="{hy+8}" rx="7" ry="4.5" fill="{BLUSH}" opacity=".5"/>' for sx in (-1, 1)]
    p += [f'<g transform="translate({hx},{hy})">', _brow(e['brow'], -13, 11, 6), _eyes(-6, 11, 6, expr, look)]
    if kind == 'pig':
        p.append(f'<ellipse cx="0" cy="7" rx="11" ry="8" fill="{muzz}" stroke="{line}" stroke-width="1.3"/>'
                 f'<ellipse cx="-4" cy="7" rx="2.2" ry="3" fill="{nose}"/><ellipse cx="4" cy="7" rx="2.2" ry="3" fill="{nose}"/>')
    elif kind in ('deer', 'lion'):
        p.append(f'<ellipse cx="0" cy="9" rx="12" ry="8.5" fill="{muzz}" stroke="{line}" stroke-width="1.2"/>')
    if kind != 'pig':
        p.append(f'<path d="M-4.5,4 h9 l-4.5,4.5 Z" fill="{nose}" stroke="{nose}" stroke-width="2" stroke-linejoin="round"/>')
    p += [_mouth(e['mouth'], 17 if kind != 'pig' else 19, 15), '</g>']
    return _wrap(x, y, s, "".join(p) + extra)


def tortoise(x, y, s=1.0, expr='calm', look=(0, 0), specs=True, extra=""):
    """Old Tortoise - a domed shell with his head out the front, and his reading
    glasses, because he is OLD Tortoise. Front-facing like everyone else."""
    e = EXPR[expr]
    shell = "#7FAE5A"
    p = [f'<ellipse cx="{sx*30}" cy="-7" rx="13" ry="9" fill="#B8C878" stroke="#8A9A50" stroke-width="1.5"/>'
         for sx in (-1, 1)]
    p.append(f'<path d="M-58,-14 Q-56,-78 0,-80 Q56,-78 58,-14 Z" fill="{shell}" stroke="#4E7A34" stroke-width="2"/>'
             f'<path d="M-60,-14 h120" stroke="#4E7A34" stroke-width="5" stroke-linecap="round"/>'
             f'<path d="M-16,-62 l16,-8 l16,8 v16 l-16,8 l-16,-8 Z M-44,-30 l-10,-18 M44,-30 l10,-18 '
             f'M-16,-46 l-20,10 v14 M16,-46 l20,10 v14" stroke="#4E7A34" stroke-width="2" fill="none" stroke-linejoin="round"/>')
    hx, hy = 0, -30
    p.append(f'<ellipse cx="{hx}" cy="{hy}" rx="21" ry="19" fill="#B8C878" stroke="#8A9A50" stroke-width="1.5"/>')
    if e.get('blush'):
        p += [f'<ellipse cx="{hx+sx*14}" cy="{hy+7}" rx="5" ry="3.5" fill="{BLUSH}" opacity=".55"/>' for sx in (-1, 1)]
    p += [f'<g transform="translate({hx},{hy})">', _brow(e['brow'], -9, 8, 4.6), _eyes(-3, 8, 4.6, expr, look)]
    if specs:
        p.append(f'<circle cx="-8" cy="-3" r="7" fill="none" stroke="#6B5B47" stroke-width="1.6"/>'
                 f'<circle cx="8" cy="-3" r="7" fill="none" stroke="#6B5B47" stroke-width="1.6"/>'
                 f'<path d="M-1,-3 h2" stroke="#6B5B47" stroke-width="1.6"/>')
    p += [_mouth(e['mouth'], 9, 12), '</g>']
    return _wrap(x, y, s, "".join(p) + extra)
