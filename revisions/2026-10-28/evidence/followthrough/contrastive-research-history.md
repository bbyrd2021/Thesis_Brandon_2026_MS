---
type: direction
title: "Class-conditioned language fusion for long-tail road events"
aliases: [class-conditioned fusion gate, per-class language gate]
created: 2026-09-11
updated: 2026-09-17
sources: [wiki/artifacts/class-conditioned-fusion-discussion.md, wiki/artifacts/class-gate-study/protocol.json]
tags: [road-waymo, long-tail, language, fusion, research-proposal]
status: draft
novelty: false
novelty_status: close-prior-art-identified-specific-contribution-unverified
feasibility: cluster
datasets_required: [road-waymo, bdd-x]
---

# Class-conditioned language fusion for long-tail road events

**Current deadlines (Brandon, September 14):** matched study **September 25**; committee draft **October 1**; defense window **October 14–16, 2026**. See [[thesis-defense-roadmap-2026]] for priorities, controls and the working schedule.

## Research question

Can a small module learn which ROAD-Waymo composition classes need language support, improving rare-event recognition while preserving the overall performance of the learned composition classifier?

Brandon proposed this direction on September 11, 2026: common compositions may not need as much help as rare ones, so the model could conditionally strengthen individual class-score columns. This is an experiment proposal, not an implemented module or a verified novelty claim. The required Boolean `novelty: false` records that algorithmic novelty has not been established. The subsequent review found close precedents for the broad idea.

## Motivation: measure the tradeoff

Slide 67 of the working presentation contains the following historical ROAD-Waymo results:

| Stage | Configuration | All-triplet f-mAP (%) | Deep-tail f-mAP: 28 classes (%) |
|---|---|---:|---:|
| 4 | Phrase head on InternVideo2 crops | 8.94 | 4.63* |
| 5 | Flat head + composition MLP on crops | 11.13 | 4.25 |
| 6 | Phrase evidence fused into the MLP | 10.98 | 4.73 |

The slide is explicitly titled **ARCHIVED: MIXED-PROTOCOL METRICS**; its Stage 4 deep-tail value carries an unexplained asterisk. These values motivate a hypothesis, not a definitive matched comparison. They suggest stronger overall performance from Stage 5 and stronger deep-tail performance from phrase-based scoring/fusion. The ongoing repeated-seed study must establish the tradeoff under a shared frame population and evaluator before claims are made.

See [[directions/thesis-proposal-fall-2026]] for the approved scope and [[findings/exp12-phrase-head-attribution]] for historical attribution experiments. Do not conflate the 28-class deep tail in this slide with the 47-class tail used elsewhere, or with historical validation-ranked rare-class subsets.

## Proposed module

For crop x and composition class c, blend the two experts' calibrated probabilities before applying the shared detector confidence:

\[
p_c(x)=(1-g_c(x))p_{\mathrm{MLP},c}(x)+g_c(x)p_{\mathrm{phrase},c}(x),\qquad 0\leq g_c(x)\leq1.
\]

The final score is \(s_c(x)=q(x)p_c(x)\), where q is YOLO agentness. Apply q exactly once. Here a "column" means one output class across detections, not a metric column in the presentation table. Larger g gives language more influence; the convex blend is not guaranteed to increase a numerical score or improve AP.

Start with the 135 composition outputs (49 duplex + 86 triplet), retaining the 49 agentness/primitive outputs and detector boxes unchanged. This preserves the 184-score layout. Report triplet results separately from duplex results.

The first learned version uses \(g_c=\operatorname{sigmoid}(a_c)\): one scalar parameter per composition class. It learns class preferences without assuming that every rare class benefits from language. A later version can condition g on the current crop and expert disagreement, allowing different decisions for different examples of the same class.

## Architecture and gate-training diagrams

These diagrams specify the proposed first gate experiment, grounded in the existing Stage 4 phrase head and Stage 5 composition MLP. They are a design specification, not a report of an implemented or trained gate. Shape, color, and frozen-component conventions follow the proposal presentation.

### Architecture

![Class-conditioned fusion architecture: shared crop features, two frozen experts, 135 class gates, and final 184-score assembly](../artifacts/class-gate-diagrams/class-gate-architecture.png)

[Full-resolution PNG](../artifacts/class-gate-diagrams/class-gate-architecture.png) · [PDF](../artifacts/class-gate-diagrams/class-gate-architecture.pdf) · [Editable draw.io source](../artifacts/class-gate-diagrams/class-gate-architecture.drawio)

Each composition class has one learned mixture weight, shared across crops. The gate blends 135 composition probabilities; YOLO agentness multiplies the result once. The other 49 outputs retain their existing assembly. The flat head's first 49 sigmoid probabilities used internally by the MLP are distinct from those final 49 detector/primitive scores.

### Gate fitting and regularization

![Gate training: held-out video predictions, a fixed global anchor, class-specific weights, classification loss, and shrinkage](../artifacts/class-gate-diagrams/class-gate-training.png)

[Full-resolution PNG](../artifacts/class-gate-diagrams/class-gate-training.png) · [PDF](../artifacts/class-gate-diagrams/class-gate-training.pdf) · [Editable draw.io source](../artifacts/class-gate-diagrams/class-gate-training.drawio)

Fit a global gate logit a0 first, then hold it fixed while learning 135 class logits. The proposed objective combines probability-space binary cross-entropy before detector-confidence scaling with mean squared deviation of the class logits from a0. This regularizer discourages unsupported extreme class weights; it does not guarantee a global fallback. Explicitly fix classes without positive gate-training examples to a0 if that fallback is required. Select regularization strength on internal development videos and keep the final evaluation set separate. Existing expert training uses focal loss; BCE here is a proposed gate-fitting choice.

[Artifact notes and implementation grounding](../artifacts/class-gate-diagrams/README.md) document dimensions, source files, and technical/visual review. The [builder](../artifacts/class-gate-diagrams/build.py) reproduces the editable diagrams. See [[comparisons/class-conditioned-language-fusion-review]] for the evidence behind this design.

## Experiments and controls

1. Compare the MLP alone, phrase head alone, and existing Stage 6 fusion on identical inputs and evaluation frames.
2. Add a single global mixing weight to test whether simple blending already explains the improvement.
3. Add fixed frequency-based weights, using training frequencies only, as a simple reference.
4. Learn per-class weights; compare against the global gate and fixed frequency rule.
5. Only then test input-dependent weights, controlling additional capacity.

Fit gates and any calibration on training-only out-of-fold predictions. For the composition MLP, this requires predictions that are also out of fold with respect to the MLP itself: the existing MLP's out-of-fold *inputs* do not make its own training-row outputs out of fold. Use nested video-level folds or a separate video-level gate-training split. Do not tune gates on the final reported evaluation set.

Sparse positive examples can make rare-class gates unstable. Test shrinkage toward a global weight and report learned weights across seeds. Select hyperparameters using an internal development split. Fix the scoring/calibration convention across comparisons; if calibration is added, include calibrated expert-only controls as well.

Report overall triplet f-mAP, tail 47, deep tail 28, common 39, paired seed differences, and all per-class AP changes under the same 36,717-frame protocol. Class groups come from training frequencies. Plot learned language weights against training frequency and actual per-class gains; frequency alone does not establish benefit. The goal is to characterize the tail–overall tradeoff and determine whether gating improves that balance.

