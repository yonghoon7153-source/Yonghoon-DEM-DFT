#!/usr/bin/env bash
# 캠페인 실행 — 런마다 **np=1 직렬**, 여러 개를 **동시에** 띄운다 (MPI 효율 걱정 없음).
# 사용:  MAXJ=10 bash dem_scripts/mixer_20260921/run_all.sh
#   LMP   = LIGGGHTS 실행 파일 (기본 **lmp_serial**)   MAXJ = 동시 실행 수 (기본 = 코어 수)
#   FORCE=1 = 죽은(미완주) 런을 **처음부터** 다시 띄운다 (로그·덤프가 덮인다).  기본은 **목록만** 찍는다.
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
#
# ★★ 2026-09-22 — **완주 판정은 배너 하나로 하지 않는다.**  완주 = `Total wall time` 배너 **또는**
#   마지막 thermo step ≥ 덱의 `run` 합.  새 덱(09-21, `restart` 포함)은 마지막 `run` 을 끝내고
#   **배너 없이 죽는다** (E0 기준 런 3/3 실측 — 같은 자리, 결정론; 덤프·`settled.bin` 은 무사).
#   배너만 보던 옛 판은 그 런을 "미완주" 로 읽어 **재발사해 로그·덤프를 지웠다** — 09-22 10:2x 에
#   `E0_s49979687` 이 실제로 그렇게 됐다 (런처가 MAXJ 대기열에서 기다리다 슬롯이 비는 순간 띄웠다).
# ★★ 죽은(미완주) 런은 **자동 재발사하지 않는다** — 목록만 찍고 끝낸다.  원인을 본 뒤 `FORCE=1` 로만.
#   회귀: dem_scripts/mixer_20260921/test_launcher.sh (check_all.sh 에 배선).
#
# ★★ 2026-09-28 (Codex 3차 HBR3-08) — **고-Bo `LH_*` 런은 이 런처가 기본으로 띄우지 않는다** (건너뜀을 찍는다).
#   사전등록 docs/reviews/mixer_highbo_prereg_20260927.md §8 (D-4) = `LH_s32452843` 하나 먼저 → bin 0 스모크 통과 → 나머지 둘.
#   그런데 이 런처는 미실행 `_s*` 를 전부 돌고 스모크 결과를 읽지 않으므로 LH 덱 셋이 있으면 **셋을 한꺼번에** 띄웠다
#   (옛 §2-5 의 `MAXJ=3 run_all.sh`).  `MAXJ=1` 로도 못 막는다 — 첫 런이 끝나면 다음을 띄울 뿐 스모크 판정을 기다리지 않는다.
#   ⇒ LH 는 `launch_highbo.sh first` (첫 시드만) · `launch_highbo.sh rest <smoke.json>` (증서 확인 뒤 나머지 둘) 로만 뜬다.
#     그 런처가 `ALLOW_LH=1 ONLY="<런 이름>"` 으로 이 스크립트를 부른다 — 둘 다 있고 · 이름이 ONLY 에 있고 · 발사 전 봉인
#     (`launch_record.json`) 이 있을 때만 띄운다.  로그가 있는 LH 는 FORCE=1 로도 처음부터 다시 띄우지 않는다 (재개는 resume_all.sh).
#   ONLY = 공백으로 가른 런 이름 목록 (비어 있으면 전부 = 옛 동작).  동시 상한은 그대로 **전 런** 을 센다.
#   LH 가 아닌 런의 판정 · 발사는 한 글자도 안 바뀐다.
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="${OUT:-$ROOT/dem_scripts/mixer_20260921/runs}"
LMP="${LMP:-lmp_serial}"; MAXJ="${MAXJ:-$(nproc)}"
ONLY="${ONLY:-}"; ALLOW_LH="${ALLOW_LH:-0}"
command -v "$LMP" >/dev/null || { echo "⛔ $LMP 없음 — LMP=<실행파일> 로 지정 (권장: lmp_serial)"; exit 1; }
case "$LMP" in *lmp_auto|*lmp_mpi)
  echo "⛔ '$LMP' 는 MPI 빌드다.  이 기계에서는 직접 실행도 mpirun 도 멈춘다 (위 주석)."
  echo "   MPI 로 가려면 MPI 가 실제로 도는 기계에서 LMP=$LMP MPIOK=1 로 강제할 것."
  [ "${MPIOK:-0}" = 1 ] || exit 1;; esac
PRE=(); command -v stdbuf >/dev/null && PRE=(stdbuf -oL -eL)
echo "[실행] ${PRE[*]} $LMP  ·  런마다 1 코어 · 동시 상한 $MAXJ  ·  FORCE=${FORCE:-0}${ONLY:+  ·  ONLY=$ONLY · ALLOW_LH=$ALLOW_LH}"

