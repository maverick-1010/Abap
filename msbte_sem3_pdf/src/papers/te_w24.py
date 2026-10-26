from dsl import *

p = Paper("TE-W24", "313310", "Thermal Engineering", "TE", "W24", "Winter 2024", "K-scheme", "3 Hours", 70, "12425",
          "Thermal_Engineering_Winter_2024_Question_Paper_First_K_Scheme_Paper.pdf", 3)

C_LAW = "Basic concepts and laws of thermodynamics"
C_GAS = "Perfect gases and gas processes"
C_STM = "Properties of steam"
C_BOI = "Steam boilers"
C_TUR = "Steam turbines"
C_PLT = "Steam power plant, condensers and cooling towers"
C_ICE = "Air standard cycles and I.C. engines"
C_HT = "Heat transfer and heat exchangers"

# ------------------------------------------------------------------ Q1
p.group(1, "Attempt any FIVE of the following:", 10, 5)
p.q("a", "Define Zeroth law of thermodynamics.", "zeroth-law", C_LAW, [
    H("Zeroth law"),
    P("<b>Statement:</b> If two bodies (systems) are each in thermal equilibrium with a third body, then they are also in thermal equilibrium with each other."),
    P("That is, if A is in equilibrium with C and B is in equilibrium with C, then A and B are in equilibrium with each other (their temperatures are equal)."),
    P("<b>Use:</b> This law is the basis of temperature measurement – the third body is the thermometer."),
    MS(("Statement", 1), ("Explanation / example", 1))])
p.q("b", "Define Dryness fraction of steam.", "dryness-fraction", C_STM, [
    P("<b>Dryness fraction (x)</b> is the ratio of the mass of dry steam present in a given mass of wet steam to the total mass of the wet steam."),
    F("x = m_{g} / (m_{g} + m_{f})"),
    P("where m_{g} = mass of dry (vapour) steam and m_{f} = mass of water particles in suspension. For dry saturated steam x = 1; for saturated water x = 0."),
    MS(("Definition", 1), ("Formula with meaning of terms", 1))])
p.q("c", "What is universal gas constant? State it’s unit.", "universal-gas-constant", C_GAS, [
    P("<b>Universal gas constant (R_{u})</b> is the product of the molecular mass (M) of a gas and its characteristic gas constant (R). Its value is the same for all gases."),
    F("R_{u} = M × R = 8.314 kJ/kmol K  (= 8314 J/kmol K)"),
    P("<b>Unit:</b> kJ/kmol K (or J/kmol K)."),
    MS(("Definition", 1), ("Value and unit", 1))])
p.q("d", "State the Datton’s Law of partial pressure.", "dalton-law", C_GAS, [
    P("<b>Dalton’s law:</b> The total pressure exerted by a mixture of non-reacting gases is equal to the sum of the partial pressures of the individual gases."),
    F("p = p_{1} + p_{2} + p_{3} + …"),
    P("<b>Partial pressure</b> of a gas is the pressure it would exert if it alone occupied the whole volume of the mixture at the same temperature."),
    MS(("Statement", 1), ("Equation / partial pressure", 1))])
p.q("e", "Write basic function of condenser.", "condenser-function", C_PLT, [
    B("A condenser <b>condenses the exhaust steam</b> from the turbine into water by removing its latent heat with cooling water.",
      "It creates a <b>low pressure (vacuum)</b> at the turbine exhaust, so the pressure drop across the turbine increases and the work output and efficiency increase.",
      "The condensate is pure water and is reused as <b>feed water</b> for the boiler."),
    MS(("Function – condensing the steam", 1), ("Vacuum / feed water recovery", 1))])
p.q("f", "Define Thermal conductivity. Give it’s unit.", "thermal-conductivity", C_HT, [
    P("<b>Thermal conductivity (k)</b> is the quantity of heat that flows per second through a unit area of a material of unit thickness when a unit temperature difference is maintained between its two faces."),
    F("k = Q L / (A ΔT)"),
    P("<b>Unit:</b> W/m K (or W/m °C)."),
    MS(("Definition", 1), ("Unit", 1))])
