from dsl import *

p = Paper("SOM-S23", "313308", "Strength of Materials", "SOM", "S23", "Summer 2023 (extra paper, I-scheme)", "I-scheme (paper code 22306)", "3 Hours", 70, "22306 / 22223",
          "2023_summer_SOM.pdf", 6, in_scope=False,
          notes=["This paper is <b>not</b> one of the sessions you asked for (Winter 2024, Summer 2025, Winter 2025) and it is from the older <b>I-scheme</b> "
                 "(paper code 22306). It is included because it was the only Strength of Materials paper supplied. Topics may differ slightly from the K-scheme syllabus. "
                 "The scan has a website watermark over some lines, but all text and figures were readable."])

M1 = "Moment of inertia"
M2 = "Simple stresses and strains"
M3 = "Elastic constants and strain energy"
M4 = "Shear force and bending moment"
M5 = "Bending and shear stresses in beams"
M6 = "Torsion of shafts"
M7 = "Direct and bending stresses (core, eccentric loads)"

p.group(1, "Attempt any FIVE of the following:", 10, 5)
p.q("a", "Define radius of gyration. State its S.I. unit.", "som-radius-gyration", M1, [
    P("<b>Radius of gyration (k)</b> of an area about an axis is the distance from that axis at which the whole area can be assumed to be concentrated so that it gives the same moment of inertia as the actual area."),
    F("k = √(I / A)      or      I = A k²"),
    P("<b>S.I. unit:</b> metre (m); in practice mm."),
    MS(("Definition", 1), ("Formula and unit", 1))])
p.q("b", "Define shear strain and modulus of rigidity.", "som-shear-strain", M3, [
    B("<b>Shear strain (φ):</b> the angular deformation (in radian) produced in a body, measured as the angle through which a line originally perpendicular to the fixed face is turned under a shear force.",
      "<b>Modulus of rigidity (G):</b> the ratio of shear stress to shear strain within the elastic limit.  G = τ / φ  (unit N/mm² or GPa)."),
    MS(("Shear strain", 1), ("Modulus of rigidity", 1))])
p.q("c", "Define strain energy. State its S.I. unit.", "som-strain-energy", M3, [
    P("<b>Strain energy</b> is the energy stored in a body when it is deformed by an external load, within the elastic limit. It is equal to the work done by the load in deforming the body."),
    F("U = ½ P δ = σ² V / (2E)"),
    P("<b>S.I. unit:</b> joule (J) = N·m."),
    MS(("Definition", 1), ("Formula and unit", 1))])
p.q("d", "State point of contra-shear with suitable sketch.", "som-contraflexure", M4, [
    P("The question says \"contra-shear\"; the standard term for this idea in beams is the <b>point of contraflexure</b> (also called point of inflection)."),
    B("It is the point on a beam where the <b>bending moment changes sign</b> (from sagging to hogging or the reverse), so the bending moment there is zero.",
      "Such points occur in overhanging and continuous beams. At this point the curvature of the beam changes from concave to convex."),
    FIG("som_contraflexure", "Point of contraflexure on a B.M.D."),
    MS(("Statement", 1), ("Sketch", 1))],
    flag=("The printed term \"point of contra-shear\" is not a standard term in Strength of Materials.", "It is taken to mean the <b>point of contraflexure</b> (bending moment changes sign). Note: the point where shear force is zero is the point of maximum bending moment, which is a different thing."))
p.q("e", "Write the flexural formula and state the meaning of each term used in it.", "som-flexure-formula", M5, [
    F("M / I = σ_{b} / y = E / R"),
    T(["Symbol", "Meaning", "Unit"], [
        ["M", "Bending moment at the section", "N·mm"],
        ["I", "Moment of inertia of the cross-section about the neutral axis", "mm⁴"],
        ["σ_{b}", "Bending stress at a layer at distance y from the neutral axis", "N/mm²"],
        ["y", "Distance of the layer from the neutral axis", "mm"],
        ["E", "Young’s modulus of the beam material", "N/mm²"],
        ["R", "Radius of curvature of the neutral layer", "mm"]], [0.8, 4, 1]),
    MS(("Formula", 1), ("Meaning of terms", 1))])
