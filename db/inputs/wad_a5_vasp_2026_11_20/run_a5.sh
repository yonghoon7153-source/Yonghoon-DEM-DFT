#!/usr/bin/env bash
# =============================================================================
# run_a5.sh (W_ad V5 개정 5 · a5) — 은 쪽 G4 ENCUT 650 분리 끝점 한 잡 (V5_s_outer_A_G4_e70_far_a5) 의 결과 뒤 재시도 · 사다리 ⓪ → A5 → c1 → (c2)
#   ⓪ 보존된 a4 ⓐ WAVECAR 확인 (W0_WAVECAR · sha · 크기 · 머리 — 원본은 읽기만 · 복사본만 쓴다)
#   A5 LDIPOL 끔 (⓪ 이 확인되면 그 복사본에서 이어서 · 아니면 새로) → c1 (Davidson · MAXMIX 200) → c1 이 주 기준 수렴이 아니면 c2 (ALGO All · TIME 0.1)
#   SCF 판정 = OSZICAR 마지막 전자 반복행 (검사기와 같은 계약 · 외주 2차 judge() 그대로) + 단마다 행 머리 관문 (A5 · c1 = DAV/RMM · c2 = SDA/CGA)
#   개정 5 해석 1 (사용자 2026-11-20): 다음 단은 지금 단이 SCF_NOT_CONVERGED 이거나, 전자 반복행 ≥ 1 인 실행 실패 (--killed 로 기록한 끊김 포함) 로
#     끝났을 때만 띄운다 · 전자 반복행 0 → 멈춤 (7 · 다음 단을 쓰지 않는다) · 재시작 미이행 · SCF 미확인 · 설정 에코 다름 → 멈춤 (8 · 1저자) ·
#     A5 가 행은 있는데 자격 미달이면 개정 5 그대로 (⓪ 이 확인되면 그 복사본에서 c1 · c2 · 아니면 닫는다)
#   필수: VASP_CMD · POTCAR_DIR (PAW_PBE: <POTCAR_DIR>/{Li_sv,P,S,Cl,Ag}/POTCAR) · W0_WAVECAR (보존 ⓐ WAVECAR 경로 — 없으면 W0_WAVECAR=none)
#   선택: PERF_TAGS_FILE (외주 2차와 같은 NCORE = 4 · KPAR = 2 — 세 단 모두 같은 배치라야 NBANDS 872 가 그대로다) · PACK_ONLY=1 · WATCH_S (기본 60)
#   경로는 절대 경로를 권한다 (상대 경로는 이 스크립트를 부른 폴더 기준으로 푼다)
#   기록 명령 (README): --infra-abort · --infra-wall · --killed · --reset-w0 · --unlock
#   종료: 0 c1 또는 c2 주 기준 수렴 (끝) · 1 주 기준 값 없음 — 사다리 끝 (끝 · 실패도 기록) · 2 인자 · 묶음 · 환경 오류 (아무것도 띄우지 않음)
#         3 준비 실패 (그 단은 소모 안 함 — 원인을 고친 뒤 다시) · 4 포장 실패 (PACK_ONLY=1 로 다시)
#         5 누적 상한 180 h (끝) 또는 끊긴 시도 · 벽시계 미상 (--killed · --infra-abort · --infra-wall 로 기록한 뒤 다시)
#         6 공통 환경 고장 (VASP 빌드 · PP — 전체 정지) · 7 전자 반복행 0 (--infra-abort 또는 연락) · 8 1저자 검토 멈춤 (끝)
#   끝 (0 · 1 · 5 상한 · 8 · 돈 뒤의 6 — VASP 빌드 다름) 뒤에 다시 돌리면 run/final.json 을 찍고 같은 코드로 끝낸다 — 아무것도 띄우지 않는다 (포장만: PACK_ONLY=1)
#   보내는 것: 끝 뒤 `sha256sum -c a5_return.tgz.sha256` 까지 통과한 쌍
#   지원 환경: Linux · bash ≥ 4 · GNU coreutils (find sort grep cmp sha256sum od stat mv -T) · GNU tar · awk (mawk/gawk) · sed -E
# =============================================================================
set -u
ORIG_PWD=$PWD
absp(){ case "$1" in /*) printf '%s' "$1";; *) printf '%s/%s' "${ORIG_PWD%/}" "$1";; esac; }    # 상대 경로 → 부른 곳 기준 절대 경로 (cd 전에 푼다 · 리뷰 P1-3)
if [ -n "${W0_WAVECAR:-}" ] && [ "$W0_WAVECAR" != none ]; then W0_WAVECAR=$(absp "$W0_WAVECAR"); fi
if [ -n "${POTCAR_DIR:-}" ]; then POTCAR_DIR=$(absp "$POTCAR_DIR"); fi
if [ -n "${PERF_TAGS_FILE:-}" ]; then PERF_TAGS_FILE=$(absp "$PERF_TAGS_FILE"); fi
HERE=$(cd "$(dirname "$0")" && pwd); cd "$HERE"
sha256sum -c --quiet MANIFEST.sha256 || { echo "⛔ 패키지 파일이 MANIFEST 와 다르다 — 실행하지 않는다"; exit 2; }
RET_ALLOW='OUTCAR|OSZICAR|INCAR|KPOINTS|POSCAR|IBZKPT|POTCAR\.titel|POTCAR\.sha256|POTCAR\.species\.sha256|attempt\.json|stdout\.log|WAVECAR\.info|warn\.log|infra_abort\.json|LOCPOT\.zavg\.txt|attempt\.start|killed\.json'
RET_FORBID='POTCAR|WAVECAR|CHGCAR|CHG|vasprun\.xml|vdw_kernel\.bindat|LOCPOT'
JOB=V5_s_outer_A_G4_e70_far_a5
HOST=$(hostname 2>/dev/null || uname -n 2>/dev/null || echo unknown-host)
# ── 묶음 폴더에 a5 가 아닌 것 (외주 2차 폴더에 풀었을 때 · 다른 잡 흔적) → 거부 (리뷰 P2(g)) · 스케줄러 출력 파일만 둔다 ──
foreign(){
  local f b
  for f in * .[!.]* ..?*; do
    [ -e "$f" ] || [ -L "$f" ] || continue
    case "$f" in
      MANIFEST.sha256|README.md|SEALED_ENV.tsv|run_a5.sh|jobs.json|a5_return.tgz|a5_return.tgz.sha256|a5_return.list|a5_return.tgz.part|a5_return.tgz.sha256.part)
        { [ -f "$f" ] && [ ! -L "$f" ]; } || echo "$f";;
      jobs|run|run_aborted|a5_return.tmp) { [ -d "$f" ] && [ ! -L "$f" ]; } || echo "$f";;
      *.[eo][0-9]*|*.p[eo][0-9]*|slurm-*.out|nohup.out) [ -f "$f" ] || echo "$f";;
      *) echo "$f";;
    esac
  done
  for f in jobs/* jobs/.[!.]* jobs/..?*; do
    [ -e "$f" ] || [ -L "$f" ] || continue
    { [ "$f" = "jobs/$JOB" ] && [ -d "$f" ] && [ ! -L "$f" ]; } || echo "$f"
  done
  for f in run/* run/.[!.]* run/..?*; do
    [ -e "$f" ] || [ -L "$f" ] || continue
    b=${f#run/}
    case "$b" in
      "${JOB}_A5"|"${JOB}_c1"|"${JOB}_c2"|.a5.lock|".prep_${JOB}_A5"|".prep_${JOB}_c1"|".prep_${JOB}_c2") { [ -d "$f" ] && [ ! -L "$f" ]; } || echo "$f";;
      env.txt|status.tsv|infra_aborts.tsv|w0_check.json|start_point.json|final.json|*.part) { [ -f "$f" ] && [ ! -L "$f" ]; } || echo "$f";;
      *) echo "$f";;
    esac
  done
  for f in run_aborted/* run_aborted/.[!.]* run_aborted/..?*; do
    [ -e "$f" ] || [ -L "$f" ] || continue
    b=${f#run_aborted/}
    if [[ "$b" =~ ^${JOB}_(A5|c1|c2)_[1-9][0-9]*$ ]] && [ -d "$f" ] && [ ! -L "$f" ]; then :; else echo "$f"; fi
  done
}
FX=$(foreign | head -6)
[ -z "$FX" ] || { echo "⛔ 이 폴더에 a5 묶음이 아닌 것이 있다: $(printf '%s' "$FX" | tr '\n' ' ')— 새 빈 폴더에 풀어 주세요 (외주 2차 폴더에 풀지 않는다 · 묶음 zip · 제출 스크립트는 폴더 밖에)"; exit 2; }
mkdir -p run

# ── 외주 2차 러너 부품 (build_round2_vasp_package.RUN_ALL 에서 이름으로 꺼냄 · 패치 자리는 build_a5 r2_parts) ──
h(){ sha256sum "$1" 2>/dev/null | cut -d' ' -f1; }
utc(){ date -u +%FT%TZ; }
up(){ awk '{ printf "%d", $1 }' /proc/uptime 2>/dev/null; }    # 부팅 뒤 초 (단조 시계) — 벽시계 장부는 이것으로 잰다 (date 는 시계 맞춤으로 뒤로 갈 수 있다 · 자체 검토 S4)
log(){ echo "$*"; echo "$(utc) $*" >> run/env.txt; }
clean(){ printf '%s' "$1" | tr -d '"\\\r\n\t' ; }
enc_eq(){ [[ "$1" =~ ^[0-9]+(\.[0-9]+)?$ && "$2" =~ ^[0-9]+(\.[0-9]+)?$ ]] && awk -v a="$1" -v b="$2" 'BEGIN { exit !((a - b < 0.05) && (b - a < 0.05)) }'; }   # ENCUT 같음 (±0.05) — 숫자 꼴만 (awk 는 '520abc' 를 520 으로 읽는다 · Codex DD 와 같은 종류)
cap_num(){ [[ "$1" =~ ^[0-9]+(\.[0-9]+)?$ ]] && awk -v x="$1" 'BEGIN { exit !(x + 0 > 0) }'; }   # 상한 값 = 유한한 양수 (nan · inf · 음수 · 0 거부)
secs_ok(){ [[ "$1" =~ ^(0|[1-9][0-9]{0,8})$ ]]; }    # 손으로 넣는 초 = 10진 정수 · 선행 0 없음 · 9 자리 이하 (bash 산술은 선행 0 을 8진수로 읽는다 — Codex DB P1-3)
incar_val(){ awk -v T="$2" 'BEGIN{T=toupper(T)} { sub(/[#!].*/, ""); n=split($0, st, ";"); for (i=1; i<=n; i++) { s=st[i]; p=index(s, "="); if (!p) continue;
  k=substr(s, 1, p-1); v=substr(s, p+1); gsub(/[ \t]/, "", k); gsub(/^[ \t]+|[ \t]+$/, "", v); if (toupper(k)==T) val=v } } END { if (val!="") print val }' "$1" 2>/dev/null; }
