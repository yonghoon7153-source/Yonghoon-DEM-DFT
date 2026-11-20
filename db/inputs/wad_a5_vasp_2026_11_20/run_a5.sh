#!/usr/bin/env bash
# =============================================================================
# run_a5.sh (W_ad V5 개정 5 · a5) — 은 쪽 G4 ENCUT 650 분리 끝점 한 잡 (V5_s_outer_A_G4_e70_far_a5) 의 결과 뒤 재시도 · 사다리 ⓪ → A5 → c1 → (c2)
#   ⓪ 보존된 a4 ⓐ WAVECAR 확인 (W0_WAVECAR · sha · 크기 · 머리 — 원본은 읽기만 · 복사본만 쓴다)
#   A5 LDIPOL 끔 (⓪ 이 확인되면 그 복사본에서 이어서 · 아니면 새로) → c1 (Davidson · MAXMIX 200) → c1 이 주 기준 수렴이 아니면 c2 (ALGO All · TIME 0.1)
#   SCF 판정 = OSZICAR 마지막 전자 반복행 (검사기와 같은 계약 · 외주 2차 judge() 그대로) + 단마다 행 머리 관문 (A5 · c1 = DAV/RMM · c2 = SDA/CGA)
#   필수: VASP_CMD · POTCAR_DIR (PAW_PBE: <POTCAR_DIR>/{Li_sv,P,S,Cl,Ag}/POTCAR) · W0_WAVECAR (보존 ⓐ WAVECAR 경로 — 없으면 W0_WAVECAR=none 을 적는다)
#   선택: PERF_TAGS_FILE (한 줄에 대입 하나 · NCORE/NPAR/KPAR/NSIM 양의 정수 · LPLANE/LSCALU/LSCALAPACK) · PACK_ONLY=1 · WATCH_S (경보 점검 초 · 기본 60)
#   0 스텝 인프라 중단 (전자 반복행 0 · 스케줄러 기록이 있을 때만 · 잡 전체 2 회):
#     [WALL_S=<초>] bash run_a5.sh --infra-abort <A5|c1|c2> <스케줄러 잡 id> <취소 UTC> <사유…>   → run_aborted/ 로 옮긴다 · 다시 돌리면 같은 단부터
#     bash run_a5.sh --infra-wall <run_aborted 폴더 이름> <초>   (벽시계가 미상일 때만)
#   전자 스텝 뒤 러너째 끊긴 시도 (attempt.json 없음 · 다시 돌리지 않는다 · 그 단 소모): WALL_S=<초> bash run_a5.sh --killed <A5|c1|c2> <스케줄러 잡 id> <취소 UTC> <사유…>
#   ⛔ INCAR·POSCAR·KPOINTS 를 고치지 마세요 · 시도 폴더가 있으면 덮어쓰지 않습니다 (다시 돌리면 기록을 다시 판정해 다음 단을 정합니다)
#   종료: 0 c1 또는 c2 주 기준 수렴 · 1 주 기준 값 없음 (묶음 만듦 — 실패도 기록 · 보조 기준은 반송 뒤 우리가 본다) · 2 패키지·환경·인자 오류
#         4 포장 실패 (PACK_ONLY=1 로 다시) · 5 누적 상한 180 h 또는 벽시계 미상 (다음 단을 띄우지 않음) · 6 공통 환경 고장 (VASP 빌드 · PP — 전체 정지)
#   보내는 것: 종료 0·1·5·6 뒤 `sha256sum -c a5_return.tgz.sha256` 까지 통과한 쌍
#   지원 환경: Linux · bash ≥ 4 · GNU coreutils (find sort grep cmp sha256sum od stat) · GNU tar · awk (mawk/gawk) · sed -E
# =============================================================================
set -u
HERE=$(cd "$(dirname "$0")" && pwd); cd "$HERE"
sha256sum -c --quiet MANIFEST.sha256 || { echo "⛔ 패키지 파일이 MANIFEST 와 다르다 — 실행하지 않는다"; exit 2; }
RET_ALLOW='OUTCAR|OSZICAR|INCAR|KPOINTS|POSCAR|IBZKPT|POTCAR\.titel|POTCAR\.sha256|POTCAR\.species\.sha256|attempt\.json|stdout\.log|WAVECAR\.info|warn\.log|infra_abort\.json|LOCPOT\.zavg\.txt|attempt\.start|killed\.json'
RET_FORBID='POTCAR|WAVECAR|CHGCAR|CHG|vasprun\.xml|vdw_kernel\.bindat|LOCPOT'
JOB=V5_s_outer_A_G4_e70_far_a5
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
  grep -E "^(run|run_aborted)/[^/]+/(stageA/)?($RET_ALLOW)$" "$T/found" > "$T/allowed"; g=$?
  [ "$g" -le 1 ] || { pack_fail "허용 목록 필터 오류 ($g)"; return 1; }
  LC_ALL=C sort "$T/allowed" > "$T/sorted" || { pack_fail "정렬 실패"; return 1; }
  : > "$T/mgmt" || { pack_fail "관리 목록 초기화 실패"; return 1; }
  n_mg=0
  for f in run/env.txt run/status.tsv run/infra_aborts.tsv run/w0_check.json; do
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
elig5(){ # ⓐ 자격 (ⓑ 를 띄우기 전 — ① 정상 종료·유한 상태 ② 유효 WAVECAR: 머리 = ⓐ OUTCAR 원문 NKPTS·NBANDS·ENCUT · WAVECAR.info 의 OUTCAR 사본 = 원문
  #         (검사기 a_eligible 과 같다) ③ 기록 sha = 지금 WAVECAR · 복사본 sha 는 run_one 이 ⓑ 기록에 남기고 재시작 확인이 본다)
  local d=$1 s r c k
  s=$(stat5 "$d" A5)
  case "$s" in OK|SCF_NOT_CONVERGED) ;; *) echo "ⓐ 상태 $s (정상 종료·유한 상태 아님)"; return 1;; esac
  [ -s "$d/WAVECAR" ] || { echo "ⓐ WAVECAR 없음·빈 파일"; return 1; }
  for k in NKPTS NBANDS ENCUT; do
    c=$(grep -o "\"$k\": \"[^\"]*\"" "$d/WAVECAR.info" 2>/dev/null | head -1 | sed 's/.*: "//; s/"$//')
    [ -n "$c" ] && [ "$c" = "$(out_num "$d" "$k")" ] || { echo "ⓐ WAVECAR.info 의 OUTCAR 사본 $k '$c' ≠ ⓐ OUTCAR 원문 '$(out_num "$d" "$k")'"; return 1; }
  done
  r=$(awk '{ if (match($0, /"head": "[^"]*"/)) print substr($0, RSTART + 9, RLENGTH - 10) }' "$d/WAVECAR.info"); set -- $r
  [ $# -ge 6 ] && [ "$4" = "$(out_num "$d" NKPTS)" ] && [ "$5" = "$(out_num "$d" NBANDS)" ] && \
    enc_eq "$6" "$(out_num "$d" ENCUT)" || { echo "ⓐ WAVECAR 머리 ($r) ≠ OUTCAR NKPTS/NBANDS/ENCUT"; return 1; }
  [ "$(h "$d/WAVECAR")" = "$(wsha "$d/WAVECAR.info" sha256)" ] || { echo "ⓐ WAVECAR 가 기록 뒤 바뀌었다"; return 1; }
  return 0
}

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
# ── 중복 실행 막기 — 잠금 폴더 run/.a5.lock (원자적 mkdir) 에 PID · 살아 있는 실행이 있으면 계산 · 기록 · 포장 명령을 다 거부한다 ──
lock_live(){ local op; op=$(cat run/.a5.lock/pid 2>/dev/null); [ -n "$op" ] && kill -0 "$op" 2>/dev/null; }
if lock_live; then
  case "${1:-}" in --infra-abort|--infra-wall|--killed) echo "⛔ run_a5.sh (PID $(cat run/.a5.lock/pid)) 가 돌고 있다 — 기록 명령은 그 실행이 끝난 뒤에"; exit 2;; esac
  [ "${PACK_ONLY:-0}" = 1 ] && { echo "⛔ run_a5.sh (PID $(cat run/.a5.lock/pid)) 가 돌고 있다 — 포장은 그 실행이 끝난 뒤에"; exit 2; }
