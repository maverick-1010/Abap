from papers import CONCEPT_TITLES, REVISION

CONCEPT_TITLES.update({
 "zeroth-law": "Zeroth law of thermodynamics", "dryness-fraction": "Dryness fraction of steam",
 "universal-gas-constant": "Universal gas constant and its unit", "dalton-law": "Dalton's law of partial pressure",
 "condenser-function": "Function of a condenser", "thermal-conductivity": "Thermal conductivity and unit",
 "mean-effective-pressure": "Mean effective pressure", "cop-hp-refrigerator": "Heat engine / heat pump / refrigerator, COP relation",
 "second-law-statements": "Kelvin–Planck and Clausius statements", "process-pv-ts": "Gas processes on P-V and T-S diagrams",
 "gas-numerical": "Numerical on perfect gas (pV = mRT, work, ΔU)", "surface-condenser": "Surface condenser – construction and working",
 "cooling-tower": "Cooling tower – construction and working", "boiler-classification": "Classification of boilers",
 "heat-transfer-laws": "Modes of heat transfer / Fourier and Newton laws", "composite-wall": "Numerical on composite wall (conduction)",
 "ic-engine-strokes": "Two/four stroke engines, working of C.I. engine", "diesel-otto-cycle": "Diesel cycle / Otto vs Diesel",
 "steam-numerical": "Numerical on wet / superheated steam", "sfee": "Steady flow energy equation and applications",
 "gas-equation": "Characteristic gas equation (Boyle + Charles)", "special-boilers": "Benson / La-Mont boiler",
 "steam-turbine-theory": "Impulse vs reaction turbine / velocity compounding", "heat-exchangers": "Heat exchangers – types and working",
 "ic-engine-definitions": "Compression ratio, swept volume, cut-off ratio", "thermo-system-property": "Thermodynamic system and property",
 "sensible-latent-heat": "Sensible and latent heat", "black-body-absorptivity": "Black body and absorptivity",
 "ic-engine-classification": "Classification of I.C. engines", "flow-work": "Flow work", "steam-generation": "Steam generation on T-h chart",
 "rankine-cycle": "Rankine cycle on P-V and T-S", "steam-plant-layout": "Layout of steam power plant", "carnot-cycle": "Carnot cycle and limitations",
})

