# Presentation-guided proposal revision

Reference deck: `Long-Tail Compositional Road-Event Detection_ A Decoupled Hybrid with Learned and Semantic Composition on ROAD-Waymo.pptx` (75 slides, downloaded September 7, 2026).
SHA-256: `35c8bcb195ac28ffd84d2354e4dd757cbf10bfc0251e8321366f2982624d0f88`.

The visible proposal narrative (slides 1–45) guides the prose. Hidden legacy
Stages 5–6 and the large additional-reading appendix do not expand the scope.
The hidden out-of-fold explanatory slide is used because it documents the
already-completed Stage 3 training method, verified against its source code.
Stock photographs, logos, repeated transition diagrams, and bibliography
screenshots are not imported as scientific figures.

## Added figures

| Slide | Figure | Proposal placement |
|---|---|---|
| 8 | Labeled Car-Stop-VehLane example | Introduction |
| 12 | Frame-level AP evaluation | Dataset and evaluation |
| 21 | Overlap-transfer coverage | Detector replacement |
| 23 | Stage 2 architecture | Direct region features |
| 24 | RoIAlign operation | Direct region features |
| 46 (hidden) | Video-grouped out-of-fold training | Composition learning |
| 27 | Composition MLP/output replacement | Composition learning |
| 35 | Fixed-window crop construction | Proposed crop representation |

Slide 37 becomes an editable phrase-example table. Slides 3–6 inform the scene-
understanding motivation and the JAAD/PIE-to-ROAD literature transition. Slides
29–30 inform the explanation of Stage 2-to-3 tail gains. The matched phrase-
versus-linear comparison remains the primary proposed control.

## Technical checks

- Ground-truth example checked directly in
  `/data/datasets/road_waymo/road_waymo_trainval_v1.1.json`,
  video `train_00407`, frame `1`, annotation `b_49`: Car / Stop / VehLane.
- `ROAD_Reason/experiments/exp11_yolo/results_hybrid_score_transfer.json`:
  match rate 0.40608646897582856 over 6,163,968 candidate boxes / 36,717 frames.
  This is transfer coverage, not recall or accuracy.
- `ROAD_Reason/experiments/exp11_yolo/cache_roi_feats.py`: aligned RoIAlign,
  target-frame P3 slice, one spatial output bin, 256-dimensional feature.
- `ROAD_Reason/experiments/exp11_yolo/train_comp_mlp.py`: video-grouped two-fold
  training, opposite-fold predictions, 49 + 256 inputs, 305 → 512 → 135 MLP.
- `PedestrianIntent++/ROAD_plus_plus_Baseline/modules/evaluation.py`:
  class-specific greedy frame matching at IoU ≥ 0.5, global score ranking,
  interpolated precision envelope, integration over recall changes.
- `ROAD_Reason/experiments/exp12_phrase_head/cache_crop_feats.py`: same padded
  spatial rectangle across eight frames, 224 × 224 crops, target-frame token
  pooling, 1024-dimensional descriptor. This remains proposed work in the paper.
- `ROAD_Reason/experiments/exp12_phrase_head/phrases.json`: exact Car,
  Car-Stop, and Car-Stop-VehLane descriptions.
- Final-defense/submission dates rechecked against the university:
  https://www.ncat.edu/tgc/current-students/thesis/index.php

## Formatting and validation

The university template, front matter, Times New Roman, double-spaced justified
prose, five-chapter structure, and consolidated section hierarchy are retained.
Bibliography entries are kept together across page breaks. Every new figure is
introduced in prose, captioned below, and referenced by a LaTeX label. Duplicate
slide titles and explanatory footers are removed; internal labels and legends
are preserved. Native sources are included and vector PDFs normalized to PDF
1.5 for the local renderer. Raw sources and the presentation are unchanged.

All seven native diagrams passed structural validation with no errors, through-
shape edges, or connector crossings reported. The geometry warnings concern
intentional model badges, sample grids, chart panels, and overlapping boxes in
the IoU illustration. These were inspected in the rendered figures; separating
those overlaps would change the intended diagrams. Retained labels match their
source XML. Results tables match the preceding proposal byte for byte.

The 48-page local XeLaTeX/Biber build and rendered-page review passed; no
missing citations, undefined references, or overfull boxes (one inherited
nonfatal underfull-line notice); all 40
bibliography entries (38 papers and two implementation resources) are cited.
The Overleaf browser-rendered PDF has not been inspected.