p.q("f", "Draw a neat sketch to show core of rectangular section of (B × D) dimensions.", "som-core-rect", M7, [
    FIG("som_core_rect", "Core of a rectangular section (middle-third rule)"),
    P("The core is a <b>rhombus (diamond)</b> whose diagonals are B/3 along the breadth and D/3 along the depth, symmetrical about the centroid. If the load acts anywhere inside this core, no tensile stress is produced in the section."),
    MS(("Sketch", 1), ("Dimensions B/3 and D/3", 1))])
p.q("g", "Draw shear stress and bending stress distribution diagram for hollow rectangular beam section.", "som-hollow-dist", M5, [
    FIG("som_hollow_rect_dist", "Bending and shear stress distribution – hollow rectangular section"),
    B("<b>Bending stress</b> varies linearly with distance from the neutral axis: zero at N.A. and maximum (compressive at top, tensile at bottom) at the extreme fibres.",
      "<b>Shear stress</b> is zero at the top and bottom edges, increases parabolically in the flanges, jumps suddenly at the inner face where the width reduces to the two webs, and is maximum at the neutral axis."),
    MS(("Bending stress diagram", 1), ("Shear stress diagram", 1))])

p.group(2, "Attempt any THREE of the following:", 12, 3)
p.q("a", "A hollow circular section having 200 mm external diameter and 100 mm internal diameter. Calculate the moment of inertia of the section about any of the tangent. Also find polar moment of inertia.", "som-mi-hollow", M1,
    [NUM("SOM-S23-Q2a"), MS(("Given data and formula", 1), ("Moment of inertia about centroidal axis", 1), ("Parallel-axis theorem – tangent", 1), ("Polar moment of inertia", 1))], qtype="numerical")
p.q("b", "A member ABCD is subjected to point loads of P_{1}, P_{2}, P_{3} and P_{4} as shown in Figure No. 1. Calculate the force P_{2} necessary for equilibrium, if P_{1} = 45 kN, P_{3} = 450 kN and P_{4} = 130 kN. Determine the total elongation of the member, assuming the modulus of elasticity to be 2.1 × 10^{5} N/mm².\n[Figure No. 1: member ABCD – AB 625 mm², 120 cm; BC 2500 mm², 60 cm; CD 1250 mm², 90 cm]",
    "som-stepped-bar", M2, [
        FIG("som_stepped", "Stepped member ABCD (Figure No. 1)"),
        NUM("SOM-S23-Q2b"), MS(("Equilibrium – value of P_{2}", 1), ("Axial force in each part", 1), ("Elongation of each part", 1), ("Total elongation", 1))], qtype="numerical",
    flag=("The figure gives lengths in cm (120, 60, 90) but areas in mm².", "Lengths are converted to mm (1200, 600, 900). P_{1} and P_{3} act to the left and P_{2}, P_{4} to the right, as shown in the figure."))
p.q("c", "In a tri-axial stress system, the stresses along the three directions are σ_{x} = 100 N/mm² (tensile), σ_{y} = 60 N/mm² (tensile) and σ_{z} = 30 N/mm² (compressive). Find the strains in each direction. Take E = 2 × 10^{5} N/mm² and μ = 0.25. If X = 400 mm, Y = 150 mm and Z = 300 mm. Also calculate the change in volume.", "som-triaxial", M3,
    [NUM("SOM-S23-Q2c"), MS(("Formulae for strains", 1), ("Strains ε_{x}, ε_{y}, ε_{z}", 1), ("Volumetric strain", 1), ("Change in volume", 1))], qtype="numerical")
