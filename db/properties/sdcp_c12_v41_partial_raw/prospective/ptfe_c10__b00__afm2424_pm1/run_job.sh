#!/usr/bin/env bash
# 이 잡의 상(phase)들을 순서대로 돈다. POTCAR 를 이 폴더에 놓고 실행.
#
# 🔴 회신 AV P0-2 (2026-08-31) — **VASP_CMD 는 폐지됐다.** 자유형 명령 문자열은
#   staged lock·봉인·receipt 를 전부 우회하는 뒷문이었다. 실행 명령은
#   VASP_LAUNCHER_KIND(mpirun|mpiexec|srun|none|wrapper) + VASP_NPROC + VASP_EXE
#   에서 **이 스크립트가 조립**한다. staged 번들에서는 run_staged.sh 가 유일한
#   진입로이고, 여기 직접 오면 lock-owner 토큰이 없어 거부된다.
#
# 상 사슬 (하나라도 끊기면 **멈춘다** — 조용히 건너뛰면 다른 계를 계산하게 된다):
#   pre    dipole off, LWAVE=T          → WAVECAR·CHGCAR
#   relax  ISTART=1 (pre 의 WAVECAR)     → CONTCAR·CHGCAR
#   static ICHARG=1 (relax 의 CHGCAR)    → 판정 에너지
#   dense  ICHARG=1 (**static** 의 CHGCAR) → k 수렴 확인
set -e
if [ -n "${VASP_CMD:-}" ] || [ -n "${VASP_LAUNCHER:-}" ]; then
  echo "⛔ VASP_CMD/VASP_LAUNCHER 는 폐지됐습니다 (회신 AV P0-2)."
  echo "   VASP_LAUNCHER_KIND / VASP_NPROC / VASP_EXE 를 쓰세요 — README 참조"; exit 1
fi
_ROOT=../..
# ⛔⛔ 2026-09-01 (회신 AZ P0-1) — **봉인 경로를 변수 하나로 묶는다.**
#   AY P0-1 패치가 잡 폴더에서 `POTCAR_ROOT_SEAL.json` 을 찾았는데 실물은
#   `../../POTCAR_ROOT_SEAL.json` 이다. 같은 파일 안에서 두 경로가 섞여 있었고
#   (아래 진공/해시 대조는 `../../` 를 제대로 썼다), 그 결과 **16잡이 전부
#   첫 launcher 검사에서 죽었다.** selftest 300건이 통과하는 동안
#   정상 launcher 경로를 한 번도 실행하지 않아 못 봤다.
#   ⇒ 경로는 여기 한 번만 적는다. 두 벌이면 또 갈라진다.
_SEAL="$_ROOT/POTCAR_ROOT_SEAL.json"
_seal_get() {   # $1 = 키 이름 → 값 (없으면 빈 문자열)
  python3 -c 'import json,sys;print(json.load(open(sys.argv[1])).get(sys.argv[2]) or "")'     "$_SEAL" "$1" 2>/dev/null || true
}
# ⛔ 회신 AV 해제조건 ③ — 시험 표시 **파일만으로는** 아무것도 못 끈다. MANIFEST 가
#   스스로 selftest_fixture=true 를 선언한 픽스처 번들에서만 유효하다. production
#   MANIFEST 에 그 필드를 심으면 해시가 바뀌어 EXPECT·봉인·분석기 대조가 전부 깨지고,
#   반송물에 마커가 섞이면 분석기가 PROVENANCE_FIXTURE_MARKER 로 영구 게이트한다.
_FIXTURE=0
if [ -f .SELFTEST_FIXTURE ]; then
  if [ ! -f "$_ROOT/MANIFEST.json" ]; then
    # 번들 **밖** 낱개 잡(회귀 하네스·임시 복사)이다 — 마커를 존중한다. 이 경로의
    # 산출물은 어차피 분석기가 PROVENANCE_FIXTURE_MARKER 로 영구 게이트한다.
    _FIXTURE=1
  elif python3 -c 'import json,sys;sys.exit(0 if json.load(open("../../MANIFEST.json")).get("selftest_fixture") else 1)' 2>/dev/null; then
    _FIXTURE=1
  fi
