# math-posts

> **从一道题的直觉，走到可核对的数学推导。**

数学题解网站，基于 [xm-posts](https://github.com/1998x-stack/xm-posts) 的教学 Skill、SVG、文章组织与 GitHub Pages 技术体系建设，加入 Three.js 空间场景。

[网站](https://1998x-stack.github.io/math-posts/) · [高中数学知识地图](https://1998x-stack.github.io/math-posts/topics/) · [按题型浏览](https://1998x-stack.github.io/math-posts/question-types/) · [归档](https://1998x-stack.github.io/math-posts/archive/) · [RSS](https://1998x-stack.github.io/math-posts/feed.xml)

首批材料：用户上传的**《2021 年上海市建平中学高考冲刺模拟试卷 3（解析版）》**，共 21 题——12 道填空、4 道选择、5 道解答。Q01–Q19、Q21 已发布，**Q20 已纠正上一轮判别式算术错误，闭区间上界 1 与仓库记录一致；但是否允许切线端点仍待原卷复核，因此保持 draft**。Q21 已补上双峰复合函数的精确 SVG 图、水平线根数交互和二周期点独立验算。第二批材料为用户上传的**《2024届高三二模数学汇编：解析几何》**，已按原 PDF 全部16个地区顺序完成逐题转写与建模：前10道为浦东、嘉定、长宁、闵行、虹口、静安、普陀、徐汇、宝山、松江；最后6道为青浦、金山、崇明、黄浦、杨浦、奉贤。其中奉贤区第（3）问原卷条件不足，存在合法反例，暂保留草稿状态，其余十五道已发布。原 PDF 均不在公开仓库；题源页码、转写状态和独立验算写在各篇 `evidence.json`。 新增《第 12 周高三数学课堂练习》照片第 1–5 题，提供 MathML 可访问公式、专属 SVG 图和独立核验；手写答案不作为官方解析。

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
