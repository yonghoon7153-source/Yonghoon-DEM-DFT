#!/usr/bin/env bash
# =============================================================================
# run_all.sh (W_ad round2 v1) — 탄소 P2′ 23 잡 + 은 a4 1 잡 · 단계 (P 파일럿 → 1 → 2 → 3 → 4) · 탄소 잡마다 사전등록 재시도 사다리
#   (단 0 → r1 ⓐ+ⓑ → r2 ⓑ) · 은 a4 = 두 단계 한 번 · SCF 판정 = OSZICAR 마지막 전자 반복행 (검사기와 같은 계약 · OUTCAR 문구로 판정하지 않는다)
#   필수: VASP_CMD · POTCAR_DIR (PAW_PBE: <POTCAR_DIR>/{Li_sv,P,S,Cl,Ag,C}/POTCAR) · optB88 잡이 있으면 VDW_KERNEL (vdw_kernel.bindat 경로)
#   STAGES (기본 "P" = 파일럿 5 잡) — P 밖 단계는 RELEASE_FILE + RELEASE_SHA256 (파일럿 반송 뒤 우리가 보낸다) 이 맞아야만 돈다
#   선택: PERF_TAGS_FILE (한 줄에 대입 하나 · NCORE/NPAR/KPAR/NSIM 양의 정수 · LPLANE/LSCALU/LSCALAPACK .TRUE./.FALSE.) · JOBS (단계 안 일부만)
#         PACK_ONLY=1 (계산 없이 포장만) · WATCH_S (경보 점검 간격 초 · 기본 60)
#   0 스텝 인프라 중단 기록 (전자 반복행 0 · 스케줄러 기록이 있을 때만 · 잡마다 2 회):
#     bash run_all.sh --infra-abort <잡> <단 0|r1A|r1B|r2B|a4A|a4B> <스케줄러 잡 id> <취소 UTC> <사유…>   → 그 시도를 run_aborted/ 로 옮긴다 · 다시 돌리면 같은 단부터
#   전자 스텝 뒤 러너째 끊긴 시도 (스케줄러 시간 제한 · 노드 고장 — attempt.json 없음 · 다시 돌리지 않는다 · 값 없음):
#     WALL_S=<초> bash run_all.sh --killed <잡> <단> <스케줄러 잡 id> <취소 UTC> <사유…>   → 그 시도의 벽시계를 기록한다 (그 전에는 다음 잡이 안 뜬다)
#   ⛔ INCAR·POSCAR·KPOINTS 를 고치지 마세요 · 시도 폴더가 이미 있으면 덮어쓰지 않습니다 (이어 돌리기는 기록을 다시 판정해 다음 단을 정합니다)
#   종료: 0 고른 잡 전부 값 있음 · 1 값 없는 잡 있음 (묶음 만듦 — 실패도 기록) · 2 패키지·환경·인자 오류 (아무것도 안 돎) · 4 포장 실패 (PACK_ONLY=1 로 다시)
#         5 단계·전체 누적 상한 (다음 잡 안 띄움 · 묶음 만듦 · 1저자 결정) · 6 공통 환경 고장 (VASP 빌드 · PP · vdW 커널 — 전체 정지 · 묶음 만듦)
#   보내는 것: 종료 0·1·5·6 뒤 `sha256sum -c round2_return.tgz.sha256` 까지 통과한 쌍. 종료 4 면 PACK_ONLY=1 → 종료 0 + 같은 확인 뒤.
#   지원 환경: Linux · bash ≥ 4 · GNU coreutils (find sort grep cmp sha256sum od stat) · GNU tar · awk (mawk/gawk)
# =============================================================================
set -u
HERE=$(cd "$(dirname "$0")" && pwd); cd "$HERE"
sha256sum -c --quiet MANIFEST.sha256 || { echo "⛔ 패키지 파일이 MANIFEST 와 다르다 — 실행하지 않는다"; exit 2; }
RET_ALLOW='OUTCAR|OSZICAR|INCAR|KPOINTS|POSCAR|IBZKPT|POTCAR\.titel|POTCAR\.sha256|POTCAR\.species\.sha256|attempt\.json|stdout\.log|WAVECAR\.info|warn\.log|infra_abort\.json|LOCPOT\.zavg\.txt|attempt\.start|killed\.json'
RET_FORBID='POTCAR|WAVECAR|CHGCAR|CHG|vasprun\.xml|vdw_kernel\.bindat|LOCPOT'
h(){ sha256sum "$1" 2>/dev/null | cut -d' ' -f1; }
utc(){ date -u +%FT%TZ; }
up(){ awk '{ printf "%d", $1 }' /proc/uptime 2>/dev/null; }    # 부팅 뒤 초 (단조 시계) — 벽시계 장부는 이것으로 잰다 (date 는 시계 맞춤으로 뒤로 갈 수 있다 · 자체 검토 S4)
mkdir -p run
log(){ echo "$*"; echo "$(utc) $*" >> run/env.txt; }
clean(){ printf '%s' "$1" | tr -d '"\\\r\n\t' ; }
cap_num(){ [[ "$1" =~ ^[0-9]+(\.[0-9]+)?$ ]] && awk -v x="$1" 'BEGIN { exit !(x + 0 > 0) }'; }   # 상한 값 = 유한한 양수 (nan · inf · 음수 · 0 거부)
secs_ok(){ [[ "$1" =~ ^(0|[1-9][0-9]{0,8})$ ]]; }    # 손으로 넣는 초 = 10진 정수 · 선행 0 없음 · 9 자리 이하 (bash 산술은 선행 0 을 8진수로 읽는다 — Codex DB P1-3)
incar_val(){ awk -v T="$2" 'BEGIN{T=toupper(T)} { sub(/[#!].*/, ""); n=split($0, st, ";"); for (i=1; i<=n; i++) { s=st[i]; p=index(s, "="); if (!p) continue;
  k=substr(s, 1, p-1); v=substr(s, p+1); gsub(/[ \t]/, "", k); gsub(/^[ \t]+|[ \t]+$/, "", v); if (toupper(k)==T) val=v } } END { if (val!="") print val }' "$1" 2>/dev/null; }

