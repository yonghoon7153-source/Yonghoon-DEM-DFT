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
#  ★ 2026-09-17 (GAP3-19/20) — porosity 코퍼스의 **무효-데이터 필터**가 레짐 플래그에
#    다시 붙는 것을 막는다.  한 스위치가 둘을 함께 껐을 때 `porosity_unified` 의
#    헤드라인이 전부 틀린 값으로 나왔고(n 138↔129 · LOOCV 0.472↔0.502), dem·mpm 이
#    양수라 **기존 게이트에 안 걸렸다**.
run 'porosity_filter_axes    --selftest' python3 scripts/porosity_filter_axes_check.py --selftest
#  ★★ 2026-08-25 (CDXR3-8/⑩) — **셋이 여기서 안 돌고 있었다.**  Codex: "테스트 파일이
#    존재하고 수동 실행이 녹색인 것만으로는 자동 규율이 아니다."  실제로 이 세 selftest 가
#    S1 봉인의 핵심(팔 검사기·PTFE 규약·솔버 규약)인데 check_all 도 CI 도 부르지 않았다.
#    셋 다 1초 미만이라 비용 이유도 없었다 — 그냥 배선을 잊은 것이다.
#    ⇒ `check_method_discipline` 의 규칙 K 가 이 목록과 CI yml 을 대조해 재발을 막는다.
run 'sr01_stamp_compare     --selftest' python3 scripts/sr01_stamp_compare.py --selftest
run 'mpm_webapp_payload     --selftest-temperature' python3 scripts/mpm_webapp_payload.py --selftest-temperature
run 'step3_sigma            --selftest' python3 scripts/step3_sigma.py --selftest
#  ★ SELF-45 (2026-09-22) — 필드 통계가 **그림 예산에 불변**인지는 step3_sigma 의 selftest 가
#    보고, 옛 payload 를 고치는 후처리기는 자기 selftest 가 본다 (복원의 정확성 + 거부).
run 'repair_focus_top       --selftest' python3 scripts/repair_focus_top.py --selftest
#  ★ 2026-09-22 (병합 검증) — 웹앱 패치 2건의 selftest 가 **어느 레인에도 없었다**
#    (원장 lane=none · check_all/CI grep 0/0).  합쳐 3.5 초인데 자동 규율이 아니었다 =
#    CDXR3-8 이 잡았던 그 모양("테스트가 존재하고 수동 실행이 녹색인 것만으로는
#    자동 규율이 아니다").  ⇒ 둘 다 두 레인에 건다.
run 'webapp_env_audit       --selftest' python3 scripts/webapp_env_audit.py --selftest
run 'type_map_resolve       --selftest' python3 scripts/type_map_resolve.py --selftest
run 'gen_plots  --selftest-descriptions' python3 scripts/generate_comparison_plots.py --selftest-descriptions
run 'gen_plots  --selftest-fits' python3 scripts/generate_comparison_plots.py --selftest-fits
run 'eis_drt_ica            --selftest' python3 scripts/eis_drt_ica.py --selftest
run 'se_net_diagnostics     --selftest' python3 scripts/extract_se_network_diagnostics.py --selftest
run 'grade_engine          --selftest' python3 scripts/grade_engine.py --selftest
run 'constriction_deleted  --selftest' python3 scripts/audit_constriction_deleted.py --selftest
run 'gen_plots  --selftest-temp'      python3 scripts/generate_comparison_plots.py --selftest-temp
#  ★ 축소본 계약 (R8 Q6 ⓐ) — 원본 payload 는 팔당 127 MB 라 커밋할 수 없다.  커밋되는 것은
#    축소본이고, 그 selftest 의 마지막 항목이 **판정기가 축소본을 원본과 동일하게 읽는다**를
#    단언한다.  이것이 깨지면 커밋된 증거로 §9 provenance 대조를 재실행할 수 없다 —
#    즉 "증거를 넣었다" 가 조용히 거짓이 된다.
run 'reduce_arm_payloads     --selftest' python3 scripts/reduce_arm_payloads.py --selftest
#  ★★ A 트랙 판정식 (개정 A3 / R9 Q1) — A1 은 `1 − u/v` 였고 브리지가 격자 효과의
#    **부호만 뒤집어도** A = 2 로 h1 을 통과했다.  원 사전등록 정의는 절댓값이다.
#    `regr-sign-flip` 이 u = −v → A = 0 → h0 을 단언한다 (옛 식이 2.0 을 냈을 것도 함께).
run 'bridge_grid_verdict    --selftest' python3 scripts/bridge_grid_verdict.py --selftest
#  ★ 2026-08-31 — STEP B 판정기.  사전등록 문턱(0.10/0.30)이 **파일 안에서 동결**돼
#    있고 selftest 첫 줄이 그 값을 대조한다 ⇒ 결과를 보고 문턱을 옮기면 여기서 터진다.
run 'ion_r_verdict          --selftest' python3 scripts/ion_r_verdict.py --selftest
#  ★ 2026-08-31 — 접점 분포 그림.  라벨이 `CBD` 로 되돌아가면(= 바인더 포함 함의) 정의와
#    어긋나고, 규약이 다른 두 침대를 한 그림에 섞으면 74→86 과 89→112 가 합쳐진다.
#    selftest 가 그 둘을 문다.
run 'plot_cbd_contacts       --selftest' python3 scripts/plot_cbd_contacts.py --selftest
#  ★ σ_e 막대 그림.  옛 패널 (b) 의 `1.98 → 3.00 S/cm` 는 철회값이고 **단위까지 달랐다**
#    (현 세대는 mS/cm).  selftest 가 축 단위와 팔 수 대응을 문다.
run 'plot_sigma_e_bars       --selftest' python3 scripts/plot_sigma_e_bars.py --selftest
#  ★ 2026-08-31 — 컬러바 PNG 는 **논문 그림에 그대로 들어가는데** 평문·pptx 스윕이
#    PNG 속 글자를 못 읽는다.  제목이 폭을 넘어 잘리면 하필 경고 문구가 사라지고
#    그림은 여전히 그럴듯해 보인다 = 조용한 실패.  여기가 유일한 방어선이다.
if command -v node >/dev/null 2>&1; then
  run 'colorbar_fit (JS 문법)'  node --check webapp/static/js/viewer3d.js
  run 'colorbar_fit (라벨 폭)'  node scripts/check_colorbar_fit.mjs
