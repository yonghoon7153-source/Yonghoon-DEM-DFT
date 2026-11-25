#!/usr/bin/env bash
# =============================================================================
# glass_main_queue_gabia.sh — li2s 소셀 유리 본 런 나머지를 gabia 에서 **한 번에 하나씩**
#                              (탄성 modelc_2x GPU pw.x 옆 공존 · 2026-09-29)
#
# 근거 결정: D-2026-09-29-gabia-uma-coexist-elastic-li2s-main — 원장(이 repo)에서 active 가 아니면 시작하지 않는다.
#   탄성 쪽 조건 (09-11 2차 개정 · D-2026-09-11-elastic-conv-threshold): 공존은 허용하되 탄성 잡이 하나라도
#   OOM·중단이면 modelc_2x 를 **처음부터** 다시 돌린다 ⇒ 이 러너의 가드는 **우리 MD 만** 죽인다.
#   탄성 pw.x·탄성 러너는 건드리지 않는다.
#
# 쓰는 법
#   bash tools/ionic/glass_main_queue_gabia.sh --selftest      # 가짜 nvidia-smi·가짜 드라이버 · 음성 포함
#   DRY_RUN=1 bash tools/ionic/glass_main_queue_gabia.sh       # 결정·드라이버 sha·구조 판별·계획만 본다
#   bash tools/ionic/glass_main_queue_gabia.sh                 # tmux 안에서 — 큐를 끝까지, 멈추면 종료 코드로 이유
#
# v2 카드 (2026-09-30 · lpscl_smallcell_glass_md_v2_estimand_2026_09_30.json · 잠정) 에서 더한 것 — 옛 동작은 기본값 그대로다:
#   · 큐 항목 `T:seed:prod` — prod(ps) 를 런마다 준다 (없으면 PROD_DEFAULT=400). run_meta 의 prod_ps 가 그 값이어야 한다.
#   · VSEED_OFFSET (기본 0) — 드라이버 --seed = VSEED_OFFSET + seed. 드라이버의 MD 난수 = --seed + T 라서 (드라이버 :580)
#     옛 런(--seed = 구조 시드) 과 같은 난수열을 피하려면 v2 는 1000 을 준다. run_meta 의 seed 가 그 값이어야 한다.
#   · LABEL_PREFIX (기본 없음 → 옛 라벨 규칙) — 주면 라벨 = <prefix>_s<seed>_T<T>.
#   · EXCEPTION_ID 기본값 = v2 예외. 옛 예외(09-29)는 09-30 에 소멸·대체됐다 — 옛 ID 로는 결정 검사에서 멈춘다 (6).
#
# 대조 계 B (2026-10-13 · lpscl_smallcell_glass_control_li3ps4_estimand_2026_10_05.json · 카드 결정
#   D-2026-10-05-lpscl-smallcell-glass-control-li3ps4) 에서 더한 것 — SYSTEM=B 일 때만 기본값이 바뀐다 (기본 SYSTEM=A = 옛 동작):
#   · 구조 = 이 repo 의 B 담금질 회수본 $BSRC/{kgy|gabia}/B/seed<S>/final.xyz (relax 판 · seed1·2 kgy · seed3·4·5 gabia ·
#     회수 faa6dac · e9b03863) — 기계 사이로 옮기지 않는다. 기록값 = 이 러너의 판별식으로 잰 값 (최단 P–S · PS₄ 15/15 · ρ ·
#     repo 시드 게이트 2026-10-13 과 같은 파일). 판별은 A 와 같은 값 게이트 (±0.003 Å · 개수 · ±0.001 g/cm³).
#   · 기본값: QUEUE "600:2:400 600:4:400 600:5:400" (카드 §1b gabia 몫 {2, 4, 5}) · VSEED_OFFSET 1000 · LABEL_PREFIX
#     lpscl_glass_ctrlB · ROOT /data/work/runs/lpscl_glass_control_li3ps4_600K_2026_10_13 · DRV = repo 드라이버 ·
#     REF_META·REF_MDLOG = A v2 600 K seed2 (gabia) 판 — 카드 'A v2 600 K 와 같은 설정' 을 run_meta·dt 로 대조한다 ·
#     EXCEPTION_ID D-2026-10-13-gabia-uma-coexist-pwx-li2s-control-600k · CARD_DECISION = 카드 결정 (둘 다 active 여야 시작).
#   · PWX_WATCH (작업방 여럿 · 공백으로 · 기본 = ELW 하나 = 옛 동작) — 가드 ④ 가 **모든** 작업방의 *.out 을 파일별 오프셋으로
#     본다 (B 기본 = Li₃Nd r2 + 탄성 — r2 가 끝나고 탄성이 재개돼도 ④ 가 따라간다). 작업방 하나라도 *.out 이 없으면
#     시작하지 않는다 (14 · ④ 가 말없이 무력해지는 것을 막는다 — 담금질 러너 ⑧ 과 같은 규칙).
#   · 점유 표본 (회신 CS Q-CS-1 · gabia 는 실측): PMON_S (60) 초마다 nvidia-smi pmon → queue_logs/s<S>_T<T>_pmon.tsv
#     (우리 PID 트리 sm % · 모든 잡 sm % 합 · 못 읽으면 NA — 0 으로 적지 않는다). 장부 = Σ Δt × 우리/합 (합 0 → 우리 몫 1).
#   · 시작 때 torch · fairchem · ase 판과 repo HEAD 를 로그에 찍는다 (B 담금질 밀도·T₅₀ 이 담금질 기계별로 갈렸는데
#     plan.json 에 판이 없었다 — 2026-10-13 · 판정 아님).
#
# B 측정 가능 조건 카드 (2026-10-14 · lpscl_smallcell_glass_control_bmeasurable_estimand_2026_10_14.json · 잠정 · 카드 결정
#   D-2026-10-14-lpscl-smallcell-glass-control-bmeasurable = proposed) 에서 더한 것 — PRESET 을 안 주면 옛 동작 그대로:
#   · PRESET=bmeas650 → SYSTEM=B · QUEUE "650:2:400 650:4:400 650:5:400" (같은 시드–기계 대응) · VSEED_OFFSET 2000 (600 K 의 1000 과
#     다른 새 난수) · ROOT /data/work/runs/lpscl_glass_bmeas_650K_2026_10_14 · EXCEPTION_ID D-2026-10-14-gabia-uma-coexist-pwx-li2s-bmeas-650k ·
#     CARD_DECISION = 위 카드 결정 · CARD_STATE_OK "active proposed". 구조 · 기록값 · 가드 · PWX_WATCH · 설정 대조 기준은 B 그대로.
#   · CARD_STATE_OK (기본 "active") — 카드 결정이 이 상태 중 하나여야 시작한다. active 가 아니면 '잠정 실행' 줄을 찍는다
#     (li2s = 외부 1저자 트랙: 사용자 실행 승인 · 규칙 동의는 회신 · 결과는 회신 전까지 안 연다 — v2 선례). 예외 결정은 늘 active.
#   · 모르는 PRESET → 13.
#
# 큐 QUEUE="T:seed[:prod] ..." (기본 465:5 550:3 550:4 550:5 465:1 465:2 550:2 — 09-29 본 런 · gabia 에 구조가 있는 것 먼저)
#   ⛔ 550:1 은 **없다** — 550 K seed1 은 파일럿 P-2 가 본 런을 겸한다 (편지 CH · 회신 CH '그대로 가세요').
#     2026-09-29 에 기본값이 550:1 을 넣은 8 런이었다 (셈 오류 · 실제 남은 본 런 7). 1저자 09-29 저녁: seed1·2 세 런은 kgy.
#   seed3·4·5 초기구조 = $GABIA_A/seed<S>/final.xyz · seed1·2 = $INIT/seed<S>_final.xyz (kgy 에서 사람이 옮긴다 —
#   없으면 **그 차례에서 기다린다**. 조용히 건너뛰지 않는다).
#   구조는 **이름이 아니라 값으로** 가린다 (09-28 이름 함정 두 번 뒤의 규칙): 120 원자 · 단일 프레임 ·
#   최단 P–S (최소 영상) 기록값 ±0.003 Å · PS₄ 개수 (P–S ≤ 2.6 Å 가 넷 · melt_quench_uma.py R_PS) · ρ ±0.001 g/cm³.
#   기록값: lpscl_smallcell_glass_md_gateA_erratum_2026_09_24.json (relax 판) · seed3·4 는 amendment_ch 09-28 의 4 자리.
#   설정은 seed3 T465 의 run_meta.json 과 같아야 한다 (T·seed·v0 만 다름) + md.log 시간 간격(dt)이 seed3 과 같아야 한다.
#
# 가드 (SAMPLE 초마다 — ⚠ 확률적 보호: 표본 간격보다 빠른 VRAM 급등은 못 막는다)
#   ① GPU 합계 > TOTALCAP (46,000 MiB)                      → 우리 MD kill
#   ② 우리 MD (PID 트리) > OURCAP (3,500 MiB) · WARM 300 s 뒤 → 우리 MD kill
#   ③ host MemAvailable < HOSTFLOOR (8,192 MiB)              → 우리 MD kill
#   ④ 탄성 작업방의 최신 *.out 에 GPU 메모리 오류 (우리 런 시작 뒤 새로 쓰인 부분만) → 우리 MD kill
#   ①–④ 가 한 번이라도 발동하면 **예외를 닫는다** = 큐를 멈추고 종료한다 (다음 런을 안 띄운다 · 자동 재시작 없음).
#   시작 문턱: GPU 합계 ≤ START_MAX (42,500) 그리고 host ≥ HOSTFLOOR + 4,096 — 아니면 기다린다.
#
# 이어 돌리기: msd.json 이 있는 런은 건너뛴다. out_root 가 있는데 msd.json 이 없으면(중단 흔적) 그 폴더를
#   `<폴더>_aborted_<시각>` 으로 옮겨 **보존**한 뒤 다시 돈다 — md.log 는 ASE MDLogger 가 append 로 열어서
#   섞이면 생산 구간 평균 T 가 틀린다 (traj.xyz 는 드라이버가 지운다).
#
# 종료 코드: 0 큐 끝 · 2 가드 ①–③ (예외 닫힘) · 3 우리 MD CUDA OOM (예외 닫힘) · 4 우리 MD 가 msd.json 없이 끝남
#            · 5 가드 ④ 탄성 GPU 오류 (예외 닫힘 · 사람이 탄성 쪽을 본다) · 6 결정 비활성 · 7 드라이버 sha 불일치
#            · 8 구조 판별 실패 · 9 설정 불일치 (run_meta · dt) · 10 이미 실행 중 (flock — 큐를 둘 띄우지 않는다)
#            · 13 큐 항목 형식 오류 (T:seed[:prod] · 숫자 아님 · 칸 넷 이상) 또는 SYSTEM 이 A·B 아님 — 띄우기 전에 멈춘다
#            · 14 PWX_WATCH 작업방에 *.out 이 없다 (가드 ④ 가 말없이 무력해진다) · 6 은 CARD_DECISION 비활성에도 쓴다
#
# 이 러너가 **못 하는 것**
#   · 표본 간격(2 s)보다 빠른 VRAM 급등을 막지 못한다 — 탄성 pw.x 가 스스로 OOM 날 수 있다
#     (09-11 기록 피크 41.2 GB + 우리 ~2.0 GB = 43.2 / 49.1 GB · 지금 실측 30.6 GB).
#   · 탄성 러너를 멈추거나 늦추지 않는다 (SM 을 나눠 쓰니 탄성 스텝은 느려질 수 있다).
#   · kgy 의 seed1·2 구조를 가져오지 않는다. 결과(D·β·C1·C2)를 판정하지 않는다 — 판독은 msd_diffusive_check.py.
#   · friction 은 run_meta 에 없어 사후 대조를 못 한다 — 명령에 0.02 를 박았다 (드라이버 기본값도 0.02).
# =============================================================================
set -u

