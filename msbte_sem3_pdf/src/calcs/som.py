"""Strength of Materials numericals (SOM-S23, I-scheme paper 22306)."""
import math
import numpy as np
from calcfw import calc, g
from beam import Beam

PI = math.pi


@calc("SOM-S23-Q2a", "Hollow circular section: MI about tangent and polar MI")
def som_2a(c):
    D, d = 200.0, 100.0
    c.given("External diameter D", D, "mm")
    c.given("Internal diameter d", d, "mm")
    I = c.step("MI about a diameter (centroidal axis)", "I = π (D⁴ − d⁴) / 64", f"= π ({g(D)}⁴ − {g(d)}⁴) / 64", PI * (D**4 - d**4) / 64, "mm⁴")
    A = c.step("Area of section", "A = π (D² − d²) / 4", f"= π ({g(D)}² − {g(d)}²) / 4", PI * (D**2 - d**2) / 4, "mm²")
    h = D / 2
    It = c.step("MI about tangent (parallel-axis theorem)", "I_{T} = I + A h²,  h = D/2 = 100 mm", f"= {I:.4e} + {A:.2f} × {g(h)}²", I + A * h * h, "mm⁴")
    J = c.step("Polar MI", "J = π (D⁴ − d⁴) / 32", f"= π ({g(D)}⁴ − {g(d)}⁴) / 32", PI * (D**4 - d**4) / 32, "mm⁴")
    c.answer("MI about tangent I_{T}", It, "mm⁴")
    c.answer("Polar MI J", J, "mm⁴")
    out_t = 5 * PI * D**4 / 64
    in_t = PI * d**4 / 64 + (PI * d**2 / 4) * h * h
    c.check("I_{T} = (outer solid circle) − (inner solid circle) about the same tangent", out_t - in_t, It, 1e-9)
    c.check("J = 2 I (perpendicular-axis theorem)", 2 * I, J, 1e-9)


@calc("SOM-S23-Q2b", "Stepped member ABCD in equilibrium")
def som_2b(c):
    P1, P3, P4, E = 45.0, 450.0, 130.0, 2.1e5
    A = [625.0, 2500.0, 1250.0]
    L = [1200.0, 600.0, 900.0]
    c.given("P₁", P1, "kN")
    c.given("P₃", P3, "kN")
    c.given("P₄", P4, "kN")
    c.given("Areas A_{AB}, A_{BC}, A_{CD}", "625, 2500, 1250", "mm²")
    c.given("Lengths L_{AB}, L_{BC}, L_{CD}", "120, 60, 90", "cm", "= 1200, 600, 900 mm")
    c.given("E", E, "N/mm²")
    P2 = c.step("Equilibrium of whole member (→ positive): −P₁ + P₂ − P₃ + P₄ = 0", "P₂ = P₁ + P₃ − P₄", f"= {g(P1)} + {g(P3)} − {g(P4)}", P1 + P3 - P4, "kN")
    NAB = c.step("Axial force in AB (tension)", "N_{AB} = P₁", f"= {g(P1)}", P1, "kN")
    NBC = c.step("Axial force in BC (compression)", "N_{BC} = P₁ − P₂", f"= {g(P1)} − {g(P2)}", P1 - P2, "kN")
    NCD = c.step("Axial force in CD (tension)", "N_{CD} = P₄", f"= {g(P4)}", P4, "kN")
    N = [NAB, NBC, NCD]
    d = [c.step(f"Change in length of {nm}", "δ = N L / (A E)", f"= ({g(N[i])} × 10³ × {g(L[i])}) / ({g(A[i])} × {g(E)})", N[i] * 1e3 * L[i] / (A[i] * E), "mm", 4)
         for i, nm in enumerate(["AB", "BC", "CD"])]
    tot = c.step("Total elongation", "δ = δ_{AB} + δ_{BC} + δ_{CD}", f"= {d[0]:.4f} + ({d[1]:.4f}) + {d[2]:.4f}", sum(d), "mm", 4)
    c.answer("Force P₂", P2, "kN")
    c.answer("Total elongation of member", tot, "mm", 4)
    # second method: forces from the right-hand end
    N_AB_r = P4 - P3 + P2          # sum of forces right of cut in AB, taken positive towards right
    N_BC_r = P4 - P3
    N_CD_r = P4
    c.check("N_{AB} from the right-hand side equals P₁", N_AB_r, NAB, 1e-9)
    c.check("N_{BC} from the right-hand side (P₄ − P₃)", N_BC_r, NBC, 1e-9)
    c.check("Σ N L / A E recomputed using right-hand forces", sum(n * 1e3 * l / (a * E) for n, l, a in zip([N_AB_r, N_BC_r, N_CD_r], L, A)), tot, 1e-9)


