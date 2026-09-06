import math, random, sys
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from furlib import BPath, fur_layers, edge_fur, render_fur

rng = random.Random(4242)
P = "r"

# Authored facing viewer-left with light from upper-LEFT, then mirrored at the end so the
# finished portrait faces right and is lit from the upper-RIGHT (the site's documented recipe).
DEEP, SHADE, MID, BASE, LIGHT = "#6E5B47", "#A08A6E", "#CDBCA2", "#EFE7DA", "#FFFDF7"
PINK, PINKD, NOSE = "#FFB3C6", "#C97389", "#FF9BAE"

# ---------------- silhouettes ----------------
torso = (BPath((138, 186))
    .c((116, 210), (106, 252), (114, 288))
    .c((121, 318), (146, 331), (182, 332))
    .c((228, 333), (261, 306), (264, 264))
    .c((267, 220), (244, 186), (206, 180))
    .c((178, 176), (151, 174), (138, 186)))

thigh = (BPath((150, 272))
    .c((156, 242), (192, 232), (214, 252))
    .c((236, 272), (232, 314), (202, 324))
    .c((170, 334), (142, 306), (150, 272)))

head = (BPath((59, 158))
    .c((61, 122), (88, 98), (126, 98))
    .c((164, 98), (191, 122), (192, 158))
    .c((193, 192), (172, 218), (140, 226))
    .c((126, 230), (112, 230), (96, 224))
    .c((72, 216), (57, 190), (59, 158)))

ear_near = (BPath((79, 128))
    .c((64, 98), (56, 54), (67, 32))
    .c((78, 12), (98, 20), (99, 48))
    .c((100, 84), (99, 112), (97, 132)))

ear_far = (BPath((153, 132))
    .c((151, 100), (157, 54), (172, 34))
    .c((187, 14), (205, 24), (201, 52))
    .c((196, 88), (180, 112), (173, 130)))

foreleg_far = (BPath((152, 276))
    .c((158, 294), (159, 310), (156, 320))
    .c((154, 330), (140, 331), (140, 320))
    .c((140, 302), (143, 286), (146, 274)))

foreleg_near = (BPath((130, 268))
    .c((133, 288), (133, 308), (131, 320))
    .c((130, 333), (108, 334), (108, 321))
    .c((108, 304), (112, 284), (116, 266)))

hindfoot = (BPath((160, 305))
    .c((180, 304), (196, 314), (195, 325))
    .c((194, 335), (162, 339), (135, 336))
    .c((114, 334), (112, 310), (138, 306)))

tail = (BPath((250, 244))
    .c((272, 236), (288, 250), (286, 268))
    .c((284, 287), (262, 293), (252, 281))
    .c((245, 272), (243, 250), (250, 244)))

# ---------------- fur ----------------
def radiate(ox, oy):
    return lambda x, y: math.atan2(y-oy, x-ox)
body_flow = radiate(148, 196)
head_flow = radiate(120, 190)
def ear_flow(x, y): return math.atan2(y-130, (x-126)*0.18)*0.30 - math.pi/2

DARK_T  = [(DEEP, .8, .22), (DEEP, .6, .14), (SHADE, .8, .26), (MID, .7, .18)]
LITE_T  = [(SHADE, .7, .14), (MID, .8, .22), (LIGHT, .8, .34), (LIGHT, .6, .24)]
FACE_T  = [(DEEP, .55, .16), (SHADE, .6, .20), (MID, .6, .18), (LIGHT, .6, .30)]
EDGE_T  = [(SHADE, .7, .40), (BASE, .8, .60), (LIGHT, .7, .55), (DEEP, .6, .22)]

