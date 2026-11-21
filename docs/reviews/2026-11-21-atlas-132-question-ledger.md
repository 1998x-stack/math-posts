# math-posts 132 道题逐项元数据与来源审查台账（2026-11-21）

> 本台账是**每道题的身份、来源关联、文件完整性和索引分类**审查，不等于对 132 道题的数学推导与 PDF 图像逐页独立证明。不能将“结构已核对”写成“数学内容全量确认”。

## 1. 基线与审查等级

- 基线：当前 main 快照 commit `2f0385383a63a07b8291362f8a97f746e6277eb8`；旧 PR #29 仅覆盖 82 道，本审查从 main 原封不动读取原有题目数据并增量补 `paper_id` / `facets`。
- 本次逐题覆盖：**132** 条记录，**127** 道已发布，**5** 道 draft，**25** 个试卷/摘录/题集身份。
- 检查范围：每题 slug、来源归属、原题号和唯一性、题型、source_pages 字段有效性、知识地图关联、三个规范化检索 facet、文章 HTML、evidence.json 与 cover.svg 文件存在性。
- 完整性核验：132/132 条均具有 HTML、evidence.json、SVG 和有效元数据。127 道已发布题均映射知识节点；5 道草稿未进入已发布知识地图符合预期。异常条数：0。
- **QA 等级**：L1 = 仓库路径与结构；L2 = 实际静态构建/浏览器渲染；L3 = 由原始 PDF 渲染逐条检查题目数学符号、题干和答案；L4 = 独立证明数学推导与可视化断言。本台账逐题是 L1；L2 由 CI 另行执行；L3/L4 尚未覆盖全部题目。

## 2. 不应合并的隐患（逐项审查结论）

1. **旧分支污染风险 P0**：#29 的 `content/posts.json` 只有 82 条，当前 main 有 132 条，直接合并旧文件可能覆盖新增 50 道题。新审查分支以 main 为事实源重建。
2. **并行改动冲突 P0**：#13 MathML 大面积改写、#26 知识分类/SVG QA 均在未合并 PR 上，且已有冲突；不直接覆盖彼此的 SVG、证明或 Skill。
3. **来源元数据 P1**：2024 二模汇编对应 16 个地区单题摘录，一个 source_id，不可将它们按 1–16 编成同一张试卷。
4. **草稿隔离 P1**：建平 Q20、奉贤 Q20、松江 Q08/Q09/Q20 暂未发布。公开 sitemap 和试卷详情不得包含 draft 文章链接；纯 draft 的奉贤试卷摘录不产生对外路由。
5. **符号完整性 P1**：松江 Q16 的原 PDF 分段比较符缺失，目前已发布是基于左右分段逻辑的复原，不是直接辨认原卷；保留风险说明，待清晰源卷核对。
6. **数学语义 P1**：黄浦 2024 二模 Q20 椭圆焦点与双曲线顶点重合，不是两曲线共焦；本次复审从 #26 复用数学语义修补，仍需源 PDF 与图形对象逐点复核。
7. **来源答案 P1**：松江 Q19 原卷答案只写桥长 120 米，原题也要求谷深，独立验算谷深为 160 米；不能替换官方答案或抹除来源缺项。
8. **前半卷缺口 P2**：嘉定 2023 一模当前仅登记 Q11–Q20；原卷 Q1–Q10 并不在 main 的公开结构内。不能因为已有后半卷就声称全卷已上线。
9. **图解标签不足 P2**：为了防止“有一张封面 SVG 就冒充已做完整图解”，本次 method/visual 标签保守录入；仍需逐题检查图形断言后补充。
10. **学生步骤迁移 P2**：原有题解并未全部采用新 stepper。交互示例是参考实现，不代表 132 道现有题已经完成交互重构。

## 3. 全量逐卷逐题记录

### 2021 年上海市建平中学高考冲刺模拟试卷 3

- 记录 ID：`jianping-2021-mock-03`；类型：学校/地区考试；已发布 20 / 已登记 21；核实原卷总题量：21。

