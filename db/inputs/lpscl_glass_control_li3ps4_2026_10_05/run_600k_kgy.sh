#!/bin/bash
# =============================================================================
# run_600k_kgy.sh — li2s 대조 계 B (a-Li₃PS₄ 유리 120 원자) 600 K · 400 ps 의 **kgy 몫 (seed1 · seed3)** 을 한 번에 하나씩
#   카드 db/properties/lpscl_smallcell_glass_control_li3ps4_estimand_2026_10_05.json §1b — A v2 600 K 와 같은 설정 ·
#   같은 시드–기계 대응 (gabia {2, 4, 5} · kgy {1, 3} · 회신 CR Q-CR-6).
#   ⛔ 트랙 li2s = 외부 1저자. 사용자 10-13 '저번처럼 gabia, kgy에서 나눠 돌리자' 는 실행 승인이다 (규칙은 카드 · 회신 CR).
#
# 이 파일은 **설정과 문지기**만 한다. 실행은 v2 kgy 러너 db/raw/lpscl_glass_md_v2_2026_09_30/glass_kgy_q_v2.sh
#   (sha16 3aef029aced0de77 · A v2 600 K 다섯 중 kgy 몫을 돌린 그 파일 · 원자료라 고치지 않는다) 를 환경변수로 B 에 맞춰 부른다
#   ⇒ 구조 값 게이트 · run_meta 동일성 (A v2 600 K kgy 판과) · md.log dt 를 A 때와 **같은 코드**로 건다.
#
# 문지기 (하나라도 어긋나면 시작하지 않는다 · 종료 코드)
#   6  카드 결정 D-2026-10-05-lpscl-smallcell-glass-control-li3ps4 가 원장에서 active 가 아니다
#   7  v2 러너 sha16 ≠ 3aef029aced0de77 (드라이버 sha16 c3e2d358ee53cefa 는 러너가 다시 본다)
#   8  seed3 구조 (gabia 담금질 · repo 회수본) 가 없다 · $ROOT/init/seed3_final.xyz 가 이미 있는데 바이트가 다르다
#   9  설정 대조 기준 (A v2 600 K kgy 판 run_meta · md.log) 이 없다
#   13 큐에 kgy 몫 {1, 3} 밖의 시드가 있다 (카드 §1b · 바꾸려면 판독 전에 기록하고 사람이 QUEUE 를 준다 + ALLOW_OFF_MAP=1)
#   그 뒤는 러너의 종료 코드다 (러너 머리글: 4 · 7 · 8 · 9 · 10 · 11 · 12 · 13).
#   시작할 때 torch · fairchem · ase 판과 repo HEAD 를 찍는다 (B 담금질 밀도·T₅₀ 이 담금질 기계별로 갈렸는데 plan.json 에
#   판이 없었다 — 2026-10-13 · 판정 아님).
#
# 쓰는 법 (kgy · repo worktree 안에서)
#   SELFTEST_PY=<numpy·ase 있는 python> bash db/inputs/lpscl_glass_control_li3ps4_2026_10_05/run_600k_kgy.sh --selftest
#   DRY_RUN=1 bash db/inputs/lpscl_glass_control_li3ps4_2026_10_05/run_600k_kgy.sh
#   bash db/inputs/lpscl_glass_control_li3ps4_2026_10_05/run_600k_kgy.sh        # tmux 안에서
#
# ⛔ 이 파일이 못 하는 것
#   · cascade 와 GPU 를 나눠 쓸 때의 속도·비용을 통제하지 못한다 — 시작 문턱은 러너의 GPU 합계 ≤ 20,000 MiB 뿐이라
#     cascade (≈ 2.7 GB) 로는 막히지 않는다. cascade 와 겹치지 않게 하려면 **사람이** cascade 가 끝난 뒤 띄운다.
#   · 프로세스별 점유를 재지 못한다 (kgy 는 nvidia-smi 프로세스 정보가 막혀 있다) — 장부는 동시 GPU 잡 수 등분 (회신 CS Q-CS-1).
#   · 결과를 판정하지 않는다 — 판독은 tools/ionic/glass_v2_readout.py 대조 모드 (판독 전에 확장 · 카드 §2).
# =============================================================================
set -u
HERE=$(cd "$(dirname "$(realpath "$0")")" && pwd)
REPO=${REPO:-$(cd "$HERE/../../.." && pwd)}
DECISIONS=${DECISIONS:-$REPO/db/governance/decisions.json}
CARD_DECISION=${CARD_DECISION:-D-2026-10-05-lpscl-smallcell-glass-control-li3ps4}
RUNNER=${RUNNER:-$REPO/db/raw/lpscl_glass_md_v2_2026_09_30/glass_kgy_q_v2.sh}
RUNNER_SHA16=${RUNNER_SHA16:-3aef029aced0de77}
BSRC=${BSRC:-$REPO/db/raw/lpscl_glass_control_li3ps4_2026_10_05}
V2=${V2:-$HOME/work/runs/lpscl_glass_md_v2_2026_09_30/seed1/T600}      # A v2 600 K kgy 판 — 설정 기준
ALLOW_OFF_MAP=${ALLOW_OFF_MAP:-0}
export PY=${PY:-/home/kgy/apps/miniforge3/envs/uma/bin/python}
export ROOT=${ROOT:-$HOME/work/runs/lpscl_glass_control_li3ps4_600K_2026_10_13}
export DRV=${DRV:-$REPO/tools/modelc_v3/disorder_ensemble_diffusion.py}
export QUEUE=${QUEUE:-"600:1:400 600:3:400"}           # 카드 §1b kgy 몫 {1, 3}
export A=${A:-$BSRC/kgy/B}                              # seed1 = kgy 담금질 (repo 회수본 e9b03863)
export INIT=${INIT:-$ROOT/init}                         # seed3 = gabia 담금질 (repo 회수본 faa6dac) → 문지기 ③ 가 옮긴다
export REF_META=${REF_META:-$V2/run_meta.json}
export REF_MDLOG=${REF_MDLOG:-$V2/d0.00_cfg0/T600/md.log}
export LABEL_PREFIX=${LABEL_PREFIX:-lpscl_glass_ctrlB}
export VSEED_OFFSET=${VSEED_OFFSET:-1000}
# B relax 판 기록값 (최단 P–S · PS₄ · ρ) — tools/ionic/glass_main_queue_gabia.sh SYSTEM=B 와 같은 값 (같은 판별식으로 잼).
#   seed2·4·5 는 일부러 안 준다 — 러너의 A 기록값이 남아 있어서, 큐에 그 시드가 잘못 들어가면 값 게이트에서 멈춘다.
export REC_1=${REC_1:-"2.0214 15 1.6222"}
export REC_3=${REC_3:-"2.0065 15 1.5143"}