judge_r2(){
  local d=$1 rc term nrun nelm ediff oit
  rc=$(grep -o '"rc": [^,}]*[,}]' "$d/attempt.json" 2>/dev/null | head -1 | sed 's/^"rc": //; s/[,}]$//')   # 전체 값 + 끝 구분자 (숫자 접두부가 아니다 · Codex DC P1-2 와 같은 종류)
  rc=${rc:-${2:-NA}}                                    # 정수 꼴 검사는 아래 awk (rc_unknown) 한 곳에서
  term=0; grep -aq "General timing and accounting" "$d/OUTCAR" 2>/dev/null && term=1
  nrun=$(grep -acE '^[[:space:]]*vasp\.[0-9]' "$d/OUTCAR" 2>/dev/null); nrun=${nrun:-0}
  nelm=$(incar_val "$d/INCAR" NELM); ediff=$(incar_val "$d/INCAR" EDIFF)
  oit=$(grep -aoE 'Iteration +[0-9]+\( *[0-9]+\)' "$d/OUTCAR" 2>/dev/null | tail -1 | sed -E 's/.*\( *([0-9]+)\)/\1/')
  osz_feed "$d" | J_RC="$rc" J_TERM="$term" J_NRUN="$nrun" J_NELM="${nelm:-NA}" J_EDIFF="${ediff:-NA}" J_OIT="${oit:-NA}" awk '
    BEGIN { rc = ENVIRON["J_RC"]; term = ENVIRON["J_TERM"]; nrun = ENVIRON["J_NRUN"]; nelm = ENVIRON["J_NELM"]; ediff = ENVIRON["J_EDIFF"]; oit = ENVIRON["J_OIT"] }   # 원문 그대로 — awk -v 는 \060 같은 이스케이프를 풀어 버린다 (Codex DD P1-2)
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
      if (rc !~ /^(0|-?[1-9][0-9]*)$/) { print "SCF_UNVERIFIED", o, "NA", "NA", "rc_unknown"; exit }
      if (rc != "0" || term != 1) { print "RUN_FAILED", o, (de == "" ? "NA" : de), (dp == "" ? "NA" : dp), "rc_or_not_terminated"; exit }
      if (!finite(de) || !finite(dp)) { print "SCF_UNVERIFIED", o, (de == "" ? "NA" : de), (dp == "" ? "NA" : dp), "nonfinite"; exit }
      if (!finite(ediff)) { print "SCF_UNVERIFIED", o, de, dp, "ediff_unknown"; exit }
      a = de + 0; b = dp + 0; if (a < 0) a = -a; if (b < 0) b = -b
      if (a <= ediff + 0 && b <= ediff + 0) print "OK", o, de, dp, "-"; else print "SCF_NOT_CONVERGED", o, de, dp, "-" }'
}
alarms(){ awk 'function isnum(s) { return s ~ /^[-+]?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][-+]?[0-9]+)?$/ }
  function ab(x) { return x < 0 ? -x : x }
  /^[ \t]*(DAV|RMM|CG|SDA|CGA):/ { n++; e[n] = $4; p[n] = $5 }
  END { out = ""; if (n == 0) { print "0 -"; exit }
    if (!isnum(e[n]) || !isnum(p[n])) out = out "nonfinite,"
    for (q = 1; q <= 2; q++) { last = (q == 1) ? e[n] : p[n]; stall = (isnum(last) && ab(last + 0) > 1e-4)
      if (n >= 80) { m1 = -1; m2 = -1
        for (i = n - 39; i <= n; i++) { v = (q == 1) ? e[i] : p[i]; if (isnum(v)) { v = ab(v + 0); if (m1 < 0 || v < m1) m1 = v } }
        for (i = n - 79; i <= n - 40; i++) { v = (q == 1) ? e[i] : p[i]; if (isnum(v)) { v = ab(v + 0); if (m2 < 0 || v < m2) m2 = v } }
        if (m1 >= 0 && m2 >= 0 && m1 >= m2) stall = 1 }
      if (stall) out = out ((q == 1) ? "dE_stall," : "deps_stall,") }
    print n, (out == "" ? "-" : out) }' "$1/OSZICAR" 2>/dev/null; }
pack_fail(){ echo "⛔ 포장: $1"; rm -f a5_return.tgz.part a5_return.tgz.sha256.part; return 1; }
pack(){
  local T=a5_return.tmp g hh n_mg n_so n_li f dirs=run
  rm -rf "$T" a5_return.tgz.part a5_return.tgz.sha256.part a5_return.list; mkdir "$T" || return 1
  [ -d run_aborted ] && dirs="run run_aborted"                   # 있는 폴더만 열거한다 — 없는 폴더의 오류를 덮으려다 run/ 열거 실패까지 덮지 않게 (CZ Q-CZ-10 ①)
  find $dirs -mindepth 2 -maxdepth 3 -type f > "$T/found" 2> "$T/find.err"; g=$?
  [ "$g" = 0 ] || { pack_fail "반송 폴더 열거 실패 (find $g: $(head -c 200 "$T/find.err" | tr '\n' ' '))"; return 1; }
  grep -E "^(run|run_aborted)/[^/.][^/]*/(stageA/)?($RET_ALLOW)$" "$T/found" > "$T/allowed"; g=$?
  [ "$g" -le 1 ] || { pack_fail "허용 목록 필터 오류 ($g)"; return 1; }
  LC_ALL=C sort "$T/allowed" > "$T/sorted" || { pack_fail "정렬 실패"; return 1; }
  : > "$T/mgmt" || { pack_fail "관리 목록 초기화 실패"; return 1; }
  n_mg=0
  for f in run/env.txt run/status.tsv run/infra_aborts.tsv run/w0_check.json run/start_point.json run/final.json; do
    [ -f "$f" ] || continue
    n_mg=$((n_mg + 1)); echo "$f" >> "$T/mgmt" || { pack_fail "관리 목록 쓰기 실패 ($f)"; return 1; }
  done
  echo MANIFEST.sha256 > a5_return.list || { pack_fail "목록 쓰기 실패 (MANIFEST.sha256)"; return 1; }
  cat "$T/mgmt" "$T/sorted" >> a5_return.list || { pack_fail "목록 쓰기 실패"; return 1; }
  n_so=$(wc -l < "$T/sorted") && n_li=$(wc -l < a5_return.list) || { pack_fail "목록 검증 준비 실패"; return 1; }
  [ "$n_li" -eq $((1 + n_mg + n_so)) ] || { pack_fail "목록 줄 수가 맞지 않는다 ($n_li ≠ 1+$n_mg+$n_so)"; return 1; }
  grep -qxF MANIFEST.sha256 a5_return.list || { pack_fail "목록에 MANIFEST.sha256 이 없다"; return 1; }
  tar czf a5_return.tgz.part -T a5_return.list || { pack_fail "tar 실패"; return 1; }
  tar tzf a5_return.tgz.part > "$T/members" || { pack_fail "묶음 구성원 열람 실패 — 검사할 수 없으면 보내지 않는다"; return 1; }
  grep -E "(^|/)($RET_FORBID)$" "$T/members" > "$T/forbidden"; g=$?
  if [ "$g" -eq 0 ]; then pack_fail "반송 묶음에 금지 파일이 들어갔다 — 보내지 않는다: $(tr '\n' ' ' < "$T/forbidden")"; return 1
  elif [ "$g" -ne 1 ]; then pack_fail "구성원 검사 오류 ($g)"; return 1; fi
  LC_ALL=C sort "$T/members" > "$T/members.sorted" && LC_ALL=C sort a5_return.list > "$T/list.sorted" || { pack_fail "구성원 대조 준비 실패"; return 1; }
  cmp -s "$T/members.sorted" "$T/list.sorted" || { pack_fail "묶음 구성원이 목록과 다르다 — 보내지 않는다"; return 1; }
  sha256sum a5_return.tgz.part > "$T/sha" || { pack_fail "sha256 계산 실패"; return 1; }
  hh=$(cut -d' ' -f1 < "$T/sha") || { pack_fail "sha256 읽기 실패"; return 1; }
  [[ "$hh" =~ ^[0-9a-fA-F]{64}$ ]] || { pack_fail "sha256 형식 이상 ($hh)"; return 1; }
  printf '%s  a5_return.tgz\n' "$hh" > a5_return.tgz.sha256.part || { pack_fail "sha 쓰기 실패"; return 1; }
  mv -f a5_return.tgz.part a5_return.tgz && mv -f a5_return.tgz.sha256.part a5_return.tgz.sha256 || { pack_fail "승격(mv) 실패 — sha256sum -c 로 확인"; return 1; }
  rm -rf "$T" || echo "⚠ 진단 폴더 정리 실패 — 묶음은 승격됐다"
  return 0
}
finish(){ # $1 종료 코드 — 포장하고 끝낸다 (포장 실패면 4)
  if ! pack; then echo "⛔ 반송 포장 실패 — 계산 결과는 run/ 에 그대로 있다. 다시 돌리지 말고 PACK_ONLY=1 bash run_a5.sh 로 포장만"; exit 4; fi
  case "$1" in
    0) echo "✅ 끝 — a5_return.tgz 와 .sha256 을 보내 주세요";;
    1) echo "⚠ 주 기준 값 없음 — 그대로 반송해 주세요 (보조 기준은 반송 뒤 우리가 봅니다 · 실패도 기록입니다)";;
    5) echo "⏸ 누적 상한 — 다음 단을 띄우지 않았다. 반송해 주시고 1저자 결정을 기다려 주세요";;
    6) echo "⛔ 공통 환경 고장 — 전체 정지. 반송해 주시고 연락 주세요";;
    8) echo "⏸ 1저자 검토 멈춤 (개정 5 해석 1) — 더 돌리지 않았다. 반송해 주시고 1저자 결정을 기다려 주세요 (다시 돌려도 아무것도 띄우지 않는다)";;
  esac
  exit "$1"
}
pp_ok(){ # $1 잡 — 해제 뒤에는 PP 종별 sha 가 봉인과 같아야 한다
  local p
  [ "$need_rel" = 1 ] || return 0
  while read -r p; do [ -n "$p" ] || continue
    [ "$(h "$POTCAR_DIR/$p/POTCAR")" = "${REL_SP[$p]:-x}" ] || { log "⛔ POTCAR $p sha 가 봉인과 다르다 — 공통 환경 고장 · 전체 정지"; return 1; }
  done < "jobs/$1/POTCAR.spec"
}
ver_of(){ grep -am1 -E '^[[:space:]]*vasp\.[0-9]' "$1/OUTCAR" 2>/dev/null | tr -s '[:space:]' ' ' | sed 's/^ //; s/ $//'; }
wav_head(){ local f=$1 r
  r=$(od -A n -t f8 -N 24 "$f" 2>/dev/null | awk '{ for (i = 1; i <= NF; i++) printf "%.0f ", $i }'); set -- $r
  [ $# -eq 3 ] && [ "$1" -gt 0 ] 2>/dev/null || { echo "NA NA NA NA NA NA"; return; }
  echo "$1 $2 $3 $(od -A n -t f8 -j "$1" -N 24 "$f" 2>/dev/null | awk '{ for (i = 1; i <= NF; i++) printf "%s ", ($i == int($i) ? sprintf("%.0f", $i) : sprintf("%.4f", $i)) }')"
}
out_num(){ if [ "$2" = ENCUT ]; then grep -aoE "ENCUT *= *[0-9.]+ eV" "$1/OUTCAR" 2>/dev/null | tail -1 | grep -oE '[0-9.]+ eV$' | grep -oE '^[0-9.]+';
  else grep -aoE "$2 *= *[0-9.]+" "$1/OUTCAR" 2>/dev/null | tail -1 | grep -oE '[0-9.]+$'; fi; }
wsha(){ grep -o "\"$2\": \"[0-9a-f]\{64\}\"" "$1" 2>/dev/null | head -1 | grep -o '[0-9a-f]\{64\}'; }   # WAVECAR.info 의 sha 필드 하나 ($1 파일 · $2 키)

# ── 봉인 환경 (외주 2차 등록부에서 · 빌드가 쓴다) · ⓪ 기대값 · 상한 ──
need_rel=1; REL_VER=""; RESTART_RE=""; W0_SHA=""; W0_SIZE=""; W0_NK=""; W0_NB=""; W0_EN=""; CAP_H=""; INFRA_MAX=""
declare -A REL_SP
while IFS=$'\t' read -r k a b; do
  case "$k" in
    vasp_version) REL_VER=$a;; species_sha256) REL_SP[$a]=$b;; restart_read_regex) RESTART_RE=$a;;
    w0_sha256) W0_SHA=$a;; w0_size) W0_SIZE=$a;; w0_nkpts) W0_NK=$a;; w0_nbands) W0_NB=$a;; w0_encut) W0_EN=$a;;
    cap_h) CAP_H=$a;; infra_max) INFRA_MAX=$a;;
  esac
