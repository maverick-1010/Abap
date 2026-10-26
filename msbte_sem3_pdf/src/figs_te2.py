"""Thermal Engineering figures, part 2: equipment sketches."""
import math
from draw import *
from figreg import fig


def pipe_h(f, x1, x2, y, w=2.4):
    f.rect(x1, y - w / 2, x2 - x1, w, fill=LIGHT, lw=0.5)


@fig("te_surface_condenser")
def te_surface_condenser():
    f = Fig(165, 84, 1.0)
    # shell, water boxes
    f.rect(36, 22, 92, 36, lw=1.2)
    f.rect(22, 22, 14, 36, lw=1.2, fill=LIGHT)
    f.rect(128, 22, 14, 36, lw=1.2, fill=LIGHT)
    f.line(22, 40, 36, 40, w=1.2)
    for i in range(6):
        f.line(36, 24.5 + i * 2.6, 128, 24.5 + i * 2.6, w=0.5)
        f.line(36, 42.5 + i * 2.6, 128, 42.5 + i * 2.6, w=0.5)
    for x in (66, 98):
        f.line(x, 58, x, 51, w=0.9); f.line(x, 22, x, 29, w=0.9)
    f.tbox(82, 33, "Tube bundle (cooling water flows inside the tubes)", size=6.6)
    f.tbox(82, 52.5, "Steam condenses on the outside of the tubes", size=6.6)
    # steam inlet
    f.rect(76, 58, 20, 7, lw=1.2)
    f.arrow(86, 80, 86, 61, w=1.3, size=5)
    f.text(86, 81.5, "Exhaust steam from turbine", size=7.2)
    # hot well
    f.pline([(64, 22), (72, 8), (100, 8), (108, 22)], w=1.2)
    f.text(86, 13.5, "Hot well", size=7)
    f.arrow(86, 8, 86, 1, w=1.3, size=5)
    f.text(90, 2, "Condensate to extraction pump", size=7, anchor="start")
    # air extraction
    f.rect(114, 16, 6, 6, lw=0.9)
    f.arrow(117, 16, 117, 9, w=1.0, size=4)
    f.text(121, 10, "Air extraction", size=6.6, anchor="start")
    # cooling water
    f.arrow(4, 30, 22, 30, w=1.4, size=5)
    f.text(2, 33.5, "Water IN", size=7, anchor="start")
    f.arrow(22, 50, 4, 50, w=1.4, size=5)
    f.text(2, 53.5, "Water OUT", size=7, anchor="start")
    f.text(29, 61, "Water box", size=6.6)
    f.text(135, 61, "Return water box", size=6.6)
    f.text(135, 40, "Water", size=6.4); f.text(135, 36.5, "turns", size=6.4)
    f.text(150, 40, "", size=6)
    f.text(82, 62.2, "", size=6)
    f.text(130, 71, "Shell", size=8, bold=True, anchor="start")
    f.leader(124, 58, 131, 70, "")
    return f.d


