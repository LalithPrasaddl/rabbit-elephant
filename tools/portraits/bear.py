import math, random, sys
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from furlib import BPath, fur_layers, edge_fur, render_fur
import common

rng = random.Random(7711)
P = "b"
g = lambda i: f"{P}-{i}"
eye = common.make_eye(P, socket="#3A2616", lidfill="#C39668", rimcol="#3A2616")

DEEP, SHADE, BASE, LIGHT, HI = "#3E2915", "#7A5230", "#A97D52", "#D9B48A", "#F2E0C6"
MUZ, MUZD, NOSE = "#EAD1B0", "#C4A67E", "#4A2C16"

# ---------------- silhouettes ----------------
torso = (BPath((136, 184))
    .c((114, 208), (103, 250), (111, 290))
    .c((119, 320), (148, 332), (184, 333))
    .c((231, 334), (265, 305), (268, 260))
    .c((271, 214), (246, 182), (206, 176))
    .c((176, 172), (150, 172), (136, 184)))

head = (BPath((58, 152))
    .c((60, 111), (88, 86), (127, 86))
    .c((166, 86), (193, 111), (195, 152))
    .c((197, 191), (170, 220), (127, 220))
    .c((84, 220), (56, 191), (58, 152)))

arm_near = (BPath((132, 232))
    .c((120, 254), (114, 288), (117, 312))
    .c((119, 328), (94, 331), (93, 314))
    .c((92, 286), (102, 248), (114, 226)))

foot_l = (BPath((110, 306))
    .c((132, 300), (152, 308), (152, 320))
    .c((152, 332), (128, 338), (108, 335))
    .c((92, 332), (90, 310), (110, 306)))
foot_r = (BPath((186, 304))
    .c((210, 299), (232, 308), (232, 320))
    .c((232, 333), (206, 338), (186, 335))
    .c((168, 332), (166, 309), (186, 304)))

# ---------------- texture ----------------
radiate = lambda ox, oy: (lambda x, y: math.atan2(y-oy, x-ox))
body_flow, head_flow = radiate(150, 184), radiate(127, 190)

DARK_T = [(DEEP, .8, .20), (SHADE, .8, .24), (SHADE, .6, .16), (LIGHT, .7, .22)]
LITE_T = [(SHADE, .7, .16), (LIGHT, .8, .26), (HI, .8, .30), (HI, .6, .20)]
FACE_T = [(DEEP, .6, .16), (SHADE, .6, .20), (LIGHT, .6, .24), (HI, .6, .24)]
EDGE_T = [(SHADE, .8, .42), (BASE, .8, .58), (LIGHT, .7, .52), (DEEP, .6, .24)]

body_fur = fur_layers([
    dict(ell=(214, 224, 56, 46), n=300, flow=body_flow, tones=DARK_T, len=(8, 17), curve=1.7),
    dict(ell=(198, 292, 60, 42), n=280, flow=body_flow, tones=DARK_T, len=(8, 16), curve=1.7),
    dict(ell=(140, 254, 34, 62), n=280, flow=body_flow, tones=LITE_T, len=(7, 14), curve=1.3),
], rng)
head_fur = fur_layers([
    dict(ell=(127, 152, 70, 66), n=640, flow=head_flow, tones=FACE_T, len=(5, 12), curve=1.0),
], rng)
ear_fur = fur_layers([
    dict(ell=(76, 100, 22, 22), n=130, flow=radiate(100, 130), tones=FACE_T, len=(5, 11), curve=.9),
    dict(ell=(178, 96, 22, 22), n=130, flow=radiate(154, 126), tones=FACE_T, len=(5, 11), curve=.9),
], rng)
limb_fur = fur_layers([
    dict(ell=(110, 274, 16, 44), n=140, flow=lambda x, y: math.pi/2+.25, tones=FACE_T, len=(5, 11), curve=.8),
    dict(ell=(120, 320, 30, 13), n=110, flow=lambda x, y: math.pi, tones=FACE_T, len=(5, 11), curve=.8),
    dict(ell=(198, 320, 32, 13), n=110, flow=lambda x, y: math.pi, tones=FACE_T, len=(5, 11), curve=.8),
], rng)

