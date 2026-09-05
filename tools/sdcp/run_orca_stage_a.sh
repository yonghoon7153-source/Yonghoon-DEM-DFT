#!/usr/bin/env bash
# =============================================================================
# run_orca_stage_a.sh — SDCP Stage A (중성 n=6 올리고머) ORCA Opt 실행기
#
# 회신 R4 (2026-08-29) 가 **조건부 GO** 를 낸 정확히 그 8잡을 위한 러너다.
# 조건 6개를 코드로 강제한다:
#   ① 현재 8개의 manifest·INP·XYZ SHA256 **동결** — 실행 전 기록하고, 바뀌면 멈춘다
#   ② `--allow_*` 우회 옵션 **사용 금지** — 이 러너는 빌더를 아예 호출하지 않는다
#   ③ 정본 입력 **읽기 전용** 보존, 계산은 **seed 별 별도 scratch 복사본**에서
#   ④ 시작 XYZ · INP · OUT · 최종 XYZ 를 **서로 다른 파일**로 보존
#      + SHA256 · ORCA 버전 · 실행 명령 기록
#   ⑤ `builder_commit` 만 믿지 말고 **builder 파일 자체의 SHA256** 도 기록
#   ⑥ 이 결과로 Stage B 를 열지 않는다 — receipt 에 그 문구를 박는다
#
# ⛔⛔ 이 러너가 막는 가장 큰 함정 (R4 위험 ③):
#   ORCA 는 `* xyzfile 0 1 foo.xyz` 로 시작해 최적화가 끝나면 **`foo.xyz` 를
#   최종구조로 덮어쓴다.** 같은 폴더에서 돌리면 **시작구조 증거가 사라진다.**
#   → scratch 로 복사해 거기서 돌리고, 정본과 `*_start.xyz` 는 손대지 않는다.
#
# ⛔ 이 도구가 **못 하는 것**:
#   · ORCA 출력의 물리적 타당성을 판정하지 않는다 (수렴·안정성 판정은 analyzer 몫).
#   · Stage B 로 넘어가도 되는지 판단하지 않는다 — 조건 ⑥ 때문에 **넘어가면 안 된다**.
#   · 병렬화를 위해 `%pal` 을 덧붙이는데, 그래서 **실행된 입력은 정본과 1줄 다르다.**
#     그 차이를 숨기지 않고 receipt 에 정본 SHA·실행본 SHA·diff 를 **둘 다** 남긴다.
#
#   ORCA=/path/to/orca NPROCS=8 bash tools/sdcp/run_orca_stage_a.sh <stageA_dir> <work_dir>
#   bash tools/sdcp/run_orca_stage_a.sh --selftest
# =============================================================================
set -uo pipefail; set +H

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
BUILDER="$REPO/tools/sdcp/build_v7c_trimer.py"
ORCA=${ORCA:-orca}
NPROCS=${NPROCS:-8}
MAXCORE=${MAXCORE:-6000}

# ⛔⛔ 2026-09-05 실측 — gs3 이 **같은 오류로 두 번** 죽었다 (09-05 02:45 · 14:16,
#   둘 다 `nprocs 8`, 둘 다 2시간을 태운 뒤):
#       [btl_tcp.c:559] recv(23) failed: Connection reset by peer (104)   × 수십 줄
#       ORCA finished by error termination in LEANSCF
#       Calling Command: mpirun -np 8 .../orca_leanscf_mpi
#   원인은 화학이 아니라 **전송층**이다: 한 대에서 도는데 OpenMPI 가 TCP BTL 로
#   통신하다 끊겼다. 단일노드는 공유메모리(vader/sm)만 쓰면 되고, 그러면 이 오류
#   계열이 원천 차단된다.
#   ⚠ 판본 차이: OpenMPI 4.x = `vader` · 5.x = `sm`. 둘 다 적어 두면 없는 쪽은 무시된다.
#   ⚠ 이 설정은 **속도가 아니라 생존**을 위한 것이다 — 결과값을 바꾸지 않는다.
#   손으로 끄려면 `STAGEA_MPI_BTL=` (빈 값) 으로 부른다.
export OMPI_MCA_btl=${STAGEA_MPI_BTL-self,vader,sm}
MPI_BTL_NOTE="${OMPI_MCA_btl:-<unset>}"

