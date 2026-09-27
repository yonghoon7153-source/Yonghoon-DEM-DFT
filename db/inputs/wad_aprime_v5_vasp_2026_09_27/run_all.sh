#!/usr/bin/env bash
# =============================================================================
# run_all.sh (v3) — A′ V5 VASP 단일점 18 잡 · 잡마다 사전등록 재시도 INCAR.r1 최대 1 회 (최대 36 실행)
#   필수: VASP_CMD (예: "mpirun -np 128 vasp_std") · POTCAR_DIR (PAW_PBE 폴더: <POTCAR_DIR>/Li_sv/POTCAR · P · S · Cl · Ag)
#   선택: PERF_TAGS_FILE — 한 줄에 대입 하나만 · 허용 NCORE/NPAR/KPAR/NSIM (양의 정수) · LPLANE/LSCALU/LSCALAPACK (.TRUE./.FALSE.)
#         세미콜론·역슬래시·중복 태그·줄 끝 주석 금지 (VASP 는 ';' 뒤를 다른 설정으로 읽는다)
#         JOBS="잡1 잡2" (일부만 — 파일럿: JOBS="V5_s_outer_A_bound V5_s_outer_A_far")
#         PACK_ONLY=1 — 계산은 하지 않고 반송 묶음만 다시 만든다 (포장이 실패했을 때 · VASP_CMD·POTCAR_DIR 불필요)
#   ⛔ INCAR·POSCAR·KPOINTS 를 고치지 마세요 · ⛔ POTCAR 는 반송하지 않습니다 (TITEL/ZVAL 줄 · sha256 만)
#   ⛔ 시도 폴더(run/<잡>, run/<잡>_r1)가 이미 있으면 그 잡은 돌지 않습니다 (원자적 mkdir). 재시도 상한은 잡마다 사전등록 1 회 —
#      그 밖의 수동 재실행은 새 승인 없이는 하지 않습니다.
#   종료코드: 0 전 잡 성공·포장 · 1 일부 잡 실패 (반송 묶음은 만든다 — 실패도 기록) · 2 패키지·성능 파일 오류 (아무것도 안 돈다)
#             4 반송 포장 실패 (계산 결과는 run/ 에 그대로 — PACK_ONLY=1 로 포장만 다시)
# =============================================================================
set -u
HERE=$(cd "$(dirname "$0")" && pwd); cd "$HERE"
sha256sum -c --quiet MANIFEST.sha256 || { echo "⛔ 패키지 파일이 MANIFEST 와 다르다 — 실행하지 않는다"; exit 2; }
pack(){  # 임시 파일에 쓰고 성공해야 승격 — 옛 묶음과 섞이지 않게
  rm -f V5_vasp_return.tgz.part V5_vasp_return.tgz.sha256.part
  tar czf V5_vasp_return.tgz.part run MANIFEST.sha256 || return 1
  mv -f V5_vasp_return.tgz.part V5_vasp_return.tgz || return 1
  sha256sum V5_vasp_return.tgz > V5_vasp_return.tgz.sha256.part || return 1
  mv -f V5_vasp_return.tgz.sha256.part V5_vasp_return.tgz.sha256 || return 1
}
if [ "${PACK_ONLY:-0}" = 1 ]; then
  [ -d run ] || { echo "⛔ run/ 이 없다 — 포장할 것이 없다"; exit 2; }
  echo "pack_only $(date -u +%FT%TZ)" >> run/env.txt
  if pack; then echo "✅ 포장만 다시 했다 — V5_vasp_return.tgz 와 .sha256 을 보내 주세요 (계산은 다시 돌리지 않았다)"; exit 0; fi
  echo "⛔ 포장 실패 — 디스크·권한을 확인한 뒤 PACK_ONLY=1 로 다시"; exit 4
fi
: "${VASP_CMD:?VASP_CMD 를 주세요 (예: mpirun -np 128 vasp_std)}"
: "${POTCAR_DIR:?POTCAR_DIR 를 주세요 (PAW_PBE 폴더)}"
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
JOBS=${JOBS:-$(cat JOBS.txt)}
for job in $JOBS; do [ -d "jobs/$job" ] || { echo "⛔ 모르는 잡 $job"; exit 2; }; done
mkdir -p run
{ echo "date_utc $(date -u +%FT%TZ)"; echo "host $(hostname 2>/dev/null)"; echo "VASP_CMD $VASP_CMD"; echo "POTCAR_DIR $POTCAR_DIR";
  echo "PERF_TAGS $(printf '%s' "$PERF_LINES" | tr '\n' ';')"; echo "MANIFEST_sha256 $(sha256sum MANIFEST.sha256 | cut -d' ' -f1)"; } >> run/env.txt
