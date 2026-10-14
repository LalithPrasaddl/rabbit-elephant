"""The six story covers, composed from scenelib backgrounds + real portrait figures.

Add a cover by writing a build_NN() that returns the finished SVG string and
registering it in COVERS. Run tools/scenes/build_covers.py to inject them.

Figures are never mirrored: the portraits are lit from the upper-RIGHT, so a
flipped figure would be lit from the wrong side. Scenes are composed with
everyone facing right instead, and the sun always sits upper-right.
"""
import math, random

import scenelib as S
import figures as F

DENSITY = 0.34          # fur density for cover-scale figures
HORIZON = 170


def _basket(P, x, y, s=1.0):
    """Woven basket of vegetables - warm wicker, lit upper-right."""
    d = (S.rad(f"{P}-bask", [(0, "#E8B679", None), (0.5, "#C68A4E", None), (1, "#7E5326", None)], cx="66%", cy="22%", r="90%") +
         S.rad(f"{P}-carr", [(0, "#FFB067", None), (0.5, "#FF7A3D", None), (1, "#C24A16", None)], cx="66%", cy="20%", r="88%") +
         S.rad(f"{P}-beet", [(0, "#FFC2D0", None), (0.5, "#FF8FA8", None), (1, "#B54A66", None)], cx="66%", cy="20%", r="88%") +
         S.rad(f"{P}-corn", [(0, "#FFF0AE", None), (0.5, "#FFD166", None), (1, "#B98A1E", None)], cx="66%", cy="20%", r="88%"))
    g = []
    g.append(S.contact_shadow(P, x, y + 26*s, 34*s, 8*s, .38))
    # veg first so the basket rim overlaps them
    for (dx, dy, rx, ry, grad, leaf) in [(-15, -20, 8, 17, 'carr', True), (0, -25, 7.5, 19, 'beet', True),
                                         (14, -19, 7.5, 16, 'corn', False)]:
        g.append(f'<ellipse cx="{x+dx*s:.0f}" cy="{y+dy*s:.0f}" rx="{rx*s:.1f}" ry="{ry*s:.1f}" fill="url(#{P}-{grad})"/>')
        if leaf:
            g.append(f'<path d="M{x+dx*s:.0f},{y+(dy-ry)*s:.0f} q{-6*s:.0f},{-9*s:.0f} {-1*s:.0f},{-13*s:.0f} '
                     f'q{5*s:.0f},{5*s:.0f} {2*s:.0f},{13*s:.0f} Z" fill="#5C9150" opacity=".9"/>')
    g.append(f'<path d="M{x-26*s:.0f},{y-8*s:.0f} L{x-20*s:.0f},{y+22*s:.0f} L{x+20*s:.0f},{y+22*s:.0f} '
             f'L{x+26*s:.0f},{y-8*s:.0f} Z" fill="url(#{P}-bask)"/>')
    # weave: horizontal bands + a shaded lower-left
    for i, yy in enumerate([-1, 7, 15]):
        g.append(f'<path d="M{x-24*s+i*1.2:.0f},{y+yy*s:.0f} q{24*s:.0f},{3*s:.0f} {47*s-i*2.4:.0f},0" '
                 f'stroke="#8A5A2E" stroke-width="{1.6*s:.1f}" fill="none" opacity=".45"/>')
    g.append(f'<ellipse cx="{x-14*s:.0f}" cy="{y+14*s:.0f}" rx="{16*s:.0f}" ry="{12*s:.0f}" fill="#5A3A18" opacity=".30" filter="url(#{P}-b2)"/>')
    g.append(f'<path d="M{x-27*s:.0f},{y-9*s:.0f} q{27*s:.0f},{-9*s:.0f} {54*s:.0f},0" stroke="#8A5A2E" '
             f'stroke-width="{4*s:.1f}" fill="none" stroke-linecap="round"/>')
    g.append(f'<path d="M{x-25*s:.0f},{y-11*s:.0f} q{25*s:.0f},{-8*s:.0f} {50*s:.0f},0" stroke="#E8B679" '
             f'stroke-width="{1.6*s:.1f}" fill="none" opacity=".7" stroke-linecap="round"/>')
    return d, "".join(g)


def build_01():
    """Rabbit and Elephant in the sunny meadow, the basket of veggies between them."""
    P = "cv1"
    rng = random.Random(101)
    d, b = [], []

    def add(pair):
        d.append(pair[0]); b.append(pair[1])

    add(S.sky(P, 'morning', HORIZON))
    add(S.sun(P, 418, 78, 34))
    b.append(S.clouds(P, [(78, 74, 40, 14, .9), (116, 66, 26, 10, .85), (232, 60, 30, 10, .6)]))
    add(S.hills(P, rng, HORIZON))
    add(S.foliage(P, rng, 44, 108, 40))
    b.insert(len(b) - 1, S.trunk(48, 118, 188, 11))

    gd, gback, gfront = S.meadow(P, rng, HORIZON,
                                 avoid=[(150, 240, 60, 55), (344, 244, 82, 60), (246, 262, 34, 30)])
    d.append(gd); b.append(gback)

    rab, ele = F.load('rabbit', DENSITY), F.load('elephant', DENSITY)
    d.append(rab[0]); d.append(ele[0])

    b.append(S.cast_shadow(P, 344, 278, 80))
    b.append(F.place(ele[1], 342, 278, 268))
    b.append(S.cast_shadow(P, 152, 274, 58))
    b.append(F.place(rab[1], 150, 274, 226))
    add(_basket(P, 246, 268, 1.0))

    b.append(gfront)
    add(S.sunwash(P, 418, 78))
    add(S.vignette(P))
    return S.wrap(P, "".join(d), "".join(b))



def build_02():
    """The thorn. Elephant favouring a sore foot, Rabbit alarmed beside him,
    Dr. Squirrel already on the way with the bag."""
    P = "cv2"
    rng = random.Random(202)
    d, b = [], []
    add = lambda p: (d.append(p[0]), b.append(p[1]))

    add(S.sky(P, 'peach', HORIZON))
    add(S.sun(P, 430, 84, 30, warm="#FFF0D8", glow="#FFD3A0"))
    b.append(S.clouds(P, [(96, 70, 44, 15, .85), (140, 63, 26, 10, .8), (300, 56, 34, 11, .5)]))
    add(S.hills(P, rng, HORIZON, far="#AFC79A", near="#8CAE6E"))
    add(S.foliage(P, rng, 52, 100, 42, dark="#4A6B34", base="#6B9146", light="#A8C96A"))
    b.insert(len(b) - 1, S.trunk(56, 110, 182, 11))

    gd, gback, gfront = S.meadow(P, rng, HORIZON, top="#94C468", bot="#43753A",
                                 avoid=[(190, 244, 78, 58), (352, 250, 56, 52), (250, 268, 40, 34)])
    d.append(gd); b.append(gback)

    ele, rab, sqr = F.load('elephant', DENSITY), F.load('rabbit', DENSITY), F.load('squirrel', DENSITY)
    d += [ele[0], rab[0], sqr[0]]

    b.append(S.cast_shadow(P, 158, 278, 76))
    b.append(F.place(ele[1], 156, 278, 258))
    b.append(S.cast_shadow(P, 316, 274, 54))
    b.append(F.place(rab[1], 314, 274, 212))
    # Dr. Squirrel arriving from the right with the bag
    b.append(S.cast_shadow(P, 416, 266, 42))
    b.append(F.place(sqr[1], 414, 266, 168))
    b.append('<g transform="translate(-26,0)"><ellipse cx="470" cy="268" rx="17" ry="4" fill="#24461F" opacity=".35"/>'
             '<rect x="454" y="240" width="34" height="24" rx="5" fill="#6E4A2E"/>'
             '<rect x="454" y="246" width="34" height="4" fill="#8A5F3A" opacity=".7"/>'
             '<rect x="468" y="246" width="6" height="12" fill="#E8533F"/>'
             '<rect x="465" y="249" width="12" height="6" fill="#E8533F"/>'
             '<path d="M462,240 q9,-9 18,0" stroke="#4E3320" stroke-width="3" fill="none"/></g>')

    # the thorn itself, big and foreground, right where the elephant just stepped
    add(S.thorn(P, 232, 292, 72))
    add(S.thorn(P, 266, 300, 40, flip=True))
    # the "ouch" burst, radiating off the sore front foot
    b.append('<g opacity=".9" stroke="#E8533F" stroke-width="4.5" stroke-linecap="round" fill="none">'
             '<path d="M196,258 l-20,-8"/><path d="M200,248 l-15,-16"/><path d="M210,242 l-6,-20"/>'
             '<path d="M222,242 l7,-19"/><path d="M230,250 l19,-11"/></g>')

    b.append(gfront)
    add(S.sunwash(P, 430, 84))
    add(S.vignette(P))
    return S.wrap(P, "".join(d), "".join(b))