@calc("SOM-S23-Q2c", "Tri-axial stress: strains and volume change")
def som_2c(c):
    sx, sy, sz, E, mu = 100.0, 60.0, -30.0, 2e5, 0.25
    X, Y, Z = 400.0, 150.0, 300.0
    c.given("σ_{x}", sx, "N/mm²", "tensile")
    c.given("σ_{y}", sy, "N/mm²", "tensile")
    c.given("σ_{z}", sz, "N/mm²", "compressive, so negative")
    c.given("E", E, "N/mm²")
    c.given("μ", mu, "")
    c.given("X, Y, Z", "400, 150, 300", "mm")
    ex = c.step("Strain in x direction", "ε_{x} = [σ_{x} − μ(σ_{y} + σ_{z})] / E", f"= [{g(sx)} − {g(mu)}({g(sy)} + ({g(sz)}))] / {g(E)}", (sx - mu * (sy + sz)) / E, "", 6)
    ey = c.step("Strain in y direction", "ε_{y} = [σ_{y} − μ(σ_{x} + σ_{z})] / E", f"= [{g(sy)} − {g(mu)}({g(sx)} + ({g(sz)}))] / {g(E)}", (sy - mu * (sx + sz)) / E, "", 6)
    ez = c.step("Strain in z direction", "ε_{z} = [σ_{z} − μ(σ_{x} + σ_{y})] / E", f"= [{g(sz)} − {g(mu)}({g(sx)} + {g(sy)})] / {g(E)}", (sz - mu * (sx + sy)) / E, "", 6)
    ev = c.step("Volumetric strain", "ε_{v} = ε_{x} + ε_{y} + ε_{z}", f"= {ex:.6g} + {ey:.6g} + ({ez:.6g})", ex + ey + ez, "", 6)
    V = X * Y * Z
    dV = c.step("Change in volume", "δV = ε_{v} × V,  V = 400 × 150 × 300", f"= {ev:.6g} × {g(V)}", ev * V, "mm³", 1)
    c.answer("ε_{x}", ex, "", 6)
    c.answer("ε_{y}", ey, "", 6)
    c.answer("ε_{z}", ez, "(negative = contraction)", 6)
    c.answer("Change in volume δV (increase)", dV, "mm³", 1)
    c.check("ε_{v} = (1 − 2μ)(σ_{x} + σ_{y} + σ_{z}) / E", (1 - 2 * mu) * (sx + sy + sz) / E, ev, 1e-9)
    c.check("δV from changed sides: (X(1+ε_x))(Y(1+ε_y))(Z(1+ε_z)) − XYZ", X * (1 + ex) * Y * (1 + ey) * Z * (1 + ez) - V, dV, 2e-3)


@calc("SOM-S23-Q3a", "MI of lamina about axis A-A")
def som_3a(c):
    B, H, R, gap = 700.0, 300.0, 150.0, 250.0
    c.given("Rectangle B × H", "700 × 300", "mm")
    c.given("Semicircular cut-out radius R", R, "mm", "diameter on the bottom edge, touching the left edge (as drawn)")
    c.given("Distance of A-A from right edge", gap, "mm")
    xa = B + gap                      # A-A position measured from left edge
    d1 = xa - B / 2
    A1 = B * H
    I1g = H * B**3 / 12
    I1 = c.step("Rectangle: I about A-A", "I₁ = H B³/12 + A₁ d₁²,  d₁ = 950 − 350 = 600", f"= {I1g:.4e} + {g(A1)} × {g(d1)}²", I1g + A1 * d1**2, "mm⁴")
    d2 = xa - R
    A2 = PI * R**2 / 2
    I2g = PI * R**4 / 8
    I2 = c.step("Semicircle: I about A-A", "I₂ = π R⁴/8 + A₂ d₂²,  d₂ = 950 − 150 = 800", f"= {I2g:.4e} + {A2:.2f} × {g(d2)}²", I2g + A2 * d2**2, "mm⁴")
    I = c.step("Lamina = rectangle − semicircle", "I_{AA} = I₁ − I₂", f"= {I1:.4e} − {I2:.4e}", I1 - I2, "mm⁴")
    c.answer("I about A-A", I, "mm⁴")
    step = 0.5
    xs = np.arange(step / 2, B, step)
    ys = np.arange(step / 2, H, step)
    X, Y = np.meshgrid(xs, ys)
    inside_cut = (X - R) ** 2 + Y ** 2 < R ** 2
    num = (((xa - X) ** 2) * (~inside_cut)).sum() * step * step
    c.check("Numerical integration of ∫ x² dA over the lamina (0.5 mm grid, 0.05 %)", num, I, 5e-4)