REPO=${REPO:-$(cd "$(dirname "$(realpath "$0")")/../.." 2>/dev/null && pwd)}
SYSTEM=${SYSTEM:-A}
QUEUE_DEFAULT="465:5 550:3 550:4 550:5 465:1 465:2 550:2"   # 550:1 없음 — 위 머리글 (SYSTEM=A)
QUEUE_DEFAULT_B="600:2:400 600:4:400 600:5:400"              # 카드 §1b gabia 몫 {2, 4, 5} (SYSTEM=B)
PRESET=${PRESET:-}
case "$PRESET" in
  "") ;;
  bmeas650)   # B 측정 가능 조건 카드 (2026-10-14 · 잠정) — 머리글 'B 측정 가능 조건 카드'
    SYSTEM=B
    QUEUE=${QUEUE:-"650:2:400 650:4:400 650:5:400"}
    VSEED_OFFSET=${VSEED_OFFSET:-2000}
    ROOT=${ROOT:-/data/work/runs/lpscl_glass_bmeas_650K_2026_10_14}
    EXCEPTION_ID=${EXCEPTION_ID:-D-2026-10-14-gabia-uma-coexist-pwx-li2s-bmeas-650k}
    CARD_DECISION=${CARD_DECISION:-D-2026-10-14-lpscl-smallcell-glass-control-bmeasurable}
    CARD_STATE_OK=${CARD_STATE_OK:-active proposed} ;;
  *) echo "⛔ PRESET=$PRESET — bmeas650 만 안다 (시작하지 않는다)"; exit 13 ;;
esac
if [ "$SYSTEM" = B ]; then   # 대조 계 B — 머리글 '대조 계 B'
  _V2=/data/work/runs/lpscl_glass_md_v2_2026_09_30/seed2/T600          # A v2 600 K (gabia) — 설정 기준
  ROOT=${ROOT:-/data/work/runs/lpscl_glass_control_li3ps4_600K_2026_10_13}
  DRV=${DRV:-$REPO/tools/modelc_v3/disorder_ensemble_diffusion.py}
  QUEUE=${QUEUE:-$QUEUE_DEFAULT_B}
  REF_META=${REF_META:-$_V2/run_meta.json}; REF_MDLOG=${REF_MDLOG:-$_V2/d0.00_cfg0/T600/md.log}
  EXCEPTION_ID=${EXCEPTION_ID:-D-2026-10-13-gabia-uma-coexist-pwx-li2s-control-600k}
  CARD_DECISION=${CARD_DECISION:-D-2026-10-05-lpscl-smallcell-glass-control-li3ps4}
  VSEED_OFFSET=${VSEED_OFFSET:-1000}; LABEL_PREFIX=${LABEL_PREFIX:-lpscl_glass_ctrlB}
  PWX_WATCH=${PWX_WATCH:-/data/work/runs/sei_control/li3nd_mp-976264_p333_r2 /data/work/runs/elastic_modelc_2x}
fi
BSRC=${BSRC:-$REPO/db/raw/lpscl_glass_control_li3ps4_2026_10_05}
ROOT=${ROOT:-/data/work/runs/lpscl_glass_md_main_2026_09_28}
PY=${PY:-/data/apps/miniforge3/envs/uma/bin/python}
DRV=${DRV:-/data/work/glass_src_2026_09_28/disorder_ensemble_diffusion.py}
DRV_SHA16=${DRV_SHA16:-c3e2d358ee53cefa}
QUEUE=${QUEUE:-$QUEUE_DEFAULT}
GABIA_A=${GABIA_A:-/data/work/runs/lpscl_smallcell_gabia/A}
INIT=${INIT:-$ROOT/init}
ELW=${ELW:-/data/work/runs/elastic_modelc_2x}
PWX_WATCH=${PWX_WATCH:-$ELW}
REF_META=${REF_META:-$ROOT/seed3/T465/run_meta.json}
REF_MDLOG=${REF_MDLOG:-$ROOT/seed3/T465/d0.00_cfg0/T465/md.log}
OURCAP=${OURCAP:-3500}; TOTALCAP=${TOTALCAP:-46000}; START_MAX=${START_MAX:-42500}
HOSTFLOOR=${HOSTFLOOR:-8192}; SAMPLE=${SAMPLE:-2}; WARM=${WARM:-300}; POLL=${POLL:-60}; PMON_S=${PMON_S:-60}
META_WAIT=${META_WAIT:-900}; STRUCT_WAIT=${STRUCT_WAIT:-600}; KILL_GRACE=${KILL_GRACE:-10}
EXCEPTION_ID=${EXCEPTION_ID:-D-2026-09-30-gabia-uma-coexist-elastic-li2s-v2}
CARD_DECISION=${CARD_DECISION:-}
CARD_STATE_OK=${CARD_STATE_OK:-active}   # 카드 결정이 이 상태 중 하나여야 시작 (머리글 'B 측정 가능 조건 카드')
PROD_DEFAULT=${PROD_DEFAULT:-400}; VSEED_OFFSET=${VSEED_OFFSET:-0}; LABEL_PREFIX=${LABEL_PREFIX:-}