p.q("d", "A simply supported beam of span ‘L’ is subjected to downward point load of ‘W’ at a distance ‘a’ from left support and ‘b’ from right support. Draw SF and BM diagrams. Take a &gt; b.", "som-sfbm-point", M4, [
    H("Reactions"),
    F("Taking moments about B:  R_{A} × L = W × b   ⇒   R_{A} = W b / L"),
    F("R_{B} = W − R_{A} = W a / L"),
    H("Shear force"),
    B("A to C (0 &lt; x &lt; a): F = + R_{A} = + W b / L (constant).", "C to B (a &lt; x &lt; L): F = R_{A} − W = − W a / L (constant)."),
    H("Bending moment"),
    B("At A and B: M = 0.", "At C (under the load): M_{C} = R_{A} × a = <b>+ W a b / L</b> (maximum, because S.F. changes sign here)."),
    FIG("som_sfbm_2d", "S.F.D. and B.M.D. (the figure is drawn for a &gt; b)"),
    P("Since a &gt; b, the right reaction W a / L is the larger one and the maximum shear force is W a / L."),
    MS(("Reactions", 1), ("S.F. values and diagram", 1.5 if False else 1), ("B.M. values and diagram", 1), ("Maximum values stated", 1))])

p.group(3, "Attempt any THREE of the following:", 12, 3)
p.q("a", "Calculate the moment of inertia about the axis A-A, for the lamina shown in the Figure No. 2.\n[Figure No. 2: rectangle 700 mm × 300 mm with a semicircular cut-out of R 150 mm on the bottom edge; axis A-A is 250 mm from the right edge]", "som-mi-lamina", M1, [
    FIG("som_lamina", "Lamina (Figure No. 2)"), NUM("SOM-S23-Q3a"),
    MS(("Splitting into rectangle and semicircle", 1), ("I of rectangle about A-A", 1), ("I of semicircle about A-A", 1), ("Subtraction and answer", 1))], qtype="numerical",
    flag=("The figure does not give the position of the semicircular cut-out explicitly.", "As drawn, the diameter lies on the bottom edge and starts at the left edge, so the centre is 150 mm from the left edge and 800 mm from A-A."))
p.q("b", "A metal bar 20 mm in diameter and 1000 mm long is hung vertically and a collar is attached at the lower end. A weight of 1000 N falls through a height of 250 mm on the collar. Calculate the maximum instantaneous stress, elongation and strain energy stored in a bar. Take E = 2 × 10^{5} N/mm².", "som-impact", M3,
    [NUM("SOM-S23-Q3b"), MS(("Area and formula", 1), ("Maximum stress", 1), ("Elongation", 1), ("Strain energy", 1))], qtype="numerical")
p.q("c", "Simply supported beam having span 7 m carries two point loads 3 kN at distance of 3 m from left hand support and 5 kN at distance of 2 m from right hand support. In addition to this an udl of 2 kN/m over a span of 3 m from left hand support. Draw SF and BM diagrams.", "som-sfbm-ss", M4, [
    NUM("SOM-S23-Q3c"), FIG("som_sfbm_3c", "S.F.D. and B.M.D. (values from the beam solver)"),
    MS(("Reactions", 1), ("S.F. values", 1), ("B.M. values", 1), ("Diagrams", 1))], qtype="numerical")
p.q("d", "A short column of external diameter 40 cm and internal diameter 20 cm carries an eccentric load of 80 kN. Find the greatest eccentricity which the load can have without producing tension in the column section.", "som-core-hollow", M7,
    [NUM("SOM-S23-Q3d"), MS(("Condition for no tension", 1), ("Core formula", 1), ("Substitution", 1), ("Answer with unit", 1))], qtype="numerical")

p.group(4, "Attempt any THREE of the following:", 12, 3)
p.q("a", "Define shear force and bending moment. Explain sign conventions for shear force and bending moment with neat sketches.", "som-sf-bm-define", M4, [
    B("<b>Shear force (S.F.):</b> the algebraic sum of all the vertical forces acting on either side of a section of the beam.",
      "<b>Bending moment (B.M.):</b> the algebraic sum of the moments, about the section, of all the forces acting on either side of the section."),
    H("Sign conventions"),
    B("<b>S.F.:</b> positive if the left portion tends to move upward relative to the right portion (clockwise shear); negative otherwise.",
      "<b>B.M.:</b> positive (sagging) if it bends the beam concave upwards (top fibres in compression); negative (hogging) if it bends the beam concave downwards (top fibres in tension)."),
    FIG("som_sign_conv", "Sign conventions"),
    MS(("Definition of S.F.", 1), ("Definition of B.M.", 1), ("Sign conventions of S.F.", 1), ("Sign conventions of B.M.", 1))])
