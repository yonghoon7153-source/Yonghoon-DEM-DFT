#!/bin/bash
# cascade 녹는 에너지 입력 — 트랙 cascade (사용자 = 1저자) · 사용자 10-14 "한번 해보지 뭐" · "이건 gabia에서 해도 될듯" ·
#   "mp 받고 바로 돌릴 수 있도록 코드 짜자"
#   ① MP 다형 후보 — 값이 나올 수 있는 전구체 82 + 교환상 Li₂S · LiCl · Li₃PS₄ (창 0.03 eV/atom · 화학식당 ≤ 4 · 관측 최저 포함)
#   ② 1단계 원본 구성 에너지 — v23 · as2s3_recover 의 <런>/02_screen/uma_results.json (그때 쓴 baseline 포함)
#   ③ UMA 이완 — 1단계와 같은 도구 tools/doping/run_uma_screening.py (UMA-s-1p1 omat · FIRE · FrechetCellFilter · fmax 0.05 ·
#      steps 1500) · **CPU** (gabia GPU 는 pw.x ↔ UMA 규칙 · 예외 (6) 은 li2s 세 런만) · --base canonical 로 1단계 baseline 을
#      다시 만든다 = 대조 잡 (합치기의 관문 G1 이 1단계 값과 0.5 meV/atom 안인지 본다 · 아니면 결과를 안 낸다)
#   ④ 합치기 → result/ · element_effects 분석 → element_effects/ · SHA256SUMS
#   카드 db/properties/cascade_dissolution_energy_estimand_2026_10_14.json · 결정 D-2026-10-14-cascade-dissolution-energy (proposed)
#
# 쓰는 법 (gabia · 새 worktree 루트에서):
#   bash db/inputs/cascade_dissolution_2026_10_14/run_gabia.sh --dry-run    # MP 조회 0 · 이완 0 — 점검 · 계획만
#   tmux new -d -s diss1014 "bash db/inputs/cascade_dissolution_2026_10_14/run_gabia.sh"   # 실행 (로그 = $OUT/run.log)
#   이어 돌리기: 같은 명령 — MP · 1단계 수집은 다시 하고, 이완은 run_uma_screening 이 끝난 구조를 건너뛴다.
#
# 이 스크립트가 못 하는 것
#   · GPU 를 쓰지 않는다 (CUDA_VISIBLE_DEVICES 를 비운다) — 빠르게 하려면 gabia GPU 공존 새 결정이 먼저다.
#   · MP 데이터베이스 판을 고정하지 못한다 — manifest.json 에 판을 적는다.
#   · 1단계 구조의 결함 (canonical 기하 상속 · 감사 ①) 을 고치지 않는다 — 값은 데모다 (인용 금지).
#   · 형식전하가 0 이 아닌 1단계 구성 735 개 · 질화물 5 · NbCl₅ · TaCl₅ · Li₂S · LiCl 은 값이 없다 (카드 §3).
set -euo pipefail
DRY=0; [ "${1:-}" = "--dry-run" ] && DRY=1
cd "$(dirname "$(realpath "$0")")/../../.."
REPO=$(pwd)
PY=${PY:-/data/apps/miniforge3/envs/uma/bin/python}
OUT=${OUT:-db/raw/cascade_dissolution_2026_10_14}
STAGE1_ROOTS=${STAGE1_ROOTS:-"/data/work/runs/multi_category_2026_05_26_v23 /data/work/runs/as2s3_recover"}
THREADS=${THREADS:-8}
ALL=db/properties/cascade_all_302_2026_08_25.csv
CANON=db/structures/lpscl_F43m_24G_canonical.cif
CANON_MD5=57e24e164d1b
mkdir -p "$OUT"; LOG=$OUT/run.log; [ "$DRY" = 1 ] && LOG=$OUT/dry_run.log
exec > >(tee -a "$LOG") 2>&1
say(){ echo "[$(date '+%F %T')] $*"; }
exec 9>"/tmp/cascade_dissolution_2026_10_14.$(id -u).lock"
flock -n 9 || { say "⛔ 이미 도는 중 (lock) — 두 번 띄우지 않는다"; exit 3; }
say "== cascade 녹는 에너지 입력 · $([ "$DRY" = 1 ] && echo DRY-RUN || echo 실행) · repo $(git rev-parse --short HEAD 2>/dev/null || echo ?) · $REPO"

# ---- 준비 점검 (dry-run 도 여기까지는 같다) ----
[ -x "$PY" ] || { say "⛔ 파이썬 없음: $PY"; exit 2; }
"$PY" -c "import pymatgen, mp_api, fairchem.core, ase, torch" 2>/dev/null \
    || { say "⛔ $PY 에 pymatgen · mp_api · fairchem · ase · torch 중 빠진 게 있다 (uma env 를 쓴다)"; exit 2; }
[ -n "${MP_API_KEY:-}${PMG_MAPI_KEY:-}" ] || { say "⛔ MP_API_KEY 가 환경에 없다"; exit 2; }
for f in "$ALL" "$CANON" db/structures/comp1_V0_k444.cif tools/doping/run_uma_screening.py tools/cascade/dissolution_energy.py \
         tools/cascade/element_effects.py; do
    [ -s "$f" ] || { say "⛔ 입력 없음: $f"; exit 2; }
