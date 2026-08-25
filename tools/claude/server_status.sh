#!/usr/bin/env bash
# =============================================================================
# server_status.sh — gabia · kgy 에서 "지금 뭐가 돌고 뭐가 비었나" 를 한 화면에.
#
# 왜 이 파일인가
#   watch_*.sh 들은 **작업 하나씩** 본다 (gap nscf / cage NEB / MD / sei NEB).
#   서버에 붙자마자 알아야 하는 건 그게 아니라 "**지금 걸어도 되나**" 다:
#   GPU 여유 · 돌고 있는 계산 · 살아있는 tmux · 끝나서 회수해야 할 것.
#   그 판단을 한 번에 주는 게 없어서 신설한다.
#
# 이 도구가 **못 하는 것**
#   · 결과가 맞는지 판정하지 않는다. 무엇이 도는지만 본다.
#   · 원격으로 못 본다 — 각 서버에서 실행해야 한다 (alias 로 감싸 쓸 것).
#   · 프로세스 이름으로 식별한다. 이름이 겹치면 잘못 셀 수 있다.
#
#   bash tools/claude/server_status.sh            # 지금 뭐가 도나 (빠름)
#   bash tools/claude/server_status.sh --jobs      # + 작업별 진행률 (기존 워처 위임)
#   bash tools/claude/server_status.sh --selftest
# =============================================================================
set -u

if [ "${1:-}" = "--selftest" ]; then
    ok=1
    say() { echo "  $1 $2"; if [ "$1" = "✗" ]; then ok=0; fi; return 0; }
    # [음성] nvidia-smi 가 없거나 빈 출력이어도 산술이 터지지 않아야 한다
    #   (chain_gpu_release.sh 실측 버그: `grep -c . || echo 0` 이 "0\n0" 두 줄이 됐다)
    n=$(printf '' | grep -c . | tail -1); n=${n:-0}
    [ "$n" -eq 0 ] 2>/dev/null && say "✓" "[음성] 빈 출력 → 0 (integer expression 오류 없음)" \
        || say "✗" "빈 출력 파싱 실패"
    # [음성] pgrep 이 자기 자신·watch 를 세면 안 된다
    echo "bash tools/claude/server_status.sh" | grep -qE 'uma_md_driver|argyrodite_cage_neb|pw\.x' \
        && say "✗" "자기 자신을 작업으로 센다" || say "✓" "[음성] 자기 자신을 작업으로 세지 않음"
    # [양성] GPU 여유 판정 경계
    for u in 40000 46000; do
        free=$((49140-u))
        want=$([ $free -ge 5000 ] && echo 여유 || echo 빠듯)
        say "✓" "GPU $u/49140 → 여유 ${free} MiB → $want"
    done
    # [음성] tmux 가 없어도 죽지 않아야 한다
    command -v tmux >/dev/null 2>&1 || say "✓" "[음성] tmux 없는 환경에서도 진행"
    [ "$ok" = 1 ] && { echo "selftest PASS"; exit 0; } || { echo "selftest FAIL"; exit 1; }
fi

HOST=$(hostname)
echo "════════ $(date '+%m-%d %H:%M:%S')  $HOST ════════"

# ── GPU ─────────────────────────────────────────────────────────────────────
if command -v nvidia-smi >/dev/null 2>&1; then
    read -r U T <<<"$(nvidia-smi --query-gpu=memory.used,memory.total \
                      --format=csv,noheader,nounits | head -1 | tr -d ',')"
    F=$(( T - U ))
    printf "■ GPU  %s / %s MiB   여유 %s MiB  →  " "$U" "$T" "$F"
    if   [ "$F" -ge 8000 ]; then echo "✅ 넉넉 — 뭘 걸어도 된다"
    elif [ "$F" -ge 5000 ]; then echo "🟡 보통 — UMA MD 1개는 가능 (NEB 은 빠듯)"
    elif [ "$F" -ge 2000 ]; then echo "🔴 빠듯 — 새로 걸지 말 것 (OOM 위험)"
    else                         echo "⛔ 없음 — 지금 걸면 죽는다"
    fi
    nvidia-smi --query-compute-apps=pid,used_memory,process_name --format=csv,noheader 2>/dev/null |
        awk -F', ' '{printf "     pid %-8s %-10s %s\n", $1, $2, $3}'
