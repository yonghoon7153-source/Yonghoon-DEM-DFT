# Rint ② 재검토 결함 고치기 (이름 `RR` · 10-23 · 1저자 비준)

## 비준 (1저자 10-23 원문)
- *"다 권고대로 해줘"*.
  - 범위 = 수정 계획 `docs/reviews/rint2_rereview_fix_plan_20261022.md` 의 Q1–Q8 전부 (가) + §3 "결정 없이 고치는 것" 전부.
- 숫자는 이번에 정하지 않는다: 시간 상한 · 최대 시도 수 · 기계 목록 · s_min · SV 문턱 · 점수 상한 · 역상폭 상한.
  - 이 숫자들은 SBE 숫자 탐침 뒤 · DBE 단계 2 열람 전에 1저자가 봉인한다 (수정 계획 머리 · 판정문 §6 C2-3).
  - 코드는 칸과 검사만 만든다.  기본값 숫자를 넣지 않는다.

## 입력 (먼저 다 읽는다)
- 수정 계획 (위): §2 Q1–Q8 · §3 표 · 쉽게 말하면 상자 ④ ⑤ ⑥.
- 판정문 `docs/reviews/codex_review_rint2_rereview_20261022.md`.
  - §4 = RCA2-01–08 의 자리 · 반례 · 최소 해결.
  - §7 = C6 표.  §8 = DBE R 단조 · SV 범위 · origin.  §9 = 최소 해제 목록.
- 증거 `docs/reviews/codex_rint2_rereview_evidence_20261022/`.
  - 탐침: `registration/probe_registration_current.py` · `certificate/probe_certificate.py` · `certificate/run_selected_tests.py` · `geometry/run_review.py` · `probes/provenance_probe.py` · `probes/s0_integration_probe.py --fixture-argv`.
  - 탐침은 환경 변수 `RINT_REVIEW_SOURCE` 로 소스 트리를 받는다.
  - 우리 재현 = `docs/reviews/codex_rint2_rereview_evidence_20261022/_repro_ours_20261022/README.md` (돌리는 법 §5 · `docs/reviews/codex_rint2_rereview_evidence_20261022/_repro_ours_20261022/tools/run_all.sh` · `docs/reviews/codex_rint2_rereview_evidence_20261022/_repro_ours_20261022/tools/run_with_dir.py` · `docs/reviews/codex_rint2_rereview_evidence_20261022/_repro_ours_20261022/tools/compare_json.py`).
- 등록 R `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` · 설계 v1 `docs/reviews/rint_carbon_additive_design_v1_20261020.md`.
- 원장 `docs/reviews/findings.json`: RCA2-01–09 (open) · RCA-06 (claimed_fixed · `partial_note`).
- 웹앱
  - SV 줄 = `webapp/templates/mpm_lab.html` (Jinja 행 · JS 행 둘 다) · 시험 `webapp/test_ca_ext_labels.py`.
  - 설명 = `webapp/static/explain/rint_overview_20261021.html` · 시험 `webapp/test_rint_explainer_page.py`.
- 지난 회차 보고 (회귀 목록 · 끈 경로 비교 방법) = `docs/reviews/rint2_pf2_fix_evidence_20261022/stage2_report.md` §3.

## 작업 트리 · 커밋
- 너의 격리 작업 트리에서 시작한다.
  - 먼저 `git rev-parse HEAD` 가 시작 SHA (실행 지시문에 적힘) 와 같은지 본다.
  - 다르면 `git checkout -B <가지 이름> <시작 SHA>` 로 맞춘다.  가지 이름도 실행 지시문에 적힘.
- 각 항목 = 시험 먼저 (고치기 전 판에서 실패 확인) → 구현 → 커밋 하나.
- 커밋 메시지에 `author 10-23 ratified Q1-Q8` 를 넣는다.  끝에 두 줄을 붙인다:
  - `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`
  - `Claude-Session: https://claude.ai/code/session_019HKnbzGsY9U5Gyw4qGqqzA`
