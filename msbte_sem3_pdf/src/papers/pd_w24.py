from dsl import *

p = Paper("PD-W24", "313311", "Production Drawing", "PD", "W24", "Winter 2024", "K-scheme", "4 Hours", 70, "12425",
          "Production_Drawing_Winter_2024_Question_Paper_First_K_Scheme_Paper.pdf", 8)

C_CONV = "Conventions and standard representations (BIS SP-46)"
C_FIT = "Limits, fits, tolerances, surface finish and welding symbols"
C_PROJ = "Orthographic and auxiliary views"
C_ASM = "Assembly and detail drawings"

# ------------------------------------------------------------------ Q1
p.group(1, "Attempt any FIVE of the following :", 10, 5)
p.q("a", "Draw the conventional representation of the following :\n(i) Diamond Knurling\n(ii) Splined Shaft", "pd-knurl-spline", C_CONV, [
    FIG("pd_knurl", None), FIG("pd_spline", None),
    B("<b>Diamond knurling:</b> two sets of thin continuous lines at 45° to the axis, crossing each other to form diamonds, drawn over the knurled portion (it may be shown only over a small part of the length).",
      "<b>Splined shaft:</b> in the front view the major diameter is drawn with thick lines and the minor diameter with thin lines up to the end of the spline, the runout is shown by a thin sloping line; in the end view the shaft outline with teeth is drawn."),
    MS(("Diamond knurling", 1), ("Splined shaft", 1))])
p.q("b", "Draw a sketch to represent taper 1 : 10 on a shaft of diameter 40 mm and length 110 mm.", "pd-taper", C_CONV, [
    NUM("PD-W24-Q1b"), FIG("pd_taper", "Taper 1:10 on a shaft Ø40 × 110", D=40.0, L=110.0, k=10),
    MS(("Calculation of small end diameter", 1), ("Sketch with taper symbol and dimensions", 1))], qtype="numerical")
p.q("c", "Draw the conventional representation of the following :\n(i) Short break in pipe\n(ii) Gate valve", "pd-pipe-valve", C_CONV, [
    FIG("pd_pipe_breaks", None), FIG("pd_gate_globe", None, which="gate"),
    P("<b>Short break in pipe:</b> the pipe is cut by two S-shaped (curved) thin lines so that the middle part need not be drawn. <b>Gate valve:</b> two triangles meeting at their apexes (the gate) between the pipe line, with a stem and handle on top."),
    MS(("Short break in pipe", 1), ("Gate valve", 1))])
p.q("d", "Draw the symbol for representing the geometrical tolerance in case of the following :\n(i) Circularity\n(ii) Symmetry", "pd-gt-symbols", C_FIT, [
    FIG("pd_gt_symbols", None, names=("circularity", "symmetry")),
    B("<b>Circularity (roundness):</b> a circle ○.", "<b>Symmetry:</b> three horizontal parallel lines, the middle one longer ⌯."),
    MS(("Circularity", 1), ("Symmetry", 1))])
p.q("e", "Draw a sketch showing basic size, lower deviation, upper deviation and tolerance.", "pd-tolerance-sketch", C_FIT, [
    FIG("pd_tolerance_sketch", None),
    MS(("Sketch showing zero line, basic size, upper and lower deviation, tolerance zone", 2))])
p.q("f", "State the meaning of symbols shown in the Fig. No. 1.\n[Fig. No. 1: machining symbol with 0.8 above the bar, 0.5 at left, “Grinding” above the extension line and 2 below it]", "pd-surface-meaning", C_FIT, [
    FIG("pd_surface_meaning", None, top="0.8", low="0.5", method="Grinding", sampling="2"),
    P("The symbol is the machining (surface texture) symbol: the surface is to be finished by <b>grinding</b>, the roughness value Ra must lie between <b>0.5 μm and 0.8 μm</b>, and the sampling length is <b>2 mm</b>."),
    MS(("Roughness limits 0.8 and 0.5", 1), ("Method “Grinding” and sampling length 2", 1))])
