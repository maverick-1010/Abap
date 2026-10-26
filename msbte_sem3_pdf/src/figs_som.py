"""Strength of Materials figures."""
import math
from draw import *
from figreg import fig
from beam import Beam
import calcfw


def ans(cid, i):
    return calcfw.load(cid)["answers"][i]["raw"]


def sfbm(beam, names, loads, sf_txt=None, bm_txt=None, w=118, title=None, fu="kN", mu="kN·m", udl_txt=None, height=118):
    """names: {x: 'A'}; loads: {x: '3 kN'} labels for point loads; udl_txt: [(x1,x2,'2 kN/m')]."""
    f = Fig(165, height, 1.0)
    x0 = 24
    sx = w / beam.L
    X = lambda x: x0 + x * sx
    yb = height - 24
    f.line(X(0), yb, X(beam.L), yb, w=2.4)
    for xs in (beam.a, beam.b):
        f.pline([(X(xs), yb - 1), (X(xs) - 3, yb - 6), (X(xs) + 3, yb - 6)], closed=True, w=0.8, fill=LIGHT)
    for x, nm in names.items():
        f.text(X(x), yb - 11, nm, size=7.5, bold=True)
    for x, W in beam.points:
        f.arrow(X(x), yb + 13, X(x), yb + 1.2, w=1.1, size=4)
        f.text(X(x), yb + 15, loads.get(x, f"{W} kN"), size=6.8)
    for (x1, x2, txt) in (udl_txt or []):
        f.line(X(x1), yb + 7, X(x2), yb + 7, w=0.8)
        n = max(3, int((x2 - x1) * sx / 5))
        for i in range(n + 1):
            xx = X(x1) + (X(x2) - X(x1)) * i / n
            f.arrow(xx, yb + 7, xx, yb + 1.2, w=0.5, size=2.5)
        f.text((X(x1) + X(x2)) / 2, yb + 9, txt, size=6.8)
    keys = beam.key_xs()
    sfs = [abs(beam.sf(x, "right")) for x in keys] + [abs(beam.sf(x, "left")) for x in keys]
    smax = max(sfs)
    ks = 13 / smax
    ys = yb - 30
    f.text(4, ys + 14, "S.F.D.", size=7.5, bold=True, anchor="start")
    f.line(X(0), ys, X(beam.L), ys, w=0.6)
    pts = []
    for x0_, x1_ in zip(keys, keys[1:]):
        pts += [(X(x0_), ys + ks * beam.sf(x0_, "right")), (X(x1_), ys + ks * beam.sf(x1_, "left"))]
    f.pline(pts, w=1.3)
    for x in keys:                                       # vertical jumps and drop to zero line
        a, b_ = beam.sf(x, "left"), beam.sf(x, "right")
        f.line(X(x), ys + ks * a, X(x), ys + ks * b_, w=1.3)
        f.line(X(x), yb - 7 if x in (beam.a, beam.b) else yb - 1, X(x), ys + 12, w=0.3, dash=HIDDEN) if False else None
    done = set()
    for x in keys:
        for side, anc, dx in (("right", "start", 1.2), ("left", "end", -1.2)):
            v = beam.sf(x, side)
            if (side == "left" and x == 0) or (side == "right" and x == beam.L):
                continue
            if side == "left" and abs(beam.sf(x, "left") - beam.sf(x, "right")) < 1e-9:
                continue
            key = (round(x, 6), round(v, 6))
            if key in done:
                continue
            done.add(key)
            txt = (sf_txt or {}).get((x, side), f"{v:+.2f}")
            if abs(v) < 1e-9:
                txt = "0"
            f.text(X(x) + dx, ys + ks * v + (1.5 if v >= 0 else -4.2), txt, size=6.4, anchor=anc)
    for z in beam.sf_zero_points():
        f.circle(X(z), ys, 0.8, fill=BLACK)
        f.text(X(z), ys - 4.5, f"SF = 0 at x = {z:.3f} m", size=6.2)
    yM = ys - 38
    ms = [beam.bm(i * beam.L / 400) for i in range(401)]
    kM = 15 / max(abs(m) for m in ms)
    f.text(4, yM + 14, "B.M.D.", size=7.5, bold=True, anchor="start")
    f.line(X(0), yM, X(beam.L), yM, w=0.6)
    f.pline([(X(i * beam.L / 400), yM + kM * ms[i]) for i in range(401)], w=1.3)
    for x in keys:
        m = beam.bm(x)
        f.circle(X(x), yM + kM * m, 0.7, fill=BLACK)
        if abs(m) > 1e-9:
            txt = (bm_txt or {}).get(x, f"{m:+.2f}")
            f.text(X(x), yM + kM * m + (2.0 if m >= 0 else -5), txt, size=6.4)
    for z in beam.sf_zero_points():
        m = beam.bm(z)
        if all(abs(z - k) > 1e-6 for k in keys):
            f.circle(X(z), yM + kM * m, 0.7, fill=BLACK)
            f.text(X(z), yM + kM * m + 2.0, f"{m:+.2f}", size=6.4)
    for z in beam.contraflexure():
        f.circle(X(z), yM, 1.2, w=0.9, fill=colors.white)
        f.text(X(z), yM + 4.5 if False else yM - 5, f"contraflexure x = {z:.3f} m", size=6.2)
    if fu:
        f.text(160, ys + 13, f"({fu})", size=6.4, anchor="end")
    if mu:
        f.text(160, yM + 13, f"({mu})", size=6.4, anchor="end")
    return f.d


