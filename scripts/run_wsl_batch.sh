#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════
# WSL 원샷 배치 (2026-07-24) — "이거 다하자" 중 사용자-머신 몫
#   [0] sklearn/joblib/h5py 설치  [1] NASA PCoE 실다운로드(S3, URL 200 검증됨)
#   [2] .mat→CSV 변환+인제스트(§F1 FORM/METHOD-ONLY)  [3] Severson(수동입수시) 변환
#   [4] v3 surrogate 실학습(results/ 코퍼스 → joblib+리포트)
# 사용: bash scripts/run_wsl_batch.sh          (repo 루트 어디서든)
# 재실행 안전: 다운로드/압축해제 스킵-if-exists.
# ══════════════════════════════════════════════════════════════════════════
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DATA="$ROOT/data/open_cycling"
CSV="$DATA/csv"
mkdir -p "$DATA" "$CSV"
PY=python3

echo "══ [0/4] 의존성 (scikit-learn joblib h5py) ══"
$PY -m pip install -q scikit-learn joblib h5py || echo "  ⚠ pip 실패 — venv 활성화 확인"

echo "══ [1/4] NASA PCoE 실다운로드 (~수백MB; 이미 있으면 스킵) ══"
NZ="$DATA/NASA_Battery_Data_Set.zip"
if [ ! -f "$NZ" ]; then
  curl -L --fail --retry 3 -o "$NZ" \
    "https://phm-datasets.s3.amazonaws.com/NASA/5.+Battery+Data+Set.zip" \
    || { echo "  ⚠ NASA 다운로드 실패 — 네트워크 확인"; }
fi
if [ -f "$NZ" ] && [ ! -d "$DATA/nasa" ]; then
  mkdir -p "$DATA/nasa" && unzip -q -o "$NZ" -d "$DATA/nasa"
  # 배포본은 zip-in-zip — 내부 zip 도 풀기
  find "$DATA/nasa" -name "*.zip" -execdir unzip -q -n {} \; 2>/dev/null || true
fi

echo "══ [2/4] NASA .mat → CSV → 인제스트 (liquid_lco = §F1 FORM/METHOD-ONLY) ══"
if [ -d "$DATA/nasa" ]; then
  find "$DATA/nasa" -name "B0*.mat" | sort | head -8 | while read -r f; do
    $PY "$ROOT/scripts/cycling_data_ingest.py" --nasa-mat "$f" --out-dir "$CSV" || true
  done
  for c in "$CSV"/*_nasa.csv; do
    [ -e "$c" ] || continue
    $PY "$ROOT/scripts/cycling_data_ingest.py" --csv "$c" --chemistry liquid_lco || true
  done
fi

echo "══ [3/4] Severson/MIT (matr.io 는 동적 링크 → 수동 1회) ══"
echo "    https://data.matr.io/1/  에서 batchdata *.mat 받아  $DATA/severson/  에 두면 자동 변환"
mkdir -p "$DATA/severson"
for f in "$DATA"/severson/*.mat; do
  [ -e "$f" ] || continue
  $PY "$ROOT/scripts/cycling_data_ingest.py" --severson-mat "$f" --out-dir "$CSV" --max-cells 8 || true
done
for c in "$CSV"/*_cell*.csv; do
  [ -e "$c" ] || continue
  $PY "$ROOT/scripts/cycling_data_ingest.py" --csv "$c" --chemistry liquid_lfp || true
done

echo "══ [4/4] v3 surrogate 실학습 (results/ 코퍼스 → models/cycle_surrogate) ══"
# 데이터 폴더 규약: 코드=stoic-knuth worktree, 데이터=~/Yonghoon-DEM-DFT/webapp/results (CLAUDE.md)
RESULTS="${WEBAPP_RESULTS_FOLDER:-$HOME/Yonghoon-DEM-DFT/webapp/results}"
[ -d "$RESULTS" ] || RESULTS="$ROOT/webapp/results"
$PY "$ROOT/scripts/train_cycle_surrogate.py" --results "$RESULTS" --out "$ROOT/models/cycle_surrogate"

echo ""
echo "══ (선택) A10 ledger expand-void 재실런 — Kang&Shin 1.51× magnitude 재해석 ══"
echo "    σ_e_rel≈1 예상 (shrink-proxy 아티팩트 제거 확인).  기존 100cyc 런 인자에 --poly-mode expand-void 만 추가:"
echo "    python3 scripts/cycle_contact_ledger.py <기존인자들> --poly-mode expand-void"
echo "완료.  산출: $CSV/*.csv (변환) · models/cycle_surrogate/ (joblib+리포트)"