def build_03():
    """Snow day. Everyone bundled up outside the clinic, Dr. Sheep on hand."""
    P = "cv3"
    rng = random.Random(303)
    d, b = [], []
    add = lambda p: (d.append(p[0]), b.append(p[1]))

    add(S.sky(P, 'winter', HORIZON))
    add(S.sun(P, 92, 80, 26, warm="#FFF8EC", glow="#FFE9C4"))
    b.append(S.clouds(P, [(330, 70, 52, 17, .9), (386, 62, 30, 12, .85), (196, 60, 36, 12, .6)]))
    add(S.hills(P, rng, HORIZON, far="#DCE8F4", near="#C3D6E8"))
    add(S.snowfield(P, rng, HORIZON))
    b.append(S.winter_tree(P, 462, 196, 104, 11))

    ele, rab, shp = F.load('elephant', DENSITY), F.load('rabbit', DENSITY), F.load('sheep', DENSITY)
    d += [ele[0], rab[0], shp[0]]

    cs = lambda x, y, w: S.cast_shadow(P, x, y, w, op=.30, col="#7C9BC0", stretch=1.9)
    b.append(cs(182, 274, 76))
    b.append(F.place(ele[1], 180, 274, 258))
    b.append(cs(288, 278, 54))
    b.append(F.place(rab[1], 286, 278, 218))
    b.append(cs(398, 274, 48))
    b.append(F.place(shp[1], 396, 274, 184))

    # Rabbit's scarf, hung on the real neck line (portrait y~222 is under the chin)
    nx, ny = F.to_scene(126, 222, 286, 278, 218)
    b.append(f'<g><path d="M{nx-38:.0f},{ny-4:.0f} q38,22 76,-2 q5,11 -1,18 q-40,20 -80,-2 Z" fill="#E8533F"/>'
             f'<path d="M{nx-38:.0f},{ny-4:.0f} q38,22 76,-2" stroke="#B93A2C" stroke-width="2" fill="none" opacity=".45"/>'
             f'<path d="M{nx-36:.0f},{ny+8:.0f} q-11,20 -5,38 q11,4 18,-2 q-8,-18 -3,-31 Z" fill="#E8533F"/>'
             f'<path d="M{nx-41:.0f},{ny+44:.0f} q9,5 17,-1" stroke="#B93A2C" stroke-width="2.4" fill="none" opacity=".5"/>'
             f'<path d="M{nx-30:.0f},{ny+4:.0f} q30,17 60,-1" stroke="#FFD166" stroke-width="3.4" fill="none" opacity=".6"/>'
             f'<path d="M{nx-33:.0f},{ny+22:.0f} q7,2 13,-1" stroke="#FFD166" stroke-width="3" fill="none" opacity=".55"/></g>')

    # a small snowman keeping watch on the left
    b.append('<g transform="translate(-16,-4) scale(1.1)"><ellipse cx="56" cy="288" rx="34" ry="8" fill="#9FBAD6" opacity=".45"/>'
             '<circle cx="56" cy="268" r="26" fill="#FFFFFF"/><circle cx="56" cy="238" r="19" fill="#FFFDF8"/>'
             '<circle cx="56" cy="216" r="14" fill="#FFFFFF"/>'
             '<ellipse cx="44" cy="276" rx="18" ry="14" fill="#C6D9EC" opacity=".55"/>'
             '<ellipse cx="47" cy="243" rx="12" ry="10" fill="#C6D9EC" opacity=".45"/>'
             '<circle cx="51" cy="213" r="2.2" fill="#3A3A3E"/><circle cx="61" cy="213" r="2.2" fill="#3A3A3E"/>'
             '<path d="M56,217 l10,3 -10,3 Z" fill="#FF8A3D"/>'
             '<path d="M40,205 q16,-9 32,0 l0,-7 q-16,-7 -32,0 Z" fill="#E8533F"/>'
             '<path d="M30,240 l-14,-12 M82,238 l14,-12" stroke="#6B5140" stroke-width="3" stroke-linecap="round" fill="none"/>'
             '<circle cx="56" cy="236" r="2.4" fill="#3A3A3E"/><circle cx="56" cy="246" r="2.4" fill="#3A3A3E"/></g>')

    # a small red-cross sign for the clinic, far right
    b.append('<g opacity=".95"><rect x="352" y="150" width="4" height="46" fill="#8A6A4E"/>'
             '<rect x="332" y="132" width="44" height="30" rx="6" fill="#FFF8EE"/>'
             '<rect x="350" y="139" width="8" height="16" fill="#E8533F"/>'
             '<rect x="346" y="143" width="16" height="8" fill="#E8533F"/></g>')

    b.append(S.snowfall(P, rng, 80))
    add(S.sunwash(P, 92, 80))
    add(S.vignette(P))
    return S.wrap(P, "".join(d), "".join(b))


