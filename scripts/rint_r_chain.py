#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② R 런 사슬 — SBE 보정 사다리 (등록 R §3) · DBE holdout 예측 (§4) · 판정 (§5) · 다시 판정.

정본 = 등록 R `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` §3 (3-1 – 3-5) · §4 (4-1 · 4-2) · §5 · §6 · §7-1 ·
§10 (명령 꼴 (3)–(5) · 멈춤 목록 · 런 수) · §11 · 설계 v1 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` §6 (수렴 증서 ⓐ ⓑ ⓒ ⓓ) ·
§7 (세대 `p3ca-` · 영수증 · LEAN 표 · 판정 계산기 · 다시 판정).  꼴 = 앞선 같은 부류 사슬 `scripts/sdcp_anchor_v2_chain.py`
(사슬이 점을 고른다 · 값 봉인 · 멈춤 · 요약에서 다음 단계가 읽는다 · 사람이 옮겨 적지 않는다).

  # (3) 보정 사다리 — 법칙 끝마다 (SBE arm 0 · LEAN 2 · 값 봉인)
  python3 scripts/rint_r_chain.py --stage ladder --law P0 --target 1.63 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh \\
      --root ~/sdcp --plan ~/sdcp/ca1_plan.json --s0-plan <리포 S0 계획> --s0-stage2-report <S0 단계 2 보고 (DBE 새 침대)> \\
      --s0-stage1-report <S0 단계 1 보고 (SBE 새 침대)> --machine <짧은 이름표> --max-hours H --out ~/sdcp/ca1_ladder_P0
  # (4) 예측 — 네 모서리 × {R_j,lo · R_j,0 · R_j,hi} (DBE arm 0 · R_j · 계획 · S0 계획은 사다리 요약에서 읽는다)
  python3 scripts/rint_r_chain.py --stage predict --ladders ~/sdcp/ca1_ladder_P0 ~/sdcp/ca1_ladder_P1 --kit kit_DBE_sdcp1um_vgcf100 \\
      --runner … --root ~/sdcp --machine <짧은 이름표> --max-hours H --out ~/sdcp/ca1_predict
  # (4b) ★ 10-27 묶음 C2d — 예측을 12 단위로 (원장 시도만 · 단위 = <법칙>_c<c>_<R 역할> · 넘침 점 = 같은 이름 · 끝 = 합치기)
  #   … --stage predict … --ledger <원장> --attempt <n> --unit P0_c0_R_j0 --out ~/sdcp/ca1_units
  #   … --stage predict … --ledger <원장> --merge ~/sdcp/ca1_units --out ~/sdcp/ca1_merge1            (넘침 있으면 rc 4 · expansion.json)
  #   … --stage predict … --ledger <원장> --attempt <n> --point P0_c0_R_j0 --expand ~/sdcp/ca1_merge1/expansion.json --out ~/sdcp/ca1_points
  #   … --stage predict … --ledger <원장> --merge ~/sdcp/ca1_units ~/sdcp/ca1_points --expand ~/sdcp/ca1_merge1/expansion.json --out ~/sdcp/ca1_predict
  # (0) 계획 숫자 블록 (등록 R 에 붙이는 표 · 계획 JSON 에서 생성) · 대조
  python3 scripts/rint_r_chain.py --stage plan-doc --plan ~/sdcp/ca1_plan.json [--registration <등록 R> --check-doc]
  # 감도 (등록 R §5-6 · 필수 · ★ 주 판정 단계 뒤에만 — Q-F): --variant FIBRE | UNREG | GRID (사다리 둘 + 예측) · SVORDER (예측만 · 주 사다리)
  #   … --variant FIBRE --after-main ~/sdcp/ca1_predict
  # (5) 판정 — 원 팔 JSON 전부에서 (값은 --show-results 로 한 번) · 다시 판정 (읽기 전용 · 바이트 대조)
  python3 scripts/rint_r_chain.py --stage verdict --runs <사다리 · 예측 · 감도 폴더 …> --out ~/sdcp/ca1_verdict [--show-results]
  python3 scripts/rint_r_chain.py --stage verdict --reverify ~/sdcp/ca1_verdict [--out <새 보고 폴더 · ★ C2e reverify_report.json>]

값 봉인: 사슬은 σ 를 읽어 점을 고르지만 화면 · 로그 · 공개 요약에는 σ 를 쓰지 않는다 (반복 수 · 잔차 · 판 전류 불균형 · 시간 · 상태만 ·
  σ 가 든 멈춤 사유는 그 수를 가린다).  σ 는 팔 JSON 에만 있고, 판정 결과 (`verdict_results.json`) 는 `--show-results` 로 연다.
★ Z3 (10-20) — 러너 · payload API 와 맞춤: face_alpha + 접합 (+ P1) 한 런 · 극한 런 (env `CJUNC_RJ=inf` · `0`) · origin 검사 = `ARM_LIST=1,2`
  한 런 (a0 = 앞 런의 값 그대로 · 넘으면 8 팔 = `ARMS=8`) · off 격자 sid 지문 (`sid_off` = 접합 원장 `fp.sid` · 같은 킷 · 같은 래스터 ·
  같은 origin 런끼리) · CG 반복 수 (공개 기록) · 계약 = 정본 (`ca_ext_record_ok` · `check_arm` · backend = `EXPECT_BACKEND`).
★ 3판 (10-21 · D · 등록 R 3판 · Codex RCA-01 · 02 · 06 · 08 · 09 · 10 · 13 · 사전 리뷰 PRE-design-01 · 05 · 코디네이터 Q-E · Q-F · Q-G):
  · 계획 `rint-r-plan-v2` = v1 칸 + 결과 전 등록 숫자 넷 (점 수 상한 · 역상 R 비 상한 · SV 반사실 문턱 · 범위) — 하나라도 null = 멈춤
  · 두 계획 대조 (S0 `ca-cjunc-plan-v1` ↔ R) · 등록 `| S0 계획 해시 |` 줄 (§2-1 · §10-2 ⑪)
  · 해 상태 (positive · zero · short — `run_contract.next_gen_state`) = 확장 실수 0 · ~~+∞~~ (★ 4판 Q1: short = NOT_COMPUTED) · 모든 비교 = ln
    (단위 불변 · §5-0)
  · 끝 규칙 (§3-2b · 실제 SBE 역상 · 끝 확인 런 · 바깥 실측 이웃) + 끝 origin (세 origin 합집합을 바깥에서 · PRE-design-01 Q-E) ·
    e_min = 국소 진단 (멈추지 않는다) · 역상 R 비 상한 = 계획 (⬜ · 'none' = 상한 없음으로 등록)
  · DBE origin = 네 모서리 × 세 R (§4-2) · 한 R 이라도 넘으면 그 모서리 세 R 전부 8 팔 평균
  · 감도 = 주 판정과 같은 판정 함수 (§5-6 · RCA-09) · 법칙별 I_P · U · E · `GAP_ENVELOPE_ONLY` (§5-1 · RCA-08) · 결정표 (§5-7)
  · 차단 표지 = 닫힌 집합 (§5-6a · RCA-10) · 보고 범주 `ASSUMED_UNVALIDATED` · §7-1 문장 = 판정문 §5-3 문안
  · SV 반사실 (CJUNC_SV_CF · 계획 범위 · 비 > 문턱 = `SV_DEPENDENT` · 못 읽음 = `SV_UNCHECKED` · 옛 `SV_DOMINANT` 철회 · RCA-06) —
    사슬은 비 · 상태만 읽는다 (끊는 면의 정의 무관 · PRE-impl-04 · `ca_ext_svcf.chain_view`) · ★ 10-22 (사전 리뷰 2 회차 PRE2-impl-01 ·
    1저자 Q1 (다)) 괄호 판정 — 모서리마다 아래 끝 (못 가른 덩어리 그대로) > 문턱 = `SV_DEPENDENT` · 두 끝을 읽고 위 끝 (덩어리를 통째로 뺀 판)
    ≤ 문턱 = 표지 없음 · 걸침 · 못 읽음 = `SV_UNCHECKED` (`sv_assess`) · ★ 10-23 (Codex 재검토 RCA2-01 · 1저자 Q1 (가)) 두 끝 = 증서 구간
    (아래비 = 주 해 증서 하한 / 아래 끝 증서 상한 · 위비 = 주 해 증서 상한 / 위 끝 증서 하한 · nominal 비 = 기록만) · 증서 없는 진단 기록 =
    `SV_UNCHECKED`
  · 감도 단계 = 주 판정 단계 (사다리 둘 · 예측) 가 끝난 뒤에만 (`--after-main` · 판정이 묶음을 대조 · Q-F)
★ 4판 (10-21 · DQ · 등록 R 4판 · 1저자 10-21 Q1 · Q2 "권고대로"):
  · Q1 (§5-0 ①–③ · §4-2 ③ · R4-Q5) 단락 (ELECTRODE_SHORT · J11) = 생산자 미게시 → 그 런 = NOT_COMPUTED (사유 = 상태 이름 ELECTRODE_SHORT) —
    +∞ 로 판정에 오지 않는다 · 이 등록의 풀이 상태 = POSITIVE_SOLVED · VALID_ZERO_TOPOLOGY · NOT_COMPUTED 셋 (`registration_state`) ·
    예측 단계의 NOT_COMPUTED = 등록 결과 (사다리와 같은 뜻 · 판정이 원 팔에서 다시 계산) · 판정 기록 `reasons` = 단계 · 법칙 · 사유
  · Q2 (규칙 여섯) — ① §3-2c 이름 우선순위 (하나라도 NOT_COMPUTED 면 NOT_COMPUTED · PRE-design-08 · `judge_set`) ② §3-2b ③″ 보호 띠
    (판독 [σ(1 − e), σ(1 + e)] · e = 그 런 증서 ⓓ 보장 오차 `target_err_bound_rel` (read_run 이 증서 구간에서 `step3_conv_cert.target_judge` 로
    다시 계산 · 팔 기록 `err_rel`) · 걸치면 보수 쪽 — 끝 = 바깥으로 · EDGE = EDGE · `outside_band` · `edge_hit` · PRE-design-12) ③ §4-2 origin
    상태 다름 = 넘음 · W ∈ {+∞, 0} → W₊ (`dbe_origin_ok` · PRE-design-10) ④ §5-5b 결정표 (오른쪽 칸 · 점 구간 · ⑰ 감도 미완료 · ⑱ ·
    `decide_sentence` · 표지마다 사유 `blocking_reasons` · PRE-design-09) ⑤ §5-6 변이 표지 (NOT_COMPUTED · 변이 자신의 CALIB_ORIGIN_SENSITIVE
    → <V>_UNCHECKED · `variant_flag` · PRE-design-17) ⑥ §7-1 한정어 ⑰ ⑱ (`QUALIFIERS` 18)
  · ★ RI (10-21 · §5-6 ③ "변이 판정 = NOT_COMPUTED (… 멈춤) → <V>_UNCHECKED" · 1저자 Q2 범위 = 코드를 등록에 맞춤) — 감도 변이 단계가 멈추면
    (STOPPED) 그 변이 판정 = NOT_COMPUTED → <V>_UNCHECKED (차단 · 주 판정은 그대로 계산 · `variant_stage_stopped`) · 주 판정 단계의 멈춤 = 판정
    전체 NOT_COMPUTED (INPUT_STAGE_STOPPED · `stopped_stage_rejects_verdict`) · 판정 입력 검사는 멈춘 변이 단계에도 그대로
★ PF2 (10-22 · 사전 리뷰 2 회차 · 1저자 10-22 Q1 (다) · Q2 · Q3 권고대로):
  · B (PRE2-design-01 · Q2) — 순서 = S0 단계 1 → ⑥ 숫자 탐침 (SBE · σ 봉인) → 계획 하나 봉인 → S0 단계 2 (DBE) → R 런.  사다리가
    `--s0-stage2-report` (단계 2 보고) 의 봉인 계획 해시 (`plan.r_plan.sha256` = R 계획 · `plan.sha256` = S0 계획) 를 지금 두 계획과 **정확히**
    대조 · 다르면 멈춤 (`S0_REPORT_MISMATCH`) · 예측 · 판정은 요약 기록으로 같은 함수 (`s0_stage2_problem`) 로 다시 대조
  · D (PRE2-design-02 · 08 · 탐침 C · 결정 없음) — 단계 요약 `code` = git 신원 (HEAD · 추적 파일 수정 여부 dirty) + 코드 파일 지문
    (`CODE_FILES` 12 · 사슬 폴더 · 러너 폴더 · 러너 sha256) · 다음 단계 (예측 · 감도 `--after-main` · 판정 계산기) 가 지금과 대조 · 다르거나 dirty =
    멈춤 (`CODE_PIN_MISMATCH` · 옛 = HEAD 만 · 같은 HEAD 의 dirty · 판정 문턱 한 줄을 못 막았다) · 사다리가 `--s0-stage1-report` (S0 단계 1 보고 ·
    그 보고가 만든 S0 계획 = `--s0-plan`) 와 단계 2 보고의 census · registry 일곱 파일 지문 (`S0_SAME_FILES` · 등록 R §2-1b) = 지금 R 런 코드인지
    대조 (다르면 멈춤 · s_min 다시 고르기 금지 문장 `S0_RERUN`) · `--machine` = 기계 이름표 (C · Q3 · 기록만 · 판정에 안 씀)
★ 10-25 묶음 B (Codex 재검토 RCA2-02 · 판정문 §4 F1 · F2 · §9 F5 · C6 #12 · #13 · #14 · 1저자 10-23 Q2 (가) (가-1) · Q9 설계 개정 4 R4-10 · R4-12):
  · 같은 코드 — git 두 조회 (rev-parse · status) 의 종료코드 · HEAD 40-hex · dirty 엄격한 False (조회 실패 · git 밖 = 미확인 = 멈춤 · False 로
    바꾸지 않는다) · ignore 밖 추적 안 된 파일 = dirty · 한 단계 안 사슬 ↔ 러너 (HEAD · 코드 파일 지문 · 러너 파일) · 코드 키 = 저장소 상대
    경로 (절대 경로 뺌 · 경로만 다른 두 체크아웃 = 같은 키) · 대조 파일 18 (Codex 가 짚은 모듈 6 더함) · 환경 지문 (같음 단위 = python 부 판 ·
    numpy · scipy 판 · 나머지 = 기록만 · 판정 계산기 프로세스 = 대조 안 함 R4-11) → `CODE_PIN_MISMATCH` (`git_identity` · `code_dirty_problem` ·
    `code_key` · `env_record` · `code_verdict_problem`)
  · F5 — S0 단계 2 보고의 계획 출처 = commit:<40-hex> + 그 커밋 안 R 계획 blob sha256 = 계획 sha256 → `S0_REPORT_MISMATCH` (`plan_commit_problem`)
  · 같은 침대 (RCA2-03 · 판정문 §4 F8 · 1저자 10-23 Q3 (가)) — S0 보고 (schema v3) 의 원 입력 (역할 파일 sha256 · 크기 · metrics 상자 · 두께 ·
    설정 = 킷 run_mpm.sh 의 payload 호출부) · 파생 칸 (규약 · off 격자 지문) 을 단계 요약에 보존 · R 직전 (사다리 = SBE · 예측 = SBE · DBE) ·
    판정 (`--root` 필수 · 다시 판정 포함) 에 S0 와 같은 발견 함수 (`ca_s0_census.kit_input_record`) 로 킷을 다시 해시해 대조 (경로 = 대조 밖 ·
    기계마다 자기 사본) · 같은 규약 arm 0 의 sid 지문 = S0 off 격자 지문 (`s0_grid_seed` · read_run) · 다르거나 못 읽음 = `S0_REPORT_MISMATCH`
    (재압밀 · 재생성 침대 = 새 S0) · 단계끼리 S0 기록 대조 = 경로 뺀 칸 (`s0_records_key`)
  · X6 (2 차 사전 공격 §A · 1저자 10-23 Q20 (가)) — S0 단계 2 보고 (schema v4) 의 봉인 SV census (R arm 0 와 같은 함수 `carbon_junction._sv_split` ·
    같은 격자 · 같은 문턱 `ca_ext_cjunc.registry_thresholds` · 봉인 s_min) 를 같은 규약 DBE arm 0 의 SV 기록마다 (기록 census 사본 + 증거 census ·
    세 칸) 대조 (`sv_census_problem` · `s0_census_seed`) → `S0_REPORT_MISMATCH` · census 외부 결합만 (끝 증서의 그래프 지문은 이 범위 밖)
★ 10-26 묶음 B6 (Codex 회차 ① RR1-01 · 1저자 10-26 Q1 · Q2 (가) · author 10-23 ratified Q2-Q3 Q20-Q21 (bundle B 10-25)) 끝 증서의 가중 그래프 귀속:
  · read_run — SV 기록 밖 봉인 원천 (`SV_GRAPH_SOURCE` · 같은 런의 raster · 원장 · 계획 · 등록 절단 규칙에서 솔브 없이 다시 조립한 끝 그래프 지문 ·
    `step3_sigma.solve_sigma_z(cjunc_graph_only=True)`) ↔ 증서 지문 (`ca_ext_svcf.graph_problem` · `sv_graph_state`) → 다르면 `CA_EXT_RECORD` · 원천 없음 ·
    원천 실패 = 미확인 (멈춤 아님) · 기록의 주 해 증서 사본 지문 = 이 런 주 증서 (`_mis`)
  · 판정 (`sv_assess(require_graph=True)`) — 증서 구간 SV 기록인데 그래프 귀속이 확인되지 않은 모서리 = 판정 입력 아님 → `SV_UNCHECKED` (clear · 의존
    아님 · 자기 신고 사본끼리 비교로 대신하지 않는다) · 판정은 단계 요약의 대조를 믿지 않고 원 팔을 다시 읽어 대조한다
  · ~~⚠ 생산 원천 = 아직 없음 (`SV_GRAPH_SOURCE` None · ⬜ 결정 필요) — 그 전까지 증서 구간 SV 모서리는 늘 `SV_UNCHECKED`~~
★ 10-26 B″ (1저자 10-26 Q1 (가) · 묶음 B 보고 §13 결정 1) 생산 봉인 원천 = 러너 조립만 (`RunnerGraphSource` · 기본 `SV_GRAPH_SOURCE` =
  `RUNNER_GRAPH_SOURCE`): SV 기록을 실은 런마다 같은 러너 · 같은 킷 · 같은 런 env (`runner_env_delta` · 사본 없음) + `CJUNC_GRAPH_ONLY=1` → payload
  `--step3-cjunc-graph-only` (같은 인자로 조립만 · 솔브 없음) → `cjgraph_<팔>.json` (`run_contract.cjunc_graph_only_problem`) → 환경 단위 = 사슬 ·
  결합 = 그 런 주 증서 결합 · 지문 → `ca_ext_svcf.graph_problem`.  예측 · 판정 · 다시 판정이 **각자 다시 조립한다** (단계 요약 · 생산자 옆 파일을 믿지
  않는다) · 원천 실패 (러너 rc · 출력 꼴 · 환경 · 결합 · 지문 없음 · 시간) = 미확인 (`SV_UNCHECKED`) · 원천 런 기록 (rc · 시간 · 최대 RSS) = 요약
  `sv_graph_source` · 판정 `verdict_graph_src.json` (판정 JSON 밖 — 다시 판정 바이트 대조 무관) · ⚠ 한정 (Q2) = 증서 칸 지문까지 원천 값으로 고친
  편집은 여전히 못 가린다 · ⚠ 한정 = 같은 러너 · payload · 킷이라 그 코드 · 킷 자체의 결함은 원천도 같이 갖는다 (코드 · 침대 대조 = 단계 관문)
★ 10-27 묶음 C1a (Codex 재검토 RCA2-05 · 판정문 C6 #15 · #30 · 수정 계획 Q4 (가) · Q9 설계 개정 4 Q3 · author 10-27 approved bundle C):
  · 계획 `rint-r-plan-v3` = v2 칸 + 실행 정책 `exec_policy` (같은 계획 sha256 봉인 안) — 값 칸 넷 (시간 상한 `max_hours` · 최대 시도 수
    `max_attempts` · 허용 기계 `allowed_machines` · 판 `env_unit` = python 부 판 · numpy · scipy) = null 이면 ⬜ (`PLAN_NUMBER_UNREGISTERED` · 숫자를
    사슬이 고르지 않는다) · 규칙 칸 넷 = 이 사슬이 구현한 규칙 이름 (`EXEC_POLICY_RULES` · 다르면 PLAN_INVALID) · 옛 v2 계획 = PLAN_INVALID
  · `--max-hours` = 계획 값 (다르면 NOT_REGISTERED) · `--machine` = 사다리 · 예측 필수 (없음 = 인자 오류 rc 2 · 목록 밖 = `MACHINE_NOT_ALLOWED`) ·
    런 기록마다 기계 이름 (판정 = 단계 기계 · 런 기계 · 허용 목록 대조) · 환경 지문 같음 단위 = 계획 봉인 판 (다르면 `CODE_PIN_MISMATCH` · 판정도)
  · 문서 숫자 — 등록 R 의 계획 숫자 블록 (`plan_doc_block` · 표지 `PLAN_DOC_BEGIN` · `PLAN_DOC_END`) = 계획 JSON 에서 생성 · 사다리 · 예측 · 판정이
    정확히 대조 (`plan_doc_problem` → `PLAN_DOC_MISMATCH`) · 생성 · 대조 CLI `--stage plan-doc` · 블록이 없는 등록 (봉인 전) = R 진입 거부
★ 10-27 묶음 C2a (Q9 설계 §2-1 · §2 · 개정 3 질문 4 · 개정 4 R4-06 · 개정 5 ①): SBE c 1 no-op = 사다리 단계 끝 (`ladder_noop` · 같은 사슬 부모가
  동결한 실행 환경 · 런마다 새 러너 자식) · 예측은 사다리 요약의 no-op 기록 · 런을 다시 읽어 (`noop_check`) 첫머리에서 옛 이름으로 · 예측 순서 = 모서리 →
  same_p → W0 → origin 표본 전부 → (넘침이 있으면) 이른 단조 (`checks['r_monotone_early']`) → 넘침 origin8 → 끝 단조 (그대로)
★ 10-27 묶음 C2b (Q9 설계 개정 4 Q2 · R4-02 ⓐ ⓑ ⓒ · Codex 회차 ① ② · 개정 5 ②): 러너 = 새 프로세스 그룹 (`run_in_group` · env 그룹 표지 ·
  `<단계>/groups/<런>.launch.json` · `.end.json`) · 시간 초과 · 신호 · 예외 · 스스로 끝난 뒤에도 그룹 전체를 죽이고 종료를 확인한 뒤에만 팔을 읽는다
  (확인 못 함 = `GROUP_UNCONFIRMED`) · 러너 시도 꼴 P2_ATTEMPT=1 (payload = 런 폴더 안 `.unchecked/` · 감싸개 `rint_first_result.py` = 첫 풀이 끝 표지) ·
  사슬 부모가 죽은 뒤 = `--stage recover --out <폴더>` (끝 기록 없는 그룹 · 호스트 규칙 · 미확인 = rc 3)
★ 10-27 묶음 C1b (RCA2-05 · Q4 (가) · Q9 설계 §3-2 · §3-4 · §3-5): 시도 원장 (`--stage ledger --init · --add` · 실행 트리와 다른 git 저장소 · 덧붙이기만 ·
  항목 = 시도 전에 커밋) · 시도 꼴 (`--ledger · --attempt n` · 폴더 <--out>/attempt_<n> · 풀기 전 대조 = 거부 기록 + 결과 줄 · 끝 = 그룹 확인 뒤 결과 줄) ·
  채택 (`adoption` · 처음 결과 전이 아닌 시도 + 재실행 사슬) · 원장 예측 (사다리 입력 = 채택 시도) · 원장 판정 (`ledger_verdict_check` · 판정 칸 ledger) ·
  `--stage recover --ledger` = 결과 줄 확정 · 한정 = 원장 안 시도끼리만 (그림자 런 · 모든 사본 일관 편집은 못 막는다 · Codex Q-D) · ★ C1b-2 재실행
  (`--add --resume <원 시도>` · `ResumeRunner` = 사슬 끝 시도 폴더의 끝난 런 복사 · 멈춘 런부터 새로 · 남은 payload 바이트 대조 = RESUME_MISMATCH · 없으면
  결정성 가정 = Codex Q-J 한정)
★ 10-27 묶음 C2d (Q9 설계 §3-1 – §3-5 · §4 · 개정 1–5 · Codex 회차 ① Q-A · Q-B · Q-D · Q-I · Q-L · author 10-27 approved bundle C) 12 단위 · 합치기:
  · 단위 = (c · 법칙 · R) 12 (`UNIT_RE` · 원장 대상 unit[:<변이>]:<이름>) · 단위 시도 (`--unit`) = 모서리 arm 0 (SV 반사실 = 예측과 같은 범위) + origin 표본
    (런 이름 U01_corner · U02_origin · `unit_summary.json` · UNIT_DONE) · 넘침 점 (`--point --expand <결정 기록>`) = origin8 (U01_origin8 ·
    `point_summary.json` · POINT_DONE · 풀기 전 대조 = 결정 기록의 점 · 사다리 · 계획 · 원장 조상) · 시도 하나 = 단위 · 점 하나 (CLI 단수)
  · 합치기 (`--merge <시도 폴더 · 바탕 …> --ledger`) = 같은 판정 함수 (`Predict`) · 같은 요청 순서 · fetch = `MergeFetch` (대상을 처음 요청할 때 그 대상의
    원장 대조 · 채택 · 출처 → 시도 폴더 사본 `units/<대상>/attempt_<n>` → 같은 `read_run`) · 런 이름 = 사슬 차례 · 부분 채택 (멈춤 = 그 런 요청 때) ·
    첫 합치기 넘침 = `EXPANSION_NEEDED` (rc 4 · `merge_summary.json` · 결정 기록 `expansion.json`) · 끝 합치기 (`--expand`) = 결정 기록 구조 칸 대조
    (넘침 목록 · 단위 시도 sha 집합 · 원장 접두) · 끝까지 간 뒤 남는 채택 런 = `UNIT_EXTRA` · 요청됐는데 없음 = `UNIT_MISSING` · 출처 다름 =
    `UNIT_PROVENANCE_MISMATCH` · 요청되지 않은 시도 · 대조 결과 = `merge.unused_runs` (기록만) · 원장 사본 = `ledger/ledger.bundle`
  · 판정 = 합친 예측은 원장 판정만 (`merged_ledger_check` = 같은 대조를 다시) · ⚠ 한정: 이전 사슬과 모든 멈춤 우선순위가 같다고 쓰지 않는다 (Codex Q-I) ·
    원장은 원장 안 시도끼리만 (그림자 런 · 모든 사본 일관 편집 = 못 막는다 · Q-D) · 기계마다 비트 차 = 칼날 (판정 보장 아님 · Q-G)
★ 10-27 묶음 C2e (Q9 설계 개정 5 ③ · Codex 회차 ① ③): 판정 = 판정 프로세스 환경 옆 파일 (`verdict_env.json` · 판정 JSON 밖) · 다시 판정 = 바이트 대조 그대로
  (구조 대조가 같아도 최종 등급이 다르면 REVERIFY_DIFF · 약화 · 덮어쓰기 · 유리한 쪽 고르기 없음) + 보고 (원 · 다시 계산 등급 · 다른 공개 칸 · 다른 결과 칸 이름 =
  값 봉인 · 원 · 지금 환경 · 다른 환경 칸 · `--out <새 폴더>` = `reverify_report.json`)
"""
import argparse
import glob
import hashlib
import json
import math
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import run_contract as RC                                    # noqa: E402 — 계약 정본 (사본 없음)
import ca_ext_svcf as SVCF                                   # noqa: E402 — SV 반사실 증거 꼴 (비 · 상태 · numpy 없음)

#: ★ 10-26 묶음 B6 (Codex 회차 ① RR1-01 · 1저자 10-26 Q2 (가)) SV 끝 그래프 봉인 원천 — `RUNNER_GRAPH_SOURCE` (생산 기본) | 호출 가능 (ctx →
#   `ca_ext_svcf.GRAPH_SOURCE_KEYS` 꼴 dict · 시험 · 대체 원천) | None (원천 없음 → 증서 구간 SV 기록 = 그래프 귀속 미확인 → 판정 `SV_UNCHECKED`).
#   ctx = {'req' (런 요청 · 킷 · R_j · 법칙 · c …), 'arm' (팔 번호), 'file' (팔 JSON 경로), 'outdir', ★ 10-26 B″ 'plan' (R 런 계획 · 런 env),
#   'bind' (그 런 주 증서의 결합 칸 — 입력 정체성 · 지문 칸은 주지 않는다)} — 원천은 SV 기록의 지문을 읽지 않고 같은 런의 raster · 원장 · 계획 · 등록
#   절단 규칙에서 솔브 없이 다시 조립한다 (`step3_sigma.solve_sigma_z(cjunc_graph_only=True)` 의 `cjunc_graphs`).
#   ~~None (기본 · 생산 배선 전)~~ → ★ 10-26 B″ (1저자 Q1 (가)) 기본 = `RUNNER_GRAPH_SOURCE` — 단계 (사다리 · 예측 · 판정 · 다시 판정) 가 러너 · 킷
#   뿌리로 `RunnerGraphSource` 를 만들어 read_run 에 넘긴다 (단계가 원천을 안 넘긴 자리 = 원천 없음 = 미확인).
RUNNER_GRAPH_SOURCE = 'runner'
SV_GRAPH_SOURCE = RUNNER_GRAPH_SOURCE
#: ★ 10-26 B″ (Q1 (가)) 원천 런 — 러너 env 표지 (조립만) · 출력 이름 앞자리 (러너 `cjgraph_<팔 이름>.json` · 팔 JSON p2_* 밖) · 단계 폴더 안 자리
GRAPH_ONLY_ENV = {'CJUNC_GRAPH_ONLY': '1'}
GRAPH_ONLY_PREFIX = 'cjgraph_'
GRAPH_SRC_DIR = 'graph_src'
#: 그래프 귀속 미확인의 종류 (판정 사유 글)
SV_GRAPH_WHY = {'no_source': '봉인 원천 없음', 'source_failed': '봉인 원천 실패', 'absent': '대조 기록 없음'}

TOOL = 'rint_r_chain'
SCHEMA = 'rint-r-chain-v2'                                   # ★ 3판 — v1 (2판 규칙) 요약과 섞지 않는다
REGISTRATION_DEFAULT = HERE.parent / 'docs' / 'reviews' / 'rint_carbon_additive_registration_R_draft_20261020.md'

# ═════════════════════════ 등록 R 의 숫자 — 한 곳 · 이름 (값 = 등록 정본 · 시험 X05 가 문서와 대조) ═════════════════════════
TARGET_SBE_MS = 1.63                 # §0 · §3 — SBE DC 1.63 mS/cm (보정 표적 · 판정선 · 결과 보고 옮기지 않는다)
EXP_DBE_MS = 4.68                    # §0 · §5 — DBE DC 4.68 mS/cm (holdout · 판정에 한 번)
CUR_GEN_DBE_MS = 1.8877              # §5-2 — 현 세대 SBE 보정 모형의 DBE (G0 의 기준 · 보고에 나란히)
CUR_GEN_SIGMA_STAR_DBE = 2.618       # §1 · §8 — 현 세대 DBE σ*_VGCF S/cm (보고만 · 맞추지 않는다)
EXP_RATIO = 2.86                     # §0 — 실험 비 DBE/SBE (보고만)
G0 = math.log(EXP_DBE_MS / CUR_GEN_DBE_MS)   # §5-2 G0 = ln(4.68/1.8877) = 0.908
GRADE_INFORMATIVE_MAX = G0 / 2.0     # §5-2 W ≤ G0/2 = 0.454 = 정보 있음 (비교척도 · 신뢰수준 아님)
GRADE_WEAK_MAX = G0                  # §5-2 W ≤ G0 = 0.908 = 약함 · 넘으면 정보 없음
SENS_SHIFT_FRAC_G0 = 0.1             # §5-6 끝이 0.1 G0 (= 0.091) 넘게 움직이면 크기 보고
CONFIRM_TOL = 0.02                   # ±2 % — §3-1 EDGE · §3-2 확인 런 · §3-2b 끝 표적 T± = 1.63 × (1 ± 0.02)
E_MIN = CONFIRM_TOL / math.log(math.sqrt(10.0))   # §3-2 e_min = 0.02 / ln √10 ≈ 0.017 — ★ 3판: 국소 진단 (보고 · 멈추지 않는다)
TAU_MONO = 1e-3                      # §3-2 비단조 · §4-1 같은 P 일관 (ln σ 차 · 단위 불변)
NEIGHBOR_LOG10_MAX = 0.5             # §3-2 끼는 이웃 비 ≤ 10^0.5
LADDER_START_LOG10 = (4.0, 6.0, 8.0)  # §3-2 다음 점 {1e4, 1e6, 1e8} Ω
LADDER_EXT_LOG10 = 2.0               # §3-2 끼지 않으면 같은 쪽으로 ×100
MAX_CONFIRM = 2                      # §3-2 확인 런 최대 두 번
ORIGIN_SBE_MAX = 0.02                # §3-3 SBE arm 0 · 1 · 2 의 ln(max/min) ≤ 0.02 (R_j,0)
ORIGIN_DBE_FRAC_W = 0.1              # §4-2 DBE 모서리 · R 마다 arm 0 · 1 · 2 의 ln(max/min) ≤ 0.1 W
SIG_DIGITS = 3                       # §3-2 R_j,0 = 유효숫자 3 자리 (끝 = 반올림 없음 · §3-2b)

# ═════════════════════════ 런 규약 (등록 R §10 COMMON · 머리 줄 7 · §2) ═════════════════════════
SBE_KIT = 'kit_SBE_vgcf100'
DBE_KIT = 'kit_DBE_sdcp1um_vgcf100'
LAWS = ('P0', 'P1')                  # PTFE–접합 법칙 끝 (N2)
CS = ('0', '1')                      # SDCP 접점 c 두 끝 (N11)
LADDER_C = '0'                       # 사다리 = c 0 (SBE 에 SDCP 없음 · c 무관 → 예측 단계가 SBE c 1 비트 같음을 검사)
VOX_MAIN, VOX_GRID = 0.15, 0.125     # §9 격자 단계 = vox 0.125
VGCF_D_UM = 0.15                     # 직경 보존 기준 지름 (러너 D_REF · 설계 §1-2 #2 · #3)
FIBRE_BULK, FIBRE_BULK_DIV10 = 1e4, 1e3   # §2 Endo 흑연화 1e4 S/cm · FIBRE 감도 ÷ 10
ENV_FIXED = {'VOX': '0.15', 'SDCP_SPHERE_D': '0.30', 'PTFE_STAMP': 'face_alpha', 'BRIDGE_UM': '0.48',
             'SIGMA_AM_S_OVERRIDE': '0.0041', 'SIGMA_SDCP_OVERRIDE': '256.6', 'SIGMA_FIBRE_BULK': '1e4',
             'LEAN': '2', 'CJUNC': '1'}
MAN_FIXED = {'bridge_um': 0.48, 'sdcp_sphere_d_um': 0.30, 'sigma_am_s_S_cm': 0.0041, 'sigma_sdcp_S_cm': 256.6}
L_PAR_UM, R_PORT_UM = 0.30, 0.30     # §2-1 지금 고정 (물리 단위) — S0 계획 values_um.L_par · r_port 와 대조 (두 계획 대조)
VARIANTS = ('FIBRE', 'UNREG', 'GRID', 'SVORDER')   # §5-6 필수 감도
VARIANT_ENV = {'FIBRE': {'SIGMA_FIBRE_BULK': '1e3'}, 'UNREG': {'CJUNC_UNREG_LAW': 'fused'}, 'GRID': {'VOX': '0.125'},
               'SVORDER': {'SDCP_YIELD_VGCF': '1'}}
LIMIT_RJ = {'floor': 'inf', 'ceiling': '0'}   # §3-1 R_j → ∞ (바닥 · 간선 없음) · R_j → 0 (천장 · 정확 축약) — 러너 env 꼴
#: ★ Z3 — 극한 env → protocol · 영수증 요청의 표지 (정본 낱말 = `ca_ext_cjunc.RJ_LIMITS` · 시험 X07 이 대조 · 이 모듈은 numpy 없이 뜬다)
LIMIT_MARK = {'inf': 'inf', '0': 'zero'}
#: ★ Z3 — §3-3 · §4-2 origin 검사 팔 (러너 `ARM_LIST` · a0 = 앞 런의 값 그대로 · 다시 돌지 않는다)
ORIGIN_ARMS = (1, 2)
#: 러너 · 정본 check_arm 의 backend (등록 R §10 = GPU · 러너 기본값과 같다 — 사슬이 env 로 정한다 · 부모 셸 값은 지운다)
EXPECT_BACKEND = 'gpu'
LEAN2_PLAN = {'electronic': True, 'ionic': False, 'thermal': False, 'pore': False, 'collector': False}
LEAN2_RECEIPTS = {'electronic_main': ('applied', 'absent_geometry'), 'electronic_wetted': ('disabled',),
                  'electronic_bare': ('disabled',), 'ionic': ('disabled',)}   # 설계 §7 LEAN 표 (LEAN 2 · 양의 해)
#: ★ 3판 — R 런 계획 v2 = v1 칸 일곱 + 결과 전 등록 숫자 넷 (등록 R §3-2 점 수 상한 · §3-2b 역상 폭 상한 · §5-6 SV 반사실 문턱 · 범위)
#: ★ 10-27 묶음 C1a (RCA2-05 · author 10-27 approved bundle C) — v3 = v2 칸 + 실행 정책 `exec_policy` (같은 sha256 봉인 안 · v2 계획 = PLAN_INVALID)
PLAN_SCHEMA = 'rint-r-plan-v3'
PLAN_KEYS = ('schema', 'len_law', 'unreg_law', 's_min_um', 'tol_ff_um', 'step3_rtol', 'p2_extra',
             'max_ladder_points', 'calib_rj_ratio_max', 'sv_cf_threshold', 'sv_cf_scope', 'exec_policy')
#: ★ 10-27 묶음 C1a — 실행 정책 값 칸 (⬜ = null · 숫자 · 목록 = 봉인 때 1저자 · 사슬은 고르지 않는다 · 기본값 없음):
#   max_hours = 단계 · 시도 하나하나의 시간 상한 (`--max-hours` 가 같아야) · max_attempts = 같은 대상 최대 시도 수 · allowed_machines = 허용 기계
#   이름표 (`MACHINE_RE`) · env_unit = 환경 지문 같음 단위 ({python_minor · numpy · scipy} 판 문자열 · 풀기 전 대조 · Q9 개정 4 Q3)
EXEC_POLICY_VALUE_KEYS = ('max_hours', 'max_attempts', 'allowed_machines', 'env_unit')
#: ★ 10-27 묶음 C1a — 실행 정책 규칙 칸 = 이 사슬이 구현한 규칙의 이름 (BRIEF 묶음 C C1 · Q9 §3-5 · 바뀌면 이름을 바꾼다 · 다른 이름 = PLAN_INVALID):
#   retry_rule = 결과 전 멈춤 (첫 풀이 끝 표지 · 팔 payload 없음) 만 새 시도 · same_config = 계획 · 코드 · 침대 · 환경 지문 같음 ·
#   adoption = 원장 차례로 처음 결과 전이 아닌 시도 (+ 재실행 사슬) · attempt_dir = 시도 폴더 꼴 `attempt_<n>` (실패 시도 · 원 사유 보존)
EXEC_POLICY_RULES = {'retry_rule': 'pre_result_only_v1', 'same_config': 'plan_code_bed_env_v1', 'adoption': 'first_not_pre_result_v1',
                     'attempt_dir': 'attempt_<n>'}
EXEC_POLICY_KEYS = EXEC_POLICY_VALUE_KEYS + tuple(EXEC_POLICY_RULES)
#: ★ 10-27 묶음 C1a (판정문 C6 #30) — 등록 R 의 계획 숫자 블록 표지 (블록 = `plan_doc_block` · 정확 대조 = `plan_doc_problem`)
PLAN_DOC_BEGIN = '<!-- rint-r-plan-doc:begin v1 -->'
PLAN_DOC_END = '<!-- rint-r-plan-doc:end -->'
ENV_UNIT_VALUE_RE = re.compile(r'[A-Za-z0-9._+-]+')   # 판 문자열 (표 · 경로 글자 없음)
#: 결과 전 등록 숫자 (⬜) — 하나라도 null 이면 사슬이 멈춘다 (σ 런 전 · ★ Q-G: SV 문턱이 ⬜ 인 채로 DBE 단계에 가지 않는다)
PLAN_REGISTERED_NUMBERS = ('max_ladder_points', 'calib_rj_ratio_max', 'sv_cf_threshold', 'sv_cf_scope')
PLAN_NO_CAP = 'none'                 # calib_rj_ratio_max = 'none' — "상한을 두지 않기로" 를 등록한 값 (§3-2b ④ · 실제 양끝을 그대로 전파)
SV_CF_SCOPES = ('R_j0', 'all3')      # §5-6 SV 행 — DBE 네 모서리 × R_j,0 · × 세 R (⬜ 1저자)
PLAN_UNREG_MAIN = 'cut'              # 설계 §1-2 #12 — 주 cut · 감도 fused (UNREG)
S0_PLAN_SCHEMA = 'ca-cjunc-plan-v1'  # §2-1 · §10-2 ⑪ — S0 단계 1 계획 (`scripts/ca_s0_census.py` · 정본 = 그 모듈)
#: ★ PF2 B (10-22 · 사전 리뷰 2 회차 PRE2-design-01 · 1저자 Q2 권고대로) — S0 단계 보고 (`ca_s0_census` · `s0_stage<n>_<킷>.json`) 의 schema
#   (= ca_s0_census.SCHEMA · 시험 B09 가 대조 · 이 모듈은 numpy 없이 뜬다)
#   ★ 10-25 묶음 B (RCA2-03 · Q3 (가)) — v3 = 같은 침대 칸 (inputs.settings_sha256 · raster.sid_off_fp) · v2 보고 = 멈춤 (새 S0) ·
#   ★ v4 (X6 · Q20 (가)) = 단계 2 봉인 SV census (`sv_census` · 단계 1 = null) · v3 보고 = 멈춤
S0_REPORT_SCHEMA = 'ca-s0-census-v4'
#: ★ PF2 D (10-22 · 사전 리뷰 2 회차 PRE2-design-02 · 08 · 결정 없음) — 같은 판 대조 파일 = 등록 R · kgy 명령이 이름 댄 생산 파일 중 사슬 ·
#   러너 · payload · 증서 · 접합 · census · registry 쪽 (사슬이 부르는 계약 · SV 증거 · 판독 포함 · 시험 파일 · 재압밀 `mpm3d_compaction.py` 는
#   R 런이 돌리지 않아 뺐다).  단계 요약에 이름마다 sha256 (사슬 폴더 · 러너 폴더) 을 남기고 다음 단계 · 판정 계산기가 지금 지문과 대조한다.
#   ★ 10-25 묶음 B (RCA2-02 · 1저자 10-23 Q2 (가) ④ · 판정문 §4 F1) — Codex 가 짚은 모듈 6 을 더했다 (사슬 · payload · 접합 · 증서가 부르는
#   `ca_ext_cjunc.py` · `additives.py` · `se_material.py` · `lens_geometry.py` · `step4_dyn.py` · `rint_cycle_traj.py` — `se_material.py` ·
#   `lens_geometry.py` = 봉인 32 파일 → 읽고 해시만 한다 · 고치지 않는다) · 키 = 이 폴더 (저장소 상대 `rel` 폴더) 안 이름 (절대 경로 아님)
CODE_FILES = ('rint_r_chain.py', 'run_contract.py', 'ca_ext_svcf.py', 'sr01_stamp_compare.py', 'step3_conv_cert.py', 'carbon_junction.py',
              'ca_s0_census.py', 'ptfe_face_alpha.py', 'step3_sigma.py', 'mpm_webapp_payload.py', 'fibre_segment_raster.py',
              'sdcp_gain_vox015_8arm.sh', 'ca_ext_cjunc.py', 'additives.py', 'se_material.py', 'lens_geometry.py', 'step4_dyn.py',
              'rint_cycle_traj.py',
              'rint_first_result.py')      # ★ 10-27 묶음 C2b — payload 프로세스 안 첫 풀이 끝 표지 감싸개 (러너 시도 꼴이 부른다)
RUNNER_NAME = 'sdcp_gain_vox015_8arm.sh'     # 등록 R §10 (0) 의 러너 — 한 단계 안 러너 파일 = 사슬 폴더의 이 파일 (★ 10-25 · Q2 (가) ③)
#: ★ 10-25 묶음 B (RCA2-02 · Q2 (가) ⑤ · Q9 설계 개정 4 Q3 · R4-10) — 환경 지문의 같음 단위 (python 부 판 · numpy · scipy 판 문자열 정확히)
ENV_UNIT_KEYS = RC.ENV_UNIT_KEYS                             # ★ 10-26 B″ — 정본 = run_contract (payload 조립만 출력과 같은 칸 · 같은 이름)
#: 등록 R §2-1b — S0 단계 1 · 단계 2 · R 런의 census · registry 가 같은 코드여야 하는 일곱 파일 (S0 보고 `code.file_digests` 와 대조)
S0_SAME_FILES = ('ca_s0_census.py', 'carbon_junction.py', 'ptfe_face_alpha.py', 'step3_sigma.py', 'mpm_webapp_payload.py',
                 'fibre_segment_raster.py', 'sr01_stamp_compare.py')
#: 등록 R §10-4 결과 전 문장 3 (10-22 · PRE2-design-03 · 1저자 Q3) — 기계 이름표 = 실행자가 넣는 짧은 이름 (IP · 주소 금지 → 점 · 쌍점 · 빗금 ·
#   띄어쓰기 없는 낱말) · 단계 요약에 기록만 (판정에는 쓰지 않는다 · 단계끼리 코드 지문은 같아야 한다)
MACHINE_RE = re.compile(r'[A-Za-z0-9_-]+')
#: 러너가 읽는 env (부모 셸에서 물려받으면 지운다 — 사슬이 런마다 정확히 정한다 · 지운 이름은 요약에)
ENV_SCRUB_RE = re.compile(r'^(SIGMA_|SDCP_|PTFE_|CJUNC|STEP3_)')
ENV_SCRUB_NAMES = frozenset({'VOX', 'BRIDGE_UM', 'ARMS', 'ARM_LIST', 'KITS', 'OUTDIR', 'LEAN', 'FIBRE_STAMP', 'MPM_PERIODIC_SIGMA',
                             'P2_EXTRA', 'EXPECT_BACKEND', 'EXPECT_PROTOCOL', 'P2_SCR', 'P2_SELF', 'P2_ENV_GUARD_ONLY',
                             'P2_ATTEMPT', 'RINT_RUN_TOKEN'})   # ★ 10-27 묶음 C2b — 시도 꼴 · 그룹 표지 = 사슬이 런마다 정한다
ENV_FORBIDDEN = ('SIGMA_VGCF_OVERRIDE',)   # §10 — 있으면 멈춤 (지워서 넘어가지 않는다)
#: ★ 10-26 B″ (1저자 Q4 · 묶음 B 보고 결정 4) 러너 실행 환경 — 사슬이 런마다 러너에 준다 (부모 셸 값과 무관 · 물리 축 아님 · ENV_FIXED 밖):
#   MPM_NO_VENV=1 = 러너가 venv ($HOME/dem-venv · $SCR/../venv · $SCR/../.venv) 를 켜지 않는다 (VIRTUAL_ENV 가 빈 때의 자동 켜기) → payload 는
#   사슬 프로세스의 PATH 에서 python3 을 찾는다 (단계 요약 환경 지문 = 이 사슬 프로세스 · `env_record`).  ⚠ 한정: PATH 의 python3 = 사슬 인터프리터인지는
#   런마다 대조하지 않는다 (결정 4 의 '러너가 자기 환경을 기록하고 사슬이 대조' 안은 고르지 않았다 · kgy 명령 = dem-venv 를 켠 뒤 사슬) · 확인 = 시험
#   (`scripts/test_rint_r_chain.py` Y14 · `scripts/test_rint_r_chain_e2e.py` E11)
RUNNER_EXEC_ENV = {'MPM_NO_VENV': '1'}
#: ★ 10-27 묶음 C2b (Q9 설계 개정 4 Q2 · R4-02 ⓐ ⓒ · author 10-27 approved bundle C) 러너 시도 꼴 — 사슬이 런마다 P2_ATTEMPT=1 을 준다: 러너가 payload 를
#   처음부터 런 폴더 안 `.unchecked/` 에 쓰고 (킷 런 폴더 `$RUN` 에 payload 를 남기지 않는다) 검사 통과 뒤 런 폴더로 옮긴다 · 킷 payload 줄을 감싸개
#   (`rint_first_result.py`) 로 바꿔 payload 프로세스가 첫 σ 직후 `.unchecked/<팔>.first_result.json` (첫 풀이 끝 표지) 을 쓴다
ATTEMPT_ENV = {'P2_ATTEMPT': '1'}
UNCHECKED_DIR = '.unchecked'
FIRST_RESULT_SUFFIX = '.first_result.json'
#: ★ 10-27 묶음 C2b (R4-02 ⓑ · Codex 회차 ① ② · Q9 개정 5 ②) 러너 프로세스 그룹 — 런마다 새 세션 · env 그룹 표지 (`GROUP_TOKEN_ENV`) · 시작 · 끝 기록
#   (`<단계>/groups/<런>.launch.json` · `.end.json`) · 끝 기록 = 그룹 (표지) 이 다 끝났음을 확인한 뒤 · 대기 상한 = 구현 상수 (넘으면 미확인 · 결과 · 판정
#   숫자 아님 · 보고 "결정 필요")
GROUPS_DIR = 'groups'
GROUP_TOKEN_ENV = 'RINT_RUN_TOKEN'
GROUP_SCHEMA = 'rint-r-group-v1'
GROUP_GONE_WAIT_S = 30.0
GROUP_POLL_S = 0.05

# ═════════════════════════ 판정 이름 · 표지 · 문장 ═════════════════════════
CALIB_ORDER = ('CALIB_IMPOSSIBLE', 'CALIB_EDGE', 'CALIB_UNIDENTIFIED', 'CALIB_UNCONFIRMED', 'CALIB_NONMONOTONE',
               'CALIB_LADDER_EXHAUSTED', 'NOT_COMPUTED')   # §3-2c — 판정 전체 이름 (이 순서로 하나)
REGISTERED_OUTCOMES = frozenset(CALIB_ORDER)
GRADES = ('PASS_INFORMATIVE', 'CONSISTENT_WEAK', 'UNINFORMATIVE', 'GAP_ENVELOPE_ONLY', 'FAIL')   # §5-5 (계산기 상태 이름)
#: §7-1 (3판 · 판정문 §5-3 문안 그대로) — PASS_INFORMATIVE 이고 차단 표지가 하나도 없을 때만
SENTENCE_PASS = ('SBE 측정 한 점으로 각 법칙의 내부 접합 저항을 보정하였다. 사전에 고정한 시나리오와 보정 허용집합의 계산 결과를 이미 알려진 '
                 'DBE 측정값과 비교하였다. 모형 종류와 시나리오 방향은 해당 DBE 값 및 기존 빗나감을 알고 선정했으므로, 이 비교는 독립 '
                 'holdout 검증이나 접합 물성의 식별이 아니다.')
SENTENCE_WEAK = '넓은 시나리오 구간 안에 들었다'                                  # §5-5 CONSISTENT_WEAK ("예측했다" 금지)
SENTENCE_GAP = '어느 법칙의 허용집합에도 포함되지 않았으나 전체 envelope 에는 포함'   # §5-5 · 판정문 §5-3 (GAP_ENVELOPE_ONLY)
#: ★ 4판 (Q2-4 · 등록 R 4판 §5-5b 결정표 · PRE-design-09 · R4-Q7) — 칸 글자 (등록 표 그대로 · 시험 X05b · U07 이 문서 · 독립 조립과 대조)
SENTENCE_UNINF = '예측 주장 없음 (구간이 현 세대 빗나감보다 넓다)'                     # §5-5b UNINFORMATIVE (§5-5 표의 짧은 꼴 아님)
SENTENCE_FAIL = '빗나감 d · d/G0 · 방향 · §8 보고 (해석 금지 §8)'                      # §5-5b FAIL
SENTENCE_CALIB = '판정 없음 — 법칙별 이름 · 사유 · 바닥 · 천장 · e · 끝 후보 보고'      # §5-5b CALIB_*
SENTENCE_NC = '판정 없음 — 사유 (상태 · 멈춤 코드) 보고'                               # §5-5b NOT_COMPUTED (사슬 멈춤 포함)
SENTENCE_Q18 = 'P 는 두 끝만 등록했다 (사이 감쇠는 모형 밖)'                           # §5-1 · §7-1 ⑱ (GAP 문장에 붙인다)
SENTENCE_PASS_HELD = '계산기 판정 이름 `PASS_INFORMATIVE` · 차단 표지 {} — 판정 문장 보류'   # §5-5b PASS + 차단 표지 ({} = <목록>)
SENTENCE_BLOCKED = '(차단 표지 {})'                                                    # §5-5b 그 밖 + 차단 표지 ({} = <목록>)
SENTENCE_POINT = '점 구간'                                                             # §5-5b 점 구간이면 덧붙임 (p = null)
SENTENCE_SENS = '감도 미완료'                                                          # §7-1 ⑰ (감도 변이를 다 돌리기 전 결과 문장마다)
SENTENCE_JOIN = ' · '                     # 덧붙임 · <목록> 의 이음 (★ 구현 꼴 — 등록 문장은 이음 글자를 정하지 않았다 · 보고 "결정 필요")
VERDICT_NOTE = ('판정 이름 (PASS_INFORMATIVE · CONSISTENT_WEAK · …) = 계산기 상태 이름 — 과학적 검증 성공이 아니다 · 독립 holdout 검증 아님 '
                '(등록 R §5-5 · §7-1 · 판정문 §5-3)')
GRID_SENTENCE = 'not_computed'       # §9 '격자 의존이 현 세대보다 작았다' — 현 세대 vox 0.125 대조는 이 사슬 밖 (그 문장 금지 · GRID 표지와 별개)
#: §5-6a — 차단 표지 **닫힌 집합** (이 목록 밖 이름은 차단하지 않는다 · 하나라도 있으면 §7-1 문장 금지 · 판정 이름은 그대로)
BLOCKING_FLAGS = ('FIBRE_SENSITIVE', 'UNREG_SENSITIVE', 'GRID_SENSITIVE', 'SVORDER_SENSITIVE', 'FIBRE_UNCHECKED', 'UNREG_UNCHECKED',
                  'GRID_UNCHECKED', 'SVORDER_UNCHECKED', 'CALIB_ORIGIN_SENSITIVE', 'SV_DEPENDENT', 'SV_UNCHECKED')
#: §5-6a — 보고 한정어 범주 (늘 붙는다 · 차단하지 않는다 · 미검증 사실을 지우지 않는다)
REPORT_CATEGORY = 'ASSUMED_UNVALIDATED'
ASSUMED_UNVALIDATED = ('ptfe_diameter_convention (DIA_UNCHECKED · Ø0.248 rope · 규약 선택)', 'sdcp_vgcf_contact_resistance_zero (SV 융합)',
                       'ptfe_impermeable', 'sdcp_cluster_fill_0.64', 'sdcp_am_attach_0.5')
#: §7-1 필수 한정어 ①–⑱ (⑨ = PTFE 지름 규약 = 보고 범주 ASSUMED_UNVALIDATED · ★ 4판 (Q2-6) ⑰ 감도 미완료 (§10-4 · 10-31 판정 = 주 판정만) ·
#  ⑱ P 는 두 끝 (P0 · P1) 만 등록했다 — 사이 감쇠는 모형 밖 (§5-1 · GAP_ENVELOPE_ONLY 는 이 선언에 달린다))
QUALIFIERS = ('Q1_holdout_known_one_sided', 'Q2_Rj0_model_internal', 'Q3_scenario_ends_not_material', 'Q4_two_electrode_n1',
              'Q5_grid_flag', 'Q6_sensitivity_flags', 'Q7_S1P_pellet', 'Q8_SV_contact_zero', 'Q9_ptfe_diameter_convention',
              'Q10_junction_geometric_proximity', 'Q11_s_min_development_choice', 'Q12_long_contact_distributed_v0',
              'Q13_sv_counterfactual_ratio_threshold', 'Q14_convergence_empirical_abcd_target_cert',
              'Q15_recompaction_generation_switch', 'Q16_calibration_set_outer_enclosure',
              'Q17_sensitivity_incomplete', 'Q18_P_two_ends_only')
#: §5-7 결정표 = ★ 4판 (Q2-4) 등록 R 4판 §5-5b 표 그대로 — 판정 이름 → (차단 표지 없음 칸, 차단 표지 있음 칸 꼴 · '{}' = <목록> (붙은 차단 표지
#  이름 전부 · 사전 순)) · CALIB_* · NOT_COMPUTED 의 차단 표지 칸 = "해당 없음" (None → 왼쪽 칸 그대로) · 점 구간 · ⑰ 덧붙임 = `decide_sentence`.
#  상태 (§5-0) 는 판정 이름을 통해서만 들어오고, 상태 ↔ 이름 짝은 STATE_VERDICTS 로 닫는다 (짝이 안 맞으면 구현 결함 = 예외).
_GAP_Q18 = SENTENCE_GAP + SENTENCE_JOIN + SENTENCE_Q18          # §5-5b GAP 칸 = 판정문 §5-3 문안 + ⑱
DECISION = {'PASS_INFORMATIVE': (SENTENCE_PASS, SENTENCE_PASS_HELD),
            'CONSISTENT_WEAK': (SENTENCE_WEAK, SENTENCE_WEAK + ' ' + SENTENCE_BLOCKED),
            'UNINFORMATIVE': (SENTENCE_UNINF, SENTENCE_UNINF + ' ' + SENTENCE_BLOCKED),
            'GAP_ENVELOPE_ONLY': (_GAP_Q18, _GAP_Q18 + ' ' + SENTENCE_BLOCKED),
            'FAIL': (SENTENCE_FAIL, SENTENCE_FAIL + ' ' + SENTENCE_BLOCKED),
            **{c: (SENTENCE_CALIB, None) for c in CALIB_ORDER if c != 'NOT_COMPUTED'},
            'NOT_COMPUTED': (SENTENCE_NC, None)}
STATE_VERDICTS = {'positive': frozenset(GRADES), 'point': frozenset({'PASS_INFORMATIVE', 'FAIL'}),
                  'extended': frozenset({'UNINFORMATIVE', 'GAP_ENVELOPE_ONLY', 'FAIL'}), 'calib': frozenset(CALIB_ORDER)}
#: ★ 4판 (10-21 · 1저자 Q1 "권고대로" · 등록 R 4판 §5-0 ①–③ · §4-2 ③ · R4-Q5) — 이 등록의 풀이 상태 셋 ↔ 생산자 기록 상태
#   (`run_contract.next_gen_state` · 정본): 단락 (ELECTRODE_SHORT · J11) = 생산자 미게시 (`run_contract.conv_cert_problem` — 게시 가능 =
#   POSITIVE_SOLVED · VALID_ZERO_TOPOLOGY 뿐) → 그 런 = NOT_COMPUTED · 사유 = 상태 이름 (σ +∞ 로 판정에 오지 않는다 · 다른 멈춤 이름
#   (RUNNER_RC · CA_EXT_RECORD …) 으로 흐리지 않는다 — 기록 자체는 온전해야 러너가 옮기고 사슬이 이 이름을 남긴다).
SHORT_STATUS = 'ELECTRODE_SHORT'          # = step3_conv_cert.STATUS_SHORT (시험 Z07 이 대조 · 이 모듈은 numpy 없이 뜬다)
REG_STATES = {'positive': ('POSITIVE_SOLVED', None), 'zero': ('VALID_ZERO_TOPOLOGY', None), 'short': ('NOT_COMPUTED', SHORT_STATUS)}
#: ★ 4판 (Q1) — 예측 단계의 등록 결과 (사다리의 REGISTERED_OUTCOMES 와 같은 뜻 · 판정이 원 팔에서 다시 계산한다) · 그 밖 멈춤 = STOPPED
PREDICT_OUTCOMES = frozenset({'NOT_COMPUTED'})


def stopped_stage_rejects_verdict(s):
    """★ RI (10-21 · 등록 R 4판 §5-6 ③ · 1저자 Q2 범위 = 코드를 등록에 맞춤) — 멈춘 단계 (STOPPED · 등록 결과 이름이 아닌 멈춤) 가 판정 전체를
    거부하나: **주 판정 단계만** (판정 전체 NOT_COMPUTED · INPUT_STAGE_STOPPED · §5-5 사슬 멈춤 행 그대로).  감도 변이 단계의 멈춤 = 그 변이 판정
    NOT_COMPUTED → <V>_UNCHECKED (`variant_stage_stopped` · 4판 사슬 = 변이 단계도 판정 전체 거부)."""
    return s.get('status') == 'STOPPED' and s.get('variant') is None


def variant_stage_stopped(s):
    """★ RI (§5-6 ③ "변이 판정 = NOT_COMPUTED (풀이 · 증서 실패 · 단락 · 멈춤) → <V>_UNCHECKED") — 멈춘 감도 변이 단계 (사다리 · 예측) = 결과 없음:
    원 팔에서 다시 계산하지 않고 그 법칙 · 예측 = NOT_COMPUTED (`judge_set` → 변이 판정 NOT_COMPUTED → `variant_flag` ③).  판정 입력 검사 (계획 ·
    S0 · 등록 숫자 · 코드 핀 · 주 예측 묶음 · 예측 ↔ 사다리) 는 멈춘 단계에도 그대로 (그 기록이 없으면 그 검사의 멈춤 = 판정 전체 NOT_COMPUTED)."""
    return s.get('status') == 'STOPPED' and s.get('variant') is not None

STOPS = {
    'OUTDIR_NOT_EMPTY': '출력 폴더가 이미 있고 비어 있지 않다 (러너 SKIP 캐시 · 옛 산출물)',
    'NOT_REGISTERED': '인자가 등록 R 과 다르다 (표적 · 법칙 · 킷 · 변이)',
    'ENV_SIGMA_VGCF_OVERRIDE': 'env 에 SIGMA_VGCF_OVERRIDE (복셀값 직접 · 다음 세대 판정 런 금지)',
    'REGISTRATION_UNREADABLE': '등록 문서 · §2-1 계획 해시 줄을 못 읽는다',
    'PLAN_HASH_UNREGISTERED': '등록 §2-1 계획 해시가 아직 없다 (⬜)',
    'PLAN_HASH_MISMATCH': '계획 해시 ≠ 등록 §2-1 개정값',
    'PLAN_INVALID': '계획 파일 꼴이 틀렸다',
    'PLAN_NUMBER_UNREGISTERED': 'R 계획의 결과 전 등록 숫자 (점 수 상한 · 역상 R 비 상한 · SV 반사실 문턱 · 범위) 가 아직 null (⬜) — σ 런 없음 (Q-G)',
    'S0_PLAN_INVALID': 'S0 계획 파일 꼴 · 식 · 정준 바이트가 틀렸다 (`ca_s0_census.check_plan`)',
    'S0_PLAN_HASH_UNREGISTERED': '등록 §2-1 S0 계획 해시가 아직 없다 (⬜)',
    'S0_PLAN_HASH_MISMATCH': 'S0 계획 해시 ≠ 등록 §2-1 개정값',
    'PLAN_CROSS_MISMATCH': '두 계획 대조 실패 (R 계획 ↔ S0 계획 ↔ 사슬 상수 · 등록 R §2-1 · §10-2 ⑪)',
    'S0_REPORT_MISMATCH': 'S0 단계 보고를 못 읽거나 꼴이 틀렸다 · 단계 2 보고가 봉인한 계획 해시 (R 계획 · S0 계획) ≠ 지금 계획 (★ PF2 B · Q2 — '
                          'DBE 열람 전 계획 하나 · 바꾸려면 새 등록 · 등록 R §2-1 · §2-1b · §11 ④) · (★ 10-25 묶음 B · 판정문 F5) 계획 출처 ≠ '
                          'commit:<40-hex> · 그 커밋의 R 계획 blob sha256 ≠ 계획 sha256 · (★ 10-25 묶음 B · RCA2-03 · Q3 (가)) S0 보고의 같은 '
                          '침대 칸 (원 입력 · 설정 · off 격자 지문) 꼴이 틀렸다 · S0 보고의 원 입력 ≠ 지금 킷 (R 직전 · 판정 때 S0 와 같은 발견 함수로 '
                          '다시 해시 · 경로 = 대조 밖) · 같은 규약 arm 0 의 sid 지문 ≠ S0 off 격자 지문 · 킷을 못 읽음 — 재압밀 · 재생성 침대 = 새 S0 · '
                          '(★ X6 · Q20 (가)) S0 단계 2 봉인 SV census 꼴 · s_min · tol_ff ≠ R 계획 · 같은 규약 DBE arm 0 SV 기록의 census 사본 · 증거 census '
                          '≠ 봉인 census',
    'MAIN_NOT_DONE': '감도 단계인데 주 판정 단계 (사다리 둘 · 예측) 가 끝나지 않았다 · 묶음이 다르다 (--after-main · Q-F)',
    'MAIN_BINDING': '판정 입력의 감도 단계가 묶인 주 예측 ≠ 판정 입력의 주 예측 (Q-F)',
    'KIT_MISSING': '킷 폴더 · 러너가 없다',
    'RUNNER_RC': '러너 rc ≠ 0',
    'REJECTED_MARKER': '러너 기각 기록 .rejected_*',
    'ARM_JSON_COUNT': '팔 JSON 개수 · 번호 · 이름 ≠ 요청',
    'ARM_UNREADABLE': '팔 JSON 을 못 읽는다',
    'ARM_CONTRACT': '러너 팔 계약 (check_arm) 실패',
    'GENERATION': 'physics_protocol_id 가 p3ca- 아님 (unknown:* 포함) · 저장 ≠ 다시 계산',
    'CA_EXT_RECORD': 'ca_ext_record_ok 실패',
    'MANIFEST_MISMATCH': '매니페스트 · 영수증 ≠ 요청 (σ · vox · 브리지 · PTFE · SDCP 구 · ca_ext 지문 · rtol · SV 반사실 요청)',
    'RECEIPT_LEAN': '솔브 영수증 ≠ LEAN 2 표 (설계 §7 · 해 상태별)',
    'PTFE_CELLS_OBSERVED': 'face_alpha 런의 ptfe_cells_observed > 0',
    'SID_GRID': 'sid 격자 지문이 같은 킷 · 같은 래스터 런 사이에서 다르다 (off 격자 대조)',
    'SAME_P_CONSISTENCY': '같은 P 일관 검사 위반 (SBE c no-op · DBE c 순서)',
    'R_MONOTONE_VIOLATION': '예측 — DBE 같은 모서리의 최종 추정량 (arm 0 · 8 팔 평균) 또는 이미 구한 origin 마다 (★ 10-23 사전 공격 리뷰 C3 · '
                            '1저자 Q13 (가)) σ(R_j,lo) ≥ σ(R_j,0) ≥ σ(R_j,hi) 와 증서 구간이 모순 '
                            '(★ 10-23 · Codex 재검토 RCA2-09 · 판정문 §8 · 1저자 Q8 (가) · 추가 풀이 없음 · 새 숫자 없음 · 구현 결함 의심)',
    'TIME_LIMIT': '시간 상한',
    'MACHINE_NOT_ALLOWED': '기계 이름표가 계획의 허용 목록 (exec_policy.allowed_machines) 밖 · 빈 이름 · 런 기록의 기계 ≠ 단계 기계 (★ 10-27 묶음 C1a · '
                           'C6 #15 · Q11 · Q9 §3-4)',
    'PLAN_DOC_MISMATCH': '등록 R 의 계획 숫자 블록 ≠ 계획 JSON 에서 생성한 블록 (없음 · 둘 · 값 다름 · 표지 하나만 · ★ 10-27 묶음 C1a · 판정문 C6 #30)',
    'GROUP_UNCONFIRMED': '러너 프로세스 그룹이 다 끝났는지 확인하지 못했다 (그룹 표지 프로세스가 대기 상한 안에 남음 · /proc 를 못 읽음 · ★ 10-27 묶음 C2b · '
                         'Codex 회차 ① ② — 그 런의 팔을 읽지 않는다 · 사람이 보고 --stage recover)',
    #  ★ 10-27 묶음 C1b (RCA2-05 · Q4 (가) · Q9 설계 §3-2 · §3-4 · §3-5 · §7 의 이름 · author 10-27 approved bundle C) — 시도 원장 · 시도 폴더
    'ATTEMPT_LEDGER_MISMATCH': '시도 원장 · 시도 폴더 대조 실패 (원장 꼴 · 같은 항목 결과 줄 둘 · 덧붙이기만이 아닌 역사 · 커밋 안 한 고침 · 폴더 요약 sha ≠ '
                               '결과 줄 · 원장에 없는 시도 폴더 · 결과 줄 없는 시도 · 채택 아닌 시도 입력 · 결과 전 · 뒤 기록 ≠ 폴더 · Q9 §3-5)',
    'ATTEMPT_ORDER_MISMATCH': '같은 대상 시도 차례 위반 (앞 항목 결과 줄 전에 다음 항목 · 시작 커밋이 원장 커밋의 조상이 아님 · 시작 커밋의 원장이 바이트 접두가 '
                              '아님 · 시작 커밋에 같은 대상 앞 결과 줄이 없음 · Q9 §3-5 개정 3 · R4-07)',
    'ATTEMPT_AFTER_ADOPTED': '채택된 시도 (결과 전이 아닌 첫 시도) 뒤 같은 대상의 새 시도 (풀기 전 거부 · 대조를 거치지 않고 돈 흔적 · Q9 §3-4 · R4-03)',
    'RESUME_NOT_ALLOWED': '재실행 자격 없음 (원 시도가 채택 · 재실행 사슬 끝이 아님 · 완주 · 자원 · 인프라 원인이 아님 · 검사 실패 흔적 · 기계 · 환경 지문 다름 · '
                          'Q9 §3-5 개정 4 · R4-08)',
    'ATTEMPT_LIMIT': '같은 대상 시도 수 > 계획 exec_policy.max_attempts (★ 10-27 묶음 C1b · C1 · 이름 = 구현 때 · 결정 필요)',
    'RESUME_MISMATCH': '재실행 payload ≠ 원 시도에 남은 payload (바이트 · 결정적 재실행이 아니다 · Q9 §3-5 · ★ 10-27 묶음 C1b-2)',
    #  ★ 10-27 묶음 C2d (Q9 설계 §3-2 · §3-4 · §7 의 이름) — 12 단위 · 넘침 점 · 합치기
    'UNIT_MISSING': '합치기 다시 계산이 요청한 단위의 채택 시도가 없다 · 그 시도에 요청한 런이 없다 (넘침 점이 없으면 상태 EXPANSION_NEEDED · Q9 §3-2)',
    'UNIT_EXTRA': '합치기 다시 계산이 끝까지 갔는데 채택된 단위 · 넘침 점 시도의 런이 남았다 (요청되지 않은 채택 런 · Q9 §3-2)',
    'UNIT_PROVENANCE_MISMATCH': '단위 · 넘침 점 시도의 출처 ≠ 합치기 (계획 · S0 · 코드 · 사다리 · 침대 · SV 범위 · 기계 · 요청) · 결정 기록 (꼴 · 점 · 사다리 · '
                                '원장 조상) · 끝 합치기 다시 센 넘침 목록 · 단위 시도 sha 집합 ≠ 결정 기록 · 점 시도가 인용한 결정 기록 sha ≠ (Q9 §3-2 · §3-4)',
    'DUPLICATE_RUN': '같은 킷 · 같은 계획 두 번',
    'INPUT_SHA_MISMATCH': '판정 입력 sha256 ≠ 런 산출',
    'INPUT_MISSING': '판정 입력이 모자란다',
    'INPUT_STAGE_STOPPED': '주 판정 입력 단계가 멈춘 채다 (감도 변이 단계의 멈춤 = 그 변이 <V>_UNCHECKED · §5-6 ③)',
    'INPUT_NOT_STAGE': '판정 입력 폴더에 단계 요약이 없다',
    'LADDER_NOT_CALIBRATED': '사다리가 보정되지 않았다 (예측 안 함)',
    'LADDER_SET': '사다리 묶음이 법칙 끝 둘이 아니다',
    'PREDICT_LADDER_MISMATCH': '예측이 쓴 사다리 ≠ 판정 입력 사다리',
    'REPLAY_MISMATCH': '원 팔 JSON 에서 다시 계산한 결정 ≠ 기록',
    'CODE_PIN_MISMATCH': '단계마다 코드 (사슬 · 러너) 가 다르다 · (★ PF2 D — PRE2-design-02 · 08) 코드 파일 지문 (sha256) ≠ 앞 단계 기록 · '
                         '추적 파일이 고쳐진 트리 (dirty) · R 런 코드의 census · registry 일곱 파일 ≠ S0 단계 1 · 2 보고 (등록 R §2-1b) · '
                         '(★ 10-25 묶음 B · RCA2-02 · Q2 (가)) git 조회 실패 · git 밖 (미확인) · ignore 밖 추적 안 된 파일 · 한 단계 안 사슬 ↔ 러너 '
                         '(HEAD · 파일 지문 · 러너 파일) · 저장소 상대 경로 · 환경 지문 같음 단위 (python 부 판 · numpy · scipy 판) 다름 · 미확인',
    **{k: k for k in CALIB_ORDER},
}


class Stop(Exception):
    """구조화 멈춤 — code (STOPS 이름) · cause (원인 칸 · σ 를 가린 문장) · run (그 런 이름) · ★ 4판 (Q1) reason = 구조화 사유 (등록 문장이
    이름을 정한 것만 — 지금 = 단락의 상태 이름 `ELECTRODE_SHORT` · 그 밖 None)."""

    def __init__(self, code, cause, run=None, reason=None):
        super().__init__(f'{code}: {cause}')
        self.code, self.cause, self.run, self.reason = code, str(cause), run, reason

    def record(self):
        return {'code': self.code, 'what': STOPS.get(self.code, self.code), 'cause': self.cause, 'run': self.run, 'reason': self.reason}


class RealContract:
    """정본 계약 위임 — 사슬은 이 계약을 다시 적지 않는다 (규율 ① · `run_contract` 머리말).  시험은 이 자리에 가짜 인지 계약을 넣는다."""

    def arm_problem(self, path, receipt):
        """러너가 팔을 OUTDIR 로 옮기기 전에 거는 검사와 같은 함수 (`sr01_stamp_compare.check_arm`) — 쓴 뒤 바뀐 팔을 다시 잡는다."""
        import sr01_stamp_compare as SC
        return SC.check_arm(path, 'segment', expect_backend=EXPECT_BACKEND, receipt=receipt)

    def ca_ext_record(self, man):
        return RC.ca_ext_record_ok(man)


# ═════════════════════════ 작은 도구 ═════════════════════════
def canon_bytes(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True, allow_nan=False) + '\n').encode('utf-8')


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def sha_mismatch(path, want):
    """판정 입력 sha256 대조 → 문제 | None (§10 멈춤 · 판정 단계 입력 sha256 ≠ 런 산출)."""
    try:
        got = sha256_file(path)
    except OSError as e:
        return f'{Path(path).name} 를 못 읽는다 ({type(e).__name__})'
    return None if got == want else f'{Path(path).name} sha256 {got[:12]}… ≠ 기록 {str(want)[:12]}…'


def sig3(x):
    """유효숫자 3 자리 (§3-2 R_j,0) → float."""
    return float(f'{float(x):.{SIG_DIGITS}g}')


def rj_key(x):
    """R_j → 러너 env · 요약 문자열 (정규 · 무손실 repr) · 극한 = 'inf' · '0'."""
    x = float(x)
    if math.isinf(x) and x > 0:
        return 'inf'
    if x == 0.0:
        return '0'
    if not (math.isfinite(x) and x > 0):
        raise ValueError(f'R_j {x!r}')
    return repr(x)


def rj_float(key):
    return math.inf if key == 'inf' else float(key)


def disp_rj(key):
    return {'inf': '∞', '0': '0'}.get(key) or f'{float(key):.4g} Ω'


def interp_lnln(Ra, sa, Rb, sb, target):
    """§3-2 ln σ ↔ ln R_j 직선 보간 → target 을 지나는 R_j (양의 유한 σ 끼리만 — 부르는 쪽이 거른다)."""
    t = (math.log(target) - math.log(sa)) / (math.log(sb) - math.log(sa))
    return math.exp(math.log(Ra) + t * (math.log(Rb) - math.log(Ra)))


def elasticity(Ra, sa, Rb, sb):
    """§3-2 할선 탄성 e = |Δ ln σ / Δ ln R_j| — ★ 3판: 국소 진단 (보고 · e/e_min) · 식별 판정이 아니다 (RCA-01)."""
    return abs((math.log(sb) - math.log(sa)) / (math.log(Rb) - math.log(Ra)))


def registration_state(state):
    """★ 4판 (Q1 · 등록 R 4판 §5-0) — 생산자 기록 상태 (`run_contract.next_gen_state` 의 첫 값) → (이 등록의 풀이 상태, 사유).
    positive → POSITIVE_SOLVED · zero → VALID_ZERO_TOPOLOGY · short → NOT_COMPUTED (사유 ELECTRODE_SHORT · 생산자 미게시) · 상태가 안 섬
    (None) · 모르는 상태 → NOT_COMPUTED (사유 None — 그 상태 문장은 멈춤 원인 칸에)."""
    return REG_STATES.get(state, ('NOT_COMPUTED', None))


# ── §5-0 확장 실수 [0, +∞] (0 = VALID_ZERO_TOPOLOGY) — 모든 비교 = ln 차 (단위 불변 · RCA-13) · ★ 4판 (Q1): 단락은 +∞ 로 판정에 오지 않는다
#    (NOT_COMPUTED) — 아래 도구는 +∞ 를 다룰 수 있게 둔다 (값 쪽 일반성 · 판정 입력으로는 0 만 온다) ──
def ln_diff(a, b):
    """ln b − ln a 를 확장 실수에서 — 같은 끝 (0·0 · ∞·∞) = 0 · 0 → 양 · 양 → ∞ = +∞ · 그 반대 = −∞."""
    a, b = float(a), float(b)
    if a == b:
        return 0.0
    if a == 0.0 or b == math.inf:
        return math.inf
    if b == 0.0 or a == math.inf:
        return -math.inf
    return math.log(b) - math.log(a)


def ln_spread(vals):
    """ln(max/min) 을 확장 실수에서 — 다 같으면 0 (0 · +∞ 끼리 포함) · 0 이나 +∞ 가 다른 값과 섞이면 +∞."""
    vals = [float(v) for v in vals]
    return ln_diff(min(vals), max(vals))


def mean_ext(vals):
    """산술 평균 (8 팔) — +∞ 가 하나라도 있으면 +∞ (빼기 없음 · NaN 없음)."""
    vals = [float(v) for v in vals]
    return sum(vals) / len(vals)


def outside_band(s, X, lo, e=0.0):
    """§3-2b 끝 조건 — lo 끝: σ ≥ T⁺ (허용집합 아래쪽 밖) · hi 끝: σ ≤ T⁻ (위쪽 밖) · 확장 실수 그대로.
    ★ 4판 (Q2-2 · §3-2b ③″ · PRE-design-12) 보호 띠 — 판독 구간 [σ(1 − e), σ(1 + e)] (e = 그 런 증서의 보장 오차 `err_rel`) 이 띠 바깥에
    **다 있을 때만** 바깥 (lo: σ(1 − e) ≥ T⁺ · hi: σ(1 + e) ≤ T⁻) · 걸치면 모호 = False (보수 쪽 — 끝을 바깥으로 옮긴다) · e = 0 = 3판 그대로."""
    return s * (1.0 - e) >= X if lo else s * (1.0 + e) <= X


def edge_hit(s, e, T, tol=CONFIRM_TOL):
    """§3-1 EDGE (1.63 이 바닥 또는 천장의 2 % 안 = |σ/T − 1| ≤ 2 %) — ★ 4판 (Q2-2 · §3-2b ③″) 보호 띠: 판독 구간 [σ(1 − e), σ(1 + e)] 에서
    T 에 가장 가까운 점이 띠 안이면 EDGE (구간이 T 를 품으면 EDGE · 걸치면 모호 = EDGE 로 센다 = 보수 쪽) · e = 0 = 3판 식 그대로 · 확장 실수
    (σ 0 = 바닥 zero 정상 · EDGE 아님)."""
    a, b = s * (1.0 - e), s * (1.0 + e)
    if a <= T <= b:
        return True
    x = b if b < T else a
    return abs(x / T - 1.0) <= tol


def arm_err(rec):
    """★ 4판 (Q2-2) — 팔 기록의 판독 보장 오차 e (`err_rel` · read_run 이 증서에서 다시 계산) → float (유한 ≥ 0) · 없으면 멈춤 (보호 띠를 잴 수
    없다 — 0 으로 두면 보수 쪽이 아니다)."""
    e = rec.get('err_rel') if isinstance(rec, dict) else None
    if isinstance(e, bool) or not isinstance(e, float) or not math.isfinite(e) or e < 0.0:
        raise Stop('ARM_UNREADABLE', f'판독 보장 오차 err_rel {e!r} — 유한 0 이상 float 이어야 (§3-2b ③″ 보호 띠 · 증서 ⓓ target_err_bound_rel)')
    return e


def arm_band(rec):
    """★ 10-23 (Codex 재검토 RCA2-09 · 판정문 §8 · 1저자 Q8 (가)) 팔 기록 → 증서 구간 (정확 분수 끝 둘) — ★ 10-23 (사전 공격 리뷰 C4 · author 10-23
    ratified Q12-Q16) 그 런 증서의 목표량 구간 [target_lo, target_hi] (코드 단위 = 아래 판 전류) 을 그 증서의 scale (게시 판 전류 × scale = 증서 σ ·
    계약 `run_contract._positive_cert_problem`) 로 σ 에 옮긴 정확 분수 [scale·target_lo, scale·target_hi] — read_run 이 증서에서 옮겨 싣는다 ·
    칸이 없거나 꼴이 틀리면 멈춤 `ARM_UNREADABLE` (옛 띠 [σ(1 − e), σ(1 + e)] = float e 라 증서 구간보다 좁을 수 있었다 · 그리로 되돌아가지 않는다) ·
    같은 origin 의 세 R 은 같은 침대 · 같은 래스터라 scale (판 간격 / 단면적 · `step3_sigma` · R_j 와 무관) 이 같다 → 그 비교 = 증서 전류
    구간끼리 그대로 · 게시 판 전류가 증서 구간 안이면 새 띠는 옛 띠 안에 든다 (반올림 크기 차이 제외) · 판독 보장 오차 `err_rel` 도 그대로
    요구한다 (`arm_err` · 0 으로 두지 않는다) · σ 0 (영값 위상 · e 0) = [0, 0] · 단락은 NOT_COMPUTED 라 여기 오지 않는다 (+∞ 없음)."""
    arm_err(rec)
    s = rec.get('sigma')
    if not (_num(s) and s >= 0):
        raise Stop('ARM_UNREADABLE', f'σ {s!r} — 유한 0 이상 수여야 (R 단조 띠)')
    if s == 0:
        return Fraction(0), Fraction(0)
    lo, hi, k = rec.get('target_lo'), rec.get('target_hi'), rec.get('scale')
    if not (_num(lo) and _num(hi) and _num(k) and 0 < lo <= hi and k > 0):
        raise Stop('ARM_UNREADABLE', f'증서 목표량 구간 [{lo!r}, {hi!r}] · scale {k!r} — 유한 수 · 0 < 아래 ≤ 위 · scale > 0 이어야 (R 단조 띠 = 그 런 '
                                     f'증서 구간 · 10-23 사전 공격 리뷰 C4)')
    k = Fraction(k)
    return k * Fraction(lo), k * Fraction(hi)


def mean_band(recs):
    """★ 10-23 (RCA2-09) n 팔 평균의 증서 구간 — 끝마다 평균 (팔마다 `arm_band` (★ C4 = 그 증서 구간 × 그 scale) 의 아래끝 합 / n · 위끝 합 / n ·
    정확 분수 · 참 평균은 그 사이)."""
    bs = [arm_band(r) for r in recs]
    return sum(b[0] for b in bs) / len(bs), sum(b[1] for b in bs) / len(bs)


def r_monotone_problem(pts):
    """★ 10-23 (Codex 재검토 RCA2-09 · 1저자 Q8 (가)) 같은 모서리 · 같은 origin · 같은 최종 추정량의 점 [(R, 이름, (아래끝, 위끝))] → 첫 모순 쌍
    (R 작은 쪽 이름, R 큰 쪽 이름) | None — 단조 = R 이 클수록 σ 는 크지 않다 (R_a < R_b ⟹ σ(R_a) ≥ σ(R_b)) · 모순 = 증서 구간끼리 그 순서가
    불가능 (R_a < R_b 인데 위끝_a < 아래끝_b · R 이 같은데 두 구간이 떨어짐) · 쌍 전부를 본다 (이웃 쌍만이 아니다) · 증서 띠 안에서만 겹치는 비단조
    = 모순 아님 (멈추지 않는다)."""
    for i, (ra, na, ba) in enumerate(pts):
        for rb, nb, bb in pts[i + 1:]:
            (r1, n1, b1), (r2, n2, b2) = sorted(((ra, na, ba), (rb, nb, bb)), key=lambda t: t[0])
            if r1 < r2 and b1[1] < b2[0]:
                return n1, n2
            if r1 == r2 and (b1[1] < b2[0] or b2[1] < b1[0]):
                return n1, n2
    return None


def final_band(pr, key):
    """★ 10-23 (RCA2-09) 모서리 · R 의 최종 추정량 (판정에 들어가는 값 = `Predict.values`) 의 증서 구간 → (구간, 'arm0' | 'mean8') — origin 규칙이
    바꾼 모서리 = 8 팔 평균의 구간 (세 R 전부 · 같은 8 origin 집합) · 아니면 arm 0 팔의 구간."""
    if key in pr.adj_band:
        return pr.adj_band[key], 'mean8'
    return arm_band(pr.vals[key]), 'arm0'


#: ★ 10-23 (사전 공격 리뷰 C3 · 1저자 Q13 (가)) 예측이 이미 구한 origin 의 이름 · 검사 순서 — 모서리 런의 arm 0 · origin 런의 팔 (`ORIGIN_ARMS`) ·
#: origin 규칙이 바꾼 모서리의 8 팔 런 팔 0–7 (그 모서리만 · 세 R 전부)
ORIGIN_NAMES = ('corner_a0',) + tuple(f'origin_a{i}' for i in ORIGIN_ARMS) + tuple(f'origin8_a{i}' for i in range(8))


def origin_points(pr, law, c):
    """★ 10-23 (사전 공격 리뷰 C3 · 1저자 Q13 (가)) 모서리 (c · 법칙) 의 이미 구한 origin 마다 세 R 점 → [(origin 이름, [(R, 역할, 증서 구간)])] —
    세 R 모두에 그 origin 이 있을 때만 (예측은 origin 런을 세 R 전부에서 · 8 팔 런을 넘친 모서리의 세 R 전부에서 돌린다) · 순서 = `ORIGIN_NAMES` ·
    구간 = `arm_band` (최종 추정량 검사와 같은 띠) · 추가 풀이 없음."""
    sets = [pr.org.get((c, law, rr)) or {} for rr in RJ_ROLES]
    return [(n, [(rj_float(pr.ladders[law][rr]), rr, arm_band(s[n])) for rr, s in zip(RJ_ROLES, sets)])
            for n in ORIGIN_NAMES if all(n in s for s in sets)]


def sbe_origin_ok(vals):
    """§3-3 SBE arm 0 · 1 · 2 → (통과?, ln(max/min)) — 확장 실수."""
    sp = ln_spread(vals)
    return sp <= ORIGIN_SBE_MAX, sp


def dbe_origin_ok(vals, W0, states=None, w_pos=None):
    """§4-2 DBE 모서리 · R 마다 arm 0 · 1 · 2 → (통과?, ln(max/min)) — 문턱 0.1 W (W = arm 0 값들로 낸 첫 폭).
    ★ 4판 (Q2-3 · §4-2 PRE-design-10 · R4-Q4) — ① 세 origin 의 상태 (`states` · POSITIVE_SOLVED ↔ VALID_ZERO_TOPOLOGY) 가 서로 다르면 = 넘음
    ② 상태는 같은데 W 가 +∞ (다른 모서리의 zero) 또는 0 (점 구간) 이면 문턱의 W = W₊ (`w_pos` = arm 0 의 양수 값들만으로 낸 폭 · 없으면 0) ·
    W₊ = 0 이면 문턱 0 (산포가 조금이라도 있으면 넘음 = 보수 쪽) ③ 단락 (ELECTRODE_SHORT) 은 NOT_COMPUTED 라 여기 오지 않는다."""
    sp = ln_spread(vals)
    if states is not None and len(set(states)) > 1:
        return False, sp
    W = W0 if (0.0 < W0 < math.inf) else (0.0 if w_pos is None else w_pos)
    return sp <= ORIGIN_DBE_FRAC_W * W, sp


def w_pos_of(vals):
    """★ 4판 (Q2-3 · §4-2 ②) — W₊ = arm 0 의 양수 값들만으로 낸 폭 ln(max/min) (양수 값이 없으면 0 · 하나면 0)."""
    pos = [float(v) for v in vals if float(v) > 0.0]
    return ln_spread(pos) if pos else 0.0


def _ln_dist(x, lo, hi):
    """x 에서 구간 [lo, hi] 까지 ln 거리 (안 = 0 · 유한 끝이 없으면 +∞) 와 방향 ('inside' · 'below' = x 가 아래 · 'above' = x 가 위)."""
    if lo <= x <= hi:
        return 0.0, 'inside'
    if x < lo:
        return (math.log(lo / x) if lo < math.inf else math.inf), 'below'
    return (math.log(x / hi) if hi > 0.0 else math.inf), 'above'


def grade_W(W):
    """§5-2 등급 (양의 구간 · 4.68 ∈ U) — W ≤ G0/2 정보 있음 · ≤ G0 약함 · 넘으면 정보 없음."""
    return 'PASS_INFORMATIVE' if W <= GRADE_INFORMATIVE_MAX else 'CONSISTENT_WEAK' if W <= GRADE_WEAK_MAX else 'UNINFORMATIVE'


def in_law_sets(I, x):
    """§5-1 3판 (RCA-08) — x 를 담는 법칙별 허용집합 I_P 의 법칙 목록 (U = ∪ I_P · envelope 가 아니다)."""
    return [law for law in sorted(I) if I[law][0] <= x <= I[law][1]]


def judge(vals, x=EXP_DBE_MS, ref=CUR_GEN_DBE_MS):
    """§5-0 – §5-5 판정 함수 (주 판정 · 감도 변이가 같은 것) — vals = {(c, 법칙, R 역할): σ} (같은 단위 · 확장 실수 0 (· +∞ = 도구만 ·
    ★ 4판 Q1 단락은 NOT_COMPUTED 라 판정 입력에 없다)) →
    법칙별 I_P · U = ∪ I_P · E (envelope) · 상태 (positive · point · extended) · 판정 이름 · W · p · d · 방향 · S.
    모든 비교 = ln (단위 불변 · x · ref 도 같은 단위 · RCA-13) · 등급 W = E 의 폭 (2판 그대로 · R3-Q5)."""
    G0x = math.log(x / ref)
    by_law = {}
    for (c, law, rr), v in sorted(vals.items()):
        by_law.setdefault(law, []).append(float(v))
    I = {law: [min(v), max(v)] for law, v in by_law.items()}
    allv = [float(v) for v in vals.values()]
    lo, hi = min(allv), max(allv)
    in_law = in_law_sets(I, x)
    inU, inE = bool(in_law), lo <= x <= hi
    ext = lo == 0.0 or hi == math.inf
    state = 'extended' if ext else ('point' if lo == hi else 'positive')
    W = math.inf if ext else (0.0 if lo == hi else math.log(hi / lo))
    if inU:
        verdict = 'UNINFORMATIVE' if ext else grade_W(W)
    elif inE:
        verdict = 'GAP_ENVELOPE_ONLY'
    else:
        verdict = 'FAIL'
    d, direction = _ln_dist(x, lo, hi)
    if inE and not inU:
        direction = 'gap'
    dU = min(_ln_dist(x, a, b)[0] for a, b in I.values())
    if state == 'positive':
        p, p_why = math.log(x / lo) / W, None
    else:
        p, p_why = None, ('point_interval' if state == 'point' else 'extended_interval (zero 끝 · W = +∞)')
    if ext:
        S, mid, S_why = None, None, 'extended_interval'
    else:
        mid = math.sqrt(lo * hi)
        S, S_why = 1.0 - abs(math.log(x / mid)) / G0x, None
    return {'verdict': verdict, 'state': state, 'interval_mScm': [lo, hi], 'I_law_mScm': I, 'in_law': in_law, 'in_U': inU,
            'in_E': inE, 'W': W, 'p': p, 'p_why': p_why, 'd': d, 'd_over_G0': d / G0x, 'direction': direction,
            'd_to_U': dU, 'S': S, 'S_why': S_why, 'sigma_mid_mScm': mid}


def grade(lo, hi):
    """한 법칙 · 두 값 구간의 판정 (보조 · 시험 V09) — judge 그대로 (U = E = [lo, hi])."""
    return judge({('0', 'P0', 'R_j_lo'): lo, ('1', 'P0', 'R_j_hi'): hi})


def decide_sentence(state, verdict, blocking, sens_incomplete=False):
    """§5-7 결정표 = ★ 4판 (Q2-4) 등록 R 4판 §5-5b — (상태, 판정 이름, 차단 표지 목록, 감도 미완료) → 문장 하나 (같은 레코드 = 같은 문장).
    차단 표지 없음 = 왼쪽 칸 · 있음 = 오른쪽 칸 (PASS = *"계산기 판정 이름 `PASS_INFORMATIVE` · 차단 표지 <목록> — 판정 문장 보류"* · 그 밖 =
    왼쪽 칸 + *"(차단 표지 <목록>)"* · <목록> = 붙은 차단 표지 이름 전부 · 사전 순) · 점 구간이면 *"점 구간"* · 감도 미완료 (⑰) 면 *"감도 미완료"* 를
    덧붙인다 · CALIB_* · NOT_COMPUTED = 판정 없음 칸 (차단 표지 · 점 · 감도 해당 없음).  짝이 안 맞는 상태 · 이름 · 닫힌 집합 (§5-6a) 밖 이름 =
    구현 결함 (ValueError) · 목록이 아닌 차단 표지 (bool · 문자열) · bool 아닌 감도 미완료 = TypeError."""
    if state not in STATE_VERDICTS or verdict not in STATE_VERDICTS[state]:
        raise ValueError(f'결정표 밖 — 상태 {state!r} · 판정 {verdict!r} (§5-0 · §5-5 짝이 아니다)')
    if not isinstance(blocking, (list, tuple)):
        raise TypeError(f'차단 표지 {blocking!r} — 이름 목록이어야 (bool · 문자열 아님 · §5-5b <목록>)')
    outside = [f for f in blocking if f not in BLOCKING_FLAGS]
    if outside:
        raise ValueError(f'차단 표지 닫힌 집합 (§5-6a) 밖 이름 {outside} — `blocking_of` 를 거친 목록이어야')
    if type(sens_incomplete) is not bool:                                   # noqa: E721
        raise TypeError(f'감도 미완료 {sens_incomplete!r} (bool 이어야)')
    left, right = DECISION[verdict]
    if right is None:                                    # CALIB_* · NOT_COMPUTED — 판정 없음 (예측 단계 전 · 해당 없음)
        return left
    s = right.format(SENTENCE_JOIN.join(sorted(set(blocking)))) if blocking else left
    if state == 'point':
        s += SENTENCE_JOIN + SENTENCE_POINT
    if sens_incomplete:
        s += SENTENCE_JOIN + SENTENCE_SENS
    return s


def blocking_of(flags):
    """§5-6a 닫힌 집합 — 이 목록 밖 이름 (예: 보고 한정어 DIA_UNCHECKED · 모르는 *_UNCHECKED) 은 차단하지 않는다."""
    return sorted(f for f in set(flags) if f in BLOCKING_FLAGS)


def _sv_readable(x):
    """SV 반사실 한 끝의 비를 읽을 수 있나 — float (bool 아님) · 유한 양수 또는 +∞ (★ PF2 E · `ca_ext_svcf._end_view` 와 같은 정의역)."""
    return isinstance(x, float) and not isinstance(x, bool) and (x == math.inf or (math.isfinite(x) and x > 0.0))


def sv_assess(recs, threshold, scope, require_graph=False):
    """§5-6 SV 행 (RCA-06 · Q4) — 모서리 런 (arm 0) 의 반사실 기록 → (표지, 모서리별 기록).
    비 > 문턱 (등록 문장 '넘으면') = `SV_DEPENDENT` · 기록을 못 읽음 (없음 · 비를 싣지 않는 상태 · 주 해가 0) · 문턱 없음 = `SV_UNCHECKED` ·
    읽는 칸 = 비 · 상태 (`ca_ext_svcf.chain_view` · 끊는 면의 정의 무관 · PRE-impl-04).  ⚠ producer 의 자기 표지 비교는 ≥ (그 배선의 문턱
    = 늘 None · 이 사슬은 쓰지 않는다).
    ★ 10-22 (사전 리뷰 2 회차 PRE2-impl-01 · 1저자 Q1 (다) · 등록 R §5-6 SV 행 개정) 괄호 판정 — 모서리마다 아래 끝 (`ratio` · 못 가른 덩어리
    그대로) · 위 끝 (`ratio_hi` · 그 덩어리를 통째로 뺀 판 · 덩어리 0 = 아래 끝과 같다): 아래 끝 > 문턱 = 의존 (위 끝과 무관) · 두 끝을 읽고
    위 끝 ≤ 문턱 = 표지 없음 · 두 끝을 읽었는데 아래 ≤ 문턱 < 위 = 걸침 · 그 밖 = 못 읽음 (위 끝 칸 없는 옛 기록 포함 · 아래 끝을 못 읽은
    모서리 = 위 끝 값과 무관하게 못 읽음 = 지금 방식) → 걸침 · 못 읽음 = `SV_UNCHECKED`.  ~~비교 = 지금 SV 비교 그대로 (증서 여유 없음 · 두 끝
    같게)~~ · 모서리 묶기 = 지금 규칙 그대로 (하나라도 의존 → `SV_DEPENDENT` · 하나라도 걸침 · 못 읽음 · 문턱 없음 · 모서리 없음 →
    `SV_UNCHECKED` · 둘 다 붙을 수 있다).
    ★★ 10-23 (Codex 재검토 RCA2-01 · 1저자 Q1 (가) · author 10-23 ratified Q1-Q8) **증서 구간으로 판정** — 아래 = 아래비 (`ratio_cert_lo` =
    Gfull_lo / Gcut_lower_hi · 내림) · 위 = 위비 (`ratio_cert_hi` = Gfull_hi / Gcut_upper_lo · 올림) · `ca_ext_svcf.cert_interval` (사슬 꼴이
    기록의 증서에서 다시 센다) · 아래비 > 문턱 → 의존 · 위비 ≤ 문턱 → 표지 없음 · 그 밖 → `SV_UNCHECKED` · +∞ = 위상이 증명한 0 분모만 ·
    nominal 비 (`ratio` · `ratio_hi`) = 기록 · 보고만 (판정에 쓰지 않는다 · 옛 판 = nominal 로 판정 → 판정문 반례 증서 구간 전체가 문턱 위인데
    표지 없음) · 진단 기록 (증서 없는 런 · 지위 `diagnostic_uncertified`) = R 판정 입력 아님 → `SV_UNCHECKED` (세부 `uncertified`).
    ★ 10-26 묶음 B6 (Codex 회차 ① RR1-01 · 1저자 10-26 Q2 (가)) require_graph (판정 `verdict_compute` = True) — 증서 구간 기록인데 끝 그래프 귀속이
    확인되지 않은 모서리 (read_run `sv_graph` 상태 ≠ verified · 봉인 원천 없음 · 원천 실패 · 대조 기록 없음) = 판정 입력 아님 → `SV_UNCHECKED` (세부
    `graph_unverified` · 의존 · clear 아님) · False (기본) = 구간 함수만 (원 팔 없는 시험 꼴)."""
    rr_scope = ('R_j_lo', 'R_j0', 'R_j_hi') if scope == 'all3' else ('R_j0',)
    out, unread, straddle, dep, uncert, gun = {}, [], [], [], [], []
    for (c, law, rr), a in sorted(recs.items()):
        if rr not in rr_scope:
            continue
        v = a.get('sv_cf') if isinstance(a, dict) else None
        v = v if isinstance(v, dict) else {}
        st, r_, rh = v.get('status'), v.get('ratio'), v.get('ratio_hi')
        lo_c, hi_c = v.get('ratio_cert_lo'), v.get('ratio_cert_hi')
        key = f'c{c}_{law}_{rr}'
        out[key] = {'status': st, 'ratio': r_, 'status_hi': v.get('status_hi'), 'ratio_hi': rh, 'n_unsplit': v.get('n_unsplit'),
                    'standing': v.get('standing'), 'ratio_cert_lo': lo_c, 'ratio_cert_hi': hi_c}
        #  ★ PF2 E (10-22 · PRE2-impl-02 옆 자리) — 읽는 비 = float (bool 아님) · 유한 양수 또는 +∞ (옛 = float 이기만 하면 읽음 → 아래 NaN ·
        #    −∞ · 0 · 음수 + 위 ≤ 문턱 = 표지 없음) · 그 밖 = 못 읽음 (SV_UNCHECKED) · ★ 10-23 — 읽는 값 = 증서 구간 끝 (nominal 아님)
        lo_ok, hi_ok = _sv_readable(lo_c), _sv_readable(hi_c)
        miss = uncert if v.get('standing') == SVCF.STANDING_DIAGNOSTIC else unread
        if require_graph and v.get('standing') == SVCF.STANDING_CERTIFIED and (lo_ok or hi_ok):
            gs = a.get('sv_graph') if isinstance(a, dict) and isinstance(a.get('sv_graph'), dict) else {}
            if gs.get('state') != 'verified':             # ★ 10-26 묶음 B6 — 그래프 귀속 미확인 = 판정 입력 아님 (구간을 보지 않는다)
                out[key]['graph'] = gs.get('kind') or 'absent'
                gun.append(key)
                continue
        if threshold is None:
            if not (lo_ok and hi_ok):
                miss.append(key)
            continue
        t = float(threshold)
        if lo_ok and lo_c > t:
            dep.append(key)
        elif lo_ok and hi_ok and hi_c <= t:
            pass
        elif lo_ok and hi_ok:
            straddle.append(key)
        else:
            miss.append(key)
    flags = []
    if threshold is None or unread or straddle or uncert or gun or not out:
        flags.append('SV_UNCHECKED')
    if dep:
        flags.append('SV_DEPENDENT')
    return flags, {'threshold': threshold, 'scope': scope, 'corners': out, 'unreadable': unread, 'straddle': straddle,
                   'dependent': dep, 'uncertified': uncert, 'graph_unverified': gun}


def mask_sigma(text, vals):
    """σ 값 (S/cm · mS/cm) 과 같은 수 토큰을 가린다 — 멈춤 사유 · 계약 문장에 σ 가 실려 화면에 나가지 않게."""
    vv = [v for v in vals if isinstance(v, float) and math.isfinite(v) and v != 0.0]

    def sub(m):
        try:
            x = float(m.group(0))
        except ValueError:
            return m.group(0)
        for v in vv:
            for c in (v, v * 1e3):
                if abs(x - c) <= 1e-6 * abs(c):
                    return '«σ 봉인»'
        return m.group(0)
    return re.sub(r'[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?', sub, str(text))


_HEX40_RE = re.compile(r'[0-9a-f]{40}')


def _hex40(x):
    return isinstance(x, str) and _HEX40_RE.fullmatch(x) is not None


def git_identity(path):
    """git 신원 → {head, dirty, rel, error}.  ★ 10-25 묶음 B (RCA2-02 · 1저자 10-23 Q2 (가) ① ② · 판정문 F1 · C6 #13) — 엄격: 두 조회
    (`rev-parse HEAD` · `status`) 의 종료코드를 본다 · head = 40 자 소문자 hex 일 때만 · dirty = status 가 rc 0 일 때만 True | False · 조회 실패 ·
    git 밖 = None (미확인 — False 로 바꾸지 않는다 · 대조 함수가 멈춘다) · (가-1) untracked = ignore 밖 전부 (`--untracked-files=normal` · 사용자
    설정 status.showUntrackedFiles 를 덮어쓴다) · rel = 저장소 상대 경로 (`rev-parse --show-prefix` + 파일 이름 · 코드 키의 경로 = 이것 · 절대 경로는
    키에 없다 · C6 #14) · error = 미확인 사유 (기록 · 판정 칸 아님).  옛 = 종료코드를 안 보고 `--untracked-files=no` (status 실패 = dirty False ·
    untracked = 깨끗)."""
    rec = {'head': None, 'dirty': None, 'rel': None, 'error': None}
    try:
        p = Path(path).resolve()
        isf = p.is_file()
        d = str(p.parent if isf else p)
        r = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True)
        head = (r.stdout or '').strip()
        if r.returncode != 0 or not _hex40(head):
            rec['error'] = f'git rev-parse HEAD rc {r.returncode} · 출력 {head[:44]!r} · {(r.stderr or "").strip()[:160]}'
            return rec
        rec['head'] = head
        r = subprocess.run(['git', '-C', d, 'rev-parse', '--show-prefix'], capture_output=True, text=True)
        if r.returncode != 0:
            rec['error'] = f'git rev-parse --show-prefix rc {r.returncode} · {(r.stderr or "").strip()[:160]}'
            return rec
        pre = (r.stdout or '').strip()
        rec['rel'] = (pre + p.name) if isf else (pre.rstrip('/') or '.')
        r = subprocess.run(['git', '-C', d, 'status', '--porcelain', '--untracked-files=normal'], capture_output=True, text=True)
        if r.returncode != 0:
            rec['error'] = f'git status rc {r.returncode} · {(r.stderr or "").strip()[:160]}'
            return rec
        rec['dirty'] = bool((r.stdout or '').strip())
        return rec
    except Exception as e:                                    # noqa: BLE001 — 미확인 = None (판정 = 대조 함수가 멈춘다)
        rec['error'] = f'{type(e).__name__}: {e}'
        return rec


_ENV_MEMO = {}


def _try(fn):
    try:
        return fn()
    except Exception:                                         # noqa: BLE001 — 기록만 칸 (판정 · 같음 대조에 쓰지 않는다)
        return None


def _env_cupy():
    import importlib.metadata as _md                       # python 3.8 표준
    got = sorted(f'{d.metadata.get("Name")} {d.version}' for d in _md.distributions()
                 if str(d.metadata.get('Name') or '').lower().startswith('cupy'))
    return got or None


def _env_gpu():
    r = subprocess.run(['nvidia-smi', '--query-gpu=name,driver_version', '--format=csv,noheader'], capture_output=True, text=True,
                       timeout=20)
    return ([x.strip() for x in (r.stdout or '').splitlines() if x.strip()] or None) if r.returncode == 0 else None


#: ★ 10-27 묶음 C1b — BLAS 기록 = 새 인터프리터 (같은 python · 같은 env) 에서 numpy · scipy.linalg 를 실은 뒤의 threadpool 목록 (정렬).  옛 = 이 프로세스의
#:   지금 목록 → 무엇을 먼저 import 했는지에 따라 달랐다 (scipy.linalg 를 실으면 BLAS 한 벌 더 · 실측) — 원장 항목 (--add 프로세스) ↔ 시도 (다른 프로세스)
#:   의 환경 지문 대조 (Q9 §3-2 · 재실행 = 모든 칸) 가 import 차례로 갈리지 않게.
_BLAS_PROBE = ('import json\n'
               'try:\n'
               '    import numpy, scipy.linalg, threadpoolctl\n'
               '    keep = ("user_api", "internal_api", "prefix", "version", "architecture", "threading_layer", "num_threads")\n'
               '    out = sorted(({k: x.get(k) for k in keep if k in x} for x in threadpoolctl.threadpool_info()),\n'
               '                 key=lambda d: json.dumps(d, sort_keys=True))\n'
               'except Exception:\n'
               '    out = None\n'
               'print(json.dumps(out))\n')


def _env_blas(np_):
    try:
        r = subprocess.run([sys.executable, '-I', '-c', _BLAS_PROBE], capture_output=True, text=True, timeout=120)
        got = json.loads(r.stdout) if r.returncode == 0 else None
        if isinstance(got, list):
            return got
    except Exception:                                         # noqa: BLE001 — 기록 칸 (아래 numpy 빌드 정보로)
        pass
    if np_ is None:
        return None
    try:
        dep = ((np_.show_config(mode='dicts') or {}).get('Build Dependencies') or {}).get('blas')   # numpy ≥ 1.26
        return {'build': dep}
    except Exception:                                         # noqa: BLE001
        pass
    cfg = getattr(np_, '__config__', None)
    for nm in ('blas_opt_info', 'blas_ilp64_opt_info', 'openblas_info'):
        v = getattr(cfg, nm, None)
        if isinstance(v, dict) and v:
            return {nm: {str(k): (v[k] if isinstance(v[k], (str, int)) else str(v[k])) for k in v}}
    return None


def _env_cpu():
    try:
        with open('/proc/cpuinfo', encoding='utf-8', errors='replace') as f:
            for ln in f:
                if ln.lower().startswith('model name'):
                    return ln.split(':', 1)[1].strip()
    except OSError:
        pass
    import platform
    return platform.processor() or None


def _env_simd(np_):
    if np_ is None:
        return None
    import importlib
    for nm in ('numpy._core._multiarray_umath', 'numpy.core._multiarray_umath'):
        try:
            mod = importlib.import_module(nm)
        except Exception:                                     # noqa: BLE001
            continue
        feats = getattr(mod, '__cpu_features__', None)
        if isinstance(feats, dict):
            return {'features': sorted(k for k, v in feats.items() if v), 'baseline': [str(x) for x in getattr(mod, '__cpu_baseline__', ()) or ()],
                    'dispatch': [str(x) for x in getattr(mod, '__cpu_dispatch__', ()) or ()]}
    return None


def env_record():
    """환경 지문 → {'unit': {python_minor · numpy · scipy}, 'record_only': {…}}.  ★ 10-25 묶음 B (RCA2-02 · 1저자 10-23 Q2 (가) ⑤ · Q9 설계 개정 4
    Q3 · R4-10) — 같음 단위 (unit) = python 부 판 (major.minor) · numpy · scipy 판 문자열 정확히 → 단계끼리 · 지금 코드와 대조 (코드 키 · 다르면
    멈춤 · 칸 하나라도 미확인 = 멈춤 · `code_dirty_problem`) · record_only = python 전체 판 (패치 판 포함) · 실행 파일 · 플랫폼 · cupy 배포 · GPU
    이름 · 드라이버 (nvidia-smi) · BLAS 계산 경로 (threadpoolctl · numpy 빌드 정보) · OPENBLAS_CORETYPE · CPU 모델 · numpy SIMD = 기록만 (판정 ·
    같음 대조에 쓰지 않는다 · 기계마다 다를 수 있다 · Codex 회차 ① Q-E 답에 따라 나중에 조일 수 있다).  이 사슬 프로세스의 환경이다 (러너 ·
    payload 는 사슬 env 를 물려받는다 · ~~러너가 venv 를 따로 켜는 자리 = VIRTUAL_ENV 가 빈 때 · 보고 "결정 필요"~~ → ★ 10-26 B″ (1저자 Q4) 사슬이
    런마다 러너에 MPM_NO_VENV=1 을 준다 (`RUNNER_EXEC_ENV` · 러너가 venv 를 켜지 않는다 · 한정 = 그 상수 주석) · 판정 계산기 프로세스의 환경은
    대조하지 않는다 (R4-11 — 다른 플랫폼의 다시 판정).  한 프로세스 안에서 한 번 잰다 (값을 바꿔 보는 시험 = 이 함수를 바꿔 끼운다)."""
    if 'rec' not in _ENV_MEMO:
        import platform
        np_ = None                                            # 기록만 칸 (BLAS · SIMD) 이 읽는 모듈 — import 이름과 갈라 둔다 (규율 경고)
        #  ★ 10-26 B″ (1저자 Q1 (가)) — 같음 단위 = `run_contract.env_unit_now` (payload 조립만 출력 · 봉인 원천 대조와 같은 함수 · 사본 없음 · 값 그대로)
        unit = RC.env_unit_now()
        try:
            import numpy as _np_mod
            np_ = _np_mod
        except Exception:                                     # noqa: BLE001 — 기록만 칸 (BLAS · SIMD) 이 None 이 된다
            pass
        ro = {'python': platform.python_version(), 'implementation': platform.python_implementation(), 'executable': sys.executable,
              'platform': _try(platform.platform), 'cupy': _try(_env_cupy), 'gpu': _try(_env_gpu), 'blas': _try(lambda: _env_blas(np_)),
              'openblas_coretype': os.environ.get('OPENBLAS_CORETYPE'), 'cpu_model': _try(_env_cpu), 'numpy_simd': _try(lambda: _env_simd(np_))}
        _ENV_MEMO['rec'] = json.loads(json.dumps({'unit': unit, 'record_only': ro}, default=str))
    return json.loads(json.dumps(_ENV_MEMO['rec']))


def env_unit(env):
    """환경 지문의 같음 단위 → {python_minor · numpy · scipy} | None (칸 하나라도 없거나 빈 글자 = 미확인 = None)."""
    u = env.get('unit') if isinstance(env, dict) else None
    if not isinstance(u, dict):
        return None
    out = {k: u.get(k) for k in ENV_UNIT_KEYS}
    return out if all(isinstance(v, str) and v for v in out.values()) else None


def _same(a, b, rel=1e-12):
    if isinstance(a, bool) or isinstance(b, bool):
        return type(a) is type(b) and a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        fa, fb = float(a), float(b)
        return math.isfinite(fa) and math.isfinite(fb) and (fa == fb or abs(fa - fb) <= rel * max(abs(fa), abs(fb)))
    return a == b


def _int_or_none(x):
    """반복 수 칸 → int | None (bool · 수 아닌 것 · 음수 = None — 기록 칸이지 판정 칸이 아니다)."""
    return x if type(x) is int and x >= 0 else None          # noqa: E721 — bool 제외


def variant_vox(variant):
    return VOX_GRID if variant == 'GRID' else VOX_MAIN


def variant_raster(kit, variant):
    """sid 격자 무리 키 — R_j · c · P 는 래스터를 안 바꾼다 · vox · SDCP 양보는 바꾼다."""
    return f'{kit}|vox={variant_vox(variant)}|yield={variant == "SVORDER"}'


def sid_group(kit, variant, origin_idx):
    """★ Z3 — sid 지문 대조 무리 = 킷 · 래스터 · **origin** (팔 번호 — 격자 위상이 다르면 sid 격자도 다르다 · origin 검사 팔 1 · 2 가
    a0 와 다른 지문을 내는 것은 정상)."""
    return f'{variant_raster(kit, variant)}|origin={int(origin_idx)}'


def origins_for(vox):
    """러너의 팔 번호 ↔ origin (러너 SHIFTS 순서 그대로 — H = vox/2 소수 6 자리)."""
    h = float(f'{vox / 2:.6f}')
    return [(x, y, z) for x in (0.0, h) for y in (0.0, h) for z in (0.0, h)]


# ═════════════════════════ 등록 · 계획 ═════════════════════════
def registration_row_hash(path, prefix, code_unreg, label):
    """등록 R §2-1 의 해시 줄 하나 (`prefix` 로 시작하는 줄 · 하나뿐이어야) → (sha256 hex, 문서 sha256).  ⬜ = code_unreg."""
    try:
        raw = Path(path).read_bytes()
        text = raw.decode('utf-8')
    except (OSError, UnicodeDecodeError) as e:
        raise Stop('REGISTRATION_UNREADABLE', f'{path} ({type(e).__name__})')
    rows = [ln for ln in text.splitlines() if ln.startswith(prefix)]
    if len(rows) != 1:
        raise Stop('REGISTRATION_UNREADABLE', f'§2-1 "{prefix}" 줄이 {len(rows)} 개 (1 이어야)')
    cells = [c.strip() for c in rows[0].strip().strip('|').split('|')]
    val = cells[-1].strip('` ')
    if not re.fullmatch(r'[0-9a-f]{64}', val):
        raise Stop(code_unreg, f'§2-1 {label} 칸 = {val!r} — 개정 커밋 (숫자 + 계획 해시 · 결과 0 건) 전에는 σ 런 없음')
    return val, hashlib.sha256(raw).hexdigest()


def registration_plan_hash(path):
    """등록 R §2-1 의 R 런 계획 해시 칸 → (sha256 hex, 문서 sha256).  ⬜ 이면 PLAN_HASH_UNREGISTERED (사람이 옮겨 적지 않는다)."""
    return registration_row_hash(path, '| 계획 해시 |', 'PLAN_HASH_UNREGISTERED', '계획 해시')


def registration_s0_hash(path):
    """등록 R §2-1 의 S0 계획 해시 칸 (`| S0 계획 해시 |` · 위 줄과 다른 파일) → (sha256 hex, 문서 sha256)."""
    return registration_row_hash(path, '| S0 계획 해시 |', 'S0_PLAN_HASH_UNREGISTERED', 'S0 계획 해시')


def _reject_constant(tok):
    raise ValueError(f'JSON 상수 {tok} 거부')


def _reject_dup(pairs):
    """★ PF2 E (10-22 · 사전 리뷰 2 회차 PRE2-impl-03) — JSON 중복 칸 거부 (같은 바이트를 사람 = 앞 값 · 해석기 = 뒤 값으로 다르게 읽지 않게 ·
    등록 sha 로 묶인 계획 · S0 보고)."""
    out = {}
    for k, v in pairs:
        if k in out:
            raise ValueError(f'JSON 중복 칸 {k!r} 거부')
        out[k] = v
    return out


def _json_strict(raw, enc='utf-8'):
    """계획 · S0 보고 읽기 — NaN · Infinity 상수 거부 · 중복 칸 거부 (ValueError)."""
    return json.loads(raw.decode(enc), parse_constant=_reject_constant, object_pairs_hook=_reject_dup)


def _num(v):
    """유한 실수 (bool 아님) — ★ PF2 E (PRE2-impl-03) float 로 못 바꾸는 큰 정수 (10**400 · OverflowError) = 유한 아님 (옛 = 잡히지 않은 예외)."""
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return False
    try:
        return math.isfinite(v)
    except OverflowError:
        return False


def _show(v):
    """멈춤 사유의 값 표시 — float 로 못 바꾸는 큰 정수 (★ PF2 E · 10**400) 는 자리 수만 (수백 자리를 화면에 쏟지 않는다)."""
    if isinstance(v, int) and not isinstance(v, bool) and not _num(v):
        return f'<정수 {len(str(abs(v)))} 자리 · float 넘침>'
    return repr(v)


def exec_policy_problems(ep):
    """★ 10-27 묶음 C1a (RCA2-05 · author 10-27 approved bundle C) — 계획 `exec_policy` 칸 꼴 → 문제 목록 (값 칸 null = ⬜ · 꼴 검사는 지난다 ·
    `require_plan_numbers` 가 멈춘다).  값은 고치지 않는다 (사슬이 숫자를 고르지 않는다)."""
    if not isinstance(ep, dict) or set(ep) != set(EXEC_POLICY_KEYS):
        return [f'exec_policy 칸 {sorted(ep) if isinstance(ep, dict) else type(ep).__name__} ≠ {sorted(EXEC_POLICY_KEYS)}']
    bad = [f'exec_policy.{k} {ep[k]!r} ≠ 이 사슬의 규칙 {v!r}' for k, v in EXEC_POLICY_RULES.items() if ep[k] != v]
    mh = ep['max_hours']
    if mh is not None and not (type(mh) in (int, float) and _num(mh) and mh > 0):     # noqa: E721 — bool · 문자열 제외 · 10**400 넘침 = 유한 아님
        bad.append(f'exec_policy.max_hours {_show(mh)} (유한 > 0 · null = ⬜)')
    ma = ep['max_attempts']
    if ma is not None and not (type(ma) is int and _num(ma) and ma >= 1):            # noqa: E721
        bad.append(f'exec_policy.max_attempts {_show(ma)} (정수 ≥ 1 · 유한 · null = ⬜)')
    am = ep['allowed_machines']
    if am is not None and not (isinstance(am, list) and am and all(isinstance(m, str) and MACHINE_RE.fullmatch(m) for m in am)
                               and len(set(am)) == len(am)):
        bad.append(f'exec_policy.allowed_machines {am!r} (비지 않은 목록 · 이름표 = 영문 · 숫자 · _ · - · 중복 없음 · null = ⬜)')
    eu = ep['env_unit']
    if eu is not None and not (isinstance(eu, dict) and set(eu) == set(ENV_UNIT_KEYS)
                               and all(isinstance(eu[k], str) and ENV_UNIT_VALUE_RE.fullmatch(eu[k]) for k in ENV_UNIT_KEYS)):
        bad.append(f'exec_policy.env_unit {eu!r} (칸 = {sorted(ENV_UNIT_KEYS)} · 판 문자열 · null = ⬜)')
    return bad


def plan_form_problems(obj):
    """R 런 계획 dict 꼴 → 문제 목록 (`load_plan` · 단계 요약의 계획 기록 (예측 · 판정) 이 같은 함수).  결과 전 등록 숫자 · 실행 정책 값 칸 null =
    꼴은 지난다 (`require_plan_numbers`)."""
    if not isinstance(obj, dict) or set(obj) != set(PLAN_KEYS):
        return [f'칸 {sorted(obj) if isinstance(obj, dict) else type(obj).__name__} ≠ {sorted(PLAN_KEYS)}']
    bad = []
    if obj['schema'] != PLAN_SCHEMA:
        bad.append(f'schema {obj["schema"]!r} ≠ {PLAN_SCHEMA!r}')
    if not (isinstance(obj['len_law'], str) and re.fullmatch(r'[A-Za-z0-9_]+', obj['len_law'])):
        bad.append(f'len_law {obj["len_law"]!r}')
    if obj['unreg_law'] != PLAN_UNREG_MAIN:
        bad.append(f'unreg_law {obj["unreg_law"]!r} ≠ {PLAN_UNREG_MAIN!r} (주 = cut · fused = UNREG 감도)')
    for k, pos in (('s_min_um', False), ('tol_ff_um', False), ('step3_rtol', True)):
        v = obj[k]
        if not _num(v) or v < 0 or (pos and v == 0):
            bad.append(f'{k} {_show(v)}')
    if not (isinstance(obj['p2_extra'], str) and re.fullmatch(r'[A-Za-z0-9._=/ -]*', obj['p2_extra'])):
        bad.append(f'p2_extra {obj["p2_extra"]!r}')
    mp = obj['max_ladder_points']
    if mp is not None and not (type(mp) is int and _num(mp) and mp >= 1):    # noqa: E721 — bool 제외 · ★ PF2 E 넘침 (10**400) = 유한 아님
        bad.append(f'max_ladder_points {_show(mp)} (정수 ≥ 1 · 유한 · null = ⬜)')
    cr = obj['calib_rj_ratio_max']
    if cr is not None and cr != PLAN_NO_CAP and not (_num(cr) and cr > 1.0):
        bad.append(f'calib_rj_ratio_max {_show(cr)} (유한 > 1 · {PLAN_NO_CAP!r} = 상한 없음으로 등록 · null = ⬜)')
    th = obj['sv_cf_threshold']
    if th is not None and not (_num(th) and th >= 1.0):
        bad.append(f'sv_cf_threshold {_show(th)} (유한 ≥ 1 · 비 G_full/G_cut ≥ 1 · null = ⬜)')
    if obj['sv_cf_scope'] is not None and obj['sv_cf_scope'] not in SV_CF_SCOPES:
        bad.append(f'sv_cf_scope {obj["sv_cf_scope"]!r} ∉ {SV_CF_SCOPES} (null = ⬜)')
    bad += exec_policy_problems(obj['exec_policy'])          # ★ 10-27 묶음 C1a
    return bad


def load_plan(path):
    """R 런 계획 파일 (`rint-r-plan-v3` · 등록 §2-1 개정 커밋의 대상) → (dict, sha256).  사슬은 이 값을 러너 env 로 편다.
    결과 전 등록 숫자 넷 · 실행 정책 값 칸 넷은 null 이어도 꼴 검사는 지난다 (null = ⬜ · `require_plan_numbers` 가 멈춘다)."""
    try:
        raw = Path(path).read_bytes()
        obj = _json_strict(raw)                               # ★ PF2 E — 중복 칸 거부 (옛 = 마지막 값)
    except (OSError, UnicodeDecodeError, ValueError) as e:
        raise Stop('PLAN_INVALID', f'{path}: {type(e).__name__}: {e}')
    bad = plan_form_problems(obj)
    if bad:
        raise Stop('PLAN_INVALID', ' · '.join(bad))
    return obj, hashlib.sha256(raw).hexdigest()


def plan_record_or_stop(plan, where):
    """★ 10-27 묶음 C1a — 단계 요약에 기록된 계획 (예측 · 판정 · 사슬이 다시 읽는 자리) = 같은 꼴 검사 (`plan_form_problems` · 실행 정책 칸을 쓰기 전)."""
    bad = plan_form_problems(plan)
    if bad:
        raise Stop('PLAN_INVALID', f'{where}: ' + ' · '.join(bad))
    return plan


def require_plan_numbers(plan):
    """결과 전 등록 숫자 넷 (⬜) 이 다 있어야 σ 런을 돈다 — 등록 R §3-2 · §3-2b · §5-6 (★ Q-G: SV 문턱이 ⬜ 인 채로는 못 간다).
    ★ 10-27 묶음 C1a (RCA2-05 · 판정문 §4 "DBE 단계 2 열람 전에 … 봉인") — 실행 정책 값 칸 넷 (`exec_policy.<칸>`) 도 (봉인 전 계획 = R 진입 거부 ·
    S0 단계 2 관문 `ca_s0_census.verify_plan_commit` 도 이 함수)."""
    miss = [k for k in PLAN_REGISTERED_NUMBERS if plan.get(k) is None]
    ep = plan.get('exec_policy') if isinstance(plan.get('exec_policy'), dict) else {}
    miss += [f'exec_policy.{k}' for k in EXEC_POLICY_VALUE_KEYS if ep.get(k) is None]
    if miss:
        raise Stop('PLAN_NUMBER_UNREGISTERED', f'R 계획 칸 {miss} = null (⬜ 결과 전 등록 · 1저자 · §10 개정 · 숫자를 사슬이 고르지 않는다)')


def exec_check_or_stop(plan, max_hours, machine, code):
    """★ 10-27 묶음 C1a (RCA2-05 · C6 #15 · Q11 · Q9 개정 4 Q3 · author 10-27 approved bundle C) — 사다리 · 예측 단계 진입 대조 (러너 전):
    `--max-hours` = 계획 exec_policy.max_hours (정확히 · 다르면 NOT_REGISTERED) · `--machine` ∈ allowed_machines (밖 = MACHINE_NOT_ALLOWED) ·
    환경 지문 같음 단위 = 계획 봉인 판 (다르면 CODE_PIN_MISMATCH · 바른 판의 venv 로 다시).  require_plan_numbers 뒤에 부른다."""
    ep = plan['exec_policy']
    if not (_num(max_hours) and float(max_hours) == float(ep['max_hours'])):
        raise Stop('NOT_REGISTERED', f'--max-hours {_show(max_hours)} ≠ 계획 exec_policy.max_hours {_show(ep["max_hours"])} (RCA2-05 · 시간 상한 = 계획 '
                                     f'봉인 값 · 결과를 본 뒤 늘리지 않는다)')
    if machine not in ep['allowed_machines']:
        raise Stop('MACHINE_NOT_ALLOWED', f'--machine {machine!r} ∉ 계획 exec_policy.allowed_machines {ep["allowed_machines"]} (C6 #15 · Q11)')
    why = env_seal_problem(code, plan)
    if why:
        raise Stop('CODE_PIN_MISMATCH', why)


def env_seal_problem(code, plan):
    """★ 10-27 묶음 C1a (Q9 개정 4 Q3 · R4-10) — 단계 code 기록의 환경 지문 같음 단위 ↔ 계획 봉인 판 → 문제 | None (판정도 같은 함수)."""
    want = (plan.get('exec_policy') or {}).get('env_unit') if isinstance(plan, dict) else None
    got = env_unit((code or {}).get('env') if isinstance(code, dict) else None)
    if got != want:
        g, w = got or {}, want or {}
        diff = [f'{k} {g.get(k)!r} ≠ {w.get(k)!r}' for k in ENV_UNIT_KEYS if g.get(k) != w.get(k)] or ['미확인']
        return ('환경 지문 같음 단위 ≠ 계획 봉인 판 (exec_policy.env_unit · ' + ' · '.join(diff) + ') — 계획에 봉인한 python 부 판 · numpy · scipy 판의 '
                'venv 로 다시 (Q9 개정 4 Q3 · R4-10)')
    return None


def plan_doc_block(plan):
    """★ 10-27 묶음 C1a (판정문 C6 #30) — 계획 JSON → 등록 R 에 붙이는 계획 숫자 블록 (표지 둘 사이 · 칸 = 계획 칸 이름순 · exec_policy = 칸마다 한 줄 ·
    값 = 정준 JSON 글자 · 사람이 옮겨 적지 않는다 · 대조 = `plan_doc_problem`)."""
    rows = []
    for k in sorted(plan):
        if k == 'exec_policy' and isinstance(plan[k], dict):
            rows += [(f'exec_policy.{kk}', plan[k][kk]) for kk in sorted(plan[k])]
        else:
            rows.append((k, plan[k]))
    lines = [PLAN_DOC_BEGIN, '| R 계획 칸 | 값 |', '|---|---|']
    lines += [f'| `{k}` | `{json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":"))}` |' for k, v in rows]
    return '\n'.join(lines + [PLAN_DOC_END])


def plan_doc_problem(reg_path, plan):
    """★ 10-27 묶음 C1a (판정문 C6 #30) — 등록 R 문서의 계획 숫자 블록 = `plan_doc_block(plan)` (정확히 · 표지 각 하나 · 순서) → 문제 | None."""
    try:
        text = Path(reg_path).read_bytes().decode('utf-8')
    except (OSError, UnicodeDecodeError) as e:
        return f'등록 문서를 못 읽는다 ({type(e).__name__})'
    nb, ne = text.count(PLAN_DOC_BEGIN), text.count(PLAN_DOC_END)
    if nb != 1 or ne != 1:
        return (f'계획 숫자 블록 표지 시작 {nb} · 끝 {ne} 개 (각 1 이어야 · 봉인 때 `--stage plan-doc --plan <계획>` 출력을 그대로 붙인다 · 봉인 전 = '
                f'R 진입 없음)')
    i, j = text.index(PLAN_DOC_BEGIN), text.index(PLAN_DOC_END)
    if j < i:
        return '계획 숫자 블록 끝 표지가 시작 표지 앞에 있다'
    got, want = text[i:j + len(PLAN_DOC_END)], plan_doc_block(plan)
    if got != want:
        gl, wl = got.splitlines(), want.splitlines()
        k = next((n for n, (x, y) in enumerate(zip(gl, wl)) if x != y), min(len(gl), len(wl)))
        return (f'계획 숫자 블록 ≠ 계획 JSON 에서 생성한 블록 (줄 {k + 1}: 문서 {(gl[k] if k < len(gl) else "<없음>")[:80]!r} · 생성 '
                f'{(wl[k] if k < len(wl) else "<없음>")[:80]!r}) — 사람이 옮겨 적지 않는다 (`--stage plan-doc`)')
    return None


def plan_doc_or_stop(reg_path, plan):
    why = plan_doc_problem(reg_path, plan)
    if why:
        raise Stop('PLAN_DOC_MISMATCH', why)


def stage_machine_problem(s, plan):
    """★ 10-27 묶음 C1a (C6 #15 · Q11 · Q9 §3-4) — 단계 요약의 기계 이름표 ∈ 계획 허용 목록 (빈 이름 · 없음 = 문제) · 런 기록마다 기계 = 단계 기계
    (한 기계 단계 · 칸 없음 · 빈 · 다른 기계 = 문제) → 문제 | None (판정이 단계마다 부른다)."""
    allowed = ((plan or {}).get('exec_policy') or {}).get('allowed_machines') or []
    m = s.get('machine')
    if not (isinstance(m, str) and m in allowed):
        return f'단계 기계 {m!r} ∉ 계획 exec_policy.allowed_machines {allowed}'
    mg = s.get('merge') if isinstance(s.get('merge'), dict) else None
    for r in s.get('runs') or []:
        if mg is not None:                                    # ★ 10-27 묶음 C2d — 합친 예측: 런 기계 = 그 런 단위 시도의 기계 (허용 목록 안 · 합치기 기계와 다를 수 있다)
            src = r.get('source') if isinstance(r.get('source'), dict) else {}
            um = ((mg.get('units') or {}).get(src.get('target')) or {}).get('machine')
            if not (isinstance(r.get('machine'), str) and r.get('machine') in allowed and r.get('machine') == um):
                return f'합친 런 {r.get("name")} 기계 {r.get("machine")!r} ≠ 그 단위 시도 기계 {um!r} · 허용 목록 {allowed}'
        elif r.get('machine') != m:
            return f'런 {r.get("name")} 기계 {r.get("machine")!r} ≠ 단계 기계 {m!r} (팔마다 기계 이름 · 한 기계 단계)'
    return None


def ladder_cap(plan):
    """§3-2 점 수 상한 (⬜ = 계획 칸 · 2판 숫자 12 는 기본값이 아니다)."""
    return int(plan['max_ladder_points'])


def plan_env(plan):
    env = {'CJUNC_LEN_LAW': plan['len_law'], 'CJUNC_UNREG_LAW': plan['unreg_law'], 'CJUNC_S_MIN_UM': repr(float(plan['s_min_um'])),
           'CJUNC_TOL_FF_UM': repr(float(plan['tol_ff_um'])), 'STEP3_RTOL': repr(float(plan['step3_rtol']))}
    if plan['p2_extra']:
        env['P2_EXTRA'] = plan['p2_extra']
    return env


def check_plan_registered(plan_sha, reg_path):
    want, reg_sha = registration_plan_hash(reg_path)
    if plan_sha != want:
        raise Stop('PLAN_HASH_MISMATCH', f'계획 sha256 {plan_sha[:16]}… ≠ 등록 §2-1 {want[:16]}…')
    return {'path': str(Path(reg_path).resolve()), 'sha256': reg_sha, 'plan_hash': want}


def plans_cross_problems(plan, s0):
    """§2-1 · §10-2 ⑪ 두 계획 대조 → 문제 목록.  R 계획 tol_ff = S0 tol_ff (같은 float) · 사슬 L_par · r_port · r_f = S0 값 ·
    R 계획 step3_rtol = §3-5 봉인값 (`step3_conv_cert.CERT_RTOL_MAX`) · len_law = 등록 v0 길이 법칙 이름 (`carbon_junction.CJUNC_LEN_LAW` ·
    분산판 = 같은 총 G 법칙 · 표현 판은 원장 · model 이름) · unreg_law = cut."""
    import carbon_junction as _cj
    import step3_conv_cert as _cc
    v = (s0 or {}).get('values_um') if isinstance(s0, dict) else None
    v = v if isinstance(v, dict) else {}
    bad = []

    def eqf(name, a, b):
        if not (_num(a) and _num(b) and float(a) == float(b)):
            bad.append(f'{name}: {a!r} ≠ {b!r}')
    eqf('R 계획 tol_ff_um ↔ S0 values_um.tol_ff', plan.get('tol_ff_um'), v.get('tol_ff'))
    eqf('S0 values_um.tol_P ↔ tol_ff', v.get('tol_P'), v.get('tol_ff'))
    eqf('S0 values_um.tol_sj ↔ tol_ff', v.get('tol_sj'), v.get('tol_ff'))
    eqf('사슬 L_PAR_UM ↔ S0 values_um.L_par', L_PAR_UM, v.get('L_par'))
    eqf('사슬 R_PORT_UM ↔ S0 values_um.r_port', R_PORT_UM, v.get('r_port'))
    eqf('사슬 VGCF_D_UM/2 ↔ S0 values_um.r_f', VGCF_D_UM / 2.0, v.get('r_f'))
    eqf('R 계획 step3_rtol ↔ §3-5 봉인 CERT_RTOL_MAX', plan.get('step3_rtol'), _cc.CERT_RTOL_MAX)
    if plan.get('len_law') != _cj.CJUNC_LEN_LAW:
        bad.append(f'R 계획 len_law {plan.get("len_law")!r} ≠ 등록 v0 길이 법칙 {_cj.CJUNC_LEN_LAW!r}')
    if plan.get('unreg_law') != PLAN_UNREG_MAIN:
        bad.append(f'R 계획 unreg_law {plan.get("unreg_law")!r} ≠ {PLAN_UNREG_MAIN!r}')
    return bad


def _s0_check_obj(obj, raw):
    """S0 계획 dict · 바이트 → 문제 | None (정본 = `ca_s0_census.check_plan` · 정준 바이트 · 사본 없음)."""
    import ca_s0_census as _s0
    if not isinstance(obj, dict) or obj.get('schema') != S0_PLAN_SCHEMA:
        return f'schema {(obj or {}).get("schema") if isinstance(obj, dict) else type(obj).__name__!r} ≠ {S0_PLAN_SCHEMA!r}'
    try:
        _s0.check_plan(obj)
    except Exception as e:                                    # noqa: BLE001 — S0Error · 그 밖 = 확인 못 함 = 거부
        return f'check_plan: {type(e).__name__}: {e}'
    if raw is not None and _s0.plan_bytes_of(obj) != raw:
        return '정준 바이트가 아니다 (손으로 고친 형식 · 단계 1 산출물 그대로)'
    return None


def check_s0(s0_obj, s0_sha, raw, reg_path, plan):
    """S0 계획 → 기록 dict ({path?, sha256, content}) · 등록 `| S0 계획 해시 |` 대조 · 두 계획 대조.  실패 = Stop."""
    why = _s0_check_obj(s0_obj, raw)
    if why:
        raise Stop('S0_PLAN_INVALID', why)
    if raw is None:
        import ca_s0_census as _s0
        if hashlib.sha256(_s0.plan_bytes_of(s0_obj)).hexdigest() != s0_sha:
            raise Stop('S0_PLAN_INVALID', '기록된 S0 계획 sha256 ≠ 그 내용의 정준 바이트 sha256')
    want, _reg = registration_s0_hash(reg_path)
    if s0_sha != want:
        raise Stop('S0_PLAN_HASH_MISMATCH', f'S0 계획 sha256 {s0_sha[:16]}… ≠ 등록 §2-1 {want[:16]}…')
    bad = plans_cross_problems(plan, s0_obj)
    if bad:
        raise Stop('PLAN_CROSS_MISMATCH', ' · '.join(bad))
    return {'sha256': s0_sha, 'content': s0_obj}


def load_s0_plan(path, reg_path, plan):
    """--s0-plan 파일 → 기록 (path · sha256 · content) · 꼴 · 등록 · 대조 (`check_s0`)."""
    try:
        raw = Path(path).read_bytes()
        obj = _json_strict(raw, 'ascii')                      # ★ PF2 E — 중복 칸 거부 (정준 바이트 검사 앞)
    except (OSError, UnicodeDecodeError, ValueError) as e:
        raise Stop('S0_PLAN_INVALID', f'{path}: {type(e).__name__}: {e}')
    rec = check_s0(obj, hashlib.sha256(raw).hexdigest(), raw, reg_path, plan)
    return dict(rec, path=str(Path(path).resolve()))


def recheck_s0_record(rec, reg_path, plan):
    """요약에 기록된 S0 계획 (예측 · 판정 단계) — 내용 → 정준 바이트 sha256 = 기록 sha · 등록 · 대조 (같은 함수)."""
    if not isinstance(rec, dict) or not isinstance(rec.get('content'), dict) or not isinstance(rec.get('sha256'), str):
        raise Stop('S0_PLAN_INVALID', '요약에 S0 계획 기록 (sha256 · content) 이 없다')
    return check_s0(rec['content'], rec['sha256'], None, reg_path, plan)


# ═════════════════════════ ★ PF2 B · D (10-22) S0 단계 보고 — 봉인 계획 해시 · census · registry 파일 지문 ═════════════════════════
def _hex64(x):
    return isinstance(x, str) and re.fullmatch(r'[0-9a-f]{64}', x) is not None


S0_STAGE1_SOURCE = 'stage1_computed'   # S0 단계 1 보고의 plan.source (= `ca_s0_census.census_kit` 단계 1 · 그 계획을 그 침대에서 만들었다)
#: ★ PF2 D (등록 R §2-1b) — census · registry 파일 ≠ S0 보고일 때 멈춤 사유에 붙는 등록 문장
S0_RERUN = ('R 런을 돌리지 않는다 → S0 단계 1 · 2 를 이 R 런 판으로 다시 (σ 없음) + §2-1 개정 다시 (결과 0 건 · σ 전) · DBE (단계 2) 가 이미 '
            '열렸으면 s_min 을 다시 고르지 않는다 (같은 s_min · 바꾸려면 새 등록 · 등록 R §2-1b)')


def s0_report_record(rep, sha, path):
    """S0 단계 보고 (dict) → 사슬 기록 (판정 칸만 · 보고 경로 · 파일 sha256) — 꼴이 틀려도 기록은 만들고 (값 그대로) 검사는
    `s0_stage2_problem` · `s0_stage1_problem` · `s0_code_problem` 이 한다 (예측 · 판정은 이 기록을 다시 검사한다 · 보고 파일을 다시 읽지 않는다).
    ★ PF2 D — 보고의 code 칸 (git_head · git_dirty · file_digests) 을 그대로 싣는다 (판정 = 파일 지문 · git_head · git_dirty 는 기록만)."""
    rp = rep if isinstance(rep, dict) else {}
    pl = rp.get('plan') if isinstance(rp.get('plan'), dict) else {}
    rr = pl.get('r_plan') if isinstance(pl.get('r_plan'), dict) else {}
    kit = rp.get('kit') if isinstance(rp.get('kit'), dict) else {}
    code = rp.get('code') if isinstance(rp.get('code'), dict) else {}
    #  ★ 10-25 묶음 B (RCA2-03 · Q3 (가)) — 같은 침대 칸 (S0 보고 그대로 · 원 입력 = 역할별 path · sha256 · bytes · metrics 상자 · 두께 ·
    #    설정 sha256 / 파생 = 규약 · off 격자 지문) — 꼴 검사 = `s0_bed_record_problem` · 대조 = `bed_problem` (원 입력) · read_run (파생)
    inp = rp.get('inputs') if isinstance(rp.get('inputs'), dict) else None
    ras = rp.get('raster') if isinstance(rp.get('raster'), dict) else None
    met = (inp or {}).get('metrics')
    return {'path': path, 'sha256': sha, 'schema': rp.get('schema'), 'stage': rp.get('stage'), 'kit': kit.get('name'),
            'plan_sha256': pl.get('sha256'), 'plan_source': pl.get('source'), 'r_plan_sha256': rr.get('sha256'), 'r_plan_path': rr.get('path'),
            'git_head': code.get('git_head'), 'git_dirty': code.get('git_dirty'), 'file_digests': code.get('file_digests'),
            'inputs': (None if inp is None else
                       {'files': inp.get('files'), 'settings_sha256': inp.get('settings_sha256'),
                        'metrics': ({k: met.get(k) for k in BED_METRICS} if isinstance(met, dict) else met)}),
            'raster': (None if ras is None else {'convention': ras.get('convention'), 'sid_off_fp': ras.get('sid_off_fp')}),
            #  ★ 10-25 묶음 B (X6 · Q20 (가)) — 단계 2 봉인 SV census (census 세 칸 · 봉인 s_min · tol_ff · 지문 = 기록만) · 단계 1 = null
            'sv_census': ({k: rp['sv_census'].get(k) for k in ('census', 's_min_um', 'tol_ff_um', 'fp')}
                          if isinstance(rp.get('sv_census'), dict) else rp.get('sv_census'))}


# ═════════════════════════ ★ 10-25 묶음 B (RCA2-03 · 1저자 10-23 Q3 (가)) 같은 침대 — S0 → R ═════════════════════════
#: 원 입력 기록의 metrics 칸 (S0 보고 inputs.metrics 중 대조하는 것 · `ca_s0_census.kit_input_record` 와 같은 이름)
BED_METRICS = ('um_box_um', 'thickness_um')
#: 파생 격자 지문을 대조하는 규약 = R 주 런 arm 0 (사슬 고정값 · `ENV_FIXED` · `MAN_FIXED` · 러너 기본 선분 스탬프 · origin 0 · S0 가 잡은
#  payload 입력은 PTFE centerline 으로 찍은 뒤 PTFE 행을 뺀 off 격자 = face_alpha 의 sid 격자) — 다르면 대조 안 함 (기록만)
S0_GRID_CONVENTION = {'vox_um': VOX_MAIN, 'bridge_um': MAN_FIXED['bridge_um'], 'sdcp_sphere_d_um': MAN_FIXED['sdcp_sphere_d_um'],
                      'fibre_stamp': 'segment', 'ptfe_stamp_captured': 'centerline', 'origin_shift_um': [0.0, 0.0, 0.0]}
#: 킷 ↔ 그 킷의 S0 단계 보고 (단계 1 = SBE 새 침대 · 단계 2 = DBE 새 침대)
BED_STAGE = {SBE_KIT: 'stage1', DBE_KIT: 'stage2'}
BED_NEW_S0 = '재압밀 · 재생성 침대 = 새 S0 (등록 R §2-1 · §11 · 같은 침대가 아니면 S0 단계 1 · 2 를 그 침대로 다시)'


def _hex32(x):
    return isinstance(x, str) and re.fullmatch(r'[0-9a-f]{32}', x) is not None


def _pos_or_none(x):
    if x is None:
        return True
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        return False
    try:
        return math.isfinite(float(x)) and float(x) > 0
    except OverflowError:
        return False


def s0_bed_record_problem(rec, label):
    """S0 보고 기록의 같은 침대 칸 → 꼴 문제 | None.  원 입력 = 역할 (`ca_s0_census.KIT_ROLES` 전부 + 선택 `KIT_ROLES_OPTIONAL`) 마다
    path (문자열 · 기록만) · sha256 (64 자 소문자 hex) · bytes (정수 ≥ 0 · bool 아님) · metrics (um_box_um · thickness_um = 유한 양수 또는 null) ·
    settings_sha256 (64 hex) · 파생 = 규약 (dict) · sid_off_fp (32 자 소문자 hex).  옛 꼴 (칸 없음) = 멈춤."""
    import ca_s0_census as _s0
    r = rec if isinstance(rec, dict) else {}
    inp = r.get('inputs')
    if not isinstance(inp, dict):
        return f'{label} 보고에 원 입력 (inputs) 이 없다 (옛 꼴 · {S0_REPORT_SCHEMA} 이전) — {BED_NEW_S0}'
    fs = inp.get('files')
    if not isinstance(fs, dict):
        return f'{label} 보고의 원 입력 파일 (inputs.files) 꼴 {type(fs).__name__} (역할별 dict 이어야)'
    miss = [k for k in _s0.KIT_ROLES if k not in fs]
    extra = sorted(str(k) for k in fs if k not in _s0.KIT_ROLES + _s0.KIT_ROLES_OPTIONAL)
    if miss or extra:
        return f'{label} 보고의 원 입력 역할 — 없음 {miss} · 모르는 역할 {extra} (= {list(_s0.KIT_ROLES)} + 선택 {list(_s0.KIT_ROLES_OPTIONAL)})'
    for k in sorted(fs):
        x = fs[k]
        if not isinstance(x, dict) or not _hex64(x.get('sha256')) or type(x.get('bytes')) is not int or x['bytes'] < 0 \
                or not isinstance(x.get('path'), str):          # noqa: E721 — bool 제외
            return (f'{label} 보고의 원 입력 역할 {k} 꼴 — sha256 {(x or {}).get("sha256") if isinstance(x, dict) else x!r} (64 자 소문자 hex) · '
                    f'bytes {(x or {}).get("bytes") if isinstance(x, dict) else None!r} (정수 ≥ 0) · path (문자열)')
    met = inp.get('metrics')
    if not isinstance(met, dict) or any(k not in met or not _pos_or_none(met[k]) for k in BED_METRICS):
        return f'{label} 보고의 원 입력 metrics 꼴 {met!r} ({list(BED_METRICS)} = 유한 양수 또는 null)'
    if not _hex64(inp.get('settings_sha256')):
        return f'{label} 보고의 설정 지문 (inputs.settings_sha256) 꼴 {inp.get("settings_sha256")!r} (64 자 소문자 hex · payload 호출부)'
    ras = r.get('raster')
    if not isinstance(ras, dict) or not isinstance(ras.get('convention'), dict) or not _hex32(ras.get('sid_off_fp')):
        return (f'{label} 보고의 파생 격자 칸 (raster.convention · raster.sid_off_fp) 꼴 — sid_off_fp '
                f'{(ras or {}).get("sid_off_fp") if isinstance(ras, dict) else None!r} (32 자 소문자 hex · `carbon_junction._grid_fp`)')
    return None


def bed_view(inp):
    """원 입력 기록 (S0 보고 inputs · `ca_s0_census.kit_input_record`) → 경로 뺀 지문 {files: {역할: {sha256, bytes}} · metrics · settings_sha256}
    (경로 = 기계마다 다르다 · 대조 밖)."""
    i = inp if isinstance(inp, dict) else {}
    fs = i.get('files') if isinstance(i.get('files'), dict) else {}
    met = i.get('metrics') if isinstance(i.get('metrics'), dict) else {}
    return {'files': {str(k): ({'sha256': x.get('sha256'), 'bytes': x.get('bytes')} if isinstance(x, dict) else x) for k, x in sorted(fs.items())},
            'metrics': {k: met.get(k) for k in BED_METRICS}, 'settings_sha256': i.get('settings_sha256')}


def _bed_diff(want, got):
    out = [f'역할 {k}' for k in sorted(set(want['files']) | set(got['files'])) if want['files'].get(k) != got['files'].get(k)]
    out += [f'metrics {k}' for k in BED_METRICS if want['metrics'].get(k) != got['metrics'].get(k)]
    if want['settings_sha256'] != got['settings_sha256']:
        out.append('설정 (킷 run_mpm.sh 의 payload 호출부)')
    return out


def s0_records_key(recs):
    """단계끼리 대조할 S0 보고 기록 키 — 경로 문자열 (보고 경로 · 원 입력 파일 경로) 을 뺀 사본 (기계마다 다른 자리 · 대조 밖) · 그 밖 칸 그대로."""
    if not isinstance(recs, dict):
        return recs
    out = {}
    for k, r in recs.items():
        if not isinstance(r, dict):
            out[k] = r
            continue
        r2 = {kk: vv for kk, vv in r.items() if kk != 'path'}
        inp = r2.get('inputs')
        if isinstance(inp, dict) and isinstance(inp.get('files'), dict):
            r2['inputs'] = dict(inp, files={f: ({kk: vv for kk, vv in x.items() if kk != 'path'} if isinstance(x, dict) else x)
                                            for f, x in inp['files'].items()})
        out[k] = r2
    return out


def s0_same_convention(rec):
    """S0 보고 기록의 파생 칸 규약 = R 주 런 arm 0 규약 (`S0_GRID_CONVENTION`) 인가 — 같을 때만 off 격자 지문을 대조한다."""
    conv = ((rec or {}).get('raster') or {}).get('convention') if isinstance(rec, dict) else None
    if not isinstance(conv, dict):
        return False
    for k, want in S0_GRID_CONVENTION.items():
        got = conv.get(k)
        if isinstance(want, list):
            if not (isinstance(got, list) and len(got) == len(want) and all(_same(a, b) for a, b in zip(got, want))):
                return False
        elif isinstance(want, float):
            if not _same(got, want):
                return False
        elif got != want:
            return False
    return True


def s0_grid_seed(recs):
    """S0 보고 기록 (단계 1 · 2) → {sid 대조 무리 키: off 격자 지문} — 같은 규약 · 주 래스터 (vox 0.15 · 양보 없음 · FIBRE · UNREG 변이도
    같은 래스터) · arm 0 (origin 0) 만 (GRID · SVORDER · origin 팔 = 키가 달라 대조 안 함)."""
    out = {}
    for kit, st in BED_STAGE.items():
        r = (recs or {}).get(st) if isinstance(recs, dict) else None
        if isinstance(r, dict) and s0_same_convention(r) and _hex32((r.get('raster') or {}).get('sid_off_fp')):
            out[sid_group(kit, None, 0)] = r['raster']['sid_off_fp']
    return out


def _cnt(x):
    """0 이상 정수 · int64 범위 · bool 아님 (census 칸)."""
    return type(x) is int and 0 <= x < 2 ** 63                 # noqa: E721 — bool 제외


def s0_sv_census_problem(rec, stage, plan=None):
    """★ 10-25 묶음 B (X6 · 1저자 10-23 Q20 (가)) S0 보고 기록의 봉인 SV census → 꼴 문제 | None.  단계 1 = null (s_min 봉인 전) · 단계 2 = dict ·
    census 칸 = `ca_ext_svcf.CENSUS_KEYS` 정확히 · 0 이상 정수 · 못 가른 ≤ 다리 ≤ 닿는 (생산자 정의) · s_min · tol_ff = R 계획 (plan 이 있을 때 ·
    사슬 단계는 늘 넘긴다 · 같은 float)."""
    r = rec if isinstance(rec, dict) else {}
    sv = r.get('sv_census')
    if stage == 1:
        return None if sv is None else f'S0 단계 1 보고의 봉인 SV census = null 이어야 (s_min 봉인 전 · {type(sv).__name__})'
    if not isinstance(sv, dict):
        return f'S0 단계 2 보고에 봉인 SV census (sv_census) 가 없다 (옛 꼴 · {S0_REPORT_SCHEMA} 이전) — {BED_NEW_S0}'
    cen = sv.get('census')
    if not isinstance(cen, dict) or sorted(cen) != sorted(SVCF.CENSUS_KEYS) or not all(_cnt(cen[k]) for k in SVCF.CENSUS_KEYS):
        return f'S0 단계 2 봉인 SV census 꼴 {cen!r} (칸 = {list(SVCF.CENSUS_KEYS)} · 0 이상 정수)'
    nu, nb, nt = (cen[k] for k in SVCF.CENSUS_KEYS)
    if not nu <= nb <= nt:
        return f'S0 단계 2 봉인 SV census 못 가른 {nu} ≤ 다리 {nb} ≤ 닿는 {nt} 가 아니다 (생산자 정의 · `carbon_junction._sv_split`)'
    if plan is not None:
        for k in ('s_min_um', 'tol_ff_um'):
            a, b = sv.get(k), plan.get(k)
            if not (_num(a) and _num(b) and float(a) == float(b)):
                return f'S0 단계 2 봉인 SV census 의 {k} {a!r} ≠ R 계획 {b!r} (봉인 s_min · tol_ff 로 낸 census 여야 · R arm 0 와 같은 문턱)'
    return None


def s0_census_seed(recs):
    """S0 보고 기록 → {sid 대조 무리 키: 봉인 SV census} — 단계 2 (DBE) · 같은 규약 · 주 래스터 · arm 0 (`s0_grid_seed` 와 같은 키 규칙 · GRID ·
    SVORDER · origin 팔 = 키가 달라 대조 안 함)."""
    r = (recs or {}).get('stage2') if isinstance(recs, dict) else None
    if not (isinstance(r, dict) and s0_same_convention(r) and isinstance(r.get('sv_census'), dict)):
        return {}
    cen = r['sv_census'].get('census')
    if not (isinstance(cen, dict) and all(_cnt(cen.get(k)) for k in SVCF.CENSUS_KEYS)):
        return {}
    return {sid_group(DBE_KIT, None, 0): {k: cen[k] for k in SVCF.CENSUS_KEYS}}


def sv_census_problem(svr, ev_census, sealed):
    """★ 10-25 묶음 B (X6 · Q20 (가) · 2 차 사전 공격 §A) — SV 기록의 census 사본 · 증거 census (세 칸) = S0 단계 2 봉인 census → 문제 | None.
    기록 안 일관 (사본 = 증거) 은 기록 계약 (`ca_ext_svcf._census_problem`) 의 몫 · 이 함수 = 기록 밖 (S0 단계 2 · 같은 함수 · 같은 격자 · 봉인
    s_min) 과의 결합 — 기록 · 증거를 같이 고친 꼴을 잡는다.  기록 사본의 다리 · 닿는 칸이 없으면 (None) 기록 계약처럼 건너뛴다."""
    for k in SVCF.CENSUS_KEYS:
        w = sealed.get(k) if isinstance(sealed, dict) else None
        e = ev_census.get(k) if isinstance(ev_census, dict) else None
        if not (_cnt(e) and _cnt(w) and e == w):
            return f'증거 census {k} {e!r} ≠ S0 단계 2 봉인 SV census {w!r} (같은 함수 · 같은 격자 · 봉인 s_min — 10-25 X6)'
        v = svr.get(k) if isinstance(svr, dict) else None
        if v is None and k != 'n_unsplit_bridging_components':
            continue
        if not (_cnt(v) and v == w):
            return f'SV 기록의 census 사본 {k} {v!r} ≠ S0 단계 2 봉인 SV census {w!r} (10-25 X6)'
    return None


def kit_bed(root, kit):
    """지금 킷 (root/<킷>) → 경로 뺀 원 입력 지문 (`bed_view` · S0 와 같은 발견 함수 `ca_s0_census.kit_input_record` · 기계마다 자기 사본) ·
    킷 폴더 없음 = Stop KIT_MISSING · 못 읽음 = Stop S0_REPORT_MISMATCH (확인 못 함 = 멈춤)."""
    kp = Path(root) / kit
    if not kp.is_dir():
        raise Stop('KIT_MISSING', f'{kp}')
    import ca_s0_census as _s0
    try:
        rec = _s0.kit_input_record(str(kp), vox=VOX_MAIN, bridge_um=MAN_FIXED['bridge_um'], sdcp_sphere_d=MAN_FIXED['sdcp_sphere_d_um'])
    except Exception as e:                                    # noqa: BLE001 — S0Error · OSError · 그 밖 = 확인 못 함 = 멈춤
        raise Stop('S0_REPORT_MISMATCH', f'{kit}: S0 발견 함수가 킷을 읽지 못했다 ({type(e).__name__}: {e}) — 확인 못 함 = 멈춤 · {BED_NEW_S0}')
    return bed_view(rec)


def bed_problem(recs, root, kits):
    """R 직전 (사다리 = SBE · 예측 = SBE · DBE) · 판정 (둘 다) — S0 보고 기록의 원 입력 (경로 뺀 지문) = 지금 킷 (`kit_bed`) → {킷: 지문} ·
    다르면 Stop S0_REPORT_MISMATCH (사유 = 다른 칸 · 새 S0)."""
    out = {}
    for kit in kits:
        st = BED_STAGE[kit]
        got = kit_bed(root, kit)
        out[kit] = got
        want = bed_view(((recs or {}).get(st) or {}).get('inputs') if isinstance(recs, dict) else None)
        if got != want:
            raise Stop('S0_REPORT_MISMATCH', f'S0 단계 {st[-1]} 보고의 침대 ≠ 지금 킷 {kit} ({" · ".join(_bed_diff(want, got))}) — {BED_NEW_S0}')
    return out


def s0_stage2_problem(rec, plan_sha, s0_sha, plan=None):
    """★ PF2 B (10-22 · 사전 리뷰 2 회차 PRE2-design-01 · 탐침 E · 1저자 Q2 권고대로 · 등록 R §2-1 · §2-1b · §11 ④) — 단계 2 기록 → 문제 | None.
    단계 2 (DBE 열람) 의 인자 커밋이 봉인한 계획 해시 = 지금 쓰는 두 계획의 sha256 (**정확히**): `r_plan_sha256` = R 계획 (`--plan`) ·
    `plan_sha256` = S0 계획 (`--s0-plan`) · 꼴 = 이 도구의 S0 보고 (schema · 단계 2 · DBE 새 침대 · source commit:<sha>).  DBE 를 본 뒤 계획을
    다시 등록하면 (s_min · 결과 전 숫자 · maxiter · 계획 B) 여기서 멈춘다 (옛 사슬 = 단계 2 보고를 읽지 않아 계획 B 로 CALIBRATED)."""
    r = rec if isinstance(rec, dict) else {}
    if r.get('schema') != S0_REPORT_SCHEMA or type(r.get('stage')) is not int or r.get('stage') != 2:   # noqa: E721 — bool 제외
        return f'S0 단계 2 보고 꼴 — schema {r.get("schema")!r} · 단계 {r.get("stage")!r} (= {S0_REPORT_SCHEMA!r} · 2)'
    if r.get('kit') != DBE_KIT:
        return f'S0 단계 2 보고의 킷 {r.get("kit")!r} ≠ {DBE_KIT!r} (R 런 DBE 침대의 보고여야)'
    if not (isinstance(r.get('plan_source'), str) and _PLAN_SOURCE_RE.fullmatch(r['plan_source'])):
        return (f'S0 단계 2 보고의 계획 출처 {r.get("plan_source")!r} — commit:<40 자 소문자 hex> 이어야 (단계 2 의 인자 커밋 전체 sha · '
                f'★ 10-25 판정문 F5 · 옛 = commit: 접두만)')
    if not (_hex64(r.get('r_plan_sha256')) and _hex64(r.get('plan_sha256'))):
        return f'S0 단계 2 보고의 봉인 계획 해시 꼴 — R 계획 {r.get("r_plan_sha256")!r} · S0 계획 {r.get("plan_sha256")!r} (64 자 소문자 hex)'
    if r['r_plan_sha256'] != plan_sha:
        return (f'S0 단계 2 가 봉인한 R 계획 {r["r_plan_sha256"][:16]}… ≠ 지금 R 계획 {str(plan_sha)[:16]}… — DBE 를 본 뒤 계획을 다시 등록했다 '
                f'(Q2: 계획 하나 · 바꾸려면 새 등록 · 등록 R §2-1b)')
    if r['plan_sha256'] != s0_sha:
        return f'S0 단계 2 가 봉인한 S0 계획 {r["plan_sha256"][:16]}… ≠ 지금 S0 계획 {str(s0_sha)[:16]}…'
    why = s0_bed_record_problem(r, 'S0 단계 2') or s0_sv_census_problem(r, 2, plan)   # ★ 10-25 묶음 B (RCA2-03 · X6) — 같은 침대 · 봉인 census
    if why:
        return why
    return plan_commit_problem(r['plan_source'], r.get('r_plan_path'), r['r_plan_sha256'])


_PLAN_SOURCE_RE = re.compile(r'commit:([0-9a-f]{40})')


def _repo_rel_ok(p):
    """리포 상대 ASCII 경로 (S0 단계 2 관문 `verify_plan_commit` 의 경로 규칙과 같은 뜻 — 절대 · .. · 공백 · 역빗금 · 드라이브 문자 거부)."""
    return (isinstance(p, str) and bool(p) and not p.startswith('/') and '\\' not in p and '..' not in p.split('/') and p.isascii()
            and re.search(r'\s', p) is None and re.match(r'[A-Za-z]:', p) is None)


def plan_commit_problem(src, rel, want):
    """★ 10-25 묶음 B (판정문 §9 F5 · 1저자 10-23 Q2 (가) ⑥) — S0 단계 2 보고의 계획 출처 → 문제 | None.  문법 = `commit:` + 40 자 소문자 hex ·
    그 커밋 (이 사슬 저장소 = HERE 의 git) 안 R 계획 파일 (보고의 r_plan.path · 리포 상대) 의 blob sha256 = R 계획 sha256 (= 지금 --plan · 앞 대조가
    같음을 확인).  커밋이 HEAD 의 조상인지는 S0 단계 2 관문이 그 판에서 확인했다 (여기 = 커밋 존재 · blob).  옛 = `commit:` 접두만 ('commit:' 도
    통과 · 커밋 · blob 을 안 봤다).  S0 계획의 리포 안 경로는 보고에 없다 (그 blob 대조는 이 함수 밖 · 보고 "결정 필요")."""
    m = _PLAN_SOURCE_RE.fullmatch(src) if isinstance(src, str) else None
    if m is None:
        return f'S0 단계 2 보고의 계획 출처 {src!r} — commit:<40 자 소문자 hex> 이어야 (F5)'
    if not _repo_rel_ok(rel):
        return f'S0 단계 2 보고의 R 계획 경로 {rel!r} — 리포 상대 ASCII 경로여야 (절대 · .. · 공백 금지 · F5)'
    sha = m.group(1)
    try:
        r = subprocess.run(['git', '-C', str(HERE), 'cat-file', '-e', f'{sha}^{{commit}}'], capture_output=True)
        if r.returncode != 0:
            return (f'S0 단계 2 보고의 계획 출처 커밋 {sha[:12]} 이 이 사슬 저장소에 없다 (git fetch 뒤 · git 밖 사본 = 확인 못 함 · 미확인 = '
                    f'멈춤 · F5)')
        r = subprocess.run(['git', '-C', str(HERE), 'show', f'{sha}:{rel}'], capture_output=True)
        if r.returncode != 0:
            return f'커밋 {sha[:12]} 에 R 계획 파일 {rel} 이 없다 (F5)'
        got = hashlib.sha256(r.stdout).hexdigest()
    except Exception as e:                                    # noqa: BLE001 — 확인 못 함 = 미확인 = 멈춤
        return f'계획 출처 커밋을 git 으로 확인하지 못했다 ({type(e).__name__}: {e}) — 미확인 = 멈춤 (F5)'
    if got != want:
        return f'커밋 {sha[:12]} 의 {rel} blob sha256 {got[:16]}… ≠ R 계획 sha256 {str(want)[:16]}… — 그 커밋이 봉인한 계획이 아니다 (F5)'
    return None


def s0_stage1_problem(rec, s0_sha):
    """★ PF2 D (10-22 · 사전 리뷰 2 회차 PRE2-design-08 · 결정 없음 · 등록 R §2-1b) — 단계 1 기록 → 꼴 문제 | None.  꼴 = 이 도구의 S0 단계 1
    보고 (schema · 단계 1 · SBE 새 침대 · source stage1_computed) · 그 보고가 만든 S0 계획 sha256 = 지금 S0 계획 (`--s0-plan` · 등록 §2-1 S0 계획
    해시 칸 — 이 등록의 단계 1 보고여야 그 census · registry 지문이 s_min 을 고른 판이다)."""
    r = rec if isinstance(rec, dict) else {}
    if r.get('schema') != S0_REPORT_SCHEMA or type(r.get('stage')) is not int or r.get('stage') != 1:   # noqa: E721 — bool 제외
        return f'S0 단계 1 보고 꼴 — schema {r.get("schema")!r} · 단계 {r.get("stage")!r} (= {S0_REPORT_SCHEMA!r} · 1)'
    if r.get('kit') != SBE_KIT:
        return f'S0 단계 1 보고의 킷 {r.get("kit")!r} ≠ {SBE_KIT!r} (S0 계획을 만든 SBE 새 침대의 보고여야)'
    if r.get('plan_source') != S0_STAGE1_SOURCE:
        return f'S0 단계 1 보고의 계획 출처 {r.get("plan_source")!r} (= {S0_STAGE1_SOURCE!r} 이어야 — 그 침대에서 계획을 만든 보고)'
    if not _hex64(r.get('plan_sha256')):
        return f'S0 단계 1 보고의 계획 해시 꼴 {r.get("plan_sha256")!r} (64 자 소문자 hex)'
    if r['plan_sha256'] != s0_sha:
        return f'S0 단계 1 보고가 만든 S0 계획 {r["plan_sha256"][:16]}… ≠ 지금 S0 계획 {str(s0_sha)[:16]}… (이 등록의 단계 1 보고가 아니다)'
    return s0_bed_record_problem(r, 'S0 단계 1') or s0_sv_census_problem(r, 1)   # ★ 10-25 묶음 B (RCA2-03 · X6) — 같은 침대 칸 · 봉인 census null


def _digest_map(lst):
    """코드 파일 지문 목록 [{file, sha256}] → {이름: sha256} (꼴이 틀린 줄은 버린다 — 대조는 이름별 값으로 · 빈 값 = None)."""
    out = {}
    for x in (lst if isinstance(lst, list) else ()):
        if isinstance(x, dict) and isinstance(x.get('file'), str):
            out[x['file']] = x.get('sha256')
    return out


def s0_code_problem(rec, label, files, runner_files=None):
    """★ PF2 D (10-22 · PRE2-design-08 · 등록 R §2-1b) — S0 보고 기록의 census · registry 일곱 파일 지문 (`file_digests`) = 지금 R 런 코드 →
    문제 | None.  지금 = 사슬 폴더 지문 (`files` · 일곱 다 있어야) · 러너 폴더 지문 (`runner_files` · 그 폴더에 있는 것만 — 없는 파일은 러너가
    돌릴 수 없다).  보고의 git_dirty 는 보지 않는다 (지문 = 파일 내용 그대로 · 등록 문장은 같은 코드를 요구한다)."""
    r = rec if isinstance(rec, dict) else {}
    fd = r.get('file_digests')
    if not isinstance(fd, list) or not all(isinstance(x, dict) for x in fd):
        return f'{label} 보고의 code.file_digests 꼴 {type(fd).__name__} (파일 지문 목록이어야) — {S0_RERUN}'
    rep = {}
    for x in fd:
        if x.get('file') in rep:
            return f'{label} 보고의 code.file_digests 에 {x.get("file")!r} 가 두 번 — {S0_RERUN}'
        rep[x.get('file')] = x.get('sha256')
    here, there = _digest_map(files), _digest_map(runner_files)
    for nm in S0_SAME_FILES:
        want = rep.get(nm)
        if not _hex64(want):
            return (f'{label} 보고에 {nm} 지문이 없다 · 꼴 {want!r} (옛 다섯 파일 보고 = carbon_junction.py · ptfe_face_alpha.py 없음) — '
                    f'{S0_RERUN}')
        if here.get(nm) != want:
            return f'{label} 보고의 {nm} 지문 {want[:16]}… ≠ 지금 사슬 폴더 {str(here.get(nm))[:16]}… — {S0_RERUN}'
        if there.get(nm) is not None and there[nm] != want:
            return f'{label} 보고의 {nm} 지문 {want[:16]}… ≠ 지금 러너 폴더 {str(there[nm])[:16]}… — {S0_RERUN}'
    return None


def read_s0_report(path, stage):
    """사다리 — `--s0-stage<n>-report` 파일 → 기록 (`s0_report_record` · 검사는 `s0_reports_problem`) · 못 읽음 = Stop S0_REPORT_MISMATCH."""
    try:
        raw = Path(path).read_bytes()
        rep = _json_strict(raw)                               # ★ PF2 E — 중복 칸 거부 (사람 = 앞 · 해석기 = 뒤 로 달리 읽지 않게)
    except (OSError, UnicodeDecodeError, ValueError, TypeError) as e:
        raise Stop('S0_REPORT_MISMATCH', f'S0 단계 {stage} 보고 {path}: {type(e).__name__}: {e}')
    return s0_report_record(rep, hashlib.sha256(raw).hexdigest(), str(Path(path).resolve()))


def s0_reports_problem(recs, plan_sha, s0_sha, files, runner_files=None, plan=None):
    """사다리 · 예측 · 판정 (같은 함수) — 단계 요약의 S0 보고 기록 → (멈춤 이름, 문제) | None.  단계 2 = 봉인 계획 해시 (PF2 B) · 단계 1 = 꼴 ·
    S0 계획 (PF2 D) → S0_REPORT_MISMATCH · 두 보고의 census · registry 일곱 파일 지문 = 지금 코드 (`files` · `runner_files`) → CODE_PIN_MISMATCH.
    기록 없음 = 그 보고 없이 돈 단계 · 옛 요약 = 대조 불가 → 멈춤."""
    if not isinstance(recs, dict) or not isinstance(recs.get('stage2'), dict):
        return 'S0_REPORT_MISMATCH', 'S0 단계 2 보고 기록이 없다 (--s0-stage2-report 없이 돈 단계 · 옛 요약 — 봉인 계획 해시를 대조할 수 없다)'
    why = s0_stage2_problem(recs['stage2'], plan_sha, s0_sha, plan)
    if why:
        return 'S0_REPORT_MISMATCH', why
    if not isinstance(recs.get('stage1'), dict):
        return ('S0_REPORT_MISMATCH', 'S0 단계 1 보고 기록이 없다 (--s0-stage1-report 없이 돈 단계 · 옛 요약 — census · registry 지문을 대조할 수 '
                                      '없다)')
    why = s0_stage1_problem(recs['stage1'], s0_sha)
    if why:
        return 'S0_REPORT_MISMATCH', why
    for k, label in (('stage1', 'S0 단계 1'), ('stage2', 'S0 단계 2')):
        why = s0_code_problem(recs[k], label, files, runner_files)
        if why:
            return 'CODE_PIN_MISMATCH', why
    return None


# ═════════════════════════ ★ PF2 D (10-22) 같은 판 — 코드 파일 지문 · 추적 파일 수정 여부 ═════════════════════════
def code_files(base):
    """base 폴더의 CODE_FILES → [{file, sha256 | None}] (CODE_FILES 순서 · 없는 파일 · 못 읽는 파일 = None)."""
    out = []
    for nm in CODE_FILES:
        p = Path(base) / nm
        try:
            h = sha256_file(p) if p.is_file() else None
        except OSError:
            h = None
        out.append({'file': nm, 'sha256': h})
    return out


def code_record(runner):
    """단계 요약의 code 칸 — 사슬 · 러너 git 신원 (HEAD · dirty · 저장소 상대 경로 rel · 미확인 사유) · 러너 경로 (절대 · 기록만 · 키 아님) + 코드
    파일 지문 (사슬 폴더 `files` · 러너 폴더 `runner_files` · 러너 파일 sha256) + ★ 10-25 묶음 B 환경 지문 (`env` · `env_record`).  운영 = 사슬과
    러너가 한 핀 작업 트리 (등록 R §10 (0)) 라 두 폴더 지문이 같다 (한 단계 안 대조 = `code_dirty_problem`)."""
    rec = {'chain': git_identity(HERE / 'rint_r_chain.py'), 'runner': None, 'runner_path': None, 'files': code_files(HERE),
           'runner_files': None, 'runner_sha256': None, 'env': env_record()}
    if runner:
        rp = Path(runner).resolve()
        rec.update({'runner': git_identity(runner), 'runner_path': str(rp), 'runner_files': code_files(rp.parent),
                    'runner_sha256': (sha256_file(rp) if rp.is_file() else None)})
    return rec


def code_key(rec):
    """단계끼리 · 지금과 대조하는 코드 칸 (정준 JSON 글).  ★ 10-25 묶음 B (RCA2-02 · 1저자 10-23 Q2 (가) ④ ⑤ · C6 #14 · Q9 설계 개정 1 D6 ·
    개정 4 R4-10 · R4-12) — 사슬 · 러너 HEAD · 저장소 상대 경로 (rel) · 코드 파일 지문 (사슬 폴더 · 러너 폴더 · 이름 = CODE_FILES) · 러너 sha256 ·
    환경 지문 같음 단위 (`env_unit`).  절대 경로 (러너 경로 · 체크아웃 자리 · 옛 키의 `runner_path`) 는 키에 없다 (기계마다 다르다 · 경로만 다른
    같은 코드 = 같은 키) · 기계 이름표 · dirty · 환경 기록만 칸도 없다 (dirty · 미확인 = `code_dirty_problem` 이 따로 멈춘다)."""
    r = rec if isinstance(rec, dict) else {}
    ch = r.get('chain') if isinstance(r.get('chain'), dict) else {}
    ru = r.get('runner') if isinstance(r.get('runner'), dict) else {}
    pick = {'chain_head': ch.get('head'), 'runner_head': ru.get('head'), 'chain_rel': ch.get('rel'), 'runner_rel': ru.get('rel'),
            'files': r.get('files'), 'runner_files': r.get('runner_files'), 'runner_sha256': r.get('runner_sha256'),
            'env_unit': env_unit(r.get('env'))}
    return json.dumps(pick, sort_keys=True, ensure_ascii=False, default=repr)


def code_key_diff(a, b):
    """두 code 기록의 코드 키에서 다른 칸 (멈춤 사유용) — HEAD · 저장소 상대 경로 · 러너 sha256 · 환경 같음 단위 칸 · 다른 파일 이름."""
    ka, kb = json.loads(code_key(a)), json.loads(code_key(b))
    out = [k for k in ('chain_head', 'runner_head', 'chain_rel', 'runner_rel', 'runner_sha256') if ka.get(k) != kb.get(k)]
    if ka.get('env_unit') != kb.get('env_unit'):
        ea, eb = ka.get('env_unit') or {}, kb.get('env_unit') or {}
        out += [f'환경 {k} {ea.get(k)!r} ≠ {eb.get(k)!r}' for k in ENV_UNIT_KEYS if ea.get(k) != eb.get(k)] or ['환경 지문 (미확인)']
    for fk in ('files', 'runner_files'):
        if ka.get(fk) != kb.get(fk):
            out += [f'{fk} {n}' for n in code_diff_names(ka.get(fk), kb.get(fk))]
    return out or ['같음']


def _identity_problem(g, nm):
    """git 신원 하나 → 문제 | None (★ 10-25 · Q2 (가) ① ② — HEAD 40-hex · dirty 엄격한 False · 기록 없음 · 미확인 = 멈춤)."""
    if not isinstance(g, dict):
        return f'{nm} git 신원 기록이 없다 (옛 요약 · 꼴) — 미확인 = 멈춤 (RCA2-02 · Q2 (가) ①)'
    if not _hex40(g.get('head')):
        return (f'{nm} git HEAD 미확인 (head {g.get("head")!r} · {g.get("error")}) — git 밖 사본 · 조회 실패 = 미확인 = 멈춤 (핀 커밋의 git '
                f'체크아웃에서 돌릴 것 · RCA2-02 · Q2 (가) ① · C6 #13)')
    if g.get('dirty') is True:
        return (f'{nm} 작업 트리에 고쳐진 추적 파일 · ignore 밖 추적 안 된 파일이 있다 (dirty · HEAD {g["head"]}) — 핀 커밋 그대로의 깨끗한 트리에서 '
                f'돌릴 것 (등록 R §10 (0) · Q2 (가) ② (가-1))')
    if g.get('dirty') is not False:
        return (f'{nm} 작업 트리 상태 미확인 (dirty {g.get("dirty")!r} · {g.get("error")}) — git status 실패 = 미확인 = 멈춤 (깨끗함으로 바꾸지 '
                f'않는다 · RCA2-02 · Q2 (가) ① · C6 #13)')
    return None


def code_dirty_problem(rec):
    """같은 코드 관문 (이름은 옛 그대로) — 단계 code 기록 → 문제 | None.  ★ 10-25 묶음 B (RCA2-02 · 1저자 10-23 Q2 (가) ① ② ③ ⑤ · 판정문 F1 ·
    F2): ① 사슬 · 러너 git 신원 = HEAD 40-hex · dirty 엄격한 False (조회 실패 · git 밖 · 기록 없음 = 미확인 = 멈춤 · 옛 = dirty True 만 멈추고
    None 은 기록만) ② dirty = 추적 파일 고침 + ignore 밖 추적 안 된 파일 (`git_identity`) ③ 한 단계 안 사슬 ↔ 러너 — HEAD 같음 · 사슬 폴더 ·
    러너 폴더 코드 파일 지문 같음 · 러너 파일 = 사슬 폴더의 러너 (자기 요약끼리 비교 아님 · 옛 = 단계끼리만) ⑤ 환경 지문 같음 단위 셋이 다
    있어야 (미확인 = 멈춤 · 단계끼리 · 지금과의 같음 = 코드 키)."""
    r = rec if isinstance(rec, dict) else {}
    for k, nm in (('chain', '사슬'), ('runner', '러너')):
        why = _identity_problem(r.get(k), nm)
        if why:
            return why
    ch, ru = r['chain'], r['runner']
    fa, fr = r.get('files'), r.get('runner_files')
    bad = []
    if ch['head'] != ru['head']:
        bad.append(f'HEAD 사슬 {ch["head"][:12]} ≠ 러너 {ru["head"][:12]}')
    if not isinstance(fa, list) or fa != fr:
        bad.append('러너 폴더 코드 파일 지문 ≠ 사슬 폴더 (' + ', '.join(code_diff_names(fa, fr)) + ')')
    want = _digest_map(fa).get(RUNNER_NAME)
    if not _hex64(r.get('runner_sha256')) or r.get('runner_sha256') != want:
        bad.append(f'러너 파일 sha256 {str(r.get("runner_sha256"))[:16]}… ≠ 사슬 폴더의 {RUNNER_NAME} {str(want)[:16]}…')
    if bad:
        return ('한 단계 안 사슬 ↔ 러너가 다른 판이다 — ' + ' · '.join(bad) + ' (같은 핀 체크아웃의 사슬 · 러너로 돌릴 것 · RCA2-02 · '
                'Q2 (가) ③ · 판정문 F2)')
    if env_unit(r.get('env')) is None:
        u = r['env'].get('unit') if isinstance(r.get('env'), dict) else None
        return (f'환경 지문 미확인 — 같음 단위 (python 부 판 · numpy · scipy 판) {u!r} (옛 요약 · 불러오기 실패 = 미확인 = 멈춤 · RCA2-02 · '
                f'Q2 (가) ⑤)')
    return None


def code_diff_names(a, b):
    """두 코드 파일 지문 목록에서 다른 이름 (멈춤 사유용 · 이름별 값이 다 같으면 = 꼴 · HEAD · 러너 칸이 다르다)."""
    da, db = _digest_map(a), _digest_map(b)
    return sorted(k for k in set(da) | set(db) if da.get(k) != db.get(k)) or ['이름별 지문 같음 — 꼴 · HEAD · 러너 칸이 다르다']


def code_verdict_problem(rec, label):
    """판정 계산기 — 지금 사슬 쪽 코드 ↔ 단계 기록 → 문제 | None (git 신원 · HEAD · 사슬 폴더 코드 파일 지문).  러너 쪽 지금 상태는 보지 않는다
    (판정은 러너를 돌리지 않는다 · 단계끼리의 러너 지문 대조 = 판정 입력 검사 `code_key`).  ★ 10-25 묶음 B (RCA2-02 · Q2 (가) ① ②) — 지금 사슬
    git 신원도 엄격 (HEAD 40-hex · dirty 엄격한 False · 미확인 = 멈춤 · 옛 = dirty True 만) · 판정 프로세스의 환경 지문은 대조하지 않는다 (R4-11 —
    다른 플랫폼의 다시 판정 · 판정은 풀이를 하지 않는다)."""
    now = git_identity(HERE / 'rint_r_chain.py')
    why = _identity_problem(now, '지금 사슬')
    if why:
        return f'{why} — 판정 계산기도 깨끗한 핀 git 체크아웃에서 (등록 R §10 (0))'
    r = rec if isinstance(rec, dict) else {}
    head = r['chain'].get('head') if isinstance(r.get('chain'), dict) else None
    if now.get('head') != head:
        return f'지금 사슬 HEAD {now.get("head")} ≠ {label} 를 만든 사슬 {head} — 판정 계산기도 같은 핀에서 (다시 판정 = 같은 코드)'
    files = code_files(HERE)
    if files != r.get('files'):
        return (f'지금 사슬 폴더 코드 파일 지문 ≠ {label} 기록 ({", ".join(code_diff_names(files, r.get("files")))}) — 같은 HEAD 라도 파일이 다르면 '
                f'판정하지 않는다')
    return None


# ═════════════════════════ 팔 읽기 · 계약 (런 하나 = 폴더 하나) ═════════════════════════
def expected_request(req, plan):
    """러너에 요청한 다음 세대 선언 (영수증 `ca_ext_request` 와 매니페스트 protocol 이 같아야 한다).
    ★ Z3 — 극한 런 = 러너 꼴 (`run_contract.runner_ca_ext`): 바닥 `R_j_ohm` null + `rj_limit` 'inf' · 천장 0.0 + 'zero' (정량 런엔 칸 없음)."""
    rj = req['rj']
    unreg = 'fused' if req['variant'] == 'UNREG' else plan['unreg_law']
    cj = {'R_j_ohm': (None if rj == 'inf' else rj_float(rj)), 'len_law': plan['len_law'], 'unreg_law': unreg,
          's_min_um': float(plan['s_min_um']), 'tol_ff_um': float(plan['tol_ff_um']), 'ptfe_jlaw': req['law']}
    if rj in LIMIT_MARK:
        cj['rj_limit'] = LIMIT_MARK[rj]
    out = {'cjunc': cj}
    if req['c'] != '':
        out['sdcp_mod'] = {'c': float(req['c'])}
    return out


def _solve_ran(state, cert):
    """그 해에서 CG 가 돌았나 — 양의 해 · 행렬 그래프 영값 (조기 반환 영값 · 단락 = 솔브 없음)."""
    return state == 'positive' or (state == 'zero' and (cert or {}).get('zero_source') == 'matrix_graph')


def manifest_problems(man, rcpt, req, plan, idx, cert, state='positive'):
    """매니페스트 · 영수증 ↔ 요청 (§10 멈춤 '매니페스트 ≠ 요청') → 문제 목록."""
    var = req['variant']
    vox = variant_vox(var)
    bulk = FIBRE_BULK_DIV10 if var == 'FIBRE' else FIBRE_BULK
    yv = var == 'SVORDER'
    bad = []

    def num(k, want, r=1e-9):
        if not _same(man.get(k), want, r):
            bad.append(f'{k} {man.get(k)!r} ≠ {want!r}')

    def eq(k, want):
        if not (type(man.get(k)) is type(want) and man.get(k) == want):   # noqa: E721 — bool ↔ int 섞임 거부
            bad.append(f'{k} {man.get(k)!r} ≠ {want!r}')
    num('vox_um', vox)
    for k, v in MAN_FIXED.items():
        num(k, v)
    num('sigma_vgcf_S_cm', bulk * math.pi * VGCF_D_UM ** 2 / (4.0 * vox * vox), 1e-5)   # 직경 보존 (러너 %.6g)
    eq('ptfe_stamp', 'face_alpha')
    eq('sdcp_stamp', 'sphere')
    eq('fibre_stamp', 'segment')
    eq('periodic_xy', False)
    eq('sdcp_yield_to_vgcf', yv)
    o = man.get('origin_shift_um')
    want_o = origins_for(vox)[idx]
    if not (isinstance(o, list) and len(o) == 3 and all(_same(a, b, 1e-9) or (a == 0 and b == 0) for a, b in zip(o, want_o))):
        bad.append(f'origin_shift_um {o!r} ≠ arm {idx} {list(want_o)!r}')
    if man.get('component_plan') != LEAN2_PLAN:
        bad.append(f'component_plan {man.get("component_plan")!r} ≠ LEAN 2 {LEAN2_PLAN}')
    want_req = expected_request(req, plan)
    if man.get(RC.CA_EXT_REQUEST_FIELD) != sorted(want_req):
        bad.append(f'{RC.CA_EXT_REQUEST_FIELD} {man.get(RC.CA_EXT_REQUEST_FIELD)!r} ≠ {sorted(want_req)}')
    ca = man.get('ca_ext') if isinstance(man.get('ca_ext'), dict) else {}
    want_blk = {'schema', 'ptfe_face'} | set(want_req)
    if set(ca) != want_blk:
        bad.append(f'ca_ext 하위 블록 {sorted(ca)} ≠ {sorted(want_blk)}')
    cjb = ca.get('cjunc') if isinstance(ca.get('cjunc'), dict) else {}
    cjp = cjb.get('protocol') if isinstance(cjb.get('protocol'), dict) else {}
    lim = LIMIT_MARK.get(req['rj'])
    if lim:
        if not (cjp.get('rj_limit') == lim and cjp.get('allow_rj_limits') is True and cjp.get('quantitative') is False):
            bad.append(f'극한 런 ({lim}) 표지 — rj_limit {cjp.get("rj_limit")!r} · allow_rj_limits {cjp.get("allow_rj_limits")!r} · '
                       f'quantitative {cjp.get("quantitative")!r}')
        if lim == 'zero' and not (type(cjp.get('R_j_ohm')) is float and cjp.get('R_j_ohm') == 0.0):   # noqa: E721
            bad.append(f'천장 R_j_ohm {cjp.get("R_j_ohm")!r} ≠ 0.0')
        if lim == 'inf' and cjp.get('R_j_ohm') is not None:
            bad.append(f'바닥 R_j_ohm {cjp.get("R_j_ohm")!r} ≠ null (JSON 은 inf 를 못 쓴다 · 표지 inf 와 한 꼴)')
    else:
        if not (cjp.get('allow_rj_limits') is False and cjp.get('quantitative') is True and 'rj_limit' not in cjp):
            bad.append('정량 런인데 극한 표지가 있다')
        if not _same(cjp.get('R_j_ohm'), rj_float(req['rj'])):
            bad.append(f'cjunc.R_j_ohm {cjp.get("R_j_ohm")!r} ≠ {req["rj"]}')
    for k in ('len_law', 'unreg_law', 's_min_um', 'tol_ff_um', 'ptfe_jlaw'):
        if not _same(cjp.get(k), want_req['cjunc'][k]):
            bad.append(f'cjunc.{k} {cjp.get(k)!r} ≠ {want_req["cjunc"][k]!r}')
    for k, v in (('ptfe_stamp', 'face_alpha'), ('L_par_um', L_PAR_UM), ('r_port_um', R_PORT_UM)):
        if not _same(cjp.get(k), v):
            bad.append(f'cjunc.{k} {cjp.get(k)!r} ≠ {v!r}')
    if 'sdcp_mod' in want_req:
        cv = (((ca.get('sdcp_mod') or {}).get('protocol') or {}) if isinstance(ca.get('sdcp_mod'), dict) else {}).get('c')
        if not _same(cv, want_req['sdcp_mod']['c']):
            bad.append(f'sdcp_mod.c {cv!r} ≠ {req["c"]}')
    #  ★ 3판 — 수렴 증서 rtol = 계획 (CG 가 돈 해만 · 조기 반환 영값 · 단락 증서엔 rtol 칸이 없다 → 영수증 rtol 로 결합)
    if _solve_ran(state, cert) and not _same((cert or {}).get('rtol_used'), float(plan['step3_rtol'])):
        bad.append(f'증서 rtol_used {(cert or {}).get("rtol_used")!r} ≠ 계획 {plan["step3_rtol"]!r}')
    #  ★ 3판 — SV 반사실 요청 (사슬이 정한 런만 · producer 문턱 = None · 문턱은 이 사슬의 계획)
    want_cf = bool(req.get('sv_cf'))
    cjev = cjb.get('evidence') if isinstance(cjb.get('evidence'), dict) else {}
    if ('sv_counterfactual_request' in cjev) != want_cf:
        bad.append(f'접합 증거의 SV 반사실 요청 {"있음" if "sv_counterfactual_request" in cjev else "없음"} ≠ 사슬 요청 {want_cf}')
    elif want_cf and cjev.get('sv_counterfactual_request') != {'threshold': None}:
        bad.append(f'SV 반사실 요청 {cjev.get("sv_counterfactual_request")!r} ≠ {{"threshold": None}} (문턱 = 사슬 계획)')
    # 영수증 (러너가 무엇으로 돌라고 했나) ↔ 요청
    if not isinstance(rcpt, dict):
        bad.append('run_receipt.json 이 없다')
        return bad
    rq = rcpt.get('ca_ext_request')
    if not isinstance(rq, dict) or sorted(rq) != sorted(want_req) or any(
            not isinstance(rq.get(s), dict) or set(rq[s]) != set(want_req[s]) or not all(_same(rq[s][k], v) for k, v in want_req[s].items())
            for s in want_req):
        bad.append(f'영수증 ca_ext_request {rq!r} ≠ 요청 {want_req!r}')
    if not _same(rcpt.get('step3_rtol'), float(plan['step3_rtol'])):
        bad.append(f'영수증 step3_rtol {rcpt.get("step3_rtol")!r} ≠ 계획 {plan["step3_rtol"]!r}')
    if (rcpt.get('sv_counterfactual') is True) != want_cf or ('sv_counterfactual' in rcpt and rcpt.get('sv_counterfactual') is not True):
        bad.append(f'영수증 sv_counterfactual {rcpt.get("sv_counterfactual")!r} ≠ 사슬 요청 {want_cf}')
    for k, v in (('arms', req['arms']), ('ptfe_stamp', 'face_alpha'), ('vox_um', vox), ('sdcp_yield_to_vgcf', yv),
                 ('expect_backend', EXPECT_BACKEND)):
        if not _same(rcpt.get(k), v):
            bad.append(f'영수증 {k} {rcpt.get(k)!r} ≠ {v!r}')
    al = req.get('arm_list')                                  # ★ Z3 — 팔 고르기 런 = 영수증 arm_list (정렬 목록) · 아닌 런 = 칸 없음
    if (al is None and 'arm_list' in rcpt) or (al is not None and rcpt.get('arm_list') != list(al)):
        bad.append(f'영수증 arm_list {rcpt.get("arm_list")!r} ≠ 요청 {al!r}')
    if 'sigma_vgcf_S_cm' in rcpt:
        bad.append(f'영수증이 σ_VGCF 를 직접 정했다 ({rcpt["sigma_vgcf_S_cm"]!r} · SIGMA_VGCF_OVERRIDE 세대)')
    ok, why = RC.receipt_match(rcpt, man, origin=man.get('origin_shift_um'))
    if not ok:
        bad.append(f'영수증 ↔ 매니페스트 {why}')
    return bad


def lean_problems(man, state='positive', s3=None):
    """솔브 영수증 ↔ LEAN 2 표 (설계 §7) — ★ 3판: 조기 반환 해 (영값 위상 · 단락) 는 주 솔브 영수증 = failed (사유 = 결과 사유)."""
    s3 = s3 if isinstance(s3, dict) else {}
    early = state == 'short' or (state == 'zero' and (s3.get('conv_cert') or {}).get('zero_source') == 'early_return')
    ca = man.get('ca_ext') if isinstance(man.get('ca_ext'), dict) else {}
    bad = []
    for sub in ('ptfe_face', 'cjunc'):
        rc_ = ((ca.get(sub) or {}).get('evidence') or {}).get('receipts') if isinstance(ca.get(sub), dict) else None
        if not isinstance(rc_, dict) or set(rc_) != set(LEAN2_RECEIPTS):
            bad.append(f'{sub} 영수증 키 {sorted(rc_) if isinstance(rc_, dict) else rc_!r}')
            continue
        for name, ok_st in LEAN2_RECEIPTS.items():
            r = rc_.get(name) if isinstance(rc_.get(name), dict) else {}
            if name == 'electronic_main' and early:
                ok_st = ('failed',)
                if r.get('why') != s3.get('reason'):
                    bad.append(f'{sub}.{name} 사유 {r.get("why")!r} ≠ 결과 사유 {s3.get("reason")!r} (조기 반환 해)')
            if r.get('status') not in ok_st:
                bad.append(f'{sub}.{name} = {r.get("status")!r} (LEAN 2 표 · 상태 {state} {ok_st})')
    return bad


ARM_PUBLIC = ('file', 'index', 'sha256', 'protocol_id', 'state', 'cg_info', 'cg_resid', 'imbalance', 'cert_pass', 'sid_fp',
              'cg_iters', 'resolve_iters', 'sv_cf_status',   # ★ Z3 — CG 반복 수 · ★ 3판 — 해 상태 · SV 반사실 상태 (σ · 비 아님)
              'err_rel')                                     # ★ 4판 (Q2-2) — 판독 보장 오차 e (증서 ⓓ · 상대값 · σ 아님)
#: 런 요청 칸 (요약 `runs` · 다시 판정 · 사다리 확인 팔 다시 읽기가 같은 칸을 쓴다)
REQ_KEYS = ('name', 'role', 'kit', 'law', 'c', 'rj', 'arms', 'arm_list', 'variant', 'sv_cf')


def arm_indices(req):
    """요청 → 팔 번호 (origin 번호) 목록 — `ARM_LIST` 런 = 그 목록 · 아니면 0..ARMS−1."""
    al = req.get('arm_list')
    return list(al) if al is not None else list(range(req['arms']))


def arm_file_shas(outdir):
    """읽기가 멈춘 런의 팔 파일 → [{file, index, sha256}] (번호 순 · 번호 없는 이름은 뺀다) — 계약 판정은 하지 않는다."""
    out = []
    for p in sorted(glob.glob(str(Path(outdir) / 'p2_*.json'))):
        m = re.search(r'_a(\d+)\.json$', p)
        if m:
            try:
                out.append({'file': os.path.basename(p), 'index': int(m.group(1)), 'sha256': sha256_file(p)})
            except OSError:
                pass
    return sorted(out, key=lambda x: (x['index'], x['file']))


def sv_graph_state(svr, req, arm, path, outdir, graph_src=None, plan=None):
    """★ 10-26 묶음 B6 (Codex 회차 ① RR1-01 · 1저자 10-26 Q2 (가)) SV 기록 하나의 끝 그래프 귀속 → {'state', 'kind', 'why'} —
    not_applicable (증서 구간 기록의 비를 싣는 끝이 없다 · `ca_ext_svcf.graph_applicable`) · unverified (kind no_source = 원천 없음 ·
    source_failed = 원천 예외 · 꼴 틀림 (`ca_ext_svcf.graph_source_problem`)) · mismatch (원천 지문 ≠ 증서 지문 · `ca_ext_svcf.graph_problem` · 호출자 =
    CA_EXT_RECORD) · verified.  원천은 SV 기록의 지문을 받지 않는다 (ctx = 요청 · 팔 · 파일 · 폴더 · 계획 · 그 런 주 증서의 결합 칸).
    ★ 10-26 B″ (1저자 Q1 (가)) 원천 = `SV_GRAPH_SOURCE` — `RUNNER_GRAPH_SOURCE` (생산 기본) 이면 단계가 넘긴 graph_src (`RunnerGraphSource` · 없으면
    원천 없음) · 호출 가능 = 그것 (시험 · 대체 원천) · None = 원천 없음."""
    if not SVCF.graph_applicable(svr):
        return {'state': 'not_applicable', 'kind': None, 'why': None}
    src = SV_GRAPH_SOURCE
    if isinstance(src, str) and src == RUNNER_GRAPH_SOURCE:
        src = graph_src
    if src is None:
        return {'state': 'unverified', 'kind': 'no_source', 'why': SV_GRAPH_WHY['no_source']}
    full = svr.get('conv_cert_full') if isinstance(svr.get('conv_cert_full'), dict) else {}
    try:
        g = src({'req': dict(req), 'arm': int(arm), 'file': str(path), 'outdir': str(outdir), 'plan': plan,
                 'bind': {k: full.get(k) for k in SVCF.BIND_FIELDS}})
    except Stop:                                             # ★ 10-27 묶음 C2b — 원천 런 중 사슬이 받은 신호 = 단계 멈춤 (미확인으로 삼키지 않는다)
        raise
    except Exception as e:                                   # noqa: BLE001 — 원천 실패 = 미확인 (clear 아님 · 멈춤 아님)
        return {'state': 'unverified', 'kind': 'source_failed', 'why': f'원천 예외 {type(e).__name__}: {e}'[:300]}
    why = SVCF.graph_source_problem(g)
    if why:
        return {'state': 'unverified', 'kind': 'source_failed', 'why': f'원천 꼴 — {why}'[:300]}
    prob = SVCF.graph_problem(svr, g)
    if prob:
        return {'state': 'mismatch', 'kind': None, 'why': prob}
    return {'state': 'verified', 'kind': None, 'why': None}


def read_run(outdir, req, plan, contract, sid_reg, want_sha=None, s0_grid=None, s0_census=None, graph_src=None):
    """런 폴더 하나 → [팔 기록 …] (번호 순).  등록 R §10 멈춤 목록의 팔 쪽 전부 — 어긋나면 Stop (원인 칸 = σ 를 가린 문장).
    ★ 3판 — 해 상태 (§5-0 · `run_contract.next_gen_state` · 정본): positive (증서 ⓐ–ⓓ · σ > 0) · zero (VALID_ZERO_TOPOLOGY · σ = 0) ·
    ~~short (ELECTRODE_SHORT · σ = +∞)~~ · 그 밖 = NOT_COMPUTED.  팔 기록의 σ = 확장 실수 (0 그대로).
    ★ 4판 (10-21 · 1저자 Q1 · 등록 R 4판 §5-0 ①–③ · §4-2 ③) — short (ELECTRODE_SHORT · J11) = 생산자 미게시 → 기록 검사 (계약 · 매니페스트 ·
    LEAN · sid) 를 다 지난 뒤 이 런 = NOT_COMPUTED (멈춤 사유 reason = ELECTRODE_SHORT · `registration_state`) — 기록이 요청과 다르면 그 멈춤
    이름이 먼저다 (단락이 계약 위반을 가리지 않는다).
    ★ 10-21 (PRE-impl-07 병합) — 순서 = 세대 (GENERATION) · ca_ext 기록 (CA_EXT_RECORD) → 해 상태 (증서 · 증서 ↔ 런 결합) → 팔 계약 · 매니페스트."""
    outdir = Path(outdir)
    name = req.get('name')
    rej = sorted(os.path.basename(x) for x in glob.glob(str(outdir / '.rejected_*')))
    if rej:
        raise Stop('REJECTED_MARKER', f'{outdir.name}: {rej}', name)
    files = sorted(glob.glob(str(outdir / 'p2_*.json')))
    byi = {}
    for p in files:
        m = re.search(r'_a(\d+)\.json$', p)
        if not m or int(m.group(1)) in byi:
            raise Stop('ARM_JSON_COUNT', f'{outdir.name}: 팔 번호가 없거나 겹친다 ({os.path.basename(p)})', name)
        byi[int(m.group(1))] = p
    idx = arm_indices(req)
    if sorted(byi) != idx:
        raise Stop('ARM_JSON_COUNT', f'{outdir.name}: 팔 번호 {sorted(byi)} ≠ 요청 {idx}', name)
    pref = f'p2_{req["kit"][len("kit_"):]}_'
    if any(not os.path.basename(p).startswith(pref) for p in byi.values()):
        raise Stop('ARM_JSON_COUNT', f'{outdir.name}: 팔 이름이 킷 {req["kit"]} 의 것이 아니다', name)
    if want_sha is not None and len(want_sha) != len(idx):
        raise Stop('INPUT_SHA_MISMATCH', f'{outdir.name}: 기록된 sha256 {len(want_sha)} 개 ≠ 팔 {len(idx)}', name)
    try:
        rcpt = json.loads((outdir / 'run_receipt.json').read_text(encoding='utf-8'))
    except (OSError, ValueError):
        rcpt = None
    out = []
    for j, i in enumerate(idx):
        p = byi[i]
        if want_sha is not None:
            why = sha_mismatch(p, want_sha[j])
            if why:
                raise Stop('INPUT_SHA_MISMATCH', why, name)
        try:
            raw = Path(p).read_bytes()
            payload = json.loads(raw.decode('utf-8'))
        except (OSError, UnicodeDecodeError, ValueError) as e:
            raise Stop('ARM_UNREADABLE', f'{os.path.basename(p)}: {type(e).__name__}', name)
        s3 = RC.step3_of(payload) if isinstance(payload, dict) else None
        man = s3.get('manifest') if isinstance(s3, dict) else None
        if not isinstance(s3, dict) or not isinstance(man, dict):
            raise Stop('ARM_UNREADABLE', f'{os.path.basename(p)}: step3 · manifest 블록이 없다', name)
        cert = s3.get('conv_cert') if isinstance(s3.get('conv_cert'), dict) else None
        sv = [s3.get('sigma_e_eff_S_cm'), (cert or {}).get('sigma'), (cert or {}).get('sigma_resolve')]
        sv = [float(x) for x in sv if isinstance(x, (int, float)) and not isinstance(x, bool)]

        def stop(code, why, reason=None):
            raise Stop(code, mask_sigma(f'{os.path.basename(p)}: {why}', sv), name, reason=reason)
        #  ★ 10-21 (사전 리뷰 PRE-impl-07 병합 · B 권고) — 기록 (세대 · ca_ext) 먼저, 해 상태 (증서 · 증서 ↔ 런 결합) 는 그 뒤: 결합은 맞는 세대 ·
        #    맞는 기록 위에서만 뜻이 있다 (옛 순서 = 상태 먼저 → unknown:ca_ext 팔이 GENERATION 대신 CERT|bind| NOT_COMPUTED 로 멈췄다)
        pid = RC.physics_protocol_id(man)
        if not str(pid).startswith(RC.CA_EXT_PREFIX + '-'):
            stop('GENERATION', f'다시 계산한 id = {pid!r} (p3ca- 이어야)')
        if man.get('physics_protocol_id') != pid:
            stop('GENERATION', f'저장 id {man.get("physics_protocol_id")!r} ≠ 다시 계산 {pid!r}')
        ok, why = contract.ca_ext_record(man)
        if not ok:
            stop('CA_EXT_RECORD', why)
        state, swhy = RC.next_gen_state(s3)
        if state is None:
            stop('NOT_COMPUTED', f'해 상태 (§5-0) {swhy}')
        if state in ('positive', 'legacy'):
            ok, why = RC.conv_ok(s3.get('cg_info'), s3.get('unconverged'), s3.get('cg_resid'))
            if not ok:
                stop('NOT_COMPUTED', f'수렴 계약 {why}')
        why = contract.arm_problem(p, rcpt)
        if why:
            stop('ARM_CONTRACT', why)
        bad = manifest_problems(man, rcpt, req, plan, i, cert, state)
        if bad:
            stop('MANIFEST_MISMATCH', ' · '.join(bad[:6]) + (f' (+{len(bad) - 6})' if len(bad) > 6 else ''))
        bad = lean_problems(man, state, s3)
        if bad:
            stop('RECEIPT_LEAN', ' · '.join(bad))
        if man.get('ptfe_cells_observed') != 0:
            stop('PTFE_CELLS_OBSERVED', f'ptfe_cells_observed = {man.get("ptfe_cells_observed")!r} (face_alpha = PTFE 셀 0)')
        ca = man['ca_ext']
        fp = (ca['cjunc'].get('evidence') or {}).get('fp') or {}
        sid = fp.get('sid')
        off = ((ca['ptfe_face'].get('evidence') or {}).get('fp') or {}).get('sid_off')
        #  ★ Z3 — off 격자 지문 필수 (face_alpha 의 sid 격자 = off 격자 · 접합 원장과 같은 솔브 · 같은 지문 함수) · 정본 계약 뒤 둘째 겹
        if not isinstance(sid, str) or not sid or off != sid:
            stop('SID_GRID', f'접합 원장 sid 지문 {sid!r} · off 격자 지문 {off!r} (둘이 같아야 한다)')
        key = sid_group(req['kit'], req['variant'], i)
        if sid_reg.setdefault(key, sid) != sid:
            stop('SID_GRID', f'{key} 의 sid 지문이 앞 런과 다르다')
        #  ★ 10-25 묶음 B (RCA2-03 · Q3 (가)) — 같은 규약 arm 0 의 sid 지문 = S0 단계 보고의 off 격자 지문 (`s0_grid_seed` · 파생 격자 지문)
        want = (s0_grid or {}).get(key)
        if want is not None and want != sid:
            stop('S0_REPORT_MISMATCH', f'{key} 의 sid 지문 {sid} ≠ S0 단계 보고의 off 격자 지문 {want} (같은 규약 · arm 0) — {BED_NEW_S0}')
        reg, reg_why = registration_state(state)          # ★ 4판 (Q1) — 이 등록의 풀이 상태 셋 (§5-0)
        if reg == 'NOT_COMPUTED':
            stop('NOT_COMPUTED', f'해 상태 (§5-0 · 4판) {state} → {reg} (사유 {reg_why}) — 단락 (J11 · 판–판 0 저항 축약) = 생산자 미게시 · '
                                 f'σ 값 없음 (+∞ 로 판정에 오지 않는다 · 등록 R 4판 §5-0 ①–③)', reason=reg_why)
        if reg == 'VALID_ZERO_TOPOLOGY':
            sigma = 0.0
            err = 0.0                                    # ★ 4판 (Q2-2 · ③″) — σ = 0 정확 (위상 · 증서 대상 아님) → 판독 구간 [0, 0] (e 무관)
        else:
            sig = s3.get('sigma_e_eff_S_cm')
            if isinstance(sig, bool) or not isinstance(sig, (int, float)) or not math.isfinite(sig) or sig <= 0:
                stop('ARM_UNREADABLE', 'σ_e 가 유한 양수가 아니다')
            sigma = float(sig)
            #  ★ 4판 (Q2-2 · §3-2b ③″ · PRE-design-12 · R4-Q2) — 판독 보장 오차 e = 그 런 증서 ⓓ 의 target_err_bound_rel — 기록 칸을 믿지 않고
            #    증서 구간 · 게시 판 전류에서 생산 · 계약과 **같은 함수** (`step3_conv_cert.target_judge`) 로 다시 계산 (next_gen_state 가 ⓓ 통과를
            #    이미 확인했다 · e ≤ τ = 1e-4 · 등록 τ 가 아니라 그 런의 값)
            import step3_conv_cert as _cc
            jd = _cc.target_judge((cert or {}).get('target_lo'), (cert or {}).get('target_hi'), (cert or {}).get('I_bot'))
            err = jd.get('target_err_bound_rel')
            if jd.get('pass_d') is not True or isinstance(err, bool) or not isinstance(err, float) or not math.isfinite(err) or err < 0.0:
                stop('NOT_COMPUTED', f'증서 ⓓ 보장 오차를 다시 계산할 수 없다 ({jd.get("target_why")}) — 보호 띠 (§3-2b ③″) 를 잴 수 없다')
        solve = (ca['cjunc'].get('evidence') or {}).get('solve') or {}
        svr = solve.get('sv_counterfactual')
        #  ★ 10-23 (Codex 재검토 RCA2-04 · 1저자 Q1 (가)) — 증서 구간 기록의 주 해 증서 (비의 분자 구간) = 이 런의 주 증서 (계약이 이미 수로 다시
        #    판정한 `step3.conv_cert`) — 기록 계약 (매니페스트만 본다) 이 못 보는 결합을 판정 입력 자리에서 맞춘다 · 다르면 기록 위반
        #  ★ 10-23 (사전 공격 리뷰 C1 · 1저자 Q12 (가)) — 주 해 증서의 위상 수 (`CERT_TOPO_KEYS`) 도 맞춘다 (기록 계약이 끝 증서 위상 수를 그 수와
        #    대조한다 — 기록 안에서만 부풀린 주 해 위상 수를 이 자리에서 잡는다)
        if isinstance(svr, dict) and svr.get('standing') == SVCF.STANDING_CERTIFIED and isinstance(svr.get('conv_cert_full'), dict):
            _ccf = svr['conv_cert_full']
            _mis = [k for k in ('version', 'status', 'I_bot', 'target_lo', 'target_hi') + SVCF.BIND_FIELDS + SVCF.CERT_TOPO_KEYS
                    + (SVCF.GRAPH_KEY,) if _ccf.get(k) != (cert or {}).get(k)]
            if _mis:
                stop('CA_EXT_RECORD', f'SV 반사실 기록의 주 해 증서 칸 {_mis} ≠ 이 런의 주 증서 (비의 분자 구간이 이 런의 것이 아니다 · '
                                      f'10-23 RCA2-04)')
        #  ★ 10-25 묶음 B (X6 · Q20 (가)) — 같은 규약 DBE arm 0 의 SV 기록 = S0 단계 2 봉인 census (기록 사본 · 증거 census · 세 칸 · `s0_census_seed`)
        cen_want = (s0_census or {}).get(key)
        if cen_want is not None and isinstance(svr, dict):
            why = sv_census_problem(svr, (ca['cjunc'].get('evidence') or {}).get('census'), cen_want)
            if why:
                stop('S0_REPORT_MISMATCH', f'{why} — {BED_NEW_S0}')
        #  ★ 10-26 묶음 B6 (Codex 회차 ① RR1-01 · 1저자 10-26 Q2 (가)) — 끝 증서의 가중 그래프 귀속 (SV 기록 밖 봉인 원천 ↔ 증서 지문) · 다르면 기록 위반 ·
        #    원천 없음 · 실패 = 미확인 (판정 = SV_UNCHECKED · `sv_assess(require_graph=True)`)
        #    ★ 10-26 B″ (1저자 Q1 (가)) — 생산 원천 = 단계가 넘긴 graph_src (`RunnerGraphSource` · 러너 조립만 · 계획 = 이 런 계획)
        sv_graph = sv_graph_state(svr, req, i, p, outdir, graph_src=graph_src, plan=plan)
        if sv_graph['state'] == 'mismatch':
            stop('CA_EXT_RECORD', f"{sv_graph['why']} (봉인 원천 대조)")
        cf = SVCF.chain_view(svr) if isinstance(svr, dict) else None
        out.append({'file': os.path.basename(p), 'index': i, 'sha256': hashlib.sha256(raw).hexdigest(), 'protocol_id': pid,
                    'state': state, 'cg_info': s3.get('cg_info'), 'cg_resid': s3.get('cg_resid'), 'imbalance': (cert or {}).get('imbalance'),
                    'cert_pass': [(cert or {}).get('pass_a'), (cert or {}).get('pass_b'), (cert or {}).get('pass_c'),
                                  (cert or {}).get('pass_d')],
                    'sid_fp': sid, 'cg_iters': _int_or_none(s3.get('cg_iters')),
                    'resolve_iters': _int_or_none((cert or {}).get('resolve_iters')),
                    'sigma': sigma, 'dsigma_rel': (cert or {}).get('dsigma_rel'), 'err_rel': err,
                    #  ★ 10-23 (사전 공격 리뷰 C4) — R 단조 띠 = 그 런 증서의 목표량 구간 × scale (`arm_band`) · 공개 칸 (ARM_PUBLIC) 아님 (scale × 구간
                    #    = σ · 값 봉인) · 영값 위상 = 칸 없음 (σ 0 → 띠 [0, 0])
                    **({k: (cert or {}).get(k) for k in ('target_lo', 'target_hi', 'scale')} if reg != 'VALID_ZERO_TOPOLOGY' else
                       {'target_lo': None, 'target_hi': None, 'scale': None}),
                    'sv_cf': cf, 'sv_cf_status': (cf or {}).get('status'), 'sv_graph': sv_graph,
                    'sv_local': solve.get('sv_local_dissipation'), 'dissipation_share': solve.get('dissipation_share'),
                    'n_sdcp_near': (((ca.get('sdcp_mod') or {}).get('evidence') or {}).get('n_sdcp_near')
                                    if isinstance(ca.get('sdcp_mod'), dict) else None)})
    return out


# ═════════════════════════ 러너 (런마다 새 폴더 · env 를 사슬이 정한다) ═════════════════════════
def runner_env_delta(plan, variant, req, outdir):
    """런 하나의 러너 env (사슬이 정하는 칸 전부 · 부모 셸 값과 무관) — `Runner` (생산 팔) 와 `RunnerGraphSource` (봉인 원천 조립만 런) 가 **같은 함수**를
    쓴다 (★ 10-26 B″ · 1저자 Q1 (가) — 원천 런 = 같은 env + `GRAPH_ONLY_ENV` · 사본 없음)."""
    d = dict(ENV_FIXED)
    d.update(RUNNER_EXEC_ENV)                                # ★ 10-26 B″ (Q4) — 러너가 venv 를 켜지 않는다 (payload = 사슬 프로세스 환경)
    d.update(ATTEMPT_ENV)                                    # ★ 10-27 묶음 C2b — 러너 시도 꼴 (payload = 런 폴더 안 .unchecked/ · 첫 풀이 끝 표지)
    d.update(plan_env(plan))
    d.update(VARIANT_ENV.get(variant) or {})
    d.update({'KITS': req['kit'], 'OUTDIR': str(outdir), 'CJUNC_RJ': req['rj'], 'CJUNC_PTFE_JLAW': req['law'],
              'EXPECT_BACKEND': EXPECT_BACKEND})
    if req.get('arm_list') is not None:                      # ★ Z3 — 팔 고르기 (러너: ARMS 와 동시 = 거부 · 팔 수 = 목록 길이)
        d['ARM_LIST'] = ','.join(str(i) for i in req['arm_list'])
    else:
        d['ARMS'] = str(req['arms'])
    if req['c'] != '':
        d['SDCP_MOD_C'] = req['c']
    if req.get('sv_cf'):                                      # ★ 3판 — SV 반사실 대조 (같은 런 안 추가 풀이 · 주 σ · 규약 id 그대로)
        d['CJUNC_SV_CF'] = '1'
    return d


# ═════════════════════════ ★ 10-27 묶음 C2b 러너 프로세스 그룹 (Q9 개정 4 Q2 · R4-02 ⓑ · Codex 회차 ① ② · 개정 5 ②) ═════════════════════════
def _utc():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def write_json_atomic(path, obj):
    """정준 JSON → 원자적 쓰기 (같은 폴더 임시 파일 → fsync → os.replace) — 그룹 · 시도 기록 (반쯤 쓰인 기록을 남기지 않는다)."""
    path = Path(path)
    tmp = path.with_name(f'{path.name}.tmp.{os.getpid()}')
    with open(tmp, 'wb') as f:
        f.write(canon_bytes(obj))
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def host_ident():
    """이 프로세스가 보는 호스트 · 부팅 · pid 이름공간 (그룹 기록 · recover 의 대조 칸) — 못 읽은 칸 = None."""
    def rd(p):
        try:
            v = Path(p).read_text(encoding='ascii').strip()
        except (OSError, UnicodeDecodeError):
            return None
        return v or None
    try:
        ns = os.readlink('/proc/self/ns/pid')
    except OSError:
        ns = None
    return {'machine_id': rd('/etc/machine-id'), 'boot_id': rd('/proc/sys/kernel/random/boot_id'), 'pidns': ns}


def group_members(token):
    """/proc 에서 env 그룹 표지 (`RINT_RUN_TOKEN=token`) 를 가진 살아 있는 프로세스 pid 목록 (zombie · dead · 이 프로세스 뺌) | None (/proc 를 못
    읽음 = 확인 불가).  러너 · bash 부분 셸 · payload · 그 자식은 env 를 물려받는다 (setsid 로 그룹을 벗어나도 표지는 남는다) — env 를 지운 자식은 못
    찾는다 (한정 · 러너 · payload 는 env 를 지우지 않는다)."""
    try:
        names = os.listdir('/proc')
    except OSError:
        return None
    me, out = os.getpid(), []
    needle = f'{GROUP_TOKEN_ENV}={token}'.encode('ascii')
    for e in names:
        if not e.isdigit() or int(e) == me:
            continue
        try:
            st = Path('/proc', e, 'stat').read_bytes()
            fl = st[st.rfind(b')') + 2:].split()
            if not fl or fl[0] in (b'Z', b'X', b'x'):
                continue
            env = Path('/proc', e, 'environ').read_bytes()
        except OSError:
            continue
        if needle in env.split(b'\0'):
            out.append(int(e))
    return sorted(out)


def group_kill_pids(pids):
    for pid in pids:
        try:
            os.kill(int(pid), signal.SIGKILL)
        except (ProcessLookupError, PermissionError, OSError):
            pass


def group_settle(token, limit=None):
    """그룹 (표지 프로세스) 이 다 끝날 때까지 SIGKILL 하고 기다린다 (대기 상한 `GROUP_GONE_WAIT_S`) → (확인 bool, 남은 pid 목록 | None (못 읽음),
    죽인 프로세스 수)."""
    limit = GROUP_GONE_WAIT_S if limit is None else limit
    t_end = time.time() + limit
    killed = set()
    while True:
        m = group_members(token)
        if m is None:
            return False, None, len(killed)
        if not m:
            return True, [], len(killed)
        killed |= set(m)
        group_kill_pids(m)
        if time.time() >= t_end:
            m = group_members(token)
            return m == [], m, len(killed)
        time.sleep(GROUP_POLL_S)


class ChainSignal(BaseException):
    """사슬이 러너를 기다리는 동안 받은 SIGTERM · SIGHUP (러너 그룹을 죽이고 확인한 뒤 그 런을 멈춘다 · BaseException = 넓은 except 가 삼키지 않게)."""

    def __init__(self, signum):
        super().__init__(signum)
        self.signum = signum


def _raise_chain_signal(signum, frame):
    raise ChainSignal(signum)


def _signal_handlers(fn):
    """주 스레드에서만 SIGTERM · SIGHUP 처리기를 fn 으로 → 옛 처리기 dict (되돌리기) | None (다른 스레드 · 못 걺)."""
    import threading
    if threading.current_thread() is not threading.main_thread():
        return None
    old = {}
    for s in (signal.SIGTERM, signal.SIGHUP):
        try:
            old[s] = signal.signal(s, fn)
        except (ValueError, OSError):
            pass
    return old


def _signal_restore(old):
    for s, h in (old or {}).items():
        try:
            signal.signal(s, h)
        except (ValueError, OSError):
            pass


def signal_name(signum):
    try:
        return signal.Signals(signum).name
    except (ValueError, TypeError):
        return str(signum)


def run_in_group(argv, cwd, env, logf, timeout, gdir, name, by='chain'):
    """러너를 새 세션 (프로세스 그룹 · env 그룹 표지) 으로 띄우고 끝까지 → (rc, 원인, 끝 기록).  원인 = None (스스로 끝남) · 'timeout' · 'signal' (SIGTERM ·
    SIGHUP — 사슬이 받음) · 'exception' (그 밖 · 기록 뒤 다시 올린다) · 'signal_after' (러너가 스스로 끝난 뒤 정리 중 받은 신호 — 정리 · 끝 기록을 끊지 않고
    미뤘다 · 디스크 끝 기록의 원인은 None 그대로 · 돌려주는 dict 에 `signal_after` · 부르는 쪽 = 그 런을 멈춤).  멈출 때 그룹 전체를 SIGKILL (지도자 회수 전 = 그룹 번호가 이 그룹 것) · 스스로
    끝났어도 남은 표지 프로세스를 죽인다 · 끝 기록 (`<name>.end.json`) = 표지 프로세스가 0 임을 확인한 뒤 (대기 상한 안에 못 하면 confirmed False) ·
    시작 기록 (`<name>.launch.json`) = Popen 전 (표지 · 호스트) 과 뒤 (pid · pgid).  ⚠ 한정: 사슬 부모 자신이 SIGKILL 되면 이 함수는 끝 기록을 못 쓴다 →
    `--stage recover` (Codex ② · 끝 기록 없는 시작 기록 = 미확인 · 부모 사망 + 지금 표지 없음을 종료 증거로 쓰지 않는다).  ⚠ 한정: 처리기를 거는 · 바꾸는
    몇 바이트코드 사이 (기다림 처리기 → 미룸) 에 신호가 두 번 겹치면 이 함수가 끝 기록 없이 빠질 수 있다 — 그 경우도 recover 몫 (시작 기록 · 끝 기록 없음 =
    미확인).  처리기 = 주 스레드에서만 (다른 스레드에서 부르면 신호 처리 없음 · 기본 동작)."""
    gdir = Path(gdir)
    gdir.mkdir(parents=True, exist_ok=True)
    token = os.urandom(16).hex()
    launch = {'schema': GROUP_SCHEMA, 'name': name, 'token': token, 'pid': None, 'pgid': None, 'argv': [str(a) for a in argv],
              'host': host_ident(), 'started_utc': _utc(), 'by': by, 'chain_pid': os.getpid()}
    write_json_atomic(gdir / f'{name}.launch.json', launch)
    rc, cause, exc, p, sig = None, None, None, None, None
    pending = []

    def _defer(signum, frame):                             # 정리 중 신호 = 미룬다 (정리 · 끝 기록을 끊지 않는다 · 끝난 뒤 그 런을 멈춘다)
        pending.append(signum)
    old = _signal_handlers(_raise_chain_signal)
    try:
        try:
            try:
                p = subprocess.Popen(argv, cwd=cwd, env=dict(env, **{GROUP_TOKEN_ENV: token}), stdout=logf, stderr=subprocess.STDOUT,
                                     stdin=subprocess.DEVNULL, start_new_session=True)
                try:
                    pg = os.getpgid(p.pid)                 # 실제 그룹 번호 (새 세션 = pid · 기록 = 잰 값)
                except OSError:
                    pg = None
                launch.update(pid=p.pid, pgid=pg)
                write_json_atomic(gdir / f'{name}.launch.json', launch)
                rc = p.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                cause = 'timeout'
            except ChainSignal as e:
                cause, sig = 'signal', e.signum
            except BaseException as e:                     # noqa: BLE001 — KeyboardInterrupt 포함 · 그룹을 죽인 뒤 다시 올린다
                cause, exc = 'exception', e
            finally:
                if old is not None:                        # 원 처리기로 되돌리지 않고 바로 미룸으로 (사이에 원 처리기 = 기본 종료가 끼지 않게)
                    _signal_handlers(_defer)
        except ChainSignal as e:                           # 미룸으로 바꾸기 직전에 온 신호 — 그 런을 멈춘 것으로 (그룹은 아래에서 죽이고 확인)
            if cause is None:
                cause, sig = 'signal', e.signum
            if old is not None:
                _signal_handlers(_defer)
        if p is not None and rc is None:
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except (ProcessLookupError, PermissionError, OSError):
                pass
            try:
                rc = p.wait(timeout=GROUP_GONE_WAIT_S)
            except subprocess.TimeoutExpired:
                rc = None
        confirmed, left, n_killed = group_settle(token)
        end = {'schema': GROUP_SCHEMA, 'name': name, 'token': token, 'rc': rc, 'cause': cause, 'signal': (signal_name(sig) if sig else None),
               'confirmed': bool(confirmed), 'left': left, 'left_after_exit': (n_killed if cause is None else None), 'killed': n_killed,
               'by': by, 'ended_utc': _utc()}
        write_json_atomic(gdir / f'{name}.end.json', end)
    finally:
        _signal_restore(old)
    if exc is not None:
        raise exc
    if pending and cause is None:                          # 정리 중 받은 신호 — 그 런은 스스로 끝났다 (끝 기록 그대로 · 원인 None) · 사슬은 멈춘다
        return rc, 'signal_after', dict(end, signal_after=signal_name(pending[0]))
    return rc, cause, end


# ═════════════════════════ (2c) ★ 10-27 묶음 C1b 시도 원장 · 시도 폴더 ═════════════════════════
#   RCA2-05 · Q4 (가) · Q9 설계 §3-2 · §3-4 · §3-5 (개정 1–5) · author 10-27 approved bundle C.
#   원장 = 실행 트리와 다른 git 저장소의 덧붙이기만 하는 파일 (`LEDGER_FILE`) — 첫 줄 = 머리 (schema · 계획 sha256) · 항목 줄 (시도 **전에** 커밋 ·
#   `--stage ledger --add` · 대상 · 기계 · 재실행이면 원 시도 · 계획 · 코드 키 · 환경 · 침대 지문) · 결과 줄 (시도 끝 · 그룹 종료를 확인한 뒤 · 사슬 또는
#   `--stage recover`).  한 줄 = 정준 JSON (키 차례 · 빈칸 없는 구분자 · ensure_ascii False).  시도 폴더 = <--out>/attempt_<n> (`attempt.json` = 항목 ·
#   시작 커밋) · 풀기 전 거부 = 그 안 `rejected.json` (폴더를 만들 수 없으면 옆 attempt_<n>.rejected.json) · 결과 전 · 뒤 = 첫 풀이 끝 표지 · 팔 payload 유무
#   (원인 무관) · 채택 = 원장 차례로 처음 결과 전이 아닌 시도 + 그 재실행 사슬 · 예측 (사다리 입력) · 판정 (--ledger) 은 채택 시도만 읽는다.
#   ⚠ 한정 (Codex 회차 ① Q-D): 원장은 원장 안 시도끼리 결과를 본 뒤 고르는 길만 막는다 — 원장 밖 그림자 런 · 모든 사본 (폴더 · 결과 줄 · 원장) 을 함께 고친 손은
#   막지 못한다.  다음 시도 번호는 원장이 정한다 (같은 대상 다음 항목 · 시도 폴더에 덧쓰지 않는다 — 폴더 요약 sha 를 바꾸지 않게).
LEDGER_FILE = 'rint_r_attempts.jsonl'
LEDGER_SCHEMA = 'rint-r-ledger-v1'
ATTEMPT_SCHEMA = 'rint-r-attempt-v1'
REJECTED_SCHEMA = 'rint-r-rejected-v1'
ATTEMPT_FILE = 'attempt.json'
REJECTED_FILE = 'rejected.json'
REJECTED_SIDE = '.rejected.json'
ATTEMPT_DIR_RE = re.compile(r'attempt_([1-9][0-9]{0,8})')
ATTEMPT_SIDE_RE = re.compile(r'attempt_([1-9][0-9]{0,8})\.rejected\.json')
#: ★ 10-27 묶음 C2d (Q9 §3-1) — 단위 · 넘침 점 대상 = unit[:<변이>]:<이름> · point[:<변이>]:<이름> (이름 = `UNIT_RE` · 무리 4 = 종류 · 5 = 변이 · 6–8 = 이름)
UNIT_RE = re.compile(r'(P0|P1)_c(0|1)_(R_j_lo|R_j0|R_j_hi)')
TARGET_RE = re.compile(r'ladder:(P0|P1)(?::(FIBRE|UNREG|GRID))?|predict(?::(FIBRE|UNREG|GRID|SVORDER))?'
                       r'|(unit|point)(?::(FIBRE|UNREG|GRID|SVORDER))?:(P0|P1)_c(0|1)_(R_j_lo|R_j0|R_j_hi)')
LEDGER_GIT_CFG = ('-c', 'user.name=rint-r-chain', '-c', 'user.email=rint-r-chain@localhost', '-c', 'commit.gpgsign=false',
                  '-c', 'core.autocrlf=false')
HEADER_KEYS = frozenset({'kind', 'schema', 'plan_sha256', 'utc'})
ENTRY_KEYS = frozenset({'kind', 'n', 'target', 'machine', 'resume_of', 'plan_sha256', 'code_key_sha256', 'env', 'bed', 'utc'})
RESULT_KEYS = frozenset({'kind', 'n', 'status', 'stop', 'side', 'cause', 'resume_ok', 'folder', 'folder_sha256', 'by', 'utc'})
ATTEMPT_KEYS = frozenset({'schema', 'n', 'target', 'machine', 'resume_of', 'ledger_commit'})
RESULT_STATUSES = ('completed', 'stopped', 'rejected', 'interrupted')
#: ★ 10-27 묶음 C2d — 단위 · 넘침 점 시도의 완주 상태 (요약 이름 · 런 이름 앞자리 U · 결과 줄 completed)
UNIT_SUMMARY = {'unit': 'unit_summary.json', 'point': 'point_summary.json'}
UNIT_DONE = {'unit': 'UNIT_DONE', 'point': 'POINT_DONE'}
UNIT_PREFIX = 'U'
DONE_STATUSES = ('CALIBRATED', 'PREDICTED', 'UNIT_DONE', 'POINT_DONE')
#: ★ 10-27 묶음 C2d (Q9 §3-2 · §3-4) — 합치기 · 결정 기록 · 사본 자리 · 첫 합치기 넘침 (멈춤 아님 · 판정 입력 아님) 종료 코드
MERGE_SCHEMA = 'rint-r-merge-v1'
EXPANSION_SCHEMA = 'rint-r-expansion-v1'
EXPANSION_FILE = 'expansion.json'
MERGE_SUMMARY = 'merge_summary.json'
UNITS_DIR = 'units'
LEDGER_COPY_DIR = 'ledger'
LEDGER_BUNDLE = 'ledger.bundle'
EXPANSION_KEYS = frozenset({'schema', 'variant', 'points', 'overflow', 'attempts', 'ledger', 'ladders', 'plan_sha256', 'machine', 'env', 'utc'})
RC_EXPANSION_NEEDED = 4
#: 재실행 자격 원인 (Q9 §3-5 개정 4 — 자원 · 인프라 = 시간 초과 · 사슬이 받은 신호 · 사슬 부모 사망 (원인 기록 없음) · 그룹 종료 미확인 · 자원 낱말).
#:   그 밖 원인 (gate = 런 전 관문 · check = 팔을 읽은 뒤 검사 · 수치 · 물리 · runner_rc = 낱말 없는 러너 rc) = 재실행 불가 (보수 쪽).
RESUME_CAUSES = frozenset({'timeout', 'signal', 'parent_dead', 'group_unconfirmed', 'resource'})
#: 러너 rc ≠ 0 인 런 로그의 자원 · 인프라 낱말 (정확한 글자 · CUDA 메모리 · 호스트 메모리 · 디스크 부족 · GPU 오류) — ✅ 10-28 등록 R §10-5 다 ⑧ (1저자
#:   "Rint 권고대로" · 아홉 낱말 · 빠진 낱말 = 재실행 불가 쪽).  CUDA_ERROR_ILLEGAL_ADDRESS 는 뺐다 (코드 결함일 수 있다 → 원인 runner_rc · 시험 AL19b).
#:   검사 실패 흔적 (.unchecked/ 의 팔 payload) 이 있으면 낱말과 무관하게 재실행 불가.
RESOURCE_WORDS = ('OutOfMemoryError', 'CUDA_ERROR_OUT_OF_MEMORY', 'cudaErrorMemoryAllocation', 'MemoryError', 'No space left on device',
                  'CUDARuntimeError', 'CUDADriverError', 'CUDA_ERROR_LAUNCH_FAILED', 'cudaErrorLaunchFailure')


def ledger_line(obj):
    """원장 한 줄 (정준 JSON + 줄바꿈)."""
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False) + '\n'


def ledger_git(repo, *args, check=True):
    """원장 저장소 git (env 의 GIT_* 를 걷어낸다 · 고정 신원 · 실패 = Stop ATTEMPT_LEDGER_MISMATCH)."""
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    try:
        p = subprocess.run(['git', '-C', str(repo), *LEDGER_GIT_CFG, *args], capture_output=True, timeout=120, env=env)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise Stop('ATTEMPT_LEDGER_MISMATCH', f'원장 git {" ".join(args[:2])} 실행 실패 ({type(e).__name__})')
    if check and p.returncode != 0:
        raise Stop('ATTEMPT_LEDGER_MISMATCH', f'원장 git {" ".join(args[:2])} rc {p.returncode} · '
                                              f'{p.stderr.decode("utf-8", "replace").strip()[:200]}')
    return p


def _git_top(path):
    try:
        p = subprocess.run(['git', '-C', str(path), 'rev-parse', '--show-toplevel'], capture_output=True, timeout=60,
                           env={k: v for k, v in os.environ.items() if not k.startswith('GIT_')})
    except (OSError, subprocess.TimeoutExpired):
        return None
    return os.path.realpath(p.stdout.decode('utf-8', 'replace').strip()) if p.returncode == 0 else None


def ledger_repo_problem(repo):
    """원장 저장소 꼴 — git 작업 트리의 꼭대기 (하위 폴더 아님) · 사슬 체크아웃과 다른 저장소 (Q9 §3-5 개정 3 — 원장 커밋이 실행 트리의 HEAD 를
    바꾸지 않게) → 사유 | None."""
    top = _git_top(repo)
    if top is None:
        return f'{repo} 가 git 작업 트리가 아니다 (원장 = 따로 만든 git 저장소)'
    if top != os.path.realpath(str(repo)):
        return f'{repo} 는 git 저장소 {top} 의 하위 폴더다 — 원장 = 그 저장소의 꼭대기'
    me = _git_top(HERE)
    if me is not None and me == top:
        return f'원장 저장소 = 사슬 체크아웃 ({top}) — 실행 트리와 다른 체크아웃에 둔다 (Q9 §3-5)'
    return None


def ledger_head(repo):
    out = ledger_git(repo, 'rev-parse', '--verify', 'HEAD').stdout.decode('ascii', 'replace').strip()
    if not _hex40(out):
        raise Stop('ATTEMPT_LEDGER_MISMATCH', f'원장 HEAD {out[:44]!r}')
    return out


def ledger_blob(repo, commit):
    p = ledger_git(repo, 'show', f'{commit}:{LEDGER_FILE}', check=False)
    if p.returncode != 0:
        raise Stop('ATTEMPT_LEDGER_MISMATCH', f'원장 커밋 {str(commit)[:12]} 에 {LEDGER_FILE} 이 없다')
    return p.stdout


def ledger_is_ancestor(repo, a, b):
    return _hex40(a) and _hex40(b) and ledger_git(repo, 'merge-base', '--is-ancestor', a, b, check=False).returncode == 0


def ledger_history_problem(repo, commit):
    """원장 파일 역사 (첫 부모 차례 · 그 커밋까지) = 덧붙이기만 (판마다 앞 판의 바이트를 그대로 앞에 둔다) → 사유 | None (줄 지우기 · 바꾸기 =
    사유 · Q9 §3-5 개정 3)."""
    p = ledger_git(repo, 'log', '--first-parent', '--format=%H', commit, '--', LEDGER_FILE, check=False)
    if p.returncode != 0:
        return '원장 역사를 못 읽는다'
    prev = b''
    for c in [x for x in p.stdout.decode('ascii', 'replace').split() if x][::-1]:
        q = ledger_git(repo, 'show', f'{c}:{LEDGER_FILE}', check=False)
        if q.returncode != 0:
            return f'커밋 {c[:12]} 에서 원장 파일이 없어졌다'
        if not q.stdout.startswith(prev):
            return f'커밋 {c[:12]} 이 앞 판의 줄을 바꿨다 · 지웠다 (덧붙이기만이 아니다)'
        prev = q.stdout
    return None


def ledger_now(repo):
    """원장 = HEAD 커밋의 파일 (작업 파일 바이트 = HEAD blob · 커밋 안 한 고침 없음) → (HEAD sha, 바이트)."""
    head = ledger_head(repo)
    raw = ledger_blob(repo, head)
    lp = Path(repo) / LEDGER_FILE
    try:
        cur = lp.read_bytes() if not lp.is_symlink() else None
    except OSError:
        cur = None
    if cur != raw:
        raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{lp} 작업 파일 ≠ HEAD (커밋하지 않은 고침 · 링크 · 못 읽음 — 원장은 커밋된 판만 읽는다)')
    return head, raw


def _entry_problem(e, st):
    if set(e) != ENTRY_KEYS:
        return f'칸 {sorted(set(e) ^ ENTRY_KEYS)}'
    if not (isinstance(e['target'], str) and TARGET_RE.fullmatch(e['target'])):
        return f'대상 {e["target"]!r}'
    if not (isinstance(e['machine'], str) and e['machine'] and e['machine'] == e['machine'].strip()):
        return f'기계 {e["machine"]!r}'
    if e['plan_sha256'] != st['header']['plan_sha256']:
        return '계획 sha256 ≠ 원장 머리'
    if not _hex64(e['code_key_sha256']) or not isinstance(e['env'], dict) or not isinstance(e['bed'], dict) or not isinstance(e['utc'], str):
        return '지문 칸 꼴 (code_key_sha256 · env · bed · utc)'
    r = e['resume_of']
    if r is not None and (type(r) is not int or r not in st['entries'] or st['entries'][r]['target'] != e['target']):
        return f'resume_of {r!r} (같은 대상의 앞 항목이어야)'
    prev = [k for k, x in st['entries'].items() if x['target'] == e['target']]
    if prev and prev[-1] not in st['results']:
        raise Stop('ATTEMPT_ORDER_MISMATCH', f'원장: 항목 {e["n"]} ({e["target"]}) 이 같은 대상 앞 항목 {prev[-1]} 의 결과 줄 전에 있다 (Q9 §3-5 차례)')
    return None


def _result_problem(r):
    if set(r) != RESULT_KEYS:
        return f'칸 {sorted(set(r) ^ RESULT_KEYS)}'
    n = r['n']
    if r['status'] not in RESULT_STATUSES or r['side'] not in ('pre', 'post') or type(r['resume_ok']) is not bool \
            or r['by'] not in ('chain', 'recover'):
        return f'status {r["status"]!r} · side {r["side"]!r} · resume_ok {r["resume_ok"]!r} · by {r["by"]!r}'
    if r['folder'] not in (f'attempt_{n}', f'attempt_{n}{REJECTED_SIDE}') or not _hex64(r['folder_sha256']):
        return f'폴더 {r["folder"]!r} · 요약 sha'
    if r['stop'] is not None and not (isinstance(r['stop'], dict) and isinstance(r['stop'].get('code'), str)):
        return 'stop 꼴'
    if r['cause'] is not None and not isinstance(r['cause'], str):
        return 'cause 꼴'
    if r['status'] == 'completed' and (r['stop'] is not None or r['side'] != 'post' or r['resume_ok']):
        return '완주인데 멈춤 · 결과 전 · 재실행 자격'
    if r['status'] != 'completed' and r['stop'] is None and r['status'] != 'interrupted':
        return '멈춤 · 거부인데 멈춤 기록 없음'
    if r['status'] == 'rejected' and (r['side'] != 'pre' or r['resume_ok']):
        return '거부인데 결과 뒤 · 재실행 자격'
    if r['resume_ok'] and r['side'] != 'post':
        return '결과 전인데 재실행 자격'
    return None


def ledger_parse(raw):
    """원장 바이트 → 상태 {'header', 'entries' {n: 항목}, 'results' {n: 결과 줄}} · 꼴 · 차례 · 같은 항목 결과 줄 둘 = Stop."""
    def bad(why):
        raise Stop('ATTEMPT_LEDGER_MISMATCH', f'원장: {why}')
    try:
        txt = raw.decode('utf-8')
    except UnicodeDecodeError:
        bad('utf-8 이 아니다')
    if not txt.endswith('\n'):
        bad('비었거나 끝 줄바꿈이 없다 (덧붙이다 끊긴 꼴)')
    st = {'header': None, 'entries': {}, 'results': {}}
    for i, ln in enumerate(txt[:-1].split('\n')):
        try:
            obj = _json_strict(ln.encode('utf-8'))
        except Exception as e:                                # noqa: BLE001 — 꼴 틀림 = 멈춤
            bad(f'{i + 1} 째 줄 JSON 이 아니다 ({type(e).__name__})')
        if not isinstance(obj, dict) or ledger_line(obj) != ln + '\n':
            bad(f'{i + 1} 째 줄이 정준 JSON 한 줄이 아니다')
        kind = obj.get('kind')
        if i == 0:
            if set(obj) != HEADER_KEYS or kind != 'header' or obj.get('schema') != LEDGER_SCHEMA or not _hex64(obj.get('plan_sha256')):
                bad(f'첫 줄 = 머리 ({sorted(HEADER_KEYS)} · schema {LEDGER_SCHEMA}) 가 아니다')
            st['header'] = obj
            continue
        n = obj.get('n')
        if kind == 'entry':
            if type(n) is not int or n != len(st['entries']) + 1:
                bad(f'{i + 1} 째 줄 항목 번호 {n!r} (차례 = {len(st["entries"]) + 1})')
            why = _entry_problem(obj, st)
            if why:
                bad(f'항목 {n}: {why}')
            st['entries'][n] = obj
        elif kind == 'result':
            if type(n) is not int or n not in st['entries']:
                bad(f'{i + 1} 째 줄 결과 줄의 항목 {n!r} 이 앞에 없다')
            if n in st['results']:
                bad(f'항목 {n} 의 결과 줄이 둘 (Q9 §3-5)')
            why = _result_problem(obj)
            if why:
                bad(f'결과 줄 {n}: {why}')
            st['results'][n] = obj
        else:
            bad(f'{i + 1} 째 줄 kind {kind!r}')
    if st['header'] is None:
        bad('머리 줄이 없다')
    return st


def ledger_append(repo, obj, msg, expect=None):
    """원장에 줄 하나를 덧붙이고 커밋 → 새 HEAD.  덧붙이기 전 = 작업 파일 = HEAD (`ledger_now`) · expect = 읽어 둔 HEAD 바이트 (그 사이 다른 손이 커밋했으면
    멈춤) · 덧붙인 뒤 원장 꼴을 다시 읽는다 (꼴이 틀리면 덧붙이지 않는다 — 커밋 전)."""
    _head, raw = ledger_now(repo)
    if expect is not None and raw != expect:
        raise Stop('ATTEMPT_LEDGER_MISMATCH', '원장이 읽은 뒤 바뀌었다 (다른 손이 커밋했다) — 다시 시작')
    new = raw + ledger_line(obj).encode('utf-8')
    ledger_parse(new)
    lp = Path(repo) / LEDGER_FILE
    with open(lp, 'ab') as f:
        f.write(ledger_line(obj).encode('utf-8'))
        f.flush()
        os.fsync(f.fileno())
    ledger_git(repo, 'add', '--', LEDGER_FILE)
    ledger_git(repo, 'commit', '-q', '-m', msg, '--', LEDGER_FILE)
    return ledger_head(repo)


def folder_digest(path):
    """시도 폴더 (또는 거부 기록 파일 하나) 요약 = `sha256sum` 꼴 줄 (`<sha256>  <상대 경로>\\n`) 을 상대 경로 (POSIX · UTF-8 바이트) 차례로 이은 글의
    sha256 · 파일 하나 = 그 이름 한 줄 · 링크 · 특수 파일 · 못 읽음 = None (`cd 폴더 && find . -type f -printf '%P\\n' | LC_ALL=C sort | xargs sha256sum |
    sha256sum` 과 같은 값 · 빈 폴더는 줄이 없다)."""
    p = Path(path)
    rows = []
    try:
        if p.is_symlink():
            return None
        if p.is_file():
            rows.append((p.name, sha256_file(p)))
        elif p.is_dir():
            for root, dirs, files in os.walk(p):
                if any((Path(root) / nm).is_symlink() for nm in dirs):
                    return None
                for nm in files:
                    fp = Path(root) / nm
                    if fp.is_symlink() or not fp.is_file():
                        return None
                    rows.append((fp.relative_to(p).as_posix(), sha256_file(fp)))
        else:
            return None
    except OSError:
        return None
    rows.sort(key=lambda x: x[0].encode('utf-8'))
    return hashlib.sha256(''.join(f'{h}  {r}\n' for r, h in rows).encode('utf-8')).hexdigest()


def result_trace_name(nm):
    """결과 흔적 파일 이름 — 팔 payload (`p2_*.json*` · 쓰는 중 · 검사 실패본 포함) · 첫 풀이 끝 표지."""
    return (nm.startswith('p2_') and '.json' in nm) or nm.endswith(FIRST_RESULT_SUFFIX)


def folder_side(path):
    """결과 전 · 뒤 (Q9 §3-5 개정 4 · Q2) — 시도 폴더 (안 .unchecked/ 포함) 에 팔 payload 또는 첫 풀이 끝 표지가 하나라도 있으면 'post' · 거부 기록
    파일 하나 · 흔적 없는 폴더 = 'pre' (원인 무관)."""
    p = Path(path)
    if not p.is_dir():
        return 'pre'
    for _root, _dirs, files in os.walk(p):
        if any(result_trace_name(nm) for nm in files):
            return 'post'
    return 'pre'


def target_of(stage, law=None, variant=None, unit=None, point=None):
    """단계 → 원장 대상 이름 (ladder:<법칙>[:<변이>] · predict[:<변이>] · ★ 10-27 묶음 C2d unit[:<변이>]:<이름> · point[:<변이>]:<이름>)."""
    if stage == 'ladder':
        return f'ladder:{law}' + (f':{variant}' if variant else '')
    if unit or point:
        return unit_target('unit' if unit else 'point', variant, unit or point)
    return 'predict' + (f':{variant}' if variant else '')


def unit_name(c, law, rr):
    """★ 10-27 묶음 C2d (Q9 §3-1) — 단위 · 넘침 점 이름 <법칙>_c<c>_<R 역할> (예 P0_c0_R_j0)."""
    return f'{law}_c{c}_{rr}'


def unit_parse(name):
    """단위 이름 → (c, 법칙, R 역할) · 꼴 틀림 = None."""
    m = UNIT_RE.fullmatch(str(name))
    return (m.group(2), m.group(1), m.group(3)) if m else None


def unit_target(kind, variant, name):
    return f'{kind}' + (f':{variant}' if variant else '') + f':{name}'


def target_parts(target):
    """원장 대상 → (종류 unit | point, 변이 | None, 이름) · 단위 · 넘침 점 대상이 아니면 None."""
    m = TARGET_RE.fullmatch(str(target))
    if not m or not m.group(4):
        return None
    return m.group(4), m.group(5), f'{m.group(6)}_c{m.group(7)}_{m.group(8)}'


def target_dir(target):
    """합친 예측 안 시도 사본 자리 이름 (대상의 ':' → '-' · 예 unit-P0_c0_R_j0)."""
    return str(target).replace(':', '-')


def target_kits(target):
    return (SBE_KIT,) if str(target).startswith('ladder:') else (SBE_KIT, DBE_KIT)


def read_attempt(d):
    """시도 폴더의 attempt.json → dict | None (꼴 · 폴더 이름 = attempt_<n> · 시작 커밋 40-hex)."""
    p = Path(d) / ATTEMPT_FILE
    try:
        a = _json_strict(p.read_bytes()) if not p.is_symlink() else None
    except Exception:                                         # noqa: BLE001 — 못 읽음 = 시도 폴더 아님
        return None
    if not isinstance(a, dict) or set(a) != ATTEMPT_KEYS or a.get('schema') != ATTEMPT_SCHEMA:
        return None
    n = a.get('n')
    if type(n) is not int or n < 1 or Path(d).name != f'attempt_{n}' or not _hex40(a.get('ledger_commit')):
        return None
    if not (isinstance(a.get('target'), str) and TARGET_RE.fullmatch(a['target'])):
        return None
    return a


def adoption(st, target, sides=None, upto=None):
    """같은 대상 시도 (원장 차례) → {'attempts', 'adopted', 'chain', 'effective', 'problems'} — Q9 §3-5: 채택 = 처음 결과 전이 아닌 시도 (거부 · 결과 전
    멈춤 = 건너뜀) · 그 재실행 사슬 (원 시도를 가리키는 재실행 · 앞 사슬 끝이 재실행 자격으로 멈췄을 때만 · 거부된 재실행 = 건너뜀) · 채택 뒤 돈 새 시도 =
    ATTEMPT_AFTER_ADOPTED · 자격 없이 돈 재실행 = RESUME_NOT_ALLOWED · 결과 줄 없는 시도 = ATTEMPT_LEDGER_MISMATCH (recover 먼저).  sides = {n: 'pre' |
    'post'} (판정 = 폴더에서 · 없으면 결과 줄) · upto = 이 번호 앞만 (풀기 전 대조)."""
    ns = [k for k, e in st['entries'].items() if e['target'] == target and (upto is None or k < upto)]
    out = {'attempts': ns, 'adopted': None, 'chain': [], 'effective': None, 'problems': []}
    last = None
    for k in ns:
        e, r = st['entries'][k], st['results'].get(k)
        if r is None:
            out['problems'].append(('ATTEMPT_LEDGER_MISMATCH', f'항목 {k} ({target}) 의 결과 줄이 없다 (시도 중 · 사슬 부모 사망 = --stage recover 먼저)'))
            break
        side = (sides or {}).get(k, r['side'])
        ran = r['status'] != 'rejected'
        if out['adopted'] is None:
            if e['resume_of'] is not None:
                if ran:
                    out['problems'].append(('RESUME_NOT_ALLOWED', f'항목 {k}: 채택 전 시도의 재실행이 돌았다 (원 시도 {e["resume_of"]})'))
                continue
            if not ran or side == 'pre':
                continue
            out['adopted'], out['chain'], last = k, [k], r
            continue
        if not ran:
            continue                                          # 거부 기록만 = 기록만 (Q9 §3-4 R4-03)
        if e['resume_of'] == out['adopted'] and last['status'] != 'completed' and last['resume_ok']:
            out['chain'].append(k)
            last = r
            continue
        if e['resume_of'] is not None:
            out['problems'].append(('RESUME_NOT_ALLOWED', f'항목 {k}: 재실행 자격 없는 재실행이 돌았다 (원 시도 {e["resume_of"]} · 사슬 끝 '
                                                          f'attempt_{out["chain"][-1]})'))
        else:
            out['problems'].append(('ATTEMPT_AFTER_ADOPTED', f'항목 {k}: 채택 (attempt_{out["adopted"]}) 뒤 같은 대상 시도가 돌았다 (풀기 전 대조를 거치지 '
                                                             f'않은 흔적)'))
    out['effective'] = out['chain'][-1] if out['chain'] else None
    return out


def attempt_limit_problem(st, target, n, plan):
    k = sum(1 for x, e in st['entries'].items() if e['target'] == target and x <= n)
    mx = ((plan or {}).get('exec_policy') or {}).get('max_attempts')
    if type(mx) is not int:
        return ('PLAN_NUMBER_UNREGISTERED', 'exec_policy.max_attempts 가 없다 (봉인 전 계획)')
    if k > mx:
        return ('ATTEMPT_LIMIT', f'{target} 의 {k} 째 시도 > 최대 시도 수 {mx} (계획 exec_policy.max_attempts)')
    return None


def attempt_order_problem(st, e, plan):
    """새 항목 e (아직 원장 밖 · 또는 원장의 그 번호) 의 차례 · 채택 · 재실행 · 최대 수 (원장 st 의 앞 항목들로) → (멈춤, 사유) | None."""
    n, target = e['n'], e['target']
    prev = [k for k, x in st['entries'].items() if x['target'] == target and k < n]
    if prev and prev[-1] not in st['results']:
        return ('ATTEMPT_ORDER_MISMATCH', f'같은 대상 ({target}) 앞 항목 {prev[-1]} 의 결과 줄이 아직 없다 (차례로만 · 그룹 미확인 · 시도 중 = recover · 끝 먼저)')
    ent = dict(st['entries'])
    ent[n] = e
    lim = attempt_limit_problem(dict(st, entries=ent), target, n, plan)
    if lim:
        return lim
    ad = adoption(st, target, upto=n)
    if ad['problems']:
        return ad['problems'][0]
    if e['resume_of'] is None:
        if ad['adopted'] is not None:
            return ('ATTEMPT_AFTER_ADOPTED', f'{target} 은 이미 채택 시도 attempt_{ad["adopted"]} 가 있다 (결과 뒤 멈춤 · 완주 = 같은 등록의 재시도가 아니다 · '
                                             f'재실행은 --resume)')
        return None
    k = e['resume_of']
    last = st['results'].get(ad['effective']) if ad['effective'] is not None else None
    if ad['adopted'] != k or last is None:
        return ('RESUME_NOT_ALLOWED', f'원 시도 {k} 가 {target} 의 채택 시도가 아니다 (채택 = {ad["adopted"]})')
    if last['status'] == 'completed' or not last['resume_ok']:
        return ('RESUME_NOT_ALLOWED', f'재실행 사슬 끝 attempt_{ad["effective"]} = {last["status"]} · 원인 {last["cause"]} · 재실행 자격 {last["resume_ok"]} '
                                      f'(자원 · 인프라 원인 · 결과 뒤 · 검사 실패 흔적 없음 일 때만)')
    o = st['entries'][k]
    if e['machine'] != o['machine'] or e['env'] != o['env']:
        return ('RESUME_NOT_ALLOWED', f'재실행 기계 · 환경 지문 ≠ 원 시도 {k} (같은 기계 · 환경 지문의 모든 칸이 같아야 · Q9 R4-08 (d))')
    return None


def code_key_sha(code):
    return hashlib.sha256(code_key(code).encode('utf-8')).hexdigest()


def _env_diff(a, b, pre=''):
    if not (isinstance(a, dict) and isinstance(b, dict)):
        return [pre.rstrip('.') or '(전체)'] if a != b else []
    out = []
    for k in sorted(set(a) | set(b)):
        out += _env_diff(a.get(k), b.get(k), f'{pre}{k}.') if isinstance(a.get(k), dict) and isinstance(b.get(k), dict) else \
            ([f'{pre}{k}'] if a.get(k) != b.get(k) else [])
    return out


class Attempt:
    """시도 꼴 단계의 원장 손잡이 — 저장소 · 번호 · 항목 · 시도 폴더 · 시작 커밋 · 그 커밋의 원장 상태."""

    def __init__(self, repo, n, entry, folder, head, st):
        self.repo, self.n, self.entry, self.folder, self.head, self.st = Path(repo), n, entry, Path(folder), head, st
        self.resume_src, self.resume_eff = None, None           # ★ 10-27 묶음 C1b-2 — 재실행 원천 (사슬 끝 시도 폴더 · 번호)

    def runner_cls(self):
        return Runner if self.resume_src is None else ResumeRunner

    def runner_kw(self):
        return {} if self.resume_src is None else {'src': self.resume_src, 'src_n': self.resume_eff}

    def public(self):
        return {'n': self.n, 'target': self.entry['target'], 'machine': self.entry['machine'], 'resume_of': self.entry['resume_of'],
                'ledger': str(self.repo.resolve()), 'ledger_commit': self.head}


def _write_new_json(path, obj):
    """새 파일 (있으면 실패) 에 정준 JSON (원자적 · 같은 폴더 임시 → replace)."""
    path = Path(path)
    if path.exists() or path.is_symlink():
        raise FileExistsError(str(path))
    write_json_atomic(path, obj)


def attempt_reject(repo, raw, n, where, stop, head):
    """풀기 전 거부 — 거부 기록 (where = 시도 폴더 안 rejected.json 또는 옆 attempt_<n>.rejected.json) + 결과 줄 (rejected · 결과 전) + 커밋 → rc 3."""
    rec = {'schema': REJECTED_SCHEMA, 'n': n, 'code': stop.code, 'cause': stop.cause, 'ledger_commit': head, 'utc': _utc()}
    folder = where.parent if where.name == REJECTED_FILE else where
    try:
        _write_new_json(where, rec)
        res = {'kind': 'result', 'n': n, 'status': 'rejected', 'stop': {'code': stop.code, 'run': None, 'reason': None}, 'side': 'pre',
               'cause': 'presolve', 'resume_ok': False, 'folder': folder.name, 'folder_sha256': folder_digest(folder), 'by': 'chain', 'utc': _utc()}
        if res['folder_sha256'] is None:
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{folder} 요약 sha 를 못 셈')
        ledger_append(repo, res, f'rint-r attempt {n} rejected {stop.code}', expect=raw)
    except (OSError, Stop) as e:
        print_stop(stop)
        print_stop(e if isinstance(e, Stop) else Stop('ATTEMPT_LEDGER_MISMATCH', f'거부 기록을 못 썼다 ({type(e).__name__}: {e})'))
        return 3
    print_stop(stop)
    print(f'ATTEMPT_REJECTED n={n} code={stop.code} — 풀기 전 거부 (결과 전 · 거부 기록 {where.name} · 원장 결과 줄 커밋)')
    return 3


def attempt_open(a, stage):
    """★ 10-27 묶음 C1b — 시도 꼴 입구 (--ledger · --attempt) → None (시도 꼴 아님) | int (rc · 화면만 거부 또는 거부 기록을 쓴 거부) | Attempt.
    화면만 (원장 · 폴더 무변경): 원장 꼴 · 저장소 · 커밋 안 한 고침 · 원장에 없는 번호 · 이미 결과 줄이 있는 번호 (Q9 R4-13).  그 밖 풀기 전 대조 실패 =
    거부 기록 + 결과 줄 (결과 전 · 다음 시도 가능)."""
    if a.ledger is None and a.attempt is None:
        return None
    if a.ledger is None or a.attempt is None or getattr(a, 'dry_run', False):
        print('인자 오류: 시도 꼴 = --ledger <원장 저장소> 와 --attempt <항목 번호> 둘 다 (--dry-run 없이) — ★ 10-27 묶음 C1b', file=sys.stderr)
        return 2
    repo, n = Path(a.ledger), int(a.attempt)
    target = target_of(stage, getattr(a, 'law', None), a.variant, getattr(a, 'unit', None), getattr(a, 'point', None))
    base = Path(a.out)
    try:
        why = ledger_repo_problem(repo)
        if why:
            raise Stop('ATTEMPT_LEDGER_MISMATCH', why)
        head, raw = ledger_now(repo)
        st = ledger_parse(raw)
        if n not in st['entries']:
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'원장에 항목 {n} 이 없다 (--stage ledger --add 먼저)')
        if n in st['results']:
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'항목 {n} 은 이미 결과 줄이 있다 (Q9 R4-13 · 시도 폴더 · 거부 기록을 만들지 않는다)')
    except Stop as e:
        print_stop(e)
        return 3
    e = st['entries'][n]
    folder = base / f'attempt_{n}'
    try:
        base.mkdir(parents=True, exist_ok=True)
        folder.mkdir()
    except FileExistsError:
        return attempt_reject(repo, raw, n, base / f'attempt_{n}{REJECTED_SIDE}',
                              Stop('OUTDIR_NOT_EMPTY', f'{folder} 가 이미 있다 — 시도 폴더는 시도마다 새로'), head)
    except OSError as ex:
        print_stop(Stop('ATTEMPT_LEDGER_MISMATCH', f'시도 폴더를 못 만든다 ({type(ex).__name__}: {ex})'))
        return 3
    write_json_atomic(folder / ATTEMPT_FILE, {'schema': ATTEMPT_SCHEMA, 'n': n, 'target': e['target'], 'machine': e['machine'],
                                              'resume_of': e['resume_of'], 'ledger_commit': head})
    try:
        prob = attempt_presolve_problem(st, e, n, target, a, stage)
        if not prob and getattr(a, 'point', None):           # ★ 10-27 묶음 C2d — 넘침 점 = 결정 기록 (점 · 변이 · 사다리 · 계획 · 원장 조상)
            prob = expansion_presolve_problem(a, e, repo, head)
    except Stop as ex:
        prob = (ex.code, ex.cause)
    if prob:
        return attempt_reject(repo, raw, n, folder / REJECTED_FILE, Stop(*prob), head)
    att = Attempt(repo, n, e, folder, head, st)
    if e['resume_of'] is not None:
        att.resume_src, att.resume_eff = resume_source(st, e, n, base)
    return att


def attempt_plan(a, stage, e):
    """풀기 전 대조의 계획 — 사다리 = --plan · 예측 = 첫 사다리 요약의 계획 (그 sha256 = 항목 계획이어야 · 단계가 다시 대조한다)."""
    if stage == 'ladder':
        return load_plan(a.plan)
    s, _sha = read_summary(Path((a.ladders or [None])[0] or '/nonexistent'), 'ladder_summary.json')
    plan = ((s or {}).get('plan') or {}).get('content')
    sha = ((s or {}).get('plan') or {}).get('sha256')
    if not isinstance(plan, dict) or not _hex64(sha):
        raise Stop('LADDER_SET', '첫 사다리 폴더의 요약 · 계획을 못 읽는다 (예측 시도의 계획 대조)')
    return plan, sha


def attempt_presolve_problem(st, e, n, target, a, stage):
    """풀기 전 대조 (Q9 §3-2 · C1 동일 설정 요건) → (멈춤, 사유) | None — 대상 · 기계 · 계획 · 코드 키 · 환경 지문 (모든 칸) · 침대 · 차례 · 채택 ·
    재실행 · 최대 시도 수."""
    if e['target'] != target:
        return ('ATTEMPT_LEDGER_MISMATCH', f'항목 {n} 대상 {e["target"]} ≠ 이 단계 {target}')
    if a.machine != e['machine']:
        return ('MACHINE_NOT_ALLOWED', f'--machine {a.machine!r} ≠ 항목 {n} 의 기계 {e["machine"]!r}')
    plan, plan_sha = attempt_plan(a, stage, e)
    if plan_sha != e['plan_sha256']:
        return ('PLAN_HASH_MISMATCH', f'계획 sha256 ≠ 항목 {n} (원장 머리) 의 계획')
    code = code_record(a.runner)
    if code_key_sha(code) != e['code_key_sha256']:
        return ('CODE_PIN_MISMATCH', f'코드 키 (HEAD · 저장소 상대 경로 · 코드 파일 지문 · 러너 · 환경 단위) ≠ 항목 {n}')
    if code['env'] != e['env']:
        return ('CODE_PIN_MISMATCH', f'환경 지문 ≠ 항목 {n} (칸 {", ".join(_env_diff(e["env"], code["env"])[:6])} — 같은 셸 · venv 에서 --add 한 뒤 돌린다)')
    bed = {k: kit_bed(a.root, k) for k in target_kits(target)}
    if bed != e['bed']:
        return ('S0_REPORT_MISMATCH', f'침대 (킷 원 입력 지문) ≠ 항목 {n} ({", ".join(k for k in bed if bed[k] != e["bed"].get(k))})')
    prob = attempt_order_problem(st, e, plan)
    if prob:
        return prob
    if e['resume_of'] is not None:                         # ★ 10-27 묶음 C1b-2 — 재실행 원천 = 같은 바탕의 사슬 끝 시도 폴더 (결과 줄과 같은 폴더)
        src, eff = resume_source(st, e, n, a.out)
        r = st['results'].get(eff)
        if read_attempt(src) is None or r is None or r['folder'] != src.name or folder_digest(src) != r['folder_sha256']:
            return ('RESUME_NOT_ALLOWED', f'재실행 원천 {src} (재실행 사슬 끝 attempt_{eff}) 가 없거나 원장 결과 줄과 다르다 (같은 기계 · 같은 바탕 폴더에서)')
    return None


def resume_source(st, e, n, base):
    """재실행 항목 → (원천 폴더 = <바탕>/attempt_<사슬 끝>, 사슬 끝 번호)."""
    eff = adoption(st, e['target'], upto=n)['effective']
    return Path(base) / f'attempt_{eff}', eff


def expansion_form_problem(d):
    """★ 10-27 묶음 C2d (Q9 §3-2 결정 기록 꼴) → 사유 | None — 칸 · schema · 변이 · 점 (단위 이름 · 중복 없음) · 넘침 목록 = 점 · 시도 sha 집합 ([대상 · 번호 ·
    폴더 요약 sha] 차례) · 원장 (경로 · 커밋 · sha256) · 사다리 (법칙마다 요약 sha) · 계획 sha."""
    if not isinstance(d, dict) or set(d) != EXPANSION_KEYS or d.get('schema') != EXPANSION_SCHEMA:
        return f'칸 · schema (= {sorted(EXPANSION_KEYS)} · {EXPANSION_SCHEMA})'
    if d['variant'] is not None and d['variant'] not in VARIANTS:
        return f'변이 {d["variant"]!r}'
    pts = d['points']
    if not (isinstance(pts, list) and pts and all(isinstance(p, str) and UNIT_RE.fullmatch(p) for p in pts) and len(set(pts)) == len(pts)):
        return f'점 {pts!r}'
    if d['overflow'] != [list(unit_parse(p)) for p in pts]:
        return '넘침 목록 ≠ 점'
    at = d['attempts']
    if not (isinstance(at, list) and all(isinstance(x, list) and len(x) == 3 and isinstance(x[0], str) and type(x[1]) is int and _hex64(x[2])
                                         for x in at) and at == sorted(at)):
        return '시도 sha 집합 꼴'
    L = d['ledger']
    if not (isinstance(L, dict) and set(L) == {'path', 'commit', 'sha256'} and _hex40(L.get('commit')) and _hex64(L.get('sha256'))):
        return '원장 칸'
    if not (isinstance(d['ladders'], dict) and sorted(d['ladders']) == sorted(LAWS) and all(_hex64(v) for v in d['ladders'].values())):
        return '사다리 칸'
    if not _hex64(d['plan_sha256']):
        return '계획 sha'
    return None


def read_expansion(path):
    """결정 기록 (expansion.json) → (dict, sha256 (파일 바이트)) · 못 읽음 · 꼴 틀림 = Stop UNIT_PROVENANCE_MISMATCH."""
    try:
        raw = Path(path).read_bytes()
        d = _json_strict(raw)
    except Exception as e:                                    # noqa: BLE001 — 못 읽음 = 출처 없음
        raise Stop('UNIT_PROVENANCE_MISMATCH', f'결정 기록 {path} 를 못 읽는다 ({type(e).__name__})')
    why = expansion_form_problem(d)
    if why:
        raise Stop('UNIT_PROVENANCE_MISMATCH', f'결정 기록 {Path(path).name} 꼴 — {why}')
    return d, hashlib.sha256(raw).hexdigest()


def ladders_sha_of(dirs):
    """사다리 폴더들 → {법칙: 요약 sha256} (결정 기록 · 단위 출처 대조)."""
    out = {}
    for d in dirs or []:
        s, sha = read_summary(Path(d), 'ladder_summary.json')
        out[(s or {}).get('law')] = sha
    return out


def expansion_presolve_problem(a, e, repo, head):
    """★ 10-27 묶음 C2d (Q9 §3-2 넘침 실행 · 풀기 전 대조) — 결정 기록 꼴 · 같은 변이 · 이 점이 그 넘침 목록 안 · 같은 사다리 (요약 sha) · 같은 계획 ·
    결정 기록의 원장 커밋 = 이 원장 HEAD 의 조상 · 그 커밋 원장 sha256 → (UNIT_PROVENANCE_MISMATCH, 사유) | None (거부 = 결과 전)."""
    try:
        dec, _sha = read_expansion(a.expand)
    except Stop as ex:
        return (ex.code, ex.cause)
    why = None
    if dec['variant'] != a.variant:
        why = f'결정 기록 변이 {dec["variant"]!r} ≠ {a.variant!r}'
    elif a.point not in dec['points']:
        why = f'점 {a.point} 이 결정 기록의 넘침 목록 {dec["points"]} 에 없다 (결정 기록이 요구한 origin8 런만)'
    elif dec['ladders'] != ladders_sha_of(a.ladders):
        why = '결정 기록의 사다리 요약 sha ≠ 이 시도의 사다리'
    elif dec['plan_sha256'] != e['plan_sha256']:
        why = '결정 기록의 계획 sha256 ≠ 원장 항목'
    elif not ledger_is_ancestor(repo, dec['ledger']['commit'], head):
        why = f'결정 기록의 원장 커밋 {dec["ledger"]["commit"][:12]} 이 이 원장 HEAD 의 조상이 아니다 (다른 원장 · 다른 가지의 첫 합치기)'
    elif hashlib.sha256(ledger_blob(repo, dec['ledger']['commit'])).hexdigest() != dec['ledger']['sha256']:
        why = '결정 기록의 원장 sha256 ≠ 그 커밋의 원장'
    return ('UNIT_PROVENANCE_MISMATCH', why) if why else None


def attempt_groups_problem(folder):
    """시도 폴더의 그룹 기록 — 시작 기록마다 끝 기록 · 확인 True (아니면 사유 · 결과 줄을 쓰지 않는다 · recover 먼저)."""
    for lp in sorted(Path(folder).rglob(f'{GROUPS_DIR}/*.launch.json')):
        ep = lp.with_name(lp.name[:-len('.launch.json')] + '.end.json')
        try:
            er = json.loads(ep.read_text(encoding='utf-8')) if ep.exists() else None
        except (OSError, UnicodeDecodeError, ValueError):
            er = None
        if not (isinstance(er, dict) and er.get('confirmed') is True):
            return f'그룹 {lp.parent.parent.name}/{lp.name[:-len(".launch.json")]} 종료 미확인'
    return None


def _stopped_run(s, folder):
    run = (s.get('stop') or {}).get('run')
    rr = [r for r in (s.get('runs') or []) if r.get('name') == run] if run else []
    return (rr[-1] if rr else None), (Path(folder) / rr[-1]['outdir'] if rr and rr[-1].get('outdir') else None)


def check_trace(folder, od=None):
    """검사 실패 흔적 (Q9 §3-5 재실행 자격) — 멈춘 런 폴더 (없으면 시도 폴더 전부) 의 .unchecked/ 에 팔 payload (표지 아님) 가 있음."""
    roots = [od] if od is not None else [p for p in Path(folder).rglob(UNCHECKED_DIR) if p.is_dir()]
    for r in roots:
        u = Path(r) / UNCHECKED_DIR if od is not None else Path(r)
        if u.is_dir() and any(result_trace_name(p.name) and not p.name.endswith(FIRST_RESULT_SUFFIX) for p in u.iterdir()):
            return True
    return False


def stop_cause(s, folder):
    """멈춘 단계 요약 → 원인 이름 (기록 · 재실행 자격) — timeout · signal · group_unconfirmed · resource (러너 rc · 그 런 로그에 자원 낱말) · runner_rc ·
    gate (런 없이 멈춤) · check (팔을 읽은 뒤의 멈춤 · 등록 결과)."""
    code = (s.get('stop') or {}).get('code') or s.get('status')
    if code == 'TIME_LIMIT':
        return 'timeout'
    if code == 'GROUP_UNCONFIRMED':
        return 'group_unconfirmed'
    if code == 'RUNNER_RC':
        rr, _od = _stopped_run(s, folder)
        gc = (rr or {}).get('group_cause')
        if gc in ('signal', 'signal_after'):
            return 'signal'
        if gc == 'timeout':
            return 'timeout'
        run = (s.get('stop') or {}).get('run')
        lp = Path(folder) / 'logs' / f'{run}.log' if run else None
        try:
            txt = lp.read_text(encoding='utf-8', errors='replace') if lp is not None and lp.is_file() else ''
        except OSError:
            txt = ''
        return 'resource' if any(w in txt for w in RESOURCE_WORDS) else 'runner_rc'
    return 'gate' if not s.get('runs') else 'check'


def attempt_result_line(n, folder, s, by):
    """단계 요약 (없으면 None = 사슬 부모 사망) → 결과 줄."""
    folder = Path(folder)
    side = folder_side(folder)
    if s is None:
        status, stop, cause = 'interrupted', None, 'parent_dead'
        trace = check_trace(folder)
    else:
        done = s.get('status') in DONE_STATUSES
        status = 'completed' if done else 'stopped'
        sr = s.get('stop') or {}
        stop = None if done else {'code': sr.get('code') or s.get('status'), 'run': sr.get('run'), 'reason': sr.get('reason')}
        cause = None if done else stop_cause(s, folder)
        _rr, od = _stopped_run(s, folder)
        trace = False if done else (check_trace(folder, od) if od is not None else check_trace(folder))
    resume_ok = status != 'completed' and side == 'post' and cause in RESUME_CAUSES and not trace
    dg = folder_digest(folder)
    if dg is None:
        raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{folder} 요약 sha 를 못 셈 (링크 · 특수 파일)')
    return {'kind': 'result', 'n': n, 'status': status, 'stop': stop, 'side': side, 'cause': cause, 'resume_ok': bool(resume_ok),
            'folder': folder.name, 'folder_sha256': dg, 'by': by, 'utc': _utc()}


def attempt_close(att, s):
    """단계 끝 — 시도 폴더의 그룹이 다 확인됐으면 결과 줄 (사슬) + 커밋 → None (rc 그대로) | 3 (결과 줄을 못 씀 · 미확인 = recover)."""
    why = attempt_groups_problem(att.folder)
    if why:
        print(f'ATTEMPT_OPEN n={att.n} — 결과 줄을 쓰지 않았다 ({why}) — 사람이 보고 --stage recover --out {att.folder} --ledger {att.repo}')
        return 3
    try:
        res = attempt_result_line(att.n, att.folder, s, 'chain')
        ledger_append(att.repo, res, f'rint-r attempt {att.n} result {res["status"]}')
    except Stop as e:
        print_stop(e)
        return 3
    print(f'ATTEMPT_RESULT n={att.n} status={res["status"]} side={res["side"]} cause={res["cause"]} resume_ok={res["resume_ok"]}')
    return None


def ledger_inputs_check(dirs, repo, commit, st, want_prefix=None):
    """예측의 사다리 입력 (원장 시도) — 폴더마다 attempt.json · 이 원장의 시작 커밋 (조상) · 항목 · 결과 줄 · 폴더 요약 sha · 채택 (effective) 이어야 →
    {폴더: 번호} · 아니면 Stop ATTEMPT_LEDGER_MISMATCH (원장 판정의 대조 = `ledger_verdict_check`)."""
    out = {}
    for d in dirs:
        a = read_attempt(d)
        if a is None:
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{Path(d).name}: 원장 시도 폴더가 아니다 (attempt.json · 원장 꼴 단계의 입력 = 원장 시도만)')
        if want_prefix is not None and not a['target'].startswith(want_prefix):
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{Path(d).name}: 대상 {a["target"]} (사다리여야)')
        if not ledger_is_ancestor(repo, a['ledger_commit'], commit):
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{Path(d).name}: 시작 커밋 {a["ledger_commit"][:12]} 이 이 원장 ({repo}) 의 조상이 아니다 (다른 원장의 시도)')
        n = a['n']
        e, r = st['entries'].get(n), st['results'].get(n)
        if e is None or e['target'] != a['target'] or r is None:
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{Path(d).name}: 원장 항목 · 결과 줄 ≠ 시도 폴더')
        if folder_digest(d) != r['folder_sha256'] or r['folder'] != Path(d).name:
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{Path(d).name}: 폴더 요약 sha ≠ 원장 결과 줄')
        ad = adoption(st, a['target'])
        if ad['problems']:
            raise Stop(*ad['problems'][0])
        if ad['effective'] != n:
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{Path(d).name}: {a["target"]} 의 채택 시도가 아니다 (채택 = attempt_{ad["effective"]})')
        out[str(Path(d).resolve())] = n
    return out


def ledger_input(path, attempt_dirs):
    """판정의 원장 입력 기록 → {'path', 'commit' (지금 HEAD · 못 읽음 = None → 판정 멈춤), 'attempt_dirs'} | None (원장 없는 판정)."""
    if not path:
        return None
    try:
        commit = ledger_head(Path(path))
    except Stop:
        commit = None
    return {'path': str(Path(path).resolve()), 'commit': commit, 'attempt_dirs': [str(Path(x).resolve()) for x in (attempt_dirs or [])]}


def _attempt_folders(bases):
    """바탕 폴더들 → {n: [경로 …]} (attempt_<n> 폴더 · attempt_<n>.rejected.json 파일)."""
    found = {}
    for b in sorted({Path(x).resolve() for x in bases}):
        if not b.is_dir():
            continue
        for p in sorted(b.iterdir()):
            m = ATTEMPT_DIR_RE.fullmatch(p.name) if p.is_dir() else ATTEMPT_SIDE_RE.fullmatch(p.name)
            if m:
                found.setdefault(int(m.group(1)), [])
                if p not in found[int(m.group(1))]:
                    found[int(m.group(1))].append(p)
    return found


def target_ledger_problem(repo, st, raw, commit, target, found):
    """★ 10-27 묶음 C2d — 대상 하나의 원장 · 시도 폴더 대조 (판정 `ledger_verdict_check` · 합치기 `MergeFetch` · 합친 예측 판정 `merged_ledger_check` 가 같은
    함수 · C1b 판정 고리 그대로 + 한 항목 폴더 둘 = 멈춤): 그 대상 항목마다 결과 줄 · 폴더 (found {n: [경로]} · 없으면 엄격 결과 뒤 · 결과 줄과 다른 이름 ·
    같은 이름 둘) · 요약 sha = 결과 줄 · 결과 전 · 뒤 = 폴더 · attempt.json · 시작 커밋 (조상 · 바이트 접두 · 같은 대상 앞 결과 줄) → 채택 (폴더의 결과 전 ·
    뒤) → (항목 번호 목록, 채택, {n: 경로}) · 실패 = Stop."""
    ns = [k for k, e in st['entries'].items() if e['target'] == target]
    sides, paths = {}, {}
    for k in ns:
        r = st['results'].get(k)
        if r is None:
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'항목 {k} ({target}) 의 결과 줄이 없다 (시도 중 · --stage recover 먼저)')
        cand = found.get(k) or []
        hit = [p for p in cand if p.name == r['folder']]
        extra = [p for p in cand if p.name != r['folder']]
        if extra:
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'원장에 없는 시도 폴더 {[p.name for p in extra]} (항목 {k} 의 결과 줄 폴더 = {r["folder"]})')
        if not hit:                                           # 폴더 없는 시도 (거부 기록 없음 · 소실) = 엄격 결과 뒤 → 이 대상은 판정할 수 없다 (Q9 §3-5 개정 3)
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'항목 {k} ({target}) 의 시도 폴더 · 거부 기록 {r["folder"]} 이 없다 (엄격 — 결과 뒤로 본다 · 그 대상 '
                                                  f'판정 없음 · 다른 곳에 둔 시도 = 판정 --attempt-dirs · 합치기 --merge 경로)')
        if len(hit) > 1:                                      # ★ 10-27 묶음 C2d — 한 항목 = 폴더 하나 (Q9 §3-5 "막는 것: 한 항목에 폴더 둘")
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'항목 {k} ({target}) 의 시도 폴더 · 거부 기록이 둘 ({[str(p) for p in hit][:2]}) — 한 항목 = 폴더 하나 '
                                                  f'(Q9 §3-5)')
        p = hit[0]
        if folder_digest(p) != r['folder_sha256']:
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{p.name}: 폴더 요약 sha ≠ 원장 결과 줄 {k}')
        sides[k] = folder_side(p)
        if sides[k] != r['side']:
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{p.name}: 결과 줄 {k} 의 결과 {r["side"]} ≠ 폴더 ({sides[k]} — 표지 · payload 유무)')
        if p.is_dir():
            a = read_attempt(p)
            if a is None or a['n'] != k or a['target'] != target:
                raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{p.name}: attempt.json ≠ 원장 항목 {k}')
            c0 = a['ledger_commit']
            if not ledger_is_ancestor(repo, c0, commit):
                raise Stop('ATTEMPT_ORDER_MISMATCH', f'{p.name}: 시작 커밋 {c0[:12]} 이 원장 커밋 {commit[:12]} 의 조상이 아니다 (곁가지에서 시작 · R4-07)')
            raw0 = ledger_blob(repo, c0)
            if not raw.startswith(raw0):
                raise Stop('ATTEMPT_ORDER_MISMATCH', f'{p.name}: 시작 커밋의 원장이 원장의 바이트 접두가 아니다 (R4-07)')
            st0 = ledger_parse(raw0)
            if k not in st0['entries'] or any(j not in st0['results'] for j in ns if j < k):
                raise Stop('ATTEMPT_ORDER_MISMATCH', f'{p.name}: 시작 커밋에 자기 항목 · 같은 대상 앞 결과 줄이 없다 (차례로만)')
        paths[k] = p
    ad = adoption(st, target, sides=sides)
    if ad['problems']:
        raise Stop(*ad['problems'][0])
    return ns, ad, paths


def ledger_verdict_check(dirs, repo, attempt_dirs=(), commit=None):
    """★ 10-27 묶음 C1b — 판정 입력 ↔ 원장 (Q9 §3-4 · §3-5): 원장 (commit · 없으면 HEAD) = HEAD 의 조상 · 바이트 접두 · 역사 덧붙이기만 · 입력마다 원장 시도
    폴더 · 입력 대상의 시도 전부 = 폴더 (입력의 부모 폴더 · attempt_dirs 에서 찾음 · 없으면 엄격 결과 뒤) 요약 sha = 결과 줄 · 원장에 없는 시도 폴더 = 멈춤 ·
    결과 줄의 결과 전 · 뒤 = 폴더 · 시작 커밋 = 조상 · 바이트 접두 · 같은 대상 앞 결과 줄 있음 · 채택 (재실행 사슬 끝) = 입력 · 최대 시도 수 → 공개 기록."""
    repo = Path(repo)
    why = ledger_repo_problem(repo)
    if why:
        raise Stop('ATTEMPT_LEDGER_MISMATCH', why)
    head = ledger_head(repo)
    commit = commit or head
    if not ledger_is_ancestor(repo, commit, head):
        raise Stop('ATTEMPT_LEDGER_MISMATCH', f'원장 커밋 {commit[:12]} 이 지금 HEAD 의 조상이 아니다 (역사가 바뀌었다)')
    raw, raw_head = ledger_blob(repo, commit), ledger_blob(repo, head)
    if not raw_head.startswith(raw):
        raise Stop('ATTEMPT_LEDGER_MISMATCH', '원장 HEAD 가 그 커밋 원장의 바이트 이어 붙임이 아니다')
    why = ledger_history_problem(repo, head)
    if why:
        raise Stop('ATTEMPT_LEDGER_MISMATCH', f'원장 역사: {why}')
    st = ledger_parse(raw)
    want, merged = {}, []
    for d in dirs:
        a = read_attempt(d)
        if a is None:
            sm, _sha = read_summary(Path(d), 'predict_summary.json')
            if isinstance(sm, dict) and isinstance(sm.get('merge'), dict):   # ★ 10-27 묶음 C2d — 합친 예측 (같은 대조를 아래 `merged_ledger_check` 에서 다시)
                merged.append((Path(d).resolve(), sm))
                continue
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{Path(d).name}: 원장 시도 폴더가 아니다 (원장 판정의 입력 = 원장 시도 · 합친 예측만)')
        if a['n'] not in st['entries'] or st['entries'][a['n']]['target'] != a['target']:
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{Path(d).name}: 원장 항목 ≠ 시도 폴더')
        if a['target'] in want:
            raise Stop('DUPLICATE_RUN', f'같은 대상 {a["target"]} 입력 둘')
        want[a['target']] = (a['n'], Path(d).resolve())
    mdirs = {x for x, _s in merged}
    found = _attempt_folders([Path(d).resolve().parent for d in dirs if Path(d).resolve() not in mdirs] + [Path(x) for x in attempt_dirs])
    for k in sorted(found):
        if k not in st['entries']:
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'원장에 없는 시도 폴더 {[p.name for p in found[k]]} (항목 {k})')
    pub = {'path': str(repo.resolve()), 'commit': commit, 'sha256': hashlib.sha256(raw).hexdigest(),
           'attempt_dirs': [str(Path(x).resolve()) for x in attempt_dirs], 'targets': {}}
    for target, (n_in, d_in) in sorted(want.items()):
        ns, ad, _paths = target_ledger_problem(repo, st, raw, commit, target, found)   # ★ 10-27 묶음 C2d — 같은 함수 (합치기 · 합친 예측 판정)
        lim = attempt_limit_problem(st, target, max(ns), (read_summary(d_in, 'ladder_summary.json')[0]
                                                         or read_summary(d_in, 'predict_summary.json')[0] or {}).get('plan', {}).get('content'))
        if lim and lim[0] == 'ATTEMPT_LIMIT':
            raise Stop(*lim)
        if ad['effective'] is None or ad['effective'] != n_in:
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{d_in.name}: {target} 의 채택 시도가 아니다 (채택 = attempt_{ad["effective"]} · 원장 · 폴더 · 규칙이 '
                                                  f'정한다)')
        pub['targets'][target] = {'attempts': ad['attempts'], 'adopted': ad['adopted'], 'chain': ad['chain'], 'effective': ad['effective']}
    if merged:                                                # ★ 10-27 묶음 C2d — 합친 예측마다 같은 대조 (사본 · 채택 · 출처 · 합친 런 · 남는 런)
        pub['merged'] = {}
        for d_m, sm in merged:
            got = merged_ledger_check(d_m, sm, repo, st, raw, commit)
            pub['merged'][str(d_m)] = {'commit': got['commit']}
            pub['targets'].update(got['targets'])
    return pub


def merged_ledger_check(d, s, repo, st, raw, commit):
    """★ 10-27 묶음 C2d (Q9 §3-4 끝 줄 "판정 · 다시 판정이 같은 대조를 다시 한다") — 합친 예측 폴더 ↔ 판정 원장 (commit): 합치기 원장 커밋 = 조상 · 그 원장 =
    sha · 바이트 접두 · 사본 (units/<대상>/attempt_<n>) = 원장 항목 (원장에 없는 · 다른 대상 · 다른 변이 = 멈춤) · 합치기가 연 대상마다 같은 원장 대조
    (`target_ledger_problem` · 사본에서) · 채택 · 사슬 = 기록 · 단위 요약 출처 (`unit_summary_problem`) · 합친 런마다 source = 그 요청의 대상 · 채택 시도 ·
    단위 안 런 · 자리 · 기계 · 결정 기록 사본 sha · 넘침 목록 (PREDICTED) · PREDICTED 이면 남는 채택 런 = UNIT_EXTRA → {'commit', 'targets'}."""
    mg = s.get('merge') if isinstance(s.get('merge'), dict) else {}
    if mg.get('schema') != MERGE_SCHEMA:
        raise Stop('UNIT_PROVENANCE_MISMATCH', f'{d.name}: 합친 예측의 merge 칸 꼴 (schema {MERGE_SCHEMA})')
    L = mg.get('ledger') if isinstance(mg.get('ledger'), dict) else {}
    c_m = L.get('commit')
    if not (_hex40(c_m) and ledger_is_ancestor(repo, c_m, commit)):
        raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{d.name}: 합치기 원장 커밋 {str(c_m)[:12]} 이 판정 원장 커밋 {commit[:12]} 의 조상이 아니다')
    blob = ledger_blob(repo, c_m)
    if hashlib.sha256(blob).hexdigest() != L.get('sha256') or not raw.startswith(blob):
        raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{d.name}: 합치기 원장 sha ≠ 그 커밋 원장 · 판정 원장의 바이트 접두가 아니다')
    variant = s.get('variant')
    plan = (s.get('plan') or {}).get('content') if isinstance(s.get('plan'), dict) else None
    ub = d / UNITS_DIR
    found = _attempt_folders(sorted(p for p in ub.iterdir() if p.is_dir())) if ub.is_dir() else {}
    for k, ps in sorted(found.items()):
        e = st['entries'].get(k)
        tp = target_parts(e['target']) if e else None
        if e is None or tp is None or tp[1] != variant or any(p.parent.name != target_dir(e['target']) for p in ps):
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{d.name}: 사본 {[str(p.relative_to(d)) for p in ps][:2]} ≠ 원장 항목 {k} (원장에 없는 · 다른 대상 · 다른 변이)')
    want = merge_want(s)
    ex = mg.get('expansion')
    dsha = None
    if ex is not None:
        dsha = ex.get('sha256') if isinstance(ex, dict) else None
        cp = d / EXPANSION_FILE
        if not (isinstance(dsha, str) and cp.is_file() and sha256_file(cp) == dsha):
            raise Stop('UNIT_PROVENANCE_MISMATCH', f'{d.name}: 결정 기록 사본 {EXPANSION_FILE} ≠ merge.expansion sha')
        dec, _dsha = read_expansion(cp)
        adj = [unit_name(o.get('c'), o.get('law'), rr) for o in s.get('origin') or [] if isinstance(o, dict) and o.get('status') == 'adjusted'
               for rr in RJ_ROLES]
        if s.get('status') == 'PREDICTED' and dec['points'] != adj:
            raise Stop('UNIT_PROVENANCE_MISMATCH', f'{d.name}: 결정 기록 넘침 목록 ≠ 합친 예측의 origin 결정 ({len(dec["points"])} ↔ {len(adj)})')
    units = mg.get('units') if isinstance(mg.get('units'), dict) else {}
    lads = s.get('ladders') if isinstance(s.get('ladders'), dict) else {}
    allowed = ((plan or {}).get('exec_policy') or {}).get('allowed_machines') or []
    eff, pub_t = {}, {}
    for t, u in sorted(units.items()):
        tp = target_parts(t)
        if tp is None or tp[1] != variant or not isinstance(u, dict):
            raise Stop('UNIT_PROVENANCE_MISMATCH', f'{d.name}: merge.units 대상 {t!r} (이 변이의 단위 · 넘침 점이 아니다)')
        ns, ad, paths = target_ledger_problem(repo, st, raw, commit, t, found)
        lim = attempt_limit_problem(st, t, max(ns), plan) if ns else None
        if lim and lim[0] == 'ATTEMPT_LIMIT':
            raise Stop(*lim)
        n = ad['effective']
        if n is None or n != u.get('attempt') or ad['adopted'] != u.get('adopted') or ad['chain'] != u.get('chain'):
            raise Stop('UNIT_PROVENANCE_MISMATCH', f'{d.name}: {t} 채택 {n} · 사슬 {ad["chain"]} ≠ 합친 기록 {u.get("attempt")} · {u.get("chain")}')
        su, sha = read_summary(paths[n], UNIT_SUMMARY[tp[0]])
        entry = st['entries'][n]
        why = unit_summary_problem(su, tp[0], t, n, entry, want, dsha)
        if why is None and (entry['machine'] not in allowed or u.get('machine') != entry['machine']):
            why = f'기계 {u.get("machine")!r} · 원장 {entry["machine"]!r} · 허용 목록 {allowed}'
        if why is None and (u.get('summary_sha256') != sha or u.get('folder') != f'{UNITS_DIR}/{target_dir(t)}/attempt_{n}'):
            why = 'merge.units 기록 (요약 sha · 자리) ≠ 사본'
        if why:
            raise Stop('UNIT_PROVENANCE_MISMATCH', f'{d.name}: {t} attempt_{n}: {why}')
        eff[t] = (n, {r.get('name'): r for r in su.get('runs') or [] if isinstance(r, dict)})
        pub_t[t] = {'attempts': ad['attempts'], 'adopted': ad['adopted'], 'chain': ad['chain'], 'effective': n}
    used = {t: set() for t in eff}
    for r in s.get('runs') or []:
        src = r.get('source') if isinstance(r.get('source'), dict) else {}
        t = src.get('target')
        rr = [k for k in RJ_ROLES if (lads.get(r.get('law')) or {}).get(k) == r.get('rj')]
        want_t = (unit_target('point' if r.get('role') == 'origin8' else 'unit', variant, unit_name(r.get('c'), r.get('law'), rr[0]))
                  if len(rr) == 1 else None)
        n, runs_u = eff.get(t) or (None, {})
        iname = f'{UNIT_PREFIX}{UNIT_RUN_INDEX.get(r.get("role"), 0):02d}_{r.get("role")}'
        rec_u = runs_u.get(src.get('run'))
        ok = (t is not None and t == want_t and t in eff and src.get('attempt') == n and src.get('run') == iname and rec_u is not None
              and rec_u.get('outdir') == src.get('outdir') and all(rec_u.get(k) == r.get(k) for k in REQ_KEYS if k != 'name')
              and r.get('outdir') == f'{UNITS_DIR}/{target_dir(t)}/attempt_{n}/{src.get("outdir")}' and r.get('machine') == (units.get(t) or {}).get('machine')
              and iname not in used[t])
        if not ok:
            raise Stop('UNIT_PROVENANCE_MISMATCH', f'{d.name}: 합친 런 {r.get("name")} 의 출처 {src} ≠ 그 요청의 대상 {want_t} · 채택 시도 · 단위 안 런 · 자리')
        used[t].add(iname)
    if s.get('status') == 'PREDICTED':
        extra = [f'{t}/{nm}' for t, (_n, runs_u) in sorted(eff.items()) for nm in sorted(runs_u) if nm not in used[t]]
        for t in unit_targets(st, variant):
            if t in eff:
                continue
            try:
                _ns, ad, _p = target_ledger_problem(repo, st, raw, commit, t, found)
                if ad['effective'] is not None:
                    extra.append(f'{t}/attempt_{ad["effective"]}')
            except Stop as e:
                extra.append(f'{t} (대조 실패 {e.code})')
        if extra:
            raise Stop('UNIT_EXTRA', f'{d.name}: 합친 예측 (PREDICTED) 인데 채택 런이 남았다 ({extra[:4]}{" …" if len(extra) > 4 else ""})')
    return {'commit': c_m, 'targets': pub_t}


def run_request(prefix, n, kit, role, law, c, rj, arms, sv_cf, variant):
    """런 요청 하나 → (이름 <앞자리><번호>_<역할>, 요청 dict, 중복 키) — `Runner` · ★ 10-27 묶음 C2d 합치기 fetch (`MergeFetch`) 가 같은 함수 · 팔 고르기 꼴이
    틀리면 Stop NOT_REGISTERED (그 이름)."""
    name = f'{prefix}{n:02d}_{role}'
    al = None if isinstance(arms, int) else sorted(int(i) for i in arms)
    n_arms = int(arms) if al is None else len(al)
    if al is not None and (not al or len(set(al)) != len(al) or al[0] < 0 or al[-1] > 7 or al == list(range(n_arms))):
        raise Stop('NOT_REGISTERED', f'팔 고르기 {al} — 0–7 · 중복 없음 · 0..N−1 접두 아님 (그건 ARMS=N)', name)
    req = {'name': name, 'role': role, 'kit': kit, 'law': law, 'c': c, 'rj': rj, 'arms': n_arms, 'arm_list': al,
           'variant': variant, 'sv_cf': bool(sv_cf)}
    key = (kit, variant_raster(kit, variant), variant, law, c, rj_float(rj), tuple(arm_indices(req)))
    return name, req, key


class Runner:
    def __init__(self, runner, root, out, plan, variant, deadline, contract, dry=False, parent_env=None, prefix='R', machine=None):
        self.runner, self.root, self.out = Path(runner), Path(root), Path(out)
        self.plan, self.variant, self.deadline, self.contract, self.dry, self.prefix = plan, variant, deadline, contract, dry, prefix
        self.machine = machine               # ★ 10-27 묶음 C1a (C6 #15 · Q11) — 런 기록마다 기계 이름표 (단계 `--machine` · 판정이 대조)
        parent = dict(os.environ if parent_env is None else parent_env)
        self.scrubbed = sorted(k for k in parent if ENV_SCRUB_RE.match(k) or k in ENV_SCRUB_NAMES)
        self.env_base = {k: v for k, v in parent.items() if k not in self.scrubbed}
        self.records, self.keys, self.sid_reg, self.n = [], set(), {}, 0
        self.dry_lines = []
        self.s0_grid = None                  # ★ 10-25 묶음 B (RCA2-03) — S0 off 격자 지문 (`s0_grid_seed` · 단계가 정한다)
        self.s0_census = None                # ★ 10-25 묶음 B (X6) — S0 단계 2 봉인 SV census (`s0_census_seed`)
        self.graph_src = None                # ★ 10-26 B″ (Q1 (가)) — SV 끝 그래프 봉인 원천 (`RunnerGraphSource` · 단계가 정한다 · 없음 = 미확인)

    def env_delta(self, req, outdir):
        return runner_env_delta(self.plan, self.variant, req, outdir)

    def run(self, kit, role, law, c, rj, arms, sv_cf=False):
        """런 하나 → 팔 기록 목록.  `arms` = 팔 수 (ARMS · 0..N−1) 또는 팔 번호 튜플 (ARM_LIST · 예 ORIGIN_ARMS) · sv_cf = SV 반사실 켬.
        같은 킷 · 같은 계획 두 번 · 출력 폴더 있음 · 시간 · rc · 팔 계약 = Stop.  ★ 10-27 묶음 C1b-2 — 요청 (`_prepare`) · 실행 (`_execute`) 을 나눴다
        (재실행 `ResumeRunner` 가 같은 요청 · 이름 · 폴더로 복사하거나 새로 돈다 · 동작 그대로)."""
        name, req, outdir, delta = self._prepare(kit, role, law, c, rj, arms, sv_cf)
        if self.dry:
            self.dry_lines.append('  env ' + ' '.join(f'{k}={shlex.quote(delta[k])}' for k in sorted(delta)) + f' bash {self.runner}')
            print(self.dry_lines[-1])
            return None
        return self._execute(name, req, outdir, delta)

    def _prepare(self, kit, role, law, c, rj, arms, sv_cf):
        self.n += 1
        name, req, key = run_request(self.prefix, self.n, kit, role, law, c, rj, arms, sv_cf, self.variant)
        n_arms, al = req['arms'], req['arm_list']
        if key in self.keys:
            raise Stop('DUPLICATE_RUN', f'{kit} · {law} · c {c} · R_j {disp_rj(rj)} · 팔 {arm_indices(req)} 를 두 번 요청', name)
        self.keys.add(key)
        #  출력 폴더 = 러너가 강제하는 접미사 그대로 (`_arm<N>` · 팔 고르기면 `_arml<목록>`) — 다르면 러너가 다른 폴더에 쓴다
        sfx = '' if n_arms == 8 and al is None else f'_arm{n_arms}'
        if al is not None:
            sfx += '_arml' + '-'.join(str(i) for i in al)
        outdir = self.out / f'{name}{sfx}'
        return name, req, outdir, self.env_delta(req, outdir)

    def _execute(self, name, req, outdir, delta):
        role, rj, law, c, sv_cf = req['role'], req['rj'], req['law'], req['c'], req['sv_cf']
        if outdir.exists() and any(outdir.iterdir()):
            raise Stop('OUTDIR_NOT_EMPTY', f'{outdir} — 러너 SKIP 캐시가 옛 팔을 재사용한다', name)
        left = self.deadline - time.time()
        if left <= 0:
            raise Stop('TIME_LIMIT', '시간 상한 (--max-hours) 을 넘었다', name)
        (self.out / 'logs').mkdir(parents=True, exist_ok=True)
        rec = dict(req, outdir=outdir.name, rc=None, seconds=None, arms_read=[], machine=self.machine)
        self.records.append(rec)
        t0 = time.time()
        logp = self.out / 'logs' / f'{name}.log'
        #  ★ 10-27 묶음 C2b (R4-02 ⓑ · Codex ②) — 러너 = 새 프로세스 그룹 · 멈출 때 · 끝난 뒤 그룹 전체를 죽이고 종료를 확인한 뒤에만 팔을 읽는다
        with open(logp, 'w', encoding='utf-8') as lf:
            rc, cause, end = run_in_group(['bash', str(self.runner)], str(self.root), dict(self.env_base, **delta), lf, left,
                                          self.out / GROUPS_DIR, name)
        rec['rc'], rec['seconds'] = (rc if cause is None else None), round(time.time() - t0, 3)
        rec['group_cause'] = cause           # ★ 10-27 묶음 C1b — 그룹 원인 (None · timeout · signal · signal_after · 원장 결과 줄의 원인 · 재실행 자격)
        if not end['confirmed']:
            raise Stop('GROUP_UNCONFIRMED', f'{name}: 러너 그룹 종료 미확인 (남은 표지 프로세스 {end["left"]} · 원인 {cause}) — 그 런의 팔을 읽지 '
                                            f'않는다', name)
        if cause == 'timeout':
            raise Stop('TIME_LIMIT', f'{name}: 시간 상한 안에 끝나지 않았다 (러너 그룹을 죽이고 종료를 확인했다)', name)
        if cause == 'signal':
            raise Stop('RUNNER_RC', f'{name}: 사슬이 신호 {end.get("signal")} 를 받았다 — 러너 그룹을 죽이고 종료를 확인했다 (로그 {logp})', name)
        if cause == 'signal_after':
            raise Stop('RUNNER_RC', f'{name}: 사슬이 신호 {end.get("signal_after")} 를 받았다 (러너가 끝난 뒤 정리 중 · 그룹 종료는 확인했다) — 그 런의 팔을 '
                                    f'읽지 않는다 (로그 {logp})', name)
        if rc != 0:
            raise Stop('RUNNER_RC', f'rc {rc} (로그 {logp})', name)
        try:
            arms_ = read_run(outdir, req, self.plan, self.contract, self.sid_reg, s0_grid=self.s0_grid, s0_census=self.s0_census,
                             graph_src=self.graph_src)
        except Stop:
            #  읽기가 멈춰도 팔 파일 sha256 은 남긴다 — 등록 결과 (NOT_COMPUTED) 로 끝난 사다리를 판정이 원 팔에서 다시 계산할 수 있게.
            rec['arms_read'] = arm_file_shas(outdir)
            raise
        rec['arms_read'] = [{k: a[k] for k in ARM_PUBLIC} for a in arms_]
        a0 = arms_[0]
        ok = '✓' if all(x is True for x in a0['cert_pass']) else ('— (조기 반환 · 솔브 없음)' if a0['state'] != 'positive' else '✗')
        print(f'  {name}: {role} · R_j {disp_rj(rj)} · {law} · c {c or "-"} · 팔 {arm_indices(req)}{" · SV 반사실" if sv_cf else ""} → rc 0 · '
              f'{rec["seconds"]:.1f} s · 상태 {a0["state"]} · cg_info {a0["cg_info"]} · CG 반복 {a0["cg_iters"]} · 이어 풀기 '
              f'{a0["resolve_iters"]} · 잔차 {_e(a0["cg_resid"])} · 판 전류 불균형 {_e(a0["imbalance"])} · 증서 ⓐⓑⓒⓓ {ok} · '
              f'판독 보장 오차 e {_e(a0["err_rel"])}')
        return arms_


def resume_leftovers(run_dir):
    """원 시도의 멈춘 런 폴더에 남은 완성 payload (`p2_*.json` · 런 폴더 · 그 .unchecked/ · 표지 · 쓰는 중 파일 뺌) → [(이름, 바이트)] (재실행의 같은 이름
    payload 와 바이트 대조 · Q9 §3-5 R4-08 (a))."""
    out = []
    for d in (Path(run_dir), Path(run_dir) / UNCHECKED_DIR):
        if d.is_dir():
            for p in sorted(d.iterdir()):
                if p.is_file() and not p.is_symlink() and p.name.startswith('p2_') and p.name.endswith('.json') \
                        and not p.name.endswith(FIRST_RESULT_SUFFIX):
                    out.append((p.name, p.read_bytes()))
    return out


class ResumeRunner(Runner):
    """★ 10-27 묶음 C1b-2 (Q9 §3-5 개정 3 · 4 · R4-03 (c) · R4-08 · 개정 5 ① · Codex 회차 ① Q-J) 멈춘 런부터 재실행 — 같은 판정 함수가 같은 요청을 같은
    차례로 다시 낸다 (같은 이름 · 폴더).  원천 = 같은 바탕 폴더의 재실행 사슬 끝 시도 폴더 (`src`):
      · 원천에서 끝난 런 (끝 기록 확인 True · 원인 None · rc 0 · 런 폴더 있음) = 통째로 복사 (런 폴더 · 로그 · 그룹 기록 · 러너 0 회 · 팔 = read_run 이
        다시 대조)
      · 처음 끝나지 않은 런부터 새로 (그 뒤는 다 새로) · 그 런의 남은 payload ↔ 새 payload 바이트 대조 (다르면 RESUME_MISMATCH · 결정성 위반 = 멈춤) ·
        남은 payload 가 없으면 결정성 가정 (Q-J 한정 · `resume['determinism']` = assumed)
      · 새 프로세스 + 원 시도 환경 지문 모든 칸 = 풀기 전 대조 (개정 5 ① — "같은 프로세스" 가 아니다)."""

    def __init__(self, *a, src=None, src_n=None, **k):
        super().__init__(*a, **k)
        self.src, self.src_n, self.copying = Path(src), src_n, True
        self.resume = {'from': src_n, 'copied': [], 'rerun': None, 'compared': [], 'determinism': None}

    def _src_done(self, name, outdir_name):
        """원천의 그 런이 러너 쪽에서 끝났나 = 끝 기록 rc 0 · 런 폴더 있음.  (재실행 = 원천 결과 줄이 있어야 = 원천의 그룹 끝 기록이 다 확인됐다 · recover 가
        다시 쓴 끝 기록 = rc None · 시간 초과 · 신호 = rc ≠ 0 — 그래서 rc 0 하나로 가른다 · 복사한 팔은 read_run 이 다시 대조한다.)"""
        ep = self.src / GROUPS_DIR / f'{name}.end.json'
        try:
            er = json.loads(ep.read_text(encoding='utf-8')) if ep.is_file() else None
        except (OSError, UnicodeDecodeError, ValueError):
            er = None
        return isinstance(er, dict) and er.get('rc') == 0 and (self.src / outdir_name).is_dir()

    def run(self, kit, role, law, c, rj, arms, sv_cf=False):
        name, req, outdir, delta = self._prepare(kit, role, law, c, rj, arms, sv_cf)
        if self.copying and self._src_done(name, outdir.name):
            return self._copy(name, req, outdir)
        if not self.copying:
            return self._execute(name, req, outdir, delta)
        self.copying = False
        self.resume['rerun'] = name
        left = resume_leftovers(self.src / outdir.name)
        arms_ = self._execute(name, req, outdir, delta)
        self.resume['compared'] = [{'file': nm, 'same': (outdir / nm).is_file() and (outdir / nm).read_bytes() == raw} for nm, raw in left]
        self.resume['determinism'] = 'compared' if left else 'assumed'
        bad = [x['file'] for x in self.resume['compared'] if not x['same']]
        if bad:
            raise Stop('RESUME_MISMATCH', f'{name}: 재실행 payload ≠ 원 시도 attempt_{self.src_n} 에 남은 payload ({bad[:3]}) — 결정적 재실행이 아니다', name)
        return arms_

    def _copy(self, name, req, outdir):
        if outdir.exists():
            raise Stop('OUTDIR_NOT_EMPTY', f'{outdir} — 재실행 복사 자리가 이미 있다', name)
        try:
            shutil.copytree(self.src / outdir.name, outdir, symlinks=True)
            for sub, files in (('logs', (f'{name}.log',)), (GROUPS_DIR, (f'{name}.launch.json', f'{name}.end.json'))):
                (self.out / sub).mkdir(parents=True, exist_ok=True)
                for f in files:
                    if (self.src / sub / f).is_file():
                        shutil.copy2(self.src / sub / f, self.out / sub / f)
        except OSError as e:
            raise Stop('RESUME_NOT_ALLOWED', f'{name}: 원 시도 런 폴더를 복사하지 못했다 ({type(e).__name__}: {e})', name)
        rec = dict(req, outdir=outdir.name, rc=0, seconds=None, arms_read=[], machine=self.machine, group_cause=None, copied_from=self.src_n)
        self.records.append(rec)
        try:
            arms_ = read_run(outdir, req, self.plan, self.contract, self.sid_reg, s0_grid=self.s0_grid, s0_census=self.s0_census,
                             graph_src=self.graph_src)
        except Stop:
            rec['arms_read'] = arm_file_shas(outdir)
            raise
        rec['arms_read'] = [{k: a[k] for k in ARM_PUBLIC} for a in arms_]
        self.resume['copied'].append(name)
        print(f'  {name}: {req["role"]} · R_j {disp_rj(req["rj"])} · {req["law"]} · c {req["c"] or "-"} → 원 시도 attempt_{self.src_n} 에서 복사 '
              f'(러너 0 회 · 팔 {len(arms_)} 다시 대조)')
        return arms_


class GraphSourceError(Exception):
    """★ 10-26 B″ — 봉인 원천 런 실패 (사유 = 메시지) · `sv_graph_state` 가 잡아 미확인 (source_failed · 판정 `SV_UNCHECKED`) 으로 둔다 (멈춤 · clear 아님)."""


class RunnerGraphSource:
    """★ 10-26 B″ (1저자 10-26 Q1 (가) · 묶음 B 보고 §13 결정 1) SV 끝 그래프 **생산 봉인 원천** — 같은 러너 · 같은 킷 뿌리 · 같은 런 env
    (`runner_env_delta` · 사본 없음) + `CJUNC_GRAPH_ONLY=1` 로 payload 를 **조립만** 다시 돌려 (`--step3-cjunc-graph-only` →
    `step3_sigma.solve_sigma_z(cjunc_graph_only=True)` · CG 없음) 그 팔의 주 계 · SV 끝 가중 그래프 지문 (`carbon_junction.solved_graph_fp`) 을 돌려준다
    (`sv_graph_state` → `ca_ext_svcf.graph_problem` 이 증서 지문과 대조).
      · 원천 런 = 팔 하나 (팔 0 = ARMS 1 · 팔 i > 0 = ARM_LIST i) · 새 폴더 `<out>/G<n>_<런>_a<i>_arm1[_arml<i>]` (비지 않았으면 실패) · 로그 `<out>/logs`
      · 출력 = 그 폴더의 `cjgraph_p2_<킷>_…_a<i>.json` 정확히 하나 → `run_contract.cjunc_graph_only_problem` (꼴) → 환경 단위 = 이 사슬 프로세스
        (`env_record` 같음 단위 — 다르면 payload 가 다른 인터프리터 · 라이브러리로 돌았다 = 실패) → 결합 = ctx 'bind' (그 런 주 증서의 결합 —
        다르면 같은 입력에서 다시 조립하지 않았다 = 실패) → 지문 (None = 접합 조립 전 조기 반환 = 실패)
      · 실패 = `GraphSourceError` (사유 → 미확인) · 시간 상한 = 단계 deadline (None = 무제한 — 판정 · 다시 판정)
      · out None = 런마다 임시 폴더 (읽은 뒤 지운다 · 다시 판정 — 판정 폴더에 아무것도 쓰지 않는다)
      · `records` (`public`) = 원천 런마다 이름 · 런 · 팔 · rc · 초 · 상태 · 사유 · 출력 이름 · sha256 · 비용 (payload 가 잰 초 · 최대 RSS kB) · 환경 단위
        (σ · 비 없음 = 값 봉인) — 단계 요약 `sv_graph_source` · 판정 `verdict_graph_src.json` (판정 JSON 밖 · 다시 판정 바이트 대조 무관)
    ⚠ 한정: 원천은 그 런과 같은 코드 · 킷이다 (그 코드 · 킷 자체의 결함은 원천도 같이 갖는다 — 코드 · 침대 대조 = 단계 관문) · 증서 칸 지문까지 원천 값으로
    고친 편집은 이 대조로 못 가린다 (1저자 Q2 = 한정 · Codex 회차 ② 질문) · 비용 = 원천 런마다 러너 관문 + payload 의 CG 밖 부분 + 지문 (픽스처 실측 ·
    실침대 = 추정 · REPORT_B2)."""

    kind = 'runner_graph_only'

    def __init__(self, runner, root, out, deadline=None, parent_env=None):
        self.runner, self.root = Path(runner), Path(root)
        self.out = None if out is None else Path(out)
        self.deadline = deadline
        parent = dict(os.environ if parent_env is None else parent_env)
        self.env_base = {k: v for k, v in parent.items() if not (ENV_SCRUB_RE.match(k) or k in ENV_SCRUB_NAMES)}
        self.records, self.n = [], 0

    def env_delta(self, req, arm, outdir, plan):
        """원천 런 env = 그 런의 env (`runner_env_delta` — 같은 계획 · 변이 · 킷 · R_j · 법칙 · c · SV) + `GRAPH_ONLY_ENV` · 팔 하나 · 이 폴더."""
        arm = int(arm)
        greq = dict(req, arms=1, arm_list=(None if arm == 0 else [arm]))
        d = runner_env_delta(plan, req.get('variant'), greq, outdir)
        d.update(GRAPH_ONLY_ENV)
        return d

    def public(self):
        return {'kind': self.kind, 'runs': [dict(r) for r in self.records]}

    def __call__(self, ctx):
        req, arm = dict(ctx.get('req') or {}), int(ctx.get('arm'))
        self.n += 1
        name = f'G{self.n:02d}_{req.get("name")}_a{arm}'
        rec = {'name': name, 'run': req.get('name'), 'arm': arm, 'rc': None, 'seconds': None, 'status': 'failed', 'why': None,
               'graph_file': None, 'graph_sha256': None, 'cost': None, 'env_unit': None}
        self.records.append(rec)
        tmp = None
        try:
            base = self.out
            if base is None:
                tmp = Path(tempfile.mkdtemp(prefix='rint_graph_src_'))
                base = tmp
            g = self._run(ctx, req, arm, base, name, rec)
        except GraphSourceError as e:
            rec['why'] = str(e)[:300]
            print(f'  {name}: 봉인 원천 (조립만) → 실패 · {rec["why"]}')
            raise
        finally:
            if tmp is not None:
                shutil.rmtree(tmp, ignore_errors=True)
        rec['status'] = 'ok'
        print(f'  {name}: 봉인 원천 (조립만) · 런 {req.get("name")} 팔 {arm} → rc 0 · {rec["seconds"]:.1f} s · payload 최대 RSS '
              f'{(rec["cost"] or {}).get("peak_rss_kb")} kB (지문 대조는 다음)')
        return g

    def _run(self, ctx, req, arm, base, name, rec):
        plan = ctx.get('plan')
        if not isinstance(plan, dict):
            raise GraphSourceError('R 런 계획이 없다 (원천 env 를 만들 수 없다)')
        outdir = base / (f'{name}_arm1' + ('' if arm == 0 else f'_arml{arm}'))
        if outdir.exists() and any(outdir.iterdir()):
            raise GraphSourceError(f'원천 폴더가 비지 않았다 ({outdir.name})')
        delta = self.env_delta(req, arm, outdir, plan)
        timeout = None
        if self.deadline is not None:
            timeout = self.deadline - time.time()
            if timeout <= 0:
                raise GraphSourceError('시간 상한 (--max-hours) 을 넘었다')
        (base / 'logs').mkdir(parents=True, exist_ok=True)
        logp = base / 'logs' / f'{name}.log'
        t0 = time.time()
        #  ★ 10-27 묶음 C2b — 원천 런도 새 프로세스 그룹 · 종료 확인 뒤에만 출력을 읽는다 (사슬이 받은 신호 = 단계 멈춤 · 미확인 = 원천 실패)
        with open(logp, 'w', encoding='utf-8') as lf:
            rc, cause, end = run_in_group(['bash', str(self.runner)], str(self.root), dict(self.env_base, **delta), lf, timeout,
                                          base / GROUPS_DIR, name)
        rec['rc'], rec['seconds'] = (rc if cause is None else None), round(time.time() - t0, 3)
        if cause in ('signal', 'signal_after'):
            raise Stop('RUNNER_RC', f'{name}: 사슬이 신호 {end.get("signal") or end.get("signal_after")} 를 받았다 — 원천 러너 그룹 '
                                    f'{"을 죽였다" if cause == "signal" else "은 끝난 뒤 (정리 중)"} (종료 확인 {end["confirmed"]})', name)
        if not end['confirmed']:
            raise GraphSourceError(f'러너 그룹 종료 미확인 (남은 표지 프로세스 {end["left"]})')
        if cause == 'timeout':
            raise GraphSourceError('시간 상한 안에 끝나지 않았다')
        if rc != 0:
            raise GraphSourceError(f'러너 rc {rc} (로그 {logp.name})')
        files = sorted(glob.glob(str(outdir / f'{GRAPH_ONLY_PREFIX}*.json')))
        names = [os.path.basename(f) for f in files]
        pref = f'{GRAPH_ONLY_PREFIX}p2_{str(req.get("kit"))[len("kit_"):]}_'
        if len(files) != 1 or not names[0].startswith(pref) or not names[0].endswith(f'_a{arm}.json'):
            raise GraphSourceError(f'원천 출력 {len(files)} 개 {names[:3]} (= {pref}…_a{arm}.json 하나)')
        raw = Path(files[0]).read_bytes()
        rec['graph_file'], rec['graph_sha256'] = names[0], hashlib.sha256(raw).hexdigest()
        try:
            grec = json.loads(raw.decode('utf-8'))
        except (UnicodeDecodeError, ValueError) as e:
            raise GraphSourceError(f'원천 출력 JSON 을 못 읽는다 ({type(e).__name__})')
        why = RC.cjunc_graph_only_problem(grec)
        if why:
            raise GraphSourceError(why)
        rec['cost'], rec['env_unit'] = dict(grec['cost']), dict(grec['env_unit'])
        want_u = env_unit(env_record())
        if want_u is None or grec['env_unit'] != want_u:
            raise GraphSourceError(f'원천 런 환경 단위 {grec["env_unit"]} ≠ 사슬 {want_u} — payload 가 사슬과 다른 인터프리터 · 라이브러리로 돌았다 '
                                   f'(러너 env MPM_NO_VENV · PATH 의 python3)')
        want_b = ctx.get('bind')
        if not isinstance(want_b, dict) or grec['bind'] != want_b:
            diff = sorted(k for k in SVCF.BIND_FIELDS if not isinstance(want_b, dict) or grec['bind'].get(k) != want_b.get(k))
            raise GraphSourceError(f'원천 조립 결합 ≠ 그 런 주 증서 결합 (칸 {diff}) — 같은 입력에서 다시 조립하지 않았다')
        if grec['cjunc_graphs'] is None:
            raise GraphSourceError(f'원천 조립이 접합 조립 전에 조기 반환했다 — 지문 없음 (사유 {grec["reason"]})')
        return dict(grec['cjunc_graphs'])


class Replay:
    """판정 단계의 fetch — 기록된 런을 순서대로 대조해 원 팔 JSON 을 다시 읽는다 (sha256 대조 · 같은 계약).  ★ 10-26 B″ — graph_src = 판정의 봉인 원천
    (`RunnerGraphSource` · 원천을 다시 부른다 · 단계 요약의 대조를 믿지 않는다)."""

    def __init__(self, stage_dir, summary, plan, contract, sid_reg, cert_reg=None, graph_src=None):
        self.dir, self.plan, self.contract, self.sid_reg = Path(stage_dir), plan, contract, sid_reg
        self.graph_src = graph_src
        self.recs = list(summary.get('runs') or [])
        self.variant = summary.get('variant')
        self.i = 0
        self.cert_reg = {} if cert_reg is None else cert_reg
        self.s0_grid = s0_grid_seed(summary.get('s0_reports'))   # ★ 10-25 묶음 B (RCA2-03) — 원 단계와 같은 파생 격자 지문 대조
        self.s0_census = s0_census_seed(summary.get('s0_reports'))   # ★ 10-25 묶음 B (X6) — 원 단계와 같은 봉인 SV census 대조

    def run(self, kit, role, law, c, rj, arms, sv_cf=False):
        if self.i >= len(self.recs):
            raise Stop('REPLAY_MISMATCH', f'{self.dir.name}: 다시 계산이 {role} · R_j {disp_rj(rj)} 를 요구하는데 기록에 더 없다')
        r = self.recs[self.i]
        al = None if isinstance(arms, int) else sorted(int(i) for i in arms)
        want = (kit, role, law, c, rj, int(arms) if al is None else len(al), al, bool(sv_cf))
        got = (r.get('kit'), r.get('role'), r.get('law'), r.get('c'), r.get('rj'), r.get('arms'), r.get('arm_list'), r.get('sv_cf'))
        if want != got or r.get('rc') != 0 or r.get('variant') != self.variant:
            raise Stop('REPLAY_MISMATCH', f'{self.dir.name}: 다시 계산 {want} ≠ 기록 {got} (rc {r.get("rc")!r})', r.get('name'))
        self.i += 1
        req = {k: r.get(k) for k in REQ_KEYS}
        arms_ = read_run(self.dir / r['outdir'], req, self.plan, self.contract, self.sid_reg,
                         want_sha=[a.get('sha256') for a in r.get('arms_read') or []], s0_grid=self.s0_grid, s0_census=self.s0_census,
                         graph_src=self.graph_src)
        self.cert_reg[f'{self.dir.name}/{r["name"]}'] = [a['dsigma_rel'] for a in arms_]   # §8 수렴 증서 ⓒ 값 (판정 결과로만)
        return arms_

    def done(self):
        if self.i != len(self.recs):
            raise Stop('REPLAY_MISMATCH', f'{self.dir.name}: 기록에 다시 계산이 쓰지 않은 런 {len(self.recs) - self.i} 개')


# ═════════════════════════ 보정 사다리 (§3-1 – §3-3) ═════════════════════════
def end_pick(lad, side, X):
    """§3-2b ①–③ — 끝 하나 (arm 0): 끝 표적 X 를 사다리 규칙 그대로 끼운다 → 끼는 이웃 안 ln–ln 보간 = 후보 → 끝 확인 런 (후보 R 에서
    SBE arm 0) → 후보가 바깥 (lo: σ ≥ T⁺ · hi: σ ≤ T⁻) 이면 그 후보 · 아니면 그 점을 사다리에 넣고 **바깥 실측 이웃** (σ ≥ T⁺ 인 가장 큰 R ·
    σ ≤ T⁻ 인 가장 작은 R) → (끝 키, 기록).  반올림 없음 (끝 = 확인된 후보 또는 실측 점 · §10-2 ⑫ 3판).
    ★ 4판 (Q2-2 · ③″) — 확인 · 바깥 이웃 판정 = 판독 보호 띠 (`outside_band` · e = 그 점 런의 증서 보장 오차) · 끼우기 (후보 제안) 는 판독 그대로."""
    lo = side == 'lo'
    (Ra, ka, sa), (Rb, kb, sb) = lad._bracket_to(X, 'end_point')
    cand = rj_key(interp_lnln(Ra, sa, Rb, sb, X))
    reused = cand in lad.pts
    sc = lad.pts[cand][1] if reused else lad._get('end_confirm', cand)
    ok = outside_band(sc, X, lo, lad.err[cand])
    end = cand if ok else lad._outer_neighbor(X, lo)
    return end, {'bracket': [ka, kb], 'candidate': cand, 'confirm_reused': reused, 'confirm_ok': ok,
                 'source': 'candidate' if ok else 'outer_neighbor'}


def end_origin_push(lad, side, X, end):
    """★ Q-E (사전 리뷰 PRE-design-01 · 1저자 10-21 권고대로) — 끝에서 arm 1 · 2 도 돌려 세 origin 의 SBE 가 모두 띠 밖이어야 끝이다 ·
    하나라도 띠 안 (lo: σ < T⁺ · hi: σ > T⁻) 이면 끝을 다음 **바깥 실측 이웃** 으로 (없으면 같은 쪽 ×100 새 점 · 사다리 셈) → 세 origin
    허용집합의 합집합을 바깥에서 감싼다 (W = 그 끝들로).  → (끝 키, 민 횟수, 본 끝 목록).  origin 팔 런은 점 수에 안 센다 (§10-2 ③ 셈 그대로).
    ★ 4판 (Q2-2 · ③″) — 띠 밖 판정 = 판독 보호 띠 (팔마다 그 런 증서의 보장 오차).
    ★ 10-27 묶음 C (RCA2-07 · Q7 (가)) — 각 연장 단계 비 ≤ 100 · 총 팽창 상계 없음 (밀 때마다 다음 실측 점 또는 같은 쪽 ×100 한 칸 · 끝내는 것은 점 수
    상한 · 판정문 반례 = 보수 끝 / 참 위끝 비 443,434,903.8)."""
    lo = side == 'lo'
    pushes, seen = 0, []
    while True:
        if outside_band(lad.pts[end][1], X, lo, lad.err[end]):
            s12 = lad._org('end_origin', end)
            seen.append(end)
            if all(outside_band(s, X, lo, e) for s, e in zip(s12, lad.org_err[end])):
                return end, pushes, seen
        pushes += 1
        end = lad._next_out(end, lo)


class Ladder:
    """fetch(role, rj, arms) → 팔 기록 목록 · arm 0 σ 로 점을 고른다.  공개 상태 (st) 에는 σ 가 없다 · 봉인 칸 (sealed) 은 판정만 연다.
    max_points = 계획 점 수 상한 (⬜ 등록) · ratio_max = 계획 역상 R 비 상한 (float · 'none')."""

    def __init__(self, fetch, target_ms=None, max_points=None, ratio_max=PLAN_NO_CAP):
        if not (type(max_points) is int and max_points >= 1):    # noqa: E721
            raise Stop('PLAN_NUMBER_UNREGISTERED', f'점 수 상한 {max_points!r} (계획 칸 · ⬜ 결과 전 등록)')
        self.fetch = fetch
        self.T = (TARGET_SBE_MS if target_ms is None else target_ms) * 1e-3
        self.max_points, self.ratio_max = max_points, ratio_max
        self.st = {'order': [], 'n_runs': 0, 'n_ext': 0, 'n_bisect': 0, 'bracket': None, 'local_e_ge_emin': None, 'confirms': [],
                   'flat_pairs': [], 'states': {}, 'err_rel': {}, 'R_j0': None, 'R_j_lo': None, 'R_j_hi': None, 'ends': {}, 'R_ratio': None,
                   'ratio_cap': ratio_max, 'width_ok': None, 'origin': None, 'origin_runs': []}
        self.sealed = {'points': {}, 'e': None, 'delta': None, 'origin': None, 'ends_sigma': {}, 'origin_points': {}}
        self.pts = {}            # 키 → (R, σ arm 0) — 사다리 점 (센다)
        self.org = {}            # 키 → [σ arm 1, σ arm 2] — origin 팔 (끝 · R_j,0 공용 · 같은 R 두 번 안 돈다 · 안 센다)
        self.err = {}            # ★ 4판 (Q2-2 · ③″) 키 → 판독 보장 오차 e (arm 0 · 그 런 증서 ⓓ · σ 아님 → 공개 st['err_rel'])
        self.org_err = {}        # 키 → [e arm 1, e arm 2]
        self.flags = []

    def _get(self, role, key):
        if self.st['n_runs'] >= self.max_points:
            raise Stop('CALIB_LADDER_EXHAUSTED', f'점 수 상한 {self.max_points} (계획) — 다음 {role} R_j {disp_rj(key)} 를 돌리지 않는다')
        recs = self.fetch(role, key, 1)
        s = recs[0]['sigma']
        e = arm_err(recs[0])
        self.st['n_runs'] += 1
        self.st['order'].append(key)
        self.st['states'][key] = recs[0].get('state', 'positive')
        self.st['err_rel'][key] = e
        self.pts[key] = (rj_float(key), s)
        self.err[key] = e
        self.sealed['points'][key] = s
        self._monotone()
        return s

    def _org(self, role, key):
        if key not in self.org:
            r12 = self.fetch(role, key, ORIGIN_ARMS)
            self.org_err[key] = [arm_err(x) for x in r12]
            self.org[key] = [x['sigma'] for x in r12]
            self.st['origin_runs'].append({'role': role, 'rj': key})
            self.sealed['origin_points'][key] = list(self.org[key])
        return self.org[key]

    def _monotone(self):
        """§3-2 비단조 — R 이 커지는데 ln σ 가 τ_mono 넘게 오르면 멈춤 · 확장 실수 그대로 (바닥 0 은 끝 점이라 위반이 못 된다 ·
        유한 R 의 0 다음 양수 = +∞ 오름 = 위반 · ★ 4판 Q1: 천장 단락은 NOT_COMPUTED 라 점으로 오지 않는다)."""
        ps = sorted((R, k, s) for k, (R, s) in self.pts.items())
        for (_ra, ka, sa), (_rb, kb, sb) in zip(ps, ps[1:]):
            d = ln_diff(sa, sb)
            if d > TAU_MONO:
                raise Stop('CALIB_NONMONOTONE', f'R_j {disp_rj(ka)} → {disp_rj(kb)} 에서 ln σ 가 τ_mono {TAU_MONO:g} 넘게 오른다 '
                                                '(구현 결함 의심)')
            if 0.0 < d < math.inf and [ka, kb] not in self.st['flat_pairs']:
                self.st['flat_pairs'].append([ka, kb])           # τ 안 흔들림 = 평탄으로 기록 (멈추지 않는다)

    def _fin(self):
        """유한 R 점 (σ 는 0 일 수 있다) · 그중 양의 유한 σ (bracket · 보간 · §5-0 ②)."""
        finR = sorted((R, k, s) for k, (R, s) in self.pts.items() if 0.0 < R < math.inf)
        return finR, [x for x in finR if 0.0 < x[2] < math.inf]

    def _bracket_to(self, X, role):
        """§3-2 사다리 규칙 — X 를 끼는 양의 유한 이웃 둘 (같은 쪽 ×100 · 로그 중점 · 이웃 비 ≤ 10^0.5) → ((Ra, ka, sa), (Rb, kb, sb)).
        ★ 10-27 묶음 C (RCA2-07 · Q7 (가)) — 각 연장 단계 비 ≤ 100 · 총 팽창 상계 없음 (×100 연장을 되풀이할 수 있다 · 끝내는 것은 점 수 상한)."""
        while True:
            finR, fin = self._fin()
            br = None
            for a, b in zip(fin, fin[1:]):
                if min(a[2], b[2]) <= X <= max(a[2], b[2]):
                    br = (a, b)
                    break
            if br is None:
                if not fin or X > max(x[2] for x in fin):
                    e_new = math.log10(finR[0][0]) - LADDER_EXT_LOG10      # 더 큰 σ 가 필요 → 작은 R 쪽
                else:
                    e_new = math.log10(finR[-1][0]) + LADDER_EXT_LOG10
                self.st['n_ext'] += 1
                self._get(role, rj_key(10.0 ** e_new))
                continue
            (Ra, ka, sa), (Rb, kb, sb) = br
            if math.log10(Rb / Ra) > NEIGHBOR_LOG10_MAX + 1e-9:
                self.st['n_bisect'] += 1
                self._get(role, rj_key(10.0 ** ((math.log10(Ra) + math.log10(Rb)) / 2.0)))
                continue
            return br

    def _outer_neighbor(self, X, lo):
        """§3-2b ③ 바깥 실측 이웃 — lo: σ ≥ T⁺ 인 가장 큰 유한 R · hi: σ ≤ T⁻ 인 가장 작은 유한 R (3판 = 끼는 이웃이 늘 하나 있다).
        ★ 4판 (Q2-2 · ③″) — '바깥' = 판독 보호 띠 (`outside_band` · 그 점의 e) · 띠에 걸친 점만 남아 바깥 실측 점이 하나도 없으면 (모호 = 보수 쪽 ·
        끝을 바깥으로) 사다리 규칙 그대로 같은 쪽 ×100 새 점을 돈다 (③′ 의 '없으면 바깥 ×100 연장' 과 같은 꼴 · 점 수 상한이 끝낸다 =
        CALIB_LADDER_EXHAUSTED · ③″ 반례의 '사다리가 먼저 소진된다').
        ★ 10-27 묶음 C (RCA2-07 · Q7 (가)) — 각 연장 단계 비 ≤ 100 · 총 팽창 상계 없음 (×100 을 되풀이할 수 있다 · 끝내는 것은 점 수 상한)."""
        while True:
            finR, _fin = self._fin()
            pool = [(R, k) for R, k, s in finR if outside_band(s, X, lo, self.err[k])]
            if pool:
                return (max(pool) if lo else min(pool))[1]
            edge = finR[0][0] if lo else finR[-1][0]
            self.st['n_ext'] += 1
            self._get('end_point', rj_key(10.0 ** (math.log10(edge) + (-LADDER_EXT_LOG10 if lo else LADDER_EXT_LOG10))))

    def _next_out(self, end, lo):
        """끝을 한 칸 바깥으로 — 다음 실측 유한 점 (lo = 더 작은 R · hi = 더 큰 R) · 없으면 같은 쪽 ×100 새 점 (사다리 셈 · 상한이 끝낸다).
        ★ 10-27 묶음 C (RCA2-07 · Q7 (가)) — 각 연장 단계 비 ≤ 100 · 총 팽창 상계 없음 (한 번에 한 칸 · 여러 번 밀 수 있다)."""
        R = rj_float(end)
        finR, _fin = self._fin()
        cand = [(r, k) for r, k, _s in finR if (r < R if lo else r > R)]
        if cand:
            return (max(cand) if lo else min(cand))[1]
        key = rj_key(10.0 ** (math.log10(R) + (-LADDER_EXT_LOG10 if lo else LADDER_EXT_LOG10)))
        self.st['n_ext'] += 1
        self._get('end_point', key)
        return key

    def run(self):
        T = self.T
        sF = self._get('floor', LIMIT_RJ['floor'])
        sC = self._get('ceiling', LIMIT_RJ['ceiling'])
        if not (sF <= T <= sC):
            raise Stop('CALIB_IMPOSSIBLE', '1.63 mS/cm 이 [바닥, 천장] 밖 (값은 봉인)')
        #  §3-1 · §5-0 ② — 바닥 zero (σ 0) 는 정상 (|0/T − 1| = 1 → EDGE 아님) · ★ 4판 (Q1) 천장 단락 (ELECTRODE_SHORT) = 게시 안 됨 →
        #    천장 런에서 이미 NOT_COMPUTED (사유 ELECTRODE_SHORT · `read_run`) — 여기 오지 않는다 · ★ 4판 (Q2-2 · ③″) 판독 보호 띠 — 걸치면 EDGE
        if edge_hit(sF, self.err[LIMIT_RJ['floor']], T) or edge_hit(sC, self.err[LIMIT_RJ['ceiling']], T):
            raise Stop('CALIB_EDGE', f'1.63 이 바닥 또는 천장의 {CONFIRM_TOL:.0%} 안 (판독 보호 띠 포함 · §3-2b ③″) — R_j,0 가 하나로 안 정해진다')
        for e in LADDER_START_LOG10:
            self._get('point', rj_key(10.0 ** e))
        while True:
            (Ra, ka, sa), (Rb, kb, sb) = self._bracket_to(T, 'point')
            self.st['bracket'] = [ka, kb]
            e = elasticity(Ra, sa, Rb, sb)
            self.sealed['e'] = e
            self.st['local_e_ge_emin'] = bool(e >= E_MIN)         # ★ 3판 — 국소 진단 (보고 · 멈추지 않는다 · RCA-01)
            R0 = sig3(interp_lnln(Ra, sa, Rb, sb, T))
            k0 = rj_key(R0)
            reused = k0 in self.pts
            s0 = self.pts[k0][1] if reused else self._get('confirm', k0)
            ok = abs(s0 / T - 1.0) <= CONFIRM_TOL
            self.st['confirms'].append({'rj': k0, 'ok': ok, 'reused': reused})
            if ok:
                self.st['R_j0'] = k0
                self.sealed['delta'] = math.log(s0 / T)
                break
            if len(self.st['confirms']) >= MAX_CONFIRM:
                raise Stop('CALIB_UNCONFIRMED', f'확인 {MAX_CONFIRM} 번 다 ±{CONFIRM_TOL:.0%} 밖 (값은 봉인)')
        self._ends()

    def _ends(self):
        """§3-2b — 실제 SBE 역상 양끝 (+ ★ Q-E 세 origin 합집합) · 폭 R_j,hi/R_j,lo · 상한 (계획 · 'none' = 상한 없음)."""
        T = self.T
        ends = {}
        for side, X, tag in (('lo', T * (1.0 + CONFIRM_TOL), 'T+ = 1.63 × 1.02'), ('hi', T * (1.0 - CONFIRM_TOL), 'T- = 1.63 × 0.98')):
            end, ent = end_pick(self, side, X)
            end2, pushes, seen = end_origin_push(self, side, X, end)
            ent.update(target=tag, arm0_end=end, end=end2, origin_pushes=pushes, origin_checked=seen,
                       source=(ent['source'] if pushes == 0 else 'outer_neighbor_origin'))
            ends[side] = ent
            self.sealed['ends_sigma'][side] = self.pts[end2][1]
        self.st['ends'] = ends
        self.st['R_j_lo'], self.st['R_j_hi'] = ends['lo']['end'], ends['hi']['end']
        ratio = rj_float(self.st['R_j_hi']) / rj_float(self.st['R_j_lo'])
        self.st['R_ratio'] = ratio
        if self.ratio_max == PLAN_NO_CAP:
            self.st['width_ok'] = None
        else:
            self.st['width_ok'] = bool(ratio <= float(self.ratio_max))
            if not self.st['width_ok']:
                raise Stop('CALIB_UNIDENTIFIED', f'실제 역상 R 비 R_j,hi/R_j,lo 가 계획 상한 {self.ratio_max} 를 넘는다 (§3-2b ④ · 보정 폭이 넓다)')

    def origin(self):
        """§3-3 — R_j,0 에서 arm 1 · 2 (★ Z3 — `ARM_LIST=1,2` 한 런 · a0 = 확인 팔 값 그대로 · 다시 돌지 않는다 · 끝 origin 과 같은 R 이면
        그 런 그대로) → ln(max/min) ≤ 0.02 · 넘으면 8 팔 평균 (`ARMS=8` 한 런) · 표지 (R_j,0 그대로)."""
        k0 = self.st['R_j0']
        s0 = self.pts[k0][1]
        vals = [s0] + list(self._org('origin', k0))
        ok, sp = sbe_origin_ok(vals)
        o = {'status': 'pass' if ok else 'sensitive', 'arm_list': list(ORIGIN_ARMS), 'mean8': False}
        self.sealed['origin'] = {'spread': sp, 'arms': vals, 'mean8': None}
        if not ok:
            r8 = self.fetch('origin8', k0, 8)
            o['mean8'] = True
            self.sealed['origin']['mean8'] = mean_ext([x['sigma'] for x in r8])
            self.flags.append('CALIB_ORIGIN_SENSITIVE')
        self.st['origin'] = o


NOOP_C = '1'                         # §4-1 SBE no-op = c 1 (사다리 = c 0 · SBE 에 SDCP 없음 → 비트 같아야)


def ladder_noop(fetch, lad, law):
    """★ 10-27 묶음 C2a (Q9 설계 §2-1 · 개정 3 질문 4 · 개정 4 R4-06 (d) · 개정 5 ① · author 10-27 approved bundle C) SBE c 1 no-op = 사다리 단계 끝 —
    보정이 끝난 사다리 (CALIBRATED) 의 R_j,0 에서 SBE c 1 arm 0 한 런 (`fetch('sbe_noop', R_j,0, 1)` · 같은 사슬 부모가 동결한 실행 환경 · 런마다 새 러너
    자식 — 같은 solver 프로세스라는 뜻이 아니다 · 개정 5 ①) → 사다리 R_j,0 확인 팔 (arm 0) 과 float 같음 · SDCP 근접 0 을 대조해 기록만 한다:
    {law · rj · status ('done' | 'NOT_COMPUTED') · ok (bool | None) · stop (NOT_COMPUTED 의 멈춤 기록 | None)} (σ 없음 = 값 봉인).
    등록 결과 NOT_COMPUTED (증서 실패 · 단락) = 기록 (사다리 상태는 보정 결과만 · CALIBRATED 그대로) · 그 밖 멈춤 (러너 · 계약 · 자원 · 시간) = 사다리 시도의
    멈춤 (위로 올린다).  판정 = 예측 첫머리가 이 기록을 읽어 옛 자리 · 옛 이름 (`SAME_P_CONSISTENCY` · `NOT_COMPUTED`) 으로 낸다 (`Predict.run`)."""
    k0 = lad.st['R_j0']
    rec = {'law': law, 'rj': k0, 'status': None, 'ok': None, 'stop': None}
    try:
        r = fetch('sbe_noop', k0, 1)[0]
    except Stop as e:
        if e.code != 'NOT_COMPUTED':
            raise
        rec.update(status='NOT_COMPUTED', stop=e.record())
        return rec
    rec.update(status='done', ok=bool(r['sigma'] == lad.pts[k0][1] and r['n_sdcp_near'] == 0))
    return rec


def noop_record_problem(rec, law, k0):
    """사다리 요약의 no-op 기록 꼴 → 문제 | None (예측 · 판정이 다시 읽기 전 · 칸 집합 · 법칙 · R_j,0 · 상태 ↔ ok · 멈춤 기록)."""
    if not isinstance(rec, dict) or set(rec) != {'law', 'rj', 'status', 'ok', 'stop'}:
        return f'no-op 기록 꼴 {sorted(rec) if isinstance(rec, dict) else type(rec).__name__}'
    if rec['law'] != law or rec['rj'] != k0:
        return f'no-op 기록 법칙 · R_j {rec["law"]!r} · {rec["rj"]!r} ≠ 사다리 {law!r} · R_j,0 {k0!r}'
    if rec['status'] == 'done' and isinstance(rec['ok'], bool) and rec['stop'] is None:
        return None
    if rec['status'] == 'NOT_COMPUTED' and rec['ok'] is None and isinstance(rec['stop'], dict) and rec['stop'].get('code') == 'NOT_COMPUTED':
        return None
    return f'no-op 기록 상태 {rec["status"]!r} · ok {rec["ok"]!r} · 멈춤 {rec["stop"]!r} (done + bool · NOT_COMPUTED + 멈춤 기록)'


def noop_check(rd, s, law, k0, r0_arm, plan, contract, sid_reg):
    """★ 10-27 묶음 C2a — 예측 단계가 사다리 끝 no-op 을 다시 대조: 요약 기록 꼴 (`noop_record_problem`) · no-op 런 기록 하나 (SBE · c 1 · R_j,0 · arm 0 ·
    rc 0) · 그 팔을 원 팔에서 다시 읽어 (`read_run` · 기록 sha256) 같은 대조 (R_j,0 확인 팔 σ 와 float 같음 · SDCP 근접 0) → 기록과 다르면
    REPLAY_MISMATCH · 꼴 · 런 기록 문제 = LADDER_SET → 기록 (Predict 가 읽는다)."""
    nr = s.get('noop')
    why = noop_record_problem(nr, law, k0)
    if why:
        raise Stop('LADDER_SET', f'{Path(rd).name}: {why} (★ 10-27 묶음 C2a — 사다리 끝 no-op 기록)')
    runs = [x for x in s.get('runs') or [] if x.get('role') == 'sbe_noop']
    x = runs[0] if len(runs) == 1 else {}
    if not (x.get('kit') == SBE_KIT and x.get('law') == law and x.get('c') == NOOP_C and x.get('rj') == k0 and x.get('arms') == 1
            and x.get('arm_list') is None and x.get('rc') == 0 and runs[-1] is (s.get('runs') or [None])[-1]):
        raise Stop('LADDER_SET', f'{Path(rd).name}: 사다리 끝 no-op 런 기록 {len(runs)} 개 · 꼴 (SBE · c {NOOP_C} · R_j,0 · arm 0 · rc 0 · 마지막 런 하나여야)')
    req = {k: x.get(k) for k in REQ_KEYS}
    try:
        na = read_run(Path(rd) / x['outdir'], req, plan, contract, sid_reg, want_sha=[a['sha256'] for a in x.get('arms_read') or []])[0]
        again = {'status': 'done', 'ok': bool(na['sigma'] == r0_arm['sigma'] and na['n_sdcp_near'] == 0), 'stop': None}
    except Stop as e:
        if e.code != 'NOT_COMPUTED':
            raise
        again = {'status': 'NOT_COMPUTED', 'ok': None, 'stop': e.record()}
    if noop_key(again) != noop_key(nr):
        raise Stop('REPLAY_MISMATCH', f'{Path(rd).name}: 사다리 끝 no-op 을 원 팔에서 다시 읽은 대조 (상태 {again["status"]} · ok {again["ok"]}) ≠ 요약 '
                                      f'기록 (상태 {nr["status"]} · ok {nr["ok"]})')
    return dict(nr)


def noop_key(rec):
    """no-op 기록의 대조 칸 — 상태 · ok · 멈춤 이름 · 구조화 사유 (멈춤 원인 글 · 런 이름 = 경로 · 폴더가 들 수 있어 대조 밖 · 기록은 그대로 남는다)."""
    st = rec.get('stop') or {}
    return (rec.get('status'), rec.get('ok'), st.get('code'), st.get('reason'))


# ═════════════════════════ 예측 (§4-1 · §4-2) ═════════════════════════
RJ_ROLES = ('R_j_lo', 'R_j0', 'R_j_hi')
#: §4-2 3판 (RCA-02) — DBE origin 을 점검하는 R (세 R 모두 · 2판 = R_j,0 만) · 넘으면 그 모서리 세 R 전부 8 팔 평균 (RJ_ROLES)
ORIGIN_CHECK_ROLES = RJ_ROLES


class Predict:
    """fetch(kit, role, law, c, rj, arms, sv_cf).  ladders = {법칙: {'R_j0', 'R_j_lo', 'R_j_hi', 'r0_sigma'}} (사다리에서 읽은 값 그대로).
    ★ 3판 — 주 판정 · 감도 변이가 같은 판정 함수 (네 모서리 × 세 R · DBE origin 세 R · §5-6 · RCA-09) · sv_scope (주 판정만) = SV 반사실을
    켤 모서리 런 ('R_j0' · 'all3')."""

    def __init__(self, fetch, ladders, variant, sv_scope=None, expand_hook=None):
        self.fetch, self.ladders, self.variant, self.sv_scope = fetch, ladders, variant, sv_scope
        self.expand_hook = expand_hook       # ★ 10-27 묶음 C2 — 넘침 목록 [(c, 법칙, 역할)] 을 받는 자리 (단위 첫 합치기 · 한 기계 사슬 = None)
        self.main = variant is None
        self.checks = {'sbe_noop': [], 'same_p': [], 'r_monotone': []}     # ★ 10-23 r_monotone = RCA2-09 (모서리마다 ok · 최종 추정량 이름 ·
        #                                                                     ★ 10-23 C3 origins = 이미 구한 origin 마다 ok)
        self.origin = []
        self.vals = {}                       # (c, 법칙, 역할) → arm 0 팔 기록
        self.adj = {}                        # (c, 법칙, 역할) → 8 팔 평균 (origin 규칙이 바꾼 모서리 · 세 R 전부)
        self.adj_band = {}                   # ★ 10-23 (RCA2-09) (c, 법칙, 역할) → 그 8 팔 평균의 증서 구간 (`mean_band`)
        self.org = {}                        # ★ 10-23 (사전 공격 리뷰 C3) (c, 법칙, 역할) → {origin 이름 (`ORIGIN_NAMES`): 이미 구한 팔 기록}
        self.sealed = {'W0': None, 'origin': {}}

    def _sv_on(self, rr):
        return self.main and (self.sv_scope == 'all3' or (self.sv_scope == 'R_j0' and rr == 'R_j0'))

    def run(self):
        """★ 10-27 묶음 C2a (Q9 설계 §2 · 개정 2 Q24 (나) · 개정 3 · 개정 4 R4-06 · author 10-27 approved bundle C) 순서 = no-op 기록 (사다리 끝 런 ·
        첫머리 · 옛 자리 · 옛 이름) → 모서리 (법칙 → R → c) + same_p → W0 → ① origin 표본 전부 (법칙 → c → R) → ② 넘침이 있으면 이른 단조 검사 (이미
        있는 점 · `checks['r_monotone_early']` · 넘침 없으면 끝 검사와 같은 점이라 건너뜀) → ③ 넘침 origin8 (법칙 → c → R) → ④ 끝 단조 (그대로).
        이 순서가 바꾸는 멈춤 우선순위 둘 (ⓐ 이른 단조 > 넘침 런의 멈춤 · ⓑ origin 표본 멈춤 > 앞 모서리 origin8 멈춤 · NOT_COMPUTED ↔ STOPPED 양쪽) =
        등록 개정 몫 (결과 0 건 · Q9 §7) · 이전 사슬과 모든 멈춤 우선순위가 같다고 쓰지 않는다 (Codex Q-I)."""
        self.noop_first()
        self._run_after_noop()

    def noop_first(self):
        """SBE c 1 no-op 기록 (사다리 끝 런 · 첫머리 · 옛 자리 · 옛 이름) — 예측 다시 계산 · ★ 10-27 묶음 C2d 단위 · 넘침 점 시도 입구가 같은 함수 (단위가
        no-op 결과보다 먼저 DBE 를 풀지 않게 · 한 기계 사슬과 같은 첫 멈춤)."""
        if self.variant != 'SVORDER':        # SBE c 1 no-op — 주 · FIBRE · UNREG · GRID (SVORDER = 주 사다리 · SDCP 0 침대 양보 = no-op)
            for law in LAWS:
                nr = self.ladders[law].get('noop') or {}
                if nr.get('status') == 'NOT_COMPUTED':     # ★ 10-27 묶음 C2a — 사다리 끝 no-op 런의 등록 결과 (옛 = 예측 첫 런의 NOT_COMPUTED)
                    st = nr.get('stop') or {}
                    raise Stop('NOT_COMPUTED', f'SBE c 1 no-op (사다리 {law} 끝 런) = NOT_COMPUTED — {st.get("cause")}', st.get('run'),
                               st.get('reason'))
                ok = nr.get('status') == 'done' and nr.get('ok') is True
                self.checks['sbe_noop'].append({'law': law, 'ok': ok})
                if not ok:
                    raise Stop('SAME_P_CONSISTENCY', f'SBE c 1 ↔ c 0 (사다리 R_j,0 확인 팔) 비트 다름 또는 SDCP 근접 ≠ 0 ({law} · 사다리 끝 no-op 런 '
                                                     f'기록) — S3 이 SBE 에서 no-op 이 아니다')

    def _run_after_noop(self):
        for law in LAWS:
            for rr in RJ_ROLES:
                for c in CS:
                    self.vals[(c, law, rr)] = self.fetch(DBE_KIT, 'corner', law, c, self.ladders[law][rr], 1, self._sv_on(rr))[0]
                d = ln_diff(self.vals[('0', law, rr)]['sigma'], self.vals[('1', law, rr)]['sigma'])
                ok = d >= -TAU_MONO
                self.checks['same_p'].append({'law': law, 'rj_role': rr, 'ok': ok})
                if not ok:
                    raise Stop('SAME_P_CONSISTENCY', f'σ_DBE(c1, {law}) < σ_DBE(c0, {law}) − τ_mono at {rr} — 같은 그래프 · 같은 R_j 에서 '
                                                     f'Rayleigh 순서 위반 (구현 결함)')
        W0 = ln_spread([v['sigma'] for v in self.vals.values()])
        W_pos = w_pos_of([v['sigma'] for v in self.vals.values()])     # ★ 4판 (Q2-3 · §4-2 ②) — W ∈ {+∞, 0} 일 때 문턱의 W
        self.sealed['W0'] = W0
        self.sealed['W_pos'] = W_pos
        over_corners, sos = [], {}
        for law in LAWS:                             # ★ 10-27 묶음 C2a ① — origin 표본 전부 먼저 (옛 = 모서리마다 표본 → 넘치면 바로 origin8)
            for c in CS:
                ent = {'c': c, 'law': law, 'status': 'pass', 'arm_list': list(ORIGIN_ARMS), 'per_R': {}, 'states_differ': []}
                so = {}
                over = False
                for rr in ORIGIN_CHECK_ROLES:        # §4-2 3판 — 세 R 모두 (RCA-02)
                    a0r = self.vals[(c, law, rr)]
                    r12 = self.fetch(DBE_KIT, 'origin', law, c, self.ladders[law][rr], ORIGIN_ARMS)
                    self.org[(c, law, rr)] = dict([('corner_a0', a0r)] + [(f'origin_a{i}', x) for i, x in zip(ORIGIN_ARMS, r12)])
                    vv = [a0r['sigma']] + [x['sigma'] for x in r12]
                    sts = [a0r.get('state', 'positive')] + [x.get('state', 'positive') for x in r12]
                    ok, sp = dbe_origin_ok(vv, W0, states=sts, w_pos=W_pos)   # ★ 4판 (Q2-3 · §4-2 ①) 상태 다름 = 넘음
                    ent['per_R'][rr] = 'pass' if ok else 'over'
                    if len(set(sts)) > 1:
                        ent['states_differ'].append(rr)
                    so[rr] = {'spread': sp, 'arms': vv, 'states': sts}
                    over = over or not ok
                if over:                             # 한 R 이라도 넘으면 그 모서리 세 R 전부 같은 8 origin 집합의 평균 (③ 에서)
                    ent['status'] = 'adjusted'
                    over_corners.append((c, law))
                self.origin.append(ent)
                self.sealed['origin'][f'c{c}_{law}'] = so
                sos[(c, law)] = so
        if over_corners:                             # ★ 10-27 묶음 C2a ② — 이른 단조 (넘침 런 전 · 이미 있는 점만 · 넘침 없으면 ④ 와 같은 점)
            self._r_monotone_early(set(over_corners))
            if self.expand_hook is not None:         # ★ 10-27 묶음 C2 — 단위 합치기의 첫 합치기 = 여기서 넘침 목록을 내고 멈춘다 (한 기계 사슬 = None)
                self.expand_hook([(c, law, rr) for law in LAWS for c in CS if (c, law) in over_corners for rr in RJ_ROLES])
        for law in LAWS:                             # ③ 넘침 origin8 (법칙 → c → R)
            for c in CS:
                if (c, law) not in over_corners:
                    continue
                for rr in RJ_ROLES:
                    r8 = self.fetch(DBE_KIT, 'origin8', law, c, self.ladders[law][rr], 8)
                    m8 = mean_ext([x['sigma'] for x in r8])
                    self.adj[(c, law, rr)] = m8
                    self.adj_band[(c, law, rr)] = mean_band(r8)
                    self.org[(c, law, rr)].update((f'origin8_a{i}', x) for i, x in enumerate(r8))
                    sos[(c, law)][rr]['mean8'] = m8
        self._r_monotone()                           # ④ 끝 단조 (그대로)

    def _r_monotone_early(self, over):
        """★ 10-27 묶음 C2a (Q9 설계 §3-2 이른 단조 · 개정 2 Q24 (나) · 개정 3 P3) — 넘침 런을 요청하기 **전에** 이미 있는 점으로 같은 판정 함수
        (`r_monotone_problem`) 를 끝 검사와 같은 순서 (법칙 → c → 최종 추정량 → origin) 로: 넘침이 없는 모서리 = 최종 추정량 (arm 0) + origin 셋 ·
        넘친 모서리 = origin 셋 (corner_a0 · origin_a1 · origin_a2) 만 (8 팔 평균 · origin8 = 아직 없다 → 건너뜀 · 기록 ok · estimator = None).
        모순 = 멈춤 `R_MONOTONE_VIOLATION` (넘침 런 없이) · 기록 = `checks['r_monotone_early']` (넘침이 있을 때만 · 끝 검사 기록은 그대로)."""
        out = self.checks.setdefault('r_monotone_early', [])
        for law in LAWS:
            for c in CS:
                ent = {'law': law, 'c': c, 'ok': None, 'estimator': None, 'origins': None}
                out.append(ent)
                if (c, law) not in over:
                    pts, est = [], set()
                    for rr in RJ_ROLES:
                        b, e = final_band(self, (c, law, rr))
                        pts.append((rj_float(self.ladders[law][rr]), rr, b))
                        est.add(e)
                    bad = r_monotone_problem(pts)
                    ent.update(ok=bad is None, estimator='+'.join(sorted(est)))
                    if bad is not None:
                        raise Stop('R_MONOTONE_VIOLATION', f'σ_DBE({law}, c {c}) 의 증서 구간이 R_j 단조와 모순 — {bad[0]} (R 작음) 구간의 위끝 < '
                                                           f'{bad[1]} (R 큼) 구간의 아래끝 (이른 검사 · 넘침 런 전 · 같은 origin · 최종 추정량 '
                                                           f'{ent["estimator"]} · 추가 풀이 없음 · 구현 결함 의심 · 판정문 §8 RCA2-09)')
                org = [(n, r_monotone_problem(p)) for n, p in origin_points(self, law, c)]
                ent['origins'] = [{'origin': n, 'ok': b is None} for n, b in org]
                for n, b in org:
                    if b is not None:
                        raise Stop('R_MONOTONE_VIOLATION', f'σ_DBE({law}, c {c}) origin {n} 의 증서 구간이 R_j 단조와 모순 — {b[0]} (R 작음) 구간의 '
                                                           f'위끝 < {b[1]} (R 큼) 구간의 아래끝 (이른 검사 · 넘침 런 전 · 같은 origin 의 세 R · 이미 '
                                                           f'구한 값 · 추가 풀이 없음 · 구현 결함 의심 · 판정문 §8 RCA2-09)')

    def _r_monotone(self):
        """★ 10-23 (Codex 재검토 RCA2-09 · 판정문 §8 · 1저자 Q8 (가) · author 10-23 ratified Q1-Q8) DBE R 단조 방어 검사 — 이미 구한 값으로 (추가
        풀이 없음) 모서리마다 같은 origin · 같은 최종 추정량 (`final_band` — arm 0 · origin 규칙이 바꾼 모서리 = 8 팔 평균) 의 σ(R_j,lo) ≥ σ(R_j,0) ≥
        σ(R_j,hi) 를 증서 구간끼리 본다 (`r_monotone_problem` · 정확 분수 · 쌍 전부) — 구간이 단조와 모순일 때만 멈춤 `R_MONOTONE_VIOLATION` (새 숫자
        없음 · 값 봉인 = 문장에 σ 없음) · 검사 기록 `checks['r_monotone']` (판정의 다시 계산이 같은 검사를 다시 낸다).  표본 통과 ≠ 연속 곡선의 독립
        증명 (판정문 §8).
        ★ 10-23 (사전 공격 리뷰 C3 · 1저자 Q13 (가) · author 10-23 ratified Q12-Q16) — 최종 추정량 검사 (그대로 · 먼저) 를 지나면 같은 모서리의 이미
        구한 origin 마다 (`origin_points` — 모서리 런 arm 0 · origin 런 arm 1 · 2 · 넘친 모서리 = 8 팔 런 origin 0–7) 세 R 의 증서 구간도 같은
        판정 (`r_monotone_problem`) 으로 본다 — 모순 = 같은 멈춤 이름 · 사유에 origin 이름 (최종 추정량 아님) · 기록 칸 `origins` (origin 마다 ok ·
        최종 추정량 검사가 멈추면 None = 보지 않음) · 추가 풀이 · 새 숫자 없음."""
        for law in LAWS:
            for c in CS:
                pts, est = [], set()
                for rr in RJ_ROLES:
                    b, e = final_band(self, (c, law, rr))
                    pts.append((rj_float(self.ladders[law][rr]), rr, b))
                    est.add(e)
                bad = r_monotone_problem(pts)
                ent = {'law': law, 'c': c, 'ok': bad is None, 'estimator': '+'.join(sorted(est)), 'origins': None}
                self.checks['r_monotone'].append(ent)
                if bad is not None:
                    raise Stop('R_MONOTONE_VIOLATION', f'σ_DBE({law}, c {c}) 의 증서 구간이 R_j 단조와 모순 — {bad[0]} (R 작음) 구간의 위끝 < {bad[1]} '
                                                       f'(R 큼) 구간의 아래끝 (같은 origin · 같은 최종 추정량 {ent["estimator"]} · 추가 풀이 없음 · '
                                                       f'구현 결함 의심 · 판정문 §8 RCA2-09)')
                org = [(n, r_monotone_problem(p)) for n, p in origin_points(self, law, c)]
                ent['origins'] = [{'origin': n, 'ok': b is None} for n, b in org]
                for n, b in org:
                    if b is not None:
                        raise Stop('R_MONOTONE_VIOLATION', f'σ_DBE({law}, c {c}) origin {n} 의 증서 구간이 R_j 단조와 모순 — {b[0]} (R 작음) 구간의 '
                                                           f'위끝 < {b[1]} (R 큼) 구간의 아래끝 (같은 origin 의 세 R · 이미 구한 값 · 추가 풀이 '
                                                           f'없음 · 구현 결함 의심 · 판정문 §8 RCA2-09 · 10-23 사전 공격 리뷰 C3)')

    def values(self):
        """모서리 값 (S/cm · 확장 실수) — origin 규칙이 바꾼 모서리는 세 R 전부 8 팔 평균 (§4-2 3판)."""
        return {k: (self.adj[k] if k in self.adj else r['sigma']) for k, r in self.vals.items()}

    def states(self):
        return {k: r.get('state', 'positive') for k, r in self.vals.items()}


# ═════════════════════════ 단계 공통 ═════════════════════════
def summary_base(stage, a):
    #  ★ PF2 D (10-22 · PRE2-design-02) — code = git 신원 + 코드 파일 지문 (`code_record`) · machine = 기계 이름표 (등록 R §10-4 문장 3 · 기록만 ·
    #    판정에는 쓰지 않는다 · 없으면 null)
    return {'tool': TOOL, 'schema': SCHEMA, 'stage': stage, 'status': None, 'stop': None, 'flags': [], 'attempt': None, 'resume': None,
            'machine': getattr(a, 'machine', None), 'code': code_record(getattr(a, 'runner', None)),
            'constants': {'target_sbe_mScm': TARGET_SBE_MS, 'confirm_tol': CONFIRM_TOL, 'e_min': E_MIN, 'tau_mono': TAU_MONO,
                          'neighbor_log10_max': NEIGHBOR_LOG10_MAX, 'origin_sbe_max': ORIGIN_SBE_MAX,
                          'origin_dbe_frac_w': ORIGIN_DBE_FRAC_W}}


def outdir_empty_or_stop(out):
    out = Path(out)
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise Stop('OUTDIR_NOT_EMPTY', f'{out} — 새 --out 을 쓸 것 (그 폴더에는 아무것도 쓰지 않는다)')


def env_forbidden_or_stop(env=None):
    env = os.environ if env is None else env
    hit = [k for k in ENV_FORBIDDEN if k in env]
    if hit:
        raise Stop('ENV_SIGMA_VGCF_OVERRIDE', f'{hit} 가 env 에 있다 — unset 하고 다시 (SIGMA_FIBRE_BULK 와 함께면 러너 거부 · §10)')


def write_json(path, obj):
    Path(path).write_bytes(canon_bytes(_clean(obj)))


def print_stop(e):
    print(f'멈춤 [{e.code}] {STOPS.get(e.code, e.code)} — {e.cause}' + (f' (런 {e.run})' if e.run else ''))


def read_summary(d, name):
    p = Path(d) / name
    try:
        raw = p.read_bytes()
        return json.loads(raw.decode('utf-8')), hashlib.sha256(raw).hexdigest()
    except (OSError, UnicodeDecodeError, ValueError):
        return None, None


def same_code(a, b):
    """git 신원의 HEAD 대조 (옛 대조 · ★ PF2 D 뒤 단계 대조는 `code_key` (HEAD + 코드 파일 지문) · `code_dirty_problem` 이 한다 — 같은 HEAD 라도
    dirty · 파일이 다르면 멈춘다 · 이 함수는 남긴다 (탐침 C 가 부른다))."""
    return (a or {}).get('head') == (b or {}).get('head')


def _e(x):
    return f'{x:.1e}' if isinstance(x, (int, float)) and not isinstance(x, bool) else repr(x)


def check_after_main(after_dir, plan_sha, s0_sha, code):
    """★ Q-F — 감도 단계 = 주 판정 단계 (사다리 둘 · 예측) 가 끝난 뒤에만: 주 예측 요약 = PREDICTED · 변이 없음 · 같은 계획 · 같은 S0 계획 ·
    같은 코드 (★ PF2 D — `code_key` = HEAD + 코드 파일 지문 · 러너) → 묶음 기록 {dir, summary_sha256} (판정이 판정 입력의 주 예측과 대조한다)."""
    if not after_dir:
        raise Stop('MAIN_NOT_DONE', '--variant 인데 --after-main (주 예측 폴더) 이 없다 — 감도는 주 판정 단계가 끝난 뒤에만 (Q-F)')
    d = Path(after_dir).resolve()
    s, sha = read_summary(d, 'predict_summary.json')
    if s is None or s.get('tool') != TOOL or s.get('schema') != SCHEMA or s.get('stage') != 'predict':
        raise Stop('MAIN_NOT_DONE', f'{d}: 이 사슬의 주 예측 요약이 아니다')
    if s.get('variant') is not None or s.get('status') != 'PREDICTED':
        raise Stop('MAIN_NOT_DONE', f'{d.name}: 변이 {s.get("variant")!r} · 상태 {s.get("status")!r} — 주 예측 (변이 없음 · PREDICTED) 이어야')
    if (s.get('plan') or {}).get('sha256') != plan_sha or (s.get('s0_plan') or {}).get('sha256') != s0_sha:
        raise Stop('MAIN_NOT_DONE', f'{d.name}: 주 예측의 계획 · S0 계획 ≠ 이 감도 단계의 것')
    if code_key(s.get('code')) != code_key(code):              # ★ PF2 D — HEAD + 코드 파일 지문 (옛 = HEAD 만) · ★ 10-25 상대 경로 · 환경
        raise Stop('MAIN_NOT_DONE', f'{d.name}: 주 예측의 코드 (HEAD · 저장소 상대 경로 · 코드 파일 지문 · 러너 · 환경 지문) ≠ 지금 코드 '
                                    f'({", ".join(code_key_diff(s.get("code"), code))})')
    return {'dir': str(d), 'summary_sha256': sha}


# ═════════════════════════ (3) 사다리 단계 ═════════════════════════
def machine_missing_rc(a):
    """★ 10-27 묶음 C1a (C6 #15 · Q11) — 사다리 · 예측 = `--machine` 필수 (없음 = 인자 오류 rc 2 · 러너 · 출력 폴더 없음).  argparse 가 아니라 단계
    입구에서 본다 (문서 명령 꼴 대조 시험 K01 = 인자 해석만 · 등록 문서의 `[--machine]` 표기 개정 = 문서 몫)."""
    if getattr(a, 'machine', None) is None:
        print(f'인자 오류: --stage {a.stage} 는 --machine <짧은 이름표> 가 필요하다 (★ 10-27 묶음 C1a · 계획 exec_policy.allowed_machines 안 · 빈 이름 금지 · '
              f'런 기록마다 기계 · C6 #15) — 러너 · 출력 폴더 없음', file=sys.stderr)
        return 2
    return None


def stage_ladder(a, contract):
    rc_m = machine_missing_rc(a)
    if rc_m is not None:
        return rc_m
    #  ★ 10-27 묶음 C1b (RCA2-05 · Q9 §3-5) — 시도 꼴 (--ledger · --attempt): 풀기 전 대조 · 시도 폴더 <--out>/attempt_<n> (빈 폴더 요구를 대신한다)
    att = attempt_open(a, 'ladder')
    if isinstance(att, int):
        return att
    out = att.folder if att is not None else Path(a.out)
    if att is None:
        try:
            outdir_empty_or_stop(out)
        except Stop as e:
            print_stop(e)
            return 3
    s = summary_base('ladder', a)
    s['attempt'] = att.public() if att is not None else None
    s.update({'law': a.law, 'variant': a.variant, 'kit': a.kit or SBE_KIT, 'runs': [], 'ladder': None, 'env_scrubbed': [],
              'after_main': None, 'bed': None, 'sv_graph_source': None, 'noop': None})
    ran = False
    try:
        if not _same(a.target, TARGET_SBE_MS) or a.law not in LAWS or (a.kit or SBE_KIT) != SBE_KIT or a.variant == 'SVORDER':
            raise Stop('NOT_REGISTERED', f'--target {a.target} (등록 {TARGET_SBE_MS}) · --law {a.law} · --kit {a.kit} '
                                         f'(등록 {SBE_KIT}) · --variant {a.variant} (SVORDER 는 사다리 없음 — 주 사다리 그대로)')
        env_forbidden_or_stop()
        plan, plan_sha = load_plan(a.plan)
        s['plan'] = {'path': str(Path(a.plan).resolve()), 'sha256': plan_sha, 'content': plan}
        s['registration'] = check_plan_registered(plan_sha, a.registration)
        plan_doc_or_stop(a.registration, plan)              # ★ 10-27 묶음 C1a (C6 #30) — 등록의 계획 숫자 블록 = 계획 JSON (정확히)
        s['s0_plan'] = load_s0_plan(a.s0_plan, a.registration, plan)
        require_plan_numbers(plan)
        #  ★ PF2 B (10-22 · Q2) — S0 단계 2 보고가 봉인한 계획 해시 = 지금 두 계획 (정확히 · DBE 열람 전 계획 하나) · ★ PF2 D (PRE2-design-08) —
        #    S0 단계 1 보고 꼴 · 두 보고의 census · registry 일곱 파일 지문 = 지금 R 런 코드 (등록 R §2-1b · 다르면 멈춤 · s_min 다시 고르기 금지)
        s['s0_reports'] = {'stage2': read_s0_report(a.s0_stage2_report, 2), 'stage1': read_s0_report(a.s0_stage1_report, 1)}
        #  ★ PF2 D (PRE2-design-02) · ★ 10-25 묶음 B (RCA2-02 · Q2 (가)) — 같은 코드 관문을 S0 보고 대조 앞에 (git 밖 · 미확인 · dirty · 사슬 ↔
        #    러너 · 환경 = σ 런 없음 · 예측 · 판정과 같은 순서 · S0 대조의 계획 커밋 확인 (F5) 이 사슬 저장소의 git 을 쓴다)
        why = code_dirty_problem(s['code'])
        if why:
            raise Stop('CODE_PIN_MISMATCH', why)
        exec_check_or_stop(plan, a.max_hours, a.machine, s['code'])   # ★ 10-27 묶음 C1a — 시간 상한 · 기계 · 계획 봉인 판 (러너 전)
        got = s0_reports_problem(s['s0_reports'], plan_sha, s['s0_plan']['sha256'], s['code']['files'], s['code']['runner_files'],
                                 plan=plan)
        if got:
            raise Stop(*got)
        s['constants']['max_ladder_points'] = ladder_cap(plan)
        if a.variant is not None:
            s['after_main'] = check_after_main(a.after_main, plan_sha, s['s0_plan']['sha256'], s['code'])
        for p in (Path(a.root) / SBE_KIT, Path(a.runner)):
            if not p.exists():
                raise Stop('KIT_MISSING', f'{p}')
        #  ★ 10-25 묶음 B (RCA2-03 · Q3 (가) · 판정문 §4 F8) — R 런 직전 SBE 킷을 S0 와 같은 발견 함수로 다시 해시 = S0 단계 1 보고의 원 입력 ·
        #    설정 (경로 = 대조 밖) · 다르면 멈춤 (새 S0) · 파생 격자 지문 (off 격자 sid) 은 첫 arm 0 런을 읽을 때 (read_run · 같은 규약만)
        s['bed'] = bed_problem(s['s0_reports'], a.root, (SBE_KIT,))
        rcls, rkw = (att.runner_cls(), att.runner_kw()) if att is not None else (Runner, {})   # ★ 10-27 묶음 C1b-2 — 재실행 = ResumeRunner
        rn = rcls(a.runner, a.root, out, plan, a.variant, time.time() + a.max_hours * 3600.0, contract, dry=a.dry_run, prefix='L',
                  machine=a.machine, **rkw)
        s['resume'] = getattr(rn, 'resume', None)
        rn.s0_grid = s0_grid_seed(s['s0_reports'])
        rn.s0_census = s0_census_seed(s['s0_reports'])
        #  ★ 10-26 B″ (Q1 (가)) — 봉인 원천 (사다리 = SBE · SV 런 없음 → 부르지 않는다 · 같은 배선)
        rn.graph_src = RunnerGraphSource(a.runner, a.root, out / GRAPH_SRC_DIR, deadline=rn.deadline)
        s['env_scrubbed'] = rn.scrubbed
        if a.dry_run:
            print(f'dry-run — 사다리 {a.law} · 첫 런 (바닥 · 천장 · 1e4 · 1e6 · 1e8) 의 env (러너를 부르지 않는다 · 다음 점은 σ 로 정해진다 · '
                  f'끝 no-op = R_j,0 에서 SBE c {NOOP_C})')
            for role, rj in (('floor', 'inf'), ('ceiling', '0')) + tuple(('point', rj_key(10.0 ** e)) for e in LADDER_START_LOG10):
                rn.run(SBE_KIT, role, a.law, LADDER_C, rj, 1)
            return 0
        out.mkdir(parents=True, exist_ok=True)
        ran = True
        print(f'사다리 {a.law}{" · 변이 " + a.variant if a.variant else ""} — SBE arm 0 · LEAN 2 · 표적 {TARGET_SBE_MS} mS/cm '
              f'(값은 봉인 — 상태 · 반복 · 잔차 · 시간만)')
        lad = Ladder(lambda role, rj, arms: rn.run(SBE_KIT, role, a.law, LADDER_C, rj, arms), max_points=ladder_cap(plan),
                     ratio_max=plan['calib_rj_ratio_max'])
        try:
            try:
                lad.run()
                lad.origin()                   # §3-3 — 주 · 감도 변이 같게 (같은 판정 함수 · §5-6 3판)
                #  ★ 10-27 묶음 C2a (Q9 §2-1 · R4-06 (d) · 개정 5 ①) — SBE c 1 no-op = 사다리 단계 끝 (같은 사슬 부모의 동결 환경 · 기록만 · 기술 멈춤 =
                #    사다리 멈춤)
                s['noop'] = ladder_noop(lambda role, rj, arms: rn.run(SBE_KIT, role, a.law, NOOP_C, rj, arms), lad, a.law)
                s['status'] = 'CALIBRATED'
            finally:
                s['ladder'], s['flags'] = lad.st, list(lad.flags)
                s['runs'] = rn.records
                s['sv_graph_source'] = rn.graph_src.public()
        except Stop as e:
            s['status'] = e.code if e.code in REGISTERED_OUTCOMES else 'STOPPED'
            raise
    except Stop as e:
        s['stop'] = e.record()
        if s['status'] is None:
            s['status'] = 'STOPPED'
        print_stop(e)
    if a.dry_run and not ran:
        return 3
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / 'ladder_summary.json', s)
    if att is not None:
        rc_a = attempt_close(att, s)                      # ★ 10-27 묶음 C1b — 결과 줄 (그룹 종료 확인 뒤) · 못 쓰면 rc 3
        if rc_a is not None:
            return rc_a
    L = s.get('ladder') or {}
    if s['status'] == 'CALIBRATED':
        e_lo, e_hi = (L.get('ends') or {}).get('lo') or {}, (L.get('ends') or {}).get('hi') or {}
        print(f'보정 = CALIBRATED · R_j,0 = {disp_rj(L["R_j0"])} · R_j,lo {disp_rj(L["R_j_lo"])} ({e_lo.get("source")}) · R_j,hi '
              f'{disp_rj(L["R_j_hi"])} ({e_hi.get("source")}) · 역상 R 비 {L["R_ratio"]:.4g} · 런 {L["n_runs"]} · ×100 {L["n_ext"]} · '
              f'반씩 {L["n_bisect"]} · 확인 {len(L["confirms"])} · 국소 e ≥ e_min {L["local_e_ge_emin"]} · origin {(L["origin"] or {}).get("status")}'
              + (f' · 표지 {s["flags"]}' if s['flags'] else '')
              + f' · no-op {(s.get("noop") or {}).get("status")} {(s.get("noop") or {}).get("ok")}')
    else:
        print(f'보정 = {s["status"]}' + (f' (사유 {(s.get("stop") or {}).get("reason")})' if (s.get('stop') or {}).get('reason') else ''))
    print(f'요약 → {out / "ladder_summary.json"}')
    return 0 if s['status'] == 'CALIBRATED' else 3


# ═════════════════════════ (4) 예측 단계 ═════════════════════════
def load_ladders(dirs, variant, reg_path, contract, sid_reg, now_code=None):
    """사다리 요약 둘 → {법칙: {...}} · 계획 · S0 계획 · 코드 · 변이 사다리의 주 예측 묶음.  R_j 는 요약에서 그대로 (사람이 옮겨 적지 않는다) ·
    R_j,0 확인 팔을 다시 읽는다.  ★ PF2 D — 사다리마다 dirty 기록 · 두 사다리 코드 키 (HEAD + 코드 파일 지문) 같음 · S0 보고 지문 = 지금 코드
    (`now_code` = 예측 단계의 `code_record`)."""
    want_var = None if variant == 'SVORDER' else variant
    out, plan, plan_sha, code, s0, after = {}, None, None, None, None, None
    s0reps, first = None, True
    seen = set()
    for d in dirs:
        rd = Path(d).resolve()
        if rd in seen:
            raise Stop('DUPLICATE_RUN', f'같은 사다리 폴더 두 번 {rd}')
        seen.add(rd)
        s, sha = read_summary(rd, 'ladder_summary.json')
        if s is None or s.get('stage') != 'ladder' or s.get('tool') != TOOL or s.get('schema') != SCHEMA:
            raise Stop('LADDER_SET', f'{rd}: 이 사슬 (3판) 의 ladder_summary.json 이 없다')
        if s.get('status') != 'CALIBRATED':
            raise Stop('LADDER_NOT_CALIBRATED', f'{rd.name}: 사다리 상태 {s.get("status")} — 예측하지 않는다 (판정 = 그 이름)')
        plan_record_or_stop((s.get('plan') or {}).get('content'), rd.name)   # ★ 10-27 묶음 C1a — 기록된 계획 꼴 (실행 정책 칸을 쓰기 전)
        if s.get('variant') != want_var:
            raise Stop('LADDER_SET', f'{rd.name}: 사다리 변이 {s.get("variant")!r} ≠ {want_var!r}')
        law = s.get('law')
        if law in out:
            raise Stop('DUPLICATE_RUN', f'{law} 사다리가 둘 ({out[law]["dir"]} · {rd}) — 같은 킷 · 같은 계획 두 번')
        if plan_sha is not None and s['plan']['sha256'] != plan_sha:
            raise Stop('PLAN_HASH_MISMATCH', '두 사다리의 계획이 다르다')
        if s0 is not None and (s.get('s0_plan') or {}).get('sha256') != s0.get('sha256'):
            raise Stop('S0_PLAN_HASH_MISMATCH', '두 사다리의 S0 계획이 다르다')
        why = code_dirty_problem(s.get('code'))               # ★ PF2 D — 고쳐진 트리에서 돈 사다리 (기록) 는 예측 입력이 아니다
        if why:
            raise Stop('CODE_PIN_MISMATCH', f'{rd.name}: {why}')
        if code is not None and code_key(s.get('code')) != code_key(code):
            raise Stop('CODE_PIN_MISMATCH', '두 사다리의 코드 (HEAD · 저장소 상대 경로 · 코드 파일 지문 · 러너 · 환경 지문) 가 다르다 '
                                            f'({", ".join(code_key_diff(s.get("code"), code))})')
        if after is not None and s.get('after_main') != after:
            raise Stop('MAIN_NOT_DONE', '두 변이 사다리의 주 예측 묶음이 다르다')
        #  ★ PF2 B — 두 사다리가 같은 단계 2 봉인을 읽었나 · ★ 10-25 묶음 B (RCA2-03) — 경로 문자열 (보고 · 원 입력 파일) = 대조 밖
        if not first and s0_records_key(s.get('s0_reports')) != s0_records_key(s0reps):
            raise Stop('S0_REPORT_MISMATCH', '두 사다리의 S0 단계 보고 기록이 다르다 (경로 뺀 칸)')
        first, s0reps = False, s.get('s0_reports')
        plan, plan_sha, code, s0, after = s['plan']['content'], s['plan']['sha256'], s.get('code') or {}, s.get('s0_plan'), s.get('after_main')
        L = s['ladder']
        r0run = [r for r in s['runs'] if r.get('rj') == L['R_j0'] and r.get('arms') == 1 and r.get('arm_list') is None
                 and r.get('role') in ('confirm', 'point')]
        if not r0run:
            raise Stop('LADDER_SET', f'{rd.name}: R_j,0 확인 팔 기록이 없다')
        r = r0run[-1]
        req = {k: r.get(k) for k in REQ_KEYS}
        arm = read_run(rd / r['outdir'], req, plan, contract, sid_reg, want_sha=[x['sha256'] for x in r['arms_read']])[0]
        #  ★ 10-27 묶음 C2a (Q9 §2-1 · R4-06 (c) (d)) — 사다리 끝 no-op 기록 꼴 · 그 런을 원 팔에서 다시 읽어 다시 대조 (요약 기록을 믿지 않는다 ·
        #    NOT_COMPUTED 기록 = 다시 읽기도 같은 멈춤 · 판정이 예측 첫머리에서 옛 자리 · 옛 이름으로 낸다)
        nr = noop_check(rd, s, law, L['R_j0'], arm, plan, contract, sid_reg)
        out[law] = {'dir': str(rd), 'summary_sha256': sha, 'variant': s.get('variant'), 'R_j0': L['R_j0'], 'R_j_lo': L['R_j_lo'],
                    'R_j_hi': L['R_j_hi'], 'r0_sigma': arm['sigma'], 'noop': nr}
    if sorted(out) != sorted(LAWS):
        raise Stop('LADDER_SET', f'사다리 법칙 {sorted(out)} ≠ {list(LAWS)}')
    check_plan_registered(plan_sha, reg_path)
    s0rec = recheck_s0_record(s0, reg_path, plan)
    require_plan_numbers(plan)
    #  ★ PF2 D (10-22 · PRE2-design-02) — 지금 트리 dirty · 지금 코드 (HEAD + 코드 파일 지문 · 러너) ≠ 사다리 기록 = 멈춤 (옛 = HEAD 만)
    now = now_code if now_code is not None else code
    why = code_dirty_problem(now)
    if why:
        raise Stop('CODE_PIN_MISMATCH', f'지금 {why}')
    if code_key(code) != code_key(now):
        raise Stop('CODE_PIN_MISMATCH', f'사다리 코드 (HEAD · 저장소 상대 경로 · 코드 파일 지문 · 러너 · 환경 지문) ≠ 지금 코드 '
                                        f'({", ".join(code_key_diff(code, now))}) — 같은 핀 커밋 · 같은 환경 판에서 돌릴 것')
    #  ★ PF2 B · D — 사다리 기록의 단계 2 봉인 = 이 계획 · 단계 1 꼴 · 두 보고 지문 = 지금 코드 (같은 함수로 다시)
    got = s0_reports_problem(s0reps, plan_sha, s0rec['sha256'], now.get('files'), now.get('runner_files'), plan=plan)
    if got:
        raise Stop(*got)
    return out, plan, plan_sha, code, s0rec, after, s0reps


def stage_predict(a, contract):
    if getattr(a, 'merge', None):                         # ★ 10-27 묶음 C2d — 합치기 (러너 없음 · 시도 꼴 아님)
        return stage_merge(a, contract)
    rc_m = machine_missing_rc(a)
    if rc_m is not None:
        return rc_m
    #  ★ 10-27 묶음 C2d (Q9 §3-1 · §3-2) — 단위 (--unit) · 넘침 점 (--point · --expand) 시도 = 같은 단계 입구 · 같은 관문 · 그 단위의 늘 필요한 런만
    kind = 'unit' if getattr(a, 'unit', None) else ('point' if getattr(a, 'point', None) else None)
    att = attempt_open(a, 'predict')                     # ★ 10-27 묶음 C1b — 시도 꼴 (stage_ladder 와 같은 입구)
    if isinstance(att, int):
        return att
    out = att.folder if att is not None else Path(a.out)
    if att is None:
        try:
            outdir_empty_or_stop(out)
        except Stop as e:
            print_stop(e)
            return 3
    s = summary_base('predict' if kind is None else kind, a)
    s['attempt'] = att.public() if att is not None else None
    s.update({'variant': a.variant, 'kit': a.kit or DBE_KIT, 'runs': [], 'ladders': {}, 'checks': None, 'origin': None,
              'env_scrubbed': [], 'after_main': None, 'sv_cf': None, 'bed': None, 'sv_graph_source': None})
    if kind is not None:
        nm = a.unit if kind == 'unit' else a.point
        u_c, u_law, u_rr = unit_parse(nm)
        s['unit'] = {'kind': kind, 'name': nm, 'target': att.entry['target'], 'law': u_law, 'c': u_c, 'rj_role': u_rr}
        if kind == 'point':                               # 인용한 결정 기록 (파일 바이트 sha · 꼴 = 풀기 전 대조가 이미 봤다 · 끝 합치기가 대조)
            try:
                dsha = sha256_file(a.expand)
            except OSError:
                dsha = None
            s['expansion'] = {'path': str(Path(a.expand).resolve()), 'sha256': dsha}
    ran = False
    try:
        if (a.kit or DBE_KIT) != DBE_KIT:
            raise Stop('NOT_REGISTERED', f'--kit {a.kit} (등록 {DBE_KIT})')
        env_forbidden_or_stop()
        if att is not None:
            #  ★ 10-27 묶음 C1b (Q9 §3-5) — 원장 꼴 예측의 사다리 입력 = 같은 원장의 채택 사다리 시도만 (원장 · 폴더 · 규칙이 정한다 · 사다리 요약 읽기 전)
            ledger_inputs_check(a.ladders, att.repo, att.head, att.st, want_prefix='ladder:')
        sid_reg = {}
        #  ★ PF2 D (10-22 · PRE2-design-02) — 지금 코드 (`s['code']`) 를 넘겨 사다리 기록 · S0 보고 지문과 대조 (load_ladders 안 · 옛 = HEAD 만)
        lads, plan, plan_sha, code, s0rec, lad_after, s0reps = load_ladders(a.ladders, a.variant, a.registration, contract, sid_reg,
                                                                            now_code=s['code'])
        s['ladders'] = {k: {kk: v[kk] for kk in ('dir', 'summary_sha256', 'variant', 'R_j0', 'R_j_lo', 'R_j_hi')} for k, v in lads.items()}
        s['plan'] = {'sha256': plan_sha, 'content': plan}
        s['s0_plan'] = s0rec
        s['s0_reports'] = s0reps                             # ★ PF2 B — 사다리가 읽은 단계 2 봉인 (판정이 다시 대조)
        s['registration'] = check_plan_registered(plan_sha, a.registration)
        plan_doc_or_stop(a.registration, plan)              # ★ 10-27 묶음 C1a (C6 #30)
        exec_check_or_stop(plan, a.max_hours, a.machine, s['code'])   # ★ 10-27 묶음 C1a — 시간 상한 · 기계 · 계획 봉인 판 (러너 전)
        if a.variant is not None:
            s['after_main'] = check_after_main(a.after_main, plan_sha, s0rec['sha256'], s['code'])
            if a.variant != 'SVORDER' and lad_after != s['after_main']:
                raise Stop('MAIN_NOT_DONE', '변이 사다리가 묶인 주 예측 ≠ --after-main (같은 주 판정 단계 뒤여야)')
        scope = plan['sv_cf_scope'] if a.variant is None else None
        s['sv_cf'] = {'scope': scope, 'threshold': (plan['sv_cf_threshold'] if a.variant is None else None)}
        for p in (Path(a.root) / SBE_KIT, Path(a.root) / DBE_KIT, Path(a.runner)):
            if not p.exists():
                raise Stop('KIT_MISSING', f'{p}')
        #  ★ 10-25 묶음 B (RCA2-03 · Q3 (가) · 판정문 §4 F8) — R 런 직전 SBE · DBE 킷 다시 해시 = S0 단계 1 · 2 보고의 원 입력 · 설정
        s['bed'] = bed_problem(s0reps, a.root, (SBE_KIT, DBE_KIT))
        rcls, rkw = (att.runner_cls(), att.runner_kw()) if att is not None else (Runner, {})   # ★ 10-27 묶음 C1b-2 — 재실행 = ResumeRunner
        rn = rcls(a.runner, a.root, out, plan, a.variant, time.time() + a.max_hours * 3600.0, contract, dry=a.dry_run,
                  prefix=('P' if kind is None else UNIT_PREFIX), machine=a.machine, **rkw)
        s['resume'] = getattr(rn, 'resume', None)
        rn.sid_reg = sid_reg
        rn.s0_grid = s0_grid_seed(s0reps)
        rn.s0_census = s0_census_seed(s0reps)
        #  ★ 10-26 B″ (1저자 Q1 (가)) — SV 끝 그래프 생산 봉인 원천 (SV 모서리 런마다 같은 러너 · 같은 env 로 조립만 · 같은 시간 상한)
        rn.graph_src = RunnerGraphSource(a.runner, a.root, out / GRAPH_SRC_DIR, deadline=rn.deadline)
        s['env_scrubbed'] = rn.scrubbed
        pr = Predict(rn.run, lads, a.variant, sv_scope=scope)
        if a.dry_run:
            print('dry-run — 예측 런의 env (러너를 부르지 않는다 · origin 런은 arm 0 값으로 정해진다 · ★ 10-27 묶음 C2a — SBE no-op = 사다리 끝 런 · '
                  '예측은 그 기록을 읽는다)')
            for law in LAWS:
                for rr in RJ_ROLES:
                    for c in CS:
                        rn.run(DBE_KIT, 'corner', law, c, lads[law][rr], 1, pr._sv_on(rr))
            return 0
        out.mkdir(parents=True, exist_ok=True)
        ran = True
        if kind is None:
            print(f'예측{" · 변이 " + a.variant if a.variant else ""} — DBE arm 0 · 네 모서리 × {{R_j,lo · R_j,0 · R_j,hi}} · origin 세 R '
                  f'(값은 봉인){" · SV 반사실 범위 " + str(scope) if scope else ""}')
        else:
            print(f'{"단위" if kind == "unit" else "넘침 점"} {s["unit"]["name"]}{" · 변이 " + a.variant if a.variant else ""} — '
                  f'{"모서리 arm 0 · origin 표본 arm 1 · 2" if kind == "unit" else "origin8 (8 팔)"} (값은 봉인 · 판정 함수는 합치기가)')
        try:
            try:
                if kind is None:
                    pr.run()
                    s['status'] = 'PREDICTED'
                else:
                    unit_runs(pr, rn, kind, s['unit'], lads)     # ★ 10-27 묶음 C2d — 단위 · 넘침 점의 늘 필요한 런만
                    s['status'] = UNIT_DONE[kind]
            finally:
                s['checks'], s['origin'], s['runs'] = pr.checks, pr.origin, rn.records
                s['sv_graph_source'] = rn.graph_src.public()
        except Stop as e:
            #  ★ 4판 (Q1) — NOT_COMPUTED (풀이 · 증서 실패 · 단락 ELECTRODE_SHORT) = 예측 단계의 등록 결과 (사다리와 같은 뜻 · 판정이 원 팔에서
            #    다시 계산해 이름 · 사유를 남긴다) · 그 밖 멈춤 (계약 · 기록 · 일관 검사 …) = STOPPED (판정 입력 아님)
            s['status'] = e.code if e.code in PREDICT_OUTCOMES else 'STOPPED'
            raise
    except Stop as e:
        s['stop'] = e.record()
        if s['status'] is None:
            s['status'] = 'STOPPED'
        print_stop(e)
    if a.dry_run and not ran:
        return 3
    out.mkdir(parents=True, exist_ok=True)
    sname = 'predict_summary.json' if kind is None else UNIT_SUMMARY[kind]
    write_json(out / sname, s)
    if att is not None:
        rc_a = attempt_close(att, s)                      # ★ 10-27 묶음 C1b — 결과 줄 (그룹 종료 확인 뒤) · 못 쓰면 rc 3
        if rc_a is not None:
            return rc_a
    done = 'PREDICTED' if kind is None else UNIT_DONE[kind]
    if s['status'] == 'PREDICTED':
        n_adj = sum(1 for o in (s['origin'] or []) if o['status'] == 'adjusted')
        print(f'예측 = PREDICTED · 런 {len(s["runs"])} · 같은 P 일관 통과 · origin 규칙이 옮긴 모서리 {n_adj}')
    elif s['status'] == done:
        print(f'{kind} {s["unit"]["name"]} = {done} · 런 {len(s["runs"])}')
    else:
        print(f'{"예측" if kind is None else kind} = {s["status"]}' + (f' (사유 {(s.get("stop") or {}).get("reason")})'
                                                                    if (s.get('stop') or {}).get('reason') else ''))
    print(f'요약 → {out / sname}')
    return 0 if s['status'] == done else 3


def unit_runs(pr, rn, kind, u, lads):
    """★ 10-27 묶음 C2d (Q9 §3-1) — 단위 시도 = no-op 기록 (첫머리 · 예측과 같은 이름 · 단위가 no-op 결과보다 먼저 DBE 를 풀지 않게) → 모서리 arm 0
    (SV 반사실 = 예측과 같은 범위 `Predict._sv_on`) → origin 표본 arm 1 · 2 (이 차례 · 한 기계) · 넘침 점 = origin8 8 팔 (결정 기록이 요구한 것만).
    판정 함수 (same_p · W0 · origin 판정 · 단조) 는 여기서 부르지 않는다 (합치기가 다 모은 뒤 같은 함수로)."""
    pr.noop_first()
    rj = lads[u['law']][u['rj_role']]
    if kind == 'unit':
        rn.run(DBE_KIT, 'corner', u['law'], u['c'], rj, 1, pr._sv_on(u['rj_role']))
        rn.run(DBE_KIT, 'origin', u['law'], u['c'], rj, ORIGIN_ARMS)
    else:
        rn.run(DBE_KIT, 'origin8', u['law'], u['c'], rj, 8)


# ═════════════════════════ ★ 10-27 묶음 C2d 합치기 (Q9 §3-2 2 · 3 · §3-4 · §4 · author 10-27 approved bundle C) ═════════════════════════
#: 단위 · 넘침 점 시도 안 런 번호 (unit_runs 차례 · 앞자리 UNIT_PREFIX)
UNIT_RUN_INDEX = {'corner': 1, 'origin': 2, 'origin8': 1}
RUN_DIR_RE = re.compile(r'[A-Za-z0-9_][A-Za-z0-9_.-]*')


class ExpansionNeeded(Exception):
    """합치기 다시 계산이 넘침에 닿았다 — 첫 합치기 (first · 결정 기록을 쓴다 · 점 = 넘침 목록 · attempts = 단위 채택 시도 sha 집합) · 끝 합치기의 빠진 점
    (missing) · 멈춤 아님 · 판정 입력 아님 (상태 EXPANSION_NEEDED · rc 4)."""

    def __init__(self, points=None, first=False, attempts=None, missing=None):
        super().__init__('EXPANSION_NEEDED')
        self.points, self.first, self.attempts, self.missing = points, first, attempts, missing


def collect_attempts(paths):
    """--merge 경로 → {n: [경로 …]} — attempt_<n> 폴더 · attempt_<n>.rejected.json 파일 = 그 자신 · 그 밖 폴더 = 바탕 (자식 중 시도 꼴) · 같은 실경로 = 한 번 ·
    없는 경로 = Stop ATTEMPT_LEDGER_MISMATCH."""
    found = {}
    for x in paths:
        p = Path(x)
        if not p.exists():
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'--merge 경로 {x} 가 없다')
        rp = p.resolve()
        own = (rp.is_dir() and ATTEMPT_DIR_RE.fullmatch(rp.name)) or (rp.is_file() and ATTEMPT_SIDE_RE.fullmatch(rp.name))
        for q in ([rp] if own else (sorted(rp.iterdir()) if rp.is_dir() else [])):
            m = ATTEMPT_DIR_RE.fullmatch(q.name) if q.is_dir() else ATTEMPT_SIDE_RE.fullmatch(q.name)
            if m:
                found.setdefault(int(m.group(1)), [])
                if q not in found[int(m.group(1))]:
                    found[int(m.group(1))].append(q)
    return found


def unit_targets(st, variant):
    """원장의 단위 · 넘침 점 대상 (그 변이) → 정렬 목록."""
    out = set()
    for e in st['entries'].values():
        tp = target_parts(e['target'])
        if tp is not None and tp[1] == variant:
            out.add(e['target'])
    return sorted(out)


def merge_want(s):
    """예측 · 단위 · 합친 요약 → 단위 출처 대조 칸 (Q9 §3-3 · §3-4 "위 출처 칸이 모든 채택 폴더에서 같다") — 변이 · 계획 · S0 계획 · S0 보고 (경로 뺀 칸) · 코드 키
    (HEAD · 상대 경로 · 파일 지문 · 러너 · 환경 같음 단위) · 두 사다리 요약 sha · 주 예측 묶음 sha · SV 범위 · 침대 (경로 뺀 지문).  기계 · 원장 항목 · 단위
    이름 · 환경 지문의 기록 전용 칸은 대조 밖 (다를 수 있다)."""
    return {'variant': s.get('variant'), 'plan': (s.get('plan') or {}).get('sha256'), 's0': (s.get('s0_plan') or {}).get('sha256'),
            's0_key': s0_records_key(s.get('s0_reports')), 'code': code_key(s.get('code') if isinstance(s.get('code'), dict) else {}),
            'ladders': {law: (v or {}).get('summary_sha256') for law, v in sorted((s.get('ladders') or {}).items())},
            'after_main': (s.get('after_main') or {}).get('summary_sha256'), 'sv_cf': s.get('sv_cf'), 'bed': s.get('bed')}


def unit_summary_problem(su, kind, target, n, entry, want, dec_sha=None):
    """단위 · 넘침 점 시도 요약 ↔ 합치기 (출처) → 사유 | None — 이 사슬의 그 단계 요약 · 단위 칸 = 대상 · attempt 칸 = 원장 항목 · 기계 = 항목 기계 · 출처 칸
    (`merge_want`) 같음 · dirty 없음 · 넘침 점 = 인용한 결정 기록 sha = 이 합치기의 결정 기록 · 상태 = 완주 · 멈춤 · NOT_COMPUTED."""
    if not isinstance(su, dict) or su.get('tool') != TOOL or su.get('schema') != SCHEMA or su.get('stage') != kind:
        return f'{UNIT_SUMMARY[kind]} 이 이 사슬의 {kind} 요약이 아니다'
    u = su.get('unit') if isinstance(su.get('unit'), dict) else {}
    tp = target_parts(target)
    if u.get('kind') != kind or u.get('target') != target or tp is None or u.get('name') != tp[2]:
        return f'단위 칸 {u.get("kind")} · {u.get("target")} · {u.get("name")} ≠ 대상 {target}'
    at = su.get('attempt') if isinstance(su.get('attempt'), dict) else {}
    if at.get('n') != n or at.get('target') != target:
        return f'attempt 칸 {at.get("n")} · {at.get("target")} ≠ 원장 항목 {n}'
    if su.get('machine') != entry.get('machine'):
        return f'기계 {su.get("machine")!r} ≠ 원장 항목 기계 {entry.get("machine")!r}'
    why = code_dirty_problem(su.get('code'))
    if why:
        return why
    got = merge_want(su)
    diff = [k for k in ('variant', 'plan', 's0', 's0_key', 'code', 'ladders', 'after_main', 'sv_cf', 'bed') if got[k] != want[k]]
    if diff:
        return f'출처 칸 {diff} ≠ 합치기 (Q9 §3-4)'
    if kind == 'point' and (su.get('expansion') or {}).get('sha256') != dec_sha:
        return f'점 시도가 인용한 결정 기록 sha {str((su.get("expansion") or {}).get("sha256"))[:12]} ≠ 이 합치기의 결정 기록 {str(dec_sha)[:12]}'
    if su.get('status') not in (UNIT_DONE[kind], 'STOPPED', 'NOT_COMPUTED'):
        return f'상태 {su.get("status")!r}'
    stp = su.get('stop')
    if (su.get('status') == UNIT_DONE[kind]) != (stp is None) or (stp is not None and not (isinstance(stp, dict) and isinstance(stp.get('code'), str))):
        return f'상태 {su.get("status")!r} ↔ 멈춤 기록 {stp!r}'
    return None


class MergeFetch:
    """★ 10-27 묶음 C2d (Q9 §3-2 · §3-4 · §4) 합치기의 fetch — 한 기계 사슬과 같은 판정 함수 (`Predict`) 가 같은 차례로 요청하는 런을 채택된 단위 · 넘침 점
    시도 폴더에서 키로 찾는다 (한 번씩):
      · 대상 (요청의 법칙 · c · R → unit · origin8 = point) 을 처음 요청할 때 = 그 대상의 원장 대조 (`target_ledger_problem` · 미리 세고 그때 낸다 —
        요청되지 않은 대상의 대조 결과 = unused_runs 에 기록만) → 채택 (재실행 사슬 끝 · 없음 = UNIT_MISSING · 넘침 점 = EXPANSION_NEEDED) → 그 대상 시도
        폴더 전부 사본 (units/<대상>/attempt_<n> · 바이트 · 요약 sha = 결과 줄) → 출처 (`unit_summary_problem`)
      · 런 = 그 시도 요약의 같은 차례 런 (요청 칸 같음) · rc 0 = 사본에서 같은 `read_run` (같은 계약 · sid 원장 · S0 격자 · census · 봉인 원천) · 러너가
        멈춘 런 · 런 기록 전 멈춤 = 그 시도 요약의 멈춤을 이 런 요청에서 (부분 채택 · 한 기계 사슬과 같은 자리) · 런 이름 = 사슬 차례 (P<번호>_<역할>)
      · 넘침 (`expand_hook`) = 결정 기록 없음 → ExpansionNeeded (첫 합치기) · 있음 → 다시 센 넘침 목록 · 단위 채택 시도 sha 집합 = 결정 기록 (구조 칸 ·
        W0 · 환경 = 기록만 · 다르면 UNIT_PROVENANCE_MISMATCH = 칼날 보고 · Q9 개정 4 Q4)
      · 끝 (`finish`) = 결정 기록이 있는데 넘침 없음 · 채택 런이 남음 (UNIT_EXTRA)."""

    def __init__(self, repo, commit, raw, st, found, lads, variant, plan, contract, sid_reg, s0_grid, s0_census, graph_src, out, want,
                 env, decision=None, dec_sha=None):
        self.repo, self.commit, self.raw, self.st, self.found = Path(repo), commit, raw, st, found
        self.lads, self.variant, self.plan, self.contract, self.sid_reg = lads, variant, plan, contract, sid_reg
        self.s0_grid, self.s0_census, self.graph_src, self.out, self.want = s0_grid, s0_census, graph_src, Path(out), want
        self.env, self.decision, self.dec_sha = env, decision, dec_sha
        self.allowed = list((plan.get('exec_policy') or {}).get('allowed_machines') or [])
        self.records, self.keys, self.n = [], set(), 0
        self.opened, self.copied = {}, {}
        self.hook_called = False
        self.tinfo = {}
        for t in unit_targets(st, variant):
            info = {'ns': [k for k, e in st['entries'].items() if e['target'] == t], 'ad': None, 'paths': {}, 'problem': None}
            try:
                ns, ad, paths = target_ledger_problem(self.repo, st, raw, commit, t, found)
                info.update(ad=ad, paths=paths)
                lim = attempt_limit_problem(st, t, max(ns), plan) if ns else None
                if lim and lim[0] == 'ATTEMPT_LIMIT':
                    info['problem'] = lim
            except Stop as e:
                info['problem'] = (e.code, e.cause)
            self.tinfo[t] = info

    def _role_of(self, law, rj, name):
        rr = [k for k in RJ_ROLES if self.lads[law][k] == rj]
        if len(rr) != 1:
            raise Stop('UNIT_PROVENANCE_MISMATCH', f'요청 R_j {disp_rj(rj)} 가 {law} 사다리의 R 하나가 아니다 ({rr})', name)
        return rr[0]

    def _copy(self, target, k, src):
        if k in self.copied:
            return self.copied[k]
        dst = self.out / UNITS_DIR / target_dir(target) / src.name
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            if src.is_dir():
                shutil.copytree(src, dst, symlinks=True)
            else:
                shutil.copy2(src, dst)
        except OSError as e:
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{src.name} 사본을 못 만든다 ({type(e).__name__}: {e})')
        if folder_digest(dst) != self.st['results'][k]['folder_sha256']:
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{target_dir(target)}/{dst.name} 사본 요약 sha ≠ 원장 결과 줄 {k} (복사하는 사이 원본이 바뀌었다)')
        self.copied[k] = dst
        return dst

    def _missing_points(self):
        out = []
        for p in (self.decision or {}).get('points') or []:
            info = self.tinfo.get(unit_target('point', self.variant, p))
            if info is None or not info['ns'] or (not info['problem'] and (info['ad'] or {}).get('effective') is None):
                out.append(p)
        return out

    def _open(self, target, kind, name):
        info = self.tinfo.get(target)
        if info is not None and info['problem']:
            raise Stop(info['problem'][0], f'{target}: {info["problem"][1]}', name)
        n = ((info or {}).get('ad') or {}).get('effective')
        if n is None:
            if kind == 'point':                            # 넘침 점이 아직 없다 = 다음 단계 필요 (멈춤 아님 · Q9 §3-2 "넘침 런만 없으면 EXPANSION_NEEDED")
                raise ExpansionNeeded(missing=self._missing_points())
            raise Stop('UNIT_MISSING', f'{target}: 채택 시도가 없다 (원장 시도 {(info or {}).get("ns") or []} — 없음 · 결과 전 · 거부뿐)', name)
        for k in info['ns']:
            self._copy(target, k, info['paths'][k])
        folder = self.copied[n]
        su, sha = read_summary(folder, UNIT_SUMMARY[kind])
        if su is None and (self.st['results'].get(n) or {}).get('status') == 'interrupted':
            raise Stop('UNIT_MISSING', f'{target} attempt_{n}: 채택 시도가 끊겼다 (결과 줄 interrupted · 요약 없음 = 요청한 런을 알 수 없다 — 재실행 자격이면 '
                                       f'--add --resume {n} · 아니면 그 단위 = 멈춤)', name)
        entry = self.st['entries'][n]
        why = unit_summary_problem(su, kind, target, n, entry, self.want, self.dec_sha)
        if why is None and entry['machine'] not in self.allowed:
            why = f'기계 {entry["machine"]!r} ∉ 계획 허용 목록 {self.allowed}'
        if why:
            raise Stop('UNIT_PROVENANCE_MISMATCH', f'{target} attempt_{n}: {why}', name)
        u = {'n': n, 'ad': info['ad'], 'sum': su, 'sha': sha, 'rel': f'{UNITS_DIR}/{target_dir(target)}/{folder.name}', 'machine': entry['machine'],
             'runs': {r.get('name'): r for r in su.get('runs') or [] if isinstance(r, dict)}, 'consumed': set()}
        self.opened[target] = u
        return u

    def run(self, kit, role, law, c, rj, arms, sv_cf=False):
        self.n += 1
        name, req, key = run_request('P', self.n, kit, role, law, c, rj, arms, sv_cf, self.variant)
        if key in self.keys:
            raise Stop('DUPLICATE_RUN', f'{kit} · {law} · c {c} · R_j {disp_rj(rj)} · 팔 {arm_indices(req)} 를 두 번 요청', name)
        self.keys.add(key)
        kind = 'point' if role == 'origin8' else 'unit'
        target = unit_target(kind, self.variant, unit_name(c, law, self._role_of(law, rj, name)))
        u = self.opened.get(target) or self._open(target, kind, name)
        iname = f'{UNIT_PREFIX}{UNIT_RUN_INDEX.get(role, 0):02d}_{role}'
        rec0 = u['runs'].get(iname)
        stop0 = (u['sum'].get('stop') if isinstance(u['sum'].get('stop'), dict) else None) or {}
        if rec0 is None:
            if stop0.get('run') == iname:                  # 그 시도가 런 기록 전에 그 런에서 멈췄다 (시간 · 폴더 · 요청 꼴) = 그 멈춤 (부분 채택)
                raise Stop(stop0.get('code'), stop0.get('cause'), name, stop0.get('reason'))
            raise Stop('UNIT_MISSING', f'{target} attempt_{u["n"]}: 요청 {role} · R_j {disp_rj(rj)} 의 런 {iname} 이 그 시도에 없다', name)
        bad = [k for k in REQ_KEYS if k != 'name' and rec0.get(k) != req.get(k)]
        od = rec0.get('outdir')
        if bad or not (isinstance(od, str) and RUN_DIR_RE.fullmatch(od) and od.startswith(iname)):
            raise Stop('UNIT_PROVENANCE_MISMATCH', f'{target} attempt_{u["n"]} 런 {iname} 요청 · 폴더 ≠ 다시 계산의 요청 (칸 {bad} · 폴더 {od!r})', name)
        u['consumed'].add(iname)
        rel = f'{u["rel"]}/{od}'
        rec = dict(req, outdir=rel, rc=rec0.get('rc'), seconds=rec0.get('seconds'), arms_read=[], machine=u['machine'],
                   group_cause=rec0.get('group_cause'), source={'target': target, 'attempt': u['n'], 'run': iname, 'outdir': od})
        self.records.append(rec)
        if rec0.get('rc') != 0:                            # 러너가 멈춘 런 = 그 시도 요약의 멈춤 (부분 채택 · 그 런이 요청될 때)
            if stop0.get('run') != iname:
                raise Stop('UNIT_PROVENANCE_MISMATCH', f'{target} attempt_{u["n"]} 런 {iname} rc {rec0.get("rc")!r} 인데 그 시도의 멈춤 런 = '
                                                       f'{stop0.get("run")!r}', name)
            raise Stop(stop0.get('code'), stop0.get('cause'), name, stop0.get('reason'))
        outdir = self.out / rel
        try:
            arms_ = read_run(outdir, req, self.plan, self.contract, self.sid_reg, want_sha=[x.get('sha256') for x in rec0.get('arms_read') or []],
                             s0_grid=self.s0_grid, s0_census=self.s0_census, graph_src=self.graph_src)
        except Stop:
            rec['arms_read'] = arm_file_shas(outdir)
            raise
        if stop0.get('run') == iname:                      # 그 시도는 이 런에서 멈췄다고 적었는데 같은 바이트의 다시 읽기가 지났다
            raise Stop('UNIT_PROVENANCE_MISMATCH', f'{target} attempt_{u["n"]}: 그 시도는 런 {iname} 에서 {stop0.get("code")} 로 멈췄다고 적었는데 사본 다시 '
                                                   f'읽기가 지났다', name)
        rec['arms_read'] = [{k: a[k] for k in ARM_PUBLIC} for a in arms_]
        print(f'  {name}: {role} · R_j {disp_rj(rj)} · {law} · c {c or "-"} · 팔 {arm_indices(req)} → {target} attempt_{u["n"]} 의 {iname} '
              f'(기계 {u["machine"]} · 러너 0 회 · 팔 {len(arms_)} 사본 다시 대조)')
        return arms_

    def attempt_set(self):
        """단위 채택 시도 sha 집합 — 연 단위마다 채택 사슬 [대상 · 번호 · 폴더 요약 sha] (차례)."""
        out = []
        for t, u in self.opened.items():
            if target_parts(t)[0] == 'unit':
                out += [[t, k, self.st['results'][k]['folder_sha256']] for k in u['ad']['chain']]
        return sorted(out)

    def expand_hook(self, over):
        self.hook_called = True
        pts = [unit_name(c, law, rr) for (c, law, rr) in over]
        atts = self.attempt_set()
        if self.decision is None:
            raise ExpansionNeeded(points=pts, first=True, attempts=atts)
        d = self.decision
        if d['points'] != pts:
            raise Stop('UNIT_PROVENANCE_MISMATCH', f'끝 합치기가 다시 센 넘침 목록 {pts} ≠ 결정 기록 {d["points"]} — 칼날 보고 (첫 합치기 기계 '
                                                   f'{d.get("machine")!r} · 환경 지문 다른 칸 {_env_diff(d.get("env"), self.env)[:6]} · W0 = 봉인 · Q9 개정 4 Q4)')
        if d['attempts'] != atts:
            diff = [x for x in d['attempts'] if x not in atts] + [x for x in atts if x not in d['attempts']]
            raise Stop('UNIT_PROVENANCE_MISMATCH', f'단위 채택 시도 sha 집합 ≠ 결정 기록 (다른 줄 {diff[:3]}) — 첫 합치기 뒤 단위 시도가 바뀌었다')

    def finish(self):
        """다시 계산이 끝까지 간 뒤 — 결정 기록이 있는데 넘침 없음 = UNIT_PROVENANCE_MISMATCH · 남는 채택 런 = UNIT_EXTRA (요청되지 않은 대상의 채택 시도 ·
        연 대상의 요청되지 않은 런 · 대조가 실패한 요청되지 않은 대상 = 남는지 알 수 없다 = 보수 쪽)."""
        if self.decision is not None and not self.hook_called:
            raise Stop('UNIT_PROVENANCE_MISMATCH', '결정 기록을 받았는데 다시 계산에 넘침이 없다 (끝 합치기 = 첫 합치기와 같은 단위 시도여야)')
        extra = []
        for t, info in sorted(self.tinfo.items()):
            if t in self.opened:
                u = self.opened[t]
                extra += [f'{t}/attempt_{u["n"]}/{nm}' for nm in sorted(u['runs']) if nm not in u['consumed']]
            elif info['problem']:
                extra.append(f'{t} (대조 실패 {info["problem"][0]})')
            elif (info['ad'] or {}).get('effective') is not None:
                extra.append(f'{t}/attempt_{info["ad"]["effective"]}')
        if extra:
            raise Stop('UNIT_EXTRA', f'다시 계산이 끝까지 갔는데 채택된 런이 남았다 ({extra[:4]}{" …" if len(extra) > 4 else ""}) — 요청되지 않은 단위 · 넘침 점 시도 '
                                     f'(Q9 §3-2)')

    def copy_all(self):
        """모든 시도 사본 (요청되지 않은 대상 · 결과 전 · 거부 기록 포함 · 한 항목 = 폴더 하나일 때만 · Q9 §3-2 개정 3)."""
        for t, info in sorted(self.tinfo.items()):
            for k in info['ns']:
                ps = self.found.get(k) or []
                if k not in self.copied and len(ps) == 1:
                    self._copy(t, k, ps[0])

    def units_public(self):
        return {t: {'attempt': u['n'], 'adopted': u['ad']['adopted'], 'chain': list(u['ad']['chain']), 'machine': u['machine'], 'folder': u['rel'],
                    'summary_sha256': u['sha']} for t, u in sorted(self.opened.items())}

    def attempts_public(self):
        return [{'target': self.st['entries'][k]['target'], 'n': k, 'folder': f'{UNITS_DIR}/{target_dir(self.st["entries"][k]["target"])}/{p.name}',
                 'folder_sha256': self.st['results'][k]['folder_sha256']} for k, p in sorted(self.copied.items())]

    def unused_runs(self):
        """요청되지 않은 런 · 대조 결과 (기록만 · 멈춤 아님 · 판정 입력 아님) — 대조가 실패한 요청되지 않은 대상 (check_failed:<멈춤>) · 사본 시도 요약의 런마다
        (채택 시도 = not_requested · 재실행이 대신한 사슬 앞 시도 = replaced_by_resume · 그 밖 = not_adopted) · 팔 sha256."""
        out = []
        for t, info in sorted(self.tinfo.items()):
            if info['problem'] and t not in self.opened:
                out.append({'target': t, 'attempt': None, 'run': None, 'folder': None, 'arms_sha256': [], 'why': f'check_failed:{info["problem"][0]}'})
                continue
            ad, u, kind = info['ad'] or {}, self.opened.get(t), target_parts(t)[0]
            for k in info['ns']:
                p = self.copied.get(k)
                if p is None or not p.is_dir():
                    continue
                su, _sha = read_summary(p, UNIT_SUMMARY[kind])
                for r in (su or {}).get('runs') or []:
                    if not isinstance(r, dict) or (u is not None and k == u['n'] and r.get('name') in u['consumed']):
                        continue
                    why = 'not_requested' if k == ad.get('effective') else ('replaced_by_resume' if k in (ad.get('chain') or []) else 'not_adopted')
                    out.append({'target': t, 'attempt': k, 'run': r.get('name'), 'folder': f'{UNITS_DIR}/{target_dir(t)}/{p.name}/{r.get("outdir")}',
                                'arms_sha256': [x.get('sha256') for x in r.get('arms_read') or [] if isinstance(x, dict)], 'why': why})
        return out


def ledger_bundle(repo, head, dst):
    """원장 git 저장소 사본 (Q9 §3-2 개정 4 R4-07 · 커밋 대조용) — `git bundle create <dst> HEAD` · 그 묶음의 HEAD = 합치기 원장 커밋 → sha256."""
    dst = Path(dst).resolve()
    dst.parent.mkdir(parents=True, exist_ok=True)
    ledger_git(repo, 'bundle', 'create', str(dst), 'HEAD')
    heads = ledger_git(repo, 'bundle', 'list-heads', str(dst)).stdout.decode('ascii', 'replace').split()
    if head not in heads:
        raise Stop('ATTEMPT_LEDGER_MISMATCH', f'원장 사본 묶음의 HEAD ≠ 합치기 원장 커밋 {head[:12]} (합치기 중 원장이 바뀌었다)')
    return sha256_file(dst)


def stage_merge(a, contract):
    """★ 10-27 묶음 C2d (Q9 §3-2 2 · 3 · §3-4 · §4) — 합치기: 원장 (HEAD · 덧붙이기만 · 계획) → 사다리 (채택 사다리 시도 · 예측과 같은 `load_ladders` ·
    관문) → (끝 합치기) 결정 기록 (꼴 · 변이 · 사다리 · 계획 · 원장 조상 · 접두 · 사본) → --merge 시도 폴더 (원장 항목 · 이 변이의 단위 · 넘침 점) → 같은
    판정 함수 (`Predict` + `MergeFetch`) → 상태 PREDICTED · NOT_COMPUTED · STOPPED = `predict_summary.json` (+ merge 칸 · 사본 · 원장 묶음) · 넘침 =
    EXPANSION_NEEDED (`merge_summary.json` · 첫 합치기 = 결정 기록 `expansion.json` · rc 4 · 멈춤 아님 · 판정 입력 아님).  러너는 봉인 원천 (SV 끝 그래프 조립만)
    에만 쓴다 (풀이 없음)."""
    rc_m = machine_missing_rc(a)
    if rc_m is not None:
        return rc_m
    out = Path(a.out)
    try:
        outdir_empty_or_stop(out)
    except Stop as e:
        print_stop(e)
        return 3
    s = summary_base('predict', a)
    s.update({'variant': a.variant, 'kit': a.kit or DBE_KIT, 'runs': [], 'ladders': {}, 'checks': None, 'origin': None,
              'env_scrubbed': [], 'after_main': None, 'sv_cf': None, 'bed': None, 'sv_graph_source': None})
    mg = {'schema': MERGE_SCHEMA, 'ledger': None, 'expansion': None, 'units': {}, 'attempts': [], 'unused_runs': [], 'missing_points': None}
    s['merge'] = mg
    fetch, exp, repo, head = None, None, None, None
    try:
        if (a.kit or DBE_KIT) != DBE_KIT:
            raise Stop('NOT_REGISTERED', f'--kit {a.kit} (등록 {DBE_KIT})')
        env_forbidden_or_stop()
        repo = Path(a.ledger)
        why = ledger_repo_problem(repo)
        if why:
            raise Stop('ATTEMPT_LEDGER_MISMATCH', why)
        head, raw = ledger_now(repo)
        why = ledger_history_problem(repo, head)
        if why:
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'원장 역사: {why}')
        st = ledger_parse(raw)
        mg['ledger'] = {'path': str(repo.resolve()), 'commit': head, 'sha256': hashlib.sha256(raw).hexdigest(), 'bundle': None, 'bundle_sha256': None}
        ledger_inputs_check(a.ladders, repo, head, st, want_prefix='ladder:')
        sid_reg = {}
        lads, plan, plan_sha, code, s0rec, lad_after, s0reps = load_ladders(a.ladders, a.variant, a.registration, contract, sid_reg,
                                                                            now_code=s['code'])
        s['ladders'] = {k: {kk: v[kk] for kk in ('dir', 'summary_sha256', 'variant', 'R_j0', 'R_j_lo', 'R_j_hi')} for k, v in lads.items()}
        s['plan'] = {'sha256': plan_sha, 'content': plan}
        s['s0_plan'] = s0rec
        s['s0_reports'] = s0reps
        s['registration'] = check_plan_registered(plan_sha, a.registration)
        plan_doc_or_stop(a.registration, plan)
        exec_check_or_stop(plan, a.max_hours, a.machine, s['code'])
        if plan_sha != st['header']['plan_sha256']:
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'원장 머리의 계획 {st["header"]["plan_sha256"][:12]} ≠ 사다리 계획 {plan_sha[:12]}')
        if a.variant is not None:
            s['after_main'] = check_after_main(a.after_main, plan_sha, s0rec['sha256'], s['code'])
            if a.variant != 'SVORDER' and lad_after != s['after_main']:
                raise Stop('MAIN_NOT_DONE', '변이 사다리가 묶인 주 예측 ≠ --after-main (같은 주 판정 단계 뒤여야)')
        scope = plan['sv_cf_scope'] if a.variant is None else None
        s['sv_cf'] = {'scope': scope, 'threshold': (plan['sv_cf_threshold'] if a.variant is None else None)}
        for p in (Path(a.root) / SBE_KIT, Path(a.root) / DBE_KIT, Path(a.runner)):
            if not p.exists():
                raise Stop('KIT_MISSING', f'{p}')
        s['bed'] = bed_problem(s0reps, a.root, (SBE_KIT, DBE_KIT))
        dec, dsha = None, None
        if a.expand:                                       # 끝 합치기 — 결정 기록 (구조 칸 대조 = 다시 계산의 넘침에서 · 여기 = 꼴 · 출처 · 원장 접두)
            dec, dsha = read_expansion(a.expand)
            if dec['variant'] != a.variant or dec['plan_sha256'] != plan_sha \
                    or dec['ladders'] != {law: s['ladders'][law]['summary_sha256'] for law in LAWS}:
                raise Stop('UNIT_PROVENANCE_MISMATCH', '결정 기록의 변이 · 계획 · 사다리 요약 sha ≠ 이 합치기')
            c1 = dec['ledger']['commit']
            if not ledger_is_ancestor(repo, c1, head):
                raise Stop('ATTEMPT_LEDGER_MISMATCH', f'결정 기록의 원장 커밋 {c1[:12]} 이 이 원장 HEAD 의 조상이 아니다 (첫 · 끝 합치기 원장 = 바이트 접두 · '
                                                      f'Q9 §3-5)')
            b1 = ledger_blob(repo, c1)
            if hashlib.sha256(b1).hexdigest() != dec['ledger']['sha256'] or not raw.startswith(b1):
                raise Stop('ATTEMPT_LEDGER_MISMATCH', '결정 기록의 원장 sha ≠ 그 커밋 원장 · 이 원장의 바이트 접두가 아니다 (항목 줄 지우기 · 바꾸기 · Q9 §3-5)')
            out.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(a.expand, out / EXPANSION_FILE)
            if sha256_file(out / EXPANSION_FILE) != dsha:
                raise Stop('UNIT_PROVENANCE_MISMATCH', '결정 기록 사본 ≠ 읽은 결정 기록 (읽는 사이 바뀌었다)')
            mg['expansion'] = {'path': str(Path(a.expand).resolve()), 'sha256': dsha, 'copy': EXPANSION_FILE}
        found = collect_attempts(a.merge)
        for k, ps in sorted(found.items()):
            e = st['entries'].get(k)
            if e is None:
                raise Stop('ATTEMPT_LEDGER_MISMATCH', f'원장에 없는 시도 폴더 {[str(p) for p in ps][:2]} (항목 {k})')
            tp = target_parts(e['target'])
            if tp is None or tp[1] != a.variant:
                raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{ps[0]}: 대상 {e["target"]} 는 이 합치기 (변이 {a.variant!r}) 의 단위 · 넘침 점이 아니다 (합칠 대상이 아님)')
        out.mkdir(parents=True, exist_ok=True)
        deadline = time.time() + a.max_hours * 3600.0
        gsrc = RunnerGraphSource(a.runner, a.root, out / GRAPH_SRC_DIR, deadline=deadline)
        s['env_scrubbed'] = sorted(k for k in os.environ if ENV_SCRUB_RE.match(k) or k in ENV_SCRUB_NAMES)
        fetch = MergeFetch(repo, head, raw, st, found, lads, a.variant, plan, contract, sid_reg, s0_grid_seed(s0reps), s0_census_seed(s0reps), gsrc, out,
                           merge_want(s), (s['code'] or {}).get('env'), dec, dsha)
        pr = Predict(fetch.run, lads, a.variant, sv_scope=scope, expand_hook=fetch.expand_hook)
        print(f'합치기{" · 변이 " + a.variant if a.variant else ""}{" · 끝 (결정 기록)" if dec else ""} — 원장 {head[:12]} · 시도 폴더 {len(found)} · '
              f'같은 판정 함수 · 같은 요청 순서 (값은 봉인 · 러너 = 봉인 원천 조립만)')
        try:
            try:
                pr.run()
                fetch.finish()
                s['status'] = 'PREDICTED'
            finally:
                s['checks'], s['origin'], s['runs'] = pr.checks, pr.origin, fetch.records
                s['sv_graph_source'] = gsrc.public()
        except ExpansionNeeded as x:
            exp = x
            s['status'] = 'EXPANSION_NEEDED'
        except Stop as e:
            s['status'] = e.code if e.code in PREDICT_OUTCOMES else 'STOPPED'
            raise
    except Stop as e:
        s['stop'] = e.record()
        if s['status'] is None:
            s['status'] = 'STOPPED'
        print_stop(e)
    out.mkdir(parents=True, exist_ok=True)
    try:
        if fetch is not None:                              # 모든 시도 사본 · 기록 (멈춘 합치기도 · 판정 · 다시 판정이 같은 대조를 다시 한다)
            fetch.copy_all()
            mg['units'], mg['attempts'], mg['unused_runs'] = fetch.units_public(), fetch.attempts_public(), fetch.unused_runs()
        if mg['ledger'] is not None:
            mg['ledger']['bundle_sha256'] = ledger_bundle(repo, head, out / LEDGER_COPY_DIR / LEDGER_BUNDLE)
            mg['ledger']['bundle'] = f'{LEDGER_COPY_DIR}/{LEDGER_BUNDLE}'
    except Stop as e:                                     # 사본 · 묶음을 못 만든 합치기 = 멈춤 (판정 입력 아님)
        if s['stop'] is None:
            s['stop'], s['status'] = e.record(), 'STOPPED'
            exp = None
        print_stop(e)
    if exp is not None:
        mg['missing_points'] = exp.missing if not exp.first else None
        if exp.first:
            dec_new = {'schema': EXPANSION_SCHEMA, 'variant': a.variant, 'points': exp.points, 'overflow': [list(unit_parse(p)) for p in exp.points],
                       'attempts': exp.attempts, 'ledger': {'path': mg['ledger']['path'], 'commit': head, 'sha256': mg['ledger']['sha256']},
                       'ladders': {law: s['ladders'][law]['summary_sha256'] for law in LAWS}, 'plan_sha256': s['plan']['sha256'],
                       'machine': a.machine, 'env': (s['code'] or {}).get('env'), 'utc': _utc()}
            write_json(out / EXPANSION_FILE, dec_new)
            mg['expansion'] = {'path': str((out / EXPANSION_FILE).resolve()), 'sha256': sha256_file(out / EXPANSION_FILE), 'copy': EXPANSION_FILE}
        s['stage'] = 'merge'
        write_json(out / MERGE_SUMMARY, s)
        what = (f'넘침 점 {len(exp.points)} — 결정 기록 {out / EXPANSION_FILE} 을 인용한 --point 시도 뒤 끝 합치기 (--expand)' if exp.first else
                f'빠진 넘침 점 {exp.missing} — 그 점 시도 뒤 끝 합치기 다시')
        print(f'EXPANSION_NEEDED — {what} (멈춤 아님 · 판정 입력 아님)')
        print(f'요약 → {out / MERGE_SUMMARY}')
        return RC_EXPANSION_NEEDED
    write_json(out / 'predict_summary.json', s)
    if s['status'] == 'PREDICTED':
        print(f'합친 예측 = PREDICTED · 런 {len(s["runs"])} · 단위 · 넘침 점 {len(mg["units"])} · 남은 런 기록 {len(mg["unused_runs"])}')
    else:
        print(f'합친 예측 = {s["status"]}' + (f' (사유 {(s.get("stop") or {}).get("reason")})' if (s.get('stop') or {}).get('reason') else ''))
    print(f'요약 → {out / "predict_summary.json"}')
    return 0 if s['status'] == 'PREDICTED' else 3


# ═════════════════════════ (5) 판정 단계 ═════════════════════════
def _replay_ladder(d, s, contract, sid_reg, cert_reg, graph_src=None):
    plan = s['plan']['content']
    rp = Replay(d, s, plan, contract, sid_reg, cert_reg, graph_src=graph_src)
    lad = Ladder(lambda role, rj, arms: rp.run(SBE_KIT, role, s['law'], LADDER_C, rj, arms), max_points=ladder_cap(plan),
                 ratio_max=plan['calib_rj_ratio_max'])
    status, stop, noop = 'CALIBRATED', None, None
    try:
        lad.run()
        lad.origin()
        #  ★ 10-27 묶음 C2a (Q9 §7 · R4-06 (c)) — 사다리 끝 no-op 런을 원 팔에서 다시 읽어 같은 대조 (기록 = 남김없이 읽는다 · rp.done)
        noop = ladder_noop(lambda role, rj, arms: rp.run(SBE_KIT, role, s['law'], NOOP_C, rj, arms), lad, s['law'])
    except Stop as e:
        if e.code not in REGISTERED_OUTCOMES:
            raise
        status, stop = e.code, e.record()                     # ★ 4판 (Q1) — 등록 결과의 사유 (멈춤 기록 · 원 팔에서 다시 계산)
    rp.done()
    if status != s.get('status') or lad.st != s.get('ladder') or lad.flags != s.get('flags'):
        diff = [k for k in set(lad.st) | set(s.get('ladder') or {}) if lad.st.get(k) != (s.get('ladder') or {}).get(k)]
        raise Stop('REPLAY_MISMATCH', f'{Path(d).name}: 원 팔에서 다시 계산한 사다리 ≠ 요약 (상태 {status} ↔ {s.get("status")} · 칸 {sorted(diff)})')
    if (noop is None) != (s.get('noop') is None) or (noop is not None and (noop_record_problem(s.get('noop'), s['law'], lad.st['R_j0'])
                                                                         or noop_key(noop) != noop_key(s['noop']))):
        raise Stop('REPLAY_MISMATCH', f'{Path(d).name}: 원 팔에서 다시 계산한 사다리 끝 no-op ({noop_key(noop) if noop else None}) ≠ 요약 기록 '
                                      f'({noop_key(s["noop"]) if isinstance(s.get("noop"), dict) else s.get("noop")})')
    return {'status': status, 'stop': stop, 'st': lad.st, 'sealed': lad.sealed, 'flags': lad.flags, 'pts': lad.pts, 'noop': noop}


def _replay_predict(d, s, lads, contract, sid_reg, cert_reg, graph_src=None):
    """예측 단계 다시 계산 → (Predict, 상태 PREDICTED | NOT_COMPUTED, 멈춤 기록 | None) · ★ 4판 (Q1) — NOT_COMPUTED (단락 · 증서 실패) = 등록
    결과 (사다리 `_replay_ladder` 와 같은 꼴) · 다시 계산한 상태 · 검사 · origin 결정 ≠ 요약 = REPLAY_MISMATCH.
    ★ 10-26 B″ (Q1 (가)) — graph_src = 판정의 봉인 원천 (SV 모서리 런마다 조립만 런을 **다시** 돌린다 · 단계 요약의 `sv_graph` 를 믿지 않는다 —
    다시 계산한 `sv_graph` 가 요약과 다르면 아래 REPLAY_MISMATCH (그 런의 SV 판정 · 상태가 갈린다))."""
    rp = Replay(d, s, s['plan']['content'], contract, sid_reg, cert_reg, graph_src=graph_src)
    pr = Predict(rp.run, lads, s.get('variant'), sv_scope=(s.get('sv_cf') or {}).get('scope'))
    status, stop = 'PREDICTED', None
    try:
        pr.run()
    except Stop as e:
        if e.code not in PREDICT_OUTCOMES:
            raise
        status, stop = e.code, e.record()
    rp.done()
    if status != s.get('status') or pr.checks != s.get('checks') or pr.origin != s.get('origin'):
        raise Stop('REPLAY_MISMATCH', f'{Path(d).name}: 원 팔에서 다시 계산한 예측 (상태 {status} ↔ {s.get("status")}) · 검사 · origin 결정 '
                                      f'≠ 요약')
    return pr, status, stop


def _why(stage, law, variant, stop):
    """★ 4판 (Q1) — 판정 기록의 사유 한 줄 (§5-5b NOT_COMPUTED · CALIB_* 행 '사유 (상태 · 멈춤 코드) 보고') — 멈춤 기록에서 (σ 를 가린 원인 칸)."""
    st = stop or {}
    return {'stage': stage, 'law': law, 'variant': variant, 'code': st.get('code'), 'reason': st.get('reason'), 'run': st.get('run'),
            'cause': st.get('cause')}


def judge_set(statuses, vals):
    """같은 판정 함수 (§5-6 · Codex RCA-09) — 법칙별 사다리 상태 + 예측 값 (S/cm · 확장 실수) → 판정 dict.  주 판정 · 감도 변이가 이것 하나.
    ★ 4판 (Q1 · §5-0 ①) — 사다리 둘이 보정됐는데 vals = None = 예측 단계가 NOT_COMPUTED (등록 결과) → 판정 NOT_COMPUTED.
    ★ 4판 (Q2-1 · §3-2c PRE-design-08) — 두 법칙 이름이 다르면 하나라도 NOT_COMPUTED 면 NOT_COMPUTED (상태 먼저 — 기록이 덜 된 법칙이 있으면
    등록된 결과 이름을 붙이지 않는다 · §5-0 ①) · 아니면 등록 나열 순서 (CALIB_ORDER) 의 첫 CALIB_* · 법칙별 이름은 늘 보고 (판정 기록 calib)."""
    bad = [statuses[law] for law in LAWS if statuses[law] != 'CALIBRATED']
    if bad:
        if 'NOT_COMPUTED' in bad:
            return {'verdict': 'NOT_COMPUTED', 'state': 'calib'}
        return {'verdict': min(bad, key=CALIB_ORDER.index), 'state': 'calib'}
    if vals is None:
        return {'verdict': 'NOT_COMPUTED', 'state': 'calib'}
    return judge({k: v * 1e3 for k, v in vals.items()})


def _end_shift(a, b):
    return [abs(ln_diff(a[i], b[i])) for i in (0, 1)]


def variant_flag(V, vJ, J, vflags):
    """★ 4판 (Q2-5 · 등록 R 4판 §5-6 PRE-design-17 ② ③ ④ · R4-Q8) — 변이 V 의 판정 vJ (같은 판정 함수) ↔ 주 판정 J · 변이 자신의 표지 vflags →
    (표지 | None, 이름 비교 (True 다름 · False 같음 · None 비교 안 함), 사유 | None).  순서 = ③ → ② → ④:
    ③ 변이 판정 NOT_COMPUTED (풀이 · 증서 실패 · 단락 · 멈춤) → <V>_UNCHECKED (결과가 없다 · 이름 비교 안 함 — 3판 = 이름 다름 → _SENSITIVE) ·
    ② 이름 ≠ 주 이름 → <V>_SENSITIVE (CALIB_* 도 결과 이름이라 비교한다) · ④ 이름이 같아도 변이 자신에게 CALIB_ORIGIN_SENSITIVE → <V>_UNCHECKED
    (둔감을 인증하지 않는다) · ⑤ 변이 자신의 표지는 주 표지 목록에 옮기지 않는다 (이 표지로만 · 변이 기록에 늘 보고)."""
    if vJ['verdict'] == 'NOT_COMPUTED':
        return (f'{V}_UNCHECKED', None,
                '변이 판정 NOT_COMPUTED (풀이 · 증서 실패 · 단락 · 멈춤 — 결과가 없다 · 이름 비교 안 함 · §5-6 ③)')
    if vJ['verdict'] != J['verdict']:
        return f'{V}_SENSITIVE', True, f'변이 판정 이름 {vJ["verdict"]} ≠ 주 판정 이름 {J["verdict"]} (같은 판정 함수 · §5-6 ②)'
    if 'CALIB_ORIGIN_SENSITIVE' in (vflags or ()):
        return (f'{V}_UNCHECKED', False,
                '변이 자신의 차단 표지 CALIB_ORIGIN_SENSITIVE (판정 이름은 주와 같다 · 둔감을 인증하지 않는다 · §5-6 ④)')
    return None, False, None


#: ★ 4판 (Q2-4 · §5-5b "표지마다 사유") — 주 판정 표지의 사유 (값 = 판정 결과에만 · 공개 칸에 σ · 비를 싣지 않는다)
WHY_ORIGIN_SENSITIVE = ('세 값 (주 사다리 R_j,0 의 arm 0 · 1 · 2) 의 ln(max/min) > 0.02 — 8 팔 평균 보고 · R_j,0 = arm 0 그대로 (§3-3 · '
                        '값 = 판정 결과에만)')
WHY_NOT_RUN = '안 돌림'


def sv_corner_label(det, key):
    """★ 10-23 (Codex 재검토 RCA2-06 F6 · author 10-23 ratified Q1-Q8) 사유의 모서리 이름 — 그 모서리의 비를 싣지 않는 상태 (위 끝 구조화 실패
    `unsplit_census_mismatch` · 미수렴 · …) 를 이름 그대로 괄호에 붙인다 (구조화 실패를 끝-끝 보존 · 같은 상태 = 한 번 · 비 값은 붙이지 않는다) ·
    그런 상태가 없으면 (기록 없음 · 비를 싣는 상태인데 증서 구간을 못 정함) 모서리 이름만 (옛 글자)."""
    c = (det.get('corners') or {}).get(key) or {}
    sts = [s for s in (c.get('status'), c.get('status_hi')) if isinstance(s, str) and s and s not in SVCF.RATIO_STATUSES]
    return f'{key} ({SENTENCE_JOIN.join(dict.fromkeys(sts))})' if sts else key


def sv_reasons(flags, det):
    """§5-5b 사유 — SV 표지 (§5-6 SV 행) → {표지: 사유} (대조 비 · 문턱 · 모서리 · 비 값 = 판정 결과에만).  ★ 10-23 (RCA2-06 F6) 못 읽음 ·
    진단 모서리 이름 = `sv_corner_label` (비를 싣지 않는 상태 이름을 붙인다)."""
    out = {}
    if 'SV_DEPENDENT' in flags:
        out['SV_DEPENDENT'] = (f'대조 비 > 문턱 {det.get("threshold")!r} (증서 구간 아래 끝 · nominal 아님) — 모서리 '
                               f'{SENTENCE_JOIN.join(det.get("dependent") or [])} (범위 {det.get("scope")} · 비 = 판정 결과에만 · §5-6 SV 행)')
    if 'SV_UNCHECKED' in flags:
        parts = []
        if det.get('threshold') is None:
            parts.append('문턱 없음 (계획 sv_cf_threshold null)')
        if det.get('unreadable'):
            parts.append(f'대조 비를 못 읽음 — 모서리 {SENTENCE_JOIN.join(sv_corner_label(det, k) for k in det["unreadable"])}')
        if det.get('uncertified'):                      # ★ 10-23 (RCA2-04 · Q1 (가)) — 증서 없는 런의 진단 기록 = 판정 입력 아님
            parts.append(f'증서 없는 진단 기록 (판정 입력 아님) — 모서리 '
                         f'{SENTENCE_JOIN.join(sv_corner_label(det, k) for k in det["uncertified"])}')
        if det.get('graph_unverified'):                 # ★ 10-26 묶음 B6 (RR1-01) — 끝 증서의 가중 그래프 귀속 미확인 = 판정 입력 아님
            parts.append('끝 증서의 가중 그래프 귀속 미확인 (SV 기록 밖 봉인 원천 대조 없음 · 10-26 RR1-01 · 판정 입력 아님) — 모서리 '
                         + SENTENCE_JOIN.join(f"{k} ({SV_GRAPH_WHY.get(((det.get('corners') or {}).get(k) or {}).get('graph'), '?')})"
                                              for k in det['graph_unverified']))
        if det.get('straddle'):                         # ★ 10-22 (Q1 (다)) — 괄호가 문턱에 걸침 (비 값 = 판정 결과에만) · ★ 10-23 증서 구간
            parts.append(f'대조 비 증서 구간이 문턱에 걸침 (아래 끝 ≤ 문턱 < 위 끝 · 못 가른 덩어리 · 증서 폭) — 모서리 '
                         f'{SENTENCE_JOIN.join(det["straddle"])}')
        if not det.get('corners'):
            parts.append(f'범위 {det.get("scope")} 안 모서리 기록 없음')
        out['SV_UNCHECKED'] = SENTENCE_JOIN.join(parts) + ' (§5-6 SV 행)'
    return out


def assemble(main, variants, sv):
    """판정 조립 (순수 함수 · 시험이 직접 부른다) → (공개 칸, 결과 칸).
    main = {'statuses', 'vals' (S/cm) | None, 'flags'} · variants = {V: None (안 돌림) | {'statuses', 'vals', 'flags'}} ·
    sv = (표지, 세부) | None (주 예측이 없을 때).
    ★ 4판 — 변이 표지 = `variant_flag` (Q2-5) · 문장 = 결정표 (Q2-4 · `decide_sentence` · 감도 미완료 = 네 변이 중 하나라도 안 돌림 (⑰) ·
    판정 없음 (calib) 이면 None = 해당 없음) · 공개 `blocking_reasons` = 차단 표지마다 사유 (§5-5b)."""
    J = judge_set(main['statuses'], main['vals'])
    flags = list(main.get('flags') or [])
    why = {'CALIB_ORIGIN_SENSITIVE': WHY_ORIGIN_SENSITIVE} if 'CALIB_ORIGIN_SENSITIVE' in flags else {}
    pub_v, res_v = {}, {}
    sens_incomplete = None
    if J['state'] != 'calib':
        if sv is not None:
            flags += sv[0]
            why.update(sv_reasons(sv[0], sv[1] or {}))
        r0 = {k: v for k, v in main['vals'].items() if k[2] == 'R_j0'}
        J['main_R0_only'] = judge({k: v * 1e3 for k, v in r0.items()})      # 중앙 네 점 = 보조 · 보고만 (§5-6 · §10-2 ⑧)
        sens_incomplete = False
        for V in VARIANTS:
            vr = variants.get(V)
            if vr is None:
                pub_v[V] = {'checked': False, 'verdict': None, 'grade_changed': None, 'flag': f'{V}_UNCHECKED'}
                flags.append(f'{V}_UNCHECKED')
                why[f'{V}_UNCHECKED'] = WHY_NOT_RUN
                sens_incomplete = True                          # ⑰ — 감도 변이를 다 돌리기 전
                continue
            vJ = judge_set(vr['statuses'], vr['vals'])
            vf = sorted(set(vr.get('flags') or []))
            flag, changed, reason = variant_flag(V, vJ, J, vf)
            pub_v[V] = {'checked': True, 'verdict': vJ['verdict'], 'grade_changed': changed, 'flags': vf, 'flag': flag}
            if flag:
                flags.append(flag)
                why[flag] = reason
            ent = {'verdict': vJ['verdict'], 'judge': vJ}
            if vJ['state'] != 'calib':
                sh = _end_shift(vJ['interval_mScm'], J['interval_mScm'])
                ent.update(end_shift_log=sh, end_shift_exceeds_0p1G0=max(sh) > SENS_SHIFT_FRAC_G0 * G0)
                ent['variant_R0_only'] = judge({k: v * 1e3 for k, v in vr['vals'].items() if k[2] == 'R_j0'})
            res_v[V] = ent
    flags = sorted(set(flags))
    blocking = blocking_of(flags)
    sentence = decide_sentence(J['state'], J['verdict'], blocking, sens_incomplete=bool(sens_incomplete))
    pub = {'verdict': J['verdict'], 'state': J['state'], 'flags': flags, 'blocking_flags': blocking,
           'blocking_reasons': {f: why.get(f) for f in blocking}, 'sensitivity_incomplete': sens_incomplete,
           'sentence_allowed': J['verdict'] == 'PASS_INFORMATIVE' and not blocking, 'sentence': sentence,
           'variants': pub_v}
    return pub, {'judge': J, 'variants': res_v}


#: 판정 조립 (`assemble`) 의 공개 칸 → verdict.json (★ 4판 — 차단 표지 사유 · 감도 미완료 칸을 더했다)
PUB_FROM_ASSEMBLE = ('verdict', 'state', 'flags', 'blocking_flags', 'blocking_reasons', 'sensitivity_incomplete', 'sentence_allowed',
                     'sentence')


def default_graph_src(root, out=None):
    """★ 10-26 B″ (1저자 Q1 (가)) 판정 · 다시 판정의 봉인 원천 — 생산 기본 (`SV_GRAPH_SOURCE` = `RUNNER_GRAPH_SOURCE`) 이고 킷 뿌리가 있으면 이 사슬
    폴더의 러너 (`HERE / RUNNER_NAME` · 단계 코드 대조가 묶는 그 파일 · ★ 10-25 Q2 (가) ③) 로 `RunnerGraphSource` (시간 상한 없음 · out None = 임시
    폴더) · 아니면 None (시험이 넣은 함수 · None 원천 = `sv_graph_state` 가 모듈 값을 그대로 쓴다)."""
    if isinstance(SV_GRAPH_SOURCE, str) and SV_GRAPH_SOURCE == RUNNER_GRAPH_SOURCE and root:
        return RunnerGraphSource(HERE / RUNNER_NAME, root, out)
    return None


def verdict_compute(dirs, reg_path, contract, root, graph_src=None, ledger=None):
    """판정 계산기 (§5 · 설계 §7) — 원 팔 JSON 전부에서.  → (공개 dict, 결과 dict | None).  입력 계약 실패 = Stop.  ★ 10-25 묶음 B
    (RCA2-03) — root = 킷 뿌리 (SBE · DBE 킷을 S0 와 같은 발견 함수로 다시 해시해 단계 기록의 S0 원 입력과 대조 · 경로 = 대조 밖).
    ★ 10-26 B″ (1저자 Q1 (가)) — graph_src = 판정의 봉인 원천 (None = `default_graph_src(root)` · 임시 폴더) · SV 모서리 런마다 조립만 런을 **다시**
    돌린다 (단계 요약의 `sv_graph` · 원천 기록을 믿지 않는다 — 다시 읽은 원 팔 · 다시 조립한 지문으로 SV 판정).
    ★ 10-27 묶음 C1b — ledger = {'path', 'commit', 'attempt_dirs'} (원장 판정 · 입력 = 그 원장의 채택 시도만 · `ledger_verdict_check` · 판정 칸 ledger ·
    뒤에서 멈춰도 멈춤 기록에 원장 칸을 싣는다) · None = 원장 없는 판정 (옛 꼴 · ledger 칸 null)."""
    lpub = None
    if ledger is None:                                        # ★ 10-27 묶음 C2d — 합친 예측 = 원장 판정만 (합치기의 원장 대조를 판정이 다시 한다 · Q9 §3-4)
        for d in dirs:
            sm, _sha = read_summary(Path(d), 'predict_summary.json')
            if isinstance(sm, dict) and sm.get('merge') is not None:
                raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{Path(d).name}: 합친 예측 (단위 합치기) = 원장 판정만 (--ledger <그 원장> · 합치기의 원장 · 사본 대조를 '
                                                      f'다시 한다 · Q9 §3-4)')
    if ledger is not None:
        if not ledger.get('commit'):
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'원장 {ledger.get("path")} 의 HEAD 를 못 읽는다')
        lpub = ledger_verdict_check(dirs, ledger['path'], ledger.get('attempt_dirs') or (), ledger['commit'])
    try:
        pub, res = _verdict_compute(dirs, reg_path, contract, root, graph_src)
    except Stop as e:
        e.ledger = lpub
        raise
    pub['ledger'] = lpub
    return pub, res


def _verdict_compute(dirs, reg_path, contract, root, graph_src):
    if graph_src is None:
        graph_src = default_graph_src(root)
    pub = {'tool': TOOL, 'schema': SCHEMA, 'stage': 'verdict', 'verdict': None, 'state': None, 'stop': None, 'flags': [],
           'blocking_flags': [], 'blocking_reasons': {}, 'sensitivity_incomplete': None, 'qualifiers': list(QUALIFIERS),
           'report_category': {REPORT_CATEGORY: list(ASSUMED_UNVALIDATED)},
           'verdict_note': VERDICT_NOTE, 'sentence_allowed': False, 'sentence': None, 'calib': {}, 'variants': {},
           'inputs': [], 'arms': [], 'registration': None, 'grid_sentence': GRID_SENTENCE, 'reasons': [], 'bed': None, 'ledger': None}
    stages, seen = [], set()
    for d in dirs:
        rd = Path(d).resolve()
        if rd in seen:
            raise Stop('DUPLICATE_RUN', f'같은 입력 폴더 두 번 {rd}')
        seen.add(rd)
        got = [(n, *read_summary(rd, n)) for n in ('ladder_summary.json', 'predict_summary.json')]
        got = [(n, s, h) for n, s, h in got if s is not None]
        if len(got) != 1:
            raise Stop('INPUT_NOT_STAGE', f'{rd}: 단계 요약 {len(got)} 개 (1 이어야)')
        _n, s, h = got[0]
        if s.get('tool') != TOOL or s.get('schema') != SCHEMA:
            raise Stop('INPUT_NOT_STAGE', f'{rd}: 이 사슬 (3판) 의 요약이 아니다')
        stages.append((rd, s, h))
    stages.sort(key=lambda x: (x[1].get('variant') or '', x[1].get('stage'), x[1].get('law') or '', str(x[0])))
    plan_hash, reg_sha = registration_plan_hash(reg_path)
    s0_hash, _reg = registration_s0_hash(reg_path)
    pub['registration'] = {'path': str(Path(reg_path).resolve()), 'sha256': reg_sha, 'plan_hash': plan_hash, 's0_plan_hash': s0_hash}
    code0 = None
    plan = None
    s0r0, s0r_first = None, True
    for rd, s, h in stages:
        pub['inputs'].append({'dir': str(rd), 'stage': s.get('stage'), 'law': s.get('law'), 'variant': s.get('variant'),
                              'status': s.get('status'), 'summary_sha256': h})
        if stopped_stage_rejects_verdict(s):                 # ★ RI — 주 판정 단계만 (감도 변이 단계 = §5-6 ③ · 아래 입력 검사는 그대로)
            raise Stop('INPUT_STAGE_STOPPED', f'{rd.name}: {(s.get("stop") or {}).get("code")} — 멈춘 주 판정 단계는 판정 입력이 아니다')
        if (s.get('plan') or {}).get('sha256') != plan_hash:
            raise Stop('PLAN_HASH_MISMATCH', f'{rd.name}: 계획 sha256 ≠ 등록 §2-1 개정값')
        plan = plan_record_or_stop((s.get('plan') or {}).get('content'), rd.name)   # ★ 10-27 묶음 C1a — 기록 계획 꼴
        recheck_s0_record(s.get('s0_plan'), reg_path, plan)
        require_plan_numbers(plan)
        #  ★ 10-27 묶음 C1a (C6 #30 · Q9 개정 4 Q3 · C6 #15) — 등록의 계획 숫자 블록 = 그 계획 · 단계 환경 같음 단위 = 계획 봉인 판 (코드 키 대조 앞 ·
        #    단계끼리 대조가 사유를 덮지 않게) · 단계 · 런 기록의 기계 = 허용 목록 · 런 기계 = 단계 기계
        try:
            plan_doc_or_stop(reg_path, plan)
        except Stop as e:
            raise Stop(e.code, f'{rd.name}: {e.cause}')
        why = env_seal_problem(s.get('code'), plan)
        if why:
            raise Stop('CODE_PIN_MISMATCH', f'{rd.name}: {why}')
        why = stage_machine_problem(s, plan)
        if why:
            raise Stop('MACHINE_NOT_ALLOWED', f'{rd.name}: {why}')
        #  ★ PF2 D (10-22 · PRE2-design-02 · 탐침 C) — 단계 코드 = HEAD + 코드 파일 지문 (`code_key` · 옛 = HEAD · 러너 HEAD · 경로) · 단계마다
        #    dirty 기록 = 멈춤 · 첫 단계 ↔ 지금 사슬 쪽 (dirty · HEAD · 사슬 폴더 지문 · `code_verdict_problem`) · 단계끼리 같은 키
        c = s.get('code') if isinstance(s.get('code'), dict) else {}
        why = code_dirty_problem(c)
        if why:
            raise Stop('CODE_PIN_MISMATCH', f'{rd.name}: {why}')
        key = code_key(c)
        if code0 is None:
            code0, c0 = key, c
            why = code_verdict_problem(c, rd.name)
            if why:
                raise Stop('CODE_PIN_MISMATCH', why)
        elif key != code0:
            raise Stop('CODE_PIN_MISMATCH', f'{rd.name}: 코드 (HEAD · 저장소 상대 경로 · 코드 파일 지문 · 러너 · 환경 지문) ≠ 다른 판정 입력 '
                                            f'단계 ({", ".join(code_key_diff(c, c0))})')
        #  ★ PF2 B (10-22 · Q2) · D — 단계마다 기록한 S0 단계 2 봉인 = 등록 계획 · S0 계획 · 단계 1 꼴 · 두 보고 지문 = 이 단계 코드 (같은 함수) ·
        #    단계끼리 같은 기록
        got = s0_reports_problem(s.get('s0_reports'), plan_hash, s0_hash, c.get('files'), c.get('runner_files'), plan=plan)
        if got:
            raise Stop(got[0], f'{rd.name}: {got[1]}')
        if not s0r_first and s0_records_key(s.get('s0_reports')) != s0_records_key(s0r0):   # ★ 10-25 묶음 B — 경로 = 대조 밖
            raise Stop('S0_REPORT_MISMATCH', f'{rd.name}: S0 단계 보고 기록 ≠ 다른 판정 입력 단계의 기록 (경로 뺀 칸)')
        s0r_first, s0r0 = False, s.get('s0_reports')
        for r in s.get('runs') or []:
            for x in r.get('arms_read') or []:
                pub['arms'].append({'path': str(rd / r['outdir'] / x['file']), 'sha256': x['sha256']})
    #  ★ 10-25 묶음 B (RCA2-03 · Q3 (가)) — 판정 때 킷 다시 해시 (SBE · DBE · 판정 기계의 자기 사본) = 단계 기록의 S0 원 입력 · 설정 (단계끼리 같은
    #    기록이어도 킷과 대조 · 기록만 같게 손댄 꼴을 잡는다) · 공개 칸 = 경로 뺀 지문
    pub['bed'] = bed_problem(s0r0, root, (SBE_KIT, DBE_KIT))
    lad_in, pred_in = {}, {}
    for rd, s, h in stages:
        k = (s.get('variant'), s.get('law')) if s.get('stage') == 'ladder' else s.get('variant')
        tgt = lad_in if s.get('stage') == 'ladder' else pred_in
        if k in tgt:
            raise Stop('DUPLICATE_RUN', f'같은 단계 두 번 {k} ({tgt[k][0].name} · {rd.name})')
        tgt[k] = (rd, s, h)
    sid_reg, cert_reg = {}, {}
    res = {'reference': {'exp_dbe_mScm': EXP_DBE_MS, 'cur_gen_dbe_mScm': CUR_GEN_DBE_MS, 'cur_gen_sigma_star_dbe_S_cm': CUR_GEN_SIGMA_STAR_DBE,
                         'exp_ratio_dbe_sbe': EXP_RATIO, 'G0': G0}, 'ladders': {}, 'variants': {}}

    def ladders_of(variant):
        out = {}
        for law in LAWS:
            if (variant, law) not in lad_in:
                return None
            rd, s, h = lad_in[(variant, law)]
            #  ★ RI (§5-6 ③) — 멈춘 감도 변이 사다리 = 그 법칙 NOT_COMPUTED (다시 계산 없음 · 표지 없음) → 변이 판정 NOT_COMPUTED → <V>_UNCHECKED
            out[law] = (rd, s, h, ({'status': 'NOT_COMPUTED', 'stop': s.get('stop'), 'st': None, 'sealed': None, 'flags': [], 'pts': None}
                                   if variant_stage_stopped(s) else _replay_ladder(rd, s, contract, sid_reg, cert_reg,
                                                                                   graph_src=graph_src)))
        return out
    main_l = ladders_of(None)
    if main_l is None:
        raise Stop('INPUT_MISSING', '주 사다리 P0 · P1 둘이 다 있어야 한다')
    m_flags = []
    for law, (rd, s, h, L) in main_l.items():
        pub['calib'][law] = L['status']
        m_flags += L['flags']
        res['ladders'][law] = {'status': L['status'], 'R_j0': L['st']['R_j0'], 'R_j_lo': L['st']['R_j_lo'], 'R_j_hi': L['st']['R_j_hi'],
                               'R_ratio': L['st']['R_ratio'], 'ends': L['st']['ends'], 'local_e_ge_emin': L['st']['local_e_ge_emin'],
                               'floor_mScm': L['sealed']['points'].get('inf', math.nan) * 1e3,
                               'ceiling_mScm': L['sealed']['points'].get('0', math.nan) * 1e3,
                               'states': L['st']['states'], 'e': L['sealed']['e'],
                               'e_over_emin': (L['sealed']['e'] / E_MIN if isinstance(L['sealed']['e'], float) else None),
                               'delta': L['sealed']['delta'], 'points_mScm': {k: v * 1e3 for k, v in L['sealed']['points'].items()},
                               'origin_points_mScm': {k: [x * 1e3 for x in v] for k, v in L['sealed']['origin_points'].items()},
                               'ends_sigma_mScm': {k: v * 1e3 for k, v in L['sealed']['ends_sigma'].items()},
                               'origin': L['sealed']['origin']}
    statuses = {law: main_l[law][3]['status'] for law in LAWS}
    #  ★ 4판 (Q1 · §5-5b NOT_COMPUTED · CALIB_* 행) — 판정 기록의 사유 (주 판정 단계만 · 원 팔에서 다시 계산한 멈춤 기록)
    pub['reasons'] = [_why('ladder', law, None, main_l[law][3]['stop']) for law in LAWS if statuses[law] != 'CALIBRATED']

    def predict_of(variant, lads):
        if variant not in pred_in:
            return None
        rd, s, h = pred_in[variant]
        for law in LAWS:
            ref = (s.get('ladders') or {}).get(law) or {}
            if ref.get('summary_sha256') != lads[law][2]:
                raise Stop('PREDICT_LADDER_MISMATCH', f'{rd.name}: {law} 사다리 요약 sha256 ≠ 판정 입력')
        if variant_stage_stopped(s):
            return None, 'STOPPED', s.get('stop')             # ★ RI (§5-6 ③) — 멈춘 감도 변이 예측 = 값 없음 → 그 변이 판정 NOT_COMPUTED
        lin = {law: {'R_j0': lads[law][3]['st']['R_j0'], 'R_j_lo': lads[law][3]['st']['R_j_lo'], 'R_j_hi': lads[law][3]['st']['R_j_hi'],
                     'r0_sigma': lads[law][3]['pts'][lads[law][3]['st']['R_j0']][1],
                     'noop': lads[law][3].get('noop')} for law in LAWS}    # ★ 10-27 묶음 C2a — 다시 계산한 사다리 끝 no-op 기록
        return _replay_predict(rd, s, lin, contract, sid_reg, cert_reg, graph_src=graph_src)
    if any(st != 'CALIBRATED' for st in statuses.values()):
        P, PJ = assemble({'statuses': statuses, 'vals': None, 'flags': m_flags}, {}, None)
        pub.update({k: P[k] for k in PUB_FROM_ASSEMBLE})
        res['certificates_dsigma_rel'] = dict(cert_reg)
        return pub, _clean(res)
    got_pr = predict_of(None, main_l)
    if got_pr is None:
        raise Stop('INPUT_MISSING', '주 예측 폴더가 없다 (사다리 둘 다 보정됨)')
    pr, p_status, p_stop = got_pr
    if p_status != 'PREDICTED':
        #  ★ 4판 (Q1 · §5-0 ① ③ · §4-2 ③) — 예측 단계 NOT_COMPUTED (DBE 모서리 · origin 팔의 단락 · 증서 실패) = 판정 NOT_COMPUTED (등록 결과 ·
        #    rc 0 · 멈춤 아님) · 사유 = 그 멈춤 기록 · 감도 · SV 대조는 보지 않는다 (주 판정이 없다)
        pub['reasons'].append(_why('predict', None, None, p_stop))
        P, PJ = assemble({'statuses': statuses, 'vals': None, 'flags': m_flags}, {}, None)
        pub.update({k: P[k] for k in PUB_FROM_ASSEMBLE})
        res['predict'] = {'status': p_status, 'stop': p_stop}
        res['certificates_dsigma_rel'] = dict(cert_reg)
        return pub, _clean(res)
    main_pred_sha = pred_in[None][2]
    vals = pr.values()
    plan_main = pred_in[None][1]['plan']['content']
    svf, svd = sv_assess(pr.vals, plan_main['sv_cf_threshold'], plan_main['sv_cf_scope'], require_graph=True)   # ★ 10-26 묶음 B6
    vres = {}
    for V in VARIANTS:
        vl = main_l if V == 'SVORDER' else ladders_of(V)
        if V != 'SVORDER' and vl is None:
            vres[V] = None
            continue
        for d_ in ([pred_in[V]] if V in pred_in else []) + ([vl[law][:3] for law in LAWS] if V != 'SVORDER' else []):
            if (d_[1].get('after_main') or {}).get('summary_sha256') != main_pred_sha:      # ★ Q-F — 감도 = 이 주 예측 뒤에
                raise Stop('MAIN_BINDING', f'{d_[0].name}: 감도 단계가 묶인 주 예측 ≠ 판정 입력의 주 예측')
        vst = {law: vl[law][3]['status'] for law in LAWS}
        vflags = [] if V == 'SVORDER' else [f for law in LAWS for f in vl[law][3]['flags']]
        if all(x == 'CALIBRATED' for x in vst.values()):
            vp = predict_of(V, vl)
            if vp is None:
                vres[V] = None                          # 사다리는 됐는데 예측을 안 돌렸다 = 안 돌림
                continue
            vpr, v_status, _v_stop = vp
            #  ★ 4판 (Q1) — 변이 예측 NOT_COMPUTED (등록 결과) = 그 변이 판정 NOT_COMPUTED (vals None · `judge_set`)
            vres[V] = {'statuses': vst, 'vals': (vpr.values() if v_status == 'PREDICTED' else None), 'flags': vflags}
        else:
            vres[V] = {'statuses': vst, 'vals': None, 'flags': vflags}
    P, PJ = assemble({'statuses': statuses, 'vals': vals, 'flags': m_flags}, vres, (svf, svd))
    pub.update({k: P[k] for k in PUB_FROM_ASSEMBLE + ('variants',)})
    J = PJ['judge']
    res.update({k: J[k] for k in ('interval_mScm', 'I_law_mScm', 'in_law', 'in_U', 'in_E', 'W', 'p', 'p_why', 'd', 'd_over_G0',
                                  'direction', 'd_to_U', 'S', 'S_why', 'sigma_mid_mScm')})
    res['state'] = J['state']
    res['main_R0_only'] = J['main_R0_only']
    ms = {k: v * 1e3 for k, v in vals.items()}
    st_ = pr.states()
    res['corners_mScm'] = {f'c{c}_{law}': {rr: ms[(c, law, rr)] for rr in RJ_ROLES} for c in CS for law in LAWS}
    res['corners_state'] = {f'c{c}_{law}': {rr: st_[(c, law, rr)] for rr in RJ_ROLES} for c in CS for law in LAWS}
    res['corners_arm0_mScm'] = {f'c{c}_{law}': {rr: pr.vals[(c, law, rr)]['sigma'] * 1e3 for rr in RJ_ROLES} for c in CS for law in LAWS}
    res['origin'] = {'W0': pr.sealed['W0'], 'W_pos': pr.sealed['W_pos'], 'corners': pr.sealed['origin'],
                     'adjusted_mean8_mScm': {f'c{c}_{law}_{rr}': v * 1e3 for (c, law, rr), v in pr.adj.items()}}
    #  §6 s — R_j,lo ↔ R_j,hi 의 실제 역상 구간 할선 (분모 = 끝 두 점의 실제 Δ ln σ_SBE · §3-2b ⑦ · §10-2 ⑰ 3판)
    s_ = {}
    for c in CS:
        for law in LAWS:
            es = main_l[law][3]['sealed']['ends_sigma']
            den = ln_diff(es['hi'], es['lo'])
            num = ln_diff(vals[(c, law, 'R_j_hi')], vals[(c, law, 'R_j_lo')])
            s_[f'c{c}_{law}'] = (num / den if (math.isfinite(num) and math.isfinite(den) and den > 0) else None)
    res['s'] = s_
    res['P_effect_log'] = {f'c{c}': ln_diff(vals[(c, 'P0', 'R_j0')], vals[(c, 'P1', 'R_j0')]) for c in CS}
    res['c_effect_log'] = {law: ln_diff(vals[('0', law, 'R_j0')], vals[('1', law, 'R_j0')]) for law in LAWS}
    res['ratio_dbe_sbe'] = {f'c{c}_{law}': ms[(c, law, 'R_j0')] / TARGET_SBE_MS for c in CS for law in LAWS}
    res['dissipation_share'] = {f'c{c}_{law}_{rr}': pr.vals[(c, law, rr)]['dissipation_share'] for c in CS for law in LAWS for rr in RJ_ROLES}
    res['sv_local_dissipation'] = {f'c{c}_{law}_{rr}': pr.vals[(c, law, rr)].get('sv_local') for c in CS for law in LAWS
                                   for rr in RJ_ROLES}   # §5-6 진단 · 차단 표지 아님 (RCA-06)
    res['sv_counterfactual'] = svd
    res['variants'] = PJ['variants']
    res['certificates_dsigma_rel'] = dict(cert_reg)          # §8 수렴 증서 ⓒ (런마다 · 판정 결과로만)
    return pub, _clean(res)


def _clean(obj):
    """결과 JSON — NaN · inf 를 null 로 (allow_nan=False 직렬화 · 다시 판정 바이트 대조 · +∞ (zero 끝의 W 등) 는 상태 칸이 따로 적는다)."""
    if isinstance(obj, dict):
        return {str(k): _clean(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_clean(v) for v in obj]
    if isinstance(obj, float) and not math.isfinite(obj):
        return None
    return obj


def _stopped_pub(e, dirs, reg):
    """판정 계산기가 멈춤 (계약 · 기록 · 재현 · 입력 — 등록 판정 이름이 아닌 Stop 코드) → NOT_COMPUTED 기록 (§5-5 PRE-design-09 행 · ★ 4판 §5-5b
    NOT_COMPUTED 칸 = *"판정 없음 — 사유 (상태 · 멈춤 코드) 보고"* · 사유 = 그 멈춤 기록 · rc 3)."""
    rec = e.record()
    return {'tool': TOOL, 'schema': SCHEMA, 'stage': 'verdict', 'verdict': 'NOT_COMPUTED', 'state': 'calib', 'stop': rec, 'flags': [],
            'blocking_flags': [], 'blocking_reasons': {}, 'sensitivity_incomplete': None, 'qualifiers': list(QUALIFIERS),
            'report_category': {REPORT_CATEGORY: list(ASSUMED_UNVALIDATED)},
            'verdict_note': VERDICT_NOTE, 'sentence_allowed': False, 'sentence': decide_sentence('calib', 'NOT_COMPUTED', []),
            'calib': {}, 'variants': {}, 'grid_sentence': GRID_SENTENCE, 'inputs': [str(Path(d).resolve()) for d in dirs], 'arms': [],
            'registration': (str(Path(reg).resolve()) if reg else None), 'reasons': [_why('verdict', None, None, rec)],
            'ledger': getattr(e, 'ledger', None)}                # ★ 10-27 묶음 C1b — 원장 대조를 지난 뒤의 멈춤이면 그 원장 칸 (채택 시도)


#: ★ 10-27 묶음 C2e (Q9 설계 개정 5 ③ · Codex 회차 ① §7 ③ · author 10-27 approved bundle C) — 판정 프로세스 환경 옆 파일 (판정 JSON 밖 = 다시 판정 바이트 대조
#   무관 · 다른 플랫폼 다시 판정 = 환경 차이를 보고만) · 다시 판정 보고 (원 판정 · 다시 계산 판정 · 다른 공개 칸 · 다른 결과 칸 이름 (값 = 봉인 · 등록 R §4-1) ·
#   원 · 지금 환경 · 다른 환경 칸 · 등급 다름) — 구조 대조가 같아도 바이트가 다르면 REVERIFY_DIFF 그대로 (약화하지 않는다 · 원 판정을 덮지 않는다)
VERDICT_ENV_SCHEMA = 'rint-r-verdict-env-v1'
VERDICT_ENV_FILE = 'verdict_env.json'
REVERIFY_SCHEMA = 'rint-r-reverify-v1'
REVERIFY_REPORT = 'reverify_report.json'


def verdict_grade_view(p):
    """판정 공개 기록 → 등급 칸 (이름 · 상태 · 표지 · 차단 표지 · §7-1 문장 허용 · 멈춤 이름) — 값 없음."""
    p = p if isinstance(p, dict) else {}
    st = p.get('stop') if isinstance(p.get('stop'), dict) else None
    return {'verdict': p.get('verdict'), 'state': p.get('state'), 'flags': p.get('flags'), 'blocking_flags': p.get('blocking_flags'),
            'sentence_allowed': p.get('sentence_allowed'), 'stop_code': (st or {}).get('code')}


def reverify_report(vdir, pub0, pub, old_res, res, same, lin):
    """다시 판정 보고 (REVERIFY_SCHEMA) — 결과 JSON 은 칸 이름만 (값 = 봉인 · 화면 · 보고에 σ 없음)."""
    try:
        r0 = json.loads(old_res.decode('utf-8')) if old_res is not None else None
    except (UnicodeDecodeError, ValueError):
        r0 = None
    r1 = json.loads(canon_bytes(res).decode('utf-8')) if res is not None else None
    rkeys = sorted(k for k in set(r0 or {}) | set(r1 or {}) if (r0 or {}).get(k) != (r1 or {}).get(k)) \
        if isinstance(r0, dict) or isinstance(r1, dict) else []
    env0 = (read_summary(vdir, VERDICT_ENV_FILE)[0] or {}).get('env')
    env1 = env_record()
    g0, g1 = verdict_grade_view(pub0), verdict_grade_view(pub)
    pc = _clean(pub)
    return {'schema': REVERIFY_SCHEMA, 'verdict_dir': str(Path(vdir).resolve()), 'result': 'REVERIFY_SAME' if same else 'REVERIFY_DIFF',
            'original': g0, 'recomputed': g1, 'grade_differ': g0 != g1,
            'public_keys_differ': sorted(k for k in set(pc) | set(pub0) if pc.get(k) != pub0.get(k)),
            'results_differ': (old_res is None) != (res is None) or (r0 != r1), 'results_keys_differ': rkeys,
            'env_original': env0, 'env_now': env1, 'env_fields_differ': (_env_diff(env0, env1) if env0 is not None else None),
            'ledger_input': lin, 'utc': _utc()}


def stage_verdict(a, contract):
    if a.reverify:
        return reverify(a.reverify, contract, a.root, out=a.out)
    out = Path(a.out)
    try:
        outdir_empty_or_stop(out)
    except Stop as e:
        print_stop(e)
        return 3
    rc_ = 0
    #  ★ 10-26 B″ (1저자 Q1 (가)) — 판정의 봉인 원천 (원천 런 폴더 = <판정>/graph_src · 기록 = verdict_graph_src.json · 판정 JSON 밖 = 다시 판정 바이트
    #    대조 무관)
    gsrc = default_graph_src(a.root, out / GRAPH_SRC_DIR)
    lin = ledger_input(a.ledger, a.attempt_dirs)                # ★ 10-27 묶음 C1b — 원장 판정 입력 (경로 · 지금 HEAD · 시도 바탕 폴더 · 다시 판정이 같은 값으로)
    try:
        pub, res = verdict_compute(a.runs, a.registration, contract, a.root, graph_src=gsrc, ledger=lin)
    except Stop as e:
        print_stop(e)
        pub, res, rc_ = _stopped_pub(e, a.runs, a.registration), None, 3
    pub['input_dirs'] = [str(Path(d).resolve()) for d in a.runs]
    pub['ledger_input'] = lin
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / 'verdict.json', pub)
    #  ★ 10-27 묶음 C2e — 판정 프로세스 환경 (판정 JSON 밖 · 다시 판정이 보고에 원 환경으로 싣는다 · 바이트 대조 무관)
    write_json(out / VERDICT_ENV_FILE, {'schema': VERDICT_ENV_SCHEMA, 'env': env_record(), 'utc': _utc()})
    if gsrc is not None:
        write_json(out / 'verdict_graph_src.json', gsrc.public())
    if res is not None:
        write_json(out / 'verdict_results.json', res)
        try:
            os.chmod(out / 'verdict_results.json', 0o600)
        except OSError:
            pass
    print(f'판정 = {pub["verdict"]} (상태 {pub.get("state")}) · 표지 {pub["flags"] or "없음"} · 차단 {pub.get("blocking_flags") or "없음"} · '
          f'§7-1 문장 {"허용" if pub["sentence_allowed"] else "금지"}' + (f' · 사다리 {pub["calib"]}' if pub.get('calib') else '')
          + (' · 사유 ' + ' · '.join(f'{w.get("stage")} {w.get("law") or ""} {w.get("code")} {w.get("reason") or ""}'.replace('  ', ' ').strip()
                                    for w in pub['reasons']) if pub.get('reasons') else ''))
    if a.show_results:
        if res is None:
            print('--show-results — 판정이 없어 열지 않는다 (멈춤)')
        else:
            print('══ 판정 결과 (값 열림 · 판정에 쓰는 런이 다 끝났다 · 등록 R §4-1) ══')
            print(canon_bytes(res).decode('utf-8'))
            with open(out / 'views.jsonl', 'a', encoding='utf-8') as f:
                f.write(json.dumps({'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                                    'results_sha256': sha256_file(out / 'verdict_results.json')}) + '\n')
    print(f'판정 → {out / "verdict.json"}')
    return rc_


def reverify(vdir, contract, root, out=None):
    """다시 판정 (읽기 전용) — 같은 입력 (판정 JSON 에 적힌 폴더 · 등록) 으로 다시 계산해 두 JSON 을 바이트 대조.  ★ 10-25 묶음 B (RCA2-03) —
    root = 그 기계의 킷 뿌리 (킷을 다시 해시 · 같은 침대가 아니면 다른 판정 = REVERIFY_DIFF).  ★ 10-26 B″ (Q1 (가)) — 봉인 원천도 다시 부른다
    (`verdict_compute` 기본 = 임시 폴더 · 판정 폴더에 아무것도 쓰지 않는다).
    ★ 10-27 묶음 C2e (Q9 개정 5 ③ · Codex 회차 ① ③) — 바이트 대조 그대로 (구조 같아도 등급 다르면 REVERIFY_DIFF · 약화 · 덮어쓰기 없음) + 보고 (`reverify_report`
    · 다르면 화면에 원 · 다시 계산 등급 · 다른 결과 칸 이름 · 다른 환경 칸) · out = 새 폴더 (보고 `reverify_report.json` · 비지 않았으면 rc 3 · 없으면 화면만)."""
    vdir = Path(vdir)
    if out is not None:
        try:
            outdir_empty_or_stop(out)
        except Stop as e:
            print_stop(e)
            return 3
    try:
        old_pub = (vdir / 'verdict.json').read_bytes()
        pub0 = json.loads(old_pub.decode('utf-8'))
    except (OSError, UnicodeDecodeError, ValueError) as e:
        print(f'REVERIFY_DIFF — {vdir / "verdict.json"} 를 못 읽는다 ({type(e).__name__})')
        return 1
    rp = vdir / 'verdict_results.json'
    old_res = rp.read_bytes() if rp.exists() else None
    dirs = pub0.get('input_dirs') or []
    reg = (pub0.get('registration') or {}).get('path') if isinstance(pub0.get('registration'), dict) else pub0.get('registration')
    lin = pub0.get('ledger_input') if isinstance(pub0.get('ledger_input'), dict) else None   # ★ 10-27 묶음 C1b — 같은 원장 커밋으로 다시
    try:
        pub, res = verdict_compute(dirs, reg, contract, root, ledger=lin)
    except Stop as e:
        pub, res = _stopped_pub(e, dirs, reg), None
    pub['input_dirs'] = dirs
    pub['ledger_input'] = lin
    new_pub, new_res = canon_bytes(_clean(pub)), (canon_bytes(res) if res is not None else None)
    same = new_pub == old_pub and new_res == old_res
    rep = reverify_report(vdir, pub0, pub, old_res, res, same, lin)
    if out is not None:
        Path(out).mkdir(parents=True, exist_ok=True)
        write_json(Path(out) / REVERIFY_REPORT, rep)
    if same:
        print(f'REVERIFY_SAME — 판정 JSON · 결과 JSON 바이트 같음 ({len(dirs)} 입력 · 판정 {pub["verdict"]})')
        if out is not None:
            print(f'다시 판정 보고 → {Path(out) / REVERIFY_REPORT}')
        return 0
    keys = sorted(k for k in set(pub) | set(pub0) if _clean(pub).get(k) != pub0.get(k))
    print(f'REVERIFY_DIFF — 다시 계산한 판정이 저장본과 다르다 (공개 칸 {keys} · 결과 {"같음" if new_res == old_res else "다름"})'
          + (f' · 멈춤 {pub["stop"]["code"]}' if pub.get('stop') else ''))
    g0, g1 = rep['original'], rep['recomputed']
    print(f'  원 판정 {g0["verdict"]} ({g0["state"]}) → 다시 계산 {g1["verdict"]} ({g1["state"]}) · 등급 다름 {rep["grade_differ"]} · 다른 결과 칸 '
          f'{rep["results_keys_differ"]} (값 = 봉인) · 다른 환경 칸 {(rep["env_fields_differ"] or [])[:6] if rep["env_original"] is not None else "원 환경 기록 없음"}'
          f' — 원 판정을 덮지 않는다 · 유리한 쪽을 고르지 않는다' + (f' · 보고 → {Path(out) / REVERIFY_REPORT}' if out is not None else ''))
    return 1


def recover_group(lp, me):
    """시작 기록 하나 (끝 기록 없음 · 또는 끝 기록 미확인) → 끝 기록 dict (by recover · 원인 parent_dead).  호스트 규칙: 같은 부팅 (boot_id) · 같은 pid
    이름공간 = /proc 의 env 표지로 찾아 SIGKILL · 다 끝날 때까지 (`group_settle`) · 같은 기계 (machine_id) · 다른 부팅 = 그 부팅의 프로세스는 없다 (확인 ·
    재부팅) · 그 밖 (다른 기계 · 다른 이름공간 · 기계를 모르는 다른 부팅) = 미확인 (여기서 그 프로세스를 볼 수 없다)."""
    nm = lp.name[:-len('.launch.json')]
    try:
        L = json.loads(lp.read_text(encoding='utf-8'))
    except (OSError, UnicodeDecodeError, ValueError):
        L = None
    tok = (L or {}).get('token') if isinstance(L, dict) else None
    confirmed, left, killed, why = False, None, 0, None
    if not (isinstance(tok, str) and re.fullmatch(r'[0-9a-f]{32}', tok)):
        why = '시작 기록 꼴 (그룹 표지) 을 못 읽는다'
    else:
        h = L.get('host') if isinstance(L.get('host'), dict) else {}
        same_boot = h.get('boot_id') is not None and h.get('boot_id') == me.get('boot_id')
        same_ns = h.get('pidns') is not None and h.get('pidns') == me.get('pidns')
        same_machine = h.get('machine_id') is not None and h.get('machine_id') == me.get('machine_id')
        other_machine = h.get('machine_id') is not None and me.get('machine_id') is not None and not same_machine
        if other_machine:
            why = '다른 기계 (machine_id) — 여기서 그 프로세스를 볼 수 없다'
        elif same_boot and same_ns:
            confirmed, left, killed = group_settle(tok)
            why = None if confirmed else ('/proc 를 못 읽는다' if left is None else '표지 프로세스가 대기 상한 안에 남았다')
        elif same_machine and h.get('boot_id') is not None and me.get('boot_id') is not None and not same_boot:
            confirmed, left, why = True, [], '재부팅 — 그 부팅의 프로세스는 없다'
        else:
            why = '다른 기계 · pid 이름공간 · (기계를 모르는) 다른 부팅 — 여기서 그 프로세스를 볼 수 없다'
    return {'schema': GROUP_SCHEMA, 'name': nm, 'token': tok, 'rc': None, 'cause': 'parent_dead', 'signal': None, 'confirmed': bool(confirmed),
            'left': left, 'left_after_exit': None, 'killed': killed, 'by': 'recover', 'why': why, 'host': me, 'ended_utc': _utc()}


def stage_recover(a):
    """★ 10-27 묶음 C2b (Codex 회차 ① ② · Q9 개정 5 ② · author 10-27 approved bundle C) — 사슬 부모가 죽은 뒤 (SIGKILL · 정전 · 컨테이너 재시작) 단계 ·
    시도 폴더 아래 `groups/*.launch.json` 중 끝 기록이 없거나 미확인인 것마다 그룹 종료를 확인한다 (`recover_group`) → 끝 기록 (by recover) · 하나라도
    미확인 = rc 3 (다음 시도를 시작 · 채택하기 전에 사람이 본다 · "부모 사망 + 지금 표지 없음" 을 종료 증거로 쓰지 않는다)."""
    root = Path(a.out)
    me = host_ident()
    todo = []
    for lp in sorted(root.rglob(f'{GROUPS_DIR}/*.launch.json')):
        ep = lp.with_name(lp.name[:-len('.launch.json')] + '.end.json')
        try:
            e = json.loads(ep.read_text(encoding='utf-8')) if ep.exists() else None
        except (OSError, UnicodeDecodeError, ValueError):
            e = None
        if not (isinstance(e, dict) and e.get('confirmed') is True):
            todo.append((lp, ep))
    n_bad = 0
    for lp, ep in todo:
        end = recover_group(lp, me)
        write_json_atomic(ep, end)
        n_bad += 0 if end['confirmed'] else 1
        print(f'  recover {lp.parent.parent.name}/{end["name"]}: 종료 {"확인" if end["confirmed"] else "미확인"} · 죽인 프로세스 {end["killed"]}'
              + (f' · {end["why"]}' if end['why'] else ''))
    print(f'recover — 그룹 기록 {len(todo)} 개 정리 · 미확인 {n_bad}' + (' (다음 시도 전에 사람이 본다)' if n_bad else ''))
    if getattr(a, 'ledger', None):
        n_bad += recover_ledger(root, Path(a.ledger))
    return 0 if n_bad == 0 else 3


def recover_ledger(root, repo):
    """★ 10-27 묶음 C1b (Q9 개정 5 ② · "supervisor / recovery 가 종료를 확인한 뒤 표지 · payload · 폴더 해시를 확정") — root (시도 폴더 · 또는 그 바탕)
    아래 시도 폴더마다: 원장 항목에 결과 줄이 없고 그 폴더의 그룹이 다 확인됐으면 결과 줄 (by recover · 단계 요약 있음 = 그 상태 · 거부 기록 = rejected ·
    없음 = interrupted · 원인 parent_dead) → 못 쓴 수 (미확인 · 원장 불일치)."""
    root = Path(root)
    folders = [root] if read_attempt(root) is not None else [p for p in sorted(root.iterdir()) if p.is_dir() and read_attempt(p) is not None] \
        if root.is_dir() else []
    bad = 0
    for f in folders:
        a = read_attempt(f)
        n = a['n']
        try:
            why = ledger_repo_problem(repo)
            if why:
                raise Stop('ATTEMPT_LEDGER_MISMATCH', why)
            head, raw = ledger_now(repo)
            st = ledger_parse(raw)
            e = st['entries'].get(n)
            if e is None or e['target'] != a['target'] or not ledger_is_ancestor(repo, a['ledger_commit'], head):
                raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{f.name}: 이 원장의 항목 {n} ({a["target"]}) 시도가 아니다')
            if n in st['results']:
                continue
            why = attempt_groups_problem(f)
            if why:
                print(f'  recover {f.name}: {why} — 결과 줄을 쓰지 않는다 (미확인 · 다음 시도 채택을 막는다)')
                bad += 1
                continue
            rj = f / REJECTED_FILE
            if rj.is_file():
                rec = _json_strict(rj.read_bytes())
                res = {'kind': 'result', 'n': n, 'status': 'rejected', 'stop': {'code': str(rec.get('code')), 'run': None, 'reason': None},
                       'side': 'pre', 'cause': 'presolve', 'resume_ok': False, 'folder': f.name, 'folder_sha256': folder_digest(f),
                       'by': 'recover', 'utc': _utc()}
            else:
                s = None
                for nm in ('ladder_summary.json', 'predict_summary.json', UNIT_SUMMARY['unit'], UNIT_SUMMARY['point']):   # ★ 10-27 묶음 C2d — 단위 · 넘침 점
                    s = s or read_summary(f, nm)[0]
                res = attempt_result_line(n, f, s, 'recover')
            ledger_append(repo, res, f'rint-r attempt {n} result {res["status"]} (recover)', expect=raw)
        except (Stop, OSError, ValueError) as ex:
            print_stop(ex if isinstance(ex, Stop) else Stop('ATTEMPT_LEDGER_MISMATCH', f'{f.name}: {type(ex).__name__}: {ex}'))
            bad += 1
            continue
        print(f'  recover {f.name}: 결과 줄 {res["status"]} · 결과 {res["side"]} · 원인 {res["cause"]} · 재실행 자격 {res["resume_ok"]}')
    return bad


def stage_ledger(a):
    """★ 10-27 묶음 C1b (RCA2-05 · Q9 §3-5) — 시도 원장: --init (머리 = 계획 sha256 · 한 번) · --add (항목 = 대상 · 기계 · 재실행이면 원 시도 · 계획 ·
    코드 키 · 환경 · 침대 지문 — 시도 **전에** 커밋 · 차례 · 채택 · 재실행 자격 · 최대 시도 수를 먼저 본다 · 화면 ATTEMPT_ADDED n=<번호>)."""
    if bool(a.init) == bool(a.add) or not a.ledger:
        print('인자 오류: --stage ledger 는 --ledger <원장 git 저장소> 와 --init 또는 --add 하나', file=sys.stderr)
        return 2
    repo = Path(a.ledger)
    try:
        why = ledger_repo_problem(repo)
        if why:
            raise Stop('ATTEMPT_LEDGER_MISMATCH', why)
        lp = repo / LEDGER_FILE
        if a.init:
            if lp.exists() or lp.is_symlink():
                raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{lp} 가 이미 있다 (원장은 한 번만 시작한다)')
            plan, plan_sha = load_plan(a.plan)
            require_plan_numbers(plan)                        # 봉인 전 계획 = 원장 없음 (C1 — 봉인 전 계획이면 R 진입 거부)
            head = {'kind': 'header', 'schema': LEDGER_SCHEMA, 'plan_sha256': plan_sha, 'utc': _utc()}
            ledger_parse(ledger_line(head).encode('utf-8'))
            with open(lp, 'xb') as f:
                f.write(ledger_line(head).encode('utf-8'))
                f.flush()
                os.fsync(f.fileno())
            ledger_git(repo, 'add', '--', LEDGER_FILE)
            ledger_git(repo, 'commit', '-q', '-m', f'rint-r ledger init (plan {plan_sha[:12]})', '--', LEDGER_FILE)
            print(f'LEDGER_INIT — {lp} · 계획 sha256 {plan_sha} · 커밋 {ledger_head(repo)}')
            return 0
        if not (a.ledger_target and TARGET_RE.fullmatch(a.ledger_target)):
            raise Stop('NOT_REGISTERED', f'--ledger-target {a.ledger_target!r} (ladder:P0 · ladder:P1 · ladder:<법칙>:<FIBRE|UNREG|GRID> · predict · '
                                         f'predict:<변이> · ★ C2d unit[:<변이>]:<단위> · point[:<변이>]:<단위> — 단위 = <법칙>_c<c>_<R 역할>)')
        head, raw = ledger_now(repo)
        st = ledger_parse(raw)
        plan, plan_sha = load_plan(a.plan)
        if plan_sha != st['header']['plan_sha256']:
            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'--plan sha256 {plan_sha[:12]} ≠ 원장 머리의 계획 {st["header"]["plan_sha256"][:12]}')
        require_plan_numbers(plan)
        if a.machine not in (plan['exec_policy'].get('allowed_machines') or ()):
            raise Stop('MACHINE_NOT_ALLOWED', f'--machine {a.machine!r} ∉ 계획 허용 목록 {plan["exec_policy"].get("allowed_machines")}')
        code = code_record(a.runner)
        why = code_dirty_problem(code) or env_seal_problem(code, plan)
        if why:
            raise Stop('CODE_PIN_MISMATCH', why)
        e = {'kind': 'entry', 'n': len(st['entries']) + 1, 'target': a.ledger_target, 'machine': a.machine, 'resume_of': a.resume,
             'plan_sha256': plan_sha, 'code_key_sha256': code_key_sha(code), 'env': code['env'],
             'bed': {k: kit_bed(a.root, k) for k in target_kits(a.ledger_target)}, 'utc': _utc()}
        if a.resume is not None and (a.resume not in st['entries'] or st['entries'][a.resume]['target'] != a.ledger_target):
            raise Stop('RESUME_NOT_ALLOWED', f'--resume {a.resume} = 같은 대상 ({a.ledger_target}) 의 원장 항목이어야')
        prob = attempt_order_problem(st, e, plan)
        if prob:
            raise Stop(*prob)
        c = ledger_append(repo, e, f'rint-r attempt {e["n"]} entry {e["target"]} {e["machine"]}', expect=raw)
    except Stop as ex:
        print_stop(ex)
        return 3
    print(f'ATTEMPT_ADDED n={e["n"]} target={e["target"]} machine={e["machine"]}' + (f' resume_of={e["resume_of"]}' if e['resume_of'] else '')
          + f' commit={c} — 이 번호로 --ledger {repo} --attempt {e["n"]} (풀기 전 대조 = 이 항목의 지문)')
    return 0


def stage_plan_doc(a):
    """★ 10-27 묶음 C1a (판정문 C6 #30) — 계획 JSON → 계획 숫자 블록 (화면 · 등록 R 에 그대로 붙인다) · `--check-doc` = 등록의 블록과 정확 대조."""
    try:
        plan, _sha = load_plan(a.plan)
    except Stop as e:
        print_stop(e)
        return 3
    if not a.check_doc:
        print(plan_doc_block(plan))
        return 0
    why = plan_doc_problem(a.registration, plan)
    if why:
        print_stop(Stop('PLAN_DOC_MISMATCH', why))
        return 3
    print(f'PLAN_DOC_SAME — 등록 {a.registration} 의 계획 숫자 블록 = 계획 {a.plan} 에서 생성한 블록 (정확히)')
    return 0


# ═════════════════════════ CLI ═════════════════════════
def main(argv=None, contract=None):
    try:                                   # ★ SELF-122 — 화면을 파일로 돌려도 줄마다 바로 쓴다
        sys.stdout.reconfigure(line_buffering=True)
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--stage', choices=('ladder', 'predict', 'verdict', 'plan-doc', 'recover', 'ledger'), default='ladder')
    ap.add_argument('--law', choices=LAWS, help='ladder — PTFE–접합 법칙 끝')
    ap.add_argument('--target', type=float, default=TARGET_SBE_MS, help='ladder — 등록 표적 (1.63 이 아니면 멈춤)')
    ap.add_argument('--variant', choices=VARIANTS, default=None, help='감도 (등록 R §5-6 · 필수 · 주 판정 단계 뒤에만 — --after-main)')
    ap.add_argument('--after-main', default=None, help='ladder · predict 의 --variant — 끝난 주 예측 폴더 (Q-F · 판정이 묶음을 대조한다)')
    ap.add_argument('--kit', default=None, help=f'ladder = {SBE_KIT} · predict = {DBE_KIT} (등록 · 다르면 멈춤)')
    ap.add_argument('--runner')
    ap.add_argument('--root', help='킷 폴더가 있는 곳 = 러너 작업 폴더 · ★ 10-25 묶음 B (RCA2-03) — 판정 · 다시 판정도 필수 (킷을 S0 와 같은 '
                                   '발견 함수로 다시 해시해 S0 보고의 원 입력과 대조 · 기계마다 자기 사본 · 경로 = 대조 밖)')
    ap.add_argument('--plan', help='ladder · plan-doc — R 런 계획 파일 (rint-r-plan-v3 · 실행 정책 칸 포함 · 등록 §2-1 개정 커밋의 대상 · sha256 = '
                                   '그 칸)')
    ap.add_argument('--s0-plan', help='ladder — S0 단계 1 계획 (ca-cjunc-plan-v1 · 정준 바이트 · sha256 = 등록 §2-1 S0 계획 해시 칸) · '
                                      '두 계획 대조 (§2-1 · §10-2 ⑪)')
    ap.add_argument('--s0-stage2-report', help='ladder — S0 단계 2 보고 (s0_stage2_<DBE 킷>.json · ca_s0_census) · 그 보고가 봉인한 계획 '
                                               '해시 (R 계획 · S0 계획) = 지금 계획이어야 돈다 (★ PF2 B · Q2 · 등록 R §2-1b · §11 ④)')
    ap.add_argument('--s0-stage1-report', help='ladder — S0 단계 1 보고 (s0_stage1_<SBE 킷>.json · 그 보고가 만든 S0 계획 = --s0-plan) · '
                                               'census · registry 일곱 파일 지문 = 지금 R 런 코드여야 돈다 (★ PF2 D · 등록 R §2-1b)')
    ap.add_argument('--machine', default=None, help='ladder · predict — 기계 이름표 (★ 10-27 묶음 C1a = 필수 · 계획 exec_policy.allowed_machines 안 · '
                                                    '실행자가 넣는 짧은 이름 · 영문 · 숫자 · _ · - 만 · IP · 주소 금지 · 단계 요약 · 런 기록마다 · '
                                                    '판정이 허용 목록 · 단계 ↔ 런 대조 · 등록 R §10-4 문장 3)')
    ap.add_argument('--check-doc', action='store_true', help='plan-doc — 등록 R (--registration) 의 계획 숫자 블록이 --plan 에서 생성한 블록과 '
                                                             '정확히 같은지 (같음 rc 0 · 다름 rc 3 PLAN_DOC_MISMATCH)')
    ap.add_argument('--registration', default=str(REGISTRATION_DEFAULT), help='등록 R 문서 (§2-1 계획 해시 · S0 계획 해시를 읽는다)')
    ap.add_argument('--ladders', nargs='+', help='predict — 사다리 폴더 둘 (P0 · P1)')
    ap.add_argument('--runs', nargs='+', help='verdict — 사다리 · 예측 · 감도 폴더 전부')
    ap.add_argument('--reverify', help='verdict — 판정 폴더를 같은 입력으로 다시 판정 (읽기 전용 · 바이트 대조)')
    ap.add_argument('--out', help='새 출력 폴더 (없거나 비어 있어야) · recover = 정리할 단계 · 시도 폴더 · ★ 10-27 묶음 C2e verdict --reverify = 보고 폴더 '
                                  '(선택 · reverify_report.json)')
    ap.add_argument('--max-hours', type=float, help='ladder · predict — 시간 상한 (등록 §10 · 숫자 탐침 뒤의 값 · 기본값 없음 · ★ 10-27 묶음 C1a = '
                                                    '계획 exec_policy.max_hours 와 같아야 · 다르면 NOT_REGISTERED)')
    ap.add_argument('--dry-run', action='store_true', help='ladder · predict — 런 env 만 찍는다 (러너 · 출력 폴더 없음)')
    ap.add_argument('--show-results', action='store_true', help='verdict 만 — 판정에 쓰는 런이 다 끝난 뒤 값을 연다 (열람 기록)')
    #  ★ 10-27 묶음 C1b (RCA2-05 · Q4 (가) · Q9 설계 §3-2 · §3-5 · author 10-27 approved bundle C) — 시도 원장 · 시도 폴더
    ap.add_argument('--ledger', default=None, help='시도 원장 git 저장소 (실행 트리와 다른 체크아웃 · 파일 rint_r_attempts.jsonl) — ledger (--init · --add) · '
                                                   'ladder · predict (--attempt 와 함께 = 시도 꼴 · --out = 시도 폴더의 바탕) · verdict (원장 판정 · 채택 시도만) · '
                                                   'recover (결과 줄 확정)')
    ap.add_argument('--attempt', type=int, default=None, help='ladder · predict — 원장 항목 번호 (시도 폴더 = <--out>/attempt_<n> · 풀기 전 대조 = 그 항목 · '
                                                             '끝 = 결과 줄)')
    ap.add_argument('--init', action='store_true', help='ledger — 원장 시작 (머리 줄 = --plan sha256 · 한 번)')
    ap.add_argument('--add', action='store_true', help='ledger — 항목 하나 (--ledger-target · --machine · --plan · --runner · --root · 재실행 = --resume) · '
                                                       '시도 전에 커밋')
    ap.add_argument('--ledger-target', default=None, help='ledger --add — 대상 (ladder:P0 · ladder:P1 · ladder:<법칙>:<FIBRE|UNREG|GRID> · predict · '
                                                          'predict:<변이> · ★ 10-27 묶음 C2d unit[:<변이>]:<단위> · point[:<변이>]:<단위>)')
    ap.add_argument('--resume', type=int, default=None, help='ledger --add — 재실행 항목의 원 시도 번호 (같은 대상 · 채택 시도 · 재실행 자격 · 같은 기계 · '
                                                            '환경 지문)')
    ap.add_argument('--attempt-dirs', nargs='+', default=None, help='verdict — 시도 폴더 바탕 (입력 폴더의 부모 밖에 둔 다른 시도 · 거부 기록)')
    #  ★ 10-27 묶음 C2d (Q9 설계 §3-1 · §3-2 · author 10-27 approved bundle C) — 12 단위 · 넘침 점 · 합치기 (이름 = 구현 때 정하는 꼴)
    ap.add_argument('--unit', default=None, help='predict — 단위 시도 (<법칙>_c<c>_<R 역할> 예 P0_c0_R_j0 · --ledger · --attempt 와만 · 모서리 arm 0 + origin '
                                                 '표본 arm 1 · 2 · 요약 unit_summary.json · 원장 대상 unit[:<변이>]:<이름>)')
    ap.add_argument('--point', default=None, help='predict — 넘침 점 시도 (단위 이름 꼴 · --expand <결정 기록> · --ledger · --attempt 와만 · origin8 · 요약 '
                                                  'point_summary.json · 원장 대상 point[:<변이>]:<이름>)')
    ap.add_argument('--expand', default=None, help='predict --point · --merge — 첫 합치기의 결정 기록 (expansion.json · 넘침 점 · 끝 합치기)')
    ap.add_argument('--merge', nargs='+', default=None, help='predict — 합치기 (단위 · 넘침 점 시도 폴더 · 그 바탕 · --ledger 와 · --attempt 없이 · 넘침 있으면 '
                                                             'rc 4 + expansion.json · 끝 합치기 = --expand)')
    a = ap.parse_args(argv)
    contract = RealContract() if contract is None else contract
    if a.show_results and a.stage != 'verdict':
        ap.error('--show-results 는 --stage verdict 에서만 (등록 R §4-1 — 판정에 쓰는 런이 다 끝난 뒤 한 번)')
    if a.after_main and not a.variant:
        ap.error('--after-main 은 --variant (감도 단계) 와만')
    if a.machine is not None and (a.stage in ('verdict', 'plan-doc', 'recover') or not MACHINE_RE.fullmatch(a.machine)):
        ap.error('--machine 은 ladder · predict · ledger 에서만 · 영문 · 숫자 · _ · - 로 된 짧은 이름 (IP · 주소 · 경로 · 띄어쓰기 금지 · 등록 R §10-4 '
                 '문장 3)')
    if a.check_doc and a.stage != 'plan-doc':
        ap.error('--check-doc 은 --stage plan-doc 에서만')
    if (a.init or a.add or a.ledger_target or a.resume is not None) and a.stage != 'ledger':
        ap.error('--init · --add · --ledger-target · --resume 은 --stage ledger 에서만')
    if a.attempt is not None and a.stage not in ('ladder', 'predict'):
        ap.error('--attempt 는 ladder · predict 에서만 (--ledger 와 함께)')
    if a.attempt_dirs and not (a.stage == 'verdict' and a.ledger):
        ap.error('--attempt-dirs 는 --stage verdict --ledger 에서만')
    if a.ledger and a.stage == 'plan-doc':
        ap.error('--ledger 는 plan-doc 에 쓰지 않는다')
    if a.unit is not None or a.point is not None or a.merge is not None or a.expand is not None:      # ★ 10-27 묶음 C2d
        if a.stage != 'predict':
            ap.error('--unit · --point · --expand · --merge 는 --stage predict 에서만')
        if sum(x is not None for x in (a.unit, a.point, a.merge)) > 1:
            ap.error('--unit · --point · --merge 는 하나만 (시도 하나 = 단위 · 점 하나 · 합치기 = 시도 아님)')
        if a.expand is not None and a.point is None and a.merge is None:
            ap.error('--expand 는 --point · --merge 와만')
        if a.point is not None and a.expand is None:
            ap.error('--point 는 --expand <결정 기록> 과 (결정 기록이 요구한 origin8 런만)')
        for nm in (a.unit, a.point):
            if nm is not None and not UNIT_RE.fullmatch(nm):
                ap.error(f'단위 · 넘침 점 이름 {nm!r} (<법칙>_c<c>_<R 역할> — 예 P0_c0_R_j0 · 법칙 P0 · P1 · c 0 · 1 · R R_j_lo · R_j0 · R_j_hi)')
        if (a.unit is not None or a.point is not None) and (a.ledger is None or a.attempt is None):
            ap.error('--unit · --point = 원장 시도만 (--ledger · --attempt · 원장 밖 런 금지 · Q9 §3-5)')
        if a.merge is not None and (a.ledger is None or a.attempt is not None or a.dry_run):
            ap.error('--merge 는 --ledger 와 (--attempt · --dry-run 없이 · 합치기 = 시도 아님)')
    if a.stage == 'ledger':
        if a.add and not (a.ledger_target and a.machine and a.plan and a.runner and a.root):
            ap.error('--stage ledger --add 는 --ledger-target · --machine · --plan · --runner · --root 가 필요하다')
        if a.init and not a.plan:
            ap.error('--stage ledger --init 은 --plan 이 필요하다')
        return stage_ledger(a)
    if a.stage == 'recover':
        if not a.out:
            ap.error('--stage recover 는 --out (단계 · 시도 폴더 — 그 아래 groups/ 의 끝 기록 없는 러너 그룹) 이 필요하다')
        return stage_recover(a)
    if a.stage == 'plan-doc':
        if not a.plan:
            ap.error('--stage plan-doc 는 --plan 이 필요하다 (--check-doc 이면 --registration 의 블록과 대조)')
        return stage_plan_doc(a)
    if a.stage == 'ladder':
        if not (a.law and a.runner and a.root and a.plan and a.s0_plan and a.s0_stage2_report and a.s0_stage1_report and a.out
                and a.max_hours is not None):
            ap.error('--stage ladder 는 --law · --runner · --root · --plan · --s0-plan · --s0-stage2-report · --s0-stage1-report · --max-hours · '
                     '--out 이 필요하다')
        return stage_ladder(a, contract)
    if a.stage == 'predict':
        if not (a.ladders and a.runner and a.root and a.out and a.max_hours is not None):
            ap.error('--stage predict 는 --ladders · --runner · --root · --max-hours · --out 이 필요하다')
        return stage_predict(a, contract)
    if a.reverify:
        if not a.root:
            ap.error('--reverify 는 --root (킷 뿌리 — 침대를 다시 해시할 곳 · ★ 10-25 묶음 B · RCA2-03) 가 필요하다')
        return stage_verdict(a, contract)
    if not (a.runs and a.out and a.root):
        ap.error('--stage verdict 는 --runs · --root · --out 이 필요하다 (또는 --reverify <판정 폴더> --root <킷 뿌리>) — --root = 킷을 다시 '
                 '해시할 곳 (★ 10-25 묶음 B · RCA2-03)')
    return stage_verdict(a, contract)


if __name__ == '__main__':
    sys.exit(main())