ts(){ echo "[$(date +%H:%M:%S)] $*"; }
sha(){ sha256sum "$1" 2>/dev/null | cut -d' ' -f1; }

# ── selftest ────────────────────────────────────────────────────────────────
if [ "${1:-}" = "--selftest" ]; then
  T=$(mktemp -d); ok=0; bad=0
  chk(){ if [ "$1" = "1" ]; then echo "  ⭕ $2"; ok=$((ok+1)); else echo "  ⛔ $2"; bad=$((bad+1)); fi; }

  # 가짜 stage A: gs0 하나
  mkdir -p "$T/a/gs0"
  printf '! RKS r2SCAN-3c Opt TightSCF Hirshfeld\n%%maxcore 6000\n* xyzfile 0 1 dp6_gs0_neutral.xyz\n' \
    > "$T/a/gs0/dp6_gs0_neutral.inp"
  printf '2\ncomment\nH 0.0 0.0 0.0\nH 0.0 0.0 0.9\n' > "$T/a/gs0/dp6_gs0_neutral.xyz"
  echo '{"geometry_seeds":[{"gseed":0,"dir":"gs0","tag":"dp6_gs0_neutral"}]}' \
    > "$T/a/manifest_stage_a.json"

  # 가짜 orca: 최종 xyz 를 **덮어쓰고** out 을 낸다 (실제 ORCA 동작 재현)
  cat > "$T/fakeorca" <<'EOS'
#!/usr/bin/env bash
# ⚠ 러너는 버전을 뽑으려고 **인자 없이** 한 번 부른다. 그때 파일을 쓰면
#   CWD(= repo 루트)에 `.xyz` 쓰레기가 생긴다 (2026-08-30 실측: 커밋까지 됐다).
[ -n "${1:-}" ] || { echo "Program Version 6.1.0 - RELEASE"; exit 0; }
d=$(dirname "$1"); b=$(basename "$1" .inp)
printf '2\ncomment relaxed\nH 0.0 0.0 0.0\nH 0.0 0.0 0.74\n' > "$d/$b.xyz"
echo "Program Version 6.1.0 - RELEASE"
echo "THE OPTIMIZATION HAS CONVERGED"
echo "FINAL SINGLE POINT ENERGY      -1.234567890"
echo "****ORCA TERMINATED NORMALLY****"
EOS
  chmod +x "$T/fakeorca"

  START_SHA=$(sha "$T/a/gs0/dp6_gs0_neutral.xyz")
  ORCA="$T/fakeorca" NPROCS=2 bash "$0" "$T/a" "$T/w" >"$T/log" 2>&1
  rc=$?
  chk "$([ $rc -eq 0 ] && echo 1 || echo 0)" "정상 실행이 exit 0"
  chk "$([ "$(sha "$T/a/gs0/dp6_gs0_neutral.xyz")" = "$START_SHA" ] && echo 1 || echo 0)" \
      "[음성 R4③] **정본 시작 xyz 가 안 덮어써졌다** (ORCA 가 덮어쓰는 것을 scratch 가 막는다)"
  chk "$([ -f "$T/w/gs0/dp6_gs0_neutral_start.xyz" ] && echo 1 || echo 0)" \
      "시작 xyz 를 별도 파일로 보존한다 (*_start.xyz)"
  chk "$([ -f "$T/w/gs0/dp6_gs0_neutral_final.xyz" ] && echo 1 || echo 0)" \
      "최종 xyz 를 **다른 이름으로** 보존한다 (*_final.xyz)"
  chk "$([ "$(sha "$T/w/gs0/dp6_gs0_neutral_start.xyz")" \
        != "$(sha "$T/w/gs0/dp6_gs0_neutral_final.xyz")" ] && echo 1 || echo 0)" \
      "시작과 최종이 서로 다른 파일·다른 내용이다"
  for k in canonical_inp_sha256 canonical_xyz_sha256 executed_inp_sha256 \
           final_xyz_sha256 out_sha256 orca_version builder_sha256 command; do
    chk "$(grep -q "\"$k\"" "$T/w/gs0/receipt.json" && echo 1 || echo 0)" "receipt 에 $k"
  done
  chk "$(grep -q "Stage B" "$T/w/gs0/receipt.json" && echo 1 || echo 0)" \
      "receipt 에 조건⑥(이 결과로 Stage B 를 열지 않는다) 문구"

  # 음성: 정본이 실행 후 바뀌면 다음 실행이 멈춘다
  echo "# tampered" >> "$T/a/gs0/dp6_gs0_neutral.inp"
  ORCA="$T/fakeorca" NPROCS=2 bash "$0" "$T/a" "$T/w" >"$T/log2" 2>&1
  chk "$([ $? -ne 0 ] && echo 1 || echo 0)" \
      "[음성 ①] 정본 INP 가 바뀌면 **동결 위반으로 멈춘다** (조용히 재실행 안 한다)"
  chk "$(grep -q "동결" "$T/log2" && echo 1 || echo 0)" "그 사유를 로그에 남긴다"

  # ── ⛔ 2026-08-30 실측 두 건 (gs2~gs7 여섯 잡이 rc=126 즉사) ────────────────
  # ⓐ 죽은 잡의 receipt 에 relaxed:true 가 찍혔다. ORCA 는 basis set 을 읽는 동안
  #    입력 xyz 를 다시 쓰므로, 즉사해도 start != final 이 된다.
  cat > "$T/failorca" <<'EOS'
