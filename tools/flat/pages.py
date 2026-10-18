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
from characters import (rabbit, elephant, bear, squirrel, giraffe, sheep, critter, tortoise, bandage,
                        E_BODY, E_LINE, R_BODY, R_LINE, R_EAR, N_BODY, N_LINE, S_SCOPE, S_FACE, S_FLINE, S_DARK, _limb)


def alt(text):
    """What a screen reader says for the page's picture: who is in it and what they
    are doing. The docstring below it is a note for whoever edits the page - it names
    the story beat, which is not the same thing as describing the picture."""
    def mark(fn):
        fn.alt = text
        return fn
    return mark


# ---------------------------------------------------------------- story 06
@alt('Outside the clinic, Rabbit stomps and complains while bandaged Elephant stands calmly and Nurse Giraffe looks out of a window.')
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


@alt("Elephant gently rests his trunk on Rabbit's shoulder, and she smiles.")
def p06_2():
    """The beat of the story: a trunk resting gently on a shoulder."""
    return (S.sky('s6p2', 'golden') + S.ground('s6p2')
            + S.shadow(316, 348, 46)
            + elephant(316, 348, expr='happy', look=(-.7, .1), trunk=(-74, 24))
            + S.shadow(196, 350, 32)
            + rabbit(196, 350, expr='calm', look=(.5, -.1), arm2=(20, 18), ears=(-14, 15))
            + S.bubble(["Hey. I'm okay now.", "Let's get home."], 286, 96, tail=(316, 200)))


@alt('At a red light, a purple car driven by Bear bumps into the yellow car carrying Rabbit and Elephant. BONK!')
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


@alt('An ambulance carries Rabbit, Elephant and Bear back to the hospital.')
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


@alt("Bear sleeps in a hospital bed with a bandaged arm while a frowning Dr. Squirrel treats Elephant's ankle.")
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


@alt("Dr. Squirrel bandages Rabbit's wrist across a table, looking grumpy, while Rabbit looks worried.")
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


@alt('Rabbit and Elephant lie in two hospital beds while Dr. Squirrel stands between them, saying sorry.')
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


@alt('A cross Nurse Giraffe brings Elephant a big tray of dinner, while Rabbit, sad in her bed, has only half a glass.')
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


@alt("Nurse Giraffe comes back to Rabbit's bed with a full dinner tray and says sorry.")
def p06_9():
    """Nurse Giraffe comes back, says sorry, and brings a full dinner."""
    return (S.indoors('s6p9', wall="#F4E7DA")
            + S.bed(30, 240, w=150)
            + rabbit(64, 268, pose='lie', expr='surprised', look=(.5, 0), ears=(-70, -44))
            + S.tray(206, 258, full=True)
            + S.shadow(320, 346, 28)
            + giraffe(320, 346, expr='happy', look=(-.6, .2), arm=(-40, -14))
            + S.bubble(["I'm sorry. That", "wasn't fair to you."], 344, 92, tail=(316, 230), size=12))


@alt('Healed, Rabbit and Elephant sit in their yellow car outside the hospital as Dr. Squirrel and Nurse Giraffe wave goodbye.')
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


@alt('Rabbit and Elephant stand in a sunny field beside freshly dug seed holes, Rabbit calling out happily.')
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


@alt('In the field, Rabbit shouts about her growling tummy while she dreams of carrot halwa and Elephant dreams of fruit salad.')
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


@alt('Elephant holds up a phone to order lunch while Rabbit points toward the garden tap.')
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


@alt('While Rabbit washes her paws at the tap, Elephant grins slyly beside the open delivery box.')
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


@alt('Rabbit holds up an empty bowl in shock while Elephant looks away guiltily.')
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


@alt('Rabbit stares sadly at Elephant, who owns up with a guilty face.')
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


@alt('Elephant slides his fruit bowl across to Rabbit with his trunk, and Rabbit gives a small smile.')
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


@alt('Next morning in the field, Rabbit asks for the same order again while Elephant holds the phone.')
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


@alt('Rabbit is back at the tap while Elephant, looking sneaky, slips pancakes into her delivery box.')
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


@alt('Rabbit holds up a bowl of pancakes, puzzled, while Elephant watches with a sly look.')
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


@alt('Rabbit throws her paws up in exasperation while Elephant shrugs.')
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


@alt('Rabbit and Elephant nap side by side under their favourite tree in the golden sunshine, their bowls beside them.')
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


@alt('Rabbit arrives on a yellow bus and Elephant in a red car, beside a sign saying Pool Party Today.')
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


@alt('Rabbit stands alone in the middle of a sparkling pool, arms spread wide.')
def p05_2():
    """The whole sparkling pool, all to herself."""
    return (S.sky('s5p2', 'morning', sun=(60, 56), rays=True) + S.ground('s5p2', y=200)
            + S.pool('s5p2', *BIG_POOL, rx=150, ry=54,
                     swimmers=rabbit(292, S.waterline(296), s=1.05, expr='happy',
                                     look=(.3, 0), arm=(-26, -22), arm2=(26, -20)))
            + S.splash(232, 300, s=.6, big=False)
            + S.bubble(["This pool is all", "mine today!"], 138, 106, tail=(268, 262), size=12))


@alt('Elephant lands in the pool with a huge SPLOOSH, and the wave sends Rabbit flying into the air.')
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


@alt('Rabbit stands dripping and cross in the big pool while Elephant points his trunk at a smaller pool nearby.')
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


@alt('Elephant splashes again and Rabbit flies up once more, this time laughing that she gets it.')
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


@alt('Rabbit and Dr. Squirrel play in the small pool while Elephant and Nurse Giraffe share the big one.')
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


@alt('Rabbit and Elephant say sorry to each other beside the lunch sign.')
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


@alt('Rabbit and Elephant share lunch at a table, with a basketball and a tennis ball ready for later.')
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


@alt('At sunset, Elephant drives Rabbit home to her burrow in a red car.')
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
@alt('On the road, Rabbit waves her arms as she tells a story while Elephant listens with a big smile.')
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


@alt('Elephant steps on a huge brown thorn and cries out, while Rabbit gasps.')
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


@alt('Rabbit gets ready to run for help while Elephant winces beside the thorn.')
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


@alt('Elephant rides in the open back of a small blue truck as Rabbit drives at full speed to the hospital.')
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


@alt('The truck pulls up at the hospital and Dr. Squirrel hurries out to meet it.')
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


@alt('Elephant lies in a hospital bed as Dr. Squirrel holds up the enormous thorn in her long tweezers.')
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


@alt('Elephant rests in bed with a bandaged foot while Dr. Squirrel, holding a clipboard, checks on him.')
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


@alt("Rabbit tells silly stories at Elephant's bedside, with books and a bowl of fruit nearby, while he laughs.")
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


@alt('Elephant stands healed and smiling between Rabbit and Dr. Squirrel.')
def p02_9():
    """All healed up - and a great many thank-yous."""
    return (S.indoors('s2p9', wall="#F4E7DA")
            + S.garden_window(62, 118, w=88, h=72)
            + S.shadow(140, 348, 34)
            + rabbit(140, 348, s=1.2, expr='happy', look=(.5, 0), arm=(-30, -36))
            + S.shadow(296, 348, 50)
            + elephant(296, 348, s=1.25, expr='happy', look=(.4, .1), trunk=(-40, 40),
                       extra=bandage(30, -14, 15, 10))
            + S.shadow(412, 348, 26)
            + squirrel(412, 348, s=1.1, expr='happy', look=(-.6, 0), arm=(-34, -26))
            + S.bubble(["You're all healed up!"], 382, 106, tail=(412, 236), size=12))


@alt('Elephant rides home happily in the back of the truck, with Rabbit driving, on a golden afternoon.')
def p02_10():
    """The same truck, the same road - and a very different face."""
    return (S.sky('s2p10', 'golden', sun=(454, 56), rays=True) + S.ground('s2p10')
            + S.road(250)
            + S.truck('s2p10', 74, 320, w=316,
                      cargo_riders=elephant(176, S.cargo_seat(320, .98), s=.98, expr='happy',
                                            look=(.4, .1), trunk=(-34, 26)),
                      cab_riders=rabbit(322, S.cab_seat(320, .72), s=.72, expr='happy', look=(.5, 0)))
            + S.bubble(["No more thorns."], 148, 128, tail=(196, 246), size=12))



# ---------------------------------------------------------------- story 04
# The field is the same field on p1, p9 and p12 - same fence, same rows - so the last
# page reads as "back where it started, but careful now".
def _field04(uid, mood='morning', sun=(440, 56), rays=False):
    return (S.sky(uid, mood, sun=sun, rays=rays) + S.ground(uid)
            + S.fence(300, 496, 236, h=40)
            + S.dirt(150, 318, 120, 16) + S.dirt(360, 334, 110, 14))


def _foot(dx, dy=-10):
    """Elephant's leg stuck out in front while he sits - the one the thorn is in. The
    leg matters: a foot on its own, a body-width away, reads as a stray blob."""
    leg = f'M{dx*.3:.0f},{dy-14} Q{dx*.7:.0f},{dy-10} {dx:.0f},{dy}'
    return (f'<path d="{leg}" stroke="{E_LINE}" stroke-width="27" fill="none" stroke-linecap="round"/>'
            f'<path d="{leg}" stroke="{E_BODY}" stroke-width="24" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="{dx}" cy="{dy}" rx="22" ry="13" fill="{E_BODY}" stroke="{E_LINE}" stroke-width="1.5"/>'
            + "".join(f'<ellipse cx="{dx+ox}" cy="{dy+5}" rx="3.2" ry="2.4" fill="#E8EEF2"/>' for ox in (-9, 0, 9)))


def _pow(x, y, r=16, color="#FFD166"):
    """A little impact star."""
    import math
    pts = " ".join(f'{x + math.cos(i*math.pi/6)*(r if i % 2 == 0 else r*.45):.0f},'
                   f'{y + math.sin(i*math.pi/6)*(r if i % 2 == 0 else r*.45):.0f}' for i in range(12))
    return f'<polygon points="{pts}" fill="{color}" opacity=".9"/>'


def _shout(text, x, y, size=30, rot=-6, color="#FF6B6B"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="middle" '
            f'font-family="Fredoka One, sans-serif" transform="rotate({rot} {x} {y})">{text}</text>')


@alt('In a sunny field, Rabbit plants seeds and chats with Elephant, who looks at her instead of at the thorn by his foot.')
def p04_1():
    """Planting and chatting about lunch - and Elephant is not looking down."""
    return (_field04('s4p1', rays=True)
            + S.seedlings(y=320, xs=(60, 104, 150, 196))
            + S.thorn(404, 342, s=.7)
            + S.shadow(140, 350, 34)
            + rabbit(140, 352, s=1.2, pose='sit', expr='excited', look=(.5, -.1),
                     arm=(-16, 30), arm2=(30, -20))
            + S.shadow(330, 348, 46)
            + elephant(330, 352, s=1.25, expr='happy', look=(-.65, -.1), trunk=(-44, 30))
            + S.bubble(["Noodles for", "lunch today?"], 116, 118, tail=(138, 222), size=13)
            + S.bubble(["Or maybe...", "samosas?"], 314, 76, tail=(318, 170), size=13))


@alt('Elephant steps on a giant thorn and cries out, as birds scatter from a tree and Rabbit throws up her paws.')
def p04_2():
    """CRUNCH. A big foot, a giant thorn, and every bird in the tree takes off."""
    return (_field04('s4p2', mood='tender', sun=None)
            + S.tree(62, 226, s=.8)
            + S.birds(((104, 92), (130, 70), (160, 84), (150, 52)))
            + S.shadow(160, 350, 32)
            + rabbit(160, 352, s=1.2, expr='surprised', look=(.6, 0), arm=(-30, -40), arm2=(30, -40),
                     ears=(-20, 22))
            + S.shadow(344, 348, 46)
            + _pow(380, 334, 34) + _pow(410, 312, 12, "#FF9BAE")
            + elephant(344, 352, s=1.25, expr='hurt', trunk=(-20, -30))
            + S.thorn(398, 330, s=1.1, rot=38)
            + _shout("OWWW!", 350, 72, size=40))


@alt('Elephant sits stuck with the thorn in his foot, its roots reaching deep underground, while Rabbit looks on, worried.')
def p04_3():
    """Stuck. The roots go down and down, and he can only sit where he is."""
    return (_field04('s4p3', mood='tender', sun=None)
            + S.roots(262, 290, depth=64)
            + S.shadow(360, 294, 50)
            + elephant(360, 300, s=1.2, pose='sit', expr='sad', look=(-.5, .5), trunk=(-18, 44),
                       extra=_foot(-82, -8))
            + S.thorn(262, 292, s=.55)
            + S.shadow(120, 298, 30)
            + rabbit(120, 300, s=1.1, expr='worried', look=(.6, .2), arm=(-20, -30), arm2=(38, -8))
            + S.bubble(["I can't move,", "not even a little."], 314, 62, tail=(340, 150), size=13))


@alt('Rabbit shouts into an old crank telephone by the fence while Elephant sits stuck far across the field.')
def p04_4():
    """The old telephone by the fence, cranked as fast as her paws can go."""
    return (S.sky('s4p4', 'tender', sun=None) + S.ground('s4p4')
            + S.fence(260, 496, 236, h=40)
            + S.dirt(96, 256, 60, 8)
            + elephant(96, 262, s=.5, pose='sit', expr='sad', trunk=(-16, 30))
            + S.crank_phone(410, 350, receiver=(334, 216))
            + S.shadow(320, 350, 32)
            + rabbit(320, 352, s=1.2, expr='shout', look=(.4, 0), arm=(10, -62), arm2=(60, -24),
                     ears=(-18, 18))
            + S.bubble(["Dr. Sheep!", "Elephant's stuck!", "Please come quick!"], 172, 104,
                       tail=(300, 196), size=13))


@alt("Dr. Sheep kneels beside Elephant's stuck foot, frowning at the deep roots, while Rabbit looks puzzled.")
def p04_5():
    """Dr. Sheep kneels by the foot and frowns: this needs a digger."""
    return (_field04('s4p5', sun=(60, 56))
            + S.roots(276, 290, depth=64)
            + S.shadow(390, 294, 50)
            + elephant(390, 300, s=1.15, pose='sit', expr='hurt', look=(-.5, .4), trunk=(-24, 40),
                       extra=_foot(-98, -8))
            + S.thorn(276, 292, s=.55)
            + S.shadow(196, 300, 34)
            + sheep(196, 302, s=1.1, pose='sit', expr='worried', look=(.6, .5), arm2=(40, 8))
            + S.shadow(66, 300, 26)
            + rabbit(66, 302, s=1.0, expr='surprised', look=(.6, 0), arm2=(20, -24))
            + S.bubble(["These roots go too", "deep to pull out.", "We need a JCB!"], 262, 62,
                       tail=(206, 190), size=13)
            + S.bubble(["A what-now?"], 78, 112, tail=(70, 170), size=11))


@alt("Dr. Sheep drives a yellow digger that scoops around Elephant's foot and snips through the thorn's roots.")
def p04_6():
    """Scoop! Scoop! Scoop! - and snip, right through the roots."""
    return (_field04('s4p6')
            + S.roots(318, 296, depth=62, cut=True)
            + '<ellipse cx="236" cy="300" rx="30" ry="9" fill="#8A6A44"/>'
            + S.shadow(420, 298, 48)
            + elephant(420, 304, s=1.1, pose='sit', expr='surprised', look=(-.6, .5), trunk=(-20, 40),
                       extra=_foot(-92, -8))
            + S.digger('s4p6', 14, 318, w=170, bucket=(262, 300), bw=78,
                       cab_riders=sheep(72, S.digger_cab(318, .7), s=.7, pose='seated',
                                        expr='calm', look=(.5, .3)))
            + _shout("SCOOP!", 196, 94, size=28) + _shout("SNIP!", 372, 350, size=20, rot=8, color="#FFD166"))


@alt("Elephant and Rabbit ride in the digger's bucket as Dr. Sheep drives them down the road to the hospital.")
def p04_7():
    """Off to the hospital - Elephant riding in the bucket, Rabbit riding with him."""
    riders = (elephant(318, 262, s=.82, pose='sit', expr='excited', look=(.5, -.2), trunk=(30, -30))
              + rabbit(376, 256, s=.66, pose='sit', expr='happy', look=(-.5, 0), arm=(-22, -26)))
    return (S.sky('s4p7', 'morning', sun=(66, 54)) + S.ground('s4p7') + S.road(246)
            + S.sign(452, 190, ["H", "&#8594;"], w=40, color="#E4453F")
            + S.digger('s4p7', 30, 330, w=190, bucket=(340, 278), bw=132, bucket_riders=riders,
                       cab_riders=sheep(92, S.digger_cab(330, .7), s=.7, pose='seated',
                                        expr='happy', look=(.5, 0)))
            + S.speedlines(20, 246, back=True))


@alt('Elephant smiles from his hospital bed as Dr. Sheep pulls the last tiny piece of thorn from his foot with tweezers.')
def p04_8():
    """Tiny tweezers, the very last piece of thorn, and a whole week of rest."""
    return (S.indoors('s4p8', wall="#EEF4F7")
            + S.garden_window(96, 116, w=96, h=76)
            + S.bed(52, 244, w=200)
            + elephant(90, 272, pose='lie', expr='calm', look=(.5, 0), trunk=(-26, 24),
                       extra=_foot(128, -26))
            + S.shadow(360, 348, 38)
            + sheep(330, 350, s=1.2, expr='happy', look=(-.6, .3), arm=(-50, -26))
            + S.tweezers(248, 244, s=.8, rot=90)
            + S.thorn(224, 244, s=.3, rot=-90)
            + S.bubble(["All done!", "Now rest for a week."], 344, 104, tail=(334, 200), size=13))


@alt('Rabbit plants alone in the field, daydreaming about Elephant in his hospital bed, and does not see a thorn by her feet.')
def p04_9():
    """Planting alone, thinking about her friend - and not about her feet."""
    dream = (f'<g transform="translate(294 62) scale(.42)">'
             + S.bed(-10, 40, w=190) + elephant(28, 68, pose='lie', expr='sleepy', trunk=(-20, 20))
             + '</g>')
    return (_field04('s4p9', mood='tender', sun=None)
            + S.seedlings(y=320, xs=(60, 104, 150, 196), sprouted=True)
            + S.thorn(234, 346, s=.5)
            + S.shadow(160, 350, 32)
            + rabbit(160, 352, s=1.2, expr='sad', look=(.4, -.6), arm2=(26, 24), ears=(-4, 8))
            + S.thought([], 340, 88, (196, 206), picture=dream, rx=78, ry=48))


@alt('Rabbit hops toward the telephone on one foot, crying out, after stepping on a small thorn.')
def p04_10():
    """CRUNCH, again. Ow, ow, ow - all the way to the telephone."""
    return (_field04('s4p10', mood='tender', sun=None)
            + S.thorn(92, 346, s=.5) + _pow(92, 340, 12)
            + "".join(f'<path d="M{x0},342 Q{x0+32},{286} {x0+64},330" stroke="#B9C8D0" stroke-width="2.5" '
                      f'fill="none" stroke-dasharray="4 6" stroke-linecap="round"/>' for x0 in (100, 164))
            + S.crank_phone(430, 350)
            + S.shadow(262, 350, 26)
            + S.spin(-10, 262, 330, rabbit(262, 330, s=1.2, expr='hurt', look=(-.4, .5),
                                           arm=(-30, -40), arm2=(30, -40), ears=(-24, 26)))
            + S.bubble(["Ow, ow, ow!"], 268, 82, tail=(262, 170), size=14))


@alt("Dr. Sheep kneels and plucks the tiny thorn from Rabbit's foot, with her car parked nearby.")
def p04_11():
    """No digger needed: one small thorn, two hooves, done in seconds."""
    return (_field04('s4p11', mood='golden', sun=(66, 54))
            + S.car(318, 262, w=164, color="#74C8E4", line="#3C90AE")
            + '<rect x="386" y="276" width="7" height="22" rx="1" fill="#E4453F"/>'
              '<rect x="379" y="283" width="21" height="7" rx="1" fill="#E4453F"/>'
            + S.shadow(128, 350, 30)
            + rabbit(128, 352, s=1.2, pose='sit', expr='worried', look=(.6, .3), arm2=(20, -34),
                     extra=f'<ellipse cx="42" cy="-6" rx="17" ry="10" fill="{R_BODY}" stroke="{R_LINE}" '
                           f'stroke-width="1.5" transform="rotate(-8 42 -6)"/>')
            + S.shadow(256, 350, 34)
            + sheep(256, 352, s=1.15, pose='sit', expr='happy', look=(-.6, .3), arm=(-36, 10))
            + S.thorn(190, 310, s=.4, rot=-20)
            + S.bubble(["Elephant is enormous -", "he needed a digger.", "You're little. I've got this!"],
                       256, 88, tail=(252, 236), size=12))


