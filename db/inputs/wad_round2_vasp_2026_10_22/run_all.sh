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
#   ⛔ INCAR·POSCAR·KPOINTS 를 고치지 마세요 · 시도 폴더가 이미 있으면 덮어쓰지 않습니다 (이어 돌리기는 기록을 다시 판정해 다음 단을 정합니다)
#   종료: 0 고른 잡 전부 값 있음 · 1 값 없는 잡 있음 (묶음 만듦 — 실패도 기록) · 2 패키지·환경·인자 오류 (아무것도 안 돎) · 4 포장 실패 (PACK_ONLY=1 로 다시)
#         5 단계·전체 누적 상한 (다음 잡 안 띄움 · 묶음 만듦 · 1저자 결정) · 6 공통 환경 고장 (VASP 빌드 · PP · vdW 커널 — 전체 정지 · 묶음 만듦)
#   보내는 것: 종료 0·1·5·6 뒤 `sha256sum -c round2_return.tgz.sha256` 까지 통과한 쌍. 종료 4 면 PACK_ONLY=1 → 종료 0 + 같은 확인 뒤.
#   지원 환경: Linux · bash ≥ 4 · GNU coreutils (find sort grep cmp sha256sum od stat) · GNU tar · awk (mawk/gawk)
# =============================================================================
set -u
HERE=$(cd "$(dirname "$0")" && pwd); cd "$HERE"
sha256sum -c --quiet MANIFEST.sha256 || { echo "⛔ 패키지 파일이 MANIFEST 와 다르다 — 실행하지 않는다"; exit 2; }
RET_ALLOW='OUTCAR|OSZICAR|INCAR|KPOINTS|POSCAR|IBZKPT|POTCAR\.titel|POTCAR\.sha256|POTCAR\.species\.sha256|attempt\.json|stdout\.log|WAVECAR\.info|warn\.log|infra_abort\.json'
RET_FORBID='POTCAR|WAVECAR|CHGCAR|CHG|vasprun\.xml|vdw_kernel\.bindat'
h(){ sha256sum "$1" 2>/dev/null | cut -d' ' -f1; }
utc(){ date -u +%FT%TZ; }
mkdir -p run
log(){ echo "$*"; echo "$(utc) $*" >> run/env.txt; }
clean(){ printf '%s' "$1" | tr -d '"\\\r\n\t' ; }
incar_val(){ awk -v T="$2" 'BEGIN{T=toupper(T)} { sub(/[#!].*/, ""); n=split($0, st, ";"); for (i=1; i<=n; i++) { s=st[i]; p=index(s, "="); if (!p) continue;
  k=substr(s, 1, p-1); v=substr(s, p+1); gsub(/[ \t]/, "", k); gsub(/^[ \t]+|[ \t]+$/, "", v); if (toupper(k)==T) val=v } } END { if (val!="") print val }' "$1" 2>/dev/null; }

# ── 판정 계약 (검사기 judge_attempt 와 같다 · 순서까지) → "상태 행수 dE deps 사유" ──
#  ① 행 0 → SCF_UNVERIFIED  ② 스텝 번호 1,2,…,N 아님 · 이온 요약(F=) 뒤 행 → SCF_UNVERIFIED  ③ N > NELM(이 시도의 INCAR) → SCF_UNVERIFIED
#  ④ rc ≠ 0 · 미종료 → RUN_FAILED  ⑤ OUTCAR 실행 머리줄 ≠ 1 → SCF_UNVERIFIED  ⑥ OUTCAR 마지막 전자 반복 번호 ≠ N → SCF_UNVERIFIED
#  ⑦ 마지막 dE·d eps 가 유한수가 아님 → SCF_UNVERIFIED  ⑧ |dE| ≤ EDIFF 그리고 |d eps| ≤ EDIFF → OK · 아니면 SCF_NOT_CONVERGED
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
      if (rc != "0" || term != 1) { print "RUN_FAILED", o, (de == "" ? "NA" : de), (dp == "" ? "NA" : dp), "rc_or_not_terminated"; exit }
      if (nrun != 1) { print "SCF_UNVERIFIED", o, "NA", "NA", "run_blocks"; exit }
      if (oit != o) { print "SCF_UNVERIFIED", o, "NA", "NA", "outcar_oszicar_mismatch"; exit }
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
  local T=round2_return.tmp g hh n_mg n_so n_li f
  rm -rf "$T" round2_return.tgz.part round2_return.tgz.sha256.part round2_return.list; mkdir "$T" || return 1
  find run run_aborted -mindepth 2 -maxdepth 3 -type f > "$T/found" 2> /dev/null; g=$?
  [ -d run_aborted ] || g=0
  [ "$g" = 0 ] || { pack_fail "run/ 열거 실패"; return 1; }
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

