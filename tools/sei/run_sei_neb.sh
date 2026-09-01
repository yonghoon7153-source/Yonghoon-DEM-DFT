#!/usr/bin/env bash
# =============================================================================
# run_sei_neb.sh — SEI 3종의 CI-NEB 을 순차 실행한다 (Li₂S · Li₃P · Li₃PO₄ γ).
#
# ⚠ NEB 은 **이미지마다 SCF** 를 돌린다. 경로 스텝 하나에 (이미지−2) 번의 scf 가 들고
#   그게 수십 번 반복된다 — 갭 계산(scf 1회)의 100 배 급이다. 싼 것부터 순서를 잡는다:
#     li2s(23원자) → li3p(63) → li3po4g(127)
#   앞이 깨지면 뒤는 안 건다. 뒤로 갈수록 비싸므로 진단은 앞에서 끝내는 게 맞다.
#
# ⚠ pw.x 와 UMA 를 동시에 돌리지 않는다 (VRAM 47/48 GB 점유 사례) — nvidia-smi 가드.
#
#   bash tools/sei/run_sei_neb.sh              # 전부 (싼 것부터)
#   bash tools/sei/run_sei_neb.sh li2s         # 하나만
#
#   --after <경로>   그 폴더의 neb.x 가 끝날 때까지 **기다렸다가** 시작한다.
#     GPU 가 하나뿐이라 두 NEB 를 겹쳐 돌리면 둘 다 느려진다(VRAM 이 아니라 SM 경합).
#     예) c→b 를 완주시킨 뒤 c→c 를 자동으로 잇기:
#       WORK=/data/work/runs/sei_neb_v2_ccpath \
#       bash tools/sei/run_sei_neb.sh --after /data/work/runs/sei_neb_v2 li3nd
# =============================================================================
set -uo pipefail; set +H
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
WORK=${WORK:-/data/work/runs/sei_neb}
# ⚠ 2026-09-01 — gabia 경로가 기본값이라 kgy 에서 매번 막혔다(실측 2회).
#   기본값은 두되 **없으면 PATH 에서 찾는다**. 환경으로 준 값이 언제나 이긴다.
NEB=${NEB:-/data/apps/qe-7.4.1-gpu/bin/neb.x}
[ -x "$NEB" ] || NEB=$(command -v neb.x || echo "$NEB")
# ⛔ 2026-08-28 — 이 블록이 여기에만 있어서, 새 스크립트(run_prereq_chain.sh)가 이걸
#   빠뜨리고 `libgomp: TODO` 로 죽었다. 정본을 파일로 뽑고 둘이 같이 쓴다.
# shellcheck disable=SC1090
. "$(dirname "$0")/qe_env.sh"
ts(){ echo "[$(date +%H:%M:%S)] $*"; }