- 메인은 네 가지를 fast-forward 로 받는다.  그러니 네 커밋 SHA 는 메인에서도 같다.

---

## 묶음 A — Q1 · RCA2-04 · Q8 · RCA2-06 · RCA2-08 · 웹앱 · 상자 ④

### A1. RCA2-08 — 합산 넘침 (작은 것부터)
- `scripts/step3_conv_cert.py` 의 최종 U 합 (`fsum` · :476) · W 합 (:553) 을 보호한다.
  - 넘침이면 예외 대신 `NOT_CERTIFIABLE` 을 낸다.  사유 이름은 기존 꼴을 따른다.
- 같은 부류: :344 `tol_r` 의 중간 넘침 (우리 재현 stderr 의 `RuntimeWarning: overflow encountered in add`) 도 같은 방식으로 막는다.
- 시험 먼저
  - 판정문 꼴: 독립 노드 5 개 · gb = gt = 8e307 · p = 0.5.
  - 고치기 전 = `OverflowError` 확인.  고친 뒤 = `NOT_CERTIFIABLE` · 경고 없음 (경고를 오류로 바꿔 확인).
  - 정상 회로의 증서는 비트 같아야 한다.

### A2. Q1 (가) RCA2-01 + RCA2-04 — SV 문턱을 증서 구간으로 판정
1. 생산자 (`scripts/carbon_junction.py` · 증서 생산 :2463 쪽)
   - 주 해와 각 cut 끝 (아래 판 · 위 판) 마다 증서 구간을 SV 기록에 남긴다.
   - 남길 것 = 목표량 구간 (`target_lo` · `target_hi`) · G 와의 결합 · 분자.
2. 투영 (`scripts/ca_ext_svcf.py` 의 `sv_cf_record` :75–77)
   - 구간을 버리지 않는다.
   - `chain_view` (:303) 가 구간 비를 계산한다.