REVISION["TE"] = [
 ("Laws of thermodynamics", ["Zeroth: A~C and B~C ⇒ A~B (basis of thermometer).", "Kelvin–Planck: no engine can convert all heat to work (η &lt; 100 %).", "Clausius: heat cannot flow cold → hot without work.",
   "η_{engine} = W/Q₁ = 1 − Q₂/Q₁;  COP_{R} = Q₂/W;  COP_{HP} = Q₁/W;  <b>COP_{HP} = COP_{R} + 1</b>.", "SFEE: h₁ + C₁²/2 + gZ₁ + Q = h₂ + C₂²/2 + gZ₂ + W. Turbine W = h₁ − h₂; boiler Q = h₂ − h₁.", "Flow work = pV;  h = u + pv.", "Carnot η = 1 − T₂/T₁."]),
 ("Perfect gas", ["pV = mRT;  R = C_{p} − C_{v};  γ = C_{p}/C_{v};  C_{v} = R/(γ−1).", "R_{u} = M R = 8.314 kJ/kmol K.", "Dalton: p = p₁ + p₂ + … (partial pressures).", "Isobaric: W = p(V₂−V₁), Q = mC_{p}ΔT.  Isochoric: W = 0, Q = mC_{v}ΔT.",
   "Isothermal: pV = C, W = p₁V₁ ln(V₂/V₁), ΔU = 0.", "Adiabatic: pV^{γ} = C, W = (p₁V₁ − p₂V₂)/(γ−1), Q = 0.", "Always use T in kelvin (t + 273) and p in N/m² or kN/m² consistently."]),
 ("Steam", ["x = m_{g}/(m_{g}+m_{f});  h = h_{f} + x h_{fg};  v = x v_{g} (approx.).", "Superheated: h = h_{g} + C_{ps}(t_{sup} − t_{s});  v = v_{g} T_{sup}/T_{s}.", "If v &gt; v_{g} at that pressure ⇒ superheated; if v &lt; v_{g} ⇒ wet.", "Steam generation: sensible heat h_{f}, latent heat h_{fg}, superheat."]),
 ("Boilers", ["Fire tube (hot gas in tubes: Cochran, Lancashire) vs water tube (water in tubes: Babcock & Wilcox, La-Mont, Benson).", "La-Mont: forced circulation, pump, up to 170 bar.  Benson: once-through, no drum, ~225 bar (supercritical).", "Mountings: safety valve, pressure gauge, water level indicator, stop valve, fusible plug, blow-off cock."]),
 ("Turbines, condensers, cooling towers", ["Impulse: pressure drop only in nozzle, symmetrical blades.  Reaction: drop in fixed + moving blades.", "Velocity compounding (Curtis): optimum u = C₁cosα₁/(2z).", "Surface condenser: steam outside tubes, water inside, hot well, air pump (non-mixing).  Jet condenser: mixing.", "Cooling tower: natural draught (hyperbolic, large plants), forced / induced draught (fan); make-up water replaces losses.", "Rankine: 1-2 pump, 2-3 boiler, 3-4 turbine, 4-1 condenser; η = [(h₃−h₄)−(h₂−h₁)]/(h₃−h₂)."]),
 ("I.C. engines", ["Otto: heat added at constant V, r = 6–10.  Diesel: heat added at constant p, r = 14–22.", "Diesel η = 1 − (1/r^{γ−1})[(ρ^{γ}−1)/(γ(ρ−1))].", "r = (V_{s}+V_{c})/V_{c};  V_{s} = (π/4)D²L;  cut-off ratio ρ = V₃/V₂;  m.e.p. = W_{net}/V_{s}.", "Four stroke: suction, compression, power, exhaust (2 revolutions). Two stroke: one power stroke per revolution, ports not valves."]),
 ("Heat transfer", ["Conduction (Fourier): Q = −kA dT/dx.  Convection (Newton): Q = hA(T_{s}−T_{f}).  Radiation: Q = σAT⁴.", "Composite wall: Q = ΔT / Σ(L/kA).  Interface: T = T₁ − Q R₁.", "k unit W/m K; h unit W/m² K.", "Heat exchangers: parallel, counter, cross flow; shell & tube, plate, double pipe; uses: condenser, radiator, economiser."]),
]

CONCEPT_TITLES.update({
 "som-radius-gyration": "Radius of gyration", "som-shear-strain": "Shear strain and modulus of rigidity", "som-strain-energy": "Strain energy",
 "som-contraflexure": "Point of contraflexure", "som-flexure-formula": "Flexural formula", "som-core-rect": "Core of rectangular section",
 "som-hollow-dist": "Stress distribution, hollow rectangular section", "som-mi-hollow": "MI of hollow circular section (tangent, polar)",
 "som-stepped-bar": "Stepped bar: P₂ and total elongation", "som-triaxial": "Tri-axial stress: strains and volume change",
 "som-sfbm-point": "SFD and BMD – point load (derivation)", "som-mi-lamina": "MI of composite lamina about A-A", "som-impact": "Impact load on a bar",
 "som-sfbm-ss": "SFD and BMD – simply supported beam", "som-core-hollow": "Greatest eccentricity of hollow column", "som-sf-bm-define": "S.F., B.M. and sign conventions",
 "som-pipe-udl": "UDL a pipe can carry (bending)", "som-polar-modulus": "Polar modulus and torsion assumptions", "som-e-and-mu": "E and μ from compression test",
 "som-hollow-shaft-1": "Hollow shaft diameter (torque, twist)", "som-compound-tube": "Compound tube of steel and brass", "som-overhang": "SFD and BMD – overhanging beam",
 "som-shear-hollow-sq": "Shear stress in hollow square section", "som-t-beam": "T-beam maximum span", "som-hollow-shaft-2": "Hollow shaft from power and twist",
 "som-c-clamp": "C-clamp section (direct + bending)",
})

