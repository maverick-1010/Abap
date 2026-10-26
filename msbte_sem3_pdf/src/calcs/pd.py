"""Production Drawing calculations: tapers, limits and fits, tool-post geometry."""
import math
from calcfw import calc, g


def fit_block(c, label, basic, hole, shaft, note=""):
    """hole = (ES, EI), shaft = (es, ei) in mm. Adds steps, returns (min_cl, max_cl, type)."""
    ES, EI = hole
    es, ei = shaft
    hmax, hmin = basic + ES, basic + EI
    smax, smin = basic + es, basic + ei
    c.step(f"{label}: limits of hole", "H_{max} = B + ES,   H_{min} = B + EI", f"= {g(basic)} + ({g(ES)}),  {g(basic)} + ({g(EI)})", None)
    c.say(f"Hole: maximum = {hmax:.3f} mm,  minimum = {hmin:.3f} mm")
    c.say(f"Shaft: maximum = {smax:.3f} mm,  minimum = {smin:.3f} mm")
    maxcl = hmax - smin
    mincl = hmin - smax
    c.step(f"{label}: maximum clearance", "= H_{max} − S_{min}", f"= {hmax:.3f} − {smin:.3f}", maxcl, "mm", 3)
    c.step(f"{label}: minimum clearance", "= H_{min} − S_{max}", f"= {hmin:.3f} − {smax:.3f}", mincl, "mm", 3)
    if mincl >= -1e-12:
        typ = "CLEARANCE fit"
    elif maxcl <= 1e-12:
        typ = "INTERFERENCE fit"
    else:
        typ = "TRANSITION fit"
    c.say(f"{label}: minimum clearance {'≥' if mincl >= 0 else '<'} 0 and maximum clearance {'>' if maxcl > 0 else '≤'} 0, so it is a {typ}.")
    # second method: from deviations
    c.check(f"{label}: max clearance = ES − ei", ES - ei, maxcl, 1e-9, 1e-12)
    c.check(f"{label}: min clearance = EI − es", EI - es, mincl, 1e-9, 1e-12)
    return mincl, maxcl, typ


def taper_calc(c, D, L, k):
    c.given("Large diameter D", D, "mm")
    c.given("Length L", L, "mm")
    c.given("Taper", f"1 : {k}", "", "taper = (D − d)/L")
    d = c.step("Small diameter", f"d = D − L / {k}", f"= {g(D)} − {g(L)} / {k}", D - L / k, "mm", 2)
    c.answer("Small end diameter d", d, "mm", 2)
    c.answer("Taper per unit length (D − d)/L", f"1 : {k}", "")
    c.check("(D − d)/L = 1/k", (D - d) / L, 1 / k, 1e-12)


@calc("PD-W24-Q1b", "Taper 1:10 on a shaft Ø40 × 110")
def pd_w24_1b(c):
    taper_calc(c, 40.0, 110.0, 10)
    c.note("The taper is assumed to run over the whole length of 110 mm (it is not said otherwise).")


@calc("PD-S25-Q3b", "Taper 1:20 on a shaft Ø40 × 120")
def pd_s25_3b(c):
    taper_calc(c, 40.0, 120.0, 20)
    c.note("The taper is assumed to run over the whole length of 120 mm.")


@calc("PD-W24-Q3d", "Fit between shaft 40(−0.02/−0.04) and hole 40(+0.02/−0.04)")
def pd_w24_3d(c):
    c.given("Basic size", 40, "mm")
    c.given("Shaft deviations (es, ei)", "−0.02, −0.04", "mm")
    c.given("Hole deviations (ES, EI)", "+0.02, −0.04", "mm", "as printed")
    mn, mx, typ = fit_block(c, "Fit", 40.0, (0.02, -0.04), (-0.02, -0.04))
    c.answer("Maximum clearance", mx, "mm", 3)
    c.answer("Minimum clearance (negative = interference)", mn, "mm", 3)
    c.answer("Type of fit", typ.replace(" fit", "").title() + " fit", "")
    c.check("Type is transition (clearance range straddles zero)", 1.0 if (mn < 0 < mx) else 0.0, 1.0)


