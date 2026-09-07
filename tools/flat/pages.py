"""One compose function per in-story page, keyed by story slug.

This is to the interior pages what tools/scenes/covers.py is to the covers: the page
art is generated and injected into the story HTML by build_pages.py, so the committed
HTML is still the built output and GitHub Pages needs no build step. Edit the scene
here, never the SVG in the story file - the next build overwrites it.

Each function returns the inside of one <svg viewBox="0 0 500 360">. The horizon sits
at y≈205 and characters are anchored on the ground, so `rabbit(140, 350, ...)` stands
at x=140 with its feet on y=350.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scene as S
from characters import rabbit, elephant, bear, squirrel, giraffe, bandage


# ---------------------------------------------------------------- story 06
def p06_1():
    """Rabbit huffs outside the clinic; Nurse Giraffe overhears from a window."""
    return (S.sky('s6p1', 'tender', sun=None) + S.ground('s6p1')
            + S.hospital()
            + S.window(322, 140, w=34, h=34, dim=True)
            + S.clip('s6p1w', 305, 123, 34, 34,
                     giraffe(322, 196, s=.62, expr='sad', look=(-.55, .2), pose='seated'))
            + S.shadow(400, 348, 44)
            + elephant(400, 348, expr='calm', look=(-.75, .1), trunk=(-40, 54),
                       extra=bandage(18, -14))
            + S.shadow(140, 350, 32)
            + rabbit(140, 350, expr='shout', look=(.55, 0), arm=(-32, -46), arm2=(22, 14),
                     ears=(-16, 19))
            + S.bubble(["We waited FOREVER", "in there today!"], 118, 128, tail=(150, 214)))


def p06_2():
    """The beat of the story: a trunk resting gently on a shoulder."""
    return (S.sky('s6p2', 'golden') + S.ground('s6p2')
            + S.shadow(316, 348, 46)
            + elephant(316, 348, expr='happy', look=(-.7, .1), trunk=(-74, 24))
            + S.shadow(196, 350, 32)
            + rabbit(196, 350, expr='calm', look=(.5, -.1), arm2=(20, 18), ears=(-14, 15))
            + S.bubble(["Hey. I'm okay now.", "Let's get home."], 150, 96, tail=(300, 214)))


def p06_3():
    """The bump. Bear is waving at a friend instead of watching the road."""
    return (S.sky('s6p3', 'tender', sun=None) + S.road(228)
            + S.traffic_light(64, 150, on='red')
            + S.car(96, 246, w=228, riders=(
                rabbit(164, S.seat(246), pose='seated', expr='surprised', look=(.5, 0))
                + elephant(258, S.seat(246) + 4, pose='seated', expr='surprised',
                           look=(.5, 0), trunk=(-26, 34))))
            + S.car(332, 246, w=160, color="#C77DFF", line="#9B4DDB", riders=(
                bear(396, S.seat(246), pose='seated', expr='shout', look=(-.6, -.3),
                     arm=(-30, -36))))
            + '<text x="312" y="182" font-size="27" fill="#FF6B6B" '
              'font-family="Fredoka One, sans-serif" font-weight="700">BONK!</text>')


def p06_4():
    """Everyone carefully helped into an ambulance and driven back."""
    return (S.sky('s6p4', 'tender', sun=None,
                  clouds=((78, 44, 42, 17), (108, 36, 26, 14), (400, 52, 36, 15)))
            + S.hospital(x=352, y=92, w=140, h=112)
            + S.road(222)
            + S.ambulance('s6p4', 62, 232, w=286, h=78, riders=(
                rabbit(120, 302, s=.78, pose='seated', expr='worried', look=(.3, 0))
                + elephant(172, 305, s=.76, pose='seated', expr='worried',
                           look=(-.2, 0), trunk=(-22, 28))
                + bear(222, 302, s=.74, pose='seated', expr='sad', look=(-.4, 0))))
)


def p06_5():
    """Bear resting; Dr. Squirrel treats Elephant's ankle just as carefully."""
    return (S.indoors('s6p5')
            + S.bed(44, 236)
            + bear(80, 264, pose='lie', expr='sleepy', extra=bandage(84, -42, 15, 10))
            + '<ellipse cx="176" cy="282" rx="14" ry="10" fill="#B8E8F8" stroke="#4AA8C8" stroke-width="1.5"/>'
            + S.shadow(330, 342, 40)
            + elephant(330, 342, s=.9, expr='calm', look=(.5, .3), trunk=(-30, 40),
                       extra=bandage(26, -13, 17, 11))
            + S.shadow(424, 344, 24)
            + squirrel(424, 344, s=.92, expr='cross', look=(-.7, .2), arm=(-30, -10))
            + S.bubble(["Let's see how", "THIS one goes."], 404, 88, tail=(424, 250), size=12))


