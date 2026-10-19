# Response to post-defense requests — October 16, 2026

Source: Brandon's transcription of Dr. Moradi's message and six-item follow-up list. The newly supplied oral-defense results form is blank; it does not contain written committee feedback, recorded votes, or signatures. The changes below address the supplied comments, not an inferred complete list of committee requirements.

| Request | Work prepared | Remaining action |
|---|---|---|
| Clear description of changes from the base model | Methodology section “What Was Retained and What Was Modified”: inherited components, modification table, baseline/final architecture comparison, and frozen-versus-trained phases | Advisor/committee review |
| More explanation, figures, and examples | Candidate-to-event worked example with explicitly synthetic arithmetic; measured LarVeh and Bus ranking examples, including a failure to retain useful phrase evidence; source hashes retained | Added illustrated Bus recovery and a dedicated logical-consistency section: three synthetic conflict cases, a coherent-but-wrong control, implication equations and a real valid multi-location counterexample. A measured final-CSEB consistency audit remains outstanding. |
| Video of the prototype | Recording plan and acceptance criteria prepared; existing model-diagram animations are not labeled as a working prototype | Locate runnable final system, checkpoint and suitable input; record actual execution and inspect output |
| Journal publication / first draft | Complete generic first manuscript draft in `journal-draft/main.tex`, including methods, verified results, controls, qualitative cases, limitations and references | Confirm journal and author list; advisor revisions, venue formatting, submission and peer review remain pending |
| Personal email after departure | Handoff email field intentionally not guessed | Brandon supplies the preferred address |
| Final pass signature | Blank original form preserved; it is the Master's Thesis Final Defense results form, not evidence of a recorded outcome | Confirm defense date, Banner ID, student email and official vote count; obtain authorized signatures and department routing |
| Final thesis and slides | Revised thesis PDF and unchanged current working deck packaged for review | Committee approval, then send to the intended recipients; university submission remains unconfirmed |

## Scientific boundaries retained

- No new experiments or model performance claims were introduced.
- The worked probabilities are teaching values, not measured predictions on the illustrated car.
- The two qualitative cases are post-hoc seed-0 original-encoder crop diagnostics. They do not demonstrate final CSEB behavior.
- Both visual and text checkpoints, a projection, and cache precision change in the scaling comparison.
- Prototype demonstration, manuscript preparation, journal submission, publication acceptance, and university acceptance are separate completion states.

## Form information still required

The supplied form has fields for student name, Banner ID, program, student email, thesis title, defense type/date, pass/fail vote counts, and signatures. Known names and thesis details can be transferred once the remaining facts are confirmed. Do not infer a vote tally from “passed,” reuse signatures from other forms, or sign on behalf of committee members. The original form remains unmodified.

## October 17 example expansion

Added a second measured-case figure and explicitly synthetic logical-conflict examples in Chapter 4; aligned the journal discussion. The saved case traces do not contain the full joint outputs needed to establish a measured logical-violation rate. No model changes or new empirical results are claimed.

The new source has not been successfully compiled: the temporary TinyTeX runtime no longer contains its support files or format. The existing PDFs remain the previous verified versions and do not contain this addition. Compile the updated GitHub source in Overleaf before using a new final PDF.

## Previous PDF validation (before October 17 additions)

The revised thesis builds to 78 pages; the generic journal draft builds to nine pages. Both pass XeLaTeX/Biber compilation with no overfull boxes, missing glyphs or unresolved references. New thesis pages and all journal pages were visually reviewed. Existing result tables and the university preamble/front matter are byte-identical to the prior commit. The current October 14 working deck was copied unchanged into the local review package.
