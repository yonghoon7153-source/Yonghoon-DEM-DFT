#!/usr/bin/env bash
# run_uma_kgy.sh — 도펀트 자리 비교 1 단계: 후보 UMA 어닐 (500 K × 20 ps) + 이완 · kgy GPU
#   Nd 카드 db/properties/ndo_lpscl16_site_stability_estimand_2026_10_14.json §3 · 결정 D-2026-10-14-ndo-site-stability-estimand
#   B  카드 db/properties/b2o3_site_screen_estimand_2026_10_14.json · 결정 D-2026-10-14-b2o3-site-screen
#   사용자 10-14 '1,2,3,4를 해보자' · GPU 자리 = 'kgy 지금' · '빠르게 uma로 screening 해봐도 돼 nd 때처럼'
#
# 기본값 = Nd Rietveld 5 f.u. 23 개 (세션 ndsite_uma · 출력 uma_anneal) — 옛 붙여넣기 블록 그대로 돈다.
# 환경변수: CAND (후보 폴더 여러 개 · 공백) · N_EXPECT (중복 제거 뒤 개수) · SESSION · OUTNAME · WAIT_FOR (앞 tmux 세션)
#           TIME_PS (기본 20 · 0 = 이완만) · TEMP (기본 500 K) · SEED (기본 20261014) · RELAX_FMAX (기본 0.05 · 포논 앞 이완은 0.01)
#           — 2026-11-09 (Codex DU P1-4 · Q9):
#           옛 판은 20 ps · 500 K 를 박아 둬서 탐침이 고른 0/20/100 ps 를 전달할 길이 없었다.
#           끝나면 run_anneal.py --check_results 로 **요청한 시간 · 온도 · 개수가 실제 기록과 같은지** 보고 로그에 rc 를 남긴다.
#           후보 폴더 manifest 는 두 꼴: make_candidates (files{}) · b2o3_enumerate (bases[] — 먼저 --verify · O 꼴 파일만 넘긴다).
#           ⚠ 2026-11-09 발견: 옛 run_anneal.py 는 selftest 가 실패해도 종료코드 0 이라 ③ '자가시험 실패면 멈춤' 이 실제로는
#             못 멈췄다 (main() 반환값을 버렸다) — 지금은 sys.exit(main()).
#
# 모드 (첫 인자)
#   (없음)        아래 ①–⑤ 로 어닐을 줄 세우고 발사한다
#   --dry-run     ④ 까지 하고 줄 선 스크립트 내용만 찍는다
#   --watch-only  감시 스크립트 ~/w_<SESSION>.sh 만 다시 쓴다 (돌고 있는 세션 · 줄 선 스크립트는 안 건드린다)
#   --refs        ΔG_site 기준상 Li₂S (mp-1153) · Li₃PS₄ (mp-985583) 를 **같은 run_anneal.py 로 이완만** 한다
#                 (--time_ps 0 = MD 0 걸음 · 같은 FIRE + 셀 필터 · fmax 0.05) · 전경 · 1–2 분 · 출력 $R/uma_ref_relax
#                 후보를 어닐한 소스 ($R/src · $R/src10) 의 run_anneal.py 와 바이트가 다르면 멈춘다 (종료 8)
#
# 하는 일 (기본 모드 · 순서대로 · 하나라도 실패하면 발사 안 함)
#   ① nd_scf 설정 균일성 (Nd 카드 §6 원본 · sort | uniq -c · 읽기만)
#   ② 후보 해시 대조 (폴더마다 manifest.json) · 내용이 같은 파일은 해시로 한 번만 (B · Nd 의 같은 host)
#   ③ run_anneal.py --selftest (UMA python)
#   ④ tmux 세션 · 같은 출력 폴더 python 없음 · (줄 안 설 때만) VRAM 여유 ≥ 4000 MiB
#   ⑤ 줄 선 스크립트 $R/queue_<SESSION>.sh 를 tmux 로 — WAIT_FOR 가 끝나길 기다리고 → VRAM 여유 ≥ 4000 를 기다리고 → 어닐
#      + 감시 스크립트 ~/w_<SESSION>.sh
#
# ⚠ 2026-10-14 감시 고침: 옛 감시는 결과 json 만 봤는데 run_anneal.py 는 그 json 을 **구조 2 개마다** 쓰고,
#    로그로 돌린 stdout 은 버퍼에 쌓여서 (경고 줄만 보임) 첫 두 구조 동안 진행이 안 보였다 (kgy 실측 13:32 · 13:39).
#    이제 구조 폴더를 본다 — post_relax.xyz 수 (끝난 구조) · 진행 중 폴더의 md.log 마지막 시각 · relax.log 마지막 줄.
#    새로 발사하는 런은 PYTHONUNBUFFERED=1 로 로그도 바로 찍힌다 (이미 도는 ndsite_uma · site10_uma 는 그대로).
#
# ⛔ 이 스크립트가 못 하는 것: 순위를 매기지 않는다 (anneal_results.json 만) · ΔG_site 를 내지 않는다 (--refs 는 저장소 항까지) ·
#    DFT 를 돌리지 않는다 · kgy 옆 런 (cascade v7 · li2s) 의 속도를 지키지 않는다 — 같은 GPU 를 나눠 쓴다 (사용자 선택) ·
#    --refs 의 기준상은 MP (PBE) 바닥 다형 하나씩이다 — UMA 에서 다른 다형이 더 낮은지는 보지 않는다.
# 줄 선 스크립트 종료 코드 (2026-11-09): 0 성공 · run_anneal 의 rc (실행 실패) · 12 입력 · 소스가 제출 뒤 바뀜 · 13 결과 검사만 실패
#   --selftest = 모의 python · 가짜 nvidia-smi 로 큐를 돌려 실패 전파 네 경우 + 입력 바뀜을 본다 (GPU · python 필요 없음)
# 종료 코드: 2 python 없음 · 3 VRAM 부족 · 4 이미 도는 중 · 5 해시 불일치 · 6 자가시험 실패 · 7 후보 수 ≠ N_EXPECT (--refs: 기준상 파일 없음) ·
#            8 run_anneal.py 가 후보 쪽 소스와 다름 · 9 모르는 인자 · 10 기준상 이완 실패 · 미수렴 · 조성 이상
set -euo pipefail
MODE=run
case "${1:-}" in
  "") ;;
  --dry-run) MODE=dry ;;
  --watch-only) MODE=watch ;;
  --refs) MODE=refs ;;
  --selftest) MODE=selftest ;;
  *) echo "⛔ 모르는 인자: $1 (--dry-run · --watch-only · --refs · --selftest)"; exit 9 ;;
