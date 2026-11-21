# Analytic-geometry visual and formula audit

This reference applies to ellipse, hyperbola, parabola, circle, line, chord, tangent,
focus/directrix, vector, coordinate and locus problems. The goal is not a decorative
graph; it is to make the original mathematical object and every important deduction
inspectable.

## 1. Preserve the complete original question

Before writing a solution, create a source checklist from the rendered source page:

- Original wording, all subquestions, all options, point names, curve names and diagram labels.
- Every equation, inequality, interval, vector, slope, distance, angle and parameter restriction.
- Whether a line is vertical/horizontal, whether a point is excluded, and whether an endpoint is included.
- Source PDF page(s), transcription status and any missing/ambiguous glyphs.

Keep the source question intact. Do not silently normalize a strict inequality, add a
non-vertical-line assumption, rename a focus, or repair a suspected typo. Put editorial
explanations outside the original-question block. If a symbol cannot be verified from
the rendered source, preserve the uncertainty and keep the post in draft.

## 2. Render mathematics where it is used

Use semantic MathML in the original question and beside the corresponding reasoning step.

- Render the conic equation and its domain/branch restriction together.
- Render point coordinates, focus labels, slopes, vector components and line equations where they first appear.
- Render the discriminant, root product, chord length, tangent condition, distance product and parameter bounds beside the step that uses them.
- Do not move all formulas to a formula bank at the bottom. A formula bank is a recap, not a substitute for readable source text or derivation.
- Do not count MathML elsewhere on the page as coverage for a raw formula in a particular paragraph or list item.
- Preserve source notation and distinguish the official answer from an independently derived result.

## 3. Build the diagram from the same mathematical model

Create one authoritative geometry model containing:

- Conic coefficients and branch/domain restrictions.
- Coordinates of the centre, vertices, foci, directrix, fixed points and moving points.
- Line parameters, slopes, intersection points and tangent directions.
- Distances, angles, chord endpoints, vector components and feasible parameter ranges.

Generate the SVG paths, point markers, labels and numeric annotations from that model.
Avoid separately hardcoding SVG coordinates that can drift away from the equations in
the article.

For every diagram, record explicit assertions. Examples:

- Point-on-conic residual: abs(F(x, y)) <= tolerance.
- Point-on-line residual: abs(a*x + b*y + c) <= tolerance.
- Focus distance and directrix distance agree for a parabola.
- A tangent line passes through its contact point and has the derivative/implicit tangent slope.
- A chord's endpoints satisfy the conic equation and the line equation.
- A claimed right angle has dot product zero.
- A claimed constant is unchanged for multiple legal parameter samples.
- A claimed maximum/minimum includes endpoint, interior and degenerate cases.

Use scale-aware tolerances and record exact expected values. Numerical assertions detect
drawing/model drift; they do not replace an algebraic proof.

## 4. Mandatory special-case review

Before publishing a coordinate-geometry solution, check:

1. Vertical lines (x = constant) separately from finite-slope lines.
2. Horizontal lines, zero slopes and undefined slopes.
3. Tangency versus secancy; repeated roots versus two distinct intersections.
4. Points at vertices, foci, endpoints and excluded points.
5. Empty, singleton and full parameter ranges.
6. Degenerate conics, zero denominators and invalid square-root branches.
7. Necessary versus sufficient conditions when a coordinate manipulation divides by a variable.
8. Whether a squared equation introduced extraneous signs or roots.

A generic slope parameterization is not complete if it silently excludes vertical lines.

## 5. Diagram selection and accessible output

Prefer an accurate static SVG for a two-dimensional conic. Include axes, scale or units,
curve names, fixed points, moving points, focal points, lines/chords/tangents and a
caption explaining the mathematical question. Use a parameter control only when it
changes a real mathematical object and its allowed domain is explicit.

Use Three.js only when spatial rotation materially helps. Keep a static SVG fallback,
and do not describe a 2D coordinate problem as requiring 3D.

Every inline SVG needs title, desc, a non-empty caption and readable labels. Check that
points and labels remain inside the viewBox. At mobile widths, horizontal scrolling
belongs to the figure rather than the entire document.

## 6. Continuous repository audit

Run both audits on every pull request and main push, plus a scheduled weekly scan:

- python scripts/audit_teaching_quality.py --output _audit/teaching-quality.json
- python scripts/audit_math_rendering.py --output _audit/math-rendering.json

The rendering audit reports candidates per original question and per individual
solution step, MathML accessibility/structure, and analytic-geometry SVG inventory.
Candidates are review leads, not confirmed errors. Compare the source PDF and verify
the mathematics before changing content. The audit deliberately does not auto-rewrite
HTML or infer a missing formula from a title or filename.

For each remediation batch, keep a reviewed checklist with source page, exact original
expression, MathML location, proof step, diagram assertion, special cases, browser
screenshot and final status (passed, failed, not verified).
