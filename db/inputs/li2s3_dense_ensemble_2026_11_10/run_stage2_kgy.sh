#!/bin/bash
# =============================================================================
# run_stage2_kgy.sh — li2s-3 2 단계 (측정 온도 창) MD 를 kgy 에서 **한 번에 하나씩**
#   카드 db/properties/lpscl_glass_dense_protocol_ensemble_estimand_2026_11_10.json (결정 D-2026-11-10-li2s3-dense-protocol-ensemble)
#   두 계 (A a-Li₄PS₄Cl · B a-Li₃PS₄ · 120 원자 · 고정 밀도) × 구조 시드 11 · 12 × 600 / 650 / 700 / 750 K × 400 ps = 16 런.
#   순서 = 온도 블록 오름차순 · 블록 안에서 A11 → B11 → A12 → B12 (중간에 끊겨도 두 계가 같은 수).
#
# 이 파일은 **설정 · 문지기 · 순서 · 비용 장부**만 한다. MD 실행은 v2 kgy 러너
#   db/raw/lpscl_glass_md_v2_2026_09_30/glass_kgy_q_v2.sh (sha16 3aef029aced0de77 · 원자료라 고치지 않는다) 를 런마다 한 번씩 부른다
#   ⇒ 드라이버 sha16 · 구조 값 게이트 · run_meta 동일성 · md.log dt · GPU 시작 문턱을 옛 캠페인과 **같은 코드**로 건다.
#
# 문지기 (하나라도 어긋나면 시작하지 않는다 · 종료 코드)
#   6  카드 결정이 원장에서 active 가 아니다
#   7  v2 러너 sha16 ≠ 3aef029aced0de77
#   8  입력 구조 (li2s-2 담금질 final.xyz) 가 없거나 sha256 이 카드 기록과 다르다 · init 사본이 이미 있는데 바이트가 다르다
#   9  MD 설정 대조 기준 (run_meta · md.log) 이 없다
#   10 이 큐가 이미 돌고 있다 (flock)
#   13 모르는 PHASE
#   20 이미 있는 런 폴더가 끝나지 않았다 (msd.json 없음) — 사람이 흔적을 보존하고 정리한 뒤 다시 띄운다
#   21 첫 런 벽시계 > FIRST_RUN_MAX_H (카드 멈춤 규칙)   22 누적 + 다음 런 어림 > CAP_H (카드 상한)
#   그 밖은 러너의 종료 코드 (4 · 7 · 8 · 9 · 10 · 11 · 12 · 13) 를 그대로 낸다 — 그 자리에서 큐를 멈춘다.
#
# 쓰는 법 (kgy · repo worktree 안에서)
#   SELFTEST_PY=<numpy·ase 있는 python> bash db/inputs/li2s3_dense_ensemble_2026_11_10/run_stage2_kgy.sh --selftest
#   DRY_RUN=1 bash db/inputs/li2s3_dense_ensemble_2026_11_10/run_stage2_kgy.sh      # 검사만 (GPU 안 씀)
#   bash db/inputs/li2s3_dense_ensemble_2026_11_10/run_stage2_kgy.sh                # tmux 안에서
#   PHASE=cond550 bash …   # 조건부 550 K · 800 ps 4 런 — 16 런 판독에서 600 K 가 두 계 모두 측정 가능일 때만 (사람이 준다)
#
# ⛔ 이 파일이 못 하는 것
#   · 결과를 판정하지 않는다 (C1 · C2 · 골격 · W) — 판독 소비자는 따로다 (카드: 결과를 읽기 전에 커밋).
#   · 프로세스별 GPU 점유를 재지 못한다 — 비용 장부는 런의 벽시계다 (GPU 대기가 섞이면 넉넉하게 센다 · 상한에 보수적).
#   · 끊긴 런을 이어 돌리지 않는다 (20) · 끝난 런 (msd.json 있음) 은 건너뛴다.
#   · 조건부 550 K 를 스스로 정하지 않는다 (PHASE 는 사람이 준다).
# =============================================================================
set -u
HERE=$(cd "$(dirname "$(realpath "$0")")" && pwd)
REPO=${REPO:-$(cd "$HERE/../../.." && pwd)}
DECISIONS=${DECISIONS:-$REPO/db/governance/decisions.json}
CARD_DECISION=${CARD_DECISION:-D-2026-11-10-li2s3-dense-protocol-ensemble}
RUNNER=${RUNNER:-$REPO/db/raw/lpscl_glass_md_v2_2026_09_30/glass_kgy_q_v2.sh}
RUNNER_SHA16=${RUNNER_SHA16:-3aef029aced0de77}
PY=${PY:-/home/kgy/apps/miniforge3/envs/uma/bin/python}
DRV=${DRV:-$REPO/tools/modelc_v3/disorder_ensemble_diffusion.py}
DRV_SHA16=${DRV_SHA16:-c3e2d358ee53cefa}
SRC=${SRC:-$HOME/work/runs/li2s2_dense_1103}                    # li2s-2 담금질 뿌리 (읽기만)
BASE=${BASE:-$HOME/work/runs/li2s3_stage2_2026_11_10}
REF=${REF:-$HOME/work/runs/lpscl_glass_md_2026_09_26/pilot600/T600}   # MD 설정 대조 기준 (러너 기본과 같다 · 11-10 kgy 에 있음 확인)
REF_META=${REF_META:-$REF/run_meta.json}
REF_MDLOG=${REF_MDLOG:-$REF/d0.00_cfg0/T600/md.log}
PHASE=${PHASE:-ladder}
case "$PHASE" in
  ladder)  TEMPS=${TEMPS:-"600 650 700 750"}; PROD=${PROD:-400} ;;
  cond550) TEMPS=${TEMPS:-"550"}; PROD=${PROD:-800} ;;
  *) echo "⛔ PHASE=$PHASE — ladder · cond550 만 안다 (시작하지 않는다)"; exit 13 ;;
