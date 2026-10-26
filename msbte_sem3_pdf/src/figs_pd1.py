"""Production Drawing figures, part 1: conventions and symbols."""
import math
from draw import *
from figreg import fig


def title(f, x, y, s):
    f.text(x, y, s, size=7, bold=True)


# ---------- small symbol drawers (each fits roughly in a 8 x 8 mm box centred at x, y) ----------
def gt_symbol(f, name, x, y, r=3.2, w=0.9):
    if name == "circularity":
        f.circle(x, y, r * 0.8, w=w)
    elif name == "symmetry":
        f.line(x - r * 0.8, y + r * 0.6, x + r * 0.8, y + r * 0.6, w=w); f.line(x - r, y, x + r, y, w=w); f.line(x - r * 0.8, y - r * 0.6, x + r * 0.8, y - r * 0.6, w=w)
    elif name == "angularity":
        f.line(x - r, y - r * 0.7, x + r, y - r * 0.7, w=w); f.line(x - r, y - r * 0.7, x + r * 0.5, y + r * 0.9, w=w)
    elif name == "concentricity":
        f.circle(x, y, r * 0.85, w=w); f.circle(x, y, r * 0.45, w=w)
    elif name == "flatness":
        f.pline([(x - r, y - r * 0.5), (x + r * 0.5, y - r * 0.5), (x + r, y + r * 0.5), (x - r * 0.5, y + r * 0.5)], closed=True, w=w)
    elif name == "parallelism":
        f.line(x - r * 0.6, y - r * 0.8, x + r * 0.2, y + r * 0.8, w=w); f.line(x - r * 0.1, y - r * 0.8, x + r * 0.7, y + r * 0.8, w=w)
    elif name == "perpendicularity":
        f.line(x - r, y - r * 0.8, x + r, y - r * 0.8, w=w); f.line(x, y - r * 0.8, x, y + r * 0.9, w=w)
    elif name == "straightness":
        f.line(x - r, y, x + r, y, w=w + 0.3)
    elif name == "cylindricity":
        f.circle(x, y, r * 0.7, w=w); f.line(x - r * 1.1, y - r * 0.5, x - r * 0.4, y + r * 0.5, w=w * 0.8); f.line(x + r * 0.4, y - r * 0.5, x + r * 1.1, y + r * 0.5, w=w * 0.8)


def frame_cell(f, x, y, name, label, w=9):
    f.rect(x, y, w, w, lw=0.8)
    gt_symbol(f, name, x + w / 2, y + w / 2)
    f.text(x + w + 2, y + w / 2 - 1.2, label, size=7, anchor="start")