@calc("SOM-S23-Q3b", "Impact load on a hanging bar")
def som_3b(c):
    d, L, W, h, E = 20.0, 1000.0, 1000.0, 250.0, 2e5
    c.given("Diameter d", d, "mm")
    c.given("Length L", L, "mm")
    c.given("Falling weight W", W, "N")
    c.given("Height of fall h", h, "mm")
    c.given("E", E, "N/mm²")
    A = c.step("Area of bar", "A = π d² / 4", f"= π × {g(d)}² / 4", PI * d * d / 4, "mm²")
    k = 1 + 2 * A * E * h / (W * L)
    s = c.step("Maximum instantaneous stress", "σ = (W/A) [1 + √(1 + 2 A E h / (W L))]",
               f"= ({g(W)}/{A:.2f}) [1 + √(1 + 2 × {A:.2f} × {g(E)} × {g(h)} / ({g(W)} × {g(L)}))]",
               (W / A) * (1 + math.sqrt(k)), "N/mm²")
    dl = c.step("Instantaneous elongation", "δ = σ L / E", f"= {s:.2f} × {g(L)} / {g(E)}", s * L / E, "mm", 3)
    U = c.step("Strain energy stored", "U = σ² / (2E) × A L", f"= {s:.2f}² / (2 × {g(E)}) × {A:.2f} × {g(L)}", s * s / (2 * E) * A * L / 1000, "N·m", 2)
    c.answer("Maximum instantaneous stress", s, "N/mm²")
    c.answer("Elongation", dl, "mm", 3)
    c.answer("Strain energy stored", U, "N·m")
    c.check("Energy balance: W (h + δ) = U", W * (h + dl) / 1000, U, 1e-9)
    P = s * A
    c.check("Equivalent static load P = σ A satisfies  P δ / 2 = U", P * dl / 2 / 1000, U, 1e-9)


@calc("SOM-S23-Q3c", "Simply supported beam: SF and BM values")
def som_3c(c):
    L = 7.0
    c.given("Span L", L, "m")
    c.given("Point load W₁", "3 kN at 3 m from left support", "")
    c.given("Point load W₂", "5 kN at 2 m from right support, i.e. 5 m from left", "")
    c.given("UDL", "2 kN/m over 3 m from left support", "", "total 6 kN, acts at 1.5 m")
    Rb = c.step("Moments about A (R_{B} × 7)", "R_{B} × 7 = 3×3 + 5×5 + (2×3)×1.5", "= 9 + 25 + 9 = 43", 43 / 7, "kN", 3)
    Ra = c.step("Vertical equilibrium", "R_{A} = (3 + 5 + 6) − R_{B}", f"= 14 − {Rb:.3f}", 14 - Rb, "kN", 3)
    SF = {
        "A (right)": Ra, "C (3 m, left of 3 kN)": Ra - 6, "C (3 m, right of 3 kN)": Ra - 6 - 3,
        "D (5 m, left of 5 kN)": Ra - 9, "D (5 m, right of 5 kN)": Ra - 14, "B (left)": Ra - 14,
    }
    for k, v in SF.items():
        c.step(f"SF at {k}", "", "", v, "kN", 3)
    MC = c.step("BM at C (3 m)", "M_{C} = R_{A} × 3 − 2×3×1.5", f"= {Ra:.3f} × 3 − 9", Ra * 3 - 9, "kN·m", 3)
    MD = c.step("BM at D (5 m)", "M_{D} = R_{A} × 5 − 2×3×3.5 − 3 × 2", f"= {Ra:.3f} × 5 − 21 − 6", Ra * 5 - 21 - 6, "kN·m", 3)
    c.answer("R_{A}", Ra, "kN", 3)
    c.answer("R_{B}", Rb, "kN", 3)
    c.answer("Maximum BM (at 3 m from A, where SF changes sign)", MC, "kN·m", 3)
    bm = Beam(L, 0, L, points=[(3, 3), (5, 5)], udls=[(0, 3, 2)])
    c.check("R_{A} from the beam solver", bm.Ra, Ra, 1e-9)
    c.check("R_{B} from the beam solver", bm.Rb, Rb, 1e-9)
    c.check("BM at C from the beam solver", bm.bm(3), MC, 1e-9)
    c.check("BM at D from the beam solver", bm.bm(5), MD, 1e-9)
    c.check("BM at B is zero (simple support)", bm.bm(L), 0.0, 0, 1e-9)


