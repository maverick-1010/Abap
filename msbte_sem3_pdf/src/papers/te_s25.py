from dsl import *

p = Paper("TE-S25", "313310", "Thermal Engineering", "TE", "S25", "Summer 2025", "K-scheme", "3 Hours", 70, "24225",
          "Thermal_Engineering_Summer_2025_Question_Paper_Second_K_Scheme_Paper.pdf", 4)

C_LAW = "Basic concepts and laws of thermodynamics"
C_GAS = "Perfect gases and gas processes"
C_STM = "Properties of steam"
C_BOI = "Steam boilers"
C_TUR = "Steam turbines"
C_PLT = "Steam power plant, condensers and cooling towers"
C_ICE = "Air standard cycles and I.C. engines"
C_HT = "Heat transfer and heat exchangers"

# ------------------------------------------------------------------ Q1
p.group(1, "Attempt any FIVE of the following :", 10, 5)
p.q("a", "Define the terms:\ni) Thermodynamic System\nii) Thermodynamic Property.", "thermo-system-property", C_LAW, [
    B("<b>Thermodynamic system:</b> a definite quantity of matter or a region in space, chosen for study, which is separated from its surroundings by a boundary (real or imaginary). Types: closed, open and isolated system.",
      "<b>Thermodynamic property:</b> any measurable characteristic that describes the state (condition) of a system, such as pressure, temperature, volume, internal energy and enthalpy. Properties are of two kinds – intensive (independent of mass, e.g. p, T) and extensive (depend on mass, e.g. V, U)."),
    MS(("Thermodynamic system", 1), ("Thermodynamic property", 1))])
p.q("b", "Define the term Universal Gas Constant. State its unit.", "universal-gas-constant", C_GAS, [
    P("<b>Universal gas constant (R_{u})</b> is the product of the molecular mass (M) of a gas and its characteristic gas constant (R). It has the same value for all gases."),
    F("R_{u} = M × R = 8.314 kJ/kmol K  (= 8314 J/kmol K)"),
    MS(("Definition", 1), ("Value and unit", 1))])
p.q("c", "Define the terms:\ni) Sensible Heat\nii) Latent Heat", "sensible-latent-heat", C_STM, [
    B("<b>Sensible heat (h_{f})</b> is the heat required to raise the temperature of 1 kg of water from 0 °C to the saturation (boiling) temperature at the given pressure. It changes the temperature.",
      "<b>Latent heat (h_{fg})</b> is the heat required to convert 1 kg of water at saturation temperature into dry saturated steam at the same temperature and pressure. It changes only the phase, not the temperature."),
    MS(("Sensible heat", 1), ("Latent heat", 1))])
p.q("d", "Classify the boilers according to -\ni) Relative position of flow of water and hot gases\nii) Position of furnace.", "boiler-classification", C_BOI, [
    B("<b>(i) Relative position of flow of water and hot gases:</b> (a) Fire tube boiler – hot gases flow inside the tubes and water around them (Cochran, Lancashire, Locomotive); (b) Water tube boiler – water flows inside the tubes and hot gases outside (Babcock & Wilcox, La-Mont, Benson).",
      "<b>(ii) Position of furnace:</b> (a) Internally fired boiler – the furnace is inside the boiler shell (Cochran, Lancashire); (b) Externally fired boiler – the furnace is outside the shell (Babcock & Wilcox)."),
    MS(("Classification (i) with examples", 1), ("Classification (ii) with examples", 1))])
p.q("e", "State the Dalton's law of partial pressure.", "dalton-law", C_GAS, [
    P("<b>Dalton’s law:</b> The total pressure exerted by a mixture of non-reacting gases is equal to the sum of the partial pressures of the individual gases, each gas occupying the whole volume of the mixture at the same temperature."),
    F("p = p_{1} + p_{2} + p_{3} + …"),
    MS(("Statement", 1), ("Equation", 1))])
