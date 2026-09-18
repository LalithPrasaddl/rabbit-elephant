"""Background and staging helpers for the in-story page illustrations.

CLAUDE.md already specifies how a page background should be built - layered sky
gradient, sun, asymmetric clouds, a wavy two-band ground, tufts and flowers - and
how a speech bubble should be sized. Every page currently re-types that by hand and
drifts from it: story 01 page 1 fills its sky with a flat <rect>, and several
bubbles are eyeballed narrower than their text. These functions are that spec,
executed, so a page gets it right by calling instead of by remembering.

Pages are 500x360 with the horizon around y=205.
"""

MOODS = {                        # top -> bottom sky, picked by the beat, per CLAUDE.md
    'morning': ("#BEE7FB", "#EAF9FF"),
    'golden':  ("#FFE8B0", "#FFF5D8"),
    'tender':  ("#FFE3D6", "#FFF6EE"),   # confusion, a small mishap, a quiet feeling
    'sunset':  ("#FFB99A", "#FFE9CE"),   # end of the day - warm, never dark
}
FLOWERS = ("#FF6B6B", "#FFD166", "#C77DFF", "#74C8E4", "#FF9BAE")
INK = "#2D3748"


def sky(uid, mood='morning', sun=(430, 58), clouds=((90, 48, 40, 16), (116, 40, 24, 14), (420, 74, 34, 14)),
        rays=False):
    top, bottom = MOODS[mood]
    out = [f'<defs><linearGradient id="sky-{uid}" x1="0" y1="0" x2="0" y2="1">'
           f'<stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient>'
           f'<linearGradient id="gnd-{uid}" x1="0" y1="0" x2="0" y2="1">'
           f'<stop offset="0" stop-color="#8ECB7E"/><stop offset="1" stop-color="#63AE5B"/>'
           f'</linearGradient></defs>',
           f'<rect width="500" height="360" fill="url(#sky-{uid})"/>']
    if sun:
        sx, sy = sun
        if rays:
            out.append(f'<g stroke="#FFD166" stroke-width="3" stroke-linecap="round" opacity=".55">' + "".join(
                f'<line x1="{sx+dx*34}" y1="{sy+dy*34}" x2="{sx+dx*46}" y2="{sy+dy*46}"/>'
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (.7, .7), (-.7, .7), (.7, -.7), (-.7, -.7))) + '</g>')
        out.append(f'<circle cx="{sx}" cy="{sy}" r="28" fill="#FFD166" opacity=".95"/>'
                   f'<circle cx="{sx}" cy="{sy}" r="20" fill="#FFE9A8"/>')
    out += [f'<ellipse cx="{c[0]}" cy="{c[1]}" rx="{c[2]}" ry="{c[3]}" fill="white" opacity=".88"/>' for c in clouds]
    return "".join(out)


def ground(uid, y=205, tufts=(40, 176, 300, 460), flowers=((55, 242), (350, 250), (206, 236))):
    out = [f'<path d="M0,{y+3} Q125,{y-11} 250,{y+1} T500,{y-1} L500,360 L0,360 Z" fill="url(#gnd-{uid})"/>',
           f'<path d="M0,{y+19} Q125,{y+7} 250,{y+19} T500,{y+17} L500,{y+43} L0,{y+43} Z" fill="#4A9B4A" opacity=".28"/>']
    if tufts:
        out.append('<g stroke="#4A9B4A" stroke-width="2" stroke-linecap="round" opacity=".5">' + "".join(
            f'<path d="M{x},{y+31} q3,-9 6,0"/>' for x in tufts) + '</g>')
    for i, (fx, fy) in enumerate(flowers or ()):
        c = FLOWERS[i % len(FLOWERS)]
        out.append(f'<circle cx="{fx}" cy="{fy}" r="3.4" fill="{c}"/><circle cx="{fx}" cy="{fy}" r="1.4" fill="#fff"/>')
    return "".join(out)


def bubble(lines, cx, cy, tail=None, color="#FF6B6B", size=13):
    """A speech bubble sized FROM its text rather than eyeballed against it.

    CLAUDE.md's rule - budget 8-9px of width per character at this size, plus ~28px
    of padding each side, and split rather than let a line run long - is arithmetic,
    so do the arithmetic. `tail` is the scene point the speaker is at; the tail is
    drawn towards it.
    """
    if isinstance(lines, str):
        lines = [lines]
    rx = max(52, max(len(t) for t in lines) * size * .34 + 28)
    ry = 20 + 9 * (len(lines) - 1)
    out = [f'<ellipse cx="{cx}" cy="{cy}" rx="{rx:.0f}" ry="{ry}" fill="white" '
           f'stroke="#D0C8B8" stroke-width="1.5" opacity=".96"/>']
    if tail:
        tx, ty = tail
        dx, dy = tx - cx, ty - cy
        L = (dx*dx + dy*dy) ** .5 or 1
        bx, by = cx + dx/L*rx*.62, cy + dy/L*ry*.9
        px, py = -dy/L*9, dx/L*9
        out.append(f'<path d="M{bx-px:.0f},{by-py:.0f} L{tx:.0f},{ty:.0f} L{bx+px:.0f},{by+py:.0f} Z" '
                   f'fill="white" stroke="#D0C8B8" stroke-width="1.5"/>')
    y0 = cy - (len(lines) - 1) * 9 + 4
    for i, t in enumerate(lines):
        out.append(f'<text x="{cx}" y="{y0 + i*18:.0f}" text-anchor="middle" font-size="{size}" '
                   f'fill="{color}" font-family="Nunito, sans-serif" font-weight="700">{t}</text>')
    return "".join(out)


def shadow(x, y, rx, op=.13):
    """Soft contact shadow so a character sits on the ground instead of floating."""
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx:.0f}" ry="{rx*.22:.0f}" fill="#4A6B3A" opacity="{op}"/>'


def page(uid, content, mood='morning', horizon=205, **kw):
    return (f'<svg viewBox="0 0 500 360" xmlns="http://www.w3.org/2000/svg">'
            f'{sky(uid, mood, **kw)}{ground(uid, horizon)}{content}</svg>')


def car(x, y, w=270, h=62, color="#FFD166", line="#E8B800", riders=""):
    """A car, which draws its own occupants.

    `riders` (characters in the `seated` pose) go in BEHIND the body, so the door
    crops them at the waist and they read as sitting in the car rather than on it.
    Getting that order wrong is the obvious mistake, so the car owns it: pass the
    riders in rather than drawing them beside the call, and anchor each rider at
    seat(y) so head and shoulders clear the door by the right amount.
    """
    return (riders
            + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{color}" stroke="{line}" stroke-width="2.5"/>'
            + "".join(f'<circle cx="{x+dx}" cy="{y+h+6}" r="22" fill="#2D3748" stroke="#1A1A1A" stroke-width="2"/>'
                      f'<circle cx="{x+dx}" cy="{y+h+6}" r="12" fill="#555"/>' for dx in (w*.26, w*.81)))


def seat(car_y):
    """The ground anchor for a rider of a car whose body starts at `car_y`."""
    return car_y + 40


def road(y=230):
    return (f'<rect x="0" y="{y}" width="500" height="{360-y}" fill="#B8B8B8"/>'
            + "".join(f'<rect x="{x}" y="{y+58}" width="30" height="10" rx="3" fill="#FFD166" opacity=".7"/>'
                      for x in (60, 200, 340)))


