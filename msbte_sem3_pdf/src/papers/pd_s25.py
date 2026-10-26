from dsl import *

p = Paper("PD-S25", "313311", "Production Drawing", "PD", "S25", "Summer 2025", "K-scheme", "4 Hours", 70, "24225",
          "Production_Drawing_Summer_2025_Question_Paper_Second_K_Scheme_Paper.pdf", 7)

C_CONV = "Conventions and standard representations (BIS SP-46)"
C_FIT = "Limits, fits, tolerances, surface finish and welding symbols"
C_PROJ = "Orthographic and auxiliary views"
C_ASM = "Assembly and detail drawings"

p.group(1, "Attempt any FIVE of the following:", 10, 5)
p.q("a", "Draw the conventional representation of the following:\ni) Long Break in pipe\nii) I-section pipe.", "pd-pipe-valve", C_CONV, [
    FIG("pd_pipe_breaks", None), FIG("pd_i_section_break", None),
    B("<b>Long break in pipe:</b> the middle portion is omitted and the cut ends are shown by thin zig-zag lines (free-hand), with the centre line continuing across.",
      "<b>I-section:</b> a rolled I-section is shown with its outline in the end view; when a long part is broken, wavy free-hand break lines are used across the section."),
    MS(("Long break in pipe", 1), ("I-section", 1))],
    flag=("“I-section pipe” is not a standard item; an I-section is a rolled steel section, not a pipe.", "It is answered as the conventional representation of a break in an I-section (the usual BIS SP-46 item “break in rolled sections”)."))
p.q("b", "Draw the conventional representations of following:\ni) Bearings\nii) Holes on circular pitch.", "pd-pcd-bearing", C_CONV, [
    FIG("pd_bearings", None), FIG("pd_holes_pcd", None),
    MS(("Bearings", 1), ("Holes on circular pitch", 1))])
p.q("c", "Draw the conventional representations of following machine components:\ni) Bevel Gear\nii) Spur Gear", "pd-gears", C_CONV, [
    FIG("pd_gears", None, which="bevel"), FIG("pd_gears", None, which="spur"),
    P("In both gears the teeth are not drawn: addendum (outer) circle/lines thick, pitch circle/lines thin chain, root circle thin continuous (omitted in sections)."),
    MS(("Bevel gear", 1), ("Spur gear", 1))])
p.q("d", "Define “Taper”. Draw its standard convention.", "pd-taper", C_CONV, [
    P("<b>Taper</b> is the ratio of the difference between the diameters of the two ends of a cone (frustum) to its length:"),
    F("Taper = (D − d) / L = 1 : k"),
    P("It is shown by the taper symbol (a right-angled triangle whose sloping side points the same way as the taper) followed by the ratio, drawn on a leader or on a reference line parallel to the axis, as in the figure for a 1 : 10 taper (example)."),
    FIG("pd_taper", "Standard convention of taper (example 1 : 10)", D=40.0, L=100.0, k=10),
    MS(("Definition with formula", 1), ("Convention (symbol and ratio)", 1))])
p.q("e", "Draw the actual view and conventional representation of:\ni) Internal Screw thread\nii) Semi-elliptic leaf spring.", "pd-thread-spring", C_CONV, [
    FIG("pd_int_thread", None), FIG("pd_leaf_spring", None),
    MS(("Internal screw thread – actual and conventional", 1), ("Leaf spring – actual and conventional", 1))])
p.q("f", "Draw a sketch showing basic size, lower deviation, upper deviation and tolerance.", "pd-tolerance-sketch", C_FIT, [
    FIG("pd_tolerance_sketch", None),
    MS(("Sketch with zero line, basic size and zone", 2))])
p.q("g", "State the meaning of the symbol shown in Figure No. 1.\n[Fig. No. 1: machining symbol with 8 above the bar, 2 at left, “Grinding” above the extension line and 0.8 below it]", "pd-surface-meaning", C_FIT, [
    FIG("pd_surface_meaning", None, top="8", low="2", method="Grinding", sampling="0.8"),
    P("The surface is to be finished by <b>grinding</b>; the roughness Ra must lie between <b>2 μm and 8 μm</b>; the sampling length is <b>0.8 mm</b>."),
    MS(("Roughness limits 8 and 2", 1), ("Grinding and sampling length 0.8", 1))])

