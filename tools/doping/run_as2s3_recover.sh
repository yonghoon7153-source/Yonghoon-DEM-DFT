#!/usr/bin/env bash
# =============================================================================
# run_as2s3_recover.sh — As2S3 를 cascade 로스터에 되살린다 (2026-08-20).
#
# 왜 (근거는 사전 한 줄이다)
#   As2S3 은 stage-01 에서 n_structures = 0 으로 죽어 91→89 의 한 칸이 됐다.
#   원인은 물리가 아니라 **ALTERNATIVE_VALENCES 에 'As' 가 없던 것**이다:
#     DOPANT_DB['As'] 기본 +5 → As2S3 net_q = 2(+5)+3(−2) = +4 (중성 아님)
#     → +3 재시도를 못 해 즉사.  바로 윗줄 'Sb': [+5,+3] 은 같은 15족·같은 M2S3 인데 통과했다.
#   2026-08-20 에 'As': [+5, +3] 을 넣었고, check_valence_coverage.py 가 로스터 91/91 통과를 확인했다.
#
# 이 스크립트가 **못 하는 것**
#   · 중성이 됐다고 구조가 생긴다는 보증은 아니다. 자리 반지름 필터·시드 실패는 별개다.
#     0개가 또 나오면 그건 **다른 원인**이고, 그때는 로그를 봐야 한다.
#   · 정본 표(cascade_v23_*.csv)를 자동으로 갱신하지 않는다. 산출물만 만든다.
#   · GPU 를 예약하지 못한다. 다른 작업과 부딪히면 OOM 으로 죽는다 (재시도 안 한다).
#
# 사용 (gabia)
#   cd /data/work/repo && git pull
#   tmux new -d -s as2s3 'bash tools/doping/run_as2s3_recover.sh'
#   tail -f /data/work/runs/as2s3_recover/run.log
#   bash tools/doping/run_as2s3_recover.sh --selftest
# =============================================================================
set -u

if [ "${1:-}" = "--selftest" ]; then
    ok=1
    say() { echo "  $1 $2"; if [ "$1" = "✗" ]; then ok=0; fi; return 0; }
    R=$(cd "$(dirname "$0")/../.." && pwd)
    grep -q "'As': \[+5, +3\]" "$R/tools/doping/substitute_compound.py" \
        && say "✓" "ALTERNATIVE_VALENCES 에 As 가 들어 있다" \
        || say "✗" "As 수정이 없다 — 이 스크립트를 돌리면 또 0개가 나온다"
    [ -f "$R/tools/doping/tier_cascade.sh" ] && say "✓" "tier_cascade.sh 회수됨" \
        || say "✗" "tier_cascade.sh 없음"
    [ -f "$R/db/structures/lpscl_F43m_24G_canonical.cif" ] && say "✓" "기준 구조 있음" \
        || say "✗" "기준 구조 없음"
    python3 "$R/tools/doping/check_valence_coverage.py" --compounds As2S3 >/dev/null 2>&1 \
        && say "✓" "As2S3 전하 중성 가능 (사전 검사 통과)" \
        || say "✗" "As2S3 가 아직 중성 불가 — 먼저 고칠 것"
    [ "$ok" = 1 ] && { echo "selftest PASS"; exit 0; } || { echo "selftest FAIL"; exit 1; }
fi

REPO=${REPO:-/data/work/repo}
[ -d "$REPO/tools/doping" ] || REPO=$HOME/Yonghoon-DEM-DFT
[ -d "$REPO/tools/doping" ] || { echo "repo 못 찾음 (REPO=... 지정)"; exit 1; }
cd "$REPO" || exit 1

OUTROOT=${OUTROOT:-/data/work/runs/as2s3_recover}; mkdir -p "$OUTROOT"
exec > >(tee -a "$OUTROOT/run.log") 2>&1
ts() { date '+%m-%d %H:%M:%S'; }

# 중복 실행 가드 — pgrep 은 tmux 래퍼까지 문다 (chain_gpu_release.sh:34)
exec 9>"$OUTROOT/.lock"
flock -n 9 || { echo "[$(ts)] 이미 도는 중이다 — 중단"; exit 0; }

# 착수 전 사전 검사 — 이걸 통과 못 하면 돌려봐야 0개다
echo "[$(ts)] 전하 중성 사전 검사"
python3 tools/doping/check_valence_coverage.py --compounds As2S3 --verbose || {
    echo "[$(ts)] ⛔ As2S3 가 중성 불가 — ALTERNATIVE_VALENCES 를 먼저 고칠 것"; exit 1; }

if command -v nvidia-smi >/dev/null 2>&1; then
    read -r U T <<<"$(nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits | head -1 | tr -d ',')"
    echo "[$(ts)] GPU $U / $T MiB (여유 $((T-U)) MiB)"
    [ $((T-U)) -lt 4000 ] && echo "[$(ts)] ⚠ 여유 4 GB 미만 — OOM 가능 (재시도 안 한다)"
fi

BASE=db/structures/lpscl_F43m_24G_canonical.cif
[ -f "$BASE" ] || { echo "[$(ts)] 기준 구조 없음: $BASE"; exit 1; }

RC_ALL=0
for X in 0.02 0.05 0.10; do
    TAG=$(printf 'x%03d' "$(python3 -c "print(int(round($X*1000)))")")
    OUT=$OUTROOT/As2S3_$TAG
    if [ -f "$OUT/FINAL_RANKING.json" ]; then
        echo "[$(ts)] As2S3 $TAG: 이미 완료 — 건너뜀"; continue
    fi
    mkdir -p "$OUT"
    echo "[$(ts)] As2S3 $TAG 착수 → $OUT"
    timeout 86400 env COMPOUND_FILTER=As2S3 X_COMPOUND="$X" \
        bash tools/doping/tier_cascade.sh "$BASE" "$OUT" 5 1,1,1 0
    rc=$?
    N=$(python3 - "$OUT" <<'PY' 2>/dev/null || echo "?"
import json, sys, pathlib
p = pathlib.Path(sys.argv[1]) / "01_structures" / "structures_summary.json"
print(len(json.loads(p.read_text()).get("structures", [])) if p.exists() else 0)
PY
)
    echo "[$(ts)] As2S3 $TAG 끝 (rc=$rc) · 생성 구조 $N 개"
    [ "$N" = "0" ] && { echo "[$(ts)] ⛔ 또 0개다 — 전하 문제가 아니라 **다른 원인**이다."
                        echo "     자리 반지름 필터(site_preference_filter)나 시드 실패를 봐야 한다."; }
    [ "$rc" -ne 0 ] && RC_ALL=1
done

echo "[$(ts)] 끝. 산출: $OUTROOT/As2S3_x0*/"
echo "  ⚠ 정본 표(cascade_v23_*.csv)는 **자동으로 안 고친다.** 결과를 붙여주면 판정한다."
exit $RC_ALL
