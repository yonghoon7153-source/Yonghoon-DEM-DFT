#!/usr/bin/env bash
# =============================================================================
# box331 400 ps — **시드 확장** (기존 {2,3,4} → +{5,6}) · SYS=modelc | lpsocl
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
# ── 동시 실행 (2026-09-15, 1저자 질문 "합쳐서 돌리면 안돼?") ─────────────────
#   ✅ **물리적으로 안전하다.** 두 계는 서로 독립이고, 같은 GPU 를 나눠 써도 힘 계산은
#      안 바뀐다 — 느려질 뿐이다. 게이트가 보는 것은 구조·온도·창·프로토콜·실행모드이지
#      "GPU 를 혼자 썼나" 가 아니다.
#   ⚠ **그런데 이득이 있는지는 재 봐야 안다.** 한 런이 GPU 를 이미 포화시키면 둘을 띄워도
#      합계 처리량이 거의 안 늘고, 오히려 컨텍스트 전환으로 느려질 수 있다.
#      ⛔ 추측하지 말고 `nvidia-smi` 로 **이용률(%)과 VRAM** 을 본다:
#        · util 이 85 % 미만이고 VRAM 여유가 런 하나치 이상 → 하나 더 띄울 값어치가 있다
#        · util 이 95 % 이상 → 직렬로 두는 편이 낫다
#   락이 (계 × 시드집합) 단위라 아래 넷까지 따로 띄울 수 있다:
#     SYS=modelc SEEDS=5 · SYS=modelc SEEDS=6 · SYS=lpsocl SEEDS=5 · SYS=lpsocl SEEDS=6
#   ⚠ 넷을 한꺼번에 띄우기 전에 **하나 띄우고 재 보는 것**이 순서다.
#
# ⚠ **실행모드는 turbo 로 고정**한다. 기존 9런이 turbo 였고, 한 캠페인 안에서 모드를 섞으면
#   그 묶음을 한 표에 못 쓴다(드라이버 주석 · uma_turbo_equivalence_2026_09_11.json).
#   드라이버가 실제 모드를 ensemble_results.json 의 uma_inference_mode 에 적으므로 기계로 확인한다.
# =============================================================================
set -euo pipefail

# SYS=modelc (기본) | lpsocl
#   ⛔ **lpsocl 은 1저자 비준 전에 돌리지 않는다** — 비준된 마감을 여는 것이라 개정문이 필요하다
#      (db/properties/lpsocl_box331_seed_extension_amendment_2026_09_15.json · R5 신설, proposed).
#      아래 가드가 `LPSOCL_RATIFIED=1` 없이는 멈춘다.
SYS=${SYS:-modelc}
REPO=${REPO:-$HOME/work/Yonghoon-DEM-DFT}
case "$SYS" in
  modelc) _XYZ=modelc_relaxV0_3x3x1.xyz; _NAT=558; _ROOT=modelc_box331_400ps; _TURBO=--turbo ;;
  lpsocl) _XYZ=lpsocl_relaxV0_3x3x1.xyz; _NAT="";  _ROOT=lpsocl_box331_400ps; _TURBO=""      ;;
  *) echo "⛔ SYS 는 modelc | lpsocl 이다 (받은 값: $SYS)"; exit 1 ;;
esac
# ⚠ 실행모드가 계마다 **다르다** — modelc 9런은 turbo, lpsocl 9런은 기본 모드다.
#   섞으면 그 묶음을 한 표에 못 쓴다. 그래서 계별로 고정하고, 아래 가드 ③ 이 기존 런과 대조한다.
# ── 가드 0: **원장이 허락했나** (fail-closed) ────────────────────────────────
#   ⛔ 2026-09-15 — 처음엔 `LPSOCL_RATIFIED=1` 이라는 **사람이 치는 플래그**로 막았다.
#      그건 사람의 기억을 믿는 것이고, 비준이 취소돼도 플래그는 그대로 남는다.
#      판정은 **원장이 한다** — decisions.json 을 직접 읽어 active + ratified 인지 본다.
#   ⚠ 못 읽으면 **멈춘다**("못 읽음 ≠ 금지 없음"). 원장이 없는 기계에서는 안 돈다.
_DEC_ID=$(case "$SYS" in
  modelc) echo D-2026-09-15-modelc-box331-seed-extension ;;
  lpsocl) echo D-2026-09-15-lpsocl-box331-seed-extension-r5 ;;
esac)
python3 - "$REPO/db/governance/decisions.json" "$_DEC_ID" <<'PY' || exit 1
import json, sys
path, did = sys.argv[1], sys.argv[2]
try:
    rows = json.load(open(path, encoding="utf-8"))["decisions"]
except Exception as e:                                          # noqa: BLE001
    print(f"⛔ 원장을 못 읽었다 ({type(e).__name__}) — 못 읽음은 '금지 없음' 이 아니다: {path}")
    raise SystemExit(1)