fi
_STAGED=""
if [ -f "$_ROOT/MANIFEST.json" ]; then
  _STAGED=$(python3 -c     'import json;print(json.load(open("../../MANIFEST.json")).get("staged_runner") or "")'     2>/dev/null || true)
fi
if [ "$_FIXTURE" != 1 ] && [ -n "$_STAGED" ]; then
  # 🔴 회신 AV P0-2 → **AY P0-2 로 주장 하향**. 이 검사는 run_job.sh 가 러너를
  #   거쳐 불렸는지 **표시**하는 것이지 **소유권 증명이 아니다.**
  #   ⛔ 종전 주석은 "값을 아는 것이 곧 소유 증명" 이라고 적었는데 **틀렸다** —
  #     `.lock_bundle` 은 같은 사용자가 **읽을 수 있으므로**, 그 값을 그대로
  #     RUNNER_TOKEN 에 넣으면 직접 호출이 통과한다 (회신 AY P0-2 실측 지적).
  #   ⇒ 이 게이트가 실제로 하는 일: **사고성 직접 실행**(러너를 안 거치고 잡
  #     폴더에서 바로 `bash run_job.sh`)을 막는다. 같은 사용자의 **의도적** 우회는
  #     막지 못하며, 그것은 위협모델 밖이다(계약 문제).
  #   ⚠ 그래서 사후 구분은 분석기가 진다 — receipt 의 `_runner_start` 가 정확히
  #     하나여야 하고(AY P0-2), 상별 실행파일·launcher 해시가 root seal 과 같아야
  #     한다(AY P0-1). 러너를 안 거친 실행은 `_runner_start` 가 없어 거기서 걸린다.
  [ -n "${RUNNER_TOKEN:-}" ] || {
    echo "⛔ run_job.sh 를 직접 부르지 마세요 — 'bash $_STAGED {1|2}' 가 유일한 실행 경로입니다"
    echo "   (러너 토큰이 없습니다 — 회신 AV P0-2·AY P0-2)"; exit 1; }
  _lk=$(cat "$_ROOT/.lock_bundle" 2>/dev/null || true)
  if [ -z "$_lk" ] || [ "$_lk" != "$RUNNER_TOKEN" ]; then
    echo "⛔ RUNNER_TOKEN 이 번들 lock 과 다릅니다 — run_staged.sh 가 발급한 실행만 유효합니다"
    echo "   (⚠ 이 검사는 사고성 직접 실행을 막는 표시일 뿐 소유권 증명이 아닙니다 — AY P0-2)"; exit 1
  fi