# ── 이어달리기 안전장치 (현재 폴더에서 동작) ────────────────────────────────
#   호출 직후 러너가 `> neb.out` 으로 출력을 덮어쓰므로, **그 전에** 이력을 떠 놓고
#   restart_mode 를 맞춘다. 조건이 안 맞으면 아무것도 건드리지 않는다.
prep_resume() {
  local _NPATH _NITER _BAK _RM _BK _NB
  _NPATH=$(ls ./*.path 2>/dev/null | head -1)
  # ⚠ 스텝 수는 'activation energy (->)' 줄로 센다. neb.out 의 반복 머리글은
  #   '---- iteration N ----' 라 '^ *iteration' 로는 **한 줄도 안 잡힌다**
  #   (그렇게 짜면 _NITER=0 → 이 블록이 영영 안 돌고, 조용히 이력을 덮어쓴다).
  #   watch_gabia.py:321 이 화면의 it 를 세는 것과 같은 신호다.
  # ⚠ `grep -c ... || echo 0` 로 쓰면 안 된다: grep -c 는 0건일 때 "0" 을 **찍고도**
  #   exit 1 이라 `|| echo 0` 이 하나 더 붙어 _NITER 가 "0\n0" 이 된다 → 뒤의
  #   [ -gt ] 가 "integer expression expected" 로 터진다 (selftest ④ 가 잡았다).
  _NITER=$(grep -ac "activation energy (->)" neb.out 2>/dev/null)
  [ -n "$_NITER" ] || _NITER=0          # 파일 자체가 없으면 빈 문자열
  [ -n "$_NPATH" ] || return 0
  if [ "${_NITER:-0}" -gt 0 ]; then
    _BAK="neb.out.iter${_NITER}_$(date +%m%d)"
    cp neb.out "$_BAK" 2>/dev/null && ts "  ⭐ 이어달리기: 이력 ${_NITER}스텝 보존 → $_BAK"
  else
    # ⛔ 2026-08-27 (교차리뷰 I · P0-3) — 세 번째 구멍. neb.out 이 **옮겨졌으면**
    #   (ci 단계의 `mv neb.out neb.out.noCI`, 손백업) 이력이 0 으로 보인다. 그때
    #   손을 떼면 neb.in 의 from_scratch 가 그대로 서서 **.path 를 두고 처음부터** 돈다.
    #   → 백업에 이력이 있으면 체크포인트를 살린다. 새 백업은 안 만든다(덮어쓸 게 없다).
    _BK=$(ls -t ./neb.out.iter* ./neb.out.noCI ./neb.out.bak* 2>/dev/null | head -1)
    [ -n "$_BK" ] || return 0
    _NB=$(grep -ac "activation energy (->)" "$_BK" 2>/dev/null)
    [ -n "$_NB" ] || _NB=0
    [ "$_NB" -gt 0 ] || return 0
    ts "  ⭐ neb.out 에 이력이 없지만 ${_BK#./} 에 ${_NB}스텝 있다 — 체크포인트를 살린다"
  fi
  _RM=$(sed -n "s/.*restart_mode[[:space:]]*=[[:space:]]*'\{0,1\}\([a-z_]*\).*/\1/p" neb.in | head -1)
  if [ "$_RM" = "restart" ]; then
    ts "  ✓ restart_mode 이미 'restart'"
    return 0
  fi
  cp neb.in "neb.in.bak_$(date +%m%d)"
  if grep -aq "restart_mode" neb.in; then
    sed -i "s/restart_mode[[:space:]]*=.*/restart_mode = 'restart'/" neb.in
  else
    sed -i "0,/&PATH/s//\&PATH\n   restart_mode = 'restart'/" neb.in
  fi
  ts "  ⭐ restart_mode: '${_RM:-미기재}' → 'restart' (경로 파일 ${_NPATH#./} 를 실제로 쓴다)"
}

# ⚠⚠ 바이너리를 **미리** 확인한다 (2026-08-07 실측). neb.x 가 없으면 mpirun 이
#   "unable to launch ... could not access or execute" 만 남기고 조용히 끝나는데,
#   러너는 'convergence achieved' 가 없다는 이유로 "경로 미수렴" 이라고 보고했다.
#   → 2시간을 아무것도 안 돌고 흘려보냈다. 없는 건 없다고 즉시 말해야 한다.
# ── --selftest: prep_resume 만 검증한다 (QE 없이, 임시 폴더에서) ───────────
#   ⛔ 이 selftest 가 보증하지 **못하는** 것: neb.x 가 실제로 경로를 이어받는지,
#     끝점/의사퍼텐셜/자원 가드. 여기서 보는 건 "이력을 안 지우는가 ·
#     restart_mode 를 맞추는가 · 조건이 아니면 손대지 않는가" 세 가지뿐이다.
if [ "${1:-}" = "--selftest" ]; then
  _T=$(mktemp -d); _ok=1
  say(){ echo "  $1 $2"; if [ "$1" = "✗" ]; then _ok=0; fi; return 0; }
  # QE 가 실제로 찍는 모양: 반복 머리글은 '---- iteration N ----' 이지 '^iteration' 이 아니다
  _mkout(){ local n=$1 f=$2; : > "$f"
    for i in $(seq 1 "$n"); do
      printf '     ------------------------------ iteration %3d ---\n' "$i" >> "$f"
      printf '     activation energy (->) =   0.%03d000 eV\n' $((900 - i)) >> "$f"
      printf '     activation energy (<-) =   0.%03d000 eV\n' $((900 - i)) >> "$f"
    done; }
  _in(){ printf '&PATH\n   restart_mode = %s\n   nstep_path = 50\n/\n' "$1"; }

  echo "── prep_resume selftest ──"
  # ① 양성: .path + 이력 24스텝 + from_scratch → 백업 생김 · restart 로 바뀜
  mkdir -p "$_T/a"; ( cd "$_T/a"
    touch li3nd.path; _mkout 24 neb.out; _in "'from_scratch'" > neb.in; prep_resume >/dev/null )
  [ -f "$_T/a/neb.out.iter24_$(date +%m%d)" ] && say "✓" "① 이력 24스텝 백업" || say "✗" "① 백업이 안 생겼다"
  grep -q "restart_mode = 'restart'" "$_T/a/neb.in" && say "✓" "① restart_mode → restart" || say "✗" "① restart_mode 가 안 바뀌었다"
  # ② 회귀(이 selftest 의 존재 이유): 옛 패턴 '^ *iteration' 은 0줄이어야 한다
  [ "$(grep -ac '^ *iteration ' "$_T/a/neb.out")" = 0 ] \
    && say "✓" "② 옛 패턴은 0줄 — activation energy 로 세는 게 맞다" \
    || say "✗" "② 옛 패턴이 잡힌다 — 픽스 근거가 틀렸다"
  # ③ 음성: .path 가 없으면 (첫 실행) 아무것도 안 만들고 neb.in 도 그대로
  mkdir -p "$_T/b"; ( cd "$_T/b"
    _mkout 5 neb.out; _in "'from_scratch'" > neb.in; prep_resume >/dev/null )
  [ -z "$(ls "$_T/b"/neb.out.iter* 2>/dev/null)" ] && say "✓" "③ .path 없음 → 백업 안 만듦" || say "✗" "③ .path 없는데 손댔다"
  grep -q "restart_mode = 'from_scratch'" "$_T/b/neb.in" && say "✓" "③ .path 없음 → neb.in 그대로" || say "✗" "③ .path 없는데 neb.in 을 고쳤다"
  # ④ 음성: .path 는 있는데 이력 0스텝(초반에 죽은 런) → 덮어써도 잃을 게 없다, 손대지 않는다
  mkdir -p "$_T/c"; ( cd "$_T/c"
    touch x.path; printf '     Program NEB starts\n' > neb.out; _in "'from_scratch'" > neb.in
    prep_resume >/dev/null 2>"$_T/c.err" )
  [ -z "$(ls "$_T/c"/neb.out.iter* 2>/dev/null)" ] && say "✓" "④ 이력 0스텝 → 손대지 않음" || say "✗" "④ 이력이 없는데 백업했다"
  # ④' 조용히 지나가야 한다 — stderr 가 있으면 판정이 우연히 맞은 것이다
  [ ! -s "$_T/c.err" ] && say "✓" "④' 0건 세기에 에러 없음" || { say "✗" "④' stderr: $(head -1 "$_T/c.err")"; }
  # ④'' 파일 자체가 없는 경우도 조용해야 한다
  mkdir -p "$_T/f"; ( cd "$_T/f"; touch w.path; _in "'from_scratch'" > neb.in
    prep_resume >/dev/null 2>"$_T/f.err" )
  [ ! -s "$_T/f.err" ] && say "✓" "④'' neb.out 부재도 조용" || say "✗" "④'' stderr: $(head -1 "$_T/f.err")"
  # ⑤ restart_mode 줄이 아예 없으면 &PATH 밑에 넣는다
  mkdir -p "$_T/d"; ( cd "$_T/d"
    touch y.path; _mkout 3 neb.out; printf '&PATH\n   nstep_path = 50\n/\n' > neb.in; prep_resume >/dev/null )
  grep -q "restart_mode = 'restart'" "$_T/d/neb.in" && say "✓" "⑤ 미기재 → &PATH 밑에 삽입" || say "✗" "⑤ 삽입이 안 됐다"
  # ⑥ 이미 restart 면 neb.in 백업을 만들지 않는다 (불필요한 사본 금지)
  mkdir -p "$_T/e"; ( cd "$_T/e"
    touch z.path; _mkout 7 neb.out; _in "'restart'" > neb.in; prep_resume >/dev/null )
  [ -z "$(ls "$_T/e"/neb.in.bak_* 2>/dev/null)" ] && say "✓" "⑥ 이미 restart → neb.in 백업 안 만듦" || say "✗" "⑥ 쓸데없이 neb.in 을 백업했다"
  [ -f "$_T/e/neb.out.iter7_$(date +%m%d)" ] && say "✓" "⑥ 그래도 이력은 보존" || say "✗" "⑥ 이력을 안 지켰다"
  # ⑦ 양성(리뷰 I P0-3): neb.out 이 옮겨졌어도 백업에 이력이 있으면 restart 를 맞춘다
  mkdir -p "$_T/g"; ( cd "$_T/g"
    touch li3nd.path; _mkout 30 neb.out.noCI; _in "'from_scratch'" > neb.in; prep_resume >/dev/null )
  grep -q "restart_mode = 'restart'" "$_T/g/neb.in" \
    && say "✓" "⑦ neb.out 부재 + 백업 이력 → restart 로 맞춘다" \
    || say "✗" "⑦ 백업에 이력이 있는데 from_scratch 로 뒀다 (.path 를 버린다)"
  [ -z "$(ls "$_T/g"/neb.out.iter* 2>/dev/null)" ] && say "✓" "⑦ 새 백업은 안 만든다" || say "✗" "⑦ 쓸데없이 백업했다"
  # ⑦' 음성: 백업이 있어도 **이력이 0** 이면 손대지 않는다
  mkdir -p "$_T/h"; ( cd "$_T/h"
    touch li3nd.path; printf '     Program NEB starts\n' > neb.out.noCI
    _in "'from_scratch'" > neb.in; prep_resume >/dev/null 2>"$_T/h.err" )
  grep -q "restart_mode = 'from_scratch'" "$_T/h/neb.in" \
    && say "✓" "⑦' 백업에 이력 0 → 손대지 않음" || say "✗" "⑦' 이력이 없는데 restart 로 바꿨다"
  [ ! -s "$_T/h.err" ] && say "✓" "⑦'' 조용히 지나간다" || say "✗" "⑦'' stderr: $(head -1 "$_T/h.err")"
  rm -rf "$_T"
  [ "$_ok" = 1 ] && { echo "  ✅ selftest 통과"; exit 0; } || { echo "  ⛔ selftest 실패"; exit 1; }
fi

MODE=neb
AFTER=""
while [ $# -gt 0 ]; do
  case "$1" in
    --after) AFTER="${2:?--after 뒤에 기다릴 작업 폴더를 주세요}"; shift 2 ;;
    endpoints) MODE=endpoints; shift ;;
    ci) MODE=ci; shift ;;
    *) break ;;
  esac
