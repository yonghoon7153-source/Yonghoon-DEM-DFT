#!/usr/bin/env bash
# =============================================================================
# run_relax_kgy.sh — 외주 2차 카드 (wad_p2small_vasp_card_2026_10_15) G1: P2′ 부모 둘 (S_A · Li_A) UMA+D3 이완
#                    kgy · 한 번에 하나 · cascade v7 · Nd EOS pw.x 옆 (사용자 2026-10-17 'kgy · cascade·EOS 옆')
#
# 쓰는 법 (worktree 뿌리에서 · tmux 안에서)
#   DRY_RUN=1 bash db/inputs/wad_p2small_geometries_2026_10_17/run_relax_kgy.sh   # ①② 만 (입력 해시 · 판 · D3 · GPU) — 계산 0
#   bash db/inputs/wad_p2small_geometries_2026_10_17/run_relax_kgy.sh
#
# 순서: ① 입력 해시 (bound·far 파일 = meta.json sha256 = build_record.json)  ② 판 기록 (fairchem · torch · ase · simple-dftd3)
#       ③ 메모리 프로브 (S_A · 힘 한 번 · 체크포인트 sha 앞 16 = S1 결박값 07068e9c76702ca1 이어야 계속)
#       ④ 이완 S_A → Li_A  ⑤ SHA256SUMS (opt.traj 제외 — 회수 대상 아님)
# 결박: tools/wad/relax_uma_d3.py — uma-s-1p1 · omat · default · D3(BJ) 2체 **simple-dftd3 고정** (`--d3 dftd3` · auto 아님 —
#       다른 구현으로 조용히 넘어가지 않는다 · 이전 W_ad 이완 전부가 simple-dftd3) · FIRE · fmax 0.02 · 3000 스텝 · 셀 고정 · 마스크 = 빌더 far_half
# 가드 (relax_uma_d3.py 가 건다 · 10-15 V5 단일점 kgy 선례와 같은 꼴):
#   시작 문턱 GPU 합계 ≤ START_MAX (16,000) · 합계 > KILL_TOTAL (23,500) 이면 **이 이완만** 종료 3 · torch 상한 VRAM_CAP (4,000 MiB)
#   ⚠ 감시는 2 s 표본이다 — 표본 간격보다 빠른 급등은 못 막는다. cascade · EOS 러너는 건드리지 않는다.
# 이어 돌리기: relax_meta.json 이 있는 모델은 건너뛴다 (그 파일의 수렴·깃발을 끝 코드에 반영 · 다시 돌리려면 폴더를 사람이 옮긴다).
# 종료: 0 끝 · 2 이완 미수렴 또는 깃발 (파일 남김 · 다음 모델은 돈다 · 끝 코드 2) · 3 가드 · 4 시작 문턱 못 엶 · 5 체크포인트 결박 불일치
#       · 7 python · fairchem · simple-dftd3 없음 · 8 이미 실행 중 · 9 입력 해시 불일치
# ⛔ 못 하는 것: W·에너지 판정 없음 (이완 모드) · p05 · far · 봉인 · D3 만 G3 예측은 회수 뒤 레포에서 · cascade · EOS 를 멈추거나 늦추지 않는다
#    (SM 을 나눠 써서 그동안 조금 느려진다).
# =============================================================================
set -u
cd "$(dirname "$0")/../../.." || exit 9
G=db/inputs/wad_p2small_geometries_2026_10_17
OUT=${OUT:-$HOME/work/runs/wad_p2small_relax_2026_10_17}
PY=${PY:-/home/kgy/apps/miniforge3/envs/uma/bin/python}
START_MAX=${START_MAX:-16000}; KILL_TOTAL=${KILL_TOTAL:-23500}; VRAM_CAP=${VRAM_CAP:-4000}; WAIT_S=${WAIT_S:-21600}
CKPT16=${CKPT16:-07068e9c76702ca1}
MODELS=${MODELS:-"P2S_s_outer P2S_li_outer"}
STEPS=${STEPS:-3000}; EXTRA=${EXTRA:-}     # 시험용 (기본 = 카드 G1 3000 스텝 · 추가 인자 없음) — 실행 블록에서는 주지 않는다
mkdir -p "$OUT/logs" "$OUT/relax" "$OUT/probe"
Q=$OUT/queue.log
say(){ echo "[$(date '+%F %T')] $*" | tee -a "$Q"; }

exec 9>"$OUT/.lock"
flock -n 9 || { say "⛔ 이미 실행 중 ($OUT/.lock) — 시작 안 함"; exit 8; }
for x in $(pgrep -f "relax_uma_d3.py.*$OUT"); do
  case "$(cat /proc/$x/comm 2>/dev/null)" in python*) say "⛔ 이미 도는 이완 PID $x — 시작 안 함"; exit 8;; esac
done
say "════ P2′ 부모 둘 UMA+D3 이완 · kgy · HEAD $(git rev-parse --short HEAD 2>/dev/null) · OUT $OUT ════"