fi

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
stat5(){ # $1 시도 폴더 · $2 단 · $3 시작 WAVECAR sha (c1 · c2) → 상태 (c1 · c2 는 재시작 확인 먼저 · A5 는 재시작이 자격이 아니다)
  local d=$1 j
  [ -f "$d/attempt.json" ] || { echo INCOMPLETE_ATTEMPT; return; }
  case "$2" in c1|c2)
    { grep -q '"honoured": 1' "$d/WAVECAR.info" 2>/dev/null && [ -n "${3:-}" ] && [ "$(wsha "$d/WAVECAR.info" src_sha256)" = "$3" ] \
      && [ "$(wsha "$d/WAVECAR.info" copied_sha256)" = "$3" ] && [ "$(wsha "$d/WAVECAR.info" end_sha256)" = "$3" ] \
      && grep -aqE -e "$RESTART_RE" "$d/stdout.log" "$d/OUTCAR" 2>/dev/null; } || { echo RESTART_NOT_HONOURED; return; };;
  esac
  j=$(judge5 "$d" "$2"); echo "${j%% *}"
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

# ── 0 스텝 인프라 중단 기록 (외주 2차 --infra-abort 와 같은 확인 · 단 이름만 a5) ──
if [ "${1:-}" = "--infra-abort" ]; then
  [ $# -ge 5 ] || { echo "⛔ 쓰는 법: [WALL_S=<초>] bash run_a5.sh --infra-abort <A5|c1|c2> <스케줄러 잡 id> <취소 UTC> <사유…>"; exit 2; }
  st=$2; sid=$(clean "$3"); when=$(clean "$4"); shift 4; why=$(clean "$*")
  case "$st" in A5|c1|c2) ;; *) echo "⛔ 모르는 단 $st"; exit 2;; esac
  src=run/${JOB}_$st
  [ -d "$src" ] || { echo "⛔ $src 가 없다"; exit 2; }
  if [ -e "$src/OSZICAR" ]; then
    n=$(grep -acE '^[[:space:]]*[A-Za-z][A-Za-z ]?[A-Za-z ]?[A-Za-z ]?:' "$src/OSZICAR" 2>/dev/null); g=$?
    [ "$g" -le 1 ] && [ -n "$n" ] || { echo "⛔ $src/OSZICAR 를 읽지 못했다 (grep $g) — 0 행인지 확인할 수 없어 기록하지 않는다 (1저자)"; exit 2; }
    osz=zero_rows
  else
    n=0; osz=missing
  fi
  [ "$n" = 0 ] || { echo "⛔ 전자 반복행 $n 개 — 0 스텝 중단이 아니다 (실행 실패는 사다리가 다룬다)"; exit 2; }
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
  rm -f "$dst/POTCAR" "$dst/WAVECAR" "$dst/CHGCAR" "$dst/CHG" "$dst/vasprun.xml" "$dst/.running"     # WAVECAR 는 복사본이다 (보존 ⓐ 원본은 run/ 밖)
  if [ "$w" = ATTEMPT_JSON ]; then w=$(grep -o '"elapsed_s": [^,}]*[,}]' "$dst/attempt.json" | head -1 | sed 's/^"elapsed_s": //; s/[,}]$//'); secs_ok "$w" || w=UNKNOWN; fi
  printf '{"job": "%s", "rung": "%s", "sched_job_id": "%s", "cancel_utc": "%s", "reason": "%s", "wall_s": "%s", "oszicar": "%s", "recorded_utc": "%s"}\n' \
    "$JOB" "$st" "$sid" "$when" "$why" "$w" "$osz" "$(utc)" > "$dst/infra_abort.json"
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

