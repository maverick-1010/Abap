# Design

How the specs in `specs.md` are built. Intent is in `intend.md`.

## 1. Tools (checked in this environment)

| Need | Tool |
|------|------|
| Page images from papers | `pdftoppm` (PDF) / direct image read |
| Text layer (if the PDF has one) | `pdftotext`, `pdfplumber` |
| Build PDF, TOC, bookmarks, figures | `reportlab` 5.0.1 (platypus + graphics) |
| Check output (pages, outline) | `pypdf` 6.x, `pdfplumber` |
| Numbers | `numpy`, plain `math` |
| Fonts | DejaVu Sans, DejaVu Sans Bold, DejaVu Sans Mono (installed) |

Not installed: `matplotlib`, `sympy`, `tesseract`, `fitz`. So: diagrams are drawn with
`reportlab.graphics`, scanned pages are read visually from page images, and the
second-check calculations use plain Python.

## 2. Folder layout

```
msbte_sem3_pdf/
  intend.md  specs.md  design.md
  input/papers/                  # the 12 files (untrusted, read-only)
  work/pages/<SUBJ>-<SESS>/p01.png ...
  data/
    reading_log.json
    qbank/<SUBJ>-<SESS>.json
    solutions/<SUBJ>-<SESS>.json
    calc_results/<id>.json
    backmatter/<SUBJ>.json       # chapter table, top 10, revision sheet
  src/
    ingest.py                    # render pages, write reading_log
    qbank_check.py               # FR-2.3 marks totals, schema checks
    calcs/<SUBJ>/<id>.py         # one script per numerical
    calc_runner.py               # runs scripts, runs checks, writes results
    figures/<name>.py            # reusable vector figures
    content_check.py             # marks split, numbers match results
    build_pdf.py                 # builds sample or full PDF
    verify_pdf.py                # acceptance checks A1 to A14
  out/
```

Scripts live in `src/`, away from `input/`. Anything that reads papers runs as
`python3 -I src/<script>.py <path>`.

## 3. Pipeline

```
papers --ingest--> page images + reading_log
       --transcribe--> qbank JSON --qbank_check--> (fix reading errors)
       --write solutions + calc scripts--> solutions JSON, calcs/*.py
       --calc_runner--> calc_results/*.json (with second-method check)
       --content_check--> (blocks build on any mismatch)
       --build_pdf--> out/*.pdf --verify_pdf--> acceptance report
```

The solution text never contains hand-typed numerical results. A `numerical` block holds
only a reference to `calc_results/<id>.json`, and `build_pdf.py` prints the numbers from
that file. This is how FR-4.2 and A6 are guaranteed.

## 4. Calculation scripts

Each numerical has one script with a fixed shape:

```python
ID = "..."                      # same as the question id
def given():   ...              # list of (symbol, value, unit)
def steps():   ...              # list of (label, formula, substitution, value, unit)
def answer():  ...              # list of (name, value, unit)
def check():   ...              # second, independent method -> (method_name, passed)
```

- `calc_runner.py` imports each script, runs the four functions, compares `check()` with
  `answer()` at a stated tolerance, and writes the result JSON. A failure stops the build.
- Second check is chosen per problem, for example: substitute the answer back into the
  governing equation, use an energy or force balance, use a different but equivalent
  formula, or check units / order of magnitude.
- Misprint tests are also coded here (impossible ratio, negative value, missing input), so
  the doubt is raised by code and not only by eye.
- Conversions (mm to m, kW to W, rpm to rad/s, bar to N/m^2, and similar) are separate
  named steps so they appear in the printed solution.

## 5. Solution content design

One template per question type, so every answer looks the same to the student.

**Theory** (marks shown on the right of each heading)
1. Definition / statement (1 line)
2. Key points or classification (bullets)
3. Formula or equation if any
4. Sketch (figure or one-line description)
5. Marks split table at the end

**Numerical**
`Given:` table -> `Formula:` lines -> `Calculation:` numbered steps -> boxed
`Final answer:` with unit. A grey "Check" line shows the second method result.

**Drawing (Production Drawing)**
1. Part list table: Part No. | Name | Material | Qty.
2. Proportions table (in terms of the main dimension)
3. Drawing procedure, numbered steps
4. Vector figure of the asked views, with dimensions and hatching

