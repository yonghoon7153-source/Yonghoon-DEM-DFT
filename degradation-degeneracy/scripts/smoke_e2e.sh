#!/usr/bin/env bash
# =============================================================================
#  smoke_e2e.sh — 본 실행(약 10시간) 전에 **전 구간이 맞물리는지** 확인한다
#
#  7차 게이트 리뷰 §6 마지막 문장:
#    "실제 cache-miss → fit → score → compare → bundle → 빈 격리 clone restore
#     → validate → 재채점의 end-to-end smoke 를 통과한 뒤 본 실행을 시작해야 한다."
#
#  왜 필요한가
#  ───────────
#  일곱 라운드 내내 같은 실패 형태가 반복됐다 — 단위 테스트는 전부 통과하는데
#  실제 pipeline 을 태우면 죽거나, 죽지 않고 **틀린 것을 통과시켰다.** 대표적으로
#  F63: `reference="halfcell"` 로 run_fit 을 태우는 테스트가 하나도 없어서,
#  half-cell 첫 실행이 항상 실패하는 상태로 205개가 전부 통과했다.
#
#  그래서 이 스크립트는 mock 을 쓰지 않는다. 진짜 PyBaMM 으로 작은 격자를 만들고,
#  진짜 fitting 을 돌리고, 진짜로 묶어서 **빈 root 에 복원해 거기서 검증**한다.
#
#  사용:
#    ./scripts/smoke_e2e.sh              # 약 2~5분 (조건 8개)
#    KEEP=1 ./scripts/smoke_e2e.sh       # 산출물을 지우지 않는다 (디버깅)
# =============================================================================
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PY="${PYTHON:-python3}"
NPROC="${NPROC:-4}"
BASE="results/_smoke"
CURVES="$BASE/curves"
GFIT="$BASE/grid_fit"
HFIT="$BASE/halfcell_fit"

fail=0
# ★ dirty worktree 에서는 `clean_worktree`·`코드_identity` 가 정의상 실패한다.
#   개발 중에 이 smoke 를 돌릴 수 있어야 하므로 그 둘만 제외하고, 대신 크게 경고한다.
#   본 실행은 반드시 clean 커밋에서 시작해야 한다.
DIRTY=0
git diff --quiet HEAD 2>/dev/null || DIRTY=1
export SMOKE_DIRTY="$DIRTY"

step() { printf '\n\033[1m── %s ──\033[0m\n' "$1"; }
ok()   { printf '   ✅ %s\n' "$1"; }
bad()  { printf '   ❌ %s\n' "$1"; fail=$((fail+1)); }

rm -rf "$BASE"
mkdir -p "$BASE"

# ─────────────────────────────────────────────────────────────────── 1. 격자
step "1. PyBaMM 합성 격자 (producer artifact)"
./run.sh --mode grid --lli 0,0.1 --lam-pe 0,0.1 --lam-ne 0,0.1 \
         --noise 0 --nproc "$NPROC" --out "$CURVES" --log-level WARNING \
  && ok "곡선 생성" || bad "곡선 생성 실패"
[[ -f "$CURVES/curves_manifest.yaml" ]] \
  && ok "curves_manifest.yaml (F70 producer 기록)" \
  || bad "producer 기록이 없다 (F70)"

# ───────────────────────────────────────────────── 2. cache-miss 는 멈춰야 한다
step "2. half-cell 캐시 없음 → 안내하며 멈추는가 (F63)"
CACHE_DIR=".cache/halfcell"
STASH="$(mktemp -d)"
[[ -d "$CACHE_DIR" ]] && cp -a "$CACHE_DIR/." "$STASH/" 2>/dev/null
rm -rf "$CACHE_DIR"
# ⚠ `if cmd | grep -q` 로 쓰면 안 된다 — `set -o pipefail` 이라 run.sh 가
#   (정상적으로) nonzero 로 죽으면 grep 이 맞아도 파이프라인 상태가 1이 된다.
#   출력을 먼저 받고 검사한다.
_msg="$(./run.sh --mode fit --in "$CURVES" --out "$BASE/_should_fail" \
        --reference halfcell --objective pocv --nproc 1 --log-level ERROR 2>&1)"