@alt('Back in the field, Rabbit and Elephant plant seeds side by side, both looking carefully down at their feet.')
def p04_12():
    """Back in the field, planting and chatting - and every step looked at."""
    return (_field04('s4p12', mood='golden', sun=(440, 56), rays=True)
            + S.seedlings(y=320, xs=(60, 104, 150, 196), sprouted=True)
            + S.seedlings(y=336, xs=(300, 344, 388, 432))
            + S.shadow(150, 350, 32)
            + rabbit(150, 352, s=1.2, expr='happy', look=(0, .7), arm2=(24, 24))
            + S.shadow(330, 348, 46)
            + elephant(330, 352, s=1.25, expr='happy', look=(0, .7), trunk=(-36, 50))
            + S.bubble(["Watch your step!"], 330, 90, tail=(330, 170), size=13)
            + S.bubble(["Always."], 120, 132, tail=(146, 212), size=13))



# ---------------------------------------------------------------- story 03
# Snow outside on every exterior page, and a pale clinical blue-white inside the
# hospital, so the reader always knows which of the two worlds a page is in.
WARD = "#EEF4F7"


def _snow03(uid, mood='snow', n=26, seed=3, horizon=205):
    return S.snow_sky(uid, mood) + S.snow_ground(uid, horizon) + S.flakes(n, seed)


def _snow_window(x, y, w=92, h=74):
    """A window with the snow coming down outside it."""
    return (f'<rect x="{x-w/2:.0f}" y="{y-h/2:.0f}" width="{w}" height="{h}" rx="5" fill="#CFE3F2" stroke="#B9AE98" stroke-width="3"/>'
            f'<path d="M{x-w/2+3:.0f},{y+h/2-16:.0f} q{w*.3:.0f},-10 {w-6:.0f},-4 V{y+h/2-3:.0f} H{x-w/2+3:.0f} Z" fill="#FFFFFF"/>'
            + "".join(f'<circle cx="{x+dx}" cy="{y+dy}" r="2" fill="#FFFFFF"/>'
                      for dx, dy in ((-30, -24), (-12, -8), (8, -26), (24, -6), (32, -22), (-26, 4), (14, 8)))
            + f'<path d="M{x},{y-h/2+3:.0f} v{h-6} M{x-w/2+3:.0f},{y} h{w-6}" stroke="#B9AE98" stroke-width="2.5"/>'
            f'<rect x="{x-w/2-6:.0f}" y="{y+h/2-2:.0f}" width="{w+12}" height="8" rx="2" fill="#FFFFFF" stroke="#D8D0C0"/>')


def _heat(x, y):
    """Fever: little red heat squiggles rising."""
    return S.steam(x, y, .8, color="#FF6B6B")


@alt('In a snowy forest, Pig slides downhill on a red sled, Fox throws a snowball past a snowman and Deer leaps happily, none of them in scarves.')
def p03_1():
    """The first snow - and everyone out playing in it with no scarf or mitten."""
    return (_snow03('s3p1', n=34, seed=1)
            + S.pine(40, 226, s=.9) + S.pine(466, 222, s=1.0) + S.pine(430, 214, s=.7)
            + '<path d="M0,256 Q60,170 190,250 Z" fill="#FFFFFF" stroke="#B8D0E0" stroke-width="2.5"/>'
            + S.spin(30, 88, 206, critter('pig', 88, 206, s=.7, pose='sit', expr='excited', look=(.5, .2),
                                          arm=(-26, -28), arm2=(26, -28))
                     + '<path d="M56,210 h62 q10,0 12,-10" stroke="#E4453F" stroke-width="5" fill="none" stroke-linecap="round"/>'
                       '<path d="M64,210 v-6 M112,210 v-6" stroke="#E4453F" stroke-width="3"/>')
            + S.speedlines(44, 170, n=3, length=24, back=True)
            + S.snowman(250, 300, s=1.05)
            + S.shadow(150, 350, 30)
            + critter('fox', 150, 352, s=1.05, expr='happy', look=(.6, -.2), arm2=(28, -44))
            + S.snowball(212, 238, flying=True)
            + S.shadow(380, 348, 32)
            + critter('deer', 380, 350, s=1.05, expr='excited', look=(-.6, 0), arm=(-32, -30)))


@alt('By a crackling fire, Rabbit and Elephant sit on a rug with bowls of warm soup, their feet bandaged, while snow falls outside the window.')
def p03_2():
    """Home from hospital, toes still healing: soup by the fire instead."""
    return (S.indoors('s3p2', wall="#FFF0E0", floor="#EFD9BE")
            + _snow_window(96, 120)
            + S.fireplace(372, 250, w=112, h=124)
            + '<ellipse cx="236" cy="316" rx="178" ry="28" fill="#FF9BAE" opacity=".45"/>'
            + rabbit(160, 336, s=1.15, pose='sit', expr='happy', look=(.4, .2), arm2=(26, 6),
                     extra=bandage(-16, -2, 12, 8))
            + S.bowl(196, 312, 'soup', s=.9)
            + elephant(300, 340, s=1.2, pose='sit', expr='calm', look=(-.3, .3), trunk=(-44, 10),
                       extra=bandage(-30, -4, 15, 10))
            + S.bowl(262, 318, 'soup', s=1.05)
            + '<text x="228" y="150" font-size="22" fill="#FF6B6B" text-anchor="middle">&#9829;</text>')


@alt('Snow falls on the hospital, which has a Fully Booked banner and a Helpers Needed sign, while Wolf, Pig and Fox cough and shiver outside.')
def p03_3():
    """Days of snow, a hospital full of coughs, and an urgent call for helpers."""
    return (_snow03('s3p3', seed=2)
            + S.hospital(x=150, y=86, w=200, h=132)
            + '<rect x="186" y="170" width="128" height="26" rx="6" fill="#E4453F" transform="rotate(-4 250 183)"/>'
              '<text x="250" y="189" font-size="15" fill="#FFFFFF" text-anchor="middle" '
              'font-family="Fredoka One, sans-serif" transform="rotate(-4 250 183)">FULLY BOOKED!</text>'
            + S.sign(430, 212, ["HELPERS", "NEEDED!"], w=92, color="#E4453F")
            + S.shadow(84, 350, 26) + critter('wolf', 84, 352, s=.9, expr='sad', look=(.4, 0))
            + S.cough(116, 262)
            + S.shadow(186, 350, 26) + critter('pig', 186, 352, s=.86, expr='worried', look=(.3, -.3))
            + S.shadow(300, 350, 26) + critter('fox', 300, 352, s=.9, expr='hurt', look=(-.3, 0))
            + S.cough(270, 262, flip=True)
            + S.shiver(300, 240, h=44, gap=40))


@alt('Inside the hospital, Dr. Squirrel warmly welcomes Rabbit and Elephant, with Nurse Giraffe beside her.')
def p03_4():
    """Healed up and here to help - and Dr. Squirrel could not be happier."""
    return (S.indoors('s3p4', wall=WARD, floor="#DCE6EC")
            + '<rect x="210" y="60" width="44" height="44" rx="6" fill="#FFFFFF" stroke="#FF6B6B" stroke-width="2"/>'
              '<rect x="228" y="66" width="8" height="32" rx="2" fill="#FF6B6B"/>'
              '<rect x="216" y="78" width="32" height="8" rx="2" fill="#FF6B6B"/>'
            + S.shadow(84, 350, 30)
            + rabbit(84, 352, s=1.15, expr='excited', look=(.6, -.1), arm2=(24, -30))
            + S.shadow(200, 348, 44)
            + elephant(200, 352, s=1.2, expr='happy', look=(.5, -.1), trunk=(-24, 40))
            + S.shadow(454, 348, 30)
            + giraffe(454, 350, s=1.05, expr='calm', look=(-.6, 0))
            + S.shadow(340, 350, 26)
            + squirrel(340, 352, s=1.15, expr='happy', look=(-.6, 0), arm=(-40, -18))
            + S.bubble(["Thank you for coming!", "We really need your help."], 330, 150,
                       tail=(338, 228), size=12))


@alt('Elephant presses an enormous breathing mask onto Pig in bed while turning to chat with Nurse Giraffe, as the machine hums to life.')
def p03_5():
    """The biggest mask on the shelf, onto a very small snout."""
    return (S.indoors('s3p5', wall=WARD, floor="#DCE6EC")
            + S.breather(94, 262, on=True)
            + S.bed(150, 236, w=150)
            + critter('pig', 188, 264, pose='lie', expr='surprised', look=(0, -.4))
            + S.mask(188, 232, s=2.1, hose_to=(94, 206))
            + S.shadow(338, 348, 44)
            + elephant(338, 352, s=1.15, expr='happy', look=(.7, -.2), trunk=(-70, -10))
            + S.shadow(452, 348, 30)
            + giraffe(452, 350, s=1.05, expr='calm', look=(-.6, 0)))


@alt('A great gust from the machine sends Pig flying off the bed into the wall with a THUD, and Elephant spins round in surprise.')
def p03_6():
    """THUD! One enormous gust, and Pig sails clean off the bed."""
    return (S.indoors('s3p6', wall=WARD, floor="#DCE6EC")
            + S.bed(210, 250, w=150)
            + S.breather(174, 262, on=True)
            + "".join(f'<path d="M{206-i*6},{190+i*14} q-40,-10 -96,{-14+i*8}" stroke="#B9D4E2" '
                      f'stroke-width="3" fill="none" stroke-linecap="round" opacity=".8"/>' for i in range(4))
            + _pow(46, 146, 30)
            + S.spin(-28, 74, 190, critter('pig', 74, 190, s=.8, pose='sit', expr='surprised',
                                           arm=(-28, -26), arm2=(28, -26)))
            + S.mask(190, 118, s=2.1)
            + S.shadow(398, 348, 44)
            + elephant(398, 352, s=1.15, expr='surprised', look=(-.8, -.4), trunk=(-30, -40))
            + _shout("THUD!", 116, 70, size=34, rot=-8))


@alt('Rabbit hurries between two beds with ice cream for shivering Deer and hot chilli soup for feverish Fox.')
def p03_7():
    """Ice cream for the shivering Deer, chilli for the feverish Fox. Oh dear."""
    return (S.indoors('s3p7', wall=WARD, floor="#DCE6EC")
            + S.bed(20, 236, w=146)
            + critter('deer', 58, 264, pose='lie', expr='sad', look=(.6, 0))
            + S.shiver(58, 204, h=40, gap=38)
            + S.bed(344, 236, w=146)
            + critter('fox', 382, 264, pose='lie', expr='hurt', look=(-.6, 0))
            + _heat(382, 196)
            + S.shadow(250, 350, 32)
            + rabbit(250, 352, s=1.2, expr='excited', look=(-.4, 0), arm=(-52, -14), arm2=(52, -14))
            + S.ice_cream(186, 276, s=1.0)
            + S.bowl(314, 282, 'chilli', s=1.0)
            + _shout("?!", 272, 118, size=30, rot=6, color="#FF6B6B"))


@alt('Dr. Sheep rushes in and swaps the bowls, giving the chilli soup to Deer and the ice cream to Fox.')
def p03_8():
    """Both worse. Dr. Sheep rushes in and swaps the bowls right away."""
    return (S.indoors('s3p8', wall=WARD, floor="#DCE6EC")
            + S.bed(20, 236, w=146)
            + critter('deer', 58, 264, pose='lie', expr='sad', look=(.6, 0))
            + S.shiver(58, 204, h=40, gap=38)
            + S.bed(344, 236, w=146)
            + critter('fox', 382, 264, pose='lie', expr='hurt', look=(-.6, 0),
                      extra='<circle cx="0" cy="-38" r="26" fill="#FF6B6B" opacity=".28"/>')
            + _heat(382, 196)
            + S.shadow(250, 350, 36)
            + sheep(250, 352, s=1.2, expr='surprised', look=(0, -.2), arm=(-50, -20), arm2=(50, -20))
            + S.bowl(186, 290, 'chilli', s=.9)
            + S.ice_cream(316, 292, s=.9)
            + S.bubble(["Oh dear -", "wrong dishes!"], 250, 104, tail=(250, 200), size=13))


@alt('Elephant jabs Wolf with a giant syringe and Wolf howls, while a worried giraffe patient sits in bed beside a pot of tablets.')
def p03_9():
    """Wolf's tablets to the giraffe, the giraffe's giant injection to Wolf. OWOOO!"""
    return (S.indoors('s3p9', wall=WARD, floor="#DCE6EC")
            + giraffe(84, 330, s=1.25, pose='seated', cap=False, expr='worried', look=(.6, 0),
                      extra='<circle cx="9" cy="-110" r="22" fill="#FF6B6B" opacity=".2"/>')
            + S.bed(30, 262, w=140)
            + S.pills(146, 250)
            + S.bed(330, 236, w=160)
            + critter('wolf', 368, 264, pose='lie', expr='shout', look=(0, -.6))
            + S.shadow(250, 348, 44)
            + elephant(250, 352, s=1.15, expr='guilty', look=(.6, -.2), trunk=(40, -18))
            + S.syringe(330, 218, s=1.8, rot=160)
            + _shout("OWOOO!", 400, 150, size=30, rot=-10))


@alt('In her office, Dr. Sheep sits behind her desk while Rabbit and Elephant stand before her, looking sad.')
def p03_10():
    """Dr. Sheep's office. A kind thank-you, a sad face, and: one more chance?"""
    return (S.indoors('s3p10', wall="#F4EEE6", floor="#E8DCC8")
            + '<rect x="334" y="70" width="70" height="52" rx="3" fill="#FFFDF6" stroke="#C8A868" stroke-width="3"/>'
              '<circle cx="369" cy="102" r="7" fill="#E4453F"/><path d="M350,86 h38" stroke="#C8BCA4" stroke-width="2"/>'
            + sheep(376, 284, s=1.1, pose='seated', expr='calm', look=(-.6, .1))
            + S.table(290, 270, w=170)
            + S.books(320, 262, n=3) + S.clipboard(432, 248, s=.8)
            + S.shadow(90, 350, 30)
            + rabbit(90, 352, s=1.15, expr='sad', look=(.6, -.1), ears=(-4, 8))
            + S.shadow(214, 348, 44)
            + elephant(214, 352, s=1.2, expr='sad', look=(.6, -.2), trunk=(-20, 44))
            + S.bubble(["Please, one more chance?", "We really want to help."], 190, 108,
                       tail=(208, 222), size=12))


@alt("Elephant carefully wraps a fresh bandage around Lion's foot, and Lion smiles from his bed.")
def p03_11():
    """Slowly, carefully, a fresh neat bandage - and Lion gives a satisfied nod."""
    return (S.indoors('s3p11', wall=WARD, floor="#DCE6EC")
            + S.bed(40, 236, w=170)
            + critter('lion', 78, 264, pose='lie', expr='happy', look=(.7, .2))
            + bandage(186, 244, 16, 11)
            + '<path d="M60,352 q-8,-26 10,-30 q18,-4 16,16" stroke="#E8E8E8" stroke-width="5" fill="none" stroke-linecap="round"/>'
              '<rect x="40" y="322" width="40" height="30" rx="4" fill="#C8D0D6"/>'
            + S.shadow(310, 348, 44)
            + elephant(310, 352, s=1.15, expr='calm', look=(-.7, .5), trunk=(-92, -14))
            + '<text x="236" y="210" font-size="22" fill="#06C98A" text-anchor="middle">&#10022;</text>'
              '<text x="160" y="232" font-size="14" fill="#FFD166" text-anchor="middle">&#10022;</text>')


@alt('Rabbit drives the truck along a snowy road, with old Tortoise riding in the back, toward his little cottage.')
def p03_12():
    """Old Tortoise, driven home slowly and carefully through the snow."""
    return (_snow03('s3p12', seed=4, horizon=214)
            + S.pine(34, 222, s=.8) + S.pine(76, 216, s=.6)
            + S.cottage(430, 244, s=.9)
            + S.road(250)
            + '<path d="M0,250 q60,-8 120,0 t130,0 t130,0 t120,0" stroke="#FFFFFF" stroke-width="8" fill="none"/>'
            + S.truck('s3p12', 60, 328, w=300,
                      cargo_riders=tortoise(146, 290, s=.9, expr='happy', look=(.5, 0)),
                      cab_riders=rabbit(302, S.cab_seat(328, .72), s=.72, pose='seated', expr='calm', look=(.5, 0))))


@alt('At sunset in the snow outside the hospital, Dr. Sheep hands chocolates to Rabbit and Elephant, who grin happily.')
def p03_13():
    """A chocolate each, 'same time tomorrow?' and grins all the way home."""
    return (S.snow_sky('s3p13', 'sunset') + S.snow_ground('s3p13') + S.flakes(14, 5, bottom=200)
            + '<circle cx="444" cy="70" r="30" fill="#FFB36B" opacity=".9"/><circle cx="444" cy="70" r="21" fill="#FFE0A8"/>'
            + S.hospital(x=18, y=96, w=130, h=110)
            + S.shadow(160, 350, 34)
            + sheep(160, 352, s=1.15, expr='happy', look=(.6, 0), arm2=(48, -10))
            + S.chocolate(222, 300)
            + S.shadow(292, 350, 30)
            + rabbit(292, 352, s=1.15, expr='happy', look=(-.4, 0), arm=(-28, -12),
                     extra=S.chocolate(-56, -76, s=.8, rot=20))
            + S.shadow(410, 348, 44)
            + elephant(410, 352, s=1.2, expr='happy', look=(-.5, 0), trunk=(-40, 10))
            + S.chocolate(372, 262, s=.9, rot=-30)
            + S.bubble(["Thank you both, truly.", "Same time tomorrow?"], 176, 118, tail=(166, 214), size=12)
            + '<text x="350" y="150" font-size="22" fill="#FF6B6B" text-anchor="middle">&#9829;</text>')


# ---------------------------------------------------------------- story 07
E_SOLE, E_NAIL = "#D9CEBF", "#F6F1E8"


def _sole(x, y, rx=20, ry=16, rot=0):
    """The bottom of an elephant's foot, toenails and all - what you see of a foot
    pointing at you."""
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{E_SOLE}" stroke="{E_LINE}" stroke-width="2"/>'
            + "".join(f'<ellipse cx="{x+dx*rx:.0f}" cy="{y-ry*.62:.0f}" rx="{rx*.2:.1f}" ry="{ry*.22:.1f}" fill="{E_NAIL}" '
                      f'stroke="{E_LINE}" stroke-width="1"/>' for dx in (-.5, 0, .5))
            + '</g>')


def _rump(x, y, kick=False):
    """Elephant from behind, wedged in a doorway: a big round bottom, a tail hanging
    down it, and two back legs. `y` is the ground under the planted foot."""
    lx, rx_ = x - 36, x + 36
    out = (f'<rect x="{lx-19}" y="{y-80}" width="38" height="70" rx="15" fill="{E_BODY}" stroke="{E_LINE}" stroke-width="1.8"/>'
           + _sole(lx, y - 10, 22, 14))
    if kick:
        out += (_limb(rx_, y - 70, 50, -36, E_BODY, E_LINE, 36, bow=.2)
                + _sole(rx_ + 56, y - 110, 21, 16, rot=-36))
    else:
        out += (f'<rect x="{rx_-19}" y="{y-80}" width="38" height="70" rx="15" fill="{E_BODY}" stroke="{E_LINE}" stroke-width="1.8"/>'
                + _sole(rx_, y - 10, 22, 14))
    return (out
            + f'<ellipse cx="{x}" cy="{y-118}" rx="82" ry="64" fill="{E_BODY}" stroke="{E_LINE}" stroke-width="1.8"/>'
            f'<path d="M{x},{y-56} q-2,-18 0,-34" stroke="{E_LINE}" stroke-width="2" fill="none" stroke-linecap="round"/>'
            f'<path d="M{x-46},{y-150} q10,-12 24,-8 M{x+46},{y-150} q-10,-12 -24,-8" stroke="{E_LINE}" stroke-width="1.6" '
            f'fill="none" stroke-linecap="round" opacity=".7"/>'
            f'<path d="M{x},{y-176} q8,22 2,48" stroke="{E_LINE}" stroke-width="5" stroke-linecap="round" fill="none"/>'
            f'<path d="M{x+2},{y-130} q-8,8 -3,18 q5,-4 5,4 q4,-8 6,-4 q2,-12 -8,-18 Z" fill="{S.INK}"/>')


def _cheeks(hx, hy):
    """Elephant's cheeks puffed up like balloons, round his head-local origin."""
    return "".join(f'<circle cx="{hx+sx*30}" cy="{hy+14}" r="17" fill="{E_BODY}" stroke="{E_LINE}" stroke-width="1.5"/>'
                   f'<circle cx="{hx+sx*34}" cy="{hy+8}" r="4" fill="#FFFFFF" opacity=".6"/>' for sx in (-1, 1))


def _doorway(x0, x1, top, floor):
    """An open archway out of the room, dark beyond."""
    w = x1 - x0
    return (f'<path d="M{x0},{floor} V{top+w/2:.0f} A{w/2:.0f},{w/2:.0f} 0 0 1 {x1},{top+w/2:.0f} V{floor} Z" '
            f'fill="#5A3A1E" stroke="{S.EARTH_DK}" stroke-width="6"/>')