@fig("te_cooling_tower_forced")
def te_cooling_tower_forced():
    f = Fig(165, 88, 1.0)
    f.rect(50, 14, 76, 56, lw=1.2)
    f.line(50, 32, 50, 14, w=0)                                      # keep structure simple
    # fill / packing
    f.rect(52, 34, 72, 18, lw=0.5, fill=None)
    for i in range(0, 72, 4):
        f.line(52 + i, 34, 52 + i, 52, w=0.4)
    for j in range(0, 18, 3):
        f.line(52, 34 + j, 124, 34 + j, w=0.3)
    f.tbox(88, 42, "FILL / PACKING", size=7, bold=True)
    # spray pipes
    f.line(52, 58, 124, 58, w=1.6)
    for x in range(58, 124, 10):
        f.line(x, 58, x, 55, w=0.6)
        for dx in (-2, 0, 2):
            f.arrow(x, 55, x + dx, 52.5, w=0.4, size=2)
    f.text(88, 60.5, "Spray header with nozzles", size=6.8)
    # drift eliminators
    for x in range(54, 124, 6):
        f.line(x, 64, x + 3, 69, w=0.7); f.line(x + 3, 69, x + 6, 64, w=0.7)
    f.text(88, 71.5, "Drift eliminators", size=6.8)
    f.arrow(88, 73.5, 88, 83, w=1.2, size=5)
    f.text(88, 84.5, "Warm moist air out", size=7)
    # hot water inlet
    f.arrow(5, 58, 50, 58, w=1.4, size=5)
    f.text(5, 61.5, "Hot water from condenser", size=7, anchor="start")
    # louvres + fan
    for y in range(17, 33, 3):
        f.line(50, y, 56, y + 2, w=0.8)
    f.text(63, 25, "Louvres", size=6.5, anchor="start")
    f.circle(32, 25, 8, lw=1.0) if False else f.circle(32, 25, 8, w=1.0)
    f.line(32, 17, 32, 33, w=1.0); f.line(24, 25, 40, 25, w=1.0)
    f.text(32, 12, "Fan (forced draught)", size=6.8)
    f.arrow(12, 25, 22, 25, w=1.3, size=5)
    f.text(2, 28.5, "Atmospheric air in", size=6.8, anchor="start")
    f.arrow(41, 25, 56, 25, w=1.3, size=5)
    # basin
    f.rect(46, 4, 84, 10, lw=1.1, fill=LIGHT)
    f.text(88, 7.5, "Cold water basin", size=7)
    f.arrow(130, 8, 150, 8, w=1.4, size=5)
    f.text(135, 11.5, "Cold water to condenser", size=6.8, anchor="start")
    f.arrow(148, -1, 148, 8, w=0.9, size=4) if False else None
    f.arrow(100, -1, 100, 4, w=1.0, size=4) if False else None
    for x in (70, 90, 110):
        f.arrow(x, 52, x, 40, w=0.5, size=3, col=BLUE)
    return f.d


@fig("te_cooling_tower_natural")
def te_cooling_tower_natural(title="Natural draught (hyperbolic) cooling tower"):
    f = Fig(165, 101, 1.0)
    cx = 82
    r = lambda y: 15 + 0.0125 * (y - 62) ** 2
    ys = [10 + i * (80 - 10) / 50 for i in range(51)]
    f.pline([(cx - r(y), y) for y in ys], w=1.4)
    f.pline([(cx + r(y), y) for y in ys], w=1.4)
    f.line(cx - r(80), 80, cx + r(80), 80, w=0.6, dash=HIDDEN)
    # base columns
    for dx in (-0.9, -0.55, -0.2, 0.2, 0.55, 0.9):
        f.line(cx + dx * r(10), 4, cx + dx * r(10), 10, w=0.8)
    f.line(cx - r(10), 10, cx + r(10), 10, w=0.8)
    # fill
    xl, xr = cx - r(22) + 3, cx + r(22) - 3
    f.rect(xl, 14, xr - xl, 9, lw=0.5)
    for x in range(int(xl), int(xr), 4):
        f.line(x, 14, x, 23, w=0.35)
    f.text(cx, 17.2, "FILL", size=6.5, bold=True)
    # distribution
    f.line(xl, 30, xr, 30, w=1.6)
    for x in range(int(xl) + 4, int(xr), 8):
        f.arrow(x, 30, x, 24.5, w=0.4, size=2.5)
    f.line(cx, 4, cx, 30, w=2.2, col=RED) if False else None
    f.text(cx, 32.5, "Water distribution", size=6.8)
    # hot water pipe
    f.arrow(4, 4.2, cx - 2, 4.2, w=1.4, size=5) if False else None
    f.line(8, 28, cx, 28, w=1.2)
    f.line(cx, 28, cx, 30, w=1.2)
    f.arrow(2, 28, 12, 28, w=1.4, size=5)
    f.text(2, 31.5, "Hot water in", size=7, anchor="start")
    # air arrows
    for x, d in ((cx - r(10) - 8, 1), (cx + r(10) + 8, -1)):
        f.arrow(x, 8, x + 12 * d, 13, w=1.0, size=4.5)
    f.text(cx - r(10) - 22, 4, "Cold air in", size=6.8, anchor="start")
    f.text(cx + r(10) + 22, 4, "Cold air in", size=6.8, anchor="end")
    for x in (cx - 8, cx, cx + 8):
        f.arrow(x, 36, x, 82, w=0.8, size=4, col=BLUE)
    f.arrow(cx, 82, cx, 92, w=1.4, size=5)
    f.text(cx, 94, "Warm moist air (plume)", size=7)
    # basin
    f.rect(cx - r(10) - 4, 0, 2 * r(10) + 8, 4, lw=1.0, fill=LIGHT)
    f.text(cx, -3.5, "Cold water basin (to condenser)", size=6.8)
    f.text(cx - r(62) - 26, 62, "Hyperbolic shell", size=7, anchor="end")
    f.text(cx + r(62) + 4, 62, "(concrete)", size=6.5, anchor="start")
    f.text(cx, 49, "Natural draught:", size=6.6)
    f.text(cx, 45.5, "density difference", size=6.6)
    f.text(cx, 42, "makes the air rise", size=6.6)
    return f.d


