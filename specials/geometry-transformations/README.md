# 几何变换与不变量 · 高中竞赛数学12讲

本专题源自《高中竞赛数学60讲》课程模块 I（第 01—12 讲），按 [Olah-style-posts](https://github.com/1998x-stack/Olah-style-posts) 的问题优先、渐进图解、真实公式与浏览器 QA 工作流制作。几何定理、例题、交互脚本独立编写，并未复制第三方网页或图像。

## 课程

- [01 圆的反演变换](01-inversion.html)：圆为何会变成直线？从倒数距离到托勒密。
- [02 相似、旋转与螺旋相似](02-spiral-similarity.html)：把角度和长度比例统一成一个复数乘子。
- [03 仿射变换：椭圆、面积比与重心](03-affine.html)：把椭圆变回圆，让面积排序保持不变。
- [04 塞瓦、梅涅劳斯与共点共线](04-ceva-menelaus.html)：从三条线的交点问题走向分点比的乘积。
- [05 圆幂、根轴与根心](05-radical-axis.html)：用平方差把两个圆的关系线性化。
- [06 三角形五心、欧拉线与九点圆](06-euler-nine-point.html)：向量加法解释三种中心和九点圆。
- [07 托勒密定理与圆内接四边形](07-ptolemy.html)：三角不等式经反演成为四边形乘积关系。
- [08 西姆松线：投影为何突然共线](08-simson.html)：三个垂足与一条藏在圆周角中的直线。
- [09 米克尔点与三圆共点](09-miquel.html)：三组局部共圆关系为何锁定一个公共点。
- [10 调和点列与交比](10-cross-ratio.html)：普通距离变了，射影不变量却保持不变。
- [11 极点与极线：点线对偶](11-polar-line.html)：用切线方程发现点与直线的互易关系。
- [12 帕斯卡定理与射影几何初探](12-pascal.html)：六点圆锥曲线与三对边的神秘共线性。

## 工程

- `index.html`：专题目录
- `NN-*.html`：12 篇长文，离线情况下可相对路径加载本地 CSS 和 JS
- `assets/article.css`：响应式、打印、可访问数学排版
- `assets/geometry.js`：12 组共享二维数学对象模型，所有动态图从数学坐标而非截图驱动
- `svg/NN-*.svg`：12 幅可独立打开的矢量示意图
- `source/NN.json`：每讲的题目、知识链、MathML 原式、证明、练习和边界条件
- `source/article-template.js`：可复用页面模板，给 JSON 与 geometryScene 可再生 HTML
- `evidence.json`：来源边界与声明级别
- `tests/test_competition_geometry_special.py`（仓库根）：结构、分式、几何数值和负例测试

## 发布方式

`scripts/build_site.py` 负责将此目录中的 `index.html`、12 篇 HTML、`assets/` 与 `svg/` 复制到 `_site/specials/geometry-transformations/`，并加入首页与 sitemap。 `source/`、测试和 evidence 不公开打包。该专题不登记为试卷文章、不进入 `content/posts.json` 的考试题目统计。

不得将少量参数下的数值残差冒充定理的一般证明，也不能在 PR 合并前声称 Pages 已上线。
