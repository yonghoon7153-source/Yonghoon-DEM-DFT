#!/usr/bin/env bash
# =============================================================================
# run_uma_sp_kgy.sh — 외주 2차 카드 (wad_p2small_vasp_card_2026_10_15) 빌드 ④: P2′ 봉인 구조 9 개 UMA 단일점 (D3 없음 · G5_C 의 W_UMA 용)
#                     kgy · cascade v7 · Nd EOS pw.x 옆 · 이완 러너 (run_relax_kgy.sh) 와 같은 판·같은 가드 · 10-15 V5 단일점 kgy 선례와 같은 꼴
#
# 쓰는 법 (worktree 뿌리에서 · tmux 안에서 · 봉인이 커밋된 판)
#   DRY_RUN=1 bash db/inputs/wad_p2small_geometries_2026_10_17/run_uma_sp_kgy.sh   # ①② 만 (봉인 대조 · 판 · GPU) — 계산 0
#   bash db/inputs/wad_p2small_geometries_2026_10_17/run_uma_sp_kgy.sh
#
# 순서: ① 봉인 대조 (structures/*.extxyz 9 개 = p2s_seal_manifest.json structures_sha256 · 이름 = 집계기 UMA_NAMES 6 + UMA_G3 3)
#       ② 판 (fairchem · torch · ase · GPU)
#       ③ 단일점 (tools/wad/relax_uma_d3.py --energies · uma-s-1p1 · omat · default · D3 없음 · 3축 pbc · 가드)
#       ④ 결박 대조 (체크포인트 sha 앞 16 = S1 결박값 07068e9c76702ca1 · 모델·과제·추론 설정 · 9 행 sha = 봉인) — 어긋나면 끝 코드 5
#          (파일은 남긴다 — 집계기 load_uma 도 같은 것을 보고 거부한다)
#       ⑤ 끝 줄 → SOURCE_COMMIT · SHA256SUMS (끝 줄을 queue.log 에 먼저 쓰고 해시한다)
# 가드 (relax_uma_d3.py 가 건다): 시작 문턱 GPU 합계 ≤ START_MAX (16,000) · 합계 > KILL_TOTAL (23,500) 이면 **이 계산만** 종료 3 ·
#       torch 상한 VRAM_CAP (4,000 MiB) — ⚠ 감시는 2 s 표본이다. cascade · EOS 러너는 건드리지 않는다.
# 종료: 0 끝 · 3 가드 · 4 시작 문턱 못 엶 (계산 0 · JSON 0) · 5 결박 불일치 · 6 결과 JSON 이 이미 있음 (덮어쓰지 않는다)
#       · 7 python · fairchem 없음 · 8 이미 실행 중 · 9 봉인 불일치 · 그 밖 = relax_uma_d3.py 의 끝 코드
# ⛔ 못 하는 것: W · Δ_C · G5_C 판정 없음 (집계기 몫 · VASP 반송 뒤) · D3 항을 계산하지 않는다 (Δ_C 의 D3 는 VASP 출력에서 —
#    카드 개정 1 규약) · 봉인 구조를 고치거나 고르지 않는다 · cascade · EOS 를 멈추거나 늦추지 않는다 (SM 을 나눠 써서 그동안 조금 느려진다).
# =============================================================================
set -u
cd "$(dirname "$0")/../../.." || exit 9
SEAL=${SEAL:-db/inputs/wad_p2small_seal_2026_10_17}
OUT=${OUT:-$HOME/work/runs/wad_p2small_uma_sp_2026_10_17}
PY=${PY:-/home/kgy/apps/miniforge3/envs/uma/bin/python}
START_MAX=${START_MAX:-16000}; KILL_TOTAL=${KILL_TOTAL:-23500}; VRAM_CAP=${VRAM_CAP:-4000}; WAIT_S=${WAIT_S:-21600}
CKPT16=${CKPT16:-07068e9c76702ca1}
EXTRA=${EXTRA:-}     # 시험용 (기본 = 추가 인자 없음) — 실행 블록에서는 주지 않는다
NAMES="S_A_bound S_A_far S_A_p05_bound Li_A_bound Li_A_far Li_A_p05_bound S_A_G3_c2_bound S_A_G3_c2_far_i S_A_G3_c2_far_ii"
J=$OUT/uma_energies_p2s_2026_10_17.json
mkdir -p "$OUT"
Q=$OUT/queue.log
say(){ echo "[$(date '+%F %T')] $*" | tee -a "$Q"; }

exec 9>"$OUT/.lock"
flock -n 9 || { say "⛔ 이미 실행 중 ($OUT/.lock) — 시작 안 함"; exit 8; }
for x in $(pgrep -f "relax_uma_d3.py --energies.*$OUT"); do
  case "$(cat /proc/$x/comm 2>/dev/null)" in python*) say "⛔ 이미 도는 단일점 PID $x — 시작 안 함"; exit 8;; esac
done
[ -e "$J" ] && { say "⛔ $J 가 이미 있다 — 덮어쓰지 않는다 (다시 돌리려면 사람이 옮긴다)"; exit 6; }
say "════ P2′ 봉인 구조 UMA 단일점 · kgy · HEAD $(git rev-parse --short HEAD 2>/dev/null) · SEAL $SEAL · OUT $OUT ════"