esac
DRY=0; [ "$MODE" = dry ] && DRY=1
R=${R:-$HOME/work/runs/ndo_site_2026_10_14}
SRC=${SRC:-$R/src}
PY=${PY:-/home/kgy/apps/miniforge3/envs/uma/bin/python}
CAND=${CAND:-$SRC/db/inputs/ndo_site_2026_10_14/candidates}
N_EXPECT=${N_EXPECT:-23}
SESSION=${SESSION:-ndsite_uma}
OUTNAME=${OUTNAME:-uma_anneal}
WAIT_FOR=${WAIT_FOR:-}
TIME_PS=${TIME_PS:-20}
TEMP=${TEMP:-500}
RELAX_FMAX=${RELAX_FMAX:-0.05}
SEED=${SEED:-20261014}
OUT=$R/$OUTNAME; LOG=$R/$OUTNAME.log

write_watch() {   # $1 = 감시 스크립트 경로 · 임시 파일에 쓰고 mv (watch 가 읽는 도중에 반쯤 쓴 파일을 안 보게)
  {
    echo '#!/bin/bash'
    echo "# watch -n 60 bash ~/w_$SESSION.sh — UMA 어닐 감시 (읽기만 · run_uma_kgy.sh 가 $(date '+%F %T') 에 썼다)"
    printf 'S=%q; OUT=%q; LOG=%q; N=%q\n' "$SESSION" "$OUT" "$LOG" "$N_EXPECT"
    cat <<'W'
date "+%F %T"
tmux has-session -t "$S" 2>/dev/null && echo "tmux $S 살아 있음" || echo "tmux $S 없음 (끝났거나 죽음 — 로그 꼬리를 본다)"
# 시작 판정 = 구조 폴더가 하나라도 있거나 로그에 '시작' 줄 — 줄 서기 없이 띄운 런 (10-14 ndsite_uma) 은 '시작' 줄이 없어서
#   옛 판이 돌고 있는 런을 '아직 시작 전' 으로 찍었다 (kgy 14:36 실측)
ls -d "$OUT"/*/ >/dev/null 2>&1 || grep -q -a "시작" "$LOG" 2>/dev/null || echo "아직 시작 전 (앞 세션 · VRAM 을 기다리는 중)"
# 결과 json 은 구조 2 개마다 저장되고 로그 stdout 은 버퍼에 쌓인다 — 진행은 구조 폴더로 본다
D=$(ls "$OUT"/*/post_relax.xyz 2>/dev/null | wc -l)
echo "이완까지 끝난 구조 $D / $N"
# 구조당 시간 = md.log 생성 (MD 시작) → post_relax.xyz 수정 (이완 끝). 생성 시각을 못 읽으면 (stat %W 가 숫자 아님 · 0) 건너뛴다
born() { local b; b=$(stat -c %W "$1" 2>/dev/null); [[ "$b" =~ ^[0-9]+$ ]] && [ "$b" -gt 0 ] && echo "$b"; }
now=$(date +%s); k=0; tot=0
for d in "$OUT"/*/; do
  [ -f "$d/post_relax.xyz" ] || continue
  b=$(born "$d/md.log") || continue
  k=$((k + 1)); tot=$((tot + $(stat -c %Y "$d/post_relax.xyz") - b))
done
C=$(ls -td "$OUT"/*/ 2>/dev/null | head -1); cur=0
if [ -n "$C" ] && [ ! -f "$C/post_relax.xyz" ]; then
  nm=$(basename "$C")
  if [ -f "$C/relax.log" ]; then echo "진행 중 $nm · 이완 $(tail -1 "$C/relax.log")"
  elif [ -f "$C/md.log" ]; then
    b=$(born "$C/md.log") && el=$(( $(stat -c %Y "$C/md.log") - b )) || el=0
    awk -v n="$nm" -v el="$el" 'NF==5 && $1+0==$1 {t=$1; T=$5} END {if (t=="") {printf "진행 중 %s · MD 시작\n", n; exit}
      s=""; if (t>0 && el>0) s=sprintf(" · MD 속도 %.1f ps/h (20 ps 에 %d 분)", t*3600/el, 20*el/t/60)
      printf "진행 중 %s · MD %s ps (20 ps 까지) · T %s K%s\n", n, t, T, s}' "$C/md.log"
  fi
  b=$(born "$C/md.log") && cur=$((now - b))