#!/usr/bin/env bash
[ -n "${1:-}" ] || { echo "Program Version 6.1.1 - RELEASE"; exit 0; }
d=$(dirname "$1"); b=$(basename "$1" .inp)
printf '2\ncomment rewritten-by-orca\nH 0.0 0.0 0.0\nH 0.0 0.0 0.90000\n' > "$d/$b.xyz"
echo "Program Version 6.1.1 - RELEASE"
echo "ERROR (ORCA_MAIN): For parallel runs ORCA has to be called with full pathname"
exit 126
EOS
  chmod +x "$T/failorca"
  mkdir -p "$T/a2/gs0"; cp "$T/a/gs0/"* "$T/a2/gs0/"; cp "$T/a/manifest_stage_a.json" "$T/a2/"
  ORCA="$T/failorca" NPROCS=2 bash "$0" "$T/a2" "$T/w3" >"$T/log3" 2>&1 || true
  chk "$(grep -q '"relaxed": false' "$T/w3/gs0/receipt.json" && echo 1 || echo 0)" \
      "[음성] **죽은 잡은 relaxed:false** — start≠final 이어도 이완이 아니다 (rc=126 즉사)"
  chk "$(grep -q '"orca_terminated_normally": false' "$T/w3/gs0/receipt.json" && echo 1 || echo 0)" \
      "[음성] 정상종료 여부를 receipt 에 **따로** 남긴다"
  chk "$(grep -q '"returncode": 126' "$T/w3/gs0/receipt.json" && echo 1 || echo 0)" \
      "[음성] rc 를 그대로 기록한다"
  chk "$(grep -q '비정상' "$T/log3" && echo 1 || echo 0)" \
      "[음성] 로그가 비정상이라고 말한다"

  # ⓑ 병렬 ORCA 는 **절대경로**로 불러야 한다. 이름으로 주면 러너가 절대경로로 바꾼다.
  mkdir -p "$T/bin"; cp "$T/fakeorca" "$T/bin/orca_selftest"; chmod +x "$T/bin/orca_selftest"
  mkdir -p "$T/a3/gs0"; cp "$T/a/gs0/"* "$T/a3/gs0/"; cp "$T/a/manifest_stage_a.json" "$T/a3/"
  PATH="$T/bin:$PATH" ORCA=orca_selftest NPROCS=2 bash "$0" "$T/a3" "$T/w4" >"$T/log4" 2>&1 || true
  chk "$(grep -q "$T/bin/orca_selftest" "$T/w4/gs0/receipt.json" && echo 1 || echo 0)" \
      "[음성] 이름으로 준 ORCA 가 **절대경로로 바뀌어** 기록된다 (%pal 은 full pathname 요구)"
  ORCA=orca_no_such_binary_xyz NPROCS=2 bash "$0" "$T/a3" "$T/w5" >"$T/log5" 2>&1
  chk "$([ $? -ne 0 ] && echo 1 || echo 0)" \
      "[음성] 절대경로로 못 만들면 **돌리지 않고 멈춘다**"
  chk "$([ ! -e "$PWD/.xyz" ] && echo 1 || echo 0)" \
      "[음성] selftest 가 CWD 에 쓰레기 파일을 안 남긴다 (러너는 버전 확인차 ORCA 를 \
인자 없이 한 번 부른다 — 2026-08-30 에 그래서 repo 에 .xyz 가 커밋됐다)"

  # 음성: ORCA 가 없으면 깨끗하게 거부
  ORCA="$T/nonexistent_orca" bash "$0" "$T/a" "$T/w2" >"$T/log3" 2>&1
  chk "$([ $? -ne 0 ] && echo 1 || echo 0)" "[음성] ORCA 실행파일이 없으면 거부"

  # ══ 2026-09-02 — ONLY 필터 + seed lock (동시 실행) ═══════════════════════
  #   왜: 전역 lock 하나라 인스턴스가 하나뿐이었고, ORCA 가 8랭크 중 3개만 쓰는데도
  #   남는 코어를 못 썼다 (gs2 실측). seed 는 서로 독립이라 나눠 돌려도 된다.
  mkdir -p "$T/a6/gs0" "$T/a6/gs1"
  cp "$T/a/gs0/dp6_gs0_neutral.inp" "$T/a6/gs0/"
  cp "$T/a/gs0/dp6_gs0_neutral.xyz" "$T/a6/gs0/"
  sed 's/gs0/gs1/g' "$T/a/gs0/dp6_gs0_neutral.inp" > "$T/a6/gs1/dp6_gs1_neutral.inp"
  cp "$T/a/gs0/dp6_gs0_neutral.xyz" "$T/a6/gs1/dp6_gs1_neutral.xyz"
  echo '{"geometry_seeds":[{"gseed":0,"dir":"gs0","tag":"dp6_gs0_neutral"},
                           {"gseed":1,"dir":"gs1","tag":"dp6_gs1_neutral"}]}' \
    > "$T/a6/manifest_stage_a.json"
  ONLY=gs1 ORCA="$T/fakeorca" NPROCS=2 bash "$0" "$T/a6" "$T/w6" >"$T/log6" 2>&1 || true
  chk "$([ -f "$T/w6/gs1/receipt.json" ] && [ ! -f "$T/w6/gs0/receipt.json" ] && echo 1 || echo 0)" \
      "ONLY=gs1 은 **gs1 만** 돌린다 (gs0 은 손대지 않는다)"
  ONLY="gs0 gs1" ORCA="$T/fakeorca" NPROCS=2 bash "$0" "$T/a6" "$T/w7" >"$T/log7" 2>&1 || true
  chk "$([ -f "$T/w7/gs0/receipt.json" ] && [ -f "$T/w7/gs1/receipt.json" ] && echo 1 || echo 0)" \
      "ONLY 는 공백으로 여러 seed 를 받는다"
  # ⛔음성: 남이 잡고 있는 seed 는 **건드리지 않는다** (mkdir 원자성)
  mkdir -p "$T/w8/gs0/.lock_seed"; echo 999999 > "$T/w8/gs0/.lock_seed/pid"
  ONLY=gs0 ORCA="$T/fakeorca" NPROCS=2 bash "$0" "$T/a6" "$T/w8" >"$T/log8" 2>&1 || true
  chk "$([ ! -f "$T/w8/gs0/receipt.json" ] && grep -q "다른 인스턴스가 맡았다" "$T/log8" \
        && echo 1 || echo 0)" \
      "⛔음성: lock 이 잡힌 seed 는 **다른 인스턴스가 안 뺏는다** (같은 폴더 동시 실행 = 산출물 오염)"
  chk "$([ -d "$T/w8/gs0/.lock_seed" ] && echo 1 || echo 0)" \
      "⛔음성: 남의 lock 을 **지우지 않는다** (죽은 것으로 단정하지 않는다)"
  # 정상 종료 뒤에는 자기 lock 을 반납한다 — 안 그러면 다음 실행이 영영 막힌다
  chk "$([ ! -d "$T/w7/gs0/.lock_seed" ] && [ ! -d "$T/w7/gs1/.lock_seed" ] && echo 1 || echo 0)" \
      "끝난 seed 의 lock 은 반납된다 (남으면 재실행이 영영 막힌다)"
  # ⛔음성: ONLY 에 없는 이름을 줘도 조용히 전부 돌지 않는다
  ONLY=gs9 ORCA="$T/fakeorca" NPROCS=2 bash "$0" "$T/a6" "$T/w9" >"$T/log9" 2>&1 || true
  chk "$([ ! -f "$T/w9/gs0/receipt.json" ] && [ ! -f "$T/w9/gs1/receipt.json" ] && echo 1 || echo 0)" \
      "⛔음성: ONLY 에 없는 이름이면 **아무것도 안 돈다** (전부 도는 쪽으로 열리지 않는다)"

  rm -rf "$T"
  echo "selftest: $ok 통과 / $bad 실패"
  [ $bad -eq 0 ] || exit 1
  exit 0
