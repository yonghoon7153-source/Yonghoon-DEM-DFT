#!/usr/bin/env bash
# SR-01 (option 2) — 같은 압밀 베드 위에서 STEP3 탄소 래스터만 바꿔 **Δσ_e 를 실측**한다.
#
#   arm A = 점 스탬프   (--step3-fibre-stamp point)   → mpm_payload_pointstamp.json
#   arm B = 선분 스탬프 (--step3-fibre-stamp segment) → mpm_payload_segstamp.json
#
# ★ 두 팔을 **이 스크립트가 직접** 돌린다 (run_mpm.sh 가 만든 mpm_payload.json 을 A 로
#   재활용하지 않는다).  그 payload 는 몇 시간 전 다른 env(MPM_PERIODIC_SIGMA 등)에서
#   돌았을 수 있고, 그러면 Δ 에 스탬프 아닌 것이 섞인다.  같은 프로세스·같은 env 에서
#   연달아 돌리면 두 팔은 **스탬프 하나만** 다르다 = 교란변수 0.
#   압밀(STEP1)은 다시 돌지 않는다 — 두 팔이 같은 se_dump.npy/fibre.npy 를 읽으므로
#   베드·섬유 시딩·난수가 바이트로 동일하다.
#   run_mpm.sh 의 원본 mpm_payload.json 은 **건드리지 않는다** (production 산출물 보존).
#
# ★ 재개 가능 (2026-08-11 실사고: arm A 가 5h55m 걸려 끝난 **직후** 터미널이 끊겨 arm B 가
#   시작조차 못 했다).  이미 **완전한** 팔은 건너뛴다 — 완전함은 파일 존재가 아니라
#   sr01_stamp_compare --check-arm 이 판정한다 (스탬프 도장 일치 · CG 수렴 · σ_e>0 ·
#   **backend 일치**).  느슨하면 불완전한 팔을 SKIP 해 Δ 가 조용히 거짓이 된다.
#   ⚠⚠ backend 를 왜 보는가: 킷 run_mpm.sh 는 이미 `--step3-gpu` 를 넘긴다 → cupy 를 깔면
#   다음 팔이 **자동으로 GPU** 가 되고, 그러면 "CPU 로 끝난 A 를 SKIP 하고 B 만 GPU" 라는
#   최악의 재개가 **기본 동작**이 된다.  그래서 지금 쓸 backend 를 먼저 탐지해 비교한다.
#
# 사용:
#   bash scripts/sr01_stamp_ab.sh <KIT_DIR> [RUN_DIR]
# 예 (V100) — ★ 반드시 터미널과 분리해서 돌린다 (한 팔이 몇 시간이다):
#   cd ~/Yonghoon-DEM-DFT/se_curve
#   setsid nohup bash ~/dem-sk/scripts/sr01_stamp_ab.sh kit_ps_7_3 \
#     > kit_ps_7_3/sr01_ab.log 2>&1 &
#   python3 ~/dem-sk/scripts/sr01_watch.py kit_ps_7_3        # 진행 확인
set -uo pipefail

KIT_IN="${1:-}"
[ -n "$KIT_IN" ] || { echo "사용: bash scripts/sr01_stamp_ab.sh <KIT_DIR> [RUN_DIR]"; exit 2; }
KIT="$(cd "$KIT_IN" 2>/dev/null && pwd)" || { echo "ABORT — 킷 폴더 없음: $KIT_IN"; exit 1; }
# ── 런 폴더 결정.  ⚠ latest_run 심링크가 **없어도 압밀은 끝나 있을 수 있다** ──────────
#   2026-08-11 실사고: 옛 코드가 그 경우 "먼저 압밀을 돌리세요 (~2h)" 라고 안내했는데
#   베드(se_dump.npy)는 멀쩡히 있었다 — 안내대로 했으면 2시간을 헛되이 다시 돌았다.
#   심링크의 부재는 **압밀의 부재가 아니다**.  압밀 산출물 자체로 판정한다.
if [ -n "${2:-}" ]; then
  RUN_IN="$2"
elif [ -e "$KIT/latest_run" ]; then
  RUN_IN="$KIT/latest_run"
else
  CAND=""; NCAND=0; CANDLIST=""
  for d in "$KIT"/run_*; do
    [ -f "$d/se_dump.npy" ] || continue
    CAND="$d"; NCAND=$((NCAND + 1)); CANDLIST="$CANDLIST        $d
"
  done
  if [ "$NCAND" = 0 ]; then
    echo "ABORT — 압밀된 런이 없습니다 ($KIT/run_*/se_dump.npy 를 못 찾음)."
    echo "        먼저 압밀을 돌리세요:  bash $KIT/run_mpm.sh   (~2h)"; exit 1
  elif [ "$NCAND" = 1 ]; then
    RUN_IN="$CAND"
    echo "[sr01] latest_run 심링크가 없어 압밀된 런을 직접 씁니다: $(basename "$CAND")"
  else
    echo "ABORT — 압밀된 런이 $NCAND 개입니다.  어느 것인지 두 번째 인자로 주세요:"
    printf '%s' "$CANDLIST"; exit 1
  fi
fi
[ -e "$RUN_IN" ] || { echo "ABORT — 런 폴더가 없습니다: $RUN_IN"; exit 1; }
RUN="$(cd "$RUN_IN" && pwd)"
SCR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -z "${VIRTUAL_ENV:-}" ] && [ -z "${MPM_NO_VENV:-}" ]; then
  for _v in "$SCR/../venv" "$SCR/../.venv" "$HOME/Yonghoon-DEM-DFT/venv"; do
    [ -f "$_v/bin/activate" ] && { . "$_v/bin/activate"; echo "[venv] $_v"; break; }
  done