fi
if [ "$k" -gt 0 ]; then
  avg=$((tot / k)); rest=$((avg * (N - D) - cur)); [ "$rest" -lt 0 ] && rest=0
  if [ "$D" -ge "$N" ]; then echo "구조당 평균 $((avg / 60)) 분 (끝난 $k 개 기준) · 다 끝남"
  else echo "구조당 평균 $((avg / 60)) 분 (끝난 $k 개 기준) · 남은 $((N - D)) 개 → 어림 끝 $(date -d "@$((now + rest))" '+%m-%d %H:%M')"; fi
fi
grep -a -E "시작|끝 rc|대기" "$LOG" 2>/dev/null | tail -2
nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu --format=csv,noheader
W
  } > "$1.tmp"
  mv "$1.tmp" "$1"
}

write_queue() {   # 줄 선 스크립트를 stdout 으로 — $1 = 제출 때 해시 목록 (SUMS) · 전역: SESSION LOG WAIT_FOR SRC PY XYZ OUT TEMP TIME_PS SEED RELAX_FMAX N_EXPECT
  # ⛔ 2026-11-09 (Codex DV P1 · P2): 옛 큐는 ① 실행 · 검사가 실패해도 마지막 echo 의 성공으로 종료 0 이었고
  #   ② `echo "$(date …) rc=$?"` 가 **date 의 종료코드**를 찍었다 (bash 5.2 재현 — 10-14 · 10-16 로그의 '끝 rc=' 는 못 믿는다)
  #   ③ 대기 뒤 입력을 제출 때와 다시 대조하지 않았다. 이제 rc 를 명령 바로 뒤에 저장 · 찍고 · nonzero 로 끝내며
  #   (실행 실패 → 그 rc · 검사만 실패 → 13 · 입력 · 소스 바뀜 → 12), 발사 직전 sha256sum -c 로 재대조한다.
  echo '#!/bin/bash'
  echo "# $SESSION — run_uma_kgy.sh 가 $(date '+%F %T') 에 썼다"
  printf 'LOG=%q; WAIT_FOR=%q; SUMS=%q\n' "$LOG" "$WAIT_FOR" "$1"
  echo 'if [ -n "$WAIT_FOR" ]; then while tmux has-session -t "$WAIT_FOR" 2>/dev/null; do sleep 60; done; fi'
  echo 'while :; do read -r U T < <(nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits | head -1 | tr -d ","); F=$((T-U)); [ "$F" -ge 4000 ] && break; echo "$(date "+%F %T") VRAM 여유 $F < 4000 — 대기" >> "$LOG"; sleep 120; done'
  echo 'if ! sha256sum -c --quiet "$SUMS" >> "$LOG" 2>&1; then echo "$(date "+%F %T") ⛔ 입력 · 소스가 제출 뒤 바뀌었다 — 발사 안 함 (종료 12)" >> "$LOG"; exit 12; fi'
  echo 'echo "$(date "+%F %T") 시작 (입력 · 소스 해시 재대조 통과)" >> "$LOG"'
  printf 'cd %q && PYTHONUNBUFFERED=1 %q tools/doping/run_anneal.py --xyz' "$SRC" "$PY"; printf ' %q' "${XYZ[@]}"
  printf ' --out %q --temperature %q --time_ps %q --seed %q --relax_fmax %q --device cuda >> "$LOG" 2>&1\n' "$OUT" "$TEMP" "$TIME_PS" "$SEED" "$RELAX_FMAX"
  echo 'run_rc=$?'
  echo 'echo "$(date "+%F %T") 끝 run_rc=$run_rc" >> "$LOG"'
  printf 'cd %q && %q tools/doping/run_anneal.py --check_results %q --expect_n %q --expect_time_ps %q --expect_temperature %q >> "$LOG" 2>&1\n' \
    "$SRC" "$PY" "$OUT/anneal_results.json" "$N_EXPECT" "$TIME_PS" "$TEMP"
  echo 'check_rc=$?'
  echo 'echo "$(date "+%F %T") 결과 검사 check_rc=$check_rc (0 = 요청한 시간 · 온도 · 개수 · 결과 파일 해시가 기록과 같다)" >> "$LOG"'
  echo 'if [ "$run_rc" -ne 0 ]; then exit "$run_rc"; fi'
  echo 'if [ "$check_rc" -ne 0 ]; then exit 13; fi'
  echo 'exit 0'
}