body_edge = edge_fur(torso, 240, False, rng, EDGE_T, length=(6, 15), spread=.55)
head_edge = edge_fur(head, 210, False, rng, EDGE_T, length=(5, 13), spread=.55)
limb_edge = (edge_fur(arm_near, 70, False, rng, EDGE_T, length=(3, 9), spread=.45)
           + edge_fur(foot_l, 70, False, rng, EDGE_T, length=(3, 9), spread=.5)
           + edge_fur(foot_r, 70, False, rng, EDGE_T, length=(3, 9), spread=.5))

def ear(cx, cy, r, pre):
    return f'''<g>
  {render_fur(fur_layers([dict(ell=(cx, cy, r*.9, r*.9), n=90, flow=radiate(127, 150), tones=FACE_T, len=(5,11), curve=.9)], rng))}
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{g('ear')})"/>
  <clipPath id="{g('cear'+str(cx))}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>
  <g clip-path="url(#{g('cear'+str(cx))})">
    <ellipse cx="{cx+2}" cy="{cy+4}" rx="{r*.58}" ry="{r*.54}" fill="{MUZD}" opacity=".55" filter="url(#{g('soft3')})"/>
    <ellipse cx="{cx+1}" cy="{cy+3}" rx="{r*.44}" ry="{r*.40}" fill="{MUZ}" opacity=".85" filter="url(#{g('soft3')})"/>
    {render_fur(fur_layers([dict(ell=(cx, cy, r, r), n=120, flow=radiate(cx-6, cy-6), tones=FACE_T, len=(4,9), curve=.8)], rng))}
    <ellipse cx="{cx-r*.5}" cy="{cy+r*.6}" rx="{r*.7}" ry="{r*.5}" fill="#3E2915" opacity=".26" filter="url(#{g('soft2')})"/>
  </g>
</g>'''

defs = f'''
  <radialGradient id="{g('body')}" cx="34%" cy="22%" r="88%">
    <stop offset="0" stop-color="{HI}"/><stop offset="38%" stop-color="{LIGHT}"/>
    <stop offset="72%" stop-color="{BASE}"/><stop offset="1" stop-color="#5A3A1E"/>
  </radialGradient>
  <radialGradient id="{g('head')}" cx="30%" cy="20%" r="88%">
    <stop offset="0" stop-color="{HI}"/><stop offset="36%" stop-color="{LIGHT}"/>
    <stop offset="70%" stop-color="{BASE}"/><stop offset="1" stop-color="#5E3E20"/>
  </radialGradient>
  <radialGradient id="{g('ear')}" cx="34%" cy="26%" r="84%">
    <stop offset="0" stop-color="{LIGHT}"/><stop offset="52%" stop-color="{BASE}"/>
    <stop offset="1" stop-color="#5A3A1E"/>
  </radialGradient>
  <radialGradient id="{g('muz')}" cx="34%" cy="26%" r="84%">
    <stop offset="0" stop-color="#FBF0DE"/><stop offset="50%" stop-color="{MUZ}"/>
    <stop offset="1" stop-color="#B4906A"/>
  </radialGradient>
  <radialGradient id="{g('nose')}" cx="34%" cy="26%" r="80%">
    <stop offset="0" stop-color="#6E4526"/><stop offset="55%" stop-color="{NOSE}"/>
    <stop offset="1" stop-color="#26150A"/>
  </radialGradient>
  <clipPath id="{g('ctorso')}"><path d="{torso.d()}"/></clipPath>
  <clipPath id="{g('chead')}"><path d="{head.d()}"/></clipPath>
{common.defs_common(P)}'''