def bed(x, y, w=160, h=70, blanket=True):
    """A hospital bed with a pillow at its head end; a `lie` character sits on it."""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#B8E8F8" stroke="#4AA8C8" stroke-width="2"/>',
           f'<rect x="{x-10}" y="{y-30}" width="30" height="50" rx="6" fill="#E8C078" stroke="#C08840" stroke-width="2"/>']
    if blanket:
        out.append(f'<path d="M{x+5},{y+28} Q{x+w*.55},{y+10} {x+w-5},{y+28} '
                   f'L{x+w-5},{y+h-5} Q{x+w*.55},{y+h-18} {x+5},{y+h-5} Z" fill="#74C8E4" opacity=".6"/>')
    return "".join(out)


def indoors(uid, wall="#FFF3E4", floor="#EFE0C8", y=250):
    """A room, for the clinic interiors - same layering idea as the meadow."""
    return (f'<rect width="500" height="360" fill="{wall}"/>'
            f'<rect y="{y}" width="500" height="{360-y}" fill="{floor}"/>'
            f'<line x1="0" y1="{y}" x2="500" y2="{y}" stroke="#DCC9A8" stroke-width="2"/>')


def clip(uid, x, y, w, h, content):
    """Show `content` only inside a rectangle - a face at a window, passengers behind
    a windscreen. Without it a character placed at a window is just pasted over the
    wall, which is exactly how it looked before this existed."""
    return (f'<defs><clipPath id="clip-{uid}"><rect x="{x:.0f}" y="{y:.0f}" '
            f'width="{w:.0f}" height="{h:.0f}" rx="4"/></clipPath></defs>'
            f'<g clip-path="url(#clip-{uid})">{content}</g>')


def ambulance(uid, x, y, w=250, h=70, riders=""):
    """A white van with a light bar and a cross. Riders show THROUGH the window -
    they are clipped to it, so they read as inside the van, not stuck on its side."""
    wx, wy, ww, wh = x + w*.08, y + 9, w*.52, h*.55
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#FFFFFF" stroke="#C8C8C8" stroke-width="2"/>'
            f'<rect x="{wx:.0f}" y="{wy:.0f}" width="{ww:.0f}" height="{wh:.0f}" rx="5" fill="#CFEAF6"/>'
            + clip(uid, wx, wy, ww, wh, riders)
            + f'<rect x="{wx:.0f}" y="{wy:.0f}" width="{ww:.0f}" height="{wh:.0f}" rx="5" fill="none" stroke="#8FBCD0" stroke-width="1.5"/>'
            f'<rect x="{x+w*.74:.0f}" y="{y+h*.22:.0f}" width="9" height="30" rx="2" fill="#E4453F"/>'
            f'<rect x="{x+w*.74-7:.0f}" y="{y+h*.38:.0f}" width="23" height="9" rx="2" fill="#E4453F"/>'
            f'<rect x="{x+w*.32:.0f}" y="{y-13}" width="34" height="13" rx="4" fill="#E4453F" opacity=".9"/>'
            f'<rect x="{x+w*.32+17:.0f}" y="{y-13}" width="17" height="13" rx="4" fill="#74C8E4" opacity=".9"/>'
            + "".join(f'<circle cx="{x+dx:.0f}" cy="{y+h+6}" r="20" fill="#2D3748" stroke="#1A1A1A" stroke-width="2"/>'
                      f'<circle cx="{x+dx:.0f}" cy="{y+h+6}" r="11" fill="#555"/>' for dx in (w*.24, w*.79)))


def traffic_light(x, y, on='red'):
    lit = {'red': 0, 'amber': 1, 'green': 2}[on]
    cols = ("#E4453F", "#FFD166", "#4CC38A")
    return (f'<rect x="{x-3}" y="{y}" width="6" height="{92}" fill="#5A646C"/>'
            f'<rect x="{x-15}" y="{y-64}" width="30" height="66" rx="7" fill="#3A424A"/>'
            + "".join(f'<circle cx="{x}" cy="{y-52+i*20}" r="7" fill="{cols[i]}" '
                      f'opacity="{1 if i == lit else .22}"/>' for i in range(3)))


def tray(x, y, w=64, full=True):
    """A meal tray. `full` is the difference between Elephant's snack and Rabbit's."""
    items = (f'<circle cx="{x-w*.28:.0f}" cy="{y-9}" r="7" fill="#FFD166"/>'
             f'<path d="M{x-w*.34:.0f},{y-14} q10,-11 20,-2" stroke="#E8B800" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
             f'<rect x="{x-4:.0f}" y="{y-16}" width="16" height="11" rx="2" fill="#E8C078" stroke="#C08840" stroke-width="1.2"/>') if full else ''
    return (f'<rect x="{x-w/2:.0f}" y="{y-6}" width="{w}" height="9" rx="3" fill="#DCD2C0" stroke="#B9AE98" stroke-width="1.2"/>'
            + items + glass(x + w*.32, y - 8, full=full))


def glass(x, y, full=True):
    h, fill = (20, 15) if full else (20, 7)
    return (f'<rect x="{x-6:.0f}" y="{y-h:.0f}" width="12" height="{h}" rx="2" fill="#EAF6FB" stroke="#8FBCD0" stroke-width="1.2"/>'
            f'<rect x="{x-5:.0f}" y="{y-fill:.0f}" width="10" height="{fill-1}" rx="1.5" fill="#FFB347" opacity=".85"/>')


def window(x, y, w=26, h=26, dim=False):
    return f'<rect x="{x-w/2:.0f}" y="{y-h/2:.0f}" width="{w}" height="{h}" rx="3" fill="#74C8E4" opacity="{.5 if dim else .8}"/>'


def hospital(x=280, y=70, w=200, h=140):
    """The clinic exterior - it recurs across stories 02, 03 and 06."""
    # everything is placed as a fraction of w: at a fixed offset the windows and door
    # fall outside the wall as soon as the building is drawn narrower
    cx, dw = x + w*.5, min(60, w*.30)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="white" stroke="#D0D0D0" stroke-width="2"/>'
            f'<rect x="{x-6}" y="{y-6}" width="{w+12}" height="16" rx="4" fill="#E0E0E0" stroke="#C8C8C8" stroke-width="1.5"/>'
            f'<rect x="{cx-20:.0f}" y="{y-36}" width="40" height="40" rx="6" fill="white" stroke="#FF6B6B" stroke-width="2"/>'
            f'<rect x="{cx-4:.0f}" y="{y-32}" width="8" height="32" rx="2" fill="#FF6B6B"/>'
            f'<rect x="{cx-18:.0f}" y="{y-20}" width="36" height="8" rx="2" fill="#FF6B6B"/>'
            + "".join(f'<rect x="{x+w*fx:.0f}" y="{y+h*.19:.0f}" width="26" height="26" rx="3" '
                      f'fill="#74C8E4" opacity=".8"/>' for fx in (.08, .26, .80))
            + f'<rect x="{cx-dw/2:.0f}" y="{y+h-dw:.0f}" width="{dw:.0f}" height="{dw:.0f}" rx="4" '
              f'fill="#B8E8F8" stroke="#4AA8C8" stroke-width="2"/>')


# ---------------------------------------------------------------- story props
FRUIT = ("#FF6B6B", "#FFD166", "#C77DFF", "#4CC38A", "#FF9BAE")


def tree(x, y, s=1.0):
    """The shady tree the friends keep ending up under."""
    return (f'<rect x="{x-7*s:.0f}" y="{y-56*s:.0f}" width="{14*s:.0f}" height="{56*s:.0f}" '
            f'rx="3" fill="#A87A52"/>'
            + "".join(f'<circle cx="{x+dx*s:.0f}" cy="{y-(70+dy)*s:.0f}" r="{r*s:.0f}" fill="{c}"/>'
                      for dx, dy, r, c in ((-24, 0, 30, "#6BAF5E"), (22, 4, 28, "#6BAF5E"),
                                           (-2, 22, 34, "#8ECB7E"))))