# ── 전자 스텝 뒤 끊긴 시도의 벽시계 기록 (외주 2차 --killed 와 같은 확인 · 그 단 소모 · 값 없음) ──
if [ "${1:-}" = "--killed" ]; then
  [ $# -ge 5 ] || { echo "⛔ 쓰는 법: WALL_S=<초> bash run_a5.sh --killed <A5|c1|c2> <스케줄러 잡 id> <취소 UTC> <사유…>"; exit 2; }
  st=$2; sid=$(clean "$3"); when=$(clean "$4"); shift 4; why=$(clean "$*")
  case "$st" in A5|c1|c2) ;; *) echo "⛔ 모르는 단 $st"; exit 2;; esac
  src=run/${JOB}_$st
  [ -f "$src/attempt.start" ] || { echo "⛔ $src 에 시작 표지 (attempt.start) 가 없다 — VASP 가 뜨지 않은 시도다"; exit 2; }
  [ ! -f "$src/attempt.json" ] || { echo "⛔ $src 는 끝난 시도다 (attempt.json 있음) — 기록하지 않는다"; exit 2; }
  [ ! -f "$src/killed.json" ] || { echo "⛔ $src 는 이미 기록했다 — 고치지 않는다"; exit 2; }
  secs_ok "${WALL_S:-}" || { echo "⛔ WALL_S=<초> (스케줄러 장부의 그 시도 벽시계) 가 있어야 한다"; exit 2; }
  n=$(grep -acE '^[[:space:]]*[A-Za-z][A-Za-z ]?[A-Za-z ]?[A-Za-z ]?:' "$src/OSZICAR" 2>/dev/null); oi=$(grep -acE 'Iteration +[0-9]+\(' "$src/OUTCAR" 2>/dev/null)
  [ "${n:-0}" != 0 ] || [ "${oi:-0}" != 0 ] || { echo "⛔ $src 에 전자 반복 흔적이 없다 — 0 스텝 중단이면 --infra-abort 로 기록한다 (같은 단을 다시 돈다)"; exit 2; }
  [ -n "$sid" ] && [ -n "$when" ] && [ -n "$why" ] || { echo "⛔ 스케줄러 잡 id · 취소 시각 · 사유가 다 있어야 한다"; exit 2; }
  rid=$(grep -o '"run_id": "[^"]*"' "$src/attempt.start" | head -1 | sed 's/.*: "//; s/"$//')
  printf '{"job": "%s", "rung": "%s", "run_id": "%s", "wall_s": "%s", "sched_job_id": "%s", "cancel_utc": "%s", "reason": "%s", "osz_rows": "%s", "recorded_utc": "%s"}\n' \
    "$JOB" "$st" "$rid" "$WALL_S" "$sid" "$when" "$why" "${n:-0}" "$(utc)" > "$src/killed.json.part" && mv -f "$src/killed.json.part" "$src/killed.json" \
    || { echo "⛔ killed.json 쓰기 실패"; exit 2; }
  log "✎ $src 끊긴 시도 벽시계 $WALL_S 초 (스케줄러 $sid · $why) — 그 단 소모 · 값 없음 · 다시 돌리지 않는다"
  echo "✓ $src 벽시계 $WALL_S 초 기록 — 다시 돌리면 다음 단부터 이어 간다"; exit 0
