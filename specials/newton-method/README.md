# 牛顿迭代法：用切线寻找方程的根

双击 index.html 即可在支持 MathML Core 的现代浏览器中阅读。所有正文、CSS、JavaScript、图示均在 HTML 内；引用链接需要联网，但不影响阅读。窄屏图示可在独立区域横向滚动。

- `assets/`：8 张原创 SVG 的默认状态与清单。
- `evidence.json`：参考资料与独立推导的证据台账。
- `newton.py`：普通牛顿法、带区间保护的混合算法及 5 条数值断言。运行 `python newton.py`。
- `qa/`：原始生成阶段的 Chromium JSON 报告。截图保留在原始交付 ZIP，不提交到本仓库。

依据 [Olah-style-posts](https://github.com/1998x-stack/Olah-style-posts) 的 SKILL、数学排版、SVG、叙事和 QA 规范；教学叙事参考 Colah 与 Annotated Transformer 的方法，所有图文独立制作。此处是数学主题教学文章，而非论文解读，证据主要为 NIST DLMF 及可复算推导。

限制：环境禁止 Chromium 直接访问 file URL，故用 Playwright set_content 在离线环境载入实际 HTML/SVG 内容。未测试 Firefox/Safari，未运行仓库原版验证器和全仓库测试；采用独立静态与浏览器检查。原始交付阶段尚未发布 GitHub Pages；本仓库的发布状态以 CI 和实际页面为准。截图为各尺寸首屏、代表性切线图、各独立 SVG 和打印模式首屏，不是完整页面逐段截图。
