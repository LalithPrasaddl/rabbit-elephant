import math, random, sys
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from furlib import BPath, fur_layers, edge_fur, render_fur, curls
import common

rng = random.Random(5150)
P = "s"
g = lambda i: f"{P}-{i}"
eye = common.make_eye(P, socket="#12161E", lidfill="#4E5A6E", rimcol="#12161E")

HI, LIGHT, BASE, SHADE, DEEP = "#FFFFFF", "#F3F0E8", "#DBD5C6", "#B2AB95", "#857E69"
FDARK, FMID, FLIT, FDEEP = "#333A47", "#4A5364", "#67718A", "#1B202A"
NOSE = "#191D25"

# ---------------- fleece: a lobed cloud built from a core ellipse + perimeter puffs
FX, FY, FRX, FRY = 192, 238, 74, 62
puffs = []
n = 17
for i in range(n):
    a = 2*math.pi*i/n + 0.12
    r = rng.uniform(21, 27)
    px = FX + math.cos(a)*(FRX-8)
    py = FY + math.sin(a)*(FRY-8)
    puffs.append((round(px), round(py), round(r)))

def puff_shapes(fill, extra=""):
    out = f'<ellipse cx="{FX}" cy="{FY}" rx="{FRX}" ry="{FRY}" fill="{fill}"{extra}/>'
    out += "".join('<circle cx="%d" cy="%d" r="%d" fill="%s"%s/>' % (a, b, c, fill, extra) for a, b, c in puffs)
    return out

fleece_clip = (f'<ellipse cx="{FX}" cy="{FY}" rx="{FRX}" ry="{FRY}"/>'
               + "".join('<circle cx="%d" cy="%d" r="%d"/>' % p for p in puffs))

head_wool = [(122, 118, 22), (150, 116, 20), (100, 126, 19), (170, 128, 18), (136, 108, 17)]

# ---------------- head + limbs ----------------
head = (BPath((84, 172))
    .c((82, 140), (100, 118), (130, 118))
    .c((160, 118), (178, 140), (176, 172))
    .c((174, 204), (162, 228), (140, 236))
    .c((130, 240), (120, 240), (110, 236))
    .c((90, 228), (86, 204), (84, 172)))

ear_l = (BPath((88, 152))
    .c((70, 142), (48, 146), (42, 158))
    .c((36, 170), (52, 182), (72, 180))
    .c((84, 179), (90, 168), (88, 152)))
ear_r = (BPath((174, 148))
    .c((192, 137), (216, 140), (222, 152))
    .c((228, 165), (212, 178), (192, 176))
    .c((180, 175), (173, 164), (174, 148)))

def leg(x, top, bot, w):
    return (BPath((x-w, top))
        .c((x-w-1, top+30), (x-w+1, bot-16), (x-w+1, bot-6))
        .c((x-w+1, bot+5), (x+w-1, bot+5), (x+w-1, bot-6))
        .c((x+w-1, bot-16), (x+w+1, top+30), (x+w, top)))
leg_fn, leg_ff = leg(150, 232, 331, 8), leg(180, 228, 322, 6.5)
leg_bn, leg_bf = leg(238, 236, 331, 8.5), leg(214, 230, 322, 6.5)

WOOL_T = [(SHADE, .9, .30), (BASE, .9, .34), (HI, .9, .40), (DEEP, .8, .18)]
FACE_T = [(FDEEP, .6, .26), (FMID, .6, .24), (FLIT, .6, .26)]

wool = curls([
    dict(ell=(FX, FY, FRX+6, FRY+6), n=560, tones=WOOL_T, r=(3.4, 7.5)),
], rng)
head_wool_curls = curls([
    dict(ell=(133, 120, 44, 18), n=150, tones=WOOL_T, r=(3.0, 6.0)),
], rng)
face_fur = fur_layers([
    dict(ell=(130, 180, 48, 58), n=380, flow=lambda x, y: math.atan2(y-196, x-130), tones=FACE_T, len=(4, 9), curve=.9),
], rng)
ear_fur = fur_layers([
    dict(ell=(64, 163, 26, 16), n=90, flow=lambda x, y: math.pi, tones=FACE_T, len=(4, 9), curve=.8),
    dict(ell=(198, 158, 26, 16), n=90, flow=lambda x, y: 0.0, tones=FACE_T, len=(4, 9), curve=.8),
], rng)
head_edge = edge_fur(head, 170, False, rng, [(FMID, .7, .5), (FLIT, .7, .45), (FDEEP, .6, .3)], length=(3, 8), spread=.5)

defs = f'''
  <radialGradient id="{g('wool')}" cx="34%" cy="20%" r="90%">
    <stop offset="0" stop-color="{HI}"/><stop offset="36%" stop-color="{LIGHT}"/>
    <stop offset="70%" stop-color="{BASE}"/><stop offset="1" stop-color="#8F886F"/>
  </radialGradient>
  <radialGradient id="{g('head')}" cx="30%" cy="20%" r="88%">
    <stop offset="0" stop-color="{FLIT}"/><stop offset="42%" stop-color="{FMID}"/>
    <stop offset="1" stop-color="{FDEEP}"/>
  </radialGradient>
  <radialGradient id="{g('ear')}" cx="40%" cy="26%" r="86%">
    <stop offset="0" stop-color="{FLIT}"/><stop offset="52%" stop-color="{FMID}"/>
    <stop offset="1" stop-color="#161B24"/>
  </radialGradient>
  <linearGradient id="{g('leg')}" x1="0" y1="0" x2="1" y2="0.2">
    <stop offset="0" stop-color="{FLIT}"/><stop offset="55%" stop-color="{FMID}"/>
    <stop offset="1" stop-color="{FDEEP}"/>
  </linearGradient>
  <clipPath id="{g('cfleece')}">{fleece_clip}</clipPath>
  <clipPath id="{g('chead')}"><path d="{head.d()}"/></clipPath>
{common.defs_common(P, iris=("#6E5B44", "#2A2118", "#0C0A07"))}'''

