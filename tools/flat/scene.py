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
    so do the arithmetic. `tail` is the scene point the speaker is at: the tail is a
    short wedge AIMED at it, not a spike that reaches it. Running the tail all the
    way to the speaker drew long needles across the page that ended in a
    character's eye.
    """
    if isinstance(lines, str):
        lines = [lines]
    rx = max(52, max(len(t) for t in lines) * size * .34 + 28)
    ry = 20 + 9 * (len(lines) - 1)
    body = (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx:.0f}" ry="{ry}" fill="white" '
            f'stroke="#D0C8B8" stroke-width="1.5"/>')
    if tail:
        wedge = _tail(cx, cy, rx, ry, tail)
        # outlined wedge, then the bubble over its root, then the wedge's fill again
        # to wipe the bubble's outline where they join - one seamless shape
        out = [f'<path d="{wedge}" fill="white" stroke="#D0C8B8" stroke-width="1.5" stroke-linejoin="round"/>',
               body, f'<path d="{wedge}" fill="white"/>']
    else:
        out = [body]
    y0 = cy - (len(lines) - 1) * 9 + 4
    for i, t in enumerate(lines):
        out.append(f'<text x="{cx}" y="{y0 + i*18:.0f}" text-anchor="middle" font-size="{size}" '
                   f'fill="{color}" font-family="Nunito, sans-serif" font-weight="700">{t}</text>')
    return "".join(out)


TAIL_MAX, TAIL_GAP = 70, 18    # longest a tail gets; how far short of the speaker it stops


def _edge(cx, cy, rx, ry, ux, uy):
    """Distance from an ellipse's centre to its outline along the unit vector (ux, uy)."""
    return 1 / ((ux / rx) ** 2 + (uy / ry) ** 2) ** .5


def _tail(cx, cy, rx, ry, target):
    """A speech-bubble tail as an SVG path: rooted just inside the outline, curving
    towards `target` and covering about half the gap - far enough that a bubble up in
    the sky still visibly belongs to its speaker, never so far that it ends in their
    face (the old tails ran the whole way, and did)."""
    tx, ty = target
    dx, dy = tx - cx, ty - cy
    L = (dx*dx + dy*dy) ** .5 or 1
    ux, uy = dx / L, dy / L
    e = _edge(cx, cy, rx, ry, ux, uy)
    gap = L - e
    reach = max(14, min(TAIL_MAX, gap * .55, gap - TAIL_GAP))
    bx, by = cx + ux*(e - 4), cy + uy*(e - 4)
    px, py = -uy, ux
    half = 8 if reach < 40 else 7
    tipx, tipy = cx + ux*(e + reach), cy + uy*(e + reach)
    # both edges bow the same way, so the tail curls slightly instead of spiking
    bow = reach * .14
    mx, my = cx + ux*(e + reach*.5) + px*bow, cy + uy*(e + reach*.5) + py*bow
    return (f'M{bx - px*half:.1f},{by - py*half:.1f} Q{mx - px*half*.45:.1f},{my - py*half*.45:.1f} {tipx:.1f},{tipy:.1f} '
            f'Q{mx + px*half*.45:.1f},{my + py*half*.45:.1f} {bx + px*half:.1f},{by + py*half:.1f} Z')


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
    ux, uy = dx / L, dy / L
    e = _edge(cx, cy, rx, ry, ux, uy)
    # the dots trail off towards the thinker but stop well short of them, as the
    # speech tails do - three dots strung across half the page read as litter
    room = max(26, min(46, L - e - TAIL_GAP))
    dots = "".join(f'<circle cx="{cx+ux*(e+d*room):.0f}" cy="{cy+uy*(e+d*room):.0f}" r="{r}" '
                   f'fill="white" stroke="#D0C8B8" stroke-width="1.2"/>'
                   for d, r in ((.22, 5.5), (.6, 4), (.95, 2.8)))
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


# ---------------------------------------------------------------- story 07 props
# Story 07 is a night at Rabbit's burrow. Night is a soft indigo veil laid OVER the
# room (night()), never a dark background: the room underneath is the same warm
# burrow as in daylight, so a dim page still reads as cosy, and a lamp or the moon
# can glow back through the veil. The audience is small; dark must never mean scary.
NIGHT = "#2B3A67"
EARTH, EARTH_DK = "#C48F5E", "#A8744A"
WOOD, WOOD_DK = "#D9AE7A", "#B98A56"


def burrow(uid, floor=262, wall=("#F6E2C4", "#ECCDA4")):
    """Rabbit's burrow from the inside: a warm dug-out room under an arched earth
    ceiling, a few roots poking through, and a plank floor."""
    top, bot = wall
    pebbles = ((14, 40, 5), (34, 18, 3.5), (474, 30, 4.5), (486, 70, 3), (20, 120, 3.5), (488, 150, 4),
               (240, 6, 3), (120, 4, 2.5), (380, 5, 3))
    return (f'<defs><linearGradient id="wall-{uid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bot}"/></linearGradient></defs>'
            f'<rect width="500" height="360" fill="{EARTH}"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{EARTH_DK}" opacity=".7"/>' for x, y, r in pebbles)
            + f'<path d="M30,{floor} L30,96 Q30,16 120,14 L380,14 Q470,16 470,96 L470,{floor} Z" fill="url(#wall-{uid})"/>'
            f'<path d="M150,14 q4,18 -2,30 q-4,8 2,16 M330,14 q-3,14 3,24 M352,14 q2,10 -3,18" stroke="{EARTH_DK}" '
            f'stroke-width="3" fill="none" stroke-linecap="round"/>'
            f'<rect y="{floor}" width="500" height="{360-floor}" fill="{WOOD}"/>'
            f'<line x1="0" y1="{floor}" x2="500" y2="{floor}" stroke="{WOOD_DK}" stroke-width="3"/>'
            + "".join(f'<line x1="0" y1="{floor+dy}" x2="500" y2="{floor+dy}" stroke="{WOOD_DK}" stroke-width="1.4" opacity=".55"/>'
                      for dy in (30, 64))
            + "".join(f'<line x1="{x}" y1="{floor+y0}" x2="{x}" y2="{floor+y1}" stroke="{WOOD_DK}" stroke-width="1.4" opacity=".55"/>'
                      for x, y0, y1 in ((90, 0, 30), (300, 0, 30), (190, 30, 64), (420, 30, 64), (60, 64, 98), (330, 64, 98))))


def night(op=.42):
    """Lights out: an indigo veil over everything drawn so far."""
    return f'<rect width="500" height="360" fill="{NIGHT}" opacity="{op}"/>'


def glow(x, y, r=70, color="#FFE9A8"):
    """Warm light pooling round a lamp, drawn over the night veil."""
    return "".join(f'<circle cx="{x}" cy="{y}" r="{r*k:.0f}" fill="{color}" opacity="{o}"/>'
                   for k, o in ((1, .14), (.66, .16), (.36, .22)))


def porthole(x, y, r=34, sky='night'):
    """A round burrow window. `sky` is night (moon and stars), sunset or morning."""
    fill = {'night': "#3B4E86", 'sunset': "#FFB99A", 'morning': "#BEE7FB"}[sky]
    inner = ''
    if sky == 'night':
        inner = (f'<circle cx="{x+r*.3:.0f}" cy="{y-r*.25:.0f}" r="{r*.32:.0f}" fill="#FFF3C4"/>'
                 f'<circle cx="{x+r*.42:.0f}" cy="{y-r*.33:.0f}" r="{r*.28:.0f}" fill="{fill}"/>'
                 + "".join(f'<circle cx="{x+dx*r:.0f}" cy="{y+dy*r:.0f}" r="1.6" fill="#FFF3C4"/>'
                           for dx, dy in ((-.5, -.3), (-.2, .3), (-.55, .35), (.1, -.55), (.45, .4))))
    else:
        inner = (f'<circle cx="{x+r*.25:.0f}" cy="{y+r*.1:.0f}" r="{r*.3:.0f}" fill="#FFD166"/>'
                 f'<path d="M{x-r},{y+r*.55:.0f} q{r*.6:.0f},{-r*.35:.0f} {r*2},{-r*.1:.0f} V{y+r} H{x-r} Z" fill="#8ECB7E"/>')
    return (f'<circle cx="{x}" cy="{y}" r="{r+7}" fill="{WOOD}" stroke="{WOOD_DK}" stroke-width="2.5"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>'
            + clip(f'ph{x}{y}', x-r, y-r, 2*r, 2*r, inner)
            + f'<path d="M{x},{y-r} v{2*r} M{x-r},{y} h{2*r}" stroke="{WOOD_DK}" stroke-width="3"/>')


def picture(x, y, w=44, h=36, tilt=0, art='carrot', wobble=False):
    """A framed picture on the burrow wall; `wobble` adds the wibble-wobble marks."""
    arts = {
        'carrot': (f'<path d="M{x-4},{y-8} L{x+4},{y-8} L{x},{y+12} Z" fill="#F08A3C"/>'
                   f'<path d="M{x},{y-8} q-6,-8 -2,-10 M{x},{y-8} q6,-8 2,-10" stroke="#4A9B4A" stroke-width="2.2" fill="none"/>'),
        'heart': f'<text x="{x}" y="{y+7}" font-size="20" text-anchor="middle" fill="#FF6B6B">&#9829;</text>',
        'hills': (f'<path d="M{x-w/2+4},{y+h/2-4} L{x-6},{y-6} L{x+4},{y+4} L{x+10},{y-2} L{x+w/2-4},{y+h/2-4} Z" fill="#8ECB7E"/>'
                  f'<circle cx="{x+10}" cy="{y-8}" r="4" fill="#FFD166"/>'),
    }
    out = (f'<g transform="rotate({tilt} {x} {y-h/2})">'
           f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="3" fill="#FFFDF6" stroke="{WOOD_DK}" stroke-width="3"/>'
           f'{arts[art]}</g>')
    if wobble:
        out += "".join(f'<path d="M{x+sx*(w/2+8)},{y-10} q{sx*4},5 0,10 q{-sx*4},5 0,10" stroke="#8FA8C0" '
                       f'stroke-width="2" fill="none" stroke-linecap="round"/>' for sx in (-1, 1))
    return out


def lamp(x, y, on=True, blanket=False):
    """A side table with a little lamp on it. `y` is the floor. `blanket` is Rabbit's
    blanket, blown clean off her bed and draped over the shade."""
    out = (f'<rect x="{x-24}" y="{y-58}" width="48" height="8" rx="3" fill="{WOOD}" stroke="{WOOD_DK}" stroke-width="1.5"/>'
           f'<rect x="{x-19}" y="{y-50}" width="6" height="50" fill="{WOOD_DK}"/><rect x="{x+13}" y="{y-50}" width="6" height="50" fill="{WOOD_DK}"/>'
           f'<rect x="{x-3}" y="{y-86}" width="6" height="28" fill="#9AA6AE"/>'
           f'<ellipse cx="{x}" cy="{y-58}" rx="12" ry="4" fill="#9AA6AE"/>'
           f'<path d="M{x-22},{y-84} L{x-13},{y-112} L{x+13},{y-112} L{x+22},{y-84} Z" '
           f'fill="{"#FFE39A" if on else "#E8D6A8"}" stroke="#D8B05A" stroke-width="1.5"/>')
    if blanket:
        out += (f'<path d="M{x-30},{y-70} Q{x-26},{y-120} {x},{y-118} Q{x+28},{y-120} {x+32},{y-66} '
                f'q-8,6 -14,-2 q-8,8 -16,0 q-8,8 -16,0 q-8,8 -16,2 Z" fill="#74C8E4" stroke="#4AA8C8" stroke-width="1.5"/>'
                + "".join(f'<circle cx="{x+dx}" cy="{y+dy}" r="3" fill="#FFFDF6" opacity=".85"/>'
                          for dx, dy in ((-14, -100), (8, -106), (16, -86), (-6, -84))))
    return out


def sofa(x, y, w=180, squashed=False, color="#FF9BAE", line="#E0708A"):
    """Rabbit's sofa. `y` is the floor. Squashed, the seat is pancaked to the floor,
    the arms splay out and a spring pings loose."""
    if squashed:
        return (f'<rect x="{x-w/2:.0f}" y="{y-22}" width="{w}" height="22" rx="8" fill="{color}" stroke="{line}" stroke-width="2"/>'
                f'<rect x="{x-w/2+6:.0f}" y="{y-44}" width="{w-12}" height="24" rx="8" fill="{color}" stroke="{line}" stroke-width="2" '
                f'transform="rotate(-3 {x} {y-32})"/>'
                + "".join(f'<rect x="{x+sx*w/2-12:.0f}" y="{y-40}" width="24" height="40" rx="9" fill="{color}" stroke="{line}" '
                          f'stroke-width="2" transform="rotate({sx*28} {x+sx*w/2:.0f} {y})"/>' for sx in (-1, 1))
                + f'<path d="M{x+w*.3:.0f},{y-44} l6,-8 l-10,-6 l10,-6 l-10,-6 l8,-8" stroke="#9AA6AE" stroke-width="2.4" '
                  f'fill="none" stroke-linejoin="round" stroke-linecap="round"/>')
    return (f'<rect x="{x-w/2+10:.0f}" y="{y-96}" width="{w-20}" height="56" rx="14" fill="{color}" stroke="{line}" stroke-width="2"/>'
            f'<rect x="{x-w/2+10:.0f}" y="{y-52}" width="{w-20}" height="34" rx="8" fill="{color}" stroke="{line}" stroke-width="2"/>'
            + "".join(f'<rect x="{x+sx*(w/2-14)-14:.0f}" y="{y-70}" width="28" height="60" rx="12" fill="{color}" '
                      f'stroke="{line}" stroke-width="2"/>' for sx in (-1, 1))
            + "".join(f'<rect x="{x+dx:.0f}" y="{y-12}" width="8" height="12" fill="{WOOD_DK}"/>' for dx in (-w/2+10, w/2-18)))


