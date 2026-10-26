"""Production Drawing figures, part 4: foot step bearing and universal coupling parts."""
import math
from draw import *
from figreg import fig
from figs_pd3 import sect, rr


@fig("pd_foot_step")
def pd_foot_step():
    """Assembly of the foot step bearing (S25 Q5a): sectional front view and top view."""
    s = 0.55
    f = Fig(300, 240, s)
    cx, oz = 100, 40
    Z = lambda z: oz + z
    base_t = 18
    H = 88                                   # total height of body
    # body (C.I.): base plate 200 x 18, boss phi94 up to 88, bore phi68 with sunk recess phi71 x 3 at top
    for sg in (1, -1):
        pts = [(cx + sg * 100, Z(0)), (cx + sg * 100, Z(base_t)), (cx + sg * 47, Z(base_t)), (cx + sg * 47, Z(H)), (cx + sg * 35.5, Z(H)),
               (cx + sg * 35.5, Z(H - 3)), (cx + sg * 34, Z(H - 3)), (cx + sg * 34, Z(0))]
        sect(f, pts, 45)
    # bush (G.M.): phi68 outer, phi50 bore, collar phi78 x 8 at top, length 70
    for sg in (1, -1):
        pts = [(cx + sg * 25, Z(0)), (cx + sg * 34, Z(0)), (cx + sg * 34, Z(H - 11)), (cx + sg * 39, Z(H - 11)), (cx + sg * 39, Z(H - 3)), (cx + sg * 25, Z(H - 3))]
        sect(f, pts, -45)
    # shaft (M.S.): phi50 lower part, phi64 shoulder above the bush (not sectioned)
    f.rect(cx - 25, Z(15), 50, H + 40 - 15 + 0, lw=1.2) if False else None
    f.pline([(cx - 25, Z(15)), (cx - 25, Z(H + 30)), (cx - 32, Z(H + 30)), (cx - 32, Z(H + 55))], w=1.2)
    f.pline([(cx + 25, Z(15)), (cx + 25, Z(H + 30)), (cx + 32, Z(H + 30)), (cx + 32, Z(H + 55))], w=1.2)
    f.pline([(cx - 32, Z(H + 55)), (cx - 28, Z(H + 58)), (cx + 28, Z(H + 52)), (cx + 32, Z(H + 55))], w=0.9)
    # disc (G.M.) at the bottom under the shaft: phi50 x 15, bottom dished R60
    sect(f, rr(cx - 25, Z(0), cx + 25, Z(15)), -45, gap=1.6)
    # pin (M.S.) phi4
    f.rect(cx + 12, Z(0), 4, 6, lw=1.0, fill=BLACK)
    f.center_v(cx, Z(-6), Z(H + 66), 0)
    f.dim_h(cx - 100, cx + 100, Z(0), "200", off=-10, ext_from=(Z(0), Z(0)))
    f.dim_v(Z(0), Z(H), cx - 108, "88", off=-6, ext_from=(cx - 100, cx - 100))
    f.dim_h(cx - 47, cx + 47, Z(H), "Ø94", off=8, ext_from=(Z(H), Z(H)))
    f.dim_h(cx - 34, cx + 34, Z(30), "Ø68 H7 / g6", off=0, size=6.2) if False else None
    f.dim_h(cx - 25, cx + 25, Z(H + 60), "Ø50", off=8, size=6.5) if False else None
    for (x, z, t, a) in ((cx + 60, Z(40), "1 Body", "start"), (cx + 41, Z(70), "2 Bush", "start"), (cx + 36, Z(H + 40), "3 Shaft", "start"), (cx + 28, Z(7), "4 Disc", "start"), (cx + 18, Z(2), "5 Pin", "start")):
        f.text(x, z, t, size=6.8, anchor=a)
    f.text(cx, Z(-30), "SECTIONAL FRONT VIEW", size=8, bold=True)
    # fits annotation
    f.text(cx - 150 + 160, Z(H + 78), "fit: Ø68 H7/g6 (body–bush),  Ø50 H7/e8 (bush–shaft)", size=6.2, anchor="start") if False else None
    # top view
    tx, ty = 235, 70
    f.rect(tx - 50, ty - 32, 100, 65, lw=1.3) if False else None
    sx = 0.5
    f.rect(tx - 100 * sx, ty - 65 * sx, 200 * sx, 130 * sx, lw=1.3)
    f.circle(tx, ty, 47 * sx, w=1.3); f.circle(tx, ty, 39 * sx, w=1.0); f.circle(tx, ty, 34 * sx, w=1.0); f.circle(tx, ty, 32 * sx, w=1.0)
    for (px, py) in ((-80, 45), (-80, -45), (80, 45), (80, -45)):
        f.rect(tx + (px - 7.5) * sx, ty + (py - 7) * sx, 15 * sx, 14 * sx, lw=1.0) if False else f.circle(tx + px * sx, ty + py * sx, 7.5 * sx, w=1.0)
    f.center_h(tx - 110 * sx, tx + 110 * sx, ty, 0); f.center_v(tx, ty - 75 * sx, ty + 75 * sx, 0)
    f.dim_h(tx - 100 * sx, tx + 100 * sx, ty - 65 * sx, "200", off=-8, ext_from=(ty - 65 * sx, ty - 65 * sx))
    f.dim_v(ty - 65 * sx, ty + 65 * sx, tx + 100 * sx, "130", off=8, ext_from=(tx + 100 * sx, tx + 100 * sx))
    f.text(tx, ty - 65 * sx - 20, "TOP VIEW", size=8, bold=True)
    return f.d


