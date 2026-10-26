"""Write data/qbank/<paper>.json from the paper modules (question text, marks, chapter, flags)."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import common
from common import DATA
import dsl
import papers  # noqa: F401

for p in dsl.PAPERS.values():
    rec = dict(paper=p.pid, subject=p.subj_code, session=p.sess_code, scheme=p.scheme, total_marks=p.total, printed_id=p.printed_id,
               source_file=p.src_file, groups=[dict(no=g["no"], text=g["text"], marks=g["marks"], attempt=g["attempt"]) for g in p.groups],
               questions=[dict(id=q.id, label=q.label, text=q.text, marks=q.marks, marks_basis="group marks / number to attempt (not printed per sub-question)",
                               type=q.qtype, chapter=q.chapter, chapter_source="inferred", concept=q.concept, read_status="ok",
                               misprint=dict(flag=bool(q.flag), doubt=q.flag[0] if q.flag else "", assumption=q.flag[1] if q.flag else "")) for q in p.questions])
    (DATA / "qbank" / f"{p.pid}.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False))
    print(p.pid, len(p.questions), "questions")
