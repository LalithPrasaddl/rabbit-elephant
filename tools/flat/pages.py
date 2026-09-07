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


PAGES = {
    '06-bonk-the-bumpy-ride-home': [p06_1, p06_2, p06_3, p06_4, p06_5,
                                    p06_6, p06_7, p06_8, p06_9, p06_10],
}