## BDD-X adaptation: a separate experimental axis

Brandon selected BDD-X first and deferred CoVLA because of storage constraints. Pair BDD-X video segments with their timestamp-aligned action descriptions and justifications for contrastive adaptation of InternVideo2; then regenerate ROAD-Waymo crop features and retrain the same downstream heads. See [[datasets/bdd-x]], [[datasets/covla]], and [[comparisons/bdd-x-vs-covla]]. Current local video availability and the trainable checkpoint components still need verification.

First test gating with the original encoder. Then compare original versus BDD-X-adapted encoders with and without the gate, keeping downstream settings fixed. This separates encoder adaptation from fusion changes. Neither adaptation nor gating has been launched as part of the currently running seed study.

## Candidate contribution and prior-art check

The candidate contribution is class-dependent allocation of language evidence to improve long-tail compositional road-event recognition, supported by controlled attribution and a measured tail–overall tradeoff. Do not claim the blending formula itself is new.

Review class-wise expert gating, long-tail expert ensembles, visual–language score fusion, and frequency-conditioned calibration before making a novelty claim. The wiki already contains [[comparisons/fusion-for-detection-lit-review]]; that is a starting point, not an exhaustive novelty assessment. Distinguish this proposal from the existing Stage 6 MLP, which already receives phrase evidence and can implicitly learn class-dependent combinations. The explicit gate must demonstrate value in performance, interpretability, parameter efficiency, or stability relative to that baseline.

## Literature review update — September 11

[[comparisons/class-conditioned-language-fusion-review]] ingests seven primary papers. DRAGON already combines visual/semantic experts with sample- and frequency-dependent weighting; CLEAR explicitly weights experts by class reliability; SemLT3D uses semantic routing in long-tailed driving detection. The broad gate is therefore not a new concept. Start with global versus shrunk class-specific blending and existing Stage 6; evaluate a narrower composition-aware contribution. A constant rescaling of final scores cannot improve AP with unchanged rankings/candidates, whereas mixing complementary experts can.

## Adaptation pilot authorized — September 11

Brandon authorized [[directions/bddx-contrastive-pilot]] following the completed repeated-seed results. The bounded first phase tests partial two-tower adaptation on BDD-X, separately from gating. The earlier statement that neither experiment had launched described the initial discussion; see the pilot page for current scope and queue status.


## Conditional fusion and moving below composition scores — 2026-09-14T06:35:15-04:00

Brandon proposed adaptive/conditional/gated language fusion and potentially moving one level lower. This extends the existing September 11 proposal; no implementation or experiment launch is implied. Current motivation is the completed controlled study: repeatable standalone phrase-head tail gains, no reliable mean Stage 6 improvement, and mixed per-class gains/losses. The historical table above is not the current evidence; use [[findings/post-proposal-controlled-study]].

**Current Stage 6 already learns nonlinear fusion:** its MLP receives 1024 crop features, 49 primitive/agentness scores and 135 phrase composition scores. It can learn input- and class-dependent interactions implicitly. An explicit gate tests a different inductive bias, not the first availability of conditional fusion.

Three distinct insertion points:

1. **Composition-score gate:** blend frozen Stage 5 and phrase-head probabilities with g_c(x), fitted on genuinely held-out expert predictions. Crop features, both experts' scores and disagreement may be inputs; confidence is not correctness. Start with global and shrunk class gates before an input-dependent gate. Preserve identical detector score handling and evaluate common/tail AP. No guarantee that mixtures improve either expert.
2. **Primitive-level gate:** blend action/location evidence before the composition MLP. This tests sharing across compositions through better-supported primitives. Keep agent outputs from YOLO under the current protocol. Retrain the composition MLP on appropriately out-of-fold gated inputs; changing its input distribution at inference alone is not a fair test. Primitive fusion can lose useful full-composition language evidence and is a separate hypothesis, not automatically better.
3. **Feature-level conditioning:** let a candidate phrase embedding modulate the cached crop feature before scoring, e.g. h_c(x)=x+g_c(x)⊙Delta(x,t_c), where the learned correction has the same feature dimension. An identity-biased residual path permits a baseline-like starting point; freezing encoders avoids a new cache pass. Use known class prompts, never the ground-truth class as inference input. A shared correction across classes or factorized primitive prompts can reduce independent rare-class parameters. This operates on pooled vectors; spatial/temporal token cross-attention requires token caches or fresh extraction. Do not claim the residual mathematically guarantees preserved AP.