| 原题号 | 文章 | 答题形式 | PDF 记录页 | 知识概念 | 方法标签 | 可视化标签 | 当前状态 | 审查结论 / 后续动作 |
|---:|---|---|---|---|---|---|---|---|
| 1 | [jianping-2021-q01](../../posts/fill-in/jianping-2021-q01/index.html) | 填空 | 1 | 函数、三角函数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 2 | [jianping-2021-q02](../../posts/fill-in/jianping-2021-q02/index.html) | 填空 | 1,2 | 解析几何 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 3 | [jianping-2021-q03](../../posts/fill-in/jianping-2021-q03/index.html) | 填空 | 2,3 | 函数、不等式、最值与优化、数学思想与证明 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 4 | [jianping-2021-q04](../../posts/fill-in/jianping-2021-q04/index.html) | 填空 | 3,4 | 立体几何、向量 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 5 | [jianping-2021-q05](../../posts/fill-in/jianping-2021-q05/index.html) | 填空 | 4,5 | 立体几何 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 6 | [jianping-2021-q06](../../posts/fill-in/jianping-2021-q06/index.html) | 填空 | 5,6 | 数列 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 7 | [jianping-2021-q07](../../posts/fill-in/jianping-2021-q07/index.html) | 填空 | 6 | 组合计数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 8 | [jianping-2021-q08](../../posts/fill-in/jianping-2021-q08/index.html) | 填空 | 6,7 | 函数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 9 | [jianping-2021-q09](../../posts/fill-in/jianping-2021-q09/index.html) | 填空 | 8 | 组合计数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 10 | [jianping-2021-q10](../../posts/fill-in/jianping-2021-q10/index.html) | 填空 | 9 | 数列 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 11 | [jianping-2021-q11](../../posts/fill-in/jianping-2021-q11/index.html) | 填空 | 9,10 | 三角函数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 12 | [jianping-2021-q12](../../posts/fill-in/jianping-2021-q12/index.html) | 填空 | 11,12 | 数列、三角函数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 13 | [jianping-2021-q13](../../posts/multiple-choice/jianping-2021-q13/index.html) | 选择 | 12,13 | 解析几何、圆锥曲线、数学思想与证明、立体几何、向量 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 14 | [jianping-2021-q14](../../posts/multiple-choice/jianping-2021-q14/index.html) | 选择 | 13 | 数列 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 15 | [jianping-2021-q15](../../posts/multiple-choice/jianping-2021-q15/index.html) | 选择 | 14 | 解析几何、圆锥曲线 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 16 | [jianping-2021-q16](../../posts/multiple-choice/jianping-2021-q16/index.html) | 选择 | 14,15 | 解析几何、圆锥曲线 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 17 | [jianping-2021-q17](../../posts/worked-solutions/jianping-2021-q17/index.html) | 解答 | 15,16,17 | 立体几何、向量 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 18 | [jianping-2021-q18](../../posts/worked-solutions/jianping-2021-q18/index.html) | 解答 | 17,18,19 | 最值与优化 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 19 | [jianping-2021-q19](../../posts/worked-solutions/jianping-2021-q19/index.html) | 解答 | 19,20 | 最值与优化 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 20 | [jianping-2021-q20](../../posts/worked-solutions/jianping-2021-q20/index.html) | 解答 | 20,21,22,23 | 解析几何、圆锥曲线 | — | 待逐题图形审查 | 草稿 | 需核查题源，草稿不公开 |
| 21 | [jianping-2021-q21](../../posts/worked-solutions/jianping-2021-q21/index.html) | 解答 | 23,24,25 | 函数、数学思想与证明 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |

### 第 12 周高三数学课堂练习

- 记录 ID：`week12-gaosan-worksheet`；类型：课堂练习；已发布 15 / 已登记 15；原卷总题量未核实。

| 原题号 | 文章 | 答题形式 | PDF 记录页 | 知识概念 | 方法标签 | 可视化标签 | 当前状态 | 审查结论 / 后续动作 |
|---:|---|---|---|---|---|---|---|---|
| 1 | [week12-gaosan-q01](../../posts/fill-in/week12-gaosan-q01/index.html) | 填空 | 1 | 不等式 | — | 数轴与区间 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 2 | [week12-gaosan-q02](../../posts/fill-in/week12-gaosan-q02/index.html) | 填空 | 1 | 复数 | — | 复平面 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 3 | [week12-gaosan-q03](../../posts/fill-in/week12-gaosan-q03/index.html) | 填空 | 1 | 不等式、集合与区间 | — | 数轴与区间 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 4 | [week12-gaosan-q04](../../posts/fill-in/week12-gaosan-q04/index.html) | 填空 | 1 | 组合计数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 5 | [week12-gaosan-q05](../../posts/fill-in/week12-gaosan-q05/index.html) | 填空 | 1 | 数列 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 6 | [week12-gaosan-q06](../../posts/fill-in/week12-gaosan-q06/index.html) | 填空 | 1 | 立体几何 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 7 | [week12-gaosan-q07](../../posts/fill-in/week12-gaosan-q07/index.html) | 填空 | 1 | 函数 | — | 函数曲线 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 8 | [week12-gaosan-q08](../../posts/fill-in/week12-gaosan-q08/index.html) | 填空 | 1 | 函数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 9 | [week12-gaosan-q09](../../posts/fill-in/week12-gaosan-q09/index.html) | 填空 | 1 | 解析几何、不等式、数学思想与证明、向量 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 10 | [week12-gaosan-q10](../../posts/fill-in/week12-gaosan-q10/index.html) | 填空 | 1 | 组合计数 | 分类讨论 | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 11 | [week12-gaosan-q11](../../posts/fill-in/week12-gaosan-q11/index.html) | 填空 | 1 | 解析几何、最值与优化、数学思想与证明、向量 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 12 | [week12-gaosan-q12](../../posts/fill-in/week12-gaosan-q12/index.html) | 填空 | 1 | 数列、集合与区间、三角函数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 13 | [week12-gaosan-q13](../../posts/multiple-choice/week12-gaosan-q13/index.html) | 选择 | 1 | 解析几何、圆锥曲线 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 14 | [week12-gaosan-q14](../../posts/multiple-choice/week12-gaosan-q14/index.html) | 选择 | 1 | 解析几何、向量 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 15 | [week12-gaosan-q15](../../posts/multiple-choice/week12-gaosan-q15/index.html) | 选择 | 2 | 导数、不等式、最值与优化 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |

### 导数及其应用大题（解析版）

- 记录 ID：`derivative-classics-collection`；类型：专题题集；已发布 10 / 已登记 10；原卷总题量未核实。

| 原题号 | 文章 | 答题形式 | PDF 记录页 | 知识概念 | 方法标签 | 可视化标签 | 当前状态 | 审查结论 / 后续动作 |
|---:|---|---|---|---|---|---|---|---|
| 1 | [derivative-classics-q01](../../posts/worked-solutions/derivative-classics-q01/index.html) | 解答 | 2,3 | 导数、函数、最值与优化、数学思想与证明 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 2 | [derivative-classics-q02](../../posts/worked-solutions/derivative-classics-q02/index.html) | 解答 | 3,4,5 | 导数、函数、不等式、三角函数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 3 | [derivative-classics-q03](../../posts/worked-solutions/derivative-classics-q03/index.html) | 解答 | 5,6 | 导数、函数、不等式 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 4 | [derivative-classics-q04](../../posts/worked-solutions/derivative-classics-q04/index.html) | 解答 | 6 | 导数、函数、数学思想与证明 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 5 | [derivative-classics-q05](../../posts/worked-solutions/derivative-classics-q05/index.html) | 解答 | 6,7 | 导数、函数、不等式 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 6 | [derivative-classics-q06](../../posts/worked-solutions/derivative-classics-q06/index.html) | 解答 | 7,8,9 | 导数、函数、不等式 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 7 | [derivative-classics-q07](../../posts/worked-solutions/derivative-classics-q07/index.html) | 解答 | 9,10 | 导数、函数、不等式、数学思想与证明 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 8 | [derivative-classics-q08](../../posts/worked-solutions/derivative-classics-q08/index.html) | 解答 | 10,11 | 导数、函数、不等式 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 9 | [derivative-classics-q09](../../posts/worked-solutions/derivative-classics-q09/index.html) | 解答 | 11,12,13 | 导数、函数、不等式、三角函数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 10 | [derivative-classics-q10](../../posts/worked-solutions/derivative-classics-q10/index.html) | 解答 | 13,14 | 导数、函数、不等式、数学思想与证明 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |

### 2023 届上海市崇明区高三一模数学试卷

- 记录 ID：`chongming-2023-mock`；类型：学校/地区考试；已发布 10 / 已登记 10；原卷总题量未核实。

| 原题号 | 文章 | 答题形式 | PDF 记录页 | 知识概念 | 方法标签 | 可视化标签 | 当前状态 | 审查结论 / 后续动作 |
|---:|---|---|---|---|---|---|---|---|
| 1 | [chongming-2023-q01](../../posts/fill-in/chongming-2023-q01/index.html) | 填空 | 1 | 集合与区间 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 2 | [chongming-2023-q02](../../posts/fill-in/chongming-2023-q02/index.html) | 填空 | 1 | 不等式 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 3 | [chongming-2023-q03](../../posts/fill-in/chongming-2023-q03/index.html) | 填空 | 1 | 复数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 4 | [chongming-2023-q04](../../posts/fill-in/chongming-2023-q04/index.html) | 填空 | 1 | 函数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 5 | [chongming-2023-q05](../../posts/fill-in/chongming-2023-q05/index.html) | 填空 | 1 | 数列 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 6 | [chongming-2023-q06](../../posts/fill-in/chongming-2023-q06/index.html) | 填空 | 1 | 解析几何 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 7 | [chongming-2023-q07](../../posts/fill-in/chongming-2023-q07/index.html) | 填空 | 1 | 三角函数 | — | 单位圆 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 8 | [chongming-2023-q08](../../posts/fill-in/chongming-2023-q08/index.html) | 填空 | 1 | 立体几何 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 9 | [chongming-2023-q09](../../posts/fill-in/chongming-2023-q09/index.html) | 填空 | 1 | 解析几何、圆锥曲线、导数、函数、概率统计 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 10 | [chongming-2023-q10](../../posts/fill-in/chongming-2023-q10/index.html) | 填空 | 1,2 | 不等式、三角函数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |

### 2023 届上海市松江区高三一模数学试卷

- 记录 ID：`songjiang-2023-mock`；类型：学校/地区考试；已发布 17 / 已登记 20；原卷总题量未核实。

