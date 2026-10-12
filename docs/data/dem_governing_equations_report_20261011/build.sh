#!/usr/bin/env bash
# DEM 지배방정식 배경 보고서 (2026-10-11) — md → PDF (KaTeX + Chromium) · DOCX (pandoc · Word 수식 · 표 가로줄)
# 쓰는 법: bash build.sh <작업 폴더>
#   작업 폴더에 미리 둘 것 (리포에 넣지 않는다):
#     node_modules/  (npm: katex@0.16.11 · marked@12.0.2)
#     fonts/NotoSansKR-400.ttf · fonts/NotoSansKR-700.ttf  (Google Fonts)
#     ref_malgun.docx  (pandoc 기본 reference.docx 의 글꼴을 맑은 고딕으로 바꾼 것)
#   PANDOC = pandoc 3.9 (pip: pypandoc_binary 1.17) · CHROME = Chromium (기본: Playwright 경로)
set -euo pipefail
W=$(cd "${1:?work dir}" && pwd)
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$HERE/../../.." && pwd)
MD=$REPO/docs/dem_governing_equations_background_20261011.md
# 리포 md 의 그림 경로 (docs/ 기준) → 작업 폴더의 맨 파일명
sed -E 's#\]\(data/dem_governing_equations_report_20261011/#](#g' "$MD" > "$W/report.md"
cp "$HERE"/fig1_contact_geometry.png "$HERE"/fig2_hysteresis_cycle.png "$W/"
( cd "$W" && node "$HERE/build_html.mjs" report.md report.html "$W/fonts" "$W/node_modules/katex/dist" )
"${CHROME:-/opt/pw-browsers/chromium-1194/chrome-linux/chrome}" --headless=new --no-sandbox --disable-gpu \
  --no-pdf-header-footer --allow-file-access-from-files --print-to-pdf="$W/report.pdf" "file://$W/report.html"
# pandoc 의 TeX 수식은 \tag 를 못 읽는다 → 번호를 수식 안 글자로 바꿔 넘긴다
sed -E 's/\\tag\{([^}]*)\}/\\qquad\\text{(\1)}/g' "$W/report.md" > "$W/report_docx.md"
( cd "$W" && "${PANDOC:-pandoc}" report_docx.md -o report_raw.docx --reference-doc="$W/ref_malgun.docx" )
python3 "$HERE/docx_tables.py" "$W/report_raw.docx" "$W/report.docx"
echo "PDF  $W/report.pdf"
echo "DOCX $W/report.docx"