fi

if [ "${PACK_ONLY:-0}" = 1 ]; then
  echo "pack_only $(utc)" >> run/env.txt
  if pack; then echo "✅ 포장만 다시 했다 (계산은 다시 돌리지 않았다)"; exit 0; fi
  echo "⛔ 포장 실패 — 디스크·권한을 확인한 뒤 PACK_ONLY=1 bash run_a5.sh 로 다시"; exit 4
fi

if ! mkdir run/.a5.lock 2>/dev/null; then
  if lock_live; then echo "⛔ 다른 run_a5.sh (PID $(cat run/.a5.lock/pid 2>/dev/null)) 가 이 묶음에서 돌고 있다 — 두 번 띄우지 않는다"; exit 2; fi
  echo "⚠ 남은 잠금 (PID $(cat run/.a5.lock/pid 2>/dev/null || echo ?) 가 살아 있지 않다) — 치우고 진행"; rm -rf run/.a5.lock
  mkdir run/.a5.lock 2>/dev/null || { echo "⛔ 잠금 (run/.a5.lock) 을 만들 수 없다 — 다른 실행이 막 시작했을 수 있다"; exit 2; }
fi
echo $$ > run/.a5.lock/pid; trap 'rm -rf run/.a5.lock' EXIT
[[ "$(up)" =~ ^[0-9]+$ ]] || { echo "⛔ /proc/uptime 을 읽을 수 없다 — 벽시계 장부는 단조 시계로 잰다 (Linux)"; exit 2; }
: "${VASP_CMD:?VASP_CMD 를 주세요 (예: mpirun -np 64 vasp_std)}"
: "${POTCAR_DIR:?POTCAR_DIR 를 주세요 (PAW_PBE 폴더)}"
: "${W0_WAVECAR:?W0_WAVECAR 를 주세요 — 보존된 a4 ⓐ WAVECAR 경로 (외주 2차 묶음의 run/V5_s_outer_A_G4_e70_far_a4_a4/stageA/WAVECAR) · 없으면 W0_WAVECAR=none}"
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
{ echo "date_utc $(utc)"; echo "host $(hostname 2>/dev/null)"; echo "VASP_CMD $VASP_CMD"; echo "POTCAR_DIR $POTCAR_DIR"; echo "W0_WAVECAR $W0_WAVECAR"
  echo "PERF_TAGS $(printf '%s' "$PERF_LINES" | tr '\n' ';')"; echo "MANIFEST_sha256 $(h MANIFEST.sha256)"; } >> run/env.txt
