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


COVERS = {
    '01-the-hungry-friends': build_01,
    '02-ouch-the-big-thorn': build_02,
    '03-snow-much-help': build_03,
    '04-watch-your-step': build_04,
    '05-splash-the-pool-party': build_05,
    '06-bonk-the-bumpy-ride-home': build_06,
}