# ── 0 스텝 인프라 중단 기록 ──
if [ "${1:-}" = "--infra-abort" ]; then
  [ $# -ge 6 ] || { echo "⛔ 쓰는 법: --infra-abort <잡> <단> <스케줄러 잡 id> <취소 UTC> <사유…>"; exit 2; }
  job=$2; rung=$3; sid=$(clean "$4"); when=$(clean "$5"); shift 5; why=$(clean "$*")
  [ -n "${STAGE_OF[$job]:-}" ] || { echo "⛔ 모르는 잡 $job"; exit 2; }
  case "$rung" in 0) src=run/$job;; r1A) src=run/${job}_r1/stageA;; r1B) src=run/${job}_r1;; r2B) src=run/${job}_r2;; a4A) src=run/${job}_a4/stageA;; a4B) src=run/${job}_a4;;
    *) echo "⛔ 모르는 단 $rung"; exit 2;; esac
  [ -d "$src" ] || { echo "⛔ $src 가 없다"; exit 2; }
  n=$(grep -acE '^[[:space:]]*(DAV|RMM|CG|SDA):' "$src/OSZICAR" 2>/dev/null); n=${n:-0}
  [ "$n" = 0 ] || { echo "⛔ 전자 반복행 $n 개 — 0 스텝 중단이 아니다 (실행 실패는 사다리가 다룬다)"; exit 2; }
  [ -n "$sid" ] && [ -n "$when" ] && [ -n "$why" ] || { echo "⛔ 스케줄러 잡 id · 취소 시각 · 사유가 다 있어야 한다"; exit 2; }
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
  w=${WALL_S:-NA}
  printf '{"job": "%s", "rung": "%s", "sched_job_id": "%s", "cancel_utc": "%s", "reason": "%s", "wall_s": "%s", "recorded_utc": "%s"}\n' \
    "$job" "$rung" "$sid" "$when" "$why" "$w" "$(utc)" > "$dst/infra_abort.json"
  [ -f run/infra_aborts.tsv ] || printf "recorded_utc\tjob\trung\tsched_job_id\tcancel_utc\twall_s\treason\n" > run/infra_aborts.tsv
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$(utc)" "$job" "$rung" "$sid" "$when" "$w" "$why" >> run/infra_aborts.tsv
  echo "✓ $src → $dst (0 스텝 인프라 중단 $((k + 1))/2) — 다시 돌리면 같은 단부터"; exit 0
fi

if [ "${PACK_ONLY:-0}" = 1 ]; then
  echo "pack_only $(utc)" >> run/env.txt
  if pack; then echo "✅ 포장만 다시 했다 (계산은 다시 돌리지 않았다)"; exit 0; fi
  echo "⛔ 포장 실패 — 디스크·권한을 확인한 뒤 PACK_ONLY=1 로 다시"; exit 4
fi

# ── 단계 · 해제 파일 ──
STAGES=${STAGES:-P}
REL_STAGES=" "; REL_TOTAL=""; REL_VER=""; REL_KERNEL=""; RESTART_RE=""
declare -A REL_SP
for s in $STAGES; do [ -n "${CAP_H[$s]:-}" ] || { echo "⛔ 모르는 단계 $s"; exit 2; }; done
need_rel=0; for s in $STAGES; do [ "$s" = P ] || need_rel=1; done
if [ "$need_rel" = 1 ]; then
  [ -n "${RELEASE_FILE:-}" ] && [ -f "$RELEASE_FILE" ] && [ -n "${RELEASE_SHA256:-}" ] || { echo "⛔ P 밖 단계는 RELEASE_FILE · RELEASE_SHA256 이 필요하다 (파일럿 반송 뒤 받는다)"; exit 2; }
  [ "$(h "$RELEASE_FILE")" = "$RELEASE_SHA256" ] || { echo "⛔ 해제 파일 sha 가 RELEASE_SHA256 과 다르다"; exit 2; }
  while IFS=$'\t' read -r k a b; do
    case "$k" in
      stages) REL_STAGES=" $a ";;
      cap_h) CAP_H[$a]=$b;;
      total_cap_h) REL_TOTAL=$a;;
      vasp_version) REL_VER=$a;;
      species_sha256) REL_SP[$a]=$b;;
      kernel_sha256) REL_KERNEL=$a;;
      restart_read_regex) RESTART_RE=$a;;
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
  [ "$need_rel" = 1 ] && echo "RELEASE $RELEASE_FILE sha256 $RELEASE_SHA256"; } >> run/env.txt