def tap(x, y, running=False):
    """The old field tap. `running` adds the water they wash their hands under."""
    out = [f'<rect x="{x-4}" y="{y-56}" width="8" height="56" rx="2" fill="#9AA6AE"/>',
           f'<path d="M{x-4},{y-52} L{x+22},{y-52} L{x+22},{y-40}" stroke="#9AA6AE" '
           f'stroke-width="8" fill="none" stroke-linecap="round"/>',
           f'<circle cx="{x}" cy="{y-58}" r="7" fill="#7E8A92"/>',
           f'<ellipse cx="{x+14}" cy="{y+2}" rx="26" ry="8" fill="#C8BCA4"/>']
    if running:
        out.append(f'<path d="M{x+22},{y-38} q3,12 -1,24 q-3,10 1,14" stroke="#8FD6F0" '
                   f'stroke-width="5" fill="none" stroke-linecap="round" opacity=".85"/>')
        out += [f'<circle cx="{x+14+dx}" cy="{y-2+dy}" r="2.4" fill="#8FD6F0" opacity=".7"/>'
                for dx, dy in ((-9, -4), (10, -6), (2, -9))]
    return "".join(out)


def bowl(x, y, kind='fruit', s=1.0):
    """A takeaway bowl. `kind` is fruit | halwa | pancakes | empty."""
    w, h = 30*s, 15*s
    out = [f'<path d="M{x-w:.0f},{y-h:.0f} q{w:.0f},{h*1.9:.0f} {w*2:.0f},0 Z" '
           f'fill="#FFFFFF" stroke="#C8BCA4" stroke-width="1.5"/>']
    if kind == 'fruit':
        out += [f'<circle cx="{x+dx*s:.0f}" cy="{y-(h+2)+dy*s:.0f}" r="{4.4*s:.1f}" fill="{c}"/>'
                for (dx, dy), c in zip(((-16, 1), (-6, -3), (4, 0), (14, -2), (-1, 4)), FRUIT)]
    elif kind == 'halwa':
        out.append(f'<path d="M{x-18*s:.0f},{y-h:.0f} q{18*s:.0f},{-15*s:.0f} {36*s:.0f},0 Z" fill="#E8892E"/>')
        out += [f'<circle cx="{x+dx*s:.0f}" cy="{y-(h+5)+dy*s:.0f}" r="{1.8*s:.1f}" fill="#FFD9A8"/>'
                for dx, dy in ((-8, 2), (3, -1), (10, 3))]
    elif kind in ('soup', 'chilli'):      # warm soup; chilli is redder and has a chilli in it
        c = "#F2B24A" if kind == 'soup' else "#E4453F"
        out.append(f'<ellipse cx="{x:.0f}" cy="{y-h:.0f}" rx="{w-3:.0f}" ry="{5*s:.0f}" fill="{c}"/>')
        if kind == 'chilli':
            out.append(f'<path d="M{x-4*s:.0f},{y-h-2*s:.0f} q{10*s:.0f},{-2*s:.0f} {14*s:.0f},{-10*s:.0f}" '
                       f'stroke="#C0201A" stroke-width="{4*s:.1f}" fill="none" stroke-linecap="round"/>'
                       f'<path d="M{x+10*s:.0f},{y-h-12*s:.0f} l{3*s:.0f},{-4*s:.0f}" stroke="#4A9B4A" '
                       f'stroke-width="{2.4*s:.1f}" stroke-linecap="round"/>')
        out.append(steam(x, y - h - 8*s, s))
    elif kind == 'pancakes':
        out += [f'<ellipse cx="{x:.0f}" cy="{y-h-i*6*s:.0f}" rx="{19*s:.0f}" ry="{5*s:.0f}" '
                f'fill="#E8C078" stroke="#C08840" stroke-width="1.2"/>' for i in range(3)]
        out.append(f'<path d="M{x-11*s:.0f},{y-h-13*s:.0f} q{11*s:.0f},{6*s:.0f} {22*s:.0f},0" '
                   f'stroke="#C9781E" stroke-width="{3*s:.1f}" fill="none" stroke-linecap="round"/>')
    return "".join(out)


def parcel(x, y, s=1.0, open_lid=False):
    """A delivery box, shut or torn open."""
    out = [f'<rect x="{x-24*s:.0f}" y="{y-26*s:.0f}" width="{48*s:.0f}" height="{26*s:.0f}" '
           f'rx="3" fill="#E8C078" stroke="#C08840" stroke-width="1.5"/>']
    if open_lid:
        out.append(f'<path d="M{x-24*s:.0f},{y-26*s:.0f} l{-10*s:.0f},{-14*s:.0f} '
                   f'l{48*s:.0f},0 l{10*s:.0f},{14*s:.0f} Z" fill="#F0D9A8" '
                   f'stroke="#C08840" stroke-width="1.5"/>')
    else:
        out.append(f'<rect x="{x-26*s:.0f}" y="{y-31*s:.0f}" width="{52*s:.0f}" height="{8*s:.0f}" '
                   f'rx="2" fill="#F0D9A8" stroke="#C08840" stroke-width="1.5"/>')
    return "".join(out)


def phone(x, y, s=1.0, tilt=-12):
    return (f'<g transform="rotate({tilt} {x} {y})">'
            f'<rect x="{x-9*s:.0f}" y="{y-15*s:.0f}" width="{18*s:.0f}" height="{30*s:.0f}" '
            f'rx="3" fill="#3A424A"/>'
            f'<rect x="{x-7*s:.0f}" y="{y-13*s:.0f}" width="{14*s:.0f}" height="{24*s:.0f}" '
            f'rx="2" fill="#8FD6F0"/></g>')


def seedlings(y=300, xs=(70, 130, 190, 250, 310), sprouted=False):
    """Dug holes with seeds, or the little shoots that come later."""
    out = []
    for x in xs:
        if sprouted:
            out.append(f'<path d="M{x},{y} q0,-12 0,-14 M{x},{y-8} q-7,-5 -9,-1 M{x},{y-11} q7,-5 9,-1" '
                       f'stroke="#4A9B4A" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
        else:
            out.append(f'<ellipse cx="{x}" cy="{y}" rx="9" ry="4" fill="#8A6A44" opacity=".55"/>'
                       f'<circle cx="{x}" cy="{y-1}" r="2.4" fill="#6B4A24"/>')
    return "".join(out)


def zzz(x, y, color="#8FA8C0"):
    return "".join(f'<text x="{x+i*13}" y="{y-i*15}" font-size="{13+i*5}" fill="{color}" '
                   f'font-family="Fredoka One, sans-serif" opacity=".75">z</text>' for i in range(3))


def thought(lines, cx, cy, tail_to, size=12, picture=None, rx=None, ry=None):
    """A thought bubble: same sizing rule as bubble(), but a trail of dots.

    `picture` puts a drawing in the bubble instead of words (pass lines=[] and size
    the bubble with rx/ry) - Rabbit picturing Elephant in his hospital bed."""
    if isinstance(lines, str):
        lines = [lines]
    rx = rx or max(46, max(len(t) for t in lines) * size * .34 + 24)
    ry = ry or 18 + 9 * (len(lines) - 1)
    tx, ty = tail_to
    dx, dy = tx - cx, ty - cy
    L = (dx*dx + dy*dy) ** .5 or 1
    dots = "".join(f'<circle cx="{cx+dx*t:.0f}" cy="{cy+dy*t:.0f}" r="{3+ (1-t)*3:.1f}" '
                   f'fill="white" stroke="#D0C8B8" stroke-width="1.2"/>'
                   for t in (.62, .80, .94))
    txt = "".join(f'<text x="{cx}" y="{cy-(len(lines)-1)*9+4+i*18:.0f}" text-anchor="middle" '
                  f'font-size="{size}" fill="#6B5B47" font-family="Nunito, sans-serif" '
                  f'font-weight="700">{t}</text>' for i, t in enumerate(lines))
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx:.0f}" ry="{ry}" fill="white" '
            f'stroke="#D0C8B8" stroke-width="1.5" opacity=".96"/>{dots}{txt}{picture or ""}')


