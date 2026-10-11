#!/usr/bin/env bash
# =============================================================================
# run_r2_after_pause_gabia.sh — 탄성 13_m 정지가 끝나고 GPU 가 비면 Li3Nd P0-2 control r2 를 잇는다 (2026-10-11)
#
# 사용자 10-11: '13m bfgs 뜨면 잠정 stop하고 li3nd 로 넘어가자' · '대신 resume 잘 걸려야돼'
#
# 순서 (어긋나면 r2 를 걸지 않고 끝낸다)
#   ① 정지 로그 (tools/elastic/pause_relax_at_bfgs.sh 의 tee) 에 '✅ 러너' 가 뜰 때까지 기다린다 · '⛔' 가 뜨면 끝
#   ② 새 판정 (tools/sei/restart_qe_relax.sh · stopped 갈래 e6941d4) 으로 r2 가 '사람이 세움 … restart' 인지 본다
#      — 수렴·from_scratch 면 걸지 않는다 (40 스텝을 버리지 않는다)
#   ③ GPU 에 계산 프로세스가 **하나도 없는** 상태가 EMPTY_N 번 연속일 때까지 기다린다
#      (li2s 대조 담금질 seed5 UMA 가 끝나야 한다 — gabia GPU pw.x ↔ UMA 동시 금지 · 예외 없음)
#   ④ r2 의 .bfgs 지문을 찍고 드라이버 `--run <r2>` 를 건다 (BFGS 이력 승계 · 한 번에 하나)
#
# ⛔ 못 하는 것: r3·r1 은 안 건다 (r2 만) · 탄성 재개는 안 한다 · 물리 판정 없음
#   bash run_r2_after_pause_gabia.sh <worktree> <r2 폴더> <정지 로그>
#   bash run_r2_after_pause_gabia.sh --selftest
# =============================================================================
set -uo pipefail
POLL=${POLL:-60}; EMPTY_N=${EMPTY_N:-2}; NVSMI=${NVSMI:-nvidia-smi}
WAIT1_MAX=${WAIT1_MAX:-28800}   # ① 정지 로그 상한 8 h (BFGS 한 스텝 ≈ 65 분 + 정지 도구 상한 4 h + EXIT 뒤 2 h) — 넘으면 정지 도구가 조용히 죽은 것
WAIT3_MAX=${WAIT3_MAX:-86400}   # ③ GPU 빔 상한 24 h (seed5 남은 ≈ 4 h) — 넘으면 다른 잡이 GPU 를 쥔 것 · 걸지 않는다
ts(){ date '+%F %T'; }; say(){ echo "[$(ts)] $*"; }

main(){
  local W=$1 R2=$2 L=$3 DRV=${DRIVER:-$1/tools/sei/restart_qe_relax.sh} j n f
  [ -d "$R2" ] && [ -f "$DRV" ] || { say "⛔ r2 폴더 또는 드라이버가 없다 ($R2 · $DRV)"; return 2; }
  say "① 정지 로그를 기다린다: $L"
  local t1; t1=$(date +%s)
  until grep -q '✅ 러너' "$L" 2>/dev/null; do
    grep -q '⛔' "$L" 2>/dev/null && { say "⛔ 탄성 정지가 실패로 끝났다 — r2 를 걸지 않는다"; grep '⛔' "$L" | tail -2; return 1; }
    [ $(( $(date +%s) - t1 )) -gt "$WAIT1_MAX" ] && { say "⛔ ${WAIT1_MAX} s 동안 정지 로그에 끝이 없다 — 정지 도구가 조용히 죽었을 수 있다 · r2 를 걸지 않는다"; return 3; }
    sleep "$POLL"
  done
  say "② 탄성 정지 확인 — r2 판정"
  j=$(bash "$DRV" "$R2" 2>&1 | grep -a "$(basename "$R2")")
  echo "   $j"
  case "$j" in
    *"사람이 세움"*restart*) ;;
    *) say "⛔ r2 가 '사람이 세움 → restart' 가 아니다 — 걸지 않는다 (수렴이면 분석으로 · from_scratch 면 사람이 본다)"; return 2 ;;
  esac
  say "③ GPU 가 빌 때까지 기다린다 (계산 프로세스 0 개 × ${EMPTY_N} 번 연속 · ${POLL} s 간격)"
  n=0; local t3; t3=$(date +%s)
  while [ "$n" -lt "$EMPTY_N" ]; do
    [ $(( $(date +%s) - t3 )) -gt "$WAIT3_MAX" ] && { say "⛔ ${WAIT3_MAX} s 동안 GPU 가 안 비었다 — 다른 잡이 쥐고 있다 · r2 를 걸지 않는다"; "$NVSMI" --query-compute-apps=pid,process_name,used_memory --format=csv,noheader 2>/dev/null | head -3; return 4; }
    if [ -z "$("$NVSMI" --query-compute-apps=pid --format=csv,noheader 2>/dev/null | tr -d '[:space:]')" ]; then n=$((n+1)); else n=0; fi
    [ "$n" -lt "$EMPTY_N" ] && sleep "$POLL"
  done
  f=$(find "$R2" -maxdepth 3 -name '*.bfgs' ! -path '*PAUSED*' 2>/dev/null | head -1)
  say "④ GPU 빔 — r2 재개 · .bfgs ${f:-없음} $( [ -n "$f" ] && sha256sum "$f" | cut -c1-8)"
  bash "$DRV" --run "$R2"
}