[ -f run/status.tsv ] || printf "job\trung\tstage\trc\tstatus\tn_elec\tdE\tdeps\twhy\twall_s\n" > run/status.tsv

# ── 누적 벽시계 (a5 의 모든 시도 · 0 스텝 중단 · 끊긴 시도 · 미상은 0 초가 아니다) ──
wall5(){ local d w tot=0 unk="" dirs=run lst
  [ -d run_aborted ] && dirs="run run_aborted"
  lst=$(find $dirs \( -name attempt.json -o -name attempt.start -o -name infra_abort.json -o -name killed.json \) -type f 2>/dev/null) || { echo "UNKNOWN (반송 폴더 열거 실패)"; return; }
  for d in $(printf '%s\n' "$lst" | sed 's#/[^/]*$##' | LC_ALL=C sort -u); do
    if [ -f "$d/attempt.json" ]; then w=$(grep -o '"elapsed_s": [^,}]*[,}]' "$d/attempt.json" | head -1 | sed 's/^"elapsed_s": //; s/[,}]$//')
    elif [ -f "$d/infra_abort.json" ]; then w=$(grep -o '"wall_s": "[^"]*"' "$d/infra_abort.json" | head -1 | sed 's/.*: "//; s/"$//')
    elif [ -f "$d/killed.json" ]; then w=$(grep -o '"wall_s": "[^"]*"' "$d/killed.json" | head -1 | sed 's/.*: "//; s/"$//')
    else w=""; fi
    if [[ "$w" =~ ^(0|[1-9][0-9]{0,11})$ ]]; then tot=$((tot + w)); else [ -n "$unk" ] || unk=$d; fi
  done
  if [ -n "$unk" ]; then echo "UNKNOWN $unk"; else echo "$tot"; fi
}
cap_ok(){ # → 0 이면 다음 단을 띄워도 된다 (누적 ≤ 상한 · 벽시계 미상이면 안 띄운다)
  local w; w=$(wall5) || w="UNKNOWN (장부 계산 실패)"
  case "$w" in UNKNOWN*) log "⏸ 벽시계 미상 — ${w#UNKNOWN } · 다음 단을 띄우지 않는다. 0 스텝 중단이면 'bash run_a5.sh --infra-wall <폴더> <초>' · 끊긴 시도면 'WALL_S=<초> bash run_a5.sh --killed <단> …' 로 채운 뒤 다시"; return 1;; esac
  [[ "$w" =~ ^[0-9]+$ ]] || { log "⏸ 벽시계 장부가 숫자가 아니다 ('$w') — 다음 단을 띄우지 않는다 (반송하고 연락)"; return 1; }
  awk -v w="$w" -v c="$CAP_H" 'BEGIN { exit !(w <= c * 3600) }' || { log "⏸ a5 누적 $((w / 3600)) h > 상한 $CAP_H h — 다음 단을 띄우지 않는다 (1저자)"; return 1; }
  return 0
}