p.q("g", "Define mean effective pressure for I.C. Engine.", "mean-effective-pressure", C_ICE, [
    P("<b>Mean effective pressure (m.e.p.)</b> is the hypothetical constant pressure which, acting on the piston during the whole working stroke, would produce the same net work as is actually produced by the engine cycle."),
    F("m.e.p. = Net work done per cycle / Swept volume = W_{net} / V_{s}"),
    P("<b>Unit:</b> bar or N/m²."),
    MS(("Definition", 1), ("Formula and unit", 1))])

# ------------------------------------------------------------------ Q2
p.group(2, "Attempt any THREE of the following:", 12, 3)
p.q("a", "Prove that (COP)Heat pump = (COP)Refrigerator + 1", "cop-hp-refrigerator", C_LAW, [
    P("Consider a reversible cycle working as a refrigerator or as a heat pump. Let Q_{2} = heat absorbed from the low-temperature body, Q_{1} = heat rejected to the high-temperature body, and W = work supplied."),
    FIG("te_blocks_rhp", "Refrigerator and heat pump (block diagram)"),
    P("By the first law for the cycle:"),
    F("W = Q_{1} − Q_{2}"),
    F("(COP)_{R} = Refrigerating effect / Work = Q_{2} / W = Q_{2} / (Q_{1} − Q_{2})"),
    F("(COP)_{HP} = Heat delivered / Work = Q_{1} / W = Q_{1} / (Q_{1} − Q_{2})"),
    P("Now write Q_{1} = Q_{2} + (Q_{1} − Q_{2}):"),
    F("(COP)_{HP} = [Q_{2} + (Q_{1} − Q_{2})] / (Q_{1} − Q_{2}) = Q_{2}/(Q_{1} − Q_{2}) + (Q_{1} − Q_{2})/(Q_{1} − Q_{2})"),
    F("<b>(COP)_{HP} = (COP)_{R} + 1</b>        Hence proved."),
    MS(("Neat block diagram", 1), ("Definitions of COP", 1), ("Steps of proof", 2))])
p.q("b", "State Kelvin-plank and clausius statement of second law of thermodynamics.", "second-law-statements", C_LAW, [
    P("<b>Kelvin–Planck statement:</b> It is impossible to construct a device that, operating in a cycle, produces no effect other than the transfer of heat from a single reservoir and the performance of an equal amount of work. (In other words, no heat engine can have 100 % efficiency; some heat must be rejected to a sink.)"),
    P("<b>Clausius statement:</b> It is impossible to construct a device that, operating in a cycle, produces no effect other than the transfer of heat from a colder body to a hotter body. (Heat cannot flow from cold to hot by itself; external work is needed, as in a refrigerator.)"),
    MS(("Kelvin–Planck statement", 2), ("Clausius statement", 2))])
p.q("c", "Represent Isobaric process and Isochoric process on P-V and T-S diagram.", "process-pv-ts", C_GAS, [
    FIG("te_iso_processes", "Isobaric and isochoric processes on P-V and T-S diagrams"),
    T(["Item", "Isobaric (p = constant)", "Isochoric (V = constant)"], [
        ["Law", "V / T = constant", "p / T = constant"],
        ["Work done", "W = p (V_{2} − V_{1})", "W = 0"],
        ["Heat transfer", "Q = m C_{p} (T_{2} − T_{1})", "Q = m C_{v} (T_{2} − T_{1})"],
        ["Change in U", "m C_{v} (T_{2} − T_{1})", "m C_{v} (T_{2} − T_{1})"]], [1.2, 2, 2]),
    MS(("Isobaric: P-V and T-S diagrams", 1), ("Isochoric: P-V and T-S diagrams", 1), ("Relations / explanation", 2))])
p.q("d", "A volume of 0.5 m3 of gas at a pressure of 10 bar and 200°C is expanded in a cylinder to 1.2 m3 at a constant pressure. Calculate the amount of workdone by the gas and the increase in internal energy. Assume (Cp = 1.005 kJ/kg K and Cv = 0.712 kJ/kg K).",
    "gas-numerical", C_GAS, [
        P("The mass of gas is not given, so it is found from the characteristic gas equation."),
        NUM("TE-W24-Q2d"),
        MS(("Given data and R = C_{p} − C_{v}", 1), ("Mass of gas and final temperature", 1), ("Work done", 1), ("Increase in internal energy", 1))],
    qtype="numerical")