# seed → "최단P–S PS₄개수 ρ" (relax 판 기록값). REC_<S> 로 덮을 수 있다 (selftest 용).
rec_of(){ local v="REC_$1"; [ -n "${!v:-}" ] && { echo "${!v}"; return; }
  if [ "$SYSTEM" = B ]; then   # B relax 판 — 이 러너의 판별식 (check_struct) 으로 repo 회수본을 잰 값 (2026-10-13)
    case "$1" in 1) echo "2.0214 15 1.6222";; 2) echo "2.0157 15 1.6130";; 3) echo "2.0065 15 1.5143";;
                 4) echo "2.0206 15 1.5478";; 5) echo "2.0256 15 1.5178";; *) echo "";; esac; return; fi
  case "$1" in 1) echo "2.037 12 1.6212";; 2) echo "2.021 12 1.5782";; 3) echo "2.0055 12 1.5933";;
               4) echo "2.0324 12 1.591";; 5) echo "2.030 11 1.6181";; *) echo "";; esac; }
struct_of(){ if [ "$SYSTEM" = B ]; then
    case "$1" in 1|2) echo "$BSRC/kgy/B/seed$1/final.xyz";; 3|4|5) echo "$BSRC/gabia/B/seed$1/final.xyz";; *) echo "";; esac; return; fi
  case "$1" in 3|4|5) echo "$GABIA_A/seed$1/final.xyz";; *) echo "$INIT/seed$1_final.xyz";; esac; }
# 큐 항목 → QT QS QP (prod 가 없으면 PROD_DEFAULT) · QV (드라이버 --seed). 형식이 틀리면 1.
parse_q(){ local r n; QT=${1%%:*}; r=${1#*:}; QS=${r%%:*}; QP=$PROD_DEFAULT
  n=$(printf '%s' "$1" | tr -cd ':' | wc -c)
  [ "$n" = 1 ] || [ "$n" = 2 ] || return 1
  [ "$n" = 2 ] && QP=${r#*:}
  [[ "$QT" =~ ^[0-9]+$ ]] && [[ "$QS" =~ ^[0-9]+$ ]] && [[ "$QP" =~ ^[0-9]+([.][0-9]+)?$ ]] || return 1
  QV=$((VSEED_OFFSET + QS)); return 0; }

ts(){ date '+%F %T'; }
say(){ echo "[$(ts)] $*"; }
gpu_total(){ nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits -i 0 2>/dev/null | head -1 | tr -d ' '; }
tree_pids(){ echo "$1"; local c; for c in $(pgrep -P "$1" 2>/dev/null); do tree_pids "$c"; done; }
gpu_tree(){ local apps s=0 p v; apps=$(nvidia-smi --query-compute-apps=pid,used_memory --format=csv,noheader,nounits 2>/dev/null)
  for p in $(tree_pids "$1"); do v=$(echo "$apps" | awk -F', *' -v p="$p" '$1==p{s+=$2} END{print s+0}'); s=$((s+v)); done; echo "$s"; }
host_mib(){ [ -n "${FAKE_HOST_MIB_FILE:-}" ] && { cat "$FAKE_HOST_MIB_FILE"; return; }   # selftest 전용 훅
  awk '/MemAvailable/{printf "%d", $2/1024}' /proc/meminfo; }
kill_tree(){ local ps i=0; ps=$(tree_pids "$1"); kill -TERM $ps 2>/dev/null
  while [ "$i" -lt "$KILL_GRACE" ]; do kill -0 "$1" 2>/dev/null || break; sleep 1; i=$((i+1)); done
  kill -KILL $ps 2>/dev/null; return 0; }

decision_state_of(){ python3 - "$REPO/db/governance/decisions.json" "$1" <<'PY'
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
# 카드 결정의 상태가 CARD_STATE_OK 안에 있나 — 빈 상태 (원장에 없음 · 못 읽음) 는 늘 거부
state_ok(){ local w; [ -n "$1" ] || return 1; for w in $CARD_STATE_OK; do [ "$1" = "$w" ] && return 0; done; return 1; }
decision_active(){ [ "$(decision_state_of "${1:-$EXCEPTION_ID}")" = active ]
}

check_struct(){  # $1 xyz · $2 "ps n4 rho" → OK/FAIL 한 줄 · 0 = OK
  "$PY" - "$1" $2 <<'PY'
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

check_meta(){  # $1 새 run_meta · $2 T · $3 드라이버 seed · $4 xyz · $5 prod → 0 = 기준(seed3 T465)과 같은 설정
  python3 - "$REF_META" "$1" "$2" "$3" "$4" "${5:-$PROD_DEFAULT}" <<'PY'
import json, sys
ref = json.load(open(sys.argv[1])); new = json.load(open(sys.argv[2]))
T, S, X, P = float(sys.argv[3]), int(sys.argv[4]), sys.argv[5], float(sys.argv[6])
# prod_ps 는 기준과 비교하지 않고 큐가 준 값과 비교한다 (v2: 550 K 800 ps · 600 K 400 ps)
keys = ("n_atoms", "supercell", "equilib_ps", "fit_window_ps", "save_traj", "uma_model",
        "uma_inference_mode_requested")
bad = [f"{k} {ref.get(k)!r}→{new.get(k)!r}" for k in keys if ref.get(k) != new.get(k)]
try:
    p_ok = float(new.get("prod_ps")) == P
except (TypeError, ValueError):
    p_ok = False
if not p_ok: bad.append(f"prod_ps {new.get('prod_ps')!r} ≠ 큐 {P:g}")
if [float(t) for t in new.get("temperatures", [])] != [T]: bad.append(f"temperatures {new.get('temperatures')!r}")
if new.get("seed") != S: bad.append(f"seed {new.get('seed')!r} ≠ {S}")
if new.get("v0_xyz") != X: bad.append(f"v0_xyz {new.get('v0_xyz')!r}")
print(f"OK run_meta = seed3 T465 판과 같다 (T·seed·v0·prod 만 다름 · prod {P:g} · seed {S})" if not bad
      else "FAIL run_meta 다름: " + " · ".join(bad))
sys.exit(1 if bad else 0)
PY
}
dt_of(){ awk 'NR==2{a=$1} NR==3{printf "%.4f", $1-a; exit}' "$1" 2>/dev/null; }   # MDLogger: 1 행 머리 · 매 스텝

label_of(){ [ -n "$LABEL_PREFIX" ] && { echo "${LABEL_PREFIX}_s$1_T$2"; return; }
  local L3; L3=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1])).get('label',''))" "$REF_META" 2>/dev/null)
  case "$L3" in *s3*) L3=${L3/s3/s$1};; *) echo "lpscl_glass_main_s$1_T$2"; return;; esac
  case "$L3" in *465*) L3=${L3/465/$2};; esac; echo "$L3"; }