say(){ echo "[$(date '+%F %T')] $*"; }
decision_active(){ python3 - "$DECISIONS" "$1" <<'PY'
import json, sys
try:
    D = json.load(open(sys.argv[1]))
except Exception:
    sys.exit(1)
L = D["decisions"] if isinstance(D, dict) else D
x = [e for e in L if e.get("id") == sys.argv[2]]
sys.exit(0 if x and x[0].get("decision_state") == "active" else 1)
PY
}
versions(){ "$PY" -c "import torch, ase; import fairchem.core as f; print('torch', torch.__version__, '· fairchem', getattr(f, '__version__', '?'), '· ase', ase.__version__)" 2>/dev/null | tail -1; }

gatekeep(){
  decision_active "$CARD_DECISION" || { say "⛔ 카드 결정 $CARD_DECISION 가 원장 ($DECISIONS) 에서 active 가 아니다 — 시작하지 않는다"; return 6; }
  local s; s=$(sha256sum "$RUNNER" 2>/dev/null | cut -c1-16)
  [ "$s" = "$RUNNER_SHA16" ] || { say "⛔ v2 러너 sha16 ${s:-없음} ≠ $RUNNER_SHA16 ($RUNNER) — 시작하지 않는다"; return 7; }
  local q sd
  for q in $QUEUE; do sd=${q#*:}; sd=${sd%%:*}
    case "$sd" in 1|3) ;; *) [ "$ALLOW_OFF_MAP" = 1 ] || { say "⛔ 큐 '$q' 의 seed$sd 는 kgy 몫 {1, 3} 밖이다 (카드 §1b) — 바꾸려면 판독 전에 기록하고 ALLOW_OFF_MAP=1"; return 13; };; esac
  done
  [ -s "$REF_META" ] && [ -s "$REF_MDLOG" ] || { say "⛔ 설정 대조 기준이 없다 — $REF_META · $REF_MDLOG (A v2 600 K kgy 판)"; return 9; }
  local src=$BSRC/gabia/B/seed3/final.xyz dst=$INIT/seed3_final.xyz
  [ -s "$src" ] || { say "⛔ seed3 구조 원본이 없다 ($src · repo 회수본 faa6dac)"; return 8; }
  if [ -e "$dst" ]; then cmp -s "$src" "$dst" || { say "⛔ $dst 가 이미 있는데 원본과 바이트가 다르다 — 덮지 않는다"; return 8; }
  else mkdir -p "$INIT" && cp "$src" "$dst" || { say "⛔ seed3 구조를 $dst 로 못 옮겼다"; return 8; }; fi
  say "문지기 ✓ — 카드 $CARD_DECISION active · 러너 sha16 $s · 큐 $QUEUE · seed3 $(sha256sum "$dst" | cut -c1-16) (= repo 원본)"
  say "판 — $(versions || true) · repo $(git -C "$REPO" rev-parse --short=9 HEAD 2>/dev/null || echo '?') · ROOT $ROOT"
  return 0
}

