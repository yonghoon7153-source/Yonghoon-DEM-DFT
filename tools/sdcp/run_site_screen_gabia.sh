#!/usr/bin/env bash
# run_site_screen_gabia.sh — 자리 선호·자세 스크리닝을 gabia 에서 단계별로 돌린다.
#   프로토콜: kb/methodology/site_preference_protocol_2026_08_11.md
#
#   bash tools/sdcp/run_site_screen_gabia.sh fetch    # 0단계: 입력 회수 (SDCP 기체상 2종 + 0.85 기하)
#   bash tools/sdcp/run_site_screen_gabia.sh gate085  # 0.5단계: 0.85 재스캔 자세 전수 게이트 (새 계산 0)
#   bash tools/sdcp/run_site_screen_gabia.sh atlas    # 1단계: 자세 아틀라스 (GPU 불필요)
#   bash tools/sdcp/run_site_screen_gabia.sh rigid    # 2단계: UMA rigid SP
#   bash tools/sdcp/run_site_screen_gabia.sh relax    # 3단계: UMA relax (freeze 1.0 · 0.85)
#   bash tools/sdcp/run_site_screen_gabia.sh verdict  # 4단계: 판정표
#   bash tools/sdcp/run_site_screen_gabia.sh watch    # 진행 상황
set -euo pipefail

REPO="${REPO:-$HOME/Yonghoon-DEM-DFT}"
RUN="${RUN:-/data/work/runs/sdcp_v4_sitescreen}"
#   NOTE 2026-08-11 — 실제 경로 확인됨 (첫 실행에서 find 가 찾아냄)
MOLDIR="${MOLDIR:-/data/work/runs/sdcp_linio2_binding/inputs/sdcp_v7c}"
TOP1FREE="${TOP1FREE:-/data/work/runs/sdcp_v2/phaseA_top1free}"
LOG="$RUN/logs"; mkdir -p "$LOG"
SS="python3 $REPO/tools/sdcp/site_screen.py"
STAGE="${1:-}"

guard() {                      # CLAUDE.md — pw.x 와 UMA 동시 실행 금지
  if pgrep -fa 'pw\.x' >/dev/null 2>&1; then
    echo "⛔ pw.x 가 돌고 있다. nvidia-smi 로 확인하고 끝난 뒤에 다시."; nvidia-smi || true; exit 1
  fi
  # pgrep -fc 는 0건일 때 "0" 을 찍고 exit 1 을 낸다 — `|| echo 0` 을 붙이면 "0\n0" 이 돼
  # [ 가 깨진다(2026-08-11 실측). 출력만 받고 exit 는 무시한다.
  # 실행 **전**이므로 python 쪽 score 프로세스는 0개여야 한다 (python 내부 가드는 자기 자신을
  # 세므로 >1 을 본다 — 기준이 다른 게 맞다). 패턴은 python 프로세스만 잡도록 좁힌다.
  local n; n=$(pgrep -fc 'python.*site_screen\.py score' 2>/dev/null || true); n=${n:-0}
  if [ "$n" -gt 0 ] 2>/dev/null; then
    echo "⛔ score 가 이미 돌고 있다 (중복 실행 방지):"; pgrep -fa 'python.*site_screen\.py score' || true
    exit 1
  fi
  nvidia-smi --query-gpu=name,memory.used,memory.total --format=csv,noheader || true
}

# set -euo pipefail 아래에서 `cmd | head` 는 SIGPIPE 로 파이프라인을 실패시킨다.
# 진단용 출력에만 쓰는 안전 래퍼.
peek() { "$@" 2>/dev/null | head -"${PEEK_N:-20}" || true; }