fi
# ── 실행 argv 조립 (자유형 문자열 없음 — 회신 AV P0-2) ─────────────────────
VASP_LAUNCHER_KIND=${VASP_LAUNCHER_KIND:?VASP_LAUNCHER_KIND 를 지정하세요 (mpirun|mpiexec|srun|none|wrapper)}
VASP_EXE=${VASP_EXE:?VASP_EXE 를 지정하세요 (실행파일 절대경로)}
[ -x "$VASP_EXE" ] || { echo "⛔ VASP_EXE 가 실행파일이 아닙니다: $VASP_EXE"; exit 1; }
_np_flag="-np"
case "$VASP_LAUNCHER_KIND" in
  mpirun|mpiexec|srun)
    [ "$VASP_LAUNCHER_KIND" = srun ] && _np_flag="-n"
    case "${VASP_NPROC:-}" in
      ''|*[!0-9]*|0) echo "⛔ VASP_NPROC 가 양의 정수가 아닙니다"; exit 1 ;;
    esac
    # ⛔⛔ 2026-09-01 (회신 AY P0-1) — **PATH 조회를 폐기한다.**
    #   종전: LAUNCHER_BIN=$(command -v "$VASP_LAUNCHER_KIND"). PATH 앞에 가짜
    #   mpirun 을 두면 그놈이 이겼고, 봉인된 VASP_EXE 를 인자로 받고도 무시할 수
    #   있었다. 이제 **봉인에 적힌 절대경로**만 쓴다 (매 상 재해시는 아래 루프에서).
    if [ "$_FIXTURE" != 1 ]; then
      [ -f "$_SEAL" ] || { echo "⛔ 봉인 파일이 없습니다: $_SEAL — SEAL_POTCAR_ROOT.sh 를 먼저 돌리세요"; exit 1; }
      _lsp=$(_seal_get launcher_path)
      _lsk=$(_seal_get launcher_kind)
      [ -n "$_lsp" ] || { echo "⛔ root seal 에 launcher 가 없습니다 — SEAL_POTCAR_ROOT.sh 를 VASP_LAUNCHER_KIND·LAUNCHER_BIN 과 함께 다시 돌리세요 (회신 AY P0-1)"; exit 1; }
      [ "$_lsk" = "$VASP_LAUNCHER_KIND" ] || { echo "⛔ launcher kind 가 봉인($_lsk)과 다릅니다: $VASP_LAUNCHER_KIND"; exit 1; }
      if [ -n "${LAUNCHER_BIN:-}" ] && [ "$LAUNCHER_BIN" != "$_lsp" ]; then
        echo "⛔ LAUNCHER_BIN 이 봉인과 다릅니다 — 봉인: $_lsp"; exit 1
      fi
      LAUNCHER_BIN=$_lsp
    fi
    [ -n "${LAUNCHER_BIN:-}" ] && [ -x "$LAUNCHER_BIN" ] || {
      echo "⛔ launcher 실행파일이 없습니다: ${LAUNCHER_BIN:-<빈값>}"; exit 1; } ;;
  none) : ;;
  wrapper)
    [ -n "${VASP_WRAPPER:-}" ] && [ -x "${VASP_WRAPPER:-}" ] || {
      echo "⛔ KIND=wrapper 면 실행 가능한 VASP_WRAPPER 절대경로가 필요합니다"; exit 1; }
    case "${VASP_NPROC:-}" in
      ''|*[!0-9]*|0) echo "⛔ VASP_NPROC 가 양의 정수가 아닙니다"; exit 1 ;;
    esac ;;
  *) echo "⛔ 모르는 VASP_LAUNCHER_KIND: $VASP_LAUNCHER_KIND"; exit 1 ;;