p.q("b", "A cast iron pipe having 800 mm external diameter and 700 mm internal diameter is used to pass the hydraulic oil. The pipe is simply supported at both the ends having length 7.5 m. Calculate the intensity of uniformly distributed load that pipe can carry. Assuming bending stress in pipe material is 140 N/mm².", "som-pipe-udl", M5,
    [NUM("SOM-S23-Q4b"), MS(("Moment of inertia and Z", 1), ("Maximum bending moment M = σZ", 1), ("Equation M = wL²/8", 1), ("Answer", 1))], qtype="numerical")
p.q("c", "Write the equation of polar modulus for hollow shaft. State assumptions made in theory of pure torsion.", "som-polar-modulus", M6, [
    F("Polar modulus  Z_{p} = J / R = [π (D⁴ − d⁴) / 32] / (D/2) = π (D⁴ − d⁴) / (16 D)"),
    P("where D = external diameter and d = internal diameter of the shaft. Torque transmitted: T = (π/16) τ (D⁴ − d⁴)/D = τ Z_{p}."),
    H("Assumptions in the theory of pure torsion"),
    N("The material of the shaft is homogeneous and isotropic.",
      "The shaft has a uniform circular cross-section (solid or hollow) throughout its length.",
      "Plane transverse sections remain plane and circular after twisting; radii remain straight.",
      "The twist is uniform along the length; the shaft is subjected to pure torque only.",
      "Stresses do not exceed the elastic limit (Hooke’s law applies), so shear stress ∝ shear strain.",
      "Shear stress at a point is proportional to its distance from the axis."),
    MS(("Equation of polar modulus", 2), ("Any four assumptions", 2))])
p.q("d", "A metal bar of 50 mm × 50 mm in cross section, is subjected to axial compressive load of 500 kN. The contraction of a 200 mm gauge length is found to be 0.5 mm and increase in thickness is 0.04 mm. Find the values of Young’s modulus and Poisson’s ratio.", "som-e-and-mu", M2,
    [NUM("SOM-S23-Q4d"), MS(("Stress", 1), ("Young’s modulus", 1), ("Lateral strain", 1), ("Poisson’s ratio", 1))], qtype="numerical")
p.q("e", "A hollow shaft of diameter ratio 3/5 is required to transmit maximum torque of 61.5 kNm. The shear stress is not to exceed 63 MPa and twist in a length of 3 m is not to exceed 1.4°. Calculate the minimum external diameter satisfying these conditions. Take G = 84 GPa.", "som-hollow-shaft-1", M6,
    [NUM("SOM-S23-Q4e"), MS(("Diameter from shear stress", 1), ("Diameter from angle of twist", 1), ("Selecting the larger value", 1), ("Answer with units", 1))], qtype="numerical")

p.group(5, "Attempt any TWO of the following:", 12, 2)
p.q("a", "A compound tube consists of steel and brass, steel tube having 140 mm internal diameter and 160 mm external diameter, an outer side brass tube having 160 mm internal diameter and 180 mm external diameter. Two tubes having same length of 140 mm. The compound tube carries an axial load of 900 kN. Calculate the stresses in the tube materials and load carrying capacity of each material. Also calculate the amount the tubes gets shortens. Take E_{s} = 2 × 10^{5} N/mm² and E_{BR} = 1 × 10^{5} N/mm².", "som-compound-tube", M2,
    [NUM("SOM-S23-Q5a"), MS(("Areas of steel and brass", 1), ("Stresses (equal strain condition)", 2), ("Load shared by each", 2), ("Shortening", 1))], qtype="numerical",
    flag=("The length of the tubes is printed as 140 mm, which equals the steel inside diameter (a typing slip is possible).", "It is used as printed. The stresses and loads do not depend on the length; only the shortening (0.0853 mm) does."))