CUSHIONS = ("#FF9BAE", "#FFD166", "#74C8E4", "#C77DFF", "#8ECB7E", "#FFB347")


def nest(x, y, w=260):
    """Every cushion in the burrow, heaped into one giant bed on the floor."""
    out = [f'<ellipse cx="{x}" cy="{y-10}" rx="{w/2:.0f}" ry="24" fill="#F0D9A8" stroke="#D8B888" stroke-width="2"/>']
    for i in range(9):
        cx = x - w/2 + 26 + i*(w-52)/8
        cy = y - 22 - (8 if i % 2 else 0)
        out.append(f'<rect x="{cx-22:.0f}" y="{cy-14:.0f}" width="44" height="28" rx="11" fill="{CUSHIONS[i % 6]}" '
                   f'stroke="#00000022" stroke-width="1.5" transform="rotate({(i % 3 - 1)*9} {cx:.0f} {cy:.0f})"/>')
    return "".join(out)


def nest_front(x, y, w=260):
    """The near rim of the nest, drawn OVER whoever is lying in it so they sink in."""
    return "".join(f'<rect x="{x-w/2+10+i*(w-20)/5:.0f}" y="{y-20}" width="{(w-20)/5+8:.0f}" height="24" rx="11" '
                   f'fill="{CUSHIONS[(i+2) % 6]}" stroke="#00000022" stroke-width="1.5"/>' for i in range(5))


def little_bed(x, y, w=120, sleeper="", quilt="#74C8E4"):
    """Rabbit's own small bed, `y` the floor. Like the car, it draws its sleeper
    itself: the quilt goes OVER them, so only a head and ears show. `quilt=None`
    leaves the bed bare - the night Rabbit's quilt blows off onto the lamp."""
    top = y - 44
    return (f'<rect x="{x-w/2-8:.0f}" y="{top-46}" width="14" height="{y-top+46}" rx="5" fill="{WOOD_DK}"/>'
            f'<rect x="{x+w/2-6:.0f}" y="{top-18}" width="14" height="{y-top+18}" rx="5" fill="{WOOD_DK}"/>'
            f'<rect x="{x-w/2:.0f}" y="{top}" width="{w}" height="22" rx="6" fill="#FFFDF6" stroke="#D8C8A8" stroke-width="1.5"/>'
            f'<rect x="{x-w/2+6:.0f}" y="{top-12}" width="34" height="16" rx="7" fill="#FFFFFF" stroke="#D8C8A8" stroke-width="1.5"/>'
            + sleeper
            + ((f'<path d="M{x-w/2+26:.0f},{top+4} Q{x+10:.0f},{top-14} {x+w/2+2:.0f},{top+2} L{x+w/2+2:.0f},{top+26} '
                f'L{x-w/2+26:.0f},{top+26} Z" fill="{quilt}" stroke="#4AA8C8" stroke-width="1.5"/>'
                + "".join(f'<circle cx="{x+dx:.0f}" cy="{top+dy}" r="3" fill="#FFFDF6" opacity=".85"/>'
                          for dx, dy in ((-10, 10), (14, 4), (36, 12), (2, 20)))) if quilt else '')
            + f'<rect x="{x-w/2+4:.0f}" y="{top+22}" width="{w-8}" height="10" rx="3" fill="{WOOD}"/>')


def snore(x, y, s=1.0, n=3, soft=False):
    """Snore waves rolling out from a trunk. `soft` is the gentle side-sleeping hum."""
    col = "#8FA8C0" if soft else "#5B7BA8"
    return "".join(f'<path d="M{x+i*14*s:.0f},{y-(22+i*10)*s:.0f} q{8*s:.0f},{(22+i*10)*s:.0f} 0,{(44+i*20)*s:.0f}" '
                   f'stroke="{col}" stroke-width="{(2 if soft else 3.2)*s:.1f}" fill="none" stroke-linecap="round" '
                   f'opacity="{.85-i*.18:.2f}"/>' for i in range(n))


def peg(x, y, s=1.0, rot=0):
    """A wooden clothes peg."""
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<rect x="{x-14*s:.0f}" y="{y-4*s:.0f}" width="{28*s:.0f}" height="{4*s:.0f}" rx="1.5" fill="{WOOD}" stroke="{WOOD_DK}" stroke-width="1"/>'
            f'<rect x="{x-14*s:.0f}" y="{y+1*s:.0f}" width="{28*s:.0f}" height="{4*s:.0f}" rx="1.5" fill="{WOOD}" stroke="{WOOD_DK}" stroke-width="1"/>'
            f'<circle cx="{x}" cy="{y+.5*s:.1f}" r="{3.4*s:.1f}" fill="none" stroke="#9AA6AE" stroke-width="{1.6*s:.1f}"/></g>')


def flight(pts, color="#8FA8C0"):
    """A dotted trajectory through the given points - the peg's bouncy route."""
    d = f'M{pts[0][0]},{pts[0][1]} ' + " ".join(f'L{x},{y}' for x, y in pts[1:])
    return (f'<path d="{d}" stroke="{color}" stroke-width="2.6" fill="none" stroke-dasharray="2 7" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def apple(x, y, r=9, color="#FF6B6B"):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" stroke="#00000022" stroke-width="1"/>'
            f'<path d="M{x},{y-r} q1,-5 4,-6" stroke="#6B4A24" stroke-width="2" fill="none" stroke-linecap="round"/>'
            f'<circle cx="{x-r*.35:.1f}" cy="{y-r*.35:.1f}" r="{r*.22:.1f}" fill="#FFFFFF" opacity=".6"/>')


def fruit_bowl(x, y, w=150, rider=""):
    """The big kitchen fruit bowl, big enough to sleep in. `y` is the floor it stands
    on. It owns its rider: melon and apples go in behind them, the bowl's front over."""
    rim = y - 62
    return (f'<ellipse cx="{x}" cy="{rim}" rx="{w/2:.0f}" ry="14" fill="#E8D6B4" stroke="#C8B48C" stroke-width="2"/>'
            f'<ellipse cx="{x+w*.26:.0f}" cy="{rim-14}" rx="26" ry="22" fill="#8ECB7E" stroke="#5E9B50" stroke-width="2"/>'
            f'<path d="M{x+w*.26-14:.0f},{rim-28} q14,10 28,0 M{x+w*.26-20:.0f},{rim-16} q20,10 40,0" stroke="#5E9B50" stroke-width="1.6" fill="none"/>'
            + apple(x - w*.3, rim - 10, 11) + apple(x - w*.18, rim - 4, 10, "#FFD166")
            + rider
            + f'<path d="M{x-w/2:.0f},{rim} Q{x-w/2+6:.0f},{y-6} {x:.0f},{y-4} Q{x+w/2-6:.0f},{y-6} {x+w/2:.0f},{rim} '
              f'Q{x:.0f},{rim+16} {x-w/2:.0f},{rim} Z" fill="#FFFFFF" stroke="#C8B48C" stroke-width="2"/>'
            + f'<path d="M{x-w*.36:.0f},{rim+20} Q{x:.0f},{rim+34} {x+w*.36:.0f},{rim+20}" stroke="#74C8E4" stroke-width="4" '
              f'fill="none" stroke-linecap="round" opacity=".8"/>'
            + f'<rect x="{x-24}" y="{y-6}" width="48" height="6" rx="3" fill="#C8B48C"/>')


def kitchen(uid, floor=262):
    """The burrow kitchen: the same dug-out room, with a counter, a shelf of pots and
    a round window."""
    return (burrow(uid, floor)
            + f'<rect x="300" y="{floor-86}" width="170" height="86" fill="#F2E2C4" stroke="{WOOD_DK}" stroke-width="2"/>'
            f'<rect x="294" y="{floor-92}" width="182" height="10" rx="3" fill="{WOOD}" stroke="{WOOD_DK}" stroke-width="1.5"/>'
            + "".join(f'<rect x="{x}" y="{floor-74}" width="70" height="62" rx="4" fill="none" stroke="{WOOD_DK}" stroke-width="1.5"/>'
                      f'<circle cx="{x+35}" cy="{floor-44}" r="3" fill="{WOOD_DK}"/>' for x in (310, 390)))


def shelf(x, y, w=150, pots=True, tipped=False):
    """A wall shelf with pots and a jar. `tipped` knocks it crooked, mid-CLANG."""
    rot = -10 if tipped else 0
    items = ''
    if pots:
        items = (f'<rect x="{x-w/2+10:.0f}" y="{y-24}" width="30" height="24" rx="4" fill="#9AA6AE" stroke="#6E7880" stroke-width="1.5"/>'
                 f'<rect x="{x-6:.0f}" y="{y-30}" width="22" height="30" rx="4" fill="#FFD166" stroke="#D8A21F" stroke-width="1.5"/>'
                 f'<rect x="{x-8:.0f}" y="{y-34}" width="26" height="6" rx="2" fill="#E4453F"/>'
                 f'<rect x="{x+w/2-40:.0f}" y="{y-20}" width="30" height="20" rx="4" fill="#C8BCA4" stroke="#9A8E78" stroke-width="1.5"/>')
    return (f'<g transform="rotate({rot} {x} {y})">{items}'
            f'<rect x="{x-w/2:.0f}" y="{y}" width="{w}" height="8" rx="2" fill="{WOOD}" stroke="{WOOD_DK}" stroke-width="1.5"/>'
            f'<path d="M{x-w/2+14:.0f},{y+8} l10,14 M{x+w/2-14:.0f},{y+8} l-10,14" stroke="{WOOD_DK}" stroke-width="3"/></g>')


def saucepan(x, y, s=1.0, rot=0):
    """A saucepan, opening DOWN - jammed on a head like a helmet. `x, y` is the
    middle of its rim."""
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<path d="M{x-34*s:.0f},{y:.0f} L{x-30*s:.0f},{y-40*s:.0f} Q{x:.0f},{y-48*s:.0f} {x+30*s:.0f},{y-40*s:.0f} '
            f'L{x+34*s:.0f},{y:.0f} Z" fill="#B8C2CA" stroke="#7E8A92" stroke-width="2"/>'
            f'<rect x="{x-37*s:.0f}" y="{y-5*s:.0f}" width="{74*s:.0f}" height="{8*s:.0f}" rx="3" fill="#9AA6AE" stroke="#7E8A92" stroke-width="1.5"/>'
            f'<path d="M{x-20*s:.0f},{y-30*s:.0f} q8,-6 16,-4" stroke="#FFFFFF" stroke-width="3" fill="none" opacity=".7" stroke-linecap="round"/>'
            f'<rect x="{x+30*s:.0f}" y="{y-34*s:.0f}" width="{46*s:.0f}" height="{9*s:.0f}" rx="4" fill="#5E6870" '
            f'transform="rotate(-14 {x+30*s:.0f} {y-30*s:.0f})"/></g>')


def skate(x, y, rot=0):
    """Rabbit's roller skate, `y` the floor under its wheels."""
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<path d="M{x-22},{y-12} L{x-22},{y-34} Q{x-22},{y-40} {x-14},{y-40} L{x-4},{y-40} L{x-4},{y-24} '
            f'L{x+18},{y-22} Q{x+26},{y-20} {x+24},{y-12} Z" fill="#FF6B6B" stroke="#C0484A" stroke-width="1.5"/>'
            f'<rect x="{x-24}" y="{y-14}" width="50" height="5" rx="2" fill="#5E6870"/>'
            + "".join(f'<circle cx="{x+dx}" cy="{y-5}" r="5" fill="#FFD166" stroke="#D8A21F" stroke-width="1.5"/>' for dx in (-15, 15))
            + '</g>')


def banana(x, y, s=1.0, rot=0):
    return (f'<path d="M{x-14*s:.0f},{y-4*s:.0f} Q{x:.0f},{y+10*s:.0f} {x+16*s:.0f},{y-8*s:.0f} '
            f'Q{x:.0f},{y+2*s:.0f} {x-14*s:.0f},{y-4*s:.0f} Z" fill="#FFD166" stroke="#D8A21F" stroke-width="1.5" '
            f'transform="rotate({rot} {x} {y})"/>')


def suitcase(x, y, s=1.0, rot=0):
    """`x, y` is the handle - where a trunk grips it."""
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<path d="M{x-8*s:.0f},{y+6*s:.0f} v{-8*s:.0f} h{16*s:.0f} v{8*s:.0f}" stroke="#6B4A2E" stroke-width="{3*s:.1f}" fill="none"/>'
            f'<rect x="{x-26*s:.0f}" y="{y+6*s:.0f}" width="{52*s:.0f}" height="{36*s:.0f}" rx="5" fill="#C77DFF" stroke="#9B4DDB" stroke-width="2"/>'
            f'<rect x="{x-26*s:.0f}" y="{y+18*s:.0f}" width="{52*s:.0f}" height="{5*s:.0f}" fill="#9B4DDB" opacity=".6"/>'
            f'<circle cx="{x+12*s:.0f}" cy="{y+30*s:.0f}" r="{4*s:.1f}" fill="#FFD166"/></g>')