@fig("som_sfbm_3c")
def som_sfbm_3c():
    b = Beam(7, 0, 7, points=[(3, 3), (5, 5)], udls=[(0, 3, 2)])
    return sfbm(b, {0: "A", 3: "C", 5: "D", 7: "B"}, {3: "3 kN", 5: "5 kN"}, udl_txt=[(0, 3, "2 kN/m")])


@fig("som_sfbm_5b")
def som_sfbm_5b():
    b = Beam(7, 0, 5, points=[(2, 5), (7, 5)], udls=[(0, 7, 8)])
    return sfbm(b, {0: "A", 2: "D", 5: "B", 7: "C"}, {2: "5 kN", 7: "5 kN"}, udl_txt=[(0, 7, "8 kN/m")])


@fig("som_sfbm_2d")
def som_sfbm_2d():
    L, a = 10.0, 6.0
    b = Beam(L, 0, L, points=[(a, 10.0)])
    sf = {(0.0, "right"): "+W b / L", (a, "left"): "+W b / L", (a, "right"): "− W a / L", (L, "left"): "− W a / L"}
    bm = {a: "+ W a b / L"}
    return sfbm(b, {0: "A", a: "C", L: "B"}, {a: "W"}, sf_txt=sf, bm_txt=bm, fu="", mu="", height=118)


@fig("som_core_rect")
def som_core_rect():
    f = Fig(110, 62, 1.0)
    B, D = 60.0, 40.0
    ox, oy = 25, 8
    f.rect(ox, oy, B, D, lw=1.2)
    cx, cy = ox + B / 2, oy + D / 2
    f.pline([(cx - B / 6, cy), (cx, cy + D / 6), (cx + B / 6, cy), (cx, cy - D / 6)], closed=True, w=1.2, fill=LIGHT)
    f.text(cx, cy - 1.2, "CORE", size=6.5, bold=True)
    f.center_h(ox, ox + B, cy, 3); f.center_v(cx, oy, oy + D, 3)
    f.dim_h(ox, ox + B, oy + D, "B", off=5, ext_from=(oy + D, oy + D))
    f.dim_v(oy, oy + D, ox, "D", off=-6, ext_from=(ox, ox))
    f.dim_h(cx - B / 6, cx + B / 6, cy, "B/3", off=-D / 6 - 4, ext_from=(cy, cy), size=6.5)
    f.text(cx + B / 6 + 8, cy + D / 6, "D/3", size=6.5, anchor="start")
    f.text(95, 40, "Load inside the core", size=6.4); f.text(95, 36.5, "⇒ no tension", size=6.4)
    return f.d