p.q("b", "Draw shear force and bending moment diagram for an overhanging beam as shown in the Figure No. 3. Also find point of contra-flexure if any.\n[Figure No. 3: beam A–D–B–C; A to D 2 m, D to B 3 m, B to C 2 m; 5 kN at D; 8 kN/m over the whole length; 5 kN at C; supports at A and B]", "som-overhang", M4, [
    NUM("SOM-S23-Q5b"), FIG("som_sfbm_5b", "S.F.D. and B.M.D. of the overhanging beam"),
    MS(("Reactions", 1), ("S.F. values and diagram", 2), ("B.M. values and diagram", 2), ("Point of contraflexure", 1))], qtype="numerical",
    flag=("The figure shows the 8 kN/m load as a continuous wavy line along the whole beam A to C, and supports at A and B.", "The UDL is taken over the full length of 7 m and the supports at A and B (5 m apart), with the beam overhanging 2 m beyond B."))
p.q("c", "A hollow square section 100 mm × 100 mm outside dimensions and 20 mm thick is subjected to a shear force of 75 kN. Calculate the ratio of maximum shear stress to the average shear stress. Draw the shear stress distribution diagram showing all the values on it.", "som-shear-hollow-sq", M5, [
    NUM("SOM-S23-Q5c"), FIG("som_hollow_sq_shear", "Shear stress distribution – hollow square section"),
    MS(("Moment of inertia and area", 1), ("Average shear stress", 1), ("Maximum shear stress", 2), ("Ratio", 1), ("Diagram with values", 1))], qtype="numerical")

p.group(6, "Attempt any TWO of the following:", 12, 2)
p.q("a", "A ‘T’ section having dimensions 110 × 110 × 10 mm is used as a simply supported beam with a flange at top. It carries udl of 10 kN/m. If the maximum stress is not to exceed 150 N/mm², calculate the maximum span of beam. Also draw the bending stress distribution diagram.", "som-t-beam", M5, [
    NUM("SOM-S23-Q6a"), FIG("som_T_stress", "Bending stress distribution in the T-section"),
    MS(("Centroid", 1), ("Moment of inertia", 2), ("Section modulus and moment of resistance", 1), ("Span", 1), ("Stress diagram", 1))], qtype="numerical")
p.q("b", "A hollow shaft, having an internal diameter 40% of its external diameter, transmits 562.5 kW power at 100 r.p.m. Determine the external diameter of the shaft if the shear stress is not to exceed 60 N/mm² and the twist in a length of 2.5 m should not exceed 1.3°. Assume maximum torque = 1.25 times the mean torque and modulus of rigidity = 9 × 10^{4} N/mm².", "som-hollow-shaft-2", M6,
    [NUM("SOM-S23-Q6b"), MS(("Mean and maximum torque", 1), ("Diameter from shear stress", 2), ("Diameter from twist", 2), ("Selecting larger value", 1))], qtype="numerical")
p.q("c", "Figure No. 4. shows a C - clamp carries a load P = 27 kN. Section of clamp is rectangular having width equal to twice the thickness. Assuming that the clamp is made up of steel casting with an allowable stress of 100 N/mm². Find the dimensions of the clamp section.\n[Figure No. 4: C-clamp; load line 144 mm from the centroidal axis of the vertical member]", "som-c-clamp", M7, [
    FIG("som_cclamp", "C-clamp (Figure No. 4)"), NUM("SOM-S23-Q6c"),
    MS(("Direct and bending stress equation", 2), ("Area and section modulus in terms of t", 1), ("Solving for t", 2), ("Final dimensions", 1))], qtype="numerical",
    flag=("The figure shows a 144 mm dimension but does not say clearly which line it is measured to.", "It is taken as the distance e from the load line to the centroidal axis of the vertical member of the clamp."))