Existing support for the broad methods: [Gated Multimodal Units](https://arxiv.org/abs/1702.01992) learns multiplicative modality gates; [FiLM](https://arxiv.org/abs/1709.07871) conditions intermediate features through learned feature-wise affine modulation. Their results do not establish gains for ROAD-Waymo or novelty of this proposal. The prior literature review linked above contains closer expert-fusion precedents.

Recommended sequence: test an explicit score gate with the original encoder and genuinely held-out expert outputs; compare against Stage 5, current Stage 6, global blending and matched shuffled-text controls. If pursuing lower-level fusion, make feature conditioning a separate cell with the same cached features and a capacity-matched visual-only correction. A useful gate weight is not a causal explanation by itself: measure prediction/AP changes when phrase evidence is removed or shuffled. No final-evaluation-based class selection or tuning.


**September 14 diagnostic evidence:** [[findings/post-proposal-per-class-results]] now contains a completed frozen-checkpoint prediction trace, not only class AP comparisons. At disclosed equal prediction budgets, some phrase-only GT recoveries are preserved and some lost by Stage 6. This supports testing selective fusion, while not establishing that the gate can identify recoveries prospectively. Use held-out training-video predictions for gate fitting; keep these final-validation examples diagnostic only.


## Recommended first gate after prediction tracing — 2026-09-14T07:43:30-04:00

**Decision recommendation, not a launched experiment:** retain the original frozen encoder and experts; blend Stage 5 composition probabilities with standalone phrase-head composition probabilities after the heads and before the single YOLO confidence multiplication. Start with a 135-parameter class gate (49 duplex, 86 triplet), shrunk toward a fitted global gate. The traced class-level and instance-level complementarity supports this first test; it does not establish optimality or guaranteed gain.

Let a0 be a learned global mixing logit, a_c the class mixing logit, g_c=sigmoid(a_c), and p_c=(1−g_c)p5_c+g_c*pPhrase_c. Fit a0 on held-out training predictions, then initialize a_c=a0 and fit class weights with BCE(p,y)+lambda*mean_c((a_c−a0)^2), keeping a0 fixed. Use clamp only for numerical log safety. Classes with no positive gate-training examples retain a0 explicitly. This is 135 gate parameters in the class-fitting phase; optional calibration would add parameters and requires separate controls. Keep expert-only endpoints as baselines. The global anchor may favor either expert; it is not an assumption that Stage 5 must always dominate every class.

- Gating uses independent sigmoid probabilities, not a softmax across mutually compatible composition labels.
- No hard-coded rule that rarity implies greater language weight; no gating by whether a validation case looked like a success. The seven classes and selected pictures motivate analysis but do not train/select the gate.
- A constant class weight still changes candidate rankings when mixing two different experts. Merely scaling one expert's final class column by a positive constant cannot improve AP under unchanged candidates/ties/matching.
- Fit on a video-level split excluded from both experts' training, or nested cross-fitted expert outputs. Existing Stage 5 OOF inputs are insufficient to make its outputs held out. Cached features avoid encoder extraction, but generating honest held-out expert outputs may require head/MLP refits. Match the expert-only baselines to the same training data.
- BCE is a first fitting objective, not a guarantee of AP gain. Tune regularization on separate internal-development videos using a declared triplet-mAP criterion; report tail47/deep28/common39 and duplex metrics. Preserve the current score convention initially. If adding calibration, fit it internally and compare calibrated expert-only baselines as well.
- First comparison: Stage 5, phrase head, existing Stage 6, global blend, shrunk class gate; matched seeds and final candidates. Language attribution controls remain necessary before a semantic claim.
- If a class gate is insufficient, add a small shared per-crop adjustment g_c(x)=sigmoid(a_c+h_theta(p5_c,pPhrase_c,abs(p5_c−pPhrase_c),optional compact crop context)), initialized with zero adjustment and regularized toward the class gate. Confidence/disagreement are features, not correctness labels. Keep feature-level conditioning as a later distinct experiment rather than changing encoders at the same time.

Primary precedent rechecked: [DRAGON, WACV 2021](https://openaccess.thecvf.com/content/WACV2021/papers/Samuel_From_Generalized_Zero-Shot_Learning_to_Long-Tail_With_Class_Descriptors_WACV_2021_paper.pdf) combines visual and semantic predictions with sample-dependent mixing and class-frequency modulation. It supports the broad direction but is a different single-label classification setting, not proof of detection gains or novelty here. See [[comparisons/class-conditioned-language-fusion-review]] for calibration/reliability precedents and [[findings/post-proposal-per-class-results]] for the actual diagnostic evidence.


## Gate study authorized and launched — September 14, 2026

Brandon authorized the recommended experiment with “full send.” [Fixed protocol and scripts](../artifacts/class-gate-study/README.md). New isolated cluster root `/work/bbyrd1/class-gate-study-20260914/`; original source study remains read-only.

Eight variants × seeds 0–2: flat head, phrase head, Stage 5, Stage 6, global blend, shrunk class gate, shuffled global blend, shuffled class gate. Original frozen encoder and original cached crop rows. No new video extraction. Actual expert heads/MLPs are refit on 70% of training videos so that the separate 15% gate-fitting and 15% development videos are genuinely excluded from their supervised fitting. Two-fold composition inputs remain inside the expert partition.

**Implementation decision:** original training caches do not retain full YOLO-positive crop coordinates/features, so lambda selection uses held-out **cached-crop triplet AP**, not detection f-mAP. The cached rows preserve GT-positive + random-background + YOLO-junk-negative training. This is a disclosed fitting/deployment mismatch; final evaluation still uses the unchanged 36,717-frame YOLO-candidate detector protocol. Matched expert-only baselines use the same 70% training split. Do not directly rank the gates against older full-data training as an isolated gate effect.

Global weights fit BCE. Class logits initialize at and shrink toward the fixed fitted global logit; lambda grid is 0, 0.0001, 0.001, 0.01, 0.1. Zero-positive gate-fitting classes explicitly retain the global weight. Selection uses internal-development triplet crop AP, with all 86 triplets included and AP=0 for unsupported classes; ties choose stronger regularization. No final-evaluation fitting or hyperparameter selection. The official validation data previously informed the hypothesis through diagnostics, so no fresh blind-test claim is made.

The full synthetic pipeline passed all eight evaluations and the split, mixture, unsupported-class, learning-direction and AP checks before submission. See [test record](../artifacts/class-gate-study/test-result.json). Production input audits and afterok dependencies guard release of actual training/evaluation. Three seeds measure optimization variability within one fixed video partition.

<!-- CLASS GATE STATUS START -->

Last collected: **2026-09-14T15:44:03.380030+00:00**. **24/24 final evaluations available.**

```text
731453        COMPLETED   00:03:39      0:0
731456        COMPLETED   00:00:09      0:0
731454_0      COMPLETED   00:19:12      0:0
731454_1      COMPLETED   00:11:08      0:0
731454_2      COMPLETED   00:09:23      0:0
731455_0      COMPLETED   00:59:25      0:0
731455_1      COMPLETED   01:00:01      0:0
731455_2      COMPLETED   01:00:36      0:0
```

Actual video split: {'expert': 420, 'gate': 90, 'development': 90}. Crop rows (expert/gate/development): [2567474, 580250, 595732]. Final-video overlap: 0. Nonfinite training elements replaced using the original recipe: 0.

Matched 70%-video experts; mean ± sample SD across three head-training seeds. Percentages.

| Variant | Triplet | Tail 47 | Deep 28 | Common 39 |
|---|---:|---:|---:|---:|
| head-flat | 7.6876 ± 0.1595 | 2.9030 ± 0.0791 | 2.2403 ± 0.4463 | 13.4535 ± 0.3244 |
| head-phrase | 8.7984 ± 0.1584 | 5.6659 ± 0.1775 | 4.5360 ± 0.1615 | 12.5735 ± 0.1373 |
| stage5 | 10.1612 ± 0.1276 | 4.6823 ± 0.1609 | 3.3459 ± 0.2540 | 16.7641 ± 0.1176 |
| stage6 | 10.2583 ± 0.2870 | 5.2236 ± 0.4470 | 3.7785 ± 0.9812 | 16.3257 ± 0.1864 |
| global-blend | 10.1650 ± 0.1295 | 4.6879 ± 0.1644 | 3.3524 ± 0.2557 | 16.7656 ± 0.1178 |
| class-gate | 10.1650 ± 0.1295 | 4.6879 ± 0.1644 | 3.3524 ± 0.2557 | 16.7656 ± 0.1178 |
| shuffled-global | 10.1618 ± 0.1286 | 4.6834 ± 0.1628 | 3.3479 ± 0.2544 | 16.7639 ± 0.1175 |
| shuffled-class-gate | 10.1618 ± 0.1286 | 4.6834 ± 0.1628 | 3.3479 ± 0.2544 | 16.7639 ± 0.1175 |

All metrics and paired differences are descriptive; gate settings were chosen on internal crop AP, not these detection results. Official validation previously informed the hypothesis; this is not a fresh blind test.

[Collected run evidence](../artifacts/class-gate-study/collected/). This is a one-time collection; no continuous local monitor is implied.

<!-- CLASS GATE STATUS END -->


## Completed gate study — September 14, 2026, 11:44 EDT check

All 24 evaluations and the summary job completed successfully at 10:26:23 EDT (14:26:23 UTC). Original fixed frame/candidate hashes verified. The selected class gate gives 10.1650 triplet f-mAP versus matched Stage 5 at 10.1612: approximately +0.0038 percentage points. Tail-47 changes 4.6823 → 4.6879 (+0.0056 pp). This is effectively unchanged performance.

The phrase mixing weights are only 0.001491–0.001527 across seeds (about 0.15% language / 99.85% Stage 5). All seeds select lambda=0.1, the strongest tested shrinkage, leaving class weights almost identical to the global anchor. Six composition classes with no gate-fitting positives use the explicit global fallback. Class and global gates have identical reported means at four decimals; shuffled controls also remain effectively Stage 5.

The phrase head still exceeds the flat head on tail-47 (5.6659 versus 2.9030), while matched Stage 6 reaches 5.2236. Thus this particular BCE-fitted, strongly shrunk gate did not preserve the available phrase-head tail advantage. Near-zero language weighting is observed; whether calibration, the BCE objective, crop/evaluation distribution mismatch, or optimization accounts for it requires a separate diagnostic. It is not evidence of encoder representation collapse or proof that conditional fusion cannot work. No additional experiment was launched during this status check.


## Gate mathematics and interpretation audit — September 14, 2026

The implemented composition mixture is $p_{ic}=(1-g_c)p^{(5)}_{ic}+g_cp^{(L)}_{ic}$, with $g_c=\sigma(a_c)$ and final detection score $s_{ic}=q_i p_{ic}$. There are 135 composition weights (49 duplex, 86 triplet). The global version shares one weight. Neither version conditions its weight on the crop; these are static mixture baselines, not a learned per-instance router.

Fit the global logit using unweighted mean BCE over held-out crop/class pairs. Then fit class logits using mean BCE plus $\lambda C^{-1}\sum_c(a_c-a_0)^2$, with fixed global anchor $a_0$. Encoders and expert heads are frozen during gate fitting. The experts themselves were trained with class-weighted focal loss, so their sigmoid outputs are not guaranteed calibrated for this new unweighted BCE objective.

For an unclamped probability, $\partial\ell/\partial g=(p-y)(p^{(L)}-p^{(5)})/[p(1-p)]$. On a negative pair this reduces to $(p^{(L)}-p^{(5)})/(1-p)$; on a positive pair it is $-(p^{(L)}-p^{(5)})/p$. Language can help positive ranking yet lose the aggregate BCE tradeoff across negative pairs. This is an explanation of a possible mechanism, not a measured decomposition of this run.

A further verified result: even lambda=0 leaves every supported class's language weight below 0.00153 in all three seeds; the lowest weight is sigmoid(-8)=0.00033535, the implementation's logit lower bound. Thus shrinkage alone cannot explain near-zero language usage. Initializing class logits at the already near-zero global solution and the small sigmoid derivative warrant an optimization audit. The global fit began at g=0.5, not near zero. Repeated expert seeds demonstrate repeatability within one video split, not robustness across splits.

Next diagnostic before a more complex gate: evaluate held-out BCE versus mixing weight (including exact endpoints), separate positive/negative loss contributions and class support, and compare Adam solutions to direct bounded minimization in probability space. Without shrinkage and away from numerical clipping, BCE of an affine probability mixture is convex in g: the second derivative is $(p^{(L)}-p^{(5)})^2[y/p^2+(1-y)/(1-p)^2]\ge0$. This provides a check for optimizer artifacts. Separately plot internal-development AP versus weight to test objective mismatch; do not choose settings from final detection evaluation. Calibration and a later input-dependent gate are hypotheses to test, not established fixes. No additional jobs launched for this math explanation.


## Authorized objective audit — 2026-09-14T11:56:09.004793-04:00

Brandon authorized the next-step audit and explicitly requested that all work be logged. [Audit protocol, code and collection instructions](../artifacts/gate-objective-audit/README.md). Launched priority CPU array 731554 in isolated `/work/bbyrd1/gate-objective-audit-20260914`, using original saved gate/development predictions for three expert seeds and correct/shuffled phrase controls. No encoder extraction or expert retraining. Tests passed known endpoint/interior optima, finite-difference gradient, and AP support checks.

The audit computes direct unregularized convex BCE optima and fixed-weight curves, including separate positive/negative BCE contributions and development tail/common crop AP. Expert endpoint clipping is documented as a slight numerical distinction from deployed post-mixture clipping. No final detection evaluation is consulted. Calibration and input-dependent gates remain contingent on the findings, not assumed fixes. Initial seeds 0 and 1 report a global phrase BCE optimum of exactly zero; class/AP analysis is pending at this timestamp.


## Completed objective audit — 2026-09-14T11:58:45.773506-04:00

All three tasks of priority array 731554 completed successfully (1:10, 1:15, 1:46). Direct convex BCE global optimum is **zero language in all three seeds**, for both correct and shuffled experts. Correct phrase class optima are zero for 127/129, 127/129, and 129/129 supported classes; the largest nonzero optimum is 0.0008342. Thus a substantially positive BCE solution was not missed by the original optimizer under this numerical audit.

Internal-development results from the fixed grid (cached-crop AP, **not final detection f-mAP**):

| Seed | Stage 5 triplet AP | Grid-best triplet AP | Language weight | Stage 5 tail AP | Tail AP at selected weight |
|---|---:|---:|---:|---:|---:|
| 0 | 13.1580 | 15.8690 | 0.75 | 4.4503 | 9.9729 |
| 1 | 14.3712 | 16.4997 | 0.5 | 6.5396 | 9.4373 |
| 2 | 13.3065 | 15.9978 | 0.75 | 4.9625 | 10.0153 |

Larger weights improve development triplet ranking in all seeds, while gate-fitting BCE prefers zero. This supports an objective mismatch across the fitting/development partitions, rather than an Adam initialization fluke. At the pure expert endpoints, the increase in BCE is predominantly the negative-pair contribution; this does not by itself establish miscalibration as the cause. Development grid maxima are selection diagnostics, not unbiased new performance estimates.

[Loss and AP curves](../artifacts/gate-objective-audit/collected/objective-curves.png), [numeric curves](../artifacts/gate-objective-audit/collected/curves.csv), and [full protocol](../artifacts/gate-objective-audit/README.md). Recommended next isolated comparison: lock a global weight using internal-development triplet AP and evaluate correct/shuffled blends under the unchanged detector protocol, before adding a conditional network. No follow-up detector job has been launched yet.


## Development-AP-selected blend authorized and launched — 2026-09-14T12:07:35.779655-04:00

Brandon authorized testing development-AP-selected blending. [Frozen protocol, scripts and verification](../artifacts/ap-selected-blend/README.md). Scalar language weights selected by mean internal-development crop AP over all 86 triplets, independently per seed/control, with exact ties favoring less language. Correct phrase weights: 0.75 / 0.50 / 0.75; shuffled: 0.35 / 0.35 / 0.35. These are frozen before new detection evaluation. No final detection AP used to choose them.

Six new detection evaluations reuse the same frozen 70%-video experts and 36,717-frame YOLO-candidate protocol. Agentness/primitive AP reused unchanged; duplex/triplet AP recomputed. Isolated cluster root `/work/bbyrd1/ap-selected-blend-20260914`. Priority CPU evaluation array 731568, dependent summary 731569. No encoder extraction, expert retraining, calibration or conditional gate added. Tests passed selection/tie rules, original matching-function equivalence and end-to-end Stage 5/phrase endpoint AP parity.

This tests weight-selection objective effects following the BCE audit. Previous validation analysis informed the follow-up; it is not a fresh blind test. Use matched 70%-video controls, not historical full-training scores. Three seeds still share one partition.

<!-- AP BLEND STATUS START -->

Last collected: **2026-09-14T16:44:56.302616+00:00**. **6/6 new detection evaluations available.**

```text
731569        COMPLETED   00:00:10      0:0
731568_0      COMPLETED   00:15:26      0:0
731568_1      COMPLETED   00:15:28      0:0
731568_2      COMPLETED   00:14:14      0:0
```

Matched 70%-video experts. Mean ± sample SD across three seeds; detection AP percentages.

| Variant | Triplet | Tail 47 | Deep 28 | Common 39 |
|---|---:|---:|---:|---:|
| stage5 | 10.1612 ± 0.1276 | 4.6823 ± 0.1609 | 3.3459 ± 0.2540 | 16.7641 ± 0.1176 |
| stage6 | 10.2583 ± 0.2870 | 5.2236 ± 0.4470 | 3.7785 ± 0.9812 | 16.3257 ± 0.1864 |
| global-blend | 10.1650 ± 0.1295 | 4.6879 ± 0.1644 | 3.3524 ± 0.2557 | 16.7656 ± 0.1178 |
| class-gate | 10.1650 ± 0.1295 | 4.6879 ± 0.1644 | 3.3524 ± 0.2557 | 16.7656 ± 0.1178 |
| shuffled-global | 10.1618 ± 0.1286 | 4.6834 ± 0.1628 | 3.3479 ± 0.2544 | 16.7639 ± 0.1175 |
| ap-blend | 10.4589 ± 0.3010 | 6.2816 ± 0.1736 | 5.0151 ± 0.2345 | 15.4931 ± 0.6975 |
| ap-shuffled-blend | 9.9763 ± 0.0725 | 4.7300 ± 0.0942 | 3.4421 ± 0.3204 | 16.2987 ± 0.0714 |

[Collected evidence](../artifacts/ap-selected-blend/collected/). One-time collection; no continuous local monitoring implied.

<!-- AP BLEND STATUS END -->


## Interactive seesaw explainer — 2026-09-14T12:17:53.140168-04:00

Brandon requested an HTML explanation using a seesaw analogy, progressing from big picture to detailed math. [Self-contained interactive HTML](../artifacts/seesaw-language-explainer/seesaw-language.html), [build provenance](../artifacts/seesaw-language-explainer/provenance.json). Local Firefox access: `http://127.0.0.1:8875/seesaw-language.html` while the local server runs.

The page separates the analogy, a labelled synthetic 22-crop BCE/AP counterexample, and measured three-seed audit curves. It includes synchronized mixture sliders, seesaw animation with pause, correct/shuffled and seed controls, fixed-grid measured readouts, frozen AP-selected weights, timestamped non-live job status, q-once mathematics, and global/class-wise/scene-dependent gate distinctions. Teal/purple/gold retain the prior explainer identity; this educational interaction is not a replacement stage architecture figure. Offline desktop/mobile checks passed, including toy ranking/loss behavior, measured numerical readouts, evidence download, and no page overflow.


## Correction: slide 67 historical comparison — 2026-09-14T12:28:34.538670-04:00

Brandon correctly recalled Stage 6 as the best deep-tail model **among the rows in original slide 67**. Live slide and all seven raw-result rows verified; 28-class AP recomputed from original per-class records. Historical Stage 4/5/6 deep-tail AP is **4.627903 / 4.251427 / 4.727382**. The assistant had instead quoted the new 70%-video three-seed means **4.536005 / 3.345924 / 3.778501**, causing an inappropriate change of comparison cohort. Both numeric sets are source-correct, but the prior answer should have verified the intended cohort rather than contradicting the historical recollection.

[Full slide/source audit and provenance](../artifacts/slide67-results-audit/results.md). The deck labels this table archived and mixed-protocol; stages 4–6 use 36,716 frames and stages 0–3 use 36,717. The principal new-study differences are expert training fraction and repeated-run aggregation, not merely the empty additional frame. Separate historical phrase-v2 achieves 4.829383 and is not a row in this table. No slide or original raw result was modified. Always qualify stage metrics by cohort, training fraction, aggregation and tail threshold.


## Stage 6 rarity-aware loss hypothesis — 2026-09-14T12:31:49.386513-04:00

Brandon asked whether the archived Stage 6 result was a fluke and suggested adapting its loss to the deep-tail status of crop labels. The full-training repeated-seed study provides the appropriate robustness check, distinct from the current 70%-video gate cohort. Deep-28 Stage 5 versus Stage 6: seed 0, 4.278677 / 5.191551; seed 1, 5.708841 / 3.982791; seed 2, 4.334131 / 4.521435. Means ± sample SD: Stage 5 4.773883 ± 0.810172; Stage 6 4.565259 ± 0.605570. Stage 6 wins 2/3 paired seeds but loses on the mean because seed 1 reverses strongly. These do not establish a reliable Stage 6 advantage; archived values remain real, and “fluke” is not a statistical conclusion established here.

Both Stage 5 and Stage 6 already use class-weighted focal loss with gamma=2; the unweighted BCE audit applied to the separate post-hoc gate. Do not attribute the gate's demonstrated BCE tradeoff directly to Stage 6. Rarity belongs to a class under training-frequency statistics, not intrinsically to a crop; a multilabel crop may have common primitives and a rare triplet. Proposed weighting should act per crop/label loss term and not require ground-truth rarity at inference.

Recommended next design, not launched: a 2×2 matched comparison of Stage 5/6 × existing/revised composition loss, keeping source features and primitive/phrase heads fixed. Begin with a bounded smooth increase in rare-positive weight (optionally centered around z=-0.5), audit existing alpha weights first, and preserve negative penalties. Select hyperparameters on internal development, report common/tail/deep/overall and seed variability. Negative suppression or asymmetric focal exponents should be a separate loss factor, not silently bundled with rarity weighting. Success in both Stage 5 and Stage 6 would show imbalance handling; an additional reproducible Stage 6 gain, with semantic controls, is needed for language attribution. Current AP-selected blend evaluation continues unchanged.

Primary precedents checked: [Cui et al., CVPR 2019, Class-Balanced Loss](https://openaccess.thecvf.com/content_CVPR_2019/html/Cui_Class-Balanced_Loss_Based_on_Effective_Number_of_Samples_CVPR_2019_paper.html) provides effective-number class weighting; [Ridnik et al., ICCV 2021, Asymmetric Loss](https://openaccess.thecvf.com/content/ICCV2021/html/Ridnik_Asymmetric_Loss_for_Multi-Label_Classification_ICCV_2021_paper.html) addresses positive/negative imbalance in multilabel classification. They motivate tests but do not establish gains on ROAD-Waymo.


### AP-selected interim interpretation — 2026-09-14T12:35:56.282012-04:00

5/6 evaluations collected. All three correct-phrase blends are complete: mean triplet 10.458916, tail47 6.281575, deep28 5.015077, common39 15.493149. Compared with the matched 70%-video Stage 5/6 controls, tail and deep-tail AP improve while common AP decreases. These are not historical slide-67 models. The third shuffled evaluation and final summary remain pending; do not report a complete semantic-control comparison yet.


### Completed AP-selected detector comparison — 2026-09-14T12:45:41.798153-04:00

All six new detector evaluations and summary job completed successfully at **12:36:55 EDT** (16:36:55 UTC). Final three-seed means: AP-selected correct phrase blend triplet **10.458916**, tail47 **6.281575**, deep28 **5.015077**, common39 **15.493149**. Shuffled AP-selected blend: **9.976264 / 4.729956 / 3.442061 / 16.298739** (see collected summary for authoritative full precision).

The correct blend exceeds matched Stage 5 and Stage 6 on tail47 and deep28 in every seed. Versus Stage 5 mean deltas: approximately +0.298 triplet, +1.599 tail, +1.669 deep, -1.271 common percentage points. Versus Stage 6, mean triplet is +0.201 but wins only one of three paired seeds; do not claim consistent overall superiority. Correct blend also beats independently AP-selected shuffled controls on triplet/tail/deep in every seed. Different selected control weights mean this is a comparison of complete selection procedures, not an equal-weight semantic ablation.

Interpretation: the AP-selection follow-up realizes tail-ranking improvements under the full detection evaluator that the BCE-selected near-zero mixture missed, while sacrificing common-class performance. This strengthens evidence for useful correct-phrase expert information in this setting, without establishing split robustness, formal significance or pure semantic causality. Keep the matched 70%-video cohort separate from historical slide 67 and the full-training repeat study. [Completed summary and paired differences](../artifacts/ap-selected-blend/collected/summary.json).


## ROAD-supervised encoder adaptation feasibility — 2026-09-14T12:53:08.651407-04:00

Brandon asked whether data supports agent-aligned contrastive adaptation and whether ROAD can backpropagate into encoders. Verified local ROAD-Waymo v1.1 JSON exists (1.1 GB), raw frame samples exist under `rgb-images/train_00407`, and `exp12_phrase_head/phrases.json` contains class text. The existing crop-cache writer decodes eight real frames and extracts a padded fixed keyframe-box region across them, yielding a 1024-d keyframe feature. This is not a verified moving tracked crop; tracking/label persistence would need separate validation if introduced. Dataset plus existing code supports constructing annotated crop/phrase supervision, but a new training manifest has not been audited or built.

Recommended first adaptation: training videos only, frozen text encoder and most vision blocks, train final vision block(s)/projection with composition focal classification plus a weighted supervised crop-to-phrase contrastive term. Keep the contrastive path connected to the exact feature used downstream; prior BDD-X pilot adapted projected embeddings while downstream used intermediate keyframe features. Multiple valid positive triplets and duplicate labels must not become in-batch false negatives; use label-aware positives and carefully defined negatives. Ground truth creates training supervision only; detector evaluation remains YOLO candidates. No gradients can flow back through cached detached features.

[Supervised Contrastive Learning, Khosla et al., NeurIPS 2020](https://papers.neurips.cc/paper_files/paper/2020/hash/d89a66c7c80a29b1bdbab0f2a1a94af8-Abstract.html) supports multiple supervised positives in general; the proposed multilabel crop/text construction is our adaptation to test. ROAD class phrases are annotation-derived descriptions, not independent natural-language explanations. This tests supervised in-domain adaptation, not external-language transfer, new human rationale learning or unseen-triplet generalization. Current data supports the existing tail-gain claim within the fixed study; it does not yet demonstrate that encoder adaptation improves it.

Necessary attribution controls: frozen encoder; same encoder unfreezing with classification loss only; classification plus contrastive loss, under matched training budget and split. Begin with text frozen for interpretability and stability; unfreezing both towers is technically possible but a later change. No new jobs launched for this feasibility discussion.


## ROAD-aligned gradient pipeline authorized — 2026-09-14T13:43:00.984404-04:00

Brandon authorized implementation and the bounded pilot with “take it away.” [Fixed pilot protocol and scope](../artifacts/road-contrastive-adaptation/README.md). Isolated root `/work/bbyrd1/road-contrastive-pilot-20260914`. Prepare job 731611 builds audited raw crop/phrase supervision; gradient smoke job 731612 depends on successful preparation. Three pilot conditions will be released only after smoke passes. Last visual block only, text frozen, same seed0 expert initialization, fixed lambda=0.001, three epochs. This is not the completed matched detector study.

<!-- ROAD CONTRASTIVE PILOT STATUS START -->

Last collected: **2026-09-14T18:55:44.713959+00:00**.

```text
731611        COMPLETED   00:02:20      0:0
731612        COMPLETED   00:01:40      0:0
731626_0      COMPLETED   00:06:36      0:0
731626_1      COMPLETED   00:06:46      0:0
731626_2      COMPLETED   00:04:39      0:0
```

Audited crop manifest:
- train: 32 videos, 128 keyframes, 941 crop rows, 55/86 triplets represented.
- dev: 8 videos, 32 keyframes, 247 crop rows, 31/86 triplets represented.

Gradient smoke passed. Classification visual-gradient norm 0.0263916; contrastive visual-gradient norm 2.38837; actual visual update norm 0.0280454; peak allocated GPU memory 12.36 GB. Frozen parameters unchanged.

Pilot internal-development crop AP only; one seed, not full detector results.

| Condition | Baseline AP | Best baseline/epoch AP | Selected | Peak GPU GB |
|---|---:|---:|---|---:|
| frozen | 8.4353 | 8.4353 | baseline | 7.39 |
| classification | 8.4353 | 8.4353 | baseline | 10.80 |
| contrastive | 8.4353 | 8.4353 | baseline | 10.81 |

3/3 pilot conditions complete.

[Collected evidence](../artifacts/road-contrastive-adaptation/collected/).

<!-- ROAD CONTRASTIVE PILOT STATUS END -->


### Completed ROAD gradient pilot — September 14, 2026

All three conditions completed by 17:59:54 UTC (13:59:54 EDT), collected at 18:55:44 UTC. Baseline internal-development triplet crop AP was 8.4353 in every condition.

| Condition | Epoch 1 | Epoch 2 | Epoch 3 | Selected checkpoint |
|---|---:|---:|---:|---|
| Frozen encoder, head updates | 5.9190 | 5.7735 | 6.7704 | Starting baseline |
| Classification, final visual block + head updates | 5.9282 | 5.7365 | 6.9382 | Starting baseline |
| Classification + contrastive, final block + head/projection updates | 5.9389 | 5.7542 | 6.7775 | Starting baseline |

Engineering checks passed: gradients reach the intended visual block, encoder weights change in both adaptation arms, and frozen parameter hashes remain unchanged. Each job completed in under seven minutes including startup; measured training portions were 224–241 seconds. This does not establish full-dataset wall time.

No adaptation benefit was demonstrated. Training objective decreased while development classification loss increased in all three arms, including the frozen encoder control. This is consistent with overfitting or distribution shift from continuing a broadly trained head on a tiny selected subset; it does not isolate the cause or establish encoder collapse. Contrastive development loss briefly improved (3.3563 baseline to 3.1805 at epoch 2) without a corresponding AP improvement.

Scope: one seed, 941 training rows from 32 videos, 247 development rows from 8 videos, only 31/86 development triplet classes present. These are crop-level flat-head proxy metrics, not Stage 5/6 full YOLO detector mAP or deep-tail results. Retain the original checkpoint; audit head-update stability and sampling before scaling or adding external adaptation data. A frozen-head diagnostic would help isolate visual-feature changes from head drift.


## Full Stage 5/6 encoder study — authorized September 14, 2026

Brandon requested the complete Stage5 and Stage6 architectures, then explicitly replaced further small training pilots with full-data training. Only the necessary one-step architecture/gradient checks ran (731836); no six-arm small-subset training was submitted. Both stages exactly matched original source inference in FP32 (maximum difference0); classification and contrastive gradients reached the final visual block; Stage5/6 composition MLP gradients were positive, and Stage6 phrase-branch gradients were positive.

The full study uses all420 expert videos and all90 development videos, every saved training frame/crop from the paired-cache shards (GT positives +8 random negatives +up to16 YOLO-junk negatives), with gate videos and official evaluation held out. Three full epochs, seed0, same original encoder and existing complete expert initializations. Six runs: Stage5/6 × frozen encoder / classification partial-unfreezing / classification+contrastive partial-unfreezing. All downstream modules train jointly; only the final visual encoder block unfreezes in adaptation conditions. Stage5 never consumes phrase scores at inference; contrastive supervision uses a separate auxiliary projection.

Classification loss remains the original weighted focal gamma2 applied to the full assembled184 logits. Effective optimizer batches contain at least256 crops accumulated in microbatches up to16. Full development and detector inference use up to64 crops per forward. Contrastive lambda.001, visual LR1e-5, downstream LR1e-4; fixed text prototypes. This is a full warm-start study, not a fresh from-scratch or multi-seed comparison.

Submitted September14 at19:42:40 UTC (15:42:40 EDT): preparation731841; training array731843 (six tasks, up to4 priority H200s); dependent final evaluation array731844 (up to2 H200s). Preparation currently running, training awaits its integrity checks. Full developer-set AP selects baseline versus epoch checkpoints; official YOLO evaluation follows automatically using36,717 locked frames and includes tail47/deep28/common39. Seven-day job ceilings comply with QoS and are not runtime estimates. Training progress/checkpoints support diagnosis and resumption.

Canonical source is now `ROAD_Reason/research/post-proposal/stage56-full/`, per Brandon's code-location instruction. All149 earlier code/protocol files were preserved in the same repo under `historical/`; see [[tools/research-code-provenance]]. Collected reports: `artifacts/stage56-full/collected/`.


### September 15 recovery — 2026-09-15T00:04:18-04:00

Original full-training array731843 failed in all six conditions during initial development evaluation because `/work/bbyrd1/adapted-road-20260911/frames` disappeared. Its disappearance is verified; cause is unknown. Preparation had verified inputs previously. No training checkpoint was saved and no full-model performance result is available. This is a staging failure, not evidence about the loss or encoder adaptation.

Local original158,081 images (43,665,411,419 bytes) all exist and match inventory sizes. Eight transfer streams are restoring them into the full study's dedicated `/work/bbyrd1/stage56-full-20260914/frames/` directory. `ROAD_FRAME_ROOT` changes the storage location only; crop rows, labels, split, architecture and loss remain unchanged. Recovery verifier732169 waits for complete sizes and checks prepared train/dev image hashes. Replacement six-run array732170 depends on verification; replacement detector evaluations732171 depend on their training task. Stale evaluation array731844 was canceled because its dependencies could never succeed.

Development evaluation now caches each frame atomically with model/data/crop-code provenance. Test passed identical AP, reuse of completed frames, recomputation only of missing frames, and rejection of changed-model caches. No old development predictions can be recovered from the original failure, so initial evaluation restarts. Canonical recovery source committed in ROAD_Reason at `76b59cc`. Transfer and integrity checks are still in progress; no successful restart claimed yet.

## 2026-09-17 10:52 EDT — First full-study epoch results

Full90-video development triplet crop AP, seed0; not detector AP or tail-specific AP:

| Condition | Initial | Epoch1 | Change (points) |
|---|---:|---:|---:|
| Stage5 frozen encoder | 12.237806 | 13.489893 | +1.252087 |
| Stage5 classification adaptation | 12.237806 | 13.687565 | +1.449759 |
| Stage5 classification+contrastive | 12.237806 | 13.902646 | +1.664840 |
| Stage6 frozen encoder | 13.850310 | 14.726142 | +0.875832 |

All four select epoch1 over baseline and are now in epoch2. Stage5 contrastive exceeds classification-only by0.215081points, and classification-only exceeds frozen by0.197672points. Preliminary one-seed evidence; no significance, final detector benefit, or deep-tail gain established. Frozen arms also improve from further head training. Stage6 adaptation arms remain in epoch1 at34,391/80,626 frames (42.7%); their accuracy comparisons are pending. All six jobs running, monitor fresh, no failure alerts. Raw reports: `artifacts/stage56-full/collected/stage5-{frozen,classification,contrastive}.partial.json` and `stage6-frozen.partial.json`.

## Composition-aware contextual gate proposal — September19,2026

Brandon requested a more novel gate after the contextual composition experiment. Proposal only: no new training launched. The completed study lowers mean triplet/tail under both objectives; its positive interaction is inconclusive. Do not assume expert complementarity is exploitable from mean scores alone.

Recommended candidate: a **composition-aware reliability gate**, conditioned on the actor and candidate label. Start with frozen attention-contextual classification and corrected all184 contrastive flat184 experts to hold architecture constant. Both already include language attention; this is objective-dependent expert fusion, not a visual-versus-language causal comparison. Compare the final model descriptively with the MLP-context contrastive overall leader. Additional experts should require development-set complementary-error evidence first.

For each duplex/triplet, share router parameters across its constituent agent/action/location labels. Inputs include predicted primitive support, expert disagreement, crop/context evidence, training-only class support and optionally phrase embeddings. An interaction term handles whole-composition evidence beyond constituent contributions. A rare triplet can thereby borrow routing supervision from common primitives and related compositions. Gate output varies by actor AND candidate class; rarity is a property of candidate labels, never inferred from ground-truth labels at deployment. Read composition mappings from verified label strings, never fossil childs arrays.

Blend frozen probabilities as p_c=(1-g_c(x))*p_class,c+g_c(x)*p_contrast,c, then apply detector confidence exactly once. Route135 composition scores initially and preserve the49 primitive/agentness assembly. Convex blending offers no AP-improvement guarantee. Shared primitive routing, composition interaction, uncertainty shrinkage toward a development-selected global mixture, and ranking-oriented fitting are candidate ingredients—not established novelty or guaranteed performance.

Prior BCE gate audit selected effectively zero language whereas AP-selected blending recovered tail gains in the older matched70%-video cohort. This motivates a class-balanced ranking surrogate and actual development AP selection, rather than assuming BCE fitting optimizes the desired detector ranking. Train only the small router on predictions from videos excluded from expert fitting; separately reserve video-level selection data. Audit the reserved90-video gate split and prior exposure; contextual caches currently cover train/dev/validation, so gate context may need extraction or predictions. Do not silently fit/select on official validation or reuse expert-checkpoint-selection development predictions as fully untouched gate evidence. Include a global AP-selected blend, shrunk class gate, generic actor/class router of comparable capacity, and the proposed factorized router. Primitive/semantic inputs need ablations before causal claims. Report overall/common/tail/deep across seeds; no common-performance preservation guarantee from a penalty.

Novelty scan: [RIDE](https://arxiv.org/abs/2010.01809) already routes diverse long-tail experts; [CLEAR](https://arxiv.org/abs/2608.11287) aggregates by class reliability; [BalPoE](https://openaccess.thecvf.com/content/CVPR2023/papers/Aimar_Balanced_Product_of_Calibrated_Experts_for_Long-Tailed_Recognition_CVPR_2023_paper.pdf) studies calibrated expert combinations; [compositional knowledge transfer](https://openaccess.thecvf.com/content/CVPR2022/papers/Parisot_Long-Tail_Recognition_via_Compositional_Knowledge_Transfer_CVPR_2022_paper.pdf) already uses composition for long-tail recognition. Existing wiki review also discusses DRAGON and SemLT3D. Thus neither gating, frequency conditioning, nor composition alone is new. Candidate contribution is transferring routing reliability through shared event primitives for actor-level multilabel detection with ranking-aware evaluation. A closer methods comparison remains necessary before claiming originality.

Storage implication: preserve detector prediction matrices during complementary-error/blend analysis. Do not execute the previously proposed development-score cleanup yet; decide which matrices the audit needs first. Head-only router training avoids backbone updates, but held-out gate feature availability and disk budget must be checked before promising no additional feature extraction or an ETA.

## Gate implementation authorized and preparation started — September19,2026

Brandon approved proceeding. Canonical code: `ROAD_Reason/research/post-proposal/contextual-gate/`; frozen specification/artifacts: `wiki/artifacts/contextual-gate-20260919/protocol.json`.

**Design locked before fitting:** same-seed frozen attention-classification and attention-corrected-all184 flat184 contextual experts. Route135 compositions; retain classification expert's49 primitive/agentness outputs. The generic router receives the same candidate, primitive-probability and16 pooled crop/context descriptors as the factorized router, with2341 versus2314 trainable parameters. Factorized router shares reliability functions/embeddings across verified primitive constituents and adds a composition interaction. No language-specific causal claim: both experts already include language attention.

Reserved90 videos are split by fixed video-ID hash into45 fitting and45 selection, disjoint from420 expert-training,90 expert-development and official evaluation videos. **Selection labels choose the global blend anchor used during gate fitting/regularization and subsequently choose epochs**; this is validation-tuned configuration, not a claim that selection labels never influence the fitting procedure. Gradient examples are only from45 fitting videos. Existing official-validation exposure makes the follow-up exploratory.

Controls: AP-selected global blend (grid0:0.125:1), shrunk class gate, generic conditional router and factorized router, each paired across seeds0–2. Learned gates use five epochs×500 steps,16 supported classes per step,8positive/8negative rows per class, pairwise logistic ranking of blended-probability logits, lr0.001/weight-decay0.0001. Gate deviations shrink according to positive fitting-video support n/(n+5), with0.01 squared penalty toward the global anchor; anchors clipped to[1e-4,1−1e-4] in learned models. Zero-supported classes remain at that clipped anchor. Selection uses triplet crop AP; final endpoint is official detector tail47 factorized-minus-generic, with overall/common/deep and simpler controls also reported. This surrogate is not exact AP optimization; GT/random/junk fitting rows differ from final YOLO-candidate population.

CPU export735058 completed in6min14s:580250 actor rows from17335 frame examples. Original encoder cache untouched; missing gate-context features must be extracted locally. Preparation validates source shard hashes, frame hashes and video disjointness. Original prediction matrices are retained; final gated validation scores are reconstructed in RAM, with resumable per-class metric files, avoiding another~51GiB of persistent score matrices. Expected incremental gate storage under10GiB; no files deleted.

Independent subagent review cleared the installed code after dependency/result-signature and prediction-resume guards; four router tests passed. Additional production preflight verifies real cache integrity, matching class mapping, frozen experts, production forward/gradients and exact optimizer next-step roundtrip. Pipeline enforces both preflight success and source-hash review clearance before fitting. Two-minute monitor plus existing repair dispatcher registered and checked; CPU export complete, local context extraction active at12:05EDT. Per-frame extraction is resumable. Initial40-frame benchmark including startup projects~108min extraction; refine from steady progress. Fitting/evaluation ETA is provisional pending measured throughput; no gate metrics yet.

Separate FRCB/DCB proposal reviewed in [[contextual-head-dcb-loss]] and deferred. Its difficulty weights are not direct rarity weights, and replacing focal+alpha need not preserve gradient scale.

At12:07EDT the steady extraction rate measured~10frame examples/sec,1277/17335 complete, estimated~27min remaining; budget30–45min for extraction. Revised provisional first gate detector result13:07–14:07EDT, all controls/seeds14:07–15:07EDT, pending measured fitting/evaluation throughput. Monitor fresh/active; gate healthy/failure dispatcher fixtures passed. See artifacts/contextual-gate-20260919/eta.json.

## Completed gate study — September19,2026,14:07:49EDT

All12 detector evaluations completed; checked19:03EDT against raw results and selected-checkpoint hashes. Production preflight passed, fit/selection disjointness and fixed36717-frame/candidate protocol retained. Global contrastive weights selected on45 selection videos:0.375/0.625/0.375 for seeds0/1/2.

| Model | Triplet mean | Tail47 | Deep28 | Common39 | Duplex |
|---|---:|---:|---:|---:|---:|
| Matched attention classification |12.02425|6.18940|4.47845|19.05599|18.52173|
| Matched attention contrastive |12.12293|5.79250|3.85111|19.75192|18.83115|
| Global AP-selected blend |12.58362|6.48812|4.74494|19.92949|19.20074|
| Class gate |12.59025|6.49958|4.74673|19.93028|19.20329|
| Generic conditional gate |12.58794|6.53427|4.72801|19.88339|19.18003|
| Composition-aware factorized gate |12.59332|6.52498|4.77672|19.90645|19.15659|

Factorized triplet mean±sampleSD12.59332±0.33418. Versus classification: triplet+0.56908,tail+0.33558,deep+0.29826,common+0.85047. Triplet/tail/common improve in all3 seeds; deep improves2/3. Versus matched contrastive: triplet+0.47039,tail+0.73248,deep+0.92561,common+0.15454; all four improve in all3 seeds. This supports useful complementary expert predictions under the tested held-out blending protocol; no pure language-causality claim.

**Primary novelty test not supported by these data:** factorized-minus-generic tail47 mean−0.00930; per-seed[+0.02138,−0.06401,+0.01475], unadjusted95%paired-t interval[−0.12730,+0.10871]. Factorized-minus-global triplet+0.00970 and tail+0.03686 are small and uncertain. The global blend already captures nearly all observed improvement. No established benefit from compositional routing, no proof of equivalence from nonsignificance; keep all controls in the thesis. Generic is numerically highest tail47; factorized highest triplet/deep means by small margins. Primitive action21.54277/location26.15676 are fixed to classification by construction.

New factorized overall mean12.59 is descriptively higher than previous single contextual leader12.17405 and published FRCB event11.53; published comparisons retain pretraining/protocol/seed-count caveats. Historical full-trainingStage6 deep4.5653 is below factorized mean4.7767 descriptively, but cohorts differ. NCShare ROAD-adaptedStage6 detector results are still pending, so the conditional larger-encoder decision is not yet resolved. Current recommended simple performance reference is the global blend; retain factorized as the tested research hypothesis, not a demonstrated novelty win.

At19:03EDT NCShare Stage6 adapted classification/contrastive were47.3%/47.8% through epoch2. Stage5 frozen enteredepoch3 (~7.3%). Two active epoch1 detector inferencers22400/36717 and22325/36717 (~61%). Monitor/repair reported no incidents. Local study service inactive because complete, not failed.