fi

# ── 실행 ────────────────────────────────────────────────────────────────────
A=${1:?"stage A 디렉터리가 필요하다 (manifest_stage_a.json 이 있는 곳)"}
W=${2:?"작업 디렉터리가 필요하다 (정본과 분리된 scratch 루트)"}
MAN="$A/manifest_stage_a.json"
[ -f "$MAN" ] || { ts "⛔ $MAN 이 없다"; exit 1; }
# ⛔⛔ 2026-08-30 실측 — **병렬 ORCA 는 절대경로로 불러야 한다.**
#   `%pal nprocs N` 을 붙인 실행에서 ORCA 가 이름(PATH 해석)으로 불리면
#     ERROR (ORCA_MAIN): For parallel runs — ORCA has to be called with full pathname
#   으로 **rc=126** 에 즉사한다. 그런데 아래 존재 검사(`command -v`)는 이름도 통과시킨다.
#   실측: gs2~gs7 여섯 잡이 각 0.2 초 만에 죽었다 (gs0·gs1 은 절대경로로 돌아 멀쩡했다).
#   ⇒ 검사만 하지 말고 **여기서 절대경로로 바꾼다.** 못 바꾸면 그때 멈춘다.
case "$ORCA" in
  /*) : ;;
  *)  _abs=$(command -v "$ORCA" 2>/dev/null || true)
      if [ -n "$_abs" ]; then
        ORCA=$_abs
      else
        echo "⛔ ORCA 를 절대경로로 못 만든다: '$ORCA'"
        echo "   %pal 병렬 실행은 full pathname 을 요구한다 (rc=126 즉사)."
        echo "   ORCA=/절대/경로/orca 로 주거나 PATH 에 올려라."
        exit 1
      fi ;;
esac
command -v "$ORCA" >/dev/null 2>&1 || [ -x "$ORCA" ] || {
  ts "⛔ ORCA 를 찾을 수 없다: $ORCA  (ORCA=/full/path 로 지정)"; exit 1; }

# ⛔⛔ 2026-09-02 — **전역 lock 을 seed 별 lock 으로 바꾼다.**
#   종전엔 `/tmp/sdcp_orca_stage_a.lock` 하나라 인스턴스가 **하나만** 돌 수 있었다.
#   그래서 seed 8개가 순차로만 돌았고, 실측 결과 ORCA 가 8랭크 중 3개만 쓰는 바람에
#   (2026-09-02 gs2: 랭크 3개가 누적 CPU 2일 · 나머지 5개는 3시간 이하) 남는 코어를
#   두고도 벽시계가 77시간이었다. seed 끼리는 서로 독립이므로 **동시에 돌아도 된다**.
#   ⇒ lock 을 seed 폴더로 내리고, `ONLY` 로 맡을 seed 를 나눠 준다.
#   ⚠ 여전히 **한 seed 를 두 인스턴스가 잡는 일은 없다** (mkdir 은 원자적이다).
ONLY=${ONLY:-}                       # 예: ONLY="gs3 gs4" — 비우면 전부
STALE_LOCK_MIN=${STALE_LOCK_MIN:-0}  # >0 이면 그만큼 오래된 lock 을 죽은 것으로 본다

BSHA=$(sha "$BUILDER")                                   # 조건 ⑤
BCOMMIT=$(cd "$REPO" && git rev-parse HEAD 2>/dev/null || echo unknown)
mkdir -p "$W"
FREEZE="$W/FREEZE.sha256"                                # 조건 ①

TAGS=$(python3 -c "
import json,sys
m=json.load(open('$MAN'))
for s in m['geometry_seeds']: print(s['dir'], s['tag'])")
[ -n "$TAGS" ] || { ts "⛔ manifest 에 geometry_seeds 가 없다"; exit 1; }

# ① 동결 검사 — 처음이면 기록하고, 두 번째부터는 대조한다
NOW=$(mktemp)
{ echo "$(sha "$MAN")  manifest_stage_a.json"
  while read -r d t; do
    echo "$(sha "$A/$d/$t.inp")  $d/$t.inp"
    echo "$(sha "$A/$d/$t.xyz")  $d/$t.xyz"
  done <<< "$TAGS"; } | sort > "$NOW"
if [ -f "$FREEZE" ]; then
  if ! diff -q "$FREEZE" "$NOW" >/dev/null; then
    ts "⛔ 정본이 **동결** 이후 바뀌었다 (R4 조건①). 차이:"
    diff "$FREEZE" "$NOW" | head -10
    ts "   재생성은 금지다. 되돌리거나, 새 감사 고정점으로 리뷰를 다시 받아라."
    rm -f "$NOW"; exit 1
  fi
  ts "✓ 동결 대조 통과 ($(wc -l < "$FREEZE") 항목)"
else
  cp "$NOW" "$FREEZE"; ts "✓ 동결 기록 생성 — $FREEZE ($(wc -l < "$FREEZE") 항목)"
fi
rm -f "$NOW"

VER=$("$ORCA" 2>&1 | grep -am1 "Program Version" | sed 's/^ *//' || true)

