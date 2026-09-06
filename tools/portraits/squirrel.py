import math, random, sys
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from furlib import BPath, fur_layers, edge_fur, render_fur, cubic
import common

rng = random.Random(2024)
P = "q"
g = lambda i: f"{P}-{i}"
eye = common.make_eye(P, socket="#4A2C14", lidfill="#C08A5E", rimcol="#3A2410")

DEEP, SHADE, BASE, LIGHT, HI = "#5A3A1E", "#8B6030", "#A2683F", "#D4956C", "#F0CDA8"
BELLY, COAT, COATS, COATD = "#F4EFE6", "#FAF8F4", "#DCD6CC", "#B9B2A6"

# ---------------- bushy tail: swept plume behind the body ----------------
TAIL = ((214, 300), (120, 314), (78, 196), (150, 106))
def tail_w(t): return 7 + 31*math.sin(min(1.0, 0.10 + t*0.86)*math.pi)**0.55
tp = cubic(*TAIL, 70)
def tail_path():
    L, R = [], []
    for ((x, y), (tx, ty), t) in tp:
        nx, ny = -ty, tx; w = tail_w(t)
        L.append((x-nx*w, y-ny*w)); R.append((x+nx*w, y+ny*w))
    return "M" + " L".join("%.0f %.0f" % p for p in L + R[::-1]) + "Z"

# ---------------- body / head ----------------
torso = (BPath((176, 186))
    .c((156, 208), (148, 250), (156, 288))
    .c((164, 318), (188, 331), (214, 332))
    .c((246, 333), (266, 310), (266, 274))
    .c((266, 232), (250, 192), (222, 182))
    .c((204, 176), (188, 176), (176, 186)))

head = (BPath((146, 148))
    .c((146, 116), (166, 96), (196, 96))
    .c((226, 96), (246, 116), (246, 148))
    .c((246, 178), (230, 200), (196, 200))
    .c((162, 200), (146, 178), (146, 148)))

def ear(cx, cy, s, lean):
    return (BPath((cx-11*s, cy+14*s))
        .c((cx-13*s, cy-6*s), (cx-8*s+lean, cy-20*s), (cx+1*s+lean, cy-20*s))
        .c((cx+10*s+lean, cy-20*s), (cx+14*s, cy-4*s), (cx+12*s, cy+14*s))
        .c((cx+4*s, cy+8*s), (cx-4*s, cy+8*s), (cx-11*s, cy+14*s)))
ear_l, ear_r = ear(166, 108, 1.0, -6), ear(228, 104, 1.0, 6)

paw_l = (BPath((186, 250)).c((180, 262), (180, 276), (188, 282))
    .c((196, 288), (206, 282), (206, 270)).c((206, 258), (196, 246), (186, 250)))
paw_r = (BPath((214, 248)).c((222, 258), (224, 274), (216, 281))
    .c((208, 287), (198, 280), (199, 268)).c((200, 256), (206, 244), (214, 248)))

foot_l = (BPath((168, 312)).c((188, 307), (206, 314), (206, 324))
    .c((206, 334), (184, 338), (166, 335)).c((152, 332), (150, 314), (168, 312)))
foot_r = (BPath((228, 312)).c((248, 307), (264, 314), (264, 324))
    .c((264, 334), (244, 338), (226, 335)).c((212, 332), (212, 314), (228, 312)))

radiate = lambda ox, oy: (lambda x, y: math.atan2(y-oy, x-ox))
TAIL_T = [(DEEP, .8, .22), (SHADE, .9, .26), (LIGHT, .9, .34), (HI, .8, .32), (BASE, .7, .18)]
FACE_T = [(DEEP, .6, .18), (SHADE, .6, .22), (LIGHT, .6, .26), (HI, .6, .22)]
BODY_T = [(SHADE, .7, .18), (BASE, .8, .22), (LIGHT, .8, .26), (HI, .7, .22)]
EDGE_T = [(SHADE, .8, .42), (BASE, .8, .55), (LIGHT, .8, .55), (HI, .7, .45)]