REVISION["SOM"] = [
 ("Properties of sections", ["Rectangle: I = bd³/12 about centroid; I about base = bd³/3.", "Circle: I = πd⁴/64;  hollow: π(D⁴−d⁴)/64;  J = 2I = π(D⁴−d⁴)/32.", "Semicircle about its axis of symmetry: πR⁴/8.", "Parallel-axis: I = I_{G} + A h².  Radius of gyration k = √(I/A).",
   "Composite or lamina: add areas, subtract cut-outs."]),
 ("Stress, strain, elastic constants", ["σ = P/A;  ε = δL/L;  E = σ/ε;  δ = PL/(AE).", "Stepped bar: δ = Σ N L/(A E);  find forces from equilibrium first.", "Compound bar: equal strain, σ₁/E₁ = σ₂/E₂;  P = σ₁A₁ + σ₂A₂.", "μ = lateral strain / longitudinal strain;  E = 2G(1+μ) = 3K(1−2μ).",
   "Tri-axial: ε_{x} = [σ_{x} − μ(σ_{y} + σ_{z})]/E;  ε_{v} = Σε = (1−2μ)Σσ/E.", "Strain energy U = σ²V/(2E)."]),
 ("Impact load", ["σ = (W/A)[1 + √(1 + 2AEh/(WL))];  δ = σL/E.", "Energy balance: W(h + δ) = σ²AL/(2E).", "Suddenly applied load: σ = 2W/A;  gradually applied: σ = W/A."]),
 ("SF and BM", ["Reactions first: ΣM = 0, ΣF = 0.", "SF changes by the load at a point load; falls linearly under UDL.", "M_{max} where SF = 0 (or changes sign).", "SS beam, central point load: M = WL/4;  UDL: M = wL²/8.  Cantilever: WL, wL²/2.",
   "Overhanging beam: find the point of contraflexure by putting M(x) = 0.", "Sign: sagging +, hogging −; clockwise shear +."]),
 ("Bending and shear stress in beams", ["M/I = σ/y = E/R;  σ_{max} = M/Z;  Z = I/y_{max}.  Z rectangle = bd²/6;  circle = πd³/32.", "τ = F A ȳ / (I b);  rectangle τ_{max} = 1.5 τ_{avg};  circle 4/3 τ_{avg}.", "Hollow box: τ jumps where width changes; maximum at N.A.", "T-beam: find ȳ, then I, then use the farther fibre for the limit stress."]),
 ("Torsion", ["T/J = τ/r = Gθ/L.  Solid: T = (π/16)τd³.  Hollow: T = (π/16)τ(D⁴−d⁴)/D.", "Power P = 2πNT/60.  Use T_{max} = 1.25 T_{mean} if told.", "Take the larger diameter from the strength and the stiffness (twist) condition; θ in radian = deg × π/180.", "Polar modulus Z_{p} = J/R."]),
 ("Direct and bending stress", ["σ = P/A ± M/Z, with M = P e.", "No tension condition: e ≤ core limit.  Rectangle: B/6 and D/6 (core B/3 × D/3).  Solid circle: d/8.  Hollow circle: (D²+d²)/(8D).", "C-clamp: direct tension + bending, σ = P/A + Pe/Z ≤ allowable."]),
]