def p06_6():
    """Rabbit's wrist, bandaged gently despite how Dr. Squirrel is feeling."""
    return (S.indoors('s6p6')
            + '<rect x="150" y="272" width="200" height="12" rx="4" fill="#DCD2C0" stroke="#B9AE98" stroke-width="1.5"/>'
            + '<rect x="166" y="284" width="10" height="56" fill="#C8BCA4"/>'
            + '<rect x="324" y="284" width="10" height="56" fill="#C8BCA4"/>'
            + S.shadow(128, 344, 30)
            + rabbit(128, 344, expr='worried', look=(.6, .2), arm2=(56, -6), ears=(-16, 8))
            + bandage(206, 262, 17, 11)
            + S.shadow(292, 344, 24)
            + squirrel(292, 344, expr='calm', look=(-.8, .2), arm=(-48, -16))
            + S.bubble(["Nearly done."], 344, 104, tail=(296, 252), size=12))


def p06_7():
    """The apology. Two beds, and the grumpy feelings melting away."""
    return (S.indoors('s6p7', wall="#F4E7DA")
            + S.bed(28, 240, w=150) + S.bed(316, 240, w=150)
            + rabbit(62, 268, pose='lie', expr='happy', ears=(-74, -48),
                     extra=bandage(56, -44, 13, 9))
            + elephant(348, 268, pose='lie', expr='happy', trunk=(-22, 26))
            + S.shadow(246, 344, 24)
            + squirrel(246, 344, expr='happy', look=(-.4, 0), arm=(-30, -22), arm2=(28, -20))
            + S.bubble(["I'm sorry for how", "I sounded earlier."], 250, 84, tail=(246, 250), size=12))


def p06_8():
    """A huge tray for Elephant, half a glass for Rabbit, and nothing said."""
    return (S.indoors('s6p8')
            + S.bed(24, 240, w=146) + S.bed(300, 240, w=146)
            + rabbit(56, 268, pose='lie', expr='sad', look=(.4, 0), ears=(-74, -48))
            + S.glass(196, 262, full=False)
            + elephant(332, 268, pose='lie', expr='happy', trunk=(-20, 24))
            + S.tray(408, 258, full=True)
            + S.shadow(232, 346, 26)
            + giraffe(232, 346, s=.92, expr='cross', look=(.5, .2), arm=(30, -18))
            + '<text x="104" y="336" text-anchor="middle" font-size="13" fill="#A08A6E" '
              'font-family="Nunito, sans-serif" font-style="italic">…only half a glass.</text>')


def p06_9():
    """Nurse Giraffe comes back, says sorry, and brings a full dinner."""
    return (S.indoors('s6p9', wall="#F4E7DA")
            + S.bed(30, 240, w=150)
            + rabbit(64, 268, pose='lie', expr='surprised', look=(.5, 0), ears=(-70, -44))
            + S.tray(206, 258, full=True)
            + S.shadow(320, 346, 28)
            + giraffe(320, 346, expr='happy', look=(-.6, .2), arm=(-40, -14))
            + S.bubble(["I'm sorry. That", "wasn't fair to you."], 344, 92, tail=(316, 230), size=12))


def p06_10():
    """Healed, waved off, and this time climbing in carefully."""
    return (S.sky('s6p10', 'golden', sun=(432, 56), rays=True) + S.ground('s6p10')
            + S.hospital(x=6, y=68, w=124, h=138)
            + S.shadow(160, 342, 24) + squirrel(160, 342, expr='happy', look=(.6, 0), arm2=(30, -30))
            + S.shadow(214, 344, 26) + giraffe(214, 344, s=.88, expr='happy', look=(.6, 0), arm=(34, -34))
            + S.car(286, 250, w=196, riders=(
                rabbit(340, S.seat(250), pose='seated', expr='happy', look=(-.5, 0))
                + elephant(424, S.seat(250) + 4, pose='seated', expr='happy',
                           look=(-.5, 0), trunk=(-24, 32))))
            + S.bubble(["Bye! Drive safely!"], 254, 108, tail=(206, 246), size=12))