esac
# ── 랭크 배치를 launcher 에 **실제로** 넘긴다 ────────────────────────────────
#   ⛔⛔ 2026-09-07 Codex v37 P0-1 — 종전엔 `-np $VASP_NPROC` 만 넘겼다. 러너는
#   "잡당 4노드" 로 메모리를 나눠 놓고 **그 배치를 실행에 강제하지 않았다** — 스케줄러가
#   192 랭크를 한 노드에 몰아도 검사는 통과한 채로 OOM 이 났다. 산술만 하고 끝내면
#   가드가 장식이다. run_staged 가 정한 VASP_RANKS_PER_NODE 를 여기서 플래그로 만든다.
#
#   ⚠ 플래그 이름이 MPI 구현마다 다르다. **추측하지 않고 `--version` 으로 판별**한다:
#     Open MPI  → `-N <ppn>`      (= --npernode)
#     MPICH/Hydra·Intel MPI → `-ppn <ppn>`
#     srun      → `--nodes/--ntasks-per-node`  (모호하지 않다)
#   판별에 실패하면 **거부한다** — 모르는 채로 배치 없이 던지는 것이 P0-1 그 자체다.
_PLACE=""; _SLOT_FILE=""
if [ "$VASP_LAUNCHER_KIND" = srun ] || [ "$VASP_LAUNCHER_KIND" = mpirun ]    || [ "$VASP_LAUNCHER_KIND" = mpiexec ]; then
  # ⛔⛔ 2026-09-08 (Codex 재검토 P0-1 a) — 플래그만으로는 **동시 잡이 같은 노드를 쓰는 것**을
  #   막지 못한다. run_staged 가 할당 호스트를 서로소 조각으로 나눠 _hostpool/free/ 에 두고,
  #   여기서 조각 하나를 **원자적으로 점유**(mv)해 hostfile 로 넘긴다. 끝나면 돌려준다.
  #   모드 판별·플래그 규칙은 run_staged 가 한 번 정해 _place_flags.sh 로 준다 — 여기서 다시 안 한다.
  for _v in VASP_RANKS_PER_NODE VASP_PLACE_MODE; do
    if [ -z "$(eval echo "\${$_v:-}")" ]; then
      echo "⛔ $_v 가 없습니다 — 랭크 배치를 강제할 수 없습니다."
      echo "   'bash run_staged.sh {1|2}' 로 실행하면 사전검사·배치 프로브가 이 값을 정해 넘깁니다."
      exit 1
    fi
  done
  case "${VASP_RANKS_PER_NODE}" in ''|*[!0-9]*|0)
    echo "⛔ VASP_RANKS_PER_NODE 가 양의 정수가 아닙니다: $VASP_RANKS_PER_NODE"; exit 1 ;;
  esac
  if [ $(( 10#$VASP_NPROC % 10#$VASP_RANKS_PER_NODE )) -ne 0 ]; then
    echo "⛔ 랭크 $VASP_NPROC 이 노드당 $VASP_RANKS_PER_NODE 로 안 나뉩니다"; exit 1
  fi
  _NODES_EFF=$(( 10#$VASP_NPROC / 10#$VASP_RANKS_PER_NODE ))
  _ROOT_ABS=$(cd "$_ROOT" && pwd)
  [ -f "$_ROOT_ABS/_place_flags.sh" ] || { echo "⛔ $_ROOT_ABS/_place_flags.sh 가 없습니다 — run_staged 를 거치지 않았습니다"; exit 1; }
  # shellcheck disable=SC1090
  . "$_ROOT_ABS/_place_flags.sh"
  [ -d "$_ROOT_ABS/_hostpool/free" ] || { echo "⛔ 호스트 풀이 없습니다 — run_staged 의 배치 프로브를 거치지 않았습니다"; exit 1; }
  _try=0
  while [ -z "$_SLOT_FILE" ] && [ "$_try" -lt 3600 ]; do
    for _f in "$_ROOT_ABS"/_hostpool/free/slot_*; do
      [ -e "$_f" ] || continue
      if mv "$_f" "$_ROOT_ABS/_hostpool/busy/" 2>/dev/null; then
        _SLOT_FILE="$_ROOT_ABS/_hostpool/busy/$(basename "$_f")"; break
      fi
    done
    [ -n "$_SLOT_FILE" ] || { _try=$((_try+1)); sleep 1; }
  done
  [ -n "$_SLOT_FILE" ] || { echo "⛔ 호스트 조각을 1시간 안에 얻지 못했습니다 (동시 잡 수 > 조각 수?)"; exit 1; }
  # 끝나면(정상·오류·신호) 조각을 돌려준다 — 안 돌려주면 다음 잡이 굶는다
  trap '[ -n "$_SLOT_FILE" ] && [ -e "$_SLOT_FILE" ] && mv "$_SLOT_FILE" "$_ROOT_ABS/_hostpool/free/" 2>/dev/null; exit' EXIT INT TERM
  _PLACE=$(place_args "$VASP_PLACE_MODE" "$_SLOT_FILE" "$_NODES_EFF" "$VASP_RANKS_PER_NODE")     || { echo "⛔ 모르는 VASP_PLACE_MODE: $VASP_PLACE_MODE"; exit 1; }
  echo "  ✔ 랭크 배치: $(basename "$_SLOT_FILE") = [$(paste -sd, "$_SLOT_FILE")] · 노드 $_NODES_EFF × ${VASP_RANKS_PER_NODE}랭크 · $_PLACE"
  printf '%s	%s	%s
' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$(basename "$_SLOT_FILE")" "$(paste -sd, "$_SLOT_FILE")" >> _placement.tsv
fi
_launch() {
  case "$VASP_LAUNCHER_KIND" in
    # shellcheck disable=SC2086  — _PLACE 는 우리가 만든 고정 토큰이다 (사용자 문자열 아님)
    mpirun|mpiexec|srun) "$LAUNCHER_BIN" $_PLACE "$_np_flag" "$VASP_NPROC" "$VASP_EXE" ;;
    none)                "$VASP_EXE" ;;
    # ⛔ 2026-09-08 (Codex v38 P1-2) — wrapper 는 이 제출 경로에서 제외. 슬롯 점유·반납이 없어
    #   동시 잡의 자원이 실행 내내 서로소라는 보장을 확인할 수 없다. run_staged 가 먼저 막지만
    #   여기서도 막는다 (직접 호출 경로).
    wrapper)             echo "⛔ wrapper 는 이 제출 경로에서 지원하지 않습니다 (v38 P1-2)"; exit 1 ;;
  esac
}
[ -f POTCAR ] || { echo "⛔ POTCAR 를 이 폴더에 놓으세요 (POTCAR_SPEC.txt 의 변형)"; exit 1; }
# 🔴 회신 AB P0-8 — POTCAR **provenance 를 실행 전에 강제**한다. 종전엔 파일
#   존재만 봤다. 그래서 조립기가 allowlist 로 거부해도 그때 남아 있던 POTCAR 로
#   VASP 가 돌았다 — allowlist 실패가 계산 중단으로 이어지지 않았다.
#   셋을 요구한다: ① provenance 존재 ② 면제 아님 ③ 지금 POTCAR 의 sha 가 일치.
#   ③이 핵심 — 조립 뒤 POTCAR 를 바꿔치기하면 여기서 걸린다.
# ⛔ 회신 AF P0-7 — 종전엔 SKIP_POTCAR_PROVENANCE=1 **환경변수**로 우회됐다.
#   환경변수는 반송물에 흔적이 안 남아 분석기가 볼 수 없다. 시험 장치는 파일로 표시하고
#   (`.SELFTEST_FIXTURE`), 배포 번들에는 그 파일이 없다 — files_sha256 이 전 파일을
#   덮으므로 나중에 만들어 넣으면 무결성 검사에서 걸린다.
if [ "$_FIXTURE" != 1 ]; then
  [ -f POTCAR_PROVENANCE.json ] || {
    echo "⛔ POTCAR_PROVENANCE.json 이 없습니다 — POTCAR 를 손으로 놓지 말고"
    echo "   PP=... POTCAR_ALLOWLIST=/abs/site_allow.txt bash POTCAR_ASSEMBLE.sh"; exit 1; }
  python3 - <<'PYCHK' || exit 1
import hashlib, json, sys
try:
    d = json.load(open("POTCAR_PROVENANCE.json"))
except Exception as e:
    sys.exit("⛔ POTCAR_PROVENANCE.json 파싱 실패: %s" % e)
if d.get("allowlist_waived"):
    sys.exit("⛔ allowlist 면제로 조립된 POTCAR 입니다 — 이 계약에서 폐지됐습니다")
if not d.get("allowlist"):
    sys.exit("⛔ provenance 에 allowlist 경로가 없습니다 — 대조 없이 조립됐습니다")
if not d.get("allowlist_sha256"):
    sys.exit("⛔ provenance 에 allowlist 내용 SHA 가 없습니다 — 경로만으로는 "
             "어느 allowlist 였는지 확인할 수 없습니다")
h = hashlib.sha256(open("POTCAR", "rb").read()).hexdigest()
if h != d.get("assembled_sha256"):
    sys.exit("⛔ POTCAR 가 조립 이후 바뀌었습니다 (지금 %s / 기록 %s)"
             % (h[:16], str(d.get("assembled_sha256"))[:16]))
print("  ✔ POTCAR provenance 확인 (allowlist 대조본 · sha 일치)")
PYCHK
fi
need() { [ -s "$1" ] || { echo "⛔ $1 없음/빈 파일 — $2"; exit 1; }; }

# ★ 회신 AA P0-5 / Q8 — **1회용(one-shot) 실행이다.** 시작 전에 산출물이 있으면
#   거부한다. 종전엔 "이미 완료 — 건너뜀" 으로 넘어갔는데, 그러면 남이 다른 설정으로
#   돌려 둔 결과를 우리 것으로 반송하게 된다 (회수 후에는 구별할 방법이 없다).
#   진짜로 이어서 돌려야 하면 ALLOW_RESUME=1 을 **명시적으로** 주고, 그 사실을
#   NOTES.txt 에 남겨 주세요.
# ⛔⛔ 회신 BA 해제조건 7 — `ALLOW_RESUME` 은 **폐지됐다.** 영수증 게이트가
#   재개를 언제나 막았으므로 있으나 마나가 아니라 함정이었다. 주면 거부한다.
if [ "${ALLOW_RESUME:-0}" = "1" ]; then
  echo "⛔ ALLOW_RESUME 은 폐지됐습니다 (회신 BA 해제조건 7) — 폴더를 새로 풀고"
  echo "   처음부터 돌려 주십시오."; exit 2
fi
# 계획된 이어달리기(dense 승격)만 완료 상을 건너뛴다. DENSE_PLAN.json 이 증거다.
# ⛔⛔ 회신 BB P1 (2026-09-02) — 종전엔 **파일 존재만** 봤다. 그래서 계약이
#   "dense 전용 이어달리기" 가 아니라 "DENSE_PLAN.json 이 있으면 완료 상 전부
#   건너뛰기" 였다. 이름과 실제가 다른 게이트는 언젠가 다른 것을 통과시킨다.
#   ⇒ ① 이 잡이 **promote 목록에 있는지** 확인하고 ② 실제로 도는 상이 dense
#     **하나뿐인지** 확인한다. 아니면 거부한다.
_PLANCONT=0
if [ "${PLANNED_CONTINUATION:-0}" = "1" ]; then
  if [ ! -s "$_ROOT/DENSE_PLAN.json" ]; then
    echo "⛔ PLANNED_CONTINUATION=1 인데 $_ROOT/DENSE_PLAN.json 이 없습니다"; exit 2
  fi
  _JOBREL=$(python3 -c 'import os,sys;print(os.path.relpath(os.getcwd(), sys.argv[1]))' "$_ROOT")
  python3 - "$_ROOT/DENSE_PLAN.json" "$_JOBREL" <<'PYDP' || exit 2
import json, sys
# ⚠ 역슬래시 정규화를 넣었다가 heredoc→파이썬 문자열 두 겹을 지나며 이스케이프가
#   깨졌다 (2026-09-02 실측: SyntaxError). 이 러너는 POSIX 셸 전용이니 안 쓴다.
p, jr = sys.argv[1], sys.argv[2]
d = json.load(open(p, encoding="utf-8"))
pro = d.get("promote") or d.get("promoted") or []
keys = {(x if isinstance(x, str) else (x.get("job") or "")) for x in pro}
if not keys:
    sys.exit("⛔ DENSE_PLAN.json 에 promote 목록이 없습니다 — 무엇을 승격하는지 "
             "적히지 않은 계획은 이어달리기의 근거가 아닙니다 (회신 BB P1)")
if jr not in keys:
    sys.exit("⛔ 이 잡(%s)은 DENSE_PLAN 의 promote 목록에 **없습니다** — 계획된 "
             "이어달리기는 그 목록의 잡에만 허용됩니다 (목록 %d건). "
             "다른 잡을 이어 돌리려면 폴더를 새로 푸십시오." % (jr, len(keys)))
print("  ✔ DENSE_PLAN promote 목록에 있음: %s" % jr)
PYDP
  # dense 가 아직 안 돌았고 나머지가 완료여야 "dense 승격" 이다
  if [ -f dense/OUTCAR ] && grep -aq "General timing" dense/OUTCAR; then
    echo "⛔ dense 가 이미 완료입니다 — 승격할 것이 없습니다 (이어달리기 아님)"; exit 2
  fi
  _PLANCONT=1
fi
if [ "$_PLANCONT" != 1 ]; then
  _stale=""
  for ph in pre relax static dense; do
    [ -d "$ph" ] || continue
    for f in OUTCAR WAVECAR CHGCAR vasprun.xml CONTCAR OSZICAR; do
      [ -e "$ph/$f" ] && _stale="$_stale $ph/$f"
    done
  done
  if [ -n "$_stale" ]; then
    echo "⛔ 실행 전 산출물이 이미 있습니다:$_stale"
    echo "   이 잡은 **1회용**입니다. 이어 돌리면 다른 설정의 결과가 섞입니다."
    echo "   폴더를 새로 풀고 처음부터 돌려 주세요 (재개는 폐지됐습니다 — BA 해제조건 7)."
    exit 1
  fi
fi

for ph in pre relax static dense; do
  [ -d "$ph" ] || continue
  if [ -f "$ph/OUTCAR" ] && grep -aq "General timing" "$ph/OUTCAR"; then
    # ⛔ 회신 BB P1 — 완료 상 건너뛰기는 **계획된 이어달리기에서만** 허용된다.
    #   종전엔 이 줄이 무조건이라, 게이트 문구와 달리 아무 때나 건너뛸 수 있었다.
    if [ "$_PLANCONT" != 1 ]; then
      echo "⛔ $ph 가 이미 완료인데 계획된 이어달리기가 아닙니다 — 건너뛰지 "
      echo "   않습니다 (폴더를 새로 푸십시오)."; exit 1
    fi
    echo "  ✓ $ph 이미 완료 — 건너뜀 (계획된 이어달리기 · DENSE_PLAN promote)"; continue
  fi
  if [ "$_PLANCONT" = 1 ] && [ "$ph" != dense ]; then
    echo "⛔ 계획된 이어달리기인데 **$ph 를 새로 돌려야 합니다** — 이것은 dense "
    echo "   승격이 아닙니다 (계약: dense 하나만 추가). 폴더를 새로 푸십시오."
    exit 1
  fi
  cp POTCAR "$ph/"
  # 🔴 회신 BE P1 — 상 폴더에 **실제로 복사된** POTCAR 의 해시를 receipt 에 남긴다.
  #   종전엔 루트 POTCAR 만 provenance 와 대조했고, 상 폴더 사본은 실행 시점 해시가
  #   반송물 어디에도 없었다 (결박 없음). 분석기가 POTCAR_PROVENANCE.assembled_sha256 과 대조한다.
  _pot_h=$(sha256sum "$ph/POTCAR" | cut -d" " -f1)
  case "$ph" in
    pre)   cp POSCAR pre/POSCAR ;;
    relax) cp POSCAR relax/POSCAR
           if [ -d pre ]; then
             need pre/WAVECAR "pre 상이 WAVECAR 를 안 남겼다 (ISTART=1 이 무의미해진다)"
             need pre/CHGCAR  "pre 상이 CHGCAR 를 안 남겼다"
             cp pre/WAVECAR pre/CHGCAR relax/
           fi ;;
    static) if [ -d relax ]; then
              need relax/CONTCAR "relax 를 먼저 완주시킬 것"
              need relax/CHGCAR  "ICHARG=1 인데 승계할 전하밀도가 없다 (relax LCHARG=.TRUE. 확인)"
              cp relax/CONTCAR static/POSCAR
              cp relax/CHGCAR  static/CHGCAR
            elif [ -f PARENT_GEOM ]; then
              # 회신 AO P0-4 (2026-08-31) — nzmag canary 는 부모 기체 기준과 **같은
              #   기하**여야 한다. 종전엔 부모가 relax/CONTCAR 로 static 을 돌고
              #   canary 는 자기 루트 POSCAR 를 써서 두 에너지 차에 **구조 이완
              #   에너지가 섞였다** — 스핀 검사가 오염됐다. 부모 기하를 그대로 받는다.
              _pg=$(tr -d " \t\r\n" < PARENT_GEOM)
              [ -d "$_pg" ] || { echo "PARENT_GEOM 이 가리키는 부모가 없다: $_pg"; exit 1; }
              if [ -d "$_pg/relax" ]; then
                need "$_pg/relax/CONTCAR" "부모 기체 relax 를 먼저 완주시킬 것 (canary 는 같은 기하)"
                cp "$_pg/relax/CONTCAR" static/POSCAR
              else
                need "$_pg/POSCAR" "부모 루트 POSCAR 없음"
                cp "$_pg/POSCAR" static/POSCAR
              fi
              echo "  canary 기하 = 부모($_pg) 와 동일"
            else
              # 단일점 모드 — relax 가 애초에 없다. 루트 POSCAR 를 그대로 쓰고
              # ISTART=0/ICHARG=2 (원자중첩)로 시작한다. CHGCAR 입력 없음.
              cp POSCAR static/POSCAR
            fi ;;
    dense)  if [ -d relax ]; then
              need relax/CONTCAR "relax 를 먼저 완주시킬 것"
              cp relax/CONTCAR dense/POSCAR
            else
              cp POSCAR dense/POSCAR          # 단일점 — 기하가 안 변한다
            fi
            need static/CHGCAR "dense 는 **static** 의 전하밀도를 승계한다 — static 먼저"
            cp static/CHGCAR dense/CHGCAR ;;
  esac
  # 🔴 회신 AV P0-2 — **상 직전마다** 실행파일을 봉인과 재대조하고 receipt 에
  #   append 한다. 러너 시작 때 한 번 보는 것으로는 긴 실행 중 교체를 못 잡고,
  #   receipt 는 분석기가 읽는 **필수 반송물**이다