p.q("f", "Define the terms –\ni) Black body\nii) Abosoptivity.", "black-body-absorptivity", C_HT, [
    B("<b>Black body:</b> an ideal body which absorbs all the thermal radiation falling on it, whatever the wavelength or direction. It is also the best emitter of radiation (emissivity ε = 1).",
      "<b>Absorptivity (α):</b> the ratio of the radiant energy absorbed by a body to the total radiant energy falling on it. For a black body α = 1; for a real body α &lt; 1."),
    MS(("Black body", 1), ("Absorptivity", 1))])
p.q("g", "Classify the I.C. engines according to –\ni) Method of igniting the fuel\nii) Cycle of operation.", "ic-engine-classification", C_ICE, [
    B("<b>(i) Method of igniting the fuel:</b> Spark ignition (S.I.) engine – petrol engine, fuel ignited by a spark plug; Compression ignition (C.I.) engine – diesel engine, fuel ignited by heat of compressed air.",
      "<b>(ii) Cycle of operation:</b> Otto cycle engine (constant-volume heat addition), Diesel cycle engine (constant-pressure heat addition), Dual cycle engine (part at constant volume and part at constant pressure)."),
    MS(("Method of ignition", 1), ("Cycle of operation", 1))])

# ------------------------------------------------------------------ Q2
p.group(2, "Attempt any THREE of the following :", 12, 3)
p.q("a", "Explain the concept of Heat engine, Heat pump and Refrigerator with block diagram.", "cop-hp-refrigerator", C_LAW, [
    FIG("te_blocks", "Heat engine, refrigerator and heat pump"),
    B("<b>Heat engine:</b> a device that continuously converts heat into work while working in a cycle. It receives heat Q_{1} from a high-temperature source (T_{1}), converts part of it into work W and rejects the rest Q_{2} to a sink (T_{2}).  W = Q_{1} − Q_{2};  η = W / Q_{1} = 1 − Q_{2}/Q_{1}.",
      "<b>Refrigerator:</b> a device that works in a cycle to remove heat Q_{2} from a low-temperature space (T_{2}) and reject Q_{1} to the surroundings (T_{1}) with the help of work input W.  (COP)_{R} = Q_{2} / W.",
      "<b>Heat pump:</b> a device that works in a cycle to supply heat Q_{1} to a space to be kept warm (T_{1}) by taking Q_{2} from the cold surroundings (T_{2}) with work input W.  (COP)_{HP} = Q_{1} / W.",
      "Relation: W = Q_{1} − Q_{2} and (COP)_{HP} = (COP)_{R} + 1."),
    MS(("Heat engine – diagram and explanation", 1), ("Refrigerator – diagram and explanation", 1), ("Heat pump – diagram and explanation", 1), ("Formulae / relation", 1))])
p.q("b", "Explain the concept of flow work with neat sketch.", "flow-work", C_LAW, [
    FIG("te_flow_work", "Flow work"),
    B("<b>Flow work</b> is the work required to push a fluid element into, or out of, a control volume (an open system) against the pressure existing at the boundary.",
      "Consider a fluid element of volume V pushed into the system through a pipe of cross-section A at pressure p. Force on the element F = p × A. If the element moves a distance L, work = F × L = p A L.",
      "Since A × L = V, <b>flow work = p V</b> (for 1 kg: p v, in kJ/kg).",
      "Flow work is the reason for the term p v in enthalpy: h = u + p v."),
    MS(("Sketch", 2), ("Explanation", 1), ("Expression for flow work", 1))])
p.q("c", "Represent the isothermal process on P-V and T-S chart. State the relation to calculate the workdone during isothermal process.", "process-pv-ts", C_GAS, [
    FIG("te_isothermal", "Isothermal process on P-V and T-S diagrams"),
    B("In an isothermal process the temperature remains constant: p V = constant (Boyle’s law), so ΔU = 0 and all the heat supplied is converted into work (Q = W).",
      "On the P-V diagram it is a rectangular hyperbola; on the T-S diagram it is a horizontal straight line."),
    H("Work done"),
    F("W = p_{1} V_{1} ln (V_{2} / V_{1}) = m R T ln (V_{2} / V_{1}) = p_{1} V_{1} ln (p_{1} / p_{2})"),
    MS(("P-V diagram", 1), ("T-S diagram", 1), ("Characteristics", 1), ("Work formula", 1))])