@fig("te_benson")
def te_benson():
    f = Fig(165, 84, 1.0)
    f.rect(20, 16, 118, 52, lw=1.2)
    f.text(79, 70.5, "FURNACE", size=7.5, bold=True)
    f.circle(9, 42, 5.5, w=1.1); f.text(9, 40.8, "P", size=7.5, bold=True)
    f.text(9, 32, "Feed pump", size=6.5)
    f.arrow(0, 42, 3.5, 42, w=1.2, size=3) if False else None
    f.line(14.5, 42, 20, 42, w=1.5)
    serp(f, 20, 50, 42, 11, 3, w=1.5)
    serp(f, 50, 100, 42, 17, 5, w=1.5)
    serp(f, 100, 138, 42, 11, 3, w=1.5)
    f.line(138, 42, 150, 42, w=1.5)
    f.arrow(146, 42, 162, 42, w=1.6, size=5)
    f.text(35, 60, "Economiser", size=7, bold=True)
    f.text(75, 63, "Radiant evaporator", size=7, bold=True)
    f.text(119, 60, "Superheater", size=7, bold=True)
    f.text(35, 24, "feed water heated", size=6.4)
    f.text(75, 20, "water changes into steam", size=6.4)
    f.text(119, 24, "steam superheated", size=6.4)
    f.text(152, 46, "Steam to", size=7); f.text(152, 38, "turbine", size=7)
    f.text(82, 9, "One continuous tube, no steam drum.", size=6.8)
    f.text(82, 3, "Feed water enters at about 220 bar (above the critical pressure) and leaves as superheated steam.", size=6.4)
    return f.d


@fig("te_lamont")
def te_lamont():
    f = Fig(165, 100, 1.0)
    f.rect(44, 78, 66, 14, lw=1.3, fill=LIGHT)
    f.text(77, 83, "STEAM DRUM", size=7.5, bold=True)
    f.rect(36, 24, 86, 50, lw=1.2)
    f.text(79, 66.5, "FURNACE", size=7.5, bold=True)
    for i in range(8):
        x = 54 + i * 7
        f.line(x, 34, x, 78, w=1.1)
    f.line(50, 34, 109, 34, w=2.2)
    f.tbox(82, 28, "Distribution header", size=6.6)
    f.tbox(82, 54, "Evaporator tubes", size=7)
    # downcomer, pump and return to header
    f.line(48, 78, 48, 12, w=1.5)
    f.line(48, 12, 59, 12, w=1.5)
    f.circle(63, 12, 4.2, w=1.1); f.text(63, 10.8, "P", size=7, bold=True)
    f.line(67.2, 12, 79, 12, w=1.5)
    f.line(79, 12, 79, 34, w=1.5)
    f.arrowhead(79, 34, math.pi / 2, 4)
    f.arrowhead(48, 40, -math.pi / 2, 4)
    f.text(63, 5, "Circulating pump", size=6.6)
    f.text(46, 46, "Down-", size=6.4, anchor="end"); f.text(46, 42.5, "comer", size=6.4, anchor="end")
    # economiser + feed
    f.arrow(1, 56, 8, 56, w=1.4, size=4.5)
    f.text(1, 63, "Feed water in", size=6.8, anchor="start")
    serp(f, 8, 32, 56, 8, 2, w=1.3)
    f.text(20, 44, "Economiser", size=6.8)
    f.line(32, 56, 36, 56, w=1.3)
    f.line(36, 56, 40, 56, w=1.3); f.line(40, 56, 40, 85, w=1.3); f.line(40, 85, 44, 85, w=1.3)
    # superheater and steam outlet
    f.line(110, 85, 124, 85, w=1.4)
    serp(f, 124, 152, 85, 7, 3, w=1.4)
    f.text(138, 96, "Superheater", size=6.8)
    f.arrow(150, 85, 163, 85, w=1.5, size=5)
    f.text(150, 74, "Steam to", size=6.8, anchor="start"); f.text(150, 70, "turbine", size=6.8, anchor="start")
    f.text(82, 99, "", size=6)
    f.text(112, 14, "Pump forces water through the", size=6.4, anchor="start")
    f.text(112, 10, "evaporator tubes (forced circulation)", size=6.4, anchor="start")
    return f.d