done
M=$(md5sum "$CANON" | cut -c1-12)
[ "$M" = "$CANON_MD5" ] || { say "⛔ canonical CIF md5 $M ≠ $CANON_MD5 (1단계 baseline 의 출처가 아니다)"; exit 2; }
N_RAW=0
for d in $STAGE1_ROOTS; do
    [ -d "$d" ] || { say "⛔ 1단계 런 폴더 없음: $d"; exit 2; }
    n=$(find "$d" -mindepth 3 -maxdepth 3 -path '*/02_screen/*' \( -name uma_results.json -o -name uma_screening_results.json \) | wc -l)
    say "  1단계 원본 $d — 02_screen 결과 $n 개"
    N_RAW=$((N_RAW + n))
done
[ "$N_RAW" -gt 0 ] || { say "⛔ 1단계 02_screen 결과가 하나도 없다"; exit 2; }
"$PY" tools/cascade/dissolution_energy.py --selftest > "$OUT/selftest_dissolution.txt" 2>&1 \
    || { say "⛔ dissolution_energy selftest"; tail -n 5 "$OUT/selftest_dissolution.txt"; exit 5; }
"$PY" tools/cascade/element_effects.py --selftest > "$OUT/selftest_element_effects.txt" 2>&1 \
    || { say "⛔ element_effects selftest"; tail -n 5 "$OUT/selftest_element_effects.txt"; exit 5; }
say "selftest 둘 ✓ ($(tail -n 1 "$OUT/selftest_dissolution.txt") · $(tail -n 1 "$OUT/selftest_element_effects.txt"))"
"$PY" -c "import fairchem.core as f, torch, ase; print('  버전: fairchem', getattr(f, '__version__', '?'), '· torch', torch.__version__, '· ase', ase.__version__)"
NPROC=$(nproc); LOAD=$(cut -d' ' -f1 /proc/loadavg)
say "CPU $NPROC 코어 · 1분 부하 $LOAD · 이완 스레드 $THREADS"
if ! awk -v l="$LOAD" -v t="$THREADS" -v n="$NPROC" 'BEGIN{exit !(l + t <= n)}'; then
    ps -eo pid,pcpu,etime,args --sort=-pcpu | head -n 6 | cut -c1-150
    [ "${FORCE_LOAD:-0}" = 1 ] || { say "⛔ 부하 $LOAD + 스레드 $THREADS > 코어 $NPROC — 다른 CPU 잡과 겹친다 (THREADS 를 줄이거나 FORCE_LOAD=1)"; exit 8; }
    say "⚠ FORCE_LOAD=1 — 겹치는 걸 알고 띄운다"
fi
command -v nvidia-smi >/dev/null && nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader | sed 's/^/  GPU (이 잡은 안 씀 · 참고) /' || true
say "계획 ① MP 다형 → $OUT/mp ② 1단계 원본 → $OUT/stage1_energies.json ③ UMA 이완 CPU → $OUT/uma ④ 합치기 → $OUT/result · $OUT/element_effects"
if [ "$DRY" = 1 ]; then say "DRY-RUN 끝 (MP 조회 0 · 이완 0) ✅"; exit 0; fi

# ---- 실행 ----
T0=$(date +%s)
say "① MP 다형 후보"
"$PY" tools/cascade/dissolution_energy.py fetch --out "$OUT/mp" || { rc=$?; say "⛔ fetch rc=$rc (6 = 교환상 구조가 빠졌다)"; exit "$rc"; }
say "② 1단계 원본 구성 에너지"
# shellcheck disable=SC2086
"$PY" tools/cascade/dissolution_energy.py collect --roots $STAGE1_ROOTS --out "$OUT/stage1_energies.json" \
    || { rc=$?; say "⛔ collect rc=$rc"; exit "$rc"; }
N_ST=$("$PY" -c "import json,sys; print(len(json.load(open(sys.argv[1]))['structures']))" "$OUT/mp/structures_summary.json")
say "③ UMA 이완 — 구조 $N_ST 개 + canonical 기준 (CPU · $THREADS 스레드 · 진행: grep -c 'E/atom' $OUT/uma/relax.log)"
mkdir -p "$OUT/uma"
CUDA_VISIBLE_DEVICES="" OMP_NUM_THREADS=$THREADS MKL_NUM_THREADS=$THREADS PYTHONUNBUFFERED=1 \
    "$PY" tools/doping/run_uma_screening.py --summary "$OUT/mp/structures_summary.json" --base "$CANON" \
    --baseline "$OUT/uma/baseline_rerun.json" --out "$OUT/uma/uma_results.json" --device cpu --steps 1500 2>&1 \
    | tee -a "$OUT/uma/relax.log"
say "④ 합치기"
"$PY" tools/cascade/dissolution_energy.py combine --mp_dir "$OUT/mp" --uma "$OUT/uma/uma_results.json" \
    --stage1 "$OUT/stage1_energies.json" --out "$OUT/result" \
    || { rc=$?; say "⛔ combine rc=$rc (3 = 1단계 baseline 재현 실패 · 결과 안 냄 — 숫자를 보고 정한다)"; exit "$rc"; }
"$PY" tools/cascade/element_effects.py --label_csv "$OUT/result/label_dissolution_min_per_key_atom.csv" \
    --name dissolution_min_per_key_atom --better low --out "$OUT/element_effects"
(cd "$OUT" && find . -type f ! -name SHA256SUMS ! -name run.log ! -name dry_run.log -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS)
say "끝 ✅ $(( ($(date +%s) - T0) / 60 )) 분 · 파일 $(wc -l < "$OUT/SHA256SUMS") 개 · 다음 = 커밋·푸시 블록"
