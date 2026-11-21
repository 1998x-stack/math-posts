# 试卷 / PDF / 题目关系与来源证据 Schema（v1）

## 1. 三种实体不要混用

```text
source_document（原始 PDF / 照片 / 专题汇编）
      ├── paper（具体学校/地区试卷，或 worksheet/problem-set）
      │      ├── question_number: 01 → post slug A
      │      ├── question_number: 02 → post slug B
      │      └── ... 未转换题目保持“未收录”
      └── paper（若源 PDF 是地区汇编，可派生其他学校试卷摘录）
```

**同一个 PDF 可以包含多张试卷/多道地区题**（例如上海 2024 二模解析几何汇编）；不能因为都来自同一 PDF，就把 16 道不同地区第 20 题列成同一张试卷的第 20 题。反过来，单张学校试卷的第 1 至 21 题需要按原卷题号顺序浏览，而不是按发布时间排序。

## 2. Paper Registry

`content/papers.json` 是轻量、公开的 metadata 注册表。每条记录：

```json
{
  "id": "yangpu-2023-mock",
  "title": "2023 届上海市杨浦区高三一模数学试卷",
  "kind": "exam",
  "region": "上海市杨浦区",
  "school": null,
  "year": 2023,
  "exam_type": "一模",
  "source_id": "yangpu-2023-mock-upload",
  "source_title": "用户上传的 2023 杨浦一模 PDF",
  "source_access": "user-uploaded",
  "total_questions": null,
  "description": "按原卷顺序整理；仅列本站已登记的题目。"
}
```

- `id` 创建后永久稳定，不能因显示文案修改而换 ID。
- `kind` 在 `exam | exam-excerpt | worksheet | problem-set` 内选择。汇编中的地区单题是 `exam-excerpt`，不冒充完整考卷。
- `school` 只在来源明确指名学校时填写；“杨浦区”是地区，不是学校。
- `total_questions` 只有核实完整原卷题量才能填写数字，否则为 `null`。**已登记题数不等于原卷总题数**。
- `source_id` 指向真实来源文档的逻辑 ID（同一汇编可共用），`source_access` 不能将用户上传文档变成虚构公网 URL。
- 不将原始私密文件名/本地路径/上传地址直接展示为公开下载链接。

## 3. Question Entry：保留当前文章 URL

每条 `content/posts.json` 内容继续用原有 `slug` 和 `category` 决定文章 URL。新增：

```json
{
  "slug": "yangpu-2023-q02",
  "paper_id": "yangpu-2023-mock",
  "question_number": 2,
  "question_type": "fill-in",
  "source_pages": [1],
  "facets": {
    "concept": ["sets", "inequalities"],
    "method": [],
    "visual": ["number-line"]
  }
}
```

`question_number` 是原卷题号，不是本站最新排序号。对 “第 20 题（1）（2）（3）” 应优先保留同一文章并用内部小问 ID；若分拆页面，使用复合 `question_key` 并在 paper 目录中归属于 20 号，不能产生三个互相矛盾的 20 号记录。

**唯一键**：`(paper_id, question_number)` 在当前每题一篇的结构中唯一（将来支持 `question_key` 时改为 `(paper_id, question_key)`）；`slug` 在全库唯一。导入新批次 PDF 时检查重复，避免覆盖已有题。

## 4. 来源、答案与勘误

`evidence.json` 继续保存题目层证据：

```json
{
  "source": {
    "title": "原卷标题",
    "question": 2,
    "pages": [1],
    "material": "user-uploaded PDF (not a public URL)"
  },
  "transcription": {
    "status": "checked-against-rendered-pages"
  },
  "answer": {
    "official": "原卷确有的答案，或 null",
    "independent_check": "本站独立计算及其核验结论"
  }
}
```

