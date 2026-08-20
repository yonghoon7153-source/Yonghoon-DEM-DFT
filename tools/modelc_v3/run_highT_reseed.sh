#!/usr/bin/env bash
# =============================================================================
# High-T (800/1000 K) 3-seed reseed for BOTH systems -> SYMMETRIC error bars at
# all three temperatures, so the b2o3-vs-modelc sigma ratio gets a real bar.
#
# WHY: 600K is already 3-seeded for both (b2o3 & modelc ~1.04e-5, equal). The
# apparent b2o3 advantage sits at the SINGLE-seed 800K (ratio 1.57) / 1000K (1.19).
# High-T diffuses fast -> lower relative noise, so 3 seeds resolve it cheaply.
#
# Each driver call does --temperatures 800 1000 (seed derived per-T: base+int(T)),
# so 3 base seeds -> 3 independent trajectories at EACH of 800 and 1000 K.
# disorder 0.0 = canonical cell (b2o3_relaxV0 128-atom / modelc_V0_k663 62-atom).
# prod 100 ps is plenty: D uses only the (2,50) ps window -> identical to 200 ps,
# and matches the deck high-T length. GPU pw... err, GPU MLIP (uma-s-1p1 omat).
#
# ⛔⛔ 2026-08-20 (codex 3차 리뷰 / F9) — **--save_traj 가 빠져 있었다.**
#   disorder_ensemble_diffusion.py 는 그 플래그가 있어야 traj.xyz 를 쓴다. 그래서
#   2026-07-06/07 실행분(b2o3·modelc x 800/1000 K x s2/s3/s4 = 12 런)의 프레임이
#   디스크에 없고, **골격(비-Li) MSD 게이트를 소급으로 못 돌린다.**
#   같은 결함을 tools/ionic/run_arrhenius_6pt.sh L57-59 가 이미 적어두고 자기만
#   고쳤다(L183) — 이 러너는 안 고쳐졌다. 이제 붙인다 (런당 ~10 MB).
#
#   ⚠ 재실행은 **옛 궤적의 복원이 아니다.** 같은 시드여도 GPU 부동소수 연산 순서가
#   비결정적이고 MD 는 카오스계라 100 ps 뒤엔 다른 궤적이다. 따라서 재실행분에서
#   **D 와 beta 를 같이 뽑아 Ea 를 다시 적합**해야 한다 — 새 궤적의 beta 를 옛 Ea
#   0.199 에 붙이면 그것이 바로 F4(계보 오류)의 재발이다.
#   → b2o3 만 돌리지 말 것. 비교가 대칭이어야 하므로 modelc 도 같이 돈다(이 스크립트
#     기본값이 그렇다). 600 K 는 별도 런(200 ps)이라 현존분을 그대로 쓴다.
# =============================================================================
set -euo pipefail

REPO=${REPO:-$HOME/work/Yonghoon-DEM-DFT}          # kgy checkout
OUTROOT=${OUTROOT:-$HOME/work/runs/highT_reseed}
DEVICE=${DEVICE:-cuda}
DRIVER=$REPO/tools/modelc_v3/disorder_ensemble_diffusion.py

# system -> V0 structure (SAME cells as the deck anchors)
declare -A V0
V0[b2o3]=$REPO/db/structures/b2o3_relaxV0.xyz        # 128-atom
V0[modelc]=$REPO/db/structures/modelc_V0_k663.xyz    # 62-atom

# ── 가드 1: 중복 실행 (flock 만 쓴다) ────────────────────────────────────────
#   ⚠ pgrep 은 쓰지 않는다 — tmux/nohup 래퍼(`sh -c 'bash … | tee …'`)까지 세서
#     **자기 자신에 걸린다**. 2026-08-03 에 chain_gpu_release.sh 가 그 사고를 겪고
#     flock 으로 바꾼 선례가 있다 (그 파일 L34-37).
SELF=$(basename "$0")
LOCK=${LOCK:-/tmp/highT_reseed.lock}
exec 9>"$LOCK" || { echo "⛔ 락 파일을 못 연다: $LOCK"; exit 1; }
command -v flock >/dev/null 2>&1 && { flock -n 9 || {
  echo "⛔ 이미 도는 $SELF 가 있다 (flock $LOCK) — 중복 실행 중단"; exit 0; }; }

