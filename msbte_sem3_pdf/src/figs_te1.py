"""Thermal Engineering figures, part 1: P-V / T-S diagrams and block diagrams."""
import math
from draw import *
from figreg import fig


def plot(f, ox, oy, w, h, xl, yl, title=None):
    axes(f, ox, oy, w, h, xl, yl)
    if title:
        f.text(ox + w / 2, oy + h + 4.5, title, bold=True)
    return lambda u, v: (ox + u * w, oy + v * h)


def pt(f, M, u, v, name, dx=1.8, dy=1.2, anchor="start"):
    x, y = M(u, v)
    f.circle(x, y, 0.55, w=0.3, fill=BLACK)
    f.text(x + dx, y + dy, name, anchor=anchor, bold=True, size=7.5)


def line_arrow(f, M, pts, mid_arrow=True, w=MED, col=BLACK):
    xy = [M(*p) for p in pts]
    f.pline(xy, w=w, col=col)
    if mid_arrow and len(xy) >= 2:
        i = len(xy) // 2
        (x1, y1), (x2, y2) = xy[i - 1], xy[i]
        f.arrowhead((x1 + x2) / 2 + (x2 - x1) * 0.15, (y1 + y2) / 2 + (y2 - y1) * 0.15, math.atan2(y2 - y1, x2 - x1), 3.6)


def sample(fn, a, b, n=40):
    return [fn(a + (b - a) * i / n) for i in range(n + 1)]


def expc(t, v0, v1, k):
    return v0 + (v1 - v0) * (math.exp(k * t) - 1) / (math.exp(k) - 1)


def fill_poly(f, M, pts, col=LIGHT):
    f.pline([M(*p) for p in pts], closed=True, w=0.1, fill=col, col=col)


@fig("te_iso_processes")
def te_iso_processes():
    f = Fig(165, 100, 1.0)
    W, H = 56, 34
    # isobaric
    M = plot(f, 20, 58, W, H, "V", "p", "Isobaric process (p = constant)  P-V")
    fill_poly(f, M, [(0.2, 0), (0.8, 0), (0.8, 0.55), (0.2, 0.55)])
    f.text(*M(0.5, 0.2), "Work done", size=6.5)
    line_arrow(f, M, [(0.2, 0.55), (0.8, 0.55)])
    pt(f, M, 0.2, 0.55, "1", dx=-4, dy=1.5)
    pt(f, M, 0.8, 0.55, "2", dx=1.5, dy=1.5)
    M = plot(f, 100, 58, W, H, "s", "T", "Isobaric process  T-S")
    line_arrow(f, M, sample(lambda t: (0.2 + 0.6 * t, expc(t, 0.2, 0.8, 1.2)), 0, 1))
    pt(f, M, 0.2, 0.2, "1", dx=-4, dy=-1)
    pt(f, M, 0.8, 0.8, "2", dx=1.5, dy=0)
    # isochoric
    M = plot(f, 20, 8, W, H, "V", "p", "Isochoric process (V = constant)  P-V")
    line_arrow(f, M, [(0.45, 0.2), (0.45, 0.85)])
    pt(f, M, 0.45, 0.2, "1", dx=2, dy=-1)
    pt(f, M, 0.45, 0.85, "2", dx=2, dy=0)
    f.text(*M(0.7, 0.4), "No work (dV = 0)", size=6.5)
    M = plot(f, 100, 8, W, H, "s", "T", "Isochoric process  T-S")
    line_arrow(f, M, sample(lambda t: (0.2 + 0.5 * t, expc(t, 0.2, 0.85, 2.4)), 0, 1))
    pt(f, M, 0.2, 0.2, "1", dx=-4, dy=-1)
    pt(f, M, 0.7, 0.85, "2", dx=1.5, dy=0)
    f.text(*M(0.82, 0.3), "steeper than\nconstant-p line".split("\n")[0], size=6)
    f.text(*M(0.82, 0.2), "constant-p line".split("\n")[0], size=6)
    return f.d