# 가드 ④ — PWX_WATCH 의 **모든** 작업방 *.out 을 파일별 오프셋으로 본다 (우리 런 시작 뒤 새로 쓰인 부분만).
#   시작 뒤 새로 생긴 *.out (재개 · 다음 변형점) 은 처음부터 읽는다 — 파일 전체가 시작 뒤의 것이다.
EL_F=""; declare -A EL_OFFS=()
el_files(){ local d; for d in $PWX_WATCH; do ls "$d"/*.out 2>/dev/null; done; }
el_latest(){ local d; for d in $PWX_WATCH; do ls -t "$d"/*.out 2>/dev/null | head -1; done; }   # 작업방마다 최신 하나
el_missing(){ local d; for d in $PWX_WATCH; do ls "$d"/*.out >/dev/null 2>&1 || echo "$d"; done; }
el_mark(){ EL_OFFS=(); local f; while IFS= read -r f; do [ -n "$f" ] && EL_OFFS["$f"]=$(stat -c %s "$f"); done < <(el_files); return 0; }
el_gpu_error(){ local f o
  while IFS= read -r f; do [ -n "$f" ] || continue; o=${EL_OFFS["$f"]:-0}
    if grep -aqiE "out of memory|ALLOC_FAILED|cudaErrorMemoryAllocation" < <(tail -c +$((o + 1)) "$f" 2>/dev/null); then EL_F=$f; return 0; fi
  done < <(el_files); return 1; }
pmon_sample(){  # $1 = 우리 PID → "시각<TAB>우리 sm<TAB>모든 잡 sm 합" (pmon 을 못 읽으면 NA — 0 으로 적지 않는다)
  local t out pids; t=$(date '+%F %T')
  out=$(nvidia-smi pmon -c 1 -s u 2>/dev/null) || { printf '%s\tNA\tNA\n' "$t"; return; }
  pids=" $(tree_pids "$1" | tr '\n' ' ') "
  echo "$out" | awk -v pids="$pids" -v t="$t" '!/^#/ && NF>=4 { sm=($4 ~ /^[0-9]+$/) ? $4 : 0; all+=sm; if (index(pids, " "$2" ")) ours+=sm } END { printf "%s\t%d\t%d\n", t, ours+0, all+0 }'; }
versions(){ "$PY" -c "import torch, ase; import fairchem.core as f; print('torch', torch.__version__, '· fairchem', getattr(f, '__version__', '?'), '· ase', ase.__version__)" 2>/dev/null | tail -1; }

# ── selftest (음성 포함) ────────────────────────────────────────────────────────
if [ "${1:-}" = "--selftest" ]; then
  SPY=${SELFTEST_PY:-$PY}
  T=$(mktemp -d); f=0; SELF=$(realpath "$0")
  ck(){ if [ "$2" = "$3" ]; then echo "  ✔ $1"; else echo "  ✘ $1 — 기대 [$3] · 실제 [$2]"; f=1; fi; }
  mkdir -p "$T/bin" "$T/A/seed3" "$T/A/seed4" "$T/A/seed5" "$T/init" "$T/el" "$T/repo/db/governance"
  echo 30000 > "$T/base"; : > "$T/apps"; echo 50000 > "$T/host"
  cat > "$T/bin/nvidia-smi" <<EOF
#!/bin/bash
live(){ while IFS= read -r l; do p=\${l%%,*}; [ -n "\$p" ] && kill -0 "\$p" 2>/dev/null && echo "\$l"; done < "$T/apps"; }
case "\$*" in
  *query-gpu=memory.used*) echo \$(( \$(cat "$T/base") + \$(live | awk -F', *' '{s+=\$2} END{print s+0}') ));;
  *query-compute-apps*) live;;
  *pmon*) [ -e "$T/pmon_fail" ] && exit 1
          echo "# gpu         pid  type    sm   mem   enc   dec   command"; echo "# Idx           #   C/G     %     %     %     %   name"
          echo "    0      999999     C    90    40     -     -   pw.x"; live | awk -F', *' '{printf "    0 %s C 7 1 - - python\n", \$1}';;
esac
EOF
  chmod +x "$T/bin/nvidia-smi"
  : > "$T/el/strain_00.out"     # 가드 ④ 작업방에 *.out 이 있어야 시작한다 (14 — 대조 계 B 때 더한 규칙)
  # 가짜 드라이버 — 설정은 파일로 받는다 (러너가 환경을 그대로 넘기므로 env 도 된다)
  cat > "$T/drv.py" <<'EOF'
import json, os, sys, time, argparse
ap = argparse.ArgumentParser()
for k in ("--v0_xyz", "--label", "--out_root", "--device", "--friction", "--timestep_fs", "--equilib_ps", "--prod_ps"):
    ap.add_argument(k)
ap.add_argument("--supercell", nargs=3); ap.add_argument("--disorder_levels", nargs="+"); ap.add_argument("--n_configs")
ap.add_argument("--temperatures", nargs="+"); ap.add_argument("--fit_window_ps", nargs=2); ap.add_argument("--seed", type=int)
ap.add_argument("--save_traj", action="store_true"); ap.add_argument("--turbo", action="store_true")
a = ap.parse_args(); E = os.environ; T = float(a.temperatures[0])
with open(E["FAKE_APPS"], "a") as fh: fh.write(f"{os.getpid()}, {E.get('FAKE_OURS', '2000')}\n")
os.makedirs(a.out_root, exist_ok=True)
json.dump({"label": a.label, "n_atoms": 120, "supercell": [1, 1, 1], "v0_xyz": a.v0_xyz, "temperatures": [T],
           "prod_ps": 200.0 if E.get("FAKE_META_BAD") else float(E.get("FAKE_PROD", a.prod_ps)), "equilib_ps": 5.0,
           "seed": int(E.get("FAKE_SEED", a.seed)),
           "fit_window_ps": [2.0, 50.0], "save_traj": True, "uma_model": "uma-s-1p1",
           "uma_inference_mode_requested": "turbo"}, open(os.path.join(a.out_root, "run_meta.json"), "w"))
d = os.path.join(a.out_root, "d0.00_cfg0", f"T{int(T)}"); os.makedirs(d, exist_ok=True)
dt = float(E.get("FAKE_DT", "0.002"))
with open(os.path.join(d, "md.log"), "a") as fh:
    fh.write("Time[ps]      Etot[eV]     Epot[eV]     Ekin[eV]    T[K]\n")
    for i in range(3): fh.write(f"{i*dt:<10.4f} -1.0 -1.0 0.0 465.0\n")
if E.get("FAKE_OOM"):
    print("torch.OutOfMemoryError: CUDA out of memory. Tried to allocate 2.00 GiB"); sys.exit(1)
if E.get("FAKE_CRASH"):
    print("RuntimeError: something else"); sys.exit(1)
time.sleep(float(E.get("FAKE_SLEEP", "2")))
json.dump({"T_K": T, "D_Li_cm2_s": 1e-6}, open(os.path.join(d, "msd.json"), "w"))
EOF
  DSHA=$(sha256sum "$T/drv.py" | cut -c1-16)
  printf '%s' '{"decisions":[{"id":"D-TEST","decision_state":"active"},{"id":"D-PROP","decision_state":"proposed"}]}' \
    > "$T/repo/db/governance/decisions.json"
  # 구조 픽스처: P 12 · S 48 · Li 60 = 120 원자 · P 마다 S 넷 (첫 P 만 최단 거리를 다르게)
  "$SPY" - "$T" <<'PY' || { echo "  ✘ 픽스처 생성 실패 (numpy·ase 필요 — SELFTEST_PY)"; exit 1; }
import sys, numpy as np
from ase import Atoms
from ase.io import write
T = sys.argv[1]
def make(first_ps, n4_break=0):
    pos, sym = [], []
    tet = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]) / np.sqrt(3)
    k = 0
    for i in range(3):
        for j in range(2):
            for m in range(2):
                c = np.array([4 + 8 * i, 4 + 8 * j, 4 + 8 * m], float)
                pos.append(c); sym.append("P")
                for t_i, t in enumerate(tet):
                    r = first_ps if (k == 0 and t_i == 0) else 2.05
                    if n4_break and k == 1 and t_i == 0: r = 2.9      # 둘째 P 만 S 하나를 떼어 PS₄ 11 (최단 P–S 는 그대로)
                    pos.append(c + r * t); sym.append("S")
                k += 1
    for q in range(60):
        pos.append([2.0 + 4.0 * (q % 6), 0.3, 0.8 + 1.5 * (q // 6)]); sym.append("Li")
    return Atoms(sym, positions=pos, cell=[24, 16, 16], pbc=True)
good = make(2.030)
write(f"{T}/A/seed5/final.xyz", good, format="extxyz")
write(f"{T}/A/seed3/final.xyz", good, format="extxyz")
write(f"{T}/A/seed4/final.xyz", make(2.030, n4_break=1), format="extxyz")   # PS₄ 11 개
write(f"{T}/init/seed1_ok.xyz", good, format="extxyz")
write(f"{T}/init/two.xyz", [good, good], format="extxyz")
write(f"{T}/init/off.xyz", make(2.040), format="extxyz")                    # 최단 P–S +0.010
rho = good.get_masses().sum() * 1.66053906660 / good.get_volume()
open(f"{T}/rho", "w").write(f"{rho:.4f}")
# 대조 계 B 픽스처: P 15 · S 60 · Li 45 = 120 원자 · P 마다 S 넷 (n4_break 면 둘째 P 의 S 하나를 떼어 PS₄ 14)
def make_b(first_ps, n4_break=0):
    pos, sym = [], []
    tet = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]) / np.sqrt(3)
    k = 0
    for i in range(5):
        for j in range(3):
            c = np.array([3 + 6 * i, 3 + 6 * j, 4.0])
            pos.append(c); sym.append("P")
            for t_i, t in enumerate(tet):
                r = first_ps if (k == 0 and t_i == 0) else 2.05
                if n4_break and k == 1 and t_i == 0: r = 2.9
                pos.append(c + r * t); sym.append("S")
            k += 1
    for q in range(45):
        pos.append([1.0 + 2.0 * (q % 15), 1.0 + 6.0 * (q // 15), 9.5]); sym.append("Li")
    return Atoms(sym, positions=pos, cell=[30, 18, 12], pbc=True)
import os
gb = make_b(2.020)
for m, sd in (("kgy", 2), ("gabia", 4)):
    os.makedirs(f"{T}/bsrc/{m}/B/seed{sd}", exist_ok=True); write(f"{T}/bsrc/{m}/B/seed{sd}/final.xyz", gb, format="extxyz")
os.makedirs(f"{T}/bsrc/gabia/B/seed5", exist_ok=True)
write(f"{T}/bsrc/gabia/B/seed5/final.xyz", make_b(2.020, n4_break=1), format="extxyz")    # PS₄ 14
rb = gb.get_masses().sum() * 1.66053906660 / gb.get_volume()
open(f"{T}/rho_b", "w").write(f"{rb:.4f}")
PY
  RHO=$(cat "$T/rho")
  run(){ ( timeout 90 env ROOT="$T/root" PY="$SPY" DRV="$T/drv.py" DRV_SHA16="$DSHA" GABIA_A="$T/A" INIT="$T/init" ELW="$T/el" \
      REPO="$T/repo" EXCEPTION_ID=D-TEST REF_META="$T/ref_meta.json" REF_MDLOG="$T/ref_md.log" \
      SAMPLE=0.2 POLL=1 WARM=3 META_WAIT=20 STRUCT_WAIT=1 KILL_GRACE=2 FAKE_APPS="$T/apps" FAKE_HOST_MIB_FILE="$T/host" \
      REC_3="2.030 12 $RHO" REC_4="2.030 11 $RHO" REC_5="2.030 12 $RHO" REC_1="2.030 12 $RHO" \
      PATH="$T/bin:$PATH" "$@" bash "$SELF" > "$T/out" 2>&1 ); echo $?; }
  after_start(){ local i=0; while [ ! -s "$1" ] && [ "$i" -lt 400 ]; do sleep 0.2; i=$((i+1)); done; }
  printf '%s' '{"label":"lpscl_glass_main_s3_T465","n_atoms":120,"supercell":[1,1,1],"prod_ps":400.0,"equilib_ps":5.0,"fit_window_ps":[2.0,50.0],"save_traj":true,"uma_model":"uma-s-1p1","uma_inference_mode_requested":"turbo","temperatures":[465.0],"seed":3,"v0_xyz":"x"}' > "$T/ref_meta.json"
  printf 'Time[ps]  Etot\n0.0000 -1\n0.0020 -1\n' > "$T/ref_md.log"
  echo 30000 > "$T/base"; : > "$T/apps"
  ck "⛔음성 기본 큐에 550:1 이 없다 (P-2 겸용 · 09-29 셈 오류 재발 방지)" "$(echo " $QUEUE_DEFAULT " | grep -c ' 550:1 ')" 0
  ck "양성: 두 런 끝까지 (0)"                         "$(run QUEUE='465:5 550:3')" 0
  ck "양성: msd.json 둘 · TSV 둘 done=1"            "$(ls "$T"/root/seed5/T465/d0.00_cfg0/T465/msd.json "$T"/root/seed3/T550/d0.00_cfg0/T550/msd.json 2>/dev/null | wc -l)/$(awk -F'\t' 'NR>1 && $4==1' "$T/root/queue_coexist.tsv" | wc -l)" 2/2
  ck "양성: 라벨 = seed3 판 패턴 치환"              "$(python3 -c "import json;print(json.load(open('$T/root/seed3/T550/run_meta.json'))['label'])")" lpscl_glass_main_s3_T550
  ck "이어 돌리기: 끝난 런은 건너뜀"                "$(run QUEUE='465:5 550:3'; grep -c '이미 끝' "$T/out")" "0
2"
  mkdir -p "$T/root/seed5/T550"; echo '{}' > "$T/root/seed5/T550/run_meta.json"
  ck "중단 흔적: 보존 이동 뒤 다시 돔 (0)"          "$(run QUEUE='550:5')" 0
  ck "중단 흔적: _aborted_ 폴더가 남는다"           "$(ls -d "$T"/root/seed5/T550_aborted_* 2>/dev/null | wc -l)" 1
  ck "⛔음성 결정이 active 아님 → 6"                "$(run QUEUE='465:5' EXCEPTION_ID=D-PROP)" 6
  ck "⛔음성 결정이 원장에 없음 → 6"                 "$(run QUEUE='465:5' EXCEPTION_ID=D-NONE)" 6
  ck "⛔음성 드라이버 sha 다름 → 7"                  "$(run QUEUE='465:5' DRV_SHA16=0000000000000000)" 7
  ck "⛔음성 PS₄ 개수 다름 (기록 12 · 실제 11) → 8"  "$(run QUEUE='465:4' REC_4="2.030 12 $RHO")" 8
  cp "$T/init/off.xyz" "$T/init/seed1_final.xyz"
  ck "⛔음성 최단 P–S +0.010 Å → 8"                  "$(run QUEUE='465:1')" 8
  cp "$T/init/two.xyz" "$T/init/seed1_final.xyz"
  ck "⛔음성 프레임 둘 → 8"                          "$(run QUEUE='465:1')" 8
  rm -f "$T/init/seed1_final.xyz"; rm -rf "$T/root/seed1"
  ( sleep 3; cp "$T/init/seed1_ok.xyz" "$T/init/seed1_final.xyz" ) &
  ck "구조 없음 → 기다렸다 생기면 이어 감 (0)"       "$(run QUEUE='465:1')" 0
  ck "구조 없음 → '구조 없음' 을 알렸다"            "$(grep -c '구조 없음' "$T/out" | awk '{print ($1>0)}')" 1
  wait
  rm -rf "$T/root/seed5/T600"
  ( after_start "$T/root/seed5/T600/run_meta.json"; echo 45000 > "$T/base" ) &
  ck "⛔음성 가드① 합계 47,000 > 46,000 → 2"        "$(run QUEUE='600:5 650:5' FAKE_SLEEP=30)" 2
  wait; echo 30000 > "$T/base"
  ck "⛔음성 가드① 뒤 다음 런을 안 띄움"            "$(ls -d "$T"/root/seed5/T650 2>/dev/null | wc -l)" 0
  ck "⛔음성 가드① 뒤 우리 MD 가 죽었다"            "$(grep -c '가드 발동' "$T/out")" 1
  rm -rf "$T"/root/seed5/T600*
  ck "⛔음성 가드② 우리 4,000 > 3,500 (WARM 뒤) → 2" "$(run QUEUE='600:5' FAKE_OURS=4000 FAKE_SLEEP=30)" 2
  rm -rf "$T"/root/seed5/T600*
  ck "WARM 안에서는 가드② 안 뜀 (0)"                "$(run QUEUE='600:5' FAKE_OURS=4000 FAKE_SLEEP=1)" 0
  rm -rf "$T"/root/seed5/T600*; ( after_start "$T/root/seed5/T600/run_meta.json"; echo 7000 > "$T/host" ) &
  ck "⛔음성 가드③ host 7,000 < 8,192 MiB → 2"      "$(run QUEUE='600:5' FAKE_SLEEP=30)" 2
  wait
  echo 50000 > "$T/host"; rm -rf "$T"/root/seed5/T600*
  printf 'old out of memory (지난 일)\n' > "$T/el/strain_23_p.out"
  ( after_start "$T/root/seed5/T600/run_meta.json"; sleep 0.5
    printf '     0: ALLOCATE: 1 bytes requested; status = 2(out of memory)\n' >> "$T/el/strain_23_p.out" ) &
  ck "⛔음성 가드④ 탄성 새 출력에 OOM → 5"            "$(run QUEUE='600:5' FAKE_SLEEP=30)" 5
  wait; rm -rf "$T"/root/seed5/T600*
  ck "가드④ 는 우리 시작 전 옛 오류로는 안 뜀 (0)"  "$(run QUEUE='600:5' FAKE_SLEEP=1)" 0
  rm -rf "$T"/root/seed5/T600*
  ck "⛔음성 우리 MD CUDA OOM → 3"                   "$(run QUEUE='600:5' FAKE_OOM=1)" 3
  rm -rf "$T"/root/seed5/T600*
  ck "⛔음성 msd.json 없이 끝남 → 4"                 "$(run QUEUE='600:5' FAKE_CRASH=1)" 4
  rm -rf "$T"/root/seed5/T600*
  ck "⛔음성 run_meta 설정 다름 (prod 200) → 9"      "$(run QUEUE='600:5' FAKE_META_BAD=1 FAKE_SLEEP=30)" 9
  rm -rf "$T"/root/seed5/T600*
  ck "⛔음성 dt 다름 (1 fs) → 9"                      "$(run QUEUE='600:5' FAKE_DT=0.001 FAKE_SLEEP=30)" 9
  rm -rf "$T"/root/seed5/T600*; echo 43000 > "$T/base"
  ( i=0; while ! grep -q '대기 — GPU' "$T/out" 2>/dev/null && [ "$i" -lt 400 ]; do sleep 0.2; i=$((i+1)); done; echo 30000 > "$T/base" ) &
  ck "시작 문턱: 합계 > START_MAX 면 기다렸다 뜬다 (0)" "$(run QUEUE='600:5' FAKE_SLEEP=1)" 0
  ck "시작 문턱: '대기' 를 남겼다"                  "$(grep -c '대기 — GPU' "$T/out" | awk '{print ($1>0)}')" 1
  wait
  mkdir -p "$T/root"; ( flock -x 9; sleep 6 ) 9>"$T/root/.queue_coexist.lock" & sleep 1
  ck "⛔음성 큐가 이미 돌면 (lock) → 10"             "$(run QUEUE='465:5')" 10
  wait
  ck "DRY_RUN 은 띄우지 않는다 (0 · 새 폴더 0)"      "$(run QUEUE='700:5' DRY_RUN=1)/$(ls -d "$T"/root/seed5/T700 2>/dev/null | wc -l)" 0/0
  # ── v2 (2026-09-30): T:seed:prod · VSEED_OFFSET · LABEL_PREFIX ──
  ck "옛 동작: prod 없는 항목은 400 · --seed = 구조 시드" \
     "$(python3 -c "import json;m=json.load(open('$T/root/seed5/T465/run_meta.json'));print(m['prod_ps'],m['seed'])")" "400.0 5"
  ck "v2 양성: 800:5:800 · 오프셋 1000 · 접두 라벨 → 끝까지 (0)" \
     "$(run QUEUE='800:5:800' VSEED_OFFSET=1000 LABEL_PREFIX=lpscl_glass_v2 FAKE_SLEEP=1)" 0
  ck "v2 양성: run_meta prod 800 · seed 1005 · 라벨 접두" \
     "$(python3 -c "import json;m=json.load(open('$T/root/seed5/T800/run_meta.json'));print(m['prod_ps'],m['seed'],m['label'])")" \
     "800.0 1005 lpscl_glass_v2_s5_T800"
  ck "⛔음성 prod 기대 800 · run_meta 400 → 9"        "$(run QUEUE='810:5:800' FAKE_PROD=400 FAKE_SLEEP=30)" 9
  ck "⛔음성 seed 기대 1005 · run_meta 5 → 9"          "$(run QUEUE='820:5' VSEED_OFFSET=1000 FAKE_SEED=5 FAKE_SLEEP=30)" 9
  ck "⛔음성 큐 형식 — 칸 넷 (600:5:800:1) → 13"      "$(run QUEUE='600:5:800:1')" 13
  ck "⛔음성 큐 형식 — 숫자 아님 (600:x) → 13"         "$(run QUEUE='600:x')" 13
  ck "⛔음성 큐 형식 — 콜론 없음 (600) → 13"           "$(run QUEUE='600')" 13
  # ── 대조 계 B (2026-10-13): SYSTEM=B · BSRC · PWX_WATCH (작업방 여럿) · 점유 표본 · CARD_DECISION · 판 줄 ──
  RHOB=$(cat "$T/rho_b"); REALREPO=$(cd "$(dirname "$SELF")/../.." && pwd)
  mkdir -p "$T/el2"; : > "$T/el2/r2.out"; rm -f "$T/pmon_fail"
  bq(){ run SYSTEM=B ROOT="$T/rootB" BSRC="$T/bsrc" CARD_DECISION=D-TEST PWX_WATCH="$T/el $T/el2" PMON_S=0 \
            REC_2="2.020 15 $RHOB" REC_4="2.020 15 $RHOB" REC_5="2.020 15 $RHOB" "$@"; }
  ck "B 기본 큐 = 카드 §1b gabia 몫 {2, 4, 5} · 600 K · 400 ps" "$QUEUE_DEFAULT_B" "600:2:400 600:4:400 600:5:400"
  r=$(run SYSTEM=B ROOT="$T/rootB" BSRC="$REALREPO/db/raw/lpscl_glass_control_li3ps4_2026_10_05" CARD_DECISION=D-TEST \
          PWX_WATCH="$T/el $T/el2" REC_4= REC_5= DRY_RUN=1)
  ck "B 실물: 기본 큐 DRY_RUN (0) — repo 회수본 · 내장 기록값" "$r" 0
  ck "B 실물: 세 계획 줄이 전부 OK (seed2 kgy · seed4·5 gabia · --seed 100S · 라벨 ctrlB)" \
     "$(grep -cE "계획 T600 seed(2 · prod 400 ps · 드라이버 --seed 1002 · 라벨 lpscl_glass_ctrlB_s2_T600 · [^ ]*/kgy/B/seed2/final.xyz|4 · prod 400 ps · 드라이버 --seed 1004 · 라벨 lpscl_glass_ctrlB_s4_T600 · [^ ]*/gabia/B/seed4/final.xyz|5 · prod 400 ps · 드라이버 --seed 1005 · 라벨 lpscl_glass_ctrlB_s5_T600 · [^ ]*/gabia/B/seed5/final.xyz) · OK" "$T/out")" 3
  ck "B 실물: 판 줄 (torch · fairchem · ase · repo) 을 찍는다 — 못 읽어도 멈추지 않는다" "$(grep -c '판 — ' "$T/out")" 1
  mkdir -p "$T/swap/kgy/B/seed2"; cp "$REALREPO/db/raw/lpscl_glass_control_li3ps4_2026_10_05/kgy/B/seed1/final.xyz" "$T/swap/kgy/B/seed2/final.xyz"
  ck "⛔음성 B 실물: seed2 자리에 seed1 파일 → 값 게이트 8" \
     "$(run SYSTEM=B ROOT="$T/rootB" BSRC="$T/swap" CARD_DECISION=D-TEST PWX_WATCH="$T/el $T/el2" QUEUE='600:2:400' DRY_RUN=1)" 8
  ck "B 양성: 600:2:400 끝까지 (0)"                  "$(bq QUEUE='600:2:400' FAKE_SLEEP=2)" 0
  ck "B 양성: run_meta seed 1002 · 라벨 lpscl_glass_ctrlB_s2_T600 · v0 = kgy seed2" \
     "$(python3 -c "import json;m=json.load(open('$T/rootB/seed2/T600/run_meta.json'));print(m['seed'],m['label'],m['v0_xyz'].endswith('/kgy/B/seed2/final.xyz'))")" \
     "1002 lpscl_glass_ctrlB_s2_T600 True"
  ck "B 점유 표본: 우리 sm 7 · 합 97 행이 pmon 장부에 있다" \
     "$(awk -F'\t' 'NR>1 && $2==7 && $3==97' "$T/rootB/queue_logs/s2_T600_pmon.tsv" | wc -l | awk '{print ($1>0)}')" 1
  rm -rf "$T"/rootB/seed4; touch "$T/pmon_fail"
  ck "B 양성 (pmon 실패여도 런은 간다) (0)"           "$(bq QUEUE='600:4:400' FAKE_SLEEP=1)" 0
  ck "⛔음성 pmon 을 못 읽으면 NA (0 으로 적지 않는다)" \
     "$(awk -F'\t' 'NR>1 && $2=="NA" && $3=="NA"' "$T/rootB/queue_logs/s4_T600_pmon.tsv" | wc -l | awk '{print ($1>0)}')/$(awk -F'\t' 'NR>1 && $2=="0"' "$T/rootB/queue_logs/s4_T600_pmon.tsv" | wc -l)" 1/0
  rm -f "$T/pmon_fail"
  ck "⛔음성 B PS₄ 기록 15 · 실제 14 → 8"             "$(bq QUEUE='600:5:400')" 8
  ck "⛔음성 CARD_DECISION 이 proposed → 6"          "$(bq QUEUE='600:2:400' CARD_DECISION=D-PROP)" 6
  mkdir -p "$T/el_empty"
  ck "⛔음성 PWX_WATCH 작업방 하나에 *.out 없음 → 14" "$(bq QUEUE='600:2:400' PWX_WATCH="$T/el $T/el_empty")" 14
  ck "⛔음성 SYSTEM=C → 13"                           "$(bq QUEUE='600:2:400' SYSTEM=C)" 13
  # ── B 측정 가능 조건 카드 (2026-10-14 · 잠정): PRESET=bmeas650 · CARD_STATE_OK ──
  r=$(run SYSTEM=B PRESET=bmeas650 ROOT="$T/rootP" BSRC="$REALREPO/db/raw/lpscl_glass_control_li3ps4_2026_10_05" CARD_DECISION=D-PROP \
          PWX_WATCH="$T/el $T/el2" REC_4= REC_5= DRY_RUN=1)
  ck "프리셋 bmeas650 실물: 카드 proposed 허용 · 기본 큐 DRY_RUN (0)" "$r" 0
  ck "프리셋 bmeas650 실물: 세 계획 줄 = T650 · --seed 200S · 라벨 ctrlB_s<S>_T650 (seed2 kgy · seed4·5 gabia)" \
     "$(grep -cE "계획 T650 seed(2 · prod 400 ps · 드라이버 --seed 2002 · 라벨 lpscl_glass_ctrlB_s2_T650 · [^ ]*/kgy/B/seed2/final.xyz|4 · prod 400 ps · 드라이버 --seed 2004 · 라벨 lpscl_glass_ctrlB_s4_T650 · [^ ]*/gabia/B/seed4/final.xyz|5 · prod 400 ps · 드라이버 --seed 2005 · 라벨 lpscl_glass_ctrlB_s5_T650 · [^ ]*/gabia/B/seed5/final.xyz)" "$T/out")" 3
  ck "프리셋 bmeas650: '잠정 실행' 줄을 찍는다 (카드 proposed)" "$(grep -c '⚠ 카드 결정 D-PROP = proposed — 잠정 실행' "$T/out")" 1
  ck "프리셋 양성: 650:2:400 끝까지 (0)"              "$(bq PRESET=bmeas650 ROOT="$T/rootP" CARD_DECISION=D-PROP QUEUE='650:2:400' FAKE_SLEEP=2)" 0
  ck "프리셋 양성: run_meta T 650 · seed 2002 · 라벨 lpscl_glass_ctrlB_s2_T650" \
     "$(python3 -c "import json;m=json.load(open('$T/rootP/seed2/T650/run_meta.json'));print(m['temperatures'],m['seed'],m['label'])")" \
     "[650.0] 2002 lpscl_glass_ctrlB_s2_T650"
  ck "⛔음성 프리셋이어도 예외 결정은 active 여야 한다 (proposed → 6)" "$(bq PRESET=bmeas650 ROOT="$T/rootP" CARD_DECISION=D-PROP EXCEPTION_ID=D-PROP QUEUE='650:4:400' DRY_RUN=1)" 6
  ck "⛔음성 프리셋 · 카드 결정이 원장에 없음 → 6"   "$(bq PRESET=bmeas650 ROOT="$T/rootP" CARD_DECISION=D-NONE QUEUE='650:4:400' DRY_RUN=1)" 6
  ck "⛔음성 CARD_STATE_OK 를 active 로 좁히면 proposed 카드 → 6" "$(bq PRESET=bmeas650 ROOT="$T/rootP" CARD_DECISION=D-PROP CARD_STATE_OK=active QUEUE='650:4:400' DRY_RUN=1)" 6
  ck "⛔음성 모르는 PRESET → 13"                      "$(bq PRESET=bmeas600 QUEUE='600:2:400' DRY_RUN=1)" 13
  rm -rf "$T"/rootB/seed2; printf 'old: CUDA error: out of memory (지난 일)\n' >> "$T/el2/r2.out"
  ( after_start "$T/rootB/seed2/T600/run_meta.json"; sleep 0.5
    printf '     0: ALLOCATE: 1 bytes requested; status = 2(out of memory)\n' >> "$T/el2/r2.out" ) &
  ck "⛔음성 가드④ 둘째 작업방 (r2) 새 출력에 OOM → 5" "$(bq QUEUE='600:2:400' FAKE_SLEEP=30)" 5
  wait; rm -rf "$T"/rootB/seed2
  ck "가드④ 둘째 작업방의 시작 전 옛 오류로는 안 뜀 (0)" "$(bq QUEUE='600:2:400' FAKE_SLEEP=2)" 0
  rm -rf "$T"/rootB/seed2
  ( after_start "$T/rootB/seed2/T600/run_meta.json"; sleep 0.5
    printf 'cudaErrorMemoryAllocation\n' > "$T/el/strain_12_p.out" ) &
  ck "⛔음성 가드④ 시작 뒤 새로 생긴 *.out (탄성 재개) 의 OOM → 5" "$(bq QUEUE='600:2:400' FAKE_SLEEP=30)" 5
  wait; rm -f "$T/el/strain_12_p.out"
  rm -rf "$T"; [ "$f" = 0 ] && echo "selftest ✅ (음성 34 포함)" || echo "selftest ⛔"; exit "$f"