# ── 판정 계약 (검사기 judge_text 와 같다 · 순서까지) → "상태 행수 dE deps 사유" ──
#  ① 행 0 → SCF_UNVERIFIED  ② 스텝 번호 1,2,…,N 아님 · 이온 요약(F=) 뒤 행 → SCF_UNVERIFIED  ③ N > NELM(이 시도의 INCAR) → SCF_UNVERIFIED
#  ④ 확정 모순은 rc 보다 먼저 (CZ Q-CZ-1): OUTCAR 실행 머리줄 ≥ 2 → SCF_UNVERIFIED · OUTCAR 가 끝까지 쓰였는데 머리줄 ≠ 1 또는
#     마지막 전자 반복 번호 k ≠ N → SCF_UNVERIFIED · 안 끝났는데 k > N + 1 (판정 근거 OSZICAR 가 두 스텝 이상 모자람) → SCF_UNVERIFIED
#     (안 끝난 OUTCAR 의 k 없음 · k ≤ N + 1 은 잘림·스텝 도중 충돌 = 결측이라 ⑤ 로 간다)
#  ⑤ rc ≠ 0 · 미종료 → RUN_FAILED  ⑥ 마지막 dE·d eps 가 유한수가 아님 → SCF_UNVERIFIED  ⑦ |dE| ≤ EDIFF 그리고 |d eps| ≤ EDIFF → OK · 아니면 SCF_NOT_CONVERGED
judge(){
  local d=$1 rc term nrun nelm ediff oit
  rc=$(grep -o '"rc": *-\{0,1\}[0-9]*' "$d/attempt.json" 2>/dev/null | head -1 | grep -o -- '-\{0,1\}[0-9]*$'); rc=${rc:-${2:-NA}}
  term=0; grep -aq "General timing and accounting" "$d/OUTCAR" 2>/dev/null && term=1
  nrun=$(grep -acE '^[[:space:]]*vasp\.[0-9]' "$d/OUTCAR" 2>/dev/null); nrun=${nrun:-0}
  nelm=$(incar_val "$d/INCAR" NELM); ediff=$(incar_val "$d/INCAR" EDIFF)
  oit=$(grep -aoE 'Iteration +[0-9]+\( *[0-9]+\)' "$d/OUTCAR" 2>/dev/null | tail -1 | sed -E 's/.*\( *([0-9]+)\)/\1/')
  cat "$d/OSZICAR" 2>/dev/null | awk -v rc="$rc" -v term="$term" -v nrun="$nrun" -v nelm="${nelm:-NA}" -v ediff="${ediff:-NA}" -v oit="${oit:-NA}" '
    function isnum(s) { return s ~ /^[-+]?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][-+]?[0-9]+)?$/ }
    function finite(s,  t) { if (!isnum(s)) return 0; t = sprintf("%g", s + 0); return (t !~ /inf|nan/) }
    /^[ \t]*[0-9]+[ \t]+F=/ { ion = 1; next }
    /^[ \t]*(DAV|RMM|CG|SDA):/ { n++; k = $2; if (bad == "") { if (ion) bad = "rows_after_ion_summary"; else if (k !~ /^[0-9]+$/ || k + 0 != n) bad = "step_numbering" }
                                 de = (NF >= 5) ? $4 : ""; dp = (NF >= 5) ? $5 : ""; next }
    END { o = n + 0
      if (o == 0) { print "SCF_UNVERIFIED 0 NA NA no_rows"; exit }
      if (bad != "") { print "SCF_UNVERIFIED", o, "NA", "NA", bad; exit }
      if (nelm !~ /^[0-9]+$/) { print "SCF_UNVERIFIED", o, "NA", "NA", "nelm_unknown"; exit }
      if (o > nelm + 0) { print "SCF_UNVERIFIED", o, "NA", "NA", "n_gt_nelm"; exit }
      if (nrun + 0 >= 2) { print "SCF_UNVERIFIED", o, "NA", "NA", "run_blocks"; exit }
      if (term == 1) {
        if (nrun + 0 != 1) { print "SCF_UNVERIFIED", o, "NA", "NA", "run_blocks"; exit }
        if (oit != o) { print "SCF_UNVERIFIED", o, "NA", "NA", "outcar_oszicar_mismatch"; exit }
      } else if (oit ~ /^[0-9]+$/ && oit + 0 > o + 1) { print "SCF_UNVERIFIED", o, "NA", "NA", "outcar_oszicar_mismatch"; exit }
      if (rc != "0" || term != 1) { print "RUN_FAILED", o, (de == "" ? "NA" : de), (dp == "" ? "NA" : dp), "rc_or_not_terminated"; exit }
      if (!finite(de) || !finite(dp)) { print "SCF_UNVERIFIED", o, (de == "" ? "NA" : de), (dp == "" ? "NA" : dp), "nonfinite"; exit }
      if (!finite(ediff)) { print "SCF_UNVERIFIED", o, de, dp, "ediff_unknown"; exit }
      a = de + 0; b = dp + 0; if (a < 0) a = -a; if (b < 0) b = -b
      if (a <= ediff + 0 && b <= ediff + 0) print "OK", o, de, dp, "-"; else print "SCF_NOT_CONVERGED", o, de, dp, "-" }'
}

# ── 조기 경보 (120 스텝 뒤 20 스텝마다 · 경보 ≠ 중단) ──
alarms(){ awk 'function isnum(s) { return s ~ /^[-+]?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][-+]?[0-9]+)?$/ }
  function ab(x) { return x < 0 ? -x : x }
  /^[ \t]*(DAV|RMM|CG|SDA):/ { n++; e[n] = $4; p[n] = $5 }
  END { out = ""; if (n == 0) { print "0 -"; exit }
    if (!isnum(e[n]) || !isnum(p[n])) out = out "nonfinite,"
    for (q = 1; q <= 2; q++) { last = (q == 1) ? e[n] : p[n]; stall = (isnum(last) && ab(last + 0) > 1e-4)
      if (n >= 80) { m1 = -1; m2 = -1
        for (i = n - 39; i <= n; i++) { v = (q == 1) ? e[i] : p[i]; if (isnum(v)) { v = ab(v + 0); if (m1 < 0 || v < m1) m1 = v } }
        for (i = n - 79; i <= n - 40; i++) { v = (q == 1) ? e[i] : p[i]; if (isnum(v)) { v = ab(v + 0); if (m2 < 0 || v < m2) m2 = v } }
        if (m1 >= 0 && m2 >= 0 && m1 >= m2) stall = 1 }
      if (stall) out = out ((q == 1) ? "dE_stall," : "deps_stall,") }
    print n, (out == "" ? "-" : out) }' "$1/OSZICAR" 2>/dev/null; }
watch_scf(){
  local d=$1 tag=$2 last=100 o n a
  while [ -f "$d/.running" ]; do
    sleep "${WATCH_S:-60}"
    [ -f "$d/OSZICAR" ] || continue
    o=$(alarms "$d"); n=${o%% *}; a=${o#* }
    case "$n" in ''|*[!0-9]*) continue;; esac
    if [ "$n" -ge 120 ] && [ "$n" -ge $((last + 20)) ]; then
      last=$((n - n % 20))
      if [ "$a" != "-" ]; then echo "$(utc) $tag step $n $a" >> "$d/warn.log"; log "⚠ 경보 $tag 스텝 $n: $a (중단 아님 · NELM 까지 돈다)"; fi
    fi
  done
}

# ── 포장 (허용 목록 · 단계마다 성공 확인 · V5 v6 절차) ──
pack_fail(){ echo "⛔ 포장: $1"; rm -f round2_return.tgz.part round2_return.tgz.sha256.part; return 1; }
pack(){
  local T=round2_return.tmp g hh n_mg n_so n_li f dirs=run
  rm -rf "$T" round2_return.tgz.part round2_return.tgz.sha256.part round2_return.list; mkdir "$T" || return 1
  [ -d run_aborted ] && dirs="run run_aborted"                   # 있는 폴더만 열거한다 — 없는 폴더의 오류를 덮으려다 run/ 열거 실패까지 덮지 않게 (CZ Q-CZ-10 ①)
  find $dirs -mindepth 2 -maxdepth 3 -type f > "$T/found" 2> "$T/find.err"; g=$?
  [ "$g" = 0 ] || { pack_fail "반송 폴더 열거 실패 (find $g: $(head -c 200 "$T/find.err" | tr '\n' ' '))"; return 1; }
  grep -E "^(run|run_aborted)/[^/]+/(stageA/)?($RET_ALLOW)$" "$T/found" > "$T/allowed"; g=$?
  [ "$g" -le 1 ] || { pack_fail "허용 목록 필터 오류 ($g)"; return 1; }
  LC_ALL=C sort "$T/allowed" > "$T/sorted" || { pack_fail "정렬 실패"; return 1; }
  : > "$T/mgmt" || { pack_fail "관리 목록 초기화 실패"; return 1; }
  n_mg=0
  for f in run/env.txt run/status.tsv run/infra_aborts.tsv; do
    [ -f "$f" ] || continue
    n_mg=$((n_mg + 1)); echo "$f" >> "$T/mgmt" || { pack_fail "관리 목록 쓰기 실패 ($f)"; return 1; }
  done
  echo MANIFEST.sha256 > round2_return.list || { pack_fail "목록 쓰기 실패 (MANIFEST.sha256)"; return 1; }
  cat "$T/mgmt" "$T/sorted" >> round2_return.list || { pack_fail "목록 쓰기 실패"; return 1; }
  n_so=$(wc -l < "$T/sorted") && n_li=$(wc -l < round2_return.list) || { pack_fail "목록 검증 준비 실패"; return 1; }
  [ "$n_li" -eq $((1 + n_mg + n_so)) ] || { pack_fail "목록 줄 수가 맞지 않는다 ($n_li ≠ 1+$n_mg+$n_so)"; return 1; }
  grep -qxF MANIFEST.sha256 round2_return.list || { pack_fail "목록에 MANIFEST.sha256 이 없다"; return 1; }
  tar czf round2_return.tgz.part -T round2_return.list || { pack_fail "tar 실패"; return 1; }
  tar tzf round2_return.tgz.part > "$T/members" || { pack_fail "묶음 구성원 열람 실패 — 검사할 수 없으면 보내지 않는다"; return 1; }
  grep -E "(^|/)($RET_FORBID)$" "$T/members" > "$T/forbidden"; g=$?
  if [ "$g" -eq 0 ]; then pack_fail "반송 묶음에 금지 파일이 들어갔다 — 보내지 않는다: $(tr '\n' ' ' < "$T/forbidden")"; return 1
  elif [ "$g" -ne 1 ]; then pack_fail "구성원 검사 오류 ($g)"; return 1; fi
  LC_ALL=C sort "$T/members" > "$T/members.sorted" && LC_ALL=C sort round2_return.list > "$T/list.sorted" || { pack_fail "구성원 대조 준비 실패"; return 1; }
  cmp -s "$T/members.sorted" "$T/list.sorted" || { pack_fail "묶음 구성원이 목록과 다르다 — 보내지 않는다"; return 1; }
  sha256sum round2_return.tgz.part > "$T/sha" || { pack_fail "sha256 계산 실패"; return 1; }
  hh=$(cut -d' ' -f1 < "$T/sha") || { pack_fail "sha256 읽기 실패"; return 1; }
  [[ "$hh" =~ ^[0-9a-fA-F]{64}$ ]] || { pack_fail "sha256 형식 이상 ($hh)"; return 1; }
  printf '%s  round2_return.tgz\n' "$hh" > round2_return.tgz.sha256.part || { pack_fail "sha 쓰기 실패"; return 1; }
  mv -f round2_return.tgz.part round2_return.tgz && mv -f round2_return.tgz.sha256.part round2_return.tgz.sha256 || { pack_fail "승격(mv) 실패 — sha256sum -c 로 확인"; return 1; }
  rm -rf "$T" || echo "⚠ 진단 폴더 정리 실패 — 묶음은 승격됐다"
  return 0
}
finish(){ # $1 종료 코드 — 포장하고 끝낸다 (포장 실패면 4)
  if ! pack; then echo "⛔ 반송 포장 실패 — 계산 결과는 run/ 에 그대로 있다. 다시 돌리지 말고 PACK_ONLY=1 bash run_all.sh 로 포장만"; exit 4; fi
  case "$1" in
    0) echo "✅ 끝 — round2_return.tgz 와 .sha256 을 보내 주세요";;
    1) echo "⚠ 값 없는 잡이 있다 — 그대로 반송해 주세요 (실패도 기록입니다)";;
    5) echo "⏸ 누적 상한 — 다음 잡을 띄우지 않았다. 반송해 주시고 1저자 결정을 기다려 주세요";;
    6) echo "⛔ 공통 환경 고장 — 전체 정지. 반송해 주시고 연락 주세요";;
  esac
  exit "$1"
}

