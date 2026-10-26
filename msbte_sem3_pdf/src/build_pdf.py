"""Build the solved-papers PDF from the paper modules, calc results and figures.

Usage:  python3 src/build_pdf.py [--subjects SOM,TE,PD] [--out out/file.pdf]
"""
import argparse
import collections
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common
from common import ROOT, OUT, DATA
common.register_fonts()

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, KeepTogether, KeepInFrame, NextPageTemplate,
                                Flowable, CondPageBreak)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.graphics.shapes import Drawing

import dsl
from dsl import mk
import calcfw

# ---------------------------------------------------------------- styles
INK = colors.Color(0.08, 0.08, 0.12)
NAVY = colors.Color(0.10, 0.22, 0.45)
GRID = colors.Color(0.62, 0.62, 0.66)
BAR = colors.Color(0.88, 0.90, 0.95)
SOFT = colors.Color(0.955, 0.955, 0.965)
WARN_BG = colors.Color(1.0, 0.97, 0.88)
WARN_LN = colors.Color(0.80, 0.45, 0.05)
ANS_BG = colors.Color(0.91, 0.96, 0.92)


def S(name, **kw):
    base = dict(fontName="DV", fontSize=9, leading=12.4, textColor=INK, spaceAfter=2.5)
    base.update(kw)
    return ParagraphStyle(name, **base)


ST = dict(
    body=S("body"),
    small=S("small", fontSize=7.6, leading=10),
    tiny=S("tiny", fontSize=6.8, leading=8.6),
    cell=S("cell", fontSize=8.2, leading=10.6, spaceAfter=0),
    cellb=S("cellb", fontName="DV-B", fontSize=8.2, leading=10.6, spaceAfter=0),
    bullet=S("bullet", leftIndent=12, bulletIndent=2, spaceAfter=1.6),
    formula=S("formula", alignment=TA_CENTER, spaceBefore=1.5, spaceAfter=3.5, fontSize=9),
    h=S("h", fontName="DV-B", spaceBefore=4, spaceAfter=2, keepWithNext=1),
    title=S("title", fontName="DV-B", fontSize=24, leading=30, alignment=TA_CENTER, textColor=NAVY, spaceAfter=8),
    subtitle=S("subtitle", fontSize=12, leading=17, alignment=TA_CENTER, spaceAfter=6),
    h1=S("h1", fontName="DV-B", fontSize=17, leading=22, textColor=NAVY, spaceBefore=0, spaceAfter=6, keepWithNext=1),
    h2=S("h2", fontName="DV-B", fontSize=13, leading=17, textColor=NAVY, spaceBefore=0, spaceAfter=5, keepWithNext=1),
    grp=S("grp", fontName="DV-B", fontSize=10, leading=13, textColor=colors.white, backColor=NAVY,
          borderPadding=(3, 4, 3, 4), spaceBefore=10, spaceAfter=7, keepWithNext=1),
    qtext=S("qtext", backColor=SOFT, borderPadding=(3, 4, 3, 4), spaceAfter=6, keepWithNext=1),
    qlab=S("qlab", fontName="DV-B", fontSize=9.5, textColor=NAVY, spaceAfter=0),
    ans=S("ans", fontName="DV-B", spaceBefore=1, spaceAfter=1.5, keepWithNext=1),
    cap=S("cap", fontSize=7.6, leading=9.5, alignment=TA_CENTER, textColor=colors.Color(.3, .3, .35), spaceAfter=5),
    toc0=S("toc0", fontName="DV-B", fontSize=10.5, leading=15, spaceBefore=6, leftIndent=0),
    toc1=S("toc1", fontSize=9, leading=12.5, leftIndent=14),
)
FW = A4[0] - 36 * mm       # frame width
FIG_MAX = FW


def P_(t, st="body", **kw):
    return Paragraph(mk(t), ST[st] if not kw else ParagraphStyle("x", parent=ST[st], **kw))