@calc("PD-S25-Q3g", "Fit between shaft Ø20(+0.023/+0.012) and hole Ø20(+0.018/0)")
def pd_s25_3g(c):
    c.given("Basic size", 20, "mm")
    c.given("Shaft deviations (es, ei)", "+0.023, +0.012", "mm")
    c.given("Hole deviations (ES, EI)", "+0.018, +0.000", "mm")
    mn, mx, typ = fit_block(c, "Fit", 20.0, (0.018, 0.0), (0.023, 0.012))
    c.answer("Maximum clearance", mx, "mm", 3)
    c.answer("Minimum clearance (negative = interference)", mn, "mm", 3)
    c.answer("Type of fit", "Transition fit", "")
    c.check("Type is transition", 1.0 if (mn < 0 < mx) else 0.0, 1.0)


def ltp(c, wedge_label, R):
    z0 = 36 - (R - math.sqrt(R * R - 60 * 60))
    c.given("Wedge / ring seat radius R", R, "mm")
    c.given("Ring: outer radius, bore radius, thickness at outer edge", "60, 30, 18", "mm")
    sag = c.step("Fall of the concave seat from the ring edge to its centre", f"s = R − √(R² − 60²)", f"= {R} − √({R}² − 60²)", R - math.sqrt(R * R - 3600), "mm", 2)
    c.step("Seat height at the axis", "z₀ = 36 − s", f"= 36 − {sag:.2f}", 36 - sag, "mm above the bottom of the block", 2)
    half = R / 2
    h_end = c.step("Wedge: depth of the curve at its ends (chord = R, as the wedge length equals R)", "s_w = R − √(R² − (R/2)²)", f"= {R} − √({R}² − {half:g}²)", R - math.sqrt(R * R - half * half), "mm", 2)
    c.answer("Seat height at the axis z₀", 36 - sag, "mm", 2)
    c.answer("Depth of the wedge curve over its length", h_end, "mm", 2)
    c.check("Seat height + sag = ring edge height (36 mm)", (36 - sag) + sag, 36.0, 1e-12)


@calc("PD-W24-Q5b-geom", "Lathe tool post geometry (R = 144)")
def pd_w24_5b_geom(c):
    ltp(c, "wedge", 144)


@calc("PD-S25-Q5b-geom", "Lathe tool post geometry (R = 146)")
def pd_s25_5b_geom(c):
    ltp(c, "wedge", 146)


@calc("PD-W24-Q5b-fits", "Fits in the lathe tool post (W24 tolerance chart)")
def pd_w24_5b_fits(c):
    c.given("Tolerance chart (printed)", "Ø60H7: +0.030/0;  Ø60e8: −0.060/−0.106;  24H7: +0.021/0;  24n6: +0.036/+0.015", "mm")
    m1 = fit_block(c, "Ø60 H7/e8 (block hole – post)", 60.0, (0.030, 0.0), (-0.060, -0.106))
    m2 = fit_block(c, "24 H7/n6 (post slot – wedge)", 24.0, (0.021, 0.0), (0.036, 0.015))
    c.answer("Ø60 H7/e8 – min / max clearance", f"{m1[0]:.3f} / {m1[1]:.3f}", "mm")
    c.answer("Ø60 H7/e8", m1[2], "")
    c.answer("24 H7/n6 – max clearance / max interference", f"{m2[1]:.3f} / {-m2[0]:.3f}", "mm")
    c.answer("24 H7/n6", m2[2], "")


@calc("PD-S25-Q5b-fits", "Fits in the lathe tool post (S25 tolerance chart)")
def pd_s25_5b_fits(c):
    c.given("Tolerance chart (printed)", "Ø60H7: +0.000/+0.030;  Ø60e8: −0.060/−0.106;  24H7: +0.021/+0.000;  24n6: +0.036/+0.015", "mm")
    m1 = fit_block(c, "Ø60 H7/e8 (block hole – post)", 60.0, (0.030, 0.0), (-0.060, -0.106))
    m2 = fit_block(c, "24 H7/n6 (post slot – wedge)", 24.0, (0.021, 0.0), (0.036, 0.015))
    c.answer("Ø60 H7/e8 – min / max clearance", f"{m1[0]:.3f} / {m1[1]:.3f}", "mm")
    c.answer("Ø60 H7/e8", m1[2], "")
    c.answer("24 H7/n6 – max clearance / max interference", f"{m2[1]:.3f} / {-m2[0]:.3f}", "mm")
    c.answer("24 H7/n6", m2[2], "")