def teddy(x, y, s=1.0):
    """A little teddy bear, `x, y` its middle."""
    c, l = "#E8B47A", "#B98448"
    return (f'<circle cx="{x-8*s:.0f}" cy="{y-18*s:.0f}" r="{5*s:.1f}" fill="{c}" stroke="{l}" stroke-width="1.2"/>'
            f'<circle cx="{x+8*s:.0f}" cy="{y-18*s:.0f}" r="{5*s:.1f}" fill="{c}" stroke="{l}" stroke-width="1.2"/>'
            f'<ellipse cx="{x}" cy="{y+6*s:.0f}" rx="{11*s:.1f}" ry="{12*s:.1f}" fill="{c}" stroke="{l}" stroke-width="1.2"/>'
            f'<circle cx="{x}" cy="{y-10*s:.0f}" r="{10*s:.1f}" fill="{c}" stroke="{l}" stroke-width="1.2"/>'
            f'<circle cx="{x-3.5*s:.1f}" cy="{y-11*s:.0f}" r="{1.4*s:.1f}" fill="{INK}"/>'
            f'<circle cx="{x+3.5*s:.1f}" cy="{y-11*s:.0f}" r="{1.4*s:.1f}" fill="{INK}"/>'
            f'<ellipse cx="{x}" cy="{y-6*s:.0f}" rx="{2.4*s:.1f}" ry="{1.8*s:.1f}" fill="{l}"/>')


def pillow(x, y, w=56, h=32, rot=0, color="#FFFFFF", line="#D0C8B8"):
    return (f'<path d="M{x-w/2:.0f},{y-h/2:.0f} Q{x:.0f},{y-h/2+6:.0f} {x+w/2:.0f},{y-h/2:.0f} '
            f'Q{x+w/2-6:.0f},{y:.0f} {x+w/2:.0f},{y+h/2:.0f} Q{x:.0f},{y+h/2-6:.0f} {x-w/2:.0f},{y+h/2:.0f} '
            f'Q{x-w/2+6:.0f},{y:.0f} {x-w/2:.0f},{y-h/2:.0f} Z" fill="{color}" stroke="{line}" stroke-width="1.8" '
            f'stroke-linejoin="round" transform="rotate({rot} {x} {y})"/>')


def feather(x, y, s=1.0, rot=0):
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<path d="M{x},{y-12*s:.0f} Q{x+7*s:.0f},{y-2*s:.0f} {x},{y+10*s:.0f} Q{x-7*s:.0f},{y-2*s:.0f} {x},{y-12*s:.0f} Z" '
            f'fill="#FFFFFF" stroke="#C8C0B0" stroke-width="1.1"/>'
            f'<path d="M{x},{y-10*s:.0f} V{y+14*s:.0f}" stroke="#C8C0B0" stroke-width="1.1"/></g>')


def feathers(n=18, seed=7, box=(20, 20, 480, 300)):
    """A flurry of feathers. Deterministic, like flakes()."""
    x0, y0, x1, y1 = box
    out, v = [], seed * 7919 + 17
    for _ in range(n):
        v = (v * 1103515245 + 12345) % 2**31
        x = x0 + v % (x1 - x0)
        v = (v * 1103515245 + 12345) % 2**31
        y = y0 + v % (y1 - y0)
        out.append(feather(x, y, .8 + (v >> 9) % 3 * .2, (v >> 5) % 160 - 80))
    return "".join(out)


def burrow_hill(x, y, door=(0, 0), door_r=30, open_door=False):
    """Rabbit's front door, from outside: a grassy hump with a small round door in it.
    `x` is the hill's middle, `y` the ground; `door` offsets the doorway from the
    hill's foot. Returns the hill and door - the door is small ON PURPOSE."""
    dx, dy = x + door[0], y + door[1]
    r = door_r
    hole = (f'M{dx-r},{dy} L{dx-r},{dy-r*.9:.0f} A{r},{r} 0 0 1 {dx+r},{dy-r*.9:.0f} L{dx+r},{dy} Z')
    out = (f'<path d="M{x-190},{y+6} Q{x-150},{y-150} {x+10},{y-160} Q{x+170},{y-150} {x+210},{y+6} Z" fill="#7DBE6E"/>'
           f'<path d="M{x-150},{y-40} q20,-12 40,-6 M{x+90},{y-110} q18,-8 34,0 M{x-60},{y-130} q14,-6 28,0" '
           f'stroke="#5E9B50" stroke-width="2.4" fill="none" stroke-linecap="round" opacity=".7"/>'
           f'<path d="{hole}" fill="#5A3A1E" stroke="{EARTH_DK}" stroke-width="6"/>')
    if open_door:
        out += f'<path d="{hole}" fill="#3A2412"/>'
    else:
        out += (f'<path d="{hole}" fill="#C08840" stroke="#8A5A26" stroke-width="2"/>'
                + "".join(f'<line x1="{dx+k*r/2.5:.0f}" y1="{dy}" x2="{dx+k*r/2.5:.0f}" y2="{dy-r*1.6:.0f}" '
                          f'stroke="#8A5A26" stroke-width="1.5" opacity=".6"/>' for k in (-1, 0, 1))
                + f'<circle cx="{dx}" cy="{dy-r*1.05:.0f}" r="{r*.26:.0f}" fill="#FFE39A" stroke="#8A5A26" stroke-width="1.5"/>'
                  f'<circle cx="{dx+r*.62:.0f}" cy="{dy-r*.5:.0f}" r="2.6" fill="#FFD166"/>')
    return out


# ---------------------------------------------------------------- story 08 props
# Story 08 is hide and seek in the meadow, so every prop is a hiding place - and
# every one that hides Elephant is comically too small for him.
LEAF, LEAF_DK, LEAF_LT = "#6BAF5E", "#4A8F44", "#8ECB7E"
BARK, BARK_DK = "#A87A52", "#7E5A38"
CHECK = "#FF6B6B"


def skinny_tree(x, y, h=210, r=38):
    """A very skinny tree: a stick of a trunk and a small tuft on top. Drawn OVER
    whoever hides behind it, which is the joke."""
    return (f'<path d="M{x-8},{y} L{x-6},{y-h} L{x+6},{y-h} L{x+8},{y} Z" fill="{BARK}" stroke="{BARK_DK}" stroke-width="1.5"/>'
            f'<path d="M{x+4},{y-h*.8:.0f} q12,-6 18,-20" stroke="{BARK}" stroke-width="5" fill="none" stroke-linecap="round"/>'
            + "".join(f'<circle cx="{x+dx}" cy="{y-h+dy}" r="{rr}" fill="{c}"/>'
                      for dx, dy, rr, c in ((-16, -10, r*.7, LEAF), (16, -6, r*.66, LEAF), (0, -26, r*.8, LEAF_LT)))
            + f'<circle cx="{x+22}" cy="{y-h*.8-22:.0f}" r="9" fill="{LEAF_LT}"/>')


def leaves(pts, color=LEAF):
    """Loose leaves fluttering about: (x, y, rot) each."""
    return "".join(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="8" ry="4" fill="{color}" transform="rotate({r} {x:.0f} {y:.0f})"/>'
                   for x, y, r in pts)


def bush(x, y, w=130, h=90, tail=False, flying=False):
    """A round leafy bush, `y` the ground. `tail` is an elephant's tail poking out of
    its side; `flying` scatters a few leaves off it."""
    blobs = ((-w*.32, -h*.36, h*.42), (w*.3, -h*.38, h*.42), (0, -h*.58, h*.48), (-w*.1, -h*.3, h*.44), (w*.16, -h*.3, h*.4))
    out = (f'<ellipse cx="{x}" cy="{y-2}" rx="{w*.52:.0f}" ry="8" fill="#4A6B3A" opacity=".16"/>'
           + "".join(f'<circle cx="{x+dx:.0f}" cy="{y+dy:.0f}" r="{rr:.0f}" fill="{LEAF}" stroke="{LEAF_DK}" stroke-width="1.5"/>'
                     for dx, dy, rr in blobs)
           + "".join(f'<circle cx="{x+dx:.0f}" cy="{y+dy:.0f}" r="{rr:.0f}" fill="{LEAF_LT}" opacity=".7"/>'
                     for dx, dy, rr in ((-w*.2, -h*.6, h*.16), (w*.18, -h*.7, h*.14), (w*.32, -h*.44, h*.1))))
    if tail:
        tx, ty = x + w*.5, y - h*.36
        out += (f'<path d="M{tx-10:.0f},{ty:.0f} q24,-4 30,-22" stroke="#88A0AC" stroke-width="6" fill="none" stroke-linecap="round"/>'
                f'<path d="M{tx-10:.0f},{ty:.0f} q24,-4 30,-22" stroke="#A8C0CC" stroke-width="3.6" fill="none" stroke-linecap="round"/>'
                f'<path d="M{tx+20:.0f},{ty-22:.0f} q-2,-10 4,-14 q2,6 4,0 q6,4 2,14 Z" fill="{INK}"/>')
    if flying:
        out += "".join(f'<ellipse cx="{x+dx:.0f}" cy="{y+dy:.0f}" rx="7" ry="3.5" fill="{LEAF}" '
                       f'transform="rotate({rot} {x+dx:.0f} {y+dy:.0f})"/>'
                       for dx, dy, rot in ((-w*.6, -h*1.1, -30), (w*.1, -h*1.4, 20), (w*.62, -h*1.0, 50), (-w*.3, -h*1.5, 70)))
    return out


def pond(uid, x, y, rx=130, ry=40, swimmers=""):
    """The meadow pond: the pool, with a grassy rim, reeds and a lily pad. Like
    pool() it draws its own swimmers - anchor them at waterline(y)."""
    reeds = "".join(f'<path d="M{x+dx:.0f},{y-ry*.2:.0f} q{lean},-26 {lean*1.6:.0f},-44" stroke="#4A8F44" stroke-width="3" '
                    f'fill="none" stroke-linecap="round"/>'
                    f'<rect x="{x+dx+lean*1.2-3:.0f}" y="{y-ry*.2-40:.0f}" width="6" height="14" rx="3" fill="#8A5A2E"/>'
                    for dx, lean in ((-rx*.94, -4), (-rx*.86, 3), (rx*.9, 4)))
    return (reeds + pool(uid, x, y, rx, ry, swimmers=swimmers, rim="#7DBE6E")
            + f'<ellipse cx="{x+rx*.5:.0f}" cy="{y+ry*.32:.0f}" rx="14" ry="5" fill="#6BAF5E"/>'
            f'<circle cx="{x+rx*.5+4:.0f}" cy="{y+ry*.32-3:.0f}" r="3" fill="#FF9BAE"/>')


def bee(x, y, s=1.0, path=None):
    """A small bee. `path` is a list of points for her loopy dotted flight."""
    out = flight(path, "#C8A030") if path else ''
    return out + (f'<ellipse cx="{x-3*s:.1f}" cy="{y-8*s:.1f}" rx="{6*s:.1f}" ry="{4*s:.1f}" fill="#EAF8FF" stroke="#B8D0DC" stroke-width="1" opacity=".9"/>'
                  f'<ellipse cx="{x+4*s:.1f}" cy="{y-9*s:.1f}" rx="{6*s:.1f}" ry="{4*s:.1f}" fill="#EAF8FF" stroke="#B8D0DC" stroke-width="1" opacity=".9"/>'
                  f'<ellipse cx="{x}" cy="{y}" rx="{10*s:.1f}" ry="{7*s:.1f}" fill="#FFD166" stroke="#3A2A20" stroke-width="1.2"/>'
                  f'<path d="M{x-3*s:.1f},{y-6.5*s:.1f} v{13*s:.1f} M{x+3*s:.1f},{y-6.5*s:.1f} v{13*s:.1f}" stroke="#3A2A20" stroke-width="{2.4*s:.1f}"/>'
                  f'<circle cx="{x+7*s:.1f}" cy="{y-2*s:.1f}" r="{1.4*s:.1f}" fill="#3A2A20"/>')


def _checked(uid, d, box):
    """Red-and-white picnic check filling the path `d`; `box` bounds it."""
    x0, y0, x1, y1 = box
    stripes = ("".join(f'<rect x="{x0+i:.0f}" y="{y0}" width="9" height="{y1-y0}" fill="{CHECK}" opacity=".55"/>'
                       for i in range(0, int(x1-x0), 20))
               + "".join(f'<rect x="{x0}" y="{y0+i:.0f}" width="{x1-x0}" height="9" fill="{CHECK}" opacity=".55"/>'
                         for i in range(0, int(y1-y0), 20)))
    return (f'<defs><clipPath id="ck-{uid}"><path d="{d}"/></clipPath></defs>'
            f'<path d="{d}" fill="#FFFDF6"/>'
            f'<g clip-path="url(#ck-{uid})">{stripes}</g>'
            f'<path d="{d}" fill="none" stroke="#E0484A" stroke-width="1.6" stroke-linejoin="round"/>')


def picnic(uid, x, y, w=200, h=46):
    """A checked picnic blanket laid on the grass, `x, y` its middle."""
    d = (f'M{x-w/2+20:.0f},{y-h/2:.0f} L{x+w/2-14:.0f},{y-h/2-2:.0f} L{x+w/2+8:.0f},{y+h/2:.0f} '
         f'L{x-w/2-6:.0f},{y+h/2+2:.0f} Z')
    return _checked(uid, d, (x-w/2-10, y-h/2-4, x+w/2+10, y+h/2+4))


def draped(uid, x, y, w=70, h=74):
    """The picnic blanket thrown over someone's head, `x, y` the crown, hanging down
    with a ragged hem."""
    d = (f'M{x-w*.36:.0f},{y+6} Q{x:.0f},{y-26} {x+w*.36:.0f},{y+6} '
         f'Q{x+w*.56:.0f},{y+h*.6:.0f} {x+w*.5:.0f},{y+h:.0f} l-12,-8 l-12,8 l-12,-8 l-12,8 l-12,-8 '
         f'L{x-w*.5:.0f},{y+h:.0f} Q{x-w*.56:.0f},{y+h*.6:.0f} {x-w*.36:.0f},{y+6} Z')
    return _checked(uid, d, (x-w*.6, y-30, x+w*.6, y+h+10))


