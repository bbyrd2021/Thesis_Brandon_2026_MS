# Thesis results update, October 13, 2026

The source manuscript was synchronized from Overleaf commit `e6f389c2ae1b27af319a113def3e6a0445837ecb` before editing. A complete source backup is retained outside the Overleaf repository in the research wiki at `artifacts/thesis-results-update-20261013/overleaf-before.zip`.

## Scope

Updated the abstract and all five chapters from proposal framing to the completed study. Moved the semantic crop method and its original figures from Chapter 5 to Chapter 3. Added Stage 5/6 distinctions, contextual visual and language fusion, corrected all-184 contrastive loss, dynamic class balancing, probability blending, paired-encoder scaling, partition/selection details, new results and limitations. Added six related-work citations. Preserved the title, university preamble, main document structure, front matter other than the abstract, and all pre-existing figure bytes.

The reference slideshow is the local `Brandon L. Byrd -- Thesis Defense -- v4 -- related work revised.pptx`. Its narrative guides coverage; raw experiment records govern numbers. The slideshow was not edited. Corrected its apparent 35.35 agent entry for the RoI linear head to the verified 35.25, used IoU 0.5 (not 0.5%), and used the verified mean-pool-to-attention deltas rather than an unmatched slide-transition subtraction.

## Numerical provenance

`results-update-metrics.json` stores the source paths, SHA-256 digests, seed values, means and sample standard deviations used for new tables. The early-stage tables retain the original verified source values. Their raw metrics are `wiki/artifacts/post-proposal-experiments/cluster-results/metrics/stage0.json`, `stage2.json`, and `stage3.json`; the original Stage 1 comparison remains unchanged.

New source groups:
- `wiki/artifacts/post-proposal-experiments/cluster-results/metrics/seed*-*.json`: frozen original crop heads and composition models.
- `wiki/artifacts/contextual-roi-20260917/all-results.json`: focal contextual baselines.
- `wiki/artifacts/contextual-roi-all184-20260918/all-results.json`: adapted-text all-184 auxiliary.
- `wiki/artifacts/contextual-gate-20260919/all-results.json`: focal expert blend.
- `wiki/artifacts/contextual-roi-dcb-20260921/all-results.json`: DCB experts and blend.
- `wiki/artifacts/contextual-roi-langctl-20260919/all-results.json`: original-encoder bypass/random-bank controls.
- `wiki/artifacts/contextual-roi-1b-20260930/results-verified-20261005/full-summary.json`: scaled experts and CSEB, with original per-run source hashes.

All new local result tables use detector AP@IoU0.5 on 36,717 validation frames. Original baseline stages are single runs. Later tables use seeds 0/1/2; SD means sample SD, not standard error or a confidence interval. The 28 deeper-tail classes are contained within the 47 tail classes. Published reference rows come from ROAD-Waymo Table 3 and the archived FRCB Table 3, with FRCB Table 5 separately identifying the five-run mean. They are not matched reruns.

## Method and figure provenance

Method descriptions were checked against archived `train-repeats.py`, contextual study protocol files, `contextual-evolution-20260924/technical-evidence.md`, the DCB implementation specification, and the verified 1B scaling record. The original-encoder control evidence does not establish language effects in the scaled system. The scaling comparison changes both pretrained towers, projection and numerical cache path.

Three new architecture figures are byte-identical approved exports with their editable draw.io ancestors. `figure-sources/results-update-provenance.json` records source paths and hashes. The figures reuse established geometry, colors, routing, source imagery, and citations. Their scene imagery is illustrative, not a new evaluated detector prediction.

The six bibliography additions use original CVF/arXiv author records for MViT, MViTv2, MeMViT, STMixer and CycleACR, and the supplied original FRCB paper. CycleACR cites its 2023 technical report, matching the discussed model, not an invented CVPR venue.

## Local compilation

Local validation uses temporary TinyTeX with XeLaTeX and Biber. macOS does not resolve the newly downloaded math font by family name, so the temporary build copy resolves the exact same `texgyretermes-math.otf` by file path. The committed preamble retains `TeX Gyre Termes Math` unchanged for Overleaf. No font substitution or manuscript formatting redesign is made. Final compile and visual-check evidence is recorded outside the manuscript in the wiki update artifact directory.

Final local build: 59 pages, 19 figures, 12 tables, and 46 cited references. No missing citations/cross-references or overfull boxes. All text remains within page bounds. Original formatting and pre-existing figure assets verified unchanged across 64 protected files. Full-page contact sheets and focused figure/table renders were inspected.