@fig("te_four_stroke_ci")
def te_four_stroke_ci():
    f = Fig(165, 108, 1.0)
    cx = 70
    # cylinder block and liner
    f.rect(cx - 17, 36, 34, 48, lw=1.3)
    f.rect(cx - 22, 36, 5, 48, lw=1.0, fill=LIGHT); f.rect(cx + 17, 36, 5, 48, lw=1.0, fill=LIGHT)   # water jackets
    f.rect(cx - 22, 84, 44, 14, lw=1.3)                                                                  # head
    # valves
    for xv, nm in ((cx - 10, "Inlet valve"), (cx + 10, "Exhaust valve")):
        f.line(xv, 84, xv, 102, w=1.1)
        f.line(xv - 3.5, 84, xv + 3.5, 84, w=1.6)
        f.line(xv - 2, 102, xv + 2, 102, w=1.4)
    f.line(cx, 84, cx, 94, w=1.3)
    f.rect(cx - 2, 94, 4, 8, lw=0.9)
    # ports
    f.line(cx - 10, 92, cx - 28, 92, w=1.0); f.line(cx - 10, 96, cx - 28, 96, w=1.0)
    f.line(cx + 10, 92, cx + 28, 92, w=1.0); f.line(cx + 10, 96, cx + 28, 96, w=1.0)
    # piston
    f.rect(cx - 16, 52, 32, 17, lw=1.2, fill=LIGHT)
    for y in (65, 62, 59):
        f.line(cx - 16, y, cx + 16, y, w=0.8)
    f.circle(cx, 55, 1.6, w=0.8)
    # connecting rod and crank
    f.line(cx - 1.5, 55, cx - 4, 20, w=1.4); f.line(cx + 1.5, 55, cx + 4, 20, w=1.4)
    f.circle(cx, 14, 9, w=1.2)
    f.circle(cx, 14, 2.2, w=1.0, fill=BLACK)
    f.circle(cx + 2.3, 22, 3.6, w=1.0)
    f.rect(cx - 24, 0, 48, 36, lw=0.8, dash=HIDDEN)
    # flywheel
    f.circle(cx + 40, 14, 12, w=1.0)
    f.line(cx + 9, 14, cx + 28, 14, w=2.0)
    # labels with leaders
    L = lambda x, y, tx, ty, s, a="start": f.leader(x, y, tx, ty, s, size=6.8, anchor=a)
    L(cx - 22, 92, 6, 100, "Cylinder head")
    L(cx - 10, 99, 6, 106, "Inlet valve")
    L(cx + 10, 99, 100, 106, "Exhaust valve")
    L(cx, 99, 66, 108.5, "Fuel injector", "middle") if False else L(cx, 100, 74, 108, "Fuel injector")
    L(cx - 19, 70, 6, 76, "Water jacket")
    L(cx - 17, 50, 6, 46, "Cylinder liner")
    L(cx + 16, 62, 100, 70, "Piston rings")
    L(cx + 12, 58, 100, 56, "Piston")
    L(cx, 55, 100, 46, "Gudgeon pin")
    L(cx + 3, 36, 100, 36, "Connecting rod")
    L(cx + 2, 23, 104, 26, "Crank pin")
    L(cx - 8, 14, 6, 10, "Crank shaft")
    L(cx + 40, 18, 112, 34, "Flywheel") if False else L(cx + 48, 20, 120, 30, "Flywheel")
    L(cx - 24, 6, 6, 2, "Crank case")
    f.text(150, 94, "Air →", size=6.6, anchor="end") if False else None
    return f.d