def teapot(x, y, s=1.0, lid=0, peek=None, rider=""):
    """The picnic teapot, `y` the ground under it. `rider` sits INSIDE it: drawn
    first, so the pot covers everything below the rim. `lid` lifts the lid by that
    much; `peek` is a pair of eyes looking out under a lifted lid."""
    rim = y - 62*s
    out = [rider,
           f'<path d="M{x-34*s:.0f},{y-34*s:.0f} q{-30*s:.0f},{-4*s:.0f} {-40*s:.0f},{-32*s:.0f}" stroke="#4AA8C8" stroke-width="{9*s:.1f}" '
           f'fill="none" stroke-linecap="round"/>',
           f'<path d="M{x+36*s:.0f},{y-46*s:.0f} q{26*s:.0f},{2*s:.0f} {6*s:.0f},{30*s:.0f}" stroke="#4AA8C8" stroke-width="{7*s:.1f}" fill="none"/>',
           f'<path d="M{x-40*s:.0f},{rim:.0f} Q{x-50*s:.0f},{y-6*s:.0f} {x:.0f},{y:.0f} Q{x+50*s:.0f},{y-6*s:.0f} {x+40*s:.0f},{rim:.0f} Z" '
           f'fill="#74C8E4" stroke="#4AA8C8" stroke-width="2"/>',
           f'<ellipse cx="{x}" cy="{rim:.0f}" rx="{40*s:.0f}" ry="{5*s:.0f}" fill="#5AB6D6" stroke="#4AA8C8" stroke-width="1.5"/>']
    out += [f'<circle cx="{x+dx*s:.0f}" cy="{y+dy*s:.0f}" r="{4*s:.1f}" fill="#FFFDF6" opacity=".85"/>'
            for dx, dy in ((-18, -36), (0, -22), (18, -36), (-26, -18), (26, -18))]
    ly = rim - lid
    out.append(f'<path d="M{x-30*s:.0f},{ly:.0f} Q{x:.0f},{ly-22*s:.0f} {x+30*s:.0f},{ly:.0f} Z" fill="#74C8E4" stroke="#4AA8C8" stroke-width="2"/>'
               f'<circle cx="{x}" cy="{ly-17*s:.0f}" r="{5*s:.1f}" fill="#FFD166" stroke="#D8A21F" stroke-width="1.2"/>')
    if peek:
        out.append("".join(f'<circle cx="{x+dx*s:.0f}" cy="{rim-lid*.5:.0f}" r="{4*s:.1f}" fill="#fff" stroke="{INK}" stroke-width="1"/>'
                           f'<circle cx="{x+(dx+peek)*s:.0f}" cy="{rim-lid*.5:.0f}" r="{2.6*s:.1f}" fill="{INK}"/>' for dx in (-7, 7)))
    return "".join(out)


def flowerpot(x, y, s=1.0, rider="", flower=True):
    """A big terracotta flowerpot, `y` the ground. Its rider is drawn first, so the
    pot hides everything below the rim."""
    top = y - 70*s
    f = ''
    if flower:
        f = (f'<path d="M{x+24*s:.0f},{top:.0f} q{6*s:.0f},{-26*s:.0f} {14*s:.0f},{-40*s:.0f}" stroke="#4A8F44" stroke-width="3" fill="none"/>'
             + "".join(f'<circle cx="{x+38*s+dx:.0f}" cy="{top-42*s+dy:.0f}" r="{6*s:.1f}" fill="#FF9BAE"/>'
                       for dx, dy in ((-6, 0), (6, 0), (0, -6), (0, 6)))
             + f'<circle cx="{x+38*s:.0f}" cy="{top-42*s:.0f}" r="{4*s:.1f}" fill="#FFD166"/>')
    return (f + rider
            + f'<path d="M{x-40*s:.0f},{top+10*s:.0f} L{x-30*s:.0f},{y:.0f} L{x+30*s:.0f},{y:.0f} L{x+40*s:.0f},{top+10*s:.0f} Z" '
              f'fill="#E08A5A" stroke="#B8643A" stroke-width="2"/>'
            + f'<rect x="{x-46*s:.0f}" y="{top:.0f}" width="{92*s:.0f}" height="{16*s:.0f}" rx="4" fill="#E8996A" stroke="#B8643A" stroke-width="2"/>'
            + f'<path d="M{x-20*s:.0f},{top+30*s:.0f} q{6*s:.0f},{4*s:.0f} {12*s:.0f},0" stroke="#FFFFFF" stroke-width="3" fill="none" opacity=".4" stroke-linecap="round"/>')


def log(x, y, w=210, r=36, inside=""):
    """A hollow log lying on the grass, its open end facing left. `x` is the open
    end, `y` the ground. `inside` is drawn into the dark hole, so whatever pokes
    out of the log sits in the mouth of it."""
    cy = y - r
    return (f'<ellipse cx="{x+w/2:.0f}" cy="{y-2}" rx="{w*.56:.0f}" ry="9" fill="#4A6B3A" opacity=".16"/>'
            f'<path d="M{x},{cy-r} L{x+w},{cy-r+4} A{r*.42:.0f},{r-4} 0 0 1 {x+w},{cy+r-4} L{x},{cy+r} Z" fill="{BARK}" stroke="{BARK_DK}" stroke-width="2"/>'
            + "".join(f'<path d="M{x+dx:.0f},{cy+dy:.0f} h{ln}" stroke="{BARK_DK}" stroke-width="2" stroke-linecap="round" opacity=".6"/>'
                      for dx, dy, ln in ((40, -18, 50), (110, -4, 70), (60, 14, 40), (150, 20, 30)))
            + f'<ellipse cx="{x}" cy="{cy}" rx="{r*.46:.0f}" ry="{r}" fill="#E8C48A" stroke="{BARK_DK}" stroke-width="2"/>'
            f'<ellipse cx="{x}" cy="{cy}" rx="{r*.34:.0f}" ry="{r*.78:.0f}" fill="#3A2412"/>'
            + inside
            + f'<path d="M{x+18},{cy-r+14} q8,-14 4,-26" stroke="#4A8F44" stroke-width="3" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="{x+28}" cy="{cy-r+2}" rx="8" ry="4" fill="{LEAF}" transform="rotate(-30 {x+28} {cy-r+2})"/>')


def sunhat(x, y, s=1.0, rot=0):
    """Giraffe's straw sunhat for her day off, `x, y` the middle of the brim."""
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<ellipse cx="{x}" cy="{y}" rx="{30*s:.0f}" ry="{7*s:.0f}" fill="#F4D58A" stroke="#C8A050" stroke-width="1.5"/>'
            f'<path d="M{x-16*s:.0f},{y-2} Q{x-14*s:.0f},{y-22*s:.0f} {x:.0f},{y-22*s:.0f} Q{x+14*s:.0f},{y-22*s:.0f} {x+16*s:.0f},{y-2} Z" '
            f'fill="#F4D58A" stroke="#C8A050" stroke-width="1.5"/>'
            f'<path d="M{x-15*s:.0f},{y-7*s:.0f} Q{x:.0f},{y-4*s:.0f} {x+15*s:.0f},{y-7*s:.0f}" stroke="#FF6B6B" stroke-width="{4*s:.1f}" fill="none"/>'
            f'<circle cx="{x+12*s:.0f}" cy="{y-10*s:.0f}" r="{4*s:.1f}" fill="#FFD166"/></g>')


def squeaks(pts, color="#C77DFF"):
    """Little 'squeak' words drifting up from somewhere hidden."""
    return "".join(f'<text x="{x}" y="{y}" font-size="{f}" fill="{color}" text-anchor="middle" '
                   f'font-family="Fredoka One, sans-serif" opacity=".9">squeak</text>' for x, y, f in pts)


def earwaves(x, y, s=1.0, side=1):
    """Sound arcs curving into a listening ear."""
    return "".join(f'<path d="M{x+side*(14+i*12)*s:.0f},{y-(10+i*7)*s:.0f} q{side*8*s:.0f},{(10+i*7)*s:.0f} 0,{(20+i*14)*s:.0f}" '
                   f'stroke="#C77DFF" stroke-width="2.4" fill="none" stroke-linecap="round" opacity="{.9-i*.2:.1f}"/>'
                   for i in range(3))


# ---------------------------------------------------------------- story 09 props
# Story 09 is Rabbit learning to ride. The bike is drawn side-on, facing right, and
# owns its rider like the car does - the rider goes between the frame and the
# legs, so their feet land on the pedals instead of floating beside them.
BIKE, BIKE_DK = "#FF6B6B", "#C0484A"


def bike_seat(x, y, s=1.0):
    """Where a rider's bottom goes on bike(x, y, s)."""
    return x - 20*s, y - 70*s


def bike_bar(x, y, s=1.0):
    """The handlebar grip of bike(x, y, s) - where the paws go."""
    return x + 30*s, y - 88*s


def bike_pedals(x, y, s=1.0):
    """The near and far pedals of bike(x, y, s)."""
    return (x + 6*s, y - 14*s), (x - 12*s, y - 34*s)


def wheel(x, y, r, spin=False):
    out = (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="none" stroke="#3A4250" stroke-width="{max(3, r*.2):.1f}"/>'
           f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r*.86:.1f}" fill="#EAF2F6" opacity=".35"/>'
           f'<path d="M{x-r*.8:.1f},{y:.0f} h{r*1.6:.1f} M{x:.0f},{y-r*.8:.1f} v{r*1.6:.1f} '
           f'M{x-r*.56:.1f},{y-r*.56:.1f} l{r*1.12:.1f},{r*1.12:.1f} M{x+r*.56:.1f},{y-r*.56:.1f} l{-r*1.12:.1f},{r*1.12:.1f}" '
           f'stroke="#9AA6AE" stroke-width="1.2"/>'
           f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{max(2.5, r*.14):.1f}" fill="#9AA6AE"/>')
    if spin:
        out += (f'<path d="M{x-r-6:.0f},{y-r*.4:.0f} a{r+6:.0f},{r+6:.0f} 0 0 1 {r*.8:.0f},{-r*.8:.0f}" stroke="#8FA8C0" '
                f'stroke-width="2.4" fill="none" stroke-linecap="round"/>')
    return out


def bike(x, y, s=1.0, color=BIKE, line=BIKE_DK, rider="", legs="", training=False, flat=False, spin=False):
    """Rabbit's bike, side-on facing right; `x` is the pedals, `y` the ground.

    `rider` is drawn over the frame and `legs` over the rider, so a rider's feet sit
    on the pedals. `training` adds the two little back wheels; `flat` is the bike
    after Elephant sat on it - wheels squashed to ovals, frame folded flat."""
    if flat:
        return (f'<ellipse cx="{x-52*s:.0f}" cy="{y-9*s:.0f}" rx="{32*s:.0f}" ry="{9*s:.0f}" fill="none" stroke="#3A4250" stroke-width="5"/>'
                f'<ellipse cx="{x+54*s:.0f}" cy="{y-9*s:.0f}" rx="{32*s:.0f}" ry="{9*s:.0f}" fill="none" stroke="#3A4250" stroke-width="5"/>'
                f'<path d="M{x-80*s:.0f},{y-16*s:.0f} l{30*s:.0f},{-8*s:.0f} l{26*s:.0f},{8*s:.0f} l{30*s:.0f},{-8*s:.0f} l{28*s:.0f},{8*s:.0f} '
                f'l{30*s:.0f},{-6*s:.0f}" stroke="{color}" stroke-width="{6*s:.1f}" fill="none" stroke-linejoin="round" stroke-linecap="round"/>'
                f'<path d="M{x+68*s:.0f},{y-22*s:.0f} l{20*s:.0f},{-12*s:.0f}" stroke="#5E6870" stroke-width="{5*s:.1f}" stroke-linecap="round"/>'
                f'<ellipse cx="{x-40*s:.0f}" cy="{y-24*s:.0f}" rx="{14*s:.0f}" ry="{4*s:.0f}" fill="#3A4250"/>')
    r = 26*s
    rh, fh = (x - 48*s, y - r), (x + 50*s, y - r)
    bb, st, ht = (x, y - 24*s), (x - 18*s, y - 64*s), (x + 36*s, y - 66*s)
    gx, gy = bike_bar(x, y, s)
    frame = (f'M{rh[0]:.0f},{rh[1]:.0f} L{bb[0]:.0f},{bb[1]:.0f} L{st[0]:.0f},{st[1]:.0f} Z '
             f'M{st[0]:.0f},{st[1]:.0f} L{ht[0]:.0f},{ht[1]:.0f} L{bb[0]:.0f},{bb[1]:.0f} '
             f'M{ht[0]:.0f},{ht[1]:.0f} L{fh[0]:.0f},{fh[1]:.0f}')
    out = [wheel(*rh, r, spin), wheel(*fh, r, spin)]
    if training:
        out += [f'<path d="M{rh[0]:.0f},{rh[1]:.0f} L{rh[0]-14*s:.0f},{y-10*s:.0f}" stroke="#9AA6AE" stroke-width="{3*s:.1f}"/>',
                wheel(rh[0] - 14*s, y - 10*s, 10*s)]
    out += [f'<path d="{frame}" stroke="{line}" stroke-width="{7*s:.1f}" fill="none" stroke-linejoin="round" stroke-linecap="round"/>',
            f'<path d="{frame}" stroke="{color}" stroke-width="{4.6*s:.1f}" fill="none" stroke-linejoin="round" stroke-linecap="round"/>',
            f'<path d="M{st[0]:.0f},{st[1]:.0f} L{x-21*s:.0f},{y-70*s:.0f}" stroke="#9AA6AE" stroke-width="{3.4*s:.1f}"/>',
            f'<path d="M{ht[0]:.0f},{ht[1]:.0f} L{ht[0]-2*s:.0f},{gy+4*s:.0f} Q{ht[0]-2*s:.0f},{gy:.0f} {gx:.0f},{gy:.0f}" '
            f'stroke="#5E6870" stroke-width="{4*s:.1f}" fill="none" stroke-linecap="round"/>',
            f'<circle cx="{ht[0]+4*s:.0f}" cy="{gy+8*s:.0f}" r="{4.5*s:.1f}" fill="#FFD166" stroke="#D8A21F" stroke-width="1.2"/>',
            f'<circle cx="{bb[0]:.0f}" cy="{bb[1]:.0f}" r="{7*s:.1f}" fill="#9AA6AE" stroke="#6E7880" stroke-width="1.2"/>',
            f'<path d="M{x+6*s:.0f},{y-14*s:.0f} L{x-12*s:.0f},{y-34*s:.0f}" stroke="#6E7880" stroke-width="{3*s:.1f}" stroke-linecap="round"/>',
            rider,
            f'<ellipse cx="{x-20*s:.0f}" cy="{y-71*s:.0f}" rx="{14*s:.0f}" ry="{4.5*s:.0f}" fill="#3A4250"/>' if not rider else '',
            legs]
    return "".join(out)


