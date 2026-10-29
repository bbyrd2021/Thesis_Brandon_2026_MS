# October28 citation review versions

The original `main.tex`, chapters, bibliography, figures and formatting files are unchanged. Baseline Overleaf commit5995032 has the same tree as GitHub1a1ee8f. `original-manifest.json` preserves every original tracked file hash. A separate original-source ZIP is retained locally.

From the repository root, compile with XeLaTeX and Biber:

```
latexmk -xelatex -outdir=build/clean main-clean.tex
latexmk -xelatex -outdir=build/review main-review.tex
```

On Overleaf, select `main-clean.tex` for the revised manuscript without notes, or `main-review.tex` for red removals, green additions and review notes. `main.tex` remains the original. No change to the project's default root document is required to preserve the original.

Body changes are recorded in `body-changes.json`. Bibliography changes and primary verification sources are recorded in `bibliography-changes.json` and `evidence/`. Changed bibliography entries are green in the review copy; the notes provide the exact old/new field values, including author details hidden by et al. Citation renumbering and pagination caused by the corrections are automatic consequences, not separately colored prose changes.

The clean and review chapter files are paired snapshots, not live-linked editor modes. After future edits, update both from the same reviewed change set. Review notes are excluded from the clean document. The clean copy still needs author/advisor acceptance; unresolved provenance questions are not silently resolved by creating a clean PDF.

Formatting, results and figures are inherited unchanged. This pass does not edit the defense deck or separate IEEE Access journal. Source review uses the provided February2026 university template; it does not substitute for final Graduate College approval.

Follow-through: four attribution/provenance additions, SupCon reference, archived checkpoint hashes and direct author diagram confirmation are included. Defense slide corrections are delivered separately in the Claude review packet. Claude review and final human acceptance remain pending.