# ---------------------------------------------------------------- water & play
def waterline(pool_y):
    """The ground anchor for a character standing in a pool centred on `pool_y`."""
    return pool_y + 30


def pool(uid, x, y, rx=120, ry=44, swimmers="", rim="#4AA8C8"):
    """A pool that draws its own swimmers.

    Like car(), the container owns its occupants, because the ordering is the whole
    trick: the swimmers go in over the water and then the NEAR half of the surface is
    drawn back over them, so they sit in the pool rather than on top of it. Anchor
    each swimmer at waterline(y).
    """
    return (f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{rim}"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="{rx-6}" ry="{ry-6}" fill="#9BDCF0"/>'
            + swimmers
            + f'<path d="M{x-rx+6},{y} a{rx-6},{ry-6} 0 0 0 {2*(rx-6)},0 Z" fill="#9BDCF0" opacity=".82"/>'
            + f'<path d="M{x-rx+6},{y} a{rx-6},{ry-6} 0 0 0 {2*(rx-6)},0 Z" fill="none" '
              f'stroke="#7EC8E3" stroke-width="2"/>'
            + "".join(f'<path d="M{x+dx},{y+dy} q7,-4 14,0" stroke="#EAF8FF" stroke-width="2.2" '
                      f'fill="none" stroke-linecap="round" opacity=".8"/>'
                      for dx, dy in ((-rx*.5, ry*.42), (rx*.24, ry*.55), (-rx*.1, ry*.28))))


def splash(x, y, s=1.0, big=True):
    """The wave a jumping elephant makes. `big` is the SPLOOSH; small is a paddle."""
    n = 9 if big else 5
    import math as _m
    drops = "".join(
        f'<ellipse cx="{x + _m.cos(a)*46*s:.0f}" cy="{y - abs(_m.sin(a))*44*s:.0f}" '
        f'rx="{(6 if big else 4)*s:.1f}" ry="{(9 if big else 6)*s:.1f}" fill="#CFEEFA" '
        f'transform="rotate({_m.degrees(a)-90:.0f} {x + _m.cos(a)*46*s:.0f} {y - abs(_m.sin(a))*44*s:.0f})"/>'
        for a in [_m.pi*i/(n-1) for i in range(n)])
    arc = (f'<path d="M{x-58*s:.0f},{y} q{29*s:.0f},{-50*s:.0f} {58*s:.0f},0" stroke="#CFEEFA" '
           f'stroke-width="{7*s:.1f}" fill="none" stroke-linecap="round" opacity=".9"/>') if big else ''
    return arc + drops


def sign(x, y, lines, w=None, color="#4AA8C8"):
    """The resort's noticeboard on two posts."""
    w = w or max(120, max(len(t) for t in lines) * 8 + 24)
    h = 26 + 20 * (len(lines) - 1)
    out = [f'<rect x="{x-8}" y="{y}" width="7" height="46" fill="#A87A52"/>',
           f'<rect x="{x+1}" y="{y}" width="7" height="46" fill="#A87A52"/>',
           f'<rect x="{x-w/2:.0f}" y="{y-h-8}" width="{w}" height="{h+10}" rx="5" fill="#FFFDF6" '
           f'stroke="{color}" stroke-width="2.5"/>']
    y0 = y - h + 4
    for i, t in enumerate(lines):
        out.append(f'<text x="{x}" y="{y0 + i*19:.0f}" text-anchor="middle" font-size="13" '
                   f'fill="{color}" font-family="Fredoka One, sans-serif">{t}</text>')
    return "".join(out)


def bus(x, y, w=180, h=64, riders=""):
    return (riders
            + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#FFD166" '
              f'stroke="#E8B800" stroke-width="2.5"/>'
            + "".join(f'<rect x="{x+w*fx:.0f}" y="{y+9}" width="30" height="24" rx="4" '
                      f'fill="#CFEAF6" stroke="#8FBCD0" stroke-width="1.4"/>' for fx in (.08, .34, .60))
            + "".join(f'<circle cx="{x+dx:.0f}" cy="{y+h+5}" r="18" fill="#2D3748"/>'
                      f'<circle cx="{x+dx:.0f}" cy="{y+h+5}" r="9" fill="#555"/>' for dx in (w*.22, w*.80)))


def ball(x, y, kind='beach', r=14):
    if kind == 'basket':
        return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#E8892E" stroke="#B4661C" stroke-width="1.6"/>'
                f'<path d="M{x-r},{y} h{2*r} M{x},{y-r} v{2*r}" stroke="#B4661C" stroke-width="1.4"/>')
    if kind == 'tennis':
        return (f'<circle cx="{x}" cy="{y}" r="{r*.6:.0f}" fill="#D8E84A" stroke="#A8B82A" stroke-width="1.4"/>'
                f'<path d="M{x-r*.6:.0f},{y} q{r*.6:.0f},{-r*.5:.0f} {r*1.2:.0f},0" stroke="#fff" '
                f'stroke-width="1.4" fill="none"/>')
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFDF6" stroke="#D0C8B8" stroke-width="1.4"/>'
            + "".join(f'<path d="M{x},{y-r} a{r},{r} 0 0 1 {dx},{r*1.7:.0f} Z" fill="{c}" opacity=".85"/>'
                      for dx, c in ((-r*.9, "#FF6B6B"), (r*.9, "#74C8E4"))))


def table(x, y, w=200, top="#DCD2C0"):
    return (f'<rect x="{x-w/2:.0f}" y="{y}" width="{w}" height="12" rx="4" fill="{top}" '
            f'stroke="#B9AE98" stroke-width="1.5"/>'
            f'<rect x="{x-w/2+16:.0f}" y="{y+12}" width="10" height="52" fill="#C8BCA4"/>'
            f'<rect x="{x+w/2-26:.0f}" y="{y+12}" width="10" height="52" fill="#C8BCA4"/>')


def spin(deg, x, y, content):
    """Rotate a placed character - a rabbit launched out of the pool, say."""
    return f'<g transform="rotate({deg} {x} {y})">{content}</g>'


# ---------------------------------------------------------------- story 02 props
def thorn(x, y, s=1.0, rot=0):
    """The great big thorn. Dark and spiky so it reads instantly at page size."""
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<path d="M{x},{y-26*s:.0f} L{x+7*s:.0f},{y+8*s:.0f} L{x},{y+14*s:.0f} '
            f'L{x-7*s:.0f},{y+8*s:.0f} Z" fill="#5C3A21" stroke="#3A2412" stroke-width="1.4"/>'
            f'<path d="M{x-2*s:.0f},{y-18*s:.0f} L{x+2*s:.0f},{y+4*s:.0f}" stroke="#8A6A44" '
            f'stroke-width="{2*s:.1f}" opacity=".7"/></g>')


