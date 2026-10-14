#!/usr/bin/env bash
# run_uma_kgy.sh — Nd/O-LPSCl1.6 자리 비교 1 단계: 후보 23 개 UMA 어닐 (500 K × 20 ps) + 이완 · kgy GPU
#   카드 db/properties/ndo_lpscl16_site_stability_estimand_2026_10_14.json §3 (같은 예산) · 결정 D-2026-10-14-ndo-site-stability-estimand (proposed)
#   트랙 CEI/Nd · 1저자 = 실험. 사용자 10-14 '1,2,3,4를 해보자' + GPU 자리 = 'kgy 지금'.
#
# 하는 일 (순서대로 · 하나라도 실패하면 발사 안 함)
#   ① nd_scf 설정 균일성 (O 배치 카드 kgy 런 · 이 카드 §6 원본 · sort | uniq -c · 읽기만)
#   ② 후보 해시 대조 (manifest.json · 23 개)
#   ③ run_anneal.py --selftest (UMA python)
#   ④ VRAM 여유 ≥ 4000 MiB · tmux 세션 · 같은 출력 폴더의 python 없음
#   ⑤ tmux ndsite_uma 발사 → WAIT (기본 60) 초 뒤 로그 꼬리 · GPU 점유
#   --dry-run 이면 ④ 까지 하고 발사 명령만 찍는다.
#
# ⛔ 이 스크립트가 못 하는 것: 순위를 매기지 않는다 (anneal_results.json 만 남긴다) · DFT 를 돌리지 않는다 ·
#    kgy 옆 런 (cascade v7 · li2s) 의 속도를 지키지 않는다 — 같은 GPU 를 나눠 쓴다 (사용자 선택).
# 종료 코드: 2 python 없음 · 3 VRAM 부족 · 4 이미 도는 중 · 5 해시 불일치 · 6 자가시험 실패 · 7 후보 수 ≠ 23
set -euo pipefail
DRY=0; [ "${1:-}" = "--dry-run" ] && DRY=1
R=${R:-$HOME/work/runs/ndo_site_2026_10_14}
SRC=${SRC:-$R/src}
PY=${PY:-/home/kgy/apps/miniforge3/envs/uma/bin/python}
CAND=$SRC/db/inputs/ndo_site_2026_10_14/candidates
OUT=$R/uma_anneal
[ -x "$PY" ] || { echo "⛔ python 없음: $PY"; exit 2; }

echo "== ① nd_scf 설정 균일성 (카드 §6 · 읽기만 · 줄마다 '같은 줄이 몇 개 scf.in 에 있나')"
# ⚠ 2026-10-14 고침: 옛 판은 이 출력을 `| head -80` 으로 잘랐는데 set -o pipefail 이라 SIGPIPE 로 스크립트가 조용히 멈췄다
#   (kgy 실측 — ① 만 찍고 발사 안 함). 자르지 않고 sort | uniq -c 로 접는다.
N_SCF=$(ls "$HOME"/work/runs/nd_scf_2026_09_08/*/scf.in 2>/dev/null | wc -l)
echo "   scf.in $N_SCF 개"
if [ "$N_SCF" -gt 0 ]; then
  cat "$HOME"/work/runs/nd_scf_2026_09_08/*/scf.in \
    | grep -E "ecutwfc|ecutrho|occupations|smearing|degauss|conv_thr|mixing_beta|nspin|input_dft|UPF|^ *[0-9]+ +[0-9]+ +[0-9]+ +[01] +[01] +[01] *$" \
    | tr -s ' ' | sort | uniq -c || true
fi

echo "== ② 후보 해시"
"$PY" - "$CAND" <<'PY'
import hashlib, json, pathlib, sys
d = pathlib.Path(sys.argv[1]); m = json.load(open(d / "manifest.json"))
bad = [k for k, v in m["files"].items() if hashlib.sha256((d / k).read_bytes()).hexdigest() != v["sha256"]]
print(f"   해시 {len(m['files']) - len(bad)} / {len(m['files'])}")
sys.exit(5 if bad else 0)
PY
mapfile -t XYZ < <(ls "$CAND"/MP/*.xyz "$CAND"/MLi/*.xyz "$CAND"/host/*.xyz)
[ "${#XYZ[@]}" -eq 23 ] || { echo "⛔ 후보 ${#XYZ[@]} 개 (23 이어야 한다)"; exit 7; }

echo "== ③ 자가시험"
"$PY" "$SRC/tools/doping/run_anneal.py" --selftest | tail -1 || { echo "⛔ run_anneal 자가시험 실패"; exit 6; }

echo "== ④ 문턱"
read -r USED TOTAL < <(nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits | head -1 | tr -d ',')
FREE=$((TOTAL - USED)); echo "   VRAM 사용 $USED / $TOTAL MiB · 여유 $FREE MiB"
nvidia-smi --query-compute-apps=pid,used_memory,process_name --format=csv,noheader || true
[ "$FREE" -ge 4000 ] || { echo "⛔ VRAM 여유 $FREE MiB < 4000 — 시작 안 함"; exit 3; }
if tmux has-session -t ndsite_uma 2>/dev/null; then echo "⛔ tmux ndsite_uma 이미 있음"; exit 4; fi
for x in $(pgrep -f "ndo_site_2026_10_14/uma_anneal" || true); do
  case "$(cat /proc/$x/comm 2>/dev/null)" in python*) echo "⛔ 같은 출력 폴더의 python 이 돈다 (PID $x)"; exit 4;; esac
done

CMD="cd '$SRC' && '$PY' tools/doping/run_anneal.py --xyz ${XYZ[*]} --out '$OUT' --temperature 500 --time_ps 20 --seed 20261014 --device cuda > '$R/uma_anneal.log' 2>&1"
if [ "$DRY" = 1 ]; then echo "== (dry-run) 발사 명령:"; echo "   $CMD"; exit 0; fi

echo "== ⑤ 발사 $(date '+%F %T')"
mkdir -p "$OUT"
cat > "$HOME/w_ndsite_uma.sh" <<'W'
#!/bin/bash
# watch -n 60 bash ~/w_ndsite_uma.sh — Nd 자리 비교 UMA 어닐 감시 (읽기만)
R=$HOME/work/runs/ndo_site_2026_10_14
date '+%F %T'
tmux has-session -t ndsite_uma 2>/dev/null && echo "tmux ndsite_uma 살아 있음" || echo "tmux ndsite_uma 없음 (끝났거나 죽음 — 로그 꼬리를 본다)"
python3 - "$R/uma_anneal/anneal_results.json" <<'PY' 2>/dev/null || echo "결과 json 아직 없음 (첫 구조 진행 중)"
import json, sys
d = json.load(open(sys.argv[1])); print("끝난 구조", d.get("n_done"), "/ 23")
PY
tail -3 "$R/uma_anneal.log"
nvidia-smi --query-compute-apps=pid,used_memory,process_name --format=csv,noheader
W
echo "   감시: watch -n 60 bash ~/w_ndsite_uma.sh"
tmux new -d -s ndsite_uma "$CMD"
sleep "${WAIT:-60}"
tail -4 "$R/uma_anneal.log" || true
nvidia-smi --query-compute-apps=pid,used_memory,process_name --format=csv,noheader || true
