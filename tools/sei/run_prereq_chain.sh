#!/usr/bin/env bash
# =============================================================================
# li3nd NEB 선행검사 ②~⑤ 를 **게이트를 걸어** 순차 실행한다 (밤새 돌리기용).
#
# 순서는 교차리뷰 J(2026-08-27)가 정한 그대로다:
#   ② degauss 0.02 sentinel 3점   ← 여기서 실패하면 뒤를 태우지 않는다
#   ③ 사다리 나머지 + dense-k corner
#   ④ 스캔 λ = 0, ±0.05, ±0.10    ← 국소 곡률
#   ⑤ 스캔 나머지 진폭
#   (⑥ 은 사람이 하는 판정이라 여기 없다)
#
# ⛔⛔ 이 스크립트가 **하지 않는 것**
#   · ⑥ 판정을 대신하지 않는다. ④⑤ 결과를 보고 NEB 재개 여부를 정하는 건 사람이다.
#   · 실패를 건너뛰지 않는다. **게이트가 이 스크립트의 존재 이유**다 —
#     sentinel 이 어긋난 채 사다리를 다 돌리면, 나온 숫자가 smearing 얘기인지
#     설정이 틀린 얘기인지 못 가른다. 그런 결과는 없느니만 못하다.
#   · UMA MD 와 **동시에 안 돈다** (리뷰 J5). GPU 가 비었는지 먼저 보고, 안 비었으면
#     기다리거나(--wait) 거부한다. Codex 논거는 OOM 자체가 아니라 **실패 원인이 섞이는 것**:
#     sentinel 이 이상할 때 그게 smearing 탓인지 메모리 압박 탓인지 못 가르게 된다.
#   · 이완을 다시 하지 않는다. 전부 **고정 기하 SCF** 다.
#
# 사용:
#   bash tools/sei/run_prereq_chain.sh                       # 기본 (gabia cc333)
#   bash tools/sei/run_prereq_chain.sh --wait                # GPU 빌 때까지 기다렸다 시작
#   bash tools/sei/run_prereq_chain.sh --stage 4             # ④ 부터
#   bash tools/sei/run_prereq_chain.sh --dry                 # 무엇을 돌릴지만 보고 끝
#   bash tools/sei/run_prereq_chain.sh --selftest            # 게이트 논리 검사 (QE 없이)
# =============================================================================
set -uo pipefail

REPO="${REPO:-/data/work/repo}"
WORK="${WORK:-/data/work/runs/sei_neb_v2_cc333}"
TAG="${TAG:-li3nd}"
PY="${PY:-python3}"
SS="$REPO/tools/sei/symmetric_saddle.py"
LOG="${LOG:-/data/work/runs/prereq_chain_$(date +%m%d_%H%M).log}"
# ⛔ 2026-08-28 — 첫 판은 MPIRUN·PW **경로만** 챙기고 환경변수를 통째로 빠뜨렸다.
#   pw.x 가 `libgomp: TODO` 로 즉사했고 밤샘 체인이 첫 점에서 끝났다.
#   기존 run_sei_neb.sh 는 그 블록을 갖고 있었다 — 이제 **같은 파일을 둘이 source** 한다.
# shellcheck disable=SC1090
. "$(dirname "${BASH_SOURCE[0]}")/qe_env.sh"
GPU_FREE_MIB="${GPU_FREE_MIB:-20000}"     # 이만큼 비어야 시작한다
DRY=0; WAIT=0; STAGE=2; SELFTEST=0
while [ $# -gt 0 ]; do
  case "$1" in
    --dry) DRY=1 ;; --wait) WAIT=1 ;; --stage) STAGE="$2"; shift ;;
    --selftest) SELFTEST=1 ;;
    *) echo "모르는 인자: $1"; exit 2 ;;
  esac; shift
done

