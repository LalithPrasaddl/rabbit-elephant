"""Rebuild story 06 page 1 from the library, beside the hand-drawn original."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scene as S
from characters import rabbit, elephant, bandage, E_BODY, E_LINE

ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))


def hospital(x, y, w=200, h=140):
    """The clinic. One-off scenery still lives in the page that needs it."""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="white" stroke="#D0D0D0" stroke-width="2"/>'
            f'<rect x="{x-6}" y="{y-6}" width="{w+12}" height="16" rx="4" fill="#E0E0E0" stroke="#C8C8C8" stroke-width="1.5"/>'
            f'<rect x="{x+80}" y="{y-36}" width="40" height="40" rx="6" fill="white" stroke="#FF6B6B" stroke-width="2"/>'
            f'<rect x="{x+96}" y="{y-32}" width="8" height="32" rx="2" fill="#FF6B6B"/>'
            f'<rect x="{x+82}" y="{y-20}" width="36" height="8" rx="2" fill="#FF6B6B"/>'
            + "".join(f'<rect x="{x+dx}" y="{y+26}" width="26" height="26" rx="3" fill="#74C8E4" opacity=".8"/>'
                      for dx in (16, 52, 160))
            + f'<rect x="{x+100}" y="{y+80}" width="60" height="60" rx="4" fill="#B8E8F8" stroke="#4AA8C8" stroke-width="2"/>')


def giraffe_at_window(x, y):
    return (f'<rect x="{x-13}" y="{y-10}" width="26" height="26" rx="3" fill="#74C8E4" opacity=".5"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="9" ry="12" fill="#E8C078" stroke="#C08840" stroke-width="1.5"/>'
            f'<ellipse cx="{x-6}" cy="{y-12}" rx="2.5" ry="6" fill="#C08840"/>'
            f'<ellipse cx="{x+6}" cy="{y-12}" rx="2.5" ry="6" fill="#C08840"/>'
            f'<circle cx="{x-4}" cy="{y-2}" r="2.3" fill="#2D3748"/><circle cx="{x+4}" cy="{y-2}" r="2.3" fill="#2D3748"/>'
            f'<path d="M{x-5},{y+6} Q{x},{y+3} {x+5},{y+6}" stroke="#2D3748" stroke-width="1.3" fill="none" stroke-linecap="round"/>')


def build():
    art = "".join([
        hospital(280, 70),
        giraffe_at_window(309, 140),
        S.shadow(400, 348, 46),
        # Elephant just out of the operation: cane-free but bandaged, looking at Rabbit
        elephant(400, 348, s=1.0, expr='calm', look=(-.75, .1), trunk=(-40, 54),
                 extra=bandage(18, -14)),
        S.shadow(140, 350, 34),
        # Rabbit stomping, one paw thrown up, looking back at Elephant
        rabbit(140, 350, expr='shout', look=(.55, 0), arm=(-32, -46), arm2=(22, 14),
               ears=(-16, 19)),
        S.bubble(["We waited FOREVER", "in there today!"], 118, 128, tail=(150, 214)),
    ])
    return S.page('p1-6', art, mood='tender', horizon=205,
                  sun=None, clouds=((90, 48, 40, 16), (116, 40, 24, 14), (420, 60, 34, 14)))


def original():
    h = open(os.path.join(ROOT, 'stories/06-bonk-the-bumpy-ride-home/index.html')).read()
    return [s for s in re.findall(r'<svg.*?</svg>', h, re.S) if 2000 < len(s) < 40000][0]


if __name__ == '__main__':
    new = build()
    old = original()
    out = os.path.join(HERE, 'out')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'proof.html'), 'w').write(
        '<style>body{margin:0;padding:22px;background:#FFF9F0;font:13px system-ui;color:#6B5B47}'
        '.g{display:grid;grid-template-columns:1fr 1fr;gap:14px}figure{margin:0}'
        '.a{background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.13)}'
        '.a svg{display:block;width:100%;height:auto}'
        'figcaption{padding:7px 0;text-align:center;font-weight:700;letter-spacing:.04em}</style>'
        f'<div class="g"><figure><div class="a">{old}</div>'
        f'<figcaption>NOW — hand-drawn, {len(old)/1024:.1f} KB</figcaption></figure>'
        f'<figure><div class="a">{new}</div>'
        f'<figcaption>LIBRARY — {len(new)/1024:.1f} KB</figcaption></figure></div>')
    print(f'old {len(old)}  new {len(new)} bytes -> {out}/proof.html')