# ── ⓪ 보존된 a4 ⓐ WAVECAR 확인 (한 번 · 원본은 읽기만) ──
w0_check(){
  local p=$W0_WAVECAR s="" z="" hd="" v=0 why=""
  if [ -f run/w0_check.json ]; then
    [ "$(grep -o '"path": "[^"]*"' run/w0_check.json | head -1 | sed 's/.*: "//; s/"$//')" = "$(clean "$p")" ] \
      || { echo "⛔ W0_WAVECAR '$p' 가 첫 기록 (run/w0_check.json) 과 다르다 — 같은 경로로 다시 돌린다"; exit 2; }
    return 0
  fi
  if [ "$p" = none ]; then why="업체가 없다고 적음 (W0_WAVECAR=none)"
  elif [ -f "$p" ] && [ -r "$p" ]; then
    s=$(h "$p"); z=$(stat -c %s "$p" 2>/dev/null); hd=$(wav_head "$p"); set -- $hd
    if [ "$s" != "$W0_SHA" ]; then why="sha256 다름"
    elif [ "$z" != "$W0_SIZE" ]; then why="크기 다름"
    elif ! { [ $# -ge 6 ] && [ "$4" = "$W0_NK" ] && [ "$5" = "$W0_NB" ] && enc_eq "$6" "$W0_EN"; }; then why="머리 (NKPTS·NBANDS·ENCUT) 다름"
    else v=1; why="-"; fi
  else why="파일이 없거나 읽을 수 없다"; fi
  printf '{"path": "%s", "sha256": "%s", "size": "%s", "head": "%s", "expect": {"sha256": "%s", "size": "%s", "NKPTS": "%s", "NBANDS": "%s", "ENCUT": "%s"}, "verified": %d, "why": "%s", "checked_utc": "%s"}\n' \
    "$(clean "$p")" "$s" "$z" "$hd" "$W0_SHA" "$W0_SIZE" "$W0_NK" "$W0_NB" "$W0_EN" "$v" "$why" "$(utc)" > run/w0_check.json.part && mv -f run/w0_check.json.part run/w0_check.json \
    || { echo "⛔ run/w0_check.json 쓰기 실패"; exit 2; }
  log "⓪ 보존 ⓐ WAVECAR $( [ "$v" = 1 ] && echo '확인됨 — A5 는 그 복사본에서 이어서' || echo "확인 안 됨 ($why) — A5 는 새로 시작")"
}

# ── 한 시도 (외주 2차 run_one 과 같은 기록 꼴 · 단 이름 · 시작 WAVECAR 대조만 a5) ──
run_one5(){ # $1 단 (A5|c1|c2) · $2 변형 (A5c|A5f|c1|c2) · $3 시도 폴더 · $4 시작 WAVECAR (A5c · c1 · c2) · $5 그 기대 sha → 0 돌림 · 3 준비 실패 · 6 공통 환경 고장
  local st=$1 var=$2 d=$3 wsrc=${4:-} wexp=${5:-} inc rid t0 t1 u0 u1 el rc j wsha="" wcp="" wend hd istart icharg nr pr hon ver rs x
  inc=$(incar_of "$var")
  pp_ok "$JOB" || return 6
  mkdir "$d" 2>/dev/null || { echo "⛔ $d 가 이미 있거나 만들 수 없다 — 덮어쓰지 않는다"; return 3; }
  { cp "jobs/$JOB/POSCAR" "jobs/$JOB/KPOINTS" "$d/" && cp "jobs/$JOB/$inc" "$d/INCAR"; } || return 3
  [ -n "$PERF_LINES" ] && printf '%s' "$PERF_LINES" >> "$d/INCAR"
  : > "$d/POTCAR"; : > "$d/POTCAR.species.sha256"
  while read -r p; do
    [ -n "$p" ] || continue
    [ -f "$POTCAR_DIR/$p/POTCAR" ] || { echo "⛔ POTCAR $p 없음"; rm -f "$d/POTCAR"; return 3; }
    cat "$POTCAR_DIR/$p/POTCAR" >> "$d/POTCAR"; printf "%s %s\n" "$p" "$(h "$POTCAR_DIR/$p/POTCAR")" >> "$d/POTCAR.species.sha256"
  done < "jobs/$JOB/POTCAR.spec"
  grep -aE "TITEL|ZVAL|VRHFIN|LEXCH" "$d/POTCAR" > "$d/POTCAR.titel"; h "$d/POTCAR" > "$d/POTCAR.sha256"
  if [ -n "$wsrc" ]; then
    wsha=$(h "$wsrc")
    [ -n "$wexp" ] && [ "$wsha" = "$wexp" ] || { log "⛔ $st 시작 WAVECAR sha '$wsha' ≠ 기대 '$wexp' — 띄우지 않는다"; return 3; }
    cp "$wsrc" "$d/WAVECAR" || return 3
    wcp=$(h "$d/WAVECAR")
    [ "$wcp" = "$wexp" ] || { log "⛔ $st 복사한 WAVECAR sha 가 원본과 다르다 — 띄우지 않는다"; rm -f "$d/WAVECAR"; return 3; }
  fi
  rid="$(date -u +%Y%m%dT%H%M%S)-$$-$RANDOM"; t0=$(date +%s); u0=$(up)
  printf '{"job": "%s", "attempt": "%s", "stage": "a5", "run_id": "%s", "t_start": %d, "kernel_sha256": ""}\n' "$JOB" "$var" "$rid" "$t0" > "$d/attempt.start" || return 3
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
      printf '{"src_sha256": "%s", "copied_sha256": "%s", "end_sha256": "%s", "istart": "%s", "icharg": "%s", "not_read_phrase": %s, "positive_regex_match": "%s", "honoured": %s}\n' \
        "$wsha" "$wcp" "$wend" "${istart:-NA}" "${icharg:-NA}" "$nr" "$pr" "$hon" > "$d/WAVECAR.info";;
  esac
  if [ "$st" != c2 ]; then x=$(hist_max "$d"); case "$x" in ''|*[!0-9]*) ;; *) [ "$x" -gt 45 ] && echo "$(utc) $var info history_max $x" >> "$d/warn.log";; esac; fi
  printf '{"job": "%s", "attempt": "%s", "stage": "a5", "run_id": "%s", "rc": %d, "t_start": %d, "t_end": %d, "elapsed_s": %d, "vasp_version": "%s", "kernel_sha256": "", "perf": "%s", "sha256": {"INCAR": "%s", "POSCAR": "%s", "KPOINTS": "%s", "POTCAR": "%s", "OUTCAR": "%s", "OSZICAR": "%s", "WAVECAR.info": "%s", "stdout.log": "%s", "POTCAR.titel": "%s", "POTCAR.species.sha256": "%s", "attempt.start": "%s"}}\n' \
    "$JOB" "$var" "$rid" "$rc" "$t0" "$t1" "$el" "$ver" "$(printf '%s' "$PERF_LINES" | tr '\n' ';')" \
    "$(h "$d/INCAR")" "$(h "$d/POSCAR")" "$(h "$d/KPOINTS")" "$(cat "$d/POTCAR.sha256")" "$(h "$d/OUTCAR")" "$(h "$d/OSZICAR")" "$(h "$d/WAVECAR.info")" \
    "$(h "$d/stdout.log")" "$(h "$d/POTCAR.titel")" "$(h "$d/POTCAR.species.sha256")" "$(h "$d/attempt.start")" > "$d/attempt.json"
  j=$(judge5 "$d" "$st"); set -- $j
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$JOB" "$var" "a5" "$rc" "$1" "$2" "$3" "$4" "$5" "$el" >> run/status.tsv
  rm -f "$d/POTCAR" "$d/CHGCAR" "$d/CHG" "$d/vasprun.xml" "$d/vdw_kernel.bindat" "$d/LOCPOT"
  [ "$st" = A5 ] || rm -f "$d/WAVECAR"          # c1 · c2 의 WAVECAR 는 복사본 (끝 sha 를 잰 뒤 지운다) · A5 WAVECAR 는 잡이 끝날 때까지 둔다 (반송 안 함)
  if [ -n "$ver" ] && [ "$ver" != "$REL_VER" ]; then log "⛔ $var VASP 빌드 '$ver' ≠ 봉인 — 공통 환경 고장 · 전체 정지"; return 6; fi
  return 0
}
done5(){ [ -f "$1/attempt.json" ] || [ -f "$1/killed.json" ]; }      # 끝난 시도 (값이 있든 없든 그 단을 소모했다)
drop5(){ # $1 마지막 상태 — A5 WAVECAR 는 잡이 **끝난** 상태에서만 지운다 (검토·이어 돌리기용 상태면 남긴다 · 반송은 안 한다)
  case "$1" in INCOMPLETE_ATTEMPT|RESTART_NOT_HONOURED|SCF_UNVERIFIED|PREP_FAILED) log "… run/${JOB}_A5/WAVECAR 를 남긴다 ($1 — 검토·이어 돌리기용)";;
    *) rm -f "run/${JOB}_A5/WAVECAR";; esac
}
stage_gate(){ # $1 시도 폴더 · $2 단 → 0 이면 이미 끝난 시도 (다시 안 띄움) · 1 이면 새로 띄울 차례 · 그 밖은 멈춤 (끝 코드 출력)
  local d=$1
  [ -d "$d" ] || return 1
  done5 "$d" && return 0
  if [ -f "$d/attempt.start" ]; then log "⏸ $2 는 시작했는데 끝 기록이 없다 (끊김) — 'WALL_S=<초> bash run_a5.sh --killed $2 <스케줄러 잡 id> <취소 UTC> <사유>' 로 기록한 뒤 다시 (0 스텝이면 --infra-abort)"; finish 5; fi
  log "✗ $2 폴더는 있는데 VASP 를 띄운 흔적이 없다 (준비 실패) — 반송하고 연락"; drop5 PREP_FAILED; finish 1
}

