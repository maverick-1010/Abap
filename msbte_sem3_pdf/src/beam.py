"""Tiny statics solver for beams with two supports, point loads and UDLs.

Used (a) as an independent second check of hand-written SF/BM calculations and
(b) to draw the SFD and BMD figures, so the picture and the numbers cannot differ.
Downward loads are positive. SF = sum of vertical forces to the left of the section
(upward positive). BM sagging positive.
"""
import math


class Beam:
    def __init__(self, length, sup_a, sup_b, points=(), udls=()):
        self.L, self.a, self.b = length, sup_a, sup_b
        self.points = list(points)          # (x, W)
        self.udls = list(udls)              # (x1, x2, w)
        tot = sum(W for _, W in self.points) + sum(w * (x2 - x1) for x1, x2, w in self.udls)
        mom_a = sum(W * (x - self.a) for x, W in self.points) + \
            sum(w * (x2 - x1) * ((x1 + x2) / 2 - self.a) for x1, x2, w in self.udls)
        self.Rb = mom_a / (self.b - self.a)
        self.Ra = tot - self.Rb
        self.total_load = tot

    def sf(self, x, side="right"):
        """Shear force just right (default) or left of x."""
        eps = 1e-9 if side == "right" else -1e-9
        xx = x + eps
        v = 0.0
        if xx > self.a:
            v += self.Ra
        if xx > self.b:
            v += self.Rb
        for xp, W in self.points:
            if xx > xp:
                v -= W
        for x1, x2, w in self.udls:
            v -= w * max(0.0, min(xx, x2) - x1)
        return v

    def bm(self, x):
        m = 0.0
        if x > self.a:
            m += self.Ra * (x - self.a)
        if x > self.b:
            m += self.Rb * (x - self.b)
        for xp, W in self.points:
            if x > xp:
                m -= W * (x - xp)
        for x1, x2, w in self.udls:
            if x > x1:
                xe = min(x, x2)
                m -= w * (xe - x1) * (x - (x1 + xe) / 2)
        return m

    def key_xs(self):
        xs = {0.0, self.L, self.a, self.b}
        xs.update(xp for xp, _ in self.points)
        for x1, x2, _ in self.udls:
            xs.update((x1, x2))
        return sorted(xs)

    def sf_zero_points(self):
        """x where SF passes through zero inside a segment (BM extreme)."""
        xs, out = self.key_xs(), []
        for x0, x1 in zip(xs, xs[1:]):
            v0, v1 = self.sf(x0, "right"), self.sf(x1, "left")
            if v0 * v1 < 0:
                lo, hi = x0, x1
                for _ in range(80):
                    mid = (lo + hi) / 2
                    if self.sf(mid) * v0 > 0:
                        lo = mid
                    else:
                        hi = mid
                out.append((lo + hi) / 2)
        return out

    def contraflexure(self):
        xs, out = self.key_xs(), []
        for x0, x1 in zip(xs, xs[1:]):
            n = 400
            prev = self.bm(x0)
            for i in range(1, n + 1):
                xx = x0 + (x1 - x0) * i / n
                cur = self.bm(xx)
                if prev * cur < 0:
                    lo, hi = xx - (x1 - x0) / n, xx
                    for _ in range(80):
                        mid = (lo + hi) / 2
                        if self.bm(mid) * prev > 0:
                            lo = mid
                        else:
                            hi = mid
                    out.append((lo + hi) / 2)
                prev = cur if cur != 0 else prev
        return out
