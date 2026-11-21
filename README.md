# math-posts

> **从一道题的直觉，走到可核对的数学推导。**

数学题解网站，基于 [xm-posts](https://github.com/1998x-stack/xm-posts) 的教学 Skill、SVG、文章组织与 GitHub Pages 技术体系建设，加入 Three.js 空间场景。

[网站](https://1998x-stack.github.io/math-posts/) · [高中数学知识地图](https://1998x-stack.github.io/math-posts/topics/) · [按题型浏览](https://1998x-stack.github.io/math-posts/question-types/) · [归档](https://1998x-stack.github.io/math-posts/archive/) · [RSS](https://1998x-stack.github.io/math-posts/feed.xml)

首批材料：用户上传的**《2021 年上海市建平中学高考冲刺模拟试卷 3（解析版）》**，共 21 题——12 道填空、4 道选择、5 道解答。Q01–Q19、Q21 已发布，**Q20 已纠正上一轮判别式算术错误，闭区间上界 1 与仓库记录一致；但是否允许切线端点仍待原卷复核，因此保持 draft**。Q21 已补上双峰复合函数的精确 SVG 图、水平线根数交互和二周期点独立验算。第二批材料为用户上传的**《2024届高三二模数学汇编：解析几何》**，已按原 PDF 全部16个地区顺序完成逐题转写与建模：前10道为浦东、嘉定、长宁、闵行、虹口、静安、普陀、徐汇、宝山、松江；最后6道为青浦、金山、崇明、黄浦、杨浦、奉贤。其中奉贤区第（3）问原卷条件不足，存在合法反例，暂保留草稿状态，其余十五道已发布。原 PDF 均不在公开仓库；题源页码、转写状态和独立验算写在各篇 `evidence.json`。 新增《第 12 周高三数学课堂练习》照片第 1–5 题，提供 MathML 可访问公式、专属 SVG 图和独立核验；手写答案不作为官方解析。

新增 **《2023 届上海市崇明区高三一模数学试卷（含答案）》第 1–5 题**，涵盖集合、分式不等式、复数、对数与等比数列。原题与官方答案分别在用户上传 PDF 第 1、7 页；独立校验与 SVG 可视化详见各篇题解和 `content/source-notes.md`。

第三批材料：用户上传的**《2023 届上海市虹口区高三一模数学试卷》**（2022.12），本次先完成前五道填空题，题干位于 PDF 第 1 页，官方答案表位于 PDF 第 7 页；官方只提供答案表，文章推导均标注为独立核验。题源页码和答案边界见 `content/source-notes.md` 与各篇 `evidence.json`。

## 仓库结构

`skills/math-visual-posts/` 是 canonical 数学题解 Skill（PDF 校对、MathML、SVG、Three.js、浏览器 QA）。`posts/` 是逐题 Post；`content/` 定义试卷题型、七大领域知识地图（先修关系、难度、能力目标与例题映射）、发布状态和阅读路径；`scripts/` 生成静态站点；`site/assets/` 承载 CSS 与 JS。

## 本地运行

```bash
pip install -r requirements-dev.txt
python scripts/sync_skills.py --check
python scripts/build_site.py
python scripts/validate_site.py
python -m pytest -q
python -m http.server 8000 --directory _site
```

GitHub Actions 在 PR 上只验证，main 分支部署 Pages；确认成功之前不宣称已上线。第 4、5、13、17 题涉及空间几何，计划或已实现 Three.js，二维问题保留轻量 SVG。

## 反馈迭代

后续根据你的反馈调整 canonical Skill 与模板，再同步四套 Agent 镜像。不维护互相冲突的多套规范。

## 第六批：导数及其应用

新增《导数及其应用大题（解析版）》62页题源的前五道“百强名校最新经典试题”：衡水中学、华南师大附中、东北育才、山东省实验中学、南京大学附属中学。对应 PDF 第2–7页，每题配独立 SVG、MathML、逐步证明和 evidence.json。该 PDF 自带参考答案，本仓库额外推导必须明确区别。下一批顺序为原卷第6–10题。

## 第七批：第 12 周课堂练习第 6–10 题

延续前五题，现按纸质照片第1页继续完成第6–10道填空题（圆锥、奇偶函数、对数韦达、锐角参数范围、相同偶数数码计数）。每题含原生 MathML、题目专属 SVG、独立证据记录与验算；第10题按「相同偶数」而非任意相同数字解释，答案117。照片中的手写答案不是官方答案。

## 第七批：上海松江区2023届高三一模

从用户上传的《138-2023松江一模.pdf》按题号 **one by one** 完成第1–10题：10篇独立HTML、SVG、evidence.json；其中8篇可发布，第8、9题因原PDF关键比较符缺字而暂为draft。PDF第1页是题目，第7页有参考答案；每篇均区分参考答案与独立推导。记录在 [题源说明](content/source-notes.md)。


新增题源：**《上海市杨浦区 2023 届高三一模数学试卷》**（2022.12），首批已转换前 5 道填空题。原题来自 PDF 第 1 页，答案核对 PDF 第 8 页；官方参考答案只列结果，逐步推导为独立验算。题源页码、答案来源与说明记录在 `content/source-notes.md` 及每篇 `evidence.json`。


## 题库导航升级：按知识点、试卷、题型与解题方法

- [按试卷浏览](https://1998x-stack.github.io/math-posts/papers/)：按学校、地区、年份和原卷题号阅读；支持整卷、地区题目摘录、课堂练习与专题题集。
- [知识地图](https://1998x-stack.github.io/math-posts/topics/)：保持七大知识领域、先修依赖与学习路径。
- [首页多维筛选](https://1998x-stack.github.io/math-posts/#discover)：组合使用答题形式、知识点、试卷、解题方法及图解方式，支持链接分享查询参数，例如 `?concept=vector&category=fill-in`。
- 每道题只维护一个规范 HTML URL；试卷页和知识索引均引用它，不复制题目内容。

### 内容数据

| 文件 | 职责 |
|---|---|
| `content/posts.json` | 文章身份、原卷题号、`paper_id`、`facets`、发布状态；保持旧 `tags` 向后兼容 |
| `content/papers.json` | 每张试卷/练习/题集的稳定 ID、来源文档 ID、学校/地区、年份和已知题量 |
| `content/taxonomy.json` | 可检索的规范化概念/方法/图示标签和中文别名 |
| `content/knowledge-map.json` | 知识领域、先修依赖、难度和已发布题目映射 |
| `posts/**/evidence.json` | 真实原题与答案的来源、页码、核对边界、异常说明 |

一次来源 PDF 可能包含多套地区题，必须区分**源文档 source_id** 与 **试卷 paper_id**。例如 2024 上海二模解析几何汇编中的各区第 20 题，各自归属单独的地区试卷摘录，不把它们错误排列成同一套试卷的第 1 至第 16 题。未知总题数使用 null；草稿不提供公开文章链接。

### 教学与可视化规范

以后新题按“题意导读 → 忠实原题 → 条件标注 → 思路地图 → 每一步的目标/理由/计算/检查 → 真实 SVG 或必要的三维 → 独立复核 → 方法迁移”建设。每题仍要求完整 MathML；视觉效果不能替代代数证明。

详细 Reference：
- [学生视角逐步解题](skills/math-visual-posts/references/student-solution-design.md)
- [20 类数学问题可视化设计](skills/math-visual-posts/references/visualization-by-problem-type.md)
- [多维标签体系](skills/math-visual-posts/references/taxonomy-and-tags.md)
- [PDF / 试卷 / 题目 Schema](skills/math-visual-posts/references/exam-provenance-schema.md)

初始标签由现有知识地图、明确的题目标签与来源结构迁移；对尚未逐篇核对的解题方法和图示形式，保持空列表，不为了筛选数量而误标。未来批次必须执行逐题人工审查和浏览器检查。