# ---------------------------------------------------------------- story 01
# The running gag is Elephant eating Rabbit's food twice, so the two halves of the
# story deliberately rhyme: p4/p9 are the same crime from the same camera position,
# p5/p10 the same discovery. Keeping the staging parallel is what makes the repeat
# read as a joke rather than as a mistake.
TREE_X, TAP_X = 432, 96


def p01_1():
    """Planting seeds, a sunny morning, the work actually quite fun."""
    return (S.sky('s1p1', 'morning', sun=(438, 54), rays=True) + S.ground('s1p1')
            + S.tree(TREE_X, 232, s=.8)
            + S.seedlings(y=336, xs=(56, 104, 234, 396))
            + S.shadow(178, 348, 32)
            + rabbit(166, 352, s=1.2, expr='excited', look=(.35, .4), arm2=(28, 30))
            + S.shadow(308, 346, 44)
            + elephant(322, 352, s=1.25, expr='happy', look=(-.45, .35), trunk=(-46, 54))
            + S.bubble(["Dig, plop, cover!"], 150, 96, tail=(176, 214), size=13))


def p01_2():
    """Two growling tummies and two very specific orders."""
    return (S.sky('s1p2', 'morning') + S.ground('s1p2')
            + S.tree(TREE_X, 232, s=.8)
            + S.shadow(150, 350, 32)
            + rabbit(148, 352, s=1.2, expr='excited', look=(.45, .1), arm=(-18, 28), arm2=(22, 26))
            + S.shadow(300, 346, 44)
            + elephant(324, 352, s=1.25, expr='happy', look=(-.5, .1), trunk=(-42, 52))
            + S.bubble(["My tummy is", "GROWLING!"], 118, 108, tail=(148, 216))
            + S.thought(["Carrot Halwa!"], 276, 74, (168, 200))
            + S.thought(["Fruit salad!"], 412, 128, (330, 216)))


def p01_3():
    """The order goes in, and then: better wash our hands first."""
    return (S.sky('s1p3', 'morning') + S.ground('s1p3')
            + S.tap(58, 336)
            + S.shadow(322, 346, 44)
            + elephant(330, 352, s=1.25, expr='happy', look=(-.35, .3), trunk=(-58, 30))
            + S.phone(258, 286, s=1.6, tilt=-18)
            + S.shadow(206, 350, 32)
            + rabbit(190, 352, s=1.2, expr='calm', look=(-.6, 0), arm=(-46, -26))
            + S.bubble(["Click, click - ordered!"], 330, 92, tail=(322, 244), size=12)
            + S.bubble(["Wash hands first!"], 150, 150, tail=(190, 250), size=12))


def p01_4():
    """The crime. Rabbit is still at the tap; the halwa bowl is already empty."""
    return (S.sky('s1p4', 'tender', sun=None) + S.ground('s1p4')
            + S.tap(56, 336, running=True)
            + rabbit(126, 344, s=.9, expr='calm', look=(-.5, .2), arm=(-26, 20))
            + S.shadow(300, 346, 46)
            + elephant(336, 352, s=1.25, expr='sneaky', look=(-.55, .25), trunk=(-64, 34))
            + S.parcel(224, 348, s=1.15, open_lid=True)
            + S.bowl(424, 336, 'fruit', s=1.05)
            + S.bubble(["Mmm... the whole", "bowl is gone."], 372, 116, tail=(316, 250), size=12))


def p01_5():
    """Empty. Completely, entirely, totally EMPTY."""
    return (S.sky('s1p5', 'tender', sun=None) + S.ground('s1p5')
            + S.tree(TREE_X, 232, s=.72)
            + S.shadow(184, 350, 34)
            + rabbit(168, 352, s=1.24, expr='surprised', look=(0, .45), arm=(-34, -20), arm2=(34, -18),
                     ears=(-24, 26))
            + S.bowl(172, 306, 'empty', s=1.05)
            + S.shadow(330, 346, 42)
            + elephant(346, 352, s=1.12, expr='guilty', look=(-.72, .25), trunk=(-34, 46))
            + S.bubble(["What happened to my", "Carrot Halwa?"], 250, 96, tail=(196, 232), size=12))