@fig("te_steam_plant")
def te_steam_plant():
    f = Fig(165, 118, 1.0)
    # coal circuit
    f.rect(2, 62, 20, 10, lw=1.0, fill=LIGHT); f.text(12, 65.5, "Coal store", size=6.2)
    f.arrow(22, 67, 34, 57, w=1.1, size=4)
    f.text(12, 76, "COAL CIRCUIT", size=6.6, bold=True)
    f.text(12, 56, "(coal → crusher →", size=5.8); f.text(12, 52.5, "conveyor → furnace)", size=5.8)
    # boiler + superheater + economiser
    f.rect(34, 40, 44, 34, lw=1.3)
    f.text(56, 64, "BOILER", size=8, bold=True); f.text(56, 57, "(furnace + drum)", size=6.4)
    f.rect(42, 74, 28, 5, lw=0.9, fill=LIGHT); f.text(56, 81, "Superheater", size=6.4)
    f.arrow(56, 40, 56, 31, w=1.0, size=4); f.text(56, 27.5, "Ash to ash pit", size=6.2)
    # chimney
    f.rect(86, 40, 7, 50, lw=1.2, fill=LIGHT); f.text(89.5, 93, "Chimney", size=6.8)
    f.arrow(78, 46, 86, 46, w=1.1, size=3.5); f.text(82, 41.5, "Flue gas", size=5.6)
    # steam line to turbine
    f.line(56, 79, 56, 104, w=1.5); f.line(56, 104, 108, 104, w=1.5)
    f.line(108, 104, 108, 92, w=1.5); f.arrowhead(108, 92, -math.pi / 2, 4.5)
    f.text(82, 106, "Steam", size=6.6)
    # turbine and generator
    f.pline([(100, 70), (100, 88), (128, 96), (128, 62)], closed=True, w=1.3, fill=LIGHT)
    f.text(114, 79, "TURBINE", size=7.2, bold=True)
    f.line(128, 79, 138, 79, w=1.8)
    f.circle(147, 79, 8.5, w=1.2); f.text(147, 77.5, "G", size=9, bold=True)
    f.text(147, 66, "Generator", size=6.6)
    # condenser
    f.rect(98, 30, 32, 18, lw=1.3); f.text(114, 37, "CONDENSER", size=6.8, bold=True)
    f.arrow(114, 62, 114, 48, w=1.5, size=4.5); f.text(116, 54.5, "Exhaust steam", size=6.2, anchor="start")
    # cooling tower on the right
    cxt = 150
    r = lambda y: 5.5 + 0.0065 * (y - 28) ** 2
    ys = [10 + i * 0.6 for i in range(0, 56)]
    f.pline([(cxt - r(y), y) for y in ys], w=1.3)
    f.pline([(cxt + r(y), y) for y in ys], w=1.3)
    f.line(cxt - r(10), 10, cxt + r(10), 10, w=1.3)
    f.text(cxt, 46, "Cooling", size=6.4); f.text(cxt, 42.5, "tower", size=6.4)
    f.arrow(130, 41, 142, 41, w=1.2, size=3.8); f.text(136, 44, "hot water", size=5.6)
    f.line(144, 14, 122, 14, w=1.2); f.arrowhead(130, 14, math.pi, 3.8)
    f.line(122, 14, 122, 30, w=1.2); f.arrowhead(122, 30, math.pi / 2, 3.8)
    f.text(133, 16.5, "cold water", size=5.6)
    # condensate and feed pump
    f.line(104, 30, 104, 14, w=1.5); f.line(104, 14, 76, 14, w=1.5); f.arrowhead(76, 14, math.pi, 4.2)
    f.circle(70, 14, 5, w=1.2); f.text(70, 12.6, "P", size=7, bold=True); f.text(70, 5, "Feed pump", size=6.6)
    f.text(90, 16.8, "Condensate", size=6.2)
    f.line(65, 14, 40, 14, w=1.5); f.line(40, 14, 40, 40, w=1.5); f.arrowhead(40, 40, math.pi / 2, 4.2)
    f.text(37, 22, "Feed water", size=6.2, anchor="end")
    return f.d