queue_selftest() {   # 모의 python · 가짜 nvidia-smi 로 같은 write_queue 를 돌려 본다 (실행 · 검사 실패 네 경우 + 입력 바뀜)
  local T; T=$(mktemp -d)
  mkdir -p "$T/bin" "$T/src/tools/doping" "$T/in"
  printf '#!/bin/bash\necho "1000, 48000"\n' > "$T/bin/nvidia-smi"
  printf '#!/bin/bash\ncase " $* " in *" --check_results "*) exit "${MOCK_CHECK_RC:-0}";; *) echo ran >> "$MOCK_MARK"; exit "${MOCK_RUN_RC:-0}";; esac\n' > "$T/bin/mockpy"
  chmod +x "$T/bin/nvidia-smi" "$T/bin/mockpy"
  echo a > "$T/src/tools/doping/run_anneal.py"; echo b > "$T/src/tools/doping/_provenance.py"
  echo x1 > "$T/in/c1.cif"; echo x2 > "$T/in/c2.cif"
  SESSION=st; LOG=$T/log; WAIT_FOR=; SRC=$T/src; PY=$T/bin/mockpy; XYZ=("$T/in/c1.cif" "$T/in/c2.cif")
  OUT=$T/out; TEMP=500; TIME_PS=0; SEED=1; RELAX_FMAX=0.05; N_EXPECT=2
  local SUMS=$T/sums bad=0 rr cr want rc
  sha256sum "${XYZ[@]}" "$SRC/tools/doping/run_anneal.py" "$SRC/tools/doping/_provenance.py" > "$SUMS"
  write_queue "$SUMS" > "$T/q.sh"
  for rr in 0 7; do for cr in 0 1; do
    : > "$LOG"; rm -f "$T/mark"
    rc=0; PATH="$T/bin:$PATH" MOCK_RUN_RC=$rr MOCK_CHECK_RC=$cr MOCK_MARK=$T/mark bash "$T/q.sh" || rc=$?   # set -e 아래라 || 로 받는다
    if [ "$rr" -ne 0 ]; then want=$rr; elif [ "$cr" -ne 0 ]; then want=13; else want=0; fi
    if [ "$rc" -eq "$want" ] && grep -q "run_rc=$rr\b" "$LOG" && grep -q "check_rc=$cr\b" "$LOG"; then
      echo "  ✓ 실행 rc $rr · 검사 rc $cr → 큐 종료 $rc (기대 $want) · 로그에 두 rc 그대로"
    else echo "  ✗ 실행 rc $rr · 검사 rc $cr → 큐 종료 $rc (기대 $want) · 로그: $(tr '\n' ' ' < "$LOG")"; bad=1; fi
  done; done
  : > "$LOG"; rm -f "$T/mark"; echo changed > "$T/in/c2.cif"
  rc=0; PATH="$T/bin:$PATH" MOCK_RUN_RC=0 MOCK_CHECK_RC=0 MOCK_MARK=$T/mark bash "$T/q.sh" || rc=$?
  if [ "$rc" -eq 12 ] && [ ! -e "$T/mark" ]; then echo "  ✓ 제출 뒤 입력이 바뀌면 발사 안 함 (종료 12 · 실행 0 회)"
  else echo "  ✗ 제출 뒤 입력이 바뀌었는데 종료 $rc · 실행 $( [ -e "$T/mark" ] && echo 됨 || echo 안 됨)"; bad=1; fi
  rm -rf "$T"
  if [ "$bad" = 0 ]; then echo "queue selftest PASS (5/5)"; return 0; fi
  echo "queue selftest FAIL"; return 1
}