# ---------------------------------------------------------------- document
class Doc(BaseDocTemplate):
    def __init__(self, fn, title):
        super().__init__(fn, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                         topMargin=19 * mm, bottomMargin=16 * mm, title=title,
                         author="Prepared with Claude Code", subject="MSBTE Sem 3 Mechanical solved papers")
        main = Frame(self.leftMargin, self.bottomMargin, FW, A4[1] - 35 * mm, id="main", leftPadding=0,
                     rightPadding=0, topPadding=0, bottomPadding=0)
        rev = Frame(self.leftMargin - 4 * mm, self.bottomMargin - 3 * mm, FW + 8 * mm, A4[1] - 29 * mm, id="rev",
                    leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate("main", [main], onPageEnd=self.deco),
                               PageTemplate("rev", [rev], onPageEnd=self.deco)])
        self.hdr = ""
        self.toc_entries = []

    def deco(self, canv, doc):
        canv.saveState()
        canv.setFont("DV", 7.2)
        canv.setFillColor(colors.Color(.35, .35, .4))
        if self.page > 1 and self.hdr:
            canv.drawString(18 * mm, A4[1] - 12 * mm, self.hdr)
            canv.setStrokeColor(GRID)
            canv.setLineWidth(0.4)
            canv.line(18 * mm, A4[1] - 13.4 * mm, A4[0] - 18 * mm, A4[1] - 13.4 * mm)
        if self.page > 1:
            canv.drawCentredString(A4[0] / 2, 9 * mm, f"Page {self.page}")
        canv.restoreState()

    def afterFlowable(self, fl):
        bm = getattr(fl, "_bm", None)
        if bm:
            lvl, text, key, toc = bm
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level=lvl, closed=(lvl >= 2))
            if toc is not None:
                self.notify("TOCEntry", (toc, text, self.page, key))
        hd = getattr(fl, "_hdr", None)
        if hd:
            self.hdr = hd


_keys = collections.Counter()


def key_for(text):
    _keys[text] += 1
    return f"bm_{abs(hash(text)) % 10**8}_{_keys[text]}"


def heading(text, st, lvl, toc=None, hdr=None, key=None):
    p = Paragraph(mk(text), ST[st])
    p._bm = (lvl, text, key or key_for(text), toc)
    if hdr:
        p._hdr = hdr
    return p


def kt(items, bm=None, hdr=None):
    k = KeepTogether(items)
    if bm:
        k._bm = bm
        items[0]._bm = bm
    return k