@fig("te_velocity_compounding")
def te_velocity_compounding():
    f = Fig(165, 118, 1.0)
    # casing and nozzle
    f.rect(6, 78, 153, 34, lw=1.0, dash=HIDDEN)
    f.pline([(8, 90), (30, 92.5), (30, 100), (8, 104)], closed=True, w=1.3, fill=LIGHT)
    f.text(19, 107, "Nozzle", size=7, bold=True)
    f.arrow(0, 97, 8, 97, w=1.4, size=4.5)
    f.text(3, 101, "Steam in", size=6, anchor="start")
    f.arrow(30, 96, 40, 96, w=1.4, size=4.5)
    f.line(6, 82, 159, 82, w=0.5, dash=CHAIN)
    f.text(158, 79.5, "rotor shaft", size=5.8, anchor="end")

    def row(xc, curved_right, label, sub):
        for i in range(6):
            y = 85 + i * 4.6
            pts = f.arc_pts(xc + (4 if curved_right else -4), y + 2.5, 4.2, 235 if curved_right else -55, 305 if curved_right else 55, 14)
            f.pline(pts, w=1.3)
        f.text(xc, 118.5 - 3, label, size=6.8, bold=True)
        f.text(xc, 73.8, sub, size=6)

    row(50, True, "1st row moving blades", "(MB 1)")
    row(88, False, "Fixed (guide) blades", "(FB)")
    row(126, True, "2nd row moving blades", "(MB 2)")
    f.arrow(58, 96, 80, 96, w=0.9, size=3.5)
    f.arrow(96, 96, 118, 96, w=0.9, size=3.5)
    f.arrow(134, 96, 150, 96, w=1.0, size=3.8)
    f.text(150, 99.5, "exhaust", size=6, anchor="end")
    # pressure graph
    axes(f, 8, 38, 150, 26, "", "")
    f.text(8, 66.5, "Pressure", size=7, anchor="start", bold=True)
    f.pline([(8, 60), (28, 60), (42, 42), (150, 42)], w=1.5)
    f.text(94, 46, "pressure stays constant over blades (all the drop is in the nozzle)", size=6.2)
    # velocity graph
    axes(f, 8, 2, 150, 28, "", "")
    f.text(8, 31.5, "Absolute velocity of steam", size=7, anchor="start", bold=True)
    f.pline([(8, 6), (28, 6), (42, 27), (66, 17), (74, 17), (82, 16), (100, 11), (112, 11), (120, 12), (144, 7)], w=1.5)
    f.text(42, 28.5, "C₁ (highest)", size=6.2, anchor="middle")
    f.text(70, 20, "falls in MB 1", size=6.2)
    f.text(106, 14.5, "falls in MB 2", size=6.2) if False else f.text(106, 15, "falls in MB 2", size=6.2)
    f.text(136, 11, "small exit", size=6.2); f.text(136, 8, "velocity", size=6.2)
    for x in (30, 66, 104, 142):
        f.line(x, 2, x, 64, w=0.3, dash=HIDDEN)
    return f.d