vram_free() {   # 여유 MiB 를 찍는다 (프로세스별 표는 kgy 에서 막혀 있다 — 'Process-level GPU information is restricted')
  local used total
  read -r used total < <(nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits | head -1 | tr -d ',')
  echo "   VRAM 사용 $used / $total MiB · 여유 $((total - used)) MiB" >&2
  echo $((total - used))
}

if [ "$MODE" = watch ]; then
  write_watch "$HOME/w_$SESSION.sh"
  echo "✓ 감시 스크립트 다시 씀: ~/w_$SESSION.sh (OUT $OUT · N $N_EXPECT) — 도는 watch 는 다음 갱신부터 새 내용"
  exit 0
fi

if [ "$MODE" = selftest ]; then queue_selftest; exit $?; fi
[ -x "$PY" ] || { echo "⛔ python 없음: $PY"; exit 2; }

if [ "$MODE" = refs ]; then
  OUTR=$R/uma_ref_relax
  REFS=("$SRC/db/structures/sei_li2s_mp-1153.cif" "$SRC/db/structures/li3ps4_mp-985583.cif")
  echo "== 기준상 이완 (Li₂S · Li₃PS₄ · MD 0 ps · 이완만) — 출력 $OUTR"
  for f in "${REFS[@]}"; do [ -f "$f" ] || { echo "⛔ 기준상 파일 없음: $f"; exit 7; }; done
  NCMP=0
  for o in "$R/src" "$R/src10"; do
    [ -f "$o/tools/doping/run_anneal.py" ] || continue
    [ "$(realpath "$o")" = "$(realpath "$SRC")" ] && continue
    cmp -s "$o/tools/doping/run_anneal.py" "$SRC/tools/doping/run_anneal.py" \
      || { echo "⛔ run_anneal.py 가 $o 의 것과 다르다 — 후보와 같은 이완 코드가 아니다"; exit 8; }
    echo "   run_anneal.py = $o 의 것과 같다 (후보 어닐과 같은 이완 코드)"; NCMP=$((NCMP + 1))
  done
  [ "$NCMP" -gt 0 ] || echo "   ⚠ 비교할 후보 쪽 소스 ($R/src · $R/src10) 가 없다 — 같은 코드인지 확인 못 함"
  "$PY" "$SRC/tools/doping/run_anneal.py" --selftest | tail -1 || { echo "⛔ run_anneal 자가시험 실패"; exit 6; }
  for x in $(pgrep -f "$OUTR" || true); do
    case "$(cat /proc/$x/comm 2>/dev/null)" in python*) echo "⛔ 같은 출력 폴더의 python 이 돈다 (PID $x)"; exit 4;; esac
  done
  FREE=$(vram_free)
  [ "$FREE" -ge 4000 ] || { echo "⛔ VRAM 여유 $FREE MiB < 4000 — 시작 안 함 (조금 뒤 다시)"; exit 3; }
  echo "   이완 $(date '+%F %T') — 로그 $OUTR.log"
  # seed 는 run_anneal.py 가 필수로 받는다 (MD 0 걸음이라 결과에 영향 없음 · 후보와 같은 값)
  PYTHONUNBUFFERED=1 "$PY" "$SRC/tools/doping/run_anneal.py" --xyz "${REFS[@]}" --out "$OUTR" \
    --time_ps 0 --seed 20261014 --device cuda > "$OUTR.log" 2>&1 \
    || { rc=$?; echo "⛔ 이완 실패 (rc $rc) — 로그 꼬리:"; tail -20 "$OUTR.log"; exit 10; }
  "$PY" - "$OUTR/anneal_results.json" <<'PY' || exit 10
