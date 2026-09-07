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