def build_04():
    """Elephant marching down the track, oblivious; Rabbit spots the thorns."""
    P = "cv4"
    rng = random.Random(404)
    d, b = [], []
    add = lambda p: (d.append(p[0]), b.append(p[1]))

    add(S.sky(P, 'golden', HORIZON))
    add(S.sun(P, 404, 82, 36))
    b.append(S.clouds(P, [(102, 68, 46, 15, .8), (150, 61, 26, 10, .75)]))
    add(S.hills(P, rng, HORIZON, far="#B7C98F", near="#93B36C"))

    gd, gback, gfront = S.meadow(P, rng, HORIZON, top="#9AC96A", bot="#4B7A3C",
                                 avoid=[(180, 250, 90, 62), (368, 250, 60, 56)])
    d.append(gd); b.append(gback)
    add(S.dirt_path(P, rng, HORIZON, xtop=232, xbot=170, wtop=22, wbot=340))

    # the digger, small and hazy where the track meets the horizon
    b.append('<g opacity=".62" transform="translate(-58,0)"><rect x="300" y="146" width="40" height="20" rx="5" fill="#E0A82E"/>'
             '<rect x="325" y="133" width="19" height="16" rx="4" fill="#C99420"/>'
             '<rect x="328" y="136" width="12" height="9" rx="2" fill="#BFE0EE"/>'
             '<path d="M300,149 L272,133 L266,139 L294,156 Z" fill="#E0A82E"/>'
             '<path d="M266,139 l-10,10 8,7 12,-11 Z" fill="#C99420"/>'
             '<circle cx="310" cy="168" r="8" fill="#3A3A3E"/><circle cx="333" cy="168" r="8" fill="#3A3A3E"/></g>')
    add(S.foliage(P, rng, 54, 106, 40, dark="#436B33", base="#649143", light="#9FC968"))
    b.insert(len(b) - 1, S.trunk(58, 116, 186, 11))

    ele, rab = F.load('elephant', DENSITY), F.load('rabbit', DENSITY)
    d += [ele[0], rab[0]]

    # Elephant further down the track, so he reads as walking away into it
    b.append(S.cast_shadow(P, 150, 248, 60, col="#5E4630"))
    b.append(F.place(ele[1], 148, 248, 204))
    # Rabbit close to camera, right, calling out
    b.append(S.cast_shadow(P, 386, 290, 66))
    b.append(F.place(rab[1], 384, 290, 254))

    # thorn cluster on the track, dead ahead of the elephant's next step
    add(S.thorn(P, 196, 282, 54))
    add(S.thorn(P, 232, 292, 40, flip=True))
    add(S.thorn(P, 158, 292, 34, flip=True))
    add(S.thorn(P, 258, 276, 26))

    b.append(gfront)
    add(S.sunwash(P, 404, 82))
    add(S.vignette(P))
    return S.wrap(P, "".join(d), "".join(b))


def build_05():
    """Cannonball. Elephant is already in the pool, Rabbit is still airborne."""
    P = "cv5"
    rng = random.Random(505)
    d, b = [], []
    add = lambda p: (d.append(p[0]), b.append(p[1]))

    add(S.sky(P, 'noon', 150))
    add(S.sun(P, 424, 76, 34))
    b.append(S.clouds(P, [(84, 66, 42, 14, .9), (128, 59, 26, 10, .85), (250, 56, 30, 10, .55)]))
    add(S.hills(P, rng, 150, far="#A9CE9C", near="#87B473"))
    gd, gback, _ = S.meadow(P, rng, 150, top="#8FC163", bot="#5C8B45", flowers=8,
                            avoid=[(0, 0, 500, 500)])
    d.append(gd); b.append(gback)

    ele, rab = F.load('elephant', DENSITY), F.load('rabbit', DENSITY)
    d += [ele[0], rab[0]]

    # Elephant chest-deep in the pool; the water is drawn over his legs
    b.append(F.place(ele[1], 356, 296, 272))
    add(S.pool(P, rng, ytop=214, cx=306, rx=300))
    b.append(f'<ellipse cx="354" cy="250" rx="98" ry="17" fill="#0E6690" opacity=".30" filter="url(#{P}-b3)"/>')
    b.append(f'<ellipse cx="354" cy="248" rx="106" ry="14" fill="none" stroke="#EAF9FF" stroke-width="3" opacity=".5"/>')
    b.append(f'<ellipse cx="354" cy="254" rx="136" ry="19" fill="none" stroke="#EAF9FF" stroke-width="2" opacity=".28"/>')
    add(S.splash(P, rng, 336, 244, 1.25))

    # Rabbit on the near deck, in front of the water, catching the wave
    b.append(S.cast_shadow(P, 86, 296, 52, op=.26, col="#8C7A5E"))
    b.append(F.place(rab[1], 84, 296, 218, rot=-8))
    add(S.splash(P, rng, 150, 268, .72))

    # beach ball bobbing at the left
    d.append(S.rad(f"{P}-ball", [(0, "#FFFFFF", None), (0.35, "#FFD166", None), (1, "#E0912B", None)],
                   cx="66%", cy="24%", r="88%"))
    b.append(f'<g><ellipse cx="436" cy="272" rx="30" ry="8" fill="#0E6690" opacity=".35" filter="url(#{P}-b2)"/>'
             f'<circle cx="436" cy="256" r="25" fill="url(#{P}-ball)"/>'
             f'<path d="M436,231 q15,25 0,50" stroke="#E8533F" stroke-width="6.5" fill="none" opacity=".85"/>'
             f'<path d="M436,231 q-15,25 0,50" stroke="#4FA9DC" stroke-width="6.5" fill="none" opacity=".85"/>'
             f'<ellipse cx="427" cy="244" rx="7.5" ry="5" fill="#FFFFFF" opacity=".6"/>'
             f'<ellipse cx="436" cy="280" rx="24" ry="6" fill="#DFF6FF" opacity=".45"/></g>')

    add(S.sunwash(P, 424, 76))
    add(S.vignette(P))
    return S.wrap(P, "".join(d), "".join(b))


def build_06():
    """The drive home at golden hour, with Bear's little car coming the other way."""
    P = "cv6"
    rng = random.Random(606)
    d, b = [], []
    add = lambda p: (d.append(p[0]), b.append(p[1]))

    add(S.sky(P, 'dusk', HORIZON))
    add(S.sun(P, 408, 112, 40, warm="#FFF0D0", glow="#FFC08A"))
    b.append(S.clouds(P, [(96, 76, 48, 15, .75), (146, 68, 28, 11, .7), (300, 64, 34, 11, .5)]))
    add(S.hills(P, rng, HORIZON, far="#B99A9E", near="#94A97C"))
    add(S.foliage(P, rng, 52, 112, 40, dark="#43563A", base="#66804B", light="#A8B96A"))
    b.insert(len(b) - 1, S.trunk(56, 122, 188, 11))

    gd, gback, gfront = S.meadow(P, rng, HORIZON, top="#9EC069", bot="#4C6E3B", flowers=14,
                                 avoid=[(190, 250, 190, 70)])
    d.append(gd); b.append(gback)
    add(S.dirt_path(P, rng, HORIZON, xtop=316, xbot=250, wtop=20, wbot=380))

    # Bear's car in the distance, coming the other way
    bd, bb = S.car(P, 392, 208, 96, body_col="#7FB7E0", dark="#3D7BA8", light="#CBE7F7")
    d.append(bd)
    bear = F.load('bear', DENSITY)
    d.append(bear[0])
    b.append(F.place(bear[1], 392, 214, 108))
    b.append(bb)

    rab, ele = F.load('rabbit', DENSITY), F.load('elephant', DENSITY)
    d += [rab[0], ele[0]]

    # Rabbit driving, Elephant riding shotgun - the car body hides their legs
    b.append(F.place(ele[1], 246, 258, 210))
    b.append(F.place(rab[1], 160, 252, 180))
    cd, cb = S.car(P, 198, 274, 250)
    d.append(cd); b.append(cb)

    b.append(gfront)
    add(S.sunwash(P, 408, 112))
    add(S.vignette(P))
    return S.wrap(P, "".join(d), "".join(b))