@fig("te_isothermal")
def te_isothermal():
    f = Fig(165, 52, 1.0)
    W, H = 56, 34
    M = plot(f, 20, 8, W, H, "V", "p", "Isothermal process (pV = C)  P-V")
    cur = sample(lambda t: (0.2 + 0.65 * t, 0.16 / (0.2 + 0.65 * t) + 0.05), 0, 1)
    fill_poly(f, M, [(u, 0) for u, v in cur[:1]] + cur + [(cur[-1][0], 0)])
    line_arrow(f, M, cur)
    pt(f, M, *cur[0], "1", dx=2, dy=0)
    pt(f, M, *cur[-1], "2", dx=0.5, dy=2.5)
    M = plot(f, 100, 8, W, H, "s", "T", "Isothermal process  T-S")
    line_arrow(f, M, [(0.2, 0.5), (0.8, 0.5)])
    pt(f, M, 0.2, 0.5, "1", dx=-4, dy=1.5)
    pt(f, M, 0.8, 0.5, "2", dx=1.5, dy=1.5)
    f.text(*M(0.5, 0.62), "T = constant", size=6.5)
    return f.d


# ---- cycles ----
def pv_curve(V1, V2, P1, n, steps=40):
    return [(V1 + (V2 - V1) * i / steps, P1 * (V1 / (V1 + (V2 - V1) * i / steps)) ** n) for i in range(steps + 1)]


def dome(T):
    a = ((T - 0.12) / 0.78) ** 0.8
    return 0.08 + 0.42 * a, 0.92 - 0.42 * a        # s_liquid, s_vapour


def cycle_pv(f, M, kind):
    g = 1.4
    if kind == "otto":
        a = pv_curve(0.85, 0.25, 0.08, g)
        P3 = 0.82
        b = pv_curve(0.25, 0.85, P3, g)
        pts = a + [(0.25, P3)] + b + [(0.85, 0.08)]
        line_arrow(f, M, a); line_arrow(f, M, [(0.25, a[-1][1]), (0.25, P3)]); line_arrow(f, M, b)
        line_arrow(f, M, [(0.85, b[-1][1]), (0.85, 0.08)])
        lab = {"1": (0.85, 0.08, 2, -3), "2": (0.25, a[-1][1], -4.5, 0), "3": (0.25, P3, -4.5, 0), "4": (0.85, b[-1][1], 2, 0)}
    elif kind == "diesel":
        a = pv_curve(0.85, 0.2, 0.08, g)
        P2 = a[-1][1]
        V3 = 0.38
        b = pv_curve(V3, 0.85, P2, g)
        line_arrow(f, M, a); line_arrow(f, M, [(0.2, P2), (V3, P2)]); line_arrow(f, M, b)
        line_arrow(f, M, [(0.85, b[-1][1]), (0.85, 0.08)])
        lab = {"1": (0.85, 0.08, 2, -3), "2": (0.2, P2, -4.5, 0.5), "3": (V3, P2, 0.5, 2.5), "4": (0.85, b[-1][1], 2, 0)}
    elif kind == "carnot":
        gg = 2.0                                      # exaggerated, schematic (not to scale)
        V1, P1 = 0.12, 0.9
        V2 = 0.3
        c1 = P1 * V1
        P2 = c1 / V2
        K = P2 * V2 ** gg
        c2 = 0.05
        V3 = K / c2 ** 1 * 1.0 if False else (K / c2) ** (1 / (gg - 1))
        P3 = c2 / V3
        K1 = P1 * V1 ** gg
        V4 = (K1 / c2) ** (1 / (gg - 1))
        P4 = c2 / V4
        iso1 = sample(lambda t: (V1 + (V2 - V1) * t, c1 / (V1 + (V2 - V1) * t)), 0, 1)
        ad1 = [(V2 + (V3 - V2) * i / 40, K / (V2 + (V3 - V2) * i / 40) ** gg) for i in range(41)]
        iso2 = sample(lambda t: (V3 + (V4 - V3) * t, c2 / (V3 + (V4 - V3) * t)), 0, 1)
        ad2 = [(V4 + (V1 - V4) * i / 40, K1 / (V4 + (V1 - V4) * i / 40) ** gg) for i in range(41)]
        for s_ in (iso1, ad1, iso2, ad2):
            line_arrow(f, M, s_)
        lab = {"1": (V1, P1, -4.5, 0), "2": (V2, P2, 2, 1.5), "3": (V3, P3, 1.5, 1.5), "4": (V4, P4, -4.5, -3)}
    elif kind == "rankine":
        Vp = 0.05
        line_arrow(f, M, [(Vp, 0.113), (Vp, 0.6)], mid_arrow=True)
        line_arrow(f, M, [(Vp, 0.6), (0.28, 0.6)])
        e = sample(lambda t: (0.28 + 0.57 * t, 0.6 * (0.28 / (0.28 + 0.57 * t)) ** 1.5), 0, 1)
        line_arrow(f, M, e)
        line_arrow(f, M, [(0.85, 0.113), (Vp, 0.113)])
        lab = {"1": (Vp, 0.113, -4.5, -3), "2": (Vp, 0.6, -4.5, 1), "3": (0.28, 0.6, 0.5, 2.5), "4": (0.85, 0.113, 1.8, 1.5)}
    for k, (u, v, dx, dy) in lab.items():
        pt(f, M, u, v, k, dx=dx, dy=dy)