tot_steps() { grep -oE '^run +[0-9]+' "$1/in.mixer" 2>/dev/null | awk '{s+=$2} END{print s+0}'; }
last_step() { grep -E '^ +[0-9]+ +[0-9]+ ' "$1/log.lmp" 2>/dev/null | tail -1 | awk '{print $1+0}'; }
#  완주 = 배너 **또는** 마지막 thermo step ≥ run 합 (배너 없이 죽는 새 덱의 종료 결함을 데이터 손실로 번역하지 않는다)
done_run() {
  local d="$1" t l; [ -f "$d/log.lmp" ] || return 1
  grep -q "Total wall time" "$d/log.lmp" && return 0
  t=$(tot_steps "$d"); l=$(last_step "$d")
  [ "${t:-0}" -gt 0 ] && [ "${l:-0}" -ge "$t" ]
}
live() { local c=0; for f in "$OUT"/*_s*/pid; do [ -f "$f" ] && kill -0 "$(cat "$f")" 2>/dev/null && c=$((c+1)); done; echo $c; }
n=0; dead=(); lh=()
for d in "$OUT"/*_s*/; do
  d="${d%/}"; nm=$(basename "$d")
  [ -f "$d/in.mixer" ] || continue
  #  ONLY — 목록 밖 런은 조용히 건너뛴다 (launch_highbo.sh 가 LH 를 한 개씩 부를 때 다른 런을 건드리지 않게)
  if [ -n "$ONLY" ]; then case " $ONLY " in *" $nm "*) ;; *) continue;; esac; fi
  if [ -f "$d/pid" ] && kill -0 "$(cat "$d/pid")" 2>/dev/null; then echo "· 이미 실행 중: $d"; continue; fi
  if done_run "$d"; then
    if grep -q "Total wall time" "$d/log.lmp"; then echo "· 완료됨: $d"
    else echo "· 완료됨 (배너 없음 — 종료 결함, 데이터 무사): $d"; fi
    continue
  fi
  if [ -f "$d/log.lmp" ] && [ "${FORCE:-0}" != 1 ]; then
    echo "⚠ 죽은 런(미완주) — 자동 재발사 안 함 (원인 확인 뒤 FORCE=1 로만): $d"; dead+=("$d"); continue
  fi
  #  ★ LH 관문 (2026-09-28, Codex 3차 HBR3-08) — 여기 온 LH 는 '띄울 차례' 인 것뿐이다 (실행 중 · 완주 · 죽은 런의 판정과
  #    목록은 위에서 그대로 찍힌다).  launch_highbo.sh 가 부를 때 (ALLOW_LH=1 + ONLY 에 이름) 만, 봉인이 있을 때만 띄운다.
  case "$nm" in LH_*)
    if [ -f "$d/log.lmp" ]; then        #  FORCE=1 로 온 죽은 LH — 처음부터 다시 돌리면 로그 · 덤프가 덮인다
      echo "· LH 건너뜀 (로그 있음 — LH 는 처음부터 다시 띄우지 않는다 · 재개는 resume_all.sh): $d"; lh+=("$d"); continue
    fi
    if [ "$ALLOW_LH" != 1 ] || [ -z "$ONLY" ]; then
      echo "· LH 건너뜀 (고-Bo — 첫 시드 → bin 0 스모크 → 나머지 둘 · launch_highbo.sh 로만): $d"; lh+=("$d"); continue
    fi
    [ -s "$d/launch_record.json" ] || {
      echo "⛔ $nm: 발사 전 봉인 (launch_record.json) 이 없다 — LH 는 launch_highbo.sh 가 봉인한 뒤에만 뜬다.  중단"; exit 1; };;
  esac
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
if [ ${#dead[@]} -gt 0 ]; then
  echo "⚠ 미완주(죽은) 런 ${#dead[@]} 개 — 로그 꼬리를 본 뒤 FORCE=1 로만 재발사 (로그·덤프가 덮인다):"
  printf '   %s\n' "${dead[@]}"
fi
if [ ${#lh[@]} -gt 0 ]; then
  echo "ℹ LH (고-Bo) 런 ${#lh[@]} 개는 이 런처로 띄우지 않았다 — 사전등록 §8 (D-4) 순서 (Codex 3차 HBR3-08):"
  printf '   %s\n' "${lh[@]}"
  echo "   ① bash dem_scripts/mixer_20260921/launch_highbo.sh first               (LH_s32452843 하나)"
  echo "   ② bin 0 스모크 증서 뒤  bash dem_scripts/mixer_20260921/launch_highbo.sh rest <smoke.json>   (나머지 둘)"
fi
exit 0
