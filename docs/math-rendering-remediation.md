# MathML and visualization remediation plan

## Baseline

The latest successful main-branch workflow inspected for this plan is run
44911829560 at commit a7cd5678bed4b0fe58ae092523bfc7f03abd93d9 (2026-11-21).

Its existing teaching-quality artifact reports:

- 132 registered articles (126 published, 6 draft).
- 27 articles with zero MathML in the original-question section.
- 21 articles with zero MathML inside all solution steps.
- 37 articles with raw-formula candidates in the question.
- 87 articles with raw-formula candidates in the solution section.

These are structural indicators, not 27 or 87 proven errors. The older audit only
counts whether a section or all steps contain MathML; it can miss individual steps
that mix rendered formulas with raw text. The new audit_math_rendering.py adds
per-step candidates and geometry inventory.

## First manual review targets

### Original-question formula coverage

| Article | Review target |
|---|---|
| shanghai-2024-geometry-jingan-q20 | Render |BD|=|AC| and slope ratio 1:2√2 in the original question |
| shanghai-2024-geometry-songjiang-q20 | Render ellipse equation, foci and rectangle/area notation in the original question |
| shanghai-2024-geometry-huangpu-q20 | Render both conics, focus labels, coordinates, slopes and the distance-product relation |
| jiading-2023-q20 | Render the three piecewise curve equations and branch restrictions in the original question |
| jiading-2023-q12 | Render the parabola equation and the moving-point/velocity conditions |
| jiading-2023-q14 | Render all four hyperbola equations in the original question |

### Solution-step formula coverage

| Article | Review target |
|---|---|
| jiading-2023-q20 | Seven steps: ellipse/semicircle parameterization, distance bounds, endpoint and range calculations |
| yangpu-2023-q06 | Four steps: dot product, projection formula, projected vector and perpendicular residual |
| yangpu-2023-q08 | Four steps: both hyperbola standard forms, asymptote slopes and eccentricities |
| jiading-2023-q12 | Three steps: time parameter, implicit differentiation and speed |
| jiading-2023-q14 | Three steps: axis orientation, asymptote ratios and option checks |
| derivative-classics-q06 through q10 | Each proof step needs its own formulas; a formula bank does not satisfy in-step coverage |

This list is a review queue, not permission to bulk-convert text without checking
the source. Preserve all original constraints and use the evidence file's page
locator. Where the source has no official worked solution, label the site's proof
as independent.

## Remediation gates

1. L0 — inventory: all registered article files and evidence records resolve.
2. L1 — formula placement: original question and each proof step contain MathML
   wherever the corresponding text has a mathematical relation.
3. L2 — MathML semantics: accessible names, correct mfrac/script arity, no MathML
   inside SVG, no visible LaTeX source.
4. L3 — source fidelity: compare each edited question with the rendered source PDF,
   including symbols, inequalities, coordinates, diagram labels and subparts.
5. L4 — mathematics: independently verify algebra, roots, domain, endpoints,
   degeneracies, vertical-line cases, equality conditions and final answers.
6. L5 — visualization: use one model for equations, SVG paths and labels; test
   point-on-curve, point-on-line, tangency, perpendicularity and numerical invariants.
7. L6 — browser: Chromium screenshots at 1440, 768, 390 and 360 px, keyboard
   formula scrolling, print and no-network fallback.

Only L0–L2 are machine-auditable in bulk. L3–L6 require actual source and rendering
evidence. Do not mark an item complete just because CI is green.
