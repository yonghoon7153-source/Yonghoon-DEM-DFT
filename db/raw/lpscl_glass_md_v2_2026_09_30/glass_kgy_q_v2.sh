#!/bin/bash
# =============================================================================
# glass_kgy_q_v2.sh — li2s 소셀 유리 MD **v2 카드 (잠정)** 첫 묶음의 kgy 몫을 한 번에 하나씩
#   카드 db/properties/lpscl_smallcell_glass_md_v2_estimand_2026_09_30.json (결정 D-2026-09-30-lpscl-smallcell-glass-md-v2 · proposed)
#   ⛔ 트랙 li2s = 외부 1저자. 사용자 '이거 gabia, kgy에서 더하자' (09-30) 는 **실행 승인**이다 — 카드 규칙은 잠정이고
#      외부 1저자 동의(편지 CO) 전까지 결과를 보지 않는다 (results_seen false).
#
# 출발점: db/raw/lpscl_glass_md_main_2026_09_28/glass_kgy_q_0929.sh (sha16 ad75ffc7e09c7d29 · 09-29 kgy 3 런) — 그 파일은
#   원자료 기록이라 고치지 않고, 같은 과학 검사 셋(구조 값 게이트 · run_meta 동일성 · md.log dt)에 v2 만 더했다:
#   · 큐 항목 T:seed[:prod] (prod 없으면 PROD_DEFAULT 400) — run_meta prod_ps 가 그 값이어야 한다.
#   · VSEED_OFFSET (기본 1000) — 드라이버 --seed = 1000 + 구조 시드 → MD 난수 = --seed + T (드라이버 :580).
#     옛 런(--seed = 구조 시드)과 난수열이 겹치지 않는다. run_meta seed 가 그 값이어야 한다.
#   · 구조: seed1·2 = kgy 담금질 $A/seed<S>/final.xyz · seed3·4·5 = gabia 담금질을 옮긴 $INIT/seed<S>_final.xyz
#     (없으면 **시작하지 않는다** — 옮기고 다시 띄운다). 구조는 이름이 아니라 **값**으로 가린다 (기록값 = gabia 러너와 같다).
#   · 라벨 = <LABEL_PREFIX>_s<S>_T<T> (기본 lpscl_glass_v2).
#   · 내장 --selftest (가짜 nvidia-smi · 가짜 드라이버 · 음성 포함) — 09-29 판은 로컬 음성 9 종을 따로 돌렸다.
#
# 쓰는 법 (kgy)
#   bash glass_kgy_q_v2.sh --selftest            # SELFTEST_PY=<numpy·ase 있는 python> 필요 (기본 = PY)
#   DRY_RUN=1 bash glass_kgy_q_v2.sh             # 드라이버 sha · 기준 설정 · 구조 판별 · 계획만
#   bash glass_kgy_q_v2.sh                       # tmux 안에서
#
# 멈춤 코드: 0 큐 끝 · 4 msd.json 없이 끝남 · 7 드라이버 sha · 8 구조 (없음·값 다름) · 9 설정(run_meta·dt) · 10 이미 실행 중
#            · 11 out_root 이미 있음 · 12 GPU 대기 초과 · 13 큐 항목 형식 오류
#
# ⛔ 이 러너가 **못 하는 것**
#   · 프로세스별 VRAM 가드 (kgy 는 nvidia-smi 프로세스 정보가 막혀 있다) · 합계 기준 시작 문턱만 있다.
#   · gabia 공존 예외를 확인하지 않는다 (kgy 는 그 예외 밖이다 — cascade 와 GPU 를 나눠 쓴다).
#   · 구조를 옮기지 않는다 (사람이 옮긴다) · 결과(D·β·C1·C2)를 판정하지 않는다 — 판독은 msd_diffusive_check.py.
#   · 끊긴 런을 이어 돌리지 않는다 — out_root 가 있으면 멈춘다 (11). 사람이 흔적을 보존하고 지운 뒤 다시 띄운다.
# =============================================================================
set -u
ROOT=${ROOT:-$HOME/work/runs/lpscl_glass_md_v2_2026_09_30}
PY=${PY:-/home/kgy/apps/miniforge3/envs/uma/bin/python}
DRV=${DRV:-$HOME/li2s_glass_src/tools/modelc_v3/disorder_ensemble_diffusion.py}
DRV_SHA16=${DRV_SHA16:-c3e2d358ee53cefa}
QUEUE=${QUEUE:-"600:1:400 550:2:800 600:3:400 550:4:800 550:5:800"}   # 카드 v2 기계 배정 (kgy 몫)
A=${A:-$HOME/work/runs/lpscl_smallcell_2026_09_16/A}
INIT=${INIT:-$ROOT/init}
REF_META=${REF_META:-$HOME/work/runs/lpscl_glass_md_2026_09_26/pilot600/T600/run_meta.json}
REF_MDLOG=${REF_MDLOG:-$HOME/work/runs/lpscl_glass_md_2026_09_26/pilot600/T600/d0.00_cfg0/T600/md.log}
PROD_DEFAULT=${PROD_DEFAULT:-400}; VSEED_OFFSET=${VSEED_OFFSET:-1000}; LABEL_PREFIX=${LABEL_PREFIX:-lpscl_glass_v2}
GPU_START_MAX=${GPU_START_MAX:-20000}; GPU_WAIT=${GPU_WAIT:-3600}; META_WAIT=${META_WAIT:-900}; POLL=${POLL:-60}; KILL_GRACE=${KILL_GRACE:-10}
DRY_RUN=${DRY_RUN:-0}
rec_of(){ local v="REC_$1"; [ -n "${!v:-}" ] && { echo "${!v}"; return; }      # relax 판 기록값 (gateA erratum 09-24 · amendment_ch 09-28)
  case "$1" in 1) echo "2.037 12 1.6212";; 2) echo "2.021 12 1.5782";; 3) echo "2.0055 12 1.5933";;
               4) echo "2.0324 12 1.591";; 5) echo "2.030 11 1.6181";; *) echo "";; esac; }