# ---------------------------------------------------------------- block rendering
def tbl(rows, widths, head=True, zebra=False, fs_head=None, align_right_cols=(), bg_head=BAR, valign="TOP"):
    data = []
    for i, r in enumerate(rows):
        data.append([c if not isinstance(c, str) else Paragraph(mk(c), ST["cellb"] if (head and i == 0) else ST["cell"]) for c in r])
    t = Table(data, colWidths=widths, repeatRows=1 if head else 0)
    style = [("GRID", (0, 0), (-1, -1), 0.4, GRID), ("VALIGN", (0, 0), (-1, -1), valign),
             ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
             ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
    if head:
        style.append(("BACKGROUND", (0, 0), (-1, 0), bg_head))
    if zebra:
        for i in range(1 if head else 0, len(rows)):
            if i % 2 == 0:
                style.append(("BACKGROUND", (0, i), (-1, i), SOFT))
    t.setStyle(TableStyle(style))
    t.hAlign = "CENTER"
    return t


def note_box(text, title="Data note"):
    t = Table([[Paragraph(f"<b>{title}:</b> " + mk(text), ST["cell"])]], colWidths=[FW])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.9, WARN_LN), ("BACKGROUND", (0, 0), (-1, -1), WARN_BG),
                           ("LEFTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 3),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    return [t, Spacer(1, 4)]


def figure_flow(name, caption, kw):
    import figs
    d = figs.FIGS[name](**kw)
    assert isinstance(d, Drawing), name
    assert d.width <= FIG_MAX + 1, f"figure {name} too wide: {d.width / mm:.1f} mm"
    d.hAlign = "CENTER"
    items = [d]
    if caption:
        items.append(Paragraph(mk(caption), ST["cap"]))
    else:
        items.append(Spacer(1, 4))
    return [KeepTogether(items)]


def num_flow(cid):
    r = calcfw.load(cid)
    out = []
    out.append(P_(f"<b>Numerical:</b> {r['title']}", "body"))
    # given table
    rows = [["Given data", "Value", "Unit", "Remark"]]
    for gv in r["given"]:
        rows.append([gv["sym"], gv["val"], gv["unit"], gv["note"]])
    out.append(tbl(rows, [62 * mm, 40 * mm, 22 * mm, FW - 124 * mm]))
    out.append(Spacer(1, 4))
    out.append(P_("<b>Formula and calculation:</b>", "ans"))
    n = 0
    for s in r["steps"]:
        if not s["label"] and not s["subst"] and s["value"] is None:
            out.append(P_(s["formula"], "bullet", bulletFontName="DV"))
            continue
        n += 1
        line = f"<b>{n}.</b> {s['label']}" if s["label"] else ""
        out.append(P_(line, "body", leftIndent=0, spaceAfter=0.5, keepWithNext=1))
        line2 = s["formula"]
        if s["subst"]:
            line2 += "   " + s["subst"]
        if s["value"] is not None:
            line2 += ("   = " if (s["subst"] or s["formula"]) else "") + f"<b>{s['value']} {s['unit']}</b>".replace(" </b>", "</b>")
        elif s["unit"]:
            line2 += " " + s["unit"]
        if line2.strip():
            out.append(P_(line2, "formula", alignment=TA_LEFT, leftIndent=14, spaceBefore=0, spaceAfter=3))
    ans = [Paragraph("<b>Final answer</b>", ST["cell"])]
    for a in r["answers"]:
        unit = (" " + a["unit"]) if a["unit"] else ""
        ans.append(Paragraph(f"{mk(a['name'])} = <b>{mk(a['value'] + unit)}</b>", ST["cell"]))
    t = Table([[ans]], colWidths=[FW])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.9, colors.Color(.25, .55, .35)), ("BACKGROUND", (0, 0), (-1, -1), ANS_BG),
                           ("LEFTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    out.append(KeepTogether([Spacer(1, 2), t]))
    chk = []
    for k in r["checks"]:
        mark = "✓" if k["passed"] else "✗"
        chk.append(f"{mark} {k['method']}: {k['a']} ≈ {k['b']}")
    out.append(P_("<b>Checked in code by a second method:</b> " + "; ".join(chk), "tiny", textColor=colors.Color(.3, .3, .35), spaceBefore=2))
    for nt in r.get("notes", []):
        out.append(P_("Note: " + nt, "tiny", textColor=colors.Color(.3, .3, .35)))
    out.append(Spacer(1, 3))
    return out


def blocks_to_flow(q):
    out = []
    if q.flag:
        out += note_box(f"{q.flag[0]}<br/><b>Assumption used:</b> {q.flag[1]}")
    for b in q.ans:
        kind = b[0]
        if kind == "p":
            out.append(P_(b[1]))
        elif kind == "h":
            out.append(P_(b[1], "h"))
        elif kind == "b":
            for it in b[1]:
                out.append(Paragraph(mk(it), ST["bullet"], bulletText="•"))
        elif kind == "n":
            for i, it in enumerate(b[1], 1):
                out.append(Paragraph(mk(it), ST["bullet"], bulletText=f"{i}."))
        elif kind == "f":
            for ln in b[1]:
                out.append(Paragraph(mk(ln), ST["formula"]))
        elif kind == "t":
            _, head, rows, widths, cap = b
            n = len(head)
            w = [FW * x / sum(widths) for x in widths] if widths else [FW / n] * n
            out.append(tbl([head] + rows, w))
            out.append(Paragraph(mk(cap), ST["cap"]) if cap else Spacer(1, 4))
        elif kind == "fig":
            out += figure_flow(b[1], b[2], b[3])
        elif kind == "num":
            out += num_flow(b[1])
        elif kind == "note":
            out += note_box(b[1], "Note")
        elif kind == "ms":
            rows = [["Marks split", "Marks"]] + [[a, str(m)] for a, m in b[1]] + [["<b>Total</b>", f"<b>{sum(m for _, m in b[1])}</b>"]]
            t = tbl(rows, [FW * 0.62, 20 * mm])
            t.hAlign = "LEFT"
            out.append(KeepTogether([Spacer(1, 3), t]))
        else:
            raise ValueError(kind)
    return out


def question_flow(q, first_in_group=False):
    lab = f"Q.{q.group['no']}" + (f" ({q.sub})" if q.sub else "")
    bar = Table([[Paragraph(f"<b>{lab}</b>", ST["qlab"]), Paragraph(f"<b>[{q.marks} Marks]</b>", ParagraphStyle("r", parent=ST["qlab"], alignment=2))]],
                colWidths=[FW - 30 * mm, 30 * mm])
    bar.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), BAR), ("LEFTPADDING", (0, 0), (-1, -1), 4),
                             ("RIGHTPADDING", (0, 0), (-1, -1), 4), ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    title = f"{lab}"
    bmk = (3 if q.sub else 2, f"Q.{q.group['no']}" + (f"({q.sub})" if q.sub else ""), key_for(q.id), None)
    qt = Paragraph(mk(q.text), ST["qtext"])
    ans_lab = Paragraph("Ans.", ST["ans"])
    body = blocks_to_flow(q)
    head = [Spacer(1, 3), bar, Spacer(1, 2), qt, ans_lab]
    k = KeepTogether(head + body[:1])
    k._bm = bmk
    head[1]._bm = bmk
    return [k] + body[1:]


