#!/usr/bin/env bash
# A-1 MPM cycle-deform 앵커 생성기 (GPU 박스 전용) — real_degrading_electrode_design §3 A-1 / §5 step(iv).
#
# 기존 production 스캐폴드 압밀(mpm3d_compaction --am-scaffold --se-dump)에 --cycle-deform 를 얹어
# '충전-상태 재변형 앵커'를 만들고, cycle_geom_debond.py 로 pristine 대비 기하 debond/void 를 뽑는다.
#
# ⚠ 가역/비가역 (적대리뷰 electrochem#1/물리): 여기 ΔV 는 '충전-상태'(방전서 되돌아가는 가역 SOC
#    breathing)라 앵커 = 영구 fade 가 아니라 '충전상태 스냅샷'.  ΔV 는 SOC 스윙이라 N 따라 안 커짐 →
#    ★진짜 N-궤적은 v1 이 못 냄★ (반복-사이클 소성누적 = v2, 또는 N→ΔV 매핑 = ledger ASSUMED-FORM).
#    그래서 v1 의 정직한 산출 = pristine + 충전앵커 1점(설계 step iv '거친 MPM 앵커 1점') + ΔV-민감도.
#
# 사용:
#   bash scripts/gen_a1_anchors.sh <KIT_DIR> <SCR_DIR> <box_x> <n_grid> [OUT_DIR]
#     KIT_DIR  = am_scaffold.csv + se_scaffold.csv 가 있는 킷 폴더 (webapp 킷 or docs/data 사본)
#     SCR_DIR  = scripts 폴더 (mpm3d_compaction.py, cycle_geom_debond.py 위치)
#     box_x    = LIGGGHTS 측면 박스 (킷 run_mpm.sh 의 --lateral-box 값; real_14=0.05)
#     n_grid   = 격자 (킷 run_mpm.sh 의 --n-grid; 384 or 512)
# 예 (real_14 스캐폴드, docs/data 사본 사용):
#   bash scripts/gen_a1_anchors.sh docs/data scripts 0.05 384 a1_anchors
#   (docs/data 의 real14_am_scaffold.csv → am_scaffold.csv 로 심링크/사본 필요:
#     ln -sf real14_am_scaffold.csv docs/data/am_scaffold.csv;
#     ln -sf real14_se_scaffold.csv docs/data/se_scaffold.csv)
set -euo pipefail

KIT="${1:?KIT_DIR (am_scaffold.csv/se_scaffold.csv)}"
SCR="${2:?SCR_DIR (scripts)}"
BOX="${3:?box_x (--lateral-box)}"
NG="${4:?n_grid}"
OUT="${5:-a1_anchors}"
mkdir -p "$OUT"

# production 표준 물성(2026 lock): E_SE=1.53, ν=0.49, target=0.30, hold protocol, periodic RVE.
COMMON=(--am-scaffold "$KIT/am_scaffold.csv" --se-dump "$KIT/se_scaffold.csv" --periodic
        --lateral-box "$BOX" --n-grid "$NG" --arch cuda --gpu-mem 28 --protocol hold --frames 150
        --e-se 1.53 --nu-se 0.49 --target-gpa 0.30)

run_one() {  # $1=label  $2..=extra flags
  local lab="$1"; shift
  echo "═══ A-1 앵커: $lab ═══"
  python3 "$SCR/mpm3d_compaction.py" "${COMMON[@]}" "$@" \
    --save-metrics "$OUT/m_${lab}.json" \
    || { echo "❌ $lab 실패 — 위 트레이스 확인"; exit 1; }
}

# ① pristine (N=0, --cycle-deform 없음 = 진짜 무변형 기저)
run_one N0

# ② 충전 앵커 (설계 step iv '거친 MPM 앵커 1점'): SC −5.1%(Kondrakov) 수축 / poly +5.9%×0.30 팽창.
#    poly 부호 = expand(외피 팽창) = A-1/M3 정합 (ledger --poly-mode expand-void 와 짝).
run_one charged --cycle-deform --cycle-n 1 --cycle-dv-sc -0.051 --cycle-dv-poly 0.059 --dv-pct-poly 0.30

# ③ ΔV-민감도 (선택): 더 깊은 충전 −5.9%(Yun/Kang) — N-궤적 아님, ΔV 축 스윕(설계 §6 미결1).
run_one charged_deep --cycle-deform --cycle-n 2 --cycle-dv-sc -0.059 --cycle-dv-poly 0.059 --dv-pct-poly 0.30

echo "═══ 기하 debond/void (pristine 대비) ═══"
python3 "$SCR/cycle_geom_debond.py" \
  "$OUT/m_N0.json" "$OUT/m_charged.json" "$OUT/m_charged_deep.json" \
  --csv "$OUT/a1_debond.csv"

echo
echo "✅ 완료 → $OUT/  (m_*.json = 앵커 metrics, a1_debond.csv = 기하 debond/void 표)"
echo "   ⚠ 이 debond/void 는 '충전상태(가역)' — 영구 fade 아님.  ledger 캘리브(A-3)에서"
echo "     --mpm-anchor 로 물려 {δcr,ε,rewet_frac} 회귀 (G_c 제외); 비가역화 판정은 그쪽."