d = next((r for r in rows if r.get("id") == did), None)
if d is None:
    print(f"⛔ 원장에 {did} 가 없다 — 사전등록 없이 돌리는 것이다"); raise SystemExit(1)
st = d.get("decision_state") or d.get("status")
rat = (d.get("ratification") or {}).get("state")
if st != "active" or rat != "ratified":
    print(f"⛔ {did} 는 아직 실행 자격이 없다 (state={st} · ratification={rat}).")
    print("   1저자 비준이 원장에 기록돼야 돈다. 카드:", d.get("card"))
    raise SystemExit(1)
print(f"  ✓ 원장 허가 {did} (active · ratified {(d.get('ratification') or {}).get('timestamp','')})")
PY
OUTROOT=${OUTROOT:-$HOME/work/runs/$_ROOT}
SEEDS=${SEEDS:-"5 6"}
V0XYZ=${V0XYZ:-$REPO/db/structures/$_XYZ}
DRIVER=$REPO/tools/modelc_v3/disorder_ensemble_diffusion.py
LOG=${LOG:-$HOME/logs/${SYS}_box331_seed_extension.log}

# ── 가드 1: 중복 실행 (flock — pgrep 은 tmux 래퍼까지 세서 자기 자신에 걸린다) ──
# ⚠ 락은 **(계 × 시드집합)** 단위다. 같은 계라도 `SEEDS=5` 와 `SEEDS=6` 을 따로 띄울 수 있게
#   이름에 시드를 넣는다 — 계 단위로만 잠그면 병렬화를 스크립트가 막아 버린다.
LOCK=${LOCK:-/tmp/${SYS}_box331_seed_ext_$(echo "$SEEDS" | tr -d " ").lock}
exec 9>"$LOCK" || { echo "⛔ 락 파일을 못 연다: $LOCK"; exit 1; }
command -v flock >/dev/null 2>&1 && { flock -n 9 || {
  echo "⛔ 이미 도는 것이 있다 (flock $LOCK) — 중복 실행 중단"; exit 0; }; }

# ── 가드 2: 여기가 그 repo 인가 · 구조가 그 구조인가 ──────────────────────────
#   ⛔ 못 읽으면 **시작하지 않는다**. 경로를 추측해서 엉뚱한 셀을 돌리는 것이
#      이 repo 가 반복해 물린 자리다(조용히 틀린 경로).
[ -f "$DRIVER" ] || { echo "⛔ 드라이버가 없다: $DRIVER  (REPO= 로 지정하라)"; exit 1; }
[ -f "$V0XYZ" ]  || { echo "⛔ 구조가 없다: $V0XYZ"; exit 1; }
NAT=$(head -1 "$V0XYZ" | tr -d '[:space:]')
if [ -n "$_NAT" ]; then
  [ "$NAT" = "$_NAT" ] || { echo "⛔ 원자 수가 $_NAT 이 아니다($NAT) — 3×3×1 셀이 아니다"; exit 1; }
else
  echo "  ⚠ $SYS 의 기준 원자 수를 스크립트가 모른다($NAT 로 진행) — 가드 ③ 이 기존 런과 대조한다"
fi

# ── 가드 3: 기존 런과 **같은 조건인가** (verified-carry) ──────────────────────
#   기존 s2 의 run_meta.json 을 읽어 구조·온도·길이·창·실행모드를 대조한다.
#   못 읽으면 경고만 하고 계속 간다(첫 실행일 수 있다). 읽었는데 **다르면 멈춘다**.
REF=$OUTROOT/s2/run_meta.json
if [ -f "$REF" ]; then
  # ⭐ 2026-09-18 — 가드를 **파일로 뺐다**. heredoc 안에서는 시험을 칠 수 없고,
  #   이 가드에 예외조항(옛 판본 run_meta)을 넣게 되어 음성 시험이 필수가 됐다.
  python3 "$REPO/tools/modelc_v3/check_seed_ext_meta.py" \
      "$REF" "$V0XYZ" "${_TURBO:+turbo}" || exit 1
else
  echo "  ⚠ $REF 를 못 읽었다 — 대조 없이 진행한다 (첫 실행이면 정상)"
fi

mkdir -p "$(dirname "$LOG")"
echo "SYS    = $SYS   (실행모드 ${_TURBO:-default})"
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
  echo "===================== $SYS box331 seed ${S} ====================="
  python3 "$DRIVER" \
    --v0_xyz "$V0XYZ" --label modelc \
    --temperatures 600 800 1000 \
    --disorder_levels 0.0 --n_configs 1 \
    --equilib_ps 5 --prod_ps 400 \
    --timestep_fs 2 --friction 0.02 \
    --save_fs 100 --fit_window_ps 2 50 \
    --uma_model uma-s-1p1 --uma_task omat --save_traj $_TURBO \
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