p.group(2, "Attempt any ONE of the following:", 8, 1)
p.q("a", "Figure No. 2 shows front view, incomplete top view and partial auxiliary view of an object. Redraw the given views and complete the top view (use first angle method of projection.)\n[Fig. No. 2: bent plate – base 75 × 6, arm 60 long at 120° with the base, square hole 20 in the rounded end of the arm, top view with rounded end R10 and slot 20 wide]", "pd-projection", C_PROJ, [
    NUM("PD-S25-Q2a"),
    H("Procedure (first angle method)"),
    N("Draw the XY line. Draw the front view as given: base 75 long × 6 thick, with the arm 60 long rising at 120° to the base (60° to the horizontal), two 10 mm layers at the arm end as shown.",
      "Draw the top view below the front view: project all vertical lines from the base. The base shows its outline with the rounded end and the 20 mm slot (R10 ends) as given.",
      "The inclined arm is foreshortened in the top view: its true length 60 becomes 60 cos 60° = 30 mm. Project the arm ends from the F.V. to get its length and keep its width 40 as in the auxiliary view.",
      "Project the square hole of the aux. view: its side across the arm stays 20 mm, the side along the arm becomes 20 cos 60° = 10 mm in the top view.",
      "Complete the top view: draw hidden edges (dashed), centre lines, and the thick outline; give the main dimensions."),
    MS(("Redraw front and auxiliary views", 3), ("Projection of base and arm in top view", 3), ("Hole, hidden lines and dimensions", 2))],
    qtype="drawing",
    flag=("The printed figure is small. The exact shape of the arm end (two 10 mm layers and the square hole turned 45°) cannot be read with certainty.",
          "Only the lengths that can be calculated are given (above); no finished view is drawn here, because it would need guessing the shape of the object. Check them against your figure."))
p.q("b", "Figure No. 3 shows front view and left hand side view of an object. Draw the given views and project an auxiliary top view looking in the direction of X.", "pd-projection", C_PROJ, [
    FIG("pd_s25_2b", "Front view, left hand side view and the auxiliary top view looking along X (45°)"),
    H("Procedure"),
    N("Draw the front view: base 100, left face sloping at 45°, height 50. Draw the left hand side view: channel 75 wide and 50 high, bottom 30 wide with 45° chamfers, groove R25 with centre 15 below the top.",
      "Draw the auxiliary plane (reference line) at 90° to the direction of viewing X, that is parallel to the sloping face of the front view.",
      "Project every point of the sloping face and of the top face from the F.V. parallel to the direction X (at 45° to the base) up to the new reference line.",
      "Measure the distances from the L.H.S.V. (the widths: ± 37.5, ± 25, ± 15) and mark them on the projectors, using the centre line as datum.",
      "The groove R25 appears on the sloping face as an ellipse (semi-axes 25 and 25/sin 45° = 35.4 mm). Join the points with a smooth curve.",
      "Draw the top face as two strips and the groove edges (± 25), complete the outline, add centre lines and dimensions."),
    MS(("Redraw the given views", 3), ("Auxiliary reference line and projectors", 2), ("Elliptical groove and outline in auxiliary view", 2), ("Dimensions / line work", 1))],
    qtype="drawing")

p.group(3, "Attempt any FIVE of the following:", 20, 5)
p.q("a", "Draw conventional representation of any four of the following:\ni) Glass\nii) Pipe or tubing\niii) Cast iron\niv) Splined shaft\nv) Globe valve\nvi) Counter sunk", "pd-material", C_CONV, [
    P("All six are shown; any four are to be attempted (1 mark each)."),
    FIG("pd_materials", None, which=("glass", "cast iron")), FIG("pd_pipe_tube", None), FIG("pd_spline", None), FIG("pd_gate_globe", None, which="globe"), FIG("pd_csk", None),
    MS(("Any four items, 1 mark each", 4))])
p.q("b", "Draw a sketch to represent taper 1:20 on a shaft of φ40mm and length 120mm.", "pd-taper", C_CONV, [
    NUM("PD-S25-Q3b"), FIG("pd_taper", "Taper 1:20 on a shaft Ø40 × 120", D=40.0, L=120.0, k=20),
    MS(("Calculation of small end diameter", 1), ("Sketch with taper symbol and dimensions", 3))], qtype="numerical")