fi

# ── 본 실행 ────────────────────────────────────────────────────────────────────
say "════ li2s 유리 MD · gabia 공존 큐 · 계 $SYSTEM · 예외 $EXCEPTION_ID ════"
case "$SYSTEM" in A|B) ;; *) say "⛔ SYSTEM=$SYSTEM — A 또는 B 만 — 시작하지 않는다"; exit 13;; esac
decision_active || { say "⛔ 결정 $EXCEPTION_ID 가 원장($REPO)에서 active 가 아니다 — 시작하지 않는다"; exit 6; }
cs=
if [ -n "$CARD_DECISION" ]; then
  cs=$(decision_state_of "$CARD_DECISION")
  state_ok "$cs" || { say "⛔ 카드 결정 $CARD_DECISION 가 원장($REPO)에서 [$CARD_STATE_OK] 중 하나가 아니다 (지금: ${cs:-없음}) — 시작하지 않는다"; exit 6; }
  [ "$cs" = active ] || say "⚠ 카드 결정 $CARD_DECISION = $cs — 잠정 실행 (CARD_STATE_OK '$CARD_STATE_OK' · 사용자 실행 승인 · 규칙 동의는 외부 1저자 회신 · 결과는 회신 전까지 안 연다)"
fi
s=$(sha256sum "$DRV" 2>/dev/null | cut -c1-16)
[ "$s" = "$DRV_SHA16" ] || { say "⛔ 드라이버 sha16 ${s:-없음} ≠ $DRV_SHA16 ($DRV) — 시작하지 않는다"; exit 7; }
[ -s "$REF_META" ] || { say "⛔ 기준 run_meta 없음 ($REF_META) — 설정을 대조할 수 없다"; exit 9; }
miss=$(el_missing)
[ -z "$miss" ] || { say "⛔ PWX_WATCH 작업방에 *.out 이 없다: $miss — 가드 ④ 가 말없이 무력해진다 (작업방을 맞게 준다 · 시작하지 않는다)"; exit 14; }
say "결정 active ✓${CARD_DECISION:+ · 카드 $CARD_DECISION ($cs) ✓} · 드라이버 sha16 $s ✓ · 기준 설정 $REF_META · 가드 합계 $TOTALCAP · 우리 $OURCAP · host $HOSTFLOOR MiB"
# 판 줄은 여기서 찍지 않는다 — torch·fairchem import 가 uma env 에서 수 초 걸려 계획 줄·잠금 시점이 밀린다
#   (2026-10-13 gabia selftest: '구조 없음' 알림 · lock → 10 두 시험이 그 지연으로 빨강). DRY_RUN 끝과 잠금 뒤에서 찍는다.
ver_line(){ say "판 — $(versions || true) · repo $(git -C "$REPO" rev-parse --short=9 HEAD 2>/dev/null || echo '?') · 가드 ④ 최신 출력: $(el_latest | tr '\n' ' ')"; }
for q in $QUEUE; do
  parse_q "$q" || { say "⛔ 큐 항목 형식 오류 '$q' (T:seed[:prod] · 숫자) — 시작하지 않는다"; exit 13; }
  T=$QT; S=$QS; X=$(struct_of "$S"); R=$(rec_of "$S")
  [ -n "$R" ] || { say "⛔ seed$S 기록값 없음 — 시작하지 않는다"; exit 8; }
  if [ -s "$ROOT/seed$S/T$T/d0.00_cfg0/T$T/msd.json" ]; then st="끝남 (건너뜀)"
  elif [ -s "$X" ]; then st=$(check_struct "$X" "$R") || { say "⛔ T$T seed$S 구조 판별 실패 — $st · $X"; exit 8; }
  else st="구조 없음 — 그 차례에서 기다린다"; fi
  say "  계획 T$T seed$S · prod $QP ps · 드라이버 --seed $QV · 라벨 $(label_of "$S" "$T") · $X · $st"