@calc("SOM-S23-Q3d", "Greatest eccentricity for no tension (hollow circular column)")
def som_3d(c):
    D, d, P = 400.0, 200.0, 80e3
    c.given("External diameter D", 40, "cm", "= 400 mm")
    c.given("Internal diameter d", 20, "cm", "= 200 mm")
    c.given("Load P", 80, "kN", "= 80 000 N")
    e = c.step("Core of hollow circular section: e = (D² + d²)/(8D)", "e = (D² + d²) / (8 D)", f"= ({g(D)}² + {g(d)}²) / (8 × {g(D)})", (D**2 + d**2) / (8 * D), "mm")
    c.answer("Greatest eccentricity (radius of core)", e, "mm")
    c.answer("Greatest eccentricity", e / 10, "cm")
    A = PI / 4 * (D**2 - d**2)
    I = PI / 64 * (D**4 - d**4)
    sd, sb = P / A, P * e * (D / 2) / I
    c.step("Direct stress", "σ_{d} = P / A", f"= {g(P)} / {A:.2f}", sd, "N/mm²", 4)
    c.step("Bending stress at edge", "σ_{b} = P e y / I", f"= {g(P)} × {e:.2f} × {g(D/2)} / {I:.4e}", sb, "N/mm²", 4)
    c.check("Minimum stress σ_{d} − σ_{b} = 0 (just no tension)", sd - sb, 0.0, 0, 1e-9)


@calc("SOM-S23-Q4b", "UDL a cast iron pipe can carry")
def som_4b(c):
    D, d, L, s = 800.0, 700.0, 7500.0, 140.0
    c.given("External diameter D", D, "mm")
    c.given("Internal diameter d", d, "mm")
    c.given("Span L", 7.5, "m", "= 7500 mm")
    c.given("Permissible bending stress σ_{b}", s, "N/mm²")
    I = c.step("MI of pipe section", "I = π (D⁴ − d⁴) / 64", f"= π ({g(D)}⁴ − {g(d)}⁴) / 64", PI * (D**4 - d**4) / 64, "mm⁴")
    Z = c.step("Section modulus", "Z = I / y = I / (D/2)", f"= {I:.4e} / {g(D/2)}", I / (D / 2), "mm³")
    M = c.step("Maximum BM the pipe can resist", "M = σ_{b} Z", f"= {g(s)} × {Z:.4e}", s * Z, "N·mm")
    w = c.step("UDL from M = w L² / 8", "w = 8 M / L²", f"= 8 × {M:.4e} / {g(L)}²", 8 * M / L**2, "N/mm")
    c.answer("UDL intensity", w, "N/mm", 2)
    c.answer("UDL intensity", w, "kN/m", 2)
    c.check("Round trip: σ = (w L² / 8) / Z gives 140 N/mm²", (w * L * L / 8) / Z, s, 1e-9)
    c.note("Self-weight of pipe and oil is ignored (not asked).")


@calc("SOM-S23-Q4d", "Young's modulus and Poisson's ratio from a compression test")
def som_4d(c):
    b, P, gl, dl, dt = 50.0, 500e3, 200.0, 0.5, 0.04
    c.given("Cross-section", "50 × 50", "mm")
    c.given("Axial compressive load P", 500, "kN")
    c.given("Gauge length", gl, "mm")
    c.given("Contraction", dl, "mm")
    c.given("Increase in thickness", dt, "mm")
    s = c.step("Stress", "σ = P / A", f"= {g(P)} / ({g(b)} × {g(b)})", P / (b * b), "N/mm²")
    el = c.step("Longitudinal strain", "ε = δL / L", f"= {g(dl)} / {g(gl)}", dl / gl, "", 5)
    E = c.step("Young's modulus", "E = σ / ε", f"= {s:.2f} / {el:.5f}", s / el, "N/mm²", 0)
    et = c.step("Lateral strain", "ε_{lat} = δb / b", f"= {g(dt)} / {g(b)}", dt / b, "", 6)
    mu = c.step("Poisson's ratio", "μ = lateral strain / longitudinal strain", f"= {et:.6f} / {el:.5f}", et / el, "", 3)
    c.answer("Young's modulus E", E, "N/mm²", 0)
    c.answer("Young's modulus E", E / 1000, "GPa", 1)
    c.answer("Poisson's ratio μ", mu, "", 3)
    c.check("Reproduce the contraction: δL = P L / (A E)", P * gl / (b * b * E), dl, 1e-9)
    c.check("Reproduce the lateral change: δb = μ ε b", mu * el * b, dt, 1e-9)


