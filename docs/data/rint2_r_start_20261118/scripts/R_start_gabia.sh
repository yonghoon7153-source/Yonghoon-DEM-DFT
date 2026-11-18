# Rint ② R 시작 — gabia (§3-1b (5) 받는 쪽 → (4) 사다리 P1 → 시작 확인) · 인자 = kgy 가 찍은 넘김 기록 넷
set -u
fail(){ echo "⛔ $* — 여기서 멈춤"; exit 1; }
[ "$#" = 4 ] || fail "인자 넷 (T BR H SB) — kgy 끝 줄을 그대로"
T=$1; BR=$2; H=$3; SB=$4
cd ~/sdcp && umask 022 && [ "$(umask)" = 0022 ] || fail umask
. ~/dem-venv/bin/activate && unset SIGMA_VGCF_OVERRIDE
[ "$(command -v python3)" = "$HOME/dem-venv/bin/python3" ] || fail "venv python3 아님"
C=$HOME/dem-ca1/scripts/rint_r_chain.py; REG=$HOME/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md; RUN=$HOME/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh
S0P=$HOME/dem-ca1/docs/data/rint2_s0_sbe_20261116/files/ca1_s0_sbe_20261116T004809Z_q14final/cjunc_plan.json
S2R=$HOME/sdcp/ca1_s0_dbe/s0_stage2_kit_DBE_sdcp1um_vgcf100.json; S1R=$HOME/sdcp/ca1_s0_sbe_20261116T004809Z_q14final/s0_stage1_kit_SBE_vgcf100.json
COMMON="--runner $RUN --root $HOME/sdcp --plan $HOME/sdcp/ca1_plan.json --registration $REG"
RB=$HOME/sdcp/ca1_relay/${T}_kgy_to_gabia.bundle
echo "== 0. 확인 (읽기만)"
echo "실행 트리 $(git -C ~/dem-ca1 rev-parse --short=12 HEAD)"; [ -z "$(git -C ~/dem-ca1 status --porcelain --untracked-files=normal)" ] || fail "실행 트리가 깨끗하지 않다"
sha256sum ~/sdcp/ca1_plan.json "$S2R" "$S1R" | cut -c1-16 | tr '\n' ' '; echo "(기대 d8595a52b67f361d e69894817ea9aded c9307cfcc656a7e7)"
for p in ~/sdcp/ca1_ledger ~/sdcp/ca1_ledger.parked ~/sdcp/ca1_ladder_P1; do [ -e "$p" ] && fail "이미 있다: $p"; done
pgrep -af '^[^ ]*python[0-9.]* [^ ]*rint_r_chain[.]py' && fail "사슬이 이미 돈다"
nvidia-smi --query-gpu=name,driver_version,memory.used --format=csv,noheader
echo "== 1. 원장 받기 (5)"
[ -f "$RB" ] || fail "묶음이 없다: $RB (scp 먼저)"
[ "$(sha256sum "$RB" | cut -c1-64)" = "$SB" ] || fail "묶음 sha256 다름"
[ "$(git bundle list-heads "$RB" | grep "refs/heads/$BR" | cut -c1-40)" = "$H" ] || fail "묶음 머리 ≠ 넘김 기록 끝 커밋"
git clone -q -b "$BR" "$RB" ca1_ledger || fail "clone"
[ "$(git -C ca1_ledger rev-parse HEAD)" = "$H" ] || fail "받은 원장 끝 커밋 다름"; echo RECV_OK
echo "== 2. 사다리 P1 --dry-run (원장 · 폴더 무변경)"
python3 $C --stage ladder --law P1 --target 1.63 $COMMON --s0-plan $S0P --s0-stage2-report $S2R --s0-stage1-report $S1R --max-hours 168 --machine gabia --cjunc-store $HOME/ca1_cjstore --out $HOME/sdcp/ca1_ladder_P1 --dry-run > ~/sdcp/ca1_logs/ladder_P1_dryrun.log 2>&1
rc=$?; tail -12 ~/sdcp/ca1_logs/ladder_P1_dryrun.log; [ "$rc" = 0 ] || fail "dry-run rc $rc (원장은 gabia 에 그대로)"
echo "== 3. 항목 → 곧바로 본 시도"
A=$(python3 $C --stage ledger --ledger ~/sdcp/ca1_ledger --add --ledger-target ladder:P1 --machine gabia $COMMON 2>&1); echo "$A"
N=$(printf '%s\n' "$A" | sed -n 's/^ATTEMPT_ADDED n=\([0-9][0-9]*\) target=ladder:P1 machine=gabia.*/\1/p'); [ -n "$N" ] || fail "항목 번호를 못 읽음"
nohup python3 $C --stage ladder --law P1 --target 1.63 $COMMON --s0-plan $S0P --s0-stage2-report $S2R --s0-stage1-report $S1R --max-hours 168 --machine gabia --ledger $HOME/sdcp/ca1_ledger --attempt $N --cjunc-store $HOME/ca1_cjstore --out $HOME/sdcp/ca1_ladder_P1 > ~/sdcp/ca1_logs/ladder_P1_a$N.log 2>&1 &
echo "사다리 P1 발사 · 시도 $N · 로그 ~/sdcp/ca1_logs/ladder_P1_a$N.log"
echo "== 4. 시작 확인 (10 초마다 · 최대 30 분)"
K=""; G=0
for i in $(seq 1 180); do
  sleep 10
  K=$(python3 -c 'import json, subprocess, sys; L = subprocess.run(["git", "-C", sys.argv[1], "show", "HEAD:rint_r_attempts.jsonl"], capture_output=True, text=True, check=True).stdout.splitlines(); x = json.loads(L[-1]); print(x.get("kind"), x.get("n"))' ~/sdcp/ca1_ledger 2>/dev/null)
  G=$(ls ~/sdcp/ca1_ladder_P1/attempt_$N/groups/ 2>/dev/null | grep -c 'launch.json$')
  [ "$K" = "start $N" ] && [ "$G" -ge 1 ] && break
  pgrep -f '^[^ ]*python[0-9.]* [^ ]*rint_r_chain[.]py --stage ladder --law P1' > /dev/null || fail "사슬이 시작 확인 전에 끝났다 — tail -20 ~/sdcp/ca1_logs/ladder_P1_a$N.log 를 보내 주세요"
done
[ "$K" = "start $N" ] && [ "$G" -ge 1 ] || fail "30 분 안에 시작 확인 안 됨 (원장 ${K:-?} · launch $G)"
echo "START_OK 시도 $N · launch.json $G · 원장 = gabia 에 둔다 (먼저 끝난 기계가 받는다)"