# ------------------------------------------------------------------ Q3
p.group(3, "Attempt any THREE of the following:", 12, 3)
p.q("a", "A vessel of 0.03 m3 capacity contains gas at 350 kN/m2. pressure and 35°C temperature. Determine the mass of the gas in the vessel. If the pressure of this gas is increased to 1.05 × 10^{6} N/m2 while the volume remains constant, what will be the temperature of the gas? Take R = 290 J/kg K for the gas.",
    "gas-numerical", C_GAS, [NUM("TE-W24-Q3a"),
                             MS(("Given data / unit conversion", 1), ("Mass of gas", 1), ("Final temperature (p/T = constant)", 1), ("Answer with units", 1))],
    qtype="numerical")
p.q("b", "Explain construction and working of surface condenser with neat sketch.", "surface-condenser", C_PLT, [
    FIG("te_surface_condenser", "Surface condenser (two-pass, shell and tube type)"),
    H("Construction"),
    B("A <b>closed cylindrical shell</b> contains a large number of small-diameter brass tubes held between two tube plates.",
      "Cooling water flows <b>inside the tubes</b>; the exhaust steam from the turbine enters at the top of the shell and flows <b>outside the tubes</b>.",
      "Water boxes at the ends give a two-pass flow of cooling water. Baffles guide the steam over the tubes.",
      "A hot well at the bottom collects condensate; an air extraction pump removes air and non-condensable gases from the cold-end of the shell."),
    H("Working"),
    N("Exhaust steam enters the shell and comes in contact with the cold outer surface of the tubes.",
      "The steam gives up its latent heat to the cooling water and condenses; the volume reduces, so a vacuum is formed.",
      "The condensate collects in the hot well and is pumped to the boiler as feed water (the condensate is not mixed with cooling water).",
      "Air and other gases are drawn out by the air extraction pump to maintain the vacuum.",
      "Warm cooling water leaves from the outlet and goes to the cooling tower / river."),
    MS(("Neat sketch with labels", 2), ("Construction", 1), ("Working", 1))])
p.q("c", "Explain construction and working of forced draught cooling tower with neat sketch.", "cooling-tower", C_PLT, [
    FIG("te_cooling_tower_forced", "Forced draught (mechanical draught) cooling tower"),
    H("Construction"),
    B("A tall rectangular tower with louvres on the side or base for entry of air.",
      "A <b>fan at the air inlet (base)</b> forces air into the tower – hence the name forced draught.",
      "Inside, a <b>spray header with nozzles</b> at the top distributes hot water over the <b>fill (packing)</b> made of wooden or plastic slats. Drift eliminators at the top stop water droplets from leaving. A cold water basin is at the bottom."),
    H("Working"),
    N("Hot water from the condenser is pumped to the top and sprayed over the fill.",
      "The fan blows atmospheric air up through the fill, against the falling water (counter flow).",
      "A small part of the water evaporates, taking its latent heat from the remaining water, so the water is cooled.",
      "Cooled water collects in the basin and is pumped back to the condenser; make-up water replaces the evaporation loss; the warm moist air leaves at the top."),
    MS(("Neat sketch", 2), ("Construction", 1), ("Working", 1))])
p.q("d", "Give classification of Boiler.", "boiler-classification", C_BOI, [
    T(["Basis of classification", "Types", "Examples"], [
        ["Contents of tubes", "Fire tube boiler; Water tube boiler", "Cochran, Lancashire; Babcock & Wilcox"],
        ["Position of furnace", "Internally fired; Externally fired", "Cochran; Babcock & Wilcox"],
        ["Axis of shell", "Vertical; Horizontal; Inclined", "Cochran; Lancashire; Babcock"],
        ["Circulation of water", "Natural circulation; Forced circulation", "Babcock; La-Mont, Benson"],
        ["Pressure", "Low (below 10 bar); Medium (10–80 bar); High (above 80 bar)", "Cochran; Babcock; Benson"],
        ["Use", "Stationary; Portable (mobile) – locomotive, marine", "Lancashire; Locomotive"],
        ["Number of tubes", "Single-tube; Multi-tubular", "Simple vertical; Cochran"]], [1.4, 2.4, 2]),
    MS(("Any four bases of classification, 1 mark each (with examples)", 4))])

