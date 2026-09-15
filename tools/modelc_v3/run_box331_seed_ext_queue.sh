#!/usr/bin/env bash
# =============================================================================
# box331 시드 확장 — **직렬 대기열** (계,시드) 단위로 하나씩
#
# 왜 직렬인가 (2026-09-15 실측): modelc s5 기동 중 `nvidia-smi` 가
#   **utilization 96 % · 11544/24576 MiB** 를 냈다. 러너 헤더에 **결과 보기 전에** 적어 둔
#   규칙이 *"util ≥ 95 % → 직렬"* 이라 그대로 따른다. VRAM 도 11.5 GB × 2 = 23.1 GB 로
#   여유가 1.5 GB 뿐이라 둘째 이유가 된다.
#   ⚠ 그 수는 `torch.compile`(turbo) 구간일 수 있다 — 정상 MD 에서 util 이 85 % 아래로
#     내려가면 병렬이 이득일 수 있고, 그때는 이 대기열 대신 러너를 따로 띄우면 된다.
#
# 무엇을 하나: 이미 도는 유닛은 **락으로 기다렸다가** 다음 것을 던진다. 그래서 지금 돌고 있는
#   `modelc s5` 가 끝나는 즉시 `modelc s6` → `lpsocl s5` → `lpsocl s6` 가 이어진다.
#
# ⛔ 이 스크립트가 **못 하는 것**
#   · 게이트를 판정하지 않는다. 런만 순서대로 던진다.
#   · 실패한 유닛을 다시 던지지 않는다 — 실패는 로그에 남기고 **다음으로 간다**
#     (하나가 죽었다고 나머지를 버리면 57 h 를 통째로 날린다).
#   · 자원을 재지 않는다. 병렬로 바꿀지는 사람이 `nvidia-smi` 를 보고 정한다.
#
# 쓰기:
#   bash tools/modelc_v3/run_box331_seed_ext_queue.sh
#   UNITS="lpsocl:5 lpsocl:6" bash tools/modelc_v3/run_box331_seed_ext_queue.sh   # 일부만
#   bash tools/modelc_v3/run_box331_seed_ext_queue.sh --selftest
# =============================================================================
# ⚠ `-e` 를 **일부러 안 쓴다** — 유닛 하나가 죽어도 나머지는 계속 돈다.
set -uo pipefail

HERE=$(cd "$(dirname "$0")" && pwd)
RUNNER=$HERE/run_box331_seed_extension.sh
UNITS=${UNITS:-"modelc:5 modelc:6 lpsocl:5 lpsocl:6"}
WAIT_S=${WAIT_S:-0}          # 0 = 무한 대기 (앞 유닛이 끝날 때까지)

_unit_ok() {                 # "계:시드" 모양인가 · 아는 계인가
  case "$1" in
    modelc:[0-9]*|lpsocl:[0-9]*) return 0 ;;
    *) return 1 ;;
  esac
}

if [ "${1:-}" = "--selftest" ]; then
  # ⚠ 양성만 있는 selftest 는 통과해도 아무것도 보증 못 한다 — 음성을 같이 본다.
  fail=0
  for good in modelc:5 lpsocl:6 modelc:12; do
    _unit_ok "$good" || { echo "⛔ 양성 실패: $good 를 거부했다"; fail=1; }
  done
  for bad in b2o3:5 modelc modelc: ":5" "modelc:x" "lpsocl:"; do
    _unit_ok "$bad" && { echo "⛔ 음성 실패: $bad 를 통과시켰다"; fail=1; }
  done
  [ -x "$RUNNER" ] || { echo "⛔ 러너가 없거나 실행 불가: $RUNNER"; fail=1; }
  [ "$fail" = 0 ] && echo "selftest ✅ (양성 3 · 음성 6 · 러너 실재)" || echo "selftest ⛔"
  exit "$fail"
fi

[ -x "$RUNNER" ] || { echo "⛔ 러너가 없다: $RUNNER"; exit 1; }
for u in $UNITS; do
  _unit_ok "$u" || { echo "⛔ 유닛 모양이 틀렸다: '$u' (계:시드, 계는 modelc|lpsocl)"; exit 1; }
done

echo "대기열: $UNITS"
echo "⚠ 직렬이다 — 앞 유닛이 끝나야 다음이 시작한다 (근거: util 96 % 실측)"
echo ""

for u in $UNITS; do
  S=${u%%:*}; D=${u##*:}
  LOCK=/tmp/${S}_box331_seed_ext_${D}.lock
  echo "════ [queue] $S s$D — 앞 유닛을 기다린다 ($LOCK) ════"
  # 이미 그 유닛이 돌고 있으면 여기서 막힌다. 끝나면 락을 놓고 러너가 다시 잡는다.
  exec 8>"$LOCK" || { echo "  ⛔ 락을 못 연다 — 건너뛴다"; continue; }
  if [ "$WAIT_S" -gt 0 ]; then
    flock -w "$WAIT_S" 8 || { echo "  ⚠ ${WAIT_S}s 안에 안 비었다 — 건너뛴다"; exec 8>&-; continue; }
  else
    flock 8 || { echo "  ⛔ flock 실패 — 건너뛴다"; exec 8>&-; continue; }
  fi
  exec 8>&-                  # 러너가 자기 락을 잡아야 하므로 놓아 준다
  SYS=$S SEEDS=$D bash "$RUNNER"
  rc=$?
  [ "$rc" = 0 ] && echo "  ✓ $S s$D 끝" || echo "  ⚠ $S s$D 가 rc=$rc 로 끝났다 — 다음으로 간다"
done

echo ""
echo "대기열 종료. ⛔ 게이트 판정은 이 스크립트가 하지 않는다 — 사전등록 카드 §3 의 A/B/C 규칙으로."