def p01_6():
    """The stare, the drooping ears, and finally the truth."""
    return (S.sky('s1p6', 'tender', sun=None) + S.ground('s1p6')
            + S.tree(TREE_X + 24, 236, s=.78)
            + S.shadow(152, 352, 34)
            + rabbit(152, 352, s=1.24, expr='sad', look=(.55, 0), ears=(-4, 6))
            + S.shadow(340, 352, 50)
            + elephant(340, 352, s=1.25, expr='guilty', look=(-.72, .38), trunk=(-34, 56))
            + S.bubble(["I ate the whole thing.", "I'm really, truly sorry."], 322, 96,
                       tail=(330, 236), size=12))


def p01_7():
    """The fruit bowl pushed across by trunk, and a tiny smile back."""
    return (S.sky('s1p7', 'golden') + S.ground('s1p7')
            + S.tree(TREE_X - 26, 244, s=.95)
            + S.shadow(320, 346, 46)
            + elephant(334, 352, s=1.25, expr='calm', look=(-.72, .25), trunk=(-92, 30))
            + S.bowl(232, 330, 'fruit', s=1.15)
            + S.shadow(146, 350, 32)
            + rabbit(146, 352, s=1.2, expr='calm', look=(.5, .15), arm2=(28, 18))
            + S.bubble(["Please share mine."], 168, 100, tail=(288, 244), size=12))


def p01_8():
    """Next morning: the same order again, one small one for Rabbit."""
    return (S.sky('s1p8', 'morning', sun=(438, 54), rays=True) + S.ground('s1p8')
            + S.seedlings(y=338, xs=(54, 104, 250, 420), sprouted=True)
            + S.shadow(214, 350, 32)
            + rabbit(178, 352, s=1.2, expr='excited', look=(.5, 0), arm=(-28, -34))
            + S.shadow(346, 346, 44)
            + elephant(336, 352, s=1.25, expr='happy', look=(-.5, .28), trunk=(-52, 44))
            + S.phone(266, 288, s=1.6, tilt=16)
            + S.bubble(["Can we order the", "same again today?"], 176, 104, tail=(212, 240), size=12))


def p01_9():
    """The same crime, same camera: this time a pancake goes into her box."""
    return (S.sky('s1p9', 'tender', sun=None) + S.ground('s1p9')
            + S.tap(56, 336, running=True)
            + rabbit(126, 344, s=.9, expr='calm', look=(-.5, .2), arm=(-26, 20))
            + S.shadow(300, 346, 46)
            + elephant(336, 352, s=1.25, expr='sneaky', look=(-.58, .25), trunk=(-66, 32))
            + S.parcel(222, 350, s=1.15, open_lid=True)
            + S.bowl(222, 322, 'pancakes', s=.85)
            + S.bowl(430, 338, 'fruit', s=1.0)
            + S.thought(["...she'll never know."], 386, 116, (330, 248)))


def p01_10():
    """Pancakes. But I ordered a fruit bowl!"""
    return (S.sky('s1p10', 'tender', sun=None) + S.ground('s1p10')
            + S.tree(TREE_X, 232, s=.72)
            + S.shadow(186, 350, 34)
            + rabbit(170, 352, s=1.24, expr='surprised', look=(0, .45), arm=(-34, -18), arm2=(34, -16),
                     ears=(-26, 12))
            + S.bowl(174, 300, 'pancakes', s=.95)
            + S.shadow(334, 346, 42)
            + elephant(348, 352, s=1.12, expr='sneaky', look=(-.72, .25), trunk=(-32, 48))
            + S.bubble(["How did pancakes", "get in here?"], 256, 96, tail=(198, 230), size=12))


def p01_11():
    """AGAIN, Elephant?! A lot of sighing, a lot of trunk-shrugging."""
    return (S.sky('s1p11', 'tender', sun=None) + S.ground('s1p11')
            + S.shadow(150, 350, 32)
            + rabbit(146, 352, s=1.24, expr='shout', look=(.55, -.1), arm=(-34, -56), arm2=(34, -54),
                     ears=(-28, 30))
            + S.shadow(336, 346, 46)
            + elephant(342, 352, s=1.25, expr='guilty', look=(-.72, .22), trunk=(-66, 10))
            + S.bubble(["AGAIN, Elephant?!"], 176, 96, tail=(158, 226))
            + S.bubble(["I don't even like", "pancakes that much!"], 372, 154,
                       tail=(336, 244), size=11))