p.q("d", "Explain the process of steam generation with the help of T-H chart.", "steam-generation", C_STM, [
    FIG("te_th_chart", "Steam generation at constant pressure on the T–h chart"),
    N("<b>0 → 1 (sensible heating):</b> water at 0 °C is heated at constant pressure; its temperature rises to the saturation temperature t_{s}. Heat added = h_{f} (sensible heat).",
      "<b>1 → 2 (evaporation):</b> further heat added at constant temperature t_{s} is the latent heat h_{fg}; the water turns into steam. In between, the mixture is <b>wet steam</b> with dryness fraction x. At point 2 all water is converted: <b>dry saturated steam</b> (x = 1).  h_{wet} = h_{f} + x h_{fg};  h_{g} = h_{f} + h_{fg}.",
      "<b>2 → 3 (superheating):</b> heating dry steam at constant pressure raises its temperature above t_{s}; this is <b>superheated steam</b>.  h_{sup} = h_{g} + C_{ps} (t_{sup} − t_{s})."),
    MS(("T-h chart with labels", 2), ("Explanation of three stages", 2))])

# ------------------------------------------------------------------ Q3
p.group(3, "Attempt any THREE of the following :", 12, 3)
p.q("a", "Represent the Rankine cycle on P-V and T-S chart. Name the various processes involved in it.", "rankine-cycle", C_PLT, [
    FIG("te_cycle", "Rankine cycle", kind="rankine", legend=True),
    T(["Process", "Name", "Where it occurs"], [
        ["1 – 2", "Reversible adiabatic (isentropic) compression", "Feed pump"],
        ["2 – 3", "Constant-pressure heat addition (water → steam → superheated steam)", "Boiler and superheater"],
        ["3 – 4", "Reversible adiabatic (isentropic) expansion", "Steam turbine"],
        ["4 – 1", "Constant-pressure heat rejection (condensation)", "Condenser"]], [0.8, 3.6, 2]),
    F("η_{Rankine} = [(h_{3} − h_{4}) − (h_{2} − h_{1})] / (h_{3} − h_{2})"),
    MS(("P-V diagram", 1), ("T-S diagram", 1), ("Names of processes", 2))])
p.q("b", "Draw the layout of steam power plant and label the following components –\ni) Boiler\nii) Turbine\niii) Condenser\niv) Generator\nv) Cooling tower\nvi) Chimney\nvii) Feed Pump\nviii) Coal Circuit",
    "steam-plant-layout", C_PLT, [
        FIG("te_steam_plant", "Layout of a steam power plant"),
        T(["Component", "Function"], [
            ["Coal circuit", "Brings coal from the store through crusher and conveyor to the furnace; ash is removed to the ash pit."],
            ["Boiler", "Burns coal and generates steam at high pressure (with superheater to give superheated steam)."],
            ["Turbine", "Converts heat energy of steam into mechanical work on the shaft."],
            ["Generator", "Coupled to the turbine; converts mechanical energy into electrical energy."],
            ["Condenser", "Condenses exhaust steam and creates vacuum at the turbine outlet."],
            ["Cooling tower", "Cools the warm cooling water coming from the condenser so that it can be reused."],
            ["Feed pump", "Pumps condensate (feed water) back to the boiler against boiler pressure."],
            ["Chimney", "Discharges flue gases to the atmosphere at a safe height."]], [1.3, 5]),
        MS(("Layout with correct flow arrows", 2), ("Labelling of the eight components", 1), ("Functions", 1))])