# ------------------------------------------------------------------ Q4
p.group(4, "Attempt any THREE of the following:", 12, 3)
p.q("a", "Define various modes of heat transfer with suitable example.", "heat-transfer-laws", C_HT, [
    FIG("te_heat_modes", "Three modes of heat transfer"),
    B("<b>Conduction:</b> transfer of heat from one part of a body to another part of the same body, or between bodies in contact, by molecular vibration without any visible motion of the material. Law: Fourier, Q = −k A dT/dx. <i>Example:</i> heat flows along a metal rod heated at one end; heat flow through a boiler wall.",
      "<b>Convection:</b> transfer of heat by the actual movement of the fluid particles. It may be natural (due to density difference) or forced (by a fan or pump). Law: Newton, Q = h A (T_{s} − T_{f}). <i>Example:</i> heating of water in a kettle; cooling of an engine radiator by air.",
      "<b>Radiation:</b> transfer of heat in the form of electromagnetic waves without any medium. Law: Stefan–Boltzmann, Q = σ A T⁴. <i>Example:</i> heat from the sun to the earth; heat from a furnace to boiler tubes."),
    MS(("Conduction with example", 1), ("Convection with example", 1), ("Radiation with example", 1), ("Sketch / laws", 1))])
p.q("b", "Determine the rate of heat flow through the boiler wall made of 2 cm thick steel and covered with an insulating material of 0.5 cm thick.\nK(steel) = 58 w/mk,\nK(insulation) = 0.116 w/mk.\nthe temperature at the inner and outer surfaces of the wall are 300°C and 50°C respectively.",
    "composite-wall", C_HT, [
        FIG("te_wall_layers", "Composite wall of steel and insulation", labels=[("Steel L₁ = 2 cm, k₁ = 58", 30), ("Insulation", 18)], temps=["T₁ = 300 °C", "T₂", "T₃ = 50 °C"]),
        NUM("TE-W24-Q4b"),
        MS(("Given data / sketch", 1), ("Thermal resistances", 1), ("Total resistance and formula", 1), ("Answer with units", 1))],
    qtype="numerical",
    flag=("The wall area is not given in the question.", "Area A = 1 m² is assumed, so the answer is the heat flow <b>per square metre</b> of wall. For any other area, multiply by that area."))
p.q("c", "Differentiate two stroke and four stroke I.C. engine.", "ic-engine-strokes", C_ICE, [
    T(["Sr.", "Two stroke engine", "Four stroke engine"], [
        ["1", "One working cycle is completed in two strokes (one crankshaft revolution).", "One working cycle is completed in four strokes (two crankshaft revolutions)."],
        ["2", "One power stroke in every revolution.", "One power stroke in every two revolutions."],
        ["3", "Ports (inlet, transfer, exhaust) are used; no valves.", "Inlet and exhaust valves with a cam and camshaft are used."],
        ["4", "Turning moment is more uniform; lighter flywheel.", "Turning moment is less uniform; heavier flywheel."],
        ["5", "Power output is higher for the same size (theoretically double).", "Power output is lower for the same size."],
        ["6", "Thermal efficiency is lower (some fresh charge escapes with exhaust).", "Thermal efficiency is higher."],
        ["7", "Lubrication: oil mixed with petrol; more fuel consumption.", "Separate lubrication system; less fuel consumption."],
        ["8", "Used in scooters, mopeds, small outboard motors.", "Used in cars, buses, trucks, tractors."]], [0.4, 3, 3]),
    MS(("Any four points, 1 mark each", 4))])
p.q("d", "Explain Diesel cycle with P-V and T-S diagram.", "diesel-otto-cycle", C_ICE, [
    FIG("te_cycle", "Diesel cycle", kind="diesel", legend=True),
    H("Explanation"),
    B("The Diesel cycle is the ideal air-standard cycle for the compression-ignition engine. Heat is added at <b>constant pressure</b> and rejected at constant volume.",
      "<b>1–2:</b> Isentropic (reversible adiabatic) compression of air; the volume reduces from V_{1} to V_{2}.",
      "<b>2–3:</b> Heat addition at constant pressure (fuel injected and burnt); volume increases from V_{2} to V_{3}.",
      "<b>3–4:</b> Isentropic expansion of the hot gases (power stroke).",
      "<b>4–1:</b> Heat rejection at constant volume (exhaust)."),
    H("Air standard efficiency"),
    F("η = 1 − (1 / r^{γ−1}) × [ (ρ^{γ} − 1) / (γ (ρ − 1)) ]"),
    P("where r = compression ratio = V_{1}/V_{2}, ρ = cut-off ratio = V_{3}/V_{2}, γ = C_{p}/C_{v}."),
    MS(("P-V diagram", 1), ("T-S diagram", 1), ("Processes explanation", 1), ("Efficiency formula", 1))])