content = f'''
<ellipse cx="196" cy="334" rx="96" ry="14" fill="#3A3A44" opacity=".30" filter="url(#{g('soft')})"/>

<!-- far legs -->
<g opacity=".9"><path d="{leg_ff.d()}" fill="#252C38"/><path d="{leg_bf.d()}" fill="#252C38"/></g>

<!-- near legs + hooves -->
<g>
  <path d="{leg_fn.d()}" fill="url(#{g('leg')})"/>
  <path d="{leg_bn.d()}" fill="url(#{g('leg')})"/>
  <ellipse cx="150" cy="329" rx="9" ry="6" fill="#12161E"/>
  <ellipse cx="238" cy="329" rx="9.5" ry="6" fill="#12161E"/>
  <ellipse cx="180" cy="320" rx="7.5" ry="5" fill="#12161E" opacity=".85"/>
  <ellipse cx="214" cy="320" rx="7.5" ry="5" fill="#12161E" opacity=".85"/>
</g>

<!-- fleece -->
<g>
  {puff_shapes("url(#" + g('wool') + ")")}
  <g clip-path="url(#{g('cfleece')})">
    {render_fur(wool)}
    <ellipse cx="216" cy="186" rx="70" ry="30" fill="{HI}" opacity=".42" filter="url(#{g('soft')})"/>
    <ellipse cx="146" cy="292" rx="54" ry="38" fill="#6E6858" opacity=".34" filter="url(#{g('soft')})"/>
    <ellipse cx="212" cy="304" rx="76" ry="26" fill="#6E6858" opacity=".30" filter="url(#{g('soft')})"/>
    <ellipse cx="150" cy="212" rx="40" ry="34" fill="#6E6858" opacity=".22" filter="url(#{g('soft')})"/>
  </g>
</g>

<!-- ears -->
<g>{render_fur(ear_fur)}
  <path d="{ear_r.d()}" fill="url(#{g('ear')})"/>
  <path d="{ear_l.d()}" fill="url(#{g('ear')})"/>
  <ellipse cx="62" cy="164" rx="18" ry="9" fill="#12161E" opacity=".40" filter="url(#{g('soft3')})"/>
  <ellipse cx="200" cy="159" rx="18" ry="9" fill="#12161E" opacity=".40" filter="url(#{g('soft3')})"/>
</g>

<!-- head -->
<g>{render_fur(head_edge)}
  <path d="{head.d()}" fill="url(#{g('head')})"/>
  <g clip-path="url(#{g('chead')})">
    {render_fur(face_fur)}
    <ellipse cx="106" cy="146" rx="34" ry="24" fill="{FLIT}" opacity=".45" filter="url(#{g('soft')})"/>
    <ellipse cx="166" cy="208" rx="28" ry="26" fill="#0E121A" opacity=".40" filter="url(#{g('soft')})"/>
    <ellipse cx="130" cy="232" rx="34" ry="14" fill="#0E121A" opacity=".30" filter="url(#{g('soft')})"/>
    <ellipse cx="130" cy="206" rx="26" ry="20" fill="{FLIT}" opacity=".30" filter="url(#{g('soft2')})"/>
    <ellipse cx="94" cy="196" rx="17" ry="12" fill="#D98090" opacity=".20" filter="url(#{g('soft')})"/>
    <ellipse cx="166" cy="192" rx="16" ry="11" fill="#D98090" opacity=".16" filter="url(#{g('soft')})"/>
  </g>
</g>

<!-- woolly forehead tuft -->
<g>
  {"".join('<circle cx="%d" cy="%d" r="%d" fill="url(#%s)"/>' % (a, b, c, g('wool')) for a, b, c in head_wool)}
  <clipPath id="{g('ctuft')}">{"".join('<circle cx="%d" cy="%d" r="%d"/>' % t for t in head_wool)}</clipPath>
  <g clip-path="url(#{g('ctuft')})">
    {render_fur(head_wool_curls)}
    <ellipse cx="140" cy="140" rx="60" ry="20" fill="#6E6858" opacity=".28" filter="url(#{g('soft')})"/>
  </g>
</g>

<!-- muzzle + face -->
<g>
  <path d="M118 214C122 210 138 210 142 214C146 219 139 227 130 227C121 227 114 219 118 214Z" fill="#2A313D"/>
  <path d="M121 213C126 210 134 210 139 213" stroke="{FLIT}" stroke-width="1.6" fill="none" opacity=".5" stroke-linecap="round"/>
  <path d="M124 216C122 218 122 221 125 221C127 221 127 218 126 216" fill="{NOSE}"/>
  <path d="M136 216C138 218 138 221 135 221C133 221 133 218 134 216" fill="{NOSE}"/>
  <path d="M130 227C130 231 130 233 130 234" stroke="#0E121A" stroke-width="1.6" fill="none" stroke-linecap="round" opacity=".7"/>
  <path d="M130 234C126 239 120 239 117 235M130 234C134 239 140 239 143 235" stroke="#0E121A" stroke-width="1.6" fill="none" stroke-linecap="round" opacity=".7"/>
</g>

<g>{eye(101, 172, 11.6)}{eye(160, 169, 10.8, sq=0.90, tilt=8)}</g>
'''

svg = common.svg(P, defs, content)
open(os.path.join(HERE, 'out', 'sheep.svg'), 'w').write(svg)
print("bytes", len(svg))
