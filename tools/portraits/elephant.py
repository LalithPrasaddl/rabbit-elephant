import math, random, sys
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from furlib import BPath, fur_layers, edge_fur, render_fur, cubic, rings, speckle

rng = random.Random(31337)
P = "e"
# Authored facing viewer-left, mirrored at the end -> faces right, lit from upper-right.
DEEP, SHADE, BASE, LIGHT, HI = "#3A525D", "#6E8A98", "#A8C0CC", "#CFE0E8", "#EEF6FA"
EARB, EARL = "#B0C9D4", "#DCEAF0"

def g(i): return f"{P}-{i}"

# ---------------- silhouettes ----------------
body = (BPath((140, 174))
    .c((122, 194), (116, 236), (129, 264))
    .c((146, 290), (180, 283), (212, 283))
    .c((252, 283), (280, 256), (282, 216))
    .c((284, 176), (258, 148), (218, 145))
    .c((184, 142), (156, 156), (140, 174)))

head = (BPath((64, 166))
    .c((60, 128), (84, 100), (120, 100))
    .c((156, 100), (181, 126), (178, 164))
    .c((176, 198), (163, 226), (141, 238))
    .c((129, 244), (110, 244), (98, 238))
    .c((76, 226), (66, 200), (64, 166)))

ear_near = (BPath((150, 114))
    .c((190, 98), (222, 126), (222, 172))
    .c((222, 208), (207, 236), (187, 248))
    .c((177, 254), (175, 242), (165, 249))
    .c((153, 257), (151, 244), (140, 247))
    .c((126, 250), (120, 204), (124, 158))
    .c((127, 130), (140, 116), (150, 114)))

# left ear: the near ear mirrored about the head's centre line (x = 119)
ear_left = (BPath((88, 114))
    .c((48, 98), (16, 126), (16, 172))
    .c((16, 208), (31, 236), (51, 248))
    .c((61, 254), (63, 242), (73, 249))
    .c((85, 257), (87, 244), (98, 247))
    .c((112, 250), (118, 204), (114, 158))
    .c((111, 130), (98, 116), (88, 114)))

# trunk centreline: from the front of the face, down with a forward curl
TRUNK = ((119, 176), (107, 236), (116, 288), (108, 322))
def trunk_w(t): return 8.5 + 26.0*(1.0-t)**2.6
trunk_pts = cubic(*TRUNK, 64)
def trunk_path():
    L, R = [], []
    for ((x, y), (tx, ty), t) in trunk_pts:
        nx, ny = -ty, tx; w = trunk_w(t)
        L.append((x-nx*w, y-ny*w)); R.append((x+nx*w, y+ny*w))
    pts = L + R[::-1]
    return "M" + " L".join("%.1f %.1f" % p for p in pts) + "Z"

def leg(xt, xb, top, bot, wt, wb):
    m = (bot-top)*0.45
    return (BPath((xt-wt, top))
        .c((xt-wt-3, top+m), (xb-wb-2, bot-26), (xb-wb, bot-9))
        .c((xb-wb, bot+4), (xb-wb*0.55, bot+7), (xb, bot+7))
        .c((xb+wb*0.55, bot+7), (xb+wb, bot+4), (xb+wb, bot-9))
        .c((xb+wb+2, bot-26), (xt+wt+3, top+m), (xt+wt, top)))

leg_fn = leg(152, 147, 206, 330, 28, 24)   # front near
leg_ff = leg(190, 192, 204, 320, 24, 20)   # front far
leg_bn = leg(250, 254, 212, 330, 30, 25)   # hind near
leg_bf = leg(222, 222, 208, 318, 24, 19)   # hind far

# ---------------- texture ----------------
def tangential(ox, oy):
    return lambda x, y: math.atan2(y-oy, x-ox) + math.pi/2

CR_D = [("#2C4149", 1.3, .11), ("#3A525D", 1.1, .09)]
CR_L = [("#E4F0F6", 1.1, .14), ("#CFE0E8", 1.0, .10)]
HAIR = [("#2C4149", .6, .28), ("#5E7885", .55, .20)]

