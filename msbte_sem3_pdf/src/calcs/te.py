"""Thermal Engineering numericals (TE-W24, TE-S25)."""
import math
from calcfw import calc, g
from iapws import IAPWS97


@calc("TE-W24-Q2d", "Constant-pressure expansion of a gas")
def te_w24_2d(c):
    V1, V2, p, t1, Cp, Cv = 0.5, 1.2, 10, 200, 1.005, 0.712
    c.given("Initial volume V₁", V1, "m³")
    c.given("Final volume V₂", V2, "m³")
    c.given("Pressure p (constant)", p, "bar", "= 10 × 100 = 1000 kPa")
    c.given("Initial temperature t₁", t1, "°C", "T₁ = 200 + 273 = 473 K")
    c.given("C_{p}", Cp, "kJ/kg K")
    c.given("C_{v}", Cv, "kJ/kg K")
    pk = p * 100.0
    T1 = t1 + 273.0
    R = c.step("Characteristic gas constant", "R = C_{p} − C_{v}", f"= {g(Cp)} − {g(Cv)}", Cp - Cv, "kJ/kg K", 3)
    m = c.step("Mass of gas", "m = p V₁ / (R T₁)", f"= ({g(pk)} × {g(V1)}) / ({g(R)} × {g(T1)})", pk * V1 / (R * T1), "kg", 4)
    W = c.step("Work done (constant pressure)", "W = p (V₂ − V₁)", f"= {g(pk)} × ({g(V2)} − {g(V1)})", pk * (V2 - V1), "kJ")
    T2 = c.step("Final temperature (V/T = constant)", "T₂ = T₁ × V₂ / V₁", f"= {g(T1)} × {g(V2)} / {g(V1)}", T1 * V2 / V1, "K")
    dU = c.step("Increase in internal energy", "ΔU = m C_{v} (T₂ − T₁)", f"= {m:.4f} × {g(Cv)} × ({T2:.2f} − {g(T1)})", m * Cv * (T2 - T1), "kJ")
    c.answer("Work done by the gas", W, "kJ")
    c.answer("Increase in internal energy", dU, "kJ")
    Q = m * Cp * (T2 - T1)
    c.check("First law: Q − W (Q = m C_{p} ΔT) equals ΔU", Q - W, dU, 1e-9)
    c.check("ΔU = (C_{v}/R) × p ΔV", (Cv / R) * pk * (V2 - V1), dU, 1e-9)


@calc("TE-W24-Q3a", "Gas in a closed vessel")
def te_w24_3a(c):
    V, p1, t1, p2, R = 0.03, 350e3, 35, 1.05e6, 290
    c.given("Volume V", V, "m³")
    c.given("Initial pressure p₁", 350, "kN/m²", "= 350 000 N/m²")
    c.given("Initial temperature t₁", t1, "°C", "T₁ = 35 + 273 = 308 K")
    c.given("Final pressure p₂", p2, "N/m²")
    c.given("Gas constant R", R, "J/kg K")
    T1 = t1 + 273.0
    m = c.step("Mass of gas", "m = p₁ V / (R T₁)", f"= ({g(p1)} × {g(V)}) / ({g(R)} × {g(T1)})", p1 * V / (R * T1), "kg", 4)
    T2 = c.step("Final temperature (V constant: p/T = constant)", "T₂ = T₁ × p₂ / p₁", f"= {g(T1)} × {g(p2)} / {g(p1)}", T1 * p2 / p1, "K")
    t2 = c.step("In °C", "t₂ = T₂ − 273", f"= {T2:.2f} − 273", T2 - 273.0, "°C")
    c.answer("Mass of gas", m, "kg", 4)
    c.answer("Final temperature", T2, "K")
    c.answer("Final temperature", t2, "°C")
    c.check("p₂ V = m R T₂ (characteristic equation at final state)", m * R * T2, p2 * V, 1e-9)


