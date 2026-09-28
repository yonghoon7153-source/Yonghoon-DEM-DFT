#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════
# LHS 인계표 채우기 — WSL 원샷 (판단 J20 · 1저자 비준 2026-09-28)
#   "벽 기준 τ 새 열" · "✅ 만 이번에" · "채운 뒤 넘김" · SE-rich 0.50
#
#   [1] 재수확 v3 (벽 τ 새 열) → docs/data/lhs_descriptors_$D   (--verify-sha)
#   [2] 옛 수확 (0925) 과 공통 값 대조 — 새 수확은 **키만 늘고 값은 같아야** 한다
#   [3] 웹앱 파이프라인 일괄 (전수 판정 ✅ 열) → docs/data/lhs_webapp_$D   (작업 폴더 $WORK)
#   [4] 인계표 재생성 → docs/data/lhs_handover_$D.csv + _columns.tsv   (전 건 모드에서만)
#   [5] 결과 묶음 → ~/lhs_fill_$D.tar.gz   (보내 주면 커밋 — 원자료 · full_metrics 원본은 안 넣는다)
#
# 사용 (이 브랜치를 pull 한 리포 루트에서)
#   ONE=lhs00_000 bash scripts/run_lhs_fill_wsl.sh     # ★ 먼저 한 건 — 실제로 도는지 · 한 건에 몇 분인지
#   bash scripts/run_lhs_fill_wsl.sh                   # 전 건 (재개 안전 — 끝난 케이스는 건너뛴다)
#   환경: D (날짜 꼬리, 기본 오늘) · WORK (기본 ~/lhs_webapp_work) · ROOT_FROM/ROOT_TO (코호트 경로 치환, 기본 없음)
# ══════════════════════════════════════════════════════════════════════════════
set -uo pipefail
cd "$(dirname "$0")/.." || exit 2
D=${D:-$(date +%Y%m%d)}
WORK=${WORK:-$HOME/lhs_webapp_work}
ONE=${ONE:-}
HARV=docs/data/lhs_descriptors_$D
WAPP=docs/data/lhs_webapp_$D
OLD=docs/data/lhs_descriptors_20260925
REMAP=()
[ -n "${ROOT_FROM:-}" ] && REMAP=(--root-from "$ROOT_FROM" --root-to "${ROOT_TO:-}")
CASE=()
[ -n "$ONE" ] && CASE=(--case "$ONE")

echo "══ 코드 $(git rev-parse --short HEAD) $(git status --porcelain --untracked-files=no | head -1 | cut -c1-40) · D=$D · WORK=$WORK ${ONE:+· 한 건 $ONE}"
python3 scripts/lhs_descriptor_harvest.py --selftest >/dev/null || { echo '⛔ 수확기 selftest 실패 — 멈춘다'; exit 1; }
python3 scripts/lhs_webapp_batch.py --selftest >/dev/null || { echo '⛔ 배치 selftest 실패 — 멈춘다'; exit 1; }

echo "══ [1/5] 재수확 v3 → $HARV"
mkdir -p "$HARV"
t0=$(date +%s)
python3 scripts/lhs_harvest_batch.py --verify-sha --out-dir "$HARV" --summary "$HARV/_batch_summary.json" \
    "${REMAP[@]}" "${CASE[@]}" || echo '  ⚠ 수확 배치 rc≠0 — _batch_summary.json 의 status 를 볼 것'
echo "  수확 $(( $(date +%s) - t0 )) s"

echo "══ [2/5] 옛 수확 ($OLD) 과 공통 값 대조"
python3 - "$OLD" "$HARV" <<'EOF'
import json, sys, pathlib
old, new = map(pathlib.Path, sys.argv[1:3])
KEYS = ('phi_se', 'phi_am', 'porosity_sphere_pct_RECORD_ONLY', 'coverage_AM_P_hertz_pct', 'coverage_AM_S_hertz_pct',
        'coverage_AM_total_hertz_pct', 'tortuosity_dijkstra_SE', 'tau_detail', 'handover_qc', 'status')
