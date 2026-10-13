# Slideshow diagram and equation update

The current defense deck is `Brandon L. Byrd -- Thesis Defense -- v4 -- related work revised.pptx` (94 slides). This supersedes the September proposal diagram selection for the active manuscript. The slideshow itself was not edited.

Deck SHA-256: `8f8246d6ca659f30bf9b413d96c264a133ca4931833753c4b9d30bdfcd6516cb`.

## Diagram correspondence

| Defense slide | Active thesis asset |
|---|---|
| 84 | `Fig/frame-map.png` |
| 19 | `Fig/retinanet3d.png` |
| 21 | `Fig/yolov8x.png` |
| 24 | `Fig/score-transfer-limit.png` |
| 23 | `Fig/stage1-transfer.png` |
| 30 | `Fig/stage2-roialign.png` |
| 27 | `Fig/roi-align.png` |
| 32 | `Fig/composition-detail.png` |
| 35 | `Fig/stage3-composition.png` |
| 42 | `Fig/internvideo2-towers.png` |
| 45 | `Fig/stage4-semantic.png` |
| 47 | `Fig/stage5-composition.png` |
| 49 | `Fig/semantic-composition.png` |
| 56 | `Fig/contextual-mean-pool.png` |
| 60 | `Fig/contextual-scene-attention.png` |
| 64 | `Fig/contextual-attention.png` |
| 68 | `Fig/expert-blend-example.png` |
| 70 | `Fig/focal-expert-blend.png` |
| 75 | `Fig/dcb-expert-blend.png` |
| 80 | `Fig/scaled-expert-blend.png` |

The Comp MLP detail is the exact embedded image from slide 32, replacing the rejected older detail diagram. No editable draw.io source for that particular slide image was recovered; its original 3099 × 1200 pixels are retained. Other figures use the approved higher-resolution exports corresponding to the slide images. The deck re-encodes and downsizes its images, so matching uses visual inspection and provenance rather than claiming identical PNG bytes.

Available editable sources and hashes are in `figure-sources/slideshow/provenance.json`. Original source files outside this repository were not modified. Earlier thesis PDFs/draw.io files remain as historical assets but are not used when a slideshow replacement is available.

The obsolete separate Stage 0 summary is removed from the manuscript; the current replicated-detector diagram shows the unused ego branch. Stage 5, contextual mean pooling, standalone scene attention, the illustrative blend, the focal blend, and the original-encoder DCB blend now have their own figures. Repeated transition slides are represented once.

The out-of-fold training and fixed-window crop supplements have no separate counterpart in the current deck. They retain their verified existing diagrams and method descriptions. The dataset example and training-frequency chart in Chapter 1 remain unchanged.

## Mathematical definitions

Added numbered definitions for IoU, interpolated AP/group mAP, conditional score transfer, the RoI linear head, class-weighted focal loss, confidence assembly, the composition MLP, Stage 5/6 input dimensions, scaled dot-product attention, gated language fusion, DCB history, and AP-selected blend weight. Existing phrase-classification, contextual-fusion, all-184 contrastive, DCB, and probability-blend equations remain and have stable labels.

The source-backed distinctions are preserved: Stage 1 transfers scores without confidence multiplication; later learned heads multiply by YOLO confidence once at emission. Scene attention queries use crop plus geometry; language attention queries use the pre-language visual RoI. Stage 5 has no explicit phrase-score input. DCB history excludes the current batch and persists across epochs. Blend selection uses crop AP on 45 reserved training videos, not detector validation AP.

Formula checks use the existing verified thesis protocol, `review/presentation-revisions.md`, `review/results-update.md`, and the archived contextual implementation at `wiki/artifacts/contextual-roi-all184-20260918/pre-adapted-text-refinement/model.py` for the focal and attention operations only. That archived file predates corrected adapted-text contrastive alignment; the corrected equation is retained from the source-audited results update, not inferred from that old auxiliary implementation.

University formatting, chapter structure, results tables, numerical results, bibliography, and approval-page correction are preserved.

## Validation

XeLaTeX/Biber compilation passed: 64 pages, 24 figures, and 19 numbered methodology equations. No undefined references/citations, missing glyphs, or overfull boxes. One inherited nonfatal underfull-line notice remains. The methodology pages, affected preliminary lists, and the full-size Comp MLP page were visually reviewed. Figure hashes and available editable XML validate; the university preamble, results tables, bibliography, and approval correction are unchanged. The local PDF was checked; the Overleaf-rendered PDF was not inspected.