# ── 사다리 ──
log "════ W_ad a5 · $JOB ════"
w0_check
W0OK=0; grep -q '"verified": 1' run/w0_check.json && W0OK=1
A=run/${JOB}_A5; C1=run/${JOB}_c1; C2=run/${JOB}_c2
if ! stage_gate "$A" A5; then
  cap_ok || finish 5
  if [ "$W0OK" = 1 ]; then var=A5c; ws=$W0_WAVECAR; we=$W0_SHA; else var=A5f; ws=""; we=""; fi
  log "▶ A5 ($var · LDIPOL 끔 · MAXMIX 200)"
  run_one5 A5 "$var" "$A" "$ws" "$we"; r=$?
  [ "$r" = 6 ] && finish 6
  [ "$r" = 0 ] || { log "✗ A5 준비 실패 — 반송하고 연락"; finish 1; }
fi
if why=$(elig5 "$A"); then S=$A/WAVECAR; SS=$(wsha "$A/WAVECAR.info" sha256); START=A5
elif [ "$W0OK" = 1 ]; then S=$W0_WAVECAR; SS=$W0_SHA; START=W0; log "A5 자격 미달 — $why · c1 · c2 시작점 = 보존 ⓐ (복사본)"
else log "✗ A5 자격 미달 — $why · 보존 ⓐ 도 확인 안 됨 → 값 없음 (이 잡은 닫는다)"; drop5 STAGE_A_INELIGIBLE; finish 1; fi
log "시작점 $START (sha $SS)"
if ! stage_gate "$C1" c1; then
  cap_ok || finish 5
  log "▶ c1 (Davidson · MAXMIX 200 · AMIX 0.1 · AMIN 0.01 · NELM 400 · 시작점 $START)"
  run_one5 c1 c1 "$C1" "$S" "$SS"; r=$?
  [ "$r" = 6 ] && finish 6
  [ "$r" = 0 ] || { log "✗ c1 준비 실패 — 반송하고 연락"; drop5 PREP_FAILED; finish 1; }
fi
s1=$(stat5 "$C1" c1 "$SS"); log "c1 → $s1"
if [ "$s1" = OK ]; then drop5 OK; log "✓ c1 주 기준 수렴 — c2 를 띄우지 않는다"; finish 0; fi
if ! stage_gate "$C2" c2; then
  cap_ok || finish 5
  log "▶ c2 (ALGO All · TIME 0.1 · NELM 400 · c1 = $s1 · 시작점 $START 의 새 복사본)"
  run_one5 c2 c2 "$C2" "$S" "$SS"; r=$?
  [ "$r" = 6 ] && finish 6
  [ "$r" = 0 ] || { log "✗ c2 준비 실패 — 반송하고 연락"; drop5 PREP_FAILED; finish 1; }
fi
s2=$(stat5 "$C2" c2 "$SS"); log "c2 → $s2"
drop5 "$s2"
[ "$s2" = OK ] && finish 0
finish 1
