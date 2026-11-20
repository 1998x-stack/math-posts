# Visual-first standard for math-posts

This is the presentation contract for every published mathematics article. The goal is a visual teaching experience, not a long text explanation with a decorative cover.

## 1. Visual hierarchy and scale

A reader should understand the mathematical object and the task before reading the proof.

- The first screen must show: title, a one-sentence plain-language task, a problem diagram, and 2–4 compact condition/target chips.
- Use a visual hierarchy: **problem scene → given/target → one idea → one transformation → one check**.
- Do not place a long paragraph directly below the H1. Keep lead text to one or two short sentences.
- Break explanatory prose into short blocks. As a practical target, a paragraph should usually stay under 55 Chinese characters; split longer reasoning into a visual, list, callout, or equation block. This is a readability target, not a reason to remove necessary proof.
- Prefer labels, arrows, number lines, tables, annotated graphs, and side-by-side comparisons over repeated prose.
- Use no more than 2–4 short lines of text inside a single SVG panel. Move detailed explanation into nearby HTML text and MathML.

## 2. Required visual storyboard

Each article marked `data-visual-first="true"` must contain:

1. **Problem visual** in `#overview`: the object, key known quantities, domain/region, and target.
2. **Reasoning visuals** inside `#solution`: at least two step-level diagrams. Each diagram must be placed next to the exact step it explains, not collected at the end.
3. **Conclusion visual** in `#answer`: mark the solution, extremum, root count, feasible region, or final geometric relation.
4. Every figure has a meaningful `<title>`, `<desc>`, `aria-label`, and a caption that states a checkable mathematical claim.

A single cover SVG duplicated into a Three.js fallback does not count as multiple visualizations. A decorative illustration without mathematical labels, constraints, or a verifiable claim does not count.

## 3. Math rendering contract

- Any substantive equation, inequality, coordinate tuple, function definition, interval, piecewise rule, or algebraic transformation must be rendered as native MathML, including inline formulas inside paragraphs and the original question.
- A short symbol such as (x), (n), or (P) may remain ordinary text when it is only a name. Expressions such as `f(x)=...`, `0≤x≤1`, `a²+b²`, or a coordinate tuple must not remain plain text.
- Inline math uses `<math class="math-inline" aria-label="...">...</math>`; display math uses the keyboard-focusable `.math-scroll` region defined in `math-typesetting.md`.
- Never use Unicode superscript/subscript as a substitute for real formula markup when it carries mathematical meaning.
- SVG labels may use compact plain text when MathML cannot be embedded in SVG, but the same equation must appear as MathML in adjacent HTML.
- Each article's inline formula audit must list any intentional text-only notation and why it is not a mathematical expression.

## 4. Step-level explanation

Each step should be a compact unit:
- **Action**: one mathematical operation.
- **Reason**: one concise sentence with the specific condition/theorem.
- **Equation**: the actual transformation rendered in MathML.
- **Visual**: a local SVG if the transformation changes a region, graph, point, vector, interval, count, or geometric relationship.
- **Check**: one boundary, sign, domain, equality, unit, or degeneracy check.

Do not add an SVG to every trivial arithmetic line. Visualize every conceptual change. If a step only simplifies arithmetic, keep it concise and do not force a diagram.

## 5. Diagram-specific rules

- **Functions**: axes, domains, branches, critical points, roots, levels and intervals must be labelled. For compositions, show the first mapping and second mapping separately.
- **Sequences**: distinguish the term (a_n), partial sum (S_n), and partial product (P_n). Use a discrete plot for integer (n), not a continuous curve presented as the actual sequence.
- **Solid geometry**: name vertices, show projection feet, dashed hidden edges, highlighted planes/lines, and provide a 2D proof diagram plus a 3D scene only when rotation adds real understanding.
- **Analytic geometry**: show axes, conic, fixed point, moving secant, intersections, midpoint, and allowed parameter range.
- **Optimization/application**: label units, piecewise boundaries, feasible intervals, candidate optima, and the final comparison.
- **Counting/probability**: show a tree, set partition, or inclusion/exclusion regions and label disjoint/overlapping cases.

## 6. Acceptance checks

For every visual-first pilot page:
- at least 4 meaningful figures total (problem, 2 reasoning, conclusion);
- at least 8 MathML expressions, including inline MathML in the original question and in step explanations;
- no substantive formula-like expression left as raw prose in the key teaching sections;
- every step has a concise reason; long paragraphs are split;
- no document-level horizontal overflow at 1440, 768, 390, and 360 px;
- MathML has the correct namespace and visible nonzero geometry in Chromium;
- diagrams remain readable at 360 px and in print;
- Three.js is optional and never counted as a replacement for the static SVG storyboard.

A pilot page is not promoted to the next batch until static validation and browser rendering checks both pass.
