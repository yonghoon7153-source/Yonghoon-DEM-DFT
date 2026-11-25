#!/bin/bash
# li2s 본 런 2차 배치 — kgy (1저자 09-29 저녁: 550:1 은 P-2 겸용이라 빼고 · kgy 에서 지금) · 465:1 → 465:2 → 550:2 한 번에 하나씩
# gabia 러너(tools/ionic/glass_main_queue_gabia.sh)의 과학 검사 셋을 그대로 옮겼다 — 구조 값 게이트 · run_meta 동일성 · md.log dt.
# ⛔ kgy 에서 못 하는 것: 프로세스별 VRAM 가드 (nvidia-smi 프로세스 정보가 막혀 있다) · 탄성 가드 · gabia 예외 결정 확인 (kgy 는 그 예외 밖이다).
#    결과(D·β·C1·C2)를 판정하지 않는다 — 판독은 msd_diffusive_check.py.
# 멈춤 코드: 0 큐 끝 · 4 msd.json 없이 끝남 · 7 드라이버 sha · 8 구조 · 9 설정(run_meta·dt) · 10 이미 실행 중 · 11 out_root 이미 있음 · 12 GPU 대기 초과
set -u
ROOT=${ROOT:-$HOME/work/runs/lpscl_glass_md_main_2026_09_28}
PY=${PY:-/home/kgy/apps/miniforge3/envs/uma/bin/python}
DRV=${DRV:-$HOME/li2s_glass_src/tools/modelc_v3/disorder_ensemble_diffusion.py}
DRV_SHA16=${DRV_SHA16:-c3e2d358ee53cefa}
QUEUE=${QUEUE:-"465:1 465:2 550:2"}
A=${A:-$HOME/work/runs/lpscl_smallcell_2026_09_16/A}
REF_META=${REF_META:-$HOME/work/runs/lpscl_glass_md_2026_09_26/pilot600/T600/run_meta.json}
REF_MDLOG=${REF_MDLOG:-$HOME/work/runs/lpscl_glass_md_2026_09_26/pilot600/T600/d0.00_cfg0/T600/md.log}
GPU_START_MAX=${GPU_START_MAX:-20000}; GPU_WAIT=${GPU_WAIT:-3600}; META_WAIT=${META_WAIT:-900}; POLL=${POLL:-60}; KILL_GRACE=${KILL_GRACE:-10}
DRY_RUN=${DRY_RUN:-0}
rec_of(){ local v="REC_$1"; [ -n "${!v:-}" ] && { echo "${!v}"; return; }      # relax 판 기록값 (gateA erratum 09-24)
  case "$1" in 1) echo "2.037 12 1.6212";; 2) echo "2.021 12 1.5782";; *) echo "";; esac; }
say(){ echo "[$(date '+%F %T')] $*"; }
gpu_total(){ nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits -i 0 2>/dev/null | head -1 | tr -d ' '; }
tree_pids(){ echo "$1"; local c; for c in $(pgrep -P "$1" 2>/dev/null); do tree_pids "$c"; done; }
kill_tree(){ local ps i=0; ps=$(tree_pids "$1"); kill -TERM $ps 2>/dev/null
  while [ "$i" -lt "$KILL_GRACE" ]; do kill -0 "$1" 2>/dev/null || break; sleep 1; i=$((i+1)); done; kill -KILL $ps 2>/dev/null; return 0; }