n = bad = 0
for p in sorted(new.glob('lhs*.json')):
    q = old / p.name
    if not q.exists():
        continue
    a, b = json.loads(q.read_text()), json.loads(p.read_text())
    n += 1
    for k in KEYS:
        va, vb = a.get(k), b.get(k)
        if k == 'status':
            vb = {x: y for x, y in (vb or {}).items() if x != 'tortuosity_wall'}
        if va != vb:
            bad += 1
            print(f'  ✗ {p.stem}: {k} 가 옛 수확과 다르다')
            break
    if 'tau_wall_detail' not in b:
        bad += 1
        print(f'  ✗ {p.stem}: 벽 τ (tau_wall_detail) 가 없다 — 옛 코드로 수확됐다 (git pull 확인)')
print(f'  공통 값 대조 {n} 건 · 불일치 {bad}')
sys.exit(1 if bad or n == 0 else 0)
EOF
[ $? -eq 0 ] || { echo '⛔ 새 수확이 옛 수확과 공통 값에서 다르다 — 멈춘다 (보고할 것)'; exit 1; }

echo "══ [3/5] 웹앱 파이프라인 일괄 → $WAPP   (작업 폴더 $WORK · 순차 · network 는 웹앱 lock 으로 직렬)"
python3 scripts/lhs_webapp_batch.py --harvest-dir "$HARV" --work "$WORK" --out-dir "$WAPP" "${REMAP[@]}" "${CASE[@]}"
wrc=$?
python3 - "$WAPP" <<'EOF'
import csv, json, sys, pathlib
d = pathlib.Path(sys.argv[1])
st = json.loads((d / 'status.json').read_text(encoding='utf-8'))
cs = st['cases']
el = [c.get('elapsed_s') for c in cs.values() if c.get('status') in ('done', 'partial')]
print(f'  상태 {dict((s, sum(1 for c in cs.values() if c.get("status") == s)) for s in sorted({c.get("status") for c in cs.values()}))}'
      + (f' · 케이스당 중앙 {sorted(el)[len(el) // 2]:.0f} s' if el else ''))
rows = list(csv.DictReader(open(d / 'metrics_flat.csv', encoding='utf-8')))
if rows:
    r = rows[0]
    keys = ('se_se_cn', 'am_se_cn_mean', 'am_am_cn', 'percolation_pct', 'bulk_resistance_fraction', 'stress_cv',
            'fracture_index_force', 'area_AM전체_SE_total', 'porosity')
    print(f'  열 {len(r)} · 첫 행 {r["case"]}: ' + ' · '.join(f'{k}={r.get(k, "—")}' for k in keys))
EOF

if [ -n "$ONE" ]; then
  echo "══ 한 건 모드 — [4] 인계표 재생성은 건너뛴다 (설계행 전부가 있어야 선다).  위 시간 × 130 이 전 건 예상."
  exit $wrc
fi

echo "══ [4/5] 인계표 재생성 → docs/data/lhs_handover_$D.csv"
python3 scripts/lhs_design_dataset.py --export-handover "docs/data/lhs_handover_$D.csv" --harvest "$HARV" --webapp "$WAPP" \
    || { echo '⛔ 인계표 생성 거부 — 위 사유를 보고할 것 (같은 프레임 · 배치 미완 · 수확 세대)'; exit 1; }

echo "══ [5/5] 묶음 → $HOME/lhs_fill_$D.tar.gz"
tar czf "$HOME/lhs_fill_$D.tar.gz" "$HARV" "$WAPP" "docs/data/lhs_handover_$D.csv" "docs/data/lhs_handover_${D}_columns.tsv"
ls -la "$HOME/lhs_fill_$D.tar.gz"
echo '✓ 끝 — 이 묶음을 보내 주면 커밋하고 인계 README 를 채운다.'