@fig("som_contraflexure")
def som_contraflexure():
    f = Fig(165, 62, 1.0)
    ox, W = 15, 120
    f.line(ox, 30, ox + W, 30, w=0.6)
    f.text(ox - 2, 52, "B.M.D. of an overhanging beam", size=7, bold=True, anchor="start")
    pts = []
    for i in range(0, 61):
        x = i / 60
        y = 14 * math.sin(math.pi * x * 1.6) * (1 - 0.0) if x < 0.625 else 14 * math.sin(math.pi * x * 1.6)
        pts.append((ox + W * x, 30 + y if x < 0.625 else 30 + y * 1.0))
    f.pline(pts, w=1.5)
    xc = ox + W * 0.625
    f.circle(xc, 30, 1.6, w=1.0, fill=colors.white)
    f.text(xc, 22, "point of contraflexure", size=6.6); f.text(xc, 18.5, "(B.M. = 0, changes sign)", size=6.4)
    f.text(ox + W * 0.3, 46, "+ (sagging)", size=7); f.text(ox + W * 0.85, 15, "− (hogging)", size=7)
    return f.d



@fig("som_lamina")
def som_lamina():
    f = Fig(165, 60, 1.0)
    k = 0.1
    ox, oy = 12, 12
    Wd, Hd, R, g = 700 * k, 300 * k, 150 * k, 250 * k
    f.pline([(ox, oy + Hd), (ox + Wd, oy + Hd), (ox + Wd, oy), (ox + 2 * R, oy)] + f.arc_pts(ox + R, oy, R, 0, 180, 40)[::1] + [(ox, oy)], closed=False, w=1.4) if False else None
    outline = [(ox, oy + Hd), (ox + Wd, oy + Hd), (ox + Wd, oy), (ox + 2 * R, oy)] + f.arc_pts(ox + R, oy, R, 0, 180, 40) + [(ox, oy + Hd)]
    f.pline(outline, closed=True, w=1.4, fill=LIGHT)
    xa = ox + Wd + g
    f.line(xa, oy - 6, xa, oy + Hd + 6, w=0.8, dash=CHAIN)
    f.text(xa + 1.5, oy + Hd + 4, "A", size=8, bold=True, anchor="start"); f.text(xa + 1.5, oy - 6, "A", size=8, bold=True, anchor="start")
    f.dim_h(ox, ox + Wd, oy + Hd, "700 mm", off=6, ext_from=(oy + Hd, oy + Hd))
    f.dim_h(ox + Wd, xa, oy + Hd, "250 mm", off=6, ext_from=(oy + Hd, oy + Hd + 6))
    f.dim_v(oy, oy + Hd, ox, "300 mm", off=-6, ext_from=(ox, ox))
    f.text(ox + R, oy + 6, "R 150", size=7, bold=True)
    f.text(ox + R + 1, oy + 11, "(removed)", size=6)
    f.text(ox + 62, oy + 15, "Rectangle − semicircle", size=7)
    return f.d






def tau_curve(f, bx, cy, hD, hd, t_flange, t_web_in, t_max, k=1.0, n=14):
    """Shear-stress outline of a hollow box section about its N.A. (symmetric), drawn right of axis x=bx."""
    def tau(y):
        a = abs(y)
        if a >= hd:
            return t_flange * (1 - ((a - hd) / (hD - hd)) ** 2) if False else t_flange * (hD - a) / (hD - hd) * (2 - (hD - a) / (hD - hd))
        return t_web_in + (t_max - t_web_in) * (1 - (a / hd) ** 2)
    ys = [-hD + 2 * hD * i / 200 for i in range(201)]
    pts = []
    for y in ys:
        a = abs(y)
        if a < hd:
            pts.append((bx + tau(y) * k, cy + y))
        else:
            pts.append((bx + tau(y) * k, cy + y))
    # insert the jump at the inner face explicitly
    pts2 = []
    for (x, y) in pts:
        pts2.append((x, y))
    f.line(bx, cy - hD, bx, cy + hD, w=0.8)
    f.pline(pts2, w=1.3)
    f.line(bx, cy + hD, bx + tau(hD) * k, cy + hD, w=0.5)