else
  echo '  — colorbar_fit  건너뜀 (node 없음)'
fi
#  ★★ LHS 확장 분석기 둘 (2026-08-29, Codex R11 B1) — **결과가 나오기 전에** 배선한다.
#    R11: "추출기와 적합기를 결과 전에 커밋해야 사전등록의 규약이 실재한다."  런이 끝난 뒤
#    분석기를 짜면 규약이 데이터를 보고 정해지고, 그때는 사전등록이 아니다.
#    extract = AM 접촉 그래프의 z-퍼콜 (1차 관측량) · fit = Firth 문턱 + 프로파일 구간.
run 'lhs_perc_extract       --selftest' python3 scripts/lhs_perc_extract.py --selftest
run 'lhs_descriptor_harvest --selftest' python3 scripts/lhs_descriptor_harvest.py --selftest
run 'lhs_perc_fit           --selftest' python3 scripts/lhs_perc_fit.py --selftest
#  ★ 2026-09-19 — 같은 규칙을 이종기술 회의록에도 적용한다 (비준 (가) = 61 발화 전수).
#    **회의록 파일보다 먼저** 추출기와 계약을 배선한다 — 원문을 보고 규약을 정하면
#    규약이 결과를 정당화한다.  계약① 은 재조립이 원문과 **바이트 동일**한지를 본다.
run 'hetero_transcript      --selftest' python3 scripts/hetero_transcript.py --selftest

#  ★ 2026-08-30 — 이 둘은 selftest 가 **있었는데 배선이 없었다**.  `make_heckel_manifest.scan()`
#    이 심볼릭 링크 중복을 독립 대조로 세어 인계 문서에 가짜 확인이 적혔고, 그 회귀가
#    여기 안 걸려 있으면 다음에 또 조용히 풀린다 ("존재하고 수동 실행이 녹색인 것만으로는
#    자동 규율이 아니다" — 위 §57 과 같은 규칙).
run 'make_heckel_manifest   --selftest' python3 scripts/make_heckel_manifest.py --selftest
run 'oat_sensitivity        --selftest' python3 scripts/oat_sensitivity.py --selftest
#  ★ 2026-08-30 — 이 selftest 는 draft 파일을 **실제로 열어** docx 상수와 대조한다
#    (옛 docstring 이 "draft 가 정본" 이라 적으면서 한 번도 안 읽어 두 산출물이 갈라졌다).
run 'build_methods_docx     --selftest' python3 scripts/build_methods_docx.py --selftest
run 'check_cohort_packages  --selftest' python3 scripts/check_cohort_packages.py --selftest