# ① 입력 해시
"$PY" - "$G" $MODELS <<'PY' 2>&1 | tee -a "$Q"
import hashlib, json, os, sys
G, models = sys.argv[1], sys.argv[2:]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
rec = json.load(open(os.path.join(G, "build_record.json"), encoding="utf-8"))
want = {v["dir"].split("/")[0]: v["sha256"] for v in rec["samples"].values()}
bad = 0
for m in models:
    meta = json.load(open(os.path.join(G, m, "A", "meta.json"), encoding="utf-8"))
    for k in ("bound", "far"):
        got = sha(os.path.join(G, m, "A", f"{k}.extxyz"))
        ok = got == meta["sha256"][k] == want[m][k]
        bad += not ok
        print(f"  {'✓' if ok else '✗'} {m}/A/{k}.extxyz {got[:16]}")
sys.exit(1 if bad else 0)
PY
[ "${PIPESTATUS[0]}" = 0 ] || { say "⛔ 입력 해시 불일치 — 시작 안 함"; exit 9; }

# ② 판 · D3
"$PY" - <<'PY' 2>&1 | tee -a "$Q"
import sys
try:
    import fairchem.core as fc, torch, ase, dftd3
    from dftd3.ase import DFTD3  # noqa: F401
except Exception as e:  # noqa: BLE001
    print(f"  ✗ {type(e).__name__}: {e}"); sys.exit(1)
print(f"  판: fairchem.core {getattr(fc, '__version__', '?')} · torch {torch.__version__} · cuda {torch.version.cuda} · ase {ase.__version__} · simple-dftd3 {getattr(dftd3, '__version__', '?')} · GPU {torch.cuda.is_available()}")
PY
[ "${PIPESTATUS[0]}" = 0 ] || { say "⛔ $PY 에 fairchem · simple-dftd3 (dftd3) 가 없다 — 시작 안 함 (D3 구현을 바꾸지 않는다)"; exit 7; }
say "GPU 합계 $(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits -i 0 2>/dev/null || echo '?') MiB · 문턱 $START_MAX · 감시 $KILL_TOTAL · 상한 $VRAM_CAP"
[ "${DRY_RUN:-0}" = 1 ] && { say "DRY_RUN — 여기서 끝 (계산 0)"; exit 0; }

GUARD=(--d3 dftd3 --gpu_start_max_mib "$START_MAX" --gpu_wait_s "$WAIT_S" --gpu_kill_total_mib "$KILL_TOTAL" --vram_cap_mib "$VRAM_CAP")

# ③ 메모리 프로브 + 체크포인트 결박
if [ ! -f "$OUT/probe/mem_probe.json" ]; then
  say "▶ 프로브 P2S_s_outer/A (힘 한 번)"
  "$PY" tools/wad/relax_uma_d3.py --model_dir "$G/P2S_s_outer/A" --out "$OUT/probe" --mem_probe "${GUARD[@]}" $EXTRA > "$OUT/logs/probe.log" 2>&1
  rc=$?
  say "프로브 rc=$rc · $(grep -ao '"max_reserved_MiB": [0-9]*' "$OUT/logs/probe.log" | head -1)"
  [ "$rc" = 0 ] || { say "⛔ 프로브 실패 rc=$rc — 멈춘다 ($OUT/logs/probe.log)"; exit "$rc"; }
fi
ck=$("$PY" -c "import json,sys; c=json.load(open(sys.argv[1]))['calculator'].get('checkpoint'); print(c[0]['sha256'][:16] if isinstance(c, list) and c else 'none')" "$OUT/probe/mem_probe.json")
[ "$ck" = "$CKPT16" ] || { say "⛔ 체크포인트 sha 앞 16 $ck ≠ S1 결박값 $CKPT16 — 멈춘다"; exit 5; }
say "체크포인트 결박 ✓ $ck"

# ④ 이완
final=0
for m in $MODELS; do
  d="$OUT/relax/$m/A"
  if [ -f "$d/relax_meta.json" ]; then
    st=$("$PY" -c "import json,sys; r=json.load(open(sys.argv[1])); print('수렴·깃발 0' if r.get('converged_fmax') and not r.get('interface_check_flags') else '미수렴 또는 깃발')" "$d/relax_meta.json")
    say "건너뜀 $m/A (relax_meta.json 있음 · $st)"; [ "$st" = "수렴·깃발 0" ] || final=2; continue
  fi
  say "▶ $m/A"
  "$PY" tools/wad/relax_uma_d3.py --model_dir "$G/$m/A" --out "$d" --fmax 0.02 --steps "$STEPS" "${GUARD[@]}" $EXTRA > "$OUT/logs/${m}_A.log" 2>&1
  rc=$?
  say "$m/A rc=$rc · $(grep -ao '"steps_taken": [0-9]*\|"converged_fmax": [a-z]*\|"wall_s": [0-9.]*' "$OUT/logs/${m}_A.log" | tr '\n' ' ')"
  case $rc in
    0) ;;
    2) final=2; say "⚠ $m/A 미수렴 또는 깃발 — 파일 남김 · 다음 모델은 돈다" ;;
    *) say "⛔ $m/A rc=$rc — 큐를 멈춘다"; exit "$rc" ;;
  esac
done

# ⑤ 해시
( cd "$OUT" && find . -type f ! -name 'opt.traj' ! -name '.lock' ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS )
say "■ 큐 끝 · 끝 코드 $final · SHA256SUMS $(wc -l < "$OUT/SHA256SUMS") 줄"
exit "$final"