fi

# ── 압밀 산출물 확인.  없으면 멈춘다 (payload 만 돌리면 STALE se_dump 를 읽는다) ──
for f in se_dump.npy fibre.npy; do
  [ -f "$RUN/$f" ] || { echo "ABORT — $RUN/$f 가 없습니다."; \
                        echo "        선분 스탬프는 --fibre 없이는 못 돕니다 (조용히 점으로 되돌아감)."; exit 1; }
done

# ── run_mpm.sh 의 payload 호출부를 그대로 뽑아 스탬프/--out 만 바꾼다 ──
#   ⚠ run_mpm.sh 가 안내하는 sed 한 줄은 틀렸다 (범위가 다시 열려 파일 끝까지 뱉는다 →
#     arm B 가 latest_run 심링크를 갈아치우고 완료 마커를 찍는다).  추출은 파이썬 쪽에
#     테스트와 함께 있다: sr01_stamp_compare.extract_payload_cmd (selftest 14–20).
cd "$RUN"
PSIG=(); [ "${MPM_PERIODIC_SIGMA:-0}" = "1" ] && PSIG=(--periodic)
echo "[sr01] PSIG=${PSIG[*]:-（없음）}   (두 팔에 **동일**하게 적용됨)"

# ── 지금 돌면 실제로 어느 backend 인가 ────────────────────────────────────────────────
#   ⚠ 탐지는 **솔버가 쓰는 경로 그대로** 찔러야 한다.  2026-08-12 실사고: 처음엔
#   `cp.zeros(1).sum()` 으로 쟀는데 그건 cuBLAS/cuSPARSE 를 건드리지 않는다 → "gpu" 라고
#   답했지만 실제 솔브는 `ImportError: Failure finding "libcublasLt.so"` 로 **매번 CPU 로
#   폴백**했다 (cupy 는 깔렸지만 CUDA 수치 라이브러리가 없는 상태).  "import 되니 되겠지"
#   에서 한 걸음 더 갔을 뿐, 여전히 가정이었다.  이제 cupyx sparse CG 를 실제로 1회 돈다.
probe_backend() {
  grep -q -- '--step3-gpu' "$KIT/run_mpm.sh" || { echo cpu; return; }
  local out
  out=$(python3 -c "
try:
    import cupy as cp
    import cupyx.scipy.sparse as cxs
    from cupyx.scipy.sparse.linalg import cg          # ← step3_sigma._solve_cg 와 동일 경로
    A = cxs.diags(cp.ones(4, dtype='float64')).tocsr()
    b = cp.ones(4, dtype='float64')
    try:
        cg(A, b, rtol=1e-8, maxiter=2)
    except TypeError:
        cg(A, b, tol=1e-8, maxiter=2)
    print('gpu')
except Exception:
    print('cpu')" 2>/dev/null)
  case "$out" in gpu) echo gpu ;; *) echo cpu ;; esac
}
EXPECT="$(probe_backend)"
echo "[sr01] backend 예상: $EXPECT   (두 팔에 **동일**하게 적용된다)"

run_arm() {                       # $1 = point|segment   $2 = out 파일명
  local stamp="$1" out="$2" sh="payload_${1}stamp.sh" why=""
  # ── 재개: 이미 완전하고 backend 도 같은 팔은 건너뛴다 (6시간을 다시 돌지 않는다) ──
  if [ -s "$out" ]; then
    if why=$(python3 "$SCR/sr01_stamp_compare.py" --check-arm "$out" --stamp "$stamp" \
                     --expect-backend "$EXPECT"); then
      echo "[sr01] ── arm ${stamp} SKIP (재개) — 이미 완전합니다: $out"
      return 0
    fi
    local keep="${out%.json}.superseded.json" n=1
    while [ -e "$keep" ]; do keep="${out%.json}.superseded${n}.json"; n=$((n + 1)); done
    mv -f "$out" "$keep"          # ★ 덮어쓰지 않는다 — 옛 팔도 교차검증에 쓸 수 있다
    echo "[sr01] ── arm ${stamp} 다시 돕니다 — $why"
    echo "[sr01]    옛 결과 보존: $(basename "$keep")"
  fi
  python3 "$SCR/sr01_stamp_compare.py" --extract-payload "$KIT/run_mpm.sh" \
          --stamp "$stamp" --out-name "$out" > "_$sh" || return 1
  { echo 'set -uo pipefail'; echo "KIT=\"$KIT\""; echo "SCR=\"$SCR\"";
    echo "PSIG=(${PSIG[*]:-})"; cat "_$sh"; } > "$sh"
  rm -f "_$sh"
  echo "[sr01] ── arm ${stamp} → $out"
  bash "$sh" || { echo "[sr01] arm ${stamp} FAILED — 위 트레이스"; return 1; }
}

run_arm point   mpm_payload_pointstamp.json || exit 1
run_arm segment mpm_payload_segstamp.json   || exit 1

echo
python3 "$SCR/sr01_stamp_compare.py" \
        "$RUN/mpm_payload_pointstamp.json" "$RUN/mpm_payload_segstamp.json" \
        --label "$(basename "$KIT")" --csv "$RUN/sr01_stamp_ab.csv" || exit 1
echo
echo "[sr01] 회수할 것: $RUN/sr01_stamp_ab.csv + mpm_payload_{point,seg}stamp.json"
echo "[sr01] (run_mpm.sh 의 mpm_payload.json 은 그대로 — production 산출물 보존)"