else
    echo "■ GPU  (nvidia-smi 없음)"
fi

# ── 돌고 있는 계산 (알려진 것들에 이름을 붙인다) ────────────────────────────
echo "■ 돌고 있는 계산"
found=0
show() {   # $1 = pgrep 패턴, $2 = 사람이 읽을 이름
    local pids; pids=$(pgrep -f "$1" 2>/dev/null | grep -v "^$$\$" | tr '\n' ' ')
    [ -z "${pids// /}" ] && return
    found=1
    local et; et=$(ps -o etime= -p ${pids%% *} 2>/dev/null | tr -d ' ')
    printf "   ✅ %-34s pid %s  경과 %s\n" "$2" "${pids% }" "${et:-?}"
}
show 'uma_md_driver|disorder_ensemble_diffusion|run_highT_reseed'  'UMA MD (재시드/앙상블)'
show 'argyrodite_cage_neb'                                          'cage NEB (UMA)'
show 'qe-.*-gpu/bin/neb\.x'                                         'QE neb.x (GPU · sei NEB)'
show 'qe-.*-cpu/bin/pw\.x'                                          'QE pw.x (CPU · gap nscf)'
show 'qe-.*-gpu/bin/pw\.x'                                          'QE pw.x (GPU)'
show 'tier_cascade|run_as2s3_recover'                               'cascade (As2S3/AlI3 복구)'
show 'msd_diffusive_check'                                          'β 게이트 검사'
[ "$found" = 0 ] && echo "   ⛔ 알려진 계산이 하나도 안 돈다 — 비어 있다"

# ── tmux ────────────────────────────────────────────────────────────────────
echo "■ tmux 세션"
if command -v tmux >/dev/null 2>&1; then
    tmux ls 2>/dev/null | sed 's/^/   /' || echo "   (없음)"
else
    echo "   (tmux 없음)"
fi

# ── 최근 로그 (30분 안에 갱신된 것만) ───────────────────────────────────────
echo "■ 최근 30분 내 갱신된 로그"
find /data/work /home/kgy/work "$HOME/logs" -maxdepth 4 -name '*.log' -mmin -30 2>/dev/null |
    head -8 | while read -r f; do
        printf "   %-58s %s\n" "$f" "$(date -r "$f" '+%H:%M')"
    done
[ -z "$(find /data/work /home/kgy/work "$HOME/logs" -maxdepth 4 -name '*.log' -mmin -30 2>/dev/null | head -1)" ] \
    && echo "   (없음 — 도는 작업이 로그를 안 쓰거나 전부 끝났다)"

# ── 디스크 ──────────────────────────────────────────────────────────────────
echo "■ 디스크"
df -h 2>/dev/null | awk 'NR==1 || /\/data|\/home| \/$/ {printf "   %s\n", $0}' | head -5