def p01_12():
    """Half each, under the favourite tree, then fast asleep in the sun."""
    return (S.sky('s1p12', 'golden', sun=(64, 60), rays=True)
            + S.ground('s1p12', flowers=((330, 250), (392, 262), (268, 240)))
            + S.tree(TREE_X - 40, 248, s=1.05)
            + S.shadow(160, 348, 36)
            + rabbit(158, 352, s=1.24, expr='sleepy', pose='sit', ears=(-52, 44))
            + S.shadow(292, 346, 46)
            + elephant(316, 352, s=1.25, expr='sleepy', pose='sit', trunk=(-38, 50))
            + S.bowl(224, 344, 'pancakes', s=.8)
            + S.bowl(408, 346, 'fruit', s=.85)
            + S.zzz(206, 232) + S.zzz(352, 224)
            + '<text x="250" y="76" text-anchor="middle" font-size="15" fill="#C08840" '
              'font-family="Nunito, sans-serif" font-style="italic">Half each - and a nap.</text>')


# ---------------------------------------------------------------- story 05
# The origin story: they meet as strangers and end as best friends, so the two pool
# accidents (p3, p5) are staged identically and only Rabbit's height and temper
# change - the second one is the same joke landing harder.
BIG_POOL, SMALL_POOL = (300, 296), (118, 306)


def p05_1():
    """Two arrivals, one sign, and they have not met yet."""
    return (S.sky('s5p1', 'morning', sun=(444, 52), rays=True) + S.ground('s5p1', y=212)
            + S.sign(250, 150, ["POOL PARTY TODAY!", "All animals welcome"])
            + S.bus(6, 264, w=168, riders=rabbit(96, S.seat(264) - 2, s=.95, pose='seated',
                                                 expr='excited', look=(.5, 0)))
            + S.car(300, 268, w=180, color="#FF6B6B", line="#D94F4F",
                    riders=elephant(392, S.seat(268) + 4, s=1.05,
                                                     pose='seated', expr='happy',
                                                     look=(-.5, 0), trunk=(-26, 34)))
            + '<text x="286" y="252" font-size="16" fill="#FF6B6B" '
              'font-family="Fredoka One, sans-serif">toot!</text>')


def p05_2():
    """The whole sparkling pool, all to herself."""
    return (S.sky('s5p2', 'morning', sun=(60, 56), rays=True) + S.ground('s5p2', y=200)
            + S.pool('s5p2', *BIG_POOL, rx=150, ry=54,
                     swimmers=rabbit(292, S.waterline(296), s=1.05, expr='happy',
                                     look=(.3, 0), arm=(-26, -22), arm2=(26, -20)))
            + S.splash(232, 300, s=.6, big=False)
            + S.bubble(["This pool is all", "mine today!"], 138, 106, tail=(268, 262), size=12))


def p05_3():
    """SPLOOSH. A humongous wave, and one airborne rabbit."""
    return (S.sky('s5p3', 'morning') + S.ground('s5p3', y=200)
            + S.pool('s5p3', *BIG_POOL, rx=150, ry=54,
                     swimmers=elephant(330, S.waterline(296) + 4, s=1.2, expr='excited',
                                       look=(-.4, -.2), trunk=(-40, -18)))
            + S.splash(300, 292, s=1.25)
            + S.spin(-22, 152, 150, rabbit(152, 150, s=.92, expr='surprised',
                                           look=(.2, -.3), arm=(-34, -34), arm2=(34, -32),
                                           ears=(-34, 36)))
            + '<text x="250" y="178" text-anchor="middle" font-size="27" fill="#4AA8C8" '
              'font-family="Fredoka One, sans-serif">SPLOOSH!</text>')


def p05_4():
    """Dripping and grumpy, and a kind suggestion she does not take."""
    return (S.sky('s5p4', 'tender', sun=None) + S.ground('s5p4', y=200)
            + S.pool('s5p4', 330, 300, rx=136, ry=50,
                     swimmers=(rabbit(238, S.waterline(300), s=.95, expr='cross',
                                      look=(.55, -.2), arm=(-24, 10), arm2=(24, 8))
                               + elephant(378, S.waterline(300) + 4, s=1.2, expr='calm',
                                          look=(-.6, .1), trunk=(-56, 8))))
            + S.pool('s5p4b', 74, 318, rx=66, ry=27)
            + S.bubble(["That splash was", "way too big!"], 132, 118, tail=(226, 264), size=12)
            + '<text x="74" y="282" text-anchor="middle" font-size="12" fill="#3C90AE" '
              'font-family="Nunito, sans-serif" font-weight="700">small pool</text>')