# ── 단계 · 잡 표 ──
declare -A STAGE_OF CAP_H
STAGE_LIST=""
while IFS=$'\t' read -r s c js; do
  [ -n "$s" ] || continue
  if [ "$s" = TOTAL ]; then TOTAL_CAP=$c; continue; fi
  STAGE_LIST="$STAGE_LIST $s"; CAP_H[$s]=$c
  for j in $js; do STAGE_OF[$j]=$s; done
done < STAGES.tsv
ladder_of(){ case "$1" in V5_s_outer_A_G4_e70_far_a4) echo a4;; *) echo carbon;; esac; }
is_optb88(){ grep -qx 'GGA = BO' "jobs/$1/INCAR" 2>/dev/null || grep -qx 'GGA = BO' "jobs/$1/INCAR.a4A" 2>/dev/null; }

# ── 0 스텝 인프라 중단 기록 (CZ Q-CZ-4: OSZICAR 결측 ≠ 0 행 · 다른 출력에 전자 반복 증거가 있으면 거부 · 모르는 벽시계는 UNKNOWN — 0 초가 아니다) ──
if [ "${1:-}" = "--infra-abort" ]; then
  [ $# -ge 6 ] || { echo "⛔ 쓰는 법: WALL_S=<초> bash run_all.sh --infra-abort <잡> <단> <스케줄러 잡 id> <취소 UTC> <사유…>"; exit 2; }
  job=$2; rung=$3; sid=$(clean "$4"); when=$(clean "$5"); shift 5; why=$(clean "$*")
  [ -n "${STAGE_OF[$job]:-}" ] || { echo "⛔ 모르는 잡 $job"; exit 2; }
  case "$rung" in 0) src=run/$job;; r1A) src=run/${job}_r1/stageA;; r1B) src=run/${job}_r1;; r2B) src=run/${job}_r2;; a4A) src=run/${job}_a4/stageA;; a4B) src=run/${job}_a4;;
    *) echo "⛔ 모르는 단 $rung"; exit 2;; esac
  [ -d "$src" ] || { echo "⛔ $src 가 없다"; exit 2; }
  if [ -e "$src/OSZICAR" ]; then
    n=$(grep -acE '^[[:space:]]*(DAV|RMM|CG|SDA):' "$src/OSZICAR" 2>/dev/null); g=$?
    [ "$g" -le 1 ] && [ -n "$n" ] || { echo "⛔ $src/OSZICAR 를 읽지 못했다 (grep $g) — 0 행인지 확인할 수 없어 기록하지 않는다 (1저자)"; exit 2; }
    osz=zero_rows
  else
    n=0; osz=missing
  fi
  [ "$n" = 0 ] || { echo "⛔ 전자 반복행 $n 개 — 0 스텝 중단이 아니다 (실행 실패는 사다리가 다룬다)"; exit 2; }
  so=$(grep -acE '^[[:space:]]*(DAV|RMM|CG|SDA):' "$src/stdout.log" 2>/dev/null); so=${so:-0}
  oi=$(grep -acE 'Iteration +[0-9]+\(' "$src/OUTCAR" 2>/dev/null); oi=${oi:-0}
  [ "$so" = 0 ] && [ "$oi" = 0 ] || { echo "⛔ OSZICAR 는 $osz 인데 stdout.log 전자 반복행 $so · OUTCAR Iteration $oi — 출력 유실이지 0 스텝이 아니다 · 기록하지 않는다"; exit 2; }
  [ -n "$sid" ] && [ -n "$when" ] && [ -n "$why" ] || { echo "⛔ 스케줄러 잡 id · 취소 시각 · 사유가 다 있어야 한다"; exit 2; }
  if [ -n "${WALL_S:-}" ]; then
    secs_ok "$WALL_S" || { echo "⛔ WALL_S '$WALL_S' — 0 이상의 10진 정수 (초 · 선행 0 없이 · 9 자리 이하) 여야 한다"; exit 2; }
    w=$WALL_S
  elif [ -f "$src/attempt.json" ]; then
    w=ATTEMPT_JSON                                                      # 벽시계는 그 시도의 attempt.json (t_start → t_end) 이 이미 안다
  else
    w=UNKNOWN                                                           # 모른다 — 0 이 아니다 (wall_s_of 가 다음 잡을 막는다 · --infra-wall 로 채운다)
  fi
  k=$(awk -F'\t' -v j="$job" '$2 == j' run/infra_aborts.tsv 2>/dev/null | wc -l); k=${k:-0}
  [ "$k" -lt 2 ] || { echo "⛔ $job 0 스텝 중단 기록이 이미 2 회 — 상한 (1저자에게 알린다)"; exit 2; }
  mkdir -p run_aborted; dst=run_aborted/${job}_${rung}_$((k + 1))
  mkdir "$dst" || exit 2
  shopt -s dotglob nullglob
  if [ "$rung" = r1B ] || [ "$rung" = a4B ]; then
    [ -d "$src/.b" ] || { echo "⛔ $src 에 ⓑ 가 시작된 흔적(.b)이 없다"; exit 2; }
    for f in "$src"/*; do [ "$(basename "$f")" = stageA ] && continue; mv "$f" "$dst/" || exit 2; done
  else
    for f in "$src"/*; do mv "$f" "$dst/" || exit 2; done; rmdir "$src" || exit 2
  fi
  shopt -u dotglob nullglob
  rm -f "$dst/POTCAR" "$dst/WAVECAR" "$dst/CHGCAR" "$dst/CHG" "$dst/vasprun.xml" "$dst/vdw_kernel.bindat" "$dst/.running"
  printf '{"job": "%s", "rung": "%s", "sched_job_id": "%s", "cancel_utc": "%s", "reason": "%s", "wall_s": "%s", "oszicar": "%s", "recorded_utc": "%s"}\n' \
    "$job" "$rung" "$sid" "$when" "$why" "$w" "$osz" "$(utc)" > "$dst/infra_abort.json"
  [ -f run/infra_aborts.tsv ] || printf "recorded_utc\tjob\trung\tsched_job_id\tcancel_utc\twall_s\treason\tdir\n" > run/infra_aborts.tsv
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$(utc)" "$job" "$rung" "$sid" "$when" "$w" "$why" "$(basename "$dst")" >> run/infra_aborts.tsv
  if [ "$w" = UNKNOWN ]; then
    echo "✓ $src → $dst (0 스텝 인프라 중단 $((k + 1))/2) — ⚠ 벽시계 미상 (UNKNOWN): 'bash run_all.sh --infra-wall $(basename "$dst") <초>' 로 스케줄러 장부 값을 채울 때까지 다음 잡이 뜨지 않는다"
  else
    echo "✓ $src → $dst (0 스텝 인프라 중단 $((k + 1))/2) — 다시 돌리면 같은 단부터"
  fi
  exit 0
fi

# ── 0 스텝 중단의 벽시계 채우기 (미상일 때만 · 스케줄러 장부 값) ──
if [ "${1:-}" = "--infra-wall" ]; then
  [ $# -eq 3 ] || { echo "⛔ 쓰는 법: bash run_all.sh --infra-wall <run_aborted 폴더 이름> <초>"; exit 2; }
  dd=run_aborted/$(basename "$2"); sec=$3
  [ -f "$dd/infra_abort.json" ] || { echo "⛔ $dd/infra_abort.json 이 없다"; exit 2; }
  secs_ok "$sec" || { echo "⛔ 초 '$sec' — 0 이상의 10진 정수 (선행 0 없이 · 9 자리 이하) 여야 한다"; exit 2; }
  grep -q '"wall_s": "UNKNOWN"' "$dd/infra_abort.json" || { echo "⛔ $dd 의 벽시계는 미상이 아니다 — 고치지 않는다"; exit 2; }
  sed "s/\"wall_s\": \"UNKNOWN\"/\"wall_s\": \"$sec\", \"wall_s_filled_utc\": \"$(utc)\"/" "$dd/infra_abort.json" > "$dd/infra_abort.json.part" \
    && mv -f "$dd/infra_abort.json.part" "$dd/infra_abort.json" || { echo "⛔ infra_abort.json 고치기 실패"; exit 2; }
  if [ -f run/infra_aborts.tsv ]; then
    awk -F'\t' -v OFS='\t' -v d="$(basename "$dd")" -v w="$sec" 'NR > 1 && $8 == d && $6 == "UNKNOWN" { $6 = w } { print }' run/infra_aborts.tsv > run/infra_aborts.tsv.part \
      && mv -f run/infra_aborts.tsv.part run/infra_aborts.tsv || { echo "⛔ infra_aborts.tsv 고치기 실패"; exit 2; }
  fi
  echo "✓ $dd 벽시계 $sec 초 (스케줄러 장부) — 다시 돌리면 누적 상한 장부에 들어간다"; exit 0
fi

# ── 전자 스텝 뒤 끊긴 시도의 벽시계 기록 (스케줄러 시간 제한 · 노드 고장으로 러너째 끊김 — attempt.json 없음 · 0 스텝이 아니다 · 다시 돌리지 않는다 · 값 없음 · 1저자) ──
#    자체 검토 S3: 이 벽시계를 모르는 채로 0 초로 더하면 누적 상한이 새고, 끊긴 시도가 '사다리가 다룬다' 는 약속도 거짓이었다
if [ "${1:-}" = "--killed" ]; then
  [ $# -ge 6 ] || { echo "⛔ 쓰는 법: WALL_S=<초> bash run_all.sh --killed <잡> <단> <스케줄러 잡 id> <취소 UTC> <사유…>"; exit 2; }
  job=$2; rung=$3; sid=$(clean "$4"); when=$(clean "$5"); shift 5; why=$(clean "$*")
  [ -n "${STAGE_OF[$job]:-}" ] || { echo "⛔ 모르는 잡 $job"; exit 2; }
  case "$rung" in 0) src=run/$job;; r1A) src=run/${job}_r1/stageA;; r1B) src=run/${job}_r1;; r2B) src=run/${job}_r2;; a4A) src=run/${job}_a4/stageA;; a4B) src=run/${job}_a4;;
    *) echo "⛔ 모르는 단 $rung"; exit 2;; esac
  [ -f "$src/attempt.start" ] || { echo "⛔ $src 에 시작 표지 (attempt.start) 가 없다 — VASP 가 뜨지 않은 시도다 (기록할 벽시계가 없다)"; exit 2; }
  [ ! -f "$src/attempt.json" ] || { echo "⛔ $src 는 끝난 시도다 (attempt.json 있음) — 기록하지 않는다"; exit 2; }
  [ ! -f "$src/killed.json" ] || { echo "⛔ $src 는 이미 기록했다 — 고치지 않는다"; exit 2; }
  secs_ok "${WALL_S:-}" || { echo "⛔ WALL_S=<초> (스케줄러 장부의 그 시도 벽시계 · 0 이상의 10진 정수 · 선행 0 없이 · 9 자리 이하) 가 있어야 한다"; exit 2; }
  n=$(grep -acE '^[[:space:]]*(DAV|RMM|CG|SDA):' "$src/OSZICAR" 2>/dev/null); so=$(grep -acE '^[[:space:]]*(DAV|RMM|CG|SDA):' "$src/stdout.log" 2>/dev/null)
  oi=$(grep -acE 'Iteration +[0-9]+\(' "$src/OUTCAR" 2>/dev/null)
  [ "${n:-0}" != 0 ] || [ "${so:-0}" != 0 ] || [ "${oi:-0}" != 0 ] || { echo "⛔ $src 에 전자 반복 흔적이 없다 — 0 스텝 중단이면 --infra-abort 로 기록한다 (같은 단을 다시 돈다)"; exit 2; }
  [ -n "$sid" ] && [ -n "$when" ] && [ -n "$why" ] || { echo "⛔ 스케줄러 잡 id · 취소 시각 · 사유가 다 있어야 한다"; exit 2; }
  rid=$(grep -o '"run_id": "[^"]*"' "$src/attempt.start" | head -1 | sed 's/.*: "//; s/"$//')
  printf '{"job": "%s", "rung": "%s", "run_id": "%s", "wall_s": "%s", "sched_job_id": "%s", "cancel_utc": "%s", "reason": "%s", "osz_rows": "%s", "recorded_utc": "%s"}\n' \
    "$job" "$rung" "$rid" "$WALL_S" "$sid" "$when" "$why" "${n:-0}" "$(utc)" > "$src/killed.json.part" && mv -f "$src/killed.json.part" "$src/killed.json" \
    || { echo "⛔ killed.json 쓰기 실패"; exit 2; }
  log "✎ $src 끊긴 시도 벽시계 $WALL_S 초 (스케줄러 $sid · $why) — 값 없음 · 다시 돌리지 않는다"
  echo "✓ $src 벽시계 $WALL_S 초 기록 — 이 시도는 값 없음으로 남는다 (다시 돌리지 않는다 · 1저자). 다시 돌리면 다음 잡부터 이어 간다"; exit 0
fi

if [ "${PACK_ONLY:-0}" = 1 ]; then
  echo "pack_only $(utc)" >> run/env.txt
  if pack; then echo "✅ 포장만 다시 했다 (계산은 다시 돌리지 않았다)"; exit 0; fi
  echo "⛔ 포장 실패 — 디스크·권한을 확인한 뒤 PACK_ONLY=1 로 다시"; exit 4
fi

[[ "$(up)" =~ ^[0-9]+$ ]] || { echo "⛔ /proc/uptime 을 읽을 수 없다 — 벽시계 장부는 단조 시계로 잰다 (Linux)"; exit 2; }

# ── 단계 · 해제 파일 ──
STAGES=${STAGES:-P}
REL_STAGES=" "; REL_TOTAL=""; REL_VER=""; REL_KERNEL=""; RESTART_RE=""; KERNEL_RE=""
declare -A REL_SP
for s in $STAGES; do [ -n "${CAP_H[$s]:-}" ] || { echo "⛔ 모르는 단계 $s"; exit 2; }; done
need_rel=0; for s in $STAGES; do [ "$s" = P ] || need_rel=1; done
if [ "$need_rel" = 1 ]; then
  [ -n "${RELEASE_FILE:-}" ] && [ -f "$RELEASE_FILE" ] && [ -n "${RELEASE_SHA256:-}" ] || { echo "⛔ P 밖 단계는 RELEASE_FILE · RELEASE_SHA256 이 필요하다 (파일럿 반송 뒤 받는다)"; exit 2; }
  [ "$(h "$RELEASE_FILE")" = "$RELEASE_SHA256" ] || { echo "⛔ 해제 파일 sha 가 RELEASE_SHA256 과 다르다"; exit 2; }
  while IFS=$'\t' read -r k a b; do
    case "$k" in
      stages) REL_STAGES=" $a ";;
      cap_h) cap_num "$b" || { echo "⛔ 해제 파일의 단계 $a 상한 '$b' 가 유한한 양수가 아니다"; exit 2; }; CAP_H[$a]=$b;;
      total_cap_h) cap_num "$a" || { echo "⛔ 해제 파일의 전체 상한 '$a' 가 유한한 양수가 아니다"; exit 2; }; REL_TOTAL=$a;;
      vasp_version) REL_VER=$a;;
      species_sha256) REL_SP[$a]=$b;;
      kernel_sha256) REL_KERNEL=$a;;
      restart_read_regex) RESTART_RE=$a;;
      kernel_read_regex) KERNEL_RE=$a;;           # 기록만 (커널 읽기 판정은 검사기)
    esac
  done < "$RELEASE_FILE"
  for s in $STAGES; do [ "$s" = P ] && continue; case "$REL_STAGES" in *" $s "*) ;; *) echo "⛔ 해제 파일이 단계 $s 를 풀지 않았다"; exit 2;; esac; done
  [ -n "$REL_VER" ] && [ -n "$REL_KERNEL" ] && [ "${#REL_SP[@]}" -ge 6 ] || { echo "⛔ 해제 파일에 vasp_version · kernel_sha256 · species_sha256 (6 종) 이 다 있어야 한다"; exit 2; }
  [ -n "$REL_TOTAL" ] && TOTAL_CAP=$REL_TOTAL
fi
SEL=""
for s in $STAGES; do for j in $(awk -F'\t' -v s="$s" '$1 == s {print $3}' STAGES.tsv); do SEL="$SEL $j"; done; done
if [ -n "${JOBS:-}" ]; then
  for j in $JOBS; do case " $SEL " in *" $j "*) ;; *) echo "⛔ $j 는 고른 단계(STAGES=$STAGES)에 없다"; exit 2;; esac; done
  SEL=$JOBS
fi
: "${VASP_CMD:?VASP_CMD 를 주세요 (예: mpirun -np 64 vasp_std)}"
: "${POTCAR_DIR:?POTCAR_DIR 를 주세요 (PAW_PBE 폴더)}"
need_k=0; for j in $SEL; do is_optb88 "$j" && need_k=1; done
if [ "$need_k" = 1 ]; then
  [ -n "${VDW_KERNEL:-}" ] && [ -s "$VDW_KERNEL" ] && [ -r "$VDW_KERNEL" ] || { log "⛔ optB88 잡이 있는데 VDW_KERNEL (vdw_kernel.bindat) 이 없다 — 공통 환경 고장 · 전체 정지"; finish 6; }
  KSHA=$(h "$VDW_KERNEL"); KSIZE=$(stat -c %s "$VDW_KERNEL")
  if [ -n "$REL_KERNEL" ] && [ "$KSHA" != "$REL_KERNEL" ]; then log "⛔ vdW 커널 sha $KSHA ≠ 봉인 $REL_KERNEL — 공통 환경 고장 · 전체 정지"; finish 6; fi
fi
PERF_LINES=""
if [ -n "${PERF_TAGS_FILE:-}" ]; then
  { [ -f "$PERF_TAGS_FILE" ] && [ -r "$PERF_TAGS_FILE" ]; } || { echo "⛔ PERF_TAGS_FILE 을 읽을 수 없다: $PERF_TAGS_FILE"; exit 2; }
  bad=0; seen=" "
  while IFS= read -r ln || [ -n "$ln" ]; do
    t=$(printf '%s' "$ln" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
    case "$t" in ''|'#'*|'!'*) continue;; esac
    case "$t" in *';'*|*'\'*|*'#'*|*'!'*) echo "⛔ 성능 파일: 세미콜론·역슬래시·줄 끝 주석 금지 — $t"; bad=1; continue;; esac
    if printf '%s' "$t" | grep -Eq '^(NCORE|NPAR|KPAR|NSIM)[[:space:]]*=[[:space:]]*[1-9][0-9]*$'; then :
    elif printf '%s' "$t" | grep -Eqi '^(LPLANE|LSCALU|LSCALAPACK)[[:space:]]*=[[:space:]]*\.?(TRUE|FALSE|T|F)\.?$'; then :
    else echo "⛔ 성능 파일: 허용 밖 줄 — $t"; bad=1; continue; fi
    tag=$(printf '%s' "${t%%=*}" | tr -d '[:space:]' | tr '[:lower:]' '[:upper:]')
    case "$seen" in *" $tag "*) echo "⛔ 성능 파일: $tag 중복"; bad=1; continue;; esac
    seen="$seen$tag "; PERF_LINES="$PERF_LINES$t"$'\n'
  done < "$PERF_TAGS_FILE"
  [ "$bad" = 0 ] || exit 2
fi
{ echo "date_utc $(utc)"; echo "host $(hostname 2>/dev/null)"; echo "VASP_CMD $VASP_CMD"; echo "POTCAR_DIR $POTCAR_DIR"; echo "STAGES $STAGES"
  echo "PERF_TAGS $(printf '%s' "$PERF_LINES" | tr '\n' ';')"; echo "MANIFEST_sha256 $(h MANIFEST.sha256)"
  [ "$need_k" = 1 ] && echo "VDW_KERNEL $VDW_KERNEL sha256 $KSHA size $KSIZE"
  [ "$need_rel" = 1 ] && echo "RELEASE $RELEASE_FILE sha256 $RELEASE_SHA256"
  [ -n "$KERNEL_RE" ] && echo "KERNEL_READ_RE $KERNEL_RE"; } >> run/env.txt
[ -f run/status.tsv ] || printf "job\trung\tstage\trc\tstatus\tn_elec\tdE\tdeps\twhy\twall_s\n" > run/status.tsv

# ── 누적 벽시계 (시도 폴더마다 한 번 · 0 스텝 중단 · 끊긴 시도 포함) ──
wall_s_of(){ # $1 단계 (ALL = 전체) → 초 · 미상이 하나라도 있으면 "UNKNOWN <폴더>" (CZ Q-CZ-4 · 자체 검토 S3: 미상을 0 초로 더하지 않는다)
  #   attempt.json (elapsed_s · 단조 시계 — S4) > infra_abort.json (0 스텝 중단 · 스케줄러 장부) > killed.json (전자 스텝 뒤 끊김 · 스케줄러 장부)
  #   > attempt.start 만 (VASP 를 띄웠는데 끝 기록이 없다 = 미상) · 시작 표지가 없는 폴더 (준비 실패) 는 VASP 시간이 없다 · 열거 실패도 미상
  local d f j w s tot=0 unk="" dirs=run lst
  [ -d run_aborted ] && dirs="run run_aborted"
  lst=$(find $dirs \( -name attempt.json -o -name attempt.start -o -name infra_abort.json -o -name killed.json \) -type f 2>/dev/null) || { echo "UNKNOWN (반송 폴더 열거 실패)"; return; }
  for d in $(printf '%s\n' "$lst" | sed 's#/[^/]*$##' | LC_ALL=C sort -u); do
    if [ -f "$d/attempt.json" ]; then f=$d/attempt.json; w=$(grep -o '"elapsed_s": [0-9]*' "$f" | head -1 | sed 's/.*: *//')
    elif [ -f "$d/infra_abort.json" ]; then f=$d/infra_abort.json; w=$(grep -o '"wall_s": "[^"]*"' "$f" | head -1 | sed 's/.*: "//; s/"$//')
    elif [ -f "$d/killed.json" ]; then f=$d/killed.json; w=$(grep -o '"wall_s": "[^"]*"' "$f" | head -1 | sed 's/.*: "//; s/"$//')
    else f=$d/attempt.start; w=""; fi
    j=$(grep -o '"job": "[^"]*"' "$f" | head -1 | sed 's/"job": "//; s/"$//')
    s=${STAGE_OF[$j]:-?}
    if [ "$1" = ALL ] || [ "$1" = "$s" ]; then
      if [[ "$w" =~ ^(0|[1-9][0-9]{0,11})$ ]]; then tot=$((tot + w)); else [ -n "$unk" ] || unk=$d; fi    # 10진 정수 꼴만 (선행 0 = 8진 · 13 자리 이상 = 넘침 → 미상 · DB P1-3)
    fi
  done
  if [ -n "$unk" ]; then echo "UNKNOWN $unk"; else echo "$tot"; fi
}
cap_ok(){ # $1 잡 → 0 이면 띄워도 된다 (단계 · 전체 상한 · 벽시계 미상이면 안 띄운다)
  local s=${STAGE_OF[$1]} ws wt
  ws=$(wall_s_of "$s") || ws="UNKNOWN (장부 계산 실패)"; wt=$(wall_s_of ALL) || wt="UNKNOWN (장부 계산 실패)"
  case "$ws $wt" in *UNKNOWN*)
    log "⏸ 벽시계 미상 — $(printf '%s\n%s\n' "$ws" "$wt" | grep -m1 UNKNOWN | cut -d' ' -f2-) · $1 을 띄우지 않는다. 0 스텝 중단 (run_aborted) 이면 'bash run_all.sh --infra-wall <run_aborted 폴더 이름> <초>' ·"\
