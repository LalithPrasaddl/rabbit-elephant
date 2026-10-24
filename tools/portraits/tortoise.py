import math, random
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from furlib import BPath, cubic, rings, speckle
import common

# Little Tortoise (story 16). No fur at all, so the texture is all in the shell:
# plates laid out as a grid of hexagons clipped to the dome, each with its own
# highlight and growth rings, over a dome shading pass. The head is held up and
# FRONT-FACING out of the front of the shell, like the rest of the cast.
rng = random.Random(1616)
P = "t"
g = lambda i: f"{P}-{i}"
eye = common.make_eye(P, socket="#3E4A22", lidfill="#A9B86A", rimcol="#3E4A22")

S_DEEP, S_BASE, S_LIGHT, S_HI, SEAM = "#2F5320", "#7FAE5A", "#B6D884", "#E2F2B8", "#41692C"
K_DEEP, K_SHADE, K_BASE, K_LIGHT = "#5E6A30", "#8A9A50", "#B8C878", "#DDE6A8"

# ---------------- silhouettes ----------------
shell = (BPath((62, 292))
    .c((58, 214), (106, 136), (188, 132))
    .c((262, 130), (304, 206), (302, 292))
    .c((250, 304), (118, 304), (62, 292)))

rim = (BPath((52, 286))
    .c((120, 300), (248, 300), (310, 286))
    .c((314, 298), (306, 310), (296, 312))
    .c((230, 322), (130, 322), (66, 312))
    .c((54, 310), (48, 298), (52, 286)))

head = (BPath((40, 176))
    .c((40, 140), (64, 122), (90, 122))
    .c((118, 122), (140, 142), (140, 176))
    .c((140, 210), (118, 230), (90, 230))
    .c((62, 230), (40, 210), (40, 176)))

neck = (BPath((70, 214))
    .c((76, 236), (90, 260), (112, 278))
    .c((128, 284), (150, 276), (150, 262))
    .c((132, 244), (122, 222), (118, 206))
    .c((104, 210), (84, 214), (70, 214)))


def leg(x, w=36, top=284, foot=330):
    """A stubby column of a leg with a rounded foot and three toenails."""
    l, r = x - w/2, x + w/2
    return (BPath((l, top))
        .c((l - 2, top + 18), (l - 6, foot - 12), (l - 8, foot - 4))
        .c((l - 6, foot + 4), (r + 6, foot + 4), (r + 8, foot - 4))
        .c((r + 6, foot - 12), (r + 2, top + 18), (r, top))
        .c((r - 8, top - 4), (l + 8, top - 4), (l, top)))


# The legs are scene-space (feet on the 330 baseline); the shell, neck and head are
# lifted and enlarged by LIFT, so the leg tops tuck up under the rim band instead of
# sitting on it - a leg with a flat top drawn over the shell reads as a flowerpot.
LIFT = 'translate(172,300) scale(1.05) translate(-172,-322)'
legs_far = [leg(150, 32, top=278, foot=324), leg(282, 30, top=278, foot=322)]
legs_near = [leg(108, 40, top=278), leg(244, 38, top=278)]


def toes(x, foot=330):
    return "".join(f'<ellipse cx="{x+dx}" cy="{foot-2}" rx="4" ry="3" fill="#F4EED4" opacity=".85"/>' for dx in (-11, 0, 11))


# ---------------- shell plates ----------------
def hexagon(cx, cy, r, sq=.82):
    return " ".join(f'{"M" if i == 0 else "L"}{cx + math.cos(math.pi/6 + i*math.pi/3)*r:.1f} '
                    f'{cy + math.sin(math.pi/6 + i*math.pi/3)*r*sq:.1f}' for i in range(6)) + "Z"


plates = []
R = 34
for row, cy in enumerate((150, 196, 242, 288)):
    off = 0 if row % 2 == 0 else R * .866
    for k in range(-4, 5):
        cx = 186 + k * R * 1.732 + off
        plates.append((cx, cy))

