# Thesis proposal

Brandon L. Byrd’s NC A&T thesis proposal, revised in response to Dr. Moradi’s formatting and writing notes.

## Build

Run from this project directory:

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

Use XeLaTeX and Biber on Overleaf, with `main.tex` as the main document.
`latexmkrc` also routes the default `-pdf` build through XeLaTeX.
The document requires Times New Roman and TeX Gyre Termes Math; these fonts
are embedded in the locally validated PDF. Font binaries are not distributed
in this repository. Local validation uses Ubuntu’s TeX Live packages;
Overleaf may paginate differently with its newer TeX Live release.

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

The five chapters distinguish completed Stages 0–3 from proposed Stage 4.
Reported experimental values are preserved. The literature review cites
38 research papers and two implementation resources using BibLaTeX;
primary verification links are in `review/citation-verification.md`.

Sixteen figures include fifteen vector PDFs and one annotated dataset image. Editable diagram sources and chart data are in
`figure-sources/`. Figure captions, tables, equations, and cross-references are
editable LaTeX. The certification page is unsigned.

Pull Overleaf changes before editing; compile and review before committing
and pushing. Never put credentials in this repository.

Presentation-guided additions are documented in `review/presentation-revisions.md`.