def truck(uid, x, y, w=300, cargo_riders="", cab_riders="", color="#74C8E4", line="#3C90AE"):
    """Their big truck: a cab just big enough for Rabbit, and an enormous cargo bay.

    The cargo bay is open-topped, so its riders go in behind the front wall and show
    from the chest up; the cab's rider is clipped into the windscreen. Both are the
    container's job, as with car() and pool().
    """
    cw, bw = w*.40, w*.58
    bx, cx = x, x + w*.60
    bh, ch = 54, 64
    return (cargo_riders
            + f'<rect x="{bx}" y="{y-bh}" width="{bw:.0f}" height="{bh}" rx="6" fill="{color}" '
              f'stroke="{line}" stroke-width="2.5"/>'
            + f'<rect x="{bx+8:.0f}" y="{y-bh+9}" width="{bw-16:.0f}" height="{bh-20}" rx="4" '
              f'fill="none" stroke="{line}" stroke-width="1.4" opacity=".5"/>'
            + f'<rect x="{cx:.0f}" y="{y-ch-22}" width="{cw:.0f}" height="{ch+22}" rx="7" '
              f'fill="{color}" stroke="{line}" stroke-width="2.5"/>'
            + f'<rect x="{cx+9:.0f}" y="{y-ch-13}" width="{cw-20:.0f}" height="{44}" rx="4" fill="#CFEAF6"/>'
            + clip(uid, cx+9, y-ch-13, cw-20, 44, cab_riders)
            + f'<rect x="{cx+9:.0f}" y="{y-ch-13}" width="{cw-20:.0f}" height="{44}" rx="4" '
              f'fill="none" stroke="#8FBCD0" stroke-width="1.5"/>'
            + "".join(f'<circle cx="{x+dx:.0f}" cy="{y+8}" r="21" fill="#2D3748"/>'
                      f'<circle cx="{x+dx:.0f}" cy="{y+8}" r="11" fill="#555"/>'
                      for dx in (w*.16, w*.44, w*.82)))


def cab_seat(truck_y, s=0.86):
    """Ground anchor for the driver, so their head lands IN the windscreen.

    A `seated` character's head sits 86*s above its anchor, and the windscreen centre
    is 50 above the wheels - so the anchor has to go BELOW the wheel line. Get this
    wrong and the driver is clipped away entirely and the cab looks empty, which is
    exactly what happened the first time.
    """
    return truck_y - 55 + 86*s


def cargo_seat(truck_y, s=1.0):
    """Ground anchor for a passenger in the open cargo bay, chest above the wall."""
    return truck_y - 54 + 34*s


def garden_window(x, y, w=96, h=76):
    """A ward window with something green to look at."""
    return (f'<rect x="{x-w/2:.0f}" y="{y-h/2:.0f}" width="{w}" height="{h}" rx="5" fill="#CFEAF6" '
            f'stroke="#B9AE98" stroke-width="3"/>'
            f'<path d="M{x-w/2+3:.0f},{y+h/2-22:.0f} q{w*.25:.0f},-12 {w*.5:.0f},0 '
            f'q{w*.25:.0f},12 {w*.5-6:.0f},0 L{x+w/2-3:.0f},{y+h/2-3:.0f} '
            f'L{x-w/2+3:.0f},{y+h/2-3:.0f} Z" fill="#8ECB7E"/>'
            f'<circle cx="{x-w*.22:.0f}" cy="{y-h*.12:.0f}" r="13" fill="#6BAF5E"/>'
            f'<rect x="{x-w*.24:.0f}" y="{y-h*.12:.0f}" width="4" height="16" fill="#A87A52"/>'
            f'<path d="M{x},{y-h/2+3:.0f} v{h-6:.0f} M{x-w/2+3:.0f},{y} h{w-6:.0f}" '
            f'stroke="#B9AE98" stroke-width="2.5"/>')


def clipboard(x, y, s=1.0, tilt=-8):
    return (f'<g transform="rotate({tilt} {x} {y})">'
            f'<rect x="{x-15*s:.0f}" y="{y-20*s:.0f}" width="{30*s:.0f}" height="{40*s:.0f}" '
            f'rx="3" fill="#E8C078" stroke="#C08840" stroke-width="1.5"/>'
            f'<rect x="{x-11*s:.0f}" y="{y-15*s:.0f}" width="{22*s:.0f}" height="{30*s:.0f}" '
            f'rx="2" fill="#FFFDF6"/>'
            f'<rect x="{x-6*s:.0f}" y="{y-24*s:.0f}" width="{12*s:.0f}" height="{7*s:.0f}" '
            f'rx="2" fill="#9AA6AE"/>'
            + "".join(f'<path d="M{x-7*s:.0f},{y+(-8+i*7)*s:.0f} h{14*s:.0f}" stroke="#C8BCA4" '
                      f'stroke-width="{1.6*s:.1f}"/>' for i in range(4)) + '</g>')


def tweezers(x, y, s=1.0, rot=-30, holding=None):
    """Dr. Squirrel's special long tweezers, optionally gripping something."""
    out = (f'<g transform="rotate({rot} {x} {y})">'
           f'<path d="M{x-3*s:.0f},{y-24*s:.0f} L{x-1*s:.0f},{y+18*s:.0f}" stroke="#9AA6AE" '
           f'stroke-width="{3.4*s:.1f}" stroke-linecap="round"/>'
           f'<path d="M{x+3*s:.0f},{y-24*s:.0f} L{x+1*s:.0f},{y+18*s:.0f}" stroke="#9AA6AE" '
           f'stroke-width="{3.4*s:.1f}" stroke-linecap="round"/>'
           f'<circle cx="{x}" cy="{y-26*s:.0f}" r="{4*s:.1f}" fill="#7E8A92"/></g>')
    return out + (holding or '')


def books(x, y, n=3):
    cols = ("#FF6B6B", "#74C8E4", "#C77DFF", "#4CC38A")
    return "".join(f'<rect x="{x-18}" y="{y-(i+1)*9}" width="36" height="8" rx="2" '
                   f'fill="{cols[i % len(cols)]}" stroke="#00000022" stroke-width="1"/>'
                   for i in range(n))


def speedlines(x, y, n=4, length=34, back=True):
    """Motion streaks behind a character who is running flat out."""
    d = -1 if back else 1
    return "".join(f'<path d="M{x + d*length:.0f},{y-14+i*10} h{-d*length:.0f}" stroke="#B9C8D0" '
                   f'stroke-width="3" stroke-linecap="round" opacity="{.55 - i*.08:.2f}"/>'
                   for i in range(n))


# ---------------------------------------------------------------- story 04 props
def dirt(x, y, rx=46, ry=11):
    """A dug-over patch of field."""
    return (f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#8A6A44" opacity=".55"/>'
            f'<ellipse cx="{x-rx*.3:.0f}" cy="{y-ry*.2:.0f}" rx="{rx*.4:.0f}" ry="{ry*.4:.0f}" fill="#A8845A" opacity=".45"/>')


def roots(x, y, depth=60, cut=False):
    """A cutaway of the ground under a thorn, showing how far down its roots go.

    `cut` snips them partway down - the moment the digger gets through."""
    w = depth * .9
    out = [f'<path d="M{x-w:.0f},{y} Q{x},{y-10} {x+w:.0f},{y} Q{x+w*.8:.0f},{y+depth*.9:.0f} {x},{y+depth:.0f} '
           f'Q{x-w*.8:.0f},{y+depth*.9:.0f} {x-w:.0f},{y} Z" fill="#8A6A44"/>']
    strands = ((0, 1, 0), (-.45, .8, -.3), (.4, .85, .35), (-.2, .55, -.6), (.25, .5, .6))
    d = []
    for i, (ex, ey, bend) in enumerate(strands):
        tx, ty = x + ex*w, y + ey*depth
        if cut and i < 3:            # the long ones end in a clean snip
            tx, ty = x + ex*w*.45, y + ey*depth*.45
        d.append(f'M{x},{y} Q{x + bend*w*.5:.0f},{y + (ty-y)*.5:.0f} {tx:.0f},{ty:.0f}')
    out.append(f'<path d="{" ".join(d)}" stroke="#4A2E16" stroke-width="3" fill="none" stroke-linecap="round"/>')
    if cut:
        out += [f'<path d="M{x + ex*w*.45 - 5:.0f},{y + ey*depth*.45 + 7:.0f} l10,-4" stroke="#FFD166" '
                f'stroke-width="3" stroke-linecap="round"/>' for ex, ey, _ in strands[:3]]
    return "".join(out)