p.q("g", "Show machining symbols to represent direction of lay for approximately radial relative to the center of the surface.", "pd-lay", C_FIT, [
    FIG("pd_lay_radial", None),
    P("The direction of lay is shown by the letter <b>R</b> placed at the right of the machining symbol: R = lay approximately radial relative to the centre of the surface."),
    MS(("Machining symbol", 1), ("Letter R for radial lay", 1))])

# ------------------------------------------------------------------ Q2
p.group(2, "Attempt any ONE of the following :", 8, 1)
p.q("a", "Fig. No. 2 shows front view, auxiliary view and incomplete side view of an object. Redraw the given views and complete the side view.\n[Fig. No. 2: bent plate – base 150 × 18, arm 100 long at 60°, R40 end with Ø50 hole, plate width 80; incomplete S.V. 80 wide]", "pd-projection", C_PROJ, [
    FIG("pd_w24_2a", "Front view, auxiliary view and completed side view (first angle)"),
    H("Procedure"),
    N("Draw the X–Y reference line. Draw the front view: base 150 × 18; arm of length 100 and thickness 18 inclined at 60° to the base at the left end; end of the arm cut square.",
      "Draw the auxiliary view as given, projecting at right angles to the arm: plate width 80 (2 × R40), length 100 with R40 round end, Ø50 hole at 40 mm from the end (centre at 60 mm from the bend).",
      "Draw the side view to the right of the front view. Base: rectangle 80 × 18 with the vertical lines at 30 mm apart as given.",
      "Project the height of the arm from the F.V.: the arm rises to 100 sin 60° = 86.6 mm, the straight sides stop at 60 sin 60° = 52 mm, where the half-ellipse for the round end begins (semi-axes 40 and 34.6 mm).",
      "Project the Ø50 hole: it appears as two dashed ellipses (semi-axes 25 and 25 sin 60° = 21.7 mm) joined by dashed lines at ± 25 mm.",
      "Draw centre lines, show hidden lines dashed, and give the main dimensions."),
    MS(("Redrawing front and auxiliary views", 3), ("Projection of the arm in side view", 3), ("Hole and hidden lines", 1), ("Dimensions", 1))],
    qtype="drawing",
    flag=("The printed figure is small; a few details (the exact vertical lines in the base of the F.V., and the lines at 30 mm in the S.V.) are hard to read.", "The drawing reproduces them as printed (a line at 40 mm from the right end in the F.V.; lines at ± 15 mm in the S.V.). Check against your paper."))
p.q("b", "Fig. No. 3 shows incomplete front view, top view and auxiliary view of an object. Draw the given views and complete Front view.\n[Fig. No. 3: base plate 15 thick with slot R12 and chamfered corners, upright block 50 high, auxiliary view with Ø40 hole]", "pd-projection", C_PROJ, [
    NUM("PD-W24-Q2b"),
    H("Procedure (first angle method)"),
    N("Draw the XY line. Draw the top view first, exactly as given: plate outline with the two 15 × 15 chamfers, slot with its end radii, and the inclined block at its angle.",
      "Draw the given front view below it: base plate 15 high, block 50 high; project vertical lines from every corner of the top view down to the front view.",
      "Draw the auxiliary view on the inclined reference line (parallel to the inclined face): the Ø40 hole appears as a true circle there.",
      "Project the hole to the front view: its vertical axis stays 40 mm high; its horizontal width is 40 cos θ (see calculation). Draw the ellipse by the four-centre or trammel method, with the dash-dot axes.",
      "Complete the front view: add the chamfer edges, the slot (hidden dashed lines below the plate top) and the vertical edges of the block from the projectors.",
      "Show hidden lines by dashed lines, thick outlines, and dimension the main sizes."),
    MS(("Redraw given views", 3), ("Projection to complete F.V.", 3), ("Ellipse of the hole / hidden lines", 1), ("Dimensions", 1))],
    qtype="drawing",
    flag=("The figure is small and the angle of the inclined face, and the end radius of the slot are not clear: R12 does not match the slot width of 20 mm (15 + 20 + 15 = 50).",
          "The inclined face is taken as 30° to the XY line and the slot width as 20 mm (end radius 10 mm). No finished view is drawn here because the shape cannot be established with certainty; the method and the calculated sizes are given."))