import json, sys
from collections import Counter
from ase.io import read
d = json.load(open(sys.argv[1]))
e, bad = {}, 0
for r in d["results"]:
    if "error" in r:
        print(f"   ⛔ {r['name']}: {r['error']}"); bad = 1; continue
    c = Counter(read(r["post_relax_xyz"]).get_chemical_symbols())
    if set(c) == {"Li", "S"} and c["Li"] == 2 * c["S"]:
        f, n = "Li2S", c["S"]
    elif set(c) == {"Li", "P", "S"} and c["Li"] == 3 * c["P"] and c["S"] == 4 * c["P"]:
        f, n = "Li3PS4", c["P"]
    else:
        print(f"   ⛔ {r['name']}: 조성 {dict(c)} 이 Li2S · Li3PS4 가 아니다"); bad = 1; continue
    if f in e:
        print(f"   ⛔ {f} 가 둘이다"); bad = 1
    dv = 100 * (r["volume_post"] / r["volume_pre"] - 1)
    print(f"   {r['name']:<18} {f:<7} {n} f.u. · E/f.u. {r['E_post_relax'] / n:.5f} eV · "
          f"부피 {dv:+.2f} % (MP 구조 대비) · 이완 {r['n_relax_steps']} 걸음 · 수렴 {r['converged']}")
    if not r["converged"]:
        print(f"   ⛔ {r['name']} 이완 미수렴"); bad = 1
    e[f] = r["E_post_relax"] / n