def fence(x0, x1, y, h=46):
    """A wooden field fence: posts every ~52 units and two rails."""
    n = max(1, round((x1 - x0) / 52))
    posts = [x0 + (x1 - x0) * i / n for i in range(n + 1)]
    return (f'<g fill="#C9A06A" stroke="#A07A48" stroke-width="1.5">'
            + "".join(f'<rect x="{px-4:.0f}" y="{y-h}" width="8" height="{h}" rx="2"/>' for px in posts)
            + f'<rect x="{x0-4}" y="{y-h+8}" width="{x1-x0+8}" height="6" rx="2"/>'
              f'<rect x="{x0-4}" y="{y-h+26}" width="{x1-x0+8}" height="6" rx="2"/></g>')


def crank_phone(x, y, receiver=None):
    """The old telephone on its post by the fence: a wooden box with two bells, a
    crank on the side, and a receiver on a cord. `receiver` is where the receiver is
    now - in someone's paw at their ear - or None for hanging on its hook."""
    top = y - 150
    rx, ry = receiver or (x - 26, top + 34)
    return (f'<rect x="{x-5}" y="{top+40}" width="10" height="{y-top-40}" rx="2" fill="#A07A48"/>'
            f'<rect x="{x-22}" y="{top}" width="44" height="58" rx="5" fill="#C08840" stroke="#8A5A26" stroke-width="2"/>'
            f'<circle cx="{x-9}" cy="{top+13}" r="7" fill="#E8C078" stroke="#8A5A26" stroke-width="1.5"/>'
            f'<circle cx="{x+9}" cy="{top+13}" r="7" fill="#E8C078" stroke="#8A5A26" stroke-width="1.5"/>'
            f'<circle cx="{x}" cy="{top+36}" r="6" fill="#2D3748"/>'
            f'<path d="M{x+22},{top+34} h9 v14" stroke="#5C3A21" stroke-width="3.2" fill="none" stroke-linecap="round"/>'
            f'<circle cx="{x+31}" cy="{top+50}" r="3.5" fill="#FF6B6B"/>'
            f'<path d="M{x-22},{top+44} Q{(x-22+rx)/2:.0f},{max(top+80, ry+30):.0f} {rx:.0f},{ry+8:.0f}" '
            f'stroke="#2D3748" stroke-width="1.6" fill="none"/>'
            f'<rect x="{rx-4:.0f}" y="{ry-14:.0f}" width="8" height="28" rx="4" fill="#2D3748"/>')


def birds(pts, color="#5A6B7A"):
    """Little flapping v's - startled birds leaving a tree."""
    return (f'<path d="' + " ".join(f'M{x-8},{y-3} q4,-5 8,1 q4,-6 8,-1' for x, y in pts)
            + f'" stroke="{color}" stroke-width="2" fill="none" stroke-linecap="round"/>')


def digger(uid, x, y, w=200, bucket=None, bw=120, bucket_riders="", cab_riders="",
           color="#FFD166", line="#D9A21F"):
    """The JCB: a yellow body on two big wheels, a cab, and an arm out the front.

    `y` is the ground under the wheels. `bucket` is where the bucket's bottom-centre
    is - down in the dirt to dig, up at chest height to carry. Like truck() and car(),
    it draws its own passengers: `bucket_riders` go in BEHIND the bucket's front wall,
    so they read as sitting in it; `cab_riders` are clipped into the cab window.
    """
    bx, by = bucket or (x + w + 70, y - 8)
    cx, cw, ch = x + 12, w * .44, 72
    body_top = y - 92
    # the arm: shoulder on the body, up to an elbow, down to the bucket
    sx, sy = x + w - 16, body_top + 16
    ex, ey = (sx + bx) / 2 + 10, min(sy, by) - 62
    arm = f'M{sx:.0f},{sy:.0f} L{ex:.0f},{ey:.0f} L{bx - bw*.1:.0f},{by - 46:.0f}'
    bh = 50
    lip = (f'M{bx-bw/2:.0f},{by-bh} L{bx-bw/2+10:.0f},{by} L{bx+bw/2-6:.0f},{by} '
           f'L{bx+bw/2+8:.0f},{by-bh-6} Z')
    return (f'<path d="{arm}" stroke="{line}" stroke-width="22" fill="none" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<path d="{arm}" stroke="{color}" stroke-width="17" fill="none" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<circle cx="{ex:.0f}" cy="{ey:.0f}" r="5" fill="#5E6870"/>'
            + bucket_riders
            + f'<path d="{lip}" fill="#6E7880" stroke="#4A525A" stroke-width="2.5" stroke-linejoin="round"/>'
            + "".join(f'<path d="M{bx-bw/2+18+i*(bw-30)/4:.0f},{by} l5,8 l5,-8" fill="#4A525A"/>' for i in range(5))
            + f'<rect x="{cx:.0f}" y="{body_top-ch+8}" width="{cw:.0f}" height="{ch}" rx="8" fill="{color}" stroke="{line}" stroke-width="2.5"/>'
            + f'<rect x="{cx+9:.0f}" y="{body_top-ch+17}" width="{cw-18:.0f}" height="46" rx="5" fill="#CFEAF6"/>'
            + clip(uid, cx+9, body_top-ch+17, cw-18, 46, cab_riders)
            + f'<rect x="{cx+9:.0f}" y="{body_top-ch+17}" width="{cw-18:.0f}" height="46" rx="5" fill="none" stroke="#8FBCD0" stroke-width="1.5"/>'
            + f'<rect x="{x}" y="{body_top}" width="{w}" height="54" rx="10" fill="{color}" stroke="{line}" stroke-width="2.5"/>'
            + f'<rect x="{x+w*.52:.0f}" y="{body_top-14}" width="10" height="16" rx="2" fill="#5E6870"/>'
            + f'<rect x="{x+12}" y="{body_top+22}" width="{w-24}" height="6" rx="3" fill="{line}" opacity=".5"/>'
            + "".join(f'<circle cx="{x+dx:.0f}" cy="{y-r}" r="{r}" fill="#2D3748" stroke="#1A1A1A" stroke-width="2"/>'
                      f'<circle cx="{x+dx:.0f}" cy="{y-r}" r="{r*.45:.0f}" fill="#8A949C"/>'
                      for dx, r in ((w*.24, 34), (w*.8, 26))))


def digger_cab(y, s=.7, head=76):
    """Ground anchor for a `seated` driver so their head lands in the digger's cab.
    `head` is the character's seated head height (sheep 76, rabbit 86, elephant 84):
    the window's centre is 124 above the wheels, and the face wants to sit just under it."""
    return y - 118 + head*s


# ---------------------------------------------------------------- story 03 props
def steam(x, y, s=1.0, color="#C8BCA4"):
    """Three wavy wisps rising off something hot."""
    return (f'<path d="' + " ".join(f'M{x+dx*s:.0f},{y:.0f} q{-5*s:.0f},{-7*s:.0f} 0,{-14*s:.0f} '
                                    f'q{5*s:.0f},{-7*s:.0f} 0,{-14*s:.0f}' for dx in (-10, 0, 10))
            + f'" stroke="{color}" stroke-width="{2*s:.1f}" fill="none" stroke-linecap="round" opacity=".75"/>')