" 전자 스텝 뒤 끊긴 시도 (attempt.start 만) 면 'WALL_S=<초> bash run_all.sh --killed <잡> <단> <스케줄러 잡 id> <취소 UTC> <사유>' 로 스케줄러 장부 값을 채운 뒤 다시"\
" (실행 기록이 손상됐으면 반송하고 연락)"; return 1;;
  esac
  [[ "$ws" =~ ^[0-9]+$ && "$wt" =~ ^[0-9]+$ ]] || { log "⏸ 벽시계 장부가 숫자가 아니다 (단계 '$ws' · 전체 '$wt') — $1 을 띄우지 않는다 (반송하고 연락)"; return 1; }   # 합산 실패 · 빈 값 (DB P1-3)
  awk -v w="$ws" -v c="${CAP_H[$s]}" 'BEGIN { exit !(w <= c * 3600) }' || { log "⏸ 단계 $s 누적 $((ws / 3600)) h > 상한 ${CAP_H[$s]} h — $1 을 띄우지 않는다"; return 1; }
  awk -v w="$wt" -v c="$TOTAL_CAP" 'BEGIN { exit !(w <= c * 3600) }' || { log "⏸ 전체 누적 $((wt / 3600)) h > 상한 $TOTAL_CAP h — $1 을 띄우지 않는다"; return 1; }
  return 0
}
pp_ok(){ # $1 잡 — 해제 뒤에는 PP 종별 sha 가 봉인과 같아야 한다
  local p
  [ "$need_rel" = 1 ] || return 0
  while read -r p; do [ -n "$p" ] || continue
    [ "$(h "$POTCAR_DIR/$p/POTCAR")" = "${REL_SP[$p]:-x}" ] || { log "⛔ POTCAR $p sha 가 봉인과 다르다 — 공통 환경 고장 · 전체 정지"; return 1; }
  done < "jobs/$1/POTCAR.spec"
}
ver_of(){ grep -am1 -E '^[[:space:]]*vasp\.[0-9]' "$1/OUTCAR" 2>/dev/null | tr -s '[:space:]' ' ' | sed 's/^ //; s/ $//'; }

