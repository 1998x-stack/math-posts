# AGENTS.md — math-posts

本项目继承 xm-posts 的教学式 HTML、SVG、知识地图、GitHub Pages 工程框架，并将目标替换为**数学题目理解与可验证解题**。在任何冲突中：数学正确 > 题源忠实 > 学习体验 > 视觉偏好。

- **目录**：`posts/<category>/<slug>/index.html` + `assets/*.svg` + `evidence.json`。
- **事实源**：`content/categories.json`, `content/posts.json`, `content/reading_paths.json`；新试卷的来源说明见 `content/source-notes.md`。原卷由用户在本对话上传；禁止伪造公开 PDF 地址。
- **Skill**：`skills/math-visual-posts/` 是唯一版本；镜像在 `.claude/.pi/.agent/.opencode`，必须字节一致。修改后运行 `python scripts/sync_skills.py`。
- **数学题**：每题保留原题、选项、小问、标准答案、逐步推导、易错点、来源 PDF 页码。原解和原创补充明确区分。疑似误识别设 draft。
- **SVG/Three.js**：每题封面必须是原题专属概念图；Three.js 只用于真实三维结构，有旋转缩放/控件/真实数值/SVG 回退，锁版本，不假称全离线。
- **站点**：只公开 `status: published`，生成产物 `_site/` 不提交。PR 测试通过才合并，main Pages 成功并实际访问到页面才称部署成功。
- **QA**：检查全部链接、HTML 一 H1、响应式、MathML 可读、SVG 可读、交互可用、无横向溢出及无 console 错误。禁网下 Three.js 必须有静态回退。

本次题源：《2021 年上海市建平中学高考冲刺模拟试卷 3（解析版）》，21 题（填空 12、选择 4、解答 5）。