plate_svg = []
for cx, cy in plates:
    plate_svg.append(f'<path d="{hexagon(cx, cy, R-3)}" fill="url(#{g("plate")})" stroke="{SEAM}" stroke-width="3.2" stroke-linejoin="round"/>')
    plate_svg.append(f'<path d="{hexagon(cx, cy, R*.68)}{hexagon(cx, cy, R*.42)}" fill="none" stroke="{S_DEEP}" '
                     f'stroke-width="1.2" opacity=".28"/>')

shell_speck = speckle([dict(ell=(186, 220, 112, 80), n=170, r=(1.2, 3.4),
                            tones=[(S_DEEP, .12), (S_HI, .16), ("#5C8A3C", .14)])], rng)
skin_speck = speckle([dict(ell=(90, 176, 44, 46), n=70, r=(1.2, 2.8), tones=[(K_DEEP, .12), (K_LIGHT, .2)]),
                      dict(ell=(112, 248, 24, 30), n=50, r=(1.2, 3.0), tones=[(K_DEEP, .14), (K_LIGHT, .18)])], rng)
leg_speck = speckle([dict(ell=(x, 306, 16, 18), n=26, r=(1.5, 3.4), tones=[(K_DEEP, .16), (K_LIGHT, .2)])
                     for x in (108, 244)], rng)
NECK = ((92, 222), (100, 246), (116, 266), (138, 272))
neck_rings = rings(cubic(*NECK, 9, .1, .9), lambda t: 22 - 4*t, 9, rng, K_DEEP, .26, 1.4, .3)

defs = f'''
  <radialGradient id="{g('plate')}" cx="36%" cy="30%" r="80%">
    <stop offset="0" stop-color="{S_HI}"/><stop offset="45%" stop-color="{S_LIGHT}"/>
    <stop offset="1" stop-color="{S_BASE}"/>
  </radialGradient>
  <radialGradient id="{g('dome')}" cx="32%" cy="18%" r="90%">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity=".0"/><stop offset="55%" stop-color="{S_DEEP}" stop-opacity=".05"/>
    <stop offset="1" stop-color="{S_DEEP}" stop-opacity=".62"/>
  </radialGradient>
  <linearGradient id="{g('rim')}x" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#6E9A4A"/><stop offset="1" stop-color="#355C24"/>
  </linearGradient>
  <radialGradient id="{g('skin')}" cx="32%" cy="24%" r="86%">
    <stop offset="0" stop-color="#F1F5CC"/><stop offset="40%" stop-color="{K_LIGHT}"/>
    <stop offset="78%" stop-color="{K_BASE}"/><stop offset="1" stop-color="{K_SHADE}"/>
  </radialGradient>
  <radialGradient id="{g('leg')}" cx="30%" cy="24%" r="90%">
    <stop offset="0" stop-color="{K_LIGHT}"/><stop offset="60%" stop-color="{K_BASE}"/>
    <stop offset="1" stop-color="{K_DEEP}"/>
  </radialGradient>
  <clipPath id="{g('cshell')}"><path d="{shell.d()}"/></clipPath>
  <clipPath id="{g('chead')}"><path d="{head.d()}"/></clipPath>
  <clipPath id="{g('cneck')}"><path d="{neck.d()}"/></clipPath>
{common.defs_common(P)}'''