body_creases = fur_layers([
    dict(ell=(202, 214, 74, 56), n=300, flow=tangential(208, 180), tones=CR_D, len=(7, 20), curve=2.2, jitter=.42),
    dict(ell=(202, 214, 74, 56), n=210, flow=tangential(208, 180), tones=CR_L, len=(6, 17), curve=2.2, jitter=.42),
], rng)
head_creases = fur_layers([
    dict(ell=(120, 168, 58, 66), n=230, flow=tangential(120, 116), tones=CR_D, len=(5, 14), curve=1.8, jitter=.45),
    dict(ell=(120, 168, 58, 66), n=160, flow=tangential(120, 116), tones=CR_L, len=(5, 12), curve=1.8, jitter=.45),
], rng)
leg_creases = fur_layers([
    dict(ell=(150, 262, 27, 46), n=90, flow=lambda x, y: 0.05, tones=CR_D, len=(16, 34), curve=2.2, jitter=.16),
    dict(ell=(252, 266, 29, 46), n=90, flow=lambda x, y: -0.05, tones=CR_D, len=(16, 36), curve=2.2, jitter=.16),
    dict(ell=(150, 296, 25, 32), n=55, flow=lambda x, y: 0.05, tones=CR_L, len=(14, 28), curve=2.0, jitter=.16),
    dict(ell=(252, 300, 27, 32), n=55, flow=lambda x, y: -0.05, tones=CR_L, len=(14, 30), curve=2.0, jitter=.16),
], rng)
trunk_d = rings(cubic(*TRUNK, 34, .05, .97), lambda t: trunk_w(t)*.92, 34, rng, "#2C4149", .20, 1.5, .38)
trunk_l = rings(cubic(*TRUNK, 34, .11, .93), lambda t: trunk_w(t)*.76, 34, rng, "#EAF4F9", .22, 1.2, .38)

body_mottle = speckle([dict(ell=(202, 214, 70, 53), n=150,
    tones=[("#3A525D", .05), ("#E4F0F6", .06), ("#6E8A98", .04)], r=(4, 11))], rng)
head_mottle = speckle([dict(ell=(120, 168, 54, 62), n=95,
    tones=[("#3A525D", .05), ("#E4F0F6", .06)], r=(3, 8))], rng)
crown_hair = fur_layers([
    dict(ell=(118, 102, 20, 3), n=11, flow=lambda x, y: -math.pi/2 + .15, tones=HAIR, len=(3, 6), curve=.6, jitter=.4),
], rng)
tail_hair = fur_layers([
    dict(ell=(283, 286, 5, 8), n=34, flow=lambda x, y: math.pi/2 + .3, tones=HAIR, len=(7, 16), curve=.8, jitter=.3),
], rng)

def eye(cx, cy, s, sq=1.0, tilt=-8, lid=0.10):
    """Small, set into a brow hollow. Soft lashes - spiky ones read witchy at this scale."""
    rx, ry = s*sq, s*1.04
    cid, lidid = g(f"eye{int(cx)}"), g(f"lid{int(cx)}")
    return f'''<g transform="rotate({tilt} {cx} {cy})">
  <ellipse cx="{cx}" cy="{cy}" rx="{rx*1.7:.1f}" ry="{ry*1.5:.1f}" fill="#22333A" opacity=".26" filter="url(#{g('soft2')})"/>
  <clipPath id="{cid}"><ellipse cx="{cx}" cy="{cy}" rx="{rx:.1f}" ry="{ry:.1f}"/></clipPath>
  <ellipse cx="{cx}" cy="{cy}" rx="{rx:.1f}" ry="{ry:.1f}" fill="url(#{g('iris')})"/>
  <g clip-path="url(#{cid})">
    <circle cx="{cx}" cy="{cy+ry*.06:.1f}" r="{ry*.44:.1f}" fill="#140D07"/>
    <ellipse cx="{cx}" cy="{cy+ry*.92:.1f}" rx="{rx*.85:.1f}" ry="{ry*.45:.1f}" fill="#C08A55" opacity=".28" filter="url(#{g('soft3')})"/>
    <ellipse cx="{cx}" cy="{cy-ry*1.02:.1f}" rx="{rx*1.3:.1f}" ry="{ry*.50:.1f}" fill="#000" opacity=".24" filter="url(#{g('soft3')})"/>
  </g>
  <ellipse cx="{cx}" cy="{cy}" rx="{rx:.1f}" ry="{ry:.1f}" fill="none" stroke="#2F444E" stroke-width="{max(0.8, s*.10):.1f}" opacity=".42"/>
  <ellipse cx="{cx-rx*.34:.1f}" cy="{cy-ry*.06:.1f}" rx="{rx*.24:.1f}" ry="{ry*.26:.1f}" fill="#fff" opacity=".9"/>
  <clipPath id="{lidid}"><ellipse cx="{cx}" cy="{cy}" rx="{rx+1.2:.1f}" ry="{ry+1.2:.1f}"/></clipPath>
  <g clip-path="url(#{lidid})">
    <ellipse cx="{cx}" cy="{cy-ry*(1+lid):.1f}" rx="{rx*1.6:.1f}" ry="{ry*1.05:.1f}" fill="#9DB6C3" filter="url(#{g('soft3')})"/>
  </g>
  <path d="M{cx-rx*1.25:.1f} {cy-ry*.55:.1f}Q{cx:.1f} {cy-ry*1.5:.1f} {cx+rx*1.25:.1f} {cy-ry*.5:.1f}"
        stroke="#2F444E" stroke-width="{max(0.8, s*.11):.1f}" fill="none" opacity=".18" stroke-linecap="round"/>
</g>'''