esac
SEEDS=${SEEDS:-"11 12"}                 # 카드: 두 계 공통 포함 시드 중 작은 둘
SYSTEMS=${SYSTEMS:-"A B"}
VSEED_OFFSET=${VSEED_OFFSET:-3000}      # 카드: --seed = 3000 + 구조 시드 (드라이버가 + T 를 더한다)
GPU_START_MAX=${GPU_START_MAX:-6000}    # esp 계정 그래픽 앱 바닥 ≈ 4,000 MiB 위에 우리 잡이 없을 때만 띄운다
CAP_H=${CAP_H:-160}                     # 카드 2 단계 상한 (조건부 포함 · 벽시계 합)
FIRST_RUN_MAX_H=${FIRST_RUN_MAX_H:-8}   # 카드 멈춤 규칙
DRY_RUN=${DRY_RUN:-0}
# 입력 기록 (kgy 읽기 블록 2026-11-10 16:47:29 · 카드 '입력') — final.xyz sha256 · 러너 값 게이트 기록값 '최단 P–S · PS₄ 개수 (2.6 Å) · 밀도'
SHA_A_11=${SHA_A_11:-ff7b8020b866b354e127c3c9c154fbc6a592e529568201ae3572aa9560c093e5}
SHA_A_12=${SHA_A_12:-ed442dcf7a575e4eeaf452744e895609dd03881809431e23cfcff651ca640e17}
SHA_B_11=${SHA_B_11:-506a9eaaa9a57138533c1c8b367cf2a2663ce9af651e6f802695738309ee9908}
SHA_B_12=${SHA_B_12:-e29f3ccd77b60c390382085eb8a5c40809935d086d9fa43ff88477fa1e0847ea}
REC_A_11=${REC_A_11:-"2.0260 11 1.9135"}
REC_A_12=${REC_A_12:-"2.0309 12 1.9135"}
REC_B_11=${REC_B_11:-"2.0231 15 1.8800"}
REC_B_12=${REC_B_12:-"2.0332 14 1.8800"}
LEDGER=$BASE/cost_ledger.tsv

say(){ echo "[$(date '+%F %T')] $*"; }
val(){ local n="$1"; echo "${!n:-}"; }
decision_state_of(){ python3 - "$DECISIONS" "$1" <<'PY'
import json, sys
try:
    D = json.load(open(sys.argv[1]))
except Exception:
    sys.exit(0)
L = D["decisions"] if isinstance(D, dict) else D
x = [e for e in L if e.get("id") == sys.argv[2]]
print(x[0].get("decision_state", "") if x else "")
PY
}
versions(){ "$PY" -c "import torch, ase; import fairchem.core as f; print('torch', torch.__version__, '· fairchem', getattr(f, '__version__', '?'), '· ase', ase.__version__)" 2>/dev/null | tail -1; }
cum_h(){ awk -F'\t' 'NR>1{s+=$7} END{printf "%.4f", s+0}' "$LEDGER" 2>/dev/null || echo 0; }
last_h(){ awk -F'\t' 'NR>1{h=$7} END{printf "%.4f", h+0}' "$LEDGER" 2>/dev/null || echo 0; }
n_rows(){ awk 'END{print (NR>1)?NR-1:0}' "$LEDGER" 2>/dev/null || echo 0; }
gt(){ awk -v a="$1" -v b="$2" 'BEGIN{exit !(a>b)}'; }