body_fur = fur_layers([
    dict(ell=(214, 232, 56, 44), n=300, flow=body_flow, tones=DARK_T, len=(8, 17), curve=1.7),  # back
    dict(ell=(196, 292, 58, 42), n=280, flow=body_flow, tones=DARK_T, len=(8, 16), curve=1.7),  # rear/under
    dict(ell=(140, 258, 34, 62), n=300, flow=body_flow, tones=LITE_T, len=(7, 14), curve=1.3),  # chest
], rng)
thigh_fur = fur_layers([
    dict(ell=(190, 278, 42, 44), n=330, flow=radiate(178, 246), tones=LITE_T, len=(7, 15), curve=1.5),
], rng)
head_fur = fur_layers([
    dict(ell=(125, 162, 66, 62), n=600, flow=head_flow, tones=FACE_T, len=(5, 11), curve=1.0),
], rng)
ear_fur = fur_layers([
    dict(ell=(80, 72, 20, 52), n=120, flow=ear_flow, tones=FACE_T, len=(5, 12), curve=.7, jitter=.16),
    dict(ell=(176, 74, 22, 50), n=120, flow=ear_flow, tones=FACE_T, len=(5, 12), curve=.7, jitter=.16),
], rng)
leg_fur = fur_layers([
    dict(ell=(120, 300, 13, 30), n=100, flow=lambda x, y: math.pi/2+.22, tones=FACE_T, len=(5, 11), curve=.7),
    dict(ell=(149, 300, 10, 26), n=70, flow=lambda x, y: math.pi/2+.12, tones=DARK_T, len=(5, 11), curve=.7),
    dict(ell=(155, 322, 38, 13), n=150, flow=lambda x, y: math.pi+.1,    tones=FACE_T, len=(5, 12), curve=.7),
], rng)

body_edge  = edge_fur(torso, 230, False, rng, EDGE_T, length=(6, 15), spread=.55)
head_edge  = edge_fur(head, 175, False, rng, EDGE_T, length=(5, 13), spread=.55)
ear_edge   = (edge_fur(ear_near, 78, False, rng, EDGE_T, length=(3, 9), spread=.4)
            + edge_fur(ear_far, 78, False, rng, EDGE_T, length=(3, 9), spread=.4))
tail_edge  = edge_fur(tail, 80, False, rng, [(LIGHT, .9, .75), (BASE, .9, .6), (SHADE, .7, .3)], length=(6, 14), spread=.8)
leg_edge   = (edge_fur(foreleg_near, 60, False, rng, EDGE_T, length=(3, 8), spread=.4)
            + edge_fur(hindfoot, 70, False, rng, EDGE_T, length=(3, 9), spread=.5))

def g(i): return f"{P}-{i}"

def eye(cx, cy, s, sq=1.0, tilt=-10, lid=0.09):
    """Ellipse-based eye. `lid` is how much of the top the upper eyelid covers -
    a partly lidded eye reads calm; a full staring circle reads startled."""
    rx, ry = s*sq, s*1.06
    cid, lidid = g(f"eye{int(cx)}"), g(f"lid{int(cx)}")
    return f'''<g transform="rotate({tilt} {cx} {cy})">
  <ellipse cx="{cx}" cy="{cy}" rx="{rx*1.5:.1f}" ry="{ry*1.35:.1f}" fill="#6B573F" opacity=".26" filter="url(#{g('soft2')})"/>
  <clipPath id="{cid}"><ellipse cx="{cx}" cy="{cy}" rx="{rx:.1f}" ry="{ry:.1f}"/></clipPath>
  <ellipse cx="{cx}" cy="{cy}" rx="{rx:.1f}" ry="{ry:.1f}" fill="url(#{g('iris')})"/>
  <g clip-path="url(#{cid})">
    <circle cx="{cx}" cy="{cy+ry*.06:.1f}" r="{ry*.46:.1f}" fill="#160E08"/>
    <ellipse cx="{cx}" cy="{cy+ry*.92:.1f}" rx="{rx*.85:.1f}" ry="{ry*.45:.1f}" fill="#C08A55" opacity=".30" filter="url(#{g('soft3')})"/>
    <ellipse cx="{cx}" cy="{cy-ry*1.02:.1f}" rx="{rx*1.3:.1f}" ry="{ry*.50:.1f}" fill="#000" opacity=".24" filter="url(#{g('soft3')})"/>
  </g>
  <ellipse cx="{cx}" cy="{cy}" rx="{rx:.1f}" ry="{ry:.1f}" fill="none" stroke="#5E4A34" stroke-width="{max(0.9, s*.09):.1f}" opacity=".38"/>
  <ellipse cx="{cx-rx*.34:.1f}" cy="{cy-ry*.08:.1f}" rx="{rx*.22:.1f}" ry="{ry*.24:.1f}" fill="#fff" opacity=".92"/>
  <ellipse cx="{cx+rx*.34:.1f}" cy="{cy+ry*.44:.1f}" rx="{rx*.11:.1f}" ry="{ry*.12:.1f}" fill="#FFE7C9" opacity=".45"/>
  <clipPath id="{lidid}"><ellipse cx="{cx}" cy="{cy}" rx="{rx+1.4:.1f}" ry="{ry+1.4:.1f}"/></clipPath>
  <g clip-path="url(#{lidid})">
    <ellipse cx="{cx}" cy="{cy-ry*(1+lid):.1f}" rx="{rx*1.6:.1f}" ry="{ry*1.05:.1f}" fill="#DDD0B9" filter="url(#{g('soft3')})"/>
  </g>
</g>'''

