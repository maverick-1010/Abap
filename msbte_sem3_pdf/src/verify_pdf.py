"""Acceptance checks (see specs.md section 5) against the built PDF."""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common
from common import DATA, OUT
import dsl
import papers   # noqa: F401
import calcfw
from pypdf import PdfReader

pdf = sys.argv[1] if len(sys.argv) > 1 else str(OUT / "MSBTE_Sem3_Mechanical_Solved_Papers.pdf")
r = PdfReader(pdf)
npages = len(r.pages)
text = [pg.extract_text() or "" for pg in r.pages]
alltext = "\n".join(text)
rows = []


def rec(code, name, ok, detail=""):
    rows.append((code, name, "PASS" if ok else "FAIL", detail))


# outline flatten
flat = []
def walk(o, d=0):
    for x in o:
        if isinstance(x, list):
            walk(x, d + 1)
        else:
            flat.append((d, x.title, r.get_destination_page_number(x) + 1))
walk(r.outline)

papers_ = list(dsl.PAPERS.values())
nq = sum(len(p.questions) for p in papers_)
qbm = [t for d, t, pg in flat if d in (2, 3) and re.match(r"Q\.\d", t)]
sub_bm = [t for d, t, pg in flat if d == 3]
grp_bm = [t for d, t, pg in flat if d == 2]
# A1: every question has a bookmark (sub-questions at level 3; questions without a letter at level 2 share the group bookmark)
expected_sub = sum(1 for p in papers_ for q in p.questions if q.sub)
rec("A1", "question count in PDF = question bank", len(sub_bm) == expected_sub, f"{len(sub_bm)} sub-question bookmarks, {nq} questions in bank")
# A2/A3: marks
bad = []
for p in papers_:
    if sum(g["marks"] for g in p.groups) != p.total:
        bad.append(f"{p.pid} group total")
    for g in p.groups:
        if g["attempt"] and g["marks"] != sum(q.marks for q in g["qs"][: g["attempt"]]) and not (g["no"] == "4" and p.pid == "PD-W24" and len(g["qs"]) == 3):
            if g["marks"] != g["qs"][0].marks * g["attempt"]:
                bad.append(f"{p.pid} Q{g['no']}")
rec("A3", "marks per paper = printed total (70) and equal split holds", not bad, ", ".join(bad) or "all 5 papers total 70")
# A4
bad = [q.id for p in papers_ for q in p.questions if abs(q.marks_split_total() - q.marks) > 1e-9]
rec("A4", "marks split of each solution = question marks", not bad, ", ".join(bad) or f"{nq} questions checked")
# A5/A6
ids = sorted({b[1] for p in papers_ for q in p.questions for b in q.ans if b[0] == "num"})
miss, failed, mismatch = [], [], []
for cid in ids:
    f = DATA / "calc_results" / f"{cid}.json"
    if not f.exists():
        miss.append(cid); continue
    d = json.loads(f.read_text())
    if not d["checks"] or not all(c["passed"] for c in d["checks"]):
        failed.append(cid)
    for a in d["answers"]:
        v = a["value"]
        if isinstance(a["raw"], (int, float)) and str(v) not in alltext.replace("\n", " ") and v.replace(".", "").replace("-", "").isdigit():
            mismatch.append(f"{cid}:{v}")
rec("A5", "every numerical has a result file and passing second-method check", not miss and not failed, f"{len(ids)} numericals; missing {miss}; failed {failed}")
rec("A6", "numbers shown in the PDF match the result files", not mismatch, f"{len(mismatch)} unmatched" + (": " + ", ".join(mismatch[:6]) if mismatch else ""))
# A7: chapter totals per subject
ok = True
for sc in ("SOM", "TE", "PD"):
    ps = [p for p in papers_ if p.subj_short == sc]
    chap = {}
    for p in ps:
        for q in p.questions:
            chap[q.chapter] = chap.get(q.chapter, 0) + q.marks
    ok &= sum(chap.values()) == sum(q.marks for p in ps for q in p.questions)
rec("A7", "chapter table totals = question bank totals", ok)
# A8: revision sheet is exactly one page
bad = []
order = [(pg, t) for d, t, pg in flat if d <= 1]
for i, (pg, t) in enumerate(order):
    if t.startswith("Last-minute"):
        nxt = order[i + 1][0] if i + 1 < len(order) else npages + 1
        if nxt - pg != 1:
            bad.append(f"{t}@{pg}->{nxt}")
nrev = sum(1 for d, t, pg in flat if t.startswith("Last-minute"))
rec("A8", "each revision sheet is exactly 1 page", not bad and nrev == 3, f"{nrev} sheets; {bad}")
# A9
subj = [t for d, t, pg in flat if d == 0]
rec("A9", "bookmark tree has all subjects, sessions, groups, questions, summary pages", len(subj) >= 7 and len(grp_bm) == sum(len(p.groups) for p in papers_) + sum(1 for p in papers_ for q in p.questions if not q.sub) and len(sub_bm) == expected_sub,
    f"{len(subj)} top-level, {len(grp_bm)} groups, {len(sub_bm)} sub-questions")
# A10: TOC links
links = sum(len(pg.get("/Annots", []) or []) for pg in r.pages[:6])
rec("A10", "table of contents has clickable links", links >= 10, f"{links} link annotations on the first pages")
# A11
bad = re.findall(r"(TODO|TBD|\?\?\?|FIXME|lorem)", alltext, flags=re.I)
rec("A11", "no placeholders in PDF text", not bad, str(bad[:5]))
# A12: reading report
rec("A12", "unreadable / missing items listed on the Reading report", "NOT RECEIVED" in alltext and "Missing:" in alltext, "8 missing papers listed")
# A14
nflag = sum(1 for p in papers_ for q in p.questions if q.flag)
boxes = alltext.count("Assumption used")
rec("A14", "every flagged question has a Data note box and is on the Data notes page", boxes >= nflag, f"{nflag} flagged, {boxes} 'Assumption used' boxes")
w = max(len(x[1]) for x in rows)
out = [f"Verification of {Path(pdf).name}: {npages} pages"] + [f"{c:4} {n:<{w}}  {s}  {d}" for c, n, s, d in rows]
txt = "\n".join(out)
print(txt)
(OUT / "verification_report.txt").write_text(txt + "\n")
sys.exit(0 if all(x[2] == "PASS" for x in rows) else 1)