p.q("e", "Determine if the steam is wet or superheated and calculate the dryness fraction or the superheated steam temperature for P = 9 bar and V = 0.30 m3/kg.",
    "steam-numerical", C_STM, [
        NUM("TE-W24-Q4e"),
        MS(("Steam table data at 9 bar", 1), ("Comparison of v with v_{g} – state of steam", 1), ("Interpolation", 1), ("Superheat temperature with unit", 1))],
    qtype="numerical",
    flag=("Steam-table values differ slightly from book to book (for example v_{g} at 9 bar is 0.2148–0.2149 m³/kg).",
          "Values were taken from the IAPWS-IF97 steam tables (checked in code). Use the values from your own steam table in the exam; the result will differ by about 1 °C."))

# ------------------------------------------------------------------ Q5
p.group(5, "Attempt any TWO of the following:", 12, 2)
p.q("a", "Write steady flow energy equation and apply it to steam turbine and steam boiler.", "sfee", C_LAW, [
    FIG("te_sfee", "Control volume for steady flow", kind="general"),
    H("Steady flow energy equation (S.F.E.E.) per kg of fluid"),
    P("For a steady flow system, the energy entering with the fluid and as heat equals the energy leaving with the fluid and as work:"),
    F("h_{1} + C_{1}²/2 + g Z_{1} + Q = h_{2} + C_{2}²/2 + g Z_{2} + W        (J/kg or kJ/kg)"),
    P("h = specific enthalpy, C = velocity, Z = height above datum, Q = heat supplied to the system, W = work done by the system."),
    H("(i) Steam turbine"),
    P("The turbine is well insulated, so Q = 0; change in potential energy is zero; kinetic energy change is small and neglected:"),
    F("W = h_{1} − h_{2}        (work output = drop in enthalpy of steam)"),
    H("(ii) Steam boiler"),
    P("No work is done (W = 0) and the changes in kinetic and potential energy are negligible:"),
    F("Q = h_{2} − h_{1}        (heat supplied = increase in enthalpy of water/steam)"),
    MS(("S.F.E.E. with meaning of terms", 2), ("Assumptions", 1), ("Steam turbine", 1.5 if False else 1), ("Steam boiler", 1), ("Sketch", 1))])
p.q("b", "Derive characteristics gas equation using Boyle’s law and Charle’s law.", "gas-equation", C_GAS, [
    FIG("te_boyle_charles", "Boyle's law and Charles' law"),
    B("<b>Boyle’s law:</b> at constant temperature the absolute pressure of a given mass of gas varies inversely with its volume: p ∝ 1/V, i.e. p V = constant.",
      "<b>Charles’ law:</b> at constant pressure the volume of a given mass of gas varies directly with its absolute temperature: V ∝ T, i.e. V / T = constant."),
    P("Let 1 kg of gas change from state 1 (p_{1}, V_{1}, T_{1}) to state 2 (p_{2}, V_{2}, T_{2}) in two steps:"),
    N("<b>Process 1–A at constant temperature T_{1}</b> to the final pressure p_{2} (Boyle’s law):  p_{1} V_{1} = p_{2} V_{A},  so  V_{A} = p_{1} V_{1} / p_{2}.",
      "<b>Process A–2 at constant pressure p_{2}</b> (Charles’ law):  V_{A} / T_{1} = V_{2} / T_{2}."),
    P("Substituting V_{A} from step 1 into step 2:"),
    F("p_{1} V_{1} / (p_{2} T_{1}) = V_{2} / T_{2}        ⇒        p_{1} V_{1} / T_{1} = p_{2} V_{2} / T_{2} = constant"),
    P("The constant is called the characteristic gas constant R (per kg). For m kg of gas:"),
    F("<b>p V = m R T</b>        (characteristic gas equation)"),
    MS(("Statement of the two laws", 1), ("Sketch", 1), ("Derivation steps", 3), ("Final equation", 1))])