svg = f'''<svg viewBox="0 0 320 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
<defs>
  <radialGradient id="{g('body')}" cx="34%" cy="22%" r="88%">
    <stop offset="0" stop-color="{LIGHT}"/><stop offset="40%" stop-color="{BASE}"/>
    <stop offset="70%" stop-color="#BCA88C"/><stop offset="1" stop-color="#6F5B44"/>
  </radialGradient>
  <radialGradient id="{g('tailg')}" cx="58%" cy="26%" r="82%">
    <stop offset="0" stop-color="#FFFFFC"/><stop offset="50%" stop-color="#F6EFE3"/>
    <stop offset="1" stop-color="#A8926F"/>
  </radialGradient>
  <radialGradient id="{g('thigh')}" cx="40%" cy="26%" r="82%">
    <stop offset="0" stop-color="#FFFEF9"/><stop offset="44%" stop-color="{BASE}"/>
    <stop offset="1" stop-color="#8E7756"/>
  </radialGradient>
  <radialGradient id="{g('head')}" cx="30%" cy="22%" r="86%">
    <stop offset="0" stop-color="#FFFEFB"/><stop offset="42%" stop-color="{BASE}"/>
    <stop offset="72%" stop-color="#C3B096"/><stop offset="1" stop-color="#77644C"/>
  </radialGradient>
  <radialGradient id="{g('ear')}" cx="36%" cy="26%" r="80%">
    <stop offset="0" stop-color="#FFFAF3"/><stop offset="52%" stop-color="#E7DCCB"/>
    <stop offset="1" stop-color="#A8926F"/>
  </radialGradient>
  <radialGradient id="{g('inner')}" cx="42%" cy="30%" r="78%">
    <stop offset="0" stop-color="#FFD8E2"/><stop offset="55%" stop-color="{PINK}"/>
    <stop offset="1" stop-color="{PINKD}"/>
  </radialGradient>
  <radialGradient id="{g('iris')}" cx="34%" cy="28%" r="76%">
    <stop offset="0" stop-color="#8A5F3A"/><stop offset="45%" stop-color="#4A2E1B"/>
    <stop offset="1" stop-color="#120A05"/>
  </radialGradient>
  <radialGradient id="{g('nose')}" cx="36%" cy="26%" r="80%">
    <stop offset="0" stop-color="#FFC9D4"/><stop offset="55%" stop-color="{NOSE}"/>
    <stop offset="1" stop-color="#C4667C"/>
  </radialGradient>
  <linearGradient id="{g('rim')}" x1="0" y1="0" x2="0.9" y2="1">
    <stop offset="0" stop-color="#fff"/><stop offset=".42" stop-color="#fff" stop-opacity=".22"/>
    <stop offset=".78" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <filter id="{g('soft')}" x="-150%" y="-150%" width="400%" height="400%"><feGaussianBlur stdDeviation="8"/></filter>
  <filter id="{g('soft2')}" x="-150%" y="-150%" width="400%" height="400%"><feGaussianBlur stdDeviation="3.4"/></filter>
  <filter id="{g('soft3')}" x="-150%" y="-150%" width="400%" height="400%"><feGaussianBlur stdDeviation="1.6"/></filter>
  <clipPath id="{g('ctorso')}"><path d="{torso.d()}"/></clipPath>
  <clipPath id="{g('cthigh')}"><path d="{thigh.d()}"/></clipPath>
  <clipPath id="{g('chead')}"><path d="{head.d()}"/></clipPath>
  <clipPath id="{g('cear1')}"><path d="{ear_near.d()}"/></clipPath>
  <clipPath id="{g('cear2')}"><path d="{ear_far.d()}"/></clipPath>
  <mask id="{g('rimmask')}"><rect width="320" height="360" fill="url(#{g('rim')})"/></mask>
</defs>

<g transform="translate(320,0) scale(-1,1)">
<ellipse cx="186" cy="336" rx="92" ry="14" fill="#5B4B36" opacity=".32" filter="url(#{g('soft')})"/>

<g><ellipse cx="262" cy="272" rx="24" ry="22" fill="#5E4C39" opacity=".26" filter="url(#{g('soft2')})"/>
  {render_fur(tail_edge)}<path d="{tail.d()}" fill="url(#{g('tailg')})"/>
  {render_fur(fur_layers([dict(ell=(266, 266, 18, 18), n=150, flow=radiate(258, 250), tones=LITE_T, len=(5, 11), curve=1.2)], rng))}
  
  <ellipse cx="259" cy="279" rx="17" ry="13" fill="#A8926F" opacity=".40" filter="url(#{g('soft2')})"/></g>

<g><path d="{foreleg_far.d()}" fill="#A8967C"/></g>

<g transform="translate(7,-15)">{render_fur(ear_edge)}
  <path d="{ear_far.d()}" fill="url(#{g('ear')})"/>
  <g clip-path="url(#{g('cear2')})">
    <path d="M180 44C190 56 187 90 178 112C173 123 166 121 167 110C171 84 174 58 180 44Z" fill="url(#{g('inner')})" opacity=".88"/>
    {render_fur(ear_fur)}
    <ellipse cx="164" cy="84" rx="14" ry="50" fill="#7A6448" opacity=".30" filter="url(#{g('soft2')})"/>
  </g>
  <path d="{ear_near.d()}" fill="url(#{g('ear')})"/>
  <g clip-path="url(#{g('cear1')})">
    <path d="M74 42C84 54 91 88 90 110C90 122 82 122 81 110C79 86 68 56 74 42Z" fill="url(#{g('inner')})"/>
    <path d="M78 56C84 72 87 96 86 108" stroke="{PINKD}" stroke-width="1.2" fill="none" opacity=".45"/>
    {render_fur(ear_fur)}
    <ellipse cx="70" cy="82" rx="11" ry="50" fill="#7A6448" opacity=".32" filter="url(#{g('soft2')})"/>
  </g>
</g>

<g>{render_fur(body_edge)}
  <path d="{torso.d()}" fill="url(#{g('body')})"/>
  <g clip-path="url(#{g('ctorso')})">
    {render_fur(body_fur)}
    <ellipse cx="205" cy="200" rx="66" ry="26" fill="#FFFEF9" opacity=".34" filter="url(#{g('soft')})"/>
    <ellipse cx="126" cy="308" rx="44" ry="36" fill="#6E5B47" opacity=".34" filter="url(#{g('soft')})"/>
    <ellipse cx="150" cy="212" rx="34" ry="26" fill="#6E5B47" opacity=".30" filter="url(#{g('soft')})"/>
    <path d="M152 250C140 272 138 300 146 322" stroke="#5E4C39" stroke-width="16" fill="none" opacity=".17" filter="url(#{g('soft')})"/>
    <ellipse cx="186" cy="326" rx="66" ry="20" fill="#5E4C39" opacity=".34" filter="url(#{g('soft')})"/>
  </g>
</g>

<g><path d="{thigh.d()}" fill="url(#{g('thigh')})"/>
  <g clip-path="url(#{g('ctorso')})">{render_fur(edge_fur(thigh, 150, False, rng,
      [(BASE, .8, .30), (LIGHT, .8, .34), (SHADE, .7, .18)], length=(8, 18), spread=.55))}</g>
  <g clip-path="url(#{g('cthigh')})">
    {render_fur(thigh_fur)}
    <ellipse cx="196" cy="254" rx="48" ry="34" fill="#FFFEF9" opacity=".20" filter="url(#{g('soft')})"/>
    <path d="M154 262C168 246 196 244 214 258" stroke="#FFFEF9" stroke-width="14" fill="none" opacity=".22" filter="url(#{g('soft')})"/>
    <ellipse cx="176" cy="320" rx="42" ry="22" fill="#6E5B47" opacity=".32" filter="url(#{g('soft')})"/>
  </g>
  <path d="{thigh.d()}" fill="none" stroke="#FFF9EE" stroke-width="2.6" mask="url(#{g('rimmask')})" opacity=".55" filter="url(#{g('soft2')})"/>
</g>

<g>{render_fur(leg_edge)}
  <path d="{hindfoot.d()}" fill="#E9DFCE"/>
  <path d="M118 272C111 292 108 306 108 320" stroke="#6E5B47" stroke-width="9" fill="none" opacity=".24" filter="url(#{g('soft2')})"/>
  <path d="{foreleg_near.d()}" fill="#E7DDCB"/>
  {render_fur(leg_fur)}
  <ellipse cx="124" cy="272" rx="22" ry="14" fill="#E4DAC7" opacity=".85" filter="url(#{g('soft3')})"/>
  {render_fur(fur_layers([dict(ell=(124, 274, 24, 16), n=110, flow=lambda x, y: math.pi/2+.3, tones=LITE_T, len=(6, 13), curve=1.0)], rng))}
  <ellipse cx="152" cy="334" rx="34" ry="6" fill="#6E5B47" opacity=".30" filter="url(#{g('soft2')})"/>
  <g fill="#8A7458" opacity=".26" filter="url(#{g('soft3')})">
    <ellipse cx="128" cy="333" rx="3" ry="6"/><ellipse cx="120" cy="333" rx="3" ry="6"/>
    <ellipse cx="112" cy="331" rx="3" ry="6"/>
  </g>
  <ellipse cx="172" cy="312" rx="26" ry="9" fill="#FFFDF6" opacity=".40" filter="url(#{g('soft2')})"/>
</g>

<g transform="translate(7,-15)">{render_fur(head_edge)}
  <path d="{head.d()}" fill="url(#{g('head')})"/>
  <g clip-path="url(#{g('chead')})">
    {render_fur(head_fur)}
    <ellipse cx="104" cy="124" rx="44" ry="24" fill="#FFFEFB" opacity=".44" filter="url(#{g('soft')})"/>
    <ellipse cx="176" cy="200" rx="32" ry="30" fill="#6E5B47" opacity=".32" filter="url(#{g('soft')})"/>
    <ellipse cx="126" cy="222" rx="42" ry="16" fill="#6E5B47" opacity=".26" filter="url(#{g('soft')})"/>
    <ellipse cx="118" cy="182" rx="30" ry="22" fill="#FFFDF6" opacity=".45" filter="url(#{g('soft2')})"/>
    <ellipse cx="122" cy="206" rx="24" ry="11" fill="#8A7458" opacity=".22" filter="url(#{g('soft2')})"/>
    <ellipse cx="66" cy="196" rx="22" ry="24" fill="#8A7458" opacity=".16" filter="url(#{g('soft')})"/>
    <ellipse cx="80" cy="192" rx="20" ry="14" fill="#F2A0AE" opacity=".26" filter="url(#{g('soft')})"/>
    <ellipse cx="164" cy="188" rx="19" ry="13" fill="#F2A0AE" opacity=".22" filter="url(#{g('soft')})"/>
  </g>
  <path d="{head.d()}" fill="none" stroke="#FFF9EE" stroke-width="2.8" mask="url(#{g('rimmask')})" opacity=".8" filter="url(#{g('soft2')})"/>
</g>

<g transform="translate(7,-15)">
  {eye(90, 156, 13.2)}
  {eye(160, 153, 12.3, sq=0.90, tilt=8)}
  <ellipse cx="120" cy="190" rx="24" ry="16" fill="#8A7458" opacity=".16" filter="url(#{g('soft2')})"/>
  <ellipse cx="103" cy="191" rx="15" ry="12" fill="#FFFDF6" opacity=".40" filter="url(#{g('soft2')})"/>
  <ellipse cx="137" cy="190" rx="15" ry="12" fill="#FFFDF6" opacity=".32" filter="url(#{g('soft2')})"/>
  <path d="M110 180C114 176 126 176 130 181C133 186 126 194 120 194C113 194 107 185 110 180Z" fill="url(#{g('nose')})"/>
  <path d="M113 180C117 178 123 178 126 181" stroke="#FFE6EC" stroke-width="1.6" fill="none" opacity=".6" stroke-linecap="round"/>
  <path d="M112 184C110 186 110 189 113 189C115 189 116 186 115 184" fill="#9E4560" opacity=".7"/>
  <path d="M128 184C130 186 130 189 127 189C125 189 124 186 125 184" fill="#9E4560" opacity=".7"/>
  <path d="M120 194C120 198 120 200 120 201" stroke="#8A7057" stroke-width="1.5" fill="none" stroke-linecap="round" opacity=".7"/>
  <path d="M120 201C117 206 111 206 108 202M120 201C123 206 129 206 132 202" stroke="#8A7057" stroke-width="1.5" fill="none" stroke-linecap="round" opacity=".7"/>
  <ellipse cx="120" cy="210" rx="17" ry="8" fill="#8A7458" opacity=".20" filter="url(#{g('soft2')})"/>
  <g fill="#A08A6E" opacity=".38">
    <circle cx="99" cy="188" r=".9"/><circle cx="94" cy="192" r=".9"/><circle cx="100" cy="196" r=".9"/>
    <circle cx="141" cy="188" r=".9"/><circle cx="146" cy="191" r=".9"/><circle cx="140" cy="195" r=".9"/>
  </g>
  <g stroke="#6E5B47" fill="none" stroke-linecap="round">
    <path d="M96 187C74 180 54 178 38 182" stroke-width="1" opacity=".34"/>
    <path d="M95 192C73 190 53 194 38 202" stroke-width=".9" opacity=".30"/>
    <path d="M96 197C76 200 60 208 48 219" stroke-width=".85" opacity=".26"/>
    <path d="M97 182C78 172 62 166 48 165" stroke-width=".85" opacity=".26"/>
    <path d="M144 187C166 181 186 180 202 184" stroke-width="1" opacity=".32"/>
    <path d="M145 192C167 191 187 196 202 204" stroke-width=".9" opacity=".28"/>
    <path d="M144 197C164 201 180 209 192 220" stroke-width=".85" opacity=".24"/>
    <path d="M143 182C162 173 178 168 192 167" stroke-width=".85" opacity=".24"/>
    <path d="M84 136C74 126 62 122 51 123" stroke-width=".8" opacity=".26"/>
    <path d="M166 133C176 124 188 120 199 121" stroke-width=".8" opacity=".24"/>
  </g>
</g>
</g>
</svg>'''
open(os.path.join(HERE, 'out', 'rabbit.svg'), 'w').write(svg)
print("bytes", len(svg))