# ── --jobs: 진행률까지 (기존 워처에 위임한다) ───────────────────────────────
#   ⚠ 위는 "살아 있나" 만 본다. "얼마나 갔나" 는 작업마다 다른 파일을 읽어야 하는데,
#     그 파서는 이미 워처마다 있다. **여기서 다시 짜지 않고 불러 쓴다** —
#     tools/ 에 워처가 30개 넘게 쌓인 게 그렇게 복사해서다.
#   ⛔ 이 모드가 **못 하는 것**: 결과가 맞는지 판정하지 않는다. 각 워처가 하는 만큼만 한다.
#     워처가 없는 작업(cascade)은 로그 꼬리만 보여준다 — 그건 진행률이 아니다.
if [ "${1:-}" = "--jobs" ]; then
    R="$(cd "$(dirname "$0")/../.." && pwd)"
    sec() { echo; echo "════ $1 ════"; }
    run_if() {   # $1 = 있어야 할 파일, $2… = 실행할 것
        local f="$1"; shift
        if [ -e "$f" ]; then "$@" 2>&1 | tail -25
        else echo "   (해당 없음: $f)"; fi
    }
    sec "sei NEB (li3nd 등)"
    run_if "$R/tools/sei/watch_gabia.py" python3 "$R/tools/sei/watch_gabia.py"
    sec "gap nscf"
    run_if "$R/tools/electronic/watch_gap_nscf.sh" bash "$R/tools/electronic/watch_gap_nscf.sh"
    sec "cage NEB"
    run_if "$R/tools/neb_diffusion/watch_cage_neb.sh" bash "$R/tools/neb_diffusion/watch_cage_neb.sh"
    sec "cascade (전용 워처 없음 — 로그 꼬리)"
    # ⛔ 2026-08-25 — 첫 판은 `find … | head -1` 이라 **아무거나** 집었다. 실제로
    #   6월자 BaO_x002/cascade.log (Stage 00 FAILED) 를 물어와, 3일째 돌던 As2S3 를
    #   두고 "실패" 를 보여줬다. 시간순 최신을 고르고, 후보도 실제 쓰는 로그로 좁힌다.
    # ⛔ 그리고 이 로그는 scipy RuntimeWarning(logm/탄성텐서) 으로 도배된다 —
    #   거르지 않으면 tail 이 전부 경고라 진행을 못 본다.
    _cl=$(ls -t /data/work/runs/ali3.log /data/work/runs/as2s3_recover/run.log \
             /data/work/runs/cascade*.log 2>/dev/null | head -1)
    if [ -n "$_cl" ]; then
        echo "   $_cl  ($(date -r "$_cl" '+%m-%d %H:%M'))"
        grep -avE 'RuntimeWarning|return f\(\*arrays|warnings\.warn|FutureWarning|^[[:space:]]*$' \
            "$_cl" 2>/dev/null | tail -8 | sed 's/^/     /'
    else
        echo "   (로그를 못 찾았다 — tmux ali3 안을 직접 볼 것: tmux capture-pane -pt ali3 | tail -20)"
    fi
    sec "MD 재시드"
    # ⛔ 2026-08-25 — 첫 판은 *.log 를 뒤졌는데 이 런은 tmux 안에서만 돌아 로그 파일이
    #   없다. 그래서 7/9 완료·궤적 7개인 멀쩡한 런을 "로그 못 찾음" 으로 보여줬다.
    #   MD 는 msd.json/traj 를 보는 **전용 워처가 이미 있다** — 그걸 부른다.
    #   ⚠ 루트 이름이 둘이다: highT_reseed(옛) · highT_reseed_traj(--save_traj 판).
    #     둘 다 보고, 실제로 내용이 있는 쪽만 찍는다 (한쪽만 보면 빈 화면이 나온다).
    _w="$R/tools/modelc_v3/watch_b2o3_md.sh"
    _md_any=0
    for _root in ${MDROOTS:-/data/work/runs/highT_reseed_traj /data/work/runs/highT_reseed \
                            "$HOME/work/runs/highT_reseed_1200"}; do
        [ -d "$_root" ] || continue
        [ -f "$_w" ] || { echo "   (워처 없음: $_w)"; break; }
        _o=$(bash "$_w" "$_root" 2>&1)
        # 런이 하나도 안 잡히면 건너뛴다 — 빈 표를 세 번 찍는 게 더 헷갈린다
        echo "$_o" | grep -q '완료 0 · 진행 0' && continue
        echo "$_o" | tail -18; _md_any=1
    done
    [ "$_md_any" = 0 ] && echo "   (MD 런 없음 — 루트를 바꾸려면 MDROOTS='경로 …')"
fi