[ -f run/status.tsv ] || printf "job\tattempt\trc\tterminated\tconverged\tn_runs\tn_elec_steps\tTOTEN_eV\twall_s\n" > run/status.tsv
h(){ sha256sum "$1" 2>/dev/null | cut -d' ' -f1; }
run_one(){  # $1 잡 · $2 시도(0|r1) · $3 INCAR 파일 → 0 성공 · 1 실행했으나 실패 (재시도 대상) · 3 준비 실패 (재시도 아님)
  local job=$1 att=$2 inc=$3 d; d=run/$job; [ "$att" = r1 ] && d=run/${job}_r1
  mkdir "$d" 2>/dev/null || { echo "⛔ $d 가 이미 있거나 만들 수 없다 — 덮어쓰지 않는다"; return 3; }
  { cp "jobs/$job/POSCAR" "jobs/$job/KPOINTS" "$d/" && cp "jobs/$job/$inc" "$d/INCAR"; } || return 3
  [ -n "$PERF_LINES" ] && printf '%s' "$PERF_LINES" >> "$d/INCAR"
  : > "$d/POTCAR"; : > "$d/POTCAR.species.sha256"
  while read -r p; do
    [ -n "$p" ] || continue
    [ -f "$POTCAR_DIR/$p/POTCAR" ] || { echo "⛔ POTCAR $p 없음"; return 3; }
    cat "$POTCAR_DIR/$p/POTCAR" >> "$d/POTCAR"; printf "%s %s\n" "$p" "$(h "$POTCAR_DIR/$p/POTCAR")" >> "$d/POTCAR.species.sha256"
  done < "jobs/$job/POTCAR.spec"
  grep -E "TITEL|ZVAL|VRHFIN|LEXCH" "$d/POTCAR" > "$d/POTCAR.titel"; h "$d/POTCAR" > "$d/POTCAR.sha256"
  local rid t0 t1 rc term conv nrun nel E
  rid="$(date -u +%Y%m%dT%H%M%S)-$$-$RANDOM"; t0=$(date +%s)
  (cd "$d" && $VASP_CMD > stdout.log 2>&1); rc=$?; t1=$(date +%s)
  term=0; grep -q "General timing and accounting" "$d/OUTCAR" 2>/dev/null && term=1
  conv=0; grep -q "aborting loop because EDIFF is reached" "$d/OUTCAR" 2>/dev/null && conv=1
  grep -q "EDIFF was not reached" "$d/OUTCAR" 2>/dev/null && conv=0
  nrun=$(grep -cE '^[[:space:]]*vasp\.[0-9]' "$d/OUTCAR" 2>/dev/null); nrun=${nrun:-0}
  nel=$(grep -cE "^(DAV|RMM|CG|SDA):" "$d/OSZICAR" 2>/dev/null); nel=${nel:-0}
  E=$(grep "free  energy   TOTEN" "$d/OUTCAR" 2>/dev/null | tail -1 | awk '{print $5}')
  printf '{"job": "%s", "attempt": "%s", "run_id": "%s", "rc": %d, "t_start": %d, "t_end": %d, "sha256": {"INCAR": "%s", "POSCAR": "%s", "KPOINTS": "%s", "POTCAR": "%s", "OUTCAR": "%s", "OSZICAR": "%s"}}\n' \
    "$job" "$att" "$rid" "$rc" "$t0" "$t1" "$(h "$d/INCAR")" "$(h "$d/POSCAR")" "$(h "$d/KPOINTS")" "$(cat "$d/POTCAR.sha256")" "$(h "$d/OUTCAR")" "$(h "$d/OSZICAR")" > "$d/attempt.json"
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$job" "$att" "$rc" "$term" "$conv" "$nrun" "$nel" "${E:-NA}" "$((t1-t0))" >> run/status.tsv
  rm -f "$d/POTCAR" "$d/WAVECAR" "$d/CHGCAR" "$d/CHG" "$d/vasprun.xml"
  [ "$rc" = 0 ] && [ "$term" = 1 ] && [ "$conv" = 1 ] && [ "$nrun" = 1 ] && return 0
  return 1
}
fail=0
for job in $JOBS; do
  run_one "$job" 0 INCAR; s=$?
  if [ "$s" = 0 ]; then echo "✓ $job"
  elif [ "$s" = 1 ]; then
    echo "… $job 실행 실패·미종료·미수렴 → 사전등록 재시도 1 회 (INCAR.r1: AMIX 0.1 · BMIX 0.01 · NELM 300)"
    if run_one "$job" r1 INCAR.r1; then echo "✓ $job (r1)"; else echo "⛔ $job r1 도 실패 — 값 없음 (다른 설정으로 더 돌리지 않는다)"; fail=1; fi
  else echo "⛔ $job 준비 실패 (기존 폴더 · 입력 · POTCAR) — 재시도 대상 아님"; fail=1; fi
done
if ! pack; then echo "⛔ 반송 포장 실패 — 계산 결과는 run/ 에 그대로 있다. 다시 돌리지 말고 PACK_ONLY=1 bash run_all.sh 로 포장만 다시"; exit 4; fi
if [ "$fail" = 0 ]; then echo "✅ 끝 — V5_vasp_return.tgz 와 .sha256 을 보내 주세요"; else echo "⚠ 일부 잡 실패 — 그대로 반송해 주세요 (실패도 기록입니다)"; fi
exit "$fail"