# ------------------------------------------------------------------ Q3
p.group(3, "Attempt any FIVE of the following :", 20, 5)
p.q("a", "Draw the material convention of the following :\n(i) Copper\n(ii) Rubber\n(iii) Glass\n(iv) Marble", "pd-material", C_CONV, [
    FIG("pd_materials", "Material conventions (sectional view hatching)"),
    P("Copper (brass, bronze): inclined section lines at 45°. Rubber: close, heavy (almost solid) lines. Glass: thin lines at 45°, widely spaced with short thin dashes. Marble: thin horizontal and vertical lines forming a brick-like pattern."),
    MS(("Each convention, 1 mark", 4))])
p.q("b", "Draw the conventional representation of the following :\n(i) Holes on circular pitch\n(ii) Bearings", "pd-pcd-bearing", C_CONV, [
    FIG("pd_holes_pcd", None), FIG("pd_bearings", None),
    MS(("Holes on circular pitch", 2), ("Bearings", 2))])
p.q("c", "Draw the conventional representation of the following :\n(i) Spur gear\n(ii) Worm and worm wheel", "pd-gears", C_CONV, [
    FIG("pd_gears", None, which="spur"), FIG("pd_gears", None, which="worm"),
    B("<b>Spur gear:</b> addendum circle – thick continuous; pitch circle – thin chain; root (dedendum) circle – thin continuous (not drawn in a sectional view). Teeth are not drawn.",
      "<b>Worm and worm wheel:</b> the worm is drawn as a shaft with pitch line (thin chain) and tooth lines; the wheel is drawn like a spur gear with addendum, pitch and root circles and a throat circle in the end view."),
    MS(("Spur gear", 2), ("Worm and worm wheel", 2))])
p.q("d", "The shaft size is given as 40(−0.02/−0.04) and the hole size is 40(+0.02/−0.04). Determine the type of fit between them.", "pd-fit", C_FIT, [
    NUM("PD-W24-Q3d"),
    MS(("Limits of shaft and hole", 1), ("Maximum and minimum clearance", 2), ("Type of fit", 1))], qtype="numerical",
    flag=("The hole size is printed with a lower deviation of −0.04 (below the basic size). For a hole this is unusual (holes normally have a lower deviation of 0 or more).",
          "The sizes are used exactly as printed, giving a transition fit."))
p.q("e", "Refer Fig. No. 4 and state the meaning of symbol at X & Y.\n[Fig. No. 4: X = ∥ 0.02 A, Y = ⊥ 0.03 A, datum A]", "pd-gt-meaning", C_FIT, [
    FIG("pd_gt_symbols", None, names=("parallelism", "perpendicularity")),
    B("<b>X (∥ 0.02 A):</b> parallelism – the surface must lie between two parallel planes 0.02 mm apart which are parallel to datum A.",
      "<b>Y (⊥ 0.03 A):</b> perpendicularity (squareness) – the surface must lie between two parallel planes 0.03 mm apart which are perpendicular to datum A."),
    MS(("Meaning of X", 2), ("Meaning of Y", 2))])