@calc("SOM-S23-Q4e", "Minimum external diameter of a hollow shaft (3/5)")
def som_4e(c):
    T, tau, th, L, G, k = 61.5e6, 63.0, 1.4, 3000.0, 84e3, 3 / 5
    c.given("Maximum torque T", 61.5, "kN·m", "= 61.5 × 10⁶ N·mm")
    c.given("Shear stress limit τ", tau, "N/mm²", "= 63 MPa")
    c.given("Twist limit θ", th, "° in 3 m", "= 1.4 × π/180 rad")
    c.given("Diameter ratio d/D", "3/5 = 0.6", "")
    c.given("G", 84, "GPa", "= 84 000 N/mm²")
    f = 1 - k**4
    c.step("Factor (1 − k⁴)", "1 − (d/D)⁴", f"= 1 − 0.6⁴", f, "", 4)
    D1 = c.step("(a) From strength:  T = (π/16) τ D³ (1 − k⁴)", "D = [16 T / (π τ (1 − k⁴))]^{1/3}", f"= [16 × {g(T)} / (π × {g(tau)} × {f:.4f})]^{{1/3}}", (16 * T / (PI * tau * f)) ** (1 / 3), "mm")
    thr = th * PI / 180
    J = c.step("(b) Polar MI needed for twist", "J = T L / (G θ)", f"= ({g(T)} × {g(L)}) / ({g(G)} × {thr:.6f})", T * L / (G * thr), "mm⁴", 0)
    D2 = c.step("Diameter from  J = (π/32) D⁴ (1 − k⁴)", "D = [32 J / (π (1 − k⁴))]^{1/4}", f"= [32 × {J:.4e} / (π × {f:.4f})]^{{1/4}}", (32 * J / (PI * f)) ** 0.25, "mm")
    D = max(D1, D2)
    c.answer("Minimum external diameter (larger of the two)", D, "mm")
    c.answer("Internal diameter d = 0.6 D", 0.6 * D, "mm")
    c.check_le("Shear stress at the adopted D does not exceed 63 N/mm²", 16 * T / (PI * D**3 * f), tau)
    Jd = PI / 32 * D**4 * f
    c.check("Twist at D equals 1.4° (stiffness governs)", T * L / (G * Jd) * 180 / PI, th, 1e-9)


@calc("SOM-S23-Q5a", "Compound tube of steel and brass")
def som_5a(c):
    Es, Eb, P, L = 2e5, 1e5, 900e3, 140.0
    c.given("Steel tube", "140 mm ID, 160 mm OD", "")
    c.given("Brass tube", "160 mm ID, 180 mm OD", "")
    c.given("Length of each tube", L, "mm", "as printed")
    c.given("Axial load P", 900, "kN")
    c.given("E_{s}, E_{br}", "2 × 10⁵, 1 × 10⁵", "N/mm²")
    As = c.step("Area of steel", "A_{s} = π (160² − 140²) / 4", "", PI * (160**2 - 140**2) / 4, "mm²")
    Ab = c.step("Area of brass", "A_{b} = π (180² − 160²) / 4", "", PI * (180**2 - 160**2) / 4, "mm²")
    r = Es / Eb
    sb = c.step("Equal strain ⇒ σ_{s} = (E_{s}/E_{br}) σ_{b} = 2 σ_{b};  P = σ_{s}A_{s} + σ_{b}A_{b}", "σ_{b} = P / (2 A_{s} + A_{b})", f"= {g(P)} / (2 × {As:.2f} + {Ab:.2f})", P / (r * As + Ab), "N/mm²")
    ss = c.step("Stress in steel", "σ_{s} = 2 σ_{b}", f"= 2 × {sb:.3f}", r * sb, "N/mm²")
    Ps = c.step("Load carried by steel", "P_{s} = σ_{s} A_{s}", f"= {ss:.3f} × {As:.2f}", ss * As / 1e3, "kN")
    Pb = c.step("Load carried by brass", "P_{b} = σ_{b} A_{b}", f"= {sb:.3f} × {Ab:.2f}", sb * Ab / 1e3, "kN")
    dl = c.step("Shortening of the tubes", "δ = σ_{s} L / E_{s}", f"= {ss:.3f} × {g(L)} / {g(Es)}", ss * L / Es, "mm", 4)
    c.answer("Stress in steel", ss, "N/mm²")
    c.answer("Stress in brass", sb, "N/mm²")
    c.answer("Load carried by steel", Ps, "kN")
    c.answer("Load carried by brass", Pb, "kN")
    c.answer("Shortening", dl, "mm", 4)
    c.check("P_{s} + P_{b} = 900 kN", Ps + Pb, 900.0, 1e-9)
    c.check("Strain in brass = strain in steel", sb / Eb, ss / Es, 1e-9)
    c.note("The question gives the tube length as 140 mm (same as the steel ID); it is used as printed. Stresses and loads do not depend on length.")