p.q("c", "Explain the method of velocity compounding of an impulse turbine for achieving rotor speed reduction.", "steam-turbine-theory", C_TUR, [
    FIG("te_velocity_compounding", "Velocity compounding (Curtis) – two rows of moving blades"),
    H("Need"),
    P("In a simple impulse turbine the whole pressure drop takes place in one nozzle, so the steam leaves with a very high velocity and the rotor must run at a very high speed (the optimum blade speed is u = C_{1} cos α_{1} / 2). Such high speed is not practical for bearings and reduction gearing."),
    H("Method"),
    N("The entire pressure drop of steam occurs in a set of nozzles, so steam leaves with a high velocity C_{1}.",
      "This high-velocity steam passes through the <b>first row of moving blades</b>, which absorbs only part of the kinetic energy; the steam leaves with a reduced velocity.",
      "The steam then passes through a row of <b>fixed (guide) blades</b> fixed to the casing, which only change its direction (no pressure drop) and guide it into the second row.",
      "The <b>second row of moving blades</b> (on the same rotor) absorbs more of the remaining kinetic energy. More rows can be used.",
      "The velocity is thus reduced in steps, while pressure remains constant over the blades."),
    F("Optimum blade speed  u = C_{1} cos α_{1} / (2 z),   where z = number of moving-blade rows"),
    P("So with two rows the rotor speed is only half that of a single-stage turbine for the same nozzle velocity – this achieves the <b>speed reduction</b>."),
    MS(("Sketch with pressure and velocity variation", 2), ("Explanation of method", 2))])
p.q("d", "Suggest the non mixing type and high capacity condenser for power plant. Draw its labeled sketch and explain its working in brief.", "surface-condenser", C_PLT, [
    P("The non-mixing (surface) type condenser is suitable: the steam and cooling water do not mix, so the pure condensate is reused as boiler feed water. A shell-and-tube type with large tube area gives high capacity."),
    FIG("te_surface_condenser", "Surface condenser (shell and tube, two pass)"),
    H("Working"),
    N("Exhaust steam from the turbine enters the shell at the top and flows over the outside of the tubes.",
      "Cooling water, pumped through the tubes in two passes, absorbs the latent heat of the steam and condenses it.",
      "The condensate collects in the hot well and is pumped to the boiler as feed water.",
      "An air extraction pump removes air and non-condensable gases to maintain a high vacuum."),
    MS(("Suggestion – surface condenser with reason", 1), ("Labelled sketch", 2), ("Working", 1))])

# ------------------------------------------------------------------ Q4
p.group(4, "Attempt any THREE of the following :", 12, 3)
p.q("a", "Explain the Fourier’s law and Newton’s law of cooling related to heat transfer.", "heat-transfer-laws", C_HT, [
    B("<b>Fourier’s law (conduction):</b> the rate of heat flow by conduction through a material is directly proportional to the area A normal to the direction of flow and to the temperature gradient dT/dx.",
      "<b>Newton’s law of cooling (convection):</b> the rate of heat transfer by convection from a surface to a fluid is directly proportional to the surface area A and to the temperature difference between the surface and the fluid."),
    F("Fourier:  Q = − k A (dT/dx)        k = thermal conductivity, W/m K; the minus sign shows heat flows from higher to lower temperature"),
    F("Newton:  Q = h A (T_{s} − T_{f})        h = convection heat transfer coefficient, W/m² K"),
    MS(("Fourier’s law – statement and equation", 2), ("Newton’s law of cooling – statement and equation", 2))])
p.q("b", "Suggest the type of heat exchanger required for steam power plant. Explain its working with neat label sketch.", "heat-exchangers", C_HT, [
    P("A <b>shell-and-tube heat exchanger</b> is used in a steam power plant, for example as the <b>surface condenser</b> (also as closed feed water heater). It is a non-mixing (recuperative) type of heat exchanger."),
    FIG("te_surface_condenser", "Shell-and-tube heat exchanger used as a surface condenser"),
    H("Working"),
    N("Exhaust steam (hot fluid) enters the shell and flows outside the tubes; cooling water (cold fluid) flows inside the tubes.",
      "Heat passes from the steam through the tube wall to the cooling water; the steam condenses and the water gets warmer.",
      "Condensate is collected in the hot well; the warm water goes to the cooling tower; the baffles increase the heat transfer."),
    MS(("Type of heat exchanger", 1), ("Sketch with labels", 2), ("Working", 1))])