def toy_wheel(x, y, r=10, rot=0):
    """A training wheel, off the bike: a little wheel on its bent arm."""
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<path d="M{x},{y} l{-r*.4:.0f},{-r*1.8:.0f} l{r*1.4:.0f},{-r*.4:.0f}" stroke="#9AA6AE" stroke-width="3" fill="none" '
            f'stroke-linecap="round" stroke-linejoin="round"/>' + wheel(x, y, r) + '</g>')


def helmet(x, y, s=1.0, rot=0, color="#74C8E4", line="#3C90AE"):
    """A bike helmet, `x, y` the middle of its rim."""
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<path d="M{x-31*s:.0f},{y} Q{x-30*s:.0f},{y-30*s:.0f} {x:.0f},{y-31*s:.0f} Q{x+30*s:.0f},{y-30*s:.0f} {x+31*s:.0f},{y} Z" '
            f'fill="{color}" stroke="{line}" stroke-width="2"/>'
            f'<path d="M{x-12*s:.0f},{y-27*s:.0f} q{2*s:.0f},{12*s:.0f} 0,{24*s:.0f} M{x+12*s:.0f},{y-27*s:.0f} q{-2*s:.0f},{12*s:.0f} 0,{24*s:.0f}" '
            f'stroke="#FFFFFF" stroke-width="{4*s:.1f}" fill="none" opacity=".7"/>'
            f'<rect x="{x-33*s:.0f}" y="{y-4*s:.0f}" width="{66*s:.0f}" height="{6*s:.0f}" rx="3" fill="{line}"/></g>')


def hedge(x0, x1, y, h=96, fallen=False):
    """A long garden hedge, `y` the ground. `fallen` is the hedge after Elephant
    rode into it: flattened over on its back, leaves everywhere."""
    w = x1 - x0
    if fallen:
        top = y - 52
        out = (f'<path d="M{x0},{y} L{x0+10},{top} ' + " ".join(f'Q{x0+10+(i+.5)*(w-20)/7:.0f},{top-22} {x0+10+(i+1)*(w-20)/7:.0f},{top}' for i in range(7))
               + f' L{x1},{y} Z" fill="{LEAF}" stroke="{LEAF_DK}" stroke-width="2"/>')
        out += "".join(f'<path d="M{x0+fx*w:.0f},{y-fy*36:.0f} q6,-6 12,0" stroke="{LEAF_DK}" stroke-width="2" fill="none" stroke-linecap="round" opacity=".6"/>'
                       for fx, fy in ((.15, .5), (.4, .8), (.64, .4), (.86, .7)))
        return out + leaves(tuple((x0+fx*w, y-fy, r) for fx, fy, r in ((.1, 80, -30), (.3, 120, 30), (.62, 104, -50), (.9, 74, 20), (.46, 150, 60))))
    bumps = " ".join(f'Q{x0+(i+.5)*w/8:.0f},{y-h-18} {x0+(i+1)*w/8:.0f},{y-h}' for i in range(8))
    return (f'<path d="M{x0},{y} L{x0},{y-h} {bumps} L{x1},{y} Z" fill="{LEAF}" stroke="{LEAF_DK}" stroke-width="2"/>'
            + "".join(f'<path d="M{x0+fx*w:.0f},{y-fy*h:.0f} q6,-6 12,0" stroke="{LEAF_DK}" stroke-width="2" fill="none" stroke-linecap="round" opacity=".6"/>'
                      for fx, fy in ((.12, .7), (.3, .4), (.5, .76), (.7, .5), (.88, .78), (.4, .18), (.8, .2)))
            + "".join(f'<circle cx="{x0+fx*w:.0f}" cy="{y-fy*h:.0f}" r="9" fill="{LEAF_LT}" opacity=".6"/>'
                      for fx, fy in ((.2, .9), (.6, .94), (.94, .9))))


MUD, MUD_DK = "#9A6A3E", "#7A4E2A"


def puddle(x, y, rx=90, ry=20):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{MUD}"/>'
            f'<ellipse cx="{x-rx*.2:.0f}" cy="{y-ry*.25:.0f}" rx="{rx*.5:.0f}" ry="{ry*.35:.0f}" fill="#B88A5A" opacity=".6"/>')


def mud_splash(x, y, s=1.0):
    """Brown drops thrown up out of a puddle."""
    import math as _m
    return "".join(f'<ellipse cx="{x + _m.cos(a)*60*s:.0f}" cy="{y - abs(_m.sin(a))*54*s:.0f}" rx="{6*s:.1f}" ry="{9*s:.1f}" fill="{MUD}" '
                   f'transform="rotate({_m.degrees(a)-90:.0f} {x + _m.cos(a)*60*s:.0f} {y - abs(_m.sin(a))*54*s:.0f})"/>'
                   for a in (_m.pi*i/8 for i in range(9)))


def splat(x, y, r=6, color=MUD):
    """A dollop of mud (or cake mix) stuck on someone."""
    return (f'<path d="M{x-r},{y} q{r*.2:.1f},{-r:.1f} {r:.1f},{-r*.9:.1f} q{r:.1f},{-r*.1:.1f} {r:.1f},{r*.8:.1f} '
            f'q{-r*.1:.1f},{r:.1f} {-r:.1f},{r*.9:.1f} q{-r:.1f},0 {-r:.1f},{-r*.8:.1f} Z" fill="{color}" opacity=".9"/>')


def butterfly(x, y, s=1.0, color="#C77DFF"):
    return (f'<ellipse cx="{x-7*s:.1f}" cy="{y-4*s:.1f}" rx="{8*s:.1f}" ry="{6*s:.1f}" fill="{color}" transform="rotate(-24 {x-7*s:.1f} {y-4*s:.1f})"/>'
            f'<ellipse cx="{x+7*s:.1f}" cy="{y-4*s:.1f}" rx="{8*s:.1f}" ry="{6*s:.1f}" fill="{color}" transform="rotate(24 {x+7*s:.1f} {y-4*s:.1f})"/>'
            f'<ellipse cx="{x-5*s:.1f}" cy="{y+5*s:.1f}" rx="{5*s:.1f}" ry="{4*s:.1f}" fill="#FF9BAE"/>'
            f'<ellipse cx="{x+5*s:.1f}" cy="{y+5*s:.1f}" rx="{5*s:.1f}" ry="{4*s:.1f}" fill="#FF9BAE"/>'
            f'<rect x="{x-1.5*s:.1f}" y="{y-8*s:.1f}" width="{3*s:.1f}" height="{16*s:.1f}" rx="1.5" fill="{INK}"/>'
            f'<path d="M{x},{y-8*s:.1f} l{-4*s:.1f},{-6*s:.1f} M{x},{y-8*s:.1f} l{4*s:.1f},{-6*s:.1f}" stroke="{INK}" stroke-width="1.2"/>')


def plaster(x, y, rot=-20, s=1.0):
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<rect x="{x-12*s:.0f}" y="{y-4.5*s:.1f}" width="{24*s:.0f}" height="{9*s:.0f}" rx="4" fill="#F4C9A0" stroke="#D8A878" stroke-width="1"/>'
            f'<rect x="{x-4*s:.0f}" y="{y-4.5*s:.1f}" width="{8*s:.0f}" height="{9*s:.0f}" fill="#E8B488"/></g>')


def toolbox(x, y, s=1.0):
    """`y` is the ground under it."""
    return (f'<path d="M{x-12*s:.0f},{y-30*s:.0f} v{-8*s:.0f} h{24*s:.0f} v{8*s:.0f}" stroke="#5E6870" stroke-width="{3*s:.1f}" fill="none"/>'
            f'<rect x="{x-30*s:.0f}" y="{y-30*s:.0f}" width="{60*s:.0f}" height="{30*s:.0f}" rx="4" fill="#FF6B6B" stroke="#C0484A" stroke-width="2"/>'
            f'<rect x="{x-30*s:.0f}" y="{y-20*s:.0f}" width="{60*s:.0f}" height="{4*s:.0f}" fill="#C0484A" opacity=".6"/>')


def spanner(x, y, s=1.0, rot=0):
    """`x, y` is the handle end."""
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<rect x="{x-3*s:.1f}" y="{y-30*s:.0f}" width="{6*s:.1f}" height="{30*s:.0f}" rx="3" fill="#9AA6AE" stroke="#6E7880" stroke-width="1"/>'
            f'<path d="M{x-8*s:.0f},{y-30*s:.0f} a{8*s:.0f},{8*s:.0f} 0 1 1 {16*s:.0f},0 l{-4*s:.0f},{-8*s:.0f} h{-8*s:.0f} Z" fill="#9AA6AE" stroke="#6E7880" stroke-width="1"/></g>')


def doctor_bag(x, y, s=1.0):
    """Dr. Squirrel's bag, `y` the ground under it."""
    return (f'<path d="M{x-9*s:.0f},{y-28*s:.0f} q{9*s:.0f},{-10*s:.0f} {18*s:.0f},0" stroke="#4E3320" stroke-width="{3*s:.1f}" fill="none"/>'
            f'<rect x="{x-20*s:.0f}" y="{y-28*s:.0f}" width="{40*s:.0f}" height="{28*s:.0f}" rx="6" fill="#6E4A2E"/>'
            f'<rect x="{x-3*s:.0f}" y="{y-21*s:.0f}" width="{6*s:.0f}" height="{14*s:.0f}" fill="#E8533F"/>'
            f'<rect x="{x-7*s:.0f}" y="{y-17*s:.0f}" width="{14*s:.0f}" height="{6*s:.0f}" fill="#E8533F"/>')


def duck(x, y, s=1.0):
    """A small yellow duck, side-on facing right, `x, y` under its middle."""
    return (f'<ellipse cx="{x}" cy="{y-9*s:.1f}" rx="{14*s:.1f}" ry="{9*s:.1f}" fill="#FFD166" stroke="#D8A21F" stroke-width="1.2"/>'
            f'<circle cx="{x+10*s:.1f}" cy="{y-20*s:.1f}" r="{7*s:.1f}" fill="#FFD166" stroke="#D8A21F" stroke-width="1.2"/>'
            f'<path d="M{x+16*s:.1f},{y-21*s:.1f} l{7*s:.1f},{2*s:.1f} l{-7*s:.1f},{3*s:.1f} Z" fill="#FF9B4A"/>'
            f'<circle cx="{x+12*s:.1f}" cy="{y-22*s:.1f}" r="{1.4*s:.1f}" fill="{INK}"/>'
            f'<path d="M{x-6*s:.1f},{y-10*s:.1f} q{6*s:.1f},{-6*s:.1f} {12*s:.1f},0" stroke="#D8A21F" stroke-width="1.2" fill="none"/>')


def sweat(x, y, s=1.0):
    """Puffing-and-panting drops flying off a forehead."""
    return "".join(f'<path d="M{x+dx*s:.0f},{y+dy*s:.0f} q{-4*s:.1f},{6*s:.1f} 0,{9*s:.1f} q{4*s:.1f},{-3*s:.1f} 0,{-9*s:.1f} Z" '
                   f'fill="#9BDCF0" stroke="#5AB6D6" stroke-width="1"/>' for dx, dy in ((0, 0), (12, -10), (-10, -6)))


# ---------------------------------------------------------------- story 10 props
# Story 10 is Elephant's cold. Every sneeze is a gust that blows something away, so
# the props are the things that blow: washing, a hat, a sheep's fleece.
SOCKS = ("#FF6B6B", "#74C8E4", "#FFD166", "#C77DFF")


def sock(x, y, s=1.0, rot=0, color="#FF6B6B"):
    """A sock, `x, y` the top of its cuff, toe pointing down and right."""
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<path d="M{x-7*s:.1f},{y:.1f} L{x-7*s:.1f},{y+22*s:.1f} Q{x-7*s:.1f},{y+32*s:.1f} {x+4*s:.1f},{y+32*s:.1f} '
            f'L{x+14*s:.1f},{y+32*s:.1f} Q{x+20*s:.1f},{y+26*s:.1f} {x+14*s:.1f},{y+21*s:.1f} L{x+7*s:.1f},{y+20*s:.1f} '
            f'L{x+7*s:.1f},{y:.1f} Z" fill="{color}" stroke="#00000033" stroke-width="1.3"/>'
            f'<rect x="{x-7*s:.1f}" y="{y:.1f}" width="{14*s:.1f}" height="{5*s:.1f}" fill="#FFFFFF" opacity=".7"/></g>')


