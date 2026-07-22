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

# ② SC ΔV 스윕 앵커 (캘리브 곡선 — 2점→5점, reflow 일반화를 넓은 충전깊이서 검증; 적대리뷰 stats#1
#    '앵커 2점 too few' 선제 해소).  Kondrakov −5.1 ↔ Yun/Kang −5.9 를 −4.5..−6.3 로 확장.
#    poly 부호 = expand(외피 팽창) 고정 = A-1/M3 정합 (ledger --poly-mode expand-void 와 짝).
#    ★비용: 각 스윕점 = 풀 MPM 압밀 1회(~10분/384).  빠른 첫 확인만이면 SWEEP를 "-0.051 -0.059"로 줄여.
SWEEP="${A1_DVSC_SWEEP:--0.045 -0.051 -0.055 -0.059 -0.063}"    # env로 override 가능
_dbond_args=("$OUT/m_N0.json"); _i=1
for dv in $SWEEP; do
  lab="sc${dv#-}"                                              # 예: sc0.051
  run_one "$lab" --cycle-deform --cycle-n "$_i" --cycle-dv-sc "$dv" --cycle-dv-poly 0.059 --dv-pct-poly 0.30
  _dbond_args+=("$OUT/m_${lab}.json"); _i=$((_i+1))
done

echo "═══ 기하 debond/void (pristine 대비, SC ΔV 스윕) ═══"
python3 "$SCR/cycle_geom_debond.py" "${_dbond_args[@]}" --csv "$OUT/a1_debond.csv"

echo "═══ A-3 reflow 캘리브 (MPM 앵커 → ledger, 일반화+LOAO) ═══"
# 킷 스캐폴드(박스단위)로 atoms 재구성 → reflow 회귀 (충전앵커 전부 사용 = 진짜 LOAO)
python3 "$SCR/calibrate_ledger_reflow.py" \
  --am-scaffold "$KIT/am_scaffold.csv" --se-scaffold "$KIT/se_scaffold.csv" \
  --pristine "$OUT/m_N0.json" --charged "${_dbond_args[@]:1}" \
  --out "$OUT/a3_reflow_calib.json" \
  || echo "   (캘리브 스킵 — 위 오류 확인)"

echo
echo "✅ 완료 → $OUT/  (m_*.json 앵커, a1_debond.csv 기하손실 곡선, a3_reflow_calib.json 캘리브)"
echo "   ⚠ 충전상태(가역) — 영구 fade 아님.  ★reflow=metric/law 정합 계수(재유동 아님, 적대리뷰 철회);"
echo "     metric_split_check.py 로 지표차 분해 필수.  같은-지표선 ledger≈MPM(reflow 불필요).  docs/a3_reflow_calibration.md."