| 原题号 | 文章 | 答题形式 | PDF 记录页 | 知识概念 | 方法标签 | 可视化标签 | 当前状态 | 审查结论 / 后续动作 |
|---:|---|---|---|---|---|---|---|---|
| 1 | [songjiang-2023-mock-q01](../../posts/fill-in/songjiang-2023-mock-q01/index.html) | 填空 | 1 | 集合与区间 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 2 | [songjiang-2023-mock-q02](../../posts/fill-in/songjiang-2023-mock-q02/index.html) | 填空 | 1 | 三角函数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 3 | [songjiang-2023-mock-q03](../../posts/fill-in/songjiang-2023-mock-q03/index.html) | 填空 | 1 | 复数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 4 | [songjiang-2023-mock-q04](../../posts/fill-in/songjiang-2023-mock-q04/index.html) | 填空 | 1 | 数列 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 5 | [songjiang-2023-mock-q05](../../posts/fill-in/songjiang-2023-mock-q05/index.html) | 填空 | 1 | 函数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 6 | [songjiang-2023-mock-q06](../../posts/fill-in/songjiang-2023-mock-q06/index.html) | 填空 | 1 | 立体几何 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 7 | [songjiang-2023-mock-q07](../../posts/fill-in/songjiang-2023-mock-q07/index.html) | 填空 | 1 | 解析几何、向量 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 8 | [songjiang-2023-mock-q08](../../posts/fill-in/songjiang-2023-mock-q08/index.html) | 填空 | 1 | 不等式、最值与优化 | — | 待逐题图形审查 | 草稿 | 需核查题源，草稿不公开 |
| 9 | [songjiang-2023-mock-q09](../../posts/fill-in/songjiang-2023-mock-q09/index.html) | 填空 | 1 | 集合与区间 | — | 待逐题图形审查 | 草稿 | 需核查题源，草稿不公开 |
| 10 | [songjiang-2023-mock-q10](../../posts/fill-in/songjiang-2023-mock-q10/index.html) | 填空 | 1 | 解析几何、圆锥曲线 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 11 | [songjiang-2023-mock-q11](../../posts/fill-in/songjiang-2023-mock-q11/index.html) | 填空 | 2 | 立体几何 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 12 | [songjiang-2023-mock-q12](../../posts/fill-in/songjiang-2023-mock-q12/index.html) | 填空 | 2 | 数列 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 13 | [songjiang-2023-mock-q13](../../posts/multiple-choice/songjiang-2023-mock-q13/index.html) | 选择 | 2 | 不等式、数学思想与证明 | 反例检验 | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 14 | [songjiang-2023-mock-q14](../../posts/multiple-choice/songjiang-2023-mock-q14/index.html) | 选择 | 2 | 导数、函数 | — | 函数曲线 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 15 | [songjiang-2023-mock-q15](../../posts/multiple-choice/songjiang-2023-mock-q15/index.html) | 选择 | 2,3 | 函数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 16 | [songjiang-2023-mock-q16](../../posts/multiple-choice/songjiang-2023-mock-q16/index.html) | 选择 | 3 | 解析几何、圆锥曲线、函数、最值与优化 | — | 待逐题图形审查 | 已发布 | 右侧分段比较符在上传 PDF 缺字；需再次确认来源 |
| 17 | [songjiang-2023-mock-q17](../../posts/worked-solutions/songjiang-2023-mock-q17/index.html) | 解答 | 3 | 立体几何、向量 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 18 | [songjiang-2023-mock-q18](../../posts/worked-solutions/songjiang-2023-mock-q18/index.html) | 解答 | 4 | 三角函数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 19 | [songjiang-2023-mock-q19](../../posts/worked-solutions/songjiang-2023-mock-q19/index.html) | 解答 | 4 | 导数、函数、最值与优化 | — | 待逐题图形审查 | 已发布 | 官方参考答案漏列谷深，独立计算值需保留来源边界 |
| 20 | [songjiang-2023-mock-q20](../../posts/worked-solutions/songjiang-2023-mock-q20/index.html) | 解答 | 5 | 解析几何、圆锥曲线 | — | 待逐题图形审查 | 草稿 | 需核查题源，草稿不公开 |

### 2023 届上海市虹口区高三一模数学试卷

- 记录 ID：`hongkou-2023-mock`；类型：学校/地区考试；已发布 10 / 已登记 10；原卷总题量未核实。

| 原题号 | 文章 | 答题形式 | PDF 记录页 | 知识概念 | 方法标签 | 可视化标签 | 当前状态 | 审查结论 / 后续动作 |
|---:|---|---|---|---|---|---|---|---|
| 1 | [hongkou-2023-q01](../../posts/fill-in/hongkou-2023-q01/index.html) | 填空 | 1,7 | 不等式 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 2 | [hongkou-2023-q02](../../posts/fill-in/hongkou-2023-q02/index.html) | 填空 | 1,7 | 不等式、最值与优化 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 3 | [hongkou-2023-q03](../../posts/fill-in/hongkou-2023-q03/index.html) | 填空 | 1,7 | 立体几何 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 4 | [hongkou-2023-q04](../../posts/fill-in/hongkou-2023-q04/index.html) | 填空 | 1,7 | 组合计数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 5 | [hongkou-2023-q05](../../posts/fill-in/hongkou-2023-q05/index.html) | 填空 | 1,7 | 复数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 6 | [hongkou-2023-q06](../../posts/fill-in/hongkou-2023-q06/index.html) | 填空 | 1,7 | 数列 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 7 | [hongkou-2023-q07](../../posts/fill-in/hongkou-2023-q07/index.html) | 填空 | 1,7 | 导数、函数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 8 | [hongkou-2023-q08](../../posts/fill-in/hongkou-2023-q08/index.html) | 填空 | 1,7 | 组合计数、概率统计 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 9 | [hongkou-2023-q09](../../posts/fill-in/hongkou-2023-q09/index.html) | 填空 | 1,7 | 函数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 10 | [hongkou-2023-q10](../../posts/fill-in/hongkou-2023-q10/index.html) | 填空 | 1,7 | 函数、三角函数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |

### 2023 届上海市杨浦区高三一模数学试卷

- 记录 ID：`yangpu-2023-mock`；类型：学校/地区考试；已发布 10 / 已登记 10；原卷总题量未核实。

| 原题号 | 文章 | 答题形式 | PDF 记录页 | 知识概念 | 方法标签 | 可视化标签 | 当前状态 | 审查结论 / 后续动作 |
|---:|---|---|---|---|---|---|---|---|
| 1 | [yangpu-2023-q01](../../posts/fill-in/yangpu-2023-q01/index.html) | 填空 | 1 | 函数、不等式、概率统计 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 2 | [yangpu-2023-q02](../../posts/fill-in/yangpu-2023-q02/index.html) | 填空 | 1 | 集合与区间 | — | 数轴与区间 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 3 | [yangpu-2023-q03](../../posts/fill-in/yangpu-2023-q03/index.html) | 填空 | 1 | 函数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 4 | [yangpu-2023-q04](../../posts/fill-in/yangpu-2023-q04/index.html) | 填空 | 1 | 三角函数 | — | 单位圆 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 5 | [yangpu-2023-q05](../../posts/fill-in/yangpu-2023-q05/index.html) | 填空 | 1 | 复数 | — | 复平面 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 6 | [yangpu-2023-q06](../../posts/fill-in/yangpu-2023-q06/index.html) | 填空 | 1 | 解析几何、向量 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 7 | [yangpu-2023-q07](../../posts/fill-in/yangpu-2023-q07/index.html) | 填空 | 1 | 概率统计 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 8 | [yangpu-2023-q08](../../posts/fill-in/yangpu-2023-q08/index.html) | 填空 | 1 | 解析几何、圆锥曲线 | 分类讨论 | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 9 | [yangpu-2023-q09](../../posts/fill-in/yangpu-2023-q09/index.html) | 填空 | 1 | 不等式、最值与优化 | 代数变形 | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 10 | [yangpu-2023-q10](../../posts/fill-in/yangpu-2023-q10/index.html) | 填空 | 1 | 组合计数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |

### 2023 届上海市普陀区高三一模数学试卷

- 记录 ID：`putuo-2023-mock`；类型：学校/地区考试；已发布 10 / 已登记 10；原卷总题量未核实。

| 原题号 | 文章 | 答题形式 | PDF 记录页 | 知识概念 | 方法标签 | 可视化标签 | 当前状态 | 审查结论 / 后续动作 |
|---:|---|---|---|---|---|---|---|---|
| 1 | [shanghai-putuo-2023-q01](../../posts/fill-in/shanghai-putuo-2023-q01/index.html) | 填空 | 1 | 复数 | — | 复平面 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 2 | [shanghai-putuo-2023-q02](../../posts/fill-in/shanghai-putuo-2023-q02/index.html) | 填空 | 1 | 立体几何 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 3 | [shanghai-putuo-2023-q03](../../posts/fill-in/shanghai-putuo-2023-q03/index.html) | 填空 | 1 | 函数、不等式 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 4 | [shanghai-putuo-2023-q04](../../posts/fill-in/shanghai-putuo-2023-q04/index.html) | 填空 | 1 | 三角函数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 5 | [shanghai-putuo-2023-q05](../../posts/fill-in/shanghai-putuo-2023-q05/index.html) | 填空 | 1 | 三角函数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 6 | [shanghai-putuo-2023-q06](../../posts/fill-in/shanghai-putuo-2023-q06/index.html) | 填空 | 1 | 组合计数 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 7 | [shanghai-putuo-2023-q07](../../posts/fill-in/shanghai-putuo-2023-q07/index.html) | 填空 | 1 | 解析几何、圆锥曲线 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 8 | [shanghai-putuo-2023-q08](../../posts/fill-in/shanghai-putuo-2023-q08/index.html) | 填空 | 1 | 概率统计 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 9 | [shanghai-putuo-2023-q09](../../posts/fill-in/shanghai-putuo-2023-q09/index.html) | 填空 | 1 | 解析几何 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |
| 10 | [shanghai-putuo-2023-q10](../../posts/fill-in/shanghai-putuo-2023-q10/index.html) | 填空 | 1 | 概率统计 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |

### 2024 届上海市浦东新区高三二模 · 解析几何第 20 题摘录

- 记录 ID：`shanghai-2024-er-mo-pudong`；类型：地区摘录；已发布 1 / 已登记 1；原卷总题量未核实。