#   (열 9개: ts phase exe_sha exe kind nproc launcher launcher_sha potcar_sha — AY P0-1 · BE P1).
  _exe_h=$(sha256sum "$VASP_EXE" | cut -d" " -f1)
  if [ "$_FIXTURE" != 1 ] && [ -f "$_SEAL" ]; then
    _sealed=$(_seal_get vasp_executable_sha256)
    if [ -z "$_sealed" ] || [ "$_exe_h" != "$_sealed" ]; then
      echo "⛔ $ph 직전: 실행파일이 root 봉인과 다릅니다 (지금 $_exe_h / 봉인 $_sealed)"; exit 1
    fi
    if [ "$VASP_LAUNCHER_KIND" = wrapper ]; then
      _wr_h=$(sha256sum "$VASP_WRAPPER" | cut -d" " -f1)
      _wsealed=$(_seal_get launcher_wrapper_sha256)
      if [ -z "$_wsealed" ] || [ "$_wr_h" != "$_wsealed" ]; then
        echo "⛔ $ph 직전: wrapper 가 봉인과 다릅니다"; exit 1
      fi
    fi
    # ⛔ 회신 AY P0-1 — named launcher 도 **상 직전마다** 재해시해 봉인과 대조한다.
    #   실행파일만 보던 종전 검사로는 launcher 교체를 못 잡았다.
    case "$VASP_LAUNCHER_KIND" in
      mpirun|mpiexec|srun)
        _lh=$(sha256sum "$LAUNCHER_BIN" | cut -d" " -f1)
        _lsealed=$(_seal_get launcher_sha256)
        if [ -z "$_lsealed" ] || [ "$_lh" != "$_lsealed" ]; then
          echo "⛔ $ph 직전: launcher 가 봉인과 다릅니다 (지금 $_lh / 봉인 $_lsealed)"; exit 1
        fi ;;
    esac
  fi
  # 영수증 9열 (회신 AY P0-1·P1 + BE P1): ts phase exe_sha exe kind nproc launcher launcher_sha potcar_sha
  case "$VASP_LAUNCHER_KIND" in
    mpirun|mpiexec|srun) _rl="$LAUNCHER_BIN"; _rlh="${_lh:-$(sha256sum "$LAUNCHER_BIN" | cut -d" " -f1)}" ;;
    wrapper)             _rl="$VASP_WRAPPER"; _rlh="${_wr_h:-$(sha256sum "$VASP_WRAPPER" | cut -d" " -f1)}" ;;
    *)                   _rl="-"; _rlh="-" ;;
  esac
  printf '%s	%s	%s	%s	%s	%s	%s	%s	%s
