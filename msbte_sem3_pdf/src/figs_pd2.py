"""Production Drawing figures, part 2: orthographic projection answers."""
import math
from draw import *
from figreg import fig


def ell(cx, cy, a, b, a0=0, a1=360, n=48):
    return [(cx + a * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + b * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


@fig("pd_w24_2a")
def pd_w24_2a():
    """W24 Q2(a): front view, auxiliary view and COMPLETED side view of the bent plate."""
    k = 0.43
    f = Fig(380, 235, k)      # model space in mm
    ox, oy = 125, 34          # FV origin (corner of base)
    s60, c60 = math.sin(math.radians(60)), math.cos(math.radians(60))
    t = 18.0
    # --- front view ---
    nrm = (s60, -c60)
    xin = (t * nrm[0]) + (18 + t * c60 * 1.0 - t * c60 * 0) * 0
    # inner edge meets base top (y = 18)
    off = (t * s60, -t * c60)
    tt = (18 - off[1]) / s60
    p_in_base = (off[0] + tt * c60, 18)
    tip_o = (100 * c60, 100 * s60)
    tip_i = (tip_o[0] + off[0], tip_o[1] + off[1])
    fv = [(0, 0), (150, 0), (150, 18), p_in_base, tip_i, tip_o]
    f.pline([(ox + x, oy + y) for x, y in fv], closed=True, w=1.3)
    f.line(ox + 110, oy, ox + 110, oy + 18, w=1.0)
    f.line(ox + 107, oy, ox + 107, oy + 18, w=0.5, dash=HIDDEN)
    f.dim_h(ox, ox + 150, oy, "150", off=-12, ext_from=(oy, oy))
    f.dim_h(ox + 110, ox + 150, oy + 18, "40", off=8, ext_from=(oy + 18, oy + 18))
    f.dim_v(oy, oy + 18, ox + 150, "18", off=8, ext_from=(ox + 150, ox + 150))
    f.text(ox + 75, oy - 26, "F.V.", size=8, bold=True)
    f.arc(ox + p_in_base[0] + 4, oy + 18, 20, 0, 60, w=0.4)
    f.text(ox + 62, oy + 24, "60°", size=7)
    # --- side view (left hand side view, to the right) ---
    cx = 350
    u = lambda uu, yy: (cx + uu, oy + yy)
    f.rect(cx - 40, oy, 80, 18, lw=1.3)
    for uu in (-15, 15):
        f.line(*u(uu, 0), *u(uu, 18), w=1.0)
    f.line(*u(0, -4), *u(0, 24), w=0.35, dash=CHAIN)
    top = [u(uu, 0.866 * (60 + math.sqrt(max(0.0, 1600 - uu * uu)))) for uu in [-40 + 80 * i / 60 for i in range(61)]]
    f.pline([u(-40, 18), u(-40, 0.866 * 60)] + top + [u(40, 18)], w=1.3)
    # hidden hole (two ellipses + side lines)
    yc1 = 0.866 * 60
    yc2 = yc1 - 9
    f.pline([(cx + x, oy + y) for x, y in ell(0, yc1, 25, 25 * s60)], w=0.6, dash=HIDDEN)
    f.pline([(cx + x, oy + y) for x, y in ell(0, yc2, 25, 25 * s60)], w=0.6, dash=HIDDEN)
    for uu in (-25, 25):
        f.line(*u(uu, yc1), *u(uu, yc2), w=0.6, dash=HIDDEN)
    f.dim_h(cx - 40, cx + 40, oy, "80", off=-12, ext_from=(oy, oy))
    f.dim_h(cx - 15, cx + 15, oy + 18, "30", off=6, ext_from=(oy + 18, oy + 18), size=6.5)
    f.text(cx, oy - 26, "S.V. (completed)", size=8, bold=True)
    # projectors from F.V. heights to S.V.
    for yy in (18, tip_o[1]):
        f.line(ox + 150 + 14, oy + yy, cx - 46, oy + yy, w=0.25, dash=HIDDEN) if False else None
    f.line(ox + tip_o[0], oy + tip_o[1], cx - 40, oy + tip_o[1], w=0.25, dash=HIDDEN) if False else None
    f.line(ox + 150 + 18, oy + 18, cx - 44, oy + 18, w=0.25, dash=HIDDEN)
    f.line(ox + tip_o[0] + 8, oy + 0.866 * 100, cx + 0, oy + 0.866 * 100, w=0.25, dash=HIDDEN)
    f.line(ox + tip_o[0] + 4, oy + 0.866 * 60, cx - 40, oy + 0.866 * 60, w=0.25, dash=HIDDEN)
    # --- auxiliary view (perpendicular to the arm, upper left) ---
    dirA = (c60, s60)
    dirB = (-s60, c60)
    org = (ox, oy + 36)
    def G(a, b):
        return (org[0] + a * dirA[0] + b * dirB[0], org[1] + a * dirA[1] + b * dirB[1])
    bc = 78.0
    outline = [G(0, bc - 40), G(60, bc - 40)] + [G(60 + 40 * math.cos(math.radians(a)), bc + 40 * math.sin(math.radians(a))) for a in range(-90, 91, 10)] + [G(0, bc + 40)]
    f.pline(outline, closed=True, w=1.3)
    f.pline([G(60 + 25 * math.cos(math.radians(a)), bc + 25 * math.sin(math.radians(a))) for a in range(0, 361, 10)], w=1.3)
    f.line(*G(-4, bc), *G(104, bc), w=0.35, dash=CHAIN)
    f.line(*G(60, bc - 46), *G(60, bc + 46), w=0.35, dash=CHAIN)
    x1, y1 = G(100, bc + 44)
    f.text(x1 - 6, y1 + 6, "Aux. view", size=8, bold=True, anchor="end")
    f.text(*G(78, bc + 8), "Ø50", size=6.8)
    f.text(*G(104, bc + 14), "R40", size=6.8)
    return f.d


@fig("pd_s25_2b")
def pd_s25_2b():
    """S25 Q2(b): F.V., L.H.S.V. and auxiliary top view looking in the direction X (45°)."""
    k = 0.62
    f = Fig(265, 215, k)
    r2 = math.sqrt(0.5)
    # model: x right, z up in FV; y across in side view
    ox, oy = 12, 140
    fv = [(0, 0), (100, 0), (100, 50), (50, 50)]
    f.pline([(ox + x, oy + z) for x, z in fv], closed=True, w=1.3)
    f.line(ox + 35, oy + 35, ox + 100, oy + 35, w=0.35, dash=CHAIN)
    f.line(ox + 10, oy + 10, ox + 100, oy + 10, w=0.6, dash=HIDDEN)
    f.arc(ox, oy, 22, 0, 45, w=0.4); f.text(ox + 26, oy + 5, "45°", size=7)
    f.dim_h(ox, ox + 100, oy, "100", off=-10, ext_from=(oy, oy))
    f.text(ox + 50, oy - 22, "F.V.", size=8, bold=True)
    # direction of view X
    f.arrow(ox + 12, oy + 74, ox + 30, oy + 56, w=1.1, size=4.5)
    f.text(ox + 8, oy + 77, "X", size=8, bold=True)
    # LHSV
    cx = 175
    prof_out = [(-15, 0), (15, 0), (37.5, 22.5), (37.5, 50), (25, 50), (25, 35)]
    outer = [(-15, 0), (15, 0), (37.5, 22.5), (37.5, 50), (25, 50)]
    groove = [(25 * math.cos(math.radians(a)), 35 + 25 * math.sin(math.radians(a))) for a in range(0, -181, -10)]
    pts = [(-15, 0), (15, 0), (37.5, 22.5), (37.5, 50), (25, 50), (25, 35)] + groove[1:] + [(-25, 35), (-25, 50), (-37.5, 50), (-37.5, 22.5)]
    f.pline([(cx + y, oy + z) for y, z in pts], closed=True, w=1.3)
    f.line(cx, oy - 4, cx, oy + 56, w=0.35, dash=CHAIN)
    f.line(cx - 40, oy + 35, cx + 40, oy + 35, w=0.35, dash=CHAIN)
    f.dim_h(cx - 37.5, cx + 37.5, oy + 50, "75", off=6, ext_from=(oy + 50, oy + 50))
    f.dim_h(cx - 15, cx + 15, oy, "30", off=-10, ext_from=(oy, oy))
    f.dim_v(oy, oy + 50, cx + 37.5, "50", off=8, ext_from=(cx + 37.5, cx + 37.5))
    f.dim_v(oy + 35, oy + 50, cx + 25, "15", off=-0.0, ext_from=(cx + 25, cx + 25), size=6.5) if False else None
    f.text(cx + 3, oy + 28, "R25", size=6.8, anchor="start")
    f.text(cx, oy - 22, "L.H.S.V.", size=8, bold=True)
    # auxiliary top view: coords (y, v) with v = 0.7071 (x + z)
    ax_, ay_ = 12, 4
    A = lambda y, v: (ax_ + 37.5 + y, ay_ + v)
    def face(y, z):                     # point on the sloping end face (x = z)
        return A(y, r2 * 2 * z)
    # sloping face outline
    pl = [(-15, 0), (15, 0), (37.5, 22.5), (37.5, 50)]
    seq = [face(y, z) for y, z in pl]
    f.pline(seq, w=1.3)
    f.line(*face(37.5, 50), *A(37.5, r2 * 150), w=1.3)
    f.line(*face(-37.5, 50), *A(-37.5, r2 * 150), w=1.3)
    f.line(*A(-37.5, r2 * 150), *A(37.5, r2 * 150), w=1.3)
    f.pline([face(-15, 0), face(-37.5, 22.5), face(-37.5, 50)], w=1.3)
    f.line(*face(-37.5, 50), *face(-25, 50), w=1.3); f.line(*face(37.5, 50), *face(25, 50), w=1.3)
    # groove on the sloping face: sides y=±25 from z=50 to 35, elliptical bottom
    f.line(*face(25, 50), *face(25, 35), w=1.3); f.line(*face(-25, 50), *face(-25, 35), w=1.3)
    f.pline([face(25 * math.cos(math.radians(a)), 35 + 25 * math.sin(math.radians(a))) for a in range(0, -181, -10)], w=1.3)
    # groove edges continuing on the top face
    f.line(*A(25, r2 * 100), *A(25, r2 * 150), w=1.3); f.line(*A(-25, r2 * 100), *A(-25, r2 * 150), w=1.3)
    f.line(*face(25, 50), *A(25, r2 * 100), w=0.0)
    f.line(*A(-37.5, r2 * 100), *A(37.5, r2 * 100), w=0.35, dash=HIDDEN) if False else None
    f.line(ax_ + 37.5, ay_ - 4, ax_ + 37.5, ay_ + r2 * 150 + 6, w=0.35, dash=CHAIN)
    f.text(ax_ + 37.5 + 48, ay_ + 40, "Auxiliary top view", size=8, bold=True, anchor="start")
    f.text(ax_ + 37.5 + 48, ay_ + 33, "(looking along X, true shape of", size=6.8, anchor="start"); f.text(ax_ + 37.5 + 48, ay_ + 28.5, "the sloping face)", size=6.8, anchor="start")
    f.text(ax_ + 37.5 + 48, ay_ + 18, "Vertical sizes on the sloping face", size=6.6, anchor="start"); f.text(ax_ + 37.5 + 48, ay_ + 13.5, "are multiplied by 1/sin 45° = 1.414", size=6.6, anchor="start")
    return f.d