**Data note box** (any type): red-edged box with "Data note: doubt / assumption used".

## 6. Figures

- Built with `reportlab.graphics` (vectors, so text stays sharp and file size is small).
- A small library of reusable pieces: beam with loads, SFD / BMD, stress-strain curve,
  P-V and T-S diagrams, velocity triangles, pump / turbine layouts, and drawing helpers
  (centre lines, hatching, dimension arrows, thread symbols, title block).
- Each figure is a function `fig_name(params) -> Drawing`. Drawing-question figures take
  the proportions as parameters, so the drawing and the proportions table cannot disagree.
- Sketch quality target: clear and exam-like, not artistic.

## 7. PDF layout

- A4, margins 18 mm left/right, 16 mm top/bottom. Body DejaVu Sans 10 pt, line spacing
  about 1.35. Headings in DejaVu Sans Bold.
- Question header strip: `Q.3 (b)   [4 Marks]` on a light grey bar, then the question text
  as printed, then `Ans.` and the solution.
- Colours: black text, one dark blue for headings, light grey for bars, red edge for data
  notes. Prints clearly in black and white.
- Running header: `313308 Strength of Materials | Winter 2024`. Footer: page number.
- Tables use thin lines and repeat the header row if they break across pages.
- Questions are kept together with their header (no header at the bottom of a page alone).

### Table of contents and bookmarks
- Built with `TableOfContents` and `multiBuild` (two passes) so page numbers are right.
- Each subject, session and end-of-subject page is registered with `bookmarkPage` +
  `addOutlineEntry`, giving clickable TOC links and the outline tree:

```
Front matter
  Reading Report
  Data Notes
313308 Strength of Materials
  Winter 2024
    Q.1 ... Q.n
  Summer 2025
  Winter 2025
  Chapter-wise marks
  Top 10 repeated questions
  Revision sheet
313309 ...  (same pattern)
```

### One-page revision sheet
Own page template with a two-column dense frame and `KeepInFrame(mode='shrink')`. If the
content is still too big, the build fails with a message, and the content is trimmed.
It is never allowed to run onto a second page (A8).

## 8. Back-matter logic
- **Chapter table:** from `chapter` and `marks` in the question bank; sums by chapter and
  session; total row compared with the bank total.
- **Top 10:** questions are grouped into a "concept key" (written by hand when
  transcribing, for example `SOM:thermal-stress-bar`). Rank by number of sessions, then
  total marks. Ties are listed in order of paper appearance. Fewer than 10 groups means
  fewer rows, never padding.
- **Revision sheet:** written from the formulas and topics actually used in that
  subject's papers, so it matches the exam pattern the student will meet.

## 9. Verification
`verify_pdf.py` runs A1 to A14 from `specs.md`: reads the question bank and calc results,
reads the PDF with `pypdf` / `pdfplumber`, and prints a pass / fail table. I also render
sample pages with `pdftoppm` and look at them (A13). The reply to the student includes the
table and the list of unreadable or misprinted items.

## 10. Milestones

| # | Milestone | Done when |
|---|-----------|-----------|
| M0 | Intake | 12 papers received, reading log complete |
| M1 | SOM question bank + solutions | A1 to A7 pass for SOM |
| M2 | SOM sample PDF | Student approves layout and style |
| M3 | FMM | Same checks pass |
| M4 | TE | Same checks pass |
| M5 | PD (drawing work, slowest) | Figures match proportions tables |
| M6 | Merge, TOC, bookmarks, full verify | A1 to A14 pass, delivered |

## 11. Risks and how they are handled

| Risk | Handling |
|------|----------|
| Blurry or cropped paper pages | Reading Report; never guess; ask for a better scan |
| Misread digit changes a numerical | Marks-total check, re-read figures, flag doubtful digits |
| Solution differs from official scheme | Stated openly; cross-check if model answers are supplied |
| PD figures take long and can look rough | Parametric helpers; sample reviewed early |
| Very large PDF | Vector figures only; no embedded photos |
| Revision page overflows | Build fails instead of spilling; content trimmed |
