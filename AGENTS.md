# AGENTS.md — math-posts

本项目继承 xm-posts 的教学式 HTML、SVG、知识地图、GitHub Pages 工程框架，并将目标替换为**数学题目理解与可验证解题**。在任何冲突中：数学正确 > 题源忠实 > 学习体验 > 视觉偏好。

- **目录**：`posts/<category>/<slug>/index.html` + `assets/*.svg` + `evidence.json`。
- **事实源**：`content/categories.json`（试卷题型索引）, `content/knowledge-map.json`（学科知识地图）, `content/posts.json`, `content/reading_paths.json`；新试卷的来源说明见 `content/source-notes.md`。原卷由用户在本对话上传；禁止伪造公开 PDF 地址。
- **Skill**：`skills/math-visual-posts/` 是唯一版本；镜像在 `.claude/.pi/.agent/.opencode`，必须字节一致。修改后运行 `python scripts/sync_skills.py`。
- **数学题**：每题保留原题、选项、小问、标准答案、逐步推导、易错点、来源 PDF 页码。原解和原创补充明确区分。疑似误识别设 draft。
- **SVG/Three.js**：每题封面必须是原题专属概念图；Three.js 只用于真实三维结构，有旋转缩放/控件/真实数值/SVG 回退，锁版本，不假称全离线。
- **知识地图**：`/topics/` 以学科知识体系为主轴；七大领域、知识节点、先修依赖、1–5 难度、能力目标和关联文章均来自 `content/knowledge-map.json`。`/question-types/` 单独承载填空/选择/解答题型索引。每篇已发布文章必须关联至少一个知识节点，先修关系不得成环。
- **站点**：只公开 `status: published`，生成产物 `_site/` 不提交。PR 测试通过才合并，main Pages 成功并实际访问到页面才称部署成功。
- **QA**：检查全部链接、HTML 一 H1、响应式、MathML 可读、SVG 可读、交互可用、无横向溢出及无 console 错误。禁网下 Three.js 必须有静态回退。

现有题源包括：《2021 年上海市建平中学高考冲刺模拟试卷 3（解析版）》，21 题（填空 12、选择 4、解答 5）；以及《2024届高三二模数学汇编：解析几何》，按地区顺序分批转换。已完成前十区：浦东、嘉定、长宁、闵行、虹口、静安、普陀、徐汇、宝山、松江。2024 PDF 未附官方答案，必须把独立推导与官方答案区分记录；静安开放式设计必须标明设计假设和非唯一性。
