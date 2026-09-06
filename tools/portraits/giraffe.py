import math, random, sys
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from furlib import BPath, fur_layers, edge_fur, render_fur, cubic, blotches
import common

rng = random.Random(1414)
P = "n"
g = lambda i: f"{P}-{i}"
eye = common.make_eye(P, socket="#6B4A1E", lidfill="#D9AE6A", rimcol="#5A3E14")

DEEP, SHADE, BASE, LIGHT, HI = "#6B4A1E", "#B98B3E", "#E8C078", "#F7E1B0", "#FFF6DE"
PATCH, PATCHD, MUZ = "#B0762F", "#8A5A20", "#FFEFC4"
CAP, CAPS, RED = "#FFFFFF", "#E4DCCE", "#E4453F"

# ---------------- neck: swept from the shoulder up to the head ----------------
NECK = ((176, 250), (150, 196), (140, 152), (124, 122))
def neck_w(t): return 30 - 8*t
np_ = cubic(*NECK, 40)
def neck_path():
    L, R = [], []
    for ((x, y), (tx, ty), t) in np_:
        nx, ny = -ty, tx; w = neck_w(t)
        L.append((x-nx*w, y-ny*w)); R.append((x+nx*w, y+ny*w))
    return "M" + " L".join("%.0f %.0f" % p for p in L + R[::-1]) + "Z"

body = (BPath((160, 226))
    .c((146, 244), (144, 270), (156, 286))
    .c((170, 302), (200, 300), (222, 299))
    .c((252, 298), (272, 280), (272, 254))
    .c((272, 226), (252, 208), (222, 206))
    .c((194, 204), (172, 212), (160, 226)))

head = (BPath((84, 108))
    .c((82, 86), (94, 70), (114, 70))
    .c((134, 70), (147, 86), (146, 108))
    .c((145, 128), (140, 146), (132, 158))
    .c((126, 166), (104, 166), (98, 158))
    .c((90, 146), (85, 128), (84, 108)))

ear_l = (BPath((88, 104)).c((72, 94), (52, 94), (46, 104))
    .c((41, 114), (56, 124), (74, 121)).c((84, 119), (89, 113), (88, 104)))
ear_r = (BPath((143, 100)).c((159, 89), (180, 88), (186, 98))
    .c((192, 108), (177, 119), (159, 117)).c((149, 115), (143, 109), (143, 100)))

def leg(x, top, bot, w):
    return (BPath((x-w, top))
        .c((x-w-1, top+30), (x-w+1, bot-14), (x-w+1, bot-5))
        .c((x-w+1, bot+5), (x+w-1, bot+5), (x+w-1, bot-5))
        .c((x+w-1, bot-14), (x+w+1, top+30), (x+w, top)))
leg_fn, leg_ff = leg(172, 228, 331, 9.5), leg(200, 224, 320, 7.5)
leg_bn, leg_bf = leg(252, 230, 331, 10), leg(228, 226, 320, 7.5)

radiate = lambda ox, oy: (lambda x, y: math.atan2(y-oy, x-ox))
COAT_T = [(SHADE, .6, .16), (BASE, .7, .18), (LIGHT, .7, .22), (HI, .6, .20)]
EDGE_T = [(SHADE, .7, .38), (BASE, .8, .5), (LIGHT, .7, .48), (DEEP, .6, .2)]

body_fur = fur_layers([dict(ell=(210, 252, 60, 44), n=300, flow=radiate(186, 214), tones=COAT_T, len=(5, 12), curve=1.2)], rng)
neck_fur = fur_layers([dict(ell=(152, 190, 26, 66), n=260, flow=lambda x, y: math.atan2(y-250, x-176), tones=COAT_T, len=(5, 11), curve=1.0)], rng)
head_fur = fur_layers([dict(ell=(114, 112, 34, 46), n=280, flow=radiate(114, 150), tones=COAT_T, len=(4, 9), curve=.9)], rng)

body_patches = blotches([dict(ell=(210, 252, 54, 38), n=30, fill=PATCH, r=(10, 17), op=.80, sq=.9)], rng)
neck_patches = blotches([dict(ell=(152, 188, 20, 62), n=18, fill=PATCH, r=(7, 13), op=.78, sq=1.0)], rng)
head_patches = blotches([dict(ell=(114, 100, 26, 24), n=7, fill=PATCH, r=(6, 9), op=.50, sq=.9)], rng)

