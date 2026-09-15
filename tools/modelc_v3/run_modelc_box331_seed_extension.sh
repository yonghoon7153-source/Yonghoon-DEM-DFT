#!/usr/bin/env bash
# =============================================================================
# modelc(LPSCl1.6) 3×3×1 400 ps — **시드 확장** (기존 {2,3,4} → +{5,6})
#
# 왜: C3(아레니우스 직선성)이 inconclusive 로 HOLD 다. ΔEa 점추정 −0.0339 eV 는 허용영역
#   ±0.050 **안**인데 CI95 하단 −0.0539 만 경계를 0.0039 eV 넘는다. CI 를 20 % 좁히면
#   들어온다 → 시드 노이즈 ~1/√n 이면 3 → 5 시드.
#
# ⛔ **사전등록이 먼저다.** db/properties/modelc_box331_seed_extension_prereg_2026_09_15.json
#   (판정 규칙 A/B/C 를 결과 보기 전에 박았다) · 결정 D-2026-09-15-modelc-box331-seed-extension.
#   ⛔ 예산은 **6런**이다. 결과가 애매해도 7번째 시드를 던지지 않는다 — 그것이 '통과할 때까지
#   돌리기' 다.
#
# ⛔ **이 스크립트가 못 하는 것**
#   · 새 시드의 **자격**을 판정하지 않는다. C1·C2(창별 plateau, 상대산포 ≤10 %)는 돌린 뒤
#     `msd_diffusive_check.py --mto` 가 따로 본다 — 새 시드라고 봐주지 않는다(s3/600 과 같은 잣대).
#   · lpsocl 을 건드리지 않는다. lpsocl 마감(비준됨)의 재개 조건에 시드 추가가 없다.
#   · 기존 s2·s3·s4 를 다시 돌리지 않는다(드라이버가 msd.json 있는 곳을 건너뛰지만, 여기서는
#     애초에 새 디렉터리 s5·s6 만 쓴다).
#
# ⚠ **실행모드는 turbo 로 고정**한다. 기존 9런이 turbo 였고, 한 캠페인 안에서 모드를 섞으면
#   그 묶음을 한 표에 못 쓴다(드라이버 주석 · uma_turbo_equivalence_2026_09_11.json).
#   드라이버가 실제 모드를 ensemble_results.json 의 uma_inference_mode 에 적으므로 기계로 확인한다.
# =============================================================================
set -euo pipefail

REPO=${REPO:-$HOME/work/Yonghoon-DEM-DFT}
OUTROOT=${OUTROOT:-$HOME/work/runs/modelc_box331_400ps}
SEEDS=${SEEDS:-"5 6"}
V0XYZ=${V0XYZ:-$REPO/db/structures/modelc_relaxV0_3x3x1.xyz}
DRIVER=$REPO/tools/modelc_v3/disorder_ensemble_diffusion.py
LOG=${LOG:-$HOME/logs/modelc_box331_seed_extension.log}

# ── 가드 1: 중복 실행 (flock — pgrep 은 tmux 래퍼까지 세서 자기 자신에 걸린다) ──
LOCK=${LOCK:-/tmp/modelc_box331_seed_extension.lock}
exec 9>"$LOCK" || { echo "⛔ 락 파일을 못 연다: $LOCK"; exit 1; }
command -v flock >/dev/null 2>&1 && { flock -n 9 || {
  echo "⛔ 이미 도는 것이 있다 (flock $LOCK) — 중복 실행 중단"; exit 0; }; }

# ── 가드 2: 여기가 그 repo 인가 · 구조가 그 구조인가 ──────────────────────────
#   ⛔ 못 읽으면 **시작하지 않는다**. 경로를 추측해서 엉뚱한 셀을 돌리는 것이
#      이 repo 가 반복해 물린 자리다(조용히 틀린 경로).
[ -f "$DRIVER" ] || { echo "⛔ 드라이버가 없다: $DRIVER  (REPO= 로 지정하라)"; exit 1; }
[ -f "$V0XYZ" ]  || { echo "⛔ 구조가 없다: $V0XYZ"; exit 1; }
NAT=$(head -1 "$V0XYZ" | tr -d '[:space:]')
[ "$NAT" = "558" ] || { echo "⛔ 원자 수가 558 이 아니다($NAT) — 3×3×1 셀이 아니다"; exit 1; }