@calc("TE-W24-Q4b", "Heat flow through composite boiler wall")
def te_w24_4b(c):
    L1, k1, L2, k2, T1, T3 = 0.02, 58.0, 0.005, 0.116, 300.0, 50.0
    c.given("Steel thickness L₁", 2, "cm", "= 0.02 m")
    c.given("Steel conductivity k₁", k1, "W/m K")
    c.given("Insulation thickness L₂", 0.5, "cm", "= 0.005 m")
    c.given("Insulation conductivity k₂", k2, "W/m K")
    c.given("Inner surface temperature T₁", T1, "°C")
    c.given("Outer surface temperature T₃", T3, "°C")
    c.given("Area A", 1, "m²", "assumed – not given in the question")
    A = 1.0
    R1 = c.step("Resistance of steel", "R₁ = L₁ / (k₁ A)", f"= {g(L1)} / ({g(k1)} × 1)", L1 / (k1 * A), "K/W", 6)
    R2 = c.step("Resistance of insulation", "R₂ = L₂ / (k₂ A)", f"= {g(L2)} / ({g(k2)} × 1)", L2 / (k2 * A), "K/W", 6)
    Rt = c.step("Total resistance", "R = R₁ + R₂", f"= {R1:.6f} + {R2:.6f}", R1 + R2, "K/W", 6)
    Q = c.step("Rate of heat flow", "Q = (T₁ − T₃) / R", f"= ({g(T1)} − {g(T3)}) / {Rt:.6f}", (T1 - T3) / Rt, "W")
    c.answer("Rate of heat flow (per m² of wall)", Q, "W")
    Ti = T1 - Q * R1
    c.step("Interface temperature (for check)", "T₂ = T₁ − Q R₁", f"= {g(T1)} − {Q:.2f} × {R1:.6f}", Ti, "°C")
    c.check("Q through insulation = k₂ A (T₂ − T₃) / L₂", k2 * A * (Ti - T3) / L2, Q, 1e-9)


@calc("TE-W24-Q4e", "State of steam at 9 bar, v = 0.30 m³/kg")
def te_w24_4e(c):
    p, v = 9.0, 0.30
    sat = IAPWS97(P=p / 10, x=1)
    ts, vg = sat.T - 273.15, sat.v
    c.given("Pressure p", p, "bar")
    c.given("Specific volume v", v, "m³/kg")
    c.say(f"From steam tables at 9 bar:  t_{{s}} = {ts:.1f} °C,   v_{{g}} = {vg:.4f} m³/kg")
    c.step("Compare v with v_{g}", "v > v_{g} ?", f"{g(v)} > {vg:.4f}", None, "")
    c.say("Since v is greater than v_{g}, the steam is SUPERHEATED.")
    v300 = IAPWS97(P=p / 10, T=573.15).v
    v350 = IAPWS97(P=p / 10, T=623.15).v
    c.step("Superheat table at 9 bar, 300 °C", "v₃₀₀", "", v300, "m³/kg", 4)
    c.step("Superheat table at 9 bar, 350 °C", "v₃₅₀", "", v350, "m³/kg", 4)
    t = c.step("Interpolate for v = 0.30", "t = 300 + 50 × (v − v₃₀₀)/(v₃₅₀ − v₃₀₀)",
               f"= 300 + 50 × ({g(v)} − {v300:.4f}) / ({v350:.4f} − {v300:.4f})",
               300 + 50 * (v - v300) / (v350 - v300), "°C", 1)
    c.answer("State of steam", "Superheated", "")
    c.answer("Temperature of superheated steam", t, "°C", 1)
    c.answer("Degree of superheat", t - ts, "K", 1)
    lo, hi = 300.0, 350.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if IAPWS97(P=p / 10, T=mid + 273.15).v < v:
            lo = mid
        else:
            hi = mid
    c.check("Exact solution of v(t) = 0.30 (IAPWS-IF97) vs interpolation, within 1 °C", t, lo, 0, 1.0)
    c.note(f"Exact IF97 value: {lo:.1f} °C. Table interpolation can differ by about 1 °C from your steam table.")