@alt('At sunset, Elephant arrives at Rabbit\'s tiny burrow door with a pillow on his head, a teddy under his arm and a suitcase in his trunk, while Rabbit looks up at him, worried.')
def p07_1():
    """A sleepover! Elephant, his snack suitcase, and a very small front door."""
    return (S.sky('s7p1', 'sunset', sun=(300, 64), clouds=((80, 54, 40, 15), (108, 46, 24, 12), (210, 84, 30, 12)))
            + S.ground('s7p1', tufts=(40, 176, 250), flowers=((60, 246), (226, 252)))
            + S.burrow_hill(420, 312, door=(-6, 0), door_r=40)
            + S.shadow(170, 348, 50)
            + elephant(170, 350, s=1.25, expr='happy', look=(.5, -.1), trunk=(-70, 30), arm=(10, -8),
                       extra=S.suitcase(-80, -50, s=.8) + S.teddy(40, -64, s=1.1)
                       + S.pillow(0, -148, w=74, h=30, rot=-6, color="#FFE3EC", line="#E8A8BC"))
            + S.shadow(310, 350, 30)
            + rabbit(310, 352, s=1.1, expr='worried', look=(-.6, -.5), arm2=(40, 8), ears=(-12, 16))
            + S.bubble(["Snacks!", "Just in case."], 92, 104, tail=(150, 196)))


@alt('Elephant is stuck in Rabbit\'s round front door with only his bottom, tail and kicking back legs outside, while Rabbit tickles his foot with a feather.')
def p07_2():
    """Stuck! Front half in the burrow, back half in the garden - and a feather."""
    return (S.sky('s7p2', 'sunset', sun=(90, 60), clouds=((400, 50, 40, 15), (428, 42, 24, 12)))
            + S.ground('s7p2', tufts=(40, 300, 460), flowers=((60, 250), (440, 246)))
            + S.burrow_hill(220, 330, door_r=50, open_door=True)
            + "".join(f'<path d="M{220+sx*86},{230+i*24} q{sx*12},6 {sx*22},0" stroke="#5B7BA8" stroke-width="2.6" '
                      f'fill="none" stroke-linecap="round"/>' for sx in (-1, 1) for i in range(3))
            + _rump(220, 344, kick=True)
            + S.speedlines(318, 236, n=3, length=22, back=False)
            + S.shadow(410, 350, 30)
            + rabbit(410, 352, s=1.1, expr='sneaky', look=(-.7, -.3), arm=(-50, -50), ears=(-14, 14),
                     extra=S.feather(-80, -112, s=1.3, rot=-50))
            + _shout("HEE HEE!", 120, 110, size=26, rot=-8)
            + _shout("HOO HOO!", 370, 92, size=22, rot=8, color="#C77DFF"))


@alt('Inside the burrow, Elephant sits grinning on a squashed-flat sofa, and Rabbit lands upside down on top of his head with her ears in a knot.')
def p07_3():
    """POP! Straight onto the sofa - and Rabbit straight onto Elephant."""
    rb = rabbit(250, 304, s=.95, expr='happy', look=(0, .3), arm=(-30, 10), arm2=(30, 10), ears=(38, -38))
    return (S.burrow('s7p3')
            + S.porthole(80, 120, sky='sunset')
            + S.picture(420, 96, art='carrot')
            + S.lamp(452, 330, on=True)
            + S.sofa(250, 336, w=230, squashed=True)
            + elephant(250, 330, s=1.2, pose='sit', expr='happy', look=(0, -.6), trunk=(40, -60), arm=(34, -40))
            + S.spin(180, 250, 173, rb)
            + S.pillow(96, 232, w=50, h=28, rot=-30, color="#FFD166", line="#D8A21F")
            + S.speedlines(130, 236, n=3, length=20, back=False)
            + _pow(146, 318, 20)
            + _shout("CRUNCH!", 130, 300, size=24, rot=-8)
            + S.bubble("Ta-da!", 388, 160, tail=(300, 200))
            + S.bubble(["Welcome to", "my house."], 112, 46, tail=(200, 60), size=12))


@alt('The little spare bed has folded up around Elephant like a sandwich, with his head and feet sticking out, while Rabbit gasps.')
def p07_4():
    """CRASH! The bed folds up with Elephant as the filling."""
    half = (f'<rect x="-104" y="-12" width="104" height="24" rx="6" fill="#FFFDF6" stroke="#D8C8A8" stroke-width="2"/>'
            f'<rect x="-104" y="12" width="104" height="10" rx="3" fill="{S.WOOD}" stroke="{S.WOOD_DK}" stroke-width="1.5"/>'
            f'<rect x="-96" y="22" width="8" height="18" fill="{S.WOOD_DK}"/>')
    vx, vy = 220, 316
    return (S.burrow('s7p4')
            + S.porthole(420, 100, sky='night')
            + S.picture(110, 90, art='hills')
            + S.lamp(60, 330, on=True)
            + S.glow(60, 228, 70)
            # Elephant tipped head-up into the fold, the bed's two halves closing over him
            + S.spin(28, vx, vy, elephant(vx - 72, vy, s=1.05, pose='lie', expr='surprised', look=(.3, -.5),
                                         trunk=(-40, 20)))
            + _sole(vx + 84, vy - 70, 18, 14, rot=-30) + _sole(vx + 108, vy - 56, 18, 14, rot=-50)
            + f'<g transform="translate({vx},{vy}) rotate(28)">{half}</g>'
            + f'<g transform="translate({vx},{vy}) scale(-1,1) rotate(28)">{half}</g>'
            + S.pillow(150, 150, w=48, h=26, rot=24)
            + _pow(vx, vy + 6, 26)
            + _shout("CRASH!", 230, 96, size=34, rot=-6)
            + S.shadow(420, 350, 30)
            + rabbit(420, 352, s=1.1, expr='surprised', look=(-.7, -.2), arm=(8, -44), arm2=(-8, -44)))


@alt('In the dark, Elephant sleeps in a nest of cushions snoring HONK so loudly that Rabbit\'s ears blow flat, the pictures wobble and her blanket flies onto the lamp.')
def p07_5():
    """HONNNK - shoooo. A trumpet in a tunnel."""
    return (S.burrow('s7p5')
            + S.porthole(250, 86, sky='night')
            + S.picture(120, 96, tilt=-12, art='carrot', wobble=True)
            + S.picture(380, 90, tilt=10, art='heart', wobble=True)
            + S.lamp(330, 290, on=False, blanket=True)
            + S.night(.4)
            + S.nest(150, 348, w=270)
            + elephant(70, 316, s=1.05, pose='lie', expr='sleepy', trunk=(30, 34))
            + S.nest_front(150, 352, w=270)
            + S.snore(150, 218, s=1.3)
            + _shout("HONNNK!", 150, 150, size=36, rot=-6, color="#FFD166")
            + "".join(f'<path d="M{290+i*12},{200+i*14} h46" stroke="#C8D4E8" stroke-width="2.4" stroke-linecap="round" '
                      f'opacity=".7"/>' for i in range(3))
            + S.little_bed(430, 352, w=120, quilt=None,
                           sleeper=rabbit(438, 330, s=.95, pose='seated', expr='surprised', look=(-.6, 0), ears=(72, 84))))


@alt('Rabbit tiptoed over and clipped a peg on Elephant\'s trunk, but his puffed-up cheeks blew it PING across the room and BOINK onto Rabbit\'s nose.')
def p07_6():
    """Sneaky plan one: a clothes peg. It comes straight back at her."""
    hx, hy = 70, 316 - 44*1.05
    return (S.burrow('s7p6')
            + S.porthole(250, 86, sky='night')
            + S.picture(120, 96, tilt=-4, art='carrot')
            + S.night(.4)
            + S.nest(150, 348, w=270)
            + elephant(70, 316, s=1.05, pose='lie', expr='sleepy', trunk=(30, 34), extra=_cheeks(0, -44))
            + S.nest_front(150, 352, w=270)
            + S.flight([(112, 300), (190, 30), (470, 120), (400, 232)], color="#FFE39A")
            + _pow(190, 30, 14) + _pow(470, 120, 14)
            + _shout("PING!", 150, 230, size=26, rot=-10, color="#FFD166")
            + S.shadow(400, 350, 30)
            + rabbit(400, 352, s=1.15, expr='surprised', look=(0, .6), arm=(-6, -34), arm2=(10, 30), ears=(-24, 24),
                     extra=S.peg(0, -104, s=1.1, rot=90))
            + _shout("BOINK!", 410, 300, size=26, rot=6, color="#FFD166"))


@alt('In the dark kitchen, Rabbit is curled up in a giant fruit bowl beside a melon and apples, ears pricked, as a huge shadow creeps in through the doorway.')
def p07_7():
    """Sneaky plan two: sleep in the fruit bowl. Creak. Creak. CREAK."""
    shadow = (f'<g fill="{S.NIGHT}" opacity=".55">'
              f'<ellipse cx="150" cy="236" rx="70" ry="44"/><circle cx="96" cy="190" r="40"/>'
              f'<ellipse cx="62" cy="190" rx="26" ry="34"/><ellipse cx="130" cy="186" rx="26" ry="34"/>'
              f'<path d="M84,214 q-10,40 18,56" stroke="{S.NIGHT}" stroke-width="18" fill="none" stroke-linecap="round"/>'
              f'<rect x="110" y="250" width="26" height="40" rx="10"/><rect x="170" y="250" width="26" height="40" rx="10"/></g>')
    return (S.kitchen('s7p7')
            + _doorway(30, 120, 110, 262)
            + S.porthole(240, 90, sky='night')
            + S.shelf(390, 120)
            + S.night(.45)
            + shadow
            + '<path d="M222,112 L258,112 L360,352 L180,352 Z" fill="#FFF3C4" opacity=".14"/>'
            + S.fruit_bowl(290, 350, w=170,
                           rider=rabbit(290, 318, s=.9, pose='sit', expr='worried', look=(-.8, 0), ears=(-6, 8)))
            + _shout("creak…", 120, 330, size=18, rot=-6, color="#C8D4E8")
            + _shout("CREAK!", 196, 60, size=30, rot=-8, color="#FFE39A"))


@alt('A saucepan has landed over Elephant\'s eyes as he skids on a roller skate holding a banana, and Rabbit, standing in the fruit bowl, throws an apple at him, BONK!')
def p07_8():
    """CLANG! A monster with a metal head. BONK! It's only Elephant."""
    ex, ey, s = 190, 350, 1.2
    head = (ex, ey - 100*s)
    return (S.kitchen('s7p8')
            + S.porthole(80, 90, sky='night')
            + S.shelf(300, 110, tipped=True)
            + S.night(.36)
            + S.skate(160, 358, rot=-12)
            + elephant(ex, ey - 6, s=s, expr='surprised', look=(0, 0), trunk=(-36, 34), arm=(20, -42),
                       extra=S.banana(-44, -48, s=1.1, rot=-30))
            + S.saucepan(head[0], head[1] - 2, s=1.35, rot=-8)
            + _pow(250, 72, 18)
            + _shout("CLANG!", 250, 52, size=28, rot=8, color="#FFD166")
            + S.fruit_bowl(400, 350, w=150,
                           rider=rabbit(398, 296, s=.88, expr='shout', look=(-.8, -.3), arm=(-50, -26), arm2=(30, -40)))
            + S.apple(272, 182, 11)
            + S.speedlines(296, 186, n=3, length=26, back=False)
            + _pow(232, 168, 16, "#FF9BAE")
            + _shout("BONK!", 238, 230, size=24, rot=-8, color="#FFD166")
            + S.bubble("MONSTER!", 412, 108, tail=(404, 160))
            + S.bubble(["Ow!", "It's ME!"], 84, 196, tail=(140, 220)))


@alt('With the kitchen light on, Elephant laughs with a saucepan pushed up on his head like a hat, while Rabbit giggles on the floor among rolling apples and tells him his snores are very big.')
def p07_9():
    """Lights on. Giggles. And then Rabbit says it - kindly."""
    return (S.kitchen('s7p9')
            + S.porthole(80, 90, sky='night')
            + S.shelf(300, 110)
            + '<path d="M250,0 V40" stroke="#6B5B47" stroke-width="2"/>'
            + S.glow(250, 52, 90)
            + '<circle cx="250" cy="52" r="12" fill="#FFE39A" stroke="#D8B05A" stroke-width="1.5"/>'
              '<rect x="244" y="36" width="12" height="8" fill="#9AA6AE"/>'
            + S.shadow(160, 348, 46)
            + elephant(160, 350, s=1.2, expr='happy', look=(.6, .1), trunk=(-30, 30), arm=(22, 14))
            + S.saucepan(150, 186, s=1.1, rot=-20)
            + S.shadow(360, 350, 40)
            + S.spin(-14, 360, 350, rabbit(360, 350, s=1.05, pose='sit', expr='happy', look=(-.5, -.2),
                                           arm=(16, 16), arm2=(-16, 16), ears=(-30, 30)))
            + S.apple(270, 340, 10) + S.apple(450, 344, 10, "#FFD166") + S.apple(470, 312, 9)
            + S.speedlines(292, 336, n=2, length=18) + S.speedlines(428, 340, n=2, length=18, back=False)
            + S.bubble(["Your snores are", "very… BIG!"], 382, 120, tail=(366, 220))
            + S.bubble(["Why didn't", "you tell me?"], 106, 74, tail=(140, 170)))


@alt('By lamplight, Rabbit leaps through the air swinging a pillow at Elephant, who holds up his own pillow in his trunk, with feathers flying everywhere.')
def p07_10():
    """The side-sleeping trick, one fake snore - and a pillow fight."""
    return (S.burrow('s7p10')
            + S.porthole(250, 86, sky='night')
            + S.lamp(460, 330, on=True)
            + S.night(.28)
            + S.glow(460, 228, 80)
            + S.nest(250, 352, w=420)
            + S.shadow(150, 350, 46)
            + elephant(150, 350, s=1.2, expr='excited', look=(.7, -.2), trunk=(46, -62),
                       extra=S.pillow(54, -140, w=60, h=34, rot=20, color="#FFE3EC", line="#E8A8BC"))
            + S.shadow(350, 350, 28)
            + rabbit(350, 296, s=1.05, expr='excited', look=(-.7, -.1), arm=(-30, -50), arm2=(30, 8), ears=(-30, 10),
                     extra=S.pillow(-60, -112, w=56, h=32, rot=-30, color="#FFD166", line="#D8A21F"))
            + S.feathers(20, seed=7, box=(20, 30, 480, 260))
            + S.bubble("Got you!", 90, 70, tail=(130, 170)))


@alt('In the morning light, Elephant lies on his side behind a wall of pillows, grinning at Rabbit, who sleeps in her little bed making tiny squeaky snores.')
def p07_11():
    """A quiet night at last - and in the morning, a tiny squeak."""
    squeak = "".join(f'<text x="{x}" y="{y}" font-size="{f}" fill="#C77DFF" text-anchor="middle" '
                      f'font-family="Fredoka One, sans-serif" opacity=".85">squeak</text>'
                      for x, y, f in ((406, 214, 12), (424, 190, 14), (408, 164, 16)))
    return (S.burrow('s7p11')
            + S.porthole(250, 86, sky='morning')
            + '<path d="M222,112 L278,112 L330,262 L170,262 Z" fill="#FFF3C4" opacity=".35"/>'
            + S.picture(120, 96, art='heart')
            + S.nest(160, 348, w=290)
            + elephant(80, 318, s=1.1, pose='lie', expr='happy', look=(.8, .1), trunk=(24, 30))
            + "".join(S.pillow(x, 314, w=58, h=40, rot=r, color=c)
                      for x, r, c in ((140, 4, "#FFFFFF"), (196, -4, "#FFE3EC"), (252, 5, "#FFFFFF")))
            + S.nest_front(160, 352, w=290)
            + S.little_bed(410, 352, w=126,
                           sleeper=rabbit(394, 336, s=.9, pose='seated', expr='sleepy', ears=(-50, -30)))
            + squeak
            + S.bubble(["Rabbit… YOU", "snore too!"], 190, 160, tail=(110, 240)))


# ---------------------------------------------------------------- story 08
def _rfeet(x, y, s=1.0, kick=True):
    """Rabbit's back feet and fluffy tail, soles out - all you can see of a rabbit
    who has dived head-first into something."""
    out = []
    for sx, rot in ((-1, -24 if kick else -8), (1, 18 if kick else 8)):
        fx, fy = x + sx*13*s, y - (6 if kick and sx < 0 else 0)*s
        out.append(f'<g transform="rotate({rot} {fx:.0f} {fy:.0f})">'
                   f'<ellipse cx="{fx:.0f}" cy="{fy:.0f}" rx="{10*s:.1f}" ry="{17*s:.1f}" fill="{R_BODY}" stroke="{R_LINE}" stroke-width="1.5"/>'
                   f'<ellipse cx="{fx:.0f}" cy="{fy-4*s:.0f}" rx="{5*s:.1f}" ry="{6*s:.1f}" fill="{R_EAR}"/>'
                   + "".join(f'<circle cx="{fx+dx*s:.0f}" cy="{fy+8*s:.0f}" r="{2.4*s:.1f}" fill="{R_EAR}"/>' for dx in (-4, 0, 4))
                   + '</g>')
    out.append(f'<circle cx="{x}" cy="{y+16*s:.0f}" r="{10*s:.1f}" fill="#FFFFFF" stroke="{R_LINE}" stroke-width="1.5"/>')
    if kick:
        out.append("".join(f'<path d="M{x+sx*30*s:.0f},{y-14*s:.0f} q{sx*6*s:.0f},{-6*s:.0f} {sx*12*s:.0f},0" stroke="#8FA8C0" '
                           f'stroke-width="2.2" fill="none" stroke-linecap="round"/>' for sx in (-1, 1)))
    return "".join(out)


def _hiding(x, y, expr='surprised', look=(.8, -.2)):
    """Elephant 'hiding' behind the skinny tree: the trunk covers his middle and
    nothing else. His tail flicks out one side for good measure."""
    tail = (f'<path d="M40,-44 q22,-2 26,-24" stroke="{E_LINE}" stroke-width="6" fill="none" stroke-linecap="round"/>'
            f'<path d="M40,-44 q22,-2 26,-24" stroke="{E_BODY}" stroke-width="3.6" fill="none" stroke-linecap="round"/>'
            f'<path d="M66,-68 q-2,-10 4,-14 q2,6 4,0 q6,4 2,14 Z" fill="{S.INK}"/>')
    return (S.shadow(x, y - 2, 60)
            + elephant(x, y, s=1.25, expr=expr, look=look, trunk=(-6, 44), extra=tail)
            + S.skinny_tree(x, y + 2, h=236))


@alt('In a sunny meadow, Elephant boasts that he is the best hider, Rabbit giggles, and Nurse Giraffe in a sunhat closes her eyes and starts to count.')
def p08_1():
    """'I'm the BEST hider in the whole world.' Giraffe counts."""
    hat = S.sunhat(9, -164, s=1.0, rot=-4)
    return (S.sky('s8p1', 'morning', rays=True, sun=(440, 52))
            + S.ground('s8p1', flowers=((55, 242), (250, 252), (330, 236)))
            + S.tree(40, 214, s=.8)
            + S.shadow(160, 348, 56)
            + elephant(160, 350, s=1.25, expr='excited', look=(.2, -.3), trunk=(36, -46), arm=(30, -46))
            + S.shadow(286, 350, 30)
            + rabbit(286, 352, s=1.0, expr='happy', look=(-.7, -.4), arm=(-28, -40), arm2=(28, 10))
            + S.shadow(408, 350, 40)
            + giraffe(408, 350, s=1.05, expr='sleepy', cap=False, extra=hat)
            + S.bubble(["I'm the BEST", "hider!"], 120, 86, tail=(150, 200))
            + S.bubble(["One… two…", "three…"], 330, 92, tail=(400, 170), color="#C77DFF", size=12))


@alt('Elephant stands behind a very skinny tree with his ears, tummy and tail sticking out both sides, while Nurse Giraffe points at him and laughs. A pair of eyes peeks out of the picnic teapot.')
def p08_2():
    """Behind a very skinny tree - ears out one side, bottom out the other."""
    return (S.sky('s8p2', 'morning', sun=(60, 52), clouds=((360, 50, 40, 15), (388, 42, 24, 12)))
            + S.ground('s8p2', tufts=(150, 300, 460), flowers=((350, 250), (190, 240)))
            + S.picnic('s8p2', 80, 268, w=130, h=34)
            + S.teapot(84, 278, s=.62, lid=7, peek=1)
            + _hiding(250, 350)
            + S.shadow(410, 350, 40)
            + giraffe(410, 350, s=1.0, expr='happy', cap=False, look=(-.8, .1), arm=(-58, -16),
                      extra=S.sunhat(9, -164))
            + S.bubble(["Found you,", "Elephant!"], 400, 72, tail=(420, 180))
            + S.bubble("How?!", 120, 140, tail=(210, 200), color="#4AA8C8", size=15))