CONCEPT_TITLES.update({
 "pd-knurl-spline": "Knurling and splined shaft conventions", "pd-taper": "Taper – calculation, sketch and convention", "pd-pipe-valve": "Pipe breaks and valve conventions",
 "pd-gt-symbols": "Geometrical tolerance symbols", "pd-tolerance-sketch": "Sketch of basic size, deviations and tolerance", "pd-surface-meaning": "Meaning of machining (surface texture) symbol",
 "pd-lay": "Direction of lay symbol", "pd-projection": "Orthographic / auxiliary view completion", "pd-material": "Material and component conventions",
 "pd-pcd-bearing": "Holes on circular pitch and bearings", "pd-gears": "Gear conventions (spur, bevel, worm)", "pd-fit": "Type of fit from limits (numerical)",
 "pd-gt-meaning": "Meaning of geometrical tolerance frames", "pd-weld-drawing": "Welding drawing and symbol for a joint", "pd-ujoint": "Universal coupling – detail drawings",
 "pd-oldham": "Oldham's coupling – assembly / details", "pd-lathe-post": "Lathe tool post – assembly, bill of material, fits",
 "pd-thread-spring": "Internal thread and leaf spring conventions", "pd-weld-symbols": "Weld symbols", "pd-foot-step": "Foot step bearing – assembly",
})

REVISION["PD"] = [
 ("Lines and conventions", ["Thick continuous: outlines; thin continuous: dimensions, hatching; dashed: hidden edges; chain thin: centre/pitch lines; chain thick at ends: cutting plane.", "Section hatching 45° thin lines; adjacent parts opposite direction; C.I. close thin lines; copper/brass alternate thick-thin; rubber almost solid.",
   "Shafts, keys, bolts, pins, ribs are not sectioned when the cutting plane passes along their axis.", "Spur gear: addendum thick, pitch thin chain, root thin (not in section). Teeth not drawn."]),
 ("Taper, thread, springs", ["Taper = (D − d)/L = 1 : k;  d = D − L/k.  Taper symbol: triangle pointing towards small end, with ratio.", "External thread: major dia thick, minor dia thin; internal thread: minor dia thick, major dia thin; end view 3/4 thin circle.", "Short break: S-curves; long break: thin zig-zag.",
   "Semi-elliptic leaf spring conventional: single arc with a cross at the centre."]),
 ("Limits, fits, tolerances", ["Upper limit = basic + upper deviation; lower limit = basic + lower deviation.  Tolerance = upper − lower limit.", "Max clearance = hole max − shaft min;  Min clearance = hole min − shaft max.", "Min clearance ≥ 0: clearance fit;  max clearance ≤ 0: interference fit;  otherwise transition fit.",
   "Capital letters (H) for holes, small letters (e, g, h, n) for shafts. H7/e8 clearance; H7/n6 transition; H7/p6 interference.", "Hole-basis: H hole, EI = 0."]),
 ("Geometrical tolerance symbols", ["Form: straightness —, flatness ▱, circularity ○, cylindricity.", "Orientation: parallelism ∥, perpendicularity ⊥, angularity ∠.", "Location: position, concentricity ◎, symmetry ⌯.", "Frame: symbol | tolerance value | datum letter."]),
 ("Surface finish and welding", ["Machining symbol: Ra (μm) on top; lower limit left; method above extension line; sampling length below; lay letter R, C, M, X, = on the right.", "Weld symbols below the reference line = arrow side; above = other side.", "Single V butt ∨, fillet ◺ (leg length at left), spot ○, seam ○ with two lines, U butt ∪; convex contour = arc over the symbol."]),
 ("Projection (first angle)", ["FV above TV; LHSV to the right of FV.", "Auxiliary view: reference line ⟂ to direction of view; heights/widths measured from the reference line.", "True length of an inclined line in FV: L; its top view = L cos θ; height = L sin θ.", "A circle on an inclined plane appears as an ellipse: width = Ø cos θ."]),
 ("Assembly drawings", ["Steps: study details → list parts and materials → choose scale → main body first → inner parts → hatch → dimensions (overall) → bill of material.", "Oldham's coupling: 2 flanges + central disc with two tongues at 90°, taper keys 1 in 100.", "Lathe tool post: post + block + ring (concave seat) + wedge + screw.",
   "Universal coupling: 2 forks + centre block + 2 pins + taper pins + keys.", "Foot step bearing: body + bush + shaft + disc + pin."]),
]