case "$STAGE" in
fetch)
  echo "── 0단계: 입력 회수 ─────────────────────────────────────"
  # (a) SDCP 기체상 ORCA 기하 2종 — 못 찾으면 find 결과를 **실제로 복사**한다
  for m in neutral doped; do
    src="$MOLDIR/sdcp_v7c_$m.xyz"
    if [ ! -f "$src" ]; then
      echo "· $src 없음 — find 로 찾는다"
      src=$(find /data/work -name "sdcp_v7c_${m}.xyz" -not -path '*/\.*' 2>/dev/null | head -1 || true)
    fi
    if [ -n "$src" ] && [ -f "$src" ]; then
      cp -v "$src" "$REPO/db/structures/sdcp_v7c_$m.xyz"
    else
      echo "⛔ sdcp_v7c_$m.xyz 를 못 찾았다 — **없다**(판정 아님). 수동 탐색 필요"
    fi
  done
  # (b) freeze 0.85 (phaseA_top1free) 챔피언 기하 — VASP 단일점이 실제로 쓴 자세
  for p in doped_sulfonate_down_r0_g20 neutral_sulfonate_down_r180_g22; do
    f="$TOP1FREE/complex_$p.xyz"
    if [ -f "$f" ]; then cp -v "$f" "$REPO/db/structures/sdcp_pose_f085_$p.xyz"
    else echo "⚠ 없다: $f"; fi
  done
  echo; echo "· $TOP1FREE 자세 수: $(ls "$TOP1FREE"/complex_*.xyz 2>/dev/null | wc -l)"
  echo; echo "── 검증 ──"; cd "$REPO"; $SS inputs || true
  echo; echo "★ sha256 (프로토콜에 고정할 값):"
  sha256sum "$REPO"/db/structures/sdcp_v7c_{neutral,doped}.xyz 2>/dev/null || true
  echo; echo "→ 다음: bash tools/sdcp/run_site_screen_gabia.sh atlas"
  ;;

