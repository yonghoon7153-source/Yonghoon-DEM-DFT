#!/usr/bin/env bash
# =============================================================================
# chain_inter_split.sh — intra cage NEB 가 끝나면 **inter cage split NEB** 착수.
#
# 왜 split 인가 (2026-08-20 처방)
#   comp1 inter 단일 NEB 는 elementary 가 아니었다. 실측 밴드
#     [0.0, -0.267, -0.018, 0.432, -0.462, 0.247, -0.079, -0.179, -0.005]
#   에서 이미지 4 가 **시작보다 0.462 eV 낮다** — 중간에 별개의 안정 자리를 거친다.
#   그런 밴드의 max−E[0] 를 '장벽' 이라 부르면 틀린다. 그래서 그냥 재실행하지 않고
#   `--split`(중간자리 이완 → 두 구간 NEB)로 돈다.
#
# 왜 chain_gpu_release.sh 를 안 쓰나
#   그건 "GPU 가 비면 QE 단일점 + Li 슬랩" 전용이고 본문이 아직 비어 있다(READY 알림만).
#   여기는 대기 조건이 다르다 — **intra 프로세스 종료**가 기준이고, 그 뒤에 GPU 를 다시
#   점유하러 들어간다. 그 파일의 두 교훈(로그 디렉터리 직접 생성 · pgrep 대신 flock)은 그대로 가져왔다.
#
# 이 스크립트가 **못 하는 것**
#   · intra 가 실패로 죽었는지 성공으로 끝났는지 구분하지 않는다. **끝나면 시작한다.**
#     (intra 결과와 inter 는 독립이라 그래도 된다. 대신 종료 시각·직전 로그를 찍어 둔다.)
#   · GPU 메모리를 예약하지 못한다. 다른 사람이 먼저 잡으면 OOM 으로 죽는다 —
#     그때는 로그에 남고 재시도하지 않는다.
#   · 장벽이 맞는지 판정하지 않는다. split 결과의 신뢰도는 json 의 band/ci 수렴 플래그로 본다.
#
# 실행 (gabia)
#   cd /data/work/repo && git pull
#   tmux new -d -s intersplit 'bash tools/neb_diffusion/chain_inter_split.sh'
#   tmux ls && tail -f ~/logs/inter_split.log
#   SUPERCELL="2 2 1" tmux new -d -s intersplit 'bash ...'   # 더 큰 셀로
#   bash tools/neb_diffusion/chain_inter_split.sh --selftest
# =============================================================================
set -u

if [ "${1:-}" = "--selftest" ]; then
    T=$(mktemp -d); ok=1
    say() { echo "  $1 $2"; if [ "$1" = "✗" ]; then ok=0; fi; return 0; }

    # 양성: 대기 판정에 쓰는 패턴이 실제 intra 명령줄을 잡는다
    CL="python3 tools/neb_diffusion/argyrodite_cage_neb.py --kind intra --supercell 2 1 1"
    echo "$CL" | grep -q "argyrodite_cage_neb\.py" && say "✓" "intra 명령줄 패턴 매칭" \
        || say "✗" "패턴 매칭 실패"

    # 음성 ①: 이 체인 스크립트 자신을 intra 로 오인하면 영원히 안 끝난다
    echo "bash tools/neb_diffusion/chain_inter_split.sh" | grep -q "argyrodite_cage_neb\.py" \
        && say "✗" "자기 자신을 intra 로 오인 (무한 대기)" || say "✓" "자기 자신을 intra 로 세지 않음"

    # 음성 ②: watch 스크립트도 세면 안 된다
    echo "bash /root/watch_cage_neb.sh" | grep -q "argyrodite_cage_neb\.py" \
        && say "✗" "watch 를 intra 로 오인" || say "✓" "watch 를 intra 로 세지 않음"

    # 음성 ③: nvidia-smi 가 없거나 빈 출력일 때 개수 파싱이 터지지 않아야 한다
    #   (chain_gpu_release.sh 실측 버그: `grep -c . || echo 0` 이 "0\n0" 두 줄이 됐다)
    n=$(printf '' | grep -c . | tail -1); n=${n:-0}
    [ "$n" -eq 0 ] 2>/dev/null && say "✓" "빈 출력 → 0 (integer expression 오류 없음)" \
        || say "✗" "빈 출력 파싱 실패: '$n'"

    # 음성 ④: --split 플래그가 실제 도구에 있어야 한다 (없으면 조용히 무시돼 옛 계산이 된다)
    R=$(dirname "$0")/argyrodite_cage_neb.py
    if [ -f "$R" ]; then
        grep -q '"--split"' "$R" && say "✓" "argyrodite_cage_neb.py 에 --split 존재" \
            || say "✗" "--split 이 없다 — 이 체인은 옛 단일 NEB 를 돌리게 된다"
    else
        say "✗" "argyrodite_cage_neb.py 를 못 찾음: $R"
    fi

    # 음성 ⑤: 로그 디렉터리가 없으면 tmux 가 조용히 죽는다 — 스크립트가 직접 만드는지
    grep -q 'mkdir -p "\$LOGDIR"' "$0" && say "✓" "로그 디렉터리를 스크립트가 직접 만든다" \
        || say "✗" "LOGDIR mkdir 없음 (tmux 조용한 즉사 재발)"

    rm -rf "$T"
    [ "$ok" = 1 ] && { echo "selftest PASS"; exit 0; } || { echo "selftest FAIL"; exit 1; }