while read -r d t; do
  SD="$W/$d"                                              # ③ seed 별 scratch
  # ── ONLY 필터 (2026-09-02) — 여러 인스턴스가 seed 를 나눠 맡는다 ──────────
  if [ -n "$ONLY" ]; then
    case " $ONLY " in *" $d "*) : ;; *) continue ;; esac
  fi
  if grep -aq "ORCA TERMINATED NORMALLY" "$SD/$t.out" 2>/dev/null; then
    ts "  ✓ $d/$t 이미 완료"; continue
  fi
  # ── seed lock — 같은 seed 를 두 인스턴스가 잡지 않는다 (mkdir 은 원자적) ──
  mkdir -p "$SD"
  SEEDLOCK="$SD/.lock_seed"
  if [ "${STALE_LOCK_MIN:-0}" -gt 0 ] && [ -d "$SEEDLOCK" ]; then
    if [ -z "$(find "$SEEDLOCK" -maxdepth 0 -mmin -"$STALE_LOCK_MIN" 2>/dev/null)" ]; then
      _op=$(cat "$SEEDLOCK/pid" 2>/dev/null || echo "?")
      if [ "$_op" = "?" ] || ! kill -0 "$_op" 2>/dev/null; then
        ts "  ⚠ $d: ${STALE_LOCK_MIN}분 넘은 죽은 lock 을 치운다 (pid $_op)"
        rm -rf "$SEEDLOCK"
      fi
    fi
  fi
  if ! mkdir "$SEEDLOCK" 2>/dev/null; then
    ts "  ⏭ $d 는 다른 인스턴스가 맡았다 (pid $(cat "$SEEDLOCK/pid" 2>/dev/null || echo ?))"
    continue
  fi
  echo $$ > "$SEEDLOCK/pid"
  # ⚠ **우리 것일 때만** 지운다. 남의 lock 을 치우지 않는다.
  trap '[ "$(cat "$SEEDLOCK/pid" 2>/dev/null)" = "$$" ] && rm -rf "$SEEDLOCK"' EXIT
  ts "═══ $d/$t ═══"
  cp "$A/$d/$t.inp" "$SD/$t.inp"
  cp "$A/$d/$t.xyz" "$SD/$t.xyz"
  cp "$A/$d/$t.xyz" "$SD/${t}_start.xyz"                   # ④ 시작구조 별도 보존
  chmod a-w "$SD/${t}_start.xyz"

  # 병렬화 — 정본을 안 건드리고 실행본을 따로 만든다. 차이를 receipt 에 남긴다.
  RUN="$SD/${t}_run.inp"
  { head -1 "$SD/$t.inp"; echo "%pal nprocs $NPROCS end"; tail -n +2 "$SD/$t.inp"; } > "$RUN"
  CMD="$ORCA ${t}_run.inp"
  ts "  ▶ $CMD  (nprocs $NPROCS)"
  ( cd "$SD" && "$ORCA" "${t}_run.inp" > "$t.out" 2>&1 )
  RC=$?

  # ORCA 는 `<base>.xyz` 를 최종구조로 덮어쓴다 → 다른 이름으로 확보
  [ -f "$SD/${t}_run.xyz" ] && cp "$SD/${t}_run.xyz" "$SD/${t}_final.xyz"
  [ -f "$SD/${t}_final.xyz" ] || { [ -f "$SD/$t.xyz" ] && cp "$SD/$t.xyz" "$SD/${t}_final.xyz"; }

  python3 - "$SD" "$t" "$A/$d" "$BSHA" "$BCOMMIT" "$CMD" "$VER" "$RC" "$MPI_BTL_NOTE" <<'PY'