# ── WAVECAR 머리 (VASP 5.x: 첫 레코드 RECL·NSPIN·RTAG · 둘째 레코드 NKPTS·NBANDS·ENCUT) ──
wav_head(){ local f=$1 r
  r=$(od -A n -t f8 -N 24 "$f" 2>/dev/null | awk '{ for (i = 1; i <= NF; i++) printf "%.0f ", $i }'); set -- $r
  [ $# -eq 3 ] && [ "$1" -gt 0 ] 2>/dev/null || { echo "NA NA NA NA NA NA"; return; }
  echo "$1 $2 $3 $(od -A n -t f8 -j "$1" -N 24 "$f" 2>/dev/null | awk '{ for (i = 1; i <= NF; i++) printf "%s ", ($i == int($i) ? sprintf("%.0f", $i) : sprintf("%.4f", $i)) }')"
}
out_num(){ if [ "$2" = ENCUT ]; then grep -aoE "ENCUT *= *[0-9.]+ eV" "$1/OUTCAR" 2>/dev/null | tail -1 | grep -oE '[0-9.]+ eV$' | grep -oE '^[0-9.]+';
  else grep -aoE "$2 *= *[0-9.]+" "$1/OUTCAR" 2>/dev/null | tail -1 | grep -oE '[0-9.]+$'; fi; }

# ── LOCPOT xy 면평균 (LVHAR 잡 · 정보 · 판정 아님) — 머리 구조 · 격자 개수 · 유한수를 확인하고 어긋나면 만들지 않는다 ──
locpot_zavg(){ # $1 시도 폴더 · $2 run_id → $1/LOCPOT.zavg.txt (z Å · 면평균 eV) · 0 만듦 · 1 안 만듦 (경고만 — 계산 판정과 무관)
  local d=$1 sh
  sh=$(h "$d/LOCPOT")
  awk -v sha="$sh" -v rid="$2" '
    function isnum(s) { return s ~ /^[-+]?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][-+]?[0-9]+)?$/ }
    function finite(s,  t) { if (!isnum(s)) return 0; t = sprintf("%g", s + 0); return (t !~ /inf|nan/) }
    function die(m) { print "LOCPOT 면평균 안 만듦: " m; bad = 1; exit 1 }
    NR == 2 { if (!finite($1)) die("배율 줄"); sc = $1 + 0 }
    NR == 5 { if (NF < 3 || !finite($3)) die("c 벡터 줄"); cz = $3 * sc }
    NR == 6 { if ($1 ~ /^[0-9]/) die("6 째 줄이 원소 이름이 아니다 (VASP 5 꼴만 읽는다)") }
    NR == 7 { for (i = 1; i <= NF; i++) { if ($i !~ /^[0-9]+$/) die("원자 수 줄"); nat += $i } }
    NR == 8 { c0 = ($1 ~ /^[Ss]/) ? 10 : 9 }
    NR > 8 && NR >= c0 && NR < c0 + nat { next }
    NR > 8 && NR >= c0 + nat && !ng {
      if (NF == 0) next
      if (NF != 3 || $1 !~ /^[1-9][0-9]*$/ || $2 !~ /^[1-9][0-9]*$/ || $3 !~ /^[1-9][0-9]*$/) die("격자 줄 (" $0 ")")
      nx = $1 + 0; ny = $2 + 0; nz = $3 + 0; ng = nx * ny * nz; next }
    ng && cnt < ng { for (i = 1; i <= NF; i++) { if (cnt >= ng) die("격자 " ng " 개보다 값이 많다"); if (!finite($i)) die("비유한 값 " $i); s[int(cnt / (nx * ny))] += $i; cnt++ }; next }
    ng && NF > 0 { die("격자 " ng " 개보다 값이 많다") }
    END { if (bad) exit 1
          if (!ng) die("격자 줄 없음")
          if (cnt != ng) die("값 " cnt " 개 ≠ 격자 " nx "×" ny "×" nz " = " ng)
          printf "# LOCPOT xy-plane average (LVHAR) · grid %d %d %d · LOCPOT sha256 %s · run_id %s · c_z_A %.6f\n", nx, ny, nz, sha, rid, cz
          print "# z_A V_eV"
          for (k = 0; k < nz; k++) printf "%.6f %.8f\n", k * cz / nz, s[k] / (nx * ny) }' "$d/LOCPOT" > "$d/LOCPOT.zavg.part"
  if [ $? = 0 ]; then mv -f "$d/LOCPOT.zavg.part" "$d/LOCPOT.zavg.txt"; return 0; fi
  log "⚠ $(head -1 "$d/LOCPOT.zavg.part" 2>/dev/null) — $d (정보 항목 · 계산 판정과 무관)"; rm -f "$d/LOCPOT.zavg.part"; return 1
}