head_edge = edge_fur(head, 150, False, rng, EDGE_T, length=(3, 9), spread=.5)
body_edge = edge_fur(body, 150, False, rng, EDGE_T, length=(3, 9), spread=.5)
mane = fur_layers([dict(ell=(162, 184, 7, 58), n=170, flow=lambda x, y: math.atan2(y-250, x-176)+math.pi/2,
                        tones=[(DEEP, .9, .45), ("#8A5A20", .8, .38), (SHADE, .7, .28)], len=(5, 10), curve=.6, jitter=.16)], rng)

defs = f'''
  <radialGradient id="{g('coat')}" cx="34%" cy="20%" r="88%">
    <stop offset="0" stop-color="{HI}"/><stop offset="38%" stop-color="{LIGHT}"/>
    <stop offset="72%" stop-color="{BASE}"/><stop offset="1" stop-color="#8A5F22"/>
  </radialGradient>
  <linearGradient id="{g('neck')}" x1="0" y1="0" x2="1" y2="0.2">
    <stop offset="0" stop-color="{HI}"/><stop offset="42%" stop-color="{LIGHT}"/>
    <stop offset="1" stop-color="#8A5F22"/>
  </linearGradient>
  <linearGradient id="{g('leg')}" x1="0" y1="0" x2="1" y2="0.1">
    <stop offset="0" stop-color="{LIGHT}"/><stop offset="55%" stop-color="{BASE}"/>
    <stop offset="1" stop-color="#8A5F22"/>
  </linearGradient>
  <radialGradient id="{g('head')}" cx="30%" cy="20%" r="88%">
    <stop offset="0" stop-color="{HI}"/><stop offset="40%" stop-color="{LIGHT}"/>
    <stop offset="76%" stop-color="{BASE}"/><stop offset="1" stop-color="#8A5F22"/>
  </radialGradient>
  <linearGradient id="{g('cap')}" x1="0.1" y1="0" x2="1" y2="0.6">
    <stop offset="0" stop-color="#FFFFFF"/><stop offset="60%" stop-color="#F7F4EE"/>
    <stop offset="1" stop-color="{CAPS}"/>
  </linearGradient>
  <clipPath id="{g('cbody')}"><path d="{body.d()}"/></clipPath>
  <clipPath id="{g('cneck')}"><path d="{neck_path()}"/></clipPath>
  <clipPath id="{g('chead')}"><path d="{head.d()}"/></clipPath>
{common.defs_common(P)}'''

