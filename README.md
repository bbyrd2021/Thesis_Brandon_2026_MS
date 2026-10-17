# Thesis

Brandon L. Byrd’s NC A&T thesis, updated with the completed semantic-crop and contextual expert-blend results.

## Build

Run from this project directory:

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

Use XeLaTeX and Biber on Overleaf, with `main.tex` as the main document.
`latexmkrc` also routes the default `-pdf` build through XeLaTeX.
The document requires Times New Roman and TeX Gyre Termes Math; these fonts
are embedded in the locally validated PDF. Font binaries are not distributed
in this repository. The current local validation uses XeLaTeX and Biber on macOS;
Overleaf may paginate differently with its TeX Live release.

## Formatting and sources

The supplied official NC A&T `template.docx`, updated February 2026, governs
structure: letter paper, one-inch margins, 12-point Times New Roman,
double-spaced justified prose, Roman preliminary pages, Arabic chapter pages,
and continuous figure/table numbering. The manuscript contains no draft-status
labels or revision notes. Equations use a Times-style mathematical font.

LaTeX provenance: Mahdi Hasanzadeh’s September 2025 NCAT dissertation/proposal
template, licensed CC BY 4.0:
https://www.overleaf.com/latex/templates/nc-a-and-t-state-university-phd-dissertation-slash-proposal-template/jfvggptnckcd

The February 2026 Word template and the university’s formatting webpage differ
on preliminary-page order/numbering and chapter heading layout. This revision
follows the supplied Word template; see `review/moradi-revisions.md`.

The five chapters cover completed Stages 0–6 and contextual fusion, DCB,
expert blending, and paired-encoder scaling. Tables distinguish historical
single runs, repeated-seed means, and external published results.
The literature review uses BibLaTeX;
primary verification links are in `review/citation-verification.md`.

The thesis contains 27 figures, including 20 current defense-diagram exports. Available editable diagram sources and chart data are in
`figure-sources/`. Figure captions, tables, equations, and cross-references are
editable LaTeX. The certification page is unsigned.

Pull Overleaf changes before editing; compile and review before committing
and pushing. Never put credentials in this repository.

Presentation-guided additions are documented in `review/presentation-revisions.md`.

The October 2026 results update and source hashes are recorded in
`review/results-update.md` and `review/results-update-metrics.json`.

Current slideshow diagram correspondence and formula definitions are recorded in
`review/diagram-formula-update.md`; source hashes are in
`figure-sources/slideshow/provenance.json`.

The October 13 advisor formatting pass follows the supplied February 2026 Word template. See `review/template-alignment-20261013.md` for the measured spacing, front-matter positions, and validation.

Post-defense clarification and worked/qualitative examples are tracked in
`review/post-defense-response.md`. The separate `journal-draft/main.tex` is
a generic first paper draft; the thesis main document is still `main.tex`.
