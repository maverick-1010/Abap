"""Vector drawing helper on top of reportlab.graphics (model units = mm).

Fig(w, h, scale) creates a Drawing w*scale mm by h*scale mm. Coordinates passed to the
methods are in model mm and are multiplied by `scale`. Line widths and text sizes are in
points and do NOT change with scale, so a 1:2 drawing still has readable dimensions.
"""
import math
import numpy as np
from reportlab.graphics.shapes import Drawing, Line, Rect, Circle, Polygon, PolyLine, String, Group
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth

MM = 72 / 25.4
THICK, MED, THIN = 1.0, 0.6, 0.3
HIDDEN = [3, 1.6]
CHAIN = [9, 2, 1.5, 2]
BLACK = colors.black
GREY = colors.Color(0.55, 0.55, 0.55)
LIGHT = colors.Color(0.85, 0.85, 0.85)
BLUE = colors.Color(0.1, 0.25, 0.6)
RED = colors.Color(0.75, 0.1, 0.1)
FONT, FONTB = "DV", "DV-B"


class Fig:
    def __init__(self, w, h, scale=1.0, fs=7.0):
        self.s = scale * MM
        self.w, self.h, self.fs = w, h, fs
        self.d = Drawing(w * self.s, h * self.s)

    # ----- primitives -----
    def _add(self, shape):
        self.d.add(shape)
        return shape

    def line(self, x1, y1, x2, y2, w=MED, dash=None, col=BLACK):
        ln = Line(x1 * self.s, y1 * self.s, x2 * self.s, y2 * self.s, strokeColor=col, strokeWidth=w)
        if dash:
            ln.strokeDashArray = dash
        return self._add(ln)

    def pline(self, pts, closed=False, w=MED, dash=None, fill=None, col=BLACK):
        flat = [c * self.s for p in pts for c in p]
        if closed:
            sh = Polygon(flat, strokeColor=col, strokeWidth=w, fillColor=fill)
        else:
            sh = PolyLine(flat, strokeColor=col, strokeWidth=w)
        if dash:
            sh.strokeDashArray = dash
        return self._add(sh)

    def rect(self, x, y, w, h, lw=MED, dash=None, fill=None, col=BLACK):
        r = Rect(x * self.s, y * self.s, w * self.s, h * self.s, strokeColor=col, strokeWidth=lw, fillColor=fill)
        if dash:
            r.strokeDashArray = dash
        return self._add(r)

    def circle(self, cx, cy, r, w=MED, dash=None, fill=None, col=BLACK):
        c = Circle(cx * self.s, cy * self.s, r * self.s, strokeColor=col, strokeWidth=w, fillColor=fill)
        if dash:
            c.strokeDashArray = dash
        return self._add(c)

    def arc_pts(self, cx, cy, r, a0, a1, n=48, ry=None):
        ry = r if ry is None else ry
        return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
                 cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]

    def arc(self, cx, cy, r, a0, a1, w=MED, dash=None, ry=None, col=BLACK):
        return self.pline(self.arc_pts(cx, cy, r, a0, a1, ry=ry), w=w, dash=dash, col=col)

    def curve(self, fn, t0, t1, n=60, w=MED, dash=None, col=BLACK):
        pts = [fn(t0 + (t1 - t0) * i / n) for i in range(n + 1)]
        return self.pline(pts, w=w, dash=dash, col=col)

    def text(self, x, y, s, size=None, anchor="middle", rot=0, bold=False, col=BLACK):
        size = size or self.fs
        st = String(0, 0, s, fontName=FONTB if bold else FONT, fontSize=size, fillColor=col, textAnchor=anchor)
        if rot:
            g = Group(st)
            g.translate(x * self.s, y * self.s)
            g.rotate(rot)
            return self._add(g)
        st.x, st.y = x * self.s, y * self.s
        return self._add(st)

    def tbox(self, x, y, s, size=None, anchor="middle", bold=False, pad=0.8, col=BLACK):
        """Text with a white box behind it (keeps labels readable over lines)."""
        size = size or self.fs
        tw = stringWidth(s, FONTB if bold else FONT, size) / self.s
        th = size / self.s * 0.95
        x0 = x - tw / 2 if anchor == "middle" else (x if anchor == "start" else x - tw)
        self._add(Rect((x0 - pad) * self.s, (y - 0.25 * th - pad * 0.5) * self.s, (tw + 2 * pad) * self.s,
                       (th + pad) * self.s, fillColor=colors.white, strokeColor=None, strokeWidth=0))
        return self.text(x, y, s, size=size, anchor=anchor, bold=bold, col=col)

    def label(self, x, y, s, size=None, anchor="middle", dx=0, dy=0, **kw):
        return self.text(x + dx, y + dy, s, size=size, anchor=anchor, **kw)

    # ----- drafting helpers -----
    def arrowhead(self, x, y, ang, size=4.0, fill=BLACK):
        """Filled arrow head with tip at (x, y), pointing along `ang` (radians)."""
        L, Wd = size, size * 0.32
        tx, ty = x * self.s, y * self.s
        bx, by = tx - L * math.cos(ang), ty - L * math.sin(ang)
        px, py = -math.sin(ang) * Wd, math.cos(ang) * Wd
        self._add(Polygon([tx, ty, bx + px, by + py, bx - px, by - py], fillColor=fill, strokeColor=fill, strokeWidth=0.2))

    def arrow(self, x1, y1, x2, y2, w=MED, size=4.0, col=BLACK, dash=None):
        self.line(x1, y1, x2, y2, w=w, col=col, dash=dash)
        self.arrowhead(x2, y2, math.atan2(y2 - y1, x2 - x1), size, col)

    def darrow(self, x1, y1, x2, y2, w=MED, size=4.0):
        self.line(x1, y1, x2, y2, w=w)
        a = math.atan2(y2 - y1, x2 - x1)
        self.arrowhead(x2, y2, a, size)
        self.arrowhead(x1, y1, a + math.pi, size)

    def center_h(self, x1, x2, y, ext=3):
        self.line(x1 - ext, y, x2 + ext, y, w=THIN, dash=CHAIN)

    def center_v(self, x, y1, y2, ext=3):
        self.line(x, y1 - ext, x, y2 + ext, w=THIN, dash=CHAIN)

    def center_mark(self, cx, cy, r):
        self.center_h(cx - r, cx + r, cy)
        self.center_v(cx, cy - r, cy + r)

    def dim_h(self, x1, x2, y, txt, off=0.0, ext_from=None, size=None, above=True, tick_gap=1.0):
        """Horizontal dimension between x1 and x2 drawn at height y+off.
        ext_from=(y1, y2) draws extension lines from the object edges up to the dimension line."""
        yd = y + off
        if ext_from is not None:
            for x, ye in zip((x1, x2), ext_from):
                sgn = 1 if yd >= ye else -1
                self.line(x, ye + sgn * tick_gap, x, yd + sgn * 1.5, w=THIN)
        self.darrow(x1, yd, x2, yd, w=THIN)
        size = size or self.fs
        tw = stringWidth(txt, FONT, size) / self.s
        if tw < abs(x2 - x1) - 6 / self.s * 1.0:
            self.text((x1 + x2) / 2, yd + (1.0 if above else -3.2), txt, size=size)
        else:
            self.text(max(x1, x2) + 1.5, yd + (1.0 if above else -3.2), txt, size=size, anchor="start")

    def dim_v(self, y1, y2, x, txt, off=0.0, ext_from=None, size=None, tick_gap=1.0):
        xd = x + off
        if ext_from is not None:
            for y, xe in zip((y1, y2), ext_from):
                sgn = 1 if xd >= xe else -1
                self.line(xe + sgn * tick_gap, y, xd + sgn * 1.5, y, w=THIN)
        self.darrow(xd, y1, xd, y2, w=THIN)
        size = size or self.fs
        self.text(xd - 1.2, (y1 + y2) / 2, txt, size=size, rot=90, anchor="middle")

    def leader(self, x1, y1, x2, y2, txt, size=None, anchor="start"):
        """Text label with a leader arrow pointing at (x1, y1); text sits at (x2, y2)."""
        self.arrow(x2, y2, x1, y1, w=THIN, size=3.2)
        self.text(x2 + (0.8 if anchor == "start" else -0.8), y2 + 0.8, txt, size=size or self.fs, anchor=anchor)

    def hatch(self, rings, gap=2.0, angle=45, w=THIN, col=BLACK):
        """Section hatching. `rings` = list of closed point lists, even-odd rule (holes allowed)."""
        th = math.radians(angle)
        dx, dy = math.cos(th), math.sin(th)
        nx, ny = -dy, dx
        allp = np.array([p for r in rings for p in r], dtype=float)
        proj = allp[:, 0] * nx + allp[:, 1] * ny
        c = math.ceil(proj.min() / gap) * gap
        while c < proj.max():
            ts = []
            for r in rings:
                n = len(r)
                for i in range(n):
                    (x0, y0), (x1, y1) = r[i], r[(i + 1) % n]
                    d0 = x0 * nx + y0 * ny - c
                    d1 = x1 * nx + y1 * ny - c
                    if (d0 < 0) != (d1 < 0):
                        u = d0 / (d0 - d1)
                        px, py = x0 + u * (x1 - x0), y0 + u * (y1 - y0)
                        ts.append(px * dx + py * dy)
            ts.sort()
            for i in range(0, len(ts) - 1, 2):
                a, b = ts[i], ts[i + 1]
                self.line(nx * c + dx * a, ny * c + dy * a, nx * c + dx * b, ny * c + dy * b, w=w, col=col)
            c += gap

    def frame(self, pad=0.5):
        self.rect(pad, pad, self.w - 2 * pad, self.h - 2 * pad, lw=THIN, col=GREY)