def cycle_ts(f, M, kind):
    if kind in ("otto", "diesel"):
        k_v, k_p = 2.4, 1.2
        if kind == "otto":
            s1, s2 = 0.25, 0.65
            T1, T2, T3 = 0.18, 0.4, 0.85
            # 1-2 isentropic (vertical), 2-3 const V (curve up), 3-4 isentropic (down), 4-1 const V
            line_arrow(f, M, [(s1, T1), (s1, T2)])
            c23 = sample(lambda t: (s1 + (s2 - s1) * t, expc(t, T2, T3, k_v)), 0, 1)
            line_arrow(f, M, c23)
            T4 = 0.38
            line_arrow(f, M, [(s2, T3), (s2, T4)])
            c41 = sample(lambda t: (s2 + (s1 - s2) * t, expc(1 - t, T1, T4, k_v)), 0, 1)
            line_arrow(f, M, c41)
            lab = {"1": (s1, T1, -4.5, -1), "2": (s1, T2, -4.5, 0), "3": (s2, T3, 1.5, 1), "4": (s2, T4, 1.8, -1)}
        else:
            s1, s3 = 0.25, 0.55
            T1, T2 = 0.18, 0.42
            line_arrow(f, M, [(s1, T1), (s1, T2)])
            c23 = sample(lambda t: (s1 + (s3 - s1) * t, expc(t, T2, 0.82, 1.2)), 0, 1)
            line_arrow(f, M, c23)
            s4 = 0.78
            T4 = 0.4
            line_arrow(f, M, [(s4, 0.82 - 0.0), (s4, T4)]) if False else None
            c34 = [(s3 + (s4 - s3) * 0 + 0, 0.82), (s4, 0.82)]
            # 3-4 isentropic: vertical down from 3 to T4 at s3 ... (4 sits at the same s as 3) -> use s4 = s3
            line_arrow(f, M, [(s3, 0.82), (s3, 0.40)]) if False else None
            lab = None
            return cycle_ts_diesel(f, M)
    elif kind == "carnot":
        line_arrow(f, M, [(0.2, 0.78), (0.8, 0.78)])
        line_arrow(f, M, [(0.8, 0.78), (0.8, 0.28)])
        line_arrow(f, M, [(0.8, 0.28), (0.2, 0.28)])
        line_arrow(f, M, [(0.2, 0.28), (0.2, 0.78)])
        lab = {"1": (0.2, 0.78, -4.5, 1), "2": (0.8, 0.78, 1.5, 1), "3": (0.8, 0.28, 1.5, -2), "4": (0.2, 0.28, -4.5, -2)}
        f.text(*M(0.5, 0.84), "T₁ (source)", size=6.5)
        f.text(*M(0.5, 0.20), "T₂ (sink)", size=6.5)
    elif kind == "rankine":
        pts_l = [dome(0.12 + 0.78 * i / 40)[0:1] + (0.12 + 0.78 * i / 40,) for i in range(41)]
        pts_v = [(dome(0.12 + 0.78 * i / 40)[1], 0.12 + 0.78 * i / 40) for i in range(41)]
        f.pline([M(*p) for p in pts_l], w=THIN + 0.2, col=GREY)
        f.pline([M(*p) for p in pts_v], w=THIN + 0.2, col=GREY)
        Tc, Tb = 0.25, 0.65
        s1 = dome(Tc)[0]
        line_arrow(f, M, [(s1, Tc), (s1 + 0.01, Tc + 0.04)], mid_arrow=False)
        heat = sample(lambda t: (dome(Tc + 0.04 + (Tb - Tc - 0.04) * t)[0] + 0.01, Tc + 0.04 + (Tb - Tc - 0.04) * t), 0, 1, 24)
        line_arrow(f, M, heat)
        sa, sb = dome(Tb)
        line_arrow(f, M, [(sa, Tb), (sb, Tb)])
        sup = sample(lambda t: (sb + (0.74 - sb) * t, expc(t, Tb, 0.8, 1.0)), 0, 1)
        line_arrow(f, M, sup)
        line_arrow(f, M, [(0.74, 0.8), (0.74, Tc)])
        line_arrow(f, M, [(0.74, Tc), (s1, Tc)])
        lab = {"1": (s1, Tc, -4.5, -2), "2": (s1 + 0.01, Tc + 0.04, -5, 1), "3": (0.74, 0.8, 1.5, 1), "4": (0.74, Tc, 1.5, -2)}
        f.text(*M(0.48, 0.95), "critical point", size=5.8)
        f.text(*M(0.5, 0.33 + 0.0), "wet region", size=5.8)
    for k, (u, v, dx, dy) in lab.items():
        pt(f, M, u, v, k, dx=dx, dy=dy)