| 原题号 | 文章 | 答题形式 | PDF 记录页 | 知识概念 | 方法标签 | 可视化标签 | 当前状态 | 审查结论 / 后续动作 |
|---:|---|---|---|---|---|---|---|---|
| 20 | [shanghai-2024-geometry-pudong-q20](../../posts/worked-solutions/shanghai-2024-geometry-pudong-q20/index.html) | 解答 | 2 | 解析几何、圆锥曲线、向量 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |

### 2024 届上海市嘉定区高三二模 · 解析几何第 20 题摘录

- 记录 ID：`shanghai-2024-er-mo-jiading`；类型：地区摘录；已发布 1 / 已登记 1；原卷总题量未核实。

| 原题号 | 文章 | 答题形式 | PDF 记录页 | 知识概念 | 方法标签 | 可视化标签 | 当前状态 | 审查结论 / 后续动作 |
|---:|---|---|---|---|---|---|---|---|
| 20 | [shanghai-2024-geometry-jiading-q20](../../posts/worked-solutions/shanghai-2024-geometry-jiading-q20/index.html) | 解答 | 3 | 解析几何、圆锥曲线 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |

### 2024 届上海市长宁区高三二模 · 解析几何第 20 题摘录

- 记录 ID：`shanghai-2024-er-mo-changning`；类型：地区摘录；已发布 1 / 已登记 1；原卷总题量未核实。

| 原题号 | 文章 | 答题形式 | PDF 记录页 | 知识概念 | 方法标签 | 可视化标签 | 当前状态 | 审查结论 / 后续动作 |
|---:|---|---|---|---|---|---|---|---|
| 20 | [shanghai-2024-geometry-changning-q20](../../posts/worked-solutions/shanghai-2024-geometry-changning-q20/index.html) | 解答 | 4 | 解析几何、圆锥曲线、最值与优化、向量 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |

### 2024 届上海市闵行区高三二模 · 解析几何第 20 题摘录

- 记录 ID：`shanghai-2024-er-mo-minhang`；类型：地区摘录；已发布 1 / 已登记 1；原卷总题量未核实。

| 原题号 | 文章 | 答题形式 | PDF 记录页 | 知识概念 | 方法标签 | 可视化标签 | 当前状态 | 审查结论 / 后续动作 |
|---:|---|---|---|---|---|---|---|---|
| 20 | [shanghai-2024-geometry-minhang-q20](../../posts/worked-solutions/shanghai-2024-geometry-minhang-q20/index.html) | 解答 | 5 | 解析几何、圆锥曲线、向量 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |

### 2024 届上海市虹口区高三二模 · 解析几何第 20 题摘录

- 记录 ID：`shanghai-2024-er-mo-hongkou`；类型：地区摘录；已发布 1 / 已登记 1；原卷总题量未核实。

| 原题号 | 文章 | 答题形式 | PDF 记录页 | 知识概念 | 方法标签 | 可视化标签 | 当前状态 | 审查结论 / 后续动作 |
|---:|---|---|---|---|---|---|---|---|
| 20 | [shanghai-2024-geometry-hongkou-q20](../../posts/worked-solutions/shanghai-2024-geometry-hongkou-q20/index.html) | 解答 | 6 | 解析几何、圆锥曲线 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |

### 2024 届上海市静安区高三二模 · 解析几何第 20 题摘录

- 记录 ID：`shanghai-2024-er-mo-jingan`；类型：地区摘录；已发布 1 / 已登记 1；原卷总题量未核实。

| 原题号 | 文章 | 答题形式 | PDF 记录页 | 知识概念 | 方法标签 | 可视化标签 | 当前状态 | 审查结论 / 后续动作 |
|---:|---|---|---|---|---|---|---|---|
| 20 | [shanghai-2024-geometry-jingan-q20](../../posts/worked-solutions/shanghai-2024-geometry-jingan-q20/index.html) | 解答 | 7 | 解析几何、圆锥曲线 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |

### 2024 届上海市普陀区高三二模 · 解析几何第 20 题摘录

- 记录 ID：`shanghai-2024-er-mo-putuo`；类型：地区摘录；已发布 1 / 已登记 1；原卷总题量未核实。

| 原题号 | 文章 | 答题形式 | PDF 记录页 | 知识概念 | 方法标签 | 可视化标签 | 当前状态 | 审查结论 / 后续动作 |
|---:|---|---|---|---|---|---|---|---|
| 20 | [shanghai-2024-geometry-putuo-q20](../../posts/worked-solutions/shanghai-2024-geometry-putuo-q20/index.html) | 解答 | 8 | 解析几何、圆锥曲线、向量 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |

### 2024 届上海市徐汇区高三二模 · 解析几何第 20 题摘录

- 记录 ID：`shanghai-2024-er-mo-xuhui`；类型：地区摘录；已发布 1 / 已登记 1；原卷总题量未核实。

| 原题号 | 文章 | 答题形式 | PDF 记录页 | 知识概念 | 方法标签 | 可视化标签 | 当前状态 | 审查结论 / 后续动作 |
|---:|---|---|---|---|---|---|---|---|
| 20 | [shanghai-2024-geometry-xuhui-q20](../../posts/worked-solutions/shanghai-2024-geometry-xuhui-q20/index.html) | 解答 | 9 | 解析几何、圆锥曲线、向量 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |

### 2024 届上海市宝山区高三二模 · 解析几何第 20 题摘录

- 记录 ID：`shanghai-2024-er-mo-baoshan`；类型：地区摘录；已发布 1 / 已登记 1；原卷总题量未核实。

| 原题号 | 文章 | 答题形式 | PDF 记录页 | 知识概念 | 方法标签 | 可视化标签 | 当前状态 | 审查结论 / 后续动作 |
|---:|---|---|---|---|---|---|---|---|
| 20 | [shanghai-2024-geometry-baoshan-q20](../../posts/worked-solutions/shanghai-2024-geometry-baoshan-q20/index.html) | 解答 | 10 | 解析几何、圆锥曲线、最值与优化 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |

### 2024 届上海市松江区高三二模 · 解析几何第 20 题摘录

- 记录 ID：`shanghai-2024-er-mo-songjiang`；类型：地区摘录；已发布 1 / 已登记 1；原卷总题量未核实。

| 原题号 | 文章 | 答题形式 | PDF 记录页 | 知识概念 | 方法标签 | 可视化标签 | 当前状态 | 审查结论 / 后续动作 |
|---:|---|---|---|---|---|---|---|---|
| 20 | [shanghai-2024-geometry-songjiang-q20](../../posts/worked-solutions/shanghai-2024-geometry-songjiang-q20/index.html) | 解答 | 11 | 解析几何、圆锥曲线、向量 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |

### 2024 届上海市青浦区高三二模 · 解析几何第 20 题摘录

- 记录 ID：`shanghai-2024-er-mo-qingpu`；类型：地区摘录；已发布 1 / 已登记 1；原卷总题量未核实。

| 原题号 | 文章 | 答题形式 | PDF 记录页 | 知识概念 | 方法标签 | 可视化标签 | 当前状态 | 审查结论 / 后续动作 |
|---:|---|---|---|---|---|---|---|---|
| 20 | [shanghai-2024-geometry-qingpu-q20](../../posts/worked-solutions/shanghai-2024-geometry-qingpu-q20/index.html) | 解答 | 12 | 解析几何、圆锥曲线 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |

### 2024 届上海市金山区高三二模 · 解析几何第 20 题摘录

- 记录 ID：`shanghai-2024-er-mo-jinshan`；类型：地区摘录；已发布 1 / 已登记 1；原卷总题量未核实。

| 原题号 | 文章 | 答题形式 | PDF 记录页 | 知识概念 | 方法标签 | 可视化标签 | 当前状态 | 审查结论 / 后续动作 |
|---:|---|---|---|---|---|---|---|---|
| 20 | [shanghai-2024-geometry-jinshan-q20](../../posts/worked-solutions/shanghai-2024-geometry-jinshan-q20/index.html) | 解答 | 13 | 解析几何、圆锥曲线 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |

### 2024 届上海市崇明区高三二模 · 解析几何第 20 题摘录

- 记录 ID：`shanghai-2024-er-mo-chongming`；类型：地区摘录；已发布 1 / 已登记 1；原卷总题量未核实。

| 原题号 | 文章 | 答题形式 | PDF 记录页 | 知识概念 | 方法标签 | 可视化标签 | 当前状态 | 审查结论 / 后续动作 |
|---:|---|---|---|---|---|---|---|---|
| 20 | [shanghai-2024-geometry-chongming-q20](../../posts/worked-solutions/shanghai-2024-geometry-chongming-q20/index.html) | 解答 | 14 | 解析几何、圆锥曲线 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |

### 2024 届上海市黄浦区高三二模 · 解析几何第 20 题摘录

- 记录 ID：`shanghai-2024-er-mo-huangpu`；类型：地区摘录；已发布 1 / 已登记 1；原卷总题量未核实。

| 原题号 | 文章 | 答题形式 | PDF 记录页 | 知识概念 | 方法标签 | 可视化标签 | 当前状态 | 审查结论 / 后续动作 |
|---:|---|---|---|---|---|---|---|---|
| 20 | [shanghai-2024-geometry-huangpu-q20](../../posts/worked-solutions/shanghai-2024-geometry-huangpu-q20/index.html) | 解答 | 15 | 解析几何、圆锥曲线 | — | 待逐题图形审查 | 已发布 | 标题、摘要和封面已修正：椭圆焦点是双曲线顶点，而非双曲线焦点 |

### 2024 届上海市杨浦区高三二模 · 解析几何第 20 题摘录

- 记录 ID：`shanghai-2024-er-mo-yangpu`；类型：地区摘录；已发布 1 / 已登记 1；原卷总题量未核实。

| 原题号 | 文章 | 答题形式 | PDF 记录页 | 知识概念 | 方法标签 | 可视化标签 | 当前状态 | 审查结论 / 后续动作 |
|---:|---|---|---|---|---|---|---|---|
| 20 | [shanghai-2024-geometry-yangpu-q20](../../posts/worked-solutions/shanghai-2024-geometry-yangpu-q20/index.html) | 解答 | 16 | 解析几何、圆锥曲线、向量 | — | 待逐题图形审查 | 已发布 | 结构/归属已核对；数学证明待源卷复核 |