def snow_sky(uid, mood='snow', clouds=((90, 48, 40, 16), (116, 40, 24, 14), (400, 60, 36, 15))):
    """A soft winter sky: cool and pale, never grey. `mood` may also be any sky() mood
    - snow still falls through a golden evening at the end of story 03."""
    top, bottom = ("#CFE3F2", "#F2F8FC") if mood == 'snow' else MOODS[mood]
    return (f'<defs><linearGradient id="sky-{uid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient>'
            f'<linearGradient id="snow-{uid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#E2EDF5"/></linearGradient></defs>'
            f'<rect width="500" height="360" fill="url(#sky-{uid})"/>'
            + "".join(f'<ellipse cx="{c[0]}" cy="{c[1]}" rx="{c[2]}" ry="{c[3]}" fill="white" opacity=".85"/>'
                      for c in clouds))


def snow_ground(uid, y=205):
    """The meadow recipe, in snow: a wavy white top, a second bluish band for depth,
    and little drift bumps instead of grass tufts."""
    return (f'<path d="M0,{y+3} Q125,{y-11} 250,{y+1} T500,{y-1} L500,360 L0,360 Z" fill="url(#snow-{uid})"/>'
            f'<path d="M0,{y+19} Q125,{y+7} 250,{y+19} T500,{y+17} L500,{y+43} L0,{y+43} Z" fill="#B8D0E0" opacity=".3"/>'
            f'<g stroke="#C8DCE8" stroke-width="2" fill="none" stroke-linecap="round">'
            + "".join(f'<path d="M{x},{y+34} q8,-6 16,0"/>' for x in (40, 176, 300, 452)) + '</g>')


def flakes(n=26, seed=3, top=0, bottom=300):
    """Falling snow. Deterministic (a tiny LCG, not random) so rebuilds stay no-ops."""
    out, v = [], seed * 7919 + 17
    for _ in range(n):
        v = (v * 1103515245 + 12345) % 2**31
        x = v % 500
        v = (v * 1103515245 + 12345) % 2**31
        y = top + v % (bottom - top)
        r = 1.6 + (v >> 8) % 3 * .7
        out.append(f'<circle cx="{x}" cy="{y}" r="{r:.1f}"/>')
    return f'<g fill="#FFFFFF" opacity=".9">{"".join(out)}</g>'


def pine(x, y, s=1.0, snowy=True):
    """A fir tree, three tiers, with snow on the tiers."""
    out = [f'<rect x="{x-5*s:.0f}" y="{y-14*s:.0f}" width="{10*s:.0f}" height="{14*s:.0f}" fill="#8A6A44"/>']
    for i, (w, top, bot) in enumerate(((34, 66, 12), (28, 92, 40), (20, 116, 66))):
        out.append(f'<path d="M{x-w*s:.0f},{y-bot*s:.0f} L{x:.0f},{y-top*s-20*s:.0f} L{x+w*s:.0f},{y-bot*s:.0f} Z" '
                   f'fill="{"#3E8E5A" if i != 1 else "#4CA06A"}"/>')
        if snowy:
            out.append(f'<path d="M{x-w*.62*s:.0f},{y-bot*s-(top-bot)*.38*s:.0f} L{x:.0f},{y-top*s-20*s:.0f} '
                       f'L{x+w*.62*s:.0f},{y-bot*s-(top-bot)*.38*s:.0f} q{-w*.3*s:.0f},{5*s:.0f} {-w*.62*s:.0f},0 '
                       f'q{-w*.3*s:.0f},{-5*s:.0f} {-w*.62*s:.0f},0 Z" fill="#FFFFFF"/>')
    return "".join(out)


def snowman(x, y, s=1.0):
    return (f'<circle cx="{x}" cy="{y-24*s:.0f}" r="{26*s:.0f}" fill="#FFFFFF" stroke="#C8DCE8" stroke-width="2"/>'
            f'<circle cx="{x}" cy="{y-66*s:.0f}" r="{19*s:.0f}" fill="#FFFFFF" stroke="#C8DCE8" stroke-width="2"/>'
            f'<circle cx="{x-6*s:.0f}" cy="{y-70*s:.0f}" r="{2.4*s:.1f}" fill="{INK}"/>'
            f'<circle cx="{x+6*s:.0f}" cy="{y-70*s:.0f}" r="{2.4*s:.1f}" fill="{INK}"/>'
            f'<path d="M{x},{y-65*s:.0f} l{14*s:.0f},{3*s:.0f} l{-14*s:.0f},{3*s:.0f} Z" fill="#F08A3C"/>'
            f'<path d="M{x-7*s:.0f},{y-58*s:.0f} q{7*s:.0f},{5*s:.0f} {14*s:.0f},0" stroke="{INK}" '
            f'stroke-width="{2*s:.1f}" fill="none" stroke-linecap="round"/>'
            + "".join(f'<circle cx="{x}" cy="{y-(16+i*12)*s:.0f}" r="{2.6*s:.1f}" fill="{INK}"/>' for i in range(3))
            + f'<path d="M{x-18*s:.0f},{y-40*s:.0f} l{-18*s:.0f},{-16*s:.0f} M{x+18*s:.0f},{y-40*s:.0f} '
              f'l{18*s:.0f},{-16*s:.0f}" stroke="#8A6A44" stroke-width="{3*s:.1f}" stroke-linecap="round"/>')


def snowball(x, y, r=7, flying=False):
    out = f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" stroke="#C8DCE8" stroke-width="1.5"/>'
    if flying:
        out += "".join(f'<path d="M{x-r-4-i*9},{y-4+i*4} h-7" stroke="#C8DCE8" stroke-width="2.4" '
                       f'stroke-linecap="round"/>' for i in range(3))
    return out


def fireplace(x, y, w=110, h=120):
    """A brick hearth with a real fire in it - the cosiest thing in story 03."""
    return (f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}" rx="6" fill="#B8704A" stroke="#8A4E30" stroke-width="2"/>'
            f'<rect x="{x-10}" y="{y-h-12}" width="{w+20}" height="14" rx="4" fill="#8A5A3A"/>'
            f'<path d="M{x+18},{y} v{-h*.52:.0f} q{w/2-18:.0f},{-h*.26:.0f} {w-36},0 v{h*.52:.0f} Z" fill="#3A2420"/>'
            f'<path d="M{x+w*.3:.0f},{y-6} q{-6:.0f},-26 {w*.2:.0f},-46 q{-2:.0f},20 {w*.12:.0f},26 '
            f'q{8:.0f},-14 {2:.0f},-32 q{w*.22:.0f},24 {w*.1:.0f},52 Z" fill="#FF9A3C"/>'
            f'<path d="M{x+w*.4:.0f},{y-6} q{-2:.0f},-16 {w*.1:.0f},-26 q{4:.0f},14 {w*.1:.0f},26 Z" fill="#FFD166"/>'
            f'<rect x="{x+w*.26:.0f}" y="{y-8}" width="{w*.48:.0f}" height="8" rx="3" fill="#6B4A2E"/>'
            + "".join(f'<path d="M{x+6},{y-h+18+i*22} h{w-12}" stroke="#A0603E" stroke-width="1.5" opacity=".6"/>'
                      for i in range(2)))


def ice_cream(x, y, s=1.0):
    """A dish of ice cream - three cold scoops."""
    return (f'<path d="M{x-18*s:.0f},{y-12*s:.0f} q{18*s:.0f},{20*s:.0f} {36*s:.0f},0 Z" fill="#CFEAF6" stroke="#8FBCD0" stroke-width="1.5"/>'
            + "".join(f'<circle cx="{x+dx*s:.0f}" cy="{y+dy*s:.0f}" r="{9*s:.0f}" fill="{c}"/>'
                      for dx, dy, c in ((-9, -16, "#FFE3EC"), (9, -16, "#FFF3C4"), (0, -26, "#C8E8FF")))
            + f'<path d="M{x-4*s:.0f},{y-33*s:.0f} l{3*s:.0f},{-4*s:.0f}" stroke="#E4453F" stroke-width="{3*s:.1f}" stroke-linecap="round"/>')