def shirt(x, y, s=1.0, rot=0, color="#74C8E4"):
    """A little T-shirt, `x, y` the middle of its neckline."""
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<path d="M{x-8*s:.1f},{y:.1f} L{x-22*s:.1f},{y+4*s:.1f} L{x-30*s:.1f},{y+16*s:.1f} L{x-20*s:.1f},{y+21*s:.1f} '
            f'L{x-16*s:.1f},{y+16*s:.1f} L{x-16*s:.1f},{y+42*s:.1f} L{x+16*s:.1f},{y+42*s:.1f} L{x+16*s:.1f},{y+16*s:.1f} '
            f'L{x+20*s:.1f},{y+21*s:.1f} L{x+30*s:.1f},{y+16*s:.1f} L{x+22*s:.1f},{y+4*s:.1f} L{x+8*s:.1f},{y:.1f} '
            f'Q{x:.1f},{y+7*s:.1f} {x-8*s:.1f},{y:.1f} Z" fill="{color}" stroke="#00000033" stroke-width="1.3" stroke-linejoin="round"/>'
            f'<circle cx="{x:.1f}" cy="{y+24*s:.1f}" r="{5*s:.1f}" fill="#FFFFFF" opacity=".7"/></g>')


def bedsheet(x, y, w=110, h=70, rot=0, color="#FFFFFF"):
    """A flapping bedsheet, `x, y` the middle of its top edge."""
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<path d="M{x-w/2:.0f},{y} Q{x:.0f},{y-8} {x+w/2:.0f},{y} Q{x+w/2+8:.0f},{y+h/2:.0f} {x+w/2:.0f},{y+h} '
            f'Q{x+w/4:.0f},{y+h-10} {x:.0f},{y+h} Q{x-w/4:.0f},{y+h+10} {x-w/2:.0f},{y+h} Q{x-w/2-8:.0f},{y+h/2:.0f} {x-w/2:.0f},{y} Z" '
            f'fill="{color}" stroke="#C8D4DC" stroke-width="1.6"/>'
            f'<path d="M{x-w/2+8:.0f},{y+14} Q{x:.0f},{y+6} {x+w/2-8:.0f},{y+14}" stroke="#74C8E4" stroke-width="4" fill="none" opacity=".6"/></g>')


def washing_line(x0, x1, y, h=120, sag=18, items=()):
    """A washing line between two posts, `y` the ground. `items` hang from the line
    at fractions along it: (t, kind, color) with kind 'sock', 'shirt' or 'sheet'."""
    top = y - h
    rope = f'M{x0},{top} Q{(x0+x1)/2:.0f},{top+sag*2} {x1},{top}'
    out = ([f'<rect x="{px-4}" y="{top-8}" width="8" height="{h+8}" rx="2" fill="{WOOD_DK}"/>'
            f'<rect x="{px-14}" y="{top-10}" width="28" height="6" rx="2" fill="{WOOD_DK}"/>' for px in (x0, x1)]
           + [f'<path d="{rope}" stroke="#9AA6AE" stroke-width="2" fill="none"/>'])
    for t, kind, color in items:
        px = x0 + (x1 - x0)*t
        py = top + sag*2*2*t*(1 - t)       # point on the quadratic
        if kind == 'sock':
            out.append(sock(px, py, color=color))
        elif kind == 'shirt':
            out.append(shirt(px, py, color=color))
        else:
            out.append(bedsheet(px, py, w=90, h=64, color=color))
        out.append(f'<rect x="{px-2.5:.0f}" y="{py-6:.0f}" width="5" height="10" rx="1.5" fill="{WOOD}" stroke="{WOOD_DK}" stroke-width="1"/>')
    return "".join(out)


def sneeze(x, y, ang=0, s=1.0, n=5):
    """The blast out of a trunk tip at (x, y): streaming gust lines fanning out along
    `ang` degrees (0 = to the right), with a spray of droplets."""
    import math as _m
    out = []
    for i in range(n):
        a = _m.radians(ang + (i - (n-1)/2) * 11)
        l0, l1 = 14*s, (70 + (i % 2)*24)*s
        bx, by = -_m.sin(a)*8*s*(1 if i % 2 else -1), _m.cos(a)*8*s*(1 if i % 2 else -1)
        out.append(f'<path d="M{x+_m.cos(a)*l0:.0f},{y+_m.sin(a)*l0:.0f} Q{x+_m.cos(a)*(l0+l1)/2+bx:.0f},{y+_m.sin(a)*(l0+l1)/2+by:.0f} '
                   f'{x+_m.cos(a)*l1:.0f},{y+_m.sin(a)*l1:.0f}" stroke="#B9D4E2" stroke-width="{3.4*s:.1f}" fill="none" '
                   f'stroke-linecap="round" opacity=".85"/>')
    for i, (d, off) in enumerate(((30, -.3), (46, .25), (58, -.1), (40, .05), (66, .32), (24, .18))):
        a = _m.radians(ang) + off
        out.append(f'<circle cx="{x+_m.cos(a)*d*s:.0f}" cy="{y+_m.sin(a)*d*s:.0f}" r="{(2.4 + i % 3)*s:.1f}" fill="#CFEEFA" '
                   f'stroke="#9BCFE4" stroke-width="1"/>')
    return "".join(out)


def germ(x, y, s=1.0, color="#7DCB6A"):
    """One tiny germ: a wobbly green blob with little feelers and a cheeky face."""
    import math as _m
    feel = "".join(f'<path d="M{x+_m.cos(a)*9*s:.1f},{y+_m.sin(a)*9*s:.1f} l{_m.cos(a)*5*s:.1f},{_m.sin(a)*5*s:.1f}" '
                   f'stroke="{color}" stroke-width="{2*s:.1f}" stroke-linecap="round"/>'
                   f'<circle cx="{x+_m.cos(a)*15*s:.1f}" cy="{y+_m.sin(a)*15*s:.1f}" r="{1.8*s:.1f}" fill="{color}"/>'
                   for a in (_m.pi*i/4 for i in range(8)))
    return (feel + f'<circle cx="{x}" cy="{y}" r="{10*s:.1f}" fill="{color}" stroke="#4E9B44" stroke-width="1.2"/>'
            f'<circle cx="{x-3.5*s:.1f}" cy="{y-2*s:.1f}" r="{1.6*s:.1f}" fill="{INK}"/>'
            f'<circle cx="{x+3.5*s:.1f}" cy="{y-2*s:.1f}" r="{1.6*s:.1f}" fill="{INK}"/>'
            f'<path d="M{x-3.5*s:.1f},{y+3*s:.1f} q{3.5*s:.1f},{3*s:.1f} {7*s:.1f},0" stroke="{INK}" stroke-width="1.2" fill="none" stroke-linecap="round"/>')


def germs(pts, color="#7DCB6A"):
    return "".join(germ(x, y, s, color) for x, y, s in pts)


def specs(x, y, s=1.0, rot=0):
    """Round glasses, `x, y` the bridge."""
    return (f'<g transform="rotate({rot} {x} {y})">'
            + "".join(f'<circle cx="{x+sx*9*s:.1f}" cy="{y:.1f}" r="{7.5*s:.1f}" fill="#FFFFFF" fill-opacity=".25" '
                      f'stroke="#C08840" stroke-width="{2*s:.1f}"/>' for sx in (-1, 1))
            + f'<path d="M{x-2*s:.1f},{y-1*s:.1f} q{2*s:.1f},{-2*s:.1f} {4*s:.1f},0" stroke="#C08840" stroke-width="{2*s:.1f}" fill="none"/></g>')


def fleece_cloud(x, y, r=80, fill="#F6F2EA", line="#CFC6B2", swirl="#E4DCCB"):
    """Dr. Sheep's wool after a sneeze: blown up into one enormous cloud. `x, y` is
    the middle; draw it BEHIND her so her face still shows."""
    import math as _m
    ring = [(x + _m.cos(a)*r*.82, y + _m.sin(a)*r*.7) for a in (2*_m.pi*i/14 for i in range(14))]
    return (f'<ellipse cx="{x}" cy="{y}" rx="{r*.9:.0f}" ry="{r*.78:.0f}" fill="{fill}"/>'
            + "".join(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r*.3:.0f}" fill="{fill}" stroke="{line}" stroke-width="1.5"/>'
                      for cx, cy in ring)
            + f'<ellipse cx="{x}" cy="{y}" rx="{r*.86:.0f}" ry="{r*.72:.0f}" fill="{fill}"/>'
            + "".join(f'<circle cx="{x+dx*r:.0f}" cy="{y+dy*r:.0f}" r="{r*.1:.0f}" fill="none" stroke="{swirl}" stroke-width="2.2"/>'
                      for dx, dy in ((-.5, -.3), (.46, -.36), (-.6, .3), (.56, .26), (0, -.56))))


def sink(x, y, running=False):
    """A washbasin on a pedestal, `y` the floor. `running` turns the tap on."""
    out = (f'<rect x="{x-12}" y="{y-80}" width="24" height="80" rx="4" fill="#FFFFFF" stroke="#C8D4DC" stroke-width="1.6"/>'
           f'<path d="M{x-48},{y-100} L{x+48},{y-100} Q{x+46},{y-74} {x},{y-72} Q{x-46},{y-74} {x-48},{y-100} Z" '
           f'fill="#FFFFFF" stroke="#C8D4DC" stroke-width="1.8"/>'
           f'<ellipse cx="{x}" cy="{y-100}" rx="48" ry="7" fill="#E8F1F5" stroke="#C8D4DC" stroke-width="1.6"/>'
           f'<path d="M{x+30},{y-104} v-22 q0,-6 -6,-6 h-14 v8" stroke="#9AA6AE" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
           f'<circle cx="{x+30}" cy="{y-126}" r="5" fill="#FF6B6B"/>')
    if running:
        out += f'<path d="M{x+10},{y-120} q2,10 0,18" stroke="#9BDCF0" stroke-width="5" fill="none" stroke-linecap="round"/>'
    return out


def soap_bubbles(pts):
    """Soap bubbles: (x, y, r) each - a ring with a shine, nearly see-through."""
    return "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#EAF8FF" fill-opacity=".55" stroke="#9BCFE4" stroke-width="1.4"/>'
                   f'<path d="M{x-r*.5:.1f},{y-r*.2:.1f} q{r*.15:.1f},{-r*.4:.1f} {r*.5:.1f},{-r*.5:.1f}" stroke="#FFFFFF" '
                   f'stroke-width="{max(1.2, r*.18):.1f}" fill="none" stroke-linecap="round"/>' for x, y, r in pts)


def soup(x, y, s=1.0):
    """A bowl of warm soup with a spoon, `x, y` the middle of the rim."""
    return (f'<path d="M{x-22*s:.0f},{y} Q{x:.0f},{y+26*s:.0f} {x+22*s:.0f},{y} Z" fill="#FF9B4A" stroke="#D8743A" stroke-width="1.5"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="{22*s:.0f}" ry="{5*s:.0f}" fill="#FFC27A" stroke="#D8743A" stroke-width="1.5"/>'
            f'<path d="M{x+8*s:.0f},{y-1} l{12*s:.0f},{-18*s:.0f}" stroke="#9AA6AE" stroke-width="{3*s:.1f}" stroke-linecap="round"/>'
            + steam(x - 4*s, y - 8*s, s*.8, color="#E8D8C4"))


def basket(x, y, w=70, full=True):
    """A wicker laundry basket, `y` the ground (or the paw carrying it)."""
    out = ''
    if full:
        out = (shirt(x - w*.18, y - 52, s=.7, rot=-20, color="#FFD166")
               + sock(x + w*.2, y - 50, s=.8, rot=24, color="#C77DFF")
               + f'<ellipse cx="{x}" cy="{y-40}" rx="{w*.42:.0f}" ry="10" fill="#FFFFFF" stroke="#C8D4DC" stroke-width="1.4"/>')
    return (out
            + f'<path d="M{x-w/2:.0f},{y-42} L{x-w*.4:.0f},{y} L{x+w*.4:.0f},{y} L{x+w/2:.0f},{y-42} Z" fill="#E8C48A" stroke="#B98A56" stroke-width="2"/>'
            + "".join(f'<path d="M{x-w*.46:.0f},{y-dy} L{x+w*.46:.0f},{y-dy}" stroke="#B98A56" stroke-width="1.4" opacity=".7"/>'
                      for dy in (12, 24, 34))
            + f'<rect x="{x-w/2-3:.0f}" y="{y-46}" width="{w+6}" height="7" rx="3" fill="#D9AE7A" stroke="#B98A56" stroke-width="1.5"/>')


def magnifier(uid, x, y, r=38, inside="", rot=40):
    """A magnifying glass, `x, y` the middle of the lens. `inside` is drawn in the
    lens, clipped to it - so the germs only show where you look through it."""
    import math as _m
    a = _m.radians(rot)
    hx, hy = x + _m.cos(a)*(r+4), y + _m.sin(a)*(r+4)
    return (f'<path d="M{hx:.0f},{hy:.0f} l{_m.cos(a)*44:.0f},{_m.sin(a)*44:.0f}" stroke="#6E4A2E" stroke-width="11" stroke-linecap="round"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="#EAF8FF"/>'
            + f'<defs><clipPath id="lens-{uid}"><circle cx="{x}" cy="{y}" r="{r}"/></clipPath></defs>'
            f'<g clip-path="url(#lens-{uid})">{inside}</g>'
            + f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" fill-opacity=".12" stroke="#9AA6AE" stroke-width="6"/>'
            f'<path d="M{x-r*.6:.0f},{y-r*.3:.0f} q{r*.2:.0f},{-r*.4:.0f} {r*.6:.0f},{-r*.5:.0f}" stroke="#FFFFFF" stroke-width="4" fill="none" stroke-linecap="round" opacity=".8"/>')