tail_fur = fur_layers([
    dict(ell=(112, 214, 44, 104), n=760, flow=lambda x, y: math.atan2(y-212, x-166) + math.pi/2,
         tones=TAIL_T, len=(9, 22), curve=2.2, jitter=.42),
], rng)
head_fur = fur_layers([
    dict(ell=(196, 148, 52, 52), n=420, flow=radiate(196, 178), tones=FACE_T, len=(4, 10), curve=.9),
], rng)
body_fur = fur_layers([
    dict(ell=(212, 240, 58, 60), n=280, flow=radiate(190, 186), tones=BODY_T, len=(6, 13), curve=1.3),
], rng)
limb_fur = fur_layers([
    dict(ell=(180, 322, 28, 12), n=90, flow=lambda x, y: math.pi, tones=FACE_T, len=(4, 10), curve=.8),
    dict(ell=(240, 322, 28, 12), n=90, flow=lambda x, y: math.pi, tones=FACE_T, len=(4, 10), curve=.8),
], rng)
ear_fur = fur_layers([
    dict(ell=(166, 104, 13, 18), n=70, flow=lambda x, y: -math.pi/2, tones=FACE_T, len=(4, 12), curve=.7, jitter=.4),
    dict(ell=(228, 100, 13, 18), n=70, flow=lambda x, y: -math.pi/2, tones=FACE_T, len=(4, 12), curve=.7, jitter=.4),
], rng)

TAILP = BPath((0, 0))  # tail edge fur is sampled from the swept outline instead
def tail_edge_fur():
    out = {}
    for ((x, y), (tx, ty), t) in cubic(*TAIL, 46):
        nx, ny = -ty, tx; w = tail_w(t)
        for sgn in (-1, 1):
            bx, by = x + nx*w*sgn, y + ny*w*sgn
            for _ in range(4):
                a = math.atan2(ny*sgn, nx*sgn) + rng.uniform(-.6, .6)
                ln = rng.uniform(5, 15)
                c, wd, op = TAIL_T[rng.randrange(len(TAIL_T))]
                ex, ey = bx + math.cos(a)*ln, by + math.sin(a)*ln
                mx, my = (bx+ex)/2, (by+ey)/2
                k = rng.uniform(-2.2, 2.2)
                out.setdefault((c, wd, min(.6, op*2)), []).append(
                    "M%.0f %.0fQ%.0f %.0f %.0f %.0f" % (bx, by, mx-math.sin(a)*k, my+math.cos(a)*k, ex, ey))
    return [(k[0], k[1], k[2], "".join(v)) for k, v in out.items()]

head_edge = edge_fur(head, 170, False, rng, EDGE_T, length=(4, 11), spread=.5)
body_edge = edge_fur(torso, 150, False, rng, EDGE_T, length=(4, 11), spread=.5)
ear_edge = (edge_fur(ear_l, 60, False, rng, EDGE_T, length=(4, 12), spread=.5)
          + edge_fur(ear_r, 60, False, rng, EDGE_T, length=(4, 12), spread=.5))

defs = f'''
  <linearGradient id="{g('tail')}" x1="0.15" y1="0" x2="1" y2="0.4">
    <stop offset="0" stop-color="{HI}"/><stop offset="40%" stop-color="{LIGHT}"/>
    <stop offset="1" stop-color="#4E3018"/>
  </linearGradient>
  <radialGradient id="{g('body')}" cx="34%" cy="22%" r="88%">
    <stop offset="0" stop-color="{HI}"/><stop offset="40%" stop-color="{LIGHT}"/>
    <stop offset="74%" stop-color="{BASE}"/><stop offset="1" stop-color="#4E3018"/>
  </radialGradient>
  <radialGradient id="{g('head')}" cx="30%" cy="20%" r="88%">
    <stop offset="0" stop-color="#F8DCC0"/><stop offset="38%" stop-color="{LIGHT}"/>
    <stop offset="72%" stop-color="{BASE}"/><stop offset="1" stop-color="#54341A"/>
  </radialGradient>
  <radialGradient id="{g('ear')}" cx="36%" cy="26%" r="84%">
    <stop offset="0" stop-color="{LIGHT}"/><stop offset="54%" stop-color="{BASE}"/>
    <stop offset="1" stop-color="#4E3018"/>
  </radialGradient>
  <linearGradient id="{g('coat')}" x1="0.1" y1="0" x2="1" y2="0.5">
    <stop offset="0" stop-color="#FFFFFF"/><stop offset="45%" stop-color="{COAT}"/>
    <stop offset="1" stop-color="{COATS}"/>
  </linearGradient>
  <radialGradient id="{g('mir')}" cx="36%" cy="28%" r="78%">
    <stop offset="0" stop-color="#FFFFFF"/><stop offset="45%" stop-color="#CFD6DB"/>
    <stop offset="1" stop-color="#7C8A93"/>
  </radialGradient>
  <clipPath id="{g('chead')}"><path d="{head.d()}"/></clipPath>
  <clipPath id="{g('ctorso')}"><path d="{torso.d()}"/></clipPath>
  <clipPath id="{g('ccoat')}"><path d="M180 194C160 214 152 258 158 296C162 320 186 331 214 332C246 333 266 312 266 276C266 234 250 200 224 190C210 200 194 202 180 194Z"/></clipPath>
  <clipPath id="{g('ctail')}"><path d="{tail_path()}"/></clipPath>
{common.defs_common(P)}'''