p.q("c", "Draw the symbols for the any two of following:\ni) Single V butt weld\nii) Seam weld\niii) Spot weld\niv) Fillet weld with convex finish.", "pd-weld-symbols", C_FIT, [
    P("All four are shown; any two are to be attempted (2 marks each)."),
    FIG("pd_weld_symbols", None),
    MS(("Any two symbols, 2 marks each", 4))])
p.q("d", "Draw the symbols of following features which are controlled in geometrical tolerance.\ni) Symmetry\nii) Angularity\niii) Concentricity\niv) Flatness.", "pd-gt-symbols", C_FIT, [
    FIG("pd_gt_symbols", None, names=("symmetry", "angularity", "concentricity", "flatness")),
    MS(("Each symbol, 1 mark", 4))])
p.q("e", "Two mild steel plants of 8 mm thickness are to be welded to have a lap joint by a fillet weld of leg length 8 mm. Represent the weld on drawing with proper symbol.", "pd-weld-drawing", C_FIT, [
    FIG("pd_fillet_lap", "Lap joint with fillet weld, leg length 8 mm"),
    N("Draw the two plates of 8 mm thickness overlapping (lap joint).", "Draw the fillet weld (triangle with 8 mm legs) at the edge of the upper plate.", "Draw the arrow line to the joint, the reference line and the fillet weld symbol (triangle) below the line, with the leg length 8 to its left."),
    MS(("Lap joint drawing with weld", 2), ("Weld symbol with 8 mm leg", 2))],
    flag=("The question says “plants”; plates are meant.", "Read as “plates”."))
p.q("f", "What is the meaning of symbol at x and y as shown in Figure No. 4.\n[Fig. No. 4: X = ∥ 0.03 A, Y = ⊥ 0.03 A, datum A]", "pd-gt-meaning", C_FIT, [
    FIG("pd_gt_symbols", None, names=("parallelism", "perpendicularity")),
    B("<b>X (∥ 0.03 A):</b> parallelism – the toleranced surface must lie between two parallel planes 0.03 mm apart that are parallel to datum A.",
      "<b>Y (⊥ 0.03 A):</b> perpendicularity – the toleranced surface must lie between two parallel planes 0.03 mm apart that are perpendicular to datum A."),
    MS(("Meaning of X", 2), ("Meaning of Y", 2))])
p.q("g", "The shaft is given as φ20(+0.023/+0.012) and hole size is φ20(+0.018/+0.000). Determine the types of fit between them.", "pd-fit", C_FIT, [
    NUM("PD-S25-Q3g"),
    MS(("Limits of shaft and hole", 1), ("Maximum and minimum clearance", 2), ("Type of fit", 1))], qtype="numerical")