def cycle_ts_diesel(f, M):
    s1, s3 = 0.25, 0.55
    T1, T2, T3 = 0.18, 0.42, 0.82
    line_arrow(f, M, [(s1, T1), (s1, T2)])
    line_arrow(f, M, sample(lambda t: (s1 + (s3 - s1) * t, expc(t, T2, T3, 1.2)), 0, 1))
    T4 = 0.45
    line_arrow(f, M, [(s3, T3), (s3 + 0.15, T4)]) if False else None
    s4 = 0.75
    line_arrow(f, M, [(s4, T3 - 0.0), (s4, T4)]) if False else None
    # 3-4 isentropic expansion is vertical at s3 in an ideal T-S; use s4 = s3 + 0.0
    line_arrow(f, M, [(s3, T3), (s3, T4)])
    # 4-1 constant volume: curve back to 1
    line_arrow(f, M, sample(lambda t: (s3 + (s1 - s3) * t, expc(1 - t, T1, T4, 2.4)), 0, 1))
    for k, (u, v, dx, dy) in {"1": (s1, T1, -4.5, -1), "2": (s1, T2, -4.5, 0), "3": (s3, T3, 1.5, 1), "4": (s3, T4, 1.8, -1)}.items():
        pt(f, M, u, v, k, dx=dx, dy=dy)


NAMES = {
    "otto": ("Otto cycle", ["1-2 Isentropic compression", "2-3 Heat added at constant volume", "3-4 Isentropic expansion", "4-1 Heat rejected at constant volume"]),
    "diesel": ("Diesel cycle", ["1-2 Isentropic compression", "2-3 Heat added at constant pressure", "3-4 Isentropic expansion", "4-1 Heat rejected at constant volume"]),
    "carnot": ("Carnot cycle", ["1-2 Isothermal expansion (heat added)", "2-3 Isentropic expansion", "3-4 Isothermal compression (heat rejected)", "4-1 Isentropic compression"]),
    "rankine": ("Rankine cycle", ["1-2 Pump work (isentropic)", "2-3 Heat added in boiler (constant p)", "3-4 Isentropic expansion in turbine", "4-1 Condensation (constant p, T)"]),
}