import hashlib, json, os, sys
sd, t, adir, bsha, bcommit, cmd, ver, rc, mpibtl = sys.argv[1:10]
h = lambda p: (hashlib.sha256(open(p,'rb').read()).hexdigest()
               if os.path.isfile(p) else None)
start, final = f"{sd}/{t}_start.xyz", f"{sd}/{t}_final.xyz"
r = {
 "schema": "sdcp_stage_a_orca_receipt/v1",
 "seed_tag": t, "returncode": int(rc),
 "canonical_dir": os.path.abspath(adir),
 "canonical_inp_sha256": h(f"{adir}/{t}.inp"),
 "canonical_xyz_sha256": h(f"{adir}/{t}.xyz"),
 "executed_inp_sha256": h(f"{sd}/{t}_run.inp"),
 "executed_inp_differs_only_by": "%pal nprocs 줄 1개 (병렬화). 정본은 손대지 않았다",
 "start_xyz_sha256": h(start),
 "final_xyz_sha256": h(final),
 "out_sha256": h(f"{sd}/{t}.out"),
 "orca_version": ver or None,
 "command": cmd,
 "mpi_btl": mpibtl,
 "⚠_mpi_btl_왜_있나": ("단일노드인데 OpenMPI 가 TCP BTL 로 통신하다 끊겨 gs3 이 두 번 죽었다 "
                       "(2026-09-05 02:45·14:16 · `Connection reset by peer` in orca_leanscf_mpi). "
                       "공유메모리만 쓰도록 고정한 것이고 **결과값을 바꾸지 않는다**."),
 "builder_sha256": bsha, "repo_commit": bcommit,
 "⛔_조건6": "이 결과로 Stage B 를 열지 않는다 — P0-2~5 수정 후 실제 Stage A 산출물로 재심사 (회신 R4)",
 "⚠": "이 8개는 서로 다른 시작 conformer 이지 통계적으로 독립인 8개 반복측정이 아니다 (회신 R4)",
}
# ⛔⛔ 2026-08-30 실측 fail-open — 죽은 잡의 receipt 에 `relaxed: true` 가 찍혔다.
#   ORCA 는 basis set 을 읽는 동안 입력 xyz 를 **다시 쓴다**. 그래서 rc=126 으로
#   즉사해도 start != final 이 되어 "이완됐다" 로 기록됐다 (gs2~gs7 여섯 건 전부).
#   receipt 은 provenance 원본이라, 여기서 거짓말하면 아래 모든 판독이 오염된다.
#   ⇒ **정상종료(rc==0 + ORCA TERMINATED NORMALLY)를 같이 요구한다.**
_out = f"{sd}/{t}.out"
_norm = False
try:
    with open(_out, "rb") as _f:
        _norm = b"ORCA TERMINATED NORMALLY" in _f.read()