@fig("som_hollow_rect_dist")
def som_hollow_rect_dist():
    f = Fig(165, 78, 1.0)
    B, D, b, d = 30.0, 44.0, 18.0, 30.0
    ox, oy = 8, 16
    cx, cy = ox + B / 2, oy + D / 2
    f.rect(ox, oy, B, D, lw=1.2); f.rect(cx - b / 2, cy - d / 2, b, d, lw=1.0, fill=colors.white)
    f.center_h(ox - 3, ox + B + 3, cy, 0); f.text(ox + B + 5, cy - 1, "N.A.", size=6.5, anchor="start")
    f.text(cx + 6, oy - 7, "Hollow rectangular section", size=7, bold=True)
    bx = 66
    f.line(bx, oy, bx, oy + D, w=0.8)
    f.pline([(bx, cy), (bx + 14, oy + D), (bx, oy + D)], closed=True, w=1.0, fill=LIGHT)
    f.pline([(bx, cy), (bx - 14, oy), (bx, oy)], closed=True, w=1.0, fill=LIGHT)
    f.text(bx + 16, oy + D - 1, "compression (top)", size=6.2, anchor="start")
    f.text(bx - 16, oy + 1, "tension (bottom)", size=6.2, anchor="end")
    f.text(bx, oy - 7, "Bending stress (linear)", size=7, bold=True)
    f.text(bx + 2, cy + 1.2, "zero at N.A.", size=6, anchor="start")
    sx = 130
    tau_curve(f, sx, cy, D / 2, d / 2, 9.0, 22.0, 28.0, k=0.85)
    f.text(sx + 26, cy + 1.5, "max at N.A.", size=6.2, anchor="start")
    f.text(sx - 6, oy + D + 2.5, "0 at outer edge", size=6, anchor="start")
    f.text(sx + 8, oy - 7, "Shear stress distribution", size=7, bold=True)
    f.text(sx + 14, cy + d / 2 + 2, "sudden jump where width", size=5.8, anchor="start"); f.text(sx + 14, cy + d / 2 - 1.2, "changes (flange → webs)", size=5.8, anchor="start")
    return f.d


@fig("som_hollow_sq_shear")
def som_hollow_sq_shear():
    f = Fig(165, 78, 1.0)
    ox, oy, s = 12, 12, 0.5
    f.rect(ox, oy, 100 * s, 100 * s, lw=1.3)
    f.rect(ox + 20 * s, oy + 20 * s, 60 * s, 60 * s, lw=1.0, fill=colors.white)
    cy = oy + 50 * s
    f.center_h(ox - 3, ox + 100 * s + 3, cy, 0)
    f.text(ox + 100 * s + 5, cy - 1, "N.A.", size=6.5, anchor="start")
    f.dim_h(ox, ox + 100 * s, oy + 100 * s, "100", off=5, ext_from=(oy + 100 * s, oy + 100 * s))
    f.dim_v(oy, oy + 100 * s, ox, "100", off=-6, ext_from=(ox, ox))
    f.text(ox + 50 * s, oy - 5, "t = 20 mm, inner 60 × 60", size=6.5)
    bx = 100
    t_fl, t_in, t_max = 8.272, 20.68, 25.333
    tau_curve(f, bx, cy, 50 * s, 30 * s, t_fl, t_in, t_max, k=1.1)
    f.text(bx + 1.5, oy + 100 * s + 2.5, "0", size=6.6, anchor="start")
    f.text(bx + t_fl * 1.1 + 2, cy + 25 * s + 4, "8.27 (flange, width 100)", size=6.4, anchor="start")
    f.text(bx + t_in * 1.1 + 2, cy + 30 * s - 4, "20.68 (web, width 40)", size=6.4, anchor="start")
    f.text(bx + t_max * 1.1 + 2, cy, "25.33 max at N.A.", size=6.4, anchor="start")
    f.text(bx + 8, oy - 5, "τ distribution (N/mm²)", size=7, bold=True)
    return f.d