'     "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$ph" "$_exe_h"     "$VASP_EXE" "$VASP_LAUNCHER_KIND" "${VASP_NPROC:-1}"     "$_rl" "$_rlh" "$_pot_h" >> EXECUTABLE_RECEIPT.tsv
  # 🔴 회신 BF P1 — receipt 를 쓴 뒤 **실행 직전**에 상 폴더 POTCAR 를 다시 해시한다.
  #   복사·해시(위)와 실행 사이의 변경을 종전엔 검출하지 못했다.
  _pot_h2=$(sha256sum "$ph/POTCAR" | cut -d" " -f1)
  [ "$_pot_h2" = "$_pot_h" ] || { echo "⛔ $ph 직전: POTCAR 가 receipt 기록 뒤에 바뀌었다 (기록 ${_pot_h:0:12} / 지금 ${_pot_h2:0:12})"; exit 1; }
  echo "  ▶ $ph"
  ( cd "$ph" && _launch > vasp.out 2>&1 )
  grep -aq "General timing" "$ph/OUTCAR" || {
    echo "⛔ $ph 가 정상종료하지 않았다 (General timing 없음) — 다음 상으로 안 넘어간다"; exit 1; }
  # WAVECAR 는 크다. relax 가 끝나면 pre 것은 필요 없다.
  [ "$ph" = relax ] && rm -f pre/WAVECAR relax/WAVECAR
done
echo "✅ $(basename "$PWD") 완료"