@calc("SOM-S23-Q5b", "Overhanging beam: SF, BM and contraflexure")
def som_5b(c):
    c.given("Span AB", 5, "m", "A at 0, D at 2 m, B at 5 m")
    c.given("Overhang BC", 2, "m", "C at 7 m")
    c.given("Point loads", "5 kN at D (2 m) and 5 kN at C (7 m)", "")
    c.given("UDL", "8 kN/m over the whole beam AC", "", "total 56 kN at 3.5 m")
    Rb = c.step("Moments about A", "R_{B} × 5 = 5×2 + 56×3.5 + 5×7", "= 10 + 196 + 35 = 241", 241 / 5, "kN", 2)
    Ra = c.step("Vertical equilibrium", "R_{A} = 5 + 56 + 5 − R_{B}", f"= 66 − {Rb:.2f}", 66 - Rb, "kN", 2)
    sfs = [("A (right)", Ra), ("D (left)", Ra - 16), ("D (right)", Ra - 16 - 5), ("B (left)", Ra - 40 - 5), ("B (right)", Ra - 45 + Rb), ("C (left)", Ra - 45 + Rb - 16), ("C (right)", Ra - 45 + Rb - 16 - 5)]
    for k, v in sfs:
        c.step(f"SF at {k}", "", "", v, "kN", 2)
    MD = c.step("BM at D", "M_{D} = R_{A} × 2 − 8 × 2²/2", f"= {Ra:.1f} × 2 − 16", Ra * 2 - 16, "kN·m", 2)
    MB = c.step("BM at B", "M_{B} = R_{A} × 5 − 5 × 3 − 8 × 5²/2", f"= {Ra:.1f} × 5 − 15 − 100", Ra * 5 - 15 - 100, "kN·m", 2)
    MC = c.step("BM at C", "M_{C}", "free end, no couple", 0.0, "kN·m", 2)
    # BM between D and B (x from A): M = Ra x - 5(x-2) - 4 x^2 = 0
    a_, b_, c_ = -4.0, Ra - 5.0, 10.0
    disc = b_ * b_ - 4 * a_ * c_
    xc = c.step("Point of contraflexure (between D and B): M = 17.8x − 5(x−2) − 4x² = 0", "4x² − 12.8x − 10 = 0,  x = [12.8 + √(12.8² + 160)] / 8", f"= (12.8 + √{disc:.2f}) / 8", (-b_ - math.sqrt(disc)) / (2 * a_), "m from A", 3)
    c.answer("R_{A}", Ra, "kN")
    c.answer("R_{B}", Rb, "kN")
    c.answer("Maximum sagging BM (at D)", MD, "kN·m")
    c.answer("Maximum hogging BM (at B)", MB, "kN·m")
    c.answer("Point of contraflexure from A", xc, "m", 3)
    bm = Beam(7, 0, 5, points=[(2, 5), (7, 5)], udls=[(0, 7, 8)])
    c.check("R_{A} from the beam solver", bm.Ra, Ra, 1e-9)
    c.check("R_{B} from the beam solver", bm.Rb, Rb, 1e-9)
    c.check("BM at B from the beam solver", bm.bm(5), MB, 1e-9)
    c.check("BM at D from the beam solver", bm.bm(2), MD, 1e-9)
    c.check("BM at the free end C is zero", bm.bm(7), 0.0, 0, 1e-9)
    c.check("Contraflexure from the beam solver", bm.contraflexure()[0], xc, 1e-6)