content = f'''
<ellipse cx="190" cy="336" rx="100" ry="15" fill="#3E2915" opacity=".30" filter="url(#{g('soft')})"/>

<g>{render_fur(body_edge)}
  <path d="{torso.d()}" fill="url(#{g('body')})"/>
  <g clip-path="url(#{g('ctorso')})">
    {render_fur(body_fur)}
    <ellipse cx="206" cy="192" rx="66" ry="26" fill="{HI}" opacity=".34" filter="url(#{g('soft')})"/>
    <ellipse cx="124" cy="306" rx="46" ry="38" fill="#3E2915" opacity=".34" filter="url(#{g('soft')})"/>
    <ellipse cx="196" cy="324" rx="70" ry="22" fill="#3E2915" opacity=".30" filter="url(#{g('soft')})"/>
    <ellipse cx="152" cy="230" rx="40" ry="34" fill="#FFF6E6" opacity=".22" filter="url(#{g('soft')})"/>
  </g>
</g>

<g>{render_fur(limb_edge)}
  <path d="{foot_r.d()}" fill="#9C7048"/>
  <path d="{foot_l.d()}" fill="#B4885C"/>
  <path d="M118 230C108 254 100 288 101 312" stroke="#3E2915" stroke-width="10" fill="none" opacity=".20" filter="url(#{g('soft2')})"/>
  <path d="{arm_near.d()}" fill="#B98D60"/>
  {render_fur(limb_fur)}
  <ellipse cx="120" cy="320" rx="20" ry="9" fill="{MUZ}" opacity=".8" filter="url(#{g('soft3')})"/>
  <ellipse cx="199" cy="320" rx="21" ry="9" fill="{MUZ}" opacity=".65" filter="url(#{g('soft3')})"/>
  <g fill="{MUZD}" opacity=".55">
    <circle cx="106" cy="311" r="3.4"/><circle cx="116" cy="308" r="3.4"/><circle cx="126" cy="309" r="3.4"/>
    <circle cx="185" cy="310" r="3.4"/><circle cx="196" cy="307" r="3.4"/><circle cx="207" cy="308" r="3.4"/>
  </g>
  <ellipse cx="118" cy="332" rx="28" ry="6" fill="#3E2915" opacity=".26" filter="url(#{g('soft2')})"/>
</g>

{ear(76, 100, 24, P)}{ear(178, 96, 24, P)}

<g>{render_fur(head_edge)}
  <path d="{head.d()}" fill="url(#{g('head')})"/>
  <g clip-path="url(#{g('chead')})">
    {render_fur(head_fur)}
    <ellipse cx="100" cy="112" rx="46" ry="26" fill="{HI}" opacity=".40" filter="url(#{g('soft')})"/>
    <ellipse cx="178" cy="192" rx="34" ry="30" fill="#3E2915" opacity=".30" filter="url(#{g('soft')})"/>
    <ellipse cx="128" cy="214" rx="46" ry="16" fill="#3E2915" opacity=".24" filter="url(#{g('soft')})"/>
    <ellipse cx="86" cy="180" rx="22" ry="15" fill="#E89AA2" opacity=".22" filter="url(#{g('soft')})"/>
    <ellipse cx="170" cy="176" rx="21" ry="14" fill="#E89AA2" opacity=".18" filter="url(#{g('soft')})"/>
  </g>
  <path d="{head.d()}" fill="none" stroke="{HI}" stroke-width="2.8" mask="url(#{g('rimmask')})" opacity=".7" filter="url(#{g('soft2')})"/>
</g>

<!-- muzzle -->
<g>
  <ellipse cx="127" cy="186" rx="40" ry="30" fill="{MUZD}" opacity=".5" filter="url(#{g('soft2')})"/>
  <ellipse cx="127" cy="184" rx="37" ry="27" fill="url(#{g('muz')})"/>
  {render_fur(fur_layers([dict(ell=(127, 184, 34, 24), n=180, flow=radiate(127, 170), tones=[("#C4A67E", .5, .22), ("#FFF6E6", .5, .30)], len=(4, 9), curve=.8)], rng))}
  <ellipse cx="127" cy="204" rx="26" ry="12" fill="#B4906A" opacity=".30" filter="url(#{g('soft2')})"/>
  <path d="M113 166C118 161 136 161 141 166C145 171 138 180 127 180C116 180 109 171 113 166Z" fill="url(#{g('nose')})"/>
  <path d="M117 166C122 163 132 163 136 166" stroke="#A8825E" stroke-width="1.8" fill="none" opacity=".45" stroke-linecap="round"/>
  <path d="M127 180C127 186 127 189 127 190" stroke="#7A5230" stroke-width="1.8" fill="none" stroke-linecap="round" opacity=".6"/>
  <path d="M127 190C123 196 115 196 111 191M127 190C131 196 139 196 143 191" stroke="#7A5230" stroke-width="1.8" fill="none" stroke-linecap="round" opacity=".6"/>
</g>

<g>{eye(93, 143, 12.2)}{eye(162, 140, 11.4, sq=0.90, tilt=8)}</g>
'''

svg = common.svg(P, defs, content)
open(os.path.join(HERE, 'out', 'bear.svg'), 'w').write(svg)
print("bytes", len(svg))
