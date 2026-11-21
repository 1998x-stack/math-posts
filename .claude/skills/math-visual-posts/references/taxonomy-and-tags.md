# 数学题库多维标签与首页检索规范（v1）

## 1. 不再把“题型”当成唯一一级分类

一次检索同时可以表达五类彼此独立的信息：

| 维度 | 存储键 | 例子 | 规则 |
|---|---|---|---|
| 来源试卷 | `paper_id` | 2023 杨浦一模、2021 建平模拟 | 稳定 ID；不放入知识标签 |
| 答题形式 | `question_type` / `category` | fill-in, multiple-choice, worked-solutions | 单值；已有结构保持兼容 |
| 知识分类 | `knowledge_ids` / 知识地图 | conics, spatial-vectors | 多值，尊重现有先修关系 |
| 细粒度概念 | `facets.concept` | analytic-geometry, vector, conics | 多值；来自 `content/taxonomy.json` |
| 解题方法 | `facets.method` | number-shape, casework, counterexample | 多值；必须看过真实步骤才可加 |
| 可视化形式 | `facets.visual` | number-line, function-plot, coordinate-plane | 多值；必须在题目页面有对应真实图解 |

**考试形式与知识主题没有父子关系**：不能把“向量填空题”写成新的固定分类，而应查询 `concept=vector AND question_type=fill-in`。相同问题可以同时属于“解析几何”和“向量”。

现有 `content/categories.json` 继续作为兼容题型导航；`content/knowledge-map.json` 仍是知识节点和先修 DAG 的唯一来源。新增 `content/taxonomy.json` 仅登记跨节点的检索用标签，不复制知识树结构。

## 2. ID、别名与同义词

- 所有机器 ID 使用小写英文 kebab-case；中文显示名与同义词放在注册表中。
- `vector` 的中文为“向量”，可用别名“投影向量/空间向量/数量积”；`conics` 的别名可含“椭圆/双曲线/抛物线”。
- 别名只用于搜索和录入提示：**出现别名不代表这道题已人工审核为该标签**。
- `fill-in`、`multiple-choice` 属于 answer-form 维度，不能重复写成 concept。
- 地区、学校、年份、一模/二模归属于 paper 元数据，不能混在知识标签里。
- `visual` 只指已实现且可核验的图形表达；若一篇仅有装饰性 SVG，不允许自动标为 `coordinate-plane`。
- 方法标签由求解过程而非题目关键词决定；例如“反例”只有确实展示合法反例才能标 `counterexample`。

## 3. 首页与题库页的筛选 UX

建议页面入口：**知识点 / 试卷 / 题型 / 方法**，另设可视化专栏。首页保留精选和学习路径，不让分类卡片占据全部篇幅。

- 默认展示全部已发布题目；四种维度为独立控件（知识概念、试卷、答题形式、方法），可视化作为扩展筛选。
- 逻辑为**不同维度间 AND**；同一维度的多选（未来扩展）使用 OR。例如：解析几何 AND 向量 AND 填空 AND 杨浦一模。
- URL 参数可复制、可回退，例如 `?concept=vector&category=fill-in&paper=yangpu-2023-mock`；分页与搜索不覆盖当前筛选。
- 每个标签显示真实结果数；0 结果提供“清除某条件”和“查看全部题目”；不展示 draft 的标题、答案或文章链接。
- 题目卡片展示：知识主题、题型、来源试卷/题号、已校验可视化类型及 1–3 个高信息密度标签；避免所有标签全部展开。
- 索引键入“向量”时既能搜索标签显示名，也能搜索别名；原始自由字符串 `tags` 仅做历史搜索补充，逐批迁移后才考虑清理。

## 4. 避免标签膨胀的约束

1. 每道已发布题至少有 **1 个 concept 标签 + 1 个合法 knowledge-map 节点**；同一题无需填满所有维度。
2. 推荐概念标签 1–4 个、方法标签 0–3 个、图示标签 0–2 个；数量不是 KPI。
3. 不基于标题、文件名或“有 SVG”强推解题方法标签；没有证据保留空列表。
4. 同义词统一落入 canonical ID，禁止同一维度并存“向量/平面向量/vector”三个标签。
5. 新增知识主题先查是否属于现有知识地图；横切概念用 concept，只有前置依赖与学习目标明确时才增知识节点。
6. 标签修订记录应与原题事实分离：更改索引标签不能悄悄改题意或证明。

## 5. 数据与构建职责

- `content/posts.json`：`paper_id`、`question_number`、`category`、`facets` 与现有 `tags`。
- `content/papers.json`：考试/练习/专题文档的身份、地区、年份、来源和已知总题数；通过题目的 `paper_id` 反向建立试卷目录。
- `content/taxonomy.json`：canonical tag ID、显示名、别名、维度说明。
- `content/knowledge-map.json`：教学知识图谱及前置关系；不由 tag 注册表替代。
- `posts/**/evidence.json`：原题真伪与答案来源的事实层，不因为加标签而重新推断内容。
- `scripts/build_site.py`：统一验证引用；只构建 published 题卡、统计和页面。

## 6. 渐进迁移流程

1. 在旧 `category`、`topic`、`tags` 字段基础上**增量增加** `paper_id` 与 `facets`，保证旧 URL 不变。
2. 明确可由知识地图人工维护过的映射先加入 `concept`，其余概念、方法和可视化由逐题 QA 加入。
3. 为试卷建立 stable ID，已发布题出现在试卷列表，未公开/未收录不伪造文章。
4. 最后才做首页组合筛选与移动端视觉优化，并回归测试 URL、分页、无 JS 和草稿隔离。