@calc("SOM-S23-Q5c", "Hollow square section: shear stress ratio")
def som_5c(c):
    Bo, t, F = 100.0, 20.0, 75e3
    Bi = Bo - 2 * t
    c.given("Outer square", "100 × 100", "mm")
    c.given("Thickness t", t, "mm", "inner square 60 × 60 mm")
    c.given("Shear force F", 75, "kN")
    I = c.step("MI about NA", "I = (B⁴ − b⁴) / 12", f"= ({g(Bo)}⁴ − {g(Bi)}⁴) / 12", (Bo**4 - Bi**4) / 12, "mm⁴", 0)
    A = c.step("Area", "A = B² − b²", f"= {g(Bo)}² − {g(Bi)}²", Bo**2 - Bi**2, "mm²", 0)
    tav = c.step("Average shear stress", "τ_{avg} = F / A", f"= {g(F)} / {A:.0f}", F / A, "N/mm²", 3)
    Qna = Bo * (Bo / 2) * (Bo / 4) - Bi * (Bi / 2) * (Bi / 4)
    c.step("First moment of area above NA", "A ȳ = 100×50×25 − 60×30×15", "= 125 000 − 27 000", Qna, "mm³", 0)
    tmax = c.step("Maximum shear stress (at NA, width 2t = 40 mm)", "τ_{max} = F A ȳ / (I × 2t)", f"= {g(F)} × {Qna:.0f} / ({I:.0f} × 40)", F * Qna / (I * 2 * t), "N/mm²", 3)
    ratio = c.step("Ratio", "τ_{max} / τ_{avg}", f"= {tmax:.3f} / {tav:.3f}", tmax / tav, "", 3)
    Qf = Bo * t * (Bi / 2 + t / 2)
    t_fl = c.step("τ at the level where flange meets web, width 100 mm", "τ = F Q / (I b),  Q = 100×20×40 = 80 000", f"= {g(F)} × {Qf:.0f} / ({I:.0f} × 100)", F * Qf / (I * Bo), "N/mm²", 3)
    t_wb = c.step("τ just inside the web, width 40 mm", "τ = F Q / (I b)", f"= {g(F)} × {Qf:.0f} / ({I:.0f} × 40)", F * Qf / (I * 2 * t), "N/mm²", 3)
    c.answer("τ_{max} (at NA)", tmax, "N/mm²", 3)
    c.answer("τ_{avg}", tav, "N/mm²", 3)
    c.answer("Ratio τ_{max} / τ_{avg}", ratio, "", 3)
    ys = np.linspace(-Bo / 2, Bo / 2, 20001)
    tot = 0.0
    for i in range(len(ys) - 1):
        ay = abs((ys[i] + ys[i + 1]) / 2)
        if ay >= Bi / 2:                       # flange part: full width
            b, q = Bo, Bo * (Bo / 2 - ay) * (Bo / 2 + ay) / 2
        else:                                  # web part: two walls
            b, q = 2 * t, Bo * t * (Bi / 2 + t / 2) + 2 * t * (Bi / 2 - ay) * (Bi / 2 + ay) / 2
        tot += F * q / (I * b) * b * (ys[i + 1] - ys[i])
    c.check("Integral of τ over the section area equals F (numerical)", tot, F, 1e-4)


@calc("SOM-S23-Q6a", "T-section simply supported beam: maximum span")
def som_6a(c):
    bf, tf, dw, tw, sig, w = 110.0, 10.0, 100.0, 10.0, 150.0, 10.0
    c.given("T-section", "110 × 110 × 10", "mm", "flange 110 × 10 at top; web 10 × 100")
    c.given("UDL w", w, "kN/m", "= 10 N/mm")
    c.given("Permissible stress σ", sig, "N/mm²")
    A1, y1 = bf * tf, tf / 2
    A2, y2 = dw * tw, tf + dw / 2
    yt = c.step("Centroid from top", "ȳ = (A₁y₁ + A₂y₂) / (A₁ + A₂)", f"= ({g(A1)}×{g(y1)} + {g(A2)}×{g(y2)}) / ({g(A1)} + {g(A2)})", (A1 * y1 + A2 * y2) / (A1 + A2), "mm", 3)
    yb = c.step("Distance of bottom fibre", "y_{b} = 110 − ȳ", f"= 110 − {yt:.3f}", 110 - yt, "mm", 3)
    I = c.step("MI about NA", "I = [b₁t₁³/12 + A₁(ȳ − y₁)²] + [t₂d₂³/12 + A₂(y₂ − ȳ)²]",
               f"= [{bf*tf**3/12:.1f} + {A1}×{yt-y1:.3f}²] + [{tw*dw**3/12:.1f} + {A2}×{y2-yt:.3f}²]",
               bf * tf**3 / 12 + A1 * (yt - y1)**2 + tw * dw**3 / 12 + A2 * (y2 - yt)**2, "mm⁴", 0)
    Zb = c.step("Section modulus (critical = bottom, tension)", "Z = I / y_{b}", f"= {I:.0f} / {yb:.3f}", I / yb, "mm³", 0)
    M = c.step("Maximum BM", "M = σ Z", f"= {g(sig)} × {Zb:.0f}", sig * Zb, "N·mm", 0)
    L = c.step("Span:  M = w L² / 8", "L = √(8 M / w)", f"= √(8 × {M:.0f} / {g(w)})", math.sqrt(8 * M / w) / 1000, "m", 3)
    st = M * yt / I
    c.step("Maximum compressive stress at top fibre", "σ_{c} = M y_{t} / I", f"= {M:.0f} × {yt:.3f} / {I:.0f}", st, "N/mm²", 2)
    c.answer("Maximum span", L, "m", 3)
    c.answer("Stress at top fibre (compression)", st, "N/mm²", 2)
    c.answer("Stress at bottom fibre (tension)", sig, "N/mm²", 2)
    # second method: numerical centroid and I by fine strips
    ys = np.arange(0.005, 110, 0.01)
    wd = np.where(ys < tf, bf, tw)
    dA = wd * 0.01
    yc = (ys * dA).sum() / dA.sum()
    In = (wd * 0.01 * (ys - yc) ** 2).sum()
    c.check("Centroid from numerical strip integration", yc, yt, 1e-5)
    c.check("I from numerical strip integration", In, I, 1e-4)


