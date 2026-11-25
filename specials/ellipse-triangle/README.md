# 一个椭圆，七种证明

打开 `index.html` 导航至七篇文章；每篇 HTML 都内联 CSS、SVG、原生 MathML 及交互代码，可单独离线阅读。跨篇导航需要保留同目录中的其他 HTML。

设计依据：`1998x-stack/Olah-style-posts` 的 `skills/olah-style-paper-posts/SKILL.md`，以及 narrative-architecture、math-typesetting、html-design-system、svg-production、implementation-and-interactivity、browser-qa 等规范。本题不是论文解读，故将论文证据环节替换为自包含严格数学推导与数值断言，不引入未经核实的外部论文指标。图形独立绘制。

## 目录
- 01-affine.html：仿射变换法
- 02-trigonometry.html：三角变换法
- 03-vieta.html：直线与韦达定理法
- 04-cauchy.html：柯西不等式法
- 05-hadamard.html：哈达玛行列式不等式法
- 06-tangent.html：切线极值原理法
- 07-conjugate.html：共轭直径法
- svg/：49 幅独立 SVG，按文章分目录，交互图为静态初始状态
- evidence.json：公式数量与图示清单
- verify.py：数学交叉验证、静态结构和 Chromium 页面验收脚本（Python，依赖 beautifulsoup4、playwright，默认 /usr/bin/chromium）
- qa-report.json、qa/：实际检查结果与截图

## 验收边界
七篇文章分别在 1440、768、390、360 px 宽度用 Chromium 验证；实际测试了恢复最优状态按钮、键盘滑块和分式渲染，记录了打印模式截图。数值验证是独立交叉检查，不替代数学证明。由于运行环境禁止直接浏览 file: 与 data: URL，HTML 使用 Playwright set_content 加载，独立 SVG 通过 XML 解析并逐个在独立页面内容中加载；未测试用户本机浏览器文件导航、Safari、Firefox 或实体打印。未运行上游完整 pytest 套件或上游 SVG 提取脚本；这些 SVG 的样式直接写在图元内，使用原始自包含 SVG 导出。未发布 GitHub Pages。
