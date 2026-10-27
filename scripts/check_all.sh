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
    #  ★ 10-04 — 실패한 경우의 이름이 tail 밖이면 안 보였다 (믹서 런처 127/1 불안정 · 게이트 안에서만 · 경우 이름 미표시 2 회 —
    #    인계 문서 §5).  실패 표지 줄 (✗ · FAIL) 을 먼저 모은다 — "0 FAIL" 요약 줄은 뺀다.
    grep -n -E '✗|FAIL' /tmp/_ca.$$ | grep -v -E '(^|[^0-9])0 FAIL' | head -15 | sed 's/^/      [실패 줄] /'
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
#  ★ 2026-10-02 (①, CL-81) — 상 경계 계면 저항 r_int: 파서 · 직렬 해석해 · r 없음 비트 동일 ·
#    pid 경계 · 소산 분담 계면 몫 · 전류 진단 일관성.  규칙 K 목록 + CI yml 에도 같이 건다.
run 'step3_sigma            --selftest-rint' python3 scripts/step3_sigma.py --selftest-rint
#  ★ SELF-45 (2026-09-22) — 필드 통계가 **그림 예산에 불변**인지는 step3_sigma 의 selftest 가
#    보고, 옛 payload 를 고치는 후처리기는 자기 selftest 가 본다 (복원의 정확성 + 거부).
run 'repair_focus_top       --selftest' python3 scripts/repair_focus_top.py --selftest
#  ★ 2026-09-22 (병합 검증) — 웹앱 패치 2건의 selftest 가 **어느 레인에도 없었다**
#    (원장 lane=none · check_all/CI grep 0/0).  합쳐 3.5 초인데 자동 규율이 아니었다 =
#    CDXR3-8 이 잡았던 그 모양("테스트가 존재하고 수동 실행이 녹색인 것만으로는
#    자동 규율이 아니다").  ⇒ 둘 다 두 레인에 건다.
run 'webapp_env_audit       --selftest' python3 scripts/webapp_env_audit.py --selftest
run 'type_map_resolve       --selftest' python3 scripts/type_map_resolve.py --selftest
#  ★ 2026-09-22 (패치 §8 세 번째) — `type_map_resolve` 는 **앞으로** 들어오는 덱만 막는다.
#    이미 `?` 로 계산돼 저장된 옛 케이스는 전수 확인된 적이 없다.  스윕 도구의 selftest 가
#    ⓐ 실사고 재현 ⓑ **다른 표식**(atoms 는 `?` 가 아니라 빈 칸이다) ⓒ 빈 스윕 거부를 건다.
run 'type_map_unknown_sweep --selftest' python3 scripts/audit_type_map_unknown.py --selftest
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
#  ★ 2026-09-30 (웹앱 ① · J20-l) — 닫힌 파라미터 라벨 · 툴팁 = 코드 정의 (Hertz 계열 = c_cpl[22] · ε_sphere / ε_union 쌍 렌즈 ·
#    판 간격 · AM–AM CN std · 라벨 → 툴팁 역맵 전수 · 접촉 요약 탭이 파괴 툴팁을 빌려 쓰지 않음 · 그룹 열 · MD 보고서)
run 'webapp: closed_param_labels' python3 webapp/test_closed_param_labels.py
run 'webapp: closed_param_values' python3 webapp/test_closed_param_values.py
run 'webapp: closed_param_groupview' python3 webapp/test_closed_param_groupview.py
run 'webapp: cf_full_labels'      python3 webapp/test_cf_full_labels.py
run 'webapp: tortuosity_all'      python3 webapp/test_tortuosity_all.py
run 'webapp: closed_param_exact_union' python3 webapp/test_closed_param_exact_union.py
run 'webapp: coverage_handover_scope' python3 webapp/test_coverage_handover_scope.py
run 'webapp: am_isolation_labels'    python3 webapp/test_am_isolation_labels.py
run 'webapp: percolation_labels'     python3 webapp/test_percolation_labels.py
#  ★ 2026-10-01 (LHS 인계 v1.1 ①② · J20-l) — 경로 기준 고립 = 100 − 활성 · 분해 (단절 · 무접촉) · 고립 위험 (접촉 0–1 개) 과 다른 양
run 'webapp: ionic_isolation_labels' python3 webapp/test_ionic_isolation_labels.py
#  ★ 2026-09-30 — /mixer 침대 보기 (보기 전용) — 경로 탈출 · 맹검 잠금 (정책 fail-closed) · 덤프 관문 · 단면 경계 · 쓰기 없음 (반례 41)
run 'webapp: mixer_bed_view'      python3 webapp/test_mixer_bed_view.py
#  ★ 2026-10-01 — 투명 배경 PNG (슬라이드용) — /mixer 침대 보기 ☐ "투명 배경 PNG" (기본 꺼짐 = 옛 출력 그대로) ·
#    케이스 3D 뷰어 Screenshot ☑ (모드별 옛 기본값 · 전류밀도 장 모드 투명 = opt-in).  내보내기 함수를 잘라 node 로 그대로 돌린다
run 'webapp: png_transparent_export' python3 webapp/test_png_transparent_export.py
#  ★ 2026-09-22 — 믹서 런처·생성기 회귀 (LIGGGHTS 없이 가짜 실행파일로).  같은 날 사고 둘을 재현해 막는다:
#    배너 없는 완주 런을 "죽음" 으로 읽고 재발사(E0_s49979687) · 실행 중 덱 제자리 덮어쓰기(E0_s32452843).
run 'mixer launcher (완주 판정 · 덮어쓰기 가드)' bash dem_scripts/mixer_20260921/test_launcher.sh
#  ★ 2026-10-27 (non-Rint 통합 · 대응표 `docs/collab/claude_to_codex/20261027-0220_nonrint-merge-sha-map.md` §6 2) — 믹서 D2 소비자 ·
#    D3 유한 격자 후보 판독기 직접 시험 (합성 덱 · 합성 계약만 · 시뮬레이터 없음).  Codex 가지에서 반입된 뒤 이 파일 · CI · 등재 어디에도 없었다
#    (통합 때는 손으로만 돌림 · 13 · 28 unittest OK).  unittest 라 `--selftest` 플래그가 없어 등재 (`selftest_inventory.tsv`) 대상이 아니고
#    드라이버 (`--run-fast`) 도 못 돈다 → 이름으로 건다 (CI 에도 같이).  실측 (10-27 · 컨테이너 · 두 번) D2 1.47 · 1.27 s · D3 0.42 · 0.40 s.
run 'mixer D2 소비자 (합성 덱 · 결속 검증 · unittest)' python3 scripts/test_mixer_d2_consumers.py
run 'mixer D3 후보 판독기 (합성 계약 · unittest)'      python3 scripts/test_mixer_d3_candidates.py
#  ★ 2026-10-27 (non-Rint 통합 · 같은 대응표 §6 3) — 언로딩 키트 (ULPRI · `docs/data/ps45_unload_20261009/`) 직접 검사 다섯.  통합 뒤 이 트리의
#    키트 폴더 = 수용 핀 4c29705fa 와 같다 (`git diff` 0) 인데 이 파일 · CI 어디에도 없었다 (통합 때도 돌리지 않음).  키트는 `scripts/` · `webapp/`
#    밖이라 등재 (`selftest_inventory.tsv`) 가 보지 않는다 → 이름으로 건다 (CI 에도 같이).  꼴 = 키트 README · 인계 색인 §6 그대로 `python3 -I`
#    (봉인 키트 · 표준 라이브러리 + 같은 폴더 모듈 · 러너 모의 = bash + 가짜 mpirun · lmp · 임시 폴더 · LIGGGHTS 없음 · 물리 실행 아님).
#    실측 (10-27 · 컨테이너 · 두 번) ul_reader 14.44 · 15.54 s · ul_gates 0.27 · 0.13 s · ul_runner_test 42.20 · 39.94 s ·
#    make_unload_decks --check 1.69 · 1.73 s · seal_kit --check 1.13 · 1.16 s.
run 'ULPRI ul_reader         --selftest (언로딩 판독기)'      python3 -I docs/data/ps45_unload_20261009/ul_reader.py --selftest
run 'ULPRI ul_gates          --selftest (관문)'               python3 -I docs/data/ps45_unload_20261009/ul_gates.py --selftest
run 'ULPRI ul_runner_test    --selftest (러너 모의 · 가짜 lmp)' python3 -I docs/data/ps45_unload_20261009/ul_runner_test.py --selftest
run 'ULPRI make_unload_decks --check (덱 = 생성 결과)'        python3 -I docs/data/ps45_unload_20261009/make_unload_decks.py --check
run 'ULPRI seal_kit          --check (봉인 · 활성 규칙)'      python3 -I docs/data/ps45_unload_20261009/seal_kit.py --check
run 'webapp: launcher (포트 선점)' python3 scripts/test_webapp_launcher.py
run 'webapp: temp_pressure'       python3 webapp/test_temp_pressure_wiring.py
#  ★ v3 (2026-09-09) — 화면이 원장을 따라가는가 + **원장을 보여 주는 페이지가 금지값을
#    안 찍는가**.  후자가 이 검사의 요점이다: 초판 구현이 `/ledger` 에서 11 건, `/` 에서
#    2 건을 흘렸다 (원장 본문·`why` 가 *왜 철회됐나* 를 설명하느라 그 값을 인용한다).
#    감사가 `app.py:4035` 에서 찾은 것과 **같은 양식**이라 회귀로 못박는다.
run 'webapp: ledger_view'         python3 webapp/test_ledger_view.py
run 'webapp: meta_json_robust'    python3 webapp/test_meta_json_robust.py   # 09-26 깨진 meta.json → / 500 회귀
run 'webapp: atoms_only_viewer'   python3 webapp/test_atoms_only_viewer.py  # 10-02 atom 만 올린 케이스 결과 페이지 500 · atom+mesh 3D 판 (WEB-01)
run 'webapp: atoms_only_porosity' python3 webapp/test_atoms_only_porosity.py  # 10-07 atom + 판 메시만 — 공극률 · 두께 (접촉 분석과 같은 함수 · real_14 비트 같음) · 입자 윗면 기준 (덜 다져진 프레임) · 덤프 상자 · 기공 보기 영역 윗면
run 'webapp: dem_pore_path_view'  python3 webapp/test_dem_pore_path_view.py  # 10-07 DEM 3D — 기공 (빈 공간 · 격자 추정) 보기 · Path Only View 가 화면의 경로를 연다 (옛 판: 늘 0 번 클러스터)
run 'webapp: tau_paths_view'      python3 webapp/test_tau_paths_view.py     # 10-07 DEM 3D — Tortuosity 후보 경로 여럿 (τ 색 · 금색 = 가장 작은 τ · 주기 반 토막) · All Paths View PNG (투명 4× · 컬러바 따로 / 넣기)
run 'webapp: force_chain_view'    python3 webapp/test_force_chain_view.py   # 10-07 DEM 3D — Force Chain (접촉 쌍 색 · 굵기 = 5–95 백분위 상대 힘 · 묶음 수 · 힘 합 몫 · fn 절대값 없음 · 상자 안) · Force Chain View PNG (투명 4× · 잘림 없게 맞춤 · 범례 따로 / 넣기)
run 'webapp: viewer_coordination' python3 webapp/test_viewer_coordination.py  # 10-06 3D 뷰어 배위수 보기 — 입자별 CN 평균 = core 함수 = 보고값 (real_14 정확히) · 캐시 스키마 12 (live · archive) · 범례 PC/SC
run 'webapp: viewer_am_contacts'  python3 webapp/test_viewer_am_contacts.py   # 10-06 AM 접촉 확대 — /am-contacts (live · archive) · 최소영상 · 합집합 = 생산 함수 (real_14) · cap 각 · 4× 투명 PNG
run 'webapp: network_current_view' python3 webapp/test_network_current_view.py  # 10-07 ⚡ 전류 흐름 (DEM 뷰어) — --dump-raw-dir 비트 동일 · 한 번 덤프 도구 (게시 파일 무변경 · 세대 glob) · /network-current (상위 N · 단면 보존 · Tellegen) · 뷰어 함수 (node)
run 'webapp: net_current_density' python3 webapp/test_net_current_density.py  # 10-07 #17 접촉 전류 밀도 (A cm⁻²) — 손 계산 망 (j = I σ₀ 10⁴ / A) · 덤프 |I| 항등식 · σ₀ 출처 (증서) · ⟨J⟩_1V = 게시 σ × 10 / T · @1C = Q_areal (등급 엔진) × 1 h⁻¹ · 컬러바 @1V · @1C · 옛 몫 표시 없음
run 'webapp: viewer_load_view'  python3 webapp/test_viewer_load_view.py   # 10-07 #11 AM 만 칠하기 (LW = 정본 calc_love_weber_stress · 최대 AM–AM 힘 · 벽 표지) · WEB-06 최대 접촉 압력 (압축만 · 이름 · 툴팁) · real14 (WEB-06 점검 셈 · LW 2.737) · 발사 뒤 app.py 패치 적용 · 실행
run 'webapp: je_definition_label' python3 webapp/test_je_definition_label.py  # 10-03 RINT-03 — 입자별 je·jb 정의 표지 (옛 payload = 옛 정의 경고 · A/B 불일치)
run 'webapp: rint_scope_labels'   python3 webapp/test_rint_scope_labels.py  # 10-03 RINT-04 · 05 · 17 · 18 — Joule bulk-only · 반응 솔브 r-ON 꺼짐 · 상/계면 · 단자 R_int
run 'webapp: tau_labels'          python3 webapp/test_tau_labels.py         # 10-04 τ 2단계 ① TAU-01 · 02 · 21 — √ 행 COMSOL/EIS 표기 제거 · tau2 행 · physics 빈칸 · 정오표
run 'webapp: tau_handover_status' python3 webapp/test_tau_handover_status.py  # 10-04 τ 2단계 ② — 케이스 τ 블록 인계 상태 · 띠 규칙 행 (tau_flux 표시 · J20-l)
run 'webapp: stress_lw_labels'    python3 webapp/test_stress_lw_labels.py   # 10-04 ④b — Love–Weber 줄 · 옛 줄 이름표 (50/50) · 그룹 표 · 그림 (0 안 그림) · 보고서 · 등급 축 불변
run 'webapp: constriction_power'  python3 webapp/test_constriction_power_labels.py  # 10-04 ④a — 협착 전력 몫 행 · 옛 행 이름표 (비가중 · L2-08) · physics 칸 복사 정정 · 그룹 열 · 보고서 · 등급 축 불변
run 'webapp: s567_labels'         python3 webapp/test_s567_labels.py   # 10-04 ⑤⑥⑦ — F1 툴팁 (10 nm 출처 없음) · 경로 면적 선별 표본 (LHS-32) · 파괴 LHS-31 · eff_area 식 · A_dem_geometric
run 'webapp: tau_grade_unify'     python3 webapp/test_tau_grade_unify.py   # 10-04 ②b TAU-03 — 등급 τ · overhead = Hertz 원 솔버 σ + 짝 σ₀ (한 도우미) · COMSOL 2D 두 모드 행 · regime DB · L4-04
run 'webapp: network_handover_chain' python3 webapp/test_network_handover_chain.py  # 10-05 RGL · SELF-86 — 실 생산자 → 정지 helper → τ → 배치 기록 (stop_after=network) → build_handover 끝-끝 (옛 코드 5/8 = RGL-02 · 03 · 04)
#  ★ 2026-10-16 (Codex LHS214 재검증 L214R-03 · 수정 계획 Q3 = 화면만) — 최종 병합 뒤 현재 모드별 망 상태가 이긴다: 미채택 모드 (모형 한계 · σ 없음 · not_computed ·
#    valid_zero) 의 이온 σ · FULL 유도비 = '—' (+ 사유) · Δ '—' — split · 두 열 · 네 열 옛 CSV · 실 생산자 · Flask GET /single — 고치기 전 app.py 5/14.
run 'webapp: l214r03_display'   python3 webapp/test_l214r03_display.py
#  ★ 2026-10-16 (1저자 Q1 · 원장 WEB-09 · 화면만) — 받아들인 모드 (computed · 유한 σ > 0) 칸도 옛 contact 단계 CSV 대신 지금 full_metrics 값 (새 표와 같은 도우미 ·
#    같은 정의 · 꼴) · 한쪽만 지금 값이면 Δ '—' · 새 표 행 그대로 · valid_zero '—' 유지 — 고치기 전 app.py 7/16.
run 'webapp: web09_accepted_refresh' python3 webapp/test_web09_accepted_refresh.py
#  ★ 2026-10-19 (Codex 재확인 2 L214RR2-04 · 원장 L214R-S04 · 1저자 Q4 · 화면만) — 과거 · 외부 메트릭의 null (sigma_ratio · phi_se · tortuosity) 이 /single 을
#    500 으로 죽이지 않는다 · 툴팁 세 블록 = 숫자일 때만 형식화 · 아니면 '—' 또는 일반 문구 (키 없음의 옛 '0.0000' 도) — 고치기 전 single.html 2/6.
run 'webapp: single_null_metrics' python3 webapp/test_single_null_metrics.py
run 'webapp: psi_generation_stamp' python3 webapp/test_psi_generation_stamp.py  # 10-06 L2-01 세대 2 — full_metrics · 도장 psi_placement_physics (솔버 출력) · 망 소유 키 · 정지 계약 ⑥b · 옛 세대 재투영 · τ 협착 라벨
run 'webapp: gen2_publication_handover' python3 webapp/test_gen2_publication_handover.py  # 10-06 밤 G2R-01 · 02 — Codex 게시 · 인계 반례 (H12 주 자리 · ψ/전극 오타 · 부분 결손 · 표지 없는 후보) 를 실 생산자 사슬로: 정지 · 일반 경로 게시 전 거부 · 강제 폴더 인계 거부 · 같은 결함 코호트 · 옛 세대 추론 자격 (도장) · build_handover (옛 코드 2/11)
run 'g2_network_reread --selftest' python3 scripts/g2_network_reread.py --selftest  # 10-07 Codex 세대 2 재검증 §7-4 — 게시 다시 읽기 (읽기 전용): 실 생산자 게시 (관통 · 비관통 · GEN2-01) 양성 · 증서 CF → FULL · 도장 null · 기대 세대 다름 · manifest 선언 없음 반례 · ★ G2RR4-01 실 생산자 JSON = 상세 계약 (17/19 → 19/19)
run 'webapp: gen2_stamp_record' python3 webapp/test_gen2_stamp_record.py  # 10-06 밤 G2RR-01 — 도장 ↔ 레코드 세대 대조 (실 생산자 → 게시 → 인계): Codex 도장 변이 (unknown · null · legacy · one_null_legacy_shape) · 키 하나씩 결손 · null · unknown · legacy · 타입 → τ P4 거부 · 역사 경로 = 확인된 역사 도장 스키마 (194 v1.2 실측 194/194) · 배치 manifest 기대 세대 · 웹앱 망 세대 행 (옛 코드 6/23)
run 'webapp: hetero_transcript'   python3 webapp/test_hetero_transcript_page.py   # 10-05 이종기술 회의록 — 회의 둘 (09-18 · 10-02) 고르기 · 회의 종합 · 등록부 밖 키 404 · /hetero 논지 정본 비준 블록 (docs/hetero_thesis.md 에서 읽음 · fail-closed)
run 'webapp: rint_explainer (Rint 설명 정적 페이지 + 사이드바 링크 · 봉인 app.py 무변경 · 10-21)'   python3 webapp/test_rint_explainer_page.py
run 'webapp: mpm_lab_cmp_absent_phase (MPM lab 비교표 · 없는 상 = — · 참 0 유지 · 10-21)'   python3 webapp/test_mpm_lab_cmp_absent_phase.py
#  ★ 2026-10-03 (Codex r_int 1단계 RINT-02 · 13 · 14 · 20) — ① 계면 요청 ↔ 네 솔브 적용 영수증을 **실물 producer** 로.
#    `solve_sigma_z(..., rint=)` 호출 넷을 AST 로 찾아 하나씩 `rint=` 를 지우면 게시가 거부돼야 한다 (주 솔브만 보던
#    옛 사후 단언은 wetted/bare 배선 삭제를 초록으로 냈다) · CLI 모순 요청 · check_arm 영수증 변조 · 레지스트리 전수 분류.
run 'rint_receipts (요청 ↔ 적용 영수증 · AST 변이 4)' python3 scripts/test_rint_receipts.py
#  ★ 2026-10-07 (Rint G2 ①′ AM–AM · 계약 v3.1 · Codex v3 "계약 정정 둘 뒤 구현 GO · 정량 채택 HOLD") — 반례 먼저:
#    ε 동률 집합 규칙 (3 청구자 6 순열) · 동심 비동일 · 정확 중복 거부 · raw raster 순열 진단 (3170 ↔ 3171) · 동결 마스크 순열 불변 ·
#    OFF 비트 같음 (막 0 + 예외 융합 · 순서마다) · 단위 (같은 리드 · 1e−8·A/r) · 탄소 가림 (막 소자만) · E4′ 부류 FD · 원장 무결성.
#    고치기 전 코드 = 10 PASS · 18 FAIL (새 API 없음) · `--s3 PATH` 로 다른 step3_sigma 를 시험할 수 있다.
run 'rint_g2_am_iface (①′ AM–AM 계약 v3.1 · 반례 먼저)' python3 scripts/test_rint_g2_am_iface.py
#  ★ 2026-10-20 (Rint ② S1 · 설계 v1 §3 · R18 Q6 · 1저자 N1–N18 권고대로) — PTFE 면 개구율 `face_alpha` (기본 끔 · 끄면 옛 경로 비트 같음):
#    R18 종료조건 8 · F16 해석 개구율 (판별력) · 변이 8 · 계획 무결성 · 진단 거부 · p3ca id · ca_ext_record_ok · payload 끝-끝
#    (세 분기 · 거부 조합 19 · sid = off 격자 · 채널 독립 · check_arm).  고치기 전 (d1768cf0c) = 1+3 PASS (끔 경로 지킴이) ·
#    22+31 FAIL · 웹앱 표지 2 PASS · 7 FAIL.  `--old-scripts DIR` (기반 scripts 사본) 을 주면 끔 경로 비트 대조 B1 · B2 도 돈다.
run 'ptfe_face_alpha (Rint ② S1 · 시험 먼저)' python3 scripts/test_ptfe_face_alpha.py
run 'webapp: ca_ext_labels (S1 표지 · 봉인 밖 템플릿)' python3 webapp/test_ca_ext_labels.py
#  ★ 2026-10-20 (Rint ② S2 · S3 · 설계 v1 §4 · §5 · §6 · 1저자 N1–N18 권고대로) — 탄소 접합 R_j v0 · SDCP 접합 수정자 · STEP3 수렴 증서
#    (기본 끔 · 끄면 옛 경로 비트 같음): 손으로 세운 회로 (직렬 사슬 · 사다리) · 축약 · 절단 · 실제 그래프 가지치기 · 관문 (조립 전 거부 · CG 0) ·
#    끔 비트 같음 C0 (기준 d1768cf0c 의 step3_sigma) · PIECE (멤버십 셀 = `_fibre_segment_ijk`) · FA+CJ (S1 face_alpha 와 한 솔브에 같이 = 거부 ·
#    A · B 합침) · 증서 봉인값 (rtol 1e-12 · ε_I 1e-4) 기계적 재유도.  고치기 전 = 2/22 · 2/11 PASS.  `--quick` = C0 무작위 침대 수를 줄인다.
run 'carbon_junction (Rint ② S2 · S3 · 시험 먼저)' python3 scripts/test_carbon_junction.py
#  ★ 2026-10-20 (Rint ② B6 · 설계 v1 §4-2 · §5-2 · §6 · §7 · 1저자 N1–N18 권고대로) — payload 의 탄소 접합 · SDCP 수정자 배선 · 조합 정책
#    (face_alpha + cjunc = 거부 · face_alpha / cjunc + rtol = 허용) · 러너 다음 세대 손잡이 · 판정기 소비자 검사 (기본 끔 · 끄면 옛 경로 그대로):
#    ca_ext_b6 = run_contract 등록 · payload 끝-끝 (고치기 전 1/50 · `--old-scripts DIR` = 끔 비트 대조 B) · 10-20 실측 50 s ·
#    ca_ext_runner = 러너를 실제로 부른다 (가짜 python3 = 규율 관문 둘만 건너뜀 · payload 실물) · 발사 전 거부 40 + payload 거부 대조 ·
#    이름 태그 · SKIP 함정 · 규칙 L 격리 (고치기 전 23/114 · `--old-runner PATH` = 끔 경로 NB) · 10-20 실측 92 s ·
#    ca_ext_verdict = 판정기 (ca_ext_record_ok · p2 ↔ p3ca 섞임 · 증서 없음 = 미게시) · 실물 코호트 (고치기 전 11/31 · `--old-verdict PATH`) · 49 s.
run 'ca_ext_b6 (Rint ② B6 payload 배선 · 조합 정책 · 시험 먼저)' python3 scripts/test_ca_ext_b6.py
run 'ca_ext_runner (Rint ② B6 러너 다음 세대 손잡이 · 시험 먼저)' python3 scripts/test_ca_ext_runner.py
run 'ca_ext_verdict (Rint ② B6 판정기 소비자 검사 · 시험 먼저)' python3 scripts/test_ca_ext_verdict.py
#  ★ 2026-10-20 (Rint ② 2 일 차 Z1) — 러너 · 판정기 굳히기: SIGMA_FIBRE_BULK (직경 보존 · 손계산 · payload 다시 계산 대조 · 이름 태그) ·
#    다음 세대 노브 = STEP3_RTOL 필수 (팔 시작 전) · 사슬 env 오염 = 거부 · compare_dirs 의 ca_ext 축 · 판정기 --expect-generation
#    (고치기 전 17/86 · `--old-scripts DIR` = 끔 경로 ZB) · 10-20 실측 42 s.
run 'ca_ext_z1 (Rint ② Z1 러너 · 판정기 굳히기 · 시험 먼저)' python3 scripts/test_ca_ext_z1.py
run 'rint_r_chain (Rint ② R 런 사슬 · 사다리 · 예측 · 판정 · 가짜 러너 · 시험 먼저)' python3 scripts/test_rint_r_chain.py
run 'ca_ext_z3 (Rint ② Z3 face_alpha + 탄소 접합 한 런 · 극한 런 · ARM_LIST · sid_off · CG 반복 수 · 시험 먼저)' python3 scripts/test_ca_ext_z3.py
run 'rint_r_chain_e2e (Rint ② R 사슬 · 실제 러너 끝-끝 · 픽스처 킷 · CPU)' python3 scripts/test_rint_r_chain_e2e.py
run 'step3_target_cert (STEP3 목표량 증서 ⓓ · RCA-07 · 13 · 해 상태 · 빠른 판 · 시험 먼저)' python3 scripts/test_step3_target_cert.py
run 'step3_conv_cert (STEP3 수렴 증서 A/B/C · 봉인 표 · 10-21 실측 115–124 s 로 게이트에 넣음)' python3 scripts/test_step3_conv_cert.py
# (10-21 · 1저자 *"더 꼼꼼하게"* → 위 두 줄로 게이트에 넣음 · 실측 115–124 s · 부하 낮음 · BLAS 스레드 1 · 옛 2,305 s 는 부하 8–12 때 · ⚠ K8b 는 OpenBLAS Sandybridge 경로에서 실패 = 봉인값의 경로 의존 (원장 RCA-07 메모) · 긴 판 `python3 scripts/test_step3_target_cert.py --long` ≈ 400 s = 게이트 밖 · 증서 코드를 바꾼 커밋 뒤 한 번)
# ~~step3_conv_cert (STEP3 수렴 증서) = 게이트 밖 · 손으로 돌린다~~ — 10-20 실측 2,305 s (부하 8–12 · 합성 직접해 대조 탐침) 라 매 커밋 게이트에 넣지 않는다.
#   python3 scripts/test_step3_conv_cert.py   (리뷰 핀 · 판정 런 전 · 수렴 코드를 바꾼 커밋 뒤 한 번)
#  ★ 2026-10-20 (Rint ② S0 · 설계 v1 §2 · 등록 R §2-1) — 표현 원장 (raster 만 · 솔브 없음): 기하 원시 · 접합 census 미리보기 · 격자 원시 ·
#    계획 (식 · 해시 · 개정 커밋 대조) · 스키마 (σ · 전류 칸 없음) · 끝-끝 (payload 실물로 생산 raster 입력을 잡는다).  구현 전 = 0/23 PASS.
run 'ca_s0_census (Rint ② S0 표현 원장 · 시험 먼저)' python3 scripts/test_ca_s0_census.py
#  ★ 2026-10-26 (원장 KG50-02 · KG50-10 · 1저자 Q2) — LIGGGHTS 재개 도구 resume_ckpt.sh 를 가짜 SLURM · 가짜 dem_restart.py 로 끝까지 돌린다
#    (실패한 시험의 본 런 승격 · 재개 덱 정적 대조 · 큐 이름 · -T · -C) · 고치기 전 판 = 7/31 · 실측 ≈ 9 s.
run 'resume_ckpt (재개 도구 · 가짜 SLURM)' python3 scripts/test_resume_ckpt.py
#  ★ 2026-10-27 (50kg D3 칸 판정 · 판정 모드 Hertz = 1저자 결과 전) — 읽기 전용 판독기.  selftest 첫 항목이 등록 README §3 의 문턱 ·
#    모드 · SE_Δ 식 · coverage 두 판정 (Physics · Hertz) 줄을 대조한다 ⇒ 결과를 보고 문턱을 옮기면 여기서 터진다 · 판정 순서 ①–④ · 변이 12/12 + Physics 5/5 잡음 · 실측 < 1 s.
run 'kg50_d3_cell_verdict   --selftest' python3 scripts/kg50_d3_cell_verdict.py --selftest
#  ★ 2026-10-24 (`SELF-132` · `SELF-133` · 1저자 Q2 (가)) — kgy 실행 환경 판 (Python 3.8 · numpy 1.24.4 · scipy 1.10.1 = kgy `~/dem-venv`) 에서
#    R 경로 11 묶음 (S0 · S1 · S2/S3 · 계약 · 사슬 · 끝-끝 · 증서).  3.11 에서만 돌던 코드가 kgy 에서 멈춘 일 (08-16 · 08-25 · 10-24 세 번째) 을 막는다.
#    인터프리터 없음 · 판 다름 = 실패 (건너뛰지 않는다) → `bash scripts/setup_kgy_py38.sh` (컨테이너 재시작 뒤 한 번) · 실측 ≈ 6–7 분.
run 'kgy 판 R 경로 시험 (Python 3.8 · numpy 1.24.4 · scipy 1.10.1 · SELF-132)' bash scripts/check_kgy_py38.sh
#  ★ 2026-10-04 (τ 결정 16 ② · 1저자 비준 *"권고대로"*) — 안 A: 망 솔버 띠 선택을 `boundary_sets` 로 추출 (추출 전 기준값과 비트 동일)
#    + 쓴 규칙 · 띠 폭 기록 (LHS-17 · TAU-14) · 이온 인계 열 도우미 `tau_flux` (v2 §5 · 게이트 G1–G6 · 생산자 ↔ 소비자 계약).
run 'network boundary_rule (안 A · 동작 중립)' python3 scripts/test_network_boundary_rule.py
run 'tau_flux (이온 인계 열 · 게이트 G1–G6)' python3 scripts/test_tau_flux.py
#  ★ 2026-10-06 (Codex 5차 RGLR4-01 · 02) — 194 인계 v1.2 다시 읽기 검산기 (검산 도구 · 자동 배포 관문 아님): 복사본 변조 (공통 칸 한 칸 · 열 탈락 ·
#    감사표 누락 + 중복 · record sha · 상태 · 코호트 · 출처 부록 중복) 가 비영 종료 · 원본 PASS 유지 · 세대별 허용 목록.
run 'reread_v12 (RGLR4-01 · 02 반례 · 원본 PASS)' python3 scripts/test_reread_v12.py
run 'lhs_release v1.3 (빈칸 뜻 · ML 표 · 재적합 · 세대 g2 · τ 다시 읽기 · 발사 봉인 대조 · DRY RUN)' python3 scripts/test_lhs_release_v13.py   # 10-07 생성기 미리 준비 (옛 코드 1/77 · G2RR3-01 배포 관문 = 새 시험이 옛 코드에서 81/135 → 135/135 · ★ G2RR4-01 다시 읽기 상세 ↔ 요약 · 감사 관측 = 137/167 → 167/167 · ★ G2RR4-02 감사 단계 결합 기록 = 168/173 → 173/173 · ★ 10-12 SUP20-01 배치 신원 V22 = 239/256 → 256/256)
#  ★ 2026-10-06 (DESC-06 잔여) — 완료 압력 기록 (LIGGGHTS 로그 압밀 루프 판정 줄) + 인계 생성기 관문 · CLI 명시 승인 (--pressure-record | --pressure-unverified)
run 'lhs_pressure_record (DESC-06 완료 압력 · 생성기 관문)' python3 scripts/test_lhs_pressure_record.py
#  ★ 2026-10-06 밤 (이종기술 2-1 장 7:3 압축 곡선 · x = step) — 로그 thermo + 판 메시 → step 별 압력 · 판 높이.  재시작 잇기
#    (r2 판 재부양 거부) · run 경계 설정 줄 버림 · 판정 줄 ↔ thermo 압력 · 메시 등속 하강 반례 (변이 둘 = 빨강 확인)
run 'compaction_curve (로그 잇기 · 설정 줄 · 판 재부양 반례)' python3 scripts/test_compaction_curve.py
#  ★ 2026-10-06 (`L2-01` 세대 2 · 1저자 개정 — 계약 개정 노트) — ψ 배치 기본값 = 곱셈 · legacy 는 명시 인자로만 · 2 구 접촉 식 (세 채널 ×
#    s ≈ 0.2 · 0.5 · 0.9) · 단조 · Hertz 비트 동일 · tau_flux 협착 라벨 = ψ 배치 · 세 채널 결과의 세대 표기.
run 'psi default switch (L2-01 세대 2)' python3 scripts/test_psi_default_switch.py
#  ★ 2026-10-06 저녁 (세대 2 나머지 · 1저자 비준 C1 · C2) — Physics 면적 g2 (film_area_g2 규칙 B · 정확 lens · 쌍별 E* · µm · 원판 floor ·
#    간선마다 R_c(physics) ≤ R_c(hertz) — real_14 107,223 간선) · 정확 Dirichlet 전극 (가상 전원 제거 · 막다른 가지 · 해석해 · 경계 겹침 ·
#    CG ↔ 직접) · CF 과전도 표지 (FULL 만 거부) · H12 민감도 (짝으로만 · 식 오라클 · H0 비트 동일) · τ 세대 표기 · 섞임 거부.
run 'physics area g2 (C2 ①–⑤ · L1-01/02/03)' python3 scripts/test_physics_area_g2.py
run 'network dirichlet (L2-05 · D1–D7)' python3 scripts/test_network_dirichlet.py
run 'network generation 2 (CF 표지 · H12 · 세대 표기)' python3 scripts/test_network_generation2.py
#  ★ 2026-10-06 밤 (Codex 세대 2 적대 리뷰 G2R-01 · 02 · 1저자 비준) — 공용 세대 계약 (tau_flux.network_generation_contract · 모드마다 허용 모델 조합의
#    닫힌 표 · 부분 결손 거부 · 옛 세대 추론 = 세대 2 표지가 하나도 없을 때만 inferred_legacy) · 행마다 먼저 (같은 결함 코호트 거부) · 진짜 역사 레코드 194
#    (v1.2 배치 원천) = inferred_legacy · v1.2 표 τ 칸 재현 (옛 코드 5/24).
run 'gen2 role contract (G2R-01 · 02 — 역할 · 닫힌 열거 · 옛 세대 추론)' python3 scripts/test_gen2_role_contract.py
#  ★ 2026-10-06 밤 (Codex 세대 2 판정 G2R-03 · GEN2-01 · 1저자 비준) — 정확 Dirichlet 풀이마다 수치 증서 (I_bottom · I_top · 보존 잔차 ≤ 1e-6 ·
#    내부 잔차 ≤ 1e-6 · 방법 · 단 기록) · 증서 실패면 사다리 (직접해 → Jacobi CG → ILU GMRES · 잔차 보정) 또는 NOT_COMPUTED
#    (current_conservation_failed) · 협착-only 의 R_c = 0 = 그 가지만 NOT_COMPUTED (zero_resistance_requires_contraction) · 레코드 직렬화
#    (세 채널 · H12 · CLI 네 JSON · real_14) · 정상 망 = 고치기 전 모듈 (git a0a24c538) 과 비트 동일.
run 'network solve certificate (G2R-03 · GEN2-01)' python3 scripts/test_network_solve_certificate.py
#  ★ 2026-10-16 (Codex LHS214 재검증 L214R-01 · 수정 계획 Q1 = 생산자 수용 상수 그대로) — FULL 모형 한계 증서의 비유한 재구성 q (유한 입력의 중간 넘침 ·
#    T = A = 1e308 · scale 1e200 · 큰 정수) = 기술 실패 사유 (non_finite · 예외 아님) · 마지막 채택 시도 ↔ 요약 결합 (잔차 · 보존 · 방법별 수렴 상태 · 예외) ·
#    레코드 소비자 아홉 · 실 생산자 대조 (정상 모형 한계 · fallback 사다리 · 여섯 단) — 고치기 전 코드 48/112.
run 'L214R-01 증서 유한성 · 채택 단 결합 (반례 먼저)' python3 scripts/test_l214r01_certificate.py
#  ★ 2026-10-16 (Codex LHS214 재검증 L214R-02 · 수정 계획 Q2 = 인계표 독립 칸) — 띠 폴백 (L1 · L2 = BAND_FALLBACK · 사유 공란) 이 가리던 FULL 모형 한계 사실을
#    `full_model_limit_hertz` · `_physics` 칸으로 보존 → 배포 build · check 가 같은 함수로 H0 주 타깃 HOLD (표지 없음 · 모르는 값 · 모순 = fail-closed) ·
#    실 생산자 레코드 · 게시 → 인계 사슬 · 실제 build_v13 / check_v13 — 고치기 전 코드 17/47.
run 'L214R-02 모형 한계 독립 표지 · 배포 HOLD (반례 먼저)' python3 scripts/test_l214r02_model_limit_flag.py
#  ★ 2026-10-16 (1저자 Q3 — L214R-01 A 규칙을 게시 증서 경로로 · 원장 L214R-05) — 게시된 FULL · CF · 협착-only 증서의 재구성 q · σ 가 유한 입력에서 넘치면
#    non_finite 사유 (inf ≤ inf 통과 · 예외 아님) · 0b ∧ 결합 · 0b ∧ 세대 계약 · 레코드 판정 · τ 행 · 실 생산자 정상 증서 대조 — 고치기 전 코드 109/184.
run 'L214R-05 게시 증서 유한성 (반례 먼저)' python3 scripts/test_l214r05_published_certificate.py
#  ★ 2026-10-16 (1저자 (가) — L214R-05 에이전트가 보고한 같은 부류 셋 · 수정 계획 §4-2 · 원장 L214R-06 · 07 · 08) — 게시 증서의 채택 단 결합 (모형 한계 증서와
#    같은 함수 `adopted_attempt_binding_problem`) · 레코드 두 σ 표현 항등식의 비교 전 유한성 (옛 세대 역사 인계 경로 f_ion = ∞ · tau2 = 0 포함) ·
#    float 로 못 옮기는 큰 JSON 정수 = 예외 대신 거부 사유 (숫자 없는 가지 증서 I_bottom = 없음으로 읽지 않는다) — 고치기 전 코드 118/306.
run 'L214R-06–08 같은 부류 셋 (반례 먼저)' python3 scripts/test_l214r06_same_class.py
#  ★ 2026-10-16 (1저자 권고대로 — 마지막 고침 라운드 · 수정 계획 §4-3 · 원장 L214R-09 · 10 · 11) — τ 출력 (f · tau2 · tau) 이 셋 다 유한 양수일 때만 값 상태 ·
#    온도 규약 검사의 다시 계산한 σ_grain · 배수가 비교 전 유한 양수 (아니면 사유 · None 아님) · 정지 계약 수 변환 = tau_flux._num (큰 JSON 정수 = 거부 사유) —
#    실 생산자 · 웹 게시 폴더 · v1.2 옛 레코드 194 대조 — 고치기 전 코드 43/96.
run 'L214R-09–11 같은 부류 셋 (마지막 라운드 · 반례 먼저)' python3 scripts/test_l214r09_same_class.py
#  ★ 2026-10-18 (Codex 재확인 L214RR-01 = 원장 L214R-R01 · 수정 계획 lhs214rr_fix_plan_20261018 Q1 · 1저자 비준) — 보류된 이온 FULL (raw q > 1.5) 를 게시 상태로
#    되돌린 레코드 (값 둘 · 상태 넷 · 증서 상태 둘 — 증서 수치 그대로) = 게시 증서 공용 판정이 반올림 전 재구성 q 를 생산자 고정 정책과 대조해 거부 → 세대 계약 ·
#    정지 · τ · 다시 읽기 · 인계 · 배포 (build_v13 · 배치 관문 · 세대 관문 · τ 다시 읽기) 가 같이 거부 · 경계 1.4999999999999998 · 1.5 · 1.5000000000000002 ·
#    CF · 협착-only 진단 값 · 열 FULL · 진짜 비관통 그대로 — 고치기 전 코드 9/27.
run 'L214R-R01 보류 값 게시 복원 거부 (반례 먼저)' python3 scripts/test_l214r_r01_restored_full.py
run 'L214R-R04 게시 이온 가지 표지 ↔ 재구성 q (반례 먼저)' python3 scripts/test_l214r_r04_cf_label.py
#  ★ 2026-10-06 밤 (3단계 · C2-⑥ 1저자 비준 · LHS-25 · LHSC-08 · LHS-27) — Physics 피복 = 합집합 cap (`*_physics_union` 새 키 · 해석해 ·
#    생산자 빈칸 계약 · real_14 51.522 → 43.218 = 설계 원형 AM 457 개 1e-13 안 · case15 = 빈칸 (c_cpl[22] < 0) · 원형 ×0.87 재현) ·
#    벽 근접 접선 수 (분류 불변 · 자릿수는 파일마다 · STL 따로) · 피복 CLI 가 실행 위치 추적 파일을 안 덮는다 (--summary-out 명시만).
run 'union coverage ⑥ (C2-⑥ · LHS-25)' python3 scripts/test_union_coverage.py
run 'wall near tangent (LHSC-08)' python3 scripts/test_wall_near_tangent.py
run 'coverage CLI no tracked write (LHS-27)' python3 scripts/test_coverage_cli_no_tracked_write.py
run 'webapp: coverage_union_display' python3 webapp/test_coverage_union_display.py   # ⑥ 웹앱 같은 묶음 — Physics 열 = 합집합 · legacy 줄 · 옛 케이스 — · 그룹 · 보고서 · 그림
run 'parse_case_paste ⑥ 라벨 (합집합 · legacy 줄)' python3 scripts/test_parse_case_paste_union.py   # 전체 복사 붙여넣기 수집기가 새 행 이름에 조용히 비지 않게
#  ★ 2026-10-04 (J20-s ④b · 1저자 비준 *"권고대로"* · 원장 LHS-29) — Love–Weber 입자 응력 새 열 (접촉점 · 전체 텐서 · 벽 접촉 표지 ·
#    검사 = 열 · F = Fn + Ft · 접촉점 · 전체 virial ↔ c_strs) · real_14 독립 구현 대조 · 생산 CLI 끝단 (옛 키 불변).
run 'love_weber_stress (④b · LHS-29)' python3 scripts/test_love_weber_stress.py
#  ★ 2026-10-04 (J20-s ④a · LHS-30) — 협착 저항 전력 몫 Σ I²R_c / Σ I²R_total (같은 FULL 해 · 관통 간선) · L2-08 반례 손풀이 8.1818 % ·
#    채널 · 모드 꼬리 키 · 머지 목록 (legacy hertz · dual physics 이름 그대로).  σ 비트 동일은 network boundary_rule GOLD 가 같이 지킨다.
run 'constriction_power_share (④a · LHS-30)' python3 scripts/test_constriction_power_share.py
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
run 'lhs_supp_design (보충 · 후막 설계 · 10-06)' python3 scripts/lhs_supp_design.py --selftest
run 'lhs_supp_design (봉인 CSV ↔ 해시 · 재검증)' python3 scripts/lhs_supp_design.py --verify docs/data/lhs_supp_design_20261006.csv --expect-sha256 73d9a47f76f49989ddbd2c1237007c8499601d63bd5baf0e1ad11c527f21beb0
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
