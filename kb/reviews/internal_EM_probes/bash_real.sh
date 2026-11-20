set -u
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
RESTART_RE="the WAVECAR file was read successfully"
d=$1; echo "hdr_gate: $(hdr_gate "$d" "DAV|RMM")"; echo "judge5 c1: $(judge5 "$d" c1)"; echo "stat5 c1: $(stat5 "$d" c1 8a65bde238eaa088a7d6832cc74523acfd8034e27c1c37f1d62ae0162394e9d9)"; echo "stat5 c1 wrong start: $(stat5 "$d" c1 0000000000000000000000000000000000000000000000000000000000000000)"; echo "judge5 A5 on stageA: $(judge5 "$d/stageA" A5)"; echo "out_num: $(out_num "$d/stageA" NKPTS) $(out_num "$d/stageA" NBANDS) $(out_num "$d/stageA" ENCUT)"; echo "hist_max: $(hist_max "$d")"; echo "rms_jump: $(rms_jump "$d" c1)"; echo "alarms: $(alarms "$d")"