# ---------------------------------------------------------------- sections
def paper_flow(paper):
    out = [PageBreak()]
    hdr = f"{paper.subj_code} {paper.subj_name}  |  {paper.sess_label}"
    out.append(heading(f"{paper.sess_label}", "h2", 1, toc=1, hdr=hdr))
    info = [["Subject", f"{paper.subj_name} ({paper.subj_code})", "Time / Marks", f"{paper.hours} / {paper.total} Marks"],
            ["Session", paper.sess_label, "Paper ID printed", paper.printed_id],
            ["Scheme", paper.scheme, "Source file", paper.src_file]]
    out.append(tbl(info, [22 * mm, 62 * mm, 28 * mm, FW - 112 * mm], head=False))
    for n in paper.notes:
        out += note_box(n, "Paper note")
    out.append(Spacer(1, 2))
    for g in paper.groups:
        gk = f"Q.{g['no']}   {g['text']}   —   {g['marks']} Marks"
        if g["attempt"] and g["attempt"] > 1 and len(g["qs"]) > g["attempt"]:
            gk += f"   (each sub-question = {g['marks'] // g['attempt']} marks)"
        h = Paragraph(mk(gk), ST["grp"])
        h._bm = (2, f"Q.{g['no']}", key_for(f"{paper.pid}-g{g['no']}"), None)
        out.append(h)
        for q in g["qs"]:
            out += question_flow(q)
    return out


def missing_flow(subj_code, subj_name, sess_label, why="Paper not received – not included."):
    return [PageBreak(), heading(sess_label + " – not included", "h2", 1, toc=1, hdr=f"{subj_code} {subj_name}  |  {sess_label}"),
            P_(f"<b>{why}</b>"),
            P_("Questions and solutions for this paper will be added when the paper is supplied. Nothing has been guessed.")]


def chapter_table(papers):
    chapters = collections.OrderedDict()
    for p in papers:
        for q in p.questions:
            chapters.setdefault(q.chapter, collections.OrderedDict())
            chapters[q.chapter][p.pid] = chapters[q.chapter].get(p.pid, 0) + q.marks
    tot_by_paper = {p.pid: sum(q.marks for q in p.questions) for p in papers}
    grand = sum(tot_by_paper.values())
    head = ["Chapter"] + [p.sess_code for p in papers] + ["Total", "Share"]
    rows = []
    for ch, d in chapters.items():
        t = sum(d.values())
        rows.append([ch] + [str(d.get(p.pid, "–")) for p in papers] + [f"<b>{t}</b>", f"{100 * t / grand:.1f} %"])
    rows.append(["<b>Total (marks offered)</b>"] + [f"<b>{tot_by_paper[p.pid]}</b>" for p in papers] + [f"<b>{grand}</b>", "100 %"])
    assert sum(sum(d.values()) for d in chapters.values()) == grand      # check A7
    n = len(papers)
    w = [FW - (n * 17 + 34) * mm] + [17 * mm] * n + [17 * mm, 17 * mm]
    return tbl(rows, w, zebra=True), tot_by_paper