def notes(pts, color="#C77DFF"):
    """Musical notes drifting up from a song: (x, y, size) each."""
    return "".join(f'<text x="{x}" y="{y}" font-size="{f}" fill="{color}" text-anchor="middle" '
                   f'font-family="Nunito, sans-serif" font-weight="700">{"&#9835;" if i % 2 else "&#9834;"}</text>'
                   for i, (x, y, f) in enumerate(pts))


# ---------------------------------------------------------------- story 11 props
# Story 11 is a birthday cake baked too fast, then baked properly. Batter is
# yellow, the cake is golden, the icing pink - and the kitchen is the burrow one.
BATTER, BATTER_DK = "#FFE08A", "#E8B84A"
SPONGE, SPONGE_DK = "#F0B860", "#C88A3A"
ICING, ICING_DK = "#FFB3C6", "#E88AA4"


def recipe(x, y, s=1.0, rot=0):
    """A recipe card, `x, y` its middle: a cake picture and a list of steps."""
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<rect x="{x-24*s:.0f}" y="{y-30*s:.0f}" width="{48*s:.0f}" height="{60*s:.0f}" rx="3" fill="#FFFDF6" stroke="#C8B48C" stroke-width="1.5"/>'
            f'<rect x="{x-12*s:.0f}" y="{y-24*s:.0f}" width="{24*s:.0f}" height="{12*s:.0f}" rx="2" fill="{ICING}"/>'
            f'<rect x="{x-12*s:.0f}" y="{y-14*s:.0f}" width="{24*s:.0f}" height="{6*s:.0f}" fill="{SPONGE}"/>'
            + "".join(f'<circle cx="{x-16*s:.0f}" cy="{y+(2+i*8)*s:.0f}" r="{1.6*s:.1f}" fill="#9A8E78"/>'
                      f'<path d="M{x-11*s:.0f},{y+(2+i*8)*s:.0f} h{(24-i*4)*s:.0f}" stroke="#B9AE98" stroke-width="{2*s:.1f}" stroke-linecap="round"/>'
                      for i in range(4))
            + '</g>')


def flour_bag(x, y, s=1.0, rot=0, empty=False):
    """A paper bag of flour, `x, y` the middle of its base. `empty` scrunches it."""
    h = 34 if empty else 50
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<path d="M{x-20*s:.0f},{y} L{x-18*s:.0f},{y-h*s:.0f} L{x+18*s:.0f},{y-h*s:.0f} L{x+20*s:.0f},{y} Z" fill="#F4EAD8" stroke="#C8B48C" stroke-width="1.6"/>'
            f'<path d="M{x-18*s:.0f},{y-h*s:.0f} l{6*s:.0f},{-6*s:.0f} l{6*s:.0f},{6*s:.0f} l{6*s:.0f},{-6*s:.0f} l{6*s:.0f},{6*s:.0f} l{6*s:.0f},{-6*s:.0f} l{6*s:.0f},{6*s:.0f}" '
            f'stroke="#C8B48C" stroke-width="1.6" fill="#F4EAD8"/>'
            f'<rect x="{x-14*s:.0f}" y="{y-(h-12)*s:.0f}" width="{28*s:.0f}" height="{14*s:.0f}" rx="2" fill="#74C8E4"/>'
            f'<text x="{x}" y="{y-(h-22.5)*s:.0f}" font-size="{7.5*s:.1f}" text-anchor="middle" fill="#FFFFFF" '
            f'font-family="Nunito, sans-serif" font-weight="700">FLOUR</text></g>')


def egg(x, y, s=1.0, rot=0, cracked=False):
    out = f'<ellipse cx="{x}" cy="{y}" rx="{8*s:.1f}" ry="{10.5*s:.1f}" fill="#FFF8EE" stroke="#D8C8A8" stroke-width="1.3" transform="rotate({rot} {x} {y})"/>'
    if cracked:
        out += (f'<path d="M{x-8*s:.1f},{y-1*s:.1f} l{3*s:.1f},{-3*s:.1f} l{3*s:.1f},{3*s:.1f} l{3*s:.1f},{-3*s:.1f} l{3*s:.1f},{3*s:.1f} l{3*s:.1f},{-3*s:.1f}" '
                f'stroke="#B9A888" stroke-width="1.3" fill="none" transform="rotate({rot} {x} {y})"/>')
    return out


def eggshell(x, y, s=1.0, rot=0):
    """Half a broken shell, zig-zag edge up."""
    return (f'<path d="M{x-8*s:.1f},{y:.1f} l{3*s:.1f},{-4*s:.1f} l{3*s:.1f},{3*s:.1f} l{2*s:.1f},{-4*s:.1f} l{3*s:.1f},{3*s:.1f} l{5*s:.1f},{-2*s:.1f} '
            f'Q{x+8*s:.1f},{y+10*s:.1f} {x:.1f},{y+10*s:.1f} Q{x-8*s:.1f},{y+10*s:.1f} {x-8*s:.1f},{y:.1f} Z" fill="#FFF8EE" '
            f'stroke="#D8C8A8" stroke-width="1.2" transform="rotate({rot} {x} {y})"/>')


def egg_splat(x, y, s=1.0):
    """A cracked egg landed on someone's head: white running down, yolk on top,
    and a drip or two. `x, y` is where it landed."""
    return (f'<path d="M{x-24*s:.0f},{y+2*s:.0f} Q{x-20*s:.0f},{y-10*s:.0f} {x:.0f},{y-10*s:.0f} Q{x+22*s:.0f},{y-10*s:.0f} {x+24*s:.0f},{y+4*s:.0f} '
            f'q{-2*s:.0f},{8*s:.0f} {-6*s:.0f},{2*s:.0f} q{-2*s:.0f},{14*s:.0f} {-7*s:.0f},{2*s:.0f} q{-6*s:.0f},{4*s:.0f} {-12*s:.0f},0 '
            f'q{-4*s:.0f},{18*s:.0f} {-8*s:.0f},{0*s:.0f} q{-4*s:.0f},{4*s:.0f} {-15*s:.0f},{0:.0f} Z" fill="#FFFFFF" fill-opacity=".85" stroke="#E4DCCB" stroke-width="1.2"/>'
            f'<circle cx="{x+2*s:.0f}" cy="{y-3*s:.0f}" r="{8*s:.1f}" fill="#FFC23A" stroke="#E8A21F" stroke-width="1.2"/>'
            f'<circle cx="{x-1*s:.0f}" cy="{y-6*s:.0f}" r="{2.4*s:.1f}" fill="#FFFFFF" opacity=".7"/>')


def mixing_bowl(x, y, w=90, batter=True, spoon=False):
    """A big mixing bowl, `y` the table top it stands on."""
    rim = y - w*.5
    out = ''
    if batter:
        out += f'<ellipse cx="{x}" cy="{rim+3:.0f}" rx="{w*.44:.0f}" ry="{w*.08:.0f}" fill="{BATTER}" stroke="{BATTER_DK}" stroke-width="1.2"/>'
    if spoon:
        out += f'<path d="M{x+w*.1:.0f},{rim:.0f} l{w*.22:.0f},{-w*.4:.0f}" stroke="#D9AE7A" stroke-width="5" stroke-linecap="round"/>'
    return (f'<ellipse cx="{x}" cy="{rim:.0f}" rx="{w/2:.0f}" ry="{w*.11:.0f}" fill="#E8D6B4" stroke="#7FB8CF" stroke-width="2"/>'
            + out
            + f'<path d="M{x-w/2:.0f},{rim:.0f} Q{x-w/2+4:.0f},{y-4} {x:.0f},{y-2} Q{x+w/2-4:.0f},{y-4} {x+w/2:.0f},{rim:.0f} '
              f'Q{x:.0f},{rim+w*.16:.0f} {x-w/2:.0f},{rim:.0f} Z" fill="#9BDCF0" stroke="#5AB6D6" stroke-width="2"/>'
            + f'<path d="M{x-w*.3:.0f},{rim+w*.2:.0f} q{w*.06:.0f},{w*.12:.0f} {w*.2:.0f},{w*.16:.0f}" stroke="#FFFFFF" stroke-width="3" fill="none" opacity=".6" stroke-linecap="round"/>'
            + f'<rect x="{x-w*.18:.0f}" y="{y-5}" width="{w*.36:.0f}" height="5" rx="2" fill="#5AB6D6"/>')


def mixer(x, y, s=1.0, rot=0, whirl=False):
    """A hand mixer, `x, y` the tips of its beaters. `whirl` is SUPER FAST."""
    out = (f'<g transform="rotate({rot} {x} {y})">'
           + "".join(f'<path d="M{x+dx*s:.0f},{y-30*s:.0f} v{22*s:.0f} q{-4*s:.0f},{8*s:.0f} 0,{8*s:.0f} q{4*s:.0f},0 0,{-8*s:.0f}" '
                     f'stroke="#9AA6AE" stroke-width="{2.4*s:.1f}" fill="none"/>' for dx in (-6, 6))
           + f'<path d="M{x-20*s:.0f},{y-30*s:.0f} Q{x-22*s:.0f},{y-54*s:.0f} {x:.0f},{y-54*s:.0f} L{x+26*s:.0f},{y-54*s:.0f} '
             f'Q{x+34*s:.0f},{y-54*s:.0f} {x+34*s:.0f},{y-44*s:.0f} L{x+30*s:.0f},{y-30*s:.0f} Z" fill="#FF6B6B" stroke="#C0484A" stroke-width="1.6"/>'
           + f'<path d="M{x+4*s:.0f},{y-54*s:.0f} q{6*s:.0f},{-18*s:.0f} {24*s:.0f},{-6*s:.0f} l{-2*s:.0f},{6*s:.0f}" stroke="#C0484A" stroke-width="{6*s:.1f}" fill="none" stroke-linecap="round"/>'
           + f'<circle cx="{x+20*s:.0f}" cy="{y-42*s:.0f}" r="{3.4*s:.1f}" fill="#FFD166"/></g>')
    if whirl:
        out += "".join(f'<path d="M{x-(22+i*12)*s:.0f},{y-(6+i*6)*s:.0f} a{(22+i*12)*s:.0f},{(10+i*5)*s:.0f} 0 1 0 {2*(22+i*12)*s:.0f},0" '
                       f'stroke="#C8D4DC" stroke-width="2.4" fill="none" stroke-linecap="round" opacity="{.85-i*.2:.2f}"/>' for i in range(3))
    return out


def oven(x, y, w=124, h=112, door='shut', inside="", light=False):
    """A little oven standing on the floor at `y`. `inside` is drawn in the oven's
    window (or its open mouth, when `door='open'`); `light` glows it warm."""
    top = y - h
    wx, wy, ww, wh = x - w*.36, top + 34, w*.72, h*.44
    glow = "#FFE9A8" if light else "#3A3030"
    out = (f'<rect x="{x-w/2:.0f}" y="{top:.0f}" width="{w}" height="{h}" rx="8" fill="#BFE6D6" stroke="#7FB89E" stroke-width="2"/>'
           + "".join(f'<circle cx="{x+dx*w:.0f}" cy="{top+14:.0f}" r="6" fill="#9AA6AE" stroke="#6E7880" stroke-width="1.2"/>'
                     for dx in (-.3, -.1, .1))
           + f'<circle cx="{x+w*.32:.0f}" cy="{top+14:.0f}" r="4" fill="{"#FF6B6B" if light else "#C8D0D6"}"/>')
    if door == 'open':
        out += (f'<rect x="{wx:.0f}" y="{wy:.0f}" width="{ww:.0f}" height="{wh:.0f}" rx="5" fill="#3A3030"/>'
                + clip(f'ov{x}{y}', wx, wy, ww, wh, inside)
                + f'<path d="M{x-w/2:.0f},{y-8} L{x-w/2-6:.0f},{y+12} L{x+w/2+6:.0f},{y+12} L{x+w/2:.0f},{y-8} Z" fill="#A8DCC6" stroke="#7FB89E" stroke-width="2"/>'
                + f'<rect x="{x-w*.3:.0f}" y="{y+2}" width="{w*.6:.0f}" height="5" rx="2" fill="#6E7880"/>')
    else:
        out += (f'<rect x="{wx:.0f}" y="{wy:.0f}" width="{ww:.0f}" height="{wh:.0f}" rx="5" fill="{glow}"/>'
                + clip(f'ov{x}{y}', wx, wy, ww, wh, inside)
                + f'<rect x="{wx:.0f}" y="{wy:.0f}" width="{ww:.0f}" height="{wh:.0f}" rx="5" fill="#FFFFFF" fill-opacity=".1" stroke="#6E7880" stroke-width="3"/>'
                + f'<rect x="{x-w*.3:.0f}" y="{top+24:.0f}" width="{w*.6:.0f}" height="6" rx="3" fill="#6E7880"/>')
    return out


