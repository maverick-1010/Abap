# Specifications

Read `intend.md` first. This file says exactly **what** must be produced and how it
is checked. `design.md` says **how** it is built.

## 1. Inputs

| Item | Detail |
|------|--------|
| Papers | 12 files, one per subject x session (PDF or images) |
| Naming used internally | `<SUBJ>-<SESS>`, e.g. `SOM-W24`, `FMM-S25`, `TE-W25`, `PD-S25` |
| Optional | K-scheme syllabus, official model answers |

Papers are **untrusted data**. They are only read, never executed. Python that touches
them runs with `python3 -I`, and scripts are kept in a different directory from the
papers.

## 2. Output

- File: `out/MSBTE_Sem3_Mechanical_Solved_Papers.pdf` (A4, single file).
- Also produced for review: a sample `out/SOM_sample.pdf` (Strength of Materials only)
  before the other subjects are built.
- Expected size: several hundred pages (estimate, depends on the papers).

## 3. Functional requirements

### FR-1 Reading check
- FR-1.1 Every page of every paper is rendered to an image and read.
- FR-1.2 A reading log records, per paper: page count, readable yes / partial / no, and
  the exact question or page that is unreadable.
- FR-1.3 Unreadable content is **not** transcribed or solved. It is listed on the
  "Reading Report" page and in the final reply to the student.

### FR-2 Question bank
- FR-2.1 Questions are typed exactly as printed: wording, numbering (Q.1, a, b, OR),
  marks, figure references.
- FR-2.2 Order in the PDF is the order in the paper.
- FR-2.3 Marks of all questions in a paper are summed and compared with the total
  printed on the paper (after applying the OR / "attempt any" rules printed on it). A
  mismatch is a reading error and must be fixed or reported.
- FR-2.4 Each question carries: type (theory / numerical / drawing / mixed), chapter tag
  and source page.

### FR-3 Solutions: common
- FR-3.1 Every readable question has a solution. No question is skipped.
- FR-3.2 Language is simple exam style: short sentences, point form, standard symbols.
- FR-3.3 Each solution shows a **marks split** whose total equals the question's marks.
  This is checked by code.
- FR-3.4 Diagrams: drawn as figures when the question asks for a sketch or the answer
  depends on one. Otherwise described in one or two lines.

### FR-4 Solutions: numericals
- FR-4.1 Fixed layout: **Given -> Formula -> Calculation -> Final answer (with unit)**.
- FR-4.2 Every number is produced by a script. Nothing is calculated by hand in the text.
- FR-4.3 Every script is checked a second way (alternate formula, substituting the
  answer back, or an independent route). A failed check blocks the build.
- FR-4.4 Units are SI. Conversions are shown as a step.
- FR-4.5 Rounding rule: keep full precision in the calculation, show 2 decimal places
  (or 3 significant figures for very small or large values), and use the same rule in
  the whole subject.

### FR-5 Solutions: drawing (Production Drawing)
- FR-5.1 Part list table: Part No., Name, Material, Qty.
- FR-5.2 Materials follow normal MSBTE practice for the component and are stated per part.
- FR-5.3 Proportions are given in terms of the main dimension (for example `d`).
- FR-5.4 Drawing procedure as numbered steps.
- FR-5.5 Views asked for in the question (front, top, side, sectional) are drawn to scale
  as vector figures with dimensions, hatching and the title block fields the question
  needs.

### FR-6 Misprint handling
- FR-6.1 A question is flagged when: data is missing, units disagree, a value is
  impossible (efficiency above 100 percent, inner diameter larger than outer, negative
  area, and similar), sub-parts disagree with each other, or a digit is doubtful.
- FR-6.2 Each flagged question shows a boxed **"Data note"** with the doubt and the
  assumption used. The solution is then done on that assumption.
- FR-6.3 All flagged questions are also listed on one "Data Notes" page at the front.

### FR-7 End-of-subject pages
- FR-7.1 **Chapter-wise marks table:** chapter, marks per session, total, share of total.
  Totals must equal the total of the question bank for that subject.