@calc("SOM-S23-Q6b", "Hollow shaft transmitting 562.5 kW at 100 rpm")
def som_6b(c):
    Pk, N, tau, th, L, G, k = 562.5e3, 100.0, 60.0, 1.3, 2500.0, 9e4, 0.4
    c.given("Power P", 562.5, "kW")
    c.given("Speed N", N, "rpm")
    c.given("d/D", k, "", "internal diameter 40 % of external")
    c.given("τ limit", tau, "N/mm²")
    c.given("Twist limit", th, "° in 2.5 m")
    c.given("T_{max} / T_{mean}", 1.25, "")
    c.given("G", G, "N/mm²")
    Tm = c.step("Mean torque", "T_{mean} = 60 P / (2π N)", f"= 60 × {g(Pk)} / (2π × {g(N)})", 60 * Pk / (2 * PI * N), "N·m", 1)
    Tx = c.step("Maximum torque", "T_{max} = 1.25 T_{mean}", f"= 1.25 × {Tm:.1f}", 1.25 * Tm, "N·m", 1)
    T = Tx * 1000.0
    f = 1 - k**4
    c.step("Factor (1 − k⁴)", "1 − 0.4⁴", "", f, "", 4)
    D1 = c.step("(a) Strength:  T = (π/16) τ D³ (1 − k⁴)", "D = [16 T / (π τ (1 − k⁴))]^{1/3}", f"= [16 × {T:.0f} / (π × {g(tau)} × {f:.4f})]^{{1/3}}", (16 * T / (PI * tau * f)) ** (1 / 3), "mm")
    thr = th * PI / 180
    J = c.step("(b) Stiffness:  J = T L / (G θ)", "J", f"= ({T:.0f} × {g(L)}) / ({g(G)} × {thr:.6f})", T * L / (G * thr), "mm⁴", 0)
    D2 = c.step("Diameter from J = (π/32) D⁴ (1 − k⁴)", "D = [32 J / (π (1 − k⁴))]^{1/4}", f"= [32 × {J:.4e} / (π × {f:.4f})]^{{1/4}}", (32 * J / (PI * f)) ** 0.25, "mm")
    D = max(D1, D2)
    c.answer("External diameter (larger value)", D, "mm")
    c.answer("Internal diameter d = 0.4 D", k * D, "mm")
    c.check("Stress at D from strength equals 60 N/mm² (strength governs)", 16 * T / (PI * D**3 * f), tau, 1e-9)
    c.check_le("Twist at D does not exceed 1.3°", T * L / (G * PI / 32 * D**4 * f) * 180 / PI, th)
    c.check("T_{mean} from P = T ω", Tm * 2 * PI * N / 60, Pk, 1e-9)
    c.note("T_{max} is used for both the strength and the twist condition.")


@calc("SOM-S23-Q6c", "C-clamp section for P = 27 kN")
def som_6c(c):
    P, e, sig = 27e3, 144.0, 100.0
    c.given("Load P", 27, "kN")
    c.given("Distance of load line from centroidal axis e", e, "mm")
    c.given("Section: depth b = 2t, thickness t", "b = 2t", "")
    c.given("Allowable stress", sig, "N/mm²")
    c.say("Direct tension P/A plus bending P e / Z:  σ_{max} = P/(b t) + 6 P e/(t b²)  with b = 2t")
    c.say("A = 2t²,  Z = t b²/6 = 2t³/3,  so  σ = 13 500 / t² + 5 832 000 / t³  = 100")
    f = lambda t: P / (2 * t * t) + P * e / (2 * t**3 / 3)
    lo, hi = 1.0, 500.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if f(mid) > sig:
            lo = mid
        else:
            hi = mid
    t = c.step("Solve 100 t³ − 13 500 t − 5 832 000 = 0 for t", "t", "(trial and error / Newton)", lo, "mm", 2)
    tr = math.ceil(t)
    c.step("Adopt (rounded up)", "t", "", float(tr), "mm", 0)
    c.step("Width b = 2t", "b", "", 2.0 * tr, "mm", 0)
    st = f(tr)
    c.step("Check: stress at adopted section", "σ = P/A + P e/Z", f"= {P/(2*tr*tr):.3f} + {P*e/(2*tr**3/3):.3f}", st, "N/mm²", 2)
    c.answer("Thickness t", float(tr), "mm", 0)
    c.answer("Width b = 2t", 2.0 * tr, "mm", 0)
    c.check("Cubic residual at exact root", 100 * t**3 - 13500 * t - 5832000, 0.0, 0, 1e-3)
    c.check_le("Stress at the adopted section does not exceed 100 N/mm²", st, sig)
