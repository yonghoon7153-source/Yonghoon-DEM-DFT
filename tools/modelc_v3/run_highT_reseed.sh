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
# ⚠ 이 가드는 **재실행 함정** 방지다 — COLLECT_ONLY(수집 전용)는 traj 없는
#   구판 트리에서도 정당하므로 건너뛴다.
if [ -d "$OUTROOT" ] && [ "${COLLECT_ONLY:-0}" != "1" ]; then
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

# ⭐ 2026-08-23 — 온도·생산시간을 env 로 받는다. 헤더는 "600K is already 3-seeded for
#   **both**" 라고 단언했지만 **modelc 쪽 실물이 없었다** (b2o3 만 b2o3_600K_reseed_errorbar.csv
#   로 3시드가 있고, modelc 는 D_600 = 7.901e-06 단일값 하나뿐이다).
#   그래서 600 K 를 이 스크립트로 돌릴 수 있어야 한다.
#   ⚠ 600 K 는 **200 ps** 다 — 기존 600 K 런이 200 ps 였고(요청대장 §6-3), 100 ps 로 줄이면
#     예측 홉 수가 13.9 → ~7 로 반토막나 β 게이트가 경계로 떨어진다.
#     TEMPS=600 을 줄 때 PROD_PS=200 을 같이 주지 않으면 아래에서 막는다.
if [ "${TEMPS:-}" = "600" ] && [ "${PROD_PS:-100}" -lt 200 ]; then
  echo "⛔ 600 K 인데 PROD_PS=${PROD_PS:-100} ps 다. 600 K 는 200 ps 규약이다"
  echo "   (100 ps 면 예측 홉 13.9 → ~7 로 반토막, β 게이트가 경계로 떨어진다)"
  echo "   PROD_PS=200 TEMPS=600 ... 로 다시 실행하라. 의도한 것이면 FORCE_SHORT=1 을 붙여라."
  [ "${FORCE_SHORT:-0}" = "1" ] || exit 1
fi
echo "OUT=$OUTROOT  DEVICE=$DEVICE  SYSTEMS=$SYSTEMS  TEMPS=${TEMPS:-800 1000}  PROD_PS=${PROD_PS:-100} ps"
echo "⚠ 재실행분은 **새 런**이다 — D 와 beta 를 이 궤적들에서 같이 뽑아 Ea 를 다시 적합할 것."
[ "$SYSTEMS" = "b2o3 modelc" ] || \
  echo "⚠ 계를 갈라 돌린다 ($SYSTEMS) — 나머지 계를 다른 서버에서 돌리고 **합친 뒤** Ea 재적합."
# ── COLLECT_ONLY / env 함정 (2026-08-25 실측) ────────────────────────────────
#   드라이버는 **전부 resume-skip 인 경우에도** fairchem 을 import 한다 — (base)
#   env 에서 "수집만" 하려던 호출이 ModuleNotFoundError 로 죽고, set -e 라 collect
#   까지 못 갔다. ① COLLECT_ONLY=1 이면 드라이버 루프를 건너뛰고 수집만 한다.
#   ② 아니면 fairchem 존재를 먼저 확인하고 명확한 메시지로 죽는다.
if [ "${COLLECT_ONLY:-0}" != "1" ]; then
  python3 - <<'PYCHK' || { echo "⛔ fairchem 없음 — 'conda activate uma' 후 실행하거나, 수집만 원하면 COLLECT_ONLY=1"; exit 1; }
import importlib.util, sys
sys.exit(0 if importlib.util.find_spec("fairchem") else 1)
PYCHK
for SYS in $SYSTEMS; do
  for S in 2 3 4; do
    echo "===================== $SYS  ${TEMPS:-800 1000} K (${PROD_PS:-100} ps)  reseed s${S} ====================="
    python3 "$DRIVER" \
      --v0_xyz "${V0[$SYS]}" --label "$SYS" \
      --out_root "$OUTROOT/${SYS}/s${S}" \
      --disorder_levels 0.0 --n_configs 1 \
      --temperatures ${TEMPS:-800 1000} \
      --equilib_ps 5 --prod_ps ${PROD_PS:-100} --timestep_fs 2.0 --friction 0.02 \
      --save_fs 100 --fit_window_ps 2 50 --seed ${S} --save_traj \
      --uma_model uma-s-1p1 --uma_task omat --device "$DEVICE"
  done
done
fi

echo ""; echo "===================== collect (msd.json 경로 기반 — 위치 인덱스 아님) ====================="
# ⛔⛔ 2026-08-25 2차 수정 — TEMPS 인덱스 매핑도 틀렸다 (gabia 실측):
#   시드별 실행 이력이 달라(s2/s3 는 600 추가 패스, s4 는 800/1000 만)
#   ensemble_results.json 의 D_per_T 가 **시드마다 길이·순서가 다르다**
#   (파일은 마지막 드라이버 호출만 반영). 600 행에 s4 의 800 값이 끼었다.
#   위치 기반은 원리적으로 불안전 — **msd.json 경로의 T<K> 에서 라벨을 읽는다.**
python3 - "$OUTROOT" "$SYSTEMS" <<'PY'
import glob, json, os, re, statistics as st, sys
root, systems = sys.argv[1], (sys.argv[2].split() if len(sys.argv) > 2 and sys.argv[2].strip()
                              else ["b2o3", "modelc"])
for sysn in systems:
    per_T = {}
    for m in sorted(glob.glob(os.path.join(root, sysn, "s*", "d*", "T*", "msd.json"))):
        mt = re.search(r"T(\d+)[/\\]msd\.json$", m)
        if not mt:
            continue
        T = int(mt.group(1))
        try:
            D = json.load(open(m)).get("D_Li_cm2_s")
        except (OSError, ValueError) as e:
            print(f"  ⛔ {m}: 읽기 실패 {e}")
            continue
        seed = re.search(r"[/\\](s\d+)[/\\]", m)
        if D:
            per_T.setdefault(T, []).append((seed.group(1) if seed else "?", D))
    for T in sorted(per_T):
        vals = per_T[T]
        ds = [d for _, d in vals]
        m_ = sum(ds) / len(ds)
        sd = st.pstdev(ds) if len(ds) > 1 else 0.0
        who = " ".join(f"{s}={d:.3e}" for s, d in vals)
        print(f"{sysn:7s} {T}K (n={len(ds)}): {who}   mean={m_:.3e} +/- {sd:.1e}"
              f" ({(sd / m_ * 100) if m_ else 0:.0f}%)")
    if not per_T:
        print(f"{sysn}: msd.json 없음")
PY
echo ""
echo "NEXT: 위 mean 줄을 그대로 붙여넣을 것 (계 × TEMPS 조합 수만큼) -> 600 K 3시드와"
echo "3-seed 600K to give FULLY symmetric Ea/sigma + resolved ratio + final CSV/fig."