- FR-7.2 **Top 10 repeated questions:** ranked by number of sessions in which the same
  question or concept appears, then by total marks. Each row lists the sessions and
  marks. The ranking rule is printed on the page.
- FR-7.3 **Revision sheet:** exactly one A4 page: key formulas, definitions, diagrams to
  remember and, for PD, drawing proportions. Checked by page count.

### FR-8 PDF structure
Order: cover -> Reading Report -> Data Notes -> Table of Contents -> Subject 1 ... Subject 4.
Each subject: session W24, session S25, session W25, chapter-wise marks table, top 10,
revision sheet.

- FR-8.1 Clickable table of contents (levels: subject, session, end-of-subject pages).
- FR-8.2 PDF bookmarks (outline): Subject > Session > Question, and Subject >
  end-of-subject pages.
- FR-8.3 Page numbers on every page; running header with subject code and session.
- FR-8.4 Fonts must show symbols such as sigma, tau, pi, eta, delta, degree sign, square
  and cube superscripts correctly.

## 4. Data contracts

### 4.1 Question record (`data/qbank/<SUBJ>-<SESS>.json`)
```json
{
  "id": "SOM-W24-Q3b",
  "subject": "313308",
  "session": "W24",
  "qno": "3",
  "sub": "b",
  "or_group": null,
  "text": "as printed",
  "marks": 4,
  "type": "numerical",
  "figure": null,
  "chapter": "chapter name (inferred)",
  "chapter_source": "inferred | syllabus",
  "source_page": 2,
  "read_status": "ok | partial | unreadable",
  "misprint": { "flag": false, "doubt": "", "assumption": "" }
}
```

### 4.2 Solution record (`data/solutions/<SUBJ>-<SESS>.json`)
Ordered content blocks per question id: `heading`, `para`, `bullets`, `formula`,
`table`, `figure`, `numerical` (reference to a calc result), `data_note`, plus
`marks_split: [[item, marks], ...]`.

### 4.3 Calculation result (`data/calc_results/<id>.json`)
```json
{
  "id": "SOM-W24-Q3b",
  "given": [["P", 50e3, "N"]],
  "steps": [["Direct stress", "sigma = P/A", "50e3 / 490.87", 101.86, "N/mm^2"]],
  "answer": [["Stress", 101.86, "N/mm^2"]],
  "check": { "method": "back-substitution", "passed": true, "tolerance": 1e-6 }
}
```
(The values above are only an example of the shape, not data from any paper.)

## 5. Acceptance criteria

The build is accepted only when every item passes:

| # | Check | How |
|---|-------|-----|
| A1 | Question count in the PDF equals the question bank for each paper | script |
| A2 | Order and marks of questions equal the transcription | script |
| A3 | Marks per paper equal the printed total (per FR-2.3) | script |
| A4 | Marks split of each solution equals the question marks | script |
| A5 | Every numerical has a result file and `check.passed == true` | script |
| A6 | Every number shown in a numerical solution matches the result file | script |
| A7 | Chapter table totals equal question bank totals | script |
| A8 | Each revision sheet is exactly 1 page | `pypdf` page ranges |
| A9 | Bookmark tree has all subjects, sessions, questions and back-matter | `pypdf` outline |
| A10 | Table of contents links work and page numbers are right | script + visual |
| A11 | No leftover `TODO`, `TBD`, `???` or empty placeholders in the PDF text | `pdftotext` + grep |
| A12 | Every unreadable item is on the Reading Report and in the reply | manual |
| A13 | Rendered pages inspected visually: no cut-off text, overlap or missing symbols | page images |
| A14 | Every flagged question appears on the Data Notes page and has a boxed note | script |

## 6. Assumptions and open items

- Paper layout (total marks, OR rules, time) is **read from each paper**, not assumed.
- Production Drawing paper structure is read from the paper; no layout is presumed.
- Chapter names are inferred unless a syllabus is supplied.
- Output folder is `/home/user/Abap/msbte_sem3_pdf/` so the student can open it. Nothing
  is committed or pushed unless asked.
- File name `intend.md` is spelled as requested; it can be renamed to `intent.md`.
- **Blocked** until the 12 papers are received.