check_struct(){ "$PY" - "$1" $2 <<'PY'
import sys
import numpy as np
from ase.io import read
from ase.geometry import get_distances
f = sys.argv[1]; ps_rec = float(sys.argv[2]); n4_rec = int(sys.argv[3]); rho_rec = float(sys.argv[4])
try:
    fr = read(f, index=":")
except Exception as e:
    print(f"FAIL 읽기 {type(e).__name__}: {e}"); sys.exit(1)
if len(fr) != 1:
    print(f"FAIL 프레임 {len(fr)} 개 (단일 프레임이어야)"); sys.exit(1)
a = fr[0]
if len(a) != 120:
    print(f"FAIL 원자 {len(a)} (120 이어야)"); sys.exit(1)
sym = np.array(a.get_chemical_symbols())
if (sym == "P").sum() == 0 or (sym == "S").sum() == 0:
    print("FAIL P 또는 S 가 없다"); sys.exit(1)
_, D = get_distances(a.positions[sym == "P"], a.positions[sym == "S"], cell=a.cell, pbc=True)
ps = float(D.min()); nP = D.shape[0]; n4 = int(((D <= 2.6).sum(axis=1) == 4).sum())
rho = float(a.get_masses().sum() * 1.66053906660 / a.get_volume())
ok = abs(ps - ps_rec) <= 0.003 and n4 == n4_rec and abs(rho - rho_rec) <= 0.001
print(f"{'OK' if ok else 'FAIL'} · 최단 P–S {ps:.4f} (기록 {ps_rec} ±0.003) · PS₄ {n4}/{nP} (기록 {n4_rec}) · ρ {rho:.4f} (기록 {rho_rec} ±0.001)")
sys.exit(0 if ok else 1)
PY
}
# run_meta — 기준(600 K 파일럿 = 같은 드라이버·같은 명령 틀) 과 **그리고** gabia 본 런의 값(상수) 둘 다와 같아야 한다 (T·seed·v0 만 다름)
check_meta(){ python3 - "$REF_META" "$1" "$2" "$3" "$4" <<'PY'
import json, sys
ref = json.load(open(sys.argv[1])); new = json.load(open(sys.argv[2])) if sys.argv[2] != "-" else None
T, S, X = float(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
keys = ("n_atoms", "supercell", "prod_ps", "equilib_ps", "fit_window_ps", "save_traj", "uma_model", "uma_inference_mode_requested")
main = {"n_atoms": 120, "supercell": [1, 1, 1], "prod_ps": 400.0, "equilib_ps": 5.0, "fit_window_ps": [2.0, 50.0],
        "save_traj": True, "uma_model": "uma-s-1p1", "uma_inference_mode_requested": "turbo"}
bad = [f"기준 {k} {ref.get(k)!r} ≠ 본 런 {main[k]!r}" for k in keys if ref.get(k) != main[k]]
if new is not None:
    bad += [f"{k} {main[k]!r}→{new.get(k)!r}" for k in keys if new.get(k) != main[k]]
    if [float(t) for t in new.get("temperatures", [])] != [T]: bad.append(f"temperatures {new.get('temperatures')!r}")
    if new.get("seed") != S: bad.append(f"seed {new.get('seed')!r}")
    if new.get("v0_xyz") != X: bad.append(f"v0_xyz {new.get('v0_xyz')!r}")
msg = "기준 run_meta = gabia 본 런 설정" if new is None else "run_meta = 본 런 설정 (T·seed·v0 만 다름)"
print(f"OK {msg}" if not bad else "FAIL " + " · ".join(bad))
sys.exit(1 if bad else 0)
PY
}
dt_of(){ awk 'NR==2{a=$1} NR==3{printf "%.4f", $1-a; exit}' "$1" 2>/dev/null; }

mkdir -p "$ROOT/logs"
[ "$DRY_RUN" = 1 ] || exec > >(tee -a "$ROOT/queue_kgy.log") 2>&1
[ "$DRY_RUN" = 1 ] && say "DRY_RUN — 검사만 하고 띄우지 않는다" || say "▶ 큐 시작 · $QUEUE"
if [ "$DRY_RUN" != 1 ]; then exec 9>"$ROOT/.queue_kgy.lock"; flock -n 9 || { say "⛔ 이미 실행 중 (flock)"; exit 10; }; fi
s=$(sha256sum "$DRV" 2>/dev/null | cut -c1-16)
[ "$s" = "$DRV_SHA16" ] && say "드라이버 sha16 $s ✅" || { say "⛔ 드라이버 sha16 ${s:-없음} ≠ $DRV_SHA16"; exit 7; }
check_meta - 0 0 x > /tmp/.kgyq_ref.txt; rc=$?; say "$(cat /tmp/.kgyq_ref.txt)"; [ $rc = 0 ] || exit 9
RDT=$(dt_of "$REF_MDLOG"); say "기준 md.log dt $RDT ps/행"; [ -n "$RDT" ] || { say "⛔ 기준 md.log dt 를 못 읽었다"; exit 9; }
for q in $QUEUE; do T=${q%%:*}; S=${q##*:}; X=$A/seed$S/final.xyz; R=$(rec_of "$S")
  [ -n "$R" ] || { say "⛔ seed$S 기록값 없음"; exit 8; }
  r=$(check_struct "$X" "$R"); st=$?; say "seed$S 구조 $r"; [ $st = 0 ] || exit 8
  [ -e "$ROOT/seed$S/T$T" ] && { say "⛔ $ROOT/seed$S/T$T 가 이미 있다 — 덮지 않는다"; exit 11; }
done
say "GPU 지금 $(gpu_total) MiB (시작 문턱 ≤ $GPU_START_MAX)"
if [ "$DRY_RUN" = 1 ]; then for q in $QUEUE; do T=${q%%:*}; S=${q##*:}
  say "계획 T$T seed$S → $ROOT/seed$S/T$T · $PY $(basename "$DRV") --v0_xyz $A/seed$S/final.xyz --label lpscl_glass_main_s${S}_T${T} --temperatures $T --seed $S --equilib_ps 5 --prod_ps 400 --turbo"; done
  say "DRY_RUN 끝 — 위가 전부 OK/✅ 면 발사해도 된다"; exit 0; fi

for q in $QUEUE; do T=${q%%:*}; S=${q##*:}; X=$A/seed$S/final.xyz; OUT=$ROOT/seed$S/T$T; L=$ROOT/logs/s${S}_T${T}.log
  w=0; while g=$(gpu_total); [ -n "$g" ] && [ "$g" -gt "$GPU_START_MAX" ]; do
    [ "$w" -ge "$GPU_WAIT" ] && { say "⛔ GPU $g MiB > $GPU_START_MAX 가 ${GPU_WAIT}s 계속 — 멈춘다"; exit 12; }
    say "대기 · GPU $g MiB > $GPU_START_MAX"; sleep "$POLL"; w=$((w+POLL)); done
  r=$(check_struct "$X" "$(rec_of "$S")"); st=$?; say "T$T seed$S 구조 $r"; [ $st = 0 ] || exit 8
  [ -e "$OUT" ] && { say "⛔ $OUT 가 이미 있다"; exit 11; }
  mkdir -p "$ROOT/seed$S"
  "$PY" "$DRV" --v0_xyz "$X" --supercell 1 1 1 --label "lpscl_glass_main_s${S}_T${T}" --out_root "$OUT" \
      --disorder_levels 0 --n_configs 1 --temperatures "$T" --equilib_ps 5 --prod_ps 400 --timestep_fs 2 \
      --friction 0.02 --fit_window_ps 2 50 --save_traj --seed "$S" --turbo --device cuda > "$L" 2>&1 &
  PID=$!; say "▶ T$T seed$S PID $PID · 시작 전 GPU ${g:-?} MiB · 로그 $L"
  w=0; while [ ! -f "$OUT/run_meta.json" ]; do kill -0 $PID 2>/dev/null || break
    [ "$w" -ge "$META_WAIT" ] && { say "⛔ run_meta.json 이 ${META_WAIT}s 안에 안 생겼다"; kill_tree $PID; exit 9; }; sleep 5; w=$((w+5)); done
  if [ -f "$OUT/run_meta.json" ]; then m=$(check_meta "$OUT/run_meta.json" "$T" "$S" "$X"); st=$?; say "  $m"; [ $st = 0 ] || { kill_tree $PID; exit 9; }; fi
  MD=$OUT/d0.00_cfg0/T$T/md.log; w=0
  while kill -0 $PID 2>/dev/null && [ "$(awk 'END{print NR}' "$MD" 2>/dev/null || echo 0)" -lt 3 ]; do
    [ "$w" -ge "$META_WAIT" ] && { say "⛔ md.log 가 ${META_WAIT}s 안에 3 행이 안 됐다"; kill_tree $PID; exit 9; }; sleep 5; w=$((w+5)); done
  if [ "$(awk 'END{print NR}' "$MD" 2>/dev/null || echo 0)" -ge 3 ]; then d=$(dt_of "$MD")
    [ "$d" = "$RDT" ] && say "  dt = 기준과 같다 ($d ps/행)" || { say "⛔ dt $d ≠ 기준 $RDT"; kill_tree $PID; exit 9; }
  else say "  ⚠ md.log 가 3 행이 안 된 채 드라이버가 멈췄다 — dt 를 못 쟀다 (아래 msd.json 검사로 간다)"; fi
  wait $PID; rc=$?
  [ -f "$OUT/d0.00_cfg0/T$T/msd.json" ] || { say "⛔ T$T seed$S 가 msd.json 없이 끝났다 (rc $rc · 로그 $L)"; exit 4; }
  say "✅ T$T seed$S 끝 (rc $rc)"
done
say "■ 큐 끝 · $QUEUE"; exit 0
