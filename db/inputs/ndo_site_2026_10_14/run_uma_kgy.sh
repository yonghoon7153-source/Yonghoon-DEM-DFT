#!/usr/bin/env bash
# run_uma_kgy.sh — 도펀트 자리 비교 1 단계: 후보 UMA 어닐 (500 K × 20 ps) + 이완 · kgy GPU
#   Nd 카드 db/properties/ndo_lpscl16_site_stability_estimand_2026_10_14.json §3 · 결정 D-2026-10-14-ndo-site-stability-estimand
#   B  카드 db/properties/b2o3_site_screen_estimand_2026_10_14.json · 결정 D-2026-10-14-b2o3-site-screen
#   사용자 10-14 '1,2,3,4를 해보자' · GPU 자리 = 'kgy 지금' · '빠르게 uma로 screening 해봐도 돼 nd 때처럼'
#
# 기본값 = Nd Rietveld 5 f.u. 23 개 (세션 ndsite_uma · 출력 uma_anneal) — 옛 붙여넣기 블록 그대로 돈다.
# 환경변수: CAND (후보 폴더 여러 개 · 공백) · N_EXPECT (중복 제거 뒤 개수) · SESSION · OUTNAME · WAIT_FOR (앞 tmux 세션)
#
# 하는 일 (순서대로 · 하나라도 실패하면 발사 안 함)
#   ① nd_scf 설정 균일성 (Nd 카드 §6 원본 · sort | uniq -c · 읽기만)
#   ② 후보 해시 대조 (폴더마다 manifest.json) · 내용이 같은 파일은 해시로 한 번만 (B · Nd 의 같은 host)
#   ③ run_anneal.py --selftest (UMA python)
#   ④ tmux 세션 · 같은 출력 폴더 python 없음 · (줄 안 설 때만) VRAM 여유 ≥ 4000 MiB
#   ⑤ 줄 선 스크립트 $R/queue_<SESSION>.sh 를 tmux 로 — WAIT_FOR 가 끝나길 기다리고 → VRAM 여유 ≥ 4000 를 기다리고 → 어닐
#      + 감시 스크립트 ~/w_<SESSION>.sh
#   --dry-run 이면 ④ 까지 하고 줄 선 스크립트 내용만 찍는다.
#
# ⛔ 이 스크립트가 못 하는 것: 순위를 매기지 않는다 (anneal_results.json 만) · DFT 를 돌리지 않는다 ·
#    kgy 옆 런 (cascade v7 · li2s) 의 속도를 지키지 않는다 — 같은 GPU 를 나눠 쓴다 (사용자 선택).
# 종료 코드: 2 python 없음 · 3 VRAM 부족 · 4 이미 도는 중 · 5 해시 불일치 · 6 자가시험 실패 · 7 후보 수 ≠ N_EXPECT
set -euo pipefail
DRY=0; [ "${1:-}" = "--dry-run" ] && DRY=1
R=${R:-$HOME/work/runs/ndo_site_2026_10_14}
SRC=${SRC:-$R/src}
PY=${PY:-/home/kgy/apps/miniforge3/envs/uma/bin/python}
CAND=${CAND:-$SRC/db/inputs/ndo_site_2026_10_14/candidates}
N_EXPECT=${N_EXPECT:-23}
SESSION=${SESSION:-ndsite_uma}
OUTNAME=${OUTNAME:-uma_anneal}
WAIT_FOR=${WAIT_FOR:-}
OUT=$R/$OUTNAME; LOG=$R/$OUTNAME.log
[ -x "$PY" ] || { echo "⛔ python 없음: $PY"; exit 2; }

echo "== ① nd_scf 설정 균일성 (Nd 카드 §6 · 읽기만 · 줄마다 '같은 줄이 몇 개 scf.in 에 있나')"
# ⚠ 2026-10-14 고침: 옛 판은 이 출력을 `| head -80` 으로 잘랐는데 set -o pipefail 이라 SIGPIPE 로 스크립트가 조용히 멈췄다
#   (kgy 실측 — ① 만 찍고 발사 안 함). 자르지 않고 sort | uniq -c 로 접는다.
N_SCF=$(ls "$HOME"/work/runs/nd_scf_2026_09_08/*/scf.in 2>/dev/null | wc -l)
echo "   scf.in $N_SCF 개"
if [ "$N_SCF" -gt 0 ]; then
  cat "$HOME"/work/runs/nd_scf_2026_09_08/*/scf.in \
    | grep -E "ecutwfc|ecutrho|occupations|smearing|degauss|conv_thr|mixing_beta|nspin|input_dft|UPF|^ *[0-9]+ +[0-9]+ +[0-9]+ +[01] +[01] +[01] *$" \
    | tr -s ' ' | sort | uniq -c || true
fi

echo "== ② 후보 해시 · 중복 제거"
LIST=$(mktemp)
"$PY" - $CAND > "$LIST" <<'PY' || { rc=$?; rm -f "$LIST"; echo "⛔ 해시 단계 실패 (rc $rc)"; exit 5; }
import hashlib, json, pathlib, sys
seen, out, bad = set(), [], []
for d in map(pathlib.Path, sys.argv[1:]):
    m = json.load(open(d / "manifest.json"))
    for k, v in m["files"].items():
        h = hashlib.sha256((d / k).read_bytes()).hexdigest()
        if h != v["sha256"]:
            bad.append(str(d / k)); continue
        if h in seen:
            continue
        seen.add(h); out.append(str((d / k).resolve()))
    print(f"   {d.name}: 해시 {len(m['files'])} 개 확인", file=sys.stderr)
if bad:
    print("⛔ 해시 불일치: " + " ".join(bad), file=sys.stderr); sys.exit(5)
print("\n".join(sorted(out)))
PY
mapfile -t XYZ < "$LIST"; rm -f "$LIST"
echo "   중복 제거 뒤 ${#XYZ[@]} 개"
[ "${#XYZ[@]}" -eq "$N_EXPECT" ] || { echo "⛔ 후보 ${#XYZ[@]} 개 (N_EXPECT $N_EXPECT 이어야 한다)"; exit 7; }

echo "== ③ 자가시험"
"$PY" "$SRC/tools/doping/run_anneal.py" --selftest | tail -1 || { echo "⛔ run_anneal 자가시험 실패"; exit 6; }

echo "== ④ 문턱"
if tmux has-session -t "$SESSION" 2>/dev/null; then echo "⛔ tmux $SESSION 이미 있음"; exit 4; fi
for x in $(pgrep -f "$R/$OUTNAME" || true); do
  case "$(cat /proc/$x/comm 2>/dev/null)" in python*) echo "⛔ 같은 출력 폴더의 python 이 돈다 (PID $x)"; exit 4;; esac