p.q("c", "Represent the Carnot cycle on P-V and T-S diagram and label it. State its limitations.", "carnot-cycle", C_LAW, [
    FIG("te_cycle", "Carnot cycle (schematic, not to scale)", kind="carnot", legend=True),
    F("η_{Carnot} = 1 − T_{2} / T_{1}"),
    H("Limitations"),
    B("Isothermal heat transfer needs an infinitely slow process, and adiabatic reversible expansion/compression needs frictionless working – both are impossible in practice.",
      "The two isothermal processes need a very large temperature difference to be kept constant; the cycle cannot be built with a gas as a practical engine.",
      "The work ratio and mean effective pressure are very low, so a very large engine is needed for small output.",
      "Efficiency depends only on source and sink temperatures; the maximum temperature is limited by materials."),
    MS(("P-V diagram with labels", 1), ("T-S diagram with labels", 1), ("Limitations (any two)", 2))])
p.q("d", "Compare the Otto cycle with Diesel cycle on following basis -\ni) Representation on P-V and T-S Chart.\nii) Compression ratio.\niii) Heat addition\niv) Application", "diesel-otto-cycle", C_ICE, [
    FIG("te_otto_diesel", "Otto cycle (top) and Diesel cycle (bottom)"),
    T(["Basis", "Otto cycle", "Diesel cycle"], [
        ["Representation", "Two isentropics and two constant-volume lines on P-V (see top diagrams)", "Two isentropics, one constant-pressure and one constant-volume line (see bottom diagrams)"],
        ["Compression ratio", "Low: about 6 to 10", "High: about 14 to 22"],
        ["Heat addition", "At constant volume (2–3)", "At constant pressure (2–3)"],
        ["Application", "Petrol (S.I.) engines – cars, scooters, small generators", "Diesel (C.I.) engines – trucks, buses, tractors, locomotives, ships"]], [1.2, 2.6, 2.6]),
    MS(("Representation on P-V and T-S", 1), ("Compression ratio", 1), ("Heat addition", 1), ("Application", 1))])
p.q("e", "The initial volume of 0.17 kg of a certain gas was 0.14 m3 at a temperature of 15°C and a pressure of 1 bar. After adiabatic compression to 0.057m3, the pressure was found to be 4 bar.\nFind -\ni) Gas constant\nii) If ratio of specific heat is 1.407, find the value of CP and CV.\niii) Change in internal energy.",
    "gas-numerical", C_GAS, [NUM("TE-S25-Q4e"),
                             MS(("Gas constant", 1), ("C_{p} and C_{v}", 1), ("Final temperature", 1), ("Change in internal energy", 1))],
    qtype="numerical",
    flag=("The data are slightly inconsistent: with γ = 1.407 an adiabatic change from 0.14 m³ to 0.057 m³ would not give a final pressure of 4 bar (the end states imply γ = 1.54).",
          "The end-state data are used as printed (T_{2} = p_{2}V_{2}/mR); this is the usual method. The alternative T_{2} from the adiabatic law would give a different ΔU."))

# ------------------------------------------------------------------ Q5
p.group(5, "Attempt any TWO of the following :", 12, 2)
p.q("a", "Apply the steady flow energy equation to boiler. Show that the heat supplied to boiler increases the enthalpy of system.", "sfee", C_LAW, [
    FIG("te_sfee", "Boiler as a steady-flow control volume", kind="boiler"),
    H("Steady flow energy equation (per kg)"),
    F("h_{1} + C_{1}²/2 + g Z_{1} + Q = h_{2} + C_{2}²/2 + g Z_{2} + W"),
    H("Application to a boiler"),
    N("Feed water enters at state 1 and leaves as steam at state 2; the flow is steady (mass flow in = mass flow out).",
      "A boiler has no moving parts delivering work: <b>W = 0</b>.",
      "Inlet and outlet are at nearly the same level and the velocities are small: <b>ΔPE = 0</b> and <b>ΔKE ≈ 0</b>.",
      "Substituting in S.F.E.E.:  h_{1} + Q = h_{2}"),
    F("<b>Q = h_{2} − h_{1}</b>"),
    P("So the heat supplied to the boiler per kg is exactly equal to the increase in enthalpy of the working fluid. Hence heat supplied increases the enthalpy of the system.  Hence proved."),
    MS(("S.F.E.E. with terms", 2), ("Assumptions for boiler", 2), ("Derivation and conclusion", 2))])