# ── 가드 2: resume 함정 (2026-08-20, F9 재실행용) ────────────────────────────
#   드라이버는 msd.json 이 있으면 그 (config,T) 를 **통째로 건너뛴다**(L202-207).
#   옛 OUTROOT 에 그대로 재실행하면 --save_traj 를 붙였어도 **전부 skip 되고
#   traj.xyz 는 영영 안 생긴다** — 그런데 화면은 정상 종료처럼 보인다.
#   그래서 여기서 즉사시킨다: msd.json 은 있는데 traj.xyz 가 없는 디렉터리가 하나라도
#   있으면 새 OUTROOT 를 쓰라고 알리고 멈춘다 (경고 후 계속 아님).
if [ -d "$OUTROOT" ]; then
  STALE=$(find "$OUTROOT" -name msd.json 2>/dev/null | while read -r m; do
            [ -f "$(dirname "$m")/traj.xyz" ] || echo "$m"; done | wc -l)
  if [ "$STALE" -gt 0 ]; then
    echo "⛔ $OUTROOT 에 '궤적 없는 msd.json' 이 ${STALE}개 있다 (2026-07 실행분)."
    echo "   여기에 재실행하면 드라이버가 전부 skip 해서 traj.xyz 가 안 생긴다."
    echo "   → 새 경로로 돌릴 것:  OUTROOT=\$HOME/work/runs/highT_reseed_traj $0"
    echo "   (옛 결과는 지우지 말 것 — Ea 0.199/0.197 의 원자료다.)"
    exit 1
  fi
fi

# ── 계 선택 (2026-08-20) ─────────────────────────────────────────────────────
#   기본은 둘 다 — b2o3 만 새 런으로 갈면 "새 런 b2o3 vs 옛 런 modelc" 비교가 되어
#   그것 자체가 계보 혼합이다. 다만 **두 서버에 나눠 돌릴 때**는 갈라야 하므로
#   SYSTEMS 로 고를 수 있게 한다 (예: kgy 는 b2o3, gabia 는 modelc).
#   ⚠ 나눠 돌렸으면 **양쪽 결과를 합친 뒤에** Ea 를 재적합할 것. 한쪽만 새 값으로
#     갈아끼우면 위의 계보 혼합이 그대로 재발한다.
SYSTEMS=${SYSTEMS:-"b2o3 modelc"}
for _s in $SYSTEMS; do
  case "$_s" in b2o3|modelc) : ;;
    *) echo "⛔ SYSTEMS='$SYSTEMS' 에 모르는 계가 있다: $_s (b2o3|modelc)"; exit 1 ;;
  esac
done

echo "OUT=$OUTROOT  DEVICE=$DEVICE  SYSTEMS=$SYSTEMS"
echo "⚠ 재실행분은 **새 런**이다 — D 와 beta 를 이 궤적들에서 같이 뽑아 Ea 를 다시 적합할 것."
[ "$SYSTEMS" = "b2o3 modelc" ] || \
  echo "⚠ 계를 갈라 돌린다 ($SYSTEMS) — 나머지 계를 다른 서버에서 돌리고 **합친 뒤** Ea 재적합."
for SYS in $SYSTEMS; do
  for S in 2 3 4; do
    echo "===================== $SYS  800/1000K  reseed s${S} ====================="
    python3 "$DRIVER" \
      --v0_xyz "${V0[$SYS]}" --label "$SYS" \
      --out_root "$OUTROOT/${SYS}/s${S}" \
      --disorder_levels 0.0 --n_configs 1 \
      --temperatures 800 1000 \
      --equilib_ps 5 --prod_ps 100 --timestep_fs 2.0 --friction 0.02 \
      --save_fs 100 --fit_window_ps 2 50 --seed ${S} --save_traj \
      --uma_model uma-s-1p1 --uma_task omat --device "$DEVICE"
  done
done

echo ""; echo "===================== collect (D_per_T[0]=800, [1]=1000) ====================="
python3 - "$OUTROOT" <<'PY'
import json, os, sys, statistics as st
root=sys.argv[1]
for sysn in ("b2o3","modelc"):
    for idx,T in ((0,800),(1,1000)):
        vals=[]
        for s in (2,3,4):
            p=os.path.join(root,sysn,f"s{s}","ensemble_results.json")
            try: vals.append(json.load(open(p))["levels"][0]["configs"][0]["D_per_T"][idx])
            except Exception as e: print(f"  ({sysn} s{s} {T}K miss: {e})")
        if vals:
            m=sum(vals)/len(vals); sd=st.pstdev(vals)
            print(f"{sysn:7s} {T}K: "+"  ".join(f"{v:.3e}" for v in vals)+f"   mean={m:.3e} +/- {sd:.1e} ({sd/m*100:.0f}%)")
PY
echo ""
echo "NEXT: paste the 8 lines (b2o3/modelc x 800/1000 means) -> I combine with the"
echo "3-seed 600K to give FULLY symmetric Ea/sigma + resolved ratio + final CSV/fig."