# 하나라도 ⛔ 면 저장소 항을 찍지 않는다 — 실패한 런의 숫자가 복사돼 나가지 않게 (로컬 시험: 미수렴인데 찍혔다)
if bad == 0 and set(e) == {"Li2S", "Li3PS4"}:
    print(f"   저장소 항 4·e(Li₂S) − e(Li₃PS₄) = {4 * e['Li2S'] - e['Li3PS4']:.5f} eV "
          f"(도펀트 하나당 · M@P − M@Li = +5 Li −1 P)")
else:
    print("   ⛔ 저장소 항은 안 낸다 — 기준상 둘이 다 수렴해야 낸다"); bad = 1
sys.exit(bad)
PY
  echo "✓ 기준상 이완 끝 $(date '+%F %T')"
  exit 0
fi

echo "== ① nd_scf 설정 균일성 (Nd 카드 §6 · 읽기만 · 줄마다 '같은 줄이 몇 개 scf.in 에 있나')"
# ⚠ 2026-10-14 고침: 옛 판은 이 출력을 `| head -80` 으로 잘랐는데 set -o pipefail 이라 SIGPIPE 로 스크립트가 조용히 멈췄다
#   (kgy 실측 — ① 만 찍고 발사 안 함). 자르지 않고 sort | uniq -c 로 접는다.
#   같은 종류 하나 더 (로컬 시험에서 잡음): scf.in 이 하나도 없으면 ls 가 실패해 pipefail + set -e 로 여기서 말없이 끝났다 (rc 2).
#   kgy 에는 scf.in 이 있어 안 걸렸다. 없으면 0 개로 찍고 넘어간다.
N_SCF=$( { ls "$HOME"/work/runs/nd_scf_2026_09_08/*/scf.in 2>/dev/null || true; } | wc -l)
echo "   scf.in $N_SCF 개"
if [ "$N_SCF" -gt 0 ]; then
  cat "$HOME"/work/runs/nd_scf_2026_09_08/*/scf.in \
    | grep -E "ecutwfc|ecutrho|occupations|smearing|degauss|conv_thr|mixing_beta|nspin|input_dft|UPF|^ *[0-9]+ +[0-9]+ +[0-9]+ +[01] +[01] +[01] *$" \
    | tr -s ' ' | sort | uniq -c || true
fi

echo "== ② 후보 해시 · 중복 제거"
for d in $CAND; do
  if grep -q '"schema": "b2o3_enumerate_manifest/v1"' "$d/manifest.json" 2>/dev/null; then
    "$PY" "$SRC/tools/doping/b2o3_enumerate.py" --verify "$d" | tail -1 || { echo "⛔ $d manifest 검증 실패"; exit 5; }
  fi
done
LIST=$(mktemp)
"$PY" - $CAND > "$LIST" <<'PY' || { rc=$?; rm -f "$LIST"; echo "⛔ 해시 단계 실패 (rc $rc)"; exit 5; }
import hashlib, json, pathlib, sys
seen, out, bad = set(), [], []
for d in map(pathlib.Path, sys.argv[1:]):
    m = json.load(open(d / "manifest.json"))
    if "bases" in m:      # b2o3_enumerate manifest (2026-11-09) — 쉘이 먼저 --verify 했다 · O 꼴 파일만 (없으면 바탕)
        files = {e["file"]: e for b in m["bases"] for e in b["motifs"].values()} \
            or {b["file"]: b for b in m["bases"]}
    else:
        files = m["files"]
    for k, v in files.items():
        h = hashlib.sha256((d / k).read_bytes()).hexdigest()
        if h != v["sha256"]:
            bad.append(str(d / k)); continue
        if h in seen:
            continue
        seen.add(h); out.append(str((d / k).resolve()))
    print(f"   {d.name}: 해시 {len(files)} 개 확인", file=sys.stderr)
if bad:
    print("⛔ 해시 불일치: " + " ".join(bad), file=sys.stderr); sys.exit(5)
print("\n".join(sorted(out)))
PY
mapfile -t XYZ < "$LIST"; rm -f "$LIST"
echo "   중복 제거 뒤 ${#XYZ[@]} 개"
[ "${#XYZ[@]}" -eq "$N_EXPECT" ] || { echo "⛔ 후보 ${#XYZ[@]} 개 (N_EXPECT $N_EXPECT 이어야 한다)"; exit 7; }

echo "== ③ 자가시험"
"$PY" "$SRC/tools/doping/run_anneal.py" --selftest | tail -1 || { echo "⛔ run_anneal 자가시험 실패"; exit 6; }
queue_selftest | tail -1 || { echo "⛔ 큐 자가시험 실패 (실패 전파 · 입력 재대조)"; exit 6; }

echo "== ④ 문턱"
if tmux has-session -t "$SESSION" 2>/dev/null; then echo "⛔ tmux $SESSION 이미 있음"; exit 4; fi
for x in $(pgrep -f "$R/$OUTNAME" || true); do
  case "$(cat /proc/$x/comm 2>/dev/null)" in python*) echo "⛔ 같은 출력 폴더의 python 이 돈다 (PID $x)"; exit 4;; esac
done
FREE=$(vram_free)
nvidia-smi --query-compute-apps=pid,used_memory,process_name --format=csv,noheader || true
QUEUED=0; [ -n "$WAIT_FOR" ] && tmux has-session -t "$WAIT_FOR" 2>/dev/null && QUEUED=1
if [ "$QUEUED" = 1 ]; then echo "   줄 섬: tmux $WAIT_FOR 가 끝나면 시작 (VRAM 은 시작 직전에 다시 본다)";
else [ "$FREE" -ge 4000 ] || { echo "⛔ VRAM 여유 $FREE MiB < 4000 — 시작 안 함"; exit 3; }; fi

Q=$R/queue_$SESSION.sh
if [ "$DRY" = 1 ]; then QT=$(mktemp); SUMS=$(mktemp); else mkdir -p "$R"; QT=$Q.tmp; SUMS=$R/queue_$SESSION.sha256; fi
sha256sum "${XYZ[@]}" "$SRC/tools/doping/run_anneal.py" "$SRC/tools/doping/_provenance.py" > "$SUMS" \
  || { echo "⛔ 제출 해시 목록을 못 만든다"; exit 5; }
write_queue "$SUMS" > "$QT"
if [ "$DRY" = 1 ]; then echo "== (dry-run) 줄 선 스크립트:"; sed 's/^/   /' "$QT" | cut -c1-220 || true; rm -f "$QT" "$SUMS"; exit 0; fi
mv "$QT" "$Q"

echo "== ⑤ 발사 $(date '+%F %T')"
mkdir -p "$OUT"
write_watch "$HOME/w_$SESSION.sh"
tmux new -d -s "$SESSION" "bash '$Q'"
echo "   감시: watch -n 60 bash ~/w_$SESSION.sh"
sleep "${WAIT:-60}"
tail -4 "$LOG" 2>/dev/null || true
nvidia-smi --query-compute-apps=pid,used_memory,process_name --format=csv,noheader || true
