# 묶음 C (문서 · 웹앱) — C3 (Rint ② RR · 10-27)

> 반입 = 메인 (10-27) · 작업 트리 에이전트에게 준 지시 원문 (실행 중 · 결과 = `REPORT_C.md` 로 옮긴다) · 원문의 로컬 절대 경로만 뺐다.

## 비준 (1저자 10-27 원문)
- *"Rint는 권고대로 해도돼"* — 묶음 C 계획 Q1 = 지금 시작 · 에이전트 둘 (코드 = 따로 · 문서/웹앱 = 이 지시서) · 시험 먼저.
- *"11월 전체를 full로 사용할 수 있게 되어서 더 확실하게 하면 좋겠어 / 그렇다고 너무 늘리지는 말고"* — 범위는 그대로 · 뜻 바꿈 없음 · 확인을 더 꼼꼼히.

## 입력 (먼저 다 읽는다)
- `docs/reviews/rint2_rr_fix_evidence_20261023/BRIEF.md` — 전체 규칙 · **묶음 C 절의 C3** (이 지시서의 범위 원문).
- 수정 계획 `docs/reviews/rint2_rereview_fix_plan_20261022.md` — §2 (Q5 · Q6 · Q7 · **쉽게 말하면 ⑥ 원문**) · §3 표의 RCA2-07 줄 · "문서" 줄.
- 판정문 `docs/reviews/codex_review_rint2_rereview_20261022.md` (RCA2-07 · C3 · C6 #4 · #6 · #7 · #17 · #22 · #27 · #29 · RCA-11).
- Codex 회차 ① `docs/reviews/codex_review_rint2_rr_round1_20261026.md` §7 끝 (시간 산술 재현 = 추정의 산술만 · 처리량 · 마감 보증 아님 · 하한 한정 유지) · §9 (세 origin 표본 W 0.293 PASS ↔ 고정 8 평균 W 0.680 WEAK · all3 SV 요청 = corner 12 / origin 0 / origin8 0).
- Q9 설계 `docs/reviews/rint2_rr_fix_evidence_20261023/q9_predict_units_design.md` §6 (시간표 꼴) · 시간 자료 `docs/reviews/rint2_rr_fix_evidence_20261023/q9_time_budget.json` (`docs/reviews/rint2_rr_fix_evidence_20261023/q9_time_budget.py` 로 다시 만들 수 있다).
- 묶음 B″ 보고 `docs/reviews/rint2_rr_fix_evidence_20261023/REPORT_B2.md` §12 결정 3 (웹앱 SV 줄 문구 · 1저자 10-26 *"권고대로 해"* = 다음 웹앱 묶음 = 지금).
- 등록 R `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` (고칠 자리).
- 웹앱: SV 줄 = `webapp/templates/mpm_lab.html` (Jinja 행 · JS 행 둘 다) · 시험 `webapp/test_ca_ext_labels.py` (W17) · 설명 페이지 `webapp/static/explain/rint_overview_20261021.html` · 시험 `webapp/test_rint_explainer_page.py` (상자 ④ · ⑤ 가 들어간 꼴을 보고 ⑥ 을 같은 꼴로).

## 시작
- 시작 SHA = `5288ff3c4` (메인).  `git rev-parse HEAD` 가 다르면 `git checkout -B rr-fix-c-docs 5288ff3c4`.
- 가지 이름 = `rr-fix-c-docs`.

## 범위 (BRIEF.md C3 에서)
1. **RCA2-07 · Q7 (가)** — 등록 R :94–95 · 586 (줄 번호는 지금 판에서 찾아 맞춘다) = "각 연장 단계 비 ≤ 100 · 총 팽창 상계 없음".  (구현 주석 `scripts/rint_r_chain.py` 쪽은 코드 에이전트 몫 — 이 에이전트는 코드 파일을 고치지 않는다.)
2. **§10-4 시간표** = Q9 설계 §6 꼴 (all3 · 기계 1 · 2 · 3 대 · 예측 나눔 유무 · 추정 표지 · 하한 낙관 표지 · 넘침 86.7 – 104.9 h · 값 = `q9_time_budget.json` 그대로) + 판정문 probe 의 82 상당량 205.806–248.888 h 를 "R_j0 만의 옛 가정 (`SELF-129`)" 으로 병기 · Codex 회차 ① 의 "추정의 산술만 재현 · 처리량 · 마감 보증 아님" 한정.
3. **§10-4 문장 3** — 허용 기계 = kgy · gabia · v100 (Q3-b 닫힘 · v100 = 1저자 요청 때만).
4. **Q5 (가) 판정 문장** = "arm0 모서리 SV 가드" (8 팔 평균 envelope 에 SV 비의존을 옮겨 적지 않는다) · **Q6 (가) 결과 문장** = "표본 origin 판정 (확대된 모서리는 8 팔 평균)" (세 표본 결과를 8 팔 평균 결과로 부르지 않는다) — 등록 R 에서 해당 문장이 있는 자리 전부.
5. **수정 계획 §3 "문서" 줄 전부** — C3 "드물게 범위 밖일 수 있다" → "범위 밖일 수 있음" · C6 #4 · #6 · #7 · #17 · #22 · #27 · #29 · RCA-11 = 새 S0 실측 뒤 재판정 (줄마다 판정문의 문구를 따른다 · 뜻을 넓히지 않는다).
6. **쉽게 말하면 ⑥** — 수정 계획 §2 의 상자 ⑥ 원문 그대로를 등록 R (상자 ④ · ⑤ 가 있는 자리와 같은 꼴) 과 웹앱 설명 페이지 (상자 ④ · ⑤ 와 같은 꼴 · 머리 `sub` 줄 갱신 · 날짜 10-27 · 1저자 원문) 에 넣는다.  **시험 먼저** (`webapp/test_rint_explainer_page.py` 에 상자 ⑥ 시험 → 고치기 전 실패 확인 → 넣기 → 통과).
7. **웹앱 SV 줄 문구** (B″ 결정 3) — "봉인 원천 · 없음 = SV_UNCHECKED" → "봉인 원천 · 없음 · 실패 = SV_UNCHECKED" (Jinja · JS 두 행) · **시험 먼저** (`webapp/test_ca_ext_labels.py` W17).
8. **등록 R 머리 줄** — 묶음 C 의 자리를 덧붙인다 (지금 = 문서 C3 반영 · 코드 C1 · C2 = 진행 중 · 등록 §10-1 · §10-2 · §10-3 · ㊵ 의 Q9 개정 = 구현 이름이 나온 뒤 메인).

## 하지 않는 것
- **Q9 설계 §7 의 등록 개정** (㊵ · §4-1 · §10-1 CLI · §10-2 · §10-3 새 이름 · 시도 원장 · 순서 · 칼날 · 실행 환경 줄) — 코드 에이전트가 구현 이름을 정한 뒤 메인이 한다.  (위 3 의 기계 목록 문장만 이 에이전트.)
- 코드 (`scripts/` 아래 .py · .sh) · 원장 (`docs/reviews/findings.json`) · Q9 설계 · CLAUDE.md 고치기.
- 숫자를 새로 만들기 (시간표 값 = `q9_time_budget.json` 그대로 · 모르는 값은 "추정" · "미측정").
- push · fetch · `scripts/check_all.sh` · 다른 호스트 접속 · 메인 checkout  건드리기.
- 문서에 너의 커밋 SHA 를 적지 않는다 (`SELF-116` · SHA 는 보고에만).
- 뜻이 바뀌는 자리를 만나면 고르지 말고 "결정 필요" 로 보고한다.

## 더 확실하게 (1저자 10-27)
- 고친 문장마다 판정문 · 수정 계획의 원문 줄을 대어 본다 (보고 표 = 자리 · 옛 문구 · 새 문구 · 근거 줄).
- 웹앱 시험은 고치기 전 판에서 실패를 확인한 뒤 고친다 (보고 = 고치기 전 → 뒤 수).
- 문서 숫자는 `q9_time_budget.json` 과 한 자씩 대조 (보고에 대조 표).
- `python3 scripts/check_doc_refs.py` · `python3 scripts/check_review_findings.py` · `python3 scripts/check_review_findings.py --ban-sweep` (오래 걸리면 고친 파일만 대상으로 같은 검사 함수) rc 0.

## 커밋
- 항목마다 커밋 하나 (웹앱 둘 = 시험 커밋 → 고침 커밋).  메시지에 `author 10-27 approved bundle C` · 끝 두 줄:
  - `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`
  - `Claude-Session: https://claude.ai/code/session_01H191Ni4xzj9H5ftstAm7Ft`

## 보고 (마지막 메시지 · 표 위주)
- 커밋 목록 · 고친 자리 표 (파일:줄 · 옛 → 새 · 근거) · 웹앱 시험 고치기 전 → 뒤 · 숫자 대조 표 · 결정 필요 · 한정.
- 숫자 · 전칭은 실행 출력으로만 (`SELF-124`).

## 규칙
- BRIEF.md "규칙" 절 그대로 (python `-I` · 스레드 1 · 디스크 = 사본은 지운다 · 남은 디스크 약 6 GB).