3. 판정 (`scripts/rint_r_chain.py` 의 `sv_assess` :554 · :583–586)
   - 아래비 = Gfull_lo / Gcut_lower_hi.  위비 = Gfull_hi / Gcut_upper_lo.
   - 아래비 > t → `SV_DEPENDENT`.  위비 ≤ t → 표지 없음.  나머지 → `SV_UNCHECKED`.
   - ∞ 는 topology 가 증명한 0 분모에만 쓴다 (cut 해 증서가 영값 위상인 꼴).
   - 구간 아래끝이 0 이하인데 topology 증명이 없으면, 위비가 정해지지 않은 것이다 (그러니 "위비 ≤ t" 가 아니다).
     - 이 경우의 칸 · 이름은 기존 꼴을 따른다.
     - 새 상태 이름이 꼭 필요하면 만들되, 보고에 적는다.
   - 그대로 두는 규칙: 모서리 묶기 = "하나라도" · 두 표지 동시 가능 (C6 #1) · 아래를 못 읽으면 `SV_UNCHECKED` (C6 #2).
   - nominal 비는 기록에 남겨도 된다.  판정에는 쓰지 않는다.
4. 기록 계약 (`sv_cf_problem` :196 · 200 · 259 · 실제 소비자 `scripts/run_contract.py:756`)
   - computed 끝마다 증서가 있어야 한다.  없으면 거부.
   - 증서를 그 끝의 G · target · 분자 · rule · version 과 결합한다.  다른 회로의 증서면 거부.
   - `bracket_rule` 은 등록된 값만 받는다.
   - `n_unsplit` · 제거 수는 정수이고 의미 범위 안이어야 한다.
     - 실제 census 와 일관해야 한다.  제거 수 ↔ 못 가른 덩어리 수의 관계는 등록 · 생산자 정의대로.
     - 10^400 같은 범위 밖 값은 거부.
   - 무증서 실행 = 진단 지위 표지.  사슬은 그것을 R 판정 입력으로 받지 않는다.
5. 시험 먼저 (고치기 전 판에서 실패 확인)
   - 판정문 실제 반례 (`geometry/run_review.py` → `actual_certified_threshold_crossing`).
     - nominal 10.291249475344962 < 문턱 10.291251705345072 · 증서 구간 [10.29125393534377, 10.291253935346631] → 기대 `SV_DEPENDENT`.
     - 같은 꼴 (첫 선형 해 벡터에만 +1e-8) 을 상주 시험으로 옮긴다.  무거우면 `--long` 쪽에 둔다.
   - 경계: 양쪽 · 같음 (위비 = t → 표지 없음 · 아래비 = t → `SV_DEPENDENT` 아님) · ∞ (topology).
   - 실패 꼴: 한 끝 실패 (증서 실패 · 미수렴) · 무증서 · 외부 증서 · 임의 rule · 제거 수 변이 · 10^400.
6. 웹앱 (같은 묶음 · 시험 먼저 · Jinja · JS 두 행)
   - SV 줄에 증서 구간 비 [아래, 위] 를 판정 근거로 보인다.
   - nominal 은 있으면 따로 보이고 "판정 아님" 을 붙인다.
   - 무증서 = "진단 (판정 입력 아님)".
   - 설명 페이지에 쉽게 말하면 상자 ④ 를 넣는다.
     - 수정 계획 §2 문안을 그대로 옮긴다.
     - 기존 상자 스타일을 따른다.  다크 모드에서도 읽혀야 한다.
7. 등록 R 개정 (결과 0 건)
   - §5-6 SV 행 = 구간 판정 · 증서 필수 · 무증서 = 진단.
   - :177 · 179 · 435 의 "증서 여유 없음" 서술을 바로잡는다.
   - 상자 ④ 를 옮긴다.
   - 머리에 한 줄: *"(10-23 · Codex 재검토 RCA2-01 · 04 · 08 · 09 · 06 · 1저자 Q1 (가) · Q8 (가)) 고친 자리 = … · 결과 0 건"*.
   - 생산자 한정어 (`CJUNC_QUALIFIERS` 등) 의 괄호 판정 문장에 "증서 구간" 을 반영한다.  웹앱은 생산자 문장을 그대로 띄운다 (사본을 만들지 않는다).

### A3. Q8 (가) RCA2-09 — DBE R 단조 방어 검사
- 자리 = `Predict` (`scripts/rint_r_chain.py:1731–1782`).
- 이미 구한 값으로, 같은 origin · 같은 최종 추정량의 σ(R_lo) ≥ σ(R_0) ≥ σ(R_hi) 를 증서 구간끼리 검사한다.
  - 구간이 단조와 모순일 때만 멈춘다.  예: σ(R_lo) 구간의 위끝 < σ(R_0) 구간의 아래끝.
  - 멈춤 이름 = `R_MONOTONE_VIOLATION`.  새 숫자 없음 · 추가 풀이 없음.
- 그 자리에 증서 구간이 없고 nominal 값만 있으면, 고르지 말고 "결정 필요" 로 보고한다.
  - 판정문 §8 은 "증서/등록 ln 여유" 라고 적었다.  등록에 이미 있는 여유가 있으면 그것을 쓰고, 그 이름을 보고한다.
- 시험 먼저
  - 판정문 꼴 (R = 0.5 / 1 / 2 에 σ = 4.2 / 4.7 / 4.4 mS/cm) → 멈춤.
  - 정상 단조 → 통과.
  - 증서 띠 안에서만 겹치는 비단조 (구간끼리 모순 아님) → 통과.
- 멈춤 이름을 등록 §10-2 / §10-3 목록과 차단 집합에 넣는다 (판정문 §8 R3-Q10: 닫힌 집합 · 새 필수 관문이면 집합도 갱신).

### A4. RCA2-06 — 회귀 사각 · 실패 상태
- F4: 두 성분 fixture 를 상주 시험으로 넣는다.
  - 꼴 = 독립 4 rail · 두 SDCP 성분 (판정문 §4: 참 다리 영향 1 · G 47.61904761904763 · 괄호 [1, ∞]).
  - 전 셀 · 판 결합 제거를 확인한다.
  - 첫 성분만 지우는 변이 (위비 2) 가 새 시험에 걸려야 한다 (지금 QD2 13/13 은 그 변이에서도 통과한다).
- F6: census 불일치 (`unsplit_census_mismatch`) = 구조화 실패를 끝-끝 보존한다.
  - 실제 소비자 경로 (`scripts/run_contract.py:759`) 로 부르는 시험을 쓴다.  시험 문구도 실제 경로에 맞춘다.
  - `KNOWN_STATUSES` 에 이름만 더하는 것으로 끝내지 않는다.

### A5. 원장
- RCA2-01 · 04 · 06 · 08 · 09 → `claimed_fixed`.
  - `claimed_fixed_sha` = 고침 커밋.  `evidence_tests` = 실제 시험 이름 · 수.  필드는 기존 꼴 (예: RCA-06) 을 따른다.
- RCA-06 `partial_note` 에 한 줄 덧붙인다: 닫는 조건 RCA2-01 고침 = 이 커밋 · 검증 = Codex.
- 새 ID 는 만들지 않는다.  `python3 scripts/check_review_findings.py` rc 0.

### A6. 회귀 · 끈 경로 · 변이 · 탐침 재실행
- 회귀 (지난 회차 보고 §3 과 같은 목록)
  - 빠른 판: chain · e2e · b6 · runner · z1 · z3 · verdict · carbon_junction · s0 · target_cert · conv_cert · ptfe · run_contract selftest · step3 selftest 둘.
  - 웹앱: `test_ca_ext_labels` · `test_rint_explainer_page` · `test_rint_scope_labels` 를 포함한 지난 회차 웹앱 목록.
  - `scripts/check_method_discipline.py` 두 실행 (인자 없이 · `--selftest`).
  - `--long` = `HEAVY_EXCLUSIVE=1 HEAVY_LOCK_DIR=<SCRATCH> bash docs/handoff_rint_pf2_20261022/heavy.sh …`.
- 끈 경로: 노브를 안 켠 생산 경로의 매니페스트 · σ 가 고치기 전과 비트 같아야 한다 (지난 회차와 같은 비교 방법).
- 변이: 고친 줄마다 한 줄 되돌린 변이가 새 시험에 걸리는지 표로 보인다.
- 탐침 재실행: 판정문 탐침을 무변경으로, 고친 트리 (`RINT_REVIEW_SOURCE` = 작업 트리) 에서 다시 돌린다.
  - 증거 폴더를 `<SCRATCH>` 로 복사해서 돌린다 (리포 안에서 출력 파일을 만들지 않는다).
  - 표: 반례 → 거부 · 정상 → 그대로.  바뀐 판정값은 수정 신호다.

---

## 묶음 B — Q2 같은 코드 · Q3 같은 침대 (다음 에이전트 · 묶음 A 가 메인에 들어간 뒤)

> (10-23 · 1저자) R 은 kgy · gabia 두 기계 (v100 = 요청 때만) 에서 돈다.  허용 기계 목록 = kgy · gabia · v100 (계획 칸 · 값은 봉인 때 1저자 · 코드에 박지 않는다).  그래서 B1 ④ (상대 경로) · ⑤ (환경) 는 기계를 넘어 성립해야 한다.

### B1. Q2 (가) RCA2-02 + F5 — 같은 코드의 보장
- 자리 = `scripts/rint_r_chain.py:154 · 617–625 · 1017–1080` · S0 코드 비교 :945.
1. `git rev-parse` · `git status` 둘의 종료코드를 본다.
   - HEAD = 40-hex · dirty = 엄격한 False 일 때만 통과.
   - 조회 실패 · git 밖 = 미확인 = 멈춤.  False 로 바꾸지 않는다 (C6 #13).
2. untracked 범위 = (가-1): ignore 밖 untracked 전부를 dirty 로 센다.
3. 한 단계 안에서 chain ↔ runner 의 HEAD · 파일 지문을 서로 대조한다 (자기 요약끼리 비교 아님).
4. 파일 지문 키 = 저장소 상대 경로.  절대경로 대조는 뺀다 (C6 #14 · 기계마다 경로가 다르다).
   - 지문 목록에 모듈을 더한다: `ca_ext_cjunc.py` · `additives.py` · `se_material.py` · `lens_geometry.py` · `step4_dyn.py` · `rint_cycle_traj.py`.
   - `se_material.py` · `lens_geometry.py` 는 봉인 32 파일이다.  읽고 해시만 한다 (고치지 않는다).
5. 환경 지문을 단계마다 기록한다.
   - python · numpy · scipy 판 = 모든 단계 · 기계 사이에서 같아야 한다.  다르면 멈춘다.
   - cupy · CUDA 런타임 · GPU 이름 = 기록만 한다 (기계마다 다를 수 있음 · 판정에 쓰지 않음 · Codex 회차 ① Q-E 답에 따라 나중에 조일 수 있다).
6. F5: `plan_source` 문법 = `commit:` + 40-hex.
   - 그 커밋 안 계획 파일의 blob sha256 이 계획 sha256 과 같아야 한다.
- 시험 먼저: 판정문 `probes/provenance_probe.py` 의 F1 · F2 · F5 꼴 (git 밖 · status rc 128 · chain/runner 판 · 파일 차이 · `commit:`) → 멈춤.  같은 정상 코드 → 통과.  경로만 다른 같은 코드 (두 기계 꼴) → 통과.  numpy 판만 다름 → 멈춤.

### B2. Q3 (가) RCA2-03 — 같은 침대의 보장 (S0 → R)
- 자리 = `scripts/ca_s0_census.py:1583–1606` · `scripts/rint_r_chain.py:882–893 · 896–981 · 1327–1332 · 1858`.
- S0 보고의 `inputs` (역할 7 개 파일 sha256 · 크기 · `metrics` 상자 · 두께) 를 사슬 요약에 보존한다.
- R 런 직전과 재판정 때, 같은 발견 함수로 실제 킷 파일을 다시 해시해 대조한다.  다르면 멈춘다.  (기계마다 자기 사본을 다시 해시한다 — 사본은 바이트 같아야 한다.)
- 공통 원침대 지문 (원 입력 · 설정) 과 파생 격자 지문 (vox · origin · 격자 · `cells_by_sid`) 을 나눈다.
  - 파생 지문은 같은 규약일 때만 대조한다.  경로 문자열은 대조에서 뺀다.
- 재압밀 · 재생성 침대 = 새 S0.  등록 §2-1 · §11 에 이 문장을 넣는다.
- 시험 먼저: 판정문 `probes/s0_integration_probe.py --fixture-argv` 꼴.
  - 섬유 0.04 이동 · 셀 수 같음 · 접합 1 → 0 → 멈춤.
  - 정상 단계 · 격자 · origin 변화 → 통과.  경로만 다른 같은 사본 → 통과.

### B3. 원장 · 회귀
- RCA2-02 · 03 → `claimed_fixed` (A5 와 같은 방식).
- 회귀 · 끈 경로 · 변이 · 탐침 재실행 = A6 와 같다.
- 등록 R 머리 줄에 B 묶음 자리를 덧붙인다 · 웹앱 설명 페이지 · 등록 R 에 쉽게 말하면 상자 ⑤ (수정 계획 §2 문안 그대로 · 시험 먼저).
- (10-23 1저자 *"ㄱ"* · 묶음 A 보고 §10 결정 11) 끈 경로 비교 b6 `--only=B` · z3 O 에 SV 켬 꼴 · 허용 행을 더한다 (시험만 · 생산 코드 변경 없음 · 허용 행 = 묶음 A · A′ 의 SV 새 칸 (위상 수 · rule 투영 포함) · 한정어 한 문장).
- (10-23 사전 공격 리뷰 D6 · 판정문 C6 #14 · Q9 설계 개정 1 §3-3) 코드 키 · `check_after_main` 대조의 절대 경로 → 저장소 상대 경로 · sha · 환경 지문에 BLAS 계산 경로 (`OPENBLAS_CORETYPE` · 라이브러리 정보) = 기록만 (기계 간 float 같음 비교에 쓰지 않는다 · 시험 먼저).

---

## 묶음 C — Q4 재시도 봉인 · Q9 예측 단위 · 문서 · 시간표 (묶음 B 뒤 · Codex 회차 ① 의 Q9 설계 답을 본 뒤)

### C1. Q4 (가) RCA2-05 — 시간 · 중단 · 재시도 봉인
- 자리 = `scripts/rint_r_chain.py:1789 · 1799 · 1894 · 2043 · 2572`.
- R 계획 JSON 에 실행 정책 칸을 넣는다.  같은 봉인 (계획 sha256) 안에 든다.
  - 시간 상한: `--max-hours` 가 계획 값과 같아야 한다.  다르면 거부.
  - 최대 시도 수.
  - 재시도 규칙: 결과 전 멈춤 (관문 · 환경 · 기계 자원) 만 재시도한다.  결과 뒤 멈춤 (불수렴 · 사다리 소진 · 수치 · 물리) 은 같은 등록의 재시도가 아니다.
  - 동일 설정 요건: 계획 · 코드 · 침대 지문.
  - 채택 순서: 처음 완주한 시도.
  - 시도 폴더 `attempt_<n>`: 실패 시도 · 원 사유 · 다음 attempt ID 를 보존한다 (지금의 빈 폴더 요구를 대신한다).
  - 기계 귀속: 팔마다 기계 이름 필수 · 빈 이름 금지 · 계획의 허용 기계 목록 안 (C6 #15 · Q11).
  - 문서 숫자 (s_min 등) = 계획 JSON 에서 생성하고 정확 대조한다 (C6 #30).
    - 생성기 · 대조 검사는 fixture 계획으로 시험한다.
    - 등록 본문의 실제 숫자 칸은 "SBE 탐침 뒤 봉인" 그대로 둔다.
- 칸 값 (숫자 · 기계 목록) 은 넣지 않는다.  봉인 전 계획이면 R 진입을 거부하는 쪽으로 둔다.
- 시험 먼저: `--max-hours` 불일치 · 결과 뒤 멈춤의 재시도 · 다른 설정의 재시도 · 빈 기계 이름 · 목록 밖 기계 → 거부.  결과 전 멈춤의 재시도 · 처음 완주 채택 → 통과.

### C2. Q9 (가) — 예측 단계를 단위로 나눠 여러 기계에서
- 설계 = `docs/reviews/rint2_rr_fix_evidence_20261023/q9_predict_units_design.md` (단위 실행 → 합치기 → 넘침 런 → 합치기 · 같음 시험 · 음성 시험 · 등록 개정 목록).
- Codex 회차 ① 의 Q-A – Q-F 답을 반영한다.  답이 설계와 다르면 고르지 말고 "결정 필요" 로 보고한다.
- 시험 먼저 (설계 §8).  끈 경로 = 지금의 `--stage predict` 한 번 = 비트 같음.

### C3. 문서 (결정 없음 · 뜻 바꿈 없음)
- RCA2-07 · Q7 (가): 등록 R :94–95 · 586 · 구현 주석 (`rint_r_chain.py:1611–1634`) = "각 연장 단계 비 ≤ 100 · 총 팽창 상계 없음".
- §10-4 시간표 = Q9 설계 §6 꼴 (all3 · 기계 1 · 2 · 3 대 · 나눔 유무 · 추정 표지 · `docs/reviews/rint2_rr_fix_evidence_20261023/q9_time_budget.json`).  판정문 `registration/probe_registration_current.py` 의 82 상당량 (205.806–248.888 h) 은 R_j0 만의 옛 가정으로 병기한다 (`SELF-129`).
- §10-4 문장 3 · ㊵ · §10-1 · §10-2 · §10-3 = Q9 설계 §7.  기계 = kgy · gabia · v100 (Q3-b 닫힘).
- Q5 (가): 판정 문장 = "arm0 모서리 SV 가드".  8 팔 평균 envelope 에 SV 비의존을 옮겨 적지 않는다.
- Q6 (가): 결과 문장 = "표본 origin 판정 (확대된 모서리는 8 팔 평균)".  세 표본 결과를 8 팔 평균 결과로 부르지 않는다.
- 수정 계획 §3 "문서" 줄 전부: C3 "드물게 범위 밖일 수 있다" → "범위 밖일 수 있음" · C6 #4 · #6 · #7 · #17 · #22 · #27 · #29 · RCA-11 = 새 S0 실측 뒤 재판정.
- 웹앱 설명 페이지 · 등록 R 에 쉽게 말하면 상자 ⑥ (수정 계획 §2 문안 그대로) · 시험 먼저.
- 등록 머리 줄에 C 묶음 자리를 덧붙인다.

### C4. 원장 · 회귀
- RCA2-05 · 07 → `claimed_fixed` (A5 와 같은 방식).
- 회귀 · 끈 경로 · 변이 · 탐침 재실행 = A6 와 같다.

---

## 보고
- 마지막 메시지는 60 줄 이내.
- 긴 보고 = 마지막 메시지에 담는다 (10-23 · 하네스가 하위 에이전트의 보고 `.md` 파일 쓰기를 막는다 — 메인이 이 폴더 (`docs/reviews/rint2_rr_fix_evidence_20261023/`) 에 `REPORT_A.md` 꼴로 옮겨 적는다 · 묶음 B = `REPORT_B.md` · 묶음 C = `REPORT_C.md`).  그래서 마지막 메시지는 60 줄을 넘어도 된다 (표 위주).
  - 보고 파일에 적는 경로는 리포에 있는 것만 적는다 (`<SCRATCH>` 경로는 적지 않는다 · `scripts/check_doc_refs.py` rc 0).
- 담을 것:
  - 커밋 목록 (각 무엇).
  - 시험 수 고치기 전 → 뒤.
  - 회귀 표 · 끈 경로.
  - 변이 표 · 탐침 재실행 표.
  - 문서 고친 자리.
  - 원장 변경.
  - `S0_SAME_FILES` (`scripts/rint_r_chain.py:158`) 일곱 파일 중 바뀐 파일 (바뀌면 S0 단계 1 보고를 R 전에 다시 만들어야 한다).
  - 결정 필요 (고르지 않은 자리).

## 규칙
- python `-I` · `nice -n 19` · `OPENBLAS_NUM_THREADS=1` (OMP · MKL · NUMEXPR 도 1).
- push · fetch · `scripts/check_all.sh` 는 하지 않는다.
- 봉인 32 파일 (`scripts/run_network_194_parallel.py` 의 CODE_FILES) 은 손대지 않는다.
- 등록에 없는 새 규칙 · 숫자를 만들지 않는다 (비준된 Q1–Q8 · §3 목록만).
  - 등록이 정하지 않은 자리를 만나면 고르지 말고 "결정 필요" 로 보고한다.
- 숫자 · 전칭 ("전부" · "무변경" · "N/N" · "비트 같음") 은 실행 출력으로만 적는다 (SELF-124).  범위와 시험 판을 같이 적는다.
- 문서에 도달할 수 없는 SHA 를 쓰지 않는다 (SELF-116).
- 각 커밋 전에 `python3 scripts/check_doc_refs.py` · `python3 scripts/check_review_findings.py` rc 0.
- 디스크: 사본은 다 쓴 뒤 지운다.
- `<SCRATCH>` = 너의 scratchpad.