done < SEALED_ENV.tsv
[ -n "$REL_VER" ] && [ "${#REL_SP[@]}" -ge 5 ] && [ -n "$RESTART_RE" ] && [[ "$W0_SHA" =~ ^[0-9a-f]{64}$ ]] && [[ "$W0_SIZE" =~ ^[0-9]+$ ]] \
  && [ -n "$W0_NK" ] && [ -n "$W0_NB" ] && [ -n "$W0_EN" ] && cap_num "$CAP_H" && [[ "$INFRA_MAX" =~ ^[0-9]+$ ]] \
  || { echo "⛔ SEALED_ENV.tsv 가 불완전하다 — 실행하지 않는다"; exit 2; }
incar_of(){ case "$1" in A5c) echo INCAR.a5A5c;; A5f) echo INCAR.a5A5f;; c1) echo INCAR.a5c1;; c2) echo INCAR.a5c2;; esac; }
stage_hdr(){ case "$1" in A5|c1) echo 'DAV|RMM';; c2) echo 'SDA|CGA';; esac; }

# ── 행 머리 관문 (검사기 row_gate 와 같다): 줄 맨 앞 1–4 글자 + ':' 를 행으로 보고, 그 단의 허용 머리 밖이면 SCF_UNVERIFIED ──
hdr_gate(){ awk -v A="^(${2})\$" '/^[ \t]*[A-Za-z][A-Za-z ]?[A-Za-z ]?[A-Za-z ]?:/ { n++; h = $0; sub(/^[ \t]*/, "", h); sub(/:.*/, "", h); gsub(/ /, "", h)
    if (bad == "" && h !~ A) bad = "row_header_" h }
  END { print n + 0, (bad == "" ? "-" : bad) }' "$1/OSZICAR" 2>/dev/null; }
osz_feed(){ sed -E "s/^([[:space:]]*)(${HDR}):/\1DAV:/" "$1/OSZICAR" 2>/dev/null; }
judge5(){ # $1 시도 폴더 · $2 단 → "상태 행수 dE deps 사유" (judge 와 같은 꼴)
  local d=$1 HDR g n why
  HDR=$(stage_hdr "$2"); [ -n "$HDR" ] || { echo "SCF_UNVERIFIED 0 NA NA unknown_stage"; return; }
  [ -f "$d/OSZICAR" ] || { judge_r2 "$d"; return; }
  g=$(hdr_gate "$d" "$HDR"); n=${g%% *}; why=${g#* }
  [ -n "$g" ] || { judge_r2 "$d"; return; }
  if [ "$why" != "-" ]; then echo "SCF_UNVERIFIED ${n:-0} NA NA $why"; return; fi
  judge_r2 "$d"
}
rows_of(){ local n; n=$(grep -acE '^[[:space:]]*[A-Za-z][A-Za-z ]?[A-Za-z ]?[A-Za-z ]?:' "$1/OSZICAR" 2>/dev/null); echo "${n:-0}"; }   # 전자 반복행 수 (관문과 같은 꼴 · 없으면 0)
stat5(){ # $1 시도 폴더 · $2 단 · $3 시작 WAVECAR sha (c1 · c2) → 상태. 순서 (검사기와 같다): 행 0 → SCF_UNVERIFIED (재시작 확인 전 · 리뷰 P2(f)) →
  #        c1 · c2 재시작 (sha 셋 · 문구 · c 단 OUTCAR NKPTS·NBANDS·ENCUT = 시작 WAVECAR 머리 — 리뷰 P3) → 판정. A5 는 재시작이 자격이 아니다
  local d=$1 st=$2 ss=${3:-} j n
  [ -f "$d/attempt.json" ] || { echo INCOMPLETE_ATTEMPT; return; }
  j=$(judge5 "$d" "$st"); n=$(printf '%s\n' "$j" | awk '{ print $2; exit }')
  [ "$n" = 0 ] && { echo SCF_UNVERIFIED; return; }
  case "$st" in c1|c2)
    { grep -q '"honoured": 1' "$d/WAVECAR.info" 2>/dev/null && [ -n "$ss" ] && [ "$(wsha "$d/WAVECAR.info" src_sha256)" = "$ss" ] \
      && [ "$(wsha "$d/WAVECAR.info" copied_sha256)" = "$ss" ] && [ "$(wsha "$d/WAVECAR.info" end_sha256)" = "$ss" ] \
      && grep -aqE -e "$RESTART_RE" "$d/stdout.log" "$d/OUTCAR" 2>/dev/null \
      && [ "$(out_num "$d" NKPTS)" = "${SP_NK:-x}" ] && [ "$(out_num "$d" NBANDS)" = "${SP_NB:-x}" ] && enc_eq "$(out_num "$d" ENCUT)" "${SP_EN:-x}"; } \
      || { echo RESTART_NOT_HONOURED; return; };;
  esac
  echo "${j%% *}"
}
echo5(){ # $1 시도 폴더 · $2 변형 → "-" (맞음) 또는 "키:값!=기대,…" — a5 가 바꾼 설정의 OUTCAR 해석값 (입력 에코 구획 INCAR: … POTCAR: 은 뺀다) ·
  #        검사기 echo5 와 같은 키 · 같은 정규식 꼴 · 같은 허용치 (러너가 1저자 멈춤을 거는 부분집합 · 나머지 설정은 검사기 audit5)
  local ne ld ia am an mx tm
  case "$2" in
    A5c|A5f) ne=300; ld=F; ia=38; am=0.1; an=0.01; mx=200; tm="";;
    c1) ne=400; ld=T; ia=38; am=0.1; an=0.01; mx=200; tm="";;
    c2) ne=400; ld=T; ia=58; am=""; an=""; mx=""; tm=0.1;;
    *) echo "variant:$2"; return;;
  esac
  [ -f "$1/OUTCAR" ] || { echo "OUTCAR:missing"; return; }
  awk -v NE="$ne" -v LD="$ld" -v IA="$ia" -v AM="$am" -v AN="$an" -v MX="$mx" -v TM="$tm" '
    function isnum(s) { return s ~ /^[-+]?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][-+]?[0-9]+)?$/ }
    function ab(x) { return x < 0 ? -x : x }
    function val(s, re,   t) { t = s; sub(re, "", t); if (match(t, /^[^; \t]+/)) return substr(t, 1, RLENGTH); return "" }
    function chk(k, g, w, tol) { if (w == "") return; if (g == "") { out = out k ":missing,"; return }
      if (!isnum(g) || ab(g - w) > tol + 1e-12) out = out k ":" g "!=" w "," }
    /^[ \t]*INCAR:[ \t]*$/ { skip = 1; next }
    skip { if ($0 ~ /^[ \t]*POTCAR:/) skip = 0; else next }
    /^[ \t]*NELM[ \t]*=[ \t]*[0-9]/ { x = val($0, "^[ \t]*NELM[ \t]*=[ \t]*"); if (match(x, /^[0-9]+/)) gne = substr(x, 1, RLENGTH) }
    /^[ \t]*IALGO[ \t]*=[ \t]*[0-9]/ { x = val($0, "^[ \t]*IALGO[ \t]*=[ \t]*"); if (match(x, /^[0-9]+/)) gia = substr(x, 1, RLENGTH) }
    /^[ \t]*AMIX[ \t]*=[ \t]*[^; \t]+[ \t]*;[ \t]*BMIX/ { gam = val($0, "^[ \t]*AMIX[ \t]*=[ \t]*") }
    /^[ \t]*AMIN[ \t]*=[ \t]*[^ \t]/ { t = $0; sub(/^[ \t]*AMIN[ \t]*=[ \t]*/, "", t); if (match(t, /^[^ \t]+/)) gan = substr(t, 1, RLENGTH) }
    /MAXMIX[ \t]*=[ \t]*-?[0-9]/ { t = $0; sub(/.*MAXMIX[ \t]*=[ \t]*/, "", t); if (match(t, /^-?[0-9]+/)) gmx = substr(t, 1, RLENGTH) }
    /^[ \t]*TIME[ \t]*=[ \t]*[^ \t]/ { t = $0; sub(/^[ \t]*TIME[ \t]*=[ \t]*/, "", t); if (match(t, /^[^ \t]+/)) gtm = substr(t, 1, RLENGTH) }
    /^[ \t]*LDIPOL[ \t]*=[ \t]*[^ \t]/ { t = $0; sub(/^[ \t]*LDIPOL[ \t]*=[ \t]*/, "", t); if (match(t, /^[^ \t]+/)) gld = substr(t, 1, RLENGTH) }
    END { out = ""
      chk("NELM", gne, NE, 0); chk("IALGO", gia, IA, 0); chk("AMIX", gam, AM, 1e-3); chk("AMIN", gan, AN, 1e-4); chk("MAXMIX", gmx, MX, 0); chk("TIME", gtm, TM, 1e-3)
      l = gld; gsub(/^\.+|\.+$/, "", l); l = toupper(substr(l, 1, 1))
      if (gld == "") out = out "LDIPOL:missing,"; else if (l != LD) out = out "LDIPOL:" gld "!=" LD ","
      print (out == "" ? "-" : out) }' "$1/OUTCAR" 2>/dev/null || echo "OUTCAR:unreadable"
}
hist_max(){ awk '/eigenvalues of \(default mixing \* dielectric matrix\)/ { if (c == 2 && k > m) m = k; c = 1; k = 0; next }
  c == 1 { c = 2; next }
  c == 2 { if (NF == 0) { if (k > m) m = k; c = 0; next } for (i = 1; i <= NF; i++) if ($i ~ /^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$/) k++ }
  END { if (c == 2 && k > m) m = k; print m + 0 }' "$1/OUTCAR" 2>/dev/null; }
rms_jump(){ # $1 시도 폴더 · $2 단 → rms(c) 가 직전 20 스텝 최솟값의 100 배를 넘은 마지막 스텝 (없으면 0) · 정보
  awk -v H="^[ \t]*($(stage_hdr "$2")):" 'function isnum(s) { return s ~ /^[-+]?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][-+]?[0-9]+)?$/ }
    $0 ~ H { n++; v[n] = (NF >= 8 && isnum($8)) ? $8 + 0 : -1 }
    END { last = 0; for (k = 21; k <= n; k++) { if (v[k] < 0) continue; m = -1
            for (i = k - 20; i < k; i++) if (v[i] >= 0 && (m < 0 || v[i] < m)) m = v[i]
            if (m >= 0 && v[k] > 100 * m) last = k }
          print last }' "$1/OSZICAR" 2>/dev/null; }
watch5(){ # $1 시도 폴더 · $2 꼬리표 · $3 단 — 외주 2차 alarms (120 스텝 뒤 20 스텝마다) + a5 정보 (이력 길이 > 45 · rms(c) 급등) · 경보 ≠ 중단
  local d=$1 tag=$2 st=$3 last=100 o n a hm=0 rj=0 x
  while [ -f "$d/.running" ]; do
    sleep "${WATCH_S:-60}"
    [ -f "$d/OSZICAR" ] || continue
    o=$(alarms "$d"); n=${o%% *}; a=${o#* }
    case "$n" in ''|*[!0-9]*) continue;; esac
    if [ "$n" -ge 120 ] && [ "$n" -ge $((last + 20)) ]; then
      last=$((n - n % 20))
      if [ "$a" != "-" ]; then echo "$(utc) $tag step $n $a" >> "$d/warn.log"; log "⚠ 경보 $tag 스텝 $n: $a (중단 아님 · NELM 까지 돈다)"; fi
    fi
    [ "$st" = c2 ] && continue
    if [ "$hm" = 0 ]; then x=$(hist_max "$d"); case "$x" in ''|*[!0-9]*) ;; *) if [ "$x" -gt 45 ]; then hm=1; echo "$(utc) $tag info history_gt45 $x" >> "$d/warn.log"; fi;; esac; fi
    x=$(rms_jump "$d" "$st")
    case "$x" in ''|*[!0-9]*) ;; *) if [ "$x" -gt "$rj" ]; then rj=$x; echo "$(utc) $tag info rmsc_jump_step $x" >> "$d/warn.log"
      log "⚠ 정보 $tag rms(c) 급등 스텝 $x (직전 20 스텝 최솟값의 100 배 초과 · 중단 아님 — c1 이 실패하면 c2 는 혼합기를 안 쓴다)"; fi;; esac
  done
}