@fig("som_stepped")
def som_stepped():
    f = Fig(165, 62, 1.0)
    x = 16
    segs = [(40, 10, "625 mm²", "120 cm"), (24, 26, "2500 mm²", "60 cm"), (30, 14, "1250 mm²", "90 cm")]
    cy = 26
    xs = [x]
    for L, H, a, l in segs:
        f.rect(x, cy - H / 2, L, H, lw=1.2, fill=LIGHT)
        f.text(x + L / 2, cy - 1, a, size=6.8)
        f.dim_h(x, x + L, cy - 18, l, size=6.8, ext_from=(cy - H / 2, cy - H / 2))
        x += L
        xs.append(x)
    f.arrow(xs[0], cy, xs[0] - 13, cy, w=1.5, size=4.5); f.text(xs[0] - 6, cy + 3, "P₁", size=7.5, bold=True)
    f.arrow(xs[1], cy + 7, xs[1] + 12, cy + 7, w=1.5, size=4.5); f.text(xs[1] + 6, cy + 9, "P₂", size=7.5, bold=True)
    f.arrow(xs[2], cy - 7, xs[2] - 12, cy - 7, w=1.5, size=4.5); f.text(xs[2] - 6, cy - 12, "P₃", size=7.5, bold=True)
    f.arrow(xs[3], cy, xs[3] + 13, cy, w=1.5, size=4.5); f.text(xs[3] + 6, cy + 3, "P₄", size=7.5, bold=True)
    for nm, xx in zip("ABCD", xs):
        f.text(xx, cy + 17, nm, size=8, bold=True)
    f.text(4, 56, "Axial forces:  AB = 45 kN (tension),  BC = 320 kN (compression),  CD = 130 kN (tension)", size=6.8, anchor="start")
    return f.d


@fig("som_T_stress")
def som_T_stress():
    f = Fig(165, 82, 1.0)
    yt = 31.19
    s = 0.62
    ox, oy = 30, 12
    top = oy + 110 * s
    f.rect(ox - 55 * s, top - 10 * s, 110 * s, 10 * s, lw=1.2, fill=LIGHT)
    f.rect(ox - 5 * s, oy, 10 * s, 100 * s, lw=1.2, fill=LIGHT)
    yna = top - yt * s
    f.line(ox - 62 * s, yna, ox + 62 * s, yna, w=0.7, dash=CHAIN)
    f.text(ox + 63 * s, yna + 1, "N.A.", size=6.5, anchor="start")
    f.dim_v(yna, top, ox - 58 * s, "31.19", off=-3, ext_from=(ox - 55 * s, ox - 55 * s), size=6.5)
    f.dim_v(oy, yna, ox + 24 * s, "78.81", off=0, ext_from=(ox + 5 * s, ox + 5 * s), size=6.5)
    f.text(ox, oy - 6, "T-section 110 × 110 × 10", size=6.8)
    bx = 100
    ct, tb = ans("SOM-S23-Q6a", 1), ans("SOM-S23-Q6a", 2)
    kk = 0.28
    f.line(bx, oy, bx, top, w=0.8)
    f.pline([(bx, yna), (bx + ct * kk, top), (bx, top)], closed=True, w=1.0, fill=LIGHT)
    f.pline([(bx, yna), (bx - tb * kk, oy), (bx, oy)], closed=True, w=1.0, fill=LIGHT)
    f.text(bx + ct * kk + 1.5, top - 3, f"{ct:.2f} N/mm²", size=6.6, anchor="start"); f.text(bx + ct * kk + 1.5, top - 7, "(compression, top)", size=6.2, anchor="start")
    f.text(bx - tb * kk + 2, oy - 5, f"{tb:.2f} N/mm² (tension, bottom)", size=6.6, anchor="start")
    f.text(bx, top + 6, "Bending stress distribution", size=7, bold=True)
    f.text(bx + 3, yna + 1.5, "0 at N.A.", size=6.2, anchor="start")
    return f.d