content = f'''
<ellipse cx="212" cy="334" rx="86" ry="13" fill="#6B4A1E" opacity=".28" filter="url(#{g('soft')})"/>

<!-- far legs + tail -->
<g><path d="M266 236C282 250 288 274 285 294" stroke="{BASE}" stroke-width="8" fill="none" stroke-linecap="round"/>
  <path d="M266 238C280 251 285 272 283 290" stroke="{HI}" stroke-width="2.6" fill="none" stroke-linecap="round" opacity=".5"/>
  {render_fur(fur_layers([dict(ell=(286, 306, 6, 12), n=70, flow=lambda x, y: math.pi/2+.2,
      tones=[(DEEP, .9, .5), ("#8A5A20", .8, .4)], len=(8, 18), curve=.8, jitter=.3)], rng))}
  <path d="{leg_ff.d()}" fill="#B98B3E"/><path d="{leg_bf.d()}" fill="#B08234"/>
  <ellipse cx="200" cy="318" rx="9" ry="5" fill="#4E3612"/><ellipse cx="228" cy="318" rx="9" ry="5" fill="#4E3612"/></g>

<!-- near legs -->
<g>
  <path d="{leg_fn.d()}" fill="url(#{g('leg')})"/>
  <path d="{leg_bn.d()}" fill="url(#{g('leg')})"/>
  <ellipse cx="172" cy="329" rx="11" ry="6" fill="#4E3612"/>
  <ellipse cx="252" cy="329" rx="11.5" ry="6" fill="#4E3612"/>
  <path d="M164 300q9 4 17 0M244 302q9 4 17 0" stroke="{SHADE}" stroke-width="1.4" fill="none" opacity=".5"/>
</g>

<!-- body -->
<g>{render_fur(body_edge)}
  <path d="{body.d()}" fill="url(#{g('coat')})"/>
  <g clip-path="url(#{g('cbody')})">
    {body_patches}
    {render_fur(body_fur)}
    <ellipse cx="224" cy="216" rx="56" ry="22" fill="{HI}" opacity=".34" filter="url(#{g('soft')})"/>
    <ellipse cx="168" cy="288" rx="44" ry="28" fill="#6B4A1E" opacity=".30" filter="url(#{g('soft')})"/>
    <ellipse cx="222" cy="296" rx="60" ry="18" fill="#6B4A1E" opacity=".26" filter="url(#{g('soft')})"/>
  </g>
</g>

<!-- neck -->
<g>
  <path d="{neck_path()}" fill="url(#{g('neck')})"/>
  <g clip-path="url(#{g('cneck')})">
    {neck_patches}
    {render_fur(neck_fur)}
    <path d="M168 246C146 206 138 168 128 132" stroke="{HI}" stroke-width="16" fill="none" opacity=".28" filter="url(#{g('soft')})"/>
    <path d="M188 254C166 210 156 170 142 130" stroke="#6B4A1E" stroke-width="14" fill="none" opacity=".26" filter="url(#{g('soft')})"/>
  </g>
  {render_fur(mane)}
</g>

<!-- ears -->
<g>
  <path d="{ear_r.d()}" fill="{SHADE}"/>
  <path d="{ear_l.d()}" fill="url(#{g('coat')})"/>
  <ellipse cx="66" cy="108" rx="16" ry="7" fill="#8A5A20" opacity=".45" filter="url(#{g('soft3')})"/>
  <ellipse cx="166" cy="103" rx="14" ry="6" fill="#6B4A1E" opacity=".40" filter="url(#{g('soft3')})"/>
</g>

<!-- ossicones -->
<g>
  <path d="M97 76C95 66 94 58 97 52" stroke="{SHADE}" stroke-width="8" fill="none" stroke-linecap="round"/>
  <path d="M131 74C130 64 130 56 133 50" stroke="{SHADE}" stroke-width="8" fill="none" stroke-linecap="round"/>
  <circle cx="97" cy="50" r="7" fill="{DEEP}"/><circle cx="133" cy="48" r="7" fill="{DEEP}"/>
  <circle cx="95" cy="48" r="3" fill="#8A5A20" opacity=".8"/><circle cx="131" cy="46" r="3" fill="#8A5A20" opacity=".8"/>
</g>

<!-- head -->
<g>{render_fur(head_edge)}
  <path d="{head.d()}" fill="url(#{g('head')})"/>
  <g clip-path="url(#{g('chead')})">
    {head_patches}
    {render_fur(head_fur)}
    <ellipse cx="98" cy="86" rx="26" ry="16" fill="{HI}" opacity=".40" filter="url(#{g('soft')})"/>
    <ellipse cx="140" cy="140" rx="20" ry="20" fill="#6B4A1E" opacity=".28" filter="url(#{g('soft')})"/>
    <ellipse cx="114" cy="140" rx="26" ry="18" fill="{MUZ}" opacity=".7" filter="url(#{g('soft2')})"/>
    <ellipse cx="92" cy="128" rx="13" ry="9" fill="#E08C96" opacity=".24" filter="url(#{g('soft')})"/>
    <ellipse cx="137" cy="125" rx="12" ry="8" fill="#E08C96" opacity=".18" filter="url(#{g('soft')})"/>
  </g>
</g>

<!-- muzzle -->
<g>
  <ellipse cx="105" cy="140" rx="4.6" ry="3.4" fill="#8A5A20" opacity=".8"/>
  <ellipse cx="123" cy="139" rx="4.6" ry="3.4" fill="#8A5A20" opacity=".8"/>
  <path d="M114 150C110 155 104 155 101 151M114 150C118 155 124 155 127 151" stroke="#8A5A20" stroke-width="1.6" fill="none" stroke-linecap="round" opacity=".7"/>
</g>

<!-- nurse cap -->
<g>
  <path d="M88 66C96 50 134 48 144 62C148 68 142 72 132 70C120 68 106 69 96 72C89 74 85 72 88 66Z" fill="url(#{g('cap')})"/>
  <path d="M90 66C99 54 132 52 142 63" stroke="{CAPS}" stroke-width="1.6" fill="none" opacity=".8"/>
  <path d="M113 55h6v6h6v6h-6v6h-6v-6h-6v-6h6Z" fill="{RED}"/>
  <ellipse cx="116" cy="72" rx="30" ry="7" fill="#6B4A1E" opacity=".22" filter="url(#{g('soft3')})"/>
</g>

<g>{eye(99, 106, 10.6)}{eye(131, 103, 9.9, sq=0.90, tilt=8)}</g>
'''

svg = common.svg(P, defs, content)
open(os.path.join(HERE, 'out', 'giraffe.svg'), 'w').write(svg)
print("bytes", len(svg))
