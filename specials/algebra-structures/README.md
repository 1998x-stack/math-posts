# 高中竞赛数学｜代数结构与多项式十二讲

[系列目录](index.html) · [Olah-style-posts 规范](https://github.com/1998x-stack/Olah-style-posts)

本系列对照用户提供的《高中数学竞赛60讲_课程总纲与逐讲设计.md》的 **模块 II（原定第 13—22 讲共十讲）** 创建。本次按要求构建十二篇，将原第 18 讲拆分为复数旋转/单位根、原第 20 讲拆分为线性递推/矩阵快速幂，其他讲次保持原顺序。

## 页面与内容

- [01 韦达定理与对称多项式](01-vieta-symmetry.html) ← 原第 13 讲：把三个根压缩成三个基本对称量。
- [02 牛顿恒等式与根的幂和](02-newton-sums.html) ← 原第 14 讲：不求根，直接求高阶幂和。
- [03 多项式整除、余数与根](03-factor-remainder.html) ← 原第 15 讲：从一次代入发现整个代数因子。
- [04 拉格朗日插值](04-lagrange-interpolation.html) ← 原第 16 讲：由三个节点重建唯一二次多项式。
- [05 函数方程：从特殊代入到结构](05-cauchy-equation.html) ← 原第 17 讲：证明连续性何时把可加函数锁成直线。
- [06 复数乘法与平面旋转](06-complex-rotation.html) ← 原第 18-A 讲：模与幅角解释长度和方向。
- [07 单位根与离散筛选](07-roots-of-unity.html) ← 原第 18-B 讲：几何级数揭示旋转对称与相消。
- [08 切比雪夫多项式与倍角公式](08-chebyshev.html) ← 原第 19 讲：三角倍角变成代数递推。
- [09 线性递推与特征方程](09-characteristic-recurrence.html) ← 原第 20-A 讲：两个特征根产生指数通项。
- [10 矩阵快速幂与斐波那契递推](10-fibonacci-matrix.html) ← 原第 20-B 讲：矩阵更新、快速幂和行列式。
- [11 有限差分与数列求和](11-finite-difference.html) ← 原第 21 讲：从立方差和望远镜求出平方和。
- [12 多项式恒等式与代数构造](12-sophie-germain.html) ← 原第 22 讲：先补完全平方，再发现因子。

每页含：题意导读、核心定理与条件、四个证明步骤、四幅渐进 SVG 状态、参数驱动 SVG 动态实验、真实 MathML 分式/上下标/算子（矩阵篇含 MathML mtable）、三道分层练习与边界条件。图形由数学方程直接计算，不能替代普遍证明。

## 工程结构

- `index.html`：专题课程首页
- `NN-*.html`：独立可阅读的 12 篇页面
- `assets/article.css`、`assets/algebra.js`：离线样式与 12 个交互模型
- `svg/NN-*.svg`：12 份单独 SVG 输出
- `source/NN.json`：逐讲内容、可访问 MathML 原式和教学证明
- `source/article-template.js`：页面可再生模板
- `source/manifest.json`：十二篇与原提纲的映射
- `evidence.json`：来源与验证边界

`scripts/build_site.py` 负责将可公开的 HTML、CSS、JS 与 SVG 发布至 `_site/specials/algebra-structures/`，并加入首页和 sitemap。JSON 源数据以及 QA 脚本不需公开打包，仍保留在仓库中。

## 质量门槛

需要执行数学数值校验、MathML arity/namespace/布局检查、Chromium 1440/768/390/360 视口、交互状态、无网络依赖和文档打印检查，并以 GitHub Actions 的真实结果报告成功或失败。PR 未合并前不声称 Pages 已上线。