# ── 잠금 run/.a5.lock (원자적 mkdir) · 주인 = 기계 이름 + PID. 다른 기계의 잠금은 살아 있는지 알 수 없어 '살아 있음' 으로 본다 (리뷰 P2(d)) ──
LOCK=run/.a5.lock
lock_state(){ # → "상태 기계 PID" — none · live (이 기계 · 살아 있음) · stale (이 기계 · 죽음) · foreign (다른 기계 · 주인 기록 없음 포함)
  local o hh pp
  [ -d "$LOCK" ] || { echo "none - -"; return; }
  o=$(cat "$LOCK/owner" 2>/dev/null); hh=$(printf '%s\n' "$o" | awk '{ print $1; exit }'); pp=$(printf '%s\n' "$o" | awk '{ print $2; exit }')
  [ -n "$hh" ] || hh=-; [ -n "$pp" ] || pp=-
  if [ "$hh" != "$HOST" ]; then echo "foreign $hh $pp"
  elif [[ "$pp" =~ ^[0-9]+$ ]] && kill -0 "$pp" 2>/dev/null; then echo "live $hh $pp"
  else echo "stale $hh $pp"; fi
}
lock_say(){ # $1 상태 · $2 기계 · $3 PID · $4 거부한 것
  case "$1" in
    live) echo "⛔ run_a5.sh (기계 $2 · PID $3) 가 이 묶음에서 돌고 있다 — $4 는 그 실행이 끝난 뒤에";;
    *) echo "⛔ 다른 기계의 잠금 (기계 $2 · PID $3) — 여기서는 살아 있는지 알 수 없어 돌고 있는 것으로 본다 ($4 거부). 스케줄러로 그 잡이 끝났는지 확인한 뒤 'bash run_a5.sh --unlock $2 $3' 로 지우고 다시";;
  esac
}
read -r LK_S LK_H LK_P <<< "$(lock_state)"
if [ "${1:-}" != --unlock ] && { [ $# -gt 0 ] || [ "${PACK_ONLY:-0}" = 1 ]; }; then
  case "$LK_S" in live|foreign) lock_say "$LK_S" "$LK_H" "$LK_P" "기록 · 포장 명령"; exit 2;; esac
fi

# ── 끝난 사다리 (run/final.json) 에는 기록을 더하지 않는다 · 뒤 단이 있으면 앞 단 기록을 고치지 않는다 (리뷰 P1-1 · P0-2(c)) ──
later5(){ # $1 단 → 그 뒤 단의 폴더 · 기록 이름 (없으면 빈 출력)
  local x
  case "$1" in
    A5) for x in "run/${JOB}_c1" "run/${JOB}_c2" run/start_point.json; do [ -e "$x" ] && { echo "$x"; return; }; done
        compgen -G "run_aborted/${JOB}_c[12]_*" | head -1;;
    c1) [ -e "run/${JOB}_c2" ] && { echo "run/${JOB}_c2"; return; }
        compgen -G "run_aborted/${JOB}_c2_*" | head -1;;
  esac
}
case "${1:-}" in --infra-abort|--infra-wall|--killed|--reset-w0)
  [ ! -f run/final.json ] || { echo "⛔ 이 사다리는 끝났다 (run/final.json: $(tr -d '\n' < run/final.json | cut -c1-200)) — 기록을 더하거나 고치지 않는다 (포장만: PACK_ONLY=1)"; exit 2; };;
esac