done

# ── 중복 실행 가드 (CLAUDE.md 규율) ─────────────────────────────────────────
#   ⚠ WORK 는 **환경변수**라 cmdline 에 안 나온다 — 프로세스 이름으로 매칭하려 들면
#     못 잡는다(첫 판이 그랬다). 작업 폴더에 락을 둔다: 그게 실제로 겹치는 단위다.
mkdir -p "$WORK" 2>/dev/null || true
LOCK="$WORK/.run_sei_neb.lock"
if [ -f "$LOCK" ] && kill -0 "$(cat "$LOCK" 2>/dev/null)" 2>/dev/null; then
  ts "⛔ 이 작업 폴더가 이미 돌고 있다 (pid $(cat "$LOCK")) — 중복 실행하지 않는다"
  ts "   $WORK"
  exit 1
fi
echo $$ > "$LOCK"
trap 'rm -f "$LOCK"' EXIT

# ── --after: 앞 작업이 끝날 때까지 기다린다 ─────────────────────────────────
if [ -n "$AFTER" ]; then
  [ -d "$AFTER" ] || { ts "⛔ --after 경로가 없다: $AFTER"; exit 1; }
  # ⚠ **기다리기 전에** 내 입력이 준비됐는지 먼저 본다. 몇 시간 기다린 뒤
  #   "입력이 없다" 로 죽으면 그 시간이 통째로 날아간다.
  n_in=$(ls "$WORK"/*/neb.in 2>/dev/null | wc -l)
  if [ "$n_in" = 0 ]; then
    ts "⛔ $WORK 에 neb.in 이 없다 — 기다려도 돌릴 게 없다"
    ts "   먼저: python3 tools/sei/build_neb_inputs.py --work $WORK ..."
    exit 1
  fi
  ts "⏳ $AFTER 의 계산이 끝나기를 기다린다 (내 입력 ${n_in}개 확인됨)"
  # ⚠ 조건을 단순하게 둔다: **이 기계에 계산 프로세스가 하나도 없으면** 앞 작업이 끝난 것이다.
  #   GPU 가 하나뿐이라 겹쳐 돌리지 않기 때문이다. 프로세스 이름에서 작업
  #   폴더를 파싱하려 들면(neb.x 는 인자에 폴더를 안 싣는다) 조용히 틀린다.
  # ⚠⚠ 2026-08-13 — neb.x 만 보면 **끝점 이완 구간(pw.x)을 못 본다**. 앞 작업이
  #   `endpoints` 단계면 neb.x 가 0 이라 대기가 즉시 풀리고 pw.x 와 GPU 를 다툰다
  #   (아래 nvidia-smi 가드에 걸려 그대로 죽는다). pw.x 도 같이 본다.
  WAITPAT="[n]eb\.x|[p]w\.x"
  waited=0
  while pgrep -f "$WAITPAT" >/dev/null; do
    sleep 300; waited=$((waited+5))
    [ $((waited % 60)) = 0 ] && ts "   ... ${waited}분째 대기 (계산 프로세스 $(pgrep -cf "$WAITPAT")개)"
  done
  ts "✔ 앞 작업이 끝났다 (${waited}분 대기) — 이어서 시작한다"
  for f in "$AFTER"/*/neb.out; do
    [ -f "$f" ] && ts "   $(basename "$(dirname "$f")"): $(grep -ac 'convergence achieved' "$f" >/dev/null && echo 수렴 || echo 미수렴)"
  done
fi
if [ "$MODE" = neb ] && [ ! -x "$NEB" ]; then
  ts "⛔ neb.x 를 찾을 수 없거나 실행 권한이 없다: $NEB"
  ts "   QE-GPU 빌드에 neb.x 가 안 들어간 경우가 흔하다(pw.x/dos.x/projwfc.x 만 빌드)."
  ts "   확인:"
  ts "     ls -la $(dirname "$NEB")/ | grep -iE 'neb|pw\.x|path'"
  ts "     find /data/apps -name 'neb.x' -type f 2>/dev/null"
  ts "   빌드가 필요하면 QE 소스에서:  make neb   (pw.x 가 이미 있으면 몇 분이면 된다)"
  ts "   다른 경로에 있으면:  NEB=/경로/neb.x bash tools/sei/run_sei_neb.sh li2s"
  exit 1
fi

# ⛔ 2026-08-11 자체검토 P1-6 — 위 neb.x 검사는 **NEB 모드에만** 걸어야 한다.
#   `endpoints` 는 pw.x 만 쓰는데, 정작 위 주석이 "QE-GPU 빌드에 neb.x 가 없는 경우가
#   흔하다" 고 경고해 놓고 그 상황에서 끝점 이완조차 막고 있었다. 모드를 먼저 읽는다.
LOCK=/tmp/sei_neb.lock; exec 9>"$LOCK"
command -v flock >/dev/null && { flock -n 9 || { ts "⛔ 이미 돈다"; exit 0; }; }

# ⚠ UMA 가 GPU 를 쥐고 있으면 pw.x 가 OOM 으로 죽는다. 먼저 본다.
# ⚠ 2026-09-01 (1저자) — GPU 점유 가드를 **경고로 내린다**(종전엔 exit 1).
#   근거: 이 계들은 작고(li_metal 54원자), CPU 빌드로도 돌며, 1저자가 "같이 돌려도
#   된다, OOM 나면 끄면 된다" 고 판단했다. 실제로 kgy 에서 6.4 GB 점유(UMA)만으로
#   Li 금속 끝점 이완이 막혔다.
#   ⛔ 되살리려면 SEI_GPU_STRICT=1 — 큰 계(수백 원자)에는 그쪽이 맞다.
if command -v nvidia-smi >/dev/null; then
  used=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | head -1)
  if [ "${used:-0}" -gt 2000 ]; then
    ts "⚠ GPU 가 이미 ${used} MiB 쓰인다 (UMA?) — 같이 돌립니다. OOM 이면 멈추세요."
    if [ "${SEI_GPU_STRICT:-0}" = "1" ]; then
      ts "⛔ SEI_GPU_STRICT=1 이라 중단합니다"
      nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv
      exit 1
    fi
  fi