echo "── 리포 실물 (리포가 맞나 — selftest 가 **대신해 주지 않는다**) ──"
#  ★★ 2026-08-25 — 배터리는 느려서 여기 없지만(~20분), **문법이라도** 본다.
#    실사고: mutant 문자열 인용이 깨져 배터리가 시작하자마자 SyntaxError 로 죽었는데
#    `check_all` 은 초록이었다.  돌지 않는 검사기는 없는 것과 같다 (규칙 K 의 교훈).
run 'mutation_sweep (문법 — 배터리 자신이 도는가)' \
  python3 -c "import ast,sys; ast.parse(open('scripts/mutation_sweep_20260825.py',encoding='utf-8').read())"
run 'check_review_findings   (원장 + 철회값 스윕)' python3 scripts/check_review_findings.py
run 'check_method_discipline (규칙 A~M + claims 원장)' python3 scripts/check_method_discipline.py
#  ★★ 2026-08-30 — 원장이 "제3자가 리포만으로 재도출한 값이 이 문서와 일치한다" 고 적는데
#    그것은 08-29 에 손으로 한 번 돌린 결과였고 **아무것도 다시 확인하지 않았다**.
#    비·산포를 팔의 σ_e 에서 재계산해 원장 산문과 대조한다 (저장된 판정 필드를 읽지 않는다).
#  ★★ 2026-08-31 — 웹앱 테스트 5개가 **어디에도 배선돼 있지 않았다.**  그래서 둘이
#    빨간불인 채로 남아 있었고, 그중 하나는 앱이 **더 안전해졌기 때문에**(철회 게이트)
#    난 실패였다.  돌지 않는 검사는 없는 것과 같다 (규칙 K).
run 'webapp: pipeline_provenance' python3 webapp/test_pipeline_provenance.py
run 'webapp: predictor_ui'        python3 webapp/test_predictor_ui_and_sigma_grain.py
run 'webapp: security_phase_a'    python3 webapp/test_security_phase_a.py
run 'webapp: seminar_page'        python3 webapp/test_seminar_page.py
run 'webapp: worklog_page'        python3 webapp/test_worklog_page.py
run 'webapp: mixer_devlog_page'   python3 webapp/test_mixer_devlog_page.py
#  ★ 2026-09-22 — 믹서 런처·생성기 회귀 (LIGGGHTS 없이 가짜 실행파일로).  같은 날 사고 둘을 재현해 막는다:
#    배너 없는 완주 런을 "죽음" 으로 읽고 재발사(E0_s49979687) · 실행 중 덱 제자리 덮어쓰기(E0_s32452843).
run 'mixer launcher (완주 판정 · 덮어쓰기 가드)' bash dem_scripts/mixer_20260921/test_launcher.sh
run 'webapp: launcher (포트 선점)' python3 scripts/test_webapp_launcher.py
run 'webapp: temp_pressure'       python3 webapp/test_temp_pressure_wiring.py
#  ★ v3 (2026-09-09) — 화면이 원장을 따라가는가 + **원장을 보여 주는 페이지가 금지값을
#    안 찍는가**.  후자가 이 검사의 요점이다: 초판 구현이 `/ledger` 에서 11 건, `/` 에서
#    2 건을 흘렸다 (원장 본문·`why` 가 *왜 철회됐나* 를 설명하느라 그 값을 인용한다).
#    감사가 `app.py:4035` 에서 찾은 것과 **같은 양식**이라 회귀로 못박는다.
run 'webapp: ledger_view'         python3 webapp/test_ledger_view.py
#  ★ 2026-09-09 (Codex Q2-1) — 커버리지 재현기를 산문 스니펫에서 도구로 옮겼다.
#    옛 스니펫은 디렉터리 항목을 **현재** 파일 집합으로 펼쳐 감사 이후 생긴 파일까지 셌고
#    `.lstrip('./')` 가 dotfile 경로를 망가뜨렸다.  selftest 가 두 반례를 고정한다.
run 'audit_coverage      --selftest' python3 scripts/audit_coverage.py --selftest
#  ★★ 2026-09-14 (§6 전수 감사) — `claimed_fixed_sha` 가 **그 수정의 커밋**인가.
#    실재하는 SHA 를 요구하는 것만으로는 부족하다: `R5CX-08/10/11` 이 `672dedb1` 을 적었는데
#    그 자리에 수정이 **없었다** (진짜는 `777cd6c08`).  기전은 구조적이다 — 수정과 등재를 같은
#    커밋에 넣으면 그 커밋은 자기 SHA 를 못 적어 **부모**가 적힌다.
#    ⚠ 부모를 적은 것 자체는 결함이 아니다 (수정이 바로 앞 커밋이면 옳다).  갈라 내는 것은
#    *'등재 커밋이 그 ID 를 **실행되는 코드**에 새로 박았는가'* 다.  느슨하게 잡으면 거짓
#    양성이 쏟아진다 — 초판은 22건을 냈고 세 겹(증거 공유 · 진행 문서 · 원고)을 걷어 1건이 됐다.
run 'claimed_sha_provenance --selftest' python3 scripts/audit_claimed_sha_provenance.py --selftest
#  ★ 2026-09-09 (Codex Q2-3 · 원장 AUD-07) — 감사 원시 finding 에 **판정 상태**를 붙인다.
#    원본에는 status 가 한 건도 없어 `severity=P1` 만 골라 읽으면 후보와 확정이 합쳐진다.
#    원본은 박제라 안 고치고(해시로 못박는다) 별도 판정 원장에만 상태를 단다.
run 'audit_adjudication  --selftest' python3 scripts/check_audit_adjudication.py --selftest
run 'audit_validation_flags --selftest' python3 scripts/audit_validation_flags.py --selftest
#  ★★ 2026-09-13 (AREA-09 STEP 4 · AREA-11) — 협착저항의 **독립 기준해**.
#    축대칭 flux tube 를 직접 풀어 ψ 를 곱하는지 나누는지를 문헌 인용이 아니라 계산으로
#    가른다.  ⓪ 정규화 검사가 요점 — 초판이 conductance 의 **2π 를 통째로 빠뜨려** 모든
#    저항이 2π 배였는데 단조·수렴·극한 검사는 **전부 초록**이었다 (일률 배수라 안 깨진다).
#    배수를 실제로 재는 검사 하나만이 그것을 잡는다 = 규율 ⑤ 의 false-green.
run 'constriction_reference --selftest' python3 scripts/constriction_reference.py --selftest
#  ★★ 2026-09-13 (AREA-12) — 면적 계약의 S2 가 솔버에 **항등**임을 고정한다.
#    clamp `a_eff = min(a_contact, r_min_real)` 가 이미 수송 원판 상한을 강제하므로 cap 을
#    2πR² → πR² 로 바꿔도 `a_eff` 가 안 바뀐다.  ② 가 `A_physics` 는 실제로 바뀜을 확인해
#    검사가 공허하지 않게 하고 ③ 이 clamp 를 빼면 달라짐을 보여 판별력을 증명한다.
run 'transport_cap_equivalence --selftest' python3 scripts/audit_transport_cap_equivalence.py --selftest
#  ★ 2026-09-13 (L1-01 · L1-02) — Physics 면적 사다리의 두 결함을 **계측만** 붙였다.
#    하한>상한(feasibility)과 V_overlap(lens 가 아니라 단일 cap 공식, 얕으면 절반·깊으면
#    음수).  값은 저자 결정 전까지 안 바꾼다 — ⑨ 가 실측 핀으로 A_final 불변을 강제한다.
run 'plastic_coverage    --selftest' python3 scripts/plastic_coverage.py --selftest
#  ★ 2026-09-13 — 리뷰 비포/애프터 페이지는 손으로 적지 않고 원장에서 **생성**한다 (규율 ④).
#    서술의 인용 숫자는 해당 원장 항목 note 에 실재해야 하고, 생성 HTML 은 ban-sweep 범위 안이다.
run 'review_before_after --selftest' python3 scripts/build_review_before_after.py --selftest
#  ★ 2026-09-13 (계약 §5-v3 ③) — S3 코호트 봉인: raw 전수 + sha256, 솔버 성공 여부를 보지 않는다.
run 'seal_area_cohort   --selftest' python3 scripts/seal_area_cohort.py --selftest
#  ★ 2026-09-13 (계약 §5-v3 ①) — ρ 측정: 생산 솔버를 허용오차 ×0.1 로 두 번, 실제 경로·kwarg 기록.
run 'measure_rho        --selftest' python3 scripts/measure_rho.py --selftest
#  ★★ 2026-09-14 (계약 §5-v4 A·B·D-3) — S3 **런 전** 봉인.  라벨·순서자리·솔버 환경을
#    결과를 보기 전에 못박고, 마감(2026-09-17) 전 쓰기를 **거부**한다 (selftest 가 단언).
run 'seal_s3_prerun     --selftest' python3 scripts/seal_s3_prerun.py --selftest
#  ★★ 2026-09-15 (계약 §A·B·C·D · 원장 `L2-01`·`R4-10`) — S3 **런**.  봉인 도구는 발행만
#    막았고 런을 막는 것이 없어 마감 규칙이 산문이었다.  이 러너는 봉인 없이는 rc=2 다.
run 'run_s3_psi         --selftest' python3 scripts/run_s3_psi.py --selftest
run 'check_doc_refs          --selftest' python3 scripts/check_doc_refs.py --selftest
run 'check_cohort_packages  (커밋된 패키지 ↔ 원장)' python3 scripts/check_cohort_packages.py
run 'audit_adjudication   (원시 감사 ↔ 판정 원장)' python3 scripts/check_audit_adjudication.py
#  ★★ 2026-08-31 — 문서가 **없는 파일·없는 커밋**을 가리키는 자리를 잡는다.
#    깨진 참조는 조용하다: 열어 보기 전에는 안 보이고, 열어 봤을 때는 이미 그 문서를
#    믿고 판단한 뒤다.  예외는 `docs/reviews/doc_refs_allowlist.tsv` 에 **이유와 함께**
#    등재하고, 그 파일이 생기면 검사기가 등재 자체를 낡았다고 지적한다.
run 'check_doc_refs         (문서가 가리키는 것이 실재하는가)' python3 scripts/check_doc_refs.py --quiet
#  ★★ 2026-08-30 — 봉인된 설계를 **매번** 다시 검증한다 (R14 조건 6·7).
#    상자는 기존 130 런에서 유도되고 CSV 는 해시로 사전등록에 묶여 있는데, 08-29~30 에는
#    사람이 한 번 돌려 보고 끝이었다.  손으로만 도는 검사는 없는 것과 같다 (규칙 K).
#    ⚠ 해시를 여기 박아 두는 것이 요점이다 — CSV 가 바뀌면 이 줄이 **빨간불**이 되고,
#      그때 사전등록의 봉인도 같이 고쳐야 한다는 것이 강제된다.
run 'lhs_ext_materialize     --selftest' python3 scripts/lhs_ext_materialize.py --selftest
run 'lhs_ext_submit_gate     --selftest' python3 scripts/lhs_ext_submit_gate.py --selftest
run 'lhs_ext_design (봉인 CSV ↔ 상자 ↔ 해시)' \
  python3 scripts/lhs_ext_design.py --verify docs/data/lhs_ext_design_v2_20260829.csv \
    --box docs/data/lhs_ext_box_v2_20260829.json \
    --expect-sha256 bc72b8bf274842b7c54e319ceac70f5cb2804aa3635f329dfed34697bd52ea19

