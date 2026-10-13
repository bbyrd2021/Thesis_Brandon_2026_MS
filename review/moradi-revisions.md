# Dr. Moradi revision record — September 7, 2026

This file is not included in the proposal PDF.

- Matched the supplied February 2026 university Word template’s structure;
  removed Draft 1/status additions and the empty appendix.
- Replaced Times-compatible body fonts with actual 12-point Times New Roman
  using XeLaTeX, including the title page, captions, tables, and references.
  Mathematical symbols use TeX Gyre Termes Math. Diagram labels retain the
  established figure style.
- Justified prose, restored half-inch first-line indentation, and standardized
  body spacing and chapter/section headings.
- Rewrote the abstract to describe the developed pipeline, the functions of
  its components, the principal measured results, and the proposed experiment.
  The introduction expands that explanation; methodology provides full details.
- Added prose before the first section in every chapter, consolidated short
  sections, and removed Organization.
- Expanded related work to 34 existing research papers, checked against primary
  records. Two additional citations document implementation resources.
  BibLaTeX/Biber generate references; all figure/table references use labels.
- Removed duplicate overall titles and explanatory footers from the eight
  figures. Native diagram copies were edited; raw sources were not modified.
  Retained model labels and experimental numbers. Vector PDFs replace raster
  manuscript figures, with editable sources supplied.
- Preserved the reported full-candidate validation results and tail definitions.
  Completed work remains Stages 0–3; semantic classification remains proposed.

## Formatting-source discrepancy

The supplied official `template.docx` says it was updated February 2026. It
places the abstract in Roman-numbered front matter and uses a single-line
`CHAPTER 1: Introduction` heading. The public formatting page
https://www.ncat.edu/tgc/current-students/thesis/format.php
instead describes the abstract as Arabic page 1 and a two-line chapter heading.
These instructions cannot both be followed literally. This revision follows
the supplied template, consistent with the advisor’s request for exactly that
structure. This is not a claim of Graduate College acceptance.

## Validation

41-page local XeLaTeX/Biber compilation with no missing citations, undefined
cross-references, or overfull boxes (one nonfatal underfull-line notice); PDF font-embedding inspection; rendered-page
and figure inspection; citation/label completeness; retained results-table
comparison. The Overleaf browser’s own rendered PDF has not been inspected.

Diagram PDFs were normalized to PDF 1.5 with Ghostscript to avoid a crash in
the older local renderer. Vector content and native .drawio sources are retained.
The latexmk default `-pdf` route also passes through the XeLaTeX build.