p.q("f", "Two rectangular plates are to be welded with each other along the length. The thickness and length of both plates 12 mm and 60 mm respectively. The plates are to be U Butt welded with convex counter. Prepare welding drawing.", "pd-weld-drawing", C_FIT, [
    FIG("pd_u_butt_weld", "U butt weld with convex contour"),
    N("Draw the two plates, 12 mm thick and 60 mm long, with their edges prepared as a U groove (root face about 2 mm, root radius about 4 mm).",
      "Show the weld metal (hatched) with a slightly convex reinforcement on the top.",
      "Draw the arrow line touching the joint, the reference line, and the U-butt weld symbol below the line (arrow side).",
      "Add the convex contour symbol (an arc) over the weld symbol, and the length 60 mm."),
    MS(("Joint drawing with U preparation", 2), ("Welding symbol with contour symbol", 2))])

# ------------------------------------------------------------------ Q4
p.group(4, "Fig. No. 5 shown the assembly of universal coupling. Attempt any TWO of the following :", 16, 2)
UJ_COMMON = [
    NOTE("Fig. No. 5 (assembly of universal coupling). Part list printed in the figure and the proportions read from it are given once here; they apply to (a), (b) and (c)."),
    T(["Part No.", "Part name", "Material", "Qty."], [["1", "Fork", "C.I.", "2"], ["2", "Centre block", "C.I.", "1"], ["3", "Pin", "M.S.", "2"], ["4", "Taper pin Ø6", "M.S.", "2"], ["5", "Collar", "M.S.", "2"], ["6", "Key", "M.S.", "2"], ["7", "Shaft", "M.S.", "2"]], [1, 3, 1.2, 1]),
    T(["Feature (from Fig. 5)", "Size", "Ratio to shaft d = 50"], [
        ["Boss (hub) diameter of fork", "Ø88", "1.75 d"], ["Length of boss", "86", "1.7 d"], ["Gap between fork ears (centre block thickness)", "44", "0.9 d"],
        ["Thickness of each ear", "28", "0.55 d"], ["Pin diameter", "Ø30", "0.6 d"], ["Pin length", "106", "2.1 d"], ["Collar length", "30", "0.6 d"], ["Taper pin", "Ø6", "0.12 d"]], [3.5, 1, 1.4],
        "Proportions are read from the figure and given as a ratio to the shaft diameter so that they can be checked quickly."),
]
UJ_FLAG = ("Fig. No. 5 is a small scan; some sizes (the exact outline of the fork ears and the length of the collar) are hard to read.",
           "The drawings use the sizes legible in the figure (Ø88, 86, 44, 28, Ø30, 106, Ø50, Ø6, 30) and are approximate in proportion. Take exact sizes from your paper's Fig. 5 in the exam.")
p.q("a", "Draw the sectional front view and top view of fork.", "pd-ujoint", C_ASM, UJ_COMMON + [
    FIG("pd_ujoint_parts", "Fork (C.I.): sectional front view and top view (approximate proportions)", part="fork"),
    H("Procedure"),
    N("Draw the centre line. Draw the boss: rectangle 86 long × Ø88; the bore Ø50 through it.",
      "At the right end draw the two ears: thickness 28 each with a gap of 44 between them; the ears taper to the end; hole Ø30 for the pin at the centre of the ears.",
      "Hatch the cut surface at 45° (C.I.), leaving the bore and the gap clean.",
      "Draw the top view by projection: rectangle 86 × 88 for the boss, the fork ends and the Ø30 hole as a circle; hidden bore and gap lines dashed.",
      "Show the Ø6 taper-pin hole in the boss if required, centre lines and dimensions."),
    MS(("Sectional front view", 4), ("Top view", 3), ("Dimensions, hatching, centre lines", 1))], qtype="drawing", flag=UJ_FLAG)