except OSError:
    pass
r["orca_terminated_normally"] = _norm
r["relaxed"] = bool(_norm and int(rc) == 0
                    and r["start_xyz_sha256"] and r["final_xyz_sha256"]
                    and r["start_xyz_sha256"] != r["final_xyz_sha256"])
if not _norm:
    r["⛔"] = ("정상종료 문구가 없다 — 이 잡은 실패다. start/final 이 달라도 "
               "**이완이 아니다** (ORCA 가 읽는 중 입력 xyz 를 다시 쓴다)")
json.dump(r, open(f"{sd}/receipt.json","w"), ensure_ascii=False, indent=1)
print(f"  receipt: relaxed={r['relaxed']} · rc={rc}")
PY
  grep -aq "ORCA TERMINATED NORMALLY" "$SD/$t.out" \
    && ts "  ✓ 정상종료" || { ts "  ✗ 비정상 — 꼬리:"; tail -5 "$SD/$t.out"; }
  # seed lock 반납 — 다음 seed 로 넘어가기 전에 (trap 은 프로세스 종료용 보험이다)
  [ "$(cat "$SEEDLOCK/pid" 2>/dev/null)" = "$$" ] && rm -rf "$SEEDLOCK"
  trap - EXIT
done <<< "$TAGS"

ts "═══ 결산 ═══"
for f in "$W"/*/receipt.json; do
  [ -f "$f" ] || continue
  python3 -c "
import json,sys; r=json.load(open('$f'))
print(f\"  {r['seed_tag']:22s} rc={r['returncode']} relaxed={r['relaxed']} \"
      f\"final={str(r['final_xyz_sha256'])[:12]}\")"
done
ts "⛔ 조건⑥ — 이 결과로 Stage B 를 열지 않는다. P0-2~5 수정 후 재심사."