# ⛔ 2026-08-28 — selftest 가 `die "테스트"` 를 부르는데 die→ts 가 `tee -a "$LOG"` 를 타서
#   **실제 로그에 ⛔ 를 써 넣었다.** watch 가 그걸 진짜 실패로 잡아 가짜 경보를 냈다.
#   테스트가 운영 기록을 건드리면 안 된다 — selftest 중에는 로그를 /dev/null 로 돌린다.
ts(){ echo "[$(date +%m-%d\ %H:%M:%S)] $*" | tee -a "$LOG"; }
# ⛔ 2026-08-28 — 실패를 "타임스탬프 붙은 ⛔" 로 세는 것은 약하다. 로그에 어떤 이유로든
#   ⛔ 가 한 줄 들어가면(예: 옛 selftest 가 남긴 것) watch 가 가짜 경보를 낸다.
#   ⇒ **명시적 표지**를 단다. watch 는 이 표지만 실패로 센다.
die(){ ts "⛔ [CHAIN-FAIL] $*"; ts "   ⇒ **여기서 멈춘다.** 뒤 단계를 돌려도 읽을 수 없는 숫자가 나온다."; exit 1; }

# ── GPU 가 비었나 (리뷰 J5) ──────────────────────────────────────────────────
gpu_free_mib() {
  command -v nvidia-smi >/dev/null || { echo 999999; return; }   # 못 재면 막지 않는다
  local t u
  t=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -1)
  u=$(nvidia-smi --query-gpu=memory.used  --format=csv,noheader,nounits 2>/dev/null | head -1)
  [ -n "$t" ] && [ -n "$u" ] && echo $((t - u)) || echo 999999
}
gpu_gate() {
  local f; f=$(gpu_free_mib)
  if [ "$f" -ge "$GPU_FREE_MIB" ]; then ts "· GPU 여유 ${f} MiB — 시작한다"; return 0; fi
  if [ "$WAIT" != 1 ]; then
    ts "⛔ GPU 여유 ${f} MiB < ${GPU_FREE_MIB} — UMA MD 가 돌고 있는 듯하다."
    ts "   리뷰 J5: 같이 돌리면 **실패 원인이 섞인다** (sentinel 이 이상할 때 smearing 탓인지"
    ts "   메모리 탓인지 못 가른다). --wait 를 주면 빌 때까지 기다린다."
    return 1
  fi
  ts "· GPU 여유 ${f} MiB — 빌 때까지 기다린다 (10분마다 확인)"
  while [ "$(gpu_free_mib)" -lt "$GPU_FREE_MIB" ]; do sleep 600; done
  ts "· GPU 비었다 — 시작한다"
}

# ── SCF 하나 (이미 끝난 것은 건너뛴다 — 이어달리기 가능) ──────────────────────
run_scf() {
  local dir="$1"
  [ -f "$dir/scf.in" ] || { ts "  ⛔ 없음: $dir/scf.in"; return 1; }
  if [ -f "$dir/scf.out" ] && grep -aq "JOB DONE" "$dir/scf.out"; then
    ts "  · 건너뜀(이미 완료): ${dir#$WORK/}"; return 0; fi
  ts "  ▶ ${dir#$WORK/}"
  [ "$DRY" = 1 ] && return 0
  ( cd "$dir" && $MPIRUN -np 1 --oversubscribe "$PW" -in scf.in > scf.out 2>&1 )
  if grep -aqE "unable to launch|could not access or execute" "$dir/scf.out" 2>/dev/null; then
    ts "  ⛔ pw.x 실행 자체가 실패 — 계산이 안 돌았다"; return 1; fi
  grep -aq "JOB DONE" "$dir/scf.out" || { ts "  ⛔ JOB DONE 없음"; return 1; }
  return 0
}
run_tree() {   # $1 = 폴더 (그 밑의 모든 scf.in 을 돈다)
  local n=0 f
  while IFS= read -r f; do run_scf "$(dirname "$f")" || return 1; n=$((n+1))
  done < <(find "$1" -name scf.in | sort)
  ts "  ✓ ${n}점 완료"
}