def _burrow(P, x, ybase, r=22):
    """Rabbit's front door: a grassy mound with a small round door, lamplight in its
    window. Small on purpose - the whole joke of story 07 is that Elephant will
    never fit through it. `x, ybase` is the foot of the door."""
    d = (S.rad(f"{P}-mound", [(0, "#A8CF78", None), (0.5, "#76A653", None), (1, "#3F6A3A", None)],
               cx="62%", cy="20%", r="80%") +
         S.rad(f"{P}-door", [(0, "#E3A867", None), (0.55, "#B9773E", None), (1, "#6E4322", None)],
               cx="66%", cy="22%", r="90%") +
         S.rad(f"{P}-lamp", [(0, "#FFF6D2", "1"), (0.5, "#FFD98A", "0.7"), (1, "#FFC060", "0")]))
    top = ybase - r*1.9
    hole = f'M{x-r},{ybase} L{x-r},{ybase-r*.9:.0f} A{r},{r} 0 0 1 {x+r},{ybase-r*.9:.0f} L{x+r},{ybase} Z'
    g = (f'<path d="M{x-96},{ybase+10} C{x-80},{ybase-70} {x-30},{ybase-108} {x+40},{ybase-110} '
         f'C{x+110},{ybase-108} {x+170},{ybase-60} {x+190},{ybase+10} Z" fill="url(#{P}-mound)"/>'
         f'<ellipse cx="{x-40}" cy="{ybase-30}" rx="50" ry="40" fill="#24461F" opacity=".22" filter="url(#{P}-b4)"/>'
         f'<path d="{hole}" fill="#3A2412" stroke="#5A3A1E" stroke-width="5"/>'
         f'<path d="{hole}" fill="url(#{P}-door)"/>'
         + "".join(f'<line x1="{x+k*r/2.5:.0f}" y1="{ybase}" x2="{x+k*r/2.5:.0f}" y2="{top+4:.0f}" stroke="#6E4322" '
                   f'stroke-width="1.2" opacity=".55"/>' for k in (-1, 0, 1))
         + f'<circle cx="{x}" cy="{ybase-r*1.05:.0f}" r="{r*1.1:.0f}" fill="url(#{P}-lamp)" opacity=".75"/>'
         f'<circle cx="{x}" cy="{ybase-r*1.05:.0f}" r="{r*.3:.1f}" fill="#FFE7A6" stroke="#6E4322" stroke-width="1.2"/>'
         f'<circle cx="{x+r*.6:.0f}" cy="{ybase-r*.45:.0f}" r="1.8" fill="#FFD166"/>')
    return d, g


def _stars(rng, n=26, top=-80, bottom=120, avoid=(436, 60, 52)):
    ax, ay, ar = avoid
    out = []
    while len(out) < n:
        x, y = rng.uniform(8, 492), rng.uniform(top, bottom)
        if (x-ax)**2 + (y-ay)**2 < ar*ar:
            continue
        r = rng.uniform(.8, 2.1)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#FFF6DA" opacity="{rng.uniform(.5, .95):.2f}"/>')
        if r > 1.8:   # the brightest few get a little twinkle cross
            out.append(f'<path d="M{x-5:.0f},{y:.0f} h10 M{x:.0f},{y-5:.0f} v10" stroke="#FFF6DA" stroke-width=".8" opacity=".7"/>')
    return "".join(out)


def build_07():
    """Bedtime at the burrow: Elephant, pillow on his head and snacks in hand, next to
    a front door about the size of his foot. Rabbit is not sure about this."""
    P = "cv7"
    rng = random.Random(707)
    d, b = [], []
    add = lambda p: (d.append(p[0]), b.append(p[1]))

    add(S.sky(P, 'twilight', HORIZON))
    b.append(_stars(rng))
    # the moon takes the sun's place upper-right, so the figures' lighting still holds
    add(S.sun(P, 436, 64, 24, warm="#FFFBEA", glow="#FFF0C6"))
    b.append(S.clouds(P, [(96, 92, 44, 13, .55), (138, 86, 24, 9, .5)]))
    add(S.hills(P, rng, HORIZON, far="#9C93B8", near="#7E9E78"))

    gd, gback, gfront = S.meadow(P, rng, HORIZON, top="#8DB86A", bot="#3D6638", flowers=16,
                                 avoid=[(160, 260, 90, 60), (318, 262, 56, 52), (404, 262, 50, 30)])
    d.append(gd); b.append(gback)
    add(_burrow(P, 404, 262, 22))

    ele, rab = F.load('elephant', DENSITY), F.load('rabbit', DENSITY)
    d += [ele[0], rab[0]]

    b.append(S.cast_shadow(P, 162, 280, 80))
    b.append(F.place(ele[1], 160, 280, 268))
    # a pillow balanced on his head, and the snack suitcase at his feet. The crown of
    # the head sits ~44 units below the figure box's top (the box allows for the ears)
    px, py = 186, round(F.head_top(280, 268) + 44)
    b.append(f'<g transform="rotate(-8 {px} {py})">'
             f'<path d="M{px-44},{py-14} Q{px},{py-6} {px+44},{py-14} Q{px+38},{py} {px+44},{py+14} '
             f'Q{px},{py+6} {px-44},{py+14} Q{px-38},{py} {px-44},{py-14} Z" fill="#FFE3EC"/>'
             f'<path d="M{px-38},{py+6} Q{px},{py} {px+38},{py+6}" stroke="#E8A8BC" stroke-width="3" fill="none" opacity=".6"/>'
             f'<ellipse cx="{px+16}" cy="{py-9}" rx="18" ry="4" fill="#FFFFFF" opacity=".7" filter="url(#{P}-b1)"/></g>')
    b.append(S.contact_shadow(P, 236, 284, 26, 6, .4))
    b.append('<g transform="translate(-14,0)"><rect x="226" y="246" width="50" height="36" rx="6" fill="#B66FE8"/>'
             '<rect x="226" y="258" width="50" height="5" fill="#8A45C4" opacity=".6"/>'
             '<path d="M242,246 v-8 h18 v8" stroke="#6B4A2E" stroke-width="3.4" fill="none"/>'
             '<rect x="252" y="248" width="22" height="30" rx="5" fill="#E2B2FF" opacity=".35"/>'
             '<circle cx="264" cy="272" r="3.4" fill="#FFD166"/></g>')

    b.append(S.cast_shadow(P, 330, 276, 54))
    b.append(F.place(rab[1], 328, 276, 214))

    # fireflies - the night is friendly
    b.append("".join(f'<circle cx="{x}" cy="{y}" r="2.2" fill="#FFF3A0" opacity=".9" filter="url(#{P}-b1)"/>'
                     f'<circle cx="{x}" cy="{y}" r="1" fill="#FFFFFF"/>'
                     for x, y in ((96, 214), (286, 196), (452, 214), (232, 168), (380, 160))))

    b.append(gfront)
    add(S.sunwash(P, 436, 64))
    add(S.vignette(P))
    return S.wrap(P, "".join(d), "".join(b))


def _skinny_tree(P, rng, x, ybase, top):
    """A tree far too thin to hide behind: a stick of a trunk and a small tuft."""
    d, f = S.foliage(P, rng, x + 4, top, 30)
    return d, S.trunk(x, top + 14, ybase, 13) + f