# ── 한 시도 ──
run_one(){ # $1 잡 · $2 단 · $3 시도 폴더 · $4 INCAR 이름 · $5 WAVECAR 원본 (B 단만) → 0 돌림 · 3 준비 실패 · 6 공통 환경 고장
  #   A·단 0·r2 는 폴더를 mkdir 로 차지한다 · r1B·a4B 는 ⓐ 가 든 시도 폴더 안에서 `.b` 를 mkdir 로 차지한다 (둘 다 원자적 · 덮어쓰지 않는다)
  local job=$1 rung=$2 d=$3 inc=$4 wsrc=${5:-} rid t0 t1 u0 u1 el rc j wsha="" wcp="" wend hd istart icharg nr pr hon ksha="" ver
  pp_ok "$job" || return 6        # 모든 VASP 실행 직전 · 폴더를 차지하기 전 (이어 돌린 ⓑ 포함 — CZ Q-CZ-3)
  case "$rung" in
    r1B|a4B) mkdir "$d/.b" 2>/dev/null || { echo "⛔ $d/.b 가 이미 있다 — ⓑ 를 덮어쓰지 않는다"; return 3; };;
    *) mkdir "$d" 2>/dev/null || { echo "⛔ $d 가 이미 있거나 만들 수 없다 — 덮어쓰지 않는다"; return 3; };;
  esac
  { cp "jobs/$job/POSCAR" "jobs/$job/KPOINTS" "$d/" && cp "jobs/$job/$inc" "$d/INCAR"; } || return 3
  [ -n "$PERF_LINES" ] && printf '%s' "$PERF_LINES" >> "$d/INCAR"
  : > "$d/POTCAR"; : > "$d/POTCAR.species.sha256"
  while read -r p; do
    [ -n "$p" ] || continue
    [ -f "$POTCAR_DIR/$p/POTCAR" ] || { echo "⛔ POTCAR $p 없음"; rm -f "$d/POTCAR"; return 3; }
    cat "$POTCAR_DIR/$p/POTCAR" >> "$d/POTCAR"; printf "%s %s\n" "$p" "$(h "$POTCAR_DIR/$p/POTCAR")" >> "$d/POTCAR.species.sha256"
  done < "jobs/$job/POTCAR.spec"
  grep -aE "TITEL|ZVAL|VRHFIN|LEXCH" "$d/POTCAR" > "$d/POTCAR.titel"; h "$d/POTCAR" > "$d/POTCAR.sha256"
  if grep -qx 'GGA = BO' "$d/INCAR"; then
    cp "$VDW_KERNEL" "$d/vdw_kernel.bindat" || return 6
    ksha=$(h "$d/vdw_kernel.bindat"); [ "$ksha" = "$KSHA" ] || { log "⛔ 복사한 vdW 커널 sha 불일치 — 공통 환경 고장"; return 6; }
  fi
  if [ -n "$wsrc" ]; then
    cp "$wsrc" "$d/WAVECAR" || return 3
    wsha=$(h "$wsrc"); wcp=$(h "$d/WAVECAR")
  fi
  rid="$(date -u +%Y%m%dT%H%M%S)-$$-$RANDOM"; t0=$(date +%s); u0=$(up)
  # 시작 표지 — VASP 를 띄웠다는 기록 (끝 기록 attempt.json 없이 끊기면 장부가 미상으로 본다 · 자체 검토 S3)
  printf '{"job": "%s", "attempt": "%s", "stage": "%s", "run_id": "%s", "t_start": %d, "kernel_sha256": "%s"}\n' "$job" "$rung" "${STAGE_OF[$job]}" "$rid" "$t0" "$ksha" \
    > "$d/attempt.start" || return 3
  touch "$d/.running"; watch_scf "$d" "$job/$rung" & local wpid=$!
  (cd "$d" && $VASP_CMD > stdout.log 2>&1); rc=$?; t1=$(date +%s); u1=$(up)
  el=$((u1 - u0)); [ "$el" -ge 0 ] 2>/dev/null || el=$(( t1 > t0 ? t1 - t0 : 0 ))      # 경과 = 단조 시계 (S4) · 못 읽으면 벽시계 차 (음수면 0)
  rm -f "$d/.running"; kill "$wpid" 2>/dev/null; wait "$wpid" 2>/dev/null
  ver=$(clean "$(ver_of "$d")")
  case "$rung" in
    r1A|a4A)
      hd=$(wav_head "$d/WAVECAR")
      printf '{"sha256": "%s", "size": %s, "head": "%s", "outcar": {"NKPTS": "%s", "NBANDS": "%s", "ENCUT": "%s"}}\n' "$(h "$d/WAVECAR")" "$(stat -c %s "$d/WAVECAR" 2>/dev/null || echo 0)" \
        "$hd" "$(out_num "$d" NKPTS)" "$(out_num "$d" NBANDS)" "$(out_num "$d" ENCUT)" > "$d/WAVECAR.info";;
    r1B|r2B|a4B)
      wend=$(h "$d/WAVECAR")
      # Startparameter 줄만 ('ISTART = n  job :' · 'ICHARG = n  charge:') — INCAR 를 되울리는 빌드에서 입력값을 실제값으로 읽지 않게 (마지막 줄)
      istart=$(grep -aE '^[[:space:]]*ISTART *= *[0-9]+[[:space:]]+job' "$d/OUTCAR" 2>/dev/null | tail -1 | grep -oE 'ISTART *= *[0-9]+' | grep -oE '[0-9]+$')
      icharg=$(grep -aE '^[[:space:]]*ICHARG *= *[0-9]+[[:space:]]+charge' "$d/OUTCAR" 2>/dev/null | tail -1 | grep -oE 'ICHARG *= *[0-9]+' | grep -oE '[0-9]+$')
      nr=0; grep -aq "WAVECAR not read" "$d/stdout.log" "$d/OUTCAR" 2>/dev/null && nr=1
      pr=NA; if [ -n "$RESTART_RE" ]; then pr=0; grep -aqE -e "$RESTART_RE" "$d/stdout.log" "$d/OUTCAR" 2>/dev/null && pr=1; fi
      hon=0; [ "$istart" = 1 ] && [ "$icharg" = 0 ] && [ "$nr" = 0 ] && [ "$pr" != 0 ] && [ -n "$wsha" ] && [ "$wsha" = "$wcp" ] && [ "$wcp" = "$wend" ] && hon=1
      printf '{"src_sha256": "%s", "copied_sha256": "%s", "end_sha256": "%s", "istart": "%s", "icharg": "%s", "not_read_phrase": %s, "positive_regex_match": "%s", "honoured": %s}\n' \
        "$wsha" "$wcp" "$wend" "${istart:-NA}" "${icharg:-NA}" "$nr" "$pr" "$hon" > "$d/WAVECAR.info";;
  esac
  [ -f "$d/LOCPOT" ] && locpot_zavg "$d" "$rid"
  printf '{"job": "%s", "attempt": "%s", "stage": "%s", "run_id": "%s", "rc": %d, "t_start": %d, "t_end": %d, "elapsed_s": %d, "vasp_version": "%s", "kernel_sha256": "%s", "perf": "%s", "sha256": {"INCAR": "%s", "POSCAR": "%s", "KPOINTS": "%s", "POTCAR": "%s", "OUTCAR": "%s", "OSZICAR": "%s", "WAVECAR.info": "%s", "LOCPOT.zavg.txt": "%s", "stdout.log": "%s", "POTCAR.titel": "%s", "POTCAR.species.sha256": "%s", "attempt.start": "%s"}}\n' \
    "$job" "$rung" "${STAGE_OF[$job]}" "$rid" "$rc" "$t0" "$t1" "$el" "$ver" "$ksha" "$(printf '%s' "$PERF_LINES" | tr '\n' ';')" \
    "$(h "$d/INCAR")" "$(h "$d/POSCAR")" "$(h "$d/KPOINTS")" "$(cat "$d/POTCAR.sha256")" "$(h "$d/OUTCAR")" "$(h "$d/OSZICAR")" "$(h "$d/WAVECAR.info")" \
    "$(h "$d/LOCPOT.zavg.txt")" "$(h "$d/stdout.log")" "$(h "$d/POTCAR.titel")" "$(h "$d/POTCAR.species.sha256")" "$(h "$d/attempt.start")" > "$d/attempt.json"
  j=$(judge "$d"); set -- $j
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$job" "$rung" "${STAGE_OF[$job]}" "$rc" "$1" "$2" "$3" "$4" "$5" "$el" >> run/status.tsv
  rm -f "$d/POTCAR" "$d/CHGCAR" "$d/CHG" "$d/vasprun.xml" "$d/vdw_kernel.bindat" "$d/LOCPOT"
  case "$rung" in r1A|a4A) ;; *) rm -f "$d/WAVECAR";; esac      # ⓐ WAVECAR 는 그 잡 사다리가 끝날 때까지 둔다 (반송 안 함 · sha·크기·머리만)
  if [ "$need_rel" = 1 ] && [ -n "$ver" ] && [ "$ver" != "$REL_VER" ]; then log "⛔ $job/$rung VASP 빌드 '$ver' ≠ 봉인 — 공통 환경 고장 · 전체 정지"; return 6; fi
  return 0
}
wsha(){ grep -o "\"$2\": \"[0-9a-f]*\"" "$1" 2>/dev/null | head -1 | grep -o '[0-9a-f]\{64\}'; }   # WAVECAR.info 의 sha 필드 하나 ($1 파일 · $2 키)
stat_of(){ # 시도 폴더 · 단 → 상태 (B 단은 재시작 확인을 먼저 · 기록 없으면 INCOMPLETE_ATTEMPT)
  #   재시작 확인 = 검사기와 같다: 기록 honoured · ⓑ src = copied = end = 그 ⓐ 의 기록 sha (r1B·a4B ← 같은 폴더 stageA · r2B ← r1 의 stageA)
  #   · 해제 파일에 재시작 regex 가 있으면 원문 (stdout.log · OUTCAR) 을 다시 본다 — 이어 돌리기 · 손댄 기록에서도 검사기와 같은 답
  local d=$1 j a s
  [ -f "$d/attempt.json" ] || { echo INCOMPLETE_ATTEMPT; return; }
  case "$2" in r1B|r2B|a4B)
    case "$2" in r2B) a=${d%_r2}_r1/stageA;; *) a=$d/stageA;; esac
    s=$(wsha "$a/WAVECAR.info" sha256)
    { grep -q '"honoured": 1' "$d/WAVECAR.info" 2>/dev/null && [ -n "$s" ] && [ "$(wsha "$d/WAVECAR.info" src_sha256)" = "$s" ] \
      && [ "$(wsha "$d/WAVECAR.info" copied_sha256)" = "$s" ] && [ "$(wsha "$d/WAVECAR.info" end_sha256)" = "$s" ] \
      && { [ -z "$RESTART_RE" ] || grep -aqE -e "$RESTART_RE" "$d/stdout.log" "$d/OUTCAR" 2>/dev/null; }; } || { echo RESTART_NOT_HONOURED; return; };;
  esac
  j=$(judge "$d"); echo "${j%% *}"
}
elig_A(){ # ⓐ 자격 (ⓑ 를 띄우기 전 — ① 정상 종료·유한 상태 ② 유효 WAVECAR: 머리 = ⓐ OUTCAR 원문 NKPTS·NBANDS·ENCUT · WAVECAR.info 의 OUTCAR 사본 = 원문
  #         (검사기 a_eligible 과 같다) ③ 기록 sha = 지금 WAVECAR · 복사본 sha 는 run_one 이 ⓑ 기록에 남기고 재시작 확인이 본다)
  local d=$1 s r c k
  s=$(stat_of "$d" A)
  case "$s" in OK|SCF_NOT_CONVERGED) ;; *) echo "ⓐ 상태 $s (정상 종료·유한 상태 아님)"; return 1;; esac
  [ -s "$d/WAVECAR" ] || { echo "ⓐ WAVECAR 없음·빈 파일"; return 1; }
  for k in NKPTS NBANDS ENCUT; do
    c=$(grep -o "\"$k\": \"[^\"]*\"" "$d/WAVECAR.info" 2>/dev/null | head -1 | sed 's/.*: "//; s/"$//')
    [ -n "$c" ] && [ "$c" = "$(out_num "$d" "$k")" ] || { echo "ⓐ WAVECAR.info 의 OUTCAR 사본 $k '$c' ≠ ⓐ OUTCAR 원문 '$(out_num "$d" "$k")'"; return 1; }
  done
  r=$(awk '{ if (match($0, /"head": "[^"]*"/)) print substr($0, RSTART + 9, RLENGTH - 10) }' "$d/WAVECAR.info"); set -- $r
  [ $# -ge 6 ] && [ "$4" = "$(out_num "$d" NKPTS)" ] && [ "$5" = "$(out_num "$d" NBANDS)" ] && \
    awk -v a="$6" -v b="$(out_num "$d" ENCUT)" 'BEGIN { exit !(b != "" && (a - b < 0.05) && (b - a < 0.05)) }' || { echo "ⓐ WAVECAR 머리 ($r) ≠ OUTCAR NKPTS/NBANDS/ENCUT"; return 1; }
  [ "$(h "$d/WAVECAR")" = "$(wsha "$d/WAVECAR.info" sha256)" ] || { echo "ⓐ WAVECAR 가 기록 뒤 바뀌었다"; return 1; }
  return 0
}
two_stage(){ # $1 잡 · $2 시도 폴더 · $3 ⓐ 단 · $4 ⓑ 단 → FINAL · 반환 0 OK · 1 값 없음/다음 단 후보 · 6 공통 환경 고장
  local job=$1 d=$2 ra=$3 rb=$4 r why
  if [ ! -d "$d/stageA" ]; then run_one "$job" "$ra" "$d/stageA" "INCAR.$ra"; r=$?; [ "$r" = 6 ] && return 6; [ "$r" = 0 ] || { FINAL=PREP_FAILED; return 1; }; fi
  [ -f "$d/stageA/attempt.json" ] || { FINAL=INCOMPLETE_ATTEMPT; return 1; }
  if [ ! -d "$d/.b" ]; then
    why=$(elig_A "$d/stageA") || { FINAL=STAGE_A_INELIGIBLE; log "$job $rb: ⓐ 자격 미달 — $why · ⓑ 를 띄우지 않는다"; return 1; }
    run_one "$job" "$rb" "$d" "INCAR.$rb" "$d/stageA/WAVECAR"; r=$?; [ "$r" = 6 ] && return 6; [ "$r" = 0 ] || { FINAL=PREP_FAILED; return 1; }
  fi
  FINAL=$(stat_of "$d" "$rb")
  [ "$FINAL" = OK ]
}