建议增量字段 `source.question_pages`、`source.answer_pages`：原卷答案表可能在第 7 页，不能把两页混写成“题干位于 1、7 页”。未核实的历史记录先不自动回填。对官方没有完整详解的试卷，正文不能把本站推导称作官方详解。

发现原题符号无法辨认、官方答案与证明冲突、原卷缺少必要条件时，将 `status: draft`，在 evidence 说明不确定性；试卷目录可以展示“该题暂未公开”这种状态，**绝不展示其 HTML 内容、答案或跳转**。

## 5. 试卷页交互合同

`/papers/` 显示真正可识别的试卷卡：地区/学校、考试、年份、已公开题数、已核实总题数（若有）；可以按年份/考试/地区筛选。

`/papers/<paper_id>/` 显示：

1. 试卷身份与来源说明、是否为摘录或专题集合；
2. 如 `total_questions` 已核实，显示覆盖进度：公开 X / 原卷 Y；否则写“本站已收录 X 道，原卷总题数尚未登记”；
3. 从最小题号升序列出所有已公开题目；仅对已知完整题量，显示未收录位置；
4. 对 draft：仅显示“暂未公开”，避免公开尚未核对的内容；
5. 题卡标注原卷题号、答题形式、知识标签、图示标签；点击跳转回同一题的规范 URL；
6. 下一题/上一题应遵循同一 `paper_id` 的已公开原卷顺序，而不是仓库文件顺序；
7. 如果原卷仅摘录地区第 20 题，明确这是“第 20 题摘录”，不把 1–19 题标成已确认缺失。

## 6. 导入 PDF 的确定性流程

1. 为原始 PDF/照片/汇编分配 `source_id`；检查同一文件是否已登记。
2. 分析它是**完整学校试卷**还是**地区题目汇编**，确定 paper 的数目、类型、学校与年份，未知字段用 null。
3. 从页面渲染核对题号、题干、选项、小问、答案表；为每题生成 evidence，不凭文件名猜总题数。
4. 按原卷题号 one by one 转写；生成 HTML/MathML/SVG/可交互证明。
5. 给文章登记 `paper_id`、`facets`、知识节点与证据状态；验证唯一性与草稿隔离。
6. 每批更新试卷目录进度、构建索引、运行浏览器/单元测试；仅已发布题目可在公开列表中点击。

## 7. 向前兼容 / 回滚

保持 `posts/<category>/<slug>/` 文章 URL 与旧 `tags` 不动；新增索引是纯加法。在未来确实需要对题目迁移目录时，先建立重定向；禁止批量修改分类直接造成文章死链。构建产物 `_site/` 不入库；CI 检查不可把 draft 排进 sitemap、RSS、搜索索引或公开试卷列表链接。


## 8. 单独的 source_document Registry（新增硬约束）

`content/source_documents.json` 保存用户上传的 PDF/图片本身的稳定身份；`papers.json` 的 `source_id` 必须引用它。同一份解析几何地区汇编的多个 `exam-excerpt` 共用一个 `source_id`。不在公开 GitHub 仓库捏造原始文件 URL。

最小例子：

```json
{
  "version": 1,
  "documents": [{
    "id": "shanghai-2024-geometry-compilation",
    "title": "2024届高三二模数学汇编：解析几何",
    "format": "pdf",
    "access": "user-uploaded",
    "page_count": null,
    "checksum_sha256": null,
    "public_url": null,
    "notes": "用户上传；源文件本身不在公开仓库。"
  }]
}
```

- `page_count` 只有实际确认总页数后才填整数；没有源文件字节时 `checksum_sha256` 不能伪造。
- 文件名可以用作显示参考，但真正去重应优先使用文件哈希和用户确认的源文档 ID。
- 多张地区试卷对应一个源文件时，试卷页只展示地区题号摘录，不拼接为一套虚假试卷。
- 同一个 `source_id` 的 paper 必须有一致的 `source_title` 和访问类型；构建前由 `scripts/atlas.py` 检查。