def _flowerpot(P, x, ybase, w=118, h=86):
    """A big terracotta pot, lit upper-right; drawn over whoever is inside it."""
    d = S.lin(f"{P}-pot", [(0, "#F2A274", None), (1, "#C4673C", None)], x1=1, y1=0, x2=0, y2=0)
    top = ybase - h
    return d, (S.contact_shadow(P, x, ybase, w*.5, 7, .4)
               + f'<path d="M{x-w*.44:.0f},{top+12} L{x-w*.34:.0f},{ybase} L{x+w*.34:.0f},{ybase} L{x+w*.44:.0f},{top+12} Z" fill="url(#{P}-pot)"/>'
               f'<path d="M{x-w*.38:.0f},{top+26} L{x-w*.31:.0f},{ybase-4}" stroke="#9A4A26" stroke-width="10" opacity=".25" filter="url(#{P}-b1)"/>'
               f'<rect x="{x-w/2:.0f}" y="{top}" width="{w}" height="18" rx="5" fill="#E89466"/>'
               f'<rect x="{x-w/2+4:.0f}" y="{top+2}" width="{w-8}" height="5" rx="2.5" fill="#FFC8A0" opacity=".6"/>')


def build_08():
    """Hide and seek: Elephant 'hiding' behind a tree as thin as a broom handle,
    and Rabbit grinning out of a flowerpot - she is much better at this."""
    P = "cv8"
    rng = random.Random(808)
    d, b = [], []
    add = lambda p: (d.append(p[0]), b.append(p[1]))

    add(S.sky(P, 'morning', HORIZON))
    add(S.sun(P, 424, 70, 32))
    b.append(S.clouds(P, [(86, 70, 42, 14, .9), (124, 62, 24, 10, .85), (250, 50, 30, 10, .6)]))
    add(S.hills(P, rng, HORIZON))

    gd, gback, gfront = S.meadow(P, rng, HORIZON, avoid=[(186, 250, 100, 60), (340, 262, 70, 40)])
    d.append(gd); b.append(gback)

    ele, rab = F.load('elephant', DENSITY), F.load('rabbit', DENSITY)
    d += [ele[0], rab[0]]

    b.append(S.cast_shadow(P, 186, 280, 82))
    b.append(F.place(ele[1], 180, 280, 262))
    # the tree goes over him: it covers a stripe down his middle and nothing else
    add(_skinny_tree(P, rng, 200, 286, 70))

    b.append(F.place(rab[1], 352, 266, 196))
    add(_flowerpot(P, 340, 284, w=150))

    b.append(gfront)
    add(S.sunwash(P, 424, 70))
    add(S.vignette(P))
    return S.wrap(P, "".join(d), "".join(b))