_rc=$?
if [[ "$_rc" -ne 0 ]] && grep -q "python -m src.halfcell" <<<"$_msg"; then
  ok "안내와 함께 중단 (조용한 캐시 생성 없음)"
else
  bad "cache-miss 에서 멈추지 않았거나 안내가 없다 (rc=$_rc)"
fi
rm -rf "$BASE/_should_fail"

step "3. half-cell 기준 준비 (봉인 가능한 별도 단계)"
"$PY" -m src.halfcell --config configs/base.yaml --method ocp --log-level WARNING >/dev/null \
  && ok "캐시 + recipe meta 생성" || bad "준비 단계 실패"
# 파일명은 `<baseline>_<method>_<recipe>.meta.yaml` — recipe 해시가 가운데 온다
ls "$CACHE_DIR"/*_ocp_*.meta.yaml >/dev/null 2>&1 \
  && ok "recipe meta 사이드카 (F64)" || bad "recipe meta 가 없다"

# ─────────────────────────────────────────────────────────────────── 4. fitting
step "4. 같은 곡선을 두 기준으로 fitting"
./run.sh --mode fit --in "$CURVES" --out "$GFIT" --reference grid \
         --objective pocv,pocv_dvdq --n-restarts 2 --nproc "$NPROC" --log-level WARNING >/dev/null \
  && ok "Case 2 (grid 기준)" || bad "grid fit 실패"
./run.sh --mode fit --in "$CURVES" --out "$HFIT" --reference halfcell \
         --objective pocv,pocv_dvdq --n-restarts 2 --nproc "$NPROC" --log-level WARNING >/dev/null \
  && ok "Case 1 (half-cell 기준)" || bad "halfcell fit 실패"

step "5. provenance — 두 산출물 모두 인용 가능한가"
"$PY" - "$GFIT" "$HFIT" <<'PYEOF'
import os, sys
from src.io import validate_provenance
# dirty worktree 에서는 이 둘이 정의상 실패한다 (본 실행은 clean 에서 해야 한다)
SKIP = {"clean_worktree", "코드_identity"} if os.environ.get("SMOKE_DIRTY") == "1" else set()
bad = 0
for d in sys.argv[1:]:
    v = validate_provenance(d)
    left = [f for f in v["fail"] if f not in SKIP]
    print(f"   {'✅' if not left else '❌'} {d}: "
          + ("통과" if not left else f"실패 — {left}")
          + (f"  (dirty 라 {sorted(SKIP)} 제외)" if SKIP and v["fail"] else ""))
    bad += 0 if not left else 1
sys.exit(1 if bad else 0)
PYEOF
[[ $? -eq 0 ]] || bad "provenance 검증 실패"

# ───────────────────────────────────────────── 6. adaptive off (paired 실행 가능)
step "6. --no-adaptive 가 실제로 도달하는가 (F66)"
./run.sh --mode fit --in "$CURVES" --out "$BASE/paired" --reference grid \
         --objective pocv_dvdq --n-restarts 3 --no-adaptive --no-warm-start \
         --nproc "$NPROC" --log-level WARNING >/dev/null
"$PY" - "$BASE/paired" <<'PYEOF'
import json, sys
import pandas as pd
import yaml
from pathlib import Path
d = Path(sys.argv[1])
spec = yaml.safe_load((d / "manifest.yaml").read_text(encoding="utf-8"))["run_spec"]
n = {len(json.loads(v)) for v in pd.read_parquet(d / "fits.parquet")["restarts_json"]}
assert spec["optimizer"]["adaptive"] is False, "서명에 adaptive=False 가 없다"
assert n == {3}, f"restart 수가 갈린다: {sorted(n)}"
print("   ✅ 모든 조건이 정확히 3 restart, 서명에 adaptive=False")
PYEOF
[[ $? -eq 0 ]] || bad "paired 실행 설정이 관철되지 않았다"

# ────────────────────────────────────────────────────── 7. 채점 → 비교 → 보고서
step "7. 채점 · 비교 · 보고서"
for d in "$GFIT" "$HFIT"; do
  ./run.sh --mode score --in "$d" >/dev/null 2>&1 || bad "채점 실패: $d"
done
ok "채점"

"$PY" -m tools.compare_objectives --in "$GFIT" >/dev/null 2>&1 \
  && ok "목적함수 비교" || bad "목적함수 비교 실패"
"$PY" -m tools.compare_cases --grid "$GFIT" --halfcell "$HFIT" \
      --log-level ERROR >/dev/null 2>&1 \
  && ok "기준 곡선 비교" || bad "기준 비교 실패"

"$PY" - "$GFIT" "$BASE/RESULTS.md" <<'PYEOF'
import sys
from pathlib import Path
from tools.make_results import build
text = build(sys.argv[1], sys.argv[2]).read_text(encoding="utf-8")
import os
if os.environ.get("SMOKE_DIRTY") == "1" and "clean_worktree" in text[:1200]:
    print("   ⚠ dirty worktree 라 배너가 뜬다 — 본 실행은 clean 커밋에서 시작할 것")
elif "인용 금지" in text[:800]:
    head = text[:800].replace("\n", " ")
    print(f"   ❌ 배너가 떴다: {head[:300]}")
    sys.exit(1)
print("   ✅ 인용 금지 배너 없음 — 전 구간 provenance 통과")
PYEOF
[[ $? -eq 0 ]] || bad "보고서에 인용 금지 배너가 떴다"

# ───────────────────────────────────── 8. 보관 → 빈 격리 root 복원 → 검증 → 재채점
step "8. 보관 → 격리 복원 → 검증 → 재채점"
"$PY" -m tools.archive_bundle bundle "$HFIT" "$BASE/art" >/dev/null \
  && ok "bundle" || bad "bundle 실패"
"$PY" -m tools.archive_bundle check "$BASE/art" >/dev/null \
  && ok "check" || bad "check 실패"

ISO="$(mktemp -d)"
"$PY" -m tools.archive_bundle restore "$BASE/art" --repo-root "$ISO" >/dev/null \
  && ok "격리 root 복원" || bad "복원 실패"
"$PY" - "$ISO" "$HFIT" <<'PYEOF'
import os, sys
from pathlib import Path
from src.io import validate_provenance
SKIP = {"clean_worktree", "코드_identity", "코드_재계산"} \
    if os.environ.get("SMOKE_DIRTY") == "1" else set()
iso, run = Path(sys.argv[1]), sys.argv[2]
v = validate_provenance(iso / run, repo_root=iso)
left = [f for f in v["fail"] if f not in SKIP]
print(f"   {'✅' if not left else '❌'} 격리 복원본 검증: "
      + ("통과" if not left else f"실패 — {left}"))
sys.exit(0 if not left else 1)
PYEOF
[[ $? -eq 0 ]] || bad "격리 복원본이 검증을 통과하지 못했다"

"$PY" - "$ISO" "$HFIT" <<'PYEOF'
import sys
from pathlib import Path
from src.scoring import run_scoring
iso, run = Path(sys.argv[1]), sys.argv[2]
s = run_scoring(iso / run)
assert s["_채점원본"]["인용가능"] is True, s["_채점원본"]
print(f"   ✅ 복원본 재채점: 정본 확인, digest {s['_채점원본']['fits_sha256'][:12]}")
PYEOF
[[ $? -eq 0 ]] || bad "복원본 재채점 실패"
rm -rf "$ISO"

# ────────────────────────────────────────────────────────────────── 마무리
[[ -d "$STASH" ]] && cp -a "$STASH/." "$CACHE_DIR/" 2>/dev/null; rm -rf "$STASH"
[[ "${KEEP:-0}" == "1" ]] || rm -rf "$BASE"

printf '\n'
[[ "$DIRTY" == "1" ]] && printf \
  '\033[33m⚠ dirty worktree 에서 돌렸다 — clean_worktree·코드_identity 는 제외했다.\n   본 실행은 반드시 커밋 후 clean 상태에서 시작할 것.\033[0m\n'
if [[ "$fail" -eq 0 ]]; then
  printf '\033[1m✅ end-to-end smoke 통과 — 본 실행을 시작해도 된다\033[0m\n'
  exit 0
fi
printf '\033[1m❌ 실패 %d건 — 본 실행을 시작하지 말 것\033[0m\n' "$fail"
exit 1