@fig("som_cclamp")
def som_cclamp():
    f = Fig(165, 74, 1.0)
    ox, oy = 40, 8
    f.pline([(ox + 56, oy + 62), (ox, oy + 62), (ox, oy), (ox + 56, oy)], w=5.0, col=GREY)
    f.rect(ox + 36, oy + 55, 24, 3, lw=0.9, fill=LIGHT); f.rect(ox + 36, oy + 4, 24, 3, lw=0.9, fill=LIGHT)
    f.arrow(ox + 48, oy + 72, ox + 48, oy + 58.5, w=1.4, size=4.5); f.text(ox + 51, oy + 66, "P", size=8, bold=True, anchor="start")
    f.arrow(ox + 48, oy - 6, ox + 48, oy + 6.5, w=1.4, size=4.5); f.text(ox + 51, oy - 3, "P", size=8, bold=True, anchor="start")
    f.center_v(ox, oy + 6, oy + 56, 0)
    f.dim_h(ox, ox + 48, oy + 31, "e = 144 mm", size=6.8)
    f.line(ox + 48, oy + 8, ox + 48, oy + 55, w=0.4, dash=CHAIN)
    f.text(ox + 3, oy + 20, "section", size=6.2, anchor="start"); f.text(ox + 3, oy + 16.5, "b × t", size=6.2, anchor="start")
    f.text(112, 52, "Section: b = 2t (depth in the plane),", size=6.8, anchor="start"); f.text(112, 47, "thickness t", size=6.8, anchor="start")
    f.text(112, 38, "σ = P/A (direct tension)", size=6.8, anchor="start"); f.text(112, 33, "    + P e / Z (bending)", size=6.8, anchor="start")
    f.text(112, 24, "σ_{max} must not exceed 100 N/mm²".replace("_{max}", "max"), size=6.8, anchor="start")
    return f.d


@fig("som_sign_conv")
def som_sign_conv():
    f = Fig(165, 60, 1.0)
    for ox, ttl, kind in ((0, "Positive S.F.", "sf+"), (42, "Negative S.F.", "sf-"), (84, "Positive B.M. (sagging)", "bm+"), (126, "Negative B.M. (hogging)", "bm-")):
        f.text(ox + 20, 54, ttl, size=6.8, bold=True)
        if kind.startswith("sf"):
            up = kind == "sf+"
            f.rect(ox + 8, 26, 24, 8, fill=LIGHT)
            f.line(ox + 20, 26, ox + 20, 34, w=0.6, dash=HIDDEN)
            a, b = (ox + 3, ox + 37)
            if up:
                f.arrow(a, 22, a, 36, w=1.5, size=4); f.arrow(b, 38, b, 24, w=1.5, size=4)
                f.text(ox + 20, 14, "left part ↑,  right part ↓", size=6.2); f.text(ox + 20, 9.5, "(clockwise)", size=6.2)
            else:
                f.arrow(a, 38, a, 24, w=1.5, size=4); f.arrow(b, 22, b, 36, w=1.5, size=4)
                f.text(ox + 20, 14, "left part ↓,  right part ↑", size=6.2); f.text(ox + 20, 9.5, "(anticlockwise)", size=6.2)
        else:
            sag = kind == "bm+"
            f.pline(f.arc_pts(ox + 20, 38 if sag else 14, 14, 215 if sag else 35, 325 if sag else 145, 20), w=2.0)
            f.text(ox + 20, 10 if sag else 44, "concave upwards" if sag else "concave downwards", size=6.2)
            f.text(ox + 20, 5.5 if sag else 40, "top fibres compressed" if sag else "top fibres in tension", size=6.2)
    return f.d