# ① 봉인 대조
"$PY" - "$SEAL" $NAMES <<'PY' 2>&1 | tee -a "$Q"
import hashlib, json, os, sys
S, want = sys.argv[1], sys.argv[2:]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
mp = os.path.join(S, "p2s_seal_manifest.json")
try:
    ss = json.load(open(mp, encoding="utf-8"))["structures_sha256"]
    have = sorted(f[:-7] for f in os.listdir(os.path.join(S, "structures")) if f.endswith(".extxyz"))
except Exception as e:  # noqa: BLE001
    print(f"  ✗ 봉인 못 읽음 — {type(e).__name__}: {e}"); sys.exit(1)
bad = 0
if have != sorted(want) or sorted(ss) != sorted(want):
    print(f"  ✗ 이름 집합 — 폴더 {have} · 봉인 {sorted(ss)} · 기대 {sorted(want)}"); bad += 1
for n in want:
    p = os.path.join(S, "structures", n + ".extxyz")
    got = sha(p) if os.path.isfile(p) else "없음"
    ok = got == ss.get(n)
    bad += not ok
    print(f"  {'✓' if ok else '✗'} {n}.extxyz {got[:16]}")
print(f"  봉인 manifest sha {sha(mp)[:16]}")
sys.exit(1 if bad else 0)
PY
[ "${PIPESTATUS[0]}" = 0 ] || { say "⛔ 봉인 불일치 — 시작 안 함"; exit 9; }

# ② 판
"$PY" - <<'PY' 2>&1 | tee -a "$Q"
import sys
try:
    import fairchem.core as fc, torch, ase
except Exception as e:  # noqa: BLE001
    print(f"  ✗ {type(e).__name__}: {e}"); sys.exit(1)
print(f"  판: fairchem.core {getattr(fc, '__version__', '?')} · torch {torch.__version__} · cuda {torch.version.cuda} · ase {ase.__version__} · GPU {torch.cuda.is_available()}")
PY
[ "${PIPESTATUS[0]}" = 0 ] || { say "⛔ $PY 에 fairchem 이 없다 — 시작 안 함"; exit 7; }
say "GPU 합계 $(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits -i 0 2>/dev/null || echo '?') MiB · 문턱 $START_MAX · 감시 $KILL_TOTAL · 상한 $VRAM_CAP"
[ "${DRY_RUN:-0}" = 1 ] && { say "DRY_RUN — 여기서 끝 (계산 0)"; exit 0; }

# ③ 단일점
say "▶ 단일점 9 구조 (D3 없음)"
"$PY" tools/wad/relax_uma_d3.py --energies $(for n in $NAMES; do echo "$SEAL/structures/$n.extxyz"; done) --out "$J" \
  --gpu_start_max_mib "$START_MAX" --gpu_wait_s "$WAIT_S" --gpu_kill_total_mib "$KILL_TOTAL" --vram_cap_mib "$VRAM_CAP" $EXTRA > "$OUT/uma.log" 2>&1
rc=$?
say "단일점 rc=$rc"
[ "$rc" = 0 ] || { say "⛔ 단일점 rc=$rc — 멈춘다 ($OUT/uma.log)"; exit "$rc"; }

# ④ 결박 대조
"$PY" - "$J" "$SEAL" "$CKPT16" $NAMES <<'PY' 2>&1 | tee -a "$Q"
import json, os, sys
J, S, ck16, want = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
r = json.load(open(J, encoding="utf-8"))
ss = json.load(open(os.path.join(S, "p2s_seal_manifest.json"), encoding="utf-8"))["structures_sha256"]
c, E = r.get("calculator") or {}, r.get("energies") or {}
ck = c.get("checkpoint")
got16 = ck[0]["sha256"][:16] if isinstance(ck, list) and ck and isinstance(ck[0], dict) and ck[0].get("sha256") else "none"
bad = []
if got16 != ck16:
    bad.append(f"체크포인트 sha 앞 16 {got16} ≠ S1 결박값 {ck16}")
for k, v in (("model", "uma-s-1p1"), ("task", "omat"), ("inference_settings", "default")):
    if ck16 != "none" and c.get(k) != v:
        bad.append(f"calculator.{k} = {c.get(k)!r} (결박 {v!r})")
if sorted(E) != sorted(want):
    bad.append(f"행 이름 {sorted(E)} ≠ {sorted(want)}")
for n in want:
    if (E.get(n) or {}).get("sha256") != ss.get(n):
        bad.append(f"{n}: 계산한 구조 sha ≠ 봉인")
print(f"  결박: fairchem.core {c.get('fairchem.core')} · {c.get('model')} · {c.get('task')} · {c.get('inference_settings')} · 체크포인트 {got16} · 행 {len(E)}")
for b in bad:
    print(f"  ✗ {b}")
sys.exit(1 if bad else 0)
PY
[ "${PIPESTATUS[0]}" = 0 ] || { say "⛔ 결박 불일치 — 끝 코드 5 (파일은 남김 · 집계기도 거부)"; exit 5; }
say "결박 ✓"

# ⑤ 끝 줄 → 해시 (끝 줄을 먼저 쓴다 — 해시 뒤에 queue.log 를 건드리지 않는다)
git rev-parse HEAD > "$OUT/SOURCE_COMMIT" 2>/dev/null || echo unknown > "$OUT/SOURCE_COMMIT"
say "■ 끝 · 끝 코드 0"
( cd "$OUT" && find . -type f ! -name '.lock' ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS )
echo "SHA256SUMS $(wc -l < "$OUT/SHA256SUMS") 줄 (queue.log 포함 · 이 줄은 queue.log 에 안 쓴다)"
exit 0