def breather(x, y, on=False):
    """The breathing machine on its trolley: a box with a dial, a light, a hose. `on`
    lights it green and draws the hum - story 03's gust starts here."""
    out = (f'<rect x="{x-24}" y="{y-96}" width="48" height="58" rx="6" fill="#E8EEF2" stroke="#9AA6AE" stroke-width="2"/>'
           f'<circle cx="{x-6}" cy="{y-72}" r="10" fill="#FFFFFF" stroke="#9AA6AE" stroke-width="2"/>'
           f'<path d="M{x-6},{y-72} l6,-6" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>'
           f'<circle cx="{x+13}" cy="{y-82}" r="4" fill="{"#06C98A" if on else "#C8D0D6"}"/>'
           f'<rect x="{x-3}" y="{y-38}" width="6" height="30" fill="#9AA6AE"/>'
           f'<rect x="{x-20}" y="{y-10}" width="40" height="6" rx="3" fill="#9AA6AE"/>'
           + "".join(f'<circle cx="{x+dx}" cy="{y-2}" r="4" fill="#5E6870"/>' for dx in (-16, 16)))
    if on:
        out += "".join(f'<path d="M{x+30+i*8},{y-86+i*2} q5,6 0,12 q-5,6 0,12" stroke="#9AA6AE" '
                       f'stroke-width="1.8" fill="none" opacity="{.8-i*.2:.1f}"/>' for i in range(3))
    return out


def mask(x, y, s=1.0, hose_to=None):
    """A breathing mask - a clear cup with a strap - and its hose back to the machine."""
    out = ''
    if hose_to:
        hx, hy = hose_to
        out += (f'<path d="M{x},{y+8*s:.0f} C{x},{y+60:.0f} {hx},{hy+50:.0f} {hx},{hy}" stroke="#8FBCD0" '
                f'stroke-width="5" fill="none" stroke-linecap="round"/>')
    return out + (f'<ellipse cx="{x}" cy="{y}" rx="{16*s:.0f}" ry="{12*s:.0f}" fill="#CFEAF6" fill-opacity=".75" '
                  f'stroke="#4AA8C8" stroke-width="2"/>'
                  f'<path d="M{x-16*s:.0f},{y-3*s:.0f} h{-8*s:.0f} M{x+16*s:.0f},{y-3*s:.0f} h{8*s:.0f}" '
                  f'stroke="#4AA8C8" stroke-width="{2.4*s:.1f}" stroke-linecap="round"/>')


def syringe(x, y, s=1.0, rot=0):
    """An injection. At s≈2 it is the giraffe-sized one - the joke on page 9."""
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<rect x="{x-22*s:.0f}" y="{y-6*s:.0f}" width="{36*s:.0f}" height="{12*s:.0f}" rx="{3*s:.0f}" '
            f'fill="#E8F4FA" stroke="#8FBCD0" stroke-width="1.6"/>'
            f'<rect x="{x-18*s:.0f}" y="{y-4*s:.0f}" width="{20*s:.0f}" height="{8*s:.0f}" fill="#FFB3C6" opacity=".8"/>'
            f'<path d="M{x-22*s:.0f},{y:.0f} h{-12*s:.0f} M{x-34*s:.0f},{y-7*s:.0f} v{14*s:.0f}" '
            f'stroke="#9AA6AE" stroke-width="{3*s:.1f}" stroke-linecap="round"/>'
            f'<path d="M{x+14*s:.0f},{y:.0f} h{16*s:.0f}" stroke="#9AA6AE" stroke-width="{1.6*s:.1f}" '
            f'stroke-linecap="round"/></g>')


def pills(x, y):
    """A little pot of tablets."""
    return (f'<rect x="{x-9}" y="{y-20}" width="18" height="20" rx="3" fill="#FFFFFF" stroke="#C8BCA4" stroke-width="1.5"/>'
            f'<rect x="{x-10}" y="{y-25}" width="20" height="6" rx="2" fill="#FF6B6B"/>'
            + "".join(f'<ellipse cx="{x+dx}" cy="{y+4}" rx="4" ry="2.4" fill="{c}"/>'
                      for dx, c in ((-16, "#74C8E4"), (15, "#FFD166"))))


def chocolate(x, y, s=1.0, rot=-10):
    """A wrapped bar of chocolate - the thank-you at the end of story 03."""
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<rect x="{x-14*s:.0f}" y="{y-8*s:.0f}" width="{28*s:.0f}" height="{16*s:.0f}" rx="2" fill="#7A4A2A"/>'
            f'<rect x="{x-2*s:.0f}" y="{y-8*s:.0f}" width="{16*s:.0f}" height="{16*s:.0f}" rx="2" fill="#E4453F"/>'
            f'<rect x="{x+3*s:.0f}" y="{y-8*s:.0f}" width="{3*s:.0f}" height="{16*s:.0f}" fill="#FFD166"/></g>')


def cottage(x, y, s=1.0, snowy=True):
    """Tortoise's little house: a door, a round window, a snowy roof. `y` is the ground."""
    w, h = 96*s, 66*s
    return (f'<rect x="{x-w/2:.0f}" y="{y-h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="#FFE9C8" stroke="#D8B888" stroke-width="2"/>'
            f'<path d="M{x-w/2-10*s:.0f},{y-h+2:.0f} L{x:.0f},{y-h-46*s:.0f} L{x+w/2+10*s:.0f},{y-h+2:.0f} Z" '
            f'fill="#E4453F" stroke="#B8302C" stroke-width="2" stroke-linejoin="round"/>'
            + (f'<path d="M{x-w/2-10*s:.0f},{y-h+2:.0f} L{x:.0f},{y-h-46*s:.0f} L{x+w/2+10*s:.0f},{y-h+2:.0f} '
               f'q{-8*s:.0f},{-8*s:.0f} {-16*s:.0f},{-6*s:.0f} q{-(w/2-6*s):.0f},{-26*s:.0f} {-(w/2+4*s):.0f},{-36*s:.0f} '
               f'q{-(w/2-6*s):.0f},{12*s:.0f} {-(w/2+4*s):.0f},{36*s:.0f} Z" fill="#FFFFFF"/>' if snowy else '')
            + f'<rect x="{x+6*s:.0f}" y="{y-40*s:.0f}" width="{22*s:.0f}" height="{40*s:.0f}" rx="{10*s:.0f}" fill="#8A5A3A"/>'
            f'<circle cx="{x+23*s:.0f}" cy="{y-20*s:.0f}" r="{2*s:.1f}" fill="#FFD166"/>'
            f'<circle cx="{x-24*s:.0f}" cy="{y-36*s:.0f}" r="{11*s:.0f}" fill="#FFE39A" stroke="#D8B888" stroke-width="2"/>')


def cough(x, y, flip=False):
    """Little puffs of a cough, for the sniffly patients."""
    d = -1 if flip else 1
    return "".join(f'<circle cx="{x+d*i*9}" cy="{y-i*3}" r="{3.5+i*1.5:.1f}" fill="#FFFFFF" '
                   f'stroke="#C8DCE8" stroke-width="1.2" opacity="{.9-i*.2:.1f}"/>' for i in range(3))


def shiver(x, y, h=40, gap=30, color="#74C8E4"):
    """Wobble lines either side of a shivering (or sweltering) patient."""
    return "".join(f'<path d="M{x+sx*gap},{y} q{sx*5},{h*.12:.0f} 0,{h*.25:.0f} q{-sx*5},{h*.12:.0f} 0,{h*.25:.0f} '
                   f'q{sx*5},{h*.12:.0f} 0,{h*.25:.0f}" stroke="{color}" stroke-width="2.2" fill="none" '
                   f'stroke-linecap="round"/>' for sx in (-1, 1))
