# Rint ② R 시작 — kgy (봉인본 · kgy 명령 문서 §3-1b (3) 원장 시작 → (4) 사다리 P0 → 시작 확인 → (5) 원장 넘김 묶기) · 1저자 11-18 GO
set -u
fail(){ echo "⛔ $* — 여기서 멈춤"; exit 1; }
cd ~/sdcp && umask 022 && [ "$(umask)" = 0022 ] || fail umask
. ~/dem-venv/bin/activate && unset SIGMA_VGCF_OVERRIDE
[ "$(command -v python3)" = "$HOME/dem-venv/bin/python3" ] || fail "venv python3 아님"
C=$HOME/dem-ca1/scripts/rint_r_chain.py; REG=$HOME/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md; RUN=$HOME/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh
S0P=$HOME/dem-ca1/docs/data/rint2_s0_sbe_20261116/files/ca1_s0_sbe_20261116T004809Z_q14final/cjunc_plan.json
S2R=$HOME/sdcp/ca1_s0_dbe/s0_stage2_kit_DBE_sdcp1um_vgcf100.json; S1R=$HOME/sdcp/ca1_s0_sbe_20261116T004809Z_q14final/s0_stage1_kit_SBE_vgcf100.json
COMMON="--runner $RUN --root $HOME/sdcp --plan $HOME/sdcp/ca1_plan.json --registration $REG"
echo "== 0. 확인 (읽기만)"
echo "실행 트리 $(git -C ~/dem-ca1 rev-parse --short=12 HEAD)"; [ -z "$(git -C ~/dem-ca1 status --porcelain --untracked-files=normal)" ] || fail "실행 트리가 깨끗하지 않다"
sha256sum ~/sdcp/ca1_plan.json "$S2R" "$S1R" | cut -c1-16 | tr '\n' ' '; echo "(기대 d8595a52b67f361d e69894817ea9aded c9307cfcc656a7e7)"
for p in ~/sdcp/ca1_ledger ~/sdcp/ca1_ledger.parked ~/sdcp/ca1_ladder_P0; do [ -e "$p" ] && fail "이미 있다: $p"; done
pgrep -af '^[^ ]*python[0-9.]* [^ ]*rint_r_chain[.]py' && fail "사슬이 이미 돈다"
nvidia-smi --query-gpu=name,driver_version,memory.used --format=csv,noheader
echo "== 1. 원장 시작 (3)"
mkdir -p ~/sdcp/ca1_ledger && git -C ~/sdcp/ca1_ledger init -q || fail "git init"
python3 $C --stage ledger --ledger ~/sdcp/ca1_ledger --init --plan ~/sdcp/ca1_plan.json --registration $REG || fail "원장 --init"
BR=$(git -C ~/sdcp/ca1_ledger symbolic-ref --short HEAD); echo "원장 가지 = $BR"
echo "== 2. 사다리 P0 --dry-run (원장 · 폴더 무변경)"
python3 $C --stage ladder --law P0 --target 1.63 $COMMON --s0-plan $S0P --s0-stage2-report $S2R --s0-stage1-report $S1R --max-hours 168 --machine kgy --cjunc-store $HOME/ca1_cjstore --out $HOME/sdcp/ca1_ladder_P0 --dry-run > ~/sdcp/ca1_logs/ladder_P0_dryrun.log 2>&1
rc=$?; tail -12 ~/sdcp/ca1_logs/ladder_P0_dryrun.log; [ "$rc" = 0 ] || fail "dry-run rc $rc (원장 = 머리 줄만 · 시도 없음)"
echo "== 3. 항목 → 곧바로 본 시도"
A=$(python3 $C --stage ledger --ledger ~/sdcp/ca1_ledger --add --ledger-target ladder:P0 --machine kgy $COMMON 2>&1); echo "$A"
N=$(printf '%s\n' "$A" | sed -n 's/^ATTEMPT_ADDED n=\([0-9][0-9]*\) target=ladder:P0 machine=kgy.*/\1/p'); [ -n "$N" ] || fail "항목 번호를 못 읽음"
nohup python3 $C --stage ladder --law P0 --target 1.63 $COMMON --s0-plan $S0P --s0-stage2-report $S2R --s0-stage1-report $S1R --max-hours 168 --machine kgy --ledger $HOME/sdcp/ca1_ledger --attempt $N --cjunc-store $HOME/ca1_cjstore --out $HOME/sdcp/ca1_ladder_P0 > ~/sdcp/ca1_logs/ladder_P0_a$N.log 2>&1 &
echo "사다리 P0 발사 · 시도 $N · 로그 ~/sdcp/ca1_logs/ladder_P0_a$N.log"
echo "== 4. 시작 확인 (10 초마다 · 최대 30 분 · 사슬은 건드리지 않는다)"
K=""; G=0
for i in $(seq 1 180); do
  sleep 10
  K=$(python3 -c 'import json, subprocess, sys; L = subprocess.run(["git", "-C", sys.argv[1], "show", "HEAD:rint_r_attempts.jsonl"], capture_output=True, text=True, check=True).stdout.splitlines(); x = json.loads(L[-1]); print(x.get("kind"), x.get("n"))' ~/sdcp/ca1_ledger 2>/dev/null)
  G=$(ls ~/sdcp/ca1_ladder_P0/attempt_$N/groups/ 2>/dev/null | grep -c 'launch.json$')
  [ "$K" = "start $N" ] && [ "$G" -ge 1 ] && break
  pgrep -f '^[^ ]*python[0-9.]* [^ ]*rint_r_chain[.]py --stage ladder --law P0' > /dev/null || fail "사슬이 시작 확인 전에 끝났다 — tail -20 ~/sdcp/ca1_logs/ladder_P0_a$N.log 를 보내 주세요"
done
[ "$K" = "start $N" ] && [ "$G" -ge 1 ] || fail "30 분 안에 시작 확인 안 됨 (원장 ${K:-?} · launch $G) — 사슬은 그대로 · 넘기지 않음"
echo "START_OK 시도 $N · launch.json $G"
echo "== 5. 원장 넘김 묶기 (kgy → gabia · 잠금 아래 · 세워 둠)"
T=$(date -u +%Y%m%dT%H%M%SZ); B=$HOME/sdcp/ca1_relay/${T}_kgy_to_gabia.bundle
flock -x -w 120 ca1_ledger/.git/rint_r_ledger.lock -c "git -C ca1_ledger bundle create \"$B\" --all && mv ca1_ledger ca1_ledger.parked" || fail "묶기 · 세우기"
H=$(git -C ca1_ledger.parked rev-parse HEAD); SB=$(sha256sum "$B" | cut -c1-64)
[ -e ca1_ledger ] && fail "원장 자리가 아직 있다"; echo PARKED_OK
echo "넘김 기록: $T · kgy → gabia · 가지 $BR · 끝 커밋 $H · 묶음 sha256 $SB · flock"
echo "== gabia 에서 돌릴 줄 (그대로 복사) =="
echo "bash ~/R_start_gabia.sh $T $BR $H $SB"
