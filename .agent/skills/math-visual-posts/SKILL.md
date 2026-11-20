---
name: math-visual-posts
description: 把数学 PDF 原题转为可溯源、可读、可交互的数学 Post。包含原卷核对、MathML、SVG 和 Three.js 空间场景的制作与校验。
---

# Math Visual Posts

本 Skill 基于 [xm-posts](https://github.com/1998x-stack/xm-posts) 的 olah-style-paper-posts 改造：**数学真实 > 原题忠实 > 教学可懂 > 视觉新奇**。服务高中生、大学生及数学自学者。每次反馈先修改本规范，再运行 sync_skills 镜像同步。

## 输入 / 产物

输入是用户上传 PDF（含图形与解析）或独立数学题。输出为 `posts/<category>/<slug>/index.html`、`assets/*.svg`（独特题目封面）、`evidence.json`、必要时的 Three.js 场景，及 `content/posts.json` 中的分类、题型、主题、题源页码和发表状态。不要把用户上传 PDF 冒充有公开链接的论文。

## Gate 0：浏览代码与试卷

读取仓库 `AGENTS.md`、分类注册表、页面构建器、此 Skill 与现有题解；浏览 PDF 原始页渲染，识别选择、填空与解答每一道题及跨页解析。图片里的上标、根号、向量、区间、`<` 与 `≤` 不能仅凭文本提取器推断。详见 [PDF 提取](references/pdf-question-extraction.md)。

## Gate 1：数学内容校对

完整记录题干、题目选项、所有小问、条件、单位、原解、正确结果和 PDF 页码。独立验算，不偷换题设；如果原解有疑似笔误，在证据中标注“原题原样 / 独立核验 / 编辑勘误”。不能核实的题一律留 `draft`，不写 `published`。把问题的可解性、定义域、取等条件、分类边界检查清楚。

## Gate 2：循序渐进的题解

固定阅读路径：**原题 → 关键观察 → 思路转换 → 每步推导 → 原创图解 / 交互实验 → 答案 → 易错点 → 相关阅读**。所有步骤都有解释；不能只贴答案、宽泛概念总结或没有数学关系的装饰。可扩展为专题长文，但题目页面仍保持独立可引用的 URL。

## Gate 3：数学排版与图解

数学公式以语义正确的 **MathML Core** 为优先，提供屏幕阅读器名称和小屏可聚焦的横向公式区；遵循 [数学排版](references/math-typesetting.md)。关键图形以**可编辑的独立 SVG** 创作并作封面；坐标轴、交点、面积、梯度、向量必须与推导一致。参考 [SVG 制作](references/svg-production.md)。每篇 cover 特定于本题，禁止重复通用“observe / derive / verify”插画。

## Gate 4：Three.js 专项规则

仅当**真正三维结构**能帮助理解时使用 Three.js：正方体动点、三棱锥、球、异面直线等。纯函数和组合题默认 SVG。Three.js 场景必须具有数学坐标、正确几何体、旋转/缩放/重置、可键盘控制的参数、实时数值与推导一致，以及禁网/无 WebGL SVG 回退。锁版本并标明运行依赖，不得称 CDN 模式完全离线。完整见 [Three.js](references/threejs-production.md)。

## Gate 5：可验证的教育交互

参数域合法，初始状态传达核心内容，极值、边界、共线、退化等状态要有正确处理；按钮、滑块、ARIA、触屏与键盘、reduced-motion、打印样式齐备。交互不是玩具，必须能验证题解中的一个论断。

## Gate 6：证据及质量闸门

`evidence.json` 至少有 `source.title`、`source.question`、`source.pages`、`transcription.status`、`answer.official` 与独立校对说明。所有数学事实来自原卷或明确标注的原创推导。

运行：
```bash
python -m pip install -r requirements-dev.txt
python scripts/sync_skills.py --check
python scripts/build_site.py
python scripts/validate_site.py
python -m pytest -q
```
浏览器至少检查 1440 / 768 / 390 / 360 px、HTML/SVG/MathML、键盘行为、无横溢、Three.js 加载与无 WebGL 回退；无法执行的检查必须明确记录为“未验证”。

## Gate 7：发布与反馈

制作 topic branch + PR，审查 diff，CI 通过后才合并；再检查 GitHub Pages 实际 workflow 与页面 URL。用户的下一轮反馈应沉淀为 canonical `skills/math-visual-posts/`；四个 `.claude/.pi/.agent/.opencode` 镜像仅由 `scripts/sync_skills.py` 更新。

## 参考路线

- [pdf-question-extraction.md](references/pdf-question-extraction.md)
- [threejs-production.md](references/threejs-production.md)
- [math-typesetting.md](references/math-typesetting.md)
- [svg-production.md](references/svg-production.md)
- [browser-qa.md](references/browser-qa.md)
- [publishing.md](references/publishing.md)