p.group(4, "Attempt the following:", 16, 1)
p.q("", "Figure No. 5 shows sectional F.V. and S.V. of the assembly of ‘OLDHAM’S COUPLING’. Draw the following details by using first angle method:\ni) Flange: Front view and S.V.\nii) Central disc: Front view and S.V.\niii) Shaft: Front view and S.V.\niv) Key: F.V., T.V and S.V.\n[Part list: 1 Flange C.I. ×2; 2 Centre block C.I. ×1; 3 Keys M.S. ×2; 4 Shaft M.S. ×2. Fit chart: 16H7/n6 transition, 30H7/g6 clearance, 50H8/g8 clearance]", "pd-oldham", C_ASM, [
    T(["Part No.", "Part name", "Material", "Qty."], [["1", "Flange", "C.I.", "2"], ["2", "Centre block (disc)", "C.I.", "1"], ["3", "Keys (taper 16 × 10)", "M.S.", "2"], ["4", "Shaft Ø50", "M.S.", "2"]], [1, 3, 1.2, 1]),
    T(["Feature (Fig. 5)", "Size", "Ratio to shaft d = 50"], [
        ["Flange head diameter", "Ø170", "3.4 d"], ["Hub diameter", "Ø106", "2.1 d"], ["Hub length", "50", "d"], ["Head thickness (with 16 deep groove)", "38", "0.76 d"],
        ["Groove (tongue) width", "30", "0.6 d"], ["Groove depth = tongue height", "16", "0.32 d"], ["Disc thickness at centre", "16 + 16 = 32", "0.64 d"], ["Key", "16 × 10, taper", "0.32 d × 0.2 d"], ["Overall length of assembly", "50 + 38 + 16 + 16 + 38 + 50 = 208", "–"]], [3.4, 2.4, 1.6]),
    FIG("pd_oldham_details", "Flange – sectional front view and side view", part="flange"),
    FIG("pd_oldham_details", "Central disc – front view and side view", part="disc"),
    FIG("pd_oldham_details", "Shaft – front view and side view", part="shaft"),
    FIG("pd_oldham_details", "Key – front view, top view and side view", part="key"),
    H("Fits"), NUM("PD-S25-Q4-fits"),
    H("Procedure"),
    N("Study the assembly: note the part sizes (the dimension string 50, 38, 16, 16, 38, 50) and the fits.",
      "Flange: draw the centre line, hub Ø106 × 50, head Ø170 × 38 with a 30 wide × 16 deep groove across the face, bore Ø50 with the keyway for the 16 × 10 key; hatch at 45° in the front view; side view: circles Ø170, Ø106, Ø50 and the groove as dashed lines.",
      "Central disc: Ø170 plate, 32 thick, with a 30 wide × 16 high tongue on each face, the two tongues at 90° to each other; side view shows the disc, one tongue as a rectangle and the other as dashed lines.",
      "Shaft: cylinder Ø50 with a broken end, keyway 16 wide for the key; side view in section with the keyway.",
      "Key: rectangular 16 × 10, length to suit (hub bore), with the 1 in 100 taper on the top face; draw the three views.",
      "Give main dimensions, fits and tolerances shown in the fit chart."),
    MS(("Flange – F.V. and S.V.", 5), ("Central disc – F.V. and S.V.", 4), ("Shaft – F.V. and S.V.", 3), ("Key – F.V., T.V., S.V.", 2), ("Dimensions and fits", 2))],
    qtype="drawing",
    flag=("Fig. No. 5 is a rotated, low-resolution scan. The label “20” beside the groove, the exact length of the shaft and key, and the fit label printed on the drawing (“50H6/f6”) differ from the fit chart (“50H8/g8”).",
          "Sizes in the table are those legible in the figure; the fit chart is used for the fits. The shaft and key length are drawn to suit the hub (not given)."))

p.group(5, "Attempt any ONE of the following:", 16, 1)
p.q("a", "Figure No. 6 shows the details of ‘FOOT STEP BEARING’. Draw the following views of the assembly:\ni) Section Front view\nii) Top view\nUse suitable scale\nGive overall dimension. Show assembly fits.\n[Parts: 1 Body C.I.; 2 Bush G.M.; 3 Shaft M.S.; 4 Disc G.M.; 5 Pin M.S.; each 1 off]", "pd-foot-step", C_ASM, [
    T(["Part No.", "Part name", "Material", "Qty."], [["1", "Body", "C.I.", "1"], ["2", "Bush", "G.M. (gun metal)", "1"], ["3", "Shaft", "M.S.", "1"], ["4", "Disc", "G.M. (gun metal)", "1"], ["5", "Pin", "M.S.", "1"]], [1, 2.2, 2, 1], "Bill of material"),
    T(["Part", "Main sizes (read from Fig. 6)"], [
        ["Body", "Base 200 × 130 (4 slotted holes 15 wide); boss Ø94; height 88; bore Ø68 H7; sunk recess Ø71, 3 deep; pin hole Ø4.6"],
        ["Bush", "Ø68 outside, bore Ø50 H7, collar Ø78, 8 thick; length about 70; 8 wide oil groove"],
        ["Shaft", "Ø64 upper part, Ø50 H8 lower part 72 long; end R60"],
        ["Disc", "Ø50 e8 × 15, dished R60, pin hole Ø4, 6 deep"],
        ["Pin", "Ø4 × 12"]], [1, 6.5]),
    FIG("pd_foot_step", "Foot step bearing – sectional front view and top view (approximate proportions)"),
    H("Procedure"),
    N("Choose a scale (1 : 1 or 1 : 2). Draw the centre line and the base line. Draw the body: base 200 × 18, boss Ø94 up to 88, bore Ø68 with the Ø71 sunk recess 3 deep.",
      "Draw the bush Ø68 outside inside the bore, bore Ø50, with the collar Ø78 × 8 resting in the recess.",
      "Draw the disc (Ø50 × 15) at the bottom of the bush bore with the pin (Ø4) locating it; then the shaft Ø50 resting on the dished disc and its Ø64 upper portion above the bush.",
      "Hatch the cut parts at 45° in different directions for each part; the shaft, pin and disc are shown according to the sectioning rules (shaft and pin are not hatched).",
      "Draw the top view: rectangle 200 × 130, four slotted holes, circles Ø94, Ø78, Ø68, Ø64; centre lines.",
      "Give overall dimensions (200, 130, 88) and the fits (Ø68 H7/h6, Ø50 H7/e8, Ø8 H7/g6) with part numbers."),
    H("Fits"), NUM("PD-S25-Q5a-fits"),
    MS(("Sectional front view", 7), ("Top view", 4), ("Overall dimensions", 2), ("Assembly fits", 2), ("Part numbers / hatching", 1))],
    qtype="drawing",
    flag=("Fig. 6 is small and several labels are doubtful: the body bore is printed “Ø68Hz” (read as H7); the bush is “68g6” on the part but the tolerance chart gives “68h6”; the bush bore “50H7” has the chart value +0.039 (that is H8); signs of e8 and g6 are lost in the scan.",
          "H7 is used for the body bore; the chart values (68H7/68h6, 50H7 +0.039/0 with 50e8 −0.050/−0.089, 8H7/8g6) are used for the fits. The assembly sketch shows the main arrangement with approximate proportions."))
