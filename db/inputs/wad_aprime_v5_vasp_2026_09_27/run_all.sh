#!/usr/bin/env bash
# =============================================================================
# run_all.sh — A′ V5 VASP 단일점 18 잡 (필요 시 잡마다 사전등록 재시도 INCAR.r1 **1 회**)
#   필수 환경변수: VASP_CMD   (예: "mpirun -np 128 vasp_std")
#                 POTCAR_DIR (PAW_PBE 폴더 — <POTCAR_DIR>/Li_sv/POTCAR · P · S · Cl · Ag)
#   선택: PERF_TAGS_FILE (NCORE/NPAR/KPAR/NSIM/LPLANE/LSCALU/LSCALAPACK 만 허용) · JOBS="잡1 잡2" (일부만 · 파일럿)
#   ⛔ INCAR·POSCAR·KPOINTS 를 고치지 마세요 — 성능 태그는 PERF_TAGS_FILE 로만. 고친 입력은 반송 검사에서 무효가 됩니다.
#   ⛔ POTCAR 는 반송하지 않습니다 (라이선스) — TITEL/ZVAL 줄과 sha256 만 남깁니다.
# =============================================================================
set -u
HERE=$(cd "$(dirname "$0")" && pwd); cd "$HERE"
: "${VASP_CMD:?VASP_CMD 를 주세요 (예: mpirun -np 128 vasp_std)}"
: "${POTCAR_DIR:?POTCAR_DIR 를 주세요 (PAW_PBE 폴더)}"
ALLOW='^[[:space:]]*(NCORE|NPAR|KPAR|NSIM|LPLANE|LSCALU|LSCALAPACK)[[:space:]]*='
sha256sum -c --quiet MANIFEST.sha256 || { echo "⛔ 패키지 파일이 MANIFEST 와 다르다 — 실행하지 않는다"; exit 2; }
if [ -n "${PERF_TAGS_FILE:-}" ]; then
  BAD=$(grep -vE '^[[:space:]]*(#|$)' "$PERF_TAGS_FILE" | grep -vE "$ALLOW" || true)
  [ -z "$BAD" ] || { echo "⛔ PERF_TAGS_FILE 에 허용 밖 태그: $BAD"; exit 2; }
fi
JOBS=${JOBS:-$(cat JOBS.txt)}
mkdir -p run
{ echo "date_utc $(date -u +%FT%TZ)"; echo "host $(hostname)"; echo "VASP_CMD $VASP_CMD"; echo "POTCAR_DIR $POTCAR_DIR";
  echo "PERF_TAGS $(grep -vE '^[[:space:]]*(#|$)' "${PERF_TAGS_FILE:-/dev/null}" 2>/dev/null | tr '\n' ';')"; } >> run/env.txt
[ -f run/status.tsv ] || printf "job\tattempt\trc\tterminated\tconverged\tn_elec_steps\tTOTEN_eV\twall_s\n" > run/status.tsv
run_one(){  # $1 잡 · $2 시도(""|r1) · $3 INCAR 파일
  local job=$1 att=$2 inc=$3 d; d=run/${job}${2:+_$2}; mkdir -p "$d"
  cp "jobs/$job/POSCAR" "jobs/$job/KPOINTS" "$d/"; cp "jobs/$job/$inc" "$d/INCAR"
  [ -n "${PERF_TAGS_FILE:-}" ] && grep -vE '^[[:space:]]*(#|$)' "$PERF_TAGS_FILE" >> "$d/INCAR"
  : > "$d/POTCAR"
  while read -r p; do [ -n "$p" ] || continue; cat "$POTCAR_DIR/$p/POTCAR" >> "$d/POTCAR" || { echo "⛔ POTCAR $p 없음"; return 3; }; done < "jobs/$job/POTCAR.spec"
  grep -E "TITEL|ZVAL|VRHFIN" "$d/POTCAR" > "$d/POTCAR.titel"; sha256sum "$d/POTCAR" | cut -d' ' -f1 > "$d/POTCAR.sha256"
  local t0 t1 rc term conv nel E; t0=$(date +%s); (cd "$d" && $VASP_CMD > stdout.log 2>&1); rc=$?; t1=$(date +%s)
  term=0; grep -q "General timing and accounting" "$d/OUTCAR" 2>/dev/null && term=1
  conv=0; grep -q "aborting loop because EDIFF is reached" "$d/OUTCAR" 2>/dev/null && conv=1
  grep -q "EDIFF was not reached" "$d/OUTCAR" 2>/dev/null && conv=0
  nel=$(grep -cE "^(DAV|RMM|CG|SDA):" "$d/OSZICAR" 2>/dev/null); nel=${nel:-0}
  E=$(grep "free  energy   TOTEN" "$d/OUTCAR" 2>/dev/null | tail -1 | awk '{print $5}')
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$job" "${att:-0}" "$rc" "$term" "$conv" "$nel" "${E:-NA}" "$((t1-t0))" >> run/status.tsv
  rm -f "$d/POTCAR" "$d/WAVECAR" "$d/CHGCAR" "$d/CHG" "$d/vasprun.xml"
  [ "$term" = 1 ] && [ "$conv" = 1 ]
}
for job in $JOBS; do
  [ -d "jobs/$job" ] || { echo "⛔ 모르는 잡 $job"; exit 2; }
  if run_one "$job" "" INCAR; then echo "✓ $job"
  else echo "… $job 미종료·미수렴 → 사전등록 재시도 1 회 (INCAR.r1: AMIX 0.1 · BMIX 0.01 · NELM 300)"
       run_one "$job" r1 INCAR.r1 && echo "✓ $job (r1)" || echo "⛔ $job r1 도 실패 — 값 없음으로 둔다 (다른 설정으로 더 돌리지 않는다)"
  fi
done
tar czf V5_vasp_return.tgz run MANIFEST.sha256 && sha256sum V5_vasp_return.tgz > V5_vasp_return.tgz.sha256
echo "✅ 끝 — V5_vasp_return.tgz 와 V5_vasp_return.tgz.sha256 을 보내 주세요"