def top10(papers):
    groups = collections.OrderedDict()
    for p in papers:
        for q in p.questions:
            assert q.marks_split_total() == q.marks, q.id            # check A4
            g = groups.setdefault(q.concept, dict(concept=q.concept, title=q.text.split("\n")[0], papers=collections.OrderedDict(), marks=0, first=len(groups)))
            g["papers"].setdefault(p.pid, []).append(q)
            g["marks"] += q.marks
    items = sorted(groups.values(), key=lambda g: (-len(g["papers"]), -g["marks"], g["first"]))
    return items[:10], sum(1 for g in groups.values() if len(g["papers"]) > 1), len(papers)


def backmatter_flow(subj_code, subj_name, papers, rev):
    out = []
    hdr = f"{subj_code} {subj_name}  |  Summary pages"
    out += [PageBreak(), heading("Chapter-wise marks table", "h2", 1, toc=1, hdr=hdr)]
    if not papers:
        out.append(P_("No paper was received for this subject, so no table can be made from the papers."))
        return out
    t, totals = chapter_table(papers)
    out.append(P_("<b>Marks offered</b> = marks of every sub-question printed in the paper, including the choice "
                  "('attempt any …'), so a column total can be more than 70. Chapter names are my own classification of each "
                  "question (the syllabus was not supplied).", "small"))
    out.append(t)
    out.append(Spacer(1, 6))
    out.append(P_("Papers counted: " + ", ".join(f"{p.sess_label}" for p in papers) + ".", "small"))
    out += [Spacer(1, 10), heading("Top 10 repeated questions", "h2", 1, toc=1, hdr=hdr)]
    items, nrep, npap = top10(papers)
    if npap < 2:
        out.append(note_box("Only one paper was supplied for this subject, so no question can be called 'repeated'. "
                            "The table below lists the 10 topics with the highest marks in that paper instead.", "Note")[0])
    else:
        out.append(P_(f"<b>Ranking rule:</b> topics are ranked by the number of supplied sessions in which they appear ({npap} sessions supplied), "
                      f"then by total marks. {nrep} topic(s) appeared in more than one session. Topics that appeared only once are "
                      "shown after them and are marked 'not repeated'.", "small"))
    rows = [["#", "Question / topic", "Where asked", "Marks", "Sessions"]]
    for i, g in enumerate(items, 1):
        where = "; ".join(f"{pid.split('-')[1]}: " + ", ".join(f"Q.{q.label}" for q in qs) for pid, qs in g["papers"].items())
        ns = len(g["papers"])
        import papers as _pp
        rows.append([str(i), mk(_pp.CONCEPT_TITLES.get(g["concept"], g["title"])), where, str(g["marks"]), f"{ns}" + (" (repeated)" if ns > 1 else (" (not repeated)" if npap > 1 else ""))])
    out.append(tbl(rows, [8 * mm, FW - 8 * mm - 44 * mm - 14 * mm - 24 * mm, 44 * mm, 14 * mm, 24 * mm], zebra=True))
    # revision sheet
    out += [NextPageTemplate("rev"), PageBreak()]
    out.append(heading("Last-minute revision sheet", "h2", 1, toc=1, hdr=hdr))
    out.append(rev_flow(rev))
    out.append(NextPageTemplate("main"))
    return out