[ -f run/status.tsv ] || printf "job\trung\tstage\trc\tstatus\tn_elec\tdE\tdeps\twhy\twall_s\n" > run/status.tsv

# ── 누적 벽시계 (attempt.json t_start→t_end · 0 스텝 중단 포함) ──
wall_s_of(){ # $1 단계 (ALL = 전체)
  local f j w s tot=0 d
  for f in $(find run run_aborted -name attempt.json 2>/dev/null) $(find run_aborted -name infra_abort.json 2>/dev/null); do
    d=$(dirname "$f")
    if [ "$(basename "$f")" = infra_abort.json ]; then
      [ -f "$d/attempt.json" ] && continue
      w=$(grep -o '"wall_s": "[0-9]*"' "$f" | grep -o '[0-9]*'); w=${w:-0}
    else
      w=$(awk '{ if (match($0, /"t_start": [0-9]+/)) a = substr($0, RSTART + 11, RLENGTH - 11); if (match($0, /"t_end": [0-9]+/)) b = substr($0, RSTART + 9, RLENGTH - 9) } END { print (b != "" && a != "") ? b - a : 0 }' "$f")
    fi
    j=$(grep -o '"job": "[^"]*"' "$f" | head -1 | sed 's/"job": "//; s/"$//')
    s=${STAGE_OF[$j]:-?}
    if [ "$1" = ALL ] || [ "$1" = "$s" ]; then tot=$((tot + w)); fi
  done
  echo "$tot"
}
cap_ok(){ # $1 잡 → 0 이면 띄워도 된다 (단계 · 전체 상한)
  local s=${STAGE_OF[$1]} ws wt
  ws=$(wall_s_of "$s"); wt=$(wall_s_of ALL)
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

# ── 한 시도 ──
run_one(){ # $1 잡 · $2 단 · $3 시도 폴더 · $4 INCAR 이름 · $5 WAVECAR 원본 (B 단만) → 0 돌림 · 3 준비 실패 · 6 공통 환경 고장
  #   A·단 0·r2 는 폴더를 mkdir 로 차지한다 · r1B·a4B 는 ⓐ 가 든 시도 폴더 안에서 `.b` 를 mkdir 로 차지한다 (둘 다 원자적 · 덮어쓰지 않는다)
  local job=$1 rung=$2 d=$3 inc=$4 wsrc=${5:-} rid t0 t1 rc j wsha="" wcp="" wend hd istart icharg nr pr hon ksha="" ver
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
  rid="$(date -u +%Y%m%dT%H%M%S)-$$-$RANDOM"; t0=$(date +%s)
  touch "$d/.running"; watch_scf "$d" "$job/$rung" & local wpid=$!
  (cd "$d" && $VASP_CMD > stdout.log 2>&1); rc=$?; t1=$(date +%s)
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
      pr=NA; if [ -n "$RESTART_RE" ]; then pr=0; grep -aqE "$RESTART_RE" "$d/stdout.log" "$d/OUTCAR" 2>/dev/null && pr=1; fi
      hon=0; [ "$istart" = 1 ] && [ "$icharg" = 0 ] && [ "$nr" = 0 ] && [ "$pr" != 0 ] && [ -n "$wsha" ] && [ "$wsha" = "$wcp" ] && [ "$wcp" = "$wend" ] && hon=1
      printf '{"src_sha256": "%s", "copied_sha256": "%s", "end_sha256": "%s", "istart": "%s", "icharg": "%s", "not_read_phrase": %s, "positive_regex_match": "%s", "honoured": %s}\n' \
        "$wsha" "$wcp" "$wend" "${istart:-NA}" "${icharg:-NA}" "$nr" "$pr" "$hon" > "$d/WAVECAR.info";;
  esac
  printf '{"job": "%s", "attempt": "%s", "stage": "%s", "run_id": "%s", "rc": %d, "t_start": %d, "t_end": %d, "vasp_version": "%s", "kernel_sha256": "%s", "perf": "%s", "sha256": {"INCAR": "%s", "POSCAR": "%s", "KPOINTS": "%s", "POTCAR": "%s", "OUTCAR": "%s", "OSZICAR": "%s", "WAVECAR.info": "%s"}}\n' \
    "$job" "$rung" "${STAGE_OF[$job]}" "$rid" "$rc" "$t0" "$t1" "$ver" "$ksha" "$(printf '%s' "$PERF_LINES" | tr '\n' ';')" \
    "$(h "$d/INCAR")" "$(h "$d/POSCAR")" "$(h "$d/KPOINTS")" "$(cat "$d/POTCAR.sha256")" "$(h "$d/OUTCAR")" "$(h "$d/OSZICAR")" "$(h "$d/WAVECAR.info")" > "$d/attempt.json"
  j=$(judge "$d"); set -- $j
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$job" "$rung" "${STAGE_OF[$job]}" "$rc" "$1" "$2" "$3" "$4" "$5" "$((t1 - t0))" >> run/status.tsv
  rm -f "$d/POTCAR" "$d/CHGCAR" "$d/CHG" "$d/vasprun.xml" "$d/vdw_kernel.bindat"
  case "$rung" in r1A|a4A) ;; *) rm -f "$d/WAVECAR";; esac      # ⓐ WAVECAR 는 그 잡 사다리가 끝날 때까지 둔다 (반송 안 함 · sha·크기·머리만)
  if [ "$need_rel" = 1 ] && [ -n "$ver" ] && [ "$ver" != "$REL_VER" ]; then log "⛔ $job/$rung VASP 빌드 '$ver' ≠ 봉인 — 공통 환경 고장 · 전체 정지"; return 6; fi
  return 0
}
stat_of(){ # 시도 폴더 · 단 → 상태 (B 단은 재시작 확인을 먼저 · 기록 없으면 INCOMPLETE_ATTEMPT)
  local d=$1 j
  [ -f "$d/attempt.json" ] || { echo INCOMPLETE_ATTEMPT; return; }
  case "$2" in r1B|r2B|a4B) grep -q '"honoured": 1' "$d/WAVECAR.info" 2>/dev/null || { echo RESTART_NOT_HONOURED; return; };; esac
  j=$(judge "$d"); echo "${j%% *}"
}
elig_A(){ # ⓐ 자격 (ⓑ 를 띄우기 전 셋 — ① 정상 종료·유한 상태 ② 유효 WAVECAR (머리 = ⓐ OUTCAR) ③ 복사본 sha 는 run_one 이 ⓑ 기록에 남기고 재시작 확인이 본다)
  local d=$1 s r
  s=$(stat_of "$d" A)
  case "$s" in OK|SCF_NOT_CONVERGED) ;; *) echo "ⓐ 상태 $s (정상 종료·유한 상태 아님)"; return 1;; esac
  [ -s "$d/WAVECAR" ] || { echo "ⓐ WAVECAR 없음·빈 파일"; return 1; }
  r=$(awk '{ if (match($0, /"head": "[^"]*"/)) print substr($0, RSTART + 9, RLENGTH - 10) }' "$d/WAVECAR.info"); set -- $r
  [ $# -ge 6 ] && [ "$4" = "$(out_num "$d" NKPTS)" ] && [ "$5" = "$(out_num "$d" NBANDS)" ] && \
    awk -v a="$6" -v b="$(out_num "$d" ENCUT)" 'BEGIN { exit !(b != "" && (a - b < 0.05) && (b - a < 0.05)) }' || { echo "ⓐ WAVECAR 머리 ($r) ≠ OUTCAR NKPTS/NBANDS/ENCUT"; return 1; }
  [ "$(h "$d/WAVECAR")" = "$(grep -o '"sha256": "[0-9a-f]*"' "$d/WAVECAR.info" | head -1 | grep -o '[0-9a-f]\{64\}')" ] || { echo "ⓐ WAVECAR 가 기록 뒤 바뀌었다"; return 1; }
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