done
read -r USED TOTAL < <(nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits | head -1 | tr -d ',')
FREE=$((TOTAL - USED)); echo "   VRAM 사용 $USED / $TOTAL MiB · 여유 $FREE MiB"
nvidia-smi --query-compute-apps=pid,used_memory,process_name --format=csv,noheader || true
QUEUED=0; [ -n "$WAIT_FOR" ] && tmux has-session -t "$WAIT_FOR" 2>/dev/null && QUEUED=1
if [ "$QUEUED" = 1 ]; then echo "   줄 섬: tmux $WAIT_FOR 가 끝나면 시작 (VRAM 은 시작 직전에 다시 본다)";
else [ "$FREE" -ge 4000 ] || { echo "⛔ VRAM 여유 $FREE MiB < 4000 — 시작 안 함"; exit 3; }; fi

Q=$R/queue_$SESSION.sh
if [ "$DRY" = 1 ]; then QT=$(mktemp); else mkdir -p "$R"; QT=$Q.tmp; fi
{
  echo '#!/bin/bash'
  echo "# $SESSION — run_uma_kgy.sh 가 $(date '+%F %T') 에 썼다"
  printf 'LOG=%q; WAIT_FOR=%q\n' "$LOG" "$WAIT_FOR"
  echo 'if [ -n "$WAIT_FOR" ]; then while tmux has-session -t "$WAIT_FOR" 2>/dev/null; do sleep 60; done; fi'
  echo 'while :; do read -r U T < <(nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits | head -1 | tr -d ","); F=$((T-U)); [ "$F" -ge 4000 ] && break; echo "$(date "+%F %T") VRAM 여유 $F < 4000 — 대기" >> "$LOG"; sleep 120; done'
  echo 'echo "$(date "+%F %T") 시작" >> "$LOG"'
  printf 'cd %q && %q tools/doping/run_anneal.py --xyz' "$SRC" "$PY"; printf ' %q' "${XYZ[@]}"
  printf ' --out %q --temperature 500 --time_ps 20 --seed 20261014 --device cuda >> "$LOG" 2>&1\n' "$OUT"
  echo 'echo "$(date "+%F %T") 끝 rc=$?" >> "$LOG"'
} > "$QT"
if [ "$DRY" = 1 ]; then echo "== (dry-run) 줄 선 스크립트:"; sed 's/^/   /' "$QT" | cut -c1-220 || true; rm -f "$QT"; exit 0; fi
mv "$QT" "$Q"

echo "== ⑤ 발사 $(date '+%F %T')"
mkdir -p "$OUT"
W=$HOME/w_$SESSION.sh
{
  echo '#!/bin/bash'
  echo "# watch -n 60 bash ~/w_$SESSION.sh — UMA 어닐 감시 (읽기만)"
  printf 'S=%q; OUT=%q; LOG=%q; N=%q\n' "$SESSION" "$OUT" "$LOG" "$N_EXPECT"
  echo 'date "+%F %T"'
  echo 'tmux has-session -t "$S" 2>/dev/null && echo "tmux $S 살아 있음" || echo "tmux $S 없음 (끝났거나 죽음 — 로그 꼬리를 본다)"'
  echo 'python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(\"끝난 구조\", d.get(\"n_done\"), \"/\", sys.argv[2])" "$OUT/anneal_results.json" "$N" 2>/dev/null || echo "결과 json 아직 없음 (대기 중이거나 첫 구조 진행 중)"'
  echo 'tail -3 "$LOG" 2>/dev/null'
  echo 'nvidia-smi --query-compute-apps=pid,used_memory,process_name --format=csv,noheader'
} > "$W"
tmux new -d -s "$SESSION" "bash '$Q'"
echo "   감시: watch -n 60 bash ~/w_$SESSION.sh"
sleep "${WAIT:-60}"
tail -4 "$LOG" 2>/dev/null || true
nvidia-smi --query-compute-apps=pid,used_memory,process_name --format=csv,noheader || true