def _bike(P, x, ybase, s=1.0):
    """Rabbit's red bike side-on, facing right; `x` is the pedals."""
    r = 25*s
    rh, fh = (x - 47*s, ybase - r), (x + 49*s, ybase - r)
    bb, st, ht = (x, ybase - 23*s), (x - 18*s, ybase - 62*s), (x + 35*s, ybase - 64*s)
    gy = ybase - 84*s
    out = [S.contact_shadow(P, x, ybase + 2, 86*s, 6, .4)]
    for hx, hy in (rh, fh):
        out.append(f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="{r:.1f}" fill="none" stroke="#2E3440" stroke-width="{5*s:.1f}"/>'
                   f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="{r-3*s:.1f}" fill="none" stroke="#5A6270" stroke-width="1.2" opacity=".6"/>'
                   + "".join(f'<path d="M{hx-r*.85*c:.1f},{hy-r*.85*sn:.1f} L{hx+r*.85*c:.1f},{hy+r*.85*sn:.1f}" stroke="#B8C2CA" stroke-width=".9"/>'
                             for c, sn in ((1, 0), (0, 1), (.7, .7), (.7, -.7)))
                   + f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="{3*s:.1f}" fill="#C9D2D8"/>')
    frame = (f'M{rh[0]:.0f},{rh[1]:.0f} L{bb[0]:.0f},{bb[1]:.0f} L{st[0]:.0f},{st[1]:.0f} Z M{st[0]:.0f},{st[1]:.0f} '
             f'L{ht[0]:.0f},{ht[1]:.0f} L{bb[0]:.0f},{bb[1]:.0f} M{ht[0]:.0f},{ht[1]:.0f} L{fh[0]:.0f},{fh[1]:.0f}')
    out += [f'<path d="{frame}" stroke="#A8302E" stroke-width="{6.4*s:.1f}" fill="none" stroke-linejoin="round" stroke-linecap="round"/>',
            f'<path d="{frame}" stroke="#E8504A" stroke-width="{4.2*s:.1f}" fill="none" stroke-linejoin="round" stroke-linecap="round"/>',
            f'<path d="{frame}" stroke="#FF9A8E" stroke-width="{1.2*s:.1f}" fill="none" stroke-linejoin="round" transform="translate(.8,-1.4)" opacity=".8"/>',
            f'<path d="M{st[0]:.0f},{st[1]:.0f} l{-3*s:.1f},{-7*s:.1f}" stroke="#9AA6AE" stroke-width="{3*s:.1f}"/>',
            f'<ellipse cx="{st[0]-4*s:.0f}" cy="{st[1]-8*s:.0f}" rx="{13*s:.1f}" ry="{4*s:.1f}" fill="#2E3440"/>',
            f'<path d="M{ht[0]:.0f},{ht[1]:.0f} L{ht[0]-2*s:.0f},{gy+4*s:.0f} Q{ht[0]-2*s:.0f},{gy:.0f} {ht[0]-8*s:.0f},{gy:.0f}" '
            f'stroke="#4A525E" stroke-width="{4*s:.1f}" fill="none" stroke-linecap="round"/>',
            f'<circle cx="{ht[0]+4*s:.0f}" cy="{gy+8*s:.0f}" r="{4.6*s:.1f}" fill="#FFD166"/>'
            f'<circle cx="{ht[0]+5*s:.0f}" cy="{gy+6.6*s:.0f}" r="{1.6*s:.1f}" fill="#FFF3C4"/>',
            f'<circle cx="{bb[0]:.0f}" cy="{bb[1]:.0f}" r="{7*s:.1f}" fill="#9AA6AE"/>',
            f'<path d="M{x+6*s:.0f},{ybase-13*s:.0f} L{x-12*s:.0f},{ybase-33*s:.0f}" stroke="#5A6270" stroke-width="{3*s:.1f}" stroke-linecap="round"/>']
    return "".join(out)


def build_09():
    """Bike day: Rabbit in her helmet with the shiny red bike, Elephant cheering her
    on, and a butterfly about to cause trouble."""
    P = "cv9"
    rng = random.Random(909)
    d, b = [], []
    add = lambda p: (d.append(p[0]), b.append(p[1]))

    add(S.sky(P, 'golden', HORIZON))
    add(S.sun(P, 420, 78, 34))
    b.append(S.clouds(P, [(90, 66, 42, 14, .85), (128, 58, 24, 10, .8), (262, 52, 30, 10, .55)]))
    add(S.hills(P, rng, HORIZON))
    add(S.foliage(P, rng, 470, 112, 36))
    b.insert(len(b) - 1, S.trunk(472, 122, 188, 10))

    gd, gback, gfront = S.meadow(P, rng, HORIZON, avoid=[(160, 250, 90, 60), (318, 262, 90, 40)])
    d.append(gd); b.append(gback)

    ele, rab = F.load('elephant', DENSITY), F.load('rabbit', DENSITY)
    d += [ele[0], rab[0]]

    b.append(S.cast_shadow(P, 154, 280, 78))
    b.append(F.place(ele[1], 150, 280, 262))

    b.append(S.cast_shadow(P, 316, 276, 54))
    b.append(F.place(rab[1], 312, 276, 210))
    # her helmet, hung on the actual crown of the portrait's head
    hx, hy = F.to_scene(125, 118, 312, 276, 210)
    d.append(S.lin(f"{P}-helm", [(0, "#A8E2F4", None), (1, "#3C90AE", None)], x1=1, y1=0, x2=0, y2=1))
    b.append(f'<g transform="rotate(-6 {hx:.0f} {hy:.0f})">'
             f'<path d="M{hx-40:.0f},{hy:.0f} Q{hx-40:.0f},{hy-40:.0f} {hx:.0f},{hy-42:.0f} Q{hx+40:.0f},{hy-40:.0f} {hx+40:.0f},{hy:.0f} Z" fill="url(#{P}-helm)"/>'
             f'<path d="M{hx-14:.0f},{hy-36:.0f} q3,16 0,32 M{hx+14:.0f},{hy-36:.0f} q-3,16 0,32" stroke="#FFFFFF" stroke-width="5" fill="none" opacity=".6"/>'
             f'<rect x="{hx-42:.0f}" y="{hy-5:.0f}" width="84" height="8" rx="4" fill="#2C6E88"/></g>')
    b.append(_bike(P, 322, 282, 1.08))

    # the butterfly that will cause all the trouble, just off Elephant's trunk
    b.append('<g transform="translate(236,150) rotate(12)">'
             '<ellipse cx="-7" cy="-4" rx="9" ry="6.5" fill="#C77DFF" transform="rotate(-24 -7 -4)"/>'
             '<ellipse cx="7" cy="-4" rx="9" ry="6.5" fill="#D9A2FF" transform="rotate(24 7 -4)"/>'
             '<ellipse cx="-5" cy="6" rx="5.5" ry="4.5" fill="#FF9BAE"/><ellipse cx="5" cy="6" rx="5.5" ry="4.5" fill="#FFB3C6"/>'
             '<rect x="-1.6" y="-9" width="3.2" height="17" rx="1.6" fill="#3A2A30"/></g>')

    b.append(gfront)
    add(S.sunwash(P, 420, 78))
    add(S.vignette(P))
    return S.wrap(P, "".join(d), "".join(b))


def _pt(rx, ry, x, ybase, h):
    """A point read off the RENDERED portrait (facing right, as it appears in the
    scene) mapped into the scene - to_scene() takes generator coordinates, which
    are mirrored."""
    return F.to_scene(F.BOX_W - rx, ry, x, ybase, h)


def _gusts(P, pts):
    """White curly wind lines: (x, y, length) each, blowing to the right."""
    return "".join(f'<path d="M{x-l:.0f},{y:.0f} H{x:.0f} q14,0 14,-11 q0,-9 -9,-9 q-7,0 -7,7" stroke="#FFFFFF" '
                   f'stroke-width="3.4" fill="none" stroke-linecap="round" opacity=".85" filter="url(#{P}-b1)"/>'
                   f'<path d="M{x-l*.8:.0f},{y+11:.0f} H{x-l*.2:.0f}" stroke="#FFFFFF" stroke-width="2.6" stroke-linecap="round" opacity=".7"/>'
                   for x, y, l in pts)


def _washing(P, x0, x1, top, ybase):
    """A washing line between two posts, everything on it streaming out sideways
    in the gust - socks, a shirt, a sheet."""
    rope = f'M{x0},{top} Q{(x0+x1)/2:.0f},{top+16} {x1},{top}'
    out = [f'<rect x="{px-3}" y="{top-6}" width="6" height="{ybase-top+6}" rx="2" fill="#8E6842"/>' for px in (x0, x1)]
    out.append(f'<path d="{rope}" stroke="#8A949C" stroke-width="1.6" fill="none"/>')
    for t, kind, col in ((.12, 'sock', "#FF6B6B"), (.3, 'shirt', "#74C8E4"), (.52, 'sheet', "#FFFDF8"), (.8, 'sock', "#FFD166")):
        px = x0 + (x1 - x0)*t
        py = top + 16*2*t*(1-t)
        if kind == 'sock':
            out.append(f'<path d="M{px:.0f},{py-3:.0f} h20 q10,0 10,8 q0,6 -8,6 h-8 v6 q0,4 -5,4 h-9 Z" fill="{col}" '
                       f'transform="rotate(8 {px:.0f} {py:.0f})"/>')
        elif kind == 'shirt':
            out.append(f'<path d="M{px:.0f},{py-2:.0f} l34,-4 l6,8 l-8,4 l-2,-3 l0,22 l-30,4 Z" fill="{col}" opacity=".95"/>')
        else:
            out.append(f'<path d="M{px:.0f},{py-2:.0f} Q{px+30:.0f},{py-12:.0f} {px+62:.0f},{py-6:.0f} Q{px+70:.0f},{py+14:.0f} {px+64:.0f},{py+34:.0f} '
                       f'Q{px+30:.0f},{py+40:.0f} {px+4:.0f},{py+38:.0f} Q{px+8:.0f},{py+18:.0f} {px:.0f},{py-2:.0f} Z" fill="{col}" '
                       f'filter="url(#{P}-b1)"/>'
                       f'<path d="M{px+6:.0f},{py+8:.0f} Q{px+32:.0f},{py+2:.0f} {px+62:.0f},{py+6:.0f}" stroke="#74C8E4" stroke-width="3" fill="none" opacity=".55"/>')
        out.append(f'<rect x="{px-2:.0f}" y="{py-5:.0f}" width="4" height="8" rx="1" fill="#C89A62"/>')
    return "".join(out)


def _straw_hat(P, x, y, rot=0, s=1.0):
    """Rabbit's straw hat, `x, y` the middle of the brim, lit from the upper right."""
    d = S.lin(f"{P}-straw", [(0, "#FBE3A6", None), (1, "#D9AE5C", None)], x1=1, y1=0, x2=0, y2=1)
    return d, (f'<g transform="rotate({rot} {x} {y})">'
               f'<ellipse cx="{x}" cy="{y}" rx="{40*s:.0f}" ry="{9*s:.0f}" fill="url(#{P}-straw)"/>'
               f'<path d="M{x-21*s:.0f},{y-2} Q{x-19*s:.0f},{y-30*s:.0f} {x:.0f},{y-30*s:.0f} Q{x+19*s:.0f},{y-30*s:.0f} {x+21*s:.0f},{y-2} Z" fill="url(#{P}-straw)"/>'
               f'<path d="M{x-20*s:.0f},{y-9*s:.0f} Q{x:.0f},{y-5*s:.0f} {x+20*s:.0f},{y-9*s:.0f}" stroke="#E8533F" stroke-width="{5*s:.1f}" fill="none"/>'
               f'<circle cx="{x+15*s:.0f}" cy="{y-13*s:.0f}" r="{5*s:.1f}" fill="#FFD166"/></g>')


def build_10():
    """The sneezy day: Elephant's ACHOO blowing the washing sideways and Rabbit's
    straw hat clean off her head, with Dr. Sheep looking on."""
    P = "cv10"
    rng = random.Random(1010)
    d, b = [], []
    add = lambda p: (d.append(p[0]), b.append(p[1]))

    add(S.sky(P, 'morning', HORIZON))
    add(S.sun(P, 426, 72, 32))
    b.append(S.clouds(P, [(84, 70, 42, 14, .9), (122, 62, 24, 10, .85), (262, 48, 30, 10, .55)]))
    add(S.hills(P, rng, HORIZON))

    gd, gback, gfront = S.meadow(P, rng, HORIZON, avoid=[(150, 250, 100, 60), (300, 262, 60, 40), (410, 260, 50, 40)])
    d.append(gd); b.append(gback)
    b.append(_washing(P, 214, 470, 120, 196))

    ele, rab, shp = F.load('elephant', DENSITY), F.load('rabbit', DENSITY), F.load('sheep', DENSITY)
    d += [ele[0], rab[0], shp[0]]

    b.append(S.cast_shadow(P, 150, 280, 80))
    b.append(F.place(ele[1], 146, 280, 258))
    b.append(S.cast_shadow(P, 400, 272, 44))
    b.append(F.place(shp[1], 398, 272, 168))
    b.append(S.cast_shadow(P, 290, 278, 52))
    b.append(F.place(rab[1], 288, 278, 204))

    # the sneeze, out of the real trunk tip and off across the meadow
    tx, ty = _pt(211, 310, 146, 280, 258)
    b.append("".join(f'<circle cx="{tx+dx:.0f}" cy="{ty+dy:.0f}" r="{r}" fill="#FFFFFF" opacity=".75" filter="url(#{P}-b1)"/>'
                     for dx, dy, r in ((10, -2, 9), (24, -10, 11), (20, 8, 8), (38, -2, 9))))
    b.append("".join(f'<circle cx="{tx+dx:.0f}" cy="{ty+dy:.0f}" r="{r}" fill="#E8F7FF" stroke="#A8D4E8" stroke-width=".8"/>'
                     for dx, dy, r in ((50, -14, 3), (58, 2, 2.4), (46, -28, 2.6), (64, -20, 2), (40, 12, 2.2))))
    # the hat, blown off the crown of her head and tumbling away on the gust
    hx, hy = F.to_scene(125, 118, 288, 278, 204)
    b.append(_gusts(P, ((hx - 24, hy - 48, 70), (hx + 6, hy - 92, 56), (hx - 70, hy - 4, 50))))
    add(_straw_hat(P, hx + 46, hy - 34, rot=28))
    b.append(f'<path d="M{hx+4:.0f},{hy-6:.0f} q14,-30 34,-30" stroke="#FFFFFF" stroke-width="2.4" fill="none" '
             f'stroke-dasharray="2 6" stroke-linecap="round" opacity=".9"/>')

    b.append(gfront)
    add(S.sunwash(P, 426, 72))
    add(S.vignette(P))
    return S.wrap(P, "".join(d), "".join(b))


def _party_table(P, x, top, w=124):
    """A garden table under a white cloth with a tall pink birthday cake on it."""
    d = (S.lin(f"{P}-cloth", [(0, "#FFFFFF", None), (1, "#E6DDD0", None)], x1=1, y1=0, x2=0, y2=1)
         + S.lin(f"{P}-sponge", [(0, "#F9CB7E", None), (1, "#D08E3C", None)], x1=1, y1=0, x2=0, y2=0)
         + S.lin(f"{P}-icing", [(0, "#FFD0DE", None), (1, "#F08AAA", None)], x1=1, y1=0, x2=0, y2=1))
    out = [S.contact_shadow(P, x, top + 52, w*.6, 7, .35),
           f'<rect x="{x-w/2+10:.0f}" y="{top}" width="7" height="52" fill="#8E6842"/>'
           f'<rect x="{x+w/2-17:.0f}" y="{top}" width="7" height="52" fill="#8E6842"/>',
           f'<path d="M{x-w/2:.0f},{top} H{x+w/2:.0f} L{x+w/2+4:.0f},{top+26} Q{x+w/4:.0f},{top+32} {x:.0f},{top+26} '
           f'Q{x-w/4:.0f},{top+32} {x-w/2-4:.0f},{top+26} Z" fill="url(#{P}-cloth)"/>',
           f'<ellipse cx="{x}" cy="{top-2}" rx="{w*.34:.0f}" ry="5" fill="#FFFFFF"/>']
    x -= w*.16                                # the cake sits left of centre
    for i, (lw, lh) in enumerate(((70, 22), (56, 20), (42, 18))):
        ly = top - 4 - sum(h for _, h in ((70, 22), (56, 20), (42, 18))[:i+1])
        out.append(f'<rect x="{x-lw/2:.0f}" y="{ly:.0f}" width="{lw}" height="{lh}" rx="5" fill="url(#{P}-sponge)"/>'
                   f'<path d="M{x-lw/2:.0f},{ly+7:.0f} V{ly+3:.0f} Q{x-lw/2:.0f},{ly-3:.0f} {x-lw/2+6:.0f},{ly-3:.0f} H{x+lw/2-6:.0f} '
                   f'Q{x+lw/2:.0f},{ly-3:.0f} {x+lw/2:.0f},{ly+3:.0f} V{ly+7:.0f} '
                   + " ".join(f'q{-lw/12:.1f},{8 if k % 2 else 3} {-lw/6:.1f},0' for k in range(6))
                   + f' Z" fill="url(#{P}-icing)"/>')
    ctop = top - 4 - 60
    for i, cx in enumerate((x - 12, x, x + 12)):
        out.append(f'<rect x="{cx-2.5}" y="{ctop-18}" width="5" height="18" rx="1.5" fill="#FFFFFF"/>'
                   f'<path d="M{cx-2.5},{ctop-12} l5,-3 M{cx-2.5},{ctop-5} l5,-3" stroke="#74C8E4" stroke-width="1.4"/>'
                   f'<ellipse cx="{cx}" cy="{ctop-24}" rx="5" ry="8" fill="#FFE39A" opacity=".55" filter="url(#{P}-b1)"/>'
                   f'<path d="M{cx},{ctop-30} q4,6 0,9 q-4,-3 0,-9 Z" fill="#FFB347"/>')
    out.append("".join(f'<circle cx="{x+dx}" cy="{ctop-1}" r="2.6" fill="{c}"/>'
                       for dx, c in ((-16, "#FF6B6B"), (-6, "#74C8E4"), (6, "#FFD166"), (16, "#C77DFF"))))
    return d, "".join(out)


def _bunting(x0, x1, y, sag=30, n=11):
    cols = ("#FF6B6B", "#FFD166", "#74C8E4", "#C77DFF", "#8ECB7E", "#FF9BAE")
    out = [f'<path d="M{x0},{y} Q{(x0+x1)/2:.0f},{y+sag*2} {x1},{y}" stroke="#8A7A62" stroke-width="1.4" fill="none"/>']
    for i in range(n):
        t = (i + .5) / n
        px, py = x0 + (x1-x0)*t, y + sag*2*2*t*(1-t)
        out.append(f'<path d="M{px-9:.0f},{py:.0f} L{px+9:.0f},{py:.0f} L{px:.0f},{py+18:.0f} Z" fill="{cols[i % 6]}" opacity=".95"/>')
    return "".join(out)


def build_11():
    """Bear's birthday: a tall pink cake on a garden table, Bear behind it, Elephant
    and Rabbit either side - and a dusting of flour on Elephant's head that
    gives the first, faster attempt away."""
    P = "cv11"
    rng = random.Random(1111)
    d, b = [], []
    add = lambda p: (d.append(p[0]), b.append(p[1]))

    add(S.sky(P, 'golden', HORIZON))
    add(S.sun(P, 428, 76, 34))
    b.append(S.clouds(P, [(90, 64, 42, 14, .85), (128, 56, 24, 10, .8), (300, 50, 30, 10, .5)]))
    add(S.hills(P, rng, HORIZON))
    add(S.foliage(P, rng, 40, 108, 38))
    b.insert(len(b) - 1, S.trunk(42, 118, 190, 10))
    add(S.foliage(P, rng, 472, 104, 34))
    b.insert(len(b) - 1, S.trunk(474, 114, 190, 10))
    b.append(_bunting(42, 474, 86, sag=28))

    gd, gback, gfront = S.meadow(P, rng, HORIZON, avoid=[(120, 250, 90, 60), (250, 260, 70, 40), (365, 262, 60, 40)])
    d.append(gd); b.append(gback)

    ele, rab, bea = F.load('elephant', DENSITY), F.load('rabbit', DENSITY), F.load('bear', DENSITY)
    d += [ele[0], rab[0], bea[0]]

    # Bear behind the table, beside his cake, the cloth hiding his legs
    b.append(F.place(bea[1], 290, 260, 164))
    add(_party_table(P, 244, 234, w=136))

    b.append(S.cast_shadow(P, 122, 282, 78))
    b.append(F.place(ele[1], 118, 282, 236))
    # flour on his head from the first, rushed go
    fx, fy = _pt(150, 100, 118, 282, 236)
    b.append(f'<ellipse cx="{fx:.0f}" cy="{fy:.0f}" rx="30" ry="9" fill="#FFFFFF" opacity=".85" filter="url(#{P}-b1)"/>'
             + "".join(f'<circle cx="{fx+dx:.0f}" cy="{fy+dy:.0f}" r="{r}" fill="#FFFFFF" opacity=".85"/>'
                       for dx, dy, r in ((-22, 8, 3), (18, 10, 2.6), (4, 14, 2.2), (-8, -12, 2), (26, -6, 1.8))))

    b.append(S.cast_shadow(P, 362, 282, 52))
    b.append(F.place(rab[1], 360, 282, 190))

    b.append(gfront)
    add(S.sunwash(P, 428, 76))
    add(S.vignette(P))
    return S.wrap(P, "".join(d), "".join(b))


def _kite(P, x, y, s=1.0, rot=0):
    """The red diamond kite with its bow-tied tail streaming off to the left."""
    d = S.lin(f"{P}-kite", [(0, "#FF9A8E", None), (1, "#D8403A", None)], x1=1, y1=0, x2=0, y2=1)
    pts = [(x + 6*s + i*15*s, y + 44*s + i*4*s + math.sin(i*1.2)*9*s) for i in range(7)]
    tail = (f'<path d="M{x:.0f},{y+40*s:.0f} ' + " ".join(f'L{px:.0f},{py:.0f}' for px, py in pts)
            + '" stroke="#5E6870" stroke-width="1.4" fill="none"/>'
            + "".join(f'<path d="M{px-4*s:.1f},{py-7*s:.1f} L{px:.1f},{py:.1f} L{px+4*s:.1f},{py-7*s:.1f} Z '
                      f'M{px-4*s:.1f},{py+7*s:.1f} L{px:.1f},{py:.1f} L{px+4*s:.1f},{py+7*s:.1f} Z" fill="{c}"/>'
                      for (px, py), c in zip(pts[1:], ("#FFD166", "#74C8E4", "#C77DFF", "#FFD166", "#74C8E4", "#C77DFF"))))
    return d, (tail + f'<g transform="rotate({rot} {x} {y})">'
               f'<path d="M{x:.0f},{y-34*s:.0f} L{x+26*s:.0f},{y-6*s:.0f} L{x:.0f},{y+40*s:.0f} L{x-26*s:.0f},{y-6*s:.0f} Z" fill="url(#{P}-kite)"/>'
               f'<path d="M{x:.0f},{y-34*s:.0f} L{x+26*s:.0f},{y-6*s:.0f} L{x:.0f},{y-6*s:.0f} Z" fill="#FFFFFF" opacity=".25"/>'
               f'<path d="M{x:.0f},{y-34*s:.0f} V{y+40*s:.0f} M{x-26*s:.0f},{y-6*s:.0f} H{x+26*s:.0f}" stroke="#A8302E" stroke-width="1.6" opacity=".8"/></g>')


def build_12():
    """Kite day: the red kite high in a windy sky, its string running down to
    Rabbit's paw, Elephant and Nurse Giraffe watching it go."""
    P = "cv12"
    rng = random.Random(1212)
    d, b = [], []
    add = lambda p: (d.append(p[0]), b.append(p[1]))

    add(S.sky(P, 'noon', HORIZON))
    add(S.sun(P, 440, 64, 30))
    b.append(S.clouds(P, [(80, 76, 46, 15, .9), (122, 68, 26, 11, .85), (230, 112, 34, 11, .6)]))
    add(S.hills(P, rng, HORIZON))
    b.append(_gusts(P, ((150, 120, 60), (300, 150, 50), (420, 120, 40))))

    gd, gback, gfront = S.meadow(P, rng, HORIZON, avoid=[(130, 250, 90, 60), (250, 250, 50, 40), (350, 262, 60, 40)])
    d.append(gd); b.append(gback)

    ele, rab, gir = F.load('elephant', DENSITY), F.load('rabbit', DENSITY), F.load('giraffe', DENSITY)
    d += [ele[0], rab[0], gir[0]]

    b.append(S.cast_shadow(P, 254, 262, 46))
    b.append(F.place(gir[1], 252, 262, 236))
    b.append(S.cast_shadow(P, 128, 282, 78))
    b.append(F.place(ele[1], 124, 282, 240))
    b.append(S.cast_shadow(P, 352, 282, 52))
    b.append(F.place(rab[1], 350, 282, 194))

    # the string from her front paw up to the kite
    px, py = _pt(167, 318, 350, 282, 194)
    kx, ky = 396, 98
    b.append(f'<path d="M{px:.0f},{py:.0f} Q{px+74:.0f},{(py+ky)/2:.0f} {kx:.0f},{ky:.0f}" stroke="#5A4A3A" stroke-width="1.3" fill="none"/>')
    add(_kite(P, kx, ky, s=1.1, rot=14))
    b.append(S.clouds(P, [(470, 150, 30, 10, .5)]))

    b.append(gfront)
    add(S.sunwash(P, 440, 64))
    add(S.vignette(P))
    return S.wrap(P, "".join(d), "".join(b))


COVERS = {
    '01-the-hungry-friends': build_01,
    '02-ouch-the-big-thorn': build_02,
    '03-snow-much-help': build_03,
    '04-watch-your-step': build_04,
    '05-splash-the-pool-party': build_05,
    '06-bonk-the-bumpy-ride-home': build_06,
    '07-shh-the-noisy-night': build_07,
    '08-hide-and-squeak': build_08,
    '09-wobble-the-big-bike-day': build_09,
    '10-achoo-the-sneezy-day': build_10,
    '11-the-great-big-cake': build_11,
    '12-whoosh-the-kite-day': build_12,
}
