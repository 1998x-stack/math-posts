# SVG pipeline: storyboard → design → extract → render → verify

## Construct

1. Make a state/edge list (e.g. input → projection Q/K/V → score → softmax → values) **before** drawing.
2. Draw shapes in model execution order; separate arrows for data flow from labels for tensors. Use `stroke-dasharray` only for an explicitly described secondary/gradient path.
3. For stacked architecture, distinguish repeated blocks and stage count; for masked attention show which entries are blocked, not just a colored matrix.
4. Each SVG must have `xmlns`, `viewBox`, `<title>`, `<desc>` and unique IDs; use `role="img" aria-labelledby` when inline.
5. Minimum label ~13px at nominal width; use native sans fonts with Chinese fallbacks. Treat color as redundant with labels/dashes.
6. Use color semantics consistently **within** a paper; do not claim identical colors across very different scientific domains.
7. Captions should describe a verifiable statement about the path, not simply 'architecture overview'.

## Extraction

Run `extract_svg.py` against **rendered HTML** with Playwright. It clones each SVG, snapshots visible CSS computed style fields (fill, stroke, font, opacity, etc.) onto the SVG elements, ensures `xmlns/viewBox`, cleans unsafe script/event attributes, and writes independent XML files. This retains labels that were previously styled only via article CSS. It does not download external assets; CSS background images and remote font dependencies must be eliminated upstream. Names prefer `<svg data-export="filename">`, otherwise stable section/figure ID.

```bash
python skills/math-visual-posts/scripts/extract_svg.py posts/architectures/resnet/index.html --out /tmp/resnet-svg
```

## Verify

- Parse as XML, confirm width/height from viewBox, no missing assets, and unique IDs.
- Open standalone SVG in a browser and capture screenshot; compare to the inline figure (cropping might differ because CSS dimensions differ).
- Inspect all lines and arrows visually: joins, topology, direction, equation symbols and labels; no visible overprint/clipping.
- Maintain a manifest mapping filename → figure number → concept → source verification.
- Do not blindly scrape or publish third-party paper SVGs: check license and permission first.

## Two anti-patterns

- Arrows that merely decorate a box: no scientific connection to described operation.
- “Perfect-looking” shapes with wrong semantics (e.g. residual skip starting after the transform, or cross-attention K/V originating in Decoder).

## 数学图示专项：坐标真值优先于视觉装饰

1. 写下具体坐标或参数方程，明确 `world_to_svg(x,y)` 对应的缩放、原点与纵轴翻转。图例和刻度必须与所用的同一坐标映射一致。
2. 对椭圆/抛物线/双曲线/圆，验证每一个标注点确实满足相应方程；焦点、渐近线、切线、弦中点、面积比或距离最值需要单独代数核验。
3. 画反例时明确“草稿／反例／原条件不足”，避免 SVG 示意图看起来像对有争议原命题的证明。
4. 移动端实际保证标签可读：在窄屏滚动 720px 左右的内在图示宽度，而不是把文字缩成 6px；焦点可达，打印恢复适页缩放。
5. 每篇文章的 inline SVG 与独立 cover.svg 都要自带 `title`、`desc`，且图注解释可检验的数学结论。不能只写“函数图像”“示意图”。
6. 将 `scripts/audit_svg.py --strict-desc` 和 Chromium 图形检查纳入 CI。对浏览器报告的 label clipping 候选复核，而不依赖固定正则判定有无视觉重叠。