p.q("b", "Figure No. 7 shows the details of ‘LATHE TOOL POST’. Draw the following views of the assembly:\ni) Sectional front view\nii) Top view\niii) Prepare bill of material. Indicate types of fit.\n[Parts: 1 Post C.I.; 2 Block C.I.; 3 Ring C.I.; 4 Wedge C.I.; 5 Screw C.I.; each 1 off]", "pd-lathe-post", C_ASM, [
    T(["Part No.", "Part name", "Material", "Qty.", "Remark"], [["1", "Post", "C.I.", "1", "Ø72 × 12 flange, Ø60 body, 144 high"], ["2", "Block", "C.I.", "1", "90 square × 18, Ø74 recess, Ø60 hole"], ["3", "Ring", "C.I.", "1", "Ø120 × 18, Ø60 bore, R146 seat"],
                                                   ["4", "Wedge", "C.I.", "1", "24 wide, 146 long, R146"], ["5", "Screw", "C.I.", "1", "M18 × 72, square head 18, collar Ø36"]], [0.9, 1.4, 1.1, 0.8, 3.6], "Bill of material"),
    NUM("PD-S25-Q5b-geom"),
    FIG("pd_lathe_post", "Lathe tool post – sectional front view and top view (assembly)", R=146),
    H("Procedure"),
    N("Draw the centre line. Draw the block: 90 square × 18, with the Ø74 recess 12 deep from below and the Ø60 hole in the 6 mm top plate.",
      "Draw the post: flange Ø72 × 12 in the recess, body Ø60 rising to 144 high, tapered to Ø48 over the top 36 mm; the slot 24 wide and 66 long, starting 60 below the top; the M18 hole at the top.",
      "Place the ring Ø120 × 18 round the post, resting on the block; its top is the concave R146 seat (calculated above).",
      "Place the wedge (24 × 24 section) in the slot of the post on the ring seat.",
      "Insert the screw M18: square head 18, collar Ø36 × 6, shank 72 long; show the screw unsectioned.",
      "Hatch the cut parts at 45° (adjacent parts in opposite directions). Draw the top view by projection.",
      "Add overall dimensions, part numbers, bill of material and the types of fit."),
    H("Types of fit"),
    NUM("PD-S25-Q5b-fits"),
    MS(("Sectional front view", 6), ("Top view", 4), ("Bill of material", 2), ("Types of fit", 2), ("Dimensions, hatching, finish", 2))], qtype="drawing",
    flag=("The post carries “φ60H7” and the block hole “φ60e8”, which is the reverse of normal practice (capital letters are for holes). The wedge shows “24 h6” in its view while the chart gives “24n6”.",
          "The Ø60 hole (block) is taken as H7 and the Ø60 post as e8 (clearance fit) – if taken literally the hole would be smaller than the shaft. The wedge is taken as 24n6 as in the chart."))