if [ "${1:-}" = "--selftest" ]; then
  T=$(mktemp -d); ok=0; bad=0
  ck(){ if [ "$2" = "$3" ]; then echo "  ⭕ $1"; ok=$((ok+1)); else echo "  ⛔ $1 — 얻음 '$2' · 기대 '$3'"; bad=$((bad+1)); fi; }
  mkdir -p "$T/w/tools/sei" "$T/r2/tmp"; echo b > "$T/r2/tmp/x.bfgs"
  # 가짜 드라이버: 판정 줄은 $T/judge 내용 · --run 이면 $T/ran 에 기록
  cat > "$T/w/tools/sei/restart_qe_relax.sh" <<EOF
#!/bin/bash
if [ "\$1" = --run ]; then echo run >> "$T/ran"; exit 0; fi
echo "  \$(cat "$T/judge") $T/r2"
EOF
  # 가짜 nvidia-smi: $T/busy 의 숫자만큼 'pid' 를 내고 하나씩 줄인다
  cat > "$T/nvsmi" <<EOF
#!/bin/bash
k=\$(cat "$T/busy"); if [ "\$k" -gt 0 ]; then echo 12345; echo \$((k-1)) > "$T/busy"; fi
EOF
  chmod +x "$T/nvsmi"
  go(){ rm -f "$T/ran"; ( POLL=0.1 EMPTY_N=2 WAIT1_MAX=${W1:-5} WAIT3_MAX=${W3:-5} NVSMI="$T/nvsmi" main "$T/w" "$T/r2" "$T/log" ) > "$T/out" 2>&1; echo $?; }
  ran(){ [ -f "$T/ran" ] && wc -l < "$T/ran" | tr -d ' ' || echo 0; }
  # 양성: 정지 성공 · 세운 잡 restart · GPU 3 번 바쁜 뒤 빔
  echo "[x] ✅ 러너 1 종료" > "$T/log"; echo "⏸ r2 사람이 세움(EXIT·max_seconds) → nstep 200 · restart (BFGS 이력 승계)" > "$T/judge"; echo 3 > "$T/busy"
  ck "양성: rc 0" "$(go)" 0
  ck "양성: --run 한 번" "$(ran)" 1
  ck "⛔음성: GPU 가 바쁜 동안은 안 걸었다 (busy 를 다 소진한 뒤)" "$(cat "$T/busy")" 0
  # ⛔ 정지 실패 로그 → 안 건다
  echo "[x] ⛔ 러너 상태가 T 가 아니다" > "$T/log"; echo 0 > "$T/busy"
  ck "⛔음성: 정지 실패면 rc 1" "$(go)" 1
  ck "⛔음성: 정지 실패면 --run 없음" "$(ran)" 0
  # ⛔ r2 가 수렴으로 판정되면 안 건다
  echo "[x] ✅ 러너 1 종료" > "$T/log"; echo "✅ r2 수렴 — 건드리지 않는다" > "$T/judge"
  ck "⛔음성: 수렴 판정이면 rc 2" "$(go)" 2
  ck "⛔음성: 수렴 판정이면 --run 없음" "$(ran)" 0
  # ⛔ 세운 잡인데 from_scratch 면 안 건다 (save 없음 → 40 스텝을 버리게 된다)
  echo "⏸ r2 사람이 세움(EXIT·max_seconds) → nstep 200 · from_scratch (BFGS 이력 승계)" > "$T/judge"
  ck "⛔음성: from_scratch 면 rc 2" "$(go)" 2
  ck "⛔음성: from_scratch 면 --run 없음" "$(ran)" 0
  # ⛔ 정지 로그가 끝없이 비면 상한에서 끝낸다 (정지 도구가 조용히 죽은 경우)
  : > "$T/log"; echo "⏸ r2 사람이 세움(EXIT·max_seconds) → nstep 200 · restart (BFGS 이력 승계)" > "$T/judge"
  ck "⛔음성: 정지 로그에 끝이 없으면 상한에서 rc 3" "$(W1=1 go)" 3
  ck "⛔음성: 그때 --run 없음" "$(ran)" 0
  # ⛔ GPU 가 상한 안에 안 비면 안 건다
  echo "[x] ✅ 러너 1 종료" > "$T/log"; echo 100000 > "$T/busy"
  ck "⛔음성: GPU 가 계속 바쁘면 상한에서 rc 4" "$(W3=1 go)" 4
  ck "⛔음성: 그때 --run 없음" "$(ran)" 0
  rm -rf "$T"
  echo "  selftest: ⭕ $ok · ⛔ $bad"; [ "$bad" = 0 ] && exit 0 || exit 1
fi

[ $# -eq 3 ] || { sed -n '2,20p' "$0"; exit 2; }
main "$@"