fi

LOGDIR=${LOGDIR:-$HOME/logs}
mkdir -p "$LOGDIR"                 # ← tmux 명령줄 리다이렉트 실패로 인한 조용한 즉사 방지
LOG=$LOGDIR/inter_split.log
exec > >(tee -a "$LOG") 2>&1
ts() { date '+%m-%d %H:%M:%S'; }

# 중복 실행 가드는 flock — pgrep 은 tmux 래퍼까지 문다 (chain_gpu_release.sh:34, 2026-08-03).
exec 9>"${LOCK:-/tmp/chain_inter_split.lock}"
flock -n 9 || { echo "[$(ts)] 이미 도는 체인이 있다 — 중복 실행 중단"; exit 0; }

REPO=${REPO:-/data/work/repo}
[ -d "$REPO/tools/neb_diffusion" ] || REPO=$HOME/Yonghoon-DEM-DFT
[ -d "$REPO/tools/neb_diffusion" ] || { echo "[$(ts)] repo 못 찾음 (REPO=... 지정)"; exit 1; }
cd "$REPO" || exit 1

STRUCT=${STRUCT:-db/structures/comp1_V0_k444.cif}
SUPERCELL=${SUPERCELL:-2 1 1}
TAG=${TAG:-inter_split_$(echo "$SUPERCELL" | tr -d ' ')}
[ -f "$STRUCT" ] || { echo "[$(ts)] 구조 없음: $STRUCT"; exit 1; }

# ── intra 종료 대기 ────────────────────────────────────────────────────────
# 자기 자신(bash 체인)·watch 는 패턴에 안 걸린다 — selftest 음성 ①②로 확인했다.
PAT='argyrodite_cage_neb\.py'
echo "[$(ts)] intra cage NEB 종료 대기 (패턴 $PAT)"
WAITED=0
while pgrep -f "$PAT" >/dev/null 2>&1; do
    P=$(pgrep -f "$PAT" | tr '\n' ' ')
    echo "[$(ts)] 아직 도는 중: pid $P  (누적 $((WAITED/60))분) — 5분 뒤 재확인"
    sleep 300; WAITED=$((WAITED+300))
done
echo "[$(ts)] intra 종료 확인 (대기 $((WAITED/60))분)"
LAST=$(ls -t db/properties/neb_*.log 2>/dev/null | head -1)
[ -n "$LAST" ] && { echo "[$(ts)] 직전 로그 $LAST 마지막 3줄:"; grep -a . "$LAST" | tail -3 | sed 's/^/    /'; }

# ── GPU 여유 확인 (예약은 못 한다 — 없으면 그냥 알리고 진행) ────────────────
if command -v nvidia-smi >/dev/null 2>&1; then
    read -r U T2 <<<"$(nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits | head -1 | tr -d ',')"
    echo "[$(ts)] GPU $U / $T2 MiB (여유 $((T2-U)) MiB)"
    [ $((T2-U)) -lt 5000 ] && echo "[$(ts)] ⚠ 여유 5 GB 미만 — OOM 으로 죽을 수 있다 (재시도 안 한다)"
fi

# ── inter split NEB 착수 ───────────────────────────────────────────────────
echo "[$(ts)] inter split NEB 착수  struct=$STRUCT  supercell=$SUPERCELL  tag=$TAG"
echo "[$(ts)] 진행 로그: db/properties/neb_${TAG}{,_seg1,_seg2}.log"
python3 tools/neb_diffusion/argyrodite_cage_neb.py \
    --struct "$STRUCT" --kind inter --supercell $SUPERCELL \
    --split --tag "$TAG" ${EXTRA:-}
RC=$?
echo "[$(ts)] 끝 (exit $RC). 결과: db/properties/argyrodite_cage_neb.json 의 tag=$TAG"
echo "  ⚠ split 값의 신뢰도는 json 의 split.segments[].{band_converged,ci_converged} 로 본다."
echo "     둘 중 하나라도 false 면 **장벽으로 인용하지 않는다.**"