def serp(f, x0, x1, y, amp, n, w=1.3, col=BLACK):
    """Draw a horizontal serpentine tube with n vertical runs between x0 and x1."""
    d = (x1 - x0) / (n + 1)
    xs = [x0 + d * (i + 1) for i in range(n)]
    pts = [(x0, y), (xs[0], y), (xs[0], y + amp)]
    sign = 1
    for i in range(1, n):
        pts.append((xs[i], y + amp * sign))
        sign = -sign
        pts.append((xs[i], y + amp * sign))
    pts += [(xs[-1], y), (x1, y)]
    f.pline(pts, w=w, col=col)


def rect_pts(x, y, w, h):
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]


def mirror_x(pts, cx=0.0):
    return [(2 * cx - x, y) for x, y in pts]


def axes(f, x0, y0, w, h, xl="", yl="", size=None):
    """Draw L-shaped axes with arrows and axis labels; returns nothing."""
    f.arrow(x0, y0, x0 + w, y0, w=MED, size=3.5)
    f.arrow(x0, y0, x0, y0 + h, w=MED, size=3.5)
    f.text(x0 + w, y0 - 3.5, xl, size=size or f.fs, anchor="end", bold=True)
    f.text(x0 - 1.5, y0 + h, yl, size=size or f.fs, anchor="end", bold=True)


def tag(f, x, y, s, dx=1.6, dy=1.6, size=None, anchor="start", bold=False):
    f.circle(x, y, 0.45, w=0.3, fill=BLACK)
    f.text(x + dx, y + dy, s, size=size or f.fs, anchor=anchor, bold=bold)