@alt('Elephant has jumped out of a leafy bush away from a buzzing bee and landed bottom-first in the pond with a big splash.')
def p08_3():
    """A bush with a tail - then a bee - then SPLASH."""
    ele = elephant(270, S.waterline(304), s=1.15, pose='sit', expr='surprised', look=(.3, -.8), trunk=(46, -40), arm=(30, -50))
    return (S.sky('s8p3', 'morning', sun=(440, 50), clouds=((80, 46, 40, 15), (108, 40, 24, 12)))
            + S.ground('s8p3', tufts=(40, 440), flowers=((440, 240), (30, 250)))
            + S.bush(70, 300, w=110, h=84, flying=True)
            + S.pond('s8p3', 270, 304, rx=160, ry=42, swimmers=ele)
            + S.splash(270, 330, s=1.25)
            + S.bee(330, 104, s=1.3, path=[(210, 220), (180, 160), (230, 120), (290, 150), (320, 110)])
            + _shout("EEEK!", 110, 120, size=30, rot=-10)
            + _shout("SPLASH!", 420, 200, size=30, rot=8, color="#4AA8C8"))


@alt('The lid of the picnic teapot has popped up and Rabbit bursts out of it with her arms in the air, while Nurse Giraffe and a dripping-wet Elephant stare in surprise.')
def p08_4():
    """Out of the teapot pops Rabbit. 'I win!'"""
    rab = rabbit(250, 282, s=.85, expr='excited', look=(0, -.2), arm=(-34, -44), arm2=(34, -44))
    drips = "".join(f'<path d="M{x},{y} q-4,6 0,9 q4,-3 0,-9 Z" fill="#9BDCF0" stroke="#5AB6D6" stroke-width="1"/>'
                    for x, y in ((356, 230), (446, 214), (376, 300), (430, 312)))
    return (S.sky('s8p4', 'golden', sun=(440, 50))
            + S.ground('s8p4', tufts=(40, 460), flowers=((40, 240), (460, 250)))
            + S.picnic('s8p4', 250, 312, w=300, h=58)
            + S.teapot(250, 318, s=1.3, lid=96, rider=rab)
            + S.shadow(90, 350, 40)
            + giraffe(90, 350, s=1.0, expr='surprised', cap=False, look=(.9, .2), extra=S.sunhat(9, -164))
            + S.shadow(410, 350, 50)
            + elephant(410, 350, s=1.2, expr='surprised', look=(-.9, -.1), trunk=(-40, 40))
            + drips
            + S.bubble(["Here I am!", "I win!"], 250, 50, tail=(250, 130)))


@alt('Elephant sneezes a huge ACHOO, blowing the picnic blanket off him and onto Nurse Giraffe\'s head, and she stumbles blindly into him. Rabbit\'s ears peek out of a flowerpot.')
def p08_5():
    """The rock that sneezed - and Giraffe under the blanket."""
    blind = (S.draped('s8p5', 9, -168, w=74, h=80)
             + _limb(-18, -60, -44, -18, N_BODY, N_LINE, 11))
    ears = "".join(f'<ellipse cx="{462+dx}" cy="{214}" rx="7" ry="20" fill="{R_BODY}" stroke="{R_LINE}" stroke-width="1.5" '
                   f'transform="rotate({dx*1.4} {462+dx} 230)"/>' for dx in (-8, 8))
    return (S.sky('s8p5', 'morning', sun=(60, 50), clouds=((330, 50, 40, 15), (356, 42, 24, 12)))
            + S.ground('s8p5', tufts=(40, 300), flowers=((40, 246), (260, 252)))
            + ears + S.flowerpot(462, 270, s=.6, flower=False)
            + S.shadow(330, 350, 54)
            + elephant(330, 350, s=1.2, pose='sit', expr='surprised', look=(-.6, -.3), trunk=(-56, 10))
            + S.speedlines(200, 236, n=3, length=26, back=False)
            + S.spin(8, 170, 350, giraffe(170, 350, s=1.0, expr='calm', cap=False, arm=(48, -18), extra=blind))
            + _shout("AAAA-CHOO!", 340, 120, size=30, rot=-6)
            + S.bubble("Found you!", 96, 90, tail=(150, 160)))


@alt('Rabbit pops out of a flowerpot, grinning, while Elephant stamps his foot with a THUMP and shouts that it isn\'t fair, and Nurse Giraffe\'s sunhat bounces off her head.')
def p08_6():
    """Grumpy Elephant stamps - THUMP - and Giraffe's hat goes flying."""
    rab = rabbit(84, 300, s=.85, expr='happy', look=(.7, -.2), arm=(-30, -40), arm2=(30, -40))
    dust = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#E8DCC4" opacity=".85"/>'
                   for x, y, r in ((210, 344, 10), (196, 334, 7), (330, 344, 10), (344, 334, 7), (226, 338, 6), (314, 338, 6)))
    return (S.sky('s8p6', 'tender', sun=(440, 52))
            + S.ground('s8p6', tufts=(40, 460), flowers=((440, 250), (160, 240)))
            + S.flowerpot(84, 344, s=1.1, rider=rab)
            + S.shadow(270, 350, 56)
            + elephant(270, 342, s=1.25, expr='shout', look=(0, 0), trunk=(-40, 30), arm=(36, -50))
            + dust
            + _shout("THUMP!", 182, 304, size=22, rot=-8, color="#A87A52")
            + S.shadow(420, 350, 38)
            + giraffe(420, 350, s=1.0, expr='surprised', cap=False, look=(.2, -1))
            + S.sunhat(440, 118, s=1.0, rot=26)
            + "".join(f'<path d="M{x},{y} q4,-6 0,-12" stroke="#8FA8C0" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
                      for x, y in ((412, 150), (422, 158)))
            + S.bubble(["This game", "isn't fair!"], 250, 74, tail=(266, 186)))


@alt('Only Rabbit\'s kicking feet and fluffy tail stick out of the end of a hollow log, and a tiny voice from inside says "Um… help?"')
def p08_7():
    """Deeper and deeper into the log - and stuck."""
    return (S.sky('s8p7', 'tender', sun=(440, 52), clouds=((80, 46, 40, 15), (108, 40, 24, 12)))
            + S.ground('s8p7', tufts=(40, 460), flowers=((40, 246), (450, 246), (120, 300)))
            + S.log(150, 330, w=240, r=46, inside=_rfeet(150, 274, s=1.25))
            + S.bubble(["Um…", "help?"], 110, 150, tail=(146, 240), size=12)
            + S.shadow(436, 268, 22)
            + giraffe(436, 270, s=.5, expr='sleepy', cap=False, arm=(-6, -84), extra=S.sunhat(9, -164)))


@alt('Nurse Giraffe searches high up in vain, while Elephant spreads his big ears and listens to tiny squeaks coming from a log far away.')
def p08_8():
    """Big ears are very good for listening."""
    return (S.sky('s8p8', 'tender', sun=(60, 52), clouds=((300, 46, 40, 15), (326, 40, 24, 12)))
            + S.ground('s8p8', tufts=(40, 300), flowers=((40, 246), (300, 252)))
            + S.log(380, 262, w=100, r=18)
            + S.squeaks(((396, 216, 12), (414, 192, 14), (400, 168, 16)))
            + S.shadow(90, 350, 38)
            + giraffe(90, 350, s=.95, expr='worried', cap=False, look=(-.4, -1), extra=S.sunhat(9, -164))
            + S.shadow(260, 350, 56)
            + elephant(260, 350, s=1.25, expr='excited', look=(.9, -.2), trunk=(-20, 40), arm=(30, -64))
            + S.earwaves(332, 228, s=1.2)
            + S.bubble(["Rabbit? Where", "are you?"], 120, 92, tail=(110, 170), color="#C77DFF", size=12)
            + S.bubble(["I can", "hear her!"], 300, 90, tail=(270, 196)))


@alt('Rabbit has popped out of the log and landed on Elephant\'s tummy, and Elephant has fallen flat on his bottom with his feet in the air, both of them laughing.')
def p08_9():
    """POP! out of the log, BUMP onto his bottom, and onto his tummy she lands."""
    legs = _foot(-44, -4) + _foot(44, -4)
    return (S.sky('s8p9', 'golden', sun=(440, 52))
            + S.ground('s8p9', tufts=(40, 460), flowers=((40, 246), (460, 250)))
            + S.log(270, 330, w=230, r=42)
            + _pow(270, 286, 26)
            + _shout("POP!", 290, 212, size=30, rot=8, color="#C77DFF")
            + S.speedlines(236, 250, n=3, length=30, back=False)
            + S.shadow(110, 350, 60)
            + elephant(110, 346, s=1.15, pose='sit', expr='happy', look=(.7, .3), trunk=(50, -30), extra=legs)
            + rabbit(200, 346, s=.72, pose='sit', expr='happy', look=(-.3, -.3), arm=(-30, -40), arm2=(30, -40))
            + _shout("BUMP!", 70, 200, size=26, rot=-10, color="#A87A52"))


@alt('Rabbit cheers that Elephant is the best finder, and Elephant goes pink and says sorry for being grumpy, while Nurse Giraffe smiles.')
def p08_10():
    """'You're the best FINDER!' - and a sorry."""
    return (S.sky('s8p10', 'golden', sun=(440, 52), rays=True)
            + S.ground('s8p10', tufts=(40, 460), flowers=((40, 246), (460, 250), (250, 238)))
            + S.tree(460, 214, s=.7)
            + S.shadow(400, 334, 30)
            + giraffe(400, 336, s=.75, expr='happy', cap=False, look=(-.6, .2), extra=S.sunhat(9, -164))
            + S.shadow(150, 350, 34)
            + rabbit(150, 352, s=1.15, expr='happy', look=(.8, -.4), arm=(-30, -44), arm2=(34, -44))
            + S.shadow(300, 350, 54)
            + elephant(300, 350, s=1.25, expr='happy', look=(-.8, .2), trunk=(-30, 40))
            + S.bubble(["You're the best", "FINDER!"], 130, 70, tail=(150, 170))
            + S.bubble(["Sorry I got", "grumpy."], 360, 98, tail=(318, 196), color="#4AA8C8"))


@alt('Elephant hides behind the skinny tree again, with his ears and tail sticking out, and Rabbit and Nurse Giraffe laugh as they find him.')
def p08_11():
    """Ears and bottom sticking out - and everybody laughing."""
    return (S.sky('s8p11', 'golden', sun=(440, 52), rays=True, clouds=((80, 46, 40, 15), (108, 40, 24, 12)))
            + S.ground('s8p11', tufts=(40, 460), flowers=((40, 246), (460, 250), (160, 300)))
            + _hiding(330, 350, expr='happy', look=(-.6, 0))
            + S.shadow(90, 350, 36)
            + giraffe(90, 350, s=.95, expr='happy', cap=False, look=(.8, .2), arm=(30, -56), extra=S.sunhat(9, -164))
            + S.shadow(196, 350, 30)
            + rabbit(196, 352, s=1.05, expr='happy', look=(.8, -.2), arm=(-26, -44), arm2=(40, -30))
            + S.bubble("Found you!", 160, 90, tail=(190, 180))
            + _shout("Ha ha!", 440, 110, size=24, rot=8, color="#C77DFF"))


# ---------------------------------------------------------------- story 09
def _rider(x, y, bs=1.0, rs=.9, expr='happy', look=(.6, 0), ears=None, muddy=False, lid=True, arm=True):
    """Rabbit riding bike(x, y, bs): returns (rider, legs) to hand to bike(), so the
    paws land on the handlebar and the feet on the pedals."""
    sx, sy = S.bike_seat(x, y, bs)
    gx, gy = S.bike_bar(x, y, bs)
    lx, ly = (gx - sx) / rs, (gy - sy) / rs
    extra = S.helmet(0, -126, s=1.0, rot=-4) if lid else ''
    if muddy:
        extra += "".join(S.splat(dx, dy, r) for dx, dy, r in ((-12, -30, 7), (14, -48, 6), (-18, -92, 5), (16, -72, 5), (4, -18, 6)))
    rid = rabbit(sx, sy + 2*bs, s=rs, pose='seated', expr=expr, look=look, ears=ears,
                 arm2=(lx - 24, ly + 44), arm=(lx + 24, ly + 44) if arm else (-34, -36), extra=extra)
    (nx, ny), (fx, fy) = S.bike_pedals(x, y, bs)
    legs = ""
    for hx, (px, py) in ((-8, (fx, fy)), (8, (nx, ny))):
        hipx, hipy = sx + hx*rs, sy - 4*rs
        legs += (_limb(hipx, hipy, px - hipx, py - hipy, R_BODY, R_LINE, 11*rs, bow=-.18)
                 + f'<ellipse cx="{px+3:.0f}" cy="{py:.0f}" rx="{12*rs:.1f}" ry="{6.5*rs:.1f}" fill="{R_BODY}" stroke="{R_LINE}" stroke-width="1.5"/>')
    return rid, legs


@alt('Rabbit stands with her shiny red bike and rings its bell, wearing a blue helmet, while Elephant cheers that he will help.')
def p09_1():
    """A shiny new bike - and no idea how to ride it."""
    return (S.sky('s9p1', 'morning', rays=True, sun=(440, 52))
            + S.ground('s9p1', flowers=((55, 242), (250, 236), (460, 250)))
            + S.tree(40, 214, s=.8)
            + S.shadow(130, 348, 56)
            + elephant(130, 350, s=1.25, expr='excited', look=(.7, -.1), trunk=(40, -40), arm=(46, -24))
            + S.shadow(320, 350, 70)
            + rabbit(306, 336, s=1.1, expr='happy', look=(.6, -.2), arm2=(36, -26),
                     extra=S.helmet(0, -126, rot=-4))
            + S.bike(316, 348, s=1.2)
            + _shout("Ring-ring!", 420, 190, size=24, rot=10, color="#C77DFF")
            + S.bubble("I'll help!", 110, 92, tail=(130, 200)))


@alt('A red bike lies tipped over by a hedge and only Rabbit\'s feet stick out of the leaves, while Elephant goes cross-eyed at a butterfly on the tip of his trunk.')
def p09_2():
    """A butterfly - Elephant lets go - CRASH, into the hedge."""
    return (S.sky('s9p2', 'morning', sun=(60, 52), clouds=((300, 46, 40, 15), (326, 40, 24, 12)))
            + S.ground('s9p2', tufts=(40, 160), flowers=((40, 246), (180, 252)))
            + S.flight([(80, 330), (140, 316), (190, 334), (240, 312), (290, 324)])
            + S.hedge(290, 500, 330, h=118)
            + _rfeet(370, 262, s=1.15)
            + S.leaves(((330, 210, -30), (420, 196, 30), (370, 180, 60), (460, 226, -50)))
            + S.spin(-22, 250, 344, S.bike(250, 344, s=1.05, spin=True))
            + S.shadow(110, 350, 56)
            + elephant(110, 350, s=1.25, expr='happy', look=(.5, -.9), trunk=(36, -60))
            + S.butterfly(166, 162, s=1.1)
            + _shout("CRASH!", 400, 150, size=32, rot=8)
            + _shout("wibble… wobble…", 250, 236, size=15, rot=-6, color="#8FA8C0"))


@alt('Rabbit rides her bike straight into a big muddy puddle with a SPLOSH, and mud flies everywhere and splats on her ears, while Elephant gasps.')
def p09_3():
    """Faster and faster - straight into the puddle."""
    rid, legs = _rider(290, 340, bs=1.1, rs=.9, expr='surprised', look=(0, -.4), ears=(-30, 30), muddy=True)
    return (S.sky('s9p3', 'tender', sun=(440, 52))
            + S.ground('s9p3', tufts=(40, 460), flowers=((40, 246), (460, 250)))
            + S.puddle(290, 340, rx=140, ry=22)
            + S.bike(290, 344, s=1.1, rider=rid, legs=legs)
            + S.mud_splash(290, 336, s=2.1)
            + S.speedlines(150, 280, n=3, length=30)
            + S.shadow(80, 350, 46)
            + elephant(80, 350, s=1.05, expr='surprised', look=(.8, -.2), trunk=(30, 30))
            + _shout("SPLOSH!", 300, 92, size=34, rot=-6, color=S.MUD_DK))


@alt('Elephant sits on Rabbit\'s little bike and squashes it flat as a pancake with a CRUNCH, while muddy Rabbit throws up her paws in shock.')
def p09_4():
    """'Let me show you how' - CRUNCH."""
    mud = "".join(S.splat(dx, dy, r) for dx, dy, r in ((-12, -40, 7), (16, -60, 6), (-14, -150, 5), (12, -132, 5)))
    return (S.sky('s9p4', 'tender', sun=(60, 52), clouds=((360, 46, 40, 15), (388, 40, 24, 12)))
            + S.ground('s9p4', tufts=(40, 460), flowers=((40, 246), (460, 250)))
            + S.shadow(220, 350, 90)
            + elephant(220, 334, s=1.25, pose='sit', expr='surprised', look=(.4, .5), trunk=(40, 30))
            + S.bike(214, 350, s=1.3, flat=True)
            + _pow(110, 320, 20) + _pow(330, 324, 16)
            + _shout("CRUNCH!", 220, 116, size=34, rot=-6)
            + '<circle cx="318" cy="318" r="6" fill="#FFD166" stroke="#D8A21F" stroke-width="1.2"/>'
            + _shout("ding… dunk", 316, 296, size=14, rot=8, color="#8FA8C0")
            + S.shadow(420, 350, 32)
            + rabbit(420, 352, s=1.05, expr='surprised', look=(-.8, .2), ears=(-24, 24), arm=(-30, -48), arm2=(30, -48), extra=mud))


@alt('Dr. Squirrel fixes Rabbit\'s bike with a spanner and adds two little training wheels, next to her toolbox, while Rabbit sits nearby with a plaster on her knee.')
def p09_5():
    """Dr. Squirrel: a plaster, a spanner, and training wheels."""
    return (S.sky('s9p5', 'morning', sun=(440, 52))
            + S.ground('s9p5', tufts=(40, 460), flowers=((40, 246), (460, 250), (180, 236)))
            + S.shadow(80, 350, 34)
            + rabbit(80, 352, s=1.05, pose='sit', expr='happy', look=(.8, -.2), arm2=(30, -8),
                     extra=S.plaster(18, -16, rot=-20))
            + S.doctor_bag(150, 352, s=.9)
            + S.bike(250, 346, s=1.15, training=True)
            + S.shadow(370, 350, 34)
            + squirrel(370, 350, s=1.15, expr='happy', look=(-.8, .3), arm=(-50, 12),
                       extra=S.spanner(-70, 22, s=1.0, rot=-110))
            + S.toolbox(452, 352, s=1.0)
            + S.bubble(["Training", "wheels!"], 400, 110, tail=(376, 220), color="#A2683F"))


@alt('Rabbit zooms down a bumpy hill on her bike as the training wheels ping off, one flying through the air and the other landing on Elephant\'s head like a hat.')
def p09_6():
    """Bumpety, bumpety, BUMP! PING! PING!"""
    rid, legs = _rider(0, 0, bs=1.05, rs=.86, expr='excited', look=(.6, .4), ears=(-30, -6))
    hill = ('<path d="M0,150 C90,146 200,190 290,262 C330,294 370,320 420,340 L420,360 L0,360 Z" fill="#7DBE6E"/>'
            '<path d="M0,150 C90,146 200,190 290,262 C330,294 370,320 420,340" stroke="#5E9B50" stroke-width="3" fill="none"/>')
    lumps = "".join(f'<path d="M{x},{y} q8,-8 16,0" stroke="#5E9B50" stroke-width="2.4" fill="none"/>' for x, y in ((60, 158), (120, 166), (180, 186)))
    return (S.sky('s9p6', 'morning', sun=(440, 52), clouds=((300, 46, 40, 15), (326, 40, 24, 12)))
            + S.ground('s9p6', tufts=(440,), flowers=((450, 250),))
            + hill + lumps
            + f'<g transform="translate(196,228) rotate(30)">' + S.bike(0, 0, s=1.05, rider=rid, legs=legs) + '</g>'
            + S.speedlines(110, 160, n=3, length=30)
            + S.toy_wheel(110, 96, r=10, rot=-50)
            + _shout("PING!", 70, 70, size=22, rot=-10, color="#C77DFF")
            + S.flight([(250, 240), (300, 170), (360, 150), (410, 176)])
            + S.shadow(420, 350, 50)
            + elephant(420, 350, s=1.15, expr='surprised', look=(-.6, -.6), trunk=(-30, 40),
                       extra=S.toy_wheel(4, -150, r=10, rot=6))
            + _pow(440, 184, 14)
            + _shout("BONK!", 446, 146, size=22, rot=10)
            + _shout("Bumpety BUMP!", 100, 300, size=18, rot=20, color="#A87A52"))


@alt('Rabbit sits sadly in the long grass after a tumble, her helmet thrown down beside her and her bike dropped in the grass, as Elephant comes over looking worried.')
def p09_7():
    """'I'm no good at this. I'll never, ever learn.'"""
    grass = "".join(f'<path d="M{x},360 q{lean},-24 {lean*2},-{h}" stroke="#4A9B4A" stroke-width="3" fill="none" stroke-linecap="round"/>'
                    for x, lean, h in ((150, -3, 40), (166, 2, 52), (180, -2, 36), (236, 3, 46), (252, -2, 38), (270, 2, 50)))
    return (S.sky('s9p7', 'tender', sun=None)
            + S.ground('s9p7', tufts=(40, 460), flowers=((40, 246), (460, 250)))
            + S.spin(-8, 90, 344, S.bike(90, 344, s=.95))
            + S.shadow(210, 350, 40)
            + rabbit(210, 352, s=1.15, pose='sit', expr='sad', look=(0, .5), ears=(-46, 46), arm=(20, 10), arm2=(-20, 10))
            + grass
            + S.helmet(316, 336, s=.9, rot=150)
            + "".join(f'<path d="M{x},{y} q-8,-4 -14,0" stroke="#8FA8C0" stroke-width="2.2" fill="none" stroke-linecap="round"/>' for x, y in ((296, 300), (300, 312)))
            + S.shadow(420, 350, 50)
            + elephant(420, 350, s=1.15, expr='worried', look=(-.9, .2), trunk=(-36, 40))
            + S.bubble(["I'll never,", "ever learn."], 200, 100, tail=(210, 190), color="#4AA8C8"))