@calc("PD-S25-Q5a-fits", "Fits in the foot step bearing (tolerance chart)")
def pd_s25_5a_fits(c):
    c.given("Tolerance chart (printed)", "68H7: +0.030/0;  68h6: 0/−0.019;  50H7: +0.039/0;  50e8: −0.050/−0.089;  8H7: +0.015/0;  8g6: −0.005/−0.014 (signs read from the scan)", "mm")
    m1 = fit_block(c, "Ø68 H7/h6 (body bore – bush)", 68.0, (0.030, 0.0), (0.0, -0.019))
    m2 = fit_block(c, "Ø50 H7/e8 (bush bore – shaft/disc)", 50.0, (0.039, 0.0), (-0.050, -0.089))
    m3 = fit_block(c, "Ø8 H7/g6 (pin)", 8.0, (0.015, 0.0), (-0.005, -0.014))
    for lab, m in (("Ø68 H7/h6", m1), ("Ø50 H7/e8", m2), ("Ø8 H7/g6", m3)):
        c.answer(lab, f"{m[2]}  (clearance {m[0]:.3f} to {m[1]:.3f} mm)", "")


@calc("PD-S25-Q4-fits", "Fits in the Oldham's coupling (ISO 286 limits)")
def pd_s25_4_fits(c):
    c.given("Fit chart (printed)", "16H7/n6 transition; 30H7/g6 clearance; 50H8/g8 clearance", "")
    c.given("Limits used (standard ISO 286 values – not printed in the paper)", "16H7 +0.018/0, n6 +0.023/+0.012; 30H7 +0.021/0, g6 −0.007/−0.020; 50H8 +0.039/0, g8 −0.009/−0.048", "mm")
    m1 = fit_block(c, "16 H7/n6 (key – keyway)", 16.0, (0.018, 0.0), (0.023, 0.012))
    m2 = fit_block(c, "30 H7/g6 (groove – tongue)", 30.0, (0.021, 0.0), (-0.007, -0.020))
    m3 = fit_block(c, "50 H8/g8 (flange bore – shaft)", 50.0, (0.039, 0.0), (-0.009, -0.048))
    c.answer("16 H7/n6", m1[2], "")
    c.answer("30 H7/g6", m2[2], "")
    c.answer("50 H8/g8", m3[2], "")
    c.check("Types agree with the printed fit chart (transition, clearance, clearance)", 1.0 if (m1[2].startswith("TRANS") and m2[2].startswith("CLEAR") and m3[2].startswith("CLEAR")) else 0.0, 1.0)


@calc("PD-W24-Q2b", "Completing the front view: size of the Ø40 hole in the inclined block")
def pd_w24_2b(c):
    c.given("Hole diameter", 40, "mm")
    c.given("Angle of the inclined face with the XY line in plan", 30, "°", "read from the auxiliary view of the figure")
    th = 30.0
    w = c.step("Width of the hole's ellipse in the front view", "w = Ø × cos θ", f"= 40 × cos {th:g}°", 40 * math.cos(math.radians(th)), "mm", 2)
    c.step("Height of the ellipse in the front view", "h = Ø (true size, the vertical axis is parallel to the V.P.)", "= 40", 40.0, "mm", 2)
    c.answer("Ellipse in front view: width × height", f"{w:.2f} × 40", "mm")
    c.check("w² + (Ø sin θ)² = Ø²", w ** 2 + (40 * math.sin(math.radians(th))) ** 2, 1600.0, 1e-12)
    c.note("Slot check: the dimensions 15 + 20 + 15 = 50 mm give a slot width of 20 mm, so the end radius should be 10 mm, but the figure says R12.")


@calc("PD-S25-Q2a", "Completing the top view of the bent plate (inclined arm at 60°)")
def pd_s25_2a(c):
    L, th, t = 60.0, 60.0, 6.0
    c.given("Length of inclined arm (true length, seen in the F.V.)", L, "mm")
    c.given("Inclination of the arm with the horizontal", th, "°", "bend angle 120° between the base and the arm")
    c.given("Plate thickness", t, "mm")
    lp = c.step("Length of the arm in the top view", "l = L cos θ", f"= {g(L)} × cos {th:g}°", L * math.cos(math.radians(th)), "mm", 2)
    h = c.step("Height of the arm end in the front view", "h = L sin θ", f"= {g(L)} × sin {th:g}°", L * math.sin(math.radians(th)), "mm", 2)
    sq = c.step("A 20 mm square hole on the arm: length in the top view", "a' = 20 cos θ", f"= 20 × cos {th:g}°", 20 * math.cos(math.radians(th)), "mm", 2)
    c.answer("Foreshortened length of arm in top view", lp, "mm")
    c.answer("Height of arm end in F.V.", h, "mm")
    c.answer("20 mm square hole appears as 20 × a'", sq, "mm")
    c.check("l² + h² = L²", lp ** 2 + h ** 2, L ** 2, 1e-12)