@fig("te_cycle")
def te_cycle(kind="otto", legend=True):
    f = Fig(165, 62 if legend else 50, 1.0)
    W, H = 56, 34
    y0 = 20 if legend else 8
    M1 = plot(f, 20, y0, W, H, "V", "p", f"{NAMES[kind][0]}  P-V")
    cycle_pv(f, M1, kind)
    M2 = plot(f, 100, y0, W, H, "s", "T", f"{NAMES[kind][0]}  T-S")
    cycle_ts(f, M2, kind)
    if legend:
        for i, t in enumerate(NAMES[kind][1]):
            f.text(8 + (i % 2) * 80, 11 - (i // 2) * 6, t, size=6.6, anchor="start")
    return f.d


@fig("te_otto_diesel")
def te_otto_diesel():
    f = Fig(165, 112, 1.0)
    W, H = 56, 34
    for row, kind in enumerate(("otto", "diesel")):
        y0 = 66 - row * 56
        M1 = plot(f, 20, y0, W, H, "V", "p", f"{NAMES[kind][0]}  P-V")
        cycle_pv(f, M1, kind)
        M2 = plot(f, 100, y0, W, H, "s", "T", f"{NAMES[kind][0]}  T-S")
        cycle_ts(f, M2, kind)
    return f.d


@fig("te_boyle_charles")
def te_boyle_charles():
    f = Fig(165, 52, 1.0)
    W, H = 56, 34
    M = plot(f, 20, 8, W, H, "V", "p", "Boyle's law (T constant)")
    f.pline([M(*p) for p in sample(lambda t: (0.2 + 0.65 * t, 0.16 / (0.2 + 0.65 * t) + 0.05), 0, 1)], w=MED)
    f.text(*M(0.6, 0.62), "p V = constant", size=6.8)
    M = plot(f, 100, 8, W, H, "T (K)", "V", "Charles' law (p constant)")
    f.line(*M(0.0, 0.0), *M(0.9, 0.8), w=MED)
    f.text(*M(0.45, 0.62), "V / T = constant", size=6.8)
    return f.d


@fig("te_blocks")
def te_blocks(which="all"):
    """Heat engine, refrigerator and heat pump block diagrams."""
    f = Fig(165, 68 if which == "all" else 68, 1.0)

    def block(ox, title, hot, cold, kind):
        f.rect(ox + 7, 54, 36, 8, fill=LIGHT)
        f.text(ox + 25, 56.3, hot, size=7)
        f.rect(ox + 7, 4, 36, 8, fill=LIGHT)
        f.text(ox + 25, 6.3, cold, size=7)
        f.circle(ox + 25, 33, 8)
        f.text(ox + 25, 32, {"engine": "Engine", "ref": "Refrig.", "hp": "H.P."}[kind], size=6.2)
        f.text(ox + 25, 66, title, bold=True, size=7.5)
        if kind == "engine":
            f.arrow(ox + 20, 54, ox + 20, 41); f.text(ox + 16, 47, "Q₁", size=7, anchor="end")
            f.arrow(ox + 20, 25, ox + 20, 12); f.text(ox + 16, 18, "Q₂", size=7, anchor="end")
            f.arrow(ox + 33, 33, ox + 47, 33); f.text(ox + 40, 35, "W", size=7)
        else:
            f.arrow(ox + 20, 12, ox + 20, 25); f.text(ox + 16, 18, "Q₂", size=7, anchor="end")
            f.arrow(ox + 20, 41, ox + 20, 54); f.text(ox + 16, 47, "Q₁", size=7, anchor="end")
            f.arrow(ox + 47, 33, ox + 33, 33); f.text(ox + 40, 35, "W", size=7)

    block(0, "Heat engine", "Source (T₁)", "Sink (T₂)", "engine")
    block(55, "Refrigerator", "Surroundings (T₁)", "Cold space (T₂)", "ref")
    block(110, "Heat pump", "Room to be heated (T₁)", "Atmosphere (T₂)", "hp")
    return f.d


@fig("te_blocks_rhp")
def te_blocks_rhp():
    f = Fig(110, 68, 1.0)
    for ox, title, hot, cold, k in ((0, "Refrigerator", "Surroundings (T₁)", "Cold space (T₂)", "ref"), (55, "Heat pump", "Room (T₁)", "Atmosphere (T₂)", "hp")):
        f.rect(ox + 7, 54, 36, 8, fill=LIGHT); f.text(ox + 25, 56.3, hot, size=7)
        f.rect(ox + 7, 4, 36, 8, fill=LIGHT); f.text(ox + 25, 6.3, cold, size=7)
        f.circle(ox + 25, 33, 8)
        f.text(ox + 25, 32, "Refrig." if k == "ref" else "H.P.", size=6.2)
        f.text(ox + 25, 66, title, bold=True, size=7.5)
        f.arrow(ox + 20, 12, ox + 20, 25); f.text(ox + 16, 18, "Q₂", size=7, anchor="end")
        f.arrow(ox + 20, 41, ox + 20, 54); f.text(ox + 16, 47, "Q₁", size=7, anchor="end")
        f.arrow(ox + 47, 33, ox + 33, 33); f.text(ox + 40, 35, "W", size=7)
    return f.d


@fig("te_flow_work")
def te_flow_work():
    f = Fig(165, 56, 1.0)
    # pipe
    f.rect(10, 14, 100, 26, fill=None)
    f.rect(10, 14, 40, 26, fill=LIGHT)
    f.text(30, 25, "Fluid element", size=7); f.text(30, 20, "volume V", size=7)
    f.line(50, 14, 50, 40, w=0.8, dash=HIDDEN)
    f.text(80, 30, "System", size=8, bold=True); f.text(80, 24.5, "(control volume)", size=7)
    f.arrow(2, 27, 10, 27, w=1.0)
    f.text(1, 31, "p", size=8, anchor="start", bold=True)
    f.dim_h(10, 50, 14, "L", off=-5, ext_from=(14, 14), size=7)
    f.text(10, 44, "Cross-section A", size=7, anchor="start")
    f.text(125, 40, "Force on the element  F = p × A", size=7.2, anchor="start")
    f.text(125, 33, "Distance moved        = L", size=7.2, anchor="start")
    f.text(125, 26, "Flow work = F × L = p A L", size=7.2, anchor="start")
    f.text(125, 19, "           = p V", size=7.2, anchor="start", bold=True)
    return f.d


@fig("te_th_chart")
def te_th_chart():
    f = Fig(165, 78, 1.0)
    ox, oy, W, H = 22, 12, 124, 58
    axes(f, ox, oy, W, H, "Enthalpy h", "Temperature t")
    # points
    h0, hf, hg = 0.08, 0.34, 0.66
    ts = 0.46
    def M(u, v): return (ox + u * W, oy + v * H)
    f.pline([M(h0, 0.08), M(hf, ts)], w=1.0)
    f.pline([M(hf, ts), M(hg, ts)], w=1.0)
    sup = sample(lambda t: (hg + 0.26 * t, ts + 0.42 * t - 0.05 * t * t), 0, 1)
    f.pline([M(*p) for p in sup], w=1.0)
    for u, v, s, dx, dy in ((hf, ts, "A  (saturated water)", -2, 2.0), (hg, ts, "B  (dry saturated steam)", 2, -4)):
        pass
    for u in (hf, hg):
        f.line(*M(u, 0), *M(u, ts), w=THIN, dash=HIDDEN)
    f.line(*M(0, ts), *M(hf, ts), w=THIN, dash=HIDDEN)
    f.text(ox - 2, oy + ts * H - 1, "t_{s}".replace("_{s}", "ₛ"), anchor="end", size=8, bold=True)
    f.text(*M(hf, -0.07), "h_f", anchor="middle", size=7.5, bold=True)
    f.text(*M(hg, -0.07), "h_g", anchor="middle", size=7.5, bold=True)
    f.dim_h(M(hf, 0)[0], M(hg, 0)[0], oy + 6, "h_fg (latent heat)", off=0, size=6.8)
    f.text(*M(0.20, 0.30), "Sensible heating", size=6.8, rot=0)
    f.text(*M(0.20, 0.25), "of water (0→1)", size=6.8)
    f.text(*M(0.50, ts + 0.06), "Wet steam (evaporation at t_s)".replace("t_s", "tₛ"), size=6.8)
    f.text(*M(0.74, 0.90), "Superheated steam", size=6.8)
    f.text(*M(0.74, 0.84), "(heating of vapour, 2→3)", size=6.3)
    f.text(*M(0.03, -0.07), "water at 0°C", size=6.3, anchor="start")
    for (u, v, nm, dx, dy) in ((h0, 0.08, "0", -2, -2), (hf, ts, "1", -4, 1.5), (hg, ts, "2", 1.5, -4), (hg + 0.26, ts + 0.37, "3", 1.5, 0)):
        pt(f, M, u, v, nm, dx=dx, dy=dy)
    f.text(*M(0.20, 0.54), "sub-cooled water", size=6.3)
    return f.d