def p05_5():
    """The same jump, the same wave, and this time she gets it."""
    return (S.sky('s5p5', 'tender', sun=None) + S.ground('s5p5', y=200)
            + S.pool('s5p5', *BIG_POOL, rx=150, ry=54,
                     swimmers=elephant(330, S.waterline(296) + 4, s=1.2, expr='excited',
                                       look=(-.4, -.2), trunk=(-40, -22)))
            + S.splash(300, 292, s=1.35)
            + S.spin(-16, 146, 108, rabbit(146, 108, s=.92, expr='shout',
                                           look=(.2, .3), arm=(-32, -30), arm2=(32, -28),
                                           ears=(-36, 38)))
            + S.bubble(["Okay, okay -", "I get it now!"], 138, 232, tail=(146, 156), size=12))


def p05_6():
    """Two pools, both the right size for everyone in them."""
    return (S.sky('s5p6', 'morning', sun=(452, 50)) + S.ground('s5p6', y=196)
            + S.pool('s5p6b', 344, 292, rx=142, ry=50,
                     swimmers=(elephant(304, S.waterline(292) + 4, s=1.15, expr='happy',
                                        look=(.4, 0), trunk=(-34, -14))
                               + giraffe(412, S.waterline(292), s=.92, expr='happy',
                                         look=(-.5, 0), cap=False, pose='seated')))
            + S.pool('s5p6a', 108, 318, rx=98, ry=38,
                     swimmers=(rabbit(76, S.waterline(318), s=.86, expr='happy',
                                      look=(.5, 0), arm=(-22, -20))
                               + squirrel(160, S.waterline(318), s=.82, expr='happy',
                                          look=(-.5, 0), coat=False, arm=(-22, -18))))
            + S.splash(146, 320, s=.55, big=False) + S.splash(330, 294, s=.7, big=False))


def p05_7():
    """Two apologies in the lunch queue."""
    return (S.sky('s5p7', 'golden') + S.ground('s5p7')
            + S.sign(452, 196, ["LUNCH"], w=88, color="#E8892E")
            + S.shadow(168, 352, 34)
            + rabbit(168, 352, s=1.2, expr='guilty', look=(.55, 0), arm2=(26, 14))
            + S.shadow(324, 352, 50)
            + elephant(324, 352, s=1.25, expr='guilty', look=(-.7, .2), trunk=(-52, 30))
            + S.bubble(["I'm sorry I didn't listen."], 158, 92, tail=(172, 226), size=11)
            + S.bubble(["And I'm sorry about", "my splashes."], 366, 132, tail=(326, 240), size=11))


def p05_8():
    """Lunch, then tennis, then basketball - the best day."""
    return (S.sky('s5p8', 'golden') + S.ground('s5p8')
            + S.table(250, 288)
            + S.shadow(150, 352, 34)
            + rabbit(150, 352, s=1.2, expr='happy', look=(.5, .1), arm2=(30, -34))
            + S.shadow(352, 352, 50)
            + elephant(352, 352, s=1.25, expr='happy', look=(-.6, .1), trunk=(-44, 26))
            + S.bowl(214, 282, 'fruit', s=.8) + S.bowl(300, 282, 'pancakes', s=.62)
            + S.shadow(70, 340, 20) + S.ball(70, 322, 'basket', r=18)
            + S.shadow(446, 344, 14) + S.ball(446, 332, 'tennis', r=16)
            + S.bubble(["Best day ever!"], 250, 78, tail=(180, 216), size=12))


def p05_9():
    """A lift home at sunset, and a friendship that starts here."""
    return (S.sky('s5p9', 'sunset', sun=(72, 74), rays=True) + S.ground('s5p9')
            + S.tree(452, 252, s=.9)
            + '<ellipse cx="212" cy="344" rx="54" ry="26" fill="#8A6A44"/>'
              '<ellipse cx="212" cy="348" rx="40" ry="19" fill="#5C4426"/>'
            + '<text x="212" y="300" text-anchor="middle" font-size="12" fill="#7A5A34" '
              'font-family="Nunito, sans-serif" font-weight="700">Rabbit\'s burrow</text>'
            + S.car(268, 262, w=190, color="#FF6B6B", line="#D94F4F", riders=(
                rabbit(322, S.seat(262), s=1.0, pose='seated', expr='happy', look=(-.5, 0))
                + elephant(404, S.seat(262) + 4, s=1.1, pose='seated', expr='happy',
                           look=(-.5, 0), trunk=(-26, 32))))
            + S.bubble(["Best friends, from", "that day on."], 150, 122, tail=(228, 300), size=12))