@fig("te_sfee")
def te_sfee(kind="general"):
    f = Fig(165, 62, 1.0)
    f.rect(50, 10, 66, 42, lw=1.3)
    f.text(83, 46, "Control volume", size=7.5, bold=True)
    f.text(83, 30, {"general": "Device", "boiler": "BOILER", "turbine": "TURBINE"}[kind], size=9, bold=True)
    f.arrow(14, 30, 50, 30, w=1.5, size=5)
    f.arrow(116, 30, 152, 30, w=1.5, size=5)
    f.text(4, 36, "Inlet 1", size=7, anchor="start", bold=True)
    f.text(4, 22, "h₁, C₁, Z₁", size=7, anchor="start")
    f.text(124, 36, "Outlet 2", size=7, anchor="start", bold=True)
    f.text(124, 22, "h₂, C₂, Z₂", size=7, anchor="start")
    if kind in ("general", "boiler"):
        f.arrow(83, 0, 83, 10, w=1.5, size=5, col=RED)
        f.text(88, 2, "Q  (heat supplied)", size=7, anchor="start")
    if kind in ("general", "turbine"):
        f.arrow(100, 52, 100, 62 - 0.1, w=1.5, size=5, col=BLUE)
        f.text(105, 55.5, "W (work output)", size=7, anchor="start")
    return f.d


@fig("te_wall_layers")
def te_wall_layers(n=2, labels=None, temps=None, flow="Q", rising=False):
    labels = labels or [("L₁, k₁", 24), ("L₂, k₂", 14)]
    temps = temps or ["T₁", "T₂", "T₃"]
    f = Fig(165, 62, 1.0)
    x = 40
    f.arrow(8, 22, 38, 22, w=1.6, size=5)
    f.text(22, 25, flow, size=8, bold=True)
    xs = [x]
    for lab, w in labels:
        f.rect(x, 8, w, 28, lw=1.0, fill=LIGHT if len(xs) % 2 else None)
        f.text(x + w / 2, 20, lab, size=7)
        x += w
        xs.append(x)
    f.arrow(x + 2, 22, x + 28, 22, w=1.6, size=5)
    for xx, t in zip(xs, temps):
        f.line(xx, 36, xx, 41, w=0.5, dash=HIDDEN)
        f.text(xx, 43, t, size=7.5, bold=True)
    # temperature profile
    ys = [52, 48, 40, 38][: len(temps)]
    prof = [(xx, 58 - 6 * i - (i > 0) * 3 * i) for i, xx in enumerate(xs)]
    f.pline([(xs[i], (46 + 4 * i) if rising else (54 - 4 * i)) for i in range(len(xs))], w=1.2, col=RED)
    f.text(xs[0] - 2, 52, "Temperature profile", size=6.6, anchor="end", col=RED)
    return f.d


@fig("te_heat_modes")
def te_heat_modes():
    f = Fig(165, 50, 1.0)
    # conduction
    f.rect(8, 14, 40, 14, lw=1.0, fill=LIGHT)
    f.text(28, 19.5, "Solid bar", size=7)
    f.text(8, 31, "Hot end", size=6.5, anchor="start", col=RED); f.text(48, 31, "Cold end", size=6.5, anchor="end", col=BLUE)
    f.arrow(12, 8, 44, 8, w=1.3, size=4.5); f.text(28, 2, "Heat flow", size=6.5)
    f.text(28, 42, "CONDUCTION", size=7.5, bold=True); f.text(28, 37.5, "(through solid, no motion)", size=6.2)
    # convection
    f.rect(70, 8, 36, 5, lw=1.0, fill=LIGHT)
    f.text(88, 9.2, "Hot plate", size=6.3)
    for x in (74, 88, 102):
        f.pline([(x, 14), (x - 3, 20), (x + 3, 26), (x, 32)], w=0.9)
        f.arrowhead(x, 32, math.pi / 2, 3.5)
    f.text(88, 42, "CONVECTION", size=7.5, bold=True); f.text(88, 37.5, "(fluid in motion)", size=6.2)
    # radiation
    f.circle(128, 22, 7, w=1.0, fill=LIGHT); f.text(128, 20.8, "Hot", size=6.3)
    f.rect(152, 12, 6, 22, lw=1.0, fill=LIGHT)
    for dy in (-6, 0, 6):
        f.pline([(136, 22 + dy), (140, 23 + dy), (144, 21 + dy), (148, 22 + dy)], w=0.9)
        f.arrowhead(151, 22 + dy, 0, 3.5)
    f.text(135, 42, "RADIATION", size=7.5, bold=True); f.text(135, 37.5, "(waves, no medium)", size=6.2)
    return f.d
