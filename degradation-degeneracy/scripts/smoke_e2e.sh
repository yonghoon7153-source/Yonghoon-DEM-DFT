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

# run.sh 와 같은 규칙 — venv 밖에서 불러도 같은 인터프리터를 쓴다.
# (system python 은 import 실패 → dirty 판정 fallback 으로 오탐된다)
if [[ -d ".venv" && -z "${VIRTUAL_ENV:-}" ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

PY="${PYTHON:-python3}"
NPROC="${NPROC:-4}"
BASE="results/_smoke"
CURVES="$BASE/curves"
GFIT="$BASE/grid_fit"
HFIT="$BASE/halfcell_fit"

fail=0
# ★ F81/8차 발견 10 — smoke 는 기본이 **strict** 다. 어떤 provenance 실패도
#   건너뛰지 않는다. 예전에는 repo 전체 dirty 판정 + 자동 완화가 겹쳐, V100 의
#   무관한 se_curve 수정만으로 weakened mode 에 들어가 clean_worktree ·
#   코드_identity · 코드_재계산을 건너뛰었다 — "통과" 가 실제 보장보다 강했다.
#   개발 중 완화가 필요하면 **명시적으로** ALLOW_DIRTY=1 을 준다.
DIRTY="$("$PY" -c 'from src.io import git_info; print(1 if git_info(".")["git_dirty"] else 0)' 2>/dev/null || echo 1)"
if [[ "$DIRTY" == "1" && "${ALLOW_DIRTY:-0}" != "1" ]]; then
  printf '\033[31m실행 범위(src/tools/configs/scripts)가 dirty 입니다.\n'
  printf '커밋 후 다시 돌리세요. 개발 중 완화: ALLOW_DIRTY=1 %s\033[0m\n' "$0"
  exit 1
fi
export SMOKE_DIRTY="$DIRTY"

step() { printf '\n\033[1m── %s ──\033[0m\n' "$1"; }
ok()   { printf '   ✅ %s\n' "$1"; }
bad()  { printf '   ❌ %s\n' "$1"; fail=$((fail+1)); }

rm -rf "$BASE"
mkdir -p "$BASE"

# ─────────────────────────────────────── 0. 완방상태 캐시 (F82/F82b, 10차 발견 2)
step "0. 완방상태 준비 — solver recipe 봉인·거부 (F82b)"
"$PY" -m src.baseline --config configs/base.yaml --force --log-level WARNING >/dev/null \
  && ok "baseline --force (재계산 + baseline_hash·solver 봉인)" \
  || bad "완방상태 준비 실패"
_dcache="$(ls .cache/discharged_state/*.json 2>/dev/null | head -1)"
if [[ -n "$_dcache" ]]; then
  cp "$_dcache" "$_dcache.bak"
  "$PY" - "$_dcache" <<'PYEOF'
import json, sys
p = sys.argv[1]
d = json.load(open(p, encoding="utf-8"))
d["solver"] = {"name": "casadi", "rtol": 1e-3}      # 다른 recipe 로 위장
json.dump(d, open(p, "w", encoding="utf-8"))
PYEOF
  _msg="$("$PY" -m src.baseline --config configs/base.yaml --log-level ERROR 2>&1)"
  _rc=$?
  if [[ "$_rc" -ne 0 ]] && grep -q "다른 solver" <<<"$_msg"; then
    ok "다른 solver 로 계산된 캐시 거부 (F82b)"
  else
    bad "다른 solver 캐시가 거부되지 않았다 (rc=$_rc)"
  fi
  mv "$_dcache.bak" "$_dcache"
else
  bad "완방상태 캐시 파일이 없다"
fi

# ─────────────────────────────────────────────────────────────────── 1. 격자
step "1. PyBaMM 합성 격자 (producer artifact)"
./run.sh --mode grid --lli 0,0.1 --lam-pe 0,0.1 --lam-ne 0,0.1 \
         --noise 0 --nproc "$NPROC" --out "$CURVES" --log-level WARNING \
  && ok "곡선 생성" || bad "곡선 생성 실패"
[[ -f "$CURVES/curves_manifest.yaml" ]] \
  && ok "curves_manifest.yaml (F70 producer 기록)" \
  || bad "producer 기록이 없다 (F70)"
"$PY" - "$CURVES" <<'PYEOF'
import sys
from src.config import load_config
from src.io import validate_curves_provenance
# ★ 10차 자체 확인 2 — cfg 를 넘겨 실패라벨 guard 재검까지 태운다
v = validate_curves_provenance(sys.argv[1],
                               cfg=load_config("configs/grid_coarse.yaml"))
print(f"   {'✅' if v['ok'] else '❌'} producer 독립 검증 (F74): "
      + ("통과" if v["ok"] else f"실패 — {v['fail']}"))
sys.exit(0 if v["ok"] else 1)
PYEOF
[[ $? -eq 0 ]] || bad "producer 검증 실패"

# ★ F74 — 다른 config 로 resume 하면 서명 가드가 즉시 죽어야 한다
_msg="$(./run.sh --mode grid --lli 0,0.05 --lam-pe 0 --lam-ne 0 --noise 0 \
        --nproc 1 --resume --out "$CURVES" --log-level ERROR 2>&1)"
if [[ $? -ne 0 ]] && grep -q "grid_run_sig" <<<"$_msg"; then
  ok "다른 config 의 resume 혼합 차단 (F74)"
else
  bad "resume 혼합이 차단되지 않았다"
fi

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
# ★ 10차 — 캐시가 recipe 대로 재생성되는지 대조까지 한다 (V100 prep 과 동일 경로)
"$PY" -m src.halfcell --config configs/base.yaml --method ocp --verify \
      --log-level WARNING >/dev/null \
  && ok "halfcell --verify (재생성 대조)" || bad "halfcell --verify 실패"
# ★ 11차 발견 4 — **옛 meta 가 남아 있는 정상 운영 경로**. 코드가 바뀌면
#   캐시 hit 이 옛 배열을 그대로 돌려주고 --verify 는 갱신하지 않으므로
#   `코드_identity` 로 실패해야 하고, --force --verify 는 통과해야 한다.
_meta="$(ls "$CACHE_DIR"/*_ocp_*.meta.yaml | head -1)"
cp "$_meta" "$_meta.bak"
"$PY" - "$_meta" <<'PYEOF'
import sys
import yaml
p = sys.argv[1]
m = yaml.safe_load(open(p, encoding="utf-8"))
m["source_digest"] = "stale0000000"          # 옛 커밋에서 만든 캐시로 위장
yaml.safe_dump(m, open(p, "w", encoding="utf-8"), allow_unicode=True)
PYEOF
_msg="$("$PY" -m src.halfcell --config configs/base.yaml --method ocp --verify \
        --log-level ERROR 2>&1)"
if [[ $? -ne 0 ]] && grep -q "force --verify" <<<"$_msg"; then
  ok "옛 meta 캐시 → --verify 실패 + --force 안내 (11차 발견 4)"
else
  bad "stale meta 캐시가 --verify 를 통과했다"
fi
"$PY" -m src.halfcell --config configs/base.yaml --method ocp --force --verify \
      --log-level WARNING >/dev/null \
  && ok "--force --verify 로 복구 (운영 명령)" || bad "--force --verify 실패"
rm -f "$_meta.bak"

# ─────────────────────────────────────────────────────────────────── 4. fitting
step "4. 같은 곡선을 두 기준으로 fitting"
# ★ 11차 발견 5 — sweep 끝점(w=0 ≡ pocv_dvdq, w=1 ≡ pocv_dvdq_dqdv) 일치
#   검사를 실제로 태우려면 본 실행에 **두 끝점 목적함수가 모두** 있어야 한다.
FIT_OBJ="pocv_dvdq,pocv_dvdq_dqdv"
./run.sh --mode fit --in "$CURVES" --out "$GFIT" --reference grid \
         --objective "$FIT_OBJ" --n-restarts 2 --nproc "$NPROC" --log-level WARNING >/dev/null \
  && ok "Case 2 (grid 기준)" || bad "grid fit 실패"
./run.sh --mode fit --in "$CURVES" --out "$HFIT" --reference halfcell \
         --objective "$FIT_OBJ" --n-restarts 2 --nproc "$NPROC" --log-level WARNING >/dev/null \
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
step "6. 공정 paired 실행 — 33p/34p 쌍 (F66/F81)"
./run.sh --mode fit --in "$CURVES" --out "$BASE/paired" --reference grid \
         --objective pocv_dvdq,pocv_dvdq_dqdv --n-restarts 3 \
         --no-adaptive --no-warm-start \
         --nproc "$NPROC" --log-level WARNING >/dev/null
"$PY" - "$BASE/paired" <<'PYEOF'
import json, sys
import numpy as np
import pandas as pd
import yaml
from pathlib import Path
d = Path(sys.argv[1])
spec = yaml.safe_load((d / "manifest.yaml").read_text(encoding="utf-8"))["run_spec"]
assert spec["optimizer"]["adaptive"] is False
assert spec["warm_start"] is False
f = pd.read_parquet(d / "fits.parquet")
objs = sorted(set(f["objective"]))
assert objs == ["pocv_dvdq", "pocv_dvdq_dqdv"], objs
by = {}
for _, r in f.iterrows():
    rs = json.loads(r["restarts_json"])
    assert {e["i"] for e in rs} == {0, 1, 2}, "index 집합이 예산과 다르다"
    assert all(np.isfinite(e["J"]) and all(np.isfinite(x) for x in e["p"])
               for e in rs), "비유한 restart"
    by.setdefault(r["cond_id"], {})[r["objective"]] = \
        sorted((e["i"], e["source"]) for e in rs)
for cid, m in by.items():
    assert set(m) == {"pocv_dvdq", "pocv_dvdq_dqdv"}, f"조건 {cid}가 한쪽에만 있다"
    assert m["pocv_dvdq"] == m["pocv_dvdq_dqdv"], \
        f"조건 {cid}의 두 목적함수 restart (index,source)가 다르다"
print(f"   ✅ {len(by)}조건 × 2목적함수, 조건별 (index,source) 집합 동일, "
      "전부 3 restart·유한")
PYEOF
[[ $? -eq 0 ]] || bad "paired 공정성 검사 실패"

# ★ 10차 발견 3 — paired 도 채점 → 비교 → **보고서까지** 태운다. n_restarts≥3
#   에서 multistart_random_only 블록에 pairwise·paired 메타 키가 생기는데,
#   보고서 생성이 여기서 죽는 결함이 본 실행 직전까지 숨어 있었다.
./run.sh --mode score --in "$BASE/paired" >/dev/null 2>&1 \
  && ok "paired 채점" || bad "paired 채점 실패"
"$PY" -m tools.compare_objectives --in "$BASE/paired" >/dev/null 2>&1 \
  && ok "paired 목적함수 비교" || bad "paired 비교 실패"
"$PY" - "$BASE/paired" "$BASE/RESULTS_PAIRED.md" <<'PYEOF'
import os, re, sys
from pathlib import Path
import yaml
from tools.make_results import build
# 크래시 전제조건(무작위-전용 블록의 비-dict 메타 키)이 실제로 있는지 먼저 확인
s = yaml.safe_load((Path(sys.argv[1]) / "degeneracy_summary.yaml")
                   .read_text(encoding="utf-8")) or {}
blk = s.get("multistart_random_only") or {}
meta = [k for k, v in blk.items()
        if not str(k).startswith("_") and not isinstance(v, dict)]
assert meta, ("multistart_random_only 에 메타 키가 없다 — 10차 발견 3 의 "
              "크래시 경로가 재현되지 않는 표본이다 (조건 수 확인)")
text = build(sys.argv[1], sys.argv[2]).read_text(encoding="utf-8")
head = text[:2000]
if "인용 금지" not in head:
    print("   ✅ paired 보고서 생성 (n_restarts=3, pairwise 메타 키 포함)")
    sys.exit(0)
names = set(re.findall(r"`([^`]+)`", head.split("인용하지")[0]))
allowed = {"clean_worktree", "코드_identity"} \
    if os.environ.get("SMOKE_DIRTY") == "1" else set()
extra = {n for n in names if n not in allowed and not n.startswith("_")}
if extra:
    print(f"   ❌ paired 보고서 배너 — 허용 외 실패: {sorted(extra)}")
    sys.exit(1)
print("   ⚠ dirty 완화로 paired 배너 허용")
PYEOF
[[ $? -eq 0 ]] || bad "paired 보고서 생성 실패 (10차 발견 3)"

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

# ★ F81 — 실제 weight sweep 까지 돈다 (예전 smoke 는 sweep 을 전혀 안 돌았다)
# ★ 10차 — 본 실행이 쓰는 **run.sh wrapper 경로**로 돈다. 모듈 직접 호출만
#   태우면 wrapper 의 인자 전달(F79 --out 등) 회귀를 smoke 가 못 잡는다.
./run.sh --mode wsweep --in "$CURVES" --out "$GFIT/wsweep" \
         --w-grid 0,1 --w-stride 1 --n-restarts 2 --nproc "$NPROC" \
         --log-level WARNING >/dev/null 2>&1 \
  && ok "weight sweep (run.sh wrapper, w∈{0,1})" || bad "weight sweep 실패"
"$PY" - "$GFIT/wsweep" <<'PYEOF'
import sys
import yaml
from pathlib import Path
y = yaml.safe_load((Path(sys.argv[1]) / "weight_sweep.yaml").read_text(encoding="utf-8"))
need = [k for k in ("tol", "method", "adaptive", "fits_sha256",
                    "subset_curves_sha") if k not in y]
assert not need, f"weight_sweep.yaml 에 {need} 가 없다 (F79)"
assert (Path(sys.argv[1]) / "objectives_optimized.yaml").is_file(), \
    "optimized config 가 run 디렉터리에 없다 (F79)"
print("   ✅ sweep 기록: tol·method·adaptive·digest 봉인, optimized 는 run 디렉터리에")
PYEOF
[[ $? -eq 0 ]] || bad "sweep 기록 검사 실패"
# ★ 11차 발견 5 — 끝점 결과 일치를 **도구로** 확인한다 (보고서가 이 도구를
#   인용해 왔지만 아무도 호출하지 않았다). 불일치면 nonzero.
"$PY" -m tools.check_sweep_consistency --sweep "$GFIT/wsweep" --main "$GFIT" \
      >/dev/null 2>&1 \
  && ok "sweep 끝점 ↔ 본 실행 일치 (check_sweep_consistency)" \
  || bad "sweep 끝점이 본 실행과 다르다"

"$PY" - "$GFIT" "$BASE/RESULTS.md" <<'PYEOF'
import os, re, sys
from pathlib import Path
from tools.make_results import build
text = build(sys.argv[1], sys.argv[2]).read_text(encoding="utf-8")
head = text[:2000]
if "인용 금지" not in head:
    print("   ✅ 인용 금지 배너 없음 — 전 구간 provenance 통과")
    sys.exit(0)
# ★ F81 — 예전 분기는 첫 1,200자에 clean_worktree 만 보이면 **다른 실패가 함께
#   있어도** 성공 처리했다. 실패 검사 이름을 파싱해, ALLOW_DIRTY 에서 허용되는
#   집합(clean_worktree·코드_identity)만 있는지 본다.
names = set(re.findall(r"`([^`]+)`", head.split("인용하지")[0]))
allowed = {"clean_worktree", "코드_identity"} \
    if os.environ.get("SMOKE_DIRTY") == "1" else set()
extra = {n for n in names if n not in allowed and not n.startswith("_")}
if extra:
    print(f"   ❌ 배너가 떴다 — 허용 외 실패: {sorted(extra)}")
    sys.exit(1)
print("   ⚠ dirty 완화로 배너 허용 (실패가 clean_worktree·코드_identity 뿐)")
PYEOF
[[ $? -eq 0 ]] || bad "보고서에 인용 금지 배너가 떴다"

# ★ F81 — 파생 YAML 변조가 보고서에서 걸리는가 (재계산 렌더 + stale 배너)
"$PY" - "$GFIT" "$BASE/R_tamper.md" <<'PYEOF'
import shutil, sys
import yaml
from pathlib import Path
from tools.make_results import build
d = Path(sys.argv[1])
src = d / "objective_comparison.yaml"
bak = src.with_suffix(".yaml.bak")
shutil.copy2(src, bak)
try:
    y = yaml.safe_load(src.read_text(encoding="utf-8"))
    y["table"][0]["degenerate_frac"] = 0.123456
    src.write_text(yaml.safe_dump(y, allow_unicode=True), encoding="utf-8")
    text = build(d, sys.argv[2]).read_text(encoding="utf-8")
    assert "0.123456" not in text and "12.3456" not in text, "변조 값이 렌더됐다"
    assert "파생_stale_objective_comparison.yaml" in text, "stale 배너가 없다"
    print("   ✅ 파생 변조 → 재계산 렌더 + stale 배너 (F77)")
finally:
    shutil.copy2(bak, src)
    bak.unlink()
PYEOF
[[ $? -eq 0 ]] || bad "파생 변조 검출 실패"

# ───────────────────────────────────── 8. 보관 → 빈 격리 root 복원 → 검증 → 재채점
step "8. 보관 → 격리 복원 → 검증 → 재채점"
"$PY" -m tools.archive_bundle bundle "$HFIT" "$BASE/art" >/dev/null \
  && ok "bundle (halfcell)" || bad "bundle 실패"
"$PY" -m tools.archive_bundle bundle "$GFIT" "$BASE/art_g" >/dev/null \
  && ok "bundle (grid + nested sweep)" || bad "grid bundle 실패"
"$PY" -m tools.archive_bundle check "$BASE/art" >/dev/null \
  && ok "check" || bad "check 실패"
"$PY" -m tools.archive_bundle check "$BASE/art_g" >/dev/null \
  && ok "check (nested)" || bad "nested check 실패"

ISO="$(mktemp -d)"
"$PY" -m tools.archive_bundle restore "$BASE/art" --repo-root "$ISO" >/dev/null \
  && ok "격리 root 복원" || bad "복원 실패"
"$PY" -m tools.archive_bundle restore "$BASE/art_g" --repo-root "$ISO" >/dev/null \
  && ok "격리 복원 (grid+sweep)" || bad "grid 복원 실패"
"$PY" - "$ISO" "$HFIT" "$GFIT" <<'PYEOF'
import os, sys
from pathlib import Path
from src.io import validate_provenance
from tools.archive_bundle import nested_runs
SKIP = {"clean_worktree", "코드_identity", "코드_재계산"} \
    if os.environ.get("SMOKE_DIRTY") == "1" else set()
iso = Path(sys.argv[1])
bad = 0
for run in sys.argv[2:]:
    rd = iso / run
    for d in [rd] + nested_runs(rd):
        v = validate_provenance(d, repo_root=iso)
        left = [f for f in v["fail"] if f not in SKIP]
        tag = f"{run}" + (f"/{d.name}" if d != rd else "")
        print(f"   {'✅' if not left else '❌'} 격리 복원 검증[{tag}]: "
              + ("통과" if not left else f"실패 — {left}"))
        bad += 0 if not left else 1
sys.exit(1 if bad else 0)
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

# ★ F89/10차 — 보관 대상이 디스크에 없으면 **nonzero** 로 끝나야 한다.
#   예전에는 기본 대상이 전부 없어도 "검증 가능 0개" + exit 0 이었다.
if ./scripts/archive_results.sh "results/_smoke_missing_$$" >/dev/null 2>&1; then
  bad "없는 보관 대상인데 archive_results.sh 가 성공(exit 0)했다 (F89)"
else
  ok "없는 보관 대상 → nonzero 종료 (F89)"
fi

# ★ 11차 발견 6 — **기존 정상 묶음이 있는 상태에서 원본이 깨지면**, wrapper 는
#   실패로 끝나고 마지막 정상 묶음을 그대로 두어야 한다. 예전에는 stale 원본을
#   그대로 묶어 정상 묶음을 덮어쓰고 exit 0 이었다.
ARCH_TMP="$BASE/arch"
mkdir -p "$ARCH_TMP"
cp -a "$GFIT" "$BASE/keep_run"
"$PY" -m tools.archive_bundle bundle "$GFIT" "$ARCH_TMP/grid_fit" >/dev/null \
  && ok "기준 묶음 생성" || bad "기준 묶음 생성 실패"
_before="$(sha256sum "$ARCH_TMP/grid_fit/payload_sha256.yaml" | cut -d' ' -f1)"
"$PY" - "$GFIT" <<'PYEOF'
import sys
from pathlib import Path
import pandas as pd
f = Path(sys.argv[1]) / "fits.parquet"
df = pd.read_parquet(f)
df["lam_pe_hat"] = df["lam_pe_hat"] + 0.5      # 봉인과 어긋나게 만든다
df.to_parquet(f, index=False)
PYEOF
if "$PY" -m tools.archive_bundle bundle "$GFIT" "$ARCH_TMP/grid_fit" >/dev/null 2>&1; then
  bad "봉인과 다른 bytes 를 그대로 묶었다 (11차 발견 6)"
else
  _after="$(sha256sum "$ARCH_TMP/grid_fit/payload_sha256.yaml" | cut -d' ' -f1)"
  [[ "$_before" == "$_after" ]] \
    && ok "실패한 재보관이 기존 묶음을 보존 (11차 발견 6)" \
    || bad "실패한 재보관이 기존 묶음을 파괴했다"
fi
rm -rf "$GFIT" && mv "$BASE/keep_run" "$GFIT"   # 변조본 폐기, 원본 복구

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
