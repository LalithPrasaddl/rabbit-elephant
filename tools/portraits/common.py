"""Shared scaffolding for the character portraits.

Conventions (learned the hard way on Rabbit + Elephant):
  * Author facing viewer-LEFT with light from upper-LEFT, then wrap everything in
    MIRROR so the finished portrait faces right and is lit from the upper-RIGHT.
  * Heads are FRONT-FACING: both eyes sit either side of the muzzle. A profile head
    with eyes placed symmetrically about the head's 2D centre puts one eye on the nose.
  * Blur filters need a generous region or the blur clips into a visible rectangle.
  * viewBox is always 0 0 320 360; feet baseline ~y 330.
"""
import math

VIEWBOX = "0 0 320 360"
MIRROR_OPEN = '<g transform="translate(320,0) scale(-1,1)">'
MIRROR_CLOSE = '</g>'


def defs_common(P, iris=("#8A5F3A", "#4A2E1B", "#120A05")):
    g = lambda i: f"{P}-{i}"
    return f'''
  <radialGradient id="{g('iris')}" cx="34%" cy="28%" r="76%">
    <stop offset="0" stop-color="{iris[0]}"/><stop offset="45%" stop-color="{iris[1]}"/>
    <stop offset="1" stop-color="{iris[2]}"/>
  </radialGradient>
  <linearGradient id="{g('rim')}" x1="0" y1="0" x2="0.9" y2="1">
    <stop offset="0" stop-color="#fff"/><stop offset=".42" stop-color="#fff" stop-opacity=".22"/>
    <stop offset=".78" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <filter id="{g('soft')}" x="-150%" y="-150%" width="400%" height="400%"><feGaussianBlur stdDeviation="8"/></filter>
  <filter id="{g('soft2')}" x="-150%" y="-150%" width="400%" height="400%"><feGaussianBlur stdDeviation="3.4"/></filter>
  <filter id="{g('soft3')}" x="-150%" y="-150%" width="400%" height="400%"><feGaussianBlur stdDeviation="1.6"/></filter>
  <mask id="{g('rimmask')}"><rect width="320" height="360" fill="url(#{g('rim')})"/></mask>'''


def make_eye(P, socket="#5A4633", lidfill="#DDD0B9", rimcol="#5E4A34"):
    """Returns eye(cx, cy, size, sq=1.0, tilt=-10, lid=0.09).

    `sq` foreshortens horizontally - keep it >= 0.7 or the eye collapses into a slit.
    `lid` is how far the upper eyelid covers; a little reads calm, none reads startled.
    """
    g = lambda i: f"{P}-{i}"
    def eye(cx, cy, s, sq=1.0, tilt=-10, lid=0.09):
        rx, ry = s*sq, s*1.06
        cid, lidid = g(f"eye{int(cx)}{int(cy)}"), g(f"lid{int(cx)}{int(cy)}")
        return f'''<g transform="rotate({tilt} {cx} {cy})">
  <ellipse cx="{cx}" cy="{cy}" rx="{rx*1.5:.1f}" ry="{ry*1.35:.1f}" fill="{socket}" opacity=".26" filter="url(#{g('soft2')})"/>
  <clipPath id="{cid}"><ellipse cx="{cx}" cy="{cy}" rx="{rx:.1f}" ry="{ry:.1f}"/></clipPath>
  <ellipse cx="{cx}" cy="{cy}" rx="{rx:.1f}" ry="{ry:.1f}" fill="url(#{g('iris')})"/>
  <g clip-path="url(#{cid})">
    <circle cx="{cx}" cy="{cy+ry*.06:.1f}" r="{ry*.46:.1f}" fill="#160E08"/>
    <ellipse cx="{cx}" cy="{cy+ry*.92:.1f}" rx="{rx*.85:.1f}" ry="{ry*.45:.1f}" fill="#C08A55" opacity=".30" filter="url(#{g('soft3')})"/>
    <ellipse cx="{cx}" cy="{cy-ry*1.02:.1f}" rx="{rx*1.3:.1f}" ry="{ry*.50:.1f}" fill="#000" opacity=".24" filter="url(#{g('soft3')})"/>
  </g>
  <ellipse cx="{cx}" cy="{cy}" rx="{rx:.1f}" ry="{ry:.1f}" fill="none" stroke="{rimcol}" stroke-width="{max(0.9, s*.09):.1f}" opacity=".38"/>
  <ellipse cx="{cx-rx*.34:.1f}" cy="{cy-ry*.08:.1f}" rx="{rx*.22:.1f}" ry="{ry*.24:.1f}" fill="#fff" opacity=".92"/>
  <ellipse cx="{cx+rx*.34:.1f}" cy="{cy+ry*.44:.1f}" rx="{rx*.11:.1f}" ry="{ry*.12:.1f}" fill="#FFE7C9" opacity=".45"/>
  <clipPath id="{lidid}"><ellipse cx="{cx}" cy="{cy}" rx="{rx+1.4:.1f}" ry="{ry+1.4:.1f}"/></clipPath>
  <g clip-path="url(#{lidid})">
    <ellipse cx="{cx}" cy="{cy-ry*(1+lid):.1f}" rx="{rx*1.6:.1f}" ry="{ry*1.05:.1f}" fill="{lidfill}" filter="url(#{g('soft3')})"/>
  </g>
</g>'''
    return eye


def svg(P, defs, content):
    return (f'<svg viewBox="{VIEWBOX}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">\n'
            f'<defs>{defs}</defs>\n{MIRROR_OPEN}\n{content}\n{MIRROR_CLOSE}\n</svg>')