gatekeep(){
  local cs; cs=$(decision_state_of "$CARD_DECISION")
  [ "$cs" = active ] || { say "⛔ 카드 결정 $CARD_DECISION 가 원장 ($DECISIONS) 에서 active 가 아니다 (지금: ${cs:-없음}) — 시작하지 않는다"; return 6; }
  local s; s=$(sha256sum "$RUNNER" 2>/dev/null | cut -c1-16)
  [ "$s" = "$RUNNER_SHA16" ] || { say "⛔ v2 러너 sha16 ${s:-없음} ≠ $RUNNER_SHA16 ($RUNNER) — 시작하지 않는다"; return 7; }
  [ -s "$REF_META" ] && [ -s "$REF_MDLOG" ] || { say "⛔ MD 설정 대조 기준이 없다 — $REF_META · $REF_MDLOG"; return 9; }
  local x sd src dst want got
  for x in $SYSTEMS; do for sd in $SEEDS; do
    src=$SRC/$x/seed$sd/final.xyz; dst=$BASE/$x/init/seed${sd}_final.xyz; want=$(val "SHA_${x}_${sd}")
    [ -n "$want" ] || { say "⛔ $x seed$sd 의 sha256 기록이 없다 (카드 입력 밖의 시드)"; return 8; }
    [ -n "$(val "REC_${x}_${sd}")" ] || { say "⛔ $x seed$sd 의 값 게이트 기록값이 없다"; return 8; }
    [ -s "$src" ] || { say "⛔ 입력 구조가 없다 ($src)"; return 8; }
    got=$(sha256sum "$src" | cut -d' ' -f1)
    [ "$got" = "$want" ] || { say "⛔ $x seed$sd final.xyz sha256 $got ≠ 카드 기록 $want — 시작하지 않는다"; return 8; }
    if [ -e "$dst" ]; then cmp -s "$src" "$dst" || { say "⛔ $dst 가 이미 있는데 원본과 바이트가 다르다 — 덮지 않는다"; return 8; }
    else mkdir -p "$(dirname "$dst")" && cp "$src" "$dst" || { say "⛔ $x seed$sd 구조를 $dst 로 못 옮겼다"; return 8; }; fi
  done; done
  say "문지기 ✓ — 카드 $CARD_DECISION (active) · 러너 sha16 $s · 입력 구조 $(echo $SYSTEMS | wc -w) 계 × $(echo $SEEDS | wc -w) 시드 sha256 = 카드 기록"
  say "판 — $(versions || true) · repo $(git -C "$REPO" rev-parse --short=9 HEAD 2>/dev/null || echo '?') · BASE $BASE · PHASE $PHASE"
  return 0
}

run_one(){   # $1 계 · $2 온도 · $3 시드 → 러너 한 번 (큐 항목 하나)
  env ROOT="$BASE/$1" PY="$PY" DRV="$DRV" DRV_SHA16="$DRV_SHA16" QUEUE="$2:$3:$PROD" A="$BASE/$1/_unused" INIT="$BASE/$1/init" \
      REF_META="$REF_META" REF_MDLOG="$REF_MDLOG" LABEL_PREFIX="li2s3_$1" VSEED_OFFSET="$VSEED_OFFSET" GPU_START_MAX="$GPU_START_MAX" \
      REC_11="$(val "REC_${1}_11")" REC_12="$(val "REC_${1}_12")" DRY_RUN="$DRY_RUN" \
      ${POLL:+POLL="$POLL"} ${GPU_WAIT:+GPU_WAIT="$GPU_WAIT"} ${META_WAIT:+META_WAIT="$META_WAIT"} ${KILL_GRACE:+KILL_GRACE="$KILL_GRACE"} \
      bash "$RUNNER"
}

