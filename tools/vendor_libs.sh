#!/bin/bash
# CDN JS/CSS 라이브러리를 webapp/static/vendor/ 로 내려받아 로컬화 (에어갭/제한망 대비).
# 실행: bash tools/vendor_libs.sh   (CDN 접근되는 기계에서 1회)
# 채워지면 사이트(app.py _vsrc)가 자동으로 로컬 파일을 씀 — 재시작 불필요(요청마다 존재확인).
set -e
D="$(cd "$(dirname "$0")/../webapp/static/vendor" && pwd)"; cd "$D"
get(){ printf '  → %-26s' "$1"; curl -fsSL -o "$1" "$2" && echo "$(du -h "$1"|cut -f1)" || echo "FAIL"; }
echo "vendoring → $D"
get marked.min.js           "https://cdn.jsdelivr.net/npm/marked@12/marked.min.js"
get katex.min.js            "https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"
get katex-autorender.min.js "https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
get katex.min.css           "https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css"
get mermaid.min.js          "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"
get plotly.min.js           "https://cdn.plot.ly/plotly-2.35.2.min.js"
get 3Dmol-min.js            "https://3dmol.org/build/3Dmol-min.js"
# KaTeX 폰트 (katex.min.css가 fonts/ 를 상대참조)
mkdir -p fonts && cd fonts
for f in KaTeX_Main-Regular KaTeX_Main-Bold KaTeX_Main-Italic KaTeX_Math-Italic KaTeX_Math-BoldItalic \
         KaTeX_AMS-Regular KaTeX_Size1-Regular KaTeX_Size2-Regular KaTeX_Size3-Regular KaTeX_Size4-Regular \
         KaTeX_Caligraphic-Regular KaTeX_Fraktur-Regular KaTeX_SansSerif-Regular KaTeX_Script-Regular KaTeX_Typewriter-Regular; do
  curl -fsSL -o "$f.woff2" "https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/fonts/$f.woff2" 2>/dev/null || true
done
echo "✅ done — 새로고침하면 로컬 사용 (에어갭 OK). 비우면 다시 CDN."