def cake(x, y, w=110, kind='tall', candles=0):
    """A cake on a plate, `y` the table top. `tall` is three iced layers; `flat` is
    the sad pancake one; `tin` is a cake baking in its tin, risen to `w*.3`."""
    out = f'<ellipse cx="{x}" cy="{y-3}" rx="{w*.62:.0f}" ry="7" fill="#FFFFFF" stroke="#C8D4DC" stroke-width="1.5"/>'
    if kind == 'flat':
        return (out + f'<ellipse cx="{x}" cy="{y-8}" rx="{w*.52:.0f}" ry="9" fill="{SPONGE}" stroke="{SPONGE_DK}" stroke-width="1.6"/>'
                f'<ellipse cx="{x}" cy="{y-11}" rx="{w*.44:.0f}" ry="5" fill="#F6CC80" opacity=".8"/>'
                + (candle(x, y - 14) if candles else ''))
    if kind == 'tin':
        return (f'<path d="M{x-w/2:.0f},{y-w*.3:.0f} Q{x:.0f},{y-w*.62:.0f} {x+w/2:.0f},{y-w*.3:.0f} Z" fill="{SPONGE}" stroke="{SPONGE_DK}" stroke-width="1.6"/>'
                f'<rect x="{x-w/2:.0f}" y="{y-w*.3:.0f}" width="{w}" height="{w*.3:.0f}" rx="3" fill="#B8C2CA" stroke="#7E8A92" stroke-width="1.6"/>')
    lh = w * .26
    for i in range(3):
        lw = w * (1 - i*.14)
        ly = y - 6 - (i+1)*lh
        out += (f'<rect x="{x-lw/2:.0f}" y="{ly:.0f}" width="{lw:.0f}" height="{lh:.0f}" rx="5" fill="{SPONGE}" stroke="{SPONGE_DK}" stroke-width="1.5"/>'
                f'<path d="M{x-lw/2:.0f},{ly+6:.0f} V{ly+2:.0f} Q{x-lw/2:.0f},{ly-3:.0f} {x-lw/2+6:.0f},{ly-3:.0f} H{x+lw/2-6:.0f} '
                f'Q{x+lw/2:.0f},{ly-3:.0f} {x+lw/2:.0f},{ly+2:.0f} V{ly+6:.0f} '
                + " ".join(f'q{-lw/12:.1f},{8 if k % 2 else 3} {-lw/6:.1f},0' for k in range(6))
                + f' Z" fill="{ICING}" stroke="{ICING_DK}" stroke-width="1.2"/>')
    top = y - 6 - 3*lh
    out += "".join(f'<circle cx="{x+dx*w:.0f}" cy="{top-1:.0f}" r="3" fill="{c}"/>'
                   for dx, c in ((-.24, "#FF6B6B"), (-.08, "#74C8E4"), (.1, "#FFD166"), (.25, "#C77DFF")))
    for i in range(candles):
        out += candle(x + (i - (candles-1)/2)*16, top - 2)
    return out


def candle(x, y, lit=True):
    """A striped birthday candle, `y` its foot."""
    return (f'<rect x="{x-3}" y="{y-22}" width="6" height="22" rx="2" fill="#FFFFFF" stroke="#74C8E4" stroke-width="1.2"/>'
            f'<path d="M{x-3},{y-16} l6,-4 M{x-3},{y-8} l6,-4" stroke="#74C8E4" stroke-width="1.6"/>'
            + (f'<path d="M{x},{y-36} q6,8 0,12 q-6,-4 0,-12 Z" fill="#FFB347" stroke="#FF8A3D" stroke-width="1"/>' if lit else ''))


def measuring_cup(x, y, s=1.0, full=True, rot=0):
    """A measuring cup, `x, y` the middle of its rim; `full` heaps flour in it."""
    return (f'<g transform="rotate({rot} {x} {y})">'
            + (f'<path d="M{x-12*s:.0f},{y:.0f} Q{x:.0f},{y-10*s:.0f} {x+12*s:.0f},{y:.0f} Z" fill="#FFFFFF" stroke="#E4DCCB" stroke-width="1.2"/>' if full else '')
            + f'<path d="M{x-12*s:.0f},{y:.0f} L{x-9*s:.0f},{y+20*s:.0f} L{x+9*s:.0f},{y+20*s:.0f} L{x+12*s:.0f},{y:.0f} Z" fill="#FF9BAE" stroke="#E0708A" stroke-width="1.5"/>'
            f'<path d="M{x+11*s:.0f},{y+4*s:.0f} h{12*s:.0f} v{6*s:.0f} h{-11*s:.0f}" stroke="#E0708A" stroke-width="{3*s:.1f}" fill="none"/>'
            f'<path d="M{x-6*s:.0f},{y+8*s:.0f} h{5*s:.0f} M{x-6*s:.0f},{y+13*s:.0f} h{5*s:.0f}" stroke="#FFFFFF" stroke-width="1.4"/></g>')


def bunting(x0, x1, y, sag=24, n=9):
    """A string of party flags across the top of the room."""
    out = [f'<path d="M{x0},{y} Q{(x0+x1)/2:.0f},{y+sag*2} {x1},{y}" stroke="#9A8E78" stroke-width="1.6" fill="none"/>']
    for i in range(n):
        t = (i + .5) / n
        px = x0 + (x1-x0)*t
        py = y + sag*2*2*t*(1-t)
        out.append(f'<path d="M{px-10:.0f},{py:.0f} L{px+10:.0f},{py:.0f} L{px:.0f},{py+20:.0f} Z" fill="{CUSHIONS[i % 6]}"/>')
    return "".join(out)


def stairs(x, y, n=4, step=18):
    """A little staircase going up to the right, `x, y` its bottom-left corner."""
    d = f'M{x},{y} ' + " ".join(f'v{-step} h{step*1.4:.0f}' for _ in range(n)) + f' V{y} Z'
    return f'<path d="{d}" fill="#E8C48A" stroke="#B98A56" stroke-width="2" stroke-linejoin="round"/>'


def party_hat(x, y, s=1.0, rot=0, color="#C77DFF"):
    """A little cone party hat, `x, y` the middle of its brim."""
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<path d="M{x-13*s:.0f},{y} L{x:.0f},{y-34*s:.0f} L{x+13*s:.0f},{y} Z" fill="{color}" stroke="#00000033" stroke-width="1.2"/>'
            f'<path d="M{x-7*s:.0f},{y-16*s:.0f} l{14*s:.0f},0" stroke="#FFFFFF" stroke-width="{3*s:.1f}" opacity=".7"/>'
            f'<circle cx="{x}" cy="{y-35*s:.0f}" r="{4.5*s:.1f}" fill="#FFD166"/></g>')


# ---------------------------------------------------------------- story 12 props
# Story 12 is a windy day and one kite between two friends. Wind is drawn, not
# implied: curly gust lines, leaves on the move, the kite's tail streaming out.
KITE, KITE_DK = "#FF6B6B", "#C0484A"


def kite(x, y, s=1.0, rot=0, tail=True):
    """A diamond kite, `x, y` where the string ties on (the middle of the cross)."""
    import math as _m
    bows = ''
    if tail:
        pts = [(x + _m.sin(i*1.3)*10*s, y + (40 + i*16)*s) for i in range(6)]
        d = f'M{x:.0f},{y+40*s:.0f} ' + " ".join(f'L{px:.0f},{py:.0f}' for px, py in pts)
        bows = (f'<path d="{d}" stroke="#5E6870" stroke-width="1.6" fill="none" stroke-linejoin="round"/>'
                + "".join(f'<path d="M{px-7*s:.1f},{py-4*s:.1f} L{px:.1f},{py:.1f} L{px-7*s:.1f},{py+4*s:.1f} Z '
                          f'M{px+7*s:.1f},{py-4*s:.1f} L{px:.1f},{py:.1f} L{px+7*s:.1f},{py+4*s:.1f} Z" fill="{c}"/>'
                          for (px, py), c in zip(pts[1:], ("#FFD166", "#74C8E4", "#C77DFF", "#FFD166", "#74C8E4"))))
    return (f'<g transform="rotate({rot} {x} {y})">{bows}'
            f'<path d="M{x:.0f},{y-34*s:.0f} L{x+26*s:.0f},{y-6*s:.0f} L{x:.0f},{y+40*s:.0f} L{x-26*s:.0f},{y-6*s:.0f} Z" '
            f'fill="{KITE}" stroke="{KITE_DK}" stroke-width="2" stroke-linejoin="round"/>'
            f'<path d="M{x:.0f},{y-34*s:.0f} L{x+26*s:.0f},{y-6*s:.0f} L{x:.0f},{y-6*s:.0f} Z" fill="#FF9BAE"/>'
            f'<path d="M{x:.0f},{y-6*s:.0f} L{x-26*s:.0f},{y-6*s:.0f} L{x:.0f},{y+40*s:.0f} Z" fill="#E4453F" opacity=".5"/>'
            f'<path d="M{x:.0f},{y-34*s:.0f} V{y+40*s:.0f} M{x-26*s:.0f},{y-6*s:.0f} H{x+26*s:.0f}" stroke="{KITE_DK}" stroke-width="1.6"/></g>')


def kite_string(x0, y0, x1, y1, sag=.12):
    """The kite string from a paw or trunk (x0, y0) up to the kite (x1, y1), with a
    little belly in it."""
    mx, my = (x0+x1)/2 + (y1-y0)*sag, (y0+y1)/2 - (x1-x0)*sag
    return f'<path d="M{x0:.0f},{y0:.0f} Q{mx:.0f},{my:.0f} {x1:.0f},{y1:.0f}" stroke="#6B5B47" stroke-width="1.4" fill="none"/>'


def gust(x, y, s=1.0, flip=False):
    """One curly gust of wind blowing to the right (`flip` blows left)."""
    d = -1 if flip else 1
    return (f'<path d="M{x-d*50*s:.0f},{y:.0f} H{x+d*20*s:.0f} q{d*16*s:.0f},0 {d*16*s:.0f},{-12*s:.0f} '
            f'q0,{-10*s:.0f} {-d*10*s:.0f},{-10*s:.0f} q{-d*8*s:.0f},0 {-d*8*s:.0f},{8*s:.0f}" '
            f'stroke="#FFFFFF" stroke-width="{3.4*s:.1f}" fill="none" stroke-linecap="round" opacity=".9"/>'
            f'<path d="M{x-d*40*s:.0f},{y+12*s:.0f} H{x+d*4*s:.0f}" stroke="#FFFFFF" stroke-width="{3*s:.1f}" '
            f'stroke-linecap="round" opacity=".75"/>')


def tall_tree(x, y, h=260):
    """A tall tree, `y` the ground, `h` up to the top of its crown - tall enough
    for a kite to get stuck in."""
    top = y - h
    return (f'<path d="M{x-12},{y} L{x-7},{top+60} L{x+7},{top+60} L{x+12},{y} Z" fill="{BARK}" stroke="{BARK_DK}" stroke-width="1.5"/>'
            f'<path d="M{x+4},{y-h*.45:.0f} q22,-10 32,-34 M{x-4},{y-h*.6:.0f} q-20,-8 -28,-30" stroke="{BARK}" stroke-width="6" fill="none" stroke-linecap="round"/>'
            + "".join(f'<circle cx="{x+dx}" cy="{top+dy}" r="{r}" fill="{c}"/>'
                      for dx, dy, r, c in ((-34, 80, 36, LEAF), (34, 76, 36, LEAF), (-20, 44, 38, LEAF), (22, 40, 36, LEAF),
                                           (0, 26, 30, LEAF_LT), (-4, 76, 30, LEAF_LT)))
            + f'<circle cx="{x+40}" cy="{y-h*.45-38:.0f}" r="13" fill="{LEAF_LT}"/><circle cx="{x-36}" cy="{y-h*.6-32:.0f}" r="12" fill="{LEAF}"/>')


def bird_nest(x, y, s=1.0, bird=True):
    """A twiggy nest, `x, y` the middle of its base, with a little blue bird in it."""
    out = ''
    if bird:
        out = (f'<ellipse cx="{x+2*s:.0f}" cy="{y-16*s:.0f}" rx="{11*s:.1f}" ry="{9*s:.1f}" fill="#74C8E4" stroke="#3C90AE" stroke-width="1.2"/>'
               f'<circle cx="{x+8*s:.0f}" cy="{y-26*s:.0f}" r="{7*s:.1f}" fill="#74C8E4" stroke="#3C90AE" stroke-width="1.2"/>'
               f'<path d="M{x+14*s:.0f},{y-27*s:.0f} l{6*s:.1f},{2*s:.1f} l{-6*s:.1f},{2*s:.1f} Z" fill="#FFB347"/>'
               f'<circle cx="{x+10*s:.0f}" cy="{y-28*s:.0f}" r="{1.4*s:.1f}" fill="{INK}"/>')
    return (out + f'<path d="M{x-22*s:.0f},{y-12*s:.0f} Q{x-20*s:.0f},{y+2*s:.0f} {x:.0f},{y+2*s:.0f} Q{x+20*s:.0f},{y+2*s:.0f} {x+22*s:.0f},{y-12*s:.0f} Z" '
                  f'fill="#B98A56" stroke="#7E5A38" stroke-width="1.5"/>'
            + "".join(f'<path d="M{x+dx*s:.0f},{y-10*s:.0f} l{14*s:.0f},{6*s:.0f}" stroke="#7E5A38" stroke-width="1.4" stroke-linecap="round"/>'
                      for dx in (-20, -8, 4)))


def belt(w=56, y=-32, color="#C77DFF"):
    """Rabbit's belt, in rabbit-local coordinates - pass it as `extra`."""
    return (f'<path d="M{-w/2},{y-2} Q0,{y+8} {w/2},{y-2}" stroke="{color}" stroke-width="7" fill="none" stroke-linecap="round"/>'
            f'<rect x="-7" y="{y-3}" width="14" height="11" rx="2" fill="#FFD166" stroke="#D8A21F" stroke-width="1.5"/>')