# ---------------------------------------------------------------- story 02
# The truck is the spine of this one: it carries Elephant to hospital on p4 and home
# again on p10, so those two pages are the same shot with the weather and his face
# changed - anxious under a pale sky, then beaming in the golden light.
def p02_1():
    """Rabbit mid-story, arms going; Elephant listening to every word."""
    return (S.sky('s2p1', 'morning', sun=(444, 52), rays=True) + S.ground('s2p1')
            + S.road(258)
            + S.shadow(160, 340, 34)
            + rabbit(160, 340, s=1.2, expr='excited', look=(.5, -.1),
                     arm=(-34, -40), arm2=(34, -30), ears=(-22, 24))
            + S.shadow(330, 340, 50)
            + elephant(330, 340, s=1.25, expr='happy', look=(-.7, 0), trunk=(-40, 42))
            + S.bubble(["...and THEN, guess", "what happened!"], 154, 92, tail=(166, 214), size=12))


def p02_2():
    """Neither of them saw it. OUCH."""
    return (S.sky('s2p2', 'tender', sun=None) + S.ground('s2p2')
            + S.road(258)
            + S.shadow(146, 342, 32)
            + rabbit(146, 342, s=1.15, expr='surprised', look=(.6, .2), arm=(-26, -20), ears=(-24, 26))
            + S.shadow(322, 344, 52)
            + elephant(322, 344, s=1.25, pose='sit', expr='hurt', look=(-.3, .5), trunk=(-46, 26))
            + S.thorn(228, 326, s=2.1, rot=16)
            + '<text x="406" y="212" text-anchor="middle" font-size="30" fill="#FF6B6B" '
              'font-family="Fredoka One, sans-serif">OOOH!</text>')


def p02_3():
    """Don't move! I'll get help! - and she runs like never before."""
    return (S.sky('s2p3', 'tender', sun=None) + S.ground('s2p3')
            + S.road(258)
            + S.shadow(356, 344, 52)
            + elephant(356, 344, s=1.2, pose='sit', expr='hurt', look=(-.6, .3), trunk=(-40, 30))
            + S.thorn(286, 328, s=1.7, rot=14)
            + S.speedlines(96, 300, n=5, length=54)
            + S.shadow(154, 342, 32)
            + rabbit(154, 342, s=1.2, expr='shout', look=(-.55, 0),
                     arm=(-40, -14), arm2=(36, 22), ears=(38, 42))
            + S.bubble(["Don't move -", "I'll get help!"], 176, 96, tail=(160, 214), size=12))


def p02_4():
    """A tiny cab, an enormous cargo bay, and FULL SPEED to the hospital."""
    return (S.sky('s2p4', 'tender', sun=None) + S.ground('s2p4')
            + S.road(250)
            + S.truck('s2p4', 74, 320, w=316,
                      cargo_riders=elephant(176, S.cargo_seat(320, .98), s=.98, expr='hurt',
                                            look=(.4, .2), trunk=(-34, 30)),
                      cab_riders=rabbit(322, S.cab_seat(320, .72), s=.72, expr='shout', look=(.5, 0)))
            + S.speedlines(40, 292, n=5, length=44)
            + '<text x="396" y="172" text-anchor="middle" font-size="19" fill="#FF6B6B" '
              'font-family="Fredoka One, sans-serif">FULL SPEED!</text>')


def p02_5():
    """Dr. Squirrel comes out at a run the moment she hears the truck."""
    return (S.sky('s2p5', 'morning') + S.ground('s2p5')
            + S.hospital(x=286, y=64, w=196, h=140)
            + S.truck('s2p5', 8, 322, w=250, color="#74C8E4",
                      cargo_riders=elephant(88, S.cargo_seat(322, .82), s=.82, expr='hurt',
                                            look=(.5, .2), trunk=(-30, 26)),
                      cab_riders=rabbit(200, S.cab_seat(322, .68), s=.68, expr='worried', look=(.5, 0)))
            + S.shadow(322, 348, 24)
            + squirrel(322, 348, s=1.0, expr='shout', look=(-.7, 0), arm=(-40, -20), arm2=(30, 18))
            + S.bubble(["Emergency!", "Right this way!"], 380, 214, tail=(330, 268), size=12))