done
if [ -n "${DRY_RUN:-}" ]; then
  ver_line
  say "  점유 표본 (시각 · 우리 · 합): $(pmon_sample $$ | tr '\t' ' ') — 우리 0 이 정상 (아직 안 띄웠다)"
  say "⇢ DRY_RUN — 띄우지 않았다 · GPU $(gpu_total) MiB · host $(host_mib) MiB"; exit 0; fi
# 중복 실행 가드 — pgrep 은 자기 자신·watch 를 센다(CLAUDE.md) · flock 은 프로세스가 죽으면 풀린다.
#   fd 9 는 MD 자식에게도 넘어가서, 러너가 죽어도 MD 가 살아 있는 동안은 새 큐가 못 뜬다 (한 번에 하나 유지).
mkdir -p "$ROOT"; exec 9>"$ROOT/.queue_coexist.lock"
flock -n 9 || { say "⛔ 큐가 이미 돌고 있다 (lock $ROOT/.queue_coexist.lock) — 둘을 동시에 띄우지 않는다"; exit 10; }
ver_line

mkdir -p "$ROOT/queue_logs"; TSV=$ROOT/queue_coexist.tsv
[ -f "$TSV" ] || printf "T\tseed\trc\tdone\twall_s\tpeak_total_MiB\tpeak_ours_MiB\tkilled\tstart\thost_min_MiB\n" > "$TSV"
for q in $QUEUE; do
  parse_q "$q" || { say "⛔ 큐 항목 형식 오류 '$q'"; exit 13; }
  T=$QT; S=$QS; PR=$QP; VS=$QV; OUT=$ROOT/seed$S/T$T; D=$OUT/d0.00_cfg0/T$T; X=$(struct_of "$S")
  [ -s "$D/msd.json" ] && { say "⏭ T$T seed$S 이미 끝 — 건너뜀"; continue; }
  if [ -e "$OUT" ]; then B="${OUT}_aborted_$(date +%m%d_%H%M%S)"; mv "$OUT" "$B"; say "↪ 중단 흔적 → $B (보존 · 다시 돈다)"; fi
  n=0; while [ ! -s "$X" ]; do
    [ $((n % 6)) = 0 ] && say "⏸ T$T seed$S 구조 없음 ($X) — 옮겨 오면 이어 간다"; n=$((n+1)); sleep "$STRUCT_WAIT"; done
  r=$(check_struct "$X" "$(rec_of "$S")") || { say "⛔ T$T seed$S 구조 판별 실패 — $r"; exit 8; }
  say "T$T seed$S 구조 $r"
  n=0; while :; do u=$(gpu_total); h=$(host_mib)
    [ -n "$u" ] && [ "$u" -le "$START_MAX" ] && [ "$h" -ge $((HOSTFLOOR + 4096)) ] && break
    [ $((n % 10)) = 0 ] && say "대기 — GPU ${u:-?}/$START_MAX MiB · host $h/$((HOSTFLOOR + 4096)) MiB"; n=$((n+1)); sleep "$POLL"; done
  L=$ROOT/queue_logs/s${S}_T${T}.log; el_mark
  "$PY" "$DRV" --v0_xyz "$X" --supercell 1 1 1 --label "$(label_of "$S" "$T")" --out_root "$OUT" \
      --disorder_levels 0 --n_configs 1 --temperatures "$T" --equilib_ps 5 --prod_ps "$PR" --timestep_fs 2 \
      --friction 0.02 --fit_window_ps 2 50 --save_traj --seed "$VS" --turbo --device cuda > "$L" 2>&1 &
  PID=$!; t0=$(date +%s); start=$(ts); say "▶ T$T seed$S PID $PID · prod $PR ps · --seed $VS · 시작 전 GPU $u MiB · 로그 $L"
  peak=0; pko=0; hmin=999999; killed=""; kcode=0; meta_ok=""; dt_ok=""; last=-999; plast=-999
  PM=$ROOT/queue_logs/s${S}_T${T}_pmon.tsv; [ -f "$PM" ] || printf 'time\tsm_ours\tsm_all\n' > "$PM"
  while kill -0 "$PID" 2>/dev/null; do
    u=$(gpu_total); o=$(gpu_tree "$PID"); h=$(host_mib); el=$(( $(date +%s) - t0 ))
    if [ $((el - plast)) -ge "$PMON_S" ]; then pmon_sample "$PID" >> "$PM"; plast=$el; fi
    [ -n "$u" ] && [ "$u" -gt "$peak" ] && peak=$u; [ "$o" -gt "$pko" ] && pko=$o; [ "$h" -lt "$hmin" ] && hmin=$h
    if   [ -n "$u" ] && [ "$u" -gt "$TOTALCAP" ]; then killed="① GPU 합계 $u > $TOTALCAP MiB"; kcode=2
    elif [ "$el" -gt "$WARM" ] && [ "$o" -gt "$OURCAP" ]; then killed="② 우리 MD $o > $OURCAP MiB"; kcode=2
    elif [ "$h" -lt "$HOSTFLOOR" ]; then killed="③ host $h < $HOSTFLOOR MiB"; kcode=2
    elif [ $((el - last)) -ge "$POLL" ]; then last=$el
      if el_gpu_error; then killed="④ pw.x 작업방 출력에 GPU 메모리 오류 ($EL_F)"; kcode=5
      elif [ -z "$meta_ok" ] && [ -s "$OUT/run_meta.json" ]; then
        m=$(check_meta "$OUT/run_meta.json" "$T" "$VS" "$X" "$PR") && { meta_ok=1; say "  $m"; } || { killed="설정 — $m"; kcode=9; }
      elif [ -z "$meta_ok" ] && [ "$el" -gt "$META_WAIT" ]; then killed="설정 — run_meta.json 이 ${META_WAIT}s 안에 안 생김"; kcode=9
      elif [ -z "$dt_ok" ] && [ -n "$(dt_of "$D/md.log")" ]; then
        a=$(dt_of "$REF_MDLOG"); b=$(dt_of "$D/md.log")
        [ "$a" = "$b" ] && { dt_ok=1; say "  dt = seed3 판과 같다 ($b ps/행)"; } || { killed="설정 — dt $b ≠ seed3 $a ps/행"; kcode=9; }
      fi
    fi
    if [ -n "$killed" ]; then say "⛔ 가드 발동: $killed — 우리 MD 만 멈춘다 (PID 트리 $PID)"; kill_tree "$PID"; break; fi
    sleep "$SAMPLE"
  done
  wait "$PID" 2>/dev/null; rc=$?; wall=$(( $(date +%s) - t0 )); dn=0; [ -s "$D/msd.json" ] && dn=1
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$T" "$S" "$rc" "$dn" "$wall" "$peak" "$pko" "${killed:-}" "$start" "$hmin" >> "$TSV"
  if [ -z "$killed" ] && [ "$dn" = 1 ]; then   # 런이 첫 점검보다 빨리 끝났으면 여기서 대조한다
    [ -z "$meta_ok" ] && { m=$(check_meta "$OUT/run_meta.json" "$T" "$VS" "$X" "$PR") || { say "⛔ 설정 — $m"; exit 9; }; say "  $m"; }
    [ -z "$dt_ok" ] && { a=$(dt_of "$REF_MDLOG"); b=$(dt_of "$D/md.log"); [ "$a" = "$b" ] || { say "⛔ 설정 — dt $b ≠ seed3 $a ps/행"; exit 9; }; }
  fi
  if [ -n "$killed" ]; then
    say "⛔ 예외 닫힘 — 큐를 멈춘다 (다음 런 안 띄움 · 결정 $EXCEPTION_ID reopen_criteria) · 종료 $kcode"; exit "$kcode"; fi
  if [ "$dn" != 1 ]; then
    if grep -aqiE "CUDA out of memory|OutOfMemoryError" "$L"; then say "⛔ 우리 MD CUDA OOM — 예외 닫힘 · $L"; exit 3; fi
    say "⛔ T$T seed$S 가 msd.json 없이 끝났다 (rc $rc) — 큐를 멈춘다 · tail -30 $L"; exit 4; fi
  say "✅ T$T seed$S 끝 · ${wall} s · 피크 합계 $peak · 우리 $pko MiB · host 최저 $hmin MiB"
done
say "■ 큐 끝 — 판독은 msd_diffusive_check.py (C1 · C2 · 감김)"