# ── selftest: 게이트가 실제로 막는가 (QE 없이) ───────────────────────────────
if [ "$SELFTEST" = 1 ]; then
  LOG=/dev/null            # ⛔ 위 ts() 주석 참조 — 테스트는 운영 로그를 안 건드린다
  ok=1; say(){ echo "  $1 $2"; [ "$1" = "✗" ] && ok=0; return 0; }
  echo "── run_prereq_chain selftest ──"
  # ① GPU 게이트: 여유가 모자라고 --wait 가 없으면 **막아야** 한다
  gpu_free_mib(){ echo 1000; }; WAIT=0
  gpu_gate >/dev/null 2>&1 && say "✗" "① GPU 부족인데 통과시켰다" || say "✓" "① GPU 부족 → 막는다"
  gpu_free_mib(){ echo 40000; }
  gpu_gate >/dev/null 2>&1 && say "✓" "① GPU 여유 → 통과" || say "✗" "① 여유인데 막았다"
  gpu_free_mib(){ echo 999999; }
  gpu_gate >/dev/null 2>&1 && say "✓" "①' nvidia-smi 를 못 재면 막지 않는다" || say "✗" "①' 못 재는데 막았다"
  # ② run_scf: JOB DONE 있는 것은 건너뛰고, 없는 것은 실패로 본다
  T=$(mktemp -d); mkdir -p "$T/a" "$T/b"
  : > "$T/a/scf.in"; printf 'JOB DONE.\n' > "$T/a/scf.out"
  run_scf "$T/a" >/dev/null 2>&1 && say "✓" "② 끝난 점은 건너뛴다(이어달리기)" || say "✗" "② 끝난 점을 다시 돌린다"
  : > "$T/b/scf.in"; printf 'oops\n' > "$T/b/scf.out"; DRY=0
  ( PW=/nonexistent MPIRUN=/nonexistent run_scf "$T/b" ) >/dev/null 2>&1 \
    && say "✗" "② JOB DONE 없는데 성공이라 했다" || say "✓" "② JOB DONE 없으면 실패로 본다"
  # ③ die 는 반드시 비영 종료 (게이트가 뚫리면 이 스크립트는 의미가 없다)
  ( die "테스트" ) >/dev/null 2>&1 && say "✗" "③ die 가 0 으로 끝났다" || say "✓" "③ die 는 비영 종료"
  # ③' **테스트가 운영 로그를 오염시키지 않는다** (실측: `⛔ 테스트` 가 watch 에 떴다)
  _PL="$T/prod.log"; : > "$_PL"
  ( LOG="$_PL"; SELFTEST=1; LOG=/dev/null; ts "이건 로그에 남으면 안 된다" ) >/dev/null 2>&1
  [ ! -s "$_PL" ] && say "✓" "③' selftest 는 운영 로그에 안 쓴다" \
                  || say "✗" "③' selftest 가 운영 로그를 오염시켰다"
  rm -rf "$T"
  [ "$ok" = 1 ] && { echo "  ✅ selftest 통과"; exit 0; } || { echo "  ⛔ selftest 실패"; exit 1; }
fi

# ═══ 본 실행 ═══════════════════════════════════════════════════════════════
ts "═══ li3nd 선행검사 체인 (리뷰 J 순서) · stage ${STAGE} 부터 · WORK=$WORK"
[ -f "$SS" ] || die "도구가 없다: $SS  (repo 를 먼저 당길 것)"
[ -x "$PW" ] || die "pw.x 가 없다: $PW"
# ⛔ 환경이 맞는지 **첫 점을 태우기 전에** 본다. libgomp 사고를 두 번 겪지 않는다.
if [ "$DRY" != 1 ]; then
  _T=$(mktemp -d); printf '&CONTROL\n/\n' > "$_T/x.in"
  ( cd "$_T" && timeout 60 $MPIRUN -np 1 --oversubscribe "$PW" -in x.in > x.out 2>&1 )
  if grep -aqE "libgomp|unable to launch|error while loading shared" "$_T/x.out" 2>/dev/null; then
    ts "⛔ pw.x 환경이 틀렸다 — 꼬리:"; sed -n '1,6p' "$_T/x.out" | sed 's/^/     /' | tee -a "$LOG"
    rm -rf "$_T"; die "환경 preflight (qe_env.sh 를 볼 것)"
  fi
  rm -rf "$_T"; ts "· pw.x 환경 preflight 통과"
fi
[ -d "$WORK/$TAG" ] || die "런 폴더가 없다: $WORK/$TAG"
[ "$DRY" = 1 ] || gpu_gate || die "GPU 게이트"

RUN_G=$($PY - "$WORK/$TAG/neb.in" <<'EOP'
import re,sys
t=open(sys.argv[1],errors="replace").read()
t=t[t.find("BEGIN_ENGINE_INPUT"):]
m=re.search(r"degauss\s*=\s*([\d.eEdD+-]+)",t)
print(m.group(1).replace("d","e") if m else "")
EOP
)
[ -n "$RUN_G" ] || die "neb.in 에서 degauss 를 못 읽었다"
ts "런의 degauss = $RUN_G Ry"