p.q("c", "Explain Benson boiler with neat sketch.", "special-boilers", C_BOI, [
    FIG("te_benson", "Benson boiler (once-through, supercritical)"),
    H("Construction"),
    B("The Benson boiler is a <b>high-pressure, water-tube, once-through</b> boiler working at or above the critical pressure (about 225 bar).",
      "It has <b>no steam drum</b>. A feed pump forces water through one continuous system of tubes: economiser, radiant evaporator and superheater placed in the furnace."),
    H("Working"),
    N("At the critical pressure (221.2 bar) the latent heat of vaporisation is zero, so water changes to steam without boiling and without bubbles.",
      "Feed water from the pump is heated in the economiser, then in the evaporator tubes (radiant heating) where it turns into steam, and the steam is superheated in the superheater.",
      "The superheated steam is sent to the turbine."),
    H("Advantages"),
    B("No drum, so light in weight and less cost; quick starting.", "High efficiency; can be run at supercritical pressure.", "Tube arrangement is flexible; no scale-deposit problem in the drum."),
    MS(("Neat sketch", 2), ("Construction", 2), ("Working", 2))])

# ------------------------------------------------------------------ Q6
p.group(6, "Attempt any TWO of the following:", 12, 2)
p.q("a", "Differentiate between Impulse turbine and Reaction turbine.", "steam-turbine-theory", C_TUR, [
    T(["Sr.", "Impulse turbine", "Reaction turbine"], [
        ["1", "Steam expands completely in the nozzle; pressure drop takes place only in the fixed nozzles.", "Steam expands partly in fixed blades and partly in moving blades; pressure drops in both."],
        ["2", "Pressure of steam is constant while passing over moving blades.", "Pressure of steam falls continuously while passing over moving blades."],
        ["3", "Moving blades are symmetrical (bucket shaped).", "Moving blades are aerofoil / asymmetrical; same shape as fixed blades."],
        ["4", "Relative velocity of steam remains same (ignoring friction) over the blades.", "Relative velocity of steam increases over the moving blades."],
        ["5", "Partial admission of steam is possible.", "Full (all-round) admission of steam is required."],
        ["6", "Blade efficiency is lower; used for high-pressure stages.", "Blade efficiency is higher; used for low-pressure stages."],
        ["7", "Fewer stages, so space required is less.", "More stages, so more space is required."],
        ["8", "Examples: De-Laval, Curtis, Rateau.", "Example: Parsons turbine."]], [0.4, 3, 3]),
    MS(("Any six points, 1 mark each", 6))])
p.q("b", "Classify heat exchangers and state their applications.", "heat-exchangers", C_HT, [
    H("Classification of heat exchangers"),
    T(["Basis", "Types"], [
        ["Nature of heat exchange", "Direct contact (open) type – e.g. cooling tower, open feed water heater; Indirect contact (closed) type – recuperative (shell and tube) and regenerative"],
        ["Direction of flow", "Parallel flow; Counter flow; Cross flow"],
        ["Constructional features", "Shell and tube; Double pipe; Plate type; Finned tube (compact)"],
        ["Change of phase", "Condensers; Evaporators; Boilers (with phase change) / Heaters, coolers (no phase change)"]], [1.4, 4]),
    H("Applications"),
    B("Condenser and feed water heater in steam power plants; economiser, air pre-heater and superheater in boilers.",
      "Radiators of automobiles and oil coolers in engines.",
      "Condenser and evaporator in refrigeration and air-conditioning plants.",
      "Intercoolers in compressors; chemical, food (pasteuriser) and dairy industries."),
    MS(("Classification (any three bases)", 3), ("Applications (any three)", 3))])
p.q("c", "Define:\ni) Compression Ratio (Rc)\nii) Swept Volume (Vs)\niii) Cut off ratio.", "ic-engine-definitions", C_ICE, [
    B("<b>Compression ratio (r):</b> the ratio of the total cylinder volume when the piston is at B.D.C. to the clearance volume (volume when the piston is at T.D.C.).  r = (V_{s} + V_{c}) / V_{c}.",
      "<b>Swept volume (V_{s}):</b> the volume displaced by the piston in moving from T.D.C. to B.D.C.  V_{s} = (π/4) D² × L, where D = cylinder bore and L = stroke length.",
      "<b>Cut-off ratio (ρ):</b> in the Diesel cycle, the ratio of the volume at the end of heat addition (cut-off) to the volume at the beginning of heat addition (clearance volume).  ρ = V_{3} / V_{2}."),
    MS(("Compression ratio", 2), ("Swept volume", 2), ("Cut-off ratio", 2))])