# ── selftest (음성 포함 · 실물 B 구조 + 실제 v2 러너 · 가짜 nvidia-smi · 가짜 원장) ────────────────────────
if [ "${1:-}" = "--selftest" ]; then
  SPY=${SELFTEST_PY:-$PY}; T=$(mktemp -d); f=0; SELF=$(realpath "$0")
  ck(){ if [ "$2" = "$3" ]; then echo "  ✔ $1"; else echo "  ✘ $1 — 기대 [$3] · 실제 [$2]"; f=1; fi; }
  mkdir -p "$T/bin" "$T/v2/d0.00_cfg0/T600" "$T/empty"
  printf '#!/bin/bash\necho 3000\n' > "$T/bin/nvidia-smi"; chmod +x "$T/bin/nvidia-smi"
  printf '%s' '{"decisions":[{"id":"D-CARD","decision_state":"active"},{"id":"D-PROP","decision_state":"proposed"}]}' > "$T/dec.json"
  printf '%s' '{"label":"lpscl_glass_v2_s1_T600","n_atoms":120,"supercell":[1,1,1],"prod_ps":400.0,"equilib_ps":5.0,"fit_window_ps":[2.0,50.0],"save_traj":true,"uma_model":"uma-s-1p1","uma_inference_mode_requested":"turbo","temperatures":[600.0],"seed":1001,"v0_xyz":"x"}' > "$T/v2/run_meta.json"
  printf 'Time[ps]  Etot\n0.0000 -1\n0.0020 -1\n' > "$T/v2/d0.00_cfg0/T600/md.log"
  # ⚠ env -i — 위 설정 줄이 export 한 기본값 (REF_META · INIT · A …) 이 자식에게 새면 자식의 `${X:-기본}` 이 그 값을 쓴다
  #   (2026-10-13 첫 판에서 그렇게 양성 시험이 전부 9 로 떨어졌다) ⇒ 자식은 빈 환경에서 시작한다.
  run(){ ( env -i PATH="$T/bin:$PATH" HOME="$T" LANG="${LANG:-C.UTF-8}" PY="$SPY" DECISIONS="$T/dec.json" CARD_DECISION=D-CARD \
           V2="$T/v2" ROOT="$T/root" DRY_RUN=1 "$@" bash "$SELF" > "$T/out" 2>&1 ); echo $?; }
  ck "양성: DRY_RUN 끝까지 (0) — 실물 seed1 (kgy) · seed3 (gabia) · 실제 v2 러너" "$(run)" 0
  ck "양성: 두 구조가 값 게이트 OK (B 기록값)" "$(grep -cE "seed[13] 구조 OK · 최단 P–S .* PS₄ 15/15 \(기록 15\)" "$T/out")" 2
  ck "양성: 계획 줄 — 라벨 lpscl_glass_ctrlB · --seed 1001 · 1003 · prod 400" \
     "$(grep -cE "계획 T600 seed(1 .*lpscl_glass_ctrlB_s1_T600 .*--seed 1001 .*--prod_ps 400|3 .*lpscl_glass_ctrlB_s3_T600 .*--seed 1003 .*--prod_ps 400)" "$T/out")" 2
  ck "양성: seed3 를 init 으로 옮겼고 repo 원본과 바이트가 같다" \
     "$(cmp -s "$BSRC/gabia/B/seed3/final.xyz" "$T/root/init/seed3_final.xyz" && echo same)" same
  ck "양성: 판 줄을 찍는다 (못 읽어도 멈추지 않는다)" "$(grep -c '판 — ' "$T/out")" 1
  ck "양성: 다시 돌려도 (init 에 같은 파일) 통과 (0)" "$(run)" 0
  ck "⛔음성 카드 결정 proposed → 6"                "$(run CARD_DECISION=D-PROP)" 6
  ck "⛔음성 카드 결정 원장에 없음 → 6"              "$(run CARD_DECISION=D-NONE)" 6
  ck "⛔음성 러너 sha 다름 → 7"                      "$(run RUNNER_SHA16=0000000000000000)" 7
  ck "⛔음성 큐에 seed2 (gabia 몫) → 13"             "$(run QUEUE='600:2:400')" 13
  ck "⛔음성 기준 run_meta 없음 → 9"                 "$(run V2="$T/empty")" 9
  ck "⛔음성 seed3 원본 없음 → 8"                    "$(run BSRC="$T/empty" A="$BSRC/kgy/B")" 8
  # 값은 같고 바이트만 다른 파일 — 깨진 파일을 쓰면 러너의 값 게이트가 대신 막아서 이 문지기를 재지 못한다
  #   (2026-10-13 첫 판이 그랬다: cmp 를 빼도 초록이었다)
  sed '2s/$/ note=edited/' "$BSRC/gabia/B/seed3/final.xyz" > "$T/root/init/seed3_final.xyz"
  ck "⛔음성 init 에 바이트가 다른 seed3 (값은 같음) 가 있으면 덮지 않는다 → 8" "$(run)" 8
  ck "⛔음성 — 멈춘 곳은 문지기 ③ 이다 (러너 값 게이트가 아니다)" "$(grep -c '원본과 바이트가 다르다' "$T/out")" 1
  rm -f "$T/root/init/seed3_final.xyz"
  ck "⛔음성 seed1 기록값이 틀리면 러너 값 게이트 → 8" "$(run REC_1='2.0214 15 1.6300')" 8
  ck "⛔음성 seed3 자리에 seed1 파일 → 러너 값 게이트 8" \
     "$(mkdir -p "$T/swap/gabia/B/seed3" && cp "$BSRC/kgy/B/seed1/final.xyz" "$T/swap/gabia/B/seed3/final.xyz" && run BSRC="$T/swap" A="$BSRC/kgy/B" ROOT="$T/root2")" 8
  rm -rf "$T"; [ "$f" = 0 ] && echo "selftest ✅ (음성 10 포함)" || echo "selftest ⛔"; exit "$f"
fi

gatekeep; rc=$?; [ "$rc" = 0 ] || exit "$rc"
exec bash "$RUNNER"