# ── ② sentinel — 런 자신의 degauss 3점. **여기서 막히면 끝** ────────────────
if [ "$STAGE" -le 2 ]; then
  ts "── ② sentinel (degauss $RUN_G · 3점)"
  $PY "$SS" --work "$WORK" --tag "$TAG" --smear_ladder --ladder "$RUN_G" 2>&1 | tee -a "$LOG"
  run_tree "$WORK/$TAG/smear_ladder" || die "② SCF 실패"
  $PY "$SS" --work "$WORK" --tag "$TAG" --collect_ladder 2>&1 | tee -a "$LOG"
  if [ "$DRY" != 1 ]; then
    $PY - "$WORK/$TAG/smear_ladder/ladder_result.json" <<'EOP' || exit 1
import json,sys
d=json.load(open(sys.argv[1]))
dv=d.get("sentinel_delta_meV")
if dv is None: print("⛔ sentinel 비교가 없다 — 런 degauss 와 사다리가 안 맞는다"); sys.exit(1)
if abs(dv)>5: print(f"⛔ sentinel Δ {dv:+.1f} meV > 5 — 고정좌표 에너지를 재현 못 한다"); sys.exit(1)
print(f"✅ sentinel Δ {dv:+.1f} meV — 재현한다")
EOP
    ts "② 통과"
  fi
fi

# ── ③ 사다리 나머지 + dense-k corner ────────────────────────────────────────
if [ "$STAGE" -le 3 ]; then
  ts "── ③ 사다리 (0.02·0.01·0.005) + dense-k corner (4×4×4 × 0.01·0.005)"
  $PY "$SS" --work "$WORK" --tag "$TAG" --smear_ladder --ladder 0.02,0.01,0.005 2>&1 | tee -a "$LOG"
  run_tree "$WORK/$TAG/smear_ladder" || die "③ 사다리 SCF 실패"
  $PY "$SS" --work "$WORK" --tag "$TAG" --collect_ladder 2>&1 | tee -a "$LOG"
  $PY "$SS" --work "$WORK" --tag "$TAG" --smear_ladder --ladder 0.01,0.005 \
       --kgrid "4 4 4 0 0 0" 2>&1 | tee -a "$LOG"
  run_tree "$WORK/$TAG/smear_ladder_k444" || die "③ dense-k SCF 실패"
  $PY "$SS" --work "$WORK" --tag "$TAG" --collect_ladder --sub smear_ladder_k444 2>&1 | tee -a "$LOG"
  ts "③ 끝 — ⚠ 판정은 사람이 한다 (사다리 결론이 k 에 딸려 있는지 두 표를 나란히 볼 것)"
fi

# ── ④ 스캔 국소 곡률 ────────────────────────────────────────────────────────
if [ "$STAGE" -le 4 ]; then
  ts "── ④ 모드 스캔 λ = 0, ±0.05, ±0.10 (국소 곡률)"
  $PY "$SS" --work "$WORK" --tag "$TAG" --mode_scan --lambdas "-0.10,-0.05,0,0.05,0.10" 2>&1 | tee -a "$LOG"
  run_tree "$WORK/$TAG/mode_scan" || die "④ SCF 실패"
  $PY "$SS" --work "$WORK" --tag "$TAG" --collect_scan 2>&1 | tee -a "$LOG"
fi

# ── ⑤ 스캔 나머지 진폭 ──────────────────────────────────────────────────────
if [ "$STAGE" -le 5 ]; then
  ts "── ⑤ 모드 스캔 나머지 (±0.25 · ±0.5 · ±1)"
  $PY "$SS" --work "$WORK" --tag "$TAG" --mode_scan \
       --lambdas "-1,-0.5,-0.25,-0.10,-0.05,0,0.05,0.10,0.25,0.5,1" 2>&1 | tee -a "$LOG"
  run_tree "$WORK/$TAG/mode_scan" || die "⑤ SCF 실패"
  $PY "$SS" --work "$WORK" --tag "$TAG" --collect_scan 2>&1 | tee -a "$LOG"
fi

ts "═══ 체인 끝. 로그: $LOG"
ts "⑥ 은 사람이 한다 — 곡률 부호와 sentinel·dense-k 를 같이 놓고 NEB 재개를 판정할 것."
