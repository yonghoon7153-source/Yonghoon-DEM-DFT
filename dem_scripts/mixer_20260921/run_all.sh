#!/usr/bin/env bash
# 캠페인 실행 — 런마다 **np=1 직렬**, 여러 개를 **동시에** 띄운다 (MPI 효율 걱정 없음).
# 사용:  MAXJ=10 bash dem_scripts/mixer_20260921/run_all.sh
#   LMP  = LIGGGHTS 실행 파일 (기본 **lmp_serial**)   MAXJ = 동시 실행 수 (기본 = 코어 수)
#
# ★★ **기본은 `lmp_serial` (STUBS 직렬 빌드)** 이다 — 1저자 WSL 에서 믹서 대조쌍을 실제로 돌린
#   바이너리가 이것이다 (`docs/reviews/mixing_model_design_20260919.md` §13: *"lmp_serial, STUBS 직렬"*).
#   런마다 1 코어 · 여러 개를 **동시에** 띄운다 = "serial 로 동시에" (1저자 지시 2026-09-21).
# ⛔ **`lmp_auto`(MPI 빌드)를 쓰지 말 것.**  2026-09-21 실측: `mpirun` 없이 직접 실행하면
#   `MPI_Init` 무한 대기(CPU 0 % · RSS 19.8 MB · sleeping · 로그 0 바이트 — 2026-08-25
#   `oat_sweep/run_all.sh` §16 과 같은 증상), 그리고 **이 WSL 에서는 `mpirun -np 1` 도 같이 멈춘다**
#   (mpirun 자체가 CPU 0 · RSS 13 MB · 20 분).  ⇒ 이 기계에서 MPI 경로는 쓸 수 없다.
# ⚠ 로그를 파일로 보내면 stdio 가 4 KB 블록 버퍼를 써서 **살아 있어도 로그가 비어 보인다**
#   ⇒ `stdbuf -oL -eL` 로 줄 단위로 흘린다.
# ⚠ 정지는 **PID 로만**: kill $(cat runs/<런>/pid)   — pkill -f 금지 (규약)
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="${OUT:-$ROOT/dem_scripts/mixer_20260921/runs}"
LMP="${LMP:-lmp_serial}"; MAXJ="${MAXJ:-$(nproc)}"
command -v "$LMP" >/dev/null || { echo "⛔ $LMP 없음 — LMP=<실행파일> 로 지정 (권장: lmp_serial)"; exit 1; }
case "$LMP" in *lmp_auto|*lmp_mpi)
  echo "⛔ '$LMP' 는 MPI 빌드다.  이 기계에서는 직접 실행도 mpirun 도 멈춘다 (위 주석)."
  echo "   MPI 로 가려면 MPI 가 실제로 도는 기계에서 LMP=$LMP MPIOK=1 로 강제할 것."
  [ "${MPIOK:-0}" = 1 ] || exit 1;; esac
PRE=(); command -v stdbuf >/dev/null && PRE=(stdbuf -oL -eL)
echo "[실행] ${PRE[*]} $LMP  ·  런마다 1 코어 · 동시 상한 $MAXJ"

live() { local c=0; for f in "$OUT"/*_s*/pid; do [ -f "$f" ] && kill -0 "$(cat "$f")" 2>/dev/null && c=$((c+1)); done; echo $c; }
n=0
for d in "$OUT"/*_s*/; do
  [ -f "$d/in.mixer" ] || continue
  if [ -f "$d/pid" ] && kill -0 "$(cat "$d/pid")" 2>/dev/null; then echo "· 이미 실행 중: $d"; continue; fi
  if [ -f "$d/log.lmp" ] && grep -q "Total wall time" "$d/log.lmp"; then echo "· 완료됨: $d"; continue; fi
  #  ★ 동시 상한 — pid 파일 + kill -0 로 **살아 있는 lmp 만** 센다 (리뷰 R-14: `jobs -rp` 는 서브셸이
  #    바로 끝나 무효였다)
  while [ "$(live)" -ge "$MAXJ" ]; do sleep 30; done
  #  ⛔ 옛 판: `( cd "$d" && setsid … & echo $! > pid )` — `&` 가 **`cd && …` 전체**에 걸려
  #     `echo` 가 **cd 이전 디렉터리**에서 실행됐다.  런처 cwd 의 `pid` 를 덮어쓰고 런별 `pid` 는
  #     안 생겨 `live()` 가 항상 0 → **MAXJ 가 무효**였다 (적대 리뷰 MIX-CX-01 실측: MAXJ=1 인데 중첩).
  #  ⇒ cd 를 분리하고, 래퍼가 **자기 PID 를 먼저 적은 뒤 exec** 한다 ⇒ `pid` = 실제 계산 PID.
  ( cd "$d" || exit 1
    setsid nohup bash -c 'echo $$ > pid; exec "$@"' _ "${PRE[@]}" "$LMP" -in in.mixer \
        > log.lmp 2>&1 < /dev/null &
  )
  for _ in 1 2 3 4 5; do [ -s "$d/pid" ] && break; sleep 1; done
  [ -s "$d/pid" ] || { echo "⛔ $(basename "$d"): pid 파일이 안 생겼다 — 중단"; exit 1; }
  n=$((n+1)); echo "▶ 시작 $(basename "$d")  pid $(cat "$d/pid")  (동시 $(live)/$MAXJ)"
  sleep 2
done
echo "런처 종료 — 시작한 런 $n 개.  진행은 watch.sh"