p.q("b", "A closed vessel contains 0.4 m3 of steam at 10 bar and 300°C. Using following steam table -\ni) Identify the quality of steam.\nii) Calculate the total enthalpy of steam\niii) Find specific volume of steam.\nTake specific heat of sueperheated steam as 2.1KJ/kg K.\n\nAbsolute Pressure in bar: 10;  Temp. in °C: 179.9;  Sp. Volume (m3/kg): vf = 1.127, vg = 0.1943;  Sp. Enthalpy (kJ/kg): hf = 763.2, hg = 2778;  Sp. Entropy (kJ/kg K): sf = 2.140, sg = 6.586",
    "steam-numerical", C_STM, [NUM("TE-S25-Q5b"),
                               MS(("Quality of steam", 1), ("Specific volume", 2), ("Specific enthalpy and mass", 1), ("Total enthalpy", 2))],
    qtype="numerical",
    flag=("The table prints v_{f} = 1.127. The correct value is 0.001127 m³/kg (1.127 is in litres/kg, or the decimal is missing). \"s_{f} = 2.140\" is also not needed.",
          "v_{f}, s_{f} and s_{g} are not needed for this question, so the answer is not affected. Only t_{s}, v_{g} and h_{g} are used."))
p.q("c", "A steam power plant having power generation capacity 660 MW is to be installed where availability of water is limited. Suggest the type of cooling tower required for this plant. Draw the neat labeled sketch and explain its working principle in brief.",
    "cooling-tower", C_PLT, [
        H("Type suggested: natural draught (hyperbolic) cooling tower"),
        B("A 660 MW plant rejects a very large quantity of heat, so a large-capacity tower is needed. A natural draught tower handles very large water flows with no fan power.",
          "It is a <b>recirculating (closed-loop) tower</b>: the cooled water is used again and again. Only the evaporation, drift and blow-down loss (about 1–2 % of the flow) has to be made up – this suits a site with limited water, compared with once-through cooling.",
          "It has low running cost (no fan, no motor) and high reliability."),
        FIG("te_cooling_tower_natural", "Natural draught (hyperbolic) cooling tower"),
        H("Working principle"),
        N("Hot water from the condenser is carried to the distribution system near the base of the tower and sprayed over the fill.",
          "Atmospheric air enters through the open space at the base. Air in the tower is warm and humid, so it is lighter than the outside air; the density difference causes a <b>natural draught</b> (chimney effect) in the tall hyperbolic shell.",
          "As air rises through the falling water, a small part of the water evaporates, taking latent heat from the rest and cooling it.",
          "The cooled water falls into the basin and is pumped back to the condenser; the warm moist air leaves from the top."),
        MS(("Selection of the type with reasons", 2), ("Neat labelled sketch", 2), ("Working principle", 2))])

# ------------------------------------------------------------------ Q6
p.group(6, "Attempt any TWO of the following :", 12, 2)
p.q("a", "Explain with neat label sketch the construction and working of Lamont boiler.", "special-boilers", C_BOI, [
    FIG("te_lamont", "La-Mont boiler (forced circulation, water tube)"),
    H("Construction"),
    B("The La-Mont boiler is a <b>high-pressure, water-tube, forced-circulation</b> boiler (up to about 170 bar).",
      "Main parts: a steam drum, a <b>circulating pump</b> that takes water from the drum, a distribution header, a bank of evaporator tubes in the furnace, an economiser, a superheater, and a feed pump."),
    H("Working"),
    N("Feed water passes through the economiser and enters the steam drum.",
      "The circulating pump takes water from the drum (through the downcomer) and forces it through the distribution header into the evaporator tubes.",
      "Heat from the furnace converts part of the water into steam; the mixture of steam and water returns to the drum, where steam is separated.",
      "The dry steam goes to the superheater and then to the turbine; the remaining water is circulated again."),
    H("Advantages"),
    B("Rapid steam generation and quick starting; tubes can be arranged freely.", "Forced circulation prevents overheating of tubes and scale deposit."),
    MS(("Neat sketch with labels", 2), ("Construction", 2), ("Working", 2))])