struct_of(){ case "$1" in 1|2) echo "$A/seed$1/final.xyz";; *) echo "$INIT/seed$1_final.xyz";; esac; }
parse_q(){ local r n; QT=${1%%:*}; r=${1#*:}; QS=${r%%:*}; QP=$PROD_DEFAULT
  n=$(printf '%s' "$1" | tr -cd ':' | wc -c)
  [ "$n" = 1 ] || [ "$n" = 2 ] || return 1
  [ "$n" = 2 ] && QP=${r#*:}
  [[ "$QT" =~ ^[0-9]+$ ]] && [[ "$QS" =~ ^[0-9]+$ ]] && [[ "$QP" =~ ^[0-9]+([.][0-9]+)?$ ]] || return 1
  QV=$((VSEED_OFFSET + QS)); return 0; }
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
# run_meta — 기준(600 K 파일럿 = 같은 드라이버·같은 명령 틀) 과 **그리고** 본 런 상수 둘 다와 같아야 한다.
#   다른 것은 T · seed(= VSEED_OFFSET + 구조 시드) · v0 · prod(큐가 준 값) 뿐이다.
check_meta(){ python3 - "$REF_META" "$1" "$2" "$3" "$4" "${5:-$PROD_DEFAULT}" <<'PY'
import json, sys
ref = json.load(open(sys.argv[1])); new = json.load(open(sys.argv[2])) if sys.argv[2] != "-" else None
T, S, X, P = float(sys.argv[3]), int(sys.argv[4]), sys.argv[5], float(sys.argv[6])
keys = ("n_atoms", "supercell", "equilib_ps", "fit_window_ps", "save_traj", "uma_model", "uma_inference_mode_requested")
main = {"n_atoms": 120, "supercell": [1, 1, 1], "equilib_ps": 5.0, "fit_window_ps": [2.0, 50.0],
        "save_traj": True, "uma_model": "uma-s-1p1", "uma_inference_mode_requested": "turbo"}
bad = [f"기준 {k} {ref.get(k)!r} ≠ 본 런 {main[k]!r}" for k in keys if ref.get(k) != main[k]]
if new is not None:
    bad += [f"{k} {main[k]!r}→{new.get(k)!r}" for k in keys if new.get(k) != main[k]]
    try:
        p_ok = float(new.get("prod_ps")) == P
    except (TypeError, ValueError):
        p_ok = False
    if not p_ok: bad.append(f"prod_ps {new.get('prod_ps')!r} ≠ 큐 {P:g}")
    if [float(t) for t in new.get("temperatures", [])] != [T]: bad.append(f"temperatures {new.get('temperatures')!r}")
    if new.get("seed") != S: bad.append(f"seed {new.get('seed')!r} ≠ {S}")
    if new.get("v0_xyz") != X: bad.append(f"v0_xyz {new.get('v0_xyz')!r}")
msg = "기준 run_meta = 본 런 설정" if new is None else f"run_meta = 본 런 설정 (T·seed·v0·prod 만 다름 · prod {P:g} · seed {S})"
print(f"OK {msg}" if not bad else "FAIL " + " · ".join(bad))
sys.exit(1 if bad else 0)
PY
}
dt_of(){ awk 'NR==2{a=$1} NR==3{printf "%.4f", $1-a; exit}' "$1" 2>/dev/null; }

# ── selftest (음성 포함) ────────────────────────────────────────────────────────
if [ "${1:-}" = "--selftest" ]; then
  SPY=${SELFTEST_PY:-$PY}; T=$(mktemp -d); f=0; SELF=$(realpath "$0")
  ck(){ if [ "$2" = "$3" ]; then echo "  ✔ $1"; else echo "  ✘ $1 — 기대 [$3] · 실제 [$2]"; f=1; fi; }
  mkdir -p "$T/bin" "$T/A/seed1" "$T/A/seed2" "$T/root/init"; echo 3000 > "$T/gpu"
  printf '#!/bin/bash\ncat "%s"\n' "$T/gpu" > "$T/bin/nvidia-smi"; chmod +x "$T/bin/nvidia-smi"
  cat > "$T/drv.py" <<'EOF'
import json, os, sys, time, argparse
ap = argparse.ArgumentParser()
for k in ("--v0_xyz", "--label", "--out_root", "--device", "--friction", "--timestep_fs", "--equilib_ps", "--prod_ps"):
    ap.add_argument(k)
ap.add_argument("--supercell", nargs=3); ap.add_argument("--disorder_levels", nargs="+"); ap.add_argument("--n_configs")
ap.add_argument("--temperatures", nargs="+"); ap.add_argument("--fit_window_ps", nargs=2); ap.add_argument("--seed", type=int)
ap.add_argument("--save_traj", action="store_true"); ap.add_argument("--turbo", action="store_true")
a = ap.parse_args(); E = os.environ; T = float(a.temperatures[0])
os.makedirs(a.out_root, exist_ok=True)
json.dump({"label": a.label, "n_atoms": 120, "supercell": [1, 1, 1], "v0_xyz": a.v0_xyz, "temperatures": [T],
           "prod_ps": float(E.get("FAKE_PROD", a.prod_ps)), "equilib_ps": 5.0, "seed": int(E.get("FAKE_SEED", a.seed)),
           "fit_window_ps": [2.0, 50.0], "save_traj": True, "uma_model": "uma-s-1p1",
           "uma_inference_mode_requested": "turbo"}, open(os.path.join(a.out_root, "run_meta.json"), "w"))
d = os.path.join(a.out_root, "d0.00_cfg0", f"T{int(T)}"); os.makedirs(d, exist_ok=True)
dt = float(E.get("FAKE_DT", "0.002"))
with open(os.path.join(d, "md.log"), "a") as fh:
    fh.write("Time[ps]      Etot[eV]     Epot[eV]     Ekin[eV]    T[K]\n")
    for i in range(3): fh.write(f"{i*dt:<10.4f} -1.0 -1.0 0.0 {T}\n")
if E.get("FAKE_CRASH"):
    print("RuntimeError: something else"); sys.exit(1)
time.sleep(float(E.get("FAKE_SLEEP", "1")))
json.dump({"T_K": T, "D_Li_cm2_s": 1e-6}, open(os.path.join(d, "msd.json"), "w"))
EOF
  DSHA=$(sha256sum "$T/drv.py" | cut -c1-16)
  "$SPY" - "$T" <<'PY' || { echo "  ✘ 픽스처 생성 실패 (numpy·ase 필요 — SELFTEST_PY)"; exit 1; }
import sys, numpy as np
from ase import Atoms
from ase.io import write
T = sys.argv[1]
def make(first_ps):
    pos, sym = [], []
    tet = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]) / np.sqrt(3)
    k = 0
    for i in range(3):
        for j in range(2):
            for m in range(2):
                c = np.array([4 + 8 * i, 4 + 8 * j, 4 + 8 * m], float)
                pos.append(c); sym.append("P")
                for t_i, t in enumerate(tet):
                    pos.append(c + (first_ps if (k == 0 and t_i == 0) else 2.05) * t); sym.append("S")
                k += 1
    for q in range(60):
        pos.append([2.0 + 4.0 * (q % 6), 0.3, 0.8 + 1.5 * (q // 6)]); sym.append("Li")
    return Atoms(sym, positions=pos, cell=[24, 16, 16], pbc=True)
good = make(2.030)
for s in (1, 2):
    write(f"{T}/A/seed{s}/final.xyz", good, format="extxyz")
for s in (3, 4, 5):
    write(f"{T}/root/init/seed{s}_final.xyz", good, format="extxyz")
write(f"{T}/off.xyz", make(2.040), format="extxyz")
open(f"{T}/rho", "w").write(f"{good.get_masses().sum() * 1.66053906660 / good.get_volume():.4f}")
PY
  RHO=$(cat "$T/rho"); REC="2.030 12 $RHO"
  printf '%s' '{"label":"lpscl_glass_pilot600","n_atoms":120,"supercell":[1,1,1],"prod_ps":400.0,"equilib_ps":5.0,"fit_window_ps":[2.0,50.0],"save_traj":true,"uma_model":"uma-s-1p1","uma_inference_mode_requested":"turbo","temperatures":[600.0],"seed":1,"v0_xyz":"x"}' > "$T/ref_meta.json"
  printf 'Time[ps]  Etot\n0.0000 -1\n0.0020 -1\n' > "$T/ref_md.log"
  run(){ ( timeout 60 env ROOT="$T/root" PY="$SPY" DRV="$T/drv.py" DRV_SHA16="$DSHA" A="$T/A" INIT="$T/root/init" \
      REF_META="$T/ref_meta.json" REF_MDLOG="$T/ref_md.log" POLL=1 GPU_WAIT=3 META_WAIT=20 KILL_GRACE=2 \
      REC_1="$REC" REC_2="$REC" REC_3="$REC" REC_4="$REC" REC_5="$REC" PATH="$T/bin:$PATH" "$@" bash "$SELF" > "$T/out" 2>&1 ); echo $?; }
  ck "양성: 두 런 끝까지 (600:3:400 · 550:4:800) (0)" "$(run QUEUE='600:3:400 550:4:800')" 0
  ck "양성: msd.json 둘"                              "$(ls "$T"/root/seed3/T600/d0.00_cfg0/T600/msd.json "$T"/root/seed4/T550/d0.00_cfg0/T550/msd.json 2>/dev/null | wc -l)" 2
  ck "양성: 550:4 run_meta = prod 800 · seed 1004 · 라벨 · v0 = INIT" \
     "$(python3 -c "import json;m=json.load(open('$T/root/seed4/T550/run_meta.json'));print(m['prod_ps'],m['seed'],m['label'],m['v0_xyz'].endswith('init/seed4_final.xyz'))")" \
     "800.0 1004 lpscl_glass_v2_s4_T550 True"
  ck "양성: seed1 은 kgy 담금질 폴더 A 에서" \
     "$(run QUEUE='600:1:400' >/dev/null; python3 -c "import json;print(json.load(open('$T/root/seed1/T600/run_meta.json'))['v0_xyz'].endswith('A/seed1/final.xyz'))")" True
  ck "⛔음성 out_root 이미 있음 → 11"                  "$(run QUEUE='600:3:400')" 11
  ck "⛔음성 드라이버 sha 다름 → 7"                    "$(run QUEUE='600:2:400' DRV_SHA16=0000000000000000)" 7
  cp "$T/root/init/seed5_final.xyz" "$T/seed5.keep"; cp "$T/off.xyz" "$T/root/init/seed5_final.xyz"
  ck "⛔음성 구조 값 다름 (최단 P–S +0.010) → 8"       "$(run QUEUE='550:5:800')" 8
  rm -f "$T/root/init/seed5_final.xyz"
  ck "⛔음성 구조 없음 → 8 (조용히 건너뛰지 않는다)"   "$(run QUEUE='550:5:800')" 8
  cp "$T/seed5.keep" "$T/root/init/seed5_final.xyz"
  ck "⛔음성 run_meta prod 400 ≠ 큐 800 → 9"           "$(run QUEUE='550:5:800' FAKE_PROD=400 FAKE_SLEEP=20)" 9
  rm -rf "$T/root/seed5"
  ck "⛔음성 run_meta seed 5 ≠ 1005 → 9"               "$(run QUEUE='550:5:800' FAKE_SEED=5 FAKE_SLEEP=20)" 9
  rm -rf "$T/root/seed5"
  ck "⛔음성 dt 1 fs ≠ 기준 2 fs → 9"                   "$(run QUEUE='550:5:800' FAKE_DT=0.001 FAKE_SLEEP=20)" 9
  rm -rf "$T/root/seed5"
  ck "⛔음성 msd.json 없이 끝남 → 4"                   "$(run QUEUE='550:5:800' FAKE_CRASH=1)" 4
  rm -rf "$T/root/seed5"
  ck "⛔음성 큐 형식 (550:5:800:1) → 13"               "$(run QUEUE='550:5:800:1')" 13
  ck "⛔음성 큐 형식 (550:x) → 13"                     "$(run QUEUE='550:x')" 13
  printf '%s' '{"label":"x","n_atoms":120,"supercell":[1,1,1],"prod_ps":400.0,"equilib_ps":5.0,"fit_window_ps":[2.0,50.0],"save_traj":true,"uma_model":"uma-s-1p1","uma_inference_mode_requested":"default","temperatures":[600.0],"seed":1,"v0_xyz":"x"}' > "$T/ref_bad.json"
  ck "⛔음성 기준 run_meta 가 본 런 설정과 다름 (default 모드) → 9" "$(run QUEUE='550:5:800' REF_META="$T/ref_bad.json")" 9
  echo 25000 > "$T/gpu"
  ck "⛔음성 GPU 합계가 문턱 위로 계속 → 12"            "$(run QUEUE='550:5:800')" 12
  echo 3000 > "$T/gpu"; rm -rf "$T/root/seed5"
  ( flock -x 9; sleep 6 ) 9>"$T/root/.queue_kgy.lock" & sleep 1
  ck "⛔음성 큐가 이미 돌면 (lock) → 10"                "$(run QUEUE='550:5:800')" 10
  wait
  ck "DRY_RUN 은 띄우지 않는다 (0 · 새 폴더 0)"        "$(run QUEUE='550:5:800' DRY_RUN=1)/$(ls -d "$T"/root/seed5/T550 2>/dev/null | wc -l)" 0/0
  rm -rf "$T"; [ "$f" = 0 ] && echo "selftest ✅ (음성 13 포함)" || echo "selftest ⛔"; exit "$f"
fi

# ── 본 실행 ────────────────────────────────────────────────────────────────────
mkdir -p "$ROOT/logs"
[ "$DRY_RUN" = 1 ] || exec > >(tee -a "$ROOT/queue_kgy.log") 2>&1
[ "$DRY_RUN" = 1 ] && say "DRY_RUN — 검사만 하고 띄우지 않는다" || say "▶ v2 큐 시작 · $QUEUE"
if [ "$DRY_RUN" != 1 ]; then exec 9>"$ROOT/.queue_kgy.lock"; flock -n 9 || { say "⛔ 이미 실행 중 (flock)"; exit 10; }; fi
s=$(sha256sum "$DRV" 2>/dev/null | cut -c1-16)
[ "$s" = "$DRV_SHA16" ] && say "드라이버 sha16 $s ✅" || { say "⛔ 드라이버 sha16 ${s:-없음} ≠ $DRV_SHA16"; exit 7; }
REFTXT=$(mktemp); check_meta - 0 0 x > "$REFTXT"; rc=$?; say "$(cat "$REFTXT")"; rm -f "$REFTXT"; [ $rc = 0 ] || exit 9
RDT=$(dt_of "$REF_MDLOG"); say "기준 md.log dt $RDT ps/행"; [ -n "$RDT" ] || { say "⛔ 기준 md.log dt 를 못 읽었다"; exit 9; }
for q in $QUEUE; do
  parse_q "$q" || { say "⛔ 큐 항목 형식 오류 '$q' (T:seed[:prod] · 숫자)"; exit 13; }
  T=$QT; S=$QS; X=$(struct_of "$S"); R=$(rec_of "$S")
  [ -n "$R" ] || { say "⛔ seed$S 기록값 없음"; exit 8; }
  [ -s "$X" ] || { say "⛔ seed$S 구조 없음 ($X) — 옮기고 다시 띄운다"; exit 8; }
  r=$(check_struct "$X" "$R"); st=$?; say "seed$S 구조 $r"; [ $st = 0 ] || exit 8
  [ -e "$ROOT/seed$S/T$T" ] && { say "⛔ $ROOT/seed$S/T$T 가 이미 있다 — 덮지 않는다"; exit 11; }
done
say "GPU 지금 $(gpu_total) MiB (시작 문턱 ≤ $GPU_START_MAX)"
if [ "$DRY_RUN" = 1 ]; then for q in $QUEUE; do parse_q "$q"
  say "계획 T$QT seed$QS → $ROOT/seed$QS/T$QT · $(basename "$DRV") --v0_xyz $(struct_of "$QS") --label ${LABEL_PREFIX}_s${QS}_T${QT} --temperatures $QT --seed $QV --equilib_ps 5 --prod_ps $QP --turbo"; done
  say "DRY_RUN 끝 — 위가 전부 OK/✅ 면 발사해도 된다"; exit 0; fi

for q in $QUEUE; do parse_q "$q"; T=$QT; S=$QS; PR=$QP; VS=$QV; X=$(struct_of "$S"); OUT=$ROOT/seed$S/T$T; L=$ROOT/logs/s${S}_T${T}.log
  w=0; while g=$(gpu_total); [ -n "$g" ] && [ "$g" -gt "$GPU_START_MAX" ]; do
    [ "$w" -ge "$GPU_WAIT" ] && { say "⛔ GPU $g MiB > $GPU_START_MAX 가 ${GPU_WAIT}s 계속 — 멈춘다"; exit 12; }
    say "대기 · GPU $g MiB > $GPU_START_MAX"; sleep "$POLL"; w=$((w+POLL)); done
  r=$(check_struct "$X" "$(rec_of "$S")"); st=$?; say "T$T seed$S 구조 $r"; [ $st = 0 ] || exit 8
  [ -e "$OUT" ] && { say "⛔ $OUT 가 이미 있다"; exit 11; }
  mkdir -p "$ROOT/seed$S"
  "$PY" "$DRV" --v0_xyz "$X" --supercell 1 1 1 --label "${LABEL_PREFIX}_s${S}_T${T}" --out_root "$OUT" \
      --disorder_levels 0 --n_configs 1 --temperatures "$T" --equilib_ps 5 --prod_ps "$PR" --timestep_fs 2 \
      --friction 0.02 --fit_window_ps 2 50 --save_traj --seed "$VS" --turbo --device cuda > "$L" 2>&1 &
  PID=$!; say "▶ T$T seed$S PID $PID · prod $PR ps · --seed $VS · 시작 전 GPU ${g:-?} MiB · 로그 $L"
  w=0; while [ ! -f "$OUT/run_meta.json" ]; do kill -0 $PID 2>/dev/null || break
    [ "$w" -ge "$META_WAIT" ] && { say "⛔ run_meta.json 이 ${META_WAIT}s 안에 안 생겼다"; kill_tree $PID; exit 9; }; sleep 5; w=$((w+5)); done
  if [ -f "$OUT/run_meta.json" ]; then m=$(check_meta "$OUT/run_meta.json" "$T" "$VS" "$X" "$PR"); st=$?; say "  $m"; [ $st = 0 ] || { kill_tree $PID; exit 9; }; fi
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