p.q("b", "Draw the front view and top view of center block and pin.", "pd-ujoint", C_ASM, [
    FIG("pd_ujoint_parts", "Centre block (C.I.) and pin (M.S.)", part="block_pin"),
    H("Procedure"),
    N("Centre block: draw a block 44 thick and 50 × 50 (the width equals the pin length region); two holes Ø30 at right angles to each other at the centre.",
      "Draw the front view in section (hatched) with the Ø30 hole as dashed lines, and the top view with the hole as a circle.",
      "Pin: draw a cylinder Ø30 × 106; near one end a Ø6 hole for the taper pin; chamfer the ends 2 × 45°.",
      "Draw the top view of the pin (a circle Ø30 with centre lines) and give dimensions."),
    MS(("Centre block – both views", 4), ("Pin – both views", 3), ("Dimensions", 1))], qtype="drawing", flag=UJ_FLAG)
p.q("c", "Draw the front view and top view of collar, shaft and key.", "pd-ujoint", C_ASM, [
    FIG("pd_ujoint_parts", "Collar, shaft and key", part="collar_shaft_key"),
    H("Procedure"),
    N("Shaft: a cylinder Ø50 with a broken end (free-hand break line). Draw the keyway for the key on the top of the shaft.",
      "Collar: Ø88 × 30 with a Ø50 bore and a keyway; draw it in section (hatched at 45°).",
      "Key: a rectangular key as in the part list (M.S.) placed in the keyway; draw it unsectioned in the front view when the cutting plane passes along its length.",
      "Draw the top view by projection: rectangle for the collar, shaft lines and the key outline; show hidden bore with dashed lines."),
    MS(("Collar and shaft – front view", 3), ("Key", 2), ("Top view", 2), ("Dimensions", 1))], qtype="drawing", flag=UJ_FLAG)

# ------------------------------------------------------------------ Q5
p.group(5, "Attempt any ONE of the following :", 16, 1)
p.q("a", "Fig. No. 6 shows the details of Oldham’s coupling. Draw the following views of the assembly :\n(i) Sectional Front View\n(ii) Left hand Side View\n[Parts: 1 Flange C.I. 2 off; 2 Central disc C.I. 1 off; 3 Shaft M.S. 2 off; 4 Taper key M.S. 2 off]", "pd-oldham", C_ASM, [
    T(["Part No.", "Part name", "Material", "Qty."], [["1", "Flange", "C.I.", "2"], ["2", "Central disc", "C.I.", "1"], ["3", "Shaft", "M.S.", "2"], ["4", "Taper key (20n6 × 12 × 96, taper 1 in 100)", "M.S.", "2"]], [1, 4, 1.2, 1]),
    T(["Feature (Fig. 6)", "Size", "Ratio to shaft d = 60"], [
        ["Flange head diameter", "Ø180", "3 d"], ["Hub diameter", "Ø120", "2 d"], ["Bore", "Ø60 H8", "d"], ["Hub length", "60", "d"], ["Head thickness (incl. 20 deep groove)", "46", "0.77 d"],
        ["Groove width", "38 H7", "0.63 d"], ["Disc diameter", "Ø180", "3 d"], ["Disc plate thickness", "20", "d/3"], ["Tongue width × height", "36 g6 × 20", "0.6 d × d/3"], ["Key width", "20", "d/3"], ["Keyway length in shaft", "108", "1.8 d"]], [3.6, 1.2, 1.6]),
    FIG("pd_oldham_assembly", "Oldham's coupling – sectional front view and left hand side view"),
    H("Procedure"),
    N("Draw the centre line of the shafts. Draw the left flange: hub Ø120 × 60, head Ø180 × 46, bore Ø60; the 38 mm groove 20 deep on the head's face (vertical).",
      "Draw the central disc Ø180 × 20 in the middle; its left tongue (36 × 20) enters the vertical groove of the left flange, its right tongue (turned through 90°) enters the horizontal groove of the right flange.",
      "Draw the right flange as a mirror image, with its groove horizontal (so in section it is cut along its length and only 38 mm of material is removed at the centre).",
      "Insert the shafts Ø60 up to the groove floors and the two taper keys 20 × 12 in the keyways (keys are shown unsectioned).",
      "Hatch the flanges at 45° and the disc at 45° in the opposite direction; show break lines on the shafts.",
      "Draw the left hand side view: circles Ø180, Ø120, Ø60, key outline, with dashed lines for the grooves. Add the overall dimensions and fits."),
    MS(("Sectional front view", 8), ("Left hand side view", 5), ("Hatching and dimensions", 2), ("Part names / fits", 1))], qtype="drawing",
    flag=("In Fig. 6, the hub diameter is printed as “φ12D” and the flange keyway width as “28H7”. The key is 20 mm wide (20n6) and the shaft keyway is 20H7.", "“φ12D” is read as Ø120 (2 × shaft diameter), and the flange keyway width is taken as 20 mm to suit the 20 mm key. The key length 96 is more than the 86 mm bore, so the key is shown projecting 10 mm beyond the hub."))