def rev_flow(rev):
    """rev = list of (heading, [lines]) ; two columns, shrunk to exactly one page."""
    cols = [[], []]
    half = sum(1 + len(ls) for _, ls in rev) / 2
    acc, ci = 0, 0
    st_h = ParagraphStyle("rh", parent=ST["body"], fontName="DV-B", fontSize=8.2, leading=10.2, textColor=NAVY, spaceBefore=3, spaceAfter=1, backColor=BAR, borderPadding=(1, 2, 1, 2))
    st_l = ParagraphStyle("rl", parent=ST["body"], fontSize=7.6, leading=9.6, spaceAfter=1, leftIndent=7, bulletIndent=0)
    for h, ls in rev:
        if ci == 0 and acc >= half:
            ci = 1
        cols[ci].append(Paragraph(mk(h), st_h))
        for l in ls:
            cols[ci].append(Paragraph(mk(l), st_l, bulletText="•"))
        acc += 1 + len(ls)
    t = Table([[cols[0], cols[1]]], colWidths=[(FW + 8 * mm) / 2] * 2)
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                           ("LINEAFTER", (0, 0), (0, 0), 0.4, GRID)]))
    return KeepInFrame(FW + 8 * mm, A4[1] - 40 * mm, [t], mode="shrink")


# ---------------------------------------------------------------- front matter
def cover(papers_by_subj, requested, extra_note):
    out = [Spacer(1, 38 * mm), Paragraph("MSBTE Diploma in Mechanical Engineering", ST["subtitle"]),
           Paragraph("Semester 3 · K-Scheme", ST["subtitle"]), Spacer(1, 8 * mm),
           Paragraph("Solved Question Papers", ST["title"]),
           Paragraph("Question papers with step-by-step model-style answers", ST["subtitle"]), Spacer(1, 12 * mm)]
    rows = [["Subject", "Code", "Papers included in this book"]]
    for sc, (name, code) in requested.items():
        ps = papers_by_subj.get(sc, [])
        rows.append([name, code, ", ".join(p.sess_label for p in ps) if ps else "none received yet"])
    out.append(tbl(rows, [62 * mm, 20 * mm, FW - 82 * mm]))
    out.append(Spacer(1, 10 * mm))
    out += note_box(extra_note, "Read this first")
    out.append(Spacer(1, 4 * mm))
    out.append(P_("<b>How the answers were made.</b> The questions are copied from the papers you supplied. The solutions are written "
                  "by Claude in MSBTE model-answer style; they are <b>not</b> the official MSBTE model answers, so the marks split can "
                  "differ from the official scheme. Every numerical was calculated in a Python script and re-checked by a second method. "
                  "Where data looked wrong, a <b>Data note</b> box states the assumption.", "small"))
    return out


def reading_report(requested, reading, papers_all):
    out = [PageBreak(), heading("Reading report: which papers were received", "h1", 0, toc=0, hdr="Reading report")]
    out.append(P_("You asked for 4 subjects × 3 sessions = 12 papers. This table shows what was actually received and readable. "
                  "Nothing was guessed for papers that are missing.", "small"))
    rows = [["Subject", "Winter 2024", "Summer 2025", "Winter 2025"]]
    for sc, (name, code) in requested.items():
        r = [f"{name} ({code})"]
        for sess in ("W24", "S25", "W25"):
            pid = reading["requested"][sc][sess]
            r.append("Received and read ✓" if pid else "<font color='#B00020'><b>NOT RECEIVED</b></font>")
        rows.append(r)
    out.append(tbl(rows, [58 * mm, 38 * mm, 38 * mm, FW - 134 * mm]))
    out.append(Spacer(1, 6))
    n_ok = sum(1 for d in reading["requested"].values() for v in d.values() if v)
    out.append(P_(f"<b>Requested papers received: {n_ok} of 12.</b> Missing: " + ", ".join(
        f"{sc}-{sess}" for sc, d in reading["requested"].items() for sess, v in d.items() if not v) + ".", "body"))
    out.append(Spacer(1, 6))
    out.append(P_("<b>Page-by-page reading status of the files received</b>", "h"))
    rows = [["Paper", "File", "Pages", "How read", "Unreadable"]]
    for pid, d in reading["received"].items():
        rows.append([pid, d["file"], str(d["pages"]), d["how"], ", ".join(d["unreadable"]) or "none"])
    out.append(tbl(rows, [18 * mm, 58 * mm, 11 * mm, FW - 18 * mm - 58 * mm - 11 * mm - 20 * mm, 20 * mm]))
    out.append(Spacer(1, 6))
    for pid, d in reading["received"].items():
        if d.get("warning"):
            out += note_box(f"<b>{pid}</b>: {d['warning']}", "Warning")
    return out