@calc("TE-S25-Q4e", "Adiabatic compression of 0.17 kg of gas")
def te_s25_4e(c):
    m, V1, t1, p1, V2, p2, gam = 0.17, 0.14, 15, 1e5, 0.057, 4e5, 1.407
    c.given("Mass m", m, "kg")
    c.given("V₁", V1, "m³")
    c.given("t₁", t1, "°C", "T₁ = 15 + 273 = 288 K")
    c.given("p₁", 1, "bar", "= 10⁵ N/m²")
    c.given("V₂", V2, "m³")
    c.given("p₂", 4, "bar", "= 4 × 10⁵ N/m²")
    c.given("γ", gam, "")
    T1 = t1 + 273.0
    R = c.step("(i) Gas constant", "R = p₁ V₁ / (m T₁)", f"= ({g(p1)} × {g(V1)}) / ({g(m)} × {g(T1)})", p1 * V1 / (m * T1), "J/kg K")
    Cv = c.step("(ii) Specific heat at constant volume", "C_{v} = R / (γ − 1)", f"= {R:.2f} / ({g(gam)} − 1)", R / (gam - 1) / 1000, "kJ/kg K", 4)
    Cp = c.step("Specific heat at constant pressure", "C_{p} = γ C_{v}", f"= {g(gam)} × {Cv:.4f}", gam * Cv, "kJ/kg K", 4)
    T2 = c.step("Final temperature from end state", "T₂ = p₂ V₂ / (m R)", f"= ({g(p2)} × {g(V2)}) / ({g(m)} × {R:.2f})", p2 * V2 / (m * R), "K")
    dU = c.step("(iii) Change in internal energy", "ΔU = m C_{v} (T₂ − T₁)", f"= {g(m)} × {Cv:.4f} × ({T2:.2f} − {g(T1)})", m * Cv * (T2 - T1), "kJ")
    c.answer("Gas constant R", R, "J/kg K")
    c.answer("C_{v}", Cv, "kJ/kg K", 4)
    c.answer("C_{p}", Cp, "kJ/kg K", 4)
    c.answer("Change in internal energy ΔU (increase)", dU, "kJ")
    W = (p1 * V1 - p2 * V2) / (gam - 1) / 1000
    c.check("Adiabatic: ΔU = −W, with W = (p₁V₁ − p₂V₂)/(γ − 1)", -W, dU, 1e-9)
    c.check("C_{p} − C_{v} = R", Cp - Cv, R / 1000, 1e-9)
    gimp = math.log(p2 / p1) / math.log(V1 / V2)
    c.note(f"Data check: the end states give γ(implied) = ln(p₂/p₁)/ln(V₁/V₂) = {gimp:.3f}, not 1.407. "
           f"Using T₂ from the end state (as above) is the usual method.")
    c.note(f"T₂ by the adiabatic law T₁(V₁/V₂)^(γ−1) would be {T1 * (V1 / V2) ** (gam - 1):.1f} K – "
           f"it does not agree with {T2:.1f} K, so the data are slightly inconsistent.")


