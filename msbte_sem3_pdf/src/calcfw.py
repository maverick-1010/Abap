"""Framework for numericals: every number in the PDF comes from one of these scripts.

A calc function receives a Calc object `c` and records, in order:
    c.given(...)  c.step(...)  c.answer(...)  c.check(...)
Results are written to data/calc_results/<id>.json and the PDF is built from that file.
A failed check raises, which stops the build.
"""
import json
import math
import re
from common import DATA

REG = {}                       # id -> (title, function)


def g(x, sig=6):
    """Compact number text for use inside substitution strings."""
    if isinstance(x, str):
        return x
    if x == 0:
        return "0"
    a = abs(x)
    if a >= 1e7 or a < 1e-3:
        m, e = f"{x:.{sig - 1}e}".split("e")
        m = m.rstrip("0").rstrip(".")
        return f"{m} × 10^{{{int(e)}}}"
    s = f"{x:.{sig}g}"
    if "e" in s:
        s = f"{x:.{sig}f}".rstrip("0").rstrip(".")
    return s


def fmt(v, nd=2):
    if isinstance(v, str):
        return v
    a = abs(v)
    if a != 0 and (a >= 1e7 or a < 1e-3):
        return g(v, 4)
    return f"{v:,.{nd}f}".replace(",", "") if a < 1e5 else f"{v:,.{nd}f}".replace(",", " ")


def sci_fix(t):
    """Turn 8.32e+09 into 8.32 × 10^{9} inside any text."""
    return re.sub(r"(\d+(?:\.\d+)?)e([+-]?\d+)", lambda m: f"{m.group(1)} × 10^{{{int(m.group(2))}}}", t)


class Calc:
    def __init__(self, cid, title):
        self.id, self.title = cid, title
        self.givens, self.steps, self.answers, self.checks, self.notes = [], [], [], [], []

    def given(self, sym, val, unit="", note=""):
        self.givens.append(dict(sym=sym, val=g(val) if not isinstance(val, str) else val,
                                unit=unit, note=note))

    def step(self, label, formula, subst="", value=None, unit="", nd=2):
        self.steps.append(dict(label=label, formula=sci_fix(formula), subst=sci_fix(subst),
                               value=None if value is None else fmt(value, nd),
                               raw=value, unit=unit))
        return value

    def say(self, text):
        self.steps.append(dict(label="", formula=text, subst="", value=None, raw=None, unit=""))

    def answer(self, name, value, unit, nd=2):
        self.answers.append(dict(name=name, value=fmt(value, nd), raw=value, unit=unit))
        return value

    def check(self, method, a, b, rtol=1e-6, atol=0.0):
        ok = math.isclose(a, b, rel_tol=rtol, abs_tol=atol)
        self.checks.append(dict(method=method, a=fmt(a, 4), b=fmt(b, 4),
                                a_raw=a, b_raw=b, rtol=rtol, passed=ok))
        if not ok:
            raise AssertionError(f"[{self.id}] check failed: {method}: {a} vs {b}")

    def check_le(self, method, a, limit, tol=1e-9):
        """Pass if a <= limit (within tolerance)."""
        ok = a <= limit * (1 + tol)
        self.checks.append(dict(method=method, a=fmt(a, 4), b="≤ " + fmt(limit, 4),
                                a_raw=a, b_raw=limit, rtol=tol, passed=ok))
        if not ok:
            raise AssertionError(f"[{self.id}] check failed: {method}: {a} > {limit}")

    def note(self, text):
        self.notes.append(text)

    def to_dict(self):
        return dict(id=self.id, title=self.title, given=self.givens, steps=self.steps,
                    answers=self.answers, checks=self.checks, notes=self.notes)


def calc(cid, title):
    def deco(fn):
        REG[cid] = (title, fn)
        return fn
    return deco


def run_all():
    """Run every registered calc, write JSON, return dict of results."""
    out = {}
    for cid, (title, fn) in sorted(REG.items()):
        c = Calc(cid, title)
        fn(c)
        assert c.answers, f"{cid}: no answer recorded"
        assert c.checks, f"{cid}: no second-method check"
        d = c.to_dict()
        (DATA / "calc_results" / f"{cid}.json").write_text(json.dumps(d, indent=1, ensure_ascii=False))
        out[cid] = d
    return out


def load(cid):
    return json.loads((DATA / "calc_results" / f"{cid}.json").read_text())
