#!/usr/bin/env bash
# 커밋 **전에** 돌리는 것 — CI 가 돌릴 것을 그대로, 먼저.
#
# ★★ 왜 (2026-08-20, 같은 실수 두 번):
#   `--selftest` 는 **검사기가 맞나**를 보고, 인자 없는 실행은 **리포가 맞나**를 본다.
#   두 번 다 나는 selftest 만 돌리고 푸시했다:
#     ① CLAUDE.md 에 철회값을 인용 → ban-sweep 이 6건 (CI run 2 = failure)
#     ② CL-58 에 `kind: measurement` (유효값 아님) → 규율 J (CI run 11 = failure)
#   ②는 러너의 fail-closed 게이트라 **사용자의 GPU 런을 막았다** — CI 가 60 초 뒤 빨간불을
#   냈지만 그 사이에 pull 이 일어났다.  ⇒ 기억에 맡기지 말고 한 명령으로 묶는다.
#
#   bash scripts/check_all.sh
#
# ⚠ GPU·솔브 없음.  규칙 J 의 초소형 픽스처 스모크가 가장 오래 걸린다 (수 초).
set -uo pipefail
cd "$(dirname "$0")/.."

#  ★ preflight (2026-08-24) — 의존 부재를 **원인 이름으로** 먼저 말한다.
#    실사고: kgy 에서 `(base)` 로 돌려 scipy 가 없었고, 검사기가 fail-closed 로
#    5 오류를 냈다 (그 자체는 옳은 거동이다 — "모르면 통과가 아니라 오류다").
#    그런데 출력이 raw traceback 5벌이라 **"venv 를 켜라"가 안 보였다**.
#    ⇒ 리포 결함과 환경 결함을 갈라 준다.  검사 자체는 그대로 돈다.
_MISS=""
for _m in numpy scipy; do
  python3 -c "import $_m" 2>/dev/null || _MISS="$_MISS $_m"
done
if [ -n "$_MISS" ]; then
  echo "⚠ 파이썬 의존이 없다:$_MISS"
  echo "   → 이것은 **리포 결함이 아니라 환경 결함**이다.  검사기는 모르는 것을"
  echo "     통과시키지 않으므로(fail-closed) 아래에서 오류로 나온다."
  echo "   → GPU 호스트라면 venv 를 켤 것:   . ~/dem-venv/bin/activate"
  echo
fi

FAIL=0
run() {
  local label="$1"; shift
  if "$@" >/tmp/_ca.$$ 2>&1; then
    printf '  ✓ %s\n' "$label"
  else
    printf '  ✗ %s\n' "$label"
    sed 's/^/      /' /tmp/_ca.$$ | tail -25
    FAIL=1
  fi
  rm -f /tmp/_ca.$$
}