@calc("TE-S25-Q5b", "Superheated steam in a closed vessel (10 bar, 300 °C)")
def te_s25_5b(c):
    V, p, t, ts, vg, hg, cps = 0.4, 10, 300, 179.9, 0.1943, 2778.0, 2.1
    c.given("Volume of vessel V", V, "m³")
    c.given("Pressure p", p, "bar")
    c.given("Temperature t", t, "°C")
    c.given("From the table: t_{s}", ts, "°C")
    c.given("v_{g}", vg, "m³/kg")
    c.given("h_{g}", hg, "kJ/kg")
    c.given("C_{p} of superheated steam", cps, "kJ/kg K")
    c.step("(i) Quality of steam", "t > t_{s} ?", f"{g(t)} °C > {g(ts)} °C", None, "")
    c.say("Steam temperature is higher than saturation temperature, so the steam is SUPERHEATED.")
    Ts, T = ts + 273.0, t + 273.0
    ds = c.step("Degree of superheat", "t − t_{s}", f"= {g(t)} − {g(ts)}", t - ts, "K", 1)
    v = c.step("(iii) Specific volume (Charles' law, p constant)", "v = v_{g} × T / T_{s}", f"= {g(vg)} × {g(T)} / {g(Ts)}", vg * T / Ts, "m³/kg", 4)
    h = c.step("Specific enthalpy of superheated steam", "h = h_{g} + C_{p} (t − t_{s})", f"= {g(hg)} + {g(cps)} × ({g(t)} − {g(ts)})", hg + cps * ds, "kJ/kg")
    m = c.step("Mass of steam in vessel", "m = V / v", f"= {g(V)} / {v:.4f}", V / v, "kg", 4)
    H = c.step("(ii) Total enthalpy", "H = m h", f"= {m:.4f} × {h:.2f}", m * h, "kJ")
    c.answer("Quality of steam", "Superheated", "")
    c.answer("Total enthalpy H", H, "kJ")
    c.answer("Specific volume v", v, "m³/kg", 4)
    c.check("m × v = V", m * v, V, 1e-9)
    c.check("Charles-law v vs IAPWS-IF97 table value at 10 bar, 300 °C (approximate method, 6 %)", v, IAPWS97(P=1.0, T=573.15).v, 0.06)
    c.note("The table in the question gives vf = 1.127; the correct value is 0.001127 m³/kg (not needed here).")


@calc("TE-S25-Q6b", "Heat transfer through brick, cork and wood wall")
def te_s25_6b(c):
    A = 5 * 3
    L = [0.100, 0.080, 0.025]
    k = [0.7, 0.05, 0.20]
    Ti, To = -5.0, 15.0
    c.given("Wall area A = 5 × 3", A, "m²")
    c.given("Brick: L₁, k₁", f"{L[0]} m, {k[0]}", "W/m °C", "k printed as kW/m°C – taken as W/m°C")
    c.given("Cork: L₂, k₂", f"{L[1]} m, {k[1]}", "W/m °C")
    c.given("Wood: L₃, k₃", f"{L[2]} m, {k[2]}", "W/m °C")
    c.given("Inner wall temperature T_{i}", Ti, "°C")
    c.given("Outer wall temperature T_{o}", To, "°C")
    Rs = [c.step(f"Resistance of layer {i + 1} per m²", f"R{i + 1} = L{i + 1} / k{i + 1}", f"= {g(L[i])} / {g(k[i])}", L[i] / k[i], "m² °C/W", 5) for i in range(3)]
    Rt = c.step("Total resistance per m²", "R = R₁ + R₂ + R₃", f"= {Rs[0]:.5f} + {Rs[1]:.5f} + {Rs[2]:.5f}", sum(Rs), "m² °C/W", 5)
    q = c.step("Heat flux", "q = (T_{o} − T_{i}) / R", f"= ({g(To)} − ({g(Ti)})) / {Rt:.5f}", (To - Ti) / Rt, "W/m²", 4)
    Q = c.step("Heat flow through the wall", "Q = q × A", f"= {q:.4f} × {g(A)}", q * A, "W", 3)
    Qh = c.step("Heat transfer per hour", "Q × 3600", f"= {Q:.3f} × 3600", Q * 3600 / 1000, "kJ/h", 1)
    T12 = c.step("Temperature at brick–cork surface", "T₁₂ = T_{i} + q R₁", f"= {g(Ti)} + {q:.4f} × {Rs[0]:.5f}", Ti + q * Rs[0], "°C", 2)
    T23 = c.step("Temperature at cork–wood surface", "T₂₃ = T₁₂ + q R₂", f"= {T12:.2f} + {q:.4f} × {Rs[1]:.5f}", T12 + q * Rs[1], "°C", 2)
    c.answer("Heat transfer per hour", Qh, "kJ/h", 1)
    c.answer("Heat flow rate", Q, "W", 2)
    c.answer("Temperature at brick–cork surface", T12, "°C")
    c.answer("Temperature at cork–wood surface", T23, "°C")
    c.check("Outer wall: T₂₃ + q R₃ = T_{o}", T23 + q * Rs[2], To, 1e-9)