# ── selftest (음성 포함 · 실제 v2 러너 + 가짜 드라이버 · 가짜 nvidia-smi · 가짜 원장) ───────────────────────
if [ "${1:-}" = "--selftest" ]; then
  SPY=${SELFTEST_PY:-$PY}; T=$(mktemp -d); f=0; SELF=$(realpath "$0")
  ck(){ if [ "$2" = "$3" ]; then echo "  ✔ $1"; else echo "  ✘ $1 — 기대 [$3] · 실제 [$2]"; f=1; fi; }
  mkdir -p "$T/bin" "$T/ref/d0.00_cfg0/T600"
  printf '#!/bin/bash\necho 3000\n' > "$T/bin/nvidia-smi"; chmod +x "$T/bin/nvidia-smi"
  printf '%s' '{"decisions":[{"id":"D-CARD","decision_state":"active"},{"id":"D-PROP","decision_state":"proposed"}]}' > "$T/dec.json"
  printf '%s' '{"label":"ref","n_atoms":120,"supercell":[1,1,1],"prod_ps":400.0,"equilib_ps":5.0,"fit_window_ps":[2.0,50.0],"save_traj":true,"uma_model":"uma-s-1p1","uma_inference_mode_requested":"turbo","temperatures":[600.0],"seed":1,"v0_xyz":"x"}' > "$T/ref/run_meta.json"
  printf 'Time[ps]  Etot\n0.0000 -1\n0.0020 -1\n' > "$T/ref/d0.00_cfg0/T600/md.log"
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
           "prod_ps": float(a.prod_ps), "equilib_ps": 5.0, "seed": int(a.seed), "fit_window_ps": [2.0, 50.0],
           "save_traj": True, "uma_model": "uma-s-1p1", "uma_inference_mode_requested": "turbo"},
          open(os.path.join(a.out_root, "run_meta.json"), "w"))
d = os.path.join(a.out_root, "d0.00_cfg0", f"T{int(T)}"); os.makedirs(d, exist_ok=True)
with open(os.path.join(d, "md.log"), "a") as fh:
    fh.write("Time[ps]      Etot[eV]\n")
    for i in range(3): fh.write(f"{i*0.002:<10.4f} -1.0\n")
if E.get("FAKE_CRASH"):
    sys.exit(1)
time.sleep(float(E.get("FAKE_SLEEP", "0.2")))
json.dump({"T_K": T}, open(os.path.join(d, "msd.json"), "w"))
EOF
  DSHA=$(sha256sum "$T/drv.py" | cut -c1-16)
  "$SPY" - "$T" <<'PY' || { echo "  ✘ 픽스처 생성 실패 (numpy·ase 필요 — SELFTEST_PY)"; exit 1; }
import sys, numpy as np
from ase import Atoms
from ase.io import write
T = sys.argv[1]
pos, sym = [], []
tet = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]) / np.sqrt(3)
for i in range(3):
    for j in range(2):
        for m in range(2):
            c = np.array([4 + 8 * i, 4 + 8 * j, 4 + 8 * m], float)
            pos.append(c); sym.append("P")
            for t in tet:
                pos.append(c + 2.030 * t); sym.append("S")