content = f'''
<ellipse cx="184" cy="334" rx="132" ry="14" fill="#2F3A1A" opacity=".30" filter="url(#{g('soft')})"/>

<!-- the far legs, behind and in shadow -->
<g>{"".join(f'<path d="{l.d()}" fill="{K_DEEP}" opacity=".85"/>' for l in legs_far)}</g>

<!-- shell: plates and dome shading, light from the upper left -->
<g transform="{LIFT}">
  <path d="{shell.d()}" fill="{S_BASE}"/>
  <g clip-path="url(#{g('cshell')})">
    {"".join(plate_svg)}
    {shell_speck}
    <path d="{shell.d()}" fill="url(#{g('dome')})"/>
    <ellipse cx="146" cy="160" rx="62" ry="26" fill="#FFFFFF" opacity=".30" filter="url(#{g('soft')})"/>
    <ellipse cx="262" cy="270" rx="56" ry="34" fill="{S_DEEP}" opacity=".30" filter="url(#{g('soft')})"/>
  </g>
  <path d="{shell.d()}" fill="none" stroke="{S_HI}" stroke-width="3" mask="url(#{g('rimmask')})" opacity=".8" filter="url(#{g('soft3')})"/>
</g>

<!-- the near legs, their tops tucked under the rim -->
<g>
  {"".join(f'<path d="{l.d()}" fill="url(#{g("leg")})"/>' for l in legs_near)}
  {leg_speck}
  {toes(108)}{toes(244)}
  <ellipse cx="108" cy="300" rx="24" ry="7" fill="#28461A" opacity=".4" filter="url(#{g('soft2')})"/>
  <ellipse cx="244" cy="300" rx="23" ry="7" fill="#28461A" opacity=".4" filter="url(#{g('soft2')})"/>
</g>

<g transform="{LIFT}">
  <path d="{rim.d()}" fill="url(#{g('rim')}x)"/>
  <path d="M60 292C126 304 248 304 304 292" stroke="#A8CC80" stroke-width="2.4" fill="none" opacity=".6" stroke-linecap="round"/>
  {"".join(f'<path d="M{x} {300 + abs(x-182)*.02:.0f}v12" stroke="#28461A" stroke-width="2" opacity=".35"/>' for x in range(84, 300, 26))}
</g>

<!-- neck out of the front of the shell, with its wrinkles -->
<g transform="{LIFT}">
  <path d="{neck.d()}" fill="url(#{g('skin')})"/>
  <g clip-path="url(#{g('cneck')})">
    {"".join('<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-opacity="%s" stroke-linecap="round"/>' % (d, c, w, o) for c, w, o, d in neck_rings)}
    <ellipse cx="140" cy="262" rx="22" ry="18" fill="{K_DEEP}" opacity=".35" filter="url(#{g('soft2')})"/>
  </g>
</g>

<!-- head: front-facing, both eyes either side of the little beak -->
<g transform="{LIFT}">
  <path d="{head.d()}" fill="url(#{g('skin')})"/>
  <g clip-path="url(#{g('chead')})">
    {skin_speck}
    <ellipse cx="72" cy="140" rx="34" ry="16" fill="#FFFFFF" opacity=".34" filter="url(#{g('soft')})"/>
    <ellipse cx="122" cy="214" rx="30" ry="22" fill="{K_DEEP}" opacity=".30" filter="url(#{g('soft')})"/>
    <ellipse cx="60" cy="200" rx="13" ry="9" fill="#F49AA8" opacity=".32" filter="url(#{g('soft2')})"/>
    <ellipse cx="120" cy="200" rx="12" ry="8" fill="#F49AA8" opacity=".26" filter="url(#{g('soft2')})"/>
  </g>
  <path d="{head.d()}" fill="none" stroke="#F6F9DC" stroke-width="2.6" mask="url(#{g('rimmask')})" opacity=".7" filter="url(#{g('soft2')})"/>
  <ellipse cx="85" cy="196" rx="3" ry="2.2" fill="{K_DEEP}" opacity=".7"/>
  <ellipse cx="96" cy="196" rx="3" ry="2.2" fill="{K_DEEP}" opacity=".7"/>
  <path d="M66 205C76 216 106 216 116 204" stroke="{K_DEEP}" stroke-width="2.4" fill="none" stroke-linecap="round" opacity=".8"/>
  <path d="M70 207C80 213 102 213 112 206" stroke="#F6F9DC" stroke-width="1.4" fill="none" stroke-linecap="round" opacity=".5"/>
</g>

<g transform="{LIFT}">{eye(70, 172, 10.4)}{eye(111, 171, 9.8, sq=0.9, tilt=8)}</g>
'''

svg = common.svg(P, defs, content)
open(os.path.join(HERE, 'out', 'tortoise.svg'), 'w').write(svg)
print("bytes", len(svg))