### 2024 届上海市奉贤区高三二模 · 解析几何第 20 题摘录

- 记录 ID：`shanghai-2024-er-mo-fengxian`；类型：地区摘录；已发布 0 / 已登记 1；原卷总题量未核实。

| 原题号 | 文章 | 答题形式 | PDF 记录页 | 知识概念 | 方法标签 | 可视化标签 | 当前状态 | 审查结论 / 后续动作 |
|---:|---|---|---|---|---|---|---|---|
| 20 | [shanghai-2024-geometry-fengxian-q20](../../posts/worked-solutions/shanghai-2024-geometry-fengxian-q20/index.html) | 解答 | 17 | 解析几何、圆锥曲线 | 反例检验 | 待逐题图形审查 | 草稿 | 需核查题源，草稿不公开 |

### 2023 届上海市嘉定区高三一模数学试卷

- 记录 ID：`jiading-2023-mock`；类型：学校/地区考试；已发布 10 / 已登记 10；原卷总题量未核实。

| 原题号 | 文章 | 答题形式 | PDF 记录页 | 知识概念 | 方法标签 | 可视化标签 | 当前状态 | 审查结论 / 后续动作 |
|---:|---|---|---|---|---|---|---|---|
| 11 | [jiading-2023-q11](../../posts/fill-in/jiading-2023-q11/index.html) | 填空 | 1 | 立体几何、向量 | — | 待逐题图形审查 | 已发布 | 嘉定整卷目前仅登记 Q11–Q20，本条为节选 |
| 12 | [jiading-2023-q12](../../posts/fill-in/jiading-2023-q12/index.html) | 填空 | 1 | 解析几何、圆锥曲线、导数、函数 | — | 待逐题图形审查 | 已发布 | 嘉定整卷目前仅登记 Q11–Q20，本条为节选 |
| 13 | [jiading-2023-q13](../../posts/multiple-choice/jiading-2023-q13/index.html) | 选择 | 2 | 数学思想与证明 | 反例检验 | 待逐题图形审查 | 已发布 | 嘉定整卷目前仅登记 Q11–Q20，本条为节选 |
| 14 | [jiading-2023-q14](../../posts/multiple-choice/jiading-2023-q14/index.html) | 选择 | 2 | 解析几何、圆锥曲线 | — | 待逐题图形审查 | 已发布 | 嘉定整卷目前仅登记 Q11–Q20，本条为节选 |
| 15 | [jiading-2023-q15](../../posts/multiple-choice/jiading-2023-q15/index.html) | 选择 | 2 | 概率统计 | — | 待逐题图形审查 | 已发布 | 嘉定整卷目前仅登记 Q11–Q20，本条为节选 |
| 16 | [jiading-2023-q16](../../posts/multiple-choice/jiading-2023-q16/index.html) | 选择 | 2 | 数学思想与证明、三角函数 | — | 待逐题图形审查 | 已发布 | 嘉定整卷目前仅登记 Q11–Q20，本条为节选 |
| 17 | [jiading-2023-q17](../../posts/worked-solutions/jiading-2023-q17/index.html) | 解答 | 2 | 立体几何、向量 | — | 待逐题图形审查 | 已发布 | 嘉定整卷目前仅登记 Q11–Q20，本条为节选 |
| 18 | [jiading-2023-q18](../../posts/worked-solutions/jiading-2023-q18/index.html) | 解答 | 3 | 数列 | — | 待逐题图形审查 | 已发布 | 嘉定整卷目前仅登记 Q11–Q20，本条为节选 |
| 19 | [jiading-2023-q19](../../posts/worked-solutions/jiading-2023-q19/index.html) | 解答 | 3,4 | 最值与优化、概率统计 | — | 待逐题图形审查 | 已发布 | 嘉定整卷目前仅登记 Q11–Q20，本条为节选 |
| 20 | [jiading-2023-q20](../../posts/worked-solutions/jiading-2023-q20/index.html) | 解答 | 4 | 解析几何、圆锥曲线、不等式、最值与优化 | — | 待逐题图形审查 | 已发布 | 嘉定整卷目前仅登记 Q11–Q20，本条为节选 |

## 4. 仍需单独逐题完成的 L3/L4 审查

每一道完整数学审查应提供：PDF 页图、题干语义 MathML、可见原题细节、独立证明、端点/相异根/退化讨论、SVG 数值断言、浏览器截图或真实渲染结果、结论与原题答案的对照。**本台账没有声称已完成这些逐题数学层面的全部检查。**

### 当前结构检查异常

- 无文件路径缺失、原题号重复或公开题目知识映射缺失。5 道 draft 不出现在发布知识图谱属于设计要求，不构成结构异常。

### 回归命令

```bash
python scripts/sync_skills.py --check
python -m pytest -q
python scripts/build_site.py
python scripts/validate_site.py
python scripts/browser_smoke.py
```

> GitHub Actions 的绿色代表实际运行项通过；未运行的手工原 PDF 比对与数学定理证明不得自动标为已验证。静态路由不会展示未经核实的题干和答案。