# ── 가드 3: 기존 런과 **같은 조건인가** (verified-carry) ──────────────────────
#   기존 s2 의 run_meta.json 을 읽어 구조·온도·길이·창·실행모드를 대조한다.
#   못 읽으면 경고만 하고 계속 간다(첫 실행일 수 있다). 읽었는데 **다르면 멈춘다**.
REF=$OUTROOT/s2/run_meta.json
if [ -f "$REF" ]; then
  python3 - "$REF" "$V0XYZ" <<'PY' || exit 1
import json, sys, os
ref, v0 = sys.argv[1], sys.argv[2]
m = json.load(open(ref, encoding="utf-8"))
want = {"temperatures": [600, 800, 1000], "prod_ps": 400.0, "equilib_ps": 5.0,
        "fit_window_ps": [2.0, 50.0], "save_traj": True,
        "uma_model": "uma-s-1p1", "uma_inference_mode_requested": "turbo"}
bad = []
for k, v in want.items():
    got = m.get(k)
    if isinstance(v, list) and isinstance(got, list):
        ok = [float(x) for x in got] == [float(x) for x in v]
    elif isinstance(v, float):
        ok = got is not None and float(got) == v
    else:
        ok = got == v
    if not ok:
        bad.append(f"  {k}: 기존 {got!r} ≠ 이 스크립트 {v!r}")
if os.path.basename(str(m.get("v0_xyz", ""))) != os.path.basename(v0):
    bad.append(f"  v0_xyz: 기존 {m.get('v0_xyz')} ≠ {v0}")
if bad:
    print("⛔ 기존 런과 조건이 다르다 — 시드 확장이 아니라 다른 계산이 된다:")
    print("\n".join(bad)); raise SystemExit(1)
print(f"  ✓ 기존 s2 와 조건 일치 (n_atoms {m.get('n_atoms')} · supercell {m.get('supercell')})")
PY
else
  echo "  ⚠ $REF 를 못 읽었다 — 대조 없이 진행한다 (첫 실행이면 정상)"
fi

mkdir -p "$(dirname "$LOG")"
echo "REPO   = $REPO"
echo "V0     = $V0XYZ  ($NAT atoms)"
echo "OUT    = $OUTROOT/s{$SEEDS}"
echo "seeds  = $SEEDS   (드라이버가 온도별로 base+int(T) 로 갈라 쓴다)"
echo "예산   = 6런 × ~9.5 h ≈ 57 h  ⛔ 7번째 시드는 없다"
echo ""

cd "$REPO"                       # 드라이버가 상대경로를 부른다
for S in $SEEDS; do
  OUT=$OUTROOT/s${S}
  if [ -f "$OUT/ensemble_results.json" ]; then
    echo "  ✓ s${S} 이미 끝나 있다 — 건너뜀 ($OUT)"; continue
  fi
  echo "===================== modelc box331 seed ${S} ====================="
  python3 "$DRIVER" \
    --v0_xyz "$V0XYZ" --label modelc \
    --temperatures 600 800 1000 \
    --disorder_levels 0.0 --n_configs 1 \
    --equilib_ps 5 --prod_ps 400 \
    --timestep_fs 2 --friction 0.02 \
    --save_fs 100 --fit_window_ps 2 50 \
    --uma_model uma-s-1p1 --uma_task omat --save_traj --turbo \
    --seed "${S}" --out_root "$OUT"
done

echo ""
echo "===================== 끝난 뒤 (분석은 별도) ====================="
echo "  # ① 실행모드가 정말 turbo 였나 — 섞이면 이 묶음을 한 표에 못 쓴다"
echo "  grep -ah uma_inference_mode $OUTROOT/s*/ensemble_results.json"
echo "  # ② 새 시드의 자격 (C1·C2) — 새 시드라고 봐주지 않는다"
echo "  python3 tools/ionic/msd_diffusive_check.py --mto \\"
echo "      --glob '$OUTROOT/s*/d0.00_cfg0/T*/msd.json'"
echo "  # ③ C3 재판정은 자격 통과분만 넣어서 arrhenius_compat.py 로"
echo "  ⛔ 판정 규칙 A/B/C 는 사전등록 카드 §3 에 있다 — 결과를 보고 고르지 않는다."