fi

# 싼 것부터 — 원자 수 순서를 코드에 박아 둔다(알파벳 순이면 li3po4g 가 먼저 온다)
# 2026-08-11 6종으로 확장. lindo2 는 frozen-4f PP 게이트가 열려야 입력이 생긴다(todo #27).
# ⚠ P1-5 — li3nd 가 빠져 있어 `run_sei_neb.sh` 도 `endpoints` 도 li3nd 를 안 건드렸다.
#   ⛔ li3nd·lindo2 는 **Nd frozen-4f PP 가 있어야** 입력이 생긴다(todo #27) — 없으면
#     build 단계에서 skip 되므로 여기 있어도 안전하다. 순서는 원자 수 오름차순.
ORDER=(li2s li2o licl li3p li3nd li3po4g lindo2)
TARGETS=("$@"); [ ${#TARGETS[@]} -eq 0 ] && TARGETS=("${ORDER[@]}")

# ★ P0-2 (Codex) — vacancy 끝점을 먼저 이완한다. 미이완 끝점이 경로 최고점이 되면
#   NEB 은 끝점을 고정하므로 내리막만 남아 Ea=0 이 나온다 (li3p 사고의 미해결 절반).
# ⛔⛔ 2026-08-16 — 완료 판정이 `JOB DONE` 이었다. QE 는 **nstep 을 소진해도** JOB DONE 과
#   'End of BFGS Geometry Optimization' 을 똑같이 찍는다. 그래서 cc333 끝점(50/50 스텝
#   소진, max|F| 0.0035 vs 문턱 1e-3)이 "이미 완료" 로 건너뛰어졌다. 수렴의 유일한 증거는
#   **'Begin final coordinates'** 다 — QE 는 힘 기준을 만족했을 때만 그 블록을 찍는다.
# EPSUF: 이어달리기용 디렉터리 접미사 (예: EPSUF=_r2 → ep_initial_r2). 기본은 없음.
if [ "$MODE" = endpoints ]; then
  PW=${PW:-/data/apps/qe-7.4.1-gpu/bin/pw.x}
  [ -x "$PW" ] || PW=$(command -v pw.x || echo "$PW")
  EPSUF=${EPSUF:-}
  [ -x "$PW" ] || { ts "⛔ pw.x 없음: $PW"; exit 1; }
  for t in "${TARGETS[@]}"; do
    for ep in ep_initial ep_final; do
      d="$WORK/$t/${ep}${EPSUF}"
      [ -f "$d/relax.in" ] || { ts "⛔ 없음: $d/relax.in — build_neb_inputs.py 먼저"; continue; }
      if grep -aq "Begin final coordinates" "$d/relax.out" 2>/dev/null; then
        ts "  ✓ $t/${ep}${EPSUF} 이미 **수렴**"; continue; fi
      if grep -aq "The maximum number of steps has been reached" "$d/relax.out" 2>/dev/null; then
        ts "  ▪ $t/${ep}${EPSUF} 스텝 소진분이 있다 — 이 디렉터리를 덮어쓰고 다시 돈다"; fi
      ts "  ▶ $t/${ep}${EPSUF} relax"
      ( cd "$d" && $MPIRUN -np 1 --oversubscribe "$PW" -in relax.in > relax.out 2>&1 )
      if grep -aq "Begin final coordinates" "$d/relax.out"; then
        ts "  ✅ $t/${ep}${EPSUF} 수렴"
      elif grep -aq "The maximum number of steps has been reached" "$d/relax.out"; then
        ts "  ▪ $t/${ep}${EPSUF} **스텝 소진 — 수렴 아님.** nstep 을 늘려 이어달릴 것"
        grep -a "Total force" "$d/relax.out" | tail -2
      else
        ts "  ✗ $t/${ep}${EPSUF} 실패 — 꼬리:"; tail -6 "$d/relax.out"; fi
    done
  done
  ts "끝점 이완 끝 — build_neb_inputs.py 를 **다시 돌려** 이완 좌표를 승계시킬 것"
  exit 0
fi

# ★ P0-5 (자체검토) — 문서화된 2단계 CI 를 러너가 실제로 돌릴 수 있게 한다.
#   QE 권고: no-CI 로 먼저 수렴 → restart + CI. 그런데 옛 코드는 (a) ci 가 지문에 들어가
#   있어 재생성하면 거부당하고 (b) 안내가 "*.path 를 지우라" 인데 restart 는 바로 그
#   prefix.path 가 있어야 돈다. → CI 를 지문에서 빼고, 여기서 neb.out 만 백업한다.
if [ "$MODE" = ci ]; then
  for t in "${TARGETS[@]}"; do
    d="$WORK/$t"; [ -d "$d" ] || { ts "⛔ 없음: $d"; continue; }
    grep -aq "neb: convergence achieved" "$d/neb.out" 2>/dev/null || {
      ts "⛔ $t: 1단계(no-CI)가 아직 수렴 안 했다 — CI 로 못 넘어간다"; continue; }
    ts "  ▶ $t: no-CI 수렴본을 백업하고 CI 단계 입력을 만든다"
    mv "$d/neb.out" "$d/neb.out.noCI"          # ⚠ *.path 와 tmp 는 **남긴다** (restart 용)
    ts "     이제 생성기를 CI 로 다시 돌릴 것 (같은 WORK):"
    ts "       python3 tools/sei/build_neb_inputs.py --only $t --ci_scheme auto --restart"
    ts "     그 뒤:  bash tools/sei/run_sei_neb.sh $t"
  done
  exit 0
fi

for t in "${TARGETS[@]}"; do
  d="$WORK/$t"
  [ -f "$d/neb.in" ] || { ts "⛔ 없음: $d/neb.in — build_neb_inputs.py 부터"; continue; }
  ts "═══ $t ═══"
  cd "$d" || continue
  # ★ P0-3 (Codex) — 프로토콜이 바뀌었는데 옛 neb.out 을 '이미 수렴'으로 건너뛰면
  #   새 meta.json 과 옛 에너지가 결합된다. 지문을 대조한다.
  NEWH=$(python3 -c "import json,sys;print(json.load(open('meta.json')).get('protocol_hash',''))" 2>/dev/null)
  OLDH=$(cat .protocol_hash 2>/dev/null || echo "")
  if [ -n "$NEWH" ] && [ -n "$OLDH" ] && [ "$NEWH" != "$OLDH" ]; then
    ts "  ⛔ 프로토콜 지문이 바뀌었다 ($OLDH -> $NEWH) — 옛 neb.out/tmp/prefix.path 를 재사용하지 않는다."
    ts "     새 WORK 로 돌리거나 이 폴더의 neb.out·tmp·*.path 를 지우고 다시 걸 것."
    cd - >/dev/null; continue
  fi
  # ⛔⛔ 2026-08-11 자체검토 P0-4 — **지문 없는 레거시 산출물**이 방어를 통과했다.
  #   기존 /data/work/runs/sei_neb/li2s/ 에는 옛 규약(tot_charge=+1 · min_cell 8.02 ·
  #   끝점 미이완) 수렴본이 있는데 .protocol_hash 는 없다. 그러면 OLDH="" 라 위 거부를
  #   빠져나가고, 아래 '이미 수렴' 으로 **새 meta.json + 옛 에너지**가 결합된다 —
  #   P0-3 이 막으려던 바로 그 조합이 하필 그게 일어날 수 있는 유일한 폴더에서 뚫렸다.
  #   게다가 옛 코드는 지문 기록이 스킵 **뒤**라 그 폴더가 영구히 무장해제됐다.
  if [ -z "$OLDH" ] && [ -s neb.out ]; then
    ts "  ⛔ 지문 없는 옛 neb.out 이 있다 — **어느 프로토콜로 돈 것인지 알 수 없다**."
    ts "     재사용하지 않는다. 옛 결과를 보존하려면 옮기고, 버리려면 지울 것:"
    ts "       mv neb.out neb.out.legacy_pre20260811 && rm -rf tmp *.path"
    cd - >/dev/null; continue
  fi
  # ★ 지문은 **스킵 판정보다 먼저** 기록한다 (옛 코드는 뒤에 있어 영영 안 써졌다)
  [ -n "$NEWH" ] && echo "$NEWH" > .protocol_hash
  # ★ P0-5 — CI 단계는 물리가 아니라 수렴 전략이라 지문에서 뺐다. 대신 여기 기록한다.
  #  ⛔⛔ 2026-08-16 — 기록만 하고 **대조를 안 했다.** 그래서 2단계가 통째로 안 돌았다:
  #    ci 모드가 neb.out 을 neb.out.noCI 로 옮기지만 *.path·tmp 는 restart 용으로 남긴다.
  #    그런데 build_neb_inputs.py --restart 가 neb.out 을 **다시 만들지 않으므로**,
  #    직전 런의 neb.out 이 없으면 아래 grep 이 안 걸려야 정상인데 —
  #    li2s 는 다른 경로로 neb.out 이 남아 있어 "이미 수렴" 으로 건너뛰었다.
  #    CI 가 지문에서 빠져 있어 protocol_hash 가드도 안 걸린다 (그게 P0-5 의 대가였다).
  #    → 옛 .ci_stage 와 새 ci_scheme 가 다르면 **건너뛰지 않는다**.
  # ⛔⛔ 2026-08-16 (2차) — `.ci_stage` 사이드카는 **옛 코드가 이미 오염시켜 놨다**:
  #   스킵 판정 앞에서 무조건 써서, no-CI 결과가 든 폴더에 "auto" 가 적혀 있었다.
  #   그래서 대조를 붙여도 OLDCIS=auto=CIS 라 또 건너뛰었다.
  #   → 사이드카를 믿지 않는다. **파일 자신**을 읽는다:
  #     neb.out 의 CI_scheme = 실제로 돈 것 · neb.in 의 CI_scheme = 지금 돌리려는 것.
  #     (collect_neb.py 도 같은 규약으로 out 을 먼저 읽는다 — 그래서 v2/li2s 가
  #      neb.in 이 auto 인데도 no-CI 로 보고됐다.)
  _ci_of(){ sed -n "s/.*CI_scheme[[:space:]]*=[[:space:]]*'\{0,1\}\([A-Za-z0-9._-]*\).*/\1/p" "$1" 2>/dev/null | head -1; }
  OUTCI=$(_ci_of neb.out); INCI=$(_ci_of neb.in)
  CIS=$(python3 -c "import json;print(json.load(open('meta.json')).get('ci_scheme',''))" 2>/dev/null)
  [ -z "$INCI" ] && INCI="$CIS"
  if grep -aq "neb: convergence achieved" neb.out 2>/dev/null; then
    if [ -n "$OUTCI" ] && [ -n "$INCI" ] && [ "$OUTCI" != "$INCI" ]; then
      ts "  ▶ neb.out 은 CI=$OUTCI 로 돈 것이고 지금 입력은 CI=$INCI — 재사용하지 않고 다시 돌린다"
      mv neb.out "neb.out.${OUTCI}" 2>/dev/null || true
    elif [ "$INCI" = "no-CI" ]; then
      ts "  ✓ no-CI 수렴 — 2단계(CI)로 가려면:  bash tools/sei/run_sei_neb.sh ci $t"
      [ -n "$CIS" ] && echo "$CIS" > .ci_stage
      cd - >/dev/null; continue
    else
      ts "  ✓ 이미 수렴 — 건너뜀 (neb.out 이 CI=$OUTCI 로 돌았다)"
      [ -n "$CIS" ] && echo "$CIS" > .ci_stage
      cd - >/dev/null; continue
    fi
  fi
  # 지문은 실제로 돌리기로 한 뒤에 기록한다
  [ -n "$CIS" ] && echo "$CIS" > .ci_stage
  # ⚠ neb.x 는 재시작 파일(prefix.path)이 있으면 이어서 돈다. 지우지 말 것.
  #
  # ⛔⛔ 2026-08-24 실측 — 그 문장에 **두 구멍**이 있었다 (li3nd cc333 이 3일 7시간
  #   돌다 08-23 08:34 에 멈췄고, 이어서 돌리려다 발견했다):
  #
  #   ① `> neb.out` 이 **3일치 이력을 통째로 덮어쓴다.** iteration 1~24 의
  #      activation energy 궤적이 사라진다 — 수렴하는 중이었는지(0.936→0.880)를
  #      나중에 볼 수 없게 된다. 진행을 보는 유일한 기록인데 그걸 지우고 시작했다.
  #   ② **restart_mode 를 확인하지 않는다.** prefix.path 가 있어도 neb.in 이
  #      restart_mode='from_scratch' 면 neb.x 는 **처음부터** 돈다. 주석은
  #      "있으면 이어서 돈다" 라고 단언하지만 QE 는 그렇게 동작하지 않는다.
  #      3일을 버리고도 화면상으로는 정상 진행처럼 보인다.
  #
  #   ⇒ 이어달리기 조건이 갖춰졌으면(경로 파일 + 진행한 이력) 이력을 보존하고
  #     restart_mode 를 명시적으로 맞춘다. 아니면 손대지 않는다.
  nat=$(grep -a -m1 "nat" neb.in | grep -oE "[0-9]+")
  prep_resume
  ts "  ▶ neb.x (원자 ${nat:-?})  — 진행은 neb.out 의 'activation energy' 줄로 본다"
  $MPIRUN -np 1 --oversubscribe "$NEB" -inp neb.in > neb.out 2>&1
  # ⚠ mpirun 실행 실패는 '미수렴' 이 아니다 — 아예 안 돈 것이다. 구분해서 말한다.
  if grep -aqE "unable to launch|could not access or execute|command not found" neb.out; then
    ts "  ⛔ neb.x 실행 자체가 실패했다 (계산이 안 돌았다):"
    sed -n '1,8p' neb.out | sed 's/^/       /'
    cd - >/dev/null; break
  fi
  if grep -aq "neb: convergence achieved" neb.out; then
    ts "  ✅ 수렴"
    grep -a "activation energy" neb.out | tail -2
  else
    ts "  ⚠ 미수렴 — 꼬리:"; tail -12 neb.out
    ts "     경로 스텝을 더 주려면 neb.in 의 nstep_path 를 늘리고 다시 걸면 이어서 돈다."
    ts "     ⛔ 여기서 멈춘다 — 뒤 계는 더 비싸므로 원인을 먼저 볼 것."
    cd - >/dev/null; break
  fi
  cd - >/dev/null
done

ts "═══ 결산 ═══"
# ⛔⛔ 2026-08-16 — 여기서 --work "$WORK" 를 주면 **그 루트 하나로 db 를 통째로 덮어쓴다.**
#   collect_neb.py 는 2026-08-13 에 다중 루트로 고쳐졌는데 이 호출부가 단일 루트를 계속
#   넘기고 있었다. 실측: li2s 하나 돌렸더니 n_citable 1/8 → 0/2 가 되고
#   v2_ccpath/li3nd (0.229 eV, 인용 가능) 가 db 에서 사라졌다.
#   → 인자 없이 부른다 (기본이 ROOTS 전부). collect 쪽에도 축소 거부 가드를 넣었다.
python3 "$REPO/tools/sei/collect_neb.py" || true