svg = f'''<svg viewBox="0 0 320 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
<defs>
  <radialGradient id="{g('body')}" cx="34%" cy="18%" r="88%">
    <stop offset="0" stop-color="{HI}"/><stop offset="32%" stop-color="{LIGHT}"/>
    <stop offset="64%" stop-color="{BASE}"/><stop offset="1" stop-color="#455F6B"/>
  </radialGradient>
  <radialGradient id="{g('head')}" cx="30%" cy="16%" r="88%">
    <stop offset="0" stop-color="{HI}"/><stop offset="30%" stop-color="{LIGHT}"/>
    <stop offset="62%" stop-color="{BASE}"/><stop offset="1" stop-color="#48626E"/>
  </radialGradient>
  <linearGradient id="{g('trunk')}" x1="0.1" y1="0" x2="1" y2="0.25">
    <stop offset="0" stop-color="#E2EFF5"/><stop offset="42%" stop-color="{BASE}"/>
    <stop offset="1" stop-color="#455F6B"/>
  </linearGradient>
  <radialGradient id="{g('earl')}" cx="60%" cy="22%" r="86%">
    <stop offset="0" stop-color="{EARB}"/><stop offset="52%" stop-color="#9CB6C3"/>
    <stop offset="1" stop-color="#46606C"/>
  </radialGradient>
  <radialGradient id="{g('ear')}" cx="34%" cy="22%" r="86%">
    <stop offset="0" stop-color="{EARL}"/><stop offset="44%" stop-color="{EARB}"/>
    <stop offset="1" stop-color="#55707D"/>
  </radialGradient>
  <linearGradient id="{g('legg')}" x1="0.1" y1="0" x2="1" y2="0.2">
    <stop offset="0" stop-color="#D2E3EB"/><stop offset="48%" stop-color="#A5BFCB"/>
    <stop offset="1" stop-color="#445E6A"/>
  </linearGradient>
  <linearGradient id="{g('legf')}" x1="0.1" y1="0" x2="1" y2="0.2">
    <stop offset="0" stop-color="#A0B9C6"/><stop offset="1" stop-color="#546E7A"/>
  </linearGradient>
  <radialGradient id="{g('iris')}" cx="34%" cy="28%" r="76%">
    <stop offset="0" stop-color="#7A5231"/><stop offset="45%" stop-color="#3E2716"/>
    <stop offset="1" stop-color="#0E0906"/>
  </radialGradient>
  <linearGradient id="{g('rim')}" x1="0" y1="0" x2="0.9" y2="1">
    <stop offset="0" stop-color="#fff"/><stop offset=".4" stop-color="#fff" stop-opacity=".22"/>
    <stop offset=".76" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <filter id="{g('soft')}" x="-150%" y="-150%" width="400%" height="400%"><feGaussianBlur stdDeviation="8"/></filter>
  <filter id="{g('soft2')}" x="-150%" y="-150%" width="400%" height="400%"><feGaussianBlur stdDeviation="3.4"/></filter>
  <filter id="{g('soft3')}" x="-150%" y="-150%" width="400%" height="400%"><feGaussianBlur stdDeviation="1.6"/></filter>
  <clipPath id="{g('cbody')}"><path d="{body.d()}"/></clipPath>
  <clipPath id="{g('chead')}"><path d="{head.d()}"/></clipPath>
  <clipPath id="{g('cear')}"><path d="{ear_near.d()}"/></clipPath>
  <clipPath id="{g('cearl')}"><path d="{ear_left.d()}"/></clipPath>
  <clipPath id="{g('ctrunk')}"><path d="{trunk_path()}"/></clipPath>
  <clipPath id="{g('clegs')}"><path d="{leg_fn.d()}"/><path d="{leg_bn.d()}"/></clipPath>
  <linearGradient id="{g('legfade')}" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#000"/><stop offset=".24" stop-color="#000"/>
    <stop offset=".46" stop-color="#fff"/><stop offset="1" stop-color="#fff"/>
  </linearGradient>
  <mask id="{g('legmask')}"><rect y="180" width="320" height="180" fill="url(#{g('legfade')})"/></mask>
  <mask id="{g('rimmask')}"><rect width="320" height="360" fill="url(#{g('rim')})"/></mask>
</defs>

<g transform="translate(320,0) scale(-1,1)">
<ellipse cx="200" cy="332" rx="106" ry="15" fill="#2C4149" opacity=".30" filter="url(#{g('soft')})"/>

<!-- tail -->
<g>{render_fur(tail_hair)}
  <path d="M268 210C284 228 288 258 283 280" stroke="#7E97A4" stroke-width="7" fill="none" stroke-linecap="round"/>
  <path d="M269 214C283 230 286 256 282 276" stroke="#CFE0E8" stroke-width="2.2" fill="none" stroke-linecap="round" opacity=".45"/></g>

<!-- far legs -->
<g><path d="{leg_ff.d()}" fill="url(#{g('legf')})"/><path d="{leg_bf.d()}" fill="url(#{g('legf')})"/>
  <ellipse cx="192" cy="318" rx="21" ry="7" fill="#2C4149" opacity=".45"/>
  <ellipse cx="222" cy="316" rx="20" ry="7" fill="#2C4149" opacity=".45"/></g>

<!-- body -->
<g>
  <path d="{body.d()}" fill="url(#{g('body')})"/>
  <g clip-path="url(#{g('cbody')})">
    {body_mottle}
    {render_fur(body_creases)}
    <ellipse cx="216" cy="166" rx="72" ry="26" fill="{HI}" opacity=".32" filter="url(#{g('soft')})"/>
    <ellipse cx="148" cy="264" rx="52" ry="32" fill="#2C4149" opacity=".32" filter="url(#{g('soft')})"/>
    <ellipse cx="222" cy="272" rx="76" ry="22" fill="#2C4149" opacity=".32" filter="url(#{g('soft')})"/>
    <ellipse cx="150" cy="192" rx="34" ry="34" fill="#2C4149" opacity=".24" filter="url(#{g('soft')})"/>
  </g>
  {render_fur(crown_hair)}
  <path d="{body.d()}" fill="none" stroke="{HI}" stroke-width="3" mask="url(#{g('rimmask')})" opacity=".8" filter="url(#{g('soft2')})"/>
</g>

<!-- near legs -->
<g mask="url(#{g('legmask')})">
  <path d="{leg_fn.d()}" fill="url(#{g('legg')})"/>
  <path d="{leg_bn.d()}" fill="url(#{g('legg')})"/>
  <g clip-path="url(#{g('clegs')})">
    {render_fur(leg_creases)}
    <ellipse cx="150" cy="252" rx="40" ry="26" fill="#2C4149" opacity=".24" filter="url(#{g('soft')})"/>
    <ellipse cx="250" cy="256" rx="40" ry="26" fill="#2C4149" opacity=".24" filter="url(#{g('soft')})"/>
    <ellipse cx="140" cy="300" rx="10" ry="42" fill="{HI}" opacity=".20" filter="url(#{g('soft')})"/>
    <ellipse cx="246" cy="300" rx="10" ry="42" fill="{HI}" opacity=".20" filter="url(#{g('soft')})"/>
  </g>
  <g fill="#E9F2F7" opacity=".92">
    <ellipse cx="131" cy="329" rx="6" ry="4.4"/><ellipse cx="146" cy="331" rx="6.4" ry="4.7"/><ellipse cx="161" cy="329" rx="6" ry="4.4"/>
    <ellipse cx="238" cy="329" rx="6" ry="4.4"/><ellipse cx="254" cy="331" rx="6.4" ry="4.7"/><ellipse cx="269" cy="329" rx="6" ry="4.4"/>
  </g>
  <g fill="none" stroke="#2C4149" opacity=".22" stroke-width="1.2">
    <path d="M125 323q24 6 48 0"/><path d="M230 323q26 6 50 0"/>
  </g>
</g>

<!-- ear: fans back over the shoulder; the head covers its front attachment -->
<g transform="translate(0,-10)">
  <path d="{ear_near.d()}" fill="url(#{g('ear')})"/>
  <g clip-path="url(#{g('cear')})">
    <ellipse cx="188" cy="140" rx="52" ry="40" fill="{HI}" opacity=".30" filter="url(#{g('soft')})"/>
    <ellipse cx="132" cy="214" rx="38" ry="46" fill="#2C4149" opacity=".36" filter="url(#{g('soft')})"/>
    <g stroke="#6E8A98" fill="none" stroke-linecap="round" opacity=".45">
      <path d="M132 138C158 148 186 162 206 184" stroke-width="2.1"/>
      <path d="M132 162C156 174 180 194 194 218" stroke-width="1.8"/>
      <path d="M136 186C154 200 170 218 178 240" stroke-width="1.5"/>
      <path d="M158 152q13 -13 26 -16" stroke-width="1.3"/>
      <path d="M166 180q15 -11 30 -12" stroke-width="1.2"/>
      <path d="M162 206q10 11 14 24" stroke-width="1.1"/>
    </g>
    <path d="{ear_near.d()}" fill="none" stroke="{EARL}" stroke-width="9" opacity=".55" filter="url(#{g('soft2')})"/>
    <path d="{head.d()}" fill="#22333A" opacity=".34" filter="url(#{g('soft')})" transform="translate(12,7)"/>
  </g>
  <path d="{ear_near.d()}" fill="none" stroke="#3E5661" stroke-width="1.6" opacity=".38"/>
  <path d="{ear_left.d()}" fill="url(#{g('earl')})"/>
  <g clip-path="url(#{g('cearl')})">
    <ellipse cx="50" cy="140" rx="52" ry="40" fill="{HI}" opacity=".18" filter="url(#{g('soft')})"/>
    <ellipse cx="106" cy="214" rx="38" ry="46" fill="#22333A" opacity=".30" filter="url(#{g('soft')})"/>
    <g stroke="#5E7885" fill="none" stroke-linecap="round" opacity=".40">
      <path d="M106 138C80 148 52 162 32 184" stroke-width="2.1"/>
      <path d="M106 162C82 174 58 194 44 218" stroke-width="1.8"/>
      <path d="M102 186C84 200 68 218 60 240" stroke-width="1.5"/>
      <path d="M80 152q-13 -13 -26 -16" stroke-width="1.3"/>
      <path d="M72 180q-15 -11 -30 -12" stroke-width="1.2"/>
      <path d="M76 206q-10 11 -14 24" stroke-width="1.1"/>
    </g>
    <path d="{ear_left.d()}" fill="none" stroke="{EARL}" stroke-width="9" opacity=".38" filter="url(#{g('soft2')})"/>
    <path d="{head.d()}" fill="#22333A" opacity=".30" filter="url(#{g('soft')})" transform="translate(-10,7)"/>
  </g>
  <path d="{ear_left.d()}" fill="none" stroke="#3E5661" stroke-width="1.6" opacity=".30"/>
  <path d="{ear_near.d()}" fill="none" stroke="{HI}" stroke-width="2.4" mask="url(#{g('rimmask')})" opacity=".65" filter="url(#{g('soft2')})"/>
</g>

<!-- head -->
<g transform="translate(0,-10)">
  <path d="{head.d()}" fill="url(#{g('head')})"/>
  <g clip-path="url(#{g('chead')})">
    {head_mottle}
    {render_fur(head_creases)}
    <ellipse cx="102" cy="126" rx="42" ry="22" fill="{HI}" opacity=".40" filter="url(#{g('soft')})"/>
    <ellipse cx="164" cy="210" rx="28" ry="28" fill="#2C4149" opacity=".30" filter="url(#{g('soft')})"/>
    <path d="M80 160q22 -13 44 -5" stroke="#22333A" stroke-width="7" fill="none" opacity=".22" filter="url(#{g('soft2')})"/>
    <path d="M104 108q10 22 8 46" stroke="#22333A" stroke-width="9" fill="none" opacity=".16" filter="url(#{g('soft2')})"/>
    <ellipse cx="96" cy="130" rx="20" ry="16" fill="{HI}" opacity=".38" filter="url(#{g('soft')})"/>
    <ellipse cx="132" cy="126" rx="18" ry="15" fill="{HI}" opacity=".30" filter="url(#{g('soft')})"/>
    <ellipse cx="108" cy="206" rx="26" ry="20" fill="#22333A" opacity=".24" filter="url(#{g('soft')})"/>
    <path d="M119 112q3 30 1 62" stroke="#22333A" stroke-width="8" fill="none" opacity=".13" filter="url(#{g('soft2')})"/>
    <path d="M113 116q-2 28 -1 56" stroke="{HI}" stroke-width="5" fill="none" opacity=".14" filter="url(#{g('soft2')})"/>
    <path d="M76 164q13 -11 26 -4" stroke="#22333A" stroke-width="7" fill="none" opacity=".24" filter="url(#{g('soft2')})"/>
    <path d="M138 160q13 -10 25 -2" stroke="#22333A" stroke-width="6" fill="none" opacity=".20" filter="url(#{g('soft2')})"/>
    <ellipse cx="70" cy="188" rx="14" ry="18" fill="#22333A" opacity=".20" filter="url(#{g('soft2')})"/>
    <ellipse cx="170" cy="184" rx="13" ry="17" fill="#22333A" opacity=".18" filter="url(#{g('soft2')})"/>
    <ellipse cx="119" cy="226" rx="30" ry="14" fill="#22333A" opacity=".18" filter="url(#{g('soft2')})"/>
    <ellipse cx="72" cy="197" rx="21" ry="15" fill="#E0A79E" opacity=".20" filter="url(#{g('soft')})"/>
    <ellipse cx="168" cy="193" rx="20" ry="14" fill="#E0A79E" opacity=".17" filter="url(#{g('soft')})"/>
  </g>
  <path d="{head.d()}" fill="none" stroke="{HI}" stroke-width="2.8" mask="url(#{g('rimmask')})" opacity=".75" filter="url(#{g('soft2')})"/>
</g>

<!-- tusks -->
<g transform="translate(0,-10)">
  <path d="M100 216C99 230 95 242 88 251C84 256 79 253 82 247C89 237 93 227 93 214Z" fill="#F4F0E3"/>
  <path d="M98 219C95 231 91 240 85 248" stroke="#C8BFA6" stroke-width="1.3" fill="none" opacity=".55"/>
  <path d="M139 214C140 228 144 240 151 249C155 254 160 251 157 245C150 235 146 225 146 212Z" fill="#E3DCC8" opacity=".92"/>
</g>

<!-- trunk -->
<g transform="translate(0,-10)">
  <ellipse cx="119" cy="184" rx="30" ry="22" fill="#A8C0CC" filter="url(#{g('soft2')})"/>
  <path d="{trunk_path()}" fill="url(#{g('trunk')})"/>
  <ellipse cx="119" cy="180" rx="26" ry="15" fill="#B6CCD6" opacity=".8" filter="url(#{g('soft2')})"/>
  <g clip-path="url(#{g('ctrunk')})">
    {render_fur(trunk_d)}{render_fur(trunk_l)}
    <path d="M{TRUNK[0][0]-8} {TRUNK[0][1]}C{TRUNK[1][0]-8} {TRUNK[1][1]} {TRUNK[2][0]-8} {TRUNK[2][1]} {TRUNK[3][0]-6} {TRUNK[3][1]}"
          stroke="{HI}" stroke-width="8" fill="none" opacity=".26" filter="url(#{g('soft2')})"/>
    <path d="M{TRUNK[0][0]+9} {TRUNK[0][1]}C{TRUNK[1][0]+10} {TRUNK[1][1]} {TRUNK[2][0]+10} {TRUNK[2][1]} {TRUNK[3][0]+7} {TRUNK[3][1]}"
          stroke="#2C4149" stroke-width="9" fill="none" opacity=".26" filter="url(#{g('soft2')})"/>
  </g>
  <ellipse cx="108" cy="321" rx="10" ry="7.5" fill="#93AEBB"/>
  <path d="M102 319q6 -4 12 0" stroke="#2C4149" stroke-width="1.3" fill="none" opacity=".45"/>
  <ellipse cx="105" cy="323" rx="2.3" ry="1.8" fill="#2C4149" opacity=".5"/>
  <ellipse cx="112" cy="323" rx="2.3" ry="1.8" fill="#2C4149" opacity=".5"/>
</g>

<!-- face -->
<g transform="translate(0,-10)">{eye(89, 174, 10.4)}{eye(151, 170, 9.7, sq=0.92, tilt=6)}</g>
</g>
</svg>'''
open(os.path.join(HERE, 'out', 'elephant.svg'), 'w').write(svg)
print("bytes", len(svg))