echo "── selftest (검사기가 맞나) ──"
#  ★★★ 2026-08-25 (R3-CX-01/05/06) — 실행 계약의 **단일 출처**.  이것이 맞아야
#    producer·check_arm·판정기가 같은 계약을 쓴다 (세 사본이 갈린 것이 R3 의 뿌리).
run 'run_contract          --selftest' python3 scripts/run_contract.py --selftest
run 'check_review_findings   --selftest' python3 scripts/check_review_findings.py --selftest
run 'check_method_discipline --selftest' python3 scripts/check_method_discipline.py --selftest
run 'sdcp_gain_verdict       --selftest' python3 scripts/sdcp_gain_verdict.py --selftest
run 'sdcp_phase_ledger_match --selftest' python3 scripts/sdcp_phase_ledger_match.py --selftest
#  ★★ 2026-08-25 (CDXR3-8/⑩) — **셋이 여기서 안 돌고 있었다.**  Codex: "테스트 파일이
#    존재하고 수동 실행이 녹색인 것만으로는 자동 규율이 아니다."  실제로 이 세 selftest 가
#    S1 봉인의 핵심(팔 검사기·PTFE 규약·솔버 규약)인데 check_all 도 CI 도 부르지 않았다.
#    셋 다 1초 미만이라 비용 이유도 없었다 — 그냥 배선을 잊은 것이다.
#    ⇒ `check_method_discipline` 의 규칙 K 가 이 목록과 CI yml 을 대조해 재발을 막는다.
run 'sr01_stamp_compare     --selftest' python3 scripts/sr01_stamp_compare.py --selftest
run 'mpm_webapp_payload     --selftest-temperature' python3 scripts/mpm_webapp_payload.py --selftest-temperature
run 'step3_sigma            --selftest' python3 scripts/step3_sigma.py --selftest
#  ★ 축소본 계약 (R8 Q6 ⓐ) — 원본 payload 는 팔당 127 MB 라 커밋할 수 없다.  커밋되는 것은
#    축소본이고, 그 selftest 의 마지막 항목이 **판정기가 축소본을 원본과 동일하게 읽는다**를
#    단언한다.  이것이 깨지면 커밋된 증거로 §9 provenance 대조를 재실행할 수 없다 —
#    즉 "증거를 넣었다" 가 조용히 거짓이 된다.
run 'reduce_arm_payloads     --selftest' python3 scripts/reduce_arm_payloads.py --selftest
#  ★★ A 트랙 판정식 (개정 A3 / R9 Q1) — A1 은 `1 − u/v` 였고 브리지가 격자 효과의
#    **부호만 뒤집어도** A = 2 로 h1 을 통과했다.  원 사전등록 정의는 절댓값이다.
#    `regr-sign-flip` 이 u = −v → A = 0 → h0 을 단언한다 (옛 식이 2.0 을 냈을 것도 함께).
run 'bridge_grid_verdict    --selftest' python3 scripts/bridge_grid_verdict.py --selftest
#  ★★ LHS 확장 분석기 둘 (2026-08-29, Codex R11 B1) — **결과가 나오기 전에** 배선한다.
#    R11: "추출기와 적합기를 결과 전에 커밋해야 사전등록의 규약이 실재한다."  런이 끝난 뒤
#    분석기를 짜면 규약이 데이터를 보고 정해지고, 그때는 사전등록이 아니다.
#    extract = AM 접촉 그래프의 z-퍼콜 (1차 관측량) · fit = Firth 문턱 + 프로파일 구간.
run 'lhs_perc_extract       --selftest' python3 scripts/lhs_perc_extract.py --selftest
run 'lhs_perc_fit           --selftest' python3 scripts/lhs_perc_fit.py --selftest

#  ★ 2026-08-30 — 이 둘은 selftest 가 **있었는데 배선이 없었다**.  `make_heckel_manifest.scan()`
#    이 심볼릭 링크 중복을 독립 대조로 세어 인계 문서에 가짜 확인이 적혔고, 그 회귀가
#    여기 안 걸려 있으면 다음에 또 조용히 풀린다 ("존재하고 수동 실행이 녹색인 것만으로는
#    자동 규율이 아니다" — 위 §57 과 같은 규칙).
run 'make_heckel_manifest   --selftest' python3 scripts/make_heckel_manifest.py --selftest
run 'oat_sensitivity        --selftest' python3 scripts/oat_sensitivity.py --selftest

echo "── 리포 실물 (리포가 맞나 — selftest 가 **대신해 주지 않는다**) ──"
#  ★★ 2026-08-25 — 배터리는 느려서 여기 없지만(~20분), **문법이라도** 본다.
#    실사고: mutant 문자열 인용이 깨져 배터리가 시작하자마자 SyntaxError 로 죽었는데
#    `check_all` 은 초록이었다.  돌지 않는 검사기는 없는 것과 같다 (규칙 K 의 교훈).
run 'mutation_sweep (문법 — 배터리 자신이 도는가)' \
  python3 -c "import ast,sys; ast.parse(open('scripts/mutation_sweep_20260825.py',encoding='utf-8').read())"
run 'check_review_findings   (원장 + 철회값 스윕)' python3 scripts/check_review_findings.py
run 'check_method_discipline (규칙 A~M + claims 원장)' python3 scripts/check_method_discipline.py

echo
if [ "$FAIL" = 0 ]; then
  echo "✓ 전부 통과 — 커밋해도 된다 (CI 가 같은 것을 다시 돈다)"
else
  echo "✗ 실패가 있다 — 고치고 다시.  ⚠ 이대로 푸시하면 러너의 fail-closed 게이트가"
  echo "  사용자의 GPU 런을 막는다 (규율 검사는 런 시작 전에 걸린다)."
fi
exit "$FAIL"