@fig("pd_ujoint_parts")
def pd_ujoint_parts(part="fork"):
    """Universal coupling details (W24 Q4): proportions from Fig. 5 (shaft d = 50)."""
    s = 0.5
    f = Fig(330, 190, s)
    D, d, pin, ear, gap_, boss_L = 88, 50, 30, 28, 44, 86
    if part == "fork":
        ox, cy = 20, 120
        # sectional front view of the fork: boss (hatched) with bore and the fork ears
        for sg in (1, -1):
            pts = [(ox, cy + sg * d / 2), (ox, cy + sg * D / 2), (ox + boss_L, cy + sg * D / 2), (ox + boss_L + 30, cy + sg * gap_ / 2 + sg * ear * 0 + sg * ear), (ox + boss_L + 62, cy + sg * (gap_ / 2 + ear)),
                   (ox + boss_L + 62, cy + sg * gap_ / 2), (ox + boss_L, cy + sg * gap_ / 2), (ox + boss_L, cy + sg * d / 2)]
            pts = [(ox, cy + sg * d / 2), (ox, cy + sg * D / 2), (ox + boss_L, cy + sg * D / 2), (ox + boss_L, cy + sg * (gap_ / 2 + ear)),
                   (ox + boss_L + 40, cy + sg * (gap_ / 2 + ear)), (ox + boss_L + 40, cy + sg * gap_ / 2), (ox + boss_L, cy + sg * gap_ / 2), (ox + boss_L, cy + sg * d / 2)]
            pts = [(ox, cy + sg * d / 2), (ox, cy + sg * D / 2), (ox + boss_L, cy + sg * D / 2), (ox + boss_L + 40, cy + sg * (gap_ / 2 + ear)),
                   (ox + boss_L + 40, cy + sg * gap_ / 2), (ox + boss_L, cy + sg * gap_ / 2), (ox + boss_L, cy + sg * d / 2)]
            sect(f, pts, 45)
        f.circle(ox + boss_L + 24, cy + gap_ / 2 + ear / 2, 0.0)
        for sg in (1, -1):                       # pin holes (dashed circles shown in the section as centre marks)
            f.center_mark(ox + boss_L + 22, cy + sg * (gap_ / 2 + ear / 2), 4)
        f.line(ox + boss_L + 22 - pin / 2, cy - D / 2 - 4, ox + boss_L + 22 - pin / 2, cy + D / 2 + 4, w=0.5, dash=HIDDEN)
        f.line(ox + boss_L + 22 + pin / 2, cy - D / 2 - 4, ox + boss_L + 22 + pin / 2, cy + D / 2 + 4, w=0.5, dash=HIDDEN)
        f.center_h(ox - 8, ox + boss_L + 50, cy, 0)
        f.dim_h(ox, ox + boss_L, cy - D / 2, "86", off=-8, ext_from=(cy - D / 2, cy - D / 2))
        f.dim_v(cy - D / 2, cy + D / 2, ox, "Ø88", off=-8, ext_from=(ox, ox))
        f.dim_v(cy - d / 2, cy + d / 2, ox + 12, "Ø50", off=0, size=6.2)
        f.dim_v(cy - gap_ / 2, cy + gap_ / 2, ox + boss_L + 40, "44", off=8, ext_from=(ox + boss_L + 40, ox + boss_L + 40), size=6.5)
        f.dim_h(ox + boss_L + 22 - pin / 2, ox + boss_L + 22 + pin / 2, cy + D / 2 + 4, "Ø30 pin hole", off=4, size=6.2)
        f.text(ox + 70, cy + D / 2 + 22, "FORK – sectional front view", size=8, bold=True)
        # top view
        tx = 190
        f.rect(tx - 20, cy - D / 2, boss_L * 0.0 + 0, D, lw=0.0) if False else None
        f.rect(tx - 10, cy - D / 2, boss_L, D, lw=1.3)
        f.rect(tx - 10 + boss_L, cy - gap_ / 2 - ear, 40, ear * 2 + gap_, lw=1.3) if False else None
        f.pline([(tx - 10 + boss_L, cy + D / 2), (tx - 10 + boss_L + 40, cy + gap_ / 2 + ear), (tx - 10 + boss_L + 40, cy - gap_ / 2 - ear), (tx - 10 + boss_L, cy - D / 2)], w=1.3)
        f.line(tx - 10 + boss_L, cy - D / 2, tx - 10 + boss_L, cy + D / 2, w=1.0)
        f.circle(tx - 10 + boss_L + 22, cy, pin / 2, w=1.0)
        f.line(tx - 10, cy - d / 2, tx - 10 + boss_L, cy - d / 2, w=0.6, dash=HIDDEN); f.line(tx - 10, cy + d / 2, tx - 10 + boss_L, cy + d / 2, w=0.6, dash=HIDDEN)
        f.line(tx - 10 + boss_L, cy - gap_ / 2, tx - 10 + boss_L + 40, cy - gap_ / 2, w=0.6, dash=HIDDEN); f.line(tx - 10 + boss_L, cy + gap_ / 2, tx - 10 + boss_L + 40, cy + gap_ / 2, w=0.6, dash=HIDDEN)
        f.center_h(tx - 18, tx + boss_L + 40, cy, 0)
        f.text(tx + 40, cy + D / 2 + 22, "TOP VIEW", size=8, bold=True)
    elif part == "block_pin":
        ox, cy = 30, 120
        B = 50
        sect(f, rr(ox, cy - B / 2, ox + gap_, cy + B / 2), 45)
        f.rect(ox + gap_ / 2 - pin / 2, cy - B / 2, pin, B, lw=0.0) if False else None
        f.line(ox + gap_ / 2 - pin / 2, cy - B / 2, ox + gap_ / 2 - pin / 2, cy + B / 2, w=0.6, dash=HIDDEN); f.line(ox + gap_ / 2 + pin / 2, cy - B / 2, ox + gap_ / 2 + pin / 2, cy + B / 2, w=0.6, dash=HIDDEN)
        f.center_v(ox + gap_ / 2, cy - B / 2 - 8, cy + B / 2 + 8, 0)
        f.dim_h(ox, ox + gap_, cy - B / 2, "44", off=-8, ext_from=(cy - B / 2, cy - B / 2))
        f.dim_v(cy - B / 2, cy + B / 2, ox + gap_, "50", off=8, ext_from=(ox + gap_, ox + gap_))
        f.text(ox + 20, cy + B / 2 + 24, "CENTRE BLOCK – front view", size=8, bold=True)
        # pin: 30 dia x 106, with 6 dia taper pin hole
        px, py = 120, cy - 53
        f.rect(px, py, pin, 106, lw=1.3)
        f.circle(px + pin / 2, py + 8, 3, w=1.0)
        f.center_v(px + pin / 2, py - 6, py + 112, 0)
        f.dim_v(py, py + 106, px + pin, "106", off=8, ext_from=(px + pin, px + pin))
        f.dim_h(px, px + pin, py, "Ø30", off=-8, ext_from=(py, py))
        f.text(px + 15, py - 22, "PIN – front view", size=8, bold=True)
        # top view of the block and pin
        tx = 190
        f.rect(tx, cy - B / 2, gap_, B, lw=1.3)
        f.circle(tx + gap_ / 2, cy, pin / 2, w=1.0)
        f.center_mark(tx + gap_ / 2, cy, B / 2 + 6)
        f.text(tx + 20, cy + B / 2 + 24, "TOP VIEW", size=8, bold=True)
    elif part == "collar_shaft_key":
        ox, cy = 20, 125
        collar_L = 30
        for sg in (1, -1):
            sect(f, [(ox, cy + sg * d / 2), (ox, cy + sg * D / 2), (ox + collar_L, cy + sg * D / 2), (ox + collar_L, cy + sg * d / 2)], 45)
        f.pline([(ox - 30, cy + d / 2), (ox + 76, cy + d / 2)], w=1.2); f.pline([(ox - 30, cy - d / 2), (ox + 76, cy - d / 2)], w=1.2)
        f.pline([(ox - 30, cy + d / 2), (ox - 27, cy + 12), (ox - 33, cy), (ox - 27, cy - 12), (ox - 30, cy - d / 2)], w=0.9)
        f.rect(ox + 2, cy + d / 2 - 5, 56, 10, lw=0.0) if False else f.rect(ox + 4, cy + d / 2 - 4, 40, 8, lw=1.0)
        f.center_h(ox - 36, ox + 82, cy, 0)
        f.dim_h(ox, ox + collar_L, cy - D / 2, "30", off=-8, ext_from=(cy - D / 2, cy - D / 2))
        f.dim_v(cy - D / 2, cy + D / 2, ox, "Ø88", off=-8, ext_from=(ox, ox))
        f.dim_v(cy - d / 2, cy + d / 2, ox - 18, "Ø50", off=0, size=6.2)
        f.text(ox + 30, cy + D / 2 + 20, "COLLAR, SHAFT and KEY – front view (collar sectioned)", size=7, bold=True)
        tx = 190
        f.rect(tx, cy - D / 2, collar_L, D, lw=1.3)
        f.rect(tx - 30, cy - d / 2, 106, d, lw=0.0)
        f.line(tx - 30, cy - d / 2, tx, cy - d / 2, w=1.2); f.line(tx - 30, cy + d / 2, tx, cy + d / 2, w=1.2)
        f.line(tx + collar_L, cy - d / 2, tx + 76, cy - d / 2, w=1.2); f.line(tx + collar_L, cy + d / 2, tx + 76, cy + d / 2, w=1.2)
        f.rect(tx + 4, cy - 5, 40, 10, lw=1.0)
        f.center_h(tx - 36, tx + 82, cy, 0)
        f.text(tx + 20, cy + D / 2 + 20, "TOP VIEW", size=8, bold=True)
    return f.d
