"""Shared helpers for generating naturalistic animal SVG portraits."""
import math, random

# ---------- cubic bezier path with sampling ----------
class BPath:
    """Closed path built from cubic segments. Can emit `d` and sample edge points+normals."""
    def __init__(self, start):
        self.start = start
        self.segs = []          # (c1, c2, end)
    def c(self, c1, c2, end):
        self.segs.append((c1, c2, end)); return self
    def d(self):
        out = "M%.1f %.1f" % self.start
        for c1, c2, e in self.segs:
            out += "C%.1f %.1f %.1f %.1f %.1f %.1f" % (c1[0], c1[1], c2[0], c2[1], e[0], e[1])
        return out + "Z"
    def _pts(self):
        p0 = self.start; res = []
        for c1, c2, e in self.segs:
            res.append((p0, c1, c2, e)); p0 = e
        # close back to start
        if p0 != self.start:
            res.append((p0, p0, self.start, self.start))
        return res
    def sample(self, n):
        """Return n (point, unit_tangent) pairs spread over the path."""
        segs = self._pts(); per = max(1, n // len(segs)); out = []
        for (p0, c1, c2, e) in segs:
            for i in range(per):
                t = (i + 0.5) / per
                mt = 1 - t
                x = mt**3*p0[0] + 3*mt*mt*t*c1[0] + 3*mt*t*t*c2[0] + t**3*e[0]
                y = mt**3*p0[1] + 3*mt*mt*t*c1[1] + 3*mt*t*t*c2[1] + t**3*e[1]
                dx = 3*mt*mt*(c1[0]-p0[0]) + 6*mt*t*(c2[0]-c1[0]) + 3*t*t*(e[0]-c2[0])
                dy = 3*mt*mt*(c1[1]-p0[1]) + 6*mt*t*(c2[1]-c1[1]) + 3*t*t*(e[1]-c2[1])
                L = math.hypot(dx, dy) or 1
                out.append(((x, y), (dx/L, dy/L)))
        return out
    def centroid(self):
        pts = [p for p, _ in self.sample(120)]
        return (sum(p[0] for p in pts)/len(pts), sum(p[1] for p in pts)/len(pts))


def stroke_d(x, y, ang, ln, curve, rng):
    """One tapered-looking hair: quadratic curve from (x,y) along ang."""
    ex = x + math.cos(ang)*ln
    ey = y + math.sin(ang)*ln
    mx, my = (x+ex)/2, (y+ey)/2
    px, py = -math.sin(ang), math.cos(ang)
    k = curve * rng.uniform(-1, 1)
    return "M%d %dQ%d %d %d %d" % (round(x), round(y), round(mx+px*k), round(my+py*k), round(ex), round(ey))


def fur_layers(zones, rng):
    """zones: list of dicts. Returns list of (color, width, opacity, d) merged by tone."""
    buckets = {}
    for z in zones:
        cx, cy, rx, ry = z["ell"]
        rot = z.get("rot", 0.0)
        flow = z["flow"]
        lo, hi = z.get("len", (6, 13))
        curve = z.get("curve", 1.2)
        jitter = z.get("jitter", 0.30)
        for _ in range(z["n"]):
            t = rng.random()*2*math.pi
            r = math.sqrt(rng.random())
            ux, uy = r*math.cos(t)*rx, r*math.sin(t)*ry
            if rot:
                ca, sa = math.cos(rot), math.sin(rot)
                ux, uy = ux*ca - uy*sa, ux*sa + uy*ca
            x, y = cx+ux, cy+uy
            ang = flow(x, y) + rng.uniform(-jitter, jitter)
            ln = rng.uniform(lo, hi)
            color, width, op = z["tones"][rng.randrange(len(z["tones"]))]
            key = (color, width, op)
            buckets.setdefault(key, []).append(stroke_d(x, y, ang, ln, curve, rng))
    return [(k[0], k[1], k[2], "".join(v)) for k, v in buckets.items()]


def edge_fur(path, n, flip, rng, tones, length=(4, 11), spread=0.45, inset=1.0):
    """Hairs sprouting outward along a silhouette so the edge never reads as vector-clean."""
    buckets = {}
    for (p, tan) in path.sample(n):
        nx, ny = (tan[1], -tan[0]) if flip else (-tan[1], tan[0])
        x, y = p[0] - nx*inset, p[1] - ny*inset
        base = math.atan2(ny, nx)
        ang = base + rng.uniform(-spread, spread)
        ln = rng.uniform(*length)
        color, width, op = tones[rng.randrange(len(tones))]
        key = (color, width, op)
        buckets.setdefault(key, []).append(stroke_d(x, y, ang, ln, 0.8, rng))
    return [(k[0], k[1], k[2], "".join(v)) for k, v in buckets.items()]


def render_fur(layers, extra=""):
    return "".join(
        '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-opacity="%s" stroke-linecap="round"%s/>'
        % (d, c, w, o, extra) for (c, w, o, d) in layers)


def cubic(p0, c1, c2, p3, n, t0=0.0, t1=1.0):
    """Sample an open cubic: returns [(point, unit_tangent, t)]."""
    out = []
    for i in range(n):
        t = t0 + (t1-t0) * (i/(n-1) if n > 1 else 0)
        mt = 1-t
        x = mt**3*p0[0] + 3*mt*mt*t*c1[0] + 3*mt*t*t*c2[0] + t**3*p3[0]
        y = mt**3*p0[1] + 3*mt*mt*t*c1[1] + 3*mt*t*t*c2[1] + t**3*p3[1]
        dx = 3*mt*mt*(c1[0]-p0[0]) + 6*mt*t*(c2[0]-c1[0]) + 3*t*t*(p3[0]-c2[0])
        dy = 3*mt*mt*(c1[1]-p0[1]) + 6*mt*t*(c2[1]-c1[1]) + 3*t*t*(p3[1]-c2[1])
        L = math.hypot(dx, dy) or 1
        out.append(((x, y), (dx/L, dy/L), t))
    return out


def rings(centerline, widths, n, rng, color="#000", op=.18, w=1.4, bow=0.30):
    """Wrinkle rings across a tapering limb (trunk, leg): one arc per sample, bowed with the form."""
    ds = []
    for ((x, y), (tx, ty), t) in centerline:
        half = widths(t) * rng.uniform(.82, 1.0)
        nx, ny = -ty, tx
        ax, ay = x - nx*half, y - ny*half
        bx, by = x + nx*half, y + ny*half
        cx_, cy_ = x + tx*half*bow*2, y + ty*half*bow*2
        ds.append("M%.1f %.1fQ%.1f %.1f %.1f %.1f" % (ax, ay, cx_, cy_, bx, by))
    return [(color, w, op, "".join(ds))]


def speckle(zones, rng):
    """Soft skin mottling: low-opacity blobs that break up a flat gradient."""
    out = []
    for z in zones:
        cx, cy, rx, ry = z["ell"]
        for _ in range(z["n"]):
            t = rng.random()*2*math.pi
            r = math.sqrt(rng.random())
            x, y = cx + r*math.cos(t)*rx, cy + r*math.sin(t)*ry
            rr = rng.uniform(*z.get("r", (3, 9)))
            c, o = z["tones"][rng.randrange(len(z["tones"]))]
            out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" opacity="%.2f"/>'
                       % (x, y, rr, rr*rng.uniform(.6, 1.0), c, o))
    return "".join(out)