# ── 사다리 ──
FINAL=""
drop_wav(){ # $1 ⓐ 폴더 — ⓐ WAVECAR 는 그 잡이 **끝난** 상태에서만 지운다. 0 스텝 중단 기록 뒤 이어 돌리기 · 1저자 검토 (재시작 미이행 → 다음 단) 가
  #           ⓐ 를 다시 계산하지 않고 쓸 수 있게 미확인·재시작 미이행·기록 없음·준비 실패에서는 남긴다 (반송은 안 한다)
  case "$FINAL" in INCOMPLETE_ATTEMPT|RESTART_NOT_HONOURED|SCF_UNVERIFIED|PREP_FAILED) log "… $1/WAVECAR 를 남긴다 ($FINAL — 검토·이어 돌리기용)";; *) rm -f "$1/WAVECAR";; esac
}
ladder(){ # $1 잡 → FINAL = 마지막 상태 · 반환 0 값 있음 · 1 값 없음 · 5 상한 · 6 공통 환경 고장
  local job=$1 s r
  if [ "$(ladder_of "$job")" = a4 ]; then
    if [ ! -d "run/${job}_a4" ]; then cap_ok "$job" || return 5; pp_ok "$job" || return 6; mkdir "run/${job}_a4" || { FINAL=PREP_FAILED; return 1; }; fi
    two_stage "$job" "run/${job}_a4" a4A a4B; r=$?; [ "$r" = 6 ] && return 6      # a4 는 한 번 (사다리 아님)
    drop_wav "run/${job}_a4/stageA"; return "$r"
  fi
  if [ ! -d "run/$job" ]; then cap_ok "$job" || return 5; pp_ok "$job" || return 6; run_one "$job" 0 "run/$job" INCAR; r=$?; [ "$r" = 6 ] && return 6; [ "$r" = 0 ] || { FINAL=PREP_FAILED; return 1; }; fi
  s=$(stat_of "run/$job" 0)
  case "$s" in OK) FINAL=OK; return 0;; SCF_NOT_CONVERGED|RUN_FAILED) ;; *) FINAL=$s; return 1;; esac
  if [ ! -d "run/${job}_r1" ]; then pp_ok "$job" || return 6; mkdir "run/${job}_r1" || { FINAL=PREP_FAILED; return 1; }; fi
  two_stage "$job" "run/${job}_r1" r1A r1B; r=$?
  [ "$r" = 6 ] && return 6
  if [ "$r" = 0 ]; then drop_wav "run/${job}_r1/stageA"; return 0; fi
  case "$FINAL" in SCF_NOT_CONVERGED|RUN_FAILED) ;; *) drop_wav "run/${job}_r1/stageA"; return 1;; esac      # 미확인·자격 미달·재시작 미이행 = 자동 승격 없음
  if [ ! -d "run/${job}_r2" ]; then
    pp_ok "$job" || return 6
    [ -s "run/${job}_r1/stageA/WAVECAR" ] && elig_A "run/${job}_r1/stageA" > /dev/null || { FINAL=STAGE_A_INELIGIBLE; log "$job r2: r1 의 자격 있는 ⓐ WAVECAR 가 없다 — r2 를 띄우지 않는다"; return 1; }
    run_one "$job" r2B "run/${job}_r2" INCAR.r2B "run/${job}_r1/stageA/WAVECAR"; r=$?; [ "$r" = 6 ] && return 6; [ "$r" = 0 ] || { FINAL=PREP_FAILED; return 1; }
  fi
  FINAL=$(stat_of "run/${job}_r2" r2B); drop_wav "run/${job}_r1/stageA"
  [ "$FINAL" = OK ] && return 0 || return 1
}

rc_all=0
log "════ W_ad round2 · 단계 $STAGES · 잡 $(echo $SEL | wc -w) ════"
for job in $SEL; do
  [ -d "jobs/$job" ] || { echo "⛔ 모르는 잡 $job"; exit 2; }
  ladder "$job"; r=$?
  case "$r" in
    0) log "✓ $job ($FINAL)";;
    1) log "✗ $job 값 없음 ($FINAL)"; rc_all=1;;
    5) finish 5;;
    6) finish 6;;
  esac
done
finish "$rc_all"