p.q("b", "A 100 mm thick brick wall measuring 5m × 3 m is insulated externally by cork 80 mm thick which is further protected by wood 25 mm thick. If the interior wall temperature is - 5°C and outer wall temperature is 15°C. Determine the heat transfer through the wall per hour. Take thermal conductivities of brick, cork and wood as 0.7, 0.05, 0.20 KW/m°C respectively. Also find temperature at inner surfaces.",
    "composite-wall", C_HT, [
        FIG("te_wall_layers", "Brick, cork and wood wall", labels=[("Brick 100 mm", 26), ("Cork 80 mm", 22), ("Wood 25 mm", 14)], temps=["T_i = −5 °C", "T₁₂", "T₂₃", "T_o = 15 °C"], rising=True),
        NUM("TE-S25-Q6b"),
        MS(("Given data / sketch", 1), ("Resistances and total resistance", 2), ("Heat transfer per hour", 2), ("Temperatures at the two inner surfaces", 1))],
    qtype="numerical",
    flag=("The thermal conductivities are printed as \"0.7, 0.05, 0.20 KW/m°C\". Brick, cork and wood have conductivities of 0.7, 0.05 and 0.20 <b>W</b>/m°C (a kilowatt value would be 1000 times too large). Also, the interior wall is colder (−5 °C) than the outer wall (15 °C), so heat flows <b>into</b> the room (cold store).",
          "k is taken as 0.7, 0.05 and 0.20 W/m°C. \"Temperature at inner surfaces\" is taken as the temperatures of the brick–cork and cork–wood interfaces."))
p.q("c", "Explain with neat sketch the construction and working of single cylinder four stroke C.I. engine available in your institute laboratory.", "ic-engine-strokes", C_ICE, [
    P("<i>Note: the engine in your laboratory may differ in details; the following is the general answer for a single-cylinder four-stroke C.I. (diesel) engine.</i>"),
    FIG("te_four_stroke_ci", "Single-cylinder four-stroke C.I. engine (sectional sketch)"),
    H("Construction (main parts)"),
    B("<b>Cylinder</b> with liner and water jacket; <b>cylinder head</b> carrying inlet valve, exhaust valve and the <b>fuel injector</b> (no spark plug).",
      "<b>Piston</b> with piston rings, <b>gudgeon pin</b>, <b>connecting rod</b>, <b>crankshaft</b> with crank pin and <b>flywheel</b>; crankcase.",
      "<b>Valve gear:</b> camshaft driven at half the crankshaft speed by timing gears operates the valves. Fuel pump and injector supply fuel at about 200 bar."),
    H("Working – four strokes (two revolutions of the crankshaft)"),
    T(["Stroke", "Piston", "What happens"], [
        ["1. Suction", "T.D.C. → B.D.C.", "Inlet valve open. Only <b>air</b> is drawn into the cylinder."],
        ["2. Compression", "B.D.C. → T.D.C.", "Both valves closed. Air is compressed (ratio 14:1 to 22:1); its temperature rises above the self-ignition temperature of fuel (about 500 °C or more)."],
        ["3. Power (expansion)", "T.D.C. → B.D.C.", "Near T.D.C. fuel is injected, ignites by itself and burns; hot gases expand and push the piston – work is produced."],
        ["4. Exhaust", "B.D.C. → T.D.C.", "Exhaust valve opens; the burnt gases are pushed out through the exhaust port."]], [1.3, 1.5, 4.5]),
    MS(("Neat sketch with labels", 2), ("Construction", 1), ("Working of four strokes", 3))])