#  ★★ 2026-09-01 (Codex R19 Q6) — **어디에서도 안 돌던 검사기 72개**를 여기서 돈다.
#    규칙 K 는 이 파일 ↔ CI 를 손목록으로 대조하는데, *둘 다에 없는* 것은 원리적으로
#    못 잡았다.  실측 101개 중 72개가 그 상태였고 그중 둘은 **실제로 빨간불**이었다
#    (`env_db` 노브 누락 · `seminar_deck_extract` 표지 면제가 배너 삽입에 깨졌다).
#    ⚠ 여기 이름을 72개 적지 않는 것이 요점이다 — 손목록은 또 낡는다.  드라이버가
#      `docs/reviews/selftest_inventory.tsv` 를 읽고 돈다 (실측 합계 ~5 분).
run 'selftest_inventory     (분류·레인·CI 의존)' python3 scripts/check_selftest_inventory.py --quiet
run 'fast 자기검사 전수     (등재 기반 드라이버)' python3 scripts/check_selftest_inventory.py --run-fast

echo
if [ "$FAIL" = 0 ]; then
  echo "✓ 전부 통과 — 커밋해도 된다 (CI 가 같은 것을 다시 돈다)"
else
  echo "✗ 실패가 있다 — 고치고 다시.  ⚠ 이대로 푸시하면 러너의 fail-closed 게이트가"
  echo "  사용자의 GPU 런을 막는다 (규율 검사는 런 시작 전에 걸린다)."
fi
exit "$FAIL"