content = f'''
<ellipse cx="214" cy="336" rx="86" ry="14" fill="#4E3018" opacity=".28" filter="url(#{g('soft')})"/>

<!-- tail -->
<g>
  {render_fur(tail_edge_fur())}
  <path d="{tail_path()}" fill="url(#{g('tail')})"/>
  <g clip-path="url(#{g('ctail')})">
    {render_fur(tail_fur)}
    <path d="M182 314C120 308 92 204 140 118" stroke="{HI}" stroke-width="18" fill="none" opacity=".28" filter="url(#{g('soft')})"/>
    <path d="M196 326C130 322 104 200 156 108" stroke="#4E3018" stroke-width="16" fill="none" opacity=".24" filter="url(#{g('soft')})"/>
  </g>
</g>

<!-- ears -->
<g>{render_fur(ear_edge)}
  <path d="{ear_l.d()}" fill="url(#{g('ear')})"/>
  <path d="{ear_r.d()}" fill="url(#{g('ear')})"/>
  {render_fur(ear_fur)}
  <ellipse cx="164" cy="106" rx="7" ry="11" fill="#8B5A38" opacity=".45" filter="url(#{g('soft3')})"/>
  <ellipse cx="230" cy="102" rx="7" ry="11" fill="#8B5A38" opacity=".40" filter="url(#{g('soft3')})"/>
</g>

<!-- body -->
<g>{render_fur(body_edge)}
  <path d="{torso.d()}" fill="url(#{g('body')})"/>
  <g clip-path="url(#{g('ctorso')})">
    {render_fur(body_fur)}
    <ellipse cx="228" cy="196" rx="52" ry="24" fill="{HI}" opacity=".34" filter="url(#{g('soft')})"/>
    <ellipse cx="166" cy="300" rx="44" ry="34" fill="#4E3018" opacity=".32" filter="url(#{g('soft')})"/>
  </g>
</g>

<!-- lab coat -->
<g>
  <path d="M180 194C160 214 152 258 158 296C162 320 186 331 214 332C246 333 266 312 266 276C266 234 250 200 224 190C210 200 194 202 180 194Z" fill="url(#{g('coat')})"/>
  <g clip-path="url(#{g('ccoat')})">
  <path d="M185 197C189 216 193 238 196 254C200 238 206 214 219 194C212 201 192 201 185 197Z" fill="{LIGHT}"/>
  <path d="M196 255C196 272 196 302 196 331" stroke="{COATS}" stroke-width="1.8" fill="none" opacity=".8"/>
  <path d="M185 197C190 219 194 238 197 255" stroke="{COATD}" stroke-width="1.8" fill="none" opacity=".6"/>
  <path d="M219 194C210 216 201 238 197 255" stroke="{COATD}" stroke-width="1.8" fill="none" opacity=".55"/>
  <rect x="226" y="272" width="26" height="22" rx="3" fill="none" stroke="{COATD}" stroke-width="1.6" opacity=".55"/>
  <circle cx="196" cy="272" r="2.6" fill="{COATD}" opacity=".7"/>
  <circle cx="196" cy="298" r="2.6" fill="{COATD}" opacity=".7"/>
  <ellipse cx="166" cy="300" rx="32" ry="42" fill="#9A9384" opacity=".26" filter="url(#{g('soft')})"/>
  <ellipse cx="242" cy="212" rx="42" ry="26" fill="#FFFFFF" opacity=".5" filter="url(#{g('soft')})"/>
  </g>
</g>

<!-- paws + feet -->
<g>{render_fur(limb_fur)}
  <path d="{foot_r.d()}" fill="#A9714A"/>
  <path d="{foot_l.d()}" fill="#D9A277"/>
  {render_fur(edge_fur(foot_l, 46, False, rng, EDGE_T, length=(3,8), spread=.5))}
  {render_fur(edge_fur(foot_r, 46, False, rng, EDGE_T, length=(3,8), spread=.5))}
  <path d="{paw_r.d()}" fill="#B87A4C"/>
  <path d="{paw_l.d()}" fill="{LIGHT}"/>
  <g stroke="#8B6030" stroke-width="1.5" stroke-linecap="round" opacity=".5" fill="none">
    <path d="M188 268q-4 6 -4 12"/><path d="M196 266q-2 7 -2 13"/>
    <path d="M172 316q0 5 0 8"/><path d="M182 314q0 5 0 8"/><path d="M192 315q0 5 0 8"/>
    <path d="M232 316q0 5 0 8"/><path d="M242 314q0 5 0 8"/><path d="M252 315q0 5 0 8"/>
  </g>
</g>

<!-- head -->
<g>{render_fur(head_edge)}
  <path d="{head.d()}" fill="url(#{g('head')})"/>
  <g clip-path="url(#{g('chead')})">
    {render_fur(head_fur)}
    <ellipse cx="172" cy="116" rx="34" ry="20" fill="#FBE4CC" opacity=".42" filter="url(#{g('soft')})"/>
    <ellipse cx="234" cy="180" rx="26" ry="24" fill="#4E3018" opacity=".30" filter="url(#{g('soft')})"/>
    <ellipse cx="196" cy="196" rx="34" ry="14" fill="#4E3018" opacity=".24" filter="url(#{g('soft')})"/>
    <ellipse cx="196" cy="172" rx="26" ry="20" fill="{BELLY}" opacity=".55" filter="url(#{g('soft2')})"/>
    <ellipse cx="163" cy="168" rx="16" ry="11" fill="#E08C96" opacity=".24" filter="url(#{g('soft')})"/>
    <ellipse cx="230" cy="164" rx="15" ry="10" fill="#E08C96" opacity=".18" filter="url(#{g('soft')})"/>
  </g>
</g>

<!-- muzzle + face -->
<g>
  <path d="M188 160C191 157 201 157 204 160C207 164 202 170 196 170C190 170 185 164 188 160Z" fill="#8A4E52"/>
  <path d="M190 160C193 158 199 158 202 160" stroke="#E7B7A4" stroke-width="1.4" fill="none" opacity=".55" stroke-linecap="round"/>
  <path d="M196 170C196 175 196 177 196 178" stroke="#8B6030" stroke-width="1.5" fill="none" stroke-linecap="round" opacity=".7"/>
  <path d="M196 178C192 183 187 183 184 179M196 178C200 183 205 183 208 179" stroke="#8B6030" stroke-width="1.5" fill="none" stroke-linecap="round" opacity=".7"/>
  <path d="M190 184h5v9a2.5 2.5 0 0 1 -5 0Z" fill="#FFFDF4"/>
  <path d="M197 184h5v9a2.5 2.5 0 0 1 -5 0Z" fill="#F4EFE0"/>
  <g stroke="#6E4520" fill="none" stroke-linecap="round">
    <path d="M186 166C170 162 156 162 144 166" stroke-width=".9" opacity=".32"/>
    <path d="M186 171C170 172 156 176 146 183" stroke-width=".85" opacity=".28"/>
    <path d="M206 166C222 162 236 163 248 167" stroke-width=".9" opacity=".30"/>
    <path d="M206 171C222 173 236 177 246 184" stroke-width=".85" opacity=".26"/>
  </g>
</g>

<!-- head mirror -->
<g>
  <path d="M162 122C176 110 216 110 230 122" stroke="#3A4148" stroke-width="6" fill="none" stroke-linecap="round"/>
  <path d="M162 122C176 111 216 111 230 122" stroke="#6E7A84" stroke-width="2" fill="none" stroke-linecap="round" opacity=".7"/>
  <circle cx="196" cy="112" r="16" fill="#5A646C"/>
  <circle cx="196" cy="112" r="13.5" fill="url(#{g('mir')})"/>
  <circle cx="196" cy="112" r="4.4" fill="#39424A"/>
  <path d="M186 106C190 102 198 100 204 102" stroke="#fff" stroke-width="2.6" fill="none" opacity=".8" stroke-linecap="round"/>
</g>

<g>{eye(173, 143, 12.0)}{eye(222, 140, 11.2, sq=0.90, tilt=8)}</g>
'''

svg = common.svg(P, defs, content)
open(os.path.join(HERE, 'out', 'squirrel.svg'), 'w').write(svg)
print("bytes", len(svg))
