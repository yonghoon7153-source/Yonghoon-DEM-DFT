# static/vendor/ — 로컬 CDN 사본 (에어갭/제한망 대비)

비어 있으면 사이트는 CDN(jsdelivr·plot.ly·3dmol)을 씀.
`bash tools/vendor_libs.sh` 로 채우면 `app.py _vsrc()` 가 자동으로 **로컬 파일**을 사용
(요청마다 존재 확인 → 재시작 불필요). 파일 자체는 용량이 커서 git에 커밋하지 않음(.gitignore).

필요 파일: marked.min.js · katex.min.{js,css} · katex-autorender.min.js · mermaid.min.js ·
plotly.min.js · 3Dmol-min.js · fonts/KaTeX_*.woff2