# 0.85 재스캔 자세 **전체**를 게이트에 통과시켜 'Ni 접촉이 있는 자세가 있었나'를 본다.
# 새 계산 0 — 이미 있는 파일만 읽는다.
gate085)
  cd "$REPO"
  # 추출검사 대조군: 스캔이 **출발점으로 쓴 바로 그 슬랩**이면 변위 판정이 그대로 성립한다.
  # (같은 구속으로 이완한 깨끗한 슬랩은 에너지 기준에 필요하지, 변위 기하 판정에는 이걸로 충분.)
  CLEAN=$(ls "$TOP1FREE"/slab*relax*.vasp "$TOP1FREE"/slab*.vasp 2>/dev/null | head -1 || true)
  [ -z "$CLEAN" ] && CLEAN="$REPO/db/structures/linio2_104_sym_1x4L4_relaxed.vasp"
  echo "· 추출검사 대조 슬랩: $CLEAN"
  ECSV=$(ls "$TOP1FREE"/phaseA_v7c_results.csv "$TOP1FREE"/*results*.csv 2>/dev/null | head -1 || true)
  [ -n "$ECSV" ] && echo "· 레거시 에너지표: $ECSV" || echo "· 에너지표 없음 → 게이트만 (판정 불가)"
  for t in doped neutral; do
    echo "═══ $t ═══"
    $SS gate "$TOP1FREE" --frag "sdcp_$t" --glob "complex_${t}_*.xyz" --relaxed \
        ${CLEAN:+--clean "$CLEAN"} ${ECSV:+--csv "$ECSV"} --json "$LOG/gate085_$t.json" \
        > "$LOG/gate085_$t.txt" 2>&1
    tail -4 "$LOG/gate085_$t.txt"
  done
  echo; echo "── Ni 접촉이 있는 자세 요약 ──"
  python3 - "$LOG"/gate085_*.json <<'PY'
import json, sys
for p in sys.argv[1:]:
    rows = json.load(open(p))
    ni = [r for r in rows if r.get("d_Ni_A") is not None]
    ok = [r for r in rows if r.get("ranking_eligible")]
    print(f"{p.split('/')[-1]}: 자세 {len(rows)} · 게이트통과 {len(ok)} · **Ni 접촉 있는 자세 {len(ni)}**")
    from collections import Counter
    print("   게이트 탈락 사유:", dict(Counter(x.split('(')[0] for r in rows for x in r['gate_reasons'])) or "없음")
    print("   최근접 양이온 분포(통과분):", dict(Counter(r.get('nearest_cation') for r in ok)))
    ne = sum(1 for r in rows if r.get('E_pose_eV') is not None)
    print(f"   에너지 붙은 자세 {ne}/{len(rows)}")
PY
  echo; echo "── 자리 판정 (레거시 0.85 스캔, 짝 아님·분포 비교) ──"
  $SS verdict "$LOG/gate085_doped.json" "$LOG/gate085_neutral.json" 2>&1 | tee "$LOG/verdict085.txt"
  ;;

atlas)
  cd "$REPO"
  # ⚠ `$SS inputs` 는 조각이 없으면 exit 2 를 낸다(의도된 검사). set -e 아래에서 그대로 두면
  #   여기서 스크립트가 통째로 죽어 atlas 가 안 돈다(2026-08-11 실측). 진단은 진단으로만 쓴다.
  $SS inputs   2>&1 | tee "$LOG/inputs.txt"   || true
  $SS sites    2>&1 | tee "$LOG/sites.txt"    || true
  $SS selftest 2>&1 | tee "$LOG/selftest.txt" || true
  $SS atlas --out "$RUN" 2>&1 | tee "$LOG/atlas.txt"
  echo; echo "→ 다음: bash tools/sdcp/run_site_screen_gabia.sh rigid"
  ;;

rigid)
  guard; cd "$REPO"
  nohup $SS score --out "$RUN" --stage rigid --task "${TASK:-omat}" \
        > "$LOG/rigid_${TASK:-omat}.log" 2>&1 &
  echo "PID $! · tail -f $LOG/rigid_${TASK:-omat}.log"
  ;;

relax)
  guard; cd "$REPO"
  nohup $SS score --out "$RUN" --stage relax --task "${TASK:-omat}" \
        --freeze 1.0 0.85 --top-per-site 2 --pairs 5 \
        > "$LOG/relax_${TASK:-omat}.log" 2>&1 &
  echo "PID $! · tail -f $LOG/relax_${TASK:-omat}.log"
  ;;

verdict)
  cd "$REPO"
  for f in sdcp_neutral sdcp_doped ptfe_dimer ptfe_c10; do
    for ff in 1.00 0.85; do
      d="$RUN/$f/relax_f$ff"
      [ -d "$d" ] || continue
      echo "═══ $f · freeze $ff ═══"
      $SS verdict "$d"
    done
  done | tee "$LOG/verdict.txt"
  ;;

watch)
  echo "RUN=$RUN"
  # grep -vc 도 0건이면 exit 1 이라 `|| echo 0` 을 붙이면 "0\n0" 이 된다 — 출력만 받는다.
  count() { local n; n=$(ls "$1"/*.json 2>/dev/null | grep -vc '_references' 2>/dev/null || true); echo "${n:-0}"; }
  for f in sdcp_neutral sdcp_doped ptfe_dimer ptfe_c10; do
    a=$(ls "$RUN/$f"/*.xyz 2>/dev/null | wc -l)
    printf '  %-14s atlas %4s · rigid %4s' "$f" "$a" "$(count "$RUN/$f/rigid")"
    for ff in 1.00 0.85; do printf ' · relax@%s %3s' "$ff" "$(count "$RUN/$f/relax_f$ff")"; done
    echo
  done
  pgrep -fa 'site_screen.py score' || echo "  (score 미실행)"
  tail -3 "$LOG"/rigid_*.log "$LOG"/relax_*.log 2>/dev/null || true
  nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader || true
  ;;

*)
  sed -n '2,10p' "$0"; exit 1;;
esac