for q in range(60):
    pos.append([2.0 + 4.0 * (q % 6), 0.3, 0.8 + 1.5 * (q // 6)]); sym.append("Li")
a = Atoms(sym, positions=pos, cell=[24, 16, 16], pbc=True)
import os
for x in ("A", "B"):
    for s in (11, 12):
        os.makedirs(f"{T}/src/{x}/seed{s}", exist_ok=True)
        write(f"{T}/src/{x}/seed{s}/final.xyz", a, format="extxyz")
open(f"{T}/rho", "w").write(f"{a.get_masses().sum() * 1.66053906660 / a.get_volume():.4f}")
PY
  RHO=$(cat "$T/rho"); REC="2.030 12 $RHO"; SH=$(sha256sum "$T/src/A/seed11/final.xyz" | cut -d' ' -f1)
  run(){ ( timeout 240 env -i HOME="$T/home" PATH="$T/bin:$PATH" REPO="$REPO" DECISIONS="$T/dec.json" CARD_DECISION=D-CARD PY="$SPY" DRV="$T/drv.py" DRV_SHA16="$DSHA" \
      SRC="$T/src" REF="$T/ref" SHA_A_11="$SH" SHA_A_12="$SH" SHA_B_11="$SH" SHA_B_12="$SH" REC_A_11="$REC" REC_A_12="$REC" REC_B_11="$REC" REC_B_12="$REC" \
      POLL=1 GPU_WAIT=3 META_WAIT=30 KILL_GRACE=2 TEMPS=600 "$@" bash "$SELF" > "$T/out" 2>&1 ); echo $?; }
  ck "양성: 한 온도 블록 네 런 끝까지 (0)"                 "$(run BASE="$T/b1")" 0
  ck "양성: 순서 A11 → B11 → A12 → B12 (장부)"              "$(awk -F'\t' 'NR>1{printf "%s%s ", $1, $3}' "$T/b1/cost_ledger.tsv")" "A11 B11 A12 B12 "
  ck "양성: msd.json 넷"                                    "$(ls "$T"/b1/[AB]/seed1[12]/T600/d0.00_cfg0/T600/msd.json 2>/dev/null | wc -l)" 4
  ck "양성: run_meta seed = 3000 + 시드 · prod 400 · 라벨"  "$(python3 -c "import json;m=json.load(open('$T/b1/B/seed12/T600/run_meta.json'));print(m['seed'],m['prod_ps'],m['label'])")" "3012 400.0 li2s3_B_s12_T600"
  ck "다시 띄우면 끝난 런은 건너뛴다 (0 · 장부 그대로 넷)"   "$(run BASE="$T/b1")/$(awk 'END{print NR-1}' "$T/b1/cost_ledger.tsv")" 0/4
  ck "⛔음성 결정이 proposed → 6"                           "$(run BASE="$T/b2" CARD_DECISION=D-PROP)" 6
  ck "⛔음성 결정이 원장에 없음 → 6"                        "$(run BASE="$T/b2" CARD_DECISION=D-NONE)" 6
  ck "⛔음성 러너 sha 다름 → 7"                             "$(run BASE="$T/b2" RUNNER_SHA16=0000000000000000)" 7
  ck "⛔음성 입력 구조 sha256 다름 → 8"                     "$(run BASE="$T/b2" SHA_B_12=00)" 8
  ck "⛔음성 입력 구조 없음 → 8"                            "$(run BASE="$T/b2" SRC="$T/nosrc")" 8
  ck "⛔음성 설정 대조 기준 없음 → 9"                       "$(run BASE="$T/b2" REF="$T/noref")" 9
  ck "⛔음성 모르는 PHASE → 13"                             "$(run BASE="$T/b2" PHASE=x)" 13
  ck "문지기에서 멈추면 런 폴더 0"                          "$(ls -d "$T"/b2/[AB]/seed1[12]/T600 2>/dev/null | wc -l)" 0
  mkdir -p "$T/b3/A/seed11/T600"
  ck "⛔음성 덜 끝난 런 폴더가 있다 → 20"                   "$(run BASE="$T/b3")" 20
  ck "⛔음성 첫 런 벽시계 > 한도 → 21 (장부 한 줄)"         "$(run BASE="$T/b4" FIRST_RUN_MAX_H=0.00001 FAKE_SLEEP=1)/$(awk 'END{print NR-1}' "$T/b4/cost_ledger.tsv")" 21/1
  ck "⛔음성 누적 + 다음 어림 > 상한 → 22 (장부 한 줄)"     "$(run BASE="$T/b5" CAP_H=0.0000001 FAKE_SLEEP=1)/$(awk 'END{print NR-1}' "$T/b5/cost_ledger.tsv")" 22/1
  ck "⛔음성 러너 실패 (msd.json 없이 끝남) → 4 를 그대로"  "$(run BASE="$T/b6" FAKE_CRASH=1)" 4
  ck "    그 뒤 런은 안 띄운다 (런 폴더 하나)"              "$(ls -d "$T"/b6/[AB]/seed1[12]/T600 2>/dev/null | wc -l)" 1
  ck "DRY_RUN 은 띄우지 않는다 (0 · 런 폴더 0 · 장부 없음)" "$(run BASE="$T/b7" DRY_RUN=1)/$(ls -d "$T"/b7/[AB]/seed1[12]/T600 2>/dev/null | wc -l)/$([ -e "$T/b7/cost_ledger.tsv" ] && echo y || echo n)" 0/0/n
  ck "DRY_RUN 계획 16 줄 (기본 사다리)"                     "$(run BASE="$T/b8" DRY_RUN=1 TEMPS="600 650 700 750" >/dev/null; grep -c '^.*계획 T' "$T/out")" 16
  ck "PHASE=cond550 계획 = 550 K · prod 800 · 4 줄"         "$(env -u TEMPS true; ( timeout 120 env -i HOME="$T/home" PATH="$T/bin:$PATH" REPO="$REPO" DECISIONS="$T/dec.json" CARD_DECISION=D-CARD PY="$SPY" DRV="$T/drv.py" DRV_SHA16="$DSHA" SRC="$T/src" REF="$T/ref" SHA_A_11="$SH" SHA_A_12="$SH" SHA_B_11="$SH" SHA_B_12="$SH" REC_A_11="$REC" REC_A_12="$REC" REC_B_11="$REC" REC_B_12="$REC" BASE="$T/b9" DRY_RUN=1 PHASE=cond550 bash "$SELF" > "$T/out" 2>&1 ); grep -c '계획 T550 .*--prod_ps 800' "$T/out")" 4
  rm -rf "$T"; [ "$f" = 0 ] && echo "selftest ✅ (음성 11 포함)" || echo "selftest ⛔"; exit "$f"
fi

# ── 본 실행 ────────────────────────────────────────────────────────────────────
mkdir -p "$BASE"
if [ "$DRY_RUN" != 1 ]; then
  exec > >(tee -a "$BASE/stage2_kgy.log") 2>&1
  exec 8>"$BASE/.stage2.lock"; flock -n 8 || { say "⛔ 이 큐가 이미 돌고 있다 (flock $BASE/.stage2.lock)"; exit 10; }
fi
[ "$DRY_RUN" = 1 ] && say "DRY_RUN — 검사만 하고 띄우지 않는다 (PHASE $PHASE)" || say "▶ li2s-3 2 단계 큐 시작 · PHASE $PHASE · 온도 $TEMPS · 시드 $SEEDS · 계 $SYSTEMS · prod $PROD ps"
gatekeep; rc=$?; [ $rc = 0 ] || exit $rc
if [ "$DRY_RUN" != 1 ] && [ ! -s "$LEDGER" ]; then printf 'system\tT_K\tseed\tprod_ps\tstart\tend\thours\trc\n' > "$LEDGER"; fi
for T in $TEMPS; do for sd in $SEEDS; do for x in $SYSTEMS; do
  OUT=$BASE/$x/seed$sd/T$T
  if [ -f "$OUT/d0.00_cfg0/T$T/msd.json" ]; then say "건너뜀 — $x seed$sd T$T 는 이미 끝났다 (msd.json 있음)"; continue; fi
  [ -e "$OUT" ] && { say "⛔ $OUT 가 있는데 msd.json 이 없다 (덜 끝난 런) — 사람이 흔적을 보존하고 정리한 뒤 다시 띄운다"; exit 20; }
  if [ "$DRY_RUN" != 1 ]; then
    c=$(cum_h); e=$(last_h)
    if gt "$(awk -v a="$c" -v b="$e" 'BEGIN{printf "%.6f", a+b}')" "$CAP_H"; then
      say "⛔ 누적 $c h + 다음 런 어림 $e h > 상한 $CAP_H h — 멈춘다 (카드: 멈춘 시점의 시드 · 온도로 판정하지 않는다 · 사용자 결정)"; exit 22; fi
  fi
  t0=$(date +%s); s0=$(date '+%F %T')
  run_one "$x" "$T" "$sd"; rc=$?
  [ "$DRY_RUN" = 1 ] && { [ $rc = 0 ] || exit $rc; continue; }
  t1=$(date +%s); h=$(awk -v a="$t0" -v b="$t1" 'BEGIN{printf "%.4f", (b-a)/3600}')
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$x" "$T" "$sd" "$PROD" "$s0" "$(date '+%F %T')" "$h" "$rc" >> "$LEDGER"
  [ $rc = 0 ] || { say "⛔ $x seed$sd T$T 러너 종료 $rc — 큐를 멈춘다 (러너 로그 $BASE/$x/queue_kgy.log)"; exit $rc; }
  say "✅ $x seed$sd T$T 끝 · $h h · 누적 $(cum_h) / $CAP_H h"
  if [ "$(n_rows)" = 1 ] && gt "$h" "$FIRST_RUN_MAX_H"; then
    say "⛔ 첫 런 벽시계 $h h > $FIRST_RUN_MAX_H h — 멈추고 보고한다 (카드 멈춤 규칙)"; exit 21; fi
done; done; done
[ "$DRY_RUN" = 1 ] && say "DRY_RUN 끝 — 위가 전부 OK/✅/✓ 면 발사해도 된다" || say "■ 큐 끝 · PHASE $PHASE · 누적 $(cum_h) h"
exit 0
