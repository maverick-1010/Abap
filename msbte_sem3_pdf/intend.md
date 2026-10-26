# Intent

## What this project is
One PDF of **solved MSBTE question papers** for a Diploma Mechanical Engineering
student (3rd semester, K-scheme). The student wants to study from the papers of the
last two years and revise quickly before the exam.

## Who it is for
A diploma student preparing for the MSBTE theory exam. Language must be simple
exam-writing English, the way a model answer is written: short points, formulas,
labelled diagrams, marks shown against each point.

## Scope

| Code   | Subject                       | Short |
|--------|-------------------------------|-------|
| 313308 | Strength of Materials         | SOM   |
| 313309 | Fluid Mechanics & Machinery   | FMM   |
| 313310 | Thermal Engineering           | TE    |
| 313311 | Production Drawing            | PD    |

Sessions per subject: **Winter 2024 (W24), Summer 2025 (S25), Winter 2025 (W25)**.
That is 4 subjects x 3 sessions = **12 papers**.

## What the student gets
One PDF with a table of contents and subject-wise bookmarks. For every subject and
every session:
1. The questions as printed in the paper, same order, with marks.
2. A complete step-by-step solution for every question, in MSBTE model-answer style
   (key points, formulas, diagrams described or drawn, marks split).
3. Numericals: Given data, Formula, Calculation, Final answer with unit.
4. Drawing questions (Production Drawing): part list, materials, proportions and the
   drawing procedure.

At the end of each subject:
- Chapter-wise marks table
- Top 10 repeated questions
- One-page last-minute revision sheet

## Rules from the student (non-negotiable)
1. Use only the attached papers as the source of questions. Do not guess a missing
   question. Say which paper or page could not be read.
2. Point out every question whose data looks misprinted and state the assumption made.
3. All calculations are done in code and double-checked.
4. The PDF has a table of contents and subject-wise bookmarks.
5. Language stays simple (exam-writing style).

## Honest limits (to be stated in the PDF itself)
- The solutions are written by Claude. They are **not** the official MSBTE model
  answers, so the marks split and wording can differ from the official scheme.
- Chapter names in the marks table are Claude's classification from the question
  content unless the student supplies the syllabus.
- "Repeated questions" come from only 3 sessions per subject, so repetition is a weak
  signal. The ranking rule is stated on the page.

## Success looks like
- Every readable question from the 12 papers is in the PDF, in paper order, with the
  correct marks, and nothing is invented.
- Every numerical answer in the PDF is the output of a script that was also verified
  a second way.
- Every misprint doubt and every unreadable page is listed openly.
- The student can jump to any subject, session or question from the bookmarks.

## Out of scope
- Papers of other subjects, sessions or schemes.
- Official MSBTE model answers or marking schemes (unless the student supplies them).
- Printing layout beyond A4 PDF; Marathi or Hindi translation.
- Committing or publishing anything to GitHub unless asked.

## Status
**First full build done** from the papers received: Thermal Engineering W24 and S25, Production Drawing W24 and S25, and one Strength of Materials paper (Summer 2023, I-scheme – not a requested session).
**Still missing (8 of the 12 requested papers):** SOM W24, S25, W25; FMM W24, S25, W25; TE W25; PD W25. The build is data driven, so each new paper is a new module in `src/papers/`.

Output: `out/MSBTE_Sem3_Mechanical_Solved_Papers.pdf`; checks: `out/verification_report.txt`.