p.q("b", "Fig. No. 7 shows details of lathe tool post. Draw the following views of assembly :\n(i) Sectional FV\n(ii) Top view\n(iii) Prepare bill of material and indicate type of fit.\n[Parts: 1 Post C.I.; 2 Block C.I.; 3 Ring C.I.; 4 Wedge M.S.; 5 Screw C.I.; each 1 off]", "pd-lathe-post", C_ASM, [
    T(["Part No.", "Part name", "Material", "Qty.", "Remark"], [["1", "Post", "C.I.", "1", "Ø72 × 12 flange, Ø60 body, 144 high"], ["2", "Block", "C.I.", "1", "90 square × 18, Ø74 recess, Ø60 hole"], ["3", "Ring", "C.I.", "1", "Ø120 × 18, Ø60 bore, R144 seat"],
                                                   ["4", "Wedge", "M.S.", "1", "24 wide, 144 long, R144"], ["5", "Screw", "C.I.", "1", "M18 × 72, square head 18, collar Ø36"]], [0.9, 1.4, 1.1, 0.8, 3.6], "Bill of material"),
    NUM("PD-W24-Q5b-geom"),
    FIG("pd_lathe_post", "Lathe tool post – sectional front view and top view (assembly)", R=144),
    H("Procedure"),
    N("Draw the centre line. Draw the block: 90 square × 18, with the Ø74 recess 12 deep from below and the Ø60 hole in the 6 mm top plate.",
      "Draw the post: flange Ø72 × 12 in the recess, body Ø60 rising to 144, tapered to Ø48 over the top 36 mm; the 24-wide slot 66 long starting 60 below the top; the M18 hole at the top.",
      "Place the ring Ø120 × 18 round the post on the block; its top is the concave R144 seat (calculated above).",
      "Place the wedge (24 × 24 section) in the slot of the post resting on the ring seat.",
      "Insert the screw M18 from the top: square head 18, collar Ø36 × 6, shank 72 long; show screw unsectioned.",
      "Hatch the cut parts at 45° in different directions for adjacent parts; draw the top view by projection (wedge 24 × 144 across the post, ring Ø120, block 90 square, post Ø60, screw head).",
      "Give the overall dimensions, part numbers and the bill of material."),
    H("Types of fit"),
    NUM("PD-W24-Q5b-fits"),
    MS(("Sectional front view", 6), ("Top view", 4), ("Bill of material", 2), ("Types of fit", 2), ("Dimensions, hatching, finish", 2))], qtype="drawing",
    flag=("In the tolerance chart the entry for 24H7 is printed as “+0.021 / +40.000” and the wedge size “24n8” in the chart but “24n6” on the drawing. The post carries “φ60H7” and the block hole “φ60e8”, which is the reverse of normal practice (capital letters are for holes).",
          "24H7 is taken as +0.021 / 0.000 and 24n6 (+0.036 / +0.015). The Ø60 hole (block) is taken as H7 and the Ø60 post as e8, so that the fit is a clearance fit; if taken literally as printed the hole would be smaller than the shaft."))
