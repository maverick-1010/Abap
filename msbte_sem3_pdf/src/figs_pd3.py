"""Production Drawing figures, part 3: Oldham's coupling and lathe tool post."""
import math
from draw import *
from figreg import fig


def sect(f, pts, ang=45, gap=2.0, w=0.3):
    f.pline(pts, closed=True, w=1.2)
    f.hatch([pts], gap=gap, angle=ang, w=w)


def rr(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


# ---------------------------------------------------------------- Oldham's coupling, W24 assembly
@fig("pd_oldham_assembly")
def pd_oldham_assembly():
    """Sectional front view and left-hand side view of the assembly (W24 Q5a). Axis horizontal."""
    s = 0.40
    f = Fig(330, 475, s)
    ox, cy = 50, 335                    # x origin (left face of left hub) and axis height of the FV
    X = lambda x: ox + x
    # dimensions (mm) from Fig. 6 of the paper
    hub_r, head_r, bore_r, hubL, headL, grooveD, tong, key_w, key_t = 60, 90, 30, 60, 46, 20, 36, 20, 12
    x_head0 = hubL                       # 60
    x_face1 = hubL + headL               # 106 (right face of flange 1)
    x_groove1 = x_face1 - grooveD        # 86
    x_disc0, x_disc1 = x_face1, x_face1 + 20
    x_face2 = x_disc1                    # 126 (left face of flange 2)
    x_groove2 = x_face2 + grooveD        # 146
    x_end = x_face2 + headL + hubL       # 232
    # --- flange 1 (left) section: hub + head up to groove floor
    for sg in (1, -1):
        pts = [(X(0), cy + sg * bore_r), (X(0), cy + sg * hub_r), (X(x_head0), cy + sg * hub_r), (X(x_head0), cy + sg * head_r),
               (X(x_groove1), cy + sg * head_r), (X(x_groove1), cy + sg * bore_r)]
        sect(f, pts, 45)
    # --- flange 2 (right): hub + head; groove (|z| < 19) cut from the face
    for sg in (1, -1):
        pts = [(X(x_face2), cy + sg * 19), (X(x_face2), cy + sg * head_r), (X(x_face2 + headL), cy + sg * head_r), (X(x_face2 + headL), cy + sg * hub_r),
               (X(x_end), cy + sg * hub_r), (X(x_end), cy + sg * bore_r), (X(x_face2 + headL - 0), cy + sg * bore_r), (X(x_groove2), cy + sg * bore_r) if False else (X(x_face2 + headL), cy + sg * bore_r)]
        pts = [(X(x_face2), cy + sg * 19), (X(x_face2), cy + sg * head_r), (X(x_face2 + headL), cy + sg * head_r), (X(x_face2 + headL), cy + sg * hub_r),
               (X(x_end), cy + sg * hub_r), (X(x_end), cy + sg * bore_r), (X(x_groove2), cy + sg * bore_r), (X(x_groove2), cy + sg * 19)]
        sect(f, pts, 45)
    # --- central disc (hatched the other way): plate + left tongue (full height) + right tongue (36 wide)
    sect(f, rr(X(x_groove1), cy - head_r, X(x_disc1), cy + head_r), -45)
    f.line(X(x_disc0), cy - head_r, X(x_disc0), cy + head_r, w=0.8)
    sect(f, rr(X(x_disc1), cy - tong / 2, X(x_groove2), cy + tong / 2), -45)
    # --- shafts (not sectioned): left shaft ends at the groove floor, right shaft starts at the groove floor
    f.line(X(-35), cy + bore_r, X(x_groove1), cy + bore_r, w=1.2); f.line(X(-35), cy - bore_r, X(x_groove1), cy - bore_r, w=1.2)
    f.line(X(x_groove2), cy + bore_r, X(x_end + 35), cy + bore_r, w=1.2); f.line(X(x_groove2), cy - bore_r, X(x_end + 35), cy - bore_r, w=1.2)
    f.line(X(x_groove1), cy - bore_r, X(x_groove1), cy + bore_r, w=1.2); f.line(X(x_groove2), cy - bore_r, X(x_groove2), cy + bore_r, w=1.2)
    for xb in (X(-35), X(x_end + 35)):
        f.pline([(xb, cy + bore_r), (xb + 3, cy + 15), (xb - 3, cy), (xb + 3, cy - 15), (xb, cy - bore_r)], w=0.9)
    # --- keys (sectioned) on top of the shafts: 20 x 12, length 96
    kz0, kz1 = bore_r - 6, bore_r + 6
    kx0 = -10
    f.pline(rr(X(kx0), cy + kz0, X(kx0 + 96), cy + kz1), closed=True, w=1.2)
    f.pline(rr(X(x_end - 86), cy + kz0, X(x_end - 86 + 96), cy + kz1), closed=True, w=1.2)
    # centre line and dimensions
    f.center_h(X(-40), X(x_end + 40), cy, 4)
    f.dim_h(X(0), X(x_end), cy - head_r, f"{x_end}", off=-14, ext_from=(cy - head_r, cy - hub_r))
    f.dim_h(X(x_head0), X(x_face1), cy + head_r, "46", off=8, ext_from=(cy + head_r, cy + head_r), size=6.5)
    f.dim_h(X(0), X(x_head0), cy + hub_r, "60", off=22, ext_from=(cy + hub_r, cy + hub_r), size=6.5)
    f.dim_h(X(x_groove1), X(x_disc1), cy + head_r, "40", off=22, ext_from=(cy + head_r, cy + head_r), size=6.5)
    f.dim_v(cy - head_r, cy + head_r, X(x_face1 + 6), "Ø180", off=0, size=6.8) if False else f.dim_v(cy - head_r, cy + head_r, X(x_end + 6), "Ø180", off=14, ext_from=(X(x_end), X(x_end)), size=6.8) if False else None
    f.dim_v(cy - hub_r, cy + hub_r, X(0), "Ø120", off=-12, ext_from=(X(0), X(0)), size=6.8)
    f.dim_v(cy - bore_r, cy + bore_r, X(-35), "Ø60 f8 / H8", off=-10, size=6.2)
    f.text(X(x_end / 2), cy + head_r + 36, "SECTIONAL FRONT VIEW (assembly)", size=8, bold=True)
    for xx, yy, tx in ((X(30), cy - hub_r - 6, "1 Flange"), (X(x_disc0 + 10), cy - head_r - 7, "2 Central disc"), (X(x_end - 30), cy - hub_r - 6, "1 Flange"), (X(-20), cy + kz1 + 8, "4 Key")):
        f.text(xx, yy, tx, size=6.8)
    f.text(X(-30), cy + bore_r + 6, "3 Shaft", size=6.8)
    # --- left-hand side view (looking from the left)
    cx, cy2 = 150, 125
    f.circle(cx, cy2, head_r, w=1.3)                       # flange head
    f.circle(cx, cy2, hub_r, w=1.3)                        # hub
    f.circle(cx, cy2, bore_r, w=1.3)                       # shaft end
    f.rect(cx - key_w / 2, cy2 + kz0, key_w, key_t, lw=1.2)
    f.line(cx - 19, cy2 - head_r, cx - 19, cy2 + head_r, w=0.6, dash=HIDDEN); f.line(cx + 19, cy2 - head_r, cx + 19, cy2 + head_r, w=0.6, dash=HIDDEN)
    f.line(cx - head_r, cy2 - 18, cx + head_r, cy2 - 18, w=0.6, dash=HIDDEN); f.line(cx - head_r, cy2 + 18, cx + head_r, cy2 + 18, w=0.6, dash=HIDDEN)
    f.center_h(cx - head_r, cx + head_r, cy2, 5); f.center_v(cx, cy2 - head_r, cy2 + head_r, 5)
    f.dim_h(cx - head_r, cx + head_r, cy2 - head_r, "Ø180", off=-8, ext_from=(cy2 - head_r, cy2 - head_r))
    f.text(cx, cy2 - head_r - 24, "LEFT HAND SIDE VIEW", size=8, bold=True)
    f.text(cx + head_r + 8, cy2 + 8, "dashed: grooves of the", size=6.6, anchor="start"); f.text(cx + head_r + 8, cy2 + 2, "two flanges and tongues", size=6.6, anchor="start")
    return f.d


# ---------------------------------------------------------------- Oldham's coupling, S25 details
@fig("pd_oldham_details")
def pd_oldham_details(part="flange"):
    s = 0.62
    f = Fig(265, 215, s)
    hub_r, head_r, bore_r, hubL, headL, gD, gW, kw, kt = 53, 85, 25, 50, 38, 16, 30, 16, 10
    ox, cy = 20, 100
    if part == "flange":
        for sg in (1, -1):
            pts = [(ox, cy + sg * bore_r), (ox, cy + sg * hub_r), (ox + hubL, cy + sg * hub_r), (ox + hubL, cy + sg * head_r),
                   (ox + hubL + headL - gD, cy + sg * head_r), (ox + hubL + headL - gD, cy + sg * bore_r)]
            sect(f, pts, 45)
        # groove (15 wide in the plane) -> section through y=0 shows groove floor
        f.pline(rr(ox + hubL + headL - gD, cy - head_r, ox + hubL + headL, cy + head_r), closed=True, w=0.0)
        f.line(ox + hubL + headL, cy - head_r, ox + hubL + headL, cy + head_r, w=0.5, dash=HIDDEN)
        f.line(ox + hubL + headL - gD, cy - head_r, ox + hubL + headL - gD, cy + head_r, w=1.2)
        f.line(ox, cy - bore_r, ox + hubL + headL - gD, cy - bore_r, w=1.2); f.line(ox, cy + bore_r, ox + hubL + headL - gD, cy + bore_r, w=1.2)
        f.rect(ox, cy + bore_r, hubL + headL - gD, kt - 4, lw=0.0) if False else None
        f.center_h(ox - 6, ox + hubL + headL + 6, cy, 0)
        f.dim_h(ox, ox + hubL, cy - hub_r, "50", off=-10, ext_from=(cy - hub_r, cy - hub_r))
        f.dim_h(ox + hubL, ox + hubL + headL, cy - head_r, "38", off=-10, ext_from=(cy - head_r, cy - head_r))
        f.dim_h(ox + hubL + headL - gD, ox + hubL + headL, cy + head_r, "16", off=6, ext_from=(cy + head_r, cy + head_r), size=6.5)
        f.dim_v(cy - hub_r, cy + hub_r, ox, "Ø106", off=-8, ext_from=(ox, ox))
        f.dim_v(cy - head_r, cy + head_r, ox + hubL + headL, "Ø170", off=12, ext_from=(ox + hubL + headL, ox + hubL + headL))
        f.dim_v(cy - bore_r, cy + bore_r, ox + 14, "Ø50 H8", off=0, size=6.2)
        f.text(ox + 60, cy + head_r + 14, "FLANGE – sectional front view", size=8, bold=True)
        # side view
        cx = 190
        f.circle(cx, cy, head_r, w=1.3); f.circle(cx, cy, hub_r, w=1.3); f.circle(cx, cy, bore_r, w=1.3)
        f.rect(cx - kw / 2, cy + bore_r, kw, kt - 4 + 0, lw=1.2) if False else f.rect(cx - kw / 2, cy + bore_r - 0, kw, 5, lw=1.2)
        f.line(cx - gW / 2, cy - head_r, cx - gW / 2, cy + head_r, w=0.6, dash=HIDDEN); f.line(cx + gW / 2, cy - head_r, cx + gW / 2, cy + head_r, w=0.6, dash=HIDDEN)
        f.center_h(cx - head_r, cx + head_r, cy, 5); f.center_v(cx, cy - head_r, cy + head_r, 5)
        f.dim_h(cx - gW / 2, cx + gW / 2, cy + head_r, "30 (groove)", off=7, ext_from=(cy + head_r, cy + head_r), size=6.2)
        f.text(cx, cy + head_r + 14, "SIDE VIEW", size=8, bold=True)
    elif part == "disc":
        T, tl, tw = 32, 16, 30
        f.rect(ox, cy - head_r, T, 2 * head_r, lw=1.3) if False else None
        sect(f, rr(ox, cy - head_r, ox + T, cy + head_r), 45)
        sect(f, rr(ox - tl, cy - head_r, ox, cy + head_r), -45) if False else None
        sect(f, rr(ox + T, cy - tw / 2, ox + T + tl, cy + tw / 2), 45)
        sect(f, rr(ox - tl, cy - head_r, ox, cy + head_r), 45)
        f.center_h(ox - 24, ox + T + 24, cy, 0)
        f.dim_h(ox - tl, ox, cy + head_r, "16", off=6, ext_from=(cy + head_r, cy + head_r), size=6.5)
        f.dim_h(ox, ox + T, cy + head_r, "32", off=6, ext_from=(cy + head_r, cy + head_r), size=6.5)
        f.dim_h(ox + T, ox + T + tl, cy - tw / 2, "16", off=-8, ext_from=(cy - tw / 2, cy - tw / 2), size=6.5)
        f.dim_v(cy - head_r, cy + head_r, ox + T + tl, "Ø170", off=14, ext_from=(ox + T + tl, ox + T + tl))
        f.text(ox + 20, cy + head_r + 14, "CENTRAL DISC – front view (section)", size=8, bold=True)
        cx = 190
        f.circle(cx, cy, head_r, w=1.3)
        f.rect(cx - tw / 2, cy - head_r, tw, 2 * head_r, lw=1.2)
        f.line(cx - head_r, cy - tw / 2, cx + head_r, cy - tw / 2, w=0.7, dash=HIDDEN); f.line(cx - head_r, cy + tw / 2, cx + head_r, cy + tw / 2, w=0.7, dash=HIDDEN)
        f.center_h(cx - head_r, cx + head_r, cy, 5); f.center_v(cx, cy - head_r, cy + head_r, 5)
        f.dim_h(cx - tw / 2, cx + tw / 2, cy + head_r, "30", off=7, ext_from=(cy + head_r, cy + head_r), size=6.5)
        f.text(cx, cy + head_r + 14, "SIDE VIEW (tongues at 90°)", size=8, bold=True)
    elif part == "shaft":
        L = 150
        f.rect(ox, cy - bore_r, L, 2 * bore_r, lw=1.3)
        f.pline([(ox + L, cy + bore_r), (ox + L - 3, cy + 12), (ox + L + 3, cy), (ox + L - 3, cy - 12), (ox + L, cy - bore_r)], w=0.9)
        f.rect(ox + 8, cy + bore_r - 5, 108, 5, lw=0.0) if False else None
        f.line(ox, cy + bore_r - 5, ox + 108, cy + bore_r - 5, w=0.8); f.line(ox + 108, cy + bore_r - 5, ox + 108, cy + bore_r, w=0.8)
        f.center_h(ox - 6, ox + L + 6, cy, 0)
        f.dim_v(cy - bore_r, cy + bore_r, ox, "Ø50 g8", off=-8, ext_from=(ox, ox))
        f.dim_h(ox, ox + 108, cy - bore_r, "keyway length", off=-8, ext_from=(cy - bore_r, cy - bore_r), size=6.2)
        f.text(ox + 40, cy + bore_r + 18, "SHAFT – front view", size=8, bold=True)
        cx = 205
        sect(f, [(cx + bore_r * math.cos(math.radians(a)), cy + bore_r * math.sin(math.radians(a))) for a in range(0, 360, 6) if True][:0] or [(cx + bore_r * math.cos(math.radians(a)), cy + bore_r * math.sin(math.radians(a))) for a in range(0, 360, 6)], 45)
        f.rect(cx - kw / 2, cy + bore_r - 5, kw, 5, lw=1.0, fill=colors.white)
        f.center_h(cx - bore_r, cx + bore_r, cy, 4); f.center_v(cx, cy - bore_r, cy + bore_r, 4)
        f.text(cx, cy + bore_r + 18, "SIDE VIEW (section)", size=8, bold=True)
    elif part == "key":
        L = 80
        f.rect(ox, cy + 22, L, kt, lw=1.3)
        f.line(ox, cy + 22 + kt, ox + L, cy + 22 + kt - 1, w=0.0)
        f.text(ox + L / 2, cy + 22 + kt + 6, "KEY – front view (taper 1 in 100 on top)", size=7, bold=True)
        f.dim_h(ox, ox + L, cy + 22, "length (as per fit)", off=-6, size=6.2)
        f.dim_v(cy + 22, cy + 22 + kt, ox + L, "10", off=6, ext_from=(ox + L, ox + L), size=6.5)
        f.rect(ox, cy - 30, L, kw, lw=1.3)
        f.dim_v(cy - 30, cy - 30 + kw, ox + L, "16", off=6, ext_from=(ox + L, ox + L), size=6.5)
        f.text(ox + L / 2, cy - 30 - 8, "TOP VIEW", size=7, bold=True)
        f.rect(ox + L + 40, cy + 14, kw, kt + 8, lw=1.3) if False else f.rect(ox + L + 40, cy + 22, kw, kt, lw=1.3)
        f.text(ox + L + 48, cy + 22 + kt + 6, "SIDE VIEW", size=7, bold=True)
    return f.d


# ---------------------------------------------------------------- Lathe tool post assembly
@fig("pd_lathe_post")
def pd_lathe_post(R=146):
    s = 0.5
    f = Fig(330, 235, s)
    cx, oz = 80, 45                       # axis x and base level of the post (z = 0)
    Z = lambda z: oz + z
    z0 = 36 - (R - math.sqrt(R * R - 60 * 60))          # dish bottom (on axis)
    dish = lambda r: z0 + (R - math.sqrt(R * R - r * r))
    # block (C.I.): two pieces, recess phi74 x 12 below, hole phi60 through the 6 mm plate
    for sg in (1, -1):
        pts = [(cx + sg * 45, Z(0)), (cx + sg * 37, Z(0)), (cx + sg * 37, Z(12)), (cx + sg * 30, Z(12)), (cx + sg * 30, Z(18)), (cx + sg * 45, Z(18))]
        sect(f, pts, -45)
    # ring (C.I.) with dish top
    for sg in (1, -1):
        arc = [(cx + sg * r, Z(dish(r))) for r in [60 - 30 * i / 20 for i in range(21)]]
        sect(f, [(cx + sg * 30, Z(18)), (cx + sg * 60, Z(18)), (cx + sg * 60, Z(36))] + arc[1:], -45, gap=2.4)
    # post (C.I.)
    post = [(-36, 0), (36, 0), (36, 12), (30, 12), (30, 108), (24, 144), (9, 144), (9, 84), (12, 84), (12, 18), (-12, 18), (-12, 84), (-9, 84), (-9, 144), (-24, 144), (-30, 108), (-30, 12), (-36, 12)]
    sect(f, [(cx + x, Z(z)) for x, z in post], 45)
    # wedge in the slot (section: 24 x 24)
    sect(f, rr(cx - 12, Z(z0), cx + 12, Z(z0 + 24)), 45, gap=1.6)
    f.line(cx - 12, Z(z0), cx + 12, Z(z0), w=1.4)
    # screw (not sectioned)
    f.rect(cx - 9, Z(72), 18, 72, lw=1.2, fill=colors.white)
    f.line(cx - 7.7, Z(84), cx - 7.7, Z(144), w=0.35); f.line(cx + 7.7, Z(84), cx + 7.7, Z(144), w=0.35)
    f.line(cx - 8, Z(72), cx - 6, Z(72), w=0.0)
    f.rect(cx - 18, Z(144), 36, 6, lw=1.2, fill=colors.white)
    f.rect(cx - 9, Z(150), 18, 15, lw=1.2, fill=colors.white)
    f.center_v(cx, Z(-6), Z(172), 0)
    # dimensions
    f.dim_h(cx - 60, cx + 60, Z(36), "Ø120", off=14, ext_from=(Z(36), Z(36)))
    f.dim_h(cx - 45, cx + 45, Z(0), "90", off=-8, ext_from=(Z(0), Z(0)))
    f.dim_h(cx - 36, cx + 36, Z(0), "Ø72", off=-18, ext_from=(Z(0), Z(0)), size=6.5)
    f.dim_v(Z(0), Z(165), cx - 66, "165", off=-6, ext_from=(cx - 45, cx - 45))
    f.dim_v(Z(12), Z(144), cx + 66, "132", off=6, ext_from=(cx + 24, cx + 24), size=6.5)
    f.dim_h(cx - 12, cx + 12, Z(60), "24", off=0, size=6.2)
    # part names
    for (x, z, tx) in ((cx + 50, Z(9), "2 Block"), (cx + 64, Z(28), "3 Ring"), (cx + 30, Z(100), "1 Post"), (cx - 14, Z(z0 + 28), "4 Wedge")):
        f.text(x, z, tx, size=6.6, anchor="start")
    f.text(cx - 38, Z(155), "5 Screw", size=6.6, anchor="end")
    f.text(cx, Z(-30), "SECTIONAL FRONT VIEW", size=8, bold=True)
    # ---- top view
    tx, ty = 250, 120
    f.rect(tx - 45, ty - 45, 90, 90, lw=1.3)
    f.circle(tx, ty, 60, w=1.3)
    f.rect(tx - 12, ty + 30, 24, (R / 2 + 0) - 30, lw=1.3) if False else None
    half = R / 2
    for sg in (1, -1):
        f.rect(tx - 12, ty + (30 if sg > 0 else -half), 24, half - 30, lw=1.3)
    f.circle(tx, ty, 30, w=1.3)
    f.circle(tx, ty, 24, w=0.0)
    f.circle(tx, ty, 18, w=1.2)
    f.rect(tx - 9, ty - 9, 18, 18, lw=1.2)
    f.center_h(tx - 78, tx + 78, ty, 0); f.center_v(tx, ty - 78, ty + 78, 0)
    f.dim_h(tx - 45, tx + 45, ty - 45, "90", off=-8, ext_from=(ty - 45, ty - 45))
    f.dim_v(ty - half, ty + half, tx + 70, f"{R}", off=0, ext_from=(tx + 12, tx + 12), size=6.5) if False else f.dim_v(ty - half, ty + half, tx + 66, f"{R}", off=8, ext_from=(tx + 12, tx + 12), size=6.5)
    f.text(tx, ty - half - 14, "TOP VIEW", size=8, bold=True)
    return f.d