@alt('Elephant and Rabbit sit together in the grass as Elephant tells about learning to roller skate, picturing himself on skates in the duck pond with a duck sitting on his head, and Rabbit giggles.')
def p09_8():
    """A hundred falls, and a duck on his head."""
    mini = (f'<ellipse cx="220" cy="144" rx="86" ry="16" fill="#9BDCF0"/>'
            + elephant(220, 140, s=.56, expr='surprised', look=(0, -.6), trunk=(-30, 30), arm=(30, -40),
                       extra=S.duck(0, -138, s=1.5) + S.skate(-24, 0, rot=-14) + S.skate(24, 4, rot=12))
            + '<path d="M146,148 q20,-8 40,0 M254,148 q20,-8 40,0" stroke="#EAF8FF" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
    return (S.sky('s9p8', 'golden', sun=(440, 60))
            + S.ground('s9p8', tufts=(40, 460), flowers=((40, 246), (460, 250)))
            + S.thought([], 220, 96, tail_to=(330, 220), picture=mini, rx=128, ry=76)
            + S.shadow(160, 350, 36)
            + rabbit(160, 352, s=1.05, pose='sit', expr='happy', look=(.8, -.3), arm=(-14, -40), arm2=(30, -40))
            + S.helmet(110, 350, s=.7, rot=0)
            + S.shadow(330, 350, 56)
            + elephant(330, 350, s=1.2, pose='sit', expr='happy', look=(-.7, .1), trunk=(-36, 30))
            + _shout("Hee hee!", 70, 200, size=22, rot=-8, color="#C77DFF"))


@alt('Rabbit pedals her bike with her helmet back on while Elephant runs beside her holding the seat, puffing and panting.')
def p09_9():
    """'Don't let go!' 'I won't!'"""
    rid, legs = _rider(310, 346, bs=1.15, rs=.9, expr='worried', look=(.4, 0))
    return (S.sky('s9p9', 'morning', sun=(440, 52), clouds=((80, 46, 40, 15), (108, 40, 24, 12)))
            + S.ground('s9p9', tufts=(40, 460), flowers=((40, 246), (460, 250)))
            + S.speedlines(60, 270, n=4, length=34)
            + S.shadow(190, 350, 56)
            + elephant(190, 350, s=1.15, expr='worried', look=(.8, 0), trunk=(-30, 44), arm=(56, -16))
            + S.sweat(150, 210, s=1.1)
            + S.shadow(310, 350, 60)
            + S.bike(310, 346, s=1.15, rider=rid, legs=legs)
            + S.bubble("Don't let go!", 380, 90, tail=(320, 170))
            + S.bubble("I won't!", 110, 130, tail=(170, 220), color="#4AA8C8"))


@alt('Rabbit rides her bike all by herself, shouting with joy and ringing her bell, while far behind her a small Elephant waves his trunk.')
def p09_10():
    """'I'M DOING IT!' - and Elephant let go ages ago."""
    rid, legs = _rider(320, 346, bs=1.25, rs=.98, expr='excited', look=(.6, -.3))
    path = '<path d="M30,214 Q160,232 300,280 Q400,320 500,330 L500,360 L250,360 Q220,300 30,222 Z" fill="#E8D6A8" opacity=".75"/>'
    return (S.sky('s9p10', 'golden', sun=(440, 52), rays=True)
            + S.ground('s9p10', tufts=(40, 460), flowers=((140, 300), (460, 250)))
            + path
            + elephant(70, 236, s=.42, expr='happy', look=(.6, 0), trunk=(30, -60), arm=(30, -40))
            + S.speedlines(150, 280, n=4, length=40)
            + S.shadow(320, 350, 64)
            + S.bike(320, 346, s=1.25, rider=rid, legs=legs, spin=True)
            + _shout("Ring-ring!", 436, 214, size=20, rot=10, color="#C77DFF")
            + S.bubble("I'M DOING IT!", 300, 70, tail=(310, 140)))


@alt('Elephant has crashed his big bike into the hedge and knocked the whole hedge flat, and sits dizzy among the leaves, while Rabbit on her bike and Dr. Squirrel laugh and cheer him on.')
def p09_11():
    """Elephant's turn - and the whole hedge falls over."""
    leaves = "".join(f'<ellipse cx="{x}" cy="{y}" rx="7" ry="3.5" fill="{S.LEAF}" transform="rotate({r} {x} {y})"/>'
                     for x, y, r in ((-14, -142, -30), (12, -146, 20), (2, -150, 70)))
    rid, legs = _rider(340, 346, bs=1.0, rs=.82, expr='happy', look=(-.8, -.2), arm=False)
    return (S.sky('s9p11', 'golden', sun=(440, 52), rays=True)
            + S.ground('s9p11', tufts=(300, 460), flowers=((300, 250), (460, 250)))
            + S.spin(-14, 110, 334, S.bike(110, 334, s=1.5, color="#74C8E4", line="#3C90AE", spin=True))
            + S.hedge(20, 290, 350, fallen=True)
            + elephant(186, 334, s=1.15, pose='sit', expr='happy', look=(.6, -.3), trunk=(40, -30), extra=leaves)
            + S.bike(340, 346, s=1.0, rider=rid, legs=legs)
            + S.shadow(450, 350, 26)
            + squirrel(450, 350, s=.9, expr='happy', look=(-.8, 0), arm=(-30, -30), arm2=(30, -30))
            + _shout("CRASH!", 150, 100, size=30, rot=-8)
            + S.bubble(["Every fall means", "you're learning!"], 360, 90, tail=(350, 190)))


# ---------------------------------------------------------------- story 10
HAT = S.sunhat(0, -134, s=1.0, rot=-6)    # Rabbit's straw hat, on her head
CLINIC = "#EEF4F7"


def _ghost():
    """Elephant under the bedsheet: a white drape over his head and ears, eye holes,
    and his trunk poking out through the front. In elephant-local coordinates."""
    hem = " ".join("l-12,-8 l-12,8" for _ in range(5))
    return (f'<path d="M-62,-40 Q-72,-118 -42,-148 Q0,-172 42,-148 Q72,-118 62,-40 {hem} Z" '
            f'fill="#FFFFFF" stroke="#C8D4DC" stroke-width="2"/>'
            f'<path d="M-50,-120 Q0,-136 50,-120" stroke="#74C8E4" stroke-width="5" fill="none" opacity=".6"/>'
            + "".join(f'<ellipse cx="{sx*14}" cy="-106" rx="8" ry="10" fill="{S.INK}"/>'
                      f'<circle cx="{sx*14+3}" cy="-109" r="2.6" fill="#FFFFFF"/>' for sx in (-1, 1))
            + _limb(0, -80, -26, 46, E_BODY, E_LINE, 15, bow=.2))


def _sock_ears():
    """Two socks dangling off the tips of Rabbit's ears (ears=(-24, 24))."""
    return S.sock(-26, -180, s=.85, rot=-30, color="#FF6B6B") + S.sock(26, -180, s=.85, rot=20, color="#74C8E4")


def _wiggle(x, y):
    """Wiggle marks either side of a twitching trunk tip."""
    return "".join(f'<path d="M{x+sx*14},{y-8} q{sx*5},4 0,8 q{-sx*5},4 0,8" stroke="#8FA8C0" stroke-width="2.2" '
                   f'fill="none" stroke-linecap="round"/>' for sx in (-1, 1))


def _ecover(dx=-60, dy=-30):
    """Elephant's arm crossed in front of his face, elbow over the trunk - drawn as
    `extra`, because the arm `elephant()` draws goes UNDER the head."""
    return _limb(26, -58, dx, dy, E_BODY, E_LINE, 14)


def _scover(dx=-46, dy=-34):
    """Dr. Sheep's elbow across her muzzle, likewise drawn over the head."""
    return (_limb(28, -64, dx, dy, S_FACE, S_FLINE, 9)
            + f'<ellipse cx="{28+dx}" cy="{-64+dy}" rx="5.5" ry="5" fill="{S_DARK}"/>')


def _home(uid):
    """Elephant's bedroom: warm wall, a sunny window, a rug."""
    return (S.indoors(uid, wall="#FFF3E4", floor="#EFE0C8", y=262)
            + S.garden_window(250, 120, w=100, h=80)
            + '<ellipse cx="250" cy="330" rx="200" ry="22" fill="#FFD9A8" opacity=".6"/>')


@alt('Elephant sniffles with a tickly trunk but says he is fine, while Rabbit, wearing her straw hat, carries a basket of washing towards the washing line.')
def p10_1():
    """A tickly trunk. 'I'm fine!'"""
    return (S.sky('s10p1', 'morning', rays=True, sun=(440, 52))
            + S.ground('s10p1', flowers=((55, 242), (250, 236), (460, 250)))
            + S.washing_line(290, 470, 262, h=120)
            + S.shadow(150, 348, 56)
            + elephant(150, 350, s=1.25, expr='calm', look=(.6, -.2), trunk=(30, -30))
            + _shout("sniff, sniff", 236, 172, size=15, rot=-8, color="#8FA8C0")
            + '<path d="M196,218 q-4,7 0,10 q4,-3 0,-10 Z" fill="#9BDCF0" stroke="#5AB6D6" stroke-width="1"/>'
            + S.shadow(350, 350, 34)
            + rabbit(350, 352, s=1.1, expr='happy', look=(-.7, -.2), arm=(-12, 14), arm2=(12, 14),
                     extra=HAT + S.basket(0, -8, w=76))
            + S.bubble("I'm fine!", 110, 86, tail=(150, 200)))


@alt('Elephant sneezes a giant ACHOO and the blast blows Rabbit\'s straw hat off her head, spinning all the way to the top of a tree.')
def p10_2():
    """ACHOO! The hat flies to the top of the tree."""
    return (S.sky('s10p2', 'tender', sun=(60, 52), clouds=((300, 46, 40, 15), (326, 40, 24, 12)))
            + S.ground('s10p2', tufts=(40, 300), flowers=((40, 246), (290, 250)))
            + S.tree(446, 236, s=1.3)
            + S.shadow(130, 348, 56)
            + elephant(130, 350, s=1.25, expr='sneeze', trunk=(80, -40))
            + S.sneeze(248, 198, ang=-6, s=1.0)
            + S.shadow(330, 350, 32)
            + rabbit(330, 352, s=1.1, expr='surprised', look=(.5, -.6), ears=(40, 60), arm=(-30, -40), arm2=(30, -44))
            + S.flight([(340, 190), (370, 130), (410, 96), (440, 84)])
            + S.sunhat(446, 82, s=.9, rot=12)
            + _shout("ACHOO!", 160, 116, size=36, rot=-8)
            + S.bubble("My hat!", 290, 76, tail=(320, 190)))


@alt('After another sneeze the washing has blown off the line: a bedsheet has landed on Elephant like a ghost costume, and two socks hang off Rabbit\'s ears.')
def p10_3():
    """Everything flies off the line - 'Whooo! I'm a ghost!'"""
    return (S.sky('s10p3', 'morning', sun=(440, 52))
            + S.ground('s10p3', tufts=(40, 460), flowers=((40, 246), (460, 250)))
            + S.washing_line(220, 460, 262, h=130, sag=14)
            + S.shirt(300, 86, s=1.0, rot=30, color="#FFD166")
            + S.shirt(420, 160, s=.9, rot=-40, color="#C77DFF")
            + S.sock(250, 40, s=1.0, rot=-50, color="#FFD166")
            + S.sock(360, 40, s=1.0, rot=60, color="#C77DFF")
            + S.shadow(140, 348, 56)
            + elephant(140, 350, s=1.2, expr='happy', arm=(36, -40), extra=_ghost())
            + S.shadow(370, 350, 32)
            + rabbit(370, 352, s=1.1, expr='happy', look=(-.6, -.2), ears=(-24, 24), arm=(-24, 12), arm2=(24, 12),
                     extra=_sock_ears())
            + S.bubble(["Whooo!", "I'm a ghost!"], 130, 74, tail=(140, 170)))


@alt('On the way to Dr. Sheep\'s clinic, Elephant sneezes again and Rabbit tumbles head over heels into a bush, with only her feet sticking out.')
def p10_4():
    """ACHOO! - Boing! - only her feet stick out."""
    return (S.sky('s10p4', 'morning', sun=(60, 52), clouds=((200, 46, 40, 15), (226, 40, 24, 12)))
            + S.ground('s10p4', tufts=(40, 200), flowers=((40, 246), (200, 250)))
            + S.hospital(350, 120, w=120, h=88)
            + S.shadow(110, 348, 54)
            + elephant(110, 350, s=1.2, expr='sneeze', trunk=(70, -10))
            + S.sneeze(206, 236, ang=-10, s=.9)
            + S.flight([(250, 300), (290, 220), (330, 196), (356, 230)])
            + S.bush(370, 352, w=170, h=116)
            + _rfeet(370, 206, s=1.5)
            + S.leaves(((300, 214, -30), (440, 200, 30), (420, 250, 60)))
            + _shout("Boing!", 290, 166, size=26, rot=-8, color="#C77DFF")
            + _shout("ACHOO!", 150, 120, size=32, rot=-8))


@alt('In the clinic, Dr. Sheep listens to Elephant\'s chest with her stethoscope when he sneezes right at her, blowing her wool up into a huge fluffy cloud and knocking her glasses onto her ear.')
def p10_5():
    """'Say ahhh' - ACHOO! - Dr. Sheep's wool goes POOF."""
    sx, sy, ss = 280, 350, 1.15
    hx, hy = sx - 72*ss, sy - 56*ss          # where her hoof lands on his chest
    scope = (f'<path d="M{sx-14*ss:.0f},{sy-82*ss:.0f} Q{sx-60:.0f},{sy-30:.0f} {hx+4:.0f},{hy:.0f}" stroke="{S_SCOPE}" '
             f'stroke-width="3" fill="none"/>'
             f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="8" fill="#C9D3DC" stroke="#7D8A96" stroke-width="2"/>')
    return (S.indoors('s10p5', wall=CLINIC, floor="#DCE6EC")
            + S.garden_window(80, 110, w=90, h=72)
            + S.fleece_cloud(sx, sy - 96, r=104)
            + S.shadow(150, 348, 54)
            + elephant(150, 350, s=1.2, expr='sneeze', trunk=(64, -14))
            + S.sneeze(240, 236, ang=-6, s=.9)
            + sheep(sx, sy, s=ss, expr='surprised', look=(-.4, -.2), arm=(-44, 8))
            + scope
            + S.specs(sx + 34*ss, sy - 115*ss, s=1.0, rot=80)
            + _shout("ACHOO!", 200, 110, size=34, rot=-8)
            + _shout("POOF!", 440, 120, size=24, rot=10, color="#C77DFF"))


@alt('Dr. Sheep holds a magnifying glass over the tip of Elephant\'s trunk, showing tiny green germs, and Elephant looks at Rabbit and gasps, "Oh no!"')
def p10_6():
    """Tiny germs, too small to see - except through the glass."""
    tip = (290, 262)
    inside = (_limb(tip[0] + 30, tip[1] - 60, -30, 60, E_BODY, E_LINE, 34, bow=.1)
              + S.germs(((tip[0]-20, tip[1]-8, .9), (tip[0]+8, tip[1]-22, .8), (tip[0]-6, tip[1]+18, .7),
                         (tip[0]+22, tip[1]+10, .8), (tip[0]-26, tip[1]+22, .6))))
    return (S.indoors('s10p6', wall=CLINIC, floor="#DCE6EC")
            + S.garden_window(250, 104, w=90, h=72)
            + S.shadow(340, 348, 54)
            + elephant(340, 350, s=1.2, expr='worried', look=(.8, -.1), trunk=(-44, 12))
            + S.shadow(110, 350, 40)
            + sheep(110, 350, s=1.15, expr='calm', look=(.8, 0), arm2=(48, 20),
                    extra=S.specs(0, -101))
            + S.magnifier('s10p6', tip[0], tip[1], r=40, inside=inside, rot=150)
            + S.shadow(458, 350, 24)
            + rabbit(458, 352, s=.9, expr='worried', look=(-.8, 0), arm=(-8, 30), arm2=(8, 30))
            + S.bubble("Oh no!", 386, 92, tail=(350, 196), color="#4AA8C8")
            + S.bubble("Germs!", 100, 120, tail=(110, 210), color="#3C90AE", size=12))


@alt('Dr. Sheep shows how to sneeze into your elbow; Elephant copies her, but his long trunk pokes out past his arm, and Rabbit giggles, "Fold it up!"')
def p10_7():
    """Into your elbow - but the trunk pokes out the other side."""
    return (S.indoors('s10p7', wall=CLINIC, floor="#DCE6EC")
            + S.garden_window(250, 104, w=90, h=72)
            + S.shadow(90, 350, 40)
            + sheep(90, 350, s=1.1, expr='calm', look=(.6, 0), extra=S.specs(0, -101) + _scover())
            + S.shadow(280, 348, 54)
            + elephant(280, 350, s=1.2, expr='surprised', look=(-.6, 0), trunk=(-84, 6), extra=_ecover())
            + S.shadow(430, 350, 30)
            + rabbit(430, 352, s=1.0, expr='happy', look=(-.7, -.2), arm=(-34, -30), arm2=(20, 14))
            + S.bubble(["Into your", "elbow!"], 100, 92, tail=(96, 200), color="#3C90AE")
            + S.bubble("Fold it up!", 400, 110, tail=(430, 200)))


@alt('At the washbasin Elephant scrubs and sings and sprays water with his trunk, and soap bubbles land on his head and on Rabbit\'s and Dr. Sheep\'s heads too.')
def p10_8():
    """Scrub, sing, spray - bubbles everywhere."""
    spray = ('<path d="M150,168 Q200,90 250,150" stroke="#9BDCF0" stroke-width="5" fill="none" stroke-linecap="round" '
             'stroke-dasharray="10 8"/>'
             + "".join(f'<path d="M{x},{y} q-4,6 0,9 q4,-3 0,-9 Z" fill="#9BDCF0" stroke="#5AB6D6" stroke-width="1"/>'
                       for x, y in ((180, 110), (226, 104), (262, 140), (206, 84))))
    return (S.indoors('s10p8', wall=CLINIC, floor="#DCE6EC")
            + S.sink(232, 336, running=True)
            + S.soap_bubbles(((206, 228, 10), (226, 222, 13), (250, 226, 9)))
            + S.shadow(100, 348, 54)
            + elephant(100, 350, s=1.2, expr='happy', look=(.6, -.4), trunk=(30, -66), arm=(62, -6))
            + spray
            + S.shadow(340, 350, 30)
            + rabbit(340, 352, s=1.0, expr='happy', look=(-.6, -.4), arm=(-30, -40), arm2=(30, -40))
            + S.shadow(445, 350, 36)
            + sheep(445, 350, s=1.05, expr='happy', look=(-.6, -.3), arm=(-30, -20), extra=S.specs(0, -101))
            + S.soap_bubbles(((92, 166, 10), (112, 160, 8), (334, 210, 10), (350, 202, 8), (438, 206, 10), (456, 200, 7),
                              (60, 120, 12), (300, 80, 14), (400, 120, 11), (160, 50, 9), (470, 70, 12), (30, 210, 8)))
            + S.notes(((40, 170, 20), (70, 140, 16), (290, 160, 18))))


@alt('Back home, Elephant sits up in bed with a bowl of soup as his trunk starts to wiggle, "Ah… ah…", and Rabbit dives head-first behind the sofa.')
def p10_9():
    """'Ah… ah…' - and Rabbit dives for cover."""
    ele = elephant(150, 314, s=1.05, pose='seated', expr='worried', look=(0, -.6), trunk=(20, -44))
    return (_home('s10p9')
            + S.little_bed(160, 340, w=230, sleeper=ele, quilt="#FF9BAE")
            + S.soup(198, 300, s=1.0)
            + _wiggle(176, 186)
            + S.speedlines(450, 170, n=3, length=30, back=False)
            + S.clip('s10p9r', 300, 0, 200, 256, S.spin(164, 410, 186, rabbit(410, 186, s=.9, expr='surprised', arm=(-20, 30), arm2=(20, 30))))
            + S.sofa(400, 350, w=170)
            + _shout("Eek!", 340, 160, size=24, rot=-10, color="#C77DFF")
            + S.bubble("Ah… ah…", 120, 96, tail=(150, 190), color="#4AA8C8"))


@alt('Elephant sneezes the tiniest sneeze into his elbow, with his trunk tucked away, and nothing moves at all, while Rabbit peeks over the sofa and asks, "Was that it?"')
def p10_10():
    """'…achoo.' The tiniest sneeze ever."""
    ele = elephant(150, 314, s=1.05, pose='seated', expr='sneeze', trunk=(14, 4), extra=_limb(26, -48, -60, -26, E_BODY, E_LINE, 14))
    paws = "".join(f'<ellipse cx="{x}" cy="250" rx="9" ry="7" fill="{R_BODY}" stroke="{R_LINE}" stroke-width="1.5"/>'
                   for x in (378, 422))
    return (_home('s10p10')
            + S.little_bed(160, 340, w=230, sleeper=ele, quilt="#FF9BAE")
            + S.soup(198, 300, s=1.0)
            + _shout("…achoo.", 230, 196, size=14, rot=-4, color="#8FA8C0")
            + rabbit(400, 336, s=1.0, expr='surprised', look=(-.8, -.1), ears=(-14, 14))
            + S.sofa(400, 350, w=170)
            + paws
            + S.bubble("Was that it?", 390, 90, tail=(400, 180)))


@alt('A few days later the washing flaps on the line, Elephant is all better, and Nurse Giraffe stretches her long neck to bring Rabbit\'s straw hat down from the top of the tree.')
def p10_11():
    """All better - and the hat comes down from the tree."""
    hat = S.sunhat(30, -222, s=.9, rot=24)
    return (S.sky('s10p11', 'golden', sun=(60, 52), rays=True)
            + S.ground('s10p11', tufts=(40, 300), flowers=((40, 246), (300, 250)))
            + S.washing_line(30, 230, 262, h=120,
                             items=((.18, 'sock', "#FF6B6B"), (.38, 'shirt', "#74C8E4"), (.56, 'sock', "#FFD166"),
                                    (.8, 'sheet', "#FFFFFF")))
            + S.tree(440, 236, s=1.3)
            + S.shadow(400, 350, 40)
            + giraffe(400, 350, s=1.0, pose='stretch', expr='happy', look=(-.6, .2), cap=False, extra=hat)
            + S.shadow(130, 350, 54)
            + elephant(130, 350, s=1.2, expr='happy', look=(.7, -.3), trunk=(-30, 40), arm=(34, -40))
            + S.shadow(280, 350, 30)
            + rabbit(280, 352, s=1.05, expr='excited', look=(.7, -.6), arm=(-28, -44), arm2=(30, -44))
            + S.bubble("My hat!", 280, 90, tail=(280, 190)))


# ---------------------------------------------------------------- story 11
FLOUR = {E_BODY: "#F2F0EA", "#C5D8E0": "#FFFFFF", E_LINE: "#C8C4BA",
         R_BODY: "#FFFFFF", R_LINE: "#D8D4CC", R_EAR: "#FBE4EA"}


def _floury(svg):
    """A character after the POOF: every grey and cream turned flour-white."""
    for a, b in FLOUR.items():
        svg = svg.replace(a, b)
    return svg


def _dust(pts):
    """Flour specks hanging in the air."""
    return "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" opacity=".9"/>' for x, y, r in pts)


DUST = ((60, 60, 3), (140, 40, 2.4), (210, 90, 3.4), (300, 50, 2.6), (420, 70, 3), (470, 140, 2.4),
        (30, 170, 2.6), (190, 180, 2.2), (330, 150, 3), (260, 30, 2), (380, 200, 2.4), (90, 120, 2.2))


def _back(arms=False):
    """Elephant seen from BEHIND, arms in the air: the burrow-door rump with a head,
    ears and raised arms on top. Local coordinates, origin on the ground."""
    out = _rump(0, 0)
    out += (f'<circle cx="0" cy="-196" r="44" fill="{E_BODY}" stroke="{E_LINE}" stroke-width="1.8"/>'
            + "".join(f'<ellipse cx="{sx*46}" cy="-200" rx="26" ry="36" fill="{E_BODY}" stroke="{E_LINE}" stroke-width="1.8"/>'
                      for sx in (-1, 1)))
    if arms:
        out += "".join(_limb(sx*62, -150, sx*34, -66, E_BODY, E_LINE, 22) for sx in (-1, 1))
    return out


def _kitchen11(uid, oven=True):
    return (S.kitchen(uid)
            + S.porthole(80, 90, sky='morning')
            + S.shelf(230, 110)
            + (S.oven(385, 262) if oven else ''))


@alt('In the kitchen, Rabbit holds up a cake recipe and says first they must measure the flour, while Elephant gives a big yawn and says, "Let\'s be quick!"')
def p11_1():
    """'First we measure the flour.' 'Recipes are so slow.'"""
    return (_kitchen11('s11p1')
            + S.table(240, 292, w=150)
            + S.mixing_bowl(226, 292, w=70, batter=False)
            + S.flour_bag(282, 292)
            + S.egg(180, 282) + S.egg(196, 284, rot=24)
            + S.shadow(100, 348, 54)
            + elephant(100, 350, s=1.2, expr='yawn', trunk=(-20, 40))
            + S.shadow(400, 350, 32)
            + rabbit(400, 352, s=1.1, expr='excited', look=(-.4, -.6), arm=(-20, 10), arm2=(30, -50),
                     extra=S.recipe(58, -124, s=1.1, rot=10))
            + S.bubble(["First we measure", "the flour."], 360, 70, tail=(390, 190))
            + S.bubble(["Recipes are slow.", "Let's be quick!"], 130, 80, tail=(110, 196), color="#4AA8C8", size=12))


@alt('POOF! A huge white cloud of flour fills the kitchen, and Rabbit and Elephant are white from head to toe, with Elephant pretending to be a snowman.')
def p11_2():
    """POOF! 'We're snowmen!'"""
    return (_kitchen11('s11p2')
            + S.fleece_cloud(250, 190, r=120, fill="#FFFFFF", line="#ECE6DA", swirl="#F1ECE2")
            + S.table(250, 292, w=150)
            + S.mixing_bowl(240, 292, w=70, batter=False)
            + S.flour_bag(292, 286, rot=100, empty=True)
            + S.shadow(110, 348, 54)
            + _floury(elephant(110, 350, s=1.2, expr='excited', look=(.5, -.3), trunk=(36, -50), arm=(40, -44)))
            + S.shadow(400, 350, 32)
            + _floury(rabbit(400, 352, s=1.1, expr='surprised', look=(-.5, -.3), arm=(-30, -40), arm2=(30, -40)))
            + _dust(DUST)
            + _shout("POOF!", 250, 66, size=40, rot=-6, color="#74C8E4")
            + S.bubble(["Boo! We're", "snowmen!"], 110, 76, tail=(110, 180), color="#4AA8C8"))


@alt('Elephant cracks the eggs on the bowl with a big BONK, and the eggs fly through the air and land splat on Rabbit\'s head, dripping down her ears.')
def p11_3():
    """BONK - the shells in the bowl, the eggs on Rabbit."""
    return (_kitchen11('s11p3')
            + S.table(240, 292, w=150)
            + S.mixing_bowl(240, 292, w=80, batter=False)
            + S.eggshell(226, 246, s=1.1, rot=-10) + S.eggshell(256, 244, s=1.1, rot=14)
            + S.shadow(100, 348, 54)
            + _floury(elephant(100, 350, s=1.2, expr='excited', look=(.7, .3), trunk=(98, -14)))
            + _pow(232, 236, 16)
            + _shout("BONK!", 210, 200, size=26, rot=-8)
            + S.flight([(250, 232), (290, 150), (340, 140), (380, 186)])
            + S.shadow(400, 350, 32)
            + _floury(rabbit(400, 352, s=1.1, expr='surprised', look=(0, -.8), ears=(-20, 20)))
            + S.egg_splat(400, 204, s=1.15)
            + "".join(f'<path d="M{x},{y} q-4,6 0,9 q4,-3 0,-9 Z" fill="#FFC23A" stroke="#E8A21F" stroke-width="1"/>'
                      for x, y in ((372, 230), (432, 238), (380, 262)))
            + _shout("Drip, drip.", 320, 336, size=16, rot=-4, color="#E8A21F"))


@alt('Elephant whizzes the mixer on SUPER FAST and cake mix splatters all over the walls and ceiling, with a blob on his trunk, while Rabbit ducks with her paws over her head.')
def p11_4():
    """WHIRRRR! Cake mix on the walls, the ceiling, and Elephant's nose."""
    blobs = "".join(S.splat(x, y, r, color=S.BATTER) for x, y, r in
                    ((60, 40, 9), (170, 26, 8), (300, 34, 10), (430, 50, 9), (40, 200, 8), (350, 190, 9), (460, 130, 8),
                     (240, 70, 7), (130, 150, 7)))
    return (_kitchen11('s11p4')
            + blobs
            + S.table(240, 292, w=150)
            + S.mixing_bowl(240, 292, w=80)
            + S.mixer(240, 254, s=1.1, whirl=True)
            + S.shadow(100, 348, 54)
            + _floury(elephant(100, 350, s=1.2, expr='surprised', look=(.6, -.2), trunk=(118, -40)))
            + S.splat(132, 244, 9, color=S.BATTER)
            + S.shadow(410, 350, 32)
            + _floury(rabbit(410, 352, s=1.05, expr='worried', look=(-.4, -.6), ears=(-64, 64), arm=(20, -60), arm2=(-20, -60)))
            + _shout("WHIRRRR!", 250, 140, size=30, rot=-6, color="#FF6B6B")
            + _shout("Splot.", 176, 214, size=18, rot=-8, color=S.BATTER_DK))


@alt('Elephant opens the oven door to peek, and the cake inside, which was growing big and tall, sinks flat as a pancake, while Rabbit points at the recipe and says to wait.')
def p11_5():
    """Peek… peek… PEEK! - pfffff."""
    flat = S.cake(370, 300, w=84, kind='flat')
    return (_kitchen11('s11p5', oven=False)
            + S.oven(370, 334, w=150, h=132, door='open', inside=flat)
            + S.shadow(200, 348, 54)
            + _floury(elephant(200, 350, s=1.2, expr='surprised', look=(.9, .4), trunk=(80, 20)))
            + _shout("PEEK!", 280, 150, size=28, rot=-8)
            + _shout("pfffff…", 420, 186, size=20, rot=6, color="#6E7880")
            + S.shadow(70, 350, 30)
            + _floury(rabbit(70, 352, s=1.0, expr='worried', look=(.6, -.2), arm2=(28, -46),
                             extra=S.recipe(52, -114, s=1.0, rot=8)))
            + S.bubble(["Wait thirty", "minutes!"], 100, 80, tail=(80, 186)))


@alt('Bear arrives at the kitchen door a day early and blinks at Elephant, who is sitting on the flat cake, and Rabbit, who stands in front of the messy kitchen with her arms spread wide, both still white with flour.')
def p11_6():
    """Ding-dong! 'Why are you two covered in snow?'"""
    blobs = "".join(S.splat(x, y, r, color=S.BATTER) for x, y, r in ((340, 196, 9), (420, 160, 8), (460, 220, 9), (300, 60, 8)))
    return (S.kitchen('s11p6')
            + _doorway(24, 124, 110, 262)
            + S.porthole(230, 90, sky='morning')
            + blobs
            + S.oven(385, 262)
            + S.shadow(74, 294, 30)
            + bear(74, 296, s=.95, expr='surprised', look=(.8, .1), arm2=(26, 6))
            + f'<ellipse cx="240" cy="338" rx="72" ry="12" fill="{S.SPONGE}" stroke="{S.SPONGE_DK}" stroke-width="1.6"/>'
            + _floury(elephant(240, 344, s=1.1, pose='sit', expr='guilty', look=(-.8, -.1), trunk=(-24, 30)))
            + S.eggshell(310, 340, s=1.2, rot=20) + S.flour_bag(470, 350, rot=70, empty=True)
            + S.shadow(400, 350, 32)
            + _floury(rabbit(400, 352, s=1.05, expr='guilty', look=(-.8, 0), arm=(-46, -6), arm2=(46, -6)))
            + _shout("Ding-dong!", 300, 150, size=22, rot=-6, color="#C77DFF")
            + S.bubble(["Why are you two", "covered in snow?"], 190, 70, tail=(90, 170), color="#A87A52", size=12))


@alt('Bear puts a kind paw on sad Rabbit\'s shoulder and pictures a staircase with a cake at the top, saying they will go one step at a time, while Elephant looks sorry.')
def p11_7():
    """'Baking is like climbing stairs. One step at a time.'"""
    pic = S.stairs(374, 130, n=4, step=14) + S.cake(460, 74, w=34, kind='tall')
    return (_kitchen11('s11p7')
            + S.shadow(190, 350, 32)
            + _floury(rabbit(190, 352, s=1.1, expr='sad', look=(.6, -.2), ears=(-70, 70)))
            + S.shadow(320, 348, 36)
            + bear(320, 350, s=1.15, expr='happy', look=(-.7, .2), arm=(-60, -12))
            + S.shadow(450, 350, 40)
            + _floury(elephant(450, 350, s=.95, expr='guilty', look=(-.8, .3), trunk=(-20, 40)))
            + S.thought([], 420, 100, (330, 196), picture=pic, rx=74, ry=52)
            + S.bubble(["One step", "at a time!"], 250, 74, tail=(316, 200), color="#A87A52"))


@alt('Doing it properly: Rabbit reads the recipe out loud, Elephant carefully scoops one cup of flour with his trunk, and Bear gently taps an egg on the bowl.')
def p11_8():
    """One cup, very carefully. Tap, tap."""
    return (_kitchen11('s11p8')
            + S.shadow(250, 300, 40)
            + elephant(250, 302, s=1.0, expr='calm', look=(-.4, .6), trunk=(-16, 14))
            + S.measuring_cup(224, 232, s=1.0)
            + S.table(250, 296, w=190)
            + S.mixing_bowl(220, 296, w=74, batter=False)
            + S.flour_bag(160, 296)
            + S.shadow(80, 350, 30)
            + rabbit(80, 352, s=1.05, expr='happy', look=(.4, -.5), arm2=(30, -46), extra=S.recipe(54, -118, s=1.0, rot=8))
            + S.shadow(420, 350, 34)
            + bear(380, 352, s=1.1, expr='calm', look=(-.8, .4), arm=(-77, -27))
            + S.egg(264, 256, s=1.1, rot=-20, cracked=True)
            + _shout("tap, tap", 300, 230, size=16, rot=-6, color="#A87A52")
            + S.bubble(["One cup", "of flour…"], 100, 90, tail=(90, 190)))


@alt('Everyone waits by the oven as the cake grows inside: Elephant sits on his paws while his trunk creeps towards the oven door, Rabbit holds on to his trunk, and Bear sings and counts to a hundred.')
def p11_9():
    """The hardest step: waiting."""
    tin = S.cake(380, 288, w=80, kind='tin')
    return (_kitchen11('s11p9', oven=False)
            + S.oven(380, 340, w=150, h=132, light=True, inside=tin)
            + S.shadow(80, 350, 34)
            + bear(80, 350, s=1.0, pose='sit', expr='happy', look=(.6, -.3), arm=(-24, -30), arm2=(24, -30))
            + S.notes(((40, 180, 20), (70, 150, 16), (120, 170, 18)))
            + S.shadow(210, 350, 50)
            + elephant(210, 350, s=1.1, pose='sit', expr='worried', look=(.9, 0), trunk=(118, -2))
            + S.shadow(300, 350, 26)
            + rabbit(300, 352, s=.9, expr='calm', look=(-.6, -.6), arm=(-10, -66), arm2=(10, -66))
            + _shout("…98, 99, 100!", 250, 70, size=22, rot=-4, color="#C77DFF"))


@alt('DING! A big, tall, fluffy cake sits on the table, and as Elephant jumps up to cheer, Bear laughs and points at the flat cake still stuck to his bottom.')
def p11_10():
    """DING! The tall cake - and the flat one on Elephant's bottom."""
    stuck = (f'<ellipse cx="0" cy="-96" rx="48" ry="30" fill="{S.SPONGE}" stroke="{S.SPONGE_DK}" stroke-width="2" transform="rotate(-6 0 -96)"/>'
             f'<ellipse cx="0" cy="-100" rx="38" ry="20" fill="#F6CC80" opacity=".8" transform="rotate(-6 0 -100)"/>')
    crumbs = "".join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="{S.SPONGE}"/>' for x, y in ((70, 336), (150, 340), (100, 352)))
    return (_kitchen11('s11p10')
            + _pow(385, 140, 20, "#FFE39A")
            + _shout("DING!", 410, 110, size=30, rot=8)
            + S.table(250, 296, w=150)
            + S.cake(250, 296, w=100, kind='tall')
            + S.shadow(110, 350, 50, op=.08)
            + f'<g transform="translate(110 324) scale(.8)">{_back(arms=True)}{stuck}</g>'
            + S.speedlines(110, 344, n=2, length=20)
            + crumbs
            + S.shadow(360, 350, 28)
            + rabbit(360, 352, s=.95, expr='happy', look=(-.8, .3), arm=(-30, -40), arm2=(30, -40))
            + S.shadow(445, 350, 34)
            + bear(445, 352, s=1.05, expr='happy', look=(-.9, .4), arm=(-60, 6))
            + _shout("Ha ha!", 466, 200, size=22, rot=8, color="#A87A52")
            + S.bubble("Hooray!", 110, 70, tail=(110, 140), color="#4AA8C8"))


@alt('A birthday party in the kitchen: under bunting and party hats, Rabbit, Elephant and Bear share the tall cake and the flat "pancake cake," each with a lit candle, and Bear says both are delicious.')
def p11_11():
    """Two cakes, both delicious."""
    return (_kitchen11('s11p11')
            + S.bunting(0, 500, 18, sag=26, n=12)
            + S.table(300, 300, w=200)
            + S.cake(260, 300, w=96, kind='tall', candles=3)
            + S.cake(352, 300, w=70, kind='flat', candles=1)
            + S.shadow(80, 348, 52)
            + elephant(80, 350, s=1.15, expr='happy', look=(.6, -.2), trunk=(40, -40),
                       extra=S.party_hat(0, -138, s=1.1, rot=-6, color="#74C8E4"))
            + S.shadow(170, 350, 28)
            + rabbit(170, 352, s=.95, expr='happy', look=(.6, -.2), arm=(-26, -40), arm2=(30, -36),
                     extra=S.party_hat(0, -136, s=.9, rot=8, color="#FF6B6B"))
            + S.shadow(450, 350, 34)
            + bear(450, 352, s=1.1, expr='happy', look=(-.6, -.2), arm=(-46, -10),
                   extra=S.party_hat(0, -134, s=1.0, rot=-4, color="#C77DFF"))
            + S.bubble(["Both are", "delicious!"], 420, 86, tail=(446, 190), color="#A87A52"))


# ---------------------------------------------------------------- story 12
BELT = S.belt()


def _rpaw(x, y, s, a, right=True):
    """Where Rabbit's paw ends up, in scene coordinates, for arm offset `a`."""
    return x + s*((24 if right else -24) + a[0]), y + s*(-60 + a[1])


def _etip(x, y, s, t, pose='stand'):
    """Where Elephant's trunk tip ends up, in scene coordinates."""
    hy = {'stand': -100, 'sit': -92}[pose]
    return x + s*1.14*t[0], y + s*(hy + 20 + t[1])


def _windy(uid, mood='morning', **kw):
    return S.sky(uid, mood, **kw) + S.ground(uid, tufts=(40, 300, 460), flowers=((40, 246), (300, 252), (460, 250)))


@alt('On a windy day Nurse Giraffe holds up a bright red kite with a long wiggly tail as a present, and Rabbit and Elephant jump with excitement.')
def p12_1():
    """A bright red kite - 'for both of you.'"""
    return (_windy('s12p1', rays=True, sun=(440, 52))
            + S.gust(120, 70) + S.gust(330, 120, s=.8)
            + S.leaves(((60, 130, -30), (240, 100, 40), (400, 170, 10)))
            + S.shadow(110, 348, 54)
            + elephant(110, 350, s=1.2, expr='excited', look=(.7, -.4), trunk=(40, -50), arm=(36, -40))
            + S.shadow(250, 350, 30)
            + rabbit(250, 352, s=1.05, expr='excited', look=(.7, -.6), arm=(-28, -44), arm2=(30, -44), extra=BELT)
            + S.shadow(400, 350, 40)
            + giraffe(400, 350, s=1.05, expr='happy', look=(-.7, .2), cap=False, arm=(40, -84))
            + S.kite(454, 132, s=1.1, rot=-14)
            + S.bubble(["It's for", "both of you!"], 300, 70, tail=(390, 180), color="#C77DFF"))


@alt('Rabbit and Elephant both grab the kite string and tug it back and forth, shouting "Me first!", while the kite zigzags up and down in the sky.')
def p12_2():
    """Tug! Tug! Tug!"""
    ra = (36, -40)
    rx, ry = _rpaw(120, 352, 1.1, ra)
    et = (-84, -6)
    ex, ey = _etip(370, 350, 1.2, et)
    kx, ky = 250, 80
    return (_windy('s12p2', mood='tender', sun=(60, 52))
            + S.flight([(150, 120), (190, 60), (220, 140), (250, 80)])
            + S.kite(kx, ky, s=1.0, rot=10)
            + S.kite_string(kx, ky, (rx+ex)/2, (ry+ey)/2, sag=0)
            + f'<path d="M{rx:.0f},{ry:.0f} L{ex:.0f},{ey:.0f}" stroke="#6B5B47" stroke-width="1.6"/>'
            + S.shadow(120, 350, 32)
            + S.spin(-8, 120, 352, rabbit(120, 352, s=1.1, expr='shout', look=(.6, 0), arm2=ra, arm=(30, -10), extra=BELT))
            + S.shadow(370, 348, 54)
            + S.spin(8, 370, 350, elephant(370, 350, s=1.2, expr='shout', look=(-.6, 0), trunk=et))
            + _shout("Tug!", 250, 330, size=24, rot=-8, color="#C77DFF")
            + S.bubble("Me first!", 90, 150, tail=(110, 220))
            + S.bubble("No, me first!", 410, 130, tail=(380, 200), color="#4AA8C8"))


@alt('Elephant has fallen backwards onto his bottom with a BUMP, and the kite dives down and bonks Nurse Giraffe on the nose, while Rabbit gasps.')
def p12_3():
    """BUMP! - and the kite bonks Giraffe on the nose."""
    legs = _foot(-44, -4) + _foot(44, -4)
    return (_windy('s12p3', mood='tender', sun=(60, 52))
            + S.shadow(120, 350, 60)
            + elephant(120, 346, s=1.15, pose='sit', expr='surprised', look=(.4, -.6), trunk=(40, -40), extra=legs)
            + _shout("BUMP!", 120, 170, size=26, rot=-10, color="#A87A52")
            + S.shadow(260, 350, 28)
            + rabbit(260, 352, s=1.0, expr='surprised', look=(.6, -.6), arm=(-26, -40), arm2=(26, -40), extra=BELT)
            + S.shadow(410, 350, 40)
            + giraffe(410, 350, s=1.05, expr='hurt', look=(-.2, -.6), cap=False)
            + S.kite_string(140, 240, 360, 190, sag=-.14)
            + S.kite(372, 196, s=.95, rot=-110)
            + _pow(406, 206, 14)
            + S.bubble("Ow!", 340, 80, tail=(400, 170), color="#C77DFF"))


@alt('A huge gust of wind lifts the kite, and Rabbit holding the string floats up into the air like a balloon, crying "Heeelp!", while Elephant reaches up in alarm.')
def p12_4():
    """WHOOOSH! Rabbit floats up like a balloon."""
    ra = (14, -56)
    rx, ry = _rpaw(300, 230, 1.0, ra)
    return (_windy('s12p4', mood='morning', sun=(60, 52))
            + S.gust(110, 110) + S.gust(180, 220, s=.8) + S.gust(300, 300, s=.7)
            + S.kite(430, 60, s=1.2, rot=20)
            + S.kite_string(rx, ry, 426, 66)
            + rabbit(300, 230, s=1.0, expr='worried', look=(.4, -.6), ears=(30, 50), arm2=ra, arm=(-6, -56), extra=BELT)
            + S.shadow(300, 350, 20, op=.08)
            + S.shadow(110, 348, 54)
            + elephant(110, 350, s=1.2, expr='surprised', look=(.8, -.6), trunk=(60, -60), arm=(40, -50))
            + _shout("WHOOOSH!", 210, 70, size=30, rot=-6, color="#74C8E4")
            + S.bubble("Heeelp!", 410, 170, tail=(330, 140)))


@alt('Elephant has caught floating Rabbit by the feet with his trunk but is being dragged through the mud, and Nurse Giraffe holds on to his tail, all of them in one long wobbly line under the kite.')
def p12_5():
    """A long, wobbly line."""
    ra = (12, -54)
    rx, ry = _rpaw(380, 196, .95, ra)
    et = (79, -70)
    tail = (f'<path d="M-36,-40 q-30,-8 -46,-26" stroke="{E_LINE}" stroke-width="6" fill="none" stroke-linecap="round"/>'
            f'<path d="M-36,-40 q-30,-8 -46,-26" stroke="{E_BODY}" stroke-width="3.6" fill="none" stroke-linecap="round"/>')
    return (_windy('s12p5', mood='tender', sun=None)
            + S.gust(100, 80) + S.gust(240, 60, s=.8)
            + S.kite(450, 50, s=1.1, rot=24)
            + S.kite_string(rx, ry, 446, 56)
            + rabbit(380, 196, s=.95, expr='worried', look=(-.4, .6), ears=(30, 50), arm2=ra, arm=(-6, -56), extra=BELT)
            + S.puddle(250, 344, rx=110, ry=16)
            + S.mud_splash(300, 340, s=.9)
            + S.speedlines(150, 330, n=3, length=26, back=False)
            + elephant(250, 346, s=1.15, expr='worried', look=(.6, -.6), trunk=et, extra=tail)
            + S.shadow(90, 350, 40)
            + giraffe(90, 350, s=1.0, expr='worried', look=(.8, 0), cap=False, arm=(50, -6))
            + _shout("Hold on!", 120, 120, size=22, rot=-6, color="#C77DFF"))


@alt('The wind has stopped and Rabbit has dropped safely into Elephant\'s arms, but the kite has flown off and is stuck at the very top of a tall tree.')
def p12_6():
    """Plop. And the kite, all by itself, up the tree."""
    rab = rabbit(250, 262, s=.8, pose='sit', expr='surprised', look=(.8, -.6), ears=(-10, 30), arm=(-20, -20), extra=BELT)
    return (_windy('s12p6', mood='tender', sun=None)
            + S.tall_tree(410, 350, h=300)
            + S.kite(406, 86, s=.9, rot=-30)
            + '<path d="M406,120 q-14,60 4,110 q10,30 -6,60" stroke="#6B5B47" stroke-width="1.4" fill="none"/>'
            + S.shadow(170, 348, 54)
            + elephant(170, 350, s=1.2, expr='surprised', look=(.8, -.6), trunk=(60, -10), arm=(44, -20))
            + rab
            + _shout("Plop.", 320, 226, size=22, rot=8, color="#C77DFF"))


@alt('Rabbit and Elephant shout at each other that it was the other one\'s fault, while Nurse Giraffe stands between them shaking her head, and the kite hangs stuck in the tree behind.')
def p12_7():
    """'YOUR fault!' 'No, YOUR fault!'"""
    shake = "".join(f'<path d="M{259+sx*34},{196} q{sx*6},8 0,16" stroke="#8FA8C0" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
                    for sx in (-1, 1))
    return (_windy('s12p7', mood='tender', sun=None)
            + S.tall_tree(250, 230, h=200)
            + S.kite(250, 60, s=.6, rot=-30, tail=False)
            + S.shadow(100, 350, 32)
            + rabbit(100, 352, s=1.1, expr='shout', look=(.7, 0), arm=(-30, -10), arm2=(40, -20), extra=BELT)
            + S.shadow(400, 348, 54)
            + elephant(400, 350, s=1.2, expr='shout', look=(-.7, 0), trunk=(-60, 10))
            + S.shadow(250, 350, 36)
            + giraffe(250, 350, s=.95, expr='worried', look=(0, .2), cap=False)
            + shake
            + S.bubble("YOUR fault!", 100, 120, tail=(110, 200))
            + S.bubble(["No, YOUR", "fault!"], 410, 110, tail=(400, 200), color="#4AA8C8"))


@alt('Nurse Giraffe stretches her long, long neck up to the top of the tree and brings the kite back in her mouth, with a bird\'s nest and a little bird sitting on her head, while Rabbit and Elephant stare up amazed.')
def p12_8():
    """The long, long neck - and a nest for a hat."""
    gx, gy, gs = 330, 350, 1.05
    hx, hy = gx + 16*gs, gy - 250*gs
    return (_windy('s12p8', mood='golden', sun=(60, 52))
            + S.tall_tree(400, 350, h=300)
            + S.shadow(gx, gy, 40)
            + giraffe(gx, gy, s=gs, pose='stretch', expr='happy', look=(-.6, .4), cap=False)
            + S.bird_nest(hx, hy - 20, s=1.0)
            + S.kite(hx + 22, hy + 52, s=.8, rot=-14)
            + _shout("Tweet!", hx + 70, hy - 30, size=20, rot=8, color="#3C90AE")
            + S.shadow(110, 348, 54)
            + elephant(110, 350, s=1.2, expr='excited', look=(.8, -.8), trunk=(30, -50))
            + S.shadow(220, 350, 28)
            + rabbit(220, 352, s=1.0, expr='excited', look=(.8, -.8), arm=(-26, -40), arm2=(26, -44), extra=BELT))


@alt('Taking turns: Elephant flies the kite high in the sky with the string in his trunk, while Rabbit happily counts slowly to fifty.')
def p12_9():
    """Elephant goes first; Rabbit counts to fifty."""
    et = (36, -66)
    ex, ey = _etip(150, 350, 1.2, et)
    return (_windy('s12p9', mood='morning', sun=(60, 52))
            + S.gust(300, 150, s=.8)
            + S.kite(410, 60, s=1.1, rot=16)
            + S.kite_string(ex, ey, 406, 66)
            + S.shadow(150, 348, 54)
            + elephant(150, 350, s=1.2, expr='happy', look=(.8, -.8), trunk=et)
            + S.shadow(360, 350, 30)
            + rabbit(360, 352, s=1.05, expr='happy', look=(-.6, -.4), arm=(-26, -30), arm2=(26, -30), extra=BELT)
            + S.bubble(["…48, 49,", "FIFTY!"], 380, 160, tail=(366, 210), color="#C77DFF"))


@alt('Now it is Rabbit\'s turn: she flies the kite higher and higher while Elephant holds on to her belt with his trunk so she won\'t float away.')
def p12_10():
    """Swapped - and Elephant holds her belt."""
    ra = (12, -60)
    rx, ry = _rpaw(300, 352, 1.1, ra)
    et = (86, 52)
    return (_windy('s12p10', mood='golden', sun=(60, 52), rays=True)
            + S.gust(200, 120, s=.8)
            + S.kite(430, 46, s=1.0, rot=20)
            + S.kite_string(rx, ry, 426, 52)
            + S.shadow(300, 350, 32)
            + rabbit(300, 352, s=1.1, expr='excited', look=(.6, -.8), arm2=ra, arm=(-30, -20), extra=BELT)
            + S.shadow(140, 348, 54)
            + elephant(140, 350, s=1.2, expr='happy', look=(.8, .2), trunk=et)
            + S.bubble(["Higher,", "Rabbit!"], 120, 100, tail=(140, 200), color="#4AA8C8"))


@alt('Last of all Nurse Giraffe flies the kite with her long neck stretched up, and the kite soars higher than the clouds while Rabbit and Elephant cheer "Wheee!"')
def p12_11():
    """Higher than the clouds."""
    gx, gy, gs = 380, 350, 1.0
    hx, hy = gx + 16*gs, gy - 250*gs
    return (S.sky('s12p11', 'golden', sun=(60, 52), rays=True,
                  clouds=((300, 90, 50, 16), (334, 80, 30, 14), (440, 110, 40, 14)))
            + S.ground('s12p11', tufts=(40, 300, 460), flowers=((40, 246), (300, 252), (460, 250)))
            + S.kite(390, 34, s=.9, rot=10)
            + S.kite_string(hx + 10, hy + 14, 386, 40, sag=.2)
            + S.shadow(gx, gy, 40)
            + giraffe(gx, gy, s=gs, pose='stretch', expr='happy', look=(0, -.8), cap=False)
            + S.shadow(110, 348, 54)
            + elephant(110, 350, s=1.2, expr='excited', look=(.8, -.8), trunk=(40, -60), arm=(36, -50))
            + S.shadow(240, 350, 30)
            + rabbit(240, 352, s=1.05, expr='excited', look=(.8, -.8), arm=(-28, -44), arm2=(30, -44), extra=BELT)
            + _shout("Wheee!", 190, 110, size=34, rot=-8, color="#C77DFF"))


# ---------------------------------------------------------------- story 13
# One seed, from a paw to a sunflower. The seed is drawn far bigger than life and
# sits in the same patch of garden (x≈250) on every page, so a two-year-old can find
# it each time and watch the patch change: hole, puddle, hole again, shoot, flower.
SEED_X = 250
SQ = "#A2683F"     # Dr. Squirrel's bubbles


def _garden(uid, mood='morning', **kw):
    return S.sky(uid, mood, **kw) + S.ground(uid, tufts=(40, 176, 460), flowers=((40, 246), (450, 252), (150, 236)))


def _marker(x, y):
    """The little stick they push in to mark where the seed went."""
    return (f'<path d="M{x},{y} V{y-34}" stroke="#A87A52" stroke-width="3" stroke-linecap="round"/>'
            f'<rect x="{x-11}" y="{y-54}" width="22" height="24" rx="3" fill="#FFFDF6" stroke="#C8BCA4" stroke-width="1.5"/>'
            + S.seed(x, y - 42, s=.6))


@alt('Rabbit proudly holds up a big stripy seed she has found, next to a freshly dug hole, and Elephant points at the hole with his trunk.')
def p13_1():
    """'Let's plant it!' - dig, plop, pat."""
    ra = (14, -58)
    px, py = _rpaw(170, 352, 1.15, ra)
    return (_garden('s13p1', rays=True, sun=(440, 52))
            + S.hole(SEED_X, 318, rx=24)
            + S.shadow(170, 350, 32)
            + rabbit(170, 352, s=1.15, expr='excited', look=(.5, -.9), arm2=ra, arm=(-28, -6))
            + S.seed(px, py - 12, s=1.7, rot=10)
            + S.shadow(380, 348, 52)
            + elephant(380, 350, s=1.25, expr='happy', look=(-.7, .3), trunk=(-74, 46))
            + _shout("Dig, plop, pat!", 130, 110, size=22, rot=-6, color="#A87A52")
            + S.bubble(["Let's", "plant it!"], 400, 104, tail=(384, 200), color="#4AA8C8"))


@alt('Rabbit lies on her tummy with her ear pressed to the soil, listening for the seed, while Elephant stands with his arms folded, impatiently tapping his foot.')
def p13_2():
    """Five minutes later. Nothing."""
    tap = "".join(f'<path d="M{d}" stroke="#8FA8C0" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
                  for d in ('152,326 q8,-4 14,2', '150,314 q10,-6 18,0'))
    return (_garden('s13p2', 'tender', sun=(440, 52))
            + S.dirt(SEED_X - 46, 330, rx=40, ry=9) + _marker(SEED_X - 70, 332)
            + S.shadow(300, 350, 62)
            + rabbit(SEED_X, 352, s=1.1, pose='lie', expr='calm', look=(-.8, .4))
            + S.shadow(100, 348, 50)
            + elephant(100, 350, s=1.15, expr='cross', look=(.7, .5), trunk=(30, 40), arm=(-10, 6))
            + tap
            + S.bubble(["Is it", "growing yet?"], 330, 196, tail=(270, 290))
            + S.bubble(["Hurry UP,", "seed!"], 110, 98, tail=(104, 210), color="#4AA8C8"))


@alt('Elephant sprays a huge arc of water from his trunk onto the seed patch. SPLOOSH! Rabbit is soaked and dripping, standing in a big muddy puddle.')
def p13_3():
    """'It must be thirsty!' SPLOOSH."""
    et = (40, -60)
    ex, ey = _etip(110, 350, 1.2, et)
    return (_garden('s13p3', 'morning', sun=(440, 52))
            + S.puddle(320, 342, rx=130, ry=16)
            + S.shadow(110, 348, 52)
            + elephant(110, 350, s=1.2, expr='excited', look=(.8, -.2), trunk=et)
            + S.jet(ex, ey - 6, 300, 312, lift=90)
            + S.shadow(370, 350, 30)
            + rabbit(370, 352, s=1.1, expr='surprised', look=(-.6, -.2), ears=(-42, 44), arm=(-30, -30), arm2=(30, -30))
            + S.splash(300, 336, s=1.1)
            + S.drips([(330, 196), (408, 204), (336, 252), (402, 262), (372, 166), (318, 300)], s=1.2)
            + _shout("SPLOOSH!", 300, 96, size=34, rot=-6, color="#3C90AE"))


@alt('Rabbit, splattered with mud, holds up the muddy seed she has dug back out of the hole, and Elephant shouts that it has not done anything.')
def p13_4():
    """Dug up to check. Still just a seed."""
    ra = (30, -30)
    px, py = _rpaw(190, 352, 1.15, ra)
    mud = "".join(S.splat(x, y) for x, y in ((172, 290), (208, 316), (180, 226), (204, 240)))
    return (_garden('s13p4', 'tender', sun=None)
            + S.puddle(250, 344, rx=150, ry=12)
            + S.hole(SEED_X + 30, 330, rx=24)
            + S.shadow(190, 350, 32)
            + rabbit(190, 352, s=1.15, expr='worried', look=(1, .2), arm2=ra, arm=(-26, 10))
            + mud
            + S.seed(px + 4, py - 6, s=1.8, rot=24, muddy=True)
            + S.shadow(400, 348, 50)
            + elephant(400, 350, s=1.2, expr='shout', look=(-.8, .2), trunk=(-50, 30))
            + S.bubble(["It hasn't done", "ANYTHING!"], 380, 104, tail=(394, 206), color="#4AA8C8"))


@alt('Dr. Squirrel arrives on her morning walk and gasps at the muddy mess, while Rabbit holds out the seed and Elephant explains they want it to grow fast.')
def p13_5():
    """Dr. Squirrel - 'what are you doing to that poor seed?'"""
    ra = (34, -24)
    px, py = _rpaw(110, 352, 1.1, ra)
    return (_garden('s13p5', 'morning', sun=(440, 52))
            + S.puddle(240, 344, rx=110, ry=12) + S.hole(SEED_X, 340, rx=20)
            + S.shadow(110, 350, 30)
            + rabbit(110, 352, s=1.1, expr='calm', look=(.8, 0), arm2=ra)
            + S.seed(px + 4, py - 8, s=1.5, rot=20, muddy=True)
            + S.shadow(270, 348, 50)
            + elephant(270, 350, s=1.15, expr='excited', look=(.8, 0), trunk=(40, 20))
            + S.shadow(430, 348, 30)
            + squirrel(430, 348, s=1.1, expr='surprised', look=(-.8, .2), arm=(-26, -40), arm2=(20, 10))
            + S.bubble("Goodness!", 420, 118, tail=(428, 226), color=SQ)
            + S.bubble(["Making", "it grow!"], 100, 104, tail=(108, 200))
            + S.bubble("FAST!", 268, 96, tail=(270, 196), color="#4AA8C8"))


@alt('Dr. Squirrel explains what a seed needs, pointing up at four pictures in a row: soil, water, sun, and a clock for time, while Rabbit and Elephant listen.')
def p13_6():
    """Three things - and one more: time."""
    return (_garden('s13p6', 'morning', sun=None, clouds=((240, 160, 30, 10),))
            + S.badge(66, 62, 'soil', label='Soil') + S.badge(180, 62, 'water', label='Water')
            + S.badge(320, 62, 'sun', label='Sun') + S.badge(434, 62, 'time', label='Time', hot=True)
            + S.shadow(90, 350, 30)
            + rabbit(90, 352, s=1.1, expr='calm', look=(.6, -.3))
            + S.shadow(250, 348, 30)
            + squirrel(250, 348, s=1.2, expr='happy', look=(.5, -.6), arm2=(46, -54), arm=(-24, -10))
            + S.bubble(["And one more:", "TIME."], 250, 164, tail=(250, 226), color=SQ)
            + S.shadow(410, 348, 50)
            + elephant(410, 350, s=1.2, expr='surprised', look=(-.6, -.2), trunk=(-30, 40)))


@alt('Dr. Squirrel holds a giant magnifying glass over the ground, and through it Rabbit and Elephant can see under the soil, where the seed has a root wiggling down and a little shoot reaching up, and a worm.')
def p13_7():
    """Busy underground, where you can't see."""
    lx, ly, r = 280, 236, 66
    return (_garden('s13p7', 'morning', sun=(440, 52))
            + S.dirt(lx, 336, rx=44, ry=9)
            + S.shadow(70, 348, 46)
            + elephant(70, 350, s=1.05, expr='surprised', look=(.9, .1), trunk=(30, 40))
            + S.shadow(170, 350, 28)
            + rabbit(170, 352, s=1.0, expr='excited', look=(.9, .1), arm2=(26, -20))
            + S.magnifier('s13p7', lx, ly, r=r, inside=S.underground(lx, ly - 18, w=2*r, depth=r + 20))
            + S.shadow(410, 348, 30)
            + squirrel(410, 348, s=1.1, expr='happy', look=(-.8, -.2), arm=(-34, 8))
            + S.bubble(["So it IS", "working!"], 150, 96, tail=(166, 200)))


@alt('At sunset Elephant gives the replanted seed one tiny sprinkle of water from the tip of his trunk, while Rabbit kneels by it and whispers goodnight, next to a little sign that says Shh! Growing.')
def p13_8():
    """Planted again - a sprinkle, not a SPLOOSH."""
    et = (-88, 18)
    ex, ey = _etip(390, 350, 1.2, et)
    return (_garden('s13p8', 'sunset', sun=(440, 60), clouds=((300, 50, 40, 14), (332, 42, 24, 12)))
            + S.sign(70, 300, ["Shh! Growing"], w=112, color="#A87A52")
            + S.dirt(SEED_X, 334, rx=40, ry=9)
            + S.shadow(180, 350, 32)
            + rabbit(180, 350, s=1.1, pose='sit', expr='calm', look=(.8, .6), arm2=(34, 10))
            + S.shadow(390, 348, 50)
            + elephant(390, 350, s=1.2, expr='calm', look=(-.8, .6), trunk=et)
            + S.sprinkle(ex, ey)
            + S.bubble(["Goodnight,", "little seed."], 120, 110, tail=(176, 200), size=12))


@alt('One morning Rabbit and Elephant sit by the seed patch, thrilled, as a tiny green shoot with two leaves pokes up out of the soil. LOOK!')
def p13_9():
    """LOOK! A tiny green shoot."""
    sparks = "".join(_pow(x, y, 6) for x, y in ((222, 276), (282, 268), (250, 252)))
    return (_garden('s13p9', 'morning', sun=(440, 52), rays=True)
            + S.dirt(SEED_X, 334, rx=40, ry=9)
            + S.shoot(SEED_X, 332, s=1.7)
            + sparks
            + S.shadow(130, 350, 32)
            + rabbit(130, 350, s=1.15, pose='sit', expr='excited', look=(.9, .5), arm=(-26, -40), arm2=(30, -40))
            + S.shadow(380, 348, 52)
            + elephant(380, 350, s=1.2, pose='sit', expr='excited', look=(-.9, .5), trunk=(-40, 10))
            + _shout("LOOK!", 250, 120, size=40, rot=-6, color="#4A9B4A"))


@alt('The sunflower has grown taller than Rabbit and even taller than Elephant, with its big bud still closed at the top, and Rabbit stretches up on tiptoe beside it while Elephant gazes up in surprise.')
def p13_10():
    """Taller than Rabbit - taller than Elephant."""
    return (_garden('s13p10', 'morning', sun=(440, 52))
            + S.sunflower(SEED_X, 336, h=286, s=1.1, bloom='bud')
            + S.shadow(150, 350, 30)
            + rabbit(150, 344, s=1.1, expr='excited', look=(.6, -.9), arm2=(18, -62), arm=(-24, -10))
            + S.shadow(380, 348, 52)
            + elephant(380, 350, s=1.25, expr='surprised', look=(-.6, -.9), trunk=(-40, 30))
            + S.bubble(["How did it", "get so BIG?"], 400, 84, tail=(384, 186), color="#4AA8C8"))


@alt('A great big sunflower has opened as bright as the sun, dropping new stripy seeds, and Rabbit, Elephant and Dr. Squirrel stand smiling beneath it.')
def p13_11():
    """A great big sunflower, and a pawful of new seeds."""
    falling = "".join(S.seed(x, y, s=.9, rot=r) for x, y, r in ((196, 196, -20), (226, 230, 30), (176, 244, 10)))
    ra = (24, -36)
    px, py = _rpaw(110, 352, 1.1, ra)
    return (_garden('s13p11', 'golden', sun=(446, 46), rays=True, clouds=((70, 60, 40, 15), (100, 52, 24, 12)))
            + S.sunflower(SEED_X, 338, h=244, s=1.6)
            + falling
            + S.shadow(110, 350, 30)
            + rabbit(110, 352, s=1.1, expr='happy', look=(.6, -.6), arm2=ra)
            + S.seed(px, py - 4, s=.9, rot=-10) + S.seed(px + 10, py - 2, s=.9, rot=20)
            + S.shadow(320, 348, 28)
            + squirrel(320, 348, s=1.0, expr='happy', look=(-.4, -.6))
            + S.shadow(424, 348, 50)
            + elephant(424, 350, s=1.2, expr='happy', look=(-.6, -.6), trunk=(-44, 34))
            + S.bubble(["Now we have", "LOTS to plant!"], 400, 116, tail=(420, 200), color="#4AA8C8"))


# ---------------------------------------------------------------- story 14
# Too big for the playground, too small for the apple tree - then exactly the right
# size together. The apple tree stands in the same place (x≈330-380) on every
# orchard page so the picking reads as one continuous afternoon.
BE = "#A87A52"     # Bear's bubbles
TREE14 = 380


def _orchard(uid, mood='morning', **kw):
    return S.sky(uid, mood, **kw) + S.ground(uid, tufts=(40, 176, 300), flowers=((40, 246), (200, 238), (470, 252)))


def _trunk_at(x, y, s, t, u=.5, pose='stand'):
    """A point `u` of the way along Elephant's trunk, and its slope in degrees -
    the same quadratic _limb draws, so a rider sits ON the trunk, not near it."""
    import math
    hy = {'stand': -100, 'sit': -92}[pose]
    x0, y0 = t[0]*.42, 20
    dx, dy = t[0]*.72, t[1]
    mx, my = x0 + dx*.5 - dy*.2, y0 + dy*.5 + dx*.2
    x1, y1 = x0 + dx, y0 + dy
    px = (1-u)**2*x0 + 2*(1-u)*u*mx + u*u*x1
    py = (1-u)**2*y0 + 2*(1-u)*u*my + u*u*y1
    tx = 2*(1-u)*(mx-x0) + 2*u*(x1-mx)
    ty = 2*(1-u)*(my-y0) + 2*u*(y1-my)
    return x + s*px, y + s*(hy + py), math.degrees(math.atan2(ty, tx))


@alt('At the playground Elephant is wedged tight at the top of the slide, sweating, while Rabbit giggles at the bottom.')
def p14_1():
    """Up, up, up - and stuck. 'I'm too BIG!'"""
    sx, sy = S.slide_top(150, 350, h=150)
    return (S.sky('s14p1', 'morning', sun=(440, 52), rays=True) + S.ground('s14p1', tufts=(40, 300, 460), flowers=((40, 246), (300, 252)))
            + S.slide(150, 350, h=150, w=250,
                      rider=elephant(sx, sy + 4, s=1.0, pose='sit', expr='worried', look=(.5, .4), trunk=(30, 20))
                            + S.sweat(sx + 46, sy - 112))
            + S.shadow(440, 350, 30)
            + rabbit(440, 352, s=1.05, expr='happy', look=(-.8, -.6), arm=(-28, -30))
            + S.bubble(["Uh-oh!", "I'm too BIG!"], 330, 90, tail=(216, 110), color="#4AA8C8"))


@alt('Elephant sits on one end of the seesaw, which has thumped down to the ground, and Rabbit is flung up into the air above the other end, squeaking to be let down. BOING!')
def p14_2():
    """BOING! - and Rabbit stays up there."""
    tilt = -18
    lx, ly = S.seesaw_end(250, 350, 320, tilt, -1)
    rx, ry = S.seesaw_end(250, 350, 320, tilt, 1)
    bounce = "".join(f'<path d="M{rx+dx:.0f},{ry-8:.0f} v-20" stroke="#B9C8D0" stroke-width="3" stroke-linecap="round"/>' for dx in (-14, 0, 14))
    return (_orchard('s14p2', 'tender', sun=(60, 52))
            + S.shadow(250, 352, 120, op=.1)
            + S.seesaw(250, 350, 320, tilt)
            + elephant(lx, ly + 4, s=1.1, pose='sit', expr='surprised', look=(.8, -.8), trunk=(40, -20))
            + bounce
            + rabbit(rx + 6, ry - 44, s=.95, pose='sit', expr='worried', look=(-.2, .8), ears=(-30, 30), arm=(-30, -40), arm2=(30, -40))
            + _shout("BOING!", 250, 220, size=30, rot=-10, color="#FF6B6B")
            + S.bubble(["Get me", "DOWN!"], 236, 90, tail=(350, 120)))


@alt('Rabbit waves from the window of a treehouse, but only Elephant\'s trunk fits through the little door, and Elephant looks sad down below.')
def p14_3():
    """Only his trunk fits through the door."""
    tx, ty = S.treehouse_door(350, 350, h=200)
    et = ((tx - 160) / (1.2*1.14), (ty - 350) / 1.2 + 80)
    peek = rabbit(380, 176, s=.6, expr='happy', look=(-.6, .4), arm=(-26, -30))
    return (_orchard('s14p3', 'tender', sun=(60, 52))
            + S.treehouse(350, 350, h=200, peek=peek)
            + S.shadow(160, 348, 52)
            + elephant(160, 350, s=1.2, expr='sad', look=(.6, -.7), trunk=et)
            + S.bubble(["I'm too big for", "EVERYTHING."], 120, 92, tail=(150, 196), color="#4AA8C8"))


APPLES_HIGH = ((330, 150), (360, 112), (410, 140), (444, 112), (392, 88), (346, 78), (300, 122))


@alt('Under his apple tree Bear looks up at the apples with an empty basket, and Rabbit jumps as high as she can with her paw stretched up, but she can\'t reach them.')
def p14_4():
    """'I'm too SMALL!'"""
    ra = (12, -62)
    return (_orchard('s14p4', 'morning', sun=(60, 52))
            + S.apple_tree(TREE14, 350, h=270, apples=APPLES_HIGH)
            + S.basket(452, 350, w=60, full=False)
            + S.shadow(406, 348, 32)
            + bear(406, 348, s=1.1, expr='worried', look=(-.3, -.9), arm=(-20, 20))
            + S.shadow(220, 352, 26, op=.09)
            + rabbit(220, 296, s=1.1, expr='shout', look=(.6, -.9), arm2=ra, arm=(-20, -50))
            + ''.join(f'<path d="M{220+dx},{316} v24" stroke="#B9C8D0" stroke-width="3" stroke-linecap="round"/>' for dx in (-14, 0, 14))
            + S.bubble(["I'm too", "SMALL!"], 100, 104, tail=(188, 150)))


@alt('Rabbit\'s wobbly pile of a bucket, a box and a flowerpot has crashed down; she sits dazed on the grass with the flowerpot upside down on her head while Bear gasps.')
def p14_5():
    """Wibble, wobble, CRASH!"""
    dizzy = "".join(_pow(x, y, 7) for x, y in ((176, 180), (264, 172), (220, 156)))
    return (_orchard('s14p5', 'tender', sun=(60, 52))
            + S.apple_tree(TREE14, 350, h=270, apples=APPLES_HIGH)
            + S.shadow(406, 348, 32)
            + bear(406, 348, s=1.1, expr='surprised', look=(-.8, .2), arm=(-26, -40), arm2=(26, -40))
            + S.spin(-24, 110, 348, S.parcel(110, 348, s=1.2))
            + S.bucket(300, 340, s=1.0, rot=96)
            + S.shadow(220, 350, 34)
            + rabbit(220, 350, s=1.1, pose='sit', expr='surprised', look=(0, -.3), ears=(-74, 74), arm=(-30, 10), arm2=(30, 10))
            + S.pot(220, 194, s=1.15, rot=180)
            + dizzy
            + _shout("CRASH!", 250, 100, size=36, rot=-8, color="#E8892E"))


@alt('Rabbit and Elephant sit glumly side by side under the apple tree, one too big and one too small, while Bear scratches his head and thinks.')
def p14_6():
    """'Too big.' 'Too small.' 'Hmm.'"""
    return (_orchard('s14p6', 'tender', sun=None)
            + S.apple_tree(TREE14, 350, h=270, apples=APPLES_HIGH)
            + S.shadow(120, 350, 52)
            + elephant(120, 350, s=1.15, pose='sit', expr='sad', look=(.4, .5), trunk=(10, 30))
            + S.shadow(250, 350, 30)
            + rabbit(250, 350, s=1.0, pose='sit', expr='sad', look=(-.4, .5))
            + S.pot(296, 348, s=.8)
            + S.shadow(410, 348, 32)
            + bear(410, 348, s=1.1, expr='calm', look=(.2, -.8), arm2=(-4, -62))
            + S.bubble(["I'm too", "big."], 100, 114, tail=(116, 214), color="#4AA8C8")
            + S.bubble(["I'm too", "small."], 262, 136, tail=(254, 226))
            + S.thought("Hmm…", 420, 140, (410, 204), size=14))


APPLES_UP = ((266, 80), (308, 94), (356, 70), (394, 112), (338, 140), (420, 70))


@alt('Elephant lifts Rabbit high into the branches on the tip of his trunk, and she stretches up and touches an apple, while Bear cheers below.')
def p14_7():
    """'Hop on!' - up, up, up. 'I can reach!'"""
    et = (40, -70)
    ex, ey = _etip(170, 350, 1.2, et)
    return (_orchard('s14p7', 'golden', sun=(60, 52), rays=True)
            + S.apple_tree(340, 350, h=320, apples=APPLES_UP)
            + S.shadow(170, 348, 52)
            + elephant(170, 350, s=1.2, expr='happy', look=(.6, -.9), trunk=et)
            + rabbit(ex + 2, ey + 2, s=.8, expr='excited', look=(.7, -.8), arm2=(20, -50), arm=(-26, -24))
            + S.shadow(430, 348, 32)
            + bear(430, 348, s=1.05, expr='excited', look=(-.6, -.8), arm=(-24, -46), arm2=(24, -46))
            + S.bubble(["I can", "reach!"], 92, 80, tail=(200, 90)))


@alt('Rabbit sits on Elephant\'s head picking apples and dropping them down, and Elephant catches them in Bear\'s basket while they count: seven, eight, nine!')
def p14_8():
    """Counting apples into the basket."""
    ra = (34, -48)
    px, py = _rpaw(190, 186, .85, ra)
    inbasket = "".join(S.apple(x, y, r=9, color=c) for x, y, c in
                       ((268, 280, "#FF6B6B"), (288, 276, "#FF6B6B"), (308, 280, "#FF6B6B"), (278, 268, "#FF9BAE"), (298, 268, "#FF6B6B")))
    return (_orchard('s14p8', 'golden', sun=(60, 52))
            + S.apple_tree(340, 350, h=320, apples=((308, 94), (356, 70), (394, 112), (420, 70)))
            + S.shadow(190, 348, 52)
            + elephant(190, 350, s=1.2, expr='happy', look=(.8, .4), trunk=(-30, 40), arm=(36, 8))
            + inbasket
            + S.basket(290, 334, w=84, full=False)
            + rabbit(190, 186, s=.85, pose='sit', expr='happy', look=(.8, -.6), arm2=ra, arm=(-30, -10))
            + S.apple(px + 4, py - 4, r=9)
            + S.flight([(px + 10, py + 14), (270, 160), (284, 220), (288, 252)], color="#C8A030")
            + S.apple(282, 200, r=9)
            + S.shadow(436, 348, 32)
            + bear(436, 348, s=1.05, expr='excited', look=(-.6, -.4), arm=(-24, -46))
            + _shout("…7, 8, 9!", 96, 110, size=28, rot=-6, color="#C77DFF"))


@alt('Rabbit pokes her head out of a little hole in a hollow log, holding up the tenth apple, while Elephant, whose trunk was too big to fit, and Bear cheer.')
def p14_9():
    """Apple number ten - and only Rabbit fits."""
    lx, ly, r = 290, 350, 60
    cy = ly - r
    inside = (f'<defs><clipPath id="s14p9-hole"><ellipse cx="{lx}" cy="{cy}" rx="{r*.34:.0f}" ry="{r*.78:.0f}"/></clipPath></defs>'
              f'<g clip-path="url(#s14p9-hole)">'
              + rabbit(lx, cy + 50, s=.75, pose='seated', expr='happy', look=(-.6, 0))
              + S.apple(lx, cy + 26, r=11) + '</g>')
    return (_orchard('s14p9', 'golden', sun=(60, 52))
            + S.shadow(430, 348, 30)
            + bear(430, 348, s=1.05, expr='excited', look=(-.8, .2), arm=(-24, -46), arm2=(24, -46))
            + S.log(lx, ly, w=180, r=r, inside=inside)
            + S.shadow(120, 348, 52)
            + elephant(120, 350, s=1.2, expr='happy', look=(.9, .3), trunk=(92, 32))
            + S.bubble("Got it!", 290, 170, tail=(290, 236)))


@alt('Bear, Rabbit and Elephant sit round a table sharing a steaming dish of apple crumble, and Bear thanks them both.')
def p14_10():
    """The most delicious apple crumble ever."""
    return (_orchard('s14p10', 'golden', sun=(440, 52), rays=True)
            + elephant(110, 296, s=1.15, pose='seated', expr='happy', look=(.6, .3), trunk=(20, 20))
            + bear(250, 272, s=1.1, pose='seated', expr='happy', look=(0, .3))
            + rabbit(390, 296, s=1.1, pose='seated', expr='happy', look=(-.6, .3))
            + S.table(250, 280, w=330)
            + S.crumble(250, 280, s=1.1)
            + S.bowl(120, 280, 'halwa', s=.9) + S.bowl(380, 280, 'halwa', s=.9)
            + S.bubble(["I couldn't have done", "it without you!"], 250, 80, tail=(250, 160), color=BE))


@alt('Back at the playground, Elephant sits with his long trunk stretched down to the grass, and Rabbit whizzes down it like a slide, shouting that he is the best slide ever.')
def p14_11():
    """The best slide ever."""
    # the trunk is drawn here as one long ramp rather than through elephant(trunk=),
    # whose trunk root sits too far out on the cheek once it reaches this far
    sx, sy, cx, cy, ex, ey = 120, 278, 210, 258, 350, 346
    d = f'M{sx},{sy} Q{cx},{cy} {ex},{ey}'
    ramp = (f'<path d="{d}" stroke="{E_LINE}" stroke-width="21" fill="none" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="{E_BODY}" stroke-width="18" fill="none" stroke-linecap="round"/>')
    t = .42
    rx = (1-t)**2*sx + 2*(1-t)*t*cx + t*t*ex
    ry = (1-t)**2*sy + 2*(1-t)*t*cy + t*t*ey
    import math
    ang = math.degrees(math.atan2((1-t)*(cy-sy) + t*(ey-cy), (1-t)*(cx-sx) + t*(ex-cx)))
    return (S.sky('s14p11', 'golden', sun=(440, 52), rays=True) + S.ground('s14p11', tufts=(40, 300, 460), flowers=((40, 246), (300, 252)))
            + S.shadow(120, 350, 56)
            + elephant(120, 350, s=1.2, pose='sit', expr='happy', look=(.8, .4), trunk=(2, 6))
            + ramp
            + S.speedlines(rx - 34, ry - 30, n=3, length=24)
            + S.spin(ang, rx, ry - 6, rabbit(rx, ry - 6, s=.75, pose='sit', expr='excited', look=(.6, .2),
                                           arm=(-24, -40), arm2=(24, -40)))
            + _shout("Wheee!", 390, 230, size=36, rot=-8, color="#C77DFF")
            + S.bubble(["You're the best", "slide EVER!"], 260, 92, tail=(rx, ry - 80)))


PAGES = {
    '02-ouch-the-big-thorn': [p02_1, p02_2, p02_3, p02_4, p02_5,
                              p02_6, p02_7, p02_8, p02_9, p02_10],
    '05-splash-the-pool-party': [p05_1, p05_2, p05_3, p05_4, p05_5, p05_6, p05_7, p05_8, p05_9],
    '01-the-hungry-friends': [p01_1, p01_2, p01_3, p01_4, p01_5, p01_6,
                              p01_7, p01_8, p01_9, p01_10, p01_11, p01_12],
    '03-snow-much-help': [p03_1, p03_2, p03_3, p03_4, p03_5, p03_6, p03_7,
                          p03_8, p03_9, p03_10, p03_11, p03_12, p03_13],
    '04-watch-your-step': [p04_1, p04_2, p04_3, p04_4, p04_5, p04_6,
                           p04_7, p04_8, p04_9, p04_10, p04_11, p04_12],
    '06-bonk-the-bumpy-ride-home': [p06_1, p06_2, p06_3, p06_4, p06_5,
                                    p06_6, p06_7, p06_8, p06_9, p06_10],
    '07-shh-the-noisy-night': [p07_1, p07_2, p07_3, p07_4, p07_5, p07_6,
                               p07_7, p07_8, p07_9, p07_10, p07_11],
    '08-hide-and-squeak': [p08_1, p08_2, p08_3, p08_4, p08_5, p08_6,
                           p08_7, p08_8, p08_9, p08_10, p08_11],
    '09-wobble-the-big-bike-day': [p09_1, p09_2, p09_3, p09_4, p09_5, p09_6,
                                   p09_7, p09_8, p09_9, p09_10, p09_11],
    '10-achoo-the-sneezy-day': [p10_1, p10_2, p10_3, p10_4, p10_5, p10_6,
                                p10_7, p10_8, p10_9, p10_10, p10_11],
    '11-the-great-big-cake': [p11_1, p11_2, p11_3, p11_4, p11_5, p11_6,
                              p11_7, p11_8, p11_9, p11_10, p11_11],
    '12-whoosh-the-kite-day': [p12_1, p12_2, p12_3, p12_4, p12_5, p12_6,
                               p12_7, p12_8, p12_9, p12_10, p12_11],
    '13-grow-seed-grow': [p13_1, p13_2, p13_3, p13_4, p13_5, p13_6,
                          p13_7, p13_8, p13_9, p13_10, p13_11],
    '14-too-big-too-small': [p14_1, p14_2, p14_3, p14_4, p14_5, p14_6,
                             p14_7, p14_8, p14_9, p14_10, p14_11],
}