def p02_6():
    """POP! Even Dr. Squirrel raises her eyebrows at the size of it."""
    return (S.indoors('s2p6')
            + S.bed(36, 240, w=176)
            + elephant(74, 268, pose='lie', expr='hurt', trunk=(-24, 26),
                       extra=bandage(150, -40, 16, 11))
            + S.shadow(346, 346, 26)
            + squirrel(346, 346, s=1.1, expr='surprised', look=(-.7, .1), arm=(-46, -30))
            + S.tweezers(292, 274, s=1.7, rot=-38,
                         holding=S.thorn(272, 232, s=1.7, rot=-38))
            + '<text x="252" y="130" text-anchor="middle" font-size="26" fill="#FF6B6B" '
              'font-family="Fredoka One, sans-serif">POP!</text>'
            + S.bubble(["It was enormous!"], 402, 108, tail=(352, 250), size=11))


def p02_7():
    """A cosy ward, a garden view, and three days of no adventures."""
    return (S.indoors('s2p7', wall="#F4E7DA")
            + S.garden_window(96, 132, w=104, h=84)
            + S.bed(40, 246, w=182)
            + elephant(78, 274, pose='lie', expr='calm', trunk=(-24, 26),
                       extra=bandage(154, -38, 16, 11))
            + S.shadow(348, 346, 26)
            + squirrel(348, 346, s=1.1, expr='calm', look=(-.7, .1), arm=(-38, -22))
            + S.clipboard(292, 276, s=1.1, tilt=-12)
            + S.bubble(["Three days of rest -", "no adventures!"], 366, 116,
                       tail=(352, 252), size=11))


def p02_8():
    """Day 3, and the silly stories nearly shake the bandage loose."""
    return (S.indoors('s2p8', wall="#F4E7DA")
            + S.garden_window(432, 128, w=90, h=74)
            + S.bed(52, 244, w=190)
            + elephant(90, 272, pose='lie', expr='happy', trunk=(-26, 24),
                       extra=bandage(160, -38, 16, 11))
            + S.shadow(316, 348, 34)
            + rabbit(316, 348, s=1.2, expr='excited', look=(-.55, -.1),
                     arm=(-38, -40), arm2=(34, -28), ears=(-24, 26))
            + S.books(258, 344) + S.bowl(376, 336, 'fruit', s=.8)
            + S.bubble(["...and then the", "carrot ran away!"], 300, 96, tail=(310, 226), size=11))


def p02_9():
    """All healed up - and a great many thank-yous."""
    return (S.indoors('s2p9', wall="#F4E7DA")
            + S.garden_window(438, 126, w=88, h=72)
            + S.shadow(140, 348, 34)
            + rabbit(140, 348, s=1.2, expr='happy', look=(.5, 0), arm=(-30, -36))
            + S.shadow(296, 348, 50)
            + elephant(296, 348, s=1.25, expr='happy', look=(.4, .1), trunk=(-40, 40),
                       extra=bandage(30, -14, 15, 10))
            + S.shadow(412, 348, 26)
            + squirrel(412, 348, s=1.1, expr='happy', look=(-.6, 0), arm=(-34, -26))
            + S.bubble(["You're all healed up!"], 300, 82, tail=(404, 250), size=12))


def p02_10():
    """The same truck, the same road - and a very different face."""
    return (S.sky('s2p10', 'golden', sun=(454, 56), rays=True) + S.ground('s2p10')
            + S.road(250)
            + S.truck('s2p10', 74, 320, w=316,
                      cargo_riders=elephant(176, S.cargo_seat(320, .98), s=.98, expr='happy',
                                            look=(.4, .1), trunk=(-34, 26)),
                      cab_riders=rabbit(322, S.cab_seat(320, .72), s=.72, expr='happy', look=(.5, 0)))
            + S.bubble(["No more thorns."], 148, 128, tail=(196, 246), size=12))


PAGES = {
    '02-ouch-the-big-thorn': [p02_1, p02_2, p02_3, p02_4, p02_5,
                              p02_6, p02_7, p02_8, p02_9, p02_10],
    '05-splash-the-pool-party': [p05_1, p05_2, p05_3, p05_4, p05_5, p05_6, p05_7, p05_8, p05_9],
    '01-the-hungry-friends': [p01_1, p01_2, p01_3, p01_4, p01_5, p01_6,
                              p01_7, p01_8, p01_9, p01_10, p01_11, p01_12],
    '06-bonk-the-bumpy-ride-home': [p06_1, p06_2, p06_3, p06_4, p06_5,
                                    p06_6, p06_7, p06_8, p06_9, p06_10],
}