def curls(zones, rng):
    """Fleece: little hooked arcs rather than straight hairs."""
    buckets = {}
    for z in zones:
        cx, cy, rx, ry = z["ell"]
        for _ in range(z["n"]):
            t = rng.random()*2*math.pi
            r = math.sqrt(rng.random())
            x, y = cx + r*math.cos(t)*rx, cy + r*math.sin(t)*ry
            R = rng.uniform(*z.get("r", (3.0, 6.5)))
            a0 = rng.uniform(0, 2*math.pi)
            sweep = rng.choice([0, 1])
            ax, ay = x + math.cos(a0)*R, y + math.sin(a0)*R
            a1 = a0 + rng.uniform(2.2, 3.5)
            bx, by = x + math.cos(a1)*R, y + math.sin(a1)*R
            color, w, op = z["tones"][rng.randrange(len(z["tones"]))]
            d = "M%d %dA%d %d 0 0 %d %d %d" % (round(ax), round(ay), round(R), round(R), sweep, round(bx), round(by))
            buckets.setdefault((color, w, op), []).append(d)
    return [(k[0], k[1], k[2], "".join(v)) for k, v in buckets.items()]


def blotches(zones, rng):
    """Irregular polygon patches - giraffe markings."""
    out = []
    for z in zones:
        cx, cy, rx, ry = z["ell"]
        for _ in range(z["n"]):
            t = rng.random()*2*math.pi
            r = math.sqrt(rng.random())
            x, y = cx + r*math.cos(t)*rx, cy + r*math.sin(t)*ry
            R = rng.uniform(*z.get("r", (8, 15)))
            n = rng.randint(5, 7)
            pts = []
            for i in range(n):
                a = 2*math.pi*i/n + rng.uniform(-.25, .25)
                rr = R*rng.uniform(.62, 1.0)
                pts.append("%d %d" % (round(x+math.cos(a)*rr), round(y+math.sin(a)*rr*z.get("sq", .85))))
            out.append('<path d="M%s Z" fill="%s" opacity="%.2f"/>' % (" L".join(pts), z["fill"], z.get("op", .85)))
    return "".join(out)