# ── 잠금 지우기 — 운영자가 스케줄러로 그 잡이 끝났음을 확인한 뒤 (주인을 그대로 적어야 지운다) ──
if [ "${1:-}" = "--unlock" ]; then
  [ $# -eq 3 ] || { echo "⛔ 쓰는 법: bash run_a5.sh --unlock <기계> <PID> (잠금 주인을 그대로)"; exit 2; }
  [ "$LK_S" != none ] || { echo "⛔ 잠금이 없다"; exit 2; }
  { [ "$2" = "$LK_H" ] && [ "$3" = "$LK_P" ]; } || { echo "⛔ 잠금 주인은 기계 $LK_H · PID $LK_P 다 — 그대로 적어야 지운다"; exit 2; }
  [ "$LK_S" != live ] || { echo "⛔ 이 기계에서 PID $LK_P 가 살아 있다 — 지우지 않는다"; exit 2; }
  rm -rf "$LOCK" || { echo "⛔ 잠금을 지우지 못했다"; exit 2; }
  log "✎ 잠금을 지웠다 (기계 $LK_H · PID $LK_P · $LK_S — 운영자 확인)"; echo "✓ 잠금을 지웠다 — 다시 돌리면 기록에서 이어 간다"; exit 0
fi

# ── ⓪ 기록 지우기 — A5 를 띄우기 전에만 (경로를 잘못 적어 'sha 다름' 이 기록된 경우 · 리뷰 P1-3) ──
if [ "${1:-}" = "--reset-w0" ]; then
  [ $# -eq 1 ] || { echo "⛔ 쓰는 법: bash run_a5.sh --reset-w0"; exit 2; }
  [ -f run/w0_check.json ] || { echo "⛔ 지울 ⓪ 기록 (run/w0_check.json) 이 없다"; exit 2; }
  if [ -e "run/${JOB}_A5" ] || [ -f run/start_point.json ] || compgen -G "run_aborted/${JOB}_*" > /dev/null; then
    echo "⛔ A5 가 이미 시작했다 — ⓪ 기록은 A5 를 띄우기 전에만 지운다"; exit 2
  fi
  log "✎ ⓪ 기록을 지운다 (A5 시작 전 · 운영자) — 이전 기록 $(tr -d '\n' < run/w0_check.json | cut -c1-400)"
  rm -f run/w0_check.json || { echo "⛔ 지우지 못했다"; exit 2; }
  echo "✓ ⓪ 기록을 지웠다 — 맞는 W0_WAVECAR (또는 none) 로 다시 돌리면 ⓪ 을 다시 확인한다"; exit 0
fi

# ── 0 스텝 인프라 중단 기록 (외주 2차 --infra-abort 와 같은 확인 · 단 이름만 a5 · 뒤 단이 있으면 거부) ──
if [ "${1:-}" = "--infra-abort" ]; then
  [ $# -ge 5 ] || { echo "⛔ 쓰는 법: [WALL_S=<초>] bash run_a5.sh --infra-abort <A5|c1|c2> <스케줄러 잡 id> <취소 UTC> <사유…>"; exit 2; }
  st=$2; sid=$(clean "$3"); when=$(clean "$4"); shift 4; why=$(clean "$*")
  case "$st" in A5|c1|c2) ;; *) echo "⛔ 모르는 단 $st"; exit 2;; esac
  src=run/${JOB}_$st
  [ -d "$src" ] || { echo "⛔ $src 가 없다"; exit 2; }
  lx=$(later5 "$st"); [ -z "$lx" ] || { echo "⛔ 뒤 단 ($lx) 이 이미 있다 — $st 의 0 스텝 중단은 뒤 단을 띄우기 전에만 기록한다 (1저자에게 알린다)"; exit 2; }
  [ -f "$src/attempt.start" ] || { echo "⛔ $src 에 시작 표지 (attempt.start) 가 없다 — 이 러너가 띄운 시도가 아니다 (연락)"; exit 2; }
  if [ -e "$src/OSZICAR" ]; then
    n=$(grep -acE '^[[:space:]]*[A-Za-z][A-Za-z ]?[A-Za-z ]?[A-Za-z ]?:' "$src/OSZICAR" 2>/dev/null); g=$?
    [ "$g" -le 1 ] && [ -n "$n" ] || { echo "⛔ $src/OSZICAR 를 읽지 못했다 (grep $g) — 0 행인지 확인할 수 없어 기록하지 않는다 (1저자)"; exit 2; }
    osz=zero_rows
  else
    n=0; osz=missing
  fi
  [ "$n" = 0 ] || { echo "⛔ 전자 반복행 $n 개 — 0 스텝 중단이 아니다 (끊긴 시도면 --killed · 실행 실패는 사다리가 다룬다)"; exit 2; }
  so=$(grep -acE '^[[:space:]]*[A-Za-z][A-Za-z ]?[A-Za-z ]?[A-Za-z ]?:[[:space:]]+[0-9]' "$src/stdout.log" 2>/dev/null); so=${so:-0}
  oi=$(grep -acE 'Iteration +[0-9]+\(' "$src/OUTCAR" 2>/dev/null); oi=${oi:-0}
  [ "$so" = 0 ] && [ "$oi" = 0 ] || { echo "⛔ OSZICAR 는 $osz 인데 stdout.log 전자 반복행 $so · OUTCAR Iteration $oi — 출력 유실이지 0 스텝이 아니다 · 기록하지 않는다"; exit 2; }
  [ -n "$sid" ] && [ -n "$when" ] && [ -n "$why" ] || { echo "⛔ 스케줄러 잡 id · 취소 시각 · 사유가 다 있어야 한다"; exit 2; }
  if [ -n "${WALL_S:-}" ]; then
    secs_ok "$WALL_S" || { echo "⛔ WALL_S '$WALL_S' — 0 이상의 10진 정수 (초 · 선행 0 없이 · 9 자리 이하) 여야 한다"; exit 2; }
    w=$WALL_S
  elif [ -f "$src/attempt.json" ]; then
    w=ATTEMPT_JSON
  else
    w=UNKNOWN
  fi
  k=$(awk -F'\t' -v j="$JOB" '$2 == j' run/infra_aborts.tsv 2>/dev/null | wc -l); k=${k:-0}
  [ "$k" -lt "$INFRA_MAX" ] || { echo "⛔ 0 스텝 중단 기록이 이미 $INFRA_MAX 회 — 상한 (1저자에게 알린다)"; exit 2; }
  mkdir -p run_aborted; dst=run_aborted/${JOB}_${st}_$((k + 1))
  mkdir "$dst" || exit 2
  shopt -s dotglob nullglob
  for f in "$src"/*; do mv "$f" "$dst/" || exit 2; done; rmdir "$src" || exit 2
  shopt -u dotglob nullglob
  rm -f "$dst/POTCAR" "$dst/WAVECAR" "$dst/CHGCAR" "$dst/CHG" "$dst/vasprun.xml" "$dst/.running"     # WAVECAR 는 복사본이다 (보존 ⓐ 원본 · A5 끝 WAVECAR 는 이 폴더 밖)
  if [ "$w" = ATTEMPT_JSON ]; then w=$(grep -o '"elapsed_s": [^,}]*[,}]' "$dst/attempt.json" | head -1 | sed 's/^"elapsed_s": //; s/[,}]$//'); secs_ok "$w" || w=UNKNOWN; fi
  printf '{"job": "%s", "rung": "%s", "sched_job_id": "%s", "cancel_utc": "%s", "reason": "%s", "wall_s": "%s", "oszicar": "%s", "recorded_utc": "%s", "recorded_s": %d}\n' \
    "$JOB" "$st" "$sid" "$when" "$why" "$w" "$osz" "$(utc)" "$(date +%s)" > "$dst/infra_abort.json"
  [ -f run/infra_aborts.tsv ] || printf "recorded_utc\tjob\trung\tsched_job_id\tcancel_utc\twall_s\treason\tdir\n" > run/infra_aborts.tsv
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$(utc)" "$JOB" "$st" "$sid" "$when" "$w" "$why" "$(basename "$dst")" >> run/infra_aborts.tsv
  if [ "$w" = UNKNOWN ]; then
    echo "✓ $src → $dst (0 스텝 인프라 중단 $((k + 1))/$INFRA_MAX) — ⚠ 벽시계 미상: 'bash run_a5.sh --infra-wall $(basename "$dst") <초>' 로 채울 때까지 다음 단이 뜨지 않는다"
  else
    echo "✓ $src → $dst (0 스텝 인프라 중단 $((k + 1))/$INFRA_MAX) — 다시 돌리면 같은 단부터"
  fi
  exit 0
fi

if [ "${1:-}" = "--infra-wall" ]; then
  [ $# -eq 3 ] || { echo "⛔ 쓰는 법: bash run_a5.sh --infra-wall <run_aborted 폴더 이름> <초>"; exit 2; }
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

# ── 전자 스텝 뒤 끊긴 시도의 벽시계 기록 (그 단 소모 · 값 없음 · 전자 반복행 ≥ 1 이어야 한다 · 뒤 단이 있으면 거부) ──
if [ "${1:-}" = "--killed" ]; then
  [ $# -ge 5 ] || { echo "⛔ 쓰는 법: WALL_S=<초> bash run_a5.sh --killed <A5|c1|c2> <스케줄러 잡 id> <취소 UTC> <사유…>"; exit 2; }
  st=$2; sid=$(clean "$3"); when=$(clean "$4"); shift 4; why=$(clean "$*")
  case "$st" in A5|c1|c2) ;; *) echo "⛔ 모르는 단 $st"; exit 2;; esac
  src=run/${JOB}_$st
  [ -f "$src/attempt.start" ] || { echo "⛔ $src 에 시작 표지 (attempt.start) 가 없다 — VASP 가 뜨지 않은 시도다"; exit 2; }
  [ ! -f "$src/attempt.json" ] || { echo "⛔ $src 는 끝난 시도다 (attempt.json 있음) — 기록하지 않는다"; exit 2; }
  [ ! -f "$src/killed.json" ] || { echo "⛔ $src 는 이미 기록했다 — 고치지 않는다"; exit 2; }
  lx=$(later5 "$st"); [ -z "$lx" ] || { echo "⛔ 뒤 단 ($lx) 이 이미 있다 — $st 의 끊김은 뒤 단을 띄우기 전에만 기록한다 (1저자에게 알린다)"; exit 2; }
  secs_ok "${WALL_S:-}" || { echo "⛔ WALL_S=<초> (스케줄러 장부의 그 시도 벽시계) 가 있어야 한다"; exit 2; }
  n=$(rows_of "$src")
  [ "$n" -ge 1 ] 2>/dev/null || { echo "⛔ $src OSZICAR 전자 반복행 0 — 0 스텝 중단이면 --infra-abort (OUTCAR 에만 반복 흔적이 있으면 출력 유실 — 연락)"; exit 2; }
  [ -n "$sid" ] && [ -n "$when" ] && [ -n "$why" ] || { echo "⛔ 스케줄러 잡 id · 취소 시각 · 사유가 다 있어야 한다"; exit 2; }
  rid=$(grep -o '"run_id": "[^"]*"' "$src/attempt.start" | head -1 | sed 's/.*: "//; s/"$//')
  printf '{"job": "%s", "rung": "%s", "run_id": "%s", "wall_s": "%s", "sched_job_id": "%s", "cancel_utc": "%s", "reason": "%s", "osz_rows": "%s", "recorded_utc": "%s", "recorded_s": %d}\n' \
    "$JOB" "$st" "$rid" "$WALL_S" "$sid" "$when" "$why" "$n" "$(utc)" "$(date +%s)" > "$src/killed.json.part" && mv -f "$src/killed.json.part" "$src/killed.json" \
    || { echo "⛔ killed.json 쓰기 실패"; exit 2; }
  log "✎ $src 끊긴 시도 벽시계 $WALL_S 초 (스케줄러 $sid · $why · 전자 반복행 $n) — 그 단 소모 · 값 없음 · 다시 돌리지 않는다"
  echo "✓ $src 벽시계 $WALL_S 초 기록 — 다시 돌리면 다음 단부터 이어 간다"; exit 0
fi

if [ "${PACK_ONLY:-0}" = 1 ]; then
  echo "pack_only $(utc)" >> run/env.txt
  if pack; then echo "✅ 포장만 다시 했다 (계산은 다시 돌리지 않았다)"; exit 0; fi
  echo "⛔ 포장 실패 — 디스크·권한을 확인한 뒤 PACK_ONLY=1 bash run_a5.sh 로 다시"; exit 4
fi

[ $# -eq 0 ] || { echo "⛔ 모르는 인자 '$1' — 계산은 인자 없이 돌린다 · 기록 명령은 --infra-abort · --infra-wall · --killed · --reset-w0 · --unlock (README)"; exit 2; }

# ── 계산 실행: 잠금을 잡는다 (같은 기계의 죽은 PID 잠금만 치운다 · 다른 기계의 잠금은 --unlock 으로만) ──
if ! mkdir "$LOCK" 2>/dev/null; then
  read -r LK_S LK_H LK_P <<< "$(lock_state)"
  case "$LK_S" in
    live|foreign) lock_say "$LK_S" "$LK_H" "$LK_P" "계산"; exit 2;;
    stale) echo "⚠ 남은 잠금 (기계 $LK_H · PID $LK_P — 이 기계 · 살아 있지 않다) — 치우고 진행"; rm -rf "$LOCK";;
  esac
  mkdir "$LOCK" 2>/dev/null || { echo "⛔ 잠금 (run/.a5.lock) 을 만들 수 없다 — 다른 실행이 막 시작했을 수 있다"; exit 2; }
fi
printf '%s %s\n' "$HOST" "$$" > "$LOCK/owner" || { rm -rf "$LOCK"; echo "⛔ 잠금 주인을 적지 못했다"; exit 2; }
trap 'rm -rf "$LOCK"' EXIT; trap 'exit 143' TERM; trap 'exit 129' HUP; trap 'exit 130' INT
# ── 끝난 사다리면 아무것도 띄우지 않는다 (리뷰 P1-1) ──
if [ -f run/final.json ]; then
  fc=$(grep -o '"code": [0-9]*' run/final.json | head -1 | grep -o '[0-9]*$')
  log "■ 다시 돌림 — 이 사다리는 이미 끝났다: $(tr -d '\n' < run/final.json | cut -c1-240)"
  echo "  아무것도 띄우지 않는다 · 보낼 것은 a5_return.tgz + .sha256 그대로 (포장만 다시: PACK_ONLY=1 bash run_a5.sh)"
  case "$fc" in 0|1|5|6|8) exit "$fc";; *) echo "⛔ run/final.json 의 코드 '$fc' 를 읽을 수 없다 — 연락"; exit 2;; esac
fi
[[ "$(up)" =~ ^[0-9]+$ ]] || { echo "⛔ /proc/uptime 을 읽을 수 없다 — 벽시계 장부는 단조 시계로 잰다 (Linux)"; exit 2; }
[ -n "${VASP_CMD:-}" ] || { echo "⛔ VASP_CMD 를 주세요 (예: mpirun -np 64 vasp_std)"; exit 2; }        # \${VAR:?} 는 1 로 끝난다 — 1 은 '값 없음' 이다 (종료 코드가 겹치지 않게)
[ -n "${POTCAR_DIR:-}" ] && [ -d "$POTCAR_DIR" ] || { echo "⛔ POTCAR_DIR 를 주세요 (PAW_PBE 폴더 · 있어야 한다: '${POTCAR_DIR:-}')"; exit 2; }
[ -n "${W0_WAVECAR:-}" ] || { echo "⛔ W0_WAVECAR 를 주세요 — 보존된 a4 ⓐ WAVECAR 경로 (외주 2차 묶음의 run/V5_s_outer_A_G4_e70_far_a4_a4/stageA/WAVECAR · 먼저 ls -l · sha256sum) · 없으면 W0_WAVECAR=none"; exit 2; }
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
{ echo "date_utc $(utc)"; echo "host $HOST"; echo "VASP_CMD $VASP_CMD"; echo "POTCAR_DIR $POTCAR_DIR"; echo "W0_WAVECAR $W0_WAVECAR"
  echo "PERF_TAGS $(printf '%s' "$PERF_LINES" | tr '\n' ';')"; echo "MANIFEST_sha256 $(h MANIFEST.sha256)"; } >> run/env.txt
[ -f run/status.tsv ] || printf "job\trung\tstage\trc\tstatus\tn_elec\tdE\tdeps\twhy\twall_s\n" > run/status.tsv
rm -rf "run/.prep_${JOB}_A5" "run/.prep_${JOB}_c1" "run/.prep_${JOB}_c2"     # 앞 실행의 남은 준비 폴더 (VASP 를 띄운 적 없음 · 잠금 아래)

# ── 누적 벽시계 (a5 의 모든 시도 · 0 스텝 중단 · 끊긴 시도 · 미상은 0 초가 아니다) ──
wall5(){ local d w tot=0 unk="" dirs=run lst
  [ -d run_aborted ] && dirs="run run_aborted"
  lst=$(find $dirs -path 'run/.prep_*' -prune -o \( -name attempt.json -o -name attempt.start -o -name infra_abort.json -o -name killed.json \) -type f -print 2>/dev/null) \
    || { echo "UNKNOWN (반송 폴더 열거 실패)"; return; }
  for d in $(printf '%s\n' "$lst" | sed 's#/[^/]*$##' | LC_ALL=C sort -u); do
    if [ -f "$d/attempt.json" ]; then w=$(grep -o '"elapsed_s": [^,}]*[,}]' "$d/attempt.json" | head -1 | sed 's/^"elapsed_s": //; s/[,}]$//')
    elif [ -f "$d/infra_abort.json" ]; then w=$(grep -o '"wall_s": "[^"]*"' "$d/infra_abort.json" | head -1 | sed 's/.*: "//; s/"$//')
    elif [ -f "$d/killed.json" ]; then w=$(grep -o '"wall_s": "[^"]*"' "$d/killed.json" | head -1 | sed 's/.*: "//; s/"$//')
    else w=""; fi
    if [[ "$w" =~ ^(0|[1-9][0-9]{0,11})$ ]]; then tot=$((tot + w)); else [ -n "$unk" ] || unk=$d; fi
  done
  if [ -n "$unk" ]; then echo "UNKNOWN $unk"; else echo "$tot"; fi
}
cap_ok(){ # → 0 띄워도 된다 · 1 누적 > 상한 · 2 벽시계 미상 · 장부 이상
  local w; w=$(wall5) || w="UNKNOWN (장부 계산 실패)"
  case "$w" in UNKNOWN*) log "⏸ 벽시계 미상 — ${w#UNKNOWN } · 다음 단을 띄우지 않는다. 0 스텝 중단이면 'bash run_a5.sh --infra-wall <폴더> <초>' · 끊긴 시도면 'WALL_S=<초> bash run_a5.sh --killed <단> …' 로 채운 뒤 다시"; return 2;; esac
  [[ "$w" =~ ^[0-9]+$ ]] || { log "⏸ 벽시계 장부가 숫자가 아니다 ('$w') — 다음 단을 띄우지 않는다 (반송하고 연락)"; return 2; }
  awk -v w="$w" -v c="$CAP_H" 'BEGIN { exit !(w <= c * 3600) }' || { log "⏸ a5 누적 $((w / 3600)) h > 상한 $CAP_H h — 다음 단을 띄우지 않는다 (1저자)"; return 1; }
  return 0
}

# ── 끝 · 멈춤 ──
fin5(){ # $1 코드 (0 · 1 · 5 상한 · 6 · 8) · $2 상태 · $3 사유 — 끝: run/final.json 을 쓰고 포장한다 (다시 돌려도 아무것도 띄우지 않는다)
  log "■ 끝 [$1 $2] $3"
  printf '{"code": %d, "state": "%s", "why": "%s", "written_utc": "%s", "written_s": %d}\n' "$1" "$2" "$(clean "$3")" "$(utc)" "$(date +%s)" > run/final.json.part \
    && mv -f run/final.json.part run/final.json || { echo "⛔ run/final.json 쓰기 실패 — 디스크를 확인한 뒤 다시 돌려 주세요 (기록에서 같은 판정을 다시 낸다)"; exit 4; }
  finish "$1"
}
stop5(){ # $1 코드 (3 · 5 · 7) · $2 사유 — 멈춤 (끝이 아니다: 기록하거나 고친 뒤 다시 돌린다 · 포장하지 않는다 · run/final.json 없음)
  log "⏸ [$1] $2"
  case "$1" in
    3) echo "⛔ 준비 실패 (종료 3) — 그 단은 소모되지 않았다. 원인을 고친 뒤 다시 돌려 주세요 (막히면 PACK_ONLY=1 로 포장해 연락)";;
    5) echo "⏸ 멈춤 (종료 5) — 위 줄의 기록 명령을 쓴 뒤 다시 돌려 주세요";;
    7) echo "⏸ 멈춤 (종료 7) — 전자 반복행 0 · 다음 단을 띄우지 않았다 (위 줄 · 막히면 PACK_ONLY=1 로 포장해 연락)";;
  esac
  exit "$1"
}
env6_pre(){ # 띄우기 전 PP sha ≠ 봉인 — 이번 실행은 아무것도 띄우지 않았다 (끝 기록 없음 · POTCAR_DIR 를 고친 경우에만 다시)
  log "⛔ 공통 환경 고장 (PP sha ≠ 봉인) — 이번 실행은 아무것도 띄우지 않았다 · 반송하고 연락 (POTCAR_DIR 를 잘못 준 경우에만 고쳐서 다시)"
  if ! pack; then echo "⛔ 반송 포장 실패 — PACK_ONLY=1 bash run_a5.sh"; exit 4; fi
  echo "⛔ 공통 환경 고장 (PP) — 반송해 주시고 연락 주세요"; exit 6
}

# ── ⓪ 보존된 a4 ⓐ WAVECAR 확인 (한 번 · 원본은 읽기만 · 경로가 없거나 못 읽으면 기록하지 않고 멈춘다 — 리뷰 P1-3) ──
w0_check(){
  local p=$W0_WAVECAR s="" z="" hd="" v=0 why=""
  if [ -f run/w0_check.json ]; then
    [ "$(grep -o '"path": "[^"]*"' run/w0_check.json | head -1 | sed 's/.*: "//; s/"$//')" = "$(clean "$p")" ] \
      || { echo "⛔ W0_WAVECAR '$p' 가 첫 기록 (run/w0_check.json) 과 다르다 — 같은 경로로 다시 돌린다 (A5 를 띄우기 전이면 'bash run_a5.sh --reset-w0' 로 기록을 지울 수 있다)"; exit 2; }
    return 0
  fi
  if [ "$p" = none ]; then why="업체가 없다고 적음 (W0_WAVECAR=none)"
  elif [ -f "$p" ] && [ -r "$p" ]; then
    s=$(h "$p"); z=$(stat -c %s "$p" 2>/dev/null); hd=$(wav_head "$p"); set -- $hd
    if [ "$s" != "$W0_SHA" ]; then why="sha256 다름"
    elif [ "$z" != "$W0_SIZE" ]; then why="크기 다름"
    elif ! { [ $# -ge 6 ] && [ "$4" = "$W0_NK" ] && [ "$5" = "$W0_NB" ] && enc_eq "$6" "$W0_EN"; }; then why="머리 (NKPTS·NBANDS·ENCUT) 다름"
    else v=1; why="-"; fi
  else
    echo "⛔ W0_WAVECAR '$p' 가 없거나 읽을 수 없다 — 기록하지 않았다. 'ls -l' · 'sha256sum' 으로 경로를 확인하고, 정말 없으면 W0_WAVECAR=none 으로 다시"; exit 2
  fi
  printf '{"path": "%s", "sha256": "%s", "size": "%s", "head": "%s", "expect": {"sha256": "%s", "size": "%s", "NKPTS": "%s", "NBANDS": "%s", "ENCUT": "%s"}, "verified": %d, "why": "%s", "checked_utc": "%s"}\n' \
    "$(clean "$p")" "$s" "$z" "$hd" "$W0_SHA" "$W0_SIZE" "$W0_NK" "$W0_NB" "$W0_EN" "$v" "$why" "$(utc)" > run/w0_check.json.part && mv -f run/w0_check.json.part run/w0_check.json \
    || { echo "⛔ run/w0_check.json 쓰기 실패"; exit 2; }
  log "⓪ 보존 ⓐ WAVECAR $( [ "$v" = 1 ] && echo '확인됨 — A5 는 그 복사본에서 이어서' || echo "확인 안 됨 ($why) — A5 는 새로 시작")"
}

# ── 한 시도 — 준비는 임시 폴더 run/.prep_<잡>_<단> 에서 하고, 다 되면 시도 폴더로 이름을 바꾼 뒤 띄운다 (준비 실패는 그 단을 소모하지 않는다 — 리뷰 P2(c)) ──
pfail(){ log "⛔ $2 — 준비 실패 · 그 단은 소모되지 않았다 (임시 폴더를 지웠다 · 원인 — 디스크 · 권한 · 경로 — 을 고친 뒤 다시)"; rm -rf "$1"; }
run_one5(){ # $1 단 (A5|c1|c2) · $2 변형 (A5c|A5f|c1|c2) · $3 시도 폴더 · $4 시작 WAVECAR (A5c · c1 · c2) · $5 그 기대 sha → 0 돌림 · 3 준비 실패 · 6 띄우기 전 PP 불일치
  local st=$1 var=$2 d=$3 wsrc=${4:-} wexp=${5:-} inc tp rid t0 t1 u0 u1 el rc j wsha="" wcp="" wend hd istart icharg nr pr hon ver rs x p
  inc=$(incar_of "$var"); tp="run/.prep_${JOB}_$st"
  pp_ok "$JOB" || return 6
  [ ! -e "$d" ] || { log "⛔ $d 가 이미 있다 — 덮어쓰지 않는다"; return 3; }
  rm -rf "$tp"; mkdir "$tp" || { log "⛔ $st 준비 폴더 ($tp) 를 만들 수 없다"; return 3; }
  { cp "jobs/$JOB/POSCAR" "jobs/$JOB/KPOINTS" "$tp/" && cp "jobs/$JOB/$inc" "$tp/INCAR"; } || { pfail "$tp" "$st 입력 복사"; return 3; }
  if [ -n "$PERF_LINES" ]; then printf '%s' "$PERF_LINES" >> "$tp/INCAR" || { pfail "$tp" "$st 성능 태그"; return 3; }; fi
  { : > "$tp/POTCAR" && : > "$tp/POTCAR.species.sha256"; } || { pfail "$tp" "$st POTCAR 시작"; return 3; }
  while read -r p; do
    [ -n "$p" ] || continue
    [ -f "$POTCAR_DIR/$p/POTCAR" ] || { pfail "$tp" "POTCAR $p 없음"; return 3; }
    { cat "$POTCAR_DIR/$p/POTCAR" >> "$tp/POTCAR" && printf "%s %s\n" "$p" "$(h "$POTCAR_DIR/$p/POTCAR")" >> "$tp/POTCAR.species.sha256"; } || { pfail "$tp" "POTCAR $p 잇기"; return 3; }
  done < "jobs/$JOB/POTCAR.spec"
  { grep -aE "TITEL|ZVAL|VRHFIN|LEXCH" "$tp/POTCAR" > "$tp/POTCAR.titel" && h "$tp/POTCAR" > "$tp/POTCAR.sha256"; } || { pfail "$tp" "$st POTCAR 기록"; return 3; }
  if [ -n "$wsrc" ]; then
    wsha=$(h "$wsrc")
    { [ -n "$wexp" ] && [ "$wsha" = "$wexp" ]; } || { pfail "$tp" "$st 시작 WAVECAR ($wsrc) sha '$wsha' ≠ 기대 '$wexp'"; return 3; }
    cp "$wsrc" "$tp/WAVECAR" || { pfail "$tp" "$st 시작 WAVECAR 복사 (디스크?)"; return 3; }
    wcp=$(h "$tp/WAVECAR")
    [ "$wcp" = "$wexp" ] || { pfail "$tp" "$st 복사한 WAVECAR sha 가 원본과 다르다"; return 3; }
  fi
  rid="$(date -u +%Y%m%dT%H%M%S)-$$-$RANDOM"; t0=$(date +%s); u0=$(up)
  printf '{"job": "%s", "attempt": "%s", "stage": "a5", "run_id": "%s", "t_start": %d, "kernel_sha256": ""}\n' "$JOB" "$var" "$rid" "$t0" > "$tp/attempt.start" \
    || { pfail "$tp" "$st 시작 표지"; return 3; }
  mv -T "$tp" "$d" || { pfail "$tp" "$st 준비 폴더를 $d 로 옮기지 못했다"; return 3; }
  touch "$d/.running"; watch5 "$d" "$JOB/$var" "$st" & local wpid=$!
  (cd "$d" && $VASP_CMD > stdout.log 2>&1); rc=$?; t1=$(date +%s); u1=$(up)
  el=$((u1 - u0)); [ "$el" -ge 0 ] 2>/dev/null || el=$(( t1 > t0 ? t1 - t0 : 0 ))
  rm -f "$d/.running"; kill "$wpid" 2>/dev/null; wait "$wpid" 2>/dev/null
  ver=$(clean "$(ver_of "$d")")
  istart=$(grep -aE '^[[:space:]]*ISTART *= *[0-9]+[[:space:]]+job' "$d/OUTCAR" 2>/dev/null | tail -1 | grep -oE 'ISTART *= *[0-9]+' | grep -oE '[0-9]+$')
  icharg=$(grep -aE '^[[:space:]]*ICHARG *= *[0-9]+[[:space:]]+charge' "$d/OUTCAR" 2>/dev/null | tail -1 | grep -oE 'ICHARG *= *[0-9]+' | grep -oE '[0-9]+$')
  nr=0; grep -aq "WAVECAR not read" "$d/stdout.log" "$d/OUTCAR" 2>/dev/null && nr=1
  pr=0; grep -aqE -e "$RESTART_RE" "$d/stdout.log" "$d/OUTCAR" 2>/dev/null && pr=1
  case "$st" in
    A5)
      hd=$(wav_head "$d/WAVECAR")
      if [ "$var" = A5c ]; then
        # A5 의 재시작 확인 = 시작 복사본 sha + 문구 (끝 sha 는 안 본다 — LWAVE T 라 새로 써진다 · 정보 · 자격 아님)
        hon=0; [ "$istart" = 1 ] && [ "$icharg" = 0 ] && [ "$nr" = 0 ] && [ "$pr" = 1 ] && [ -n "$wsha" ] && [ "$wsha" = "$wcp" ] && [ "$wcp" = "$wexp" ] && hon=1
        rs=$(printf '{"src_sha256": "%s", "copied_sha256": "%s", "istart": "%s", "icharg": "%s", "not_read_phrase": %s, "positive_regex_match": "%s", "honoured_start": %s}' \
          "$wsha" "$wcp" "${istart:-NA}" "${icharg:-NA}" "$nr" "$pr" "$hon")
      else rs=null; fi
      printf '{"sha256": "%s", "size": %s, "head": "%s", "outcar": {"NKPTS": "%s", "NBANDS": "%s", "ENCUT": "%s"}, "restart": %s}\n' "$(h "$d/WAVECAR")" \
        "$(stat -c %s "$d/WAVECAR" 2>/dev/null || echo 0)" "$hd" "$(out_num "$d" NKPTS)" "$(out_num "$d" NBANDS)" "$(out_num "$d" ENCUT)" "$rs" > "$d/WAVECAR.info";;
    c1|c2)
      wend=$(h "$d/WAVECAR")
      hon=0; [ "$istart" = 1 ] && [ "$icharg" = 0 ] && [ "$nr" = 0 ] && [ "$pr" = 1 ] && [ -n "$wsha" ] && [ "$wsha" = "$wcp" ] && [ "$wcp" = "$wend" ] && hon=1
      printf '{"src_sha256": "%s", "copied_sha256": "%s", "end_sha256": "%s", "istart": "%s", "icharg": "%s", "not_read_phrase": %s, "positive_regex_match": "%s", "honoured": %s, "start_head": "%s", "outcar": {"NKPTS": "%s", "NBANDS": "%s", "ENCUT": "%s"}}\n' \
        "$wsha" "$wcp" "$wend" "${istart:-NA}" "${icharg:-NA}" "$nr" "$pr" "$hon" "$SPH" "$(out_num "$d" NKPTS)" "$(out_num "$d" NBANDS)" "$(out_num "$d" ENCUT)" > "$d/WAVECAR.info";;
  esac
  if [ "$st" != c2 ]; then x=$(hist_max "$d"); case "$x" in ''|*[!0-9]*) ;; *) [ "$x" -gt 45 ] && echo "$(utc) $var info history_max $x" >> "$d/warn.log";; esac; fi
  printf '{"job": "%s", "attempt": "%s", "stage": "a5", "run_id": "%s", "rc": %d, "t_start": %d, "t_end": %d, "elapsed_s": %d, "vasp_version": "%s", "kernel_sha256": "", "perf": "%s", "sha256": {"INCAR": "%s", "POSCAR": "%s", "KPOINTS": "%s", "POTCAR": "%s", "OUTCAR": "%s", "OSZICAR": "%s", "WAVECAR.info": "%s", "stdout.log": "%s", "POTCAR.titel": "%s", "POTCAR.species.sha256": "%s", "attempt.start": "%s"}}\n' \
    "$JOB" "$var" "$rid" "$rc" "$t0" "$t1" "$el" "$ver" "$(printf '%s' "$PERF_LINES" | tr '\n' ';')" \
    "$(h "$d/INCAR")" "$(h "$d/POSCAR")" "$(h "$d/KPOINTS")" "$(cat "$d/POTCAR.sha256")" "$(h "$d/OUTCAR")" "$(h "$d/OSZICAR")" "$(h "$d/WAVECAR.info")" \
    "$(h "$d/stdout.log")" "$(h "$d/POTCAR.titel")" "$(h "$d/POTCAR.species.sha256")" "$(h "$d/attempt.start")" > "$d/attempt.json"
  j=$(judge5 "$d" "$st"); set -- $j
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$JOB" "$var" "a5" "$rc" "$1" "$2" "$3" "$4" "$5" "$el" >> run/status.tsv
  rm -f "$d/POTCAR" "$d/CHGCAR" "$d/CHG" "$d/vasprun.xml" "$d/vdw_kernel.bindat" "$d/LOCPOT"
  [ "$st" = A5 ] || rm -f "$d/WAVECAR"          # c1 · c2 의 WAVECAR 는 복사본 (끝 sha 를 잰 뒤 지운다) · A5 WAVECAR 는 사다리가 끝날 때까지 둔다 (반송 안 함)
  return 0
}

# ── 단의 갈래 (개정 5 해석 1 · 사용자 2026-11-20 — 러너와 검사기가 같은 순서로 본다) ──
var_of(){ grep -o '"attempt": "[^"]*"' "$1/attempt.start" 2>/dev/null | head -1 | sed 's/.*: "//; s/"$//'; }
gate5(){ # $1 시도 폴더 · $2 단 → "갈래 상태 행수 사유" (빈칸 없는 낱말 넷)
  #   NEW 띄울 차례 · WAIT5 끊김 (끝 기록 없음) · ZERO 전자 반복행 0 (멈춤 7) · ENV 다른 VASP 빌드 (끝 6) · REVIEW 1저자 (끝 8) · BAD2 이 러너가 띄운 시도가 아님 ·
  #   OK 주 기준 수렴 · NEXT 다음 단 (SCF_NOT_CONVERGED · 행 ≥ 1 실행 실패 · 행 ≥ 1 끊김 기록)
  local d=$1 st=$2 n var ver e s
  [ -e "$d" ] || { echo "NEW - 0 -"; return; }
  { [ -d "$d" ] && [ -f "$d/attempt.start" ]; } || { echo "BAD2 - 0 no_start_marker"; return; }
  var=$(var_of "$d")
  case "$st:$var" in A5:A5c|A5:A5f|c1:c1|c2:c2) ;; *) echo "BAD2 - 0 variant_${var:-none}"; return;; esac
  n=$(rows_of "$d"); ver=$(clean "$(ver_of "$d")")
  if [ -f "$d/attempt.json" ]; then
    if [ -n "$ver" ] && [ "$ver" != "$REL_VER" ]; then echo "ENV VERSION_MISMATCH $n vasp_build"; return; fi
    [ "$n" -ge 1 ] 2>/dev/null || { echo "ZERO SCF_UNVERIFIED 0 no_rows"; return; }
    e=$(echo5 "$d" "$var"); [ "$e" = "-" ] || { echo "REVIEW SETTINGS_ECHO $n $e"; return; }
    s=$(stat5 "$d" "$st" "$SS")
    case "$s" in OK) echo "OK OK $n -";; SCF_NOT_CONVERGED|RUN_FAILED) echo "NEXT $s $n -";; *) echo "REVIEW $s $n -";; esac
    return
  fi
  [ -f "$d/killed.json" ] || { echo "WAIT5 INCOMPLETE_ATTEMPT $n no_end_record"; return; }
  if [ -n "$ver" ] && [ "$ver" != "$REL_VER" ]; then echo "ENV VERSION_MISMATCH $n vasp_build"; return; fi
  [ "$n" -ge 1 ] 2>/dev/null || { echo "REVIEW KILLED_NO_ROWS 0 -"; return; }
  e=$(echo5 "$d" "$var"); [ "$e" = "-" ] || { echo "REVIEW SETTINGS_ECHO $n $e"; return; }
  echo "NEXT KILLED $n -"
}
rc_of(){ grep -o '"rc": -\{0,1\}[0-9]*' "$1/attempt.json" 2>/dev/null | head -1 | grep -o -- '-\{0,1\}[0-9]*$'; }
on_stop(){ # gate5 낱말 넷 + 단 → 멈출 갈래면 끝낸다 (돌아오면 OK · NEXT)
  local k=$1 s=$2 n=$3 why=$4 st=$5
  case "$k" in
    OK|NEXT) return 0;;
    WAIT5) stop5 5 "$st 는 시작했는데 끝 기록이 없다 (끊김 · 전자 반복행 $n) — 행 ≥ 1 이면 'WALL_S=<초> bash run_a5.sh --killed $st <스케줄러 잡 id> <취소 UTC> <사유>' · 행 0 이면 'bash run_a5.sh --infra-abort $st <잡 id> <취소 UTC> <사유>' 로 기록한 뒤 다시";;
    ZERO) stop5 7 "$st 전자 반복행 0 (rc $(rc_of "run/${JOB}_$st") · stdout.log 첫 줄: $(head -c 160 "run/${JOB}_$st/stdout.log" 2>/dev/null | head -1)) — 다음 단을 띄우지 않는다. 스케줄러 기록이 있는 0 스텝 인프라 중단이면 'bash run_a5.sh --infra-abort $st <잡 id> <취소 UTC> <사유>' 뒤 다시 (같은 단부터 · 잡 전체 $INFRA_MAX 회) · 아니면 (실행 파일 · 모듈 · 입력) 고치기 전에 연락";;
    ENV) fin5 6 ENV "$st VASP 빌드가 봉인과 다르다 — 공통 환경 고장 · 전체 정지";;
    REVIEW) fin5 8 REVIEW "$st $s ($why · 전자 반복행 $n) — 개정 5 해석 1 (사용자 2026-11-20): 재시작 미이행 · SCF 미확인 · 설정 에코 다름은 더 돌리지 않는다 → 1저자";;
    BAD2) log "⛔ $st 폴더 (run/${JOB}_$st) 는 이 러너가 띄운 시도가 아니다 ($why) — 아무것도 띄우지 않는다 · 연락"; exit 2;;
    *) log "⛔ $st 갈래 '$k' 를 모른다 — 연락"; exit 2;;
  esac
}
cap_gate(){ # $1 단 — 띄우기 전 누적 상한 (넘으면 끝 5 · 벽시계 미상이면 멈춤 5)
  cap_ok; case $? in
    0) return 0;;
    1) fin5 5 CAP "누적 상한 $CAP_H h — $1 를 띄우지 않았다 (1저자)";;
    *) stop5 5 "벽시계 미상 · 장부 이상 — '--infra-wall' 또는 '--killed' 로 채운 뒤 다시 ($1 앞)";;
  esac
}
drop5(){ rm -f "run/${JOB}_A5/WAVECAR"; }    # 사다리 끝 (0 · 1) 에서만 — A5 끝 WAVECAR 는 반송하지 않는다 · 멈춤 (3 · 5 · 7 · 8) 에서는 남긴다 (검토 · 이어 돌리기용)
info_head(){ awk '{ if (match($0, /"head": "[^"]*"/)) { print substr($0, RSTART + 9, RLENGTH - 10); exit } }' "$1" 2>/dev/null; }
info_num(){ grep -o "\"$2\": [0-9]*" "$1" 2>/dev/null | head -1 | grep -o '[0-9]*$'; }
elig5(){ # A5 자격 (개정 5 '자격 = 개정 4 ⓐ 자격의 앞 셋' — 검사기 a_eligible 과 같은 기록 대조) → 0 자격 · 1 미달 (⓪ 복사본 또는 닫음) ·
  #        2 이상 (기록은 유효한 WAVECAR 인데 파일이 사라졌거나 바뀜 → 1저자 · ⓪ 으로 넘어가지 않는다)
  local d=$1 s r c k z
  s=$(stat5 "$d" A5)
  case "$s" in OK|SCF_NOT_CONVERGED) ;; *) echo "ⓐ 상태 $s (정상 종료·유한 상태 아님)"; return 1;; esac
  for k in NKPTS NBANDS ENCUT; do
    c=$(grep -o "\"$k\": \"[^\"]*\"" "$d/WAVECAR.info" 2>/dev/null | head -1 | sed 's/.*: "//; s/"$//')
    { [ -n "$c" ] && [ "$c" = "$(out_num "$d" "$k")" ]; } || { echo "ⓐ WAVECAR.info 의 OUTCAR 사본 $k '$c' ≠ ⓐ OUTCAR 원문 '$(out_num "$d" "$k")'"; return 1; }
  done
  r=$(info_head "$d/WAVECAR.info"); set -- $r
  { [ $# -ge 6 ] && [ "$4" = "$(out_num "$d" NKPTS)" ] && [ "$5" = "$(out_num "$d" NBANDS)" ] && enc_eq "$6" "$(out_num "$d" ENCUT)"; } \
    || { echo "ⓐ WAVECAR 머리 ($r) ≠ OUTCAR NKPTS/NBANDS/ENCUT"; return 1; }
  z=$(info_num "$d/WAVECAR.info" size)
  [ "${z:-0}" -gt 0 ] 2>/dev/null || { echo "ⓐ WAVECAR 기록 크기 0"; return 1; }
  [ -s "$d/WAVECAR" ] || { echo "ⓐ 끝 WAVECAR 가 기록 (크기 $z) 뒤 없어졌다"; return 2; }
  [ "$(h "$d/WAVECAR")" = "$(wsha "$d/WAVECAR.info" sha256)" ] || { echo "ⓐ 끝 WAVECAR 가 기록 뒤 바뀌었다"; return 2; }
  return 0
}
# ── 시작점 — 첫 c 단을 띄울 때 한 번 정해 run/start_point.json 에 두고, 그 뒤로는 다시 정하지 않는다 (리뷰 P0-2(b)) ──
sp_field(){ grep -o "\"$1\": \"[^\"]*\"" run/start_point.json 2>/dev/null | head -1 | sed 's/.*: "//; s/"$//'; }
sp_load(){
  SPF=$(sp_field from); S=$(sp_field path); SS=$(sp_field sha256); SPH=$(sp_field head)
  case "$SPF" in A5) [ "$S" = "run/${JOB}_A5/WAVECAR" ] || return 1;; W0) [ "$S" = "$W0_WAVECAR" ] || return 1;; *) return 1;; esac
  [[ "$SS" =~ ^[0-9a-f]{64}$ ]] || return 1
  set -- $SPH; [ $# -ge 6 ] || return 1
  SP_NK=$4; SP_NB=$5; SP_EN=$6
}
sp_write(){
  printf '{"from": "%s", "path": "%s", "sha256": "%s", "head": "%s", "a5_why": "%s", "written_utc": "%s", "written_s": %d}\n' \
    "$SPF" "$(clean "$S")" "$SS" "$SPH" "$(clean "$SPWHY")" "$(utc)" "$(date +%s)" > run/start_point.json.part && mv -f run/start_point.json.part run/start_point.json
}

# ── 사다리 ──
log "════ W_ad a5 · $JOB ════"
pp_ok "$JOB" || env6_pre
w0_check
W0OK=0; grep -q '"verified": 1' run/w0_check.json && W0OK=1
A=run/${JOB}_A5; C1=run/${JOB}_c1; C2=run/${JOB}_c2
SS=""; SPF=""; S=""; SPH=""; SP_NK=""; SP_NB=""; SP_EN=""; SPWHY="-"
# A5
read -r gk gs gn gw <<< "$(gate5 "$A" A5)"
if [ "$gk" = NEW ]; then
  [ ! -f run/start_point.json ] && [ ! -e "$C1" ] && [ ! -e "$C2" ] || fin5 8 REVIEW "A5 가 없는데 뒤 단 기록이 있다 (시작점 · c1 · c2)"
  cap_gate A5
  if [ "$W0OK" = 1 ]; then var=A5c; ws=$W0_WAVECAR; we=$W0_SHA; else var=A5f; ws=""; we=""; fi
  log "▶ A5 ($var · LDIPOL 끔 · MAXMIX 200 · AMIX 0.1 · AMIN 0.01 · NELM 300)"
  run_one5 A5 "$var" "$A" "$ws" "$we"; r=$?
  [ "$r" = 6 ] && env6_pre
  [ "$r" = 0 ] || stop5 3 "A5 준비 실패"
  read -r gk gs gn gw <<< "$(gate5 "$A" A5)"
fi
log "A5 → $gs (전자 반복행 $gn)"
on_stop "$gk" "$gs" "$gn" "$gw" A5
# 시작점
if [ -f run/start_point.json ]; then
  sp_load || fin5 8 REVIEW "시작점 기록 (run/start_point.json) 의 형식 · 경로가 맞지 않는다"
  log "시작점 $SPF (기록 · sha $SS · 다시 정하지 않는다)"
else
  { [ ! -e "$C1" ] && [ ! -e "$C2" ]; } || fin5 8 REVIEW "c 단이 있는데 시작점 기록이 없다"
  why=$(elig5 "$A"); e=$?
  case "$e" in
    0) SPF=A5; S=$A/WAVECAR; SS=$(wsha "$A/WAVECAR.info" sha256); SPH=$(info_head "$A/WAVECAR.info");;
    2) fin5 8 REVIEW "A5 끝 WAVECAR 이상 — $why";;
    *) if [ "$W0OK" = 1 ]; then
         SPF=W0; S=$W0_WAVECAR; SS=$W0_SHA; SPH=$(info_head run/w0_check.json); SPWHY=$why
         log "A5 자격 미달 — $why · c1 · c2 시작점 = 보존 ⓐ (복사본 · 개정 5 A5_자격_미달)"
       else
         log "✗ A5 자격 미달 — $why · 보존 ⓐ 도 확인 안 됨 → 값 없음 (이 잡은 닫는다)"; drop5
         fin5 1 CLOSED "A5 자격 미달 ($why) · 보존 ⓐ 확인 안 됨 — 값 없음 (개정 5 A5_자격_미달)"
       fi;;
  esac
  set -- $SPH; SP_NK=${4:-}; SP_NB=${5:-}; SP_EN=${6:-}
fi
# c1
read -r gk gs gn gw <<< "$(gate5 "$C1" c1)"
if [ "$gk" = NEW ]; then
  [ ! -e "$C2" ] || fin5 8 REVIEW "c1 이 없는데 c2 가 있다"
  cap_gate c1
  if [ ! -f run/start_point.json ]; then
    sp_write || stop5 3 "시작점 기록 (run/start_point.json) 쓰기 실패"
    log "시작점 $SPF 를 기록했다 (sha $SS — 이 뒤로 다시 정하지 않는다)"
  fi
  log "▶ c1 (Davidson · MAXMIX 200 · AMIX 0.1 · AMIN 0.01 · NELM 400 · 시작점 $SPF)"
  run_one5 c1 c1 "$C1" "$S" "$SS"; r=$?
  [ "$r" = 6 ] && env6_pre
  [ "$r" = 0 ] || stop5 3 "c1 준비 실패"
  read -r gk gs gn gw <<< "$(gate5 "$C1" c1)"
fi
log "c1 → $gs (전자 반복행 $gn)"
on_stop "$gk" "$gs" "$gn" "$gw" c1
s1=$gs
if [ "$gk" = OK ]; then
  [ ! -e "$C2" ] || fin5 8 REVIEW "c1 이 주 기준 수렴인데 c2 가 있다"
  drop5; log "✓ c1 주 기준 수렴 — c2 를 띄우지 않는다"; fin5 0 OK "c1 주 기준 수렴"
fi
# c2
read -r gk gs gn gw <<< "$(gate5 "$C2" c2)"
if [ "$gk" = NEW ]; then
  cap_gate c2
  log "▶ c2 (ALGO All · TIME 0.1 · NELM 400 · c1 = $s1 · 시작점 $SPF 의 새 복사본)"
  run_one5 c2 c2 "$C2" "$S" "$SS"; r=$?
  [ "$r" = 6 ] && env6_pre
  [ "$r" = 0 ] || stop5 3 "c2 준비 실패"
  read -r gk gs gn gw <<< "$(gate5 "$C2" c2)"
fi
log "c2 → $gs (전자 반복행 $gn)"
on_stop "$gk" "$gs" "$gn" "$gw" c2
drop5
[ "$gk" = OK ] && fin5 0 OK "c2 주 기준 수렴"
fin5 1 NO_PRIMARY "c1 $s1 · c2 $gs — 주 기준 값 없음 (보조 기준은 반송 뒤 V5 수집기)"
