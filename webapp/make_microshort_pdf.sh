#!/usr/bin/env bash
# make_microshort_pdf.sh — `/microshort/summary` 화면을 PDF 파일로 인쇄한다 (2026-10-06).
#
#   ./webapp/make_microshort_pdf.sh            # → webapp/static/pdf/microshort_summary.pdf
#   CHROME=/path/to/chrome ./webapp/make_microshort_pdf.sh
#
# · PDF 는 **화면의 사본**이다 — 내용은 templates/microshort_summary.html 하나에만 있고, 인쇄 규칙은
#   static/css/style.css 의 `@media print` 한 곳이다. 템플릿을 고쳤으면 이 스크립트를 다시 돌려 PDF 를 갱신한다.
# · 앱을 잠깐 로컬 (127.0.0.1) 에 띄우고 headless Chromium 으로 인쇄한 뒤 내린다. 바깥으로 아무것도 보내지 않는다.
set -euo pipefail
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PORT="${WEBAPP_PORT:-5099}"
CHROME="${CHROME:-$(ls -d /opt/pw-browsers/chromium-*/chrome-linux/chrome 2>/dev/null | head -1 || true)}"
[ -n "$CHROME" ] && [ -x "$CHROME" ] || { echo "Chromium 실행 파일을 찾지 못했다 — CHROME=<경로> 로 지정한다" >&2; exit 2; }
OUT="$HERE/static/pdf/microshort_summary.pdf"
mkdir -p "$(dirname "$OUT")"

WEBAPP_PORT="$PORT" python "$HERE/app.py" >/dev/null 2>&1 &
PID=$!
trap 'kill "$PID" 2>/dev/null || true' EXIT
for _ in $(seq 100); do
  curl -fs "http://127.0.0.1:$PORT/microshort/summary" >/dev/null && break
  sleep 0.2
done
curl -fs "http://127.0.0.1:$PORT/microshort/summary" >/dev/null || { echo "앱이 뜨지 않았다 (포트 $PORT)" >&2; exit 3; }

"$CHROME" --headless=new --no-sandbox --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=5000 --print-to-pdf="$OUT" "http://127.0.0.1:$PORT/microshort/summary" 2>/dev/null
[ -s "$OUT" ] || { echo "PDF 가 만들어지지 않았다" >&2; exit 4; }
echo "PDF: $OUT ($(stat -c %s "$OUT") bytes)"