@fig("pd_gt_symbols")
def pd_gt_symbols(names=("circularity", "symmetry")):
    f = Fig(165, 18 if len(names) <= 3 else 26, 1.0)
    for i, n in enumerate(names):
        cx = 5 + (i % 4) * 40
        cy = (f.h - 12) - (i // 4) * 14
        frame_cell(f, cx, cy, n, n.capitalize())
    return f.d


def surface_symbol(f, x, y, top=None, low=None, method=None, sampling=None, h=9.0):
    """Machining (surface texture) symbol with its tip at (x, y) on the surface line."""
    f.line(x, y, x - h * 0.36, y + h, w=0.9)                  # short left leg
    f.line(x, y, x + h * 0.72, y + 2 * h, w=0.9)              # long right leg
    f.line(x - h * 0.36, y + h, x + h * 0.36, y + h, w=0.9)   # horizontal bar (meets the long leg)
    xr = x + h * 0.72
    f.line(xr, y + 2 * h, xr + 22, y + 2 * h, w=0.9)          # extension line
    if top is not None:
        f.text(x, y + h + 1.0, str(top), size=7)
    if low is not None:
        f.text(x - h * 0.36 - 1.2, y + h * 0.35, str(low), size=7, anchor="end")
    if method:
        f.text(xr + 2, y + 2 * h + 1.0, method, size=7, anchor="start")
    if sampling is not None:
        f.text(xr + 2, y + 2 * h - 4.2, str(sampling), size=7, anchor="start")
    f.line(x - 16, y, x + 16, y, w=0.9)
    for i in range(-16, 16, 2):
        f.line(x + i, y, x + i - 1.6, y - 2.2, w=0.4)


@fig("pd_surface_meaning")
def pd_surface_meaning(top="0.8", low="0.5", method="Grinding", sampling="2"):
    f = Fig(165, 46, 1.0)
    surface_symbol(f, 30, 6, top, low, method, sampling)
    items = [(f"{top}", "upper limit (maximum) of surface roughness Ra, in μm  [on the bar]"),
             (f"{low}", "lower limit (minimum) of surface roughness Ra, in μm  [left of the symbol]"),
             (f"{method}", "production (machining) method  [above the extension line]"),
             (f"{sampling}", "sampling length / cut-off in mm  [below the extension line]")]
    for i, (a_, b_) in enumerate(items):
        f.text(84, 38 - i * 8, a_, size=7.5, bold=True, anchor="end")
        f.text(86, 38 - i * 8, "=  " + b_, size=7, anchor="start")
    return f.d


@fig("pd_lay_radial")
def pd_lay_radial():
    f = Fig(165, 40, 1.0)
    surface_symbol(f, 30, 8)
    f.text(45, 21, "R", size=8, bold=True, anchor="start")
    f.text(60, 21, "= direction of lay approximately radial to the centre of the surface", size=7, anchor="start")
    # example face
    f.circle(120, 14, 10, w=0.9)
    for a in range(0, 360, 30):
        f.line(120 + 3 * math.cos(math.radians(a)), 14 + 3 * math.sin(math.radians(a)), 120 + 9.6 * math.cos(math.radians(a)), 14 + 9.6 * math.sin(math.radians(a)), w=0.4)
    f.text(120, 1, "tool marks run radially", size=6.4)
    return f.d


@fig("pd_taper")
def pd_taper(D=40.0, L=110.0, k=10):
    d = D - L / k
    f = Fig(165, 62, 1.0)
    s = 0.85
    ox, cy = 14, 28
    X = lambda x: ox + x * s
    f.pline([(X(0), cy + D / 2), (X(L), cy + d / 2), (X(L), cy - d / 2), (X(0), cy - D / 2)], closed=True, w=1.2)
    f.center_h(X(0), X(L), cy, 4)
    f.dim_h(X(0), X(L), cy - D / 2, f"L = {L:g}", off=-8, ext_from=(cy - D / 2, cy - d / 2))
    f.dim_v(cy - D / 2, cy + D / 2, X(0), f"Ø{D:g}", off=-6, ext_from=(X(0), X(0)))
    f.dim_v(cy - d / 2, cy + d / 2, X(L), f"Ø{d:g}", off=6, ext_from=(X(L), X(L)))
    # taper symbol with ratio
    f.line(X(L / 2) - 10, cy + D / 2 + 9, X(L / 2) + 10, cy + D / 2 + 9, w=0.4)
    f.pline([(X(L / 2) - 8, cy + D / 2 + 11), (X(L / 2) - 8, cy + D / 2 + 17), (X(L / 2) - 14, cy + D / 2 + 11)], closed=True, w=0.8)
    f.text(X(L / 2) - 4, cy + D / 2 + 12, f"1 : {k}", size=8, anchor="start", bold=True)
    f.text(X(L / 2) + 14, cy + D / 2 + 3, "(taper symbol points towards the small end)", size=6, anchor="start") if False else None
    f.text(120, 10, f"Taper = (D − d)/L = 1/{k}", size=7, anchor="start")
    f.text(120, 5, f"d = D − L/{k} = {D:g} − {L:g}/{k} = {d:g} mm", size=7, anchor="start")
    return f.d


@fig("pd_knurl")
def pd_knurl():
    f = Fig(165, 40, 1.0)
    ox, cy = 20, 18
    f.rect(ox, cy - 8, 60, 16, lw=1.2)
    reg = [(ox + 15, cy - 8), (ox + 45, cy - 8), (ox + 45, cy + 8), (ox + 15, cy + 8)]
    f.hatch([reg], gap=2.6, angle=45, w=0.4)
    f.hatch([reg], gap=2.6, angle=-45, w=0.4)
    f.center_h(ox, ox + 60, cy, 4)
    f.text(ox + 30, cy + 14, "Diamond knurling (conventional)", size=7)
    f.text(120, cy + 1, "Two sets of thin lines at 45°", size=6.6, anchor="start"); f.text(120, cy - 4, "crossing each other,", size=6.6, anchor="start"); f.text(120, cy - 9, "drawn over the knurled part", size=6.6, anchor="start")
    return f.d


@fig("pd_spline")
def pd_spline():
    f = Fig(165, 52, 1.0)
    ox, cy = 14, 24
    f.rect(ox, cy - 10, 70, 20, lw=1.2) if False else None
    f.line(ox, cy + 10, ox + 70, cy + 10, w=1.2); f.line(ox, cy - 10, ox + 70, cy - 10, w=1.2)
    f.line(ox, cy + 8, ox + 56, cy + 8, w=0.4); f.line(ox, cy - 8, ox + 56, cy - 8, w=0.4)
    f.line(ox + 56, cy + 8, ox + 56, cy - 8, w=0.4)
    f.pline([(ox + 70, cy + 10), (ox + 68, cy + 6), (ox + 72, cy + 2), (ox + 68, cy - 2), (ox + 72, cy - 6), (ox + 70, cy - 10)], w=0.9)
    f.center_h(ox, ox + 70, cy, 4)
    f.text(ox + 30, cy + 15, "Splined shaft – front view", size=7)
    # end view
    cx = 125
    f.circle(cx, cy, 8, w=0.4)
    for i in range(6):
        a = math.radians(60 * i)
        for da in (-9, 9):
            pass
    pts = []
    for i in range(6):
        a0 = math.radians(60 * i - 12); a1 = math.radians(60 * i + 12); a2 = math.radians(60 * i + 30); a3 = math.radians(60 * i + 48)
        pts += [(cx + 10 * math.cos(a0), cy + 10 * math.sin(a0)), (cx + 10 * math.cos(a1), cy + 10 * math.sin(a1)),
                (cx + 8 * math.cos(a1), cy + 8 * math.sin(a1)), (cx + 8 * math.cos(a3 - 24 + 24 - 12 + 12 + 0), cy + 8 * math.sin(a3 - 24 + 24))] if False else []
    f.circle(cx, cy, 10, w=1.2)
    f.circle(cx, cy, 8, w=0.4, dash=HIDDEN) if False else None
    for i in range(6):
        a = math.radians(60 * i + 30)
        f.line(cx + 8 * math.cos(a), cy + 8 * math.sin(a), cx + 10 * math.cos(a), cy + 10 * math.sin(a), w=0.4)
    f.circle(cx, cy, 8, w=0.4)
    f.text(cx, cy - 16, "End view", size=7)
    return f.d


@fig("pd_pipe_breaks")
def pd_pipe_breaks(which="both"):
    f = Fig(165, 56, 1.0)
    # short break: pipe with curved break
    def pipe(ox, oy, L, kind):
        f.line(ox, oy + 7, ox + L, oy + 7, w=1.2); f.line(ox, oy - 7, ox + L, oy - 7, w=1.2)
        if kind == "short":
            for xx in (ox, ox + L):
                f.pline(f.arc_pts(xx, oy, 3.5, -90 if xx == ox else 90, 90 if xx == ox else 270, 16, ry=7), w=1.0) if False else None
            f.pline([(ox, oy + 7), (ox - 3, oy + 3), (ox + 3, oy - 3), (ox, oy - 7)], w=1.0)
            f.pline([(ox + L, oy + 7), (ox + L - 3, oy + 3), (ox + L + 3, oy - 3), (ox + L, oy - 7)], w=1.0)
        else:
            f.pline([(ox, oy + 7), (ox, oy - 7)], w=0.0)
        f.center_h(ox, ox + L, oy, 4)
    pipe(14, 40, 60, "short")
    f.text(44, 28, "Short break in pipe", size=7)
    # long break: pipe cut by two thin zig-zag lines, middle part omitted
    ox, oy = 14, 12
    f.line(ox, oy + 7, ox + 26, oy + 7, w=1.2); f.line(ox, oy - 7, ox + 26, oy - 7, w=1.2)
    f.line(ox + 54, oy + 7, ox + 80, oy + 7, w=1.2); f.line(ox + 54, oy - 7, ox + 80, oy - 7, w=1.2)
    for xz in (ox + 26, ox + 54):
        f.pline([(xz, oy + 7), (xz - 2, oy + 3), (xz + 2, oy), (xz - 2, oy - 3), (xz, oy - 7)], w=0.6)
    f.line(ox + 26, oy + 7, ox + 54, oy + 7, w=0.35, dash=HIDDEN)
    f.line(ox + 26, oy - 7, ox + 54, oy - 7, w=0.35, dash=HIDDEN)
    f.center_h(ox, ox + 80, oy, 4)
    f.text(ox + 40, oy - 14, "Long break in pipe", size=7)
    f.text(120, 40, "Pipe shown broken at both", size=6.6, anchor="start"); f.text(120, 35, "ends with S-shaped lines;", size=6.6, anchor="start"); f.text(120, 30, "long break uses thin zig-zag", size=6.6, anchor="start"); f.text(120, 25, "lines (free-hand).", size=6.6, anchor="start")
    return f.d


@fig("pd_i_section_break")
def pd_i_section_break():
    f = Fig(165, 50, 1.0)
    cx, cy = 28, 24
    # I-section end view
    f.pline([(cx - 10, cy + 14), (cx + 10, cy + 14), (cx + 10, cy + 10), (cx + 2, cy + 10), (cx + 2, cy - 10), (cx + 10, cy - 10), (cx + 10, cy - 14), (cx - 10, cy - 14), (cx - 10, cy - 10), (cx - 2, cy - 10), (cx - 2, cy + 10), (cx - 10, cy + 10)], closed=True, w=1.2)
    f.text(cx, cy - 22, "I-section (end view)", size=7)
    # front view with break
    ox = 70
    f.line(ox, cy + 14, ox + 70, cy + 14, w=1.2); f.line(ox, cy - 14, ox + 70, cy - 14, w=1.2)
    f.line(ox, cy + 10, ox + 24, cy + 10, w=0.4); f.line(ox, cy - 10, ox + 24, cy - 10, w=0.4)
    f.line(ox + 46, cy + 10, ox + 70, cy + 10, w=0.4); f.line(ox + 46, cy - 10, ox + 70, cy - 10, w=0.4)
    f.pline([(ox + 24, cy + 14), (ox + 27, cy + 7), (ox + 22, cy), (ox + 27, cy - 7), (ox + 24, cy - 14)], w=0.9)
    f.pline([(ox + 46, cy + 14), (ox + 49, cy + 7), (ox + 44, cy), (ox + 49, cy - 7), (ox + 46, cy - 14)], w=0.9)
    f.text(ox + 35, cy - 22, "Break shown with wavy free-hand lines", size=6.6)
    return f.d


@fig("pd_gate_globe")
def pd_gate_globe(which="gate"):
    f = Fig(165, 44, 1.0)
    def valve(cx, kind):
        cy = 16
        f.line(cx - 22, cy, cx - 8, cy, w=1.2); f.line(cx + 8, cy, cx + 22, cy, w=1.2)
        f.pline([(cx - 8, cy + 6), (cx, cy), (cx - 8, cy - 6)], closed=True, w=1.2)
        f.pline([(cx + 8, cy + 6), (cx, cy), (cx + 8, cy - 6)], closed=True, w=1.2)
        f.line(cx, cy, cx, cy + 16, w=1.0)
        f.line(cx - 5, cy + 16, cx + 5, cy + 16, w=1.4)
        if kind == "globe":
            f.circle(cx, cy, 1.8, fill=BLACK)
        f.text(cx, cy - 12, "Gate valve" if kind == "gate" else "Globe valve", size=7, bold=True)
    if which in ("gate", "both"):
        valve(40, "gate")
    if which in ("globe", "both"):
        valve(125 if which == "both" else 40, "globe")
    return f.d


@fig("pd_tolerance_sketch")
def pd_tolerance_sketch():
    f = Fig(165, 74, 1.0)
    ox = 20
    f.line(ox - 10, 36, ox + 85, 36, w=1.0, dash=CHAIN)
    f.text(ox - 11, 37.5, "Zero line (basic size)", size=6.8, anchor="start")
    f.rect(ox + 20, 44, 40, 12, lw=1.0, fill=LIGHT) if False else None
    # tolerance zone above the zero line (positive deviations) to show general case
    f.rect(ox + 30, 41, 24, 10, lw=1.2, fill=LIGHT)
    f.text(ox + 42, 44.5, "Tolerance zone", size=6.8)
    f.line(ox + 20, 51, ox + 62, 51, w=0.4, dash=HIDDEN); f.line(ox + 20, 41, ox + 62, 41, w=0.4, dash=HIDDEN)
    f.dim_v(36, 51, ox + 62, "Upper dev.", off=0, size=6.4)
    f.dim_v(36, 41, ox + 74, "Lower dev.", off=0, size=6.4)
    f.dim_v(41, 51, ox + 20, "Tolerance", off=0, size=6.8)
    f.text(ox + 80, 50, "Max. limit of size", size=6.2, anchor="start"); f.text(ox + 80, 40, "Min. limit of size", size=6.2, anchor="start")
    f.text(ox - 10, 20, "Basic size = nominal size, measured up to the zero line.", size=6.8, anchor="start")
    f.text(ox - 10, 15, "Upper deviation = max. limit − basic size;  Lower deviation = min. limit − basic size.", size=6.8, anchor="start")
    f.text(ox - 10, 10, "Tolerance = max. limit − min. limit = upper deviation − lower deviation.", size=6.8, anchor="start")
    f.text(ox - 10, 3, "(Here both deviations are drawn above the zero line as an example.)", size=6.2, anchor="start")
    return f.d


@fig("pd_materials")
def pd_materials(which=("copper", "rubber", "glass", "marble")):
    n = len(which)
    f = Fig(165, 40, 1.0)
    wd, ht = 30, 20
    gap = (165 - n * wd) / (n + 1)
    for i, m in enumerate(which):
        x = gap + i * (wd + gap)
        y = 12
        f.rect(x, y, wd, ht, lw=1.0)
        reg = [(x, y), (x + wd, y), (x + wd, y + ht), (x, y + ht)]
        if m == "copper":
            f.hatch([reg], gap=3.0, angle=45, w=0.8)
            f.hatch([reg], gap=3.0, angle=45, w=0.2) if False else None
        elif m == "cast iron":
            f.hatch([reg], gap=1.8, angle=45, w=0.35)
        elif m == "rubber":
            f.hatch([reg], gap=0.9, angle=45, w=0.9)
        elif m == "glass":
            f.hatch([reg], gap=3.4, angle=45, w=0.3)
            f.hatch([reg], gap=3.4, angle=-45, w=0.3) if False else None
            for k in range(3):
                f.line(x + 4, y + 4 + k * 6, x + 8, y + 4 + k * 6, w=0.3)
        elif m == "marble":
            for k in range(1, 4):
                f.line(x, y + k * ht / 4, x + wd, y + k * ht / 4, w=0.3)
            for r_ in range(4):
                off = 0 if r_ % 2 == 0 else wd / 6
                for xv in range(0, 7):
                    xx = x + off + xv * wd / 3
                    if x < xx < x + wd:
                        f.line(xx, y + r_ * ht / 4, xx, y + (r_ + 1) * ht / 4, w=0.3)
        f.text(x + wd / 2, y - 6, m.capitalize(), size=7, bold=True)
    return f.d


@fig("pd_holes_pcd")
def pd_holes_pcd():
    f = Fig(165, 52, 1.0)
    cx, cy, R = 30, 26, 16
    f.circle(cx, cy, 22, w=1.2)
    f.circle(cx, cy, R, w=0.35, dash=CHAIN)
    for i in range(6):
        a = math.radians(60 * i + 30)
        f.circle(cx + R * math.cos(a), cy + R * math.sin(a), 3.2, w=1.0)
        f.center_mark(cx + R * math.cos(a), cy + R * math.sin(a), 4.6)
    f.center_mark(cx, cy, 25)
    f.leader(cx + R * math.cos(math.radians(150)) * 0.0 + 0, cy + R, 70, 46, "PCD (pitch circle diameter) – thin chain line")
    f.leader(cx + R * math.cos(math.radians(30)) + 2, cy + R * math.sin(math.radians(30)) + 2, 70, 38, "holes equally spaced on the pitch circle")
    f.text(70, 28, "Indicate:  6 holes Ø__ on PCD __ (equispaced)", size=6.8, anchor="start")
    return f.d


@fig("pd_bearings")
def pd_bearings():
    f = Fig(165, 60, 1.0)
    # sectional detail of ball bearing
    ox, oy = 12, 12
    f.rect(ox, oy, 8, 8 + 20 + 0, lw=1.0) if False else None
    f.rect(ox + 4, oy + 26, 30, 4, lw=1.0, fill=LIGHT) if False else None
    f.rect(ox, oy + 22, 40, 5, lw=1.0)                # outer race (top)
    f.rect(ox, oy + 4, 40, 5, lw=1.0)                 # inner race (bottom)
    f.circle(ox + 20, oy + 15, 3.4, w=1.0)            # ball
    f.line(ox - 4, oy, ox + 44, oy, w=0.4, dash=CHAIN)
    f.text(ox + 20, oy - 6, "Ball bearing (detail)", size=7, bold=True)
    # conventional representation: square with diagonals
    x2 = 70
    f.rect(x2, oy + 2, 26, 26, lw=1.2)
    f.line(x2, oy + 2, x2 + 26, oy + 28, w=0.8); f.line(x2, oy + 28, x2 + 26, oy + 2, w=0.8)
    f.center_h(x2 - 6, x2 + 32, oy + 15, 0)
    f.text(x2 + 13, oy - 6, "Conventional (sectional view)", size=7, bold=True)
    # end view
    x3 = 130
    f.circle(x3, oy + 15, 14, w=1.2); f.circle(x3, oy + 15, 8, w=1.0); f.circle(x3, oy + 15, 4, w=0.4, dash=HIDDEN) if False else None
    f.center_mark(x3, oy + 15, 17)
    f.text(x3, oy - 6, "Conventional (end view)", size=7, bold=True)
    return f.d


@fig("pd_gears")
def pd_gears(which="spur"):
    f = Fig(165, 66, 1.0)
    def end_view(cx, cy, R):
        f.circle(cx, cy, R, w=1.3); f.circle(cx, cy, R * 0.82, w=0.35, dash=CHAIN); f.circle(cx, cy, R * 0.66, w=0.35)
        f.circle(cx, cy, R * 0.25, w=1.0); f.line(cx - 2, cy + R * 0.25, cx - 2, cy + R * 0.25 + 2, w=1.0) if False else None
        f.center_mark(cx, cy, R + 4)
        f.text(cx, cy - R - 6, "End view", size=7)
    if which == "spur":
        end_view(30, 33, 22)
        ox = 78
        f.rect(ox, 14, 24, 38, lw=1.3)                      # rim width
        f.line(ox - 4, 33, ox + 28, 33, w=0.4, dash=CHAIN)
        f.line(ox, 33 + 22 * 0.82, ox + 24, 33 + 22 * 0.82, w=0.35, dash=CHAIN); f.line(ox, 33 - 22 * 0.82, ox + 24, 33 - 22 * 0.82, w=0.35, dash=CHAIN)
        f.line(ox, 33 + 22 * 0.66, ox + 24, 33 + 22 * 0.66, w=0.35); f.line(ox, 33 - 22 * 0.66, ox + 24, 33 - 22 * 0.66, w=0.35)
        f.text(ox + 12, 8, "Front view", size=7)
        for (yy, tx) in ((52, "addendum circle – thick"), (44.6, "pitch circle – thin chain"), (40.5, "root circle – thin")):
            pass
        f.text(112, 52, "Addendum circle: thick continuous", size=6.6, anchor="start")
        f.text(112, 45, "Pitch circle: thin chain line", size=6.6, anchor="start")
        f.text(112, 38, "Root (dedendum) circle: thin continuous", size=6.6, anchor="start")
        f.text(112, 31, "(thin dashed in sectional views is omitted)", size=6.0, anchor="start") if False else None
    elif which == "worm":
        # worm
        f.rect(8, 40, 60, 12, lw=1.3)
        f.line(8, 46, 68, 46, w=0.35, dash=CHAIN)
        for xx in range(12, 66, 6):
            f.line(xx, 40, xx + 3, 52, w=0.4)
        f.text(38, 56, "Worm", size=7, bold=True)
        # wheel end view / front
        f.circle(38, 18, 14, w=1.3); f.circle(38, 18, 11, w=0.35, dash=CHAIN); f.circle(38, 18, 4, w=1.0)
        f.center_mark(38, 18, 17)
        f.text(38, 0, "Worm wheel (end view, meshing at the throat)", size=6.6)
        # side/section of wheel
        f.rect(102, 4, 20, 36, lw=1.3); f.line(98, 22, 126, 22, w=0.4, dash=CHAIN)
        f.line(102, 22 + 11, 122, 22 + 11, w=0.35, dash=CHAIN); f.line(102, 22 - 11, 122, 22 - 11, w=0.35, dash=CHAIN)
        f.text(112, 44, "Worm wheel (front view)", size=6.6)
        f.text(112, 47.5, "", size=6)
    elif which == "bevel":
        # sectional bevel gear
        f.pline([(20, 16), (60, 8), (60, 40), (20, 48)], closed=True, w=1.3)
        f.line(14, 32, 70, 32, w=0.4, dash=CHAIN)
        f.pline([(20, 16), (20, 8), (30, 8), (30, 14)], w=0.0)
        f.rect(8, 22, 12, 20, lw=1.2) if False else None
        f.rect(60, 22, 18, 20, lw=1.3)
        f.text(40, 4, "Sectional front view", size=7)
        f.line(20, 48, 60, 40, w=0.35, dash=CHAIN) if False else None
        f.line(20, 16, 36, 12.8, w=0.0)
        f.text(105, 40, "Outer (back) cone and face lines thick;", size=6.6, anchor="start"); f.text(105, 35, "pitch cone line thin chain;", size=6.6, anchor="start"); f.text(105, 30, "teeth not drawn in section.", size=6.6, anchor="start")
        f.circle(125, 12, 10, w=1.3); f.circle(125, 12, 6, w=0.35, dash=CHAIN); f.circle(125, 12, 3, w=1.0); f.text(125, -3, "End view", size=7)
    return f.d


@fig("pd_int_thread")
def pd_int_thread():
    f = Fig(165, 64, 1.0)
    # actual view (section): saw-tooth
    ox = 10
    f.text(ox + 24, 56, "Actual view", size=7, bold=True)
    f.line(ox, 12, ox + 50, 12, w=1.2); f.line(ox, 44, ox + 50, 44, w=1.2)
    for i in range(8):
        x = ox + 3 + i * 6
        f.pline([(x, 44), (x + 3, 37), (x + 6, 44)], w=1.0)
        f.pline([(x, 12), (x + 3, 19), (x + 6, 12)], w=1.0)
    f.center_h(ox, ox + 50, 28, 4)
    # conventional section
    ox2 = 78
    f.text(ox2 + 24, 56, "Conventional (sectional)", size=7, bold=True)
    f.line(ox2, 12, ox2 + 50, 12, w=0.4); f.line(ox2, 44, ox2 + 50, 44, w=0.4)    # major dia thin
    f.line(ox2, 19, ox2 + 50, 19, w=1.3); f.line(ox2, 37, ox2 + 50, 37, w=1.3)    # minor dia thick
    f.line(ox2, 19, ox2, 37, w=0.0)
    f.center_h(ox2, ox2 + 50, 28, 4)
    f.text(ox2 + 24, 6, "thick = minor dia, thin = major dia", size=6.2)
    # end view
    cx = 148
    f.circle(cx, 28, 9, w=1.3)
    f.pline(f.arc_pts(cx, 28, 12, 0, 270, 40), w=0.4)
    f.center_mark(cx, 28, 15)
    f.text(cx, 8, "End view", size=7, bold=True)
    return f.d


@fig("pd_leaf_spring")
def pd_leaf_spring():
    f = Fig(165, 56, 1.0)
    # actual
    cx = 38
    for i, (L, y) in enumerate(((70, 0), (58, 3), (46, 6), (34, 9), (22, 12))):
        pts = [(cx + dx, 22 + y - (dx / (L / 2)) ** 2 * 5 * (L / 70) - i * 0.0 - (0 if True else 0)) for dx in [(-L / 2) + L * j / 20 for j in range(21)]]
        f.pline([(x, yy - i * 1.6) for x, yy in pts], w=1.0)
    f.rect(cx - 5, 18, 10, 12, lw=0.9)
    f.text(cx, 8, "Actual view (leaves + clip)", size=7, bold=True)
    # conventional
    cx2 = 125
    f.pline([(cx2 + dx, 28 - (dx / 35) ** 2 * 6) for dx in [-35 + 70 * j / 24 for j in range(25)]], w=1.4)
    f.pline([(cx2 + dx, 26 - (dx / 35) ** 2 * 6) for dx in [-35 + 70 * j / 24 for j in range(25)]], w=0.0)
    f.line(cx2 - 35, 22, cx2 + 35, 22, w=0.0)
    f.line(cx2, 31, cx2, 22, w=0.9) if False else None
    f.line(cx2 - 3, 18, cx2 + 3, 30, w=0.9); f.line(cx2 + 3, 18, cx2 - 3, 30, w=0.9)
    f.text(cx2, 8, "Conventional (single bow line + cross)", size=7, bold=True)
    return f.d


@fig("pd_csk")
def pd_csk():
    f = Fig(165, 54, 1.0)
    ox = 14
    f.rect(ox, 12, 44, 22, lw=1.3)
    f.pline([(ox + 14, 34), (ox + 20, 28), (ox + 20, 12)], w=0.0)
    # hole with chamfer
    f.rect(ox + 16, 12, 12, 22, lw=0.0, fill=colors.white)
    f.pline([(ox + 12, 34), (ox + 18, 28), (ox + 18, 12)], w=1.3)
    f.pline([(ox + 32, 34), (ox + 26, 28), (ox + 26, 12)], w=1.3)
    f.center_v(ox + 22, 12, 34, 4)
    f.text(ox + 22, 4, "Countersunk hole – section", size=7, bold=True)
    f.text(ox + 22, 38, "90° included angle", size=6.4)
    cx = 125
    f.circle(cx, 24, 8, w=1.3); f.circle(cx, 24, 4.5, w=1.3)
    f.center_mark(cx, 24, 11)
    f.text(cx, 4, "Plan (two concentric circles)", size=7, bold=True)
    return f.d


# ---------- welding ----------
def weld_ref(f, x, y, L=40, arrow=True, arrow_len=14):
    f.line(x, y, x + L, y, w=1.0)
    if arrow:
        f.arrow(x, y, x - arrow_len * 0.7, y - arrow_len * 0.7, w=1.0, size=4)


def weld_sym(f, kind, x, y, size=4.0):
    """Weld symbol drawn BELOW the reference line (arrow side), centred at x."""
    if kind == "V":
        f.pline([(x - size, y), (x, y - size * 1.3), (x + size, y)], w=1.0)
    elif kind == "fillet":
        f.pline([(x - size, y), (x - size, y - size * 1.2), (x + size * 0.8, y)], closed=True, w=1.0)
    elif kind == "spot":
        f.circle(x, y - size * 0.9, size * 0.8, w=1.0)
    elif kind == "seam":
        f.circle(x, y - size * 0.9, size * 0.85, w=1.0)
        f.line(x - size, y - size * 0.55, x + size, y - size * 0.55, w=1.0)
        f.line(x - size, y - size * 1.25, x + size, y - size * 1.25, w=1.0)
    elif kind == "U":
        f.pline([(x - size, y), (x - size, y - size * 0.6)] + [(x + size * math.cos(math.radians(a)), y - size * 0.6 + size * math.sin(math.radians(a))) for a in range(180, 361, 15)] + [(x + size, y)], w=1.0)


def convex_mark(f, x, y, size=4.0, depth=2.6):
    """Convex contour symbol: an arc bulging away from the reference line, below the weld symbol."""
    f.pline([(x - size, y), (x, y - depth), (x + size, y)], w=1.0) if False else f.pline(
        [(x - size * 1.1 + 2.2 * size * i / 12, y - depth * math.sin(math.pi * i / 12)) for i in range(13)], w=1.0)


@fig("pd_weld_symbols")
def pd_weld_symbols(which=("V", "seam", "spot", "fillet_convex")):
    n = len(which)
    f = Fig(165, 50, 1.0)
    names = {"V": "Single V butt weld", "seam": "Seam weld", "spot": "Spot weld", "fillet_convex": "Fillet weld with convex finish", "U_convex": "U butt weld, convex contour", "fillet": "Fillet weld"}
    gap = 165 / n
    for i, k in enumerate(which):
        x = 12 + i * gap
        y = 26
        weld_ref(f, x, y, L=gap - 20)
        xm = x + (gap - 20) / 2
        if k == "V":
            weld_sym(f, "V", xm, y)
        elif k == "seam":
            weld_sym(f, "seam", xm, y)
        elif k == "spot":
            weld_sym(f, "spot", xm, y)
        elif k == "fillet_convex":
            weld_sym(f, "fillet", xm, y)
            convex_mark(f, xm, y - 5.2)
        elif k == "fillet":
            weld_sym(f, "fillet", xm, y)
        elif k == "U_convex":
            weld_sym(f, "U", xm, y)
            convex_mark(f, xm, y - 7.6)
        f.text(x + (gap - 20) / 2, 8, names[k], size=6.6, bold=True)
        f.text(x + (gap - 20) / 2, 42, "arrow side", size=5.8) if False else None
    f.text(4, 45, "Arrow points to the joint; symbol below the reference line = weld on the arrow side.", size=6.4, anchor="start")
    return f.d


@fig("pd_u_butt_weld")
def pd_u_butt_weld():
    f = Fig(165, 78, 1.0)
    # two plates 12 mm thick, 60 long; show end view of the joint (scale 2:1) and symbol
    s = 1.6
    ox, oy = 18, 16
    t = 12 * s
    gw = 10
    # left plate and right plate with U groove (each gets half)
    L = 30
    f.pline([(ox, oy), (ox + L, oy), (ox + L, oy + t * 0.45)] + [(ox + L + 0 + 0, oy + t * 0.45)] + [(ox + L, oy + t)] + [(ox, oy + t)], closed=True, w=0.0)
    left = [(ox, oy), (ox + L, oy), (ox + L, oy + t * 0.35)] + f.arc_pts(ox + L + 4.0, oy + t * 0.35 + 4.0, 4.0, 270 - 90, 180, 10)[::-1][:0] + [(ox + L, oy + t * 0.55), (ox + L + 3, oy + t)] + [(ox, oy + t)]
    # build plates simply with U-shaped groove: root face 2 mm, radius 4 mm
    rf = 2 * s
    rr = 4 * s
    Lp = ox + L
    gap = 2 * s
    leftp = [(ox, oy), (Lp - 0, oy), (Lp, oy + rf)] + [(Lp - rr + rr * math.cos(math.radians(a)), oy + rf + rr * math.sin(math.radians(a)) * 0 + rr - rr * math.cos(math.radians(a)) * 0) for a in []]
    # arcs: centre at (Lp + rr - gap/2 ... ) -> keep drawing simple: polylines
    cxl = Lp + rr * 0.0
    arcl = [(Lp + rr * (1 - math.cos(math.radians(a))), oy + rf + rr * math.sin(math.radians(a))) for a in range(0, 91, 10)]
    leftp = [(ox, oy), (Lp, oy), (Lp, oy + rf)] + arcl + [(Lp + rr, oy + t)] + [(ox, oy + t)]
    ox2 = Lp + 2 * gap
    arcr = [(ox2 - rr * (1 - math.cos(math.radians(a))), oy + rf + rr * math.sin(math.radians(a))) for a in range(0, 91, 10)]
    rightp = [(ox2, oy), (ox2 + L, oy), (ox2 + L, oy + t), (ox2 - rr, oy + t)] + arcr[::-1] + [(ox2, oy + rf)]
    f.pline(leftp, closed=True, w=1.2, fill=LIGHT) if False else f.pline(leftp, closed=True, w=1.2)
    f.pline(rightp, closed=True, w=1.2)
    # weld metal with convex contour
    wx0, wx1 = Lp, ox2
    weld = [(wx0, oy), (wx1, oy)] + [(wx1, oy + rf)] + arcr + [(ox2 - rr, oy + t)] + [(Lp + rr, oy + t)] + arcl[::-1] + [(wx0, oy + rf)]
    f.hatch([[(wx0, oy), (wx1, oy), (wx1, oy + rf)] + arcr + [(ox2 - rr, oy + t), (Lp + rr, oy + t)] + arcl[::-1] + [(wx0, oy + rf)]], gap=1.6, w=0.3)
    f.pline([(Lp + rr, oy + t), (Lp + (ox2 - Lp) / 2, oy + t + 3), (ox2 - rr, oy + t)], w=1.2)    # convex reinforcement
    f.dim_v(oy, oy + t, ox - 2, "12", off=-3, ext_from=(ox, ox))
    f.dim_h(ox, ox + L, oy, "", off=-6)
    f.text(Lp + (ox2 - Lp) / 2, oy - 9, "end view of joint (enlarged)", size=6.6)
    # welding symbol
    rx, ry = 100, 52
    weld_ref(f, rx, ry, L=48, arrow=False)
    f.arrow(rx, ry, rx - 9, ry - 14, w=1.0, size=4)
    xm = rx + 22
    weld_sym(f, "U", xm, ry)
    convex_mark(f, xm, ry - 7.6)
    f.text(xm + 12, ry + 2, "60", size=7, anchor="start") if False else None
    f.text(rx + 50, ry - 2, "", size=6)
    f.text(112, 66, "Welding symbol", size=7, bold=True)
    f.text(112, 40, "U butt weld, convex contour", size=6.6, anchor="start") if False else None
    f.text(100, 30, "U-groove (butt) with convex contour;", size=6.4, anchor="start"); f.text(100, 25.5, "plates 12 mm thick × 60 mm long,", size=6.4, anchor="start"); f.text(100, 21, "weld along the full 60 mm length.", size=6.4, anchor="start")
    return f.d


@fig("pd_fillet_lap")
def pd_fillet_lap():
    f = Fig(165, 62, 1.0)
    ox, oy = 14, 20
    s = 1.8
    t = 8 * s
    f.rect(ox, oy, 50, t, lw=1.2)                 # lower plate
    f.rect(ox + 20, oy + t, 50, t, lw=1.2)        # upper plate (lap)
    # fillet at the edge of the upper plate
    z = 8 * s * 0.9
    f.pline([(ox + 20, oy + t), (ox + 20 - z, oy + t), (ox + 20, oy + t + z)], closed=True, w=1.0, fill=BLACK)
    f.dim_v(oy, oy + t, ox - 2, "8", off=-3, ext_from=(ox, ox))
    f.text(ox + 35, oy - 7, "Two M.S. plates, 8 mm thick, lap joint", size=6.6)
    rx, ry = 100, 36
    weld_ref(f, rx, ry, L=46, arrow=False)
    f.arrow(rx, ry, rx - 12, ry - 14, w=1.0, size=4)
    weld_sym(f, "fillet", rx + 20, ry)
    f.text(rx + 12, ry - 5.5, "8", size=7.5, bold=True, anchor="end")
    f.text(rx + 22, ry - 14, "(8 = leg length)", size=6.4, anchor="start") if False else None
    f.text(100, 14, "Fillet weld, leg length 8 mm,", size=6.6, anchor="start"); f.text(100, 9.5, "on the arrow side (symbol below line).", size=6.6, anchor="start")
    return f.d


@fig("pd_pipe_tube")
def pd_pipe_tube():
    f = Fig(165, 44, 1.0)
    cx, cy = 30, 22
    f.circle(cx, cy, 14, w=1.3); f.circle(cx, cy, 9, w=1.3)
    ring = [(cx + 14 * math.cos(math.radians(a)), cy + 14 * math.sin(math.radians(a))) for a in range(0, 360, 10)]
    hole = [(cx + 9 * math.cos(math.radians(a)), cy + 9 * math.sin(math.radians(a))) for a in range(0, 360, 10)]
    f.hatch([ring, hole], gap=1.8, angle=45, w=0.3)
    f.center_mark(cx, cy, 17)
    f.text(cx, 2, "End view (section)", size=6.8, bold=True)
    ox = 75
    for sg in (1, -1):
        reg = [(ox, cy + sg * 9), (ox + 60, cy + sg * 9), (ox + 60, cy + sg * 14), (ox, cy + sg * 14)]
        f.pline(reg, closed=True, w=1.2)
        f.hatch([reg], gap=1.8, angle=45, w=0.3)
    f.center_h(ox - 4, ox + 64, cy, 0)
    f.text(ox + 30, 2, "Sectional front view (pipe or tubing)", size=6.8, bold=True)
    return f.d