def data_notes_page(papers):
    out = [PageBreak(), heading("Data notes: questions with doubtful data", "h1", 0, toc=0, hdr="Data notes")]
    out.append(P_("These questions have data that looks misprinted, missing or inconsistent. The assumption used in the solution is "
                  "given. Each is repeated in a box at the question itself.", "small"))
    rows = [["Question", "Doubt", "Assumption used"]]
    for p in papers:
        for q in p.questions:
            if q.flag:
                rows.append([f"{p.pid} Q.{q.label}", q.flag[0], q.flag[1]])
    out.append(tbl(rows, [26 * mm, (FW - 26 * mm) * 0.55, (FW - 26 * mm) * 0.45], zebra=True))
    return out


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subjects", default="SOM,FMM,TE,PD")
    ap.add_argument("--out", default=str(OUT / "MSBTE_Sem3_Mechanical_Solved_Papers.pdf"))
    a = ap.parse_args()

    import papers   # registers all papers
    from papers import REQUESTED, EXTRA_NOTE, REVISION
    reading = json.loads((DATA / "reading_log.json").read_text())
    want = a.subjects.split(",")
    by_subj = collections.OrderedDict((sc, [p for p in dsl.PAPERS.values() if p.subj_short == sc]) for sc in REQUESTED)
    order = {"W24": 0, "S25": 1, "W25": 2, "S23": -1}
    for sc in by_subj:
        by_subj[sc].sort(key=lambda p: order[p.sess_code])
    all_papers = [p for sc in want for p in by_subj[sc]]

    story = []
    story += cover(by_subj, {k: v for k, v in REQUESTED.items() if k in want}, EXTRA_NOTE)
    story += reading_report({k: v for k, v in REQUESTED.items() if k in want}, reading, all_papers)
    story += data_notes_page(all_papers)
    story += [PageBreak(), heading("Table of contents", "h1", 0, hdr="Contents")]
    toc = TableOfContents()
    toc.levelStyles = [ST["toc0"], ST["toc1"]]
    toc.dotsMinLevel = 0
    story.append(toc)

    for sc in want:
        name, code = REQUESTED[sc]
        ps = by_subj[sc]
        story += [PageBreak(), heading(f"{name} ({code})", "h1", 0, toc=0, hdr=f"{code} {name}")]
        std = [p for p in ps if p.in_scope]
        rows = [["Session", "Status"]]
        for sess, lab in (("W24", "Winter 2024"), ("S25", "Summer 2025"), ("W25", "Winter 2025")):
            ok = any(p.sess_code == sess for p in ps)
            rows.append([lab, "Included" if ok else "<b>Not received – not included</b>"])
        for p in ps:
            if not p.in_scope:
                rows.append([p.sess_label, "Extra paper supplied – included, clearly labelled (" + p.scheme + ")"])
        story.append(tbl(rows, [40 * mm, FW - 40 * mm]))
        story.append(Spacer(1, 4))
        story.append(P_("Marks shown against sub-questions are the paper's group marks divided by the number of sub-questions to "
                        "attempt (MSBTE equal split); the papers print only the group total.", "small"))
        miss = []
        for sess, lab in (("W24", "Winter 2024"), ("S25", "Summer 2025"), ("W25", "Winter 2025")):
            ps_s = [p for p in ps if p.sess_code == sess]
            if ps_s:
                story += paper_flow(ps_s[0])
            else:
                miss.append(lab)
        if miss:
            story += missing_flow(code, name, "Papers not received: " + ", ".join(miss), "Not received, so not included: " + ", ".join(miss) + ".")
        for p in ps:
            if not p.in_scope:
                story += paper_flow(p)
        story += backmatter_flow(code, name, ps, REVISION.get(sc))

    doc = Doc(a.out, "MSBTE Sem 3 Mechanical – Solved Question Papers")
    doc.multiBuild(story)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
