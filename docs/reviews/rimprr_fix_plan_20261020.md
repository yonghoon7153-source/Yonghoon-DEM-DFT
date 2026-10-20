# Rint 조인 재확인 (10-20) — RIMPRR-01 · RIMPR-03 · 04 · SELF-124 수정 계획 (2026-10-20 · 등록 시 결과 0 건 · ✅ 비준 10-20 · 수정 결과 = §3 끝)

> 근거 = Codex 재확인 `docs/reviews/codex_review_rint_join_rimpr_q7_recheck_20261020.md` (검토 핀 `2b9efa253` · 대조 핀 `dcb97f1ed`) · 증거 `docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/` (우리 트리 재현 = 판정값 차이 0 · `_README_import.md`).
> 판정 요지: `RIMPR-01` · `02` · Q7 범위 한정 닫힘 (verified) · 새 P1 · P2 없음 · 새 P3 `RIMPRR-01` (원장 `RIMPR-R01` — 원장 ID 규칙 접두 5 글자) · `RIMPR-04` 범위 보강 · `RIMPR-03` = ASCII 범위 명시면 연기 가능 · **①′ 정량 채택 · 생산 HOLD 유지**.
> 범위: 진단 관문 `scripts/rint_iface_join.py` (봉인 32 밖 — 두 Rint 커밋 ∩ `CODE_FILES` = 0 · 10-20 git 확인) · 시험 `scripts/test_rint_g2_join.py` · 문서.  생산 σ 경로 · iface 끔 경로 · 봉인 32 무변경.  **이 문서는 계획만 — 코드는 고치지 않았다.**

## 1. 결함과 최소 해결 (판정문 §3 · §4 · §1 · §7 그대로)

| ID | 결함 | 자리 (핀 `2b9efa253`) | 최소 해결 (판정문) |
|---|---|---|---|
| `RIMPR-R01` (= Codex `RIMPRR-01`) P3 | 구역 분류 `startswith()` + 헤더 표지 전역 `replace()` → `ITEM: ATOMSid …` · `ITEM: BOX BOUNDS ff ff ff ITEM: BOX BOUNDS` (및 경계 없음 · 반복 · 후첨 10 건) 이 조인 PASS · 정량 ACCEPT · 소비 배열은 정상과 같음 · 대조 핀에도 있음 | `scripts/rint_iface_join.py:278–279 · 298 · 302` (step / count 의 명시 헤더 검사 `:286–288` 가 이 셋에는 없다) | 구역 이름 = 정확한 단어 경계 · 표지 하나만 앞에서 제거 · 나머지 토큰은 기존 열 · 상자 검사로 · 정상 공백 · 탭 · 쓰지 않는 진단 열은 일괄 금지하지 않음 · 두 사례 + contact 대응 상주 회귀 |
| `RIMPR-04` P3 (범위 보강) | 입력 유한 ≠ 계산 결과 유한 — 비-AM 두 구 x 1e160 → 거리 · 허용폭 norm inf → `inf > inf` 거짓 → 조인 PASS / 정량 ACCEPT (1e150 대조 = REJECT) · 한-AM 1e160 → `delta_bound_um` inf (후단 ledger 가 거부) · `sim_to_um` 1e160 → AM–AM 면적 inf | `scripts/rint_iface_join.py:641–645` · `:767` · `:799` | 연기 가능 (조건 넷 — 원장 note) · 정량 채택 전 결과 유한성 · 수치적으로 안정한 거리 · 오차폭 검토 · 범위 제한이면 명시적 입력 계약 |
| `RIMPR-03` P3 | 정수 정규식 `\d` 가 전각 · 아라비아-인도 숫자를 받는다 (수치 · ID 대응은 ASCII 와 같음) · ASCII 0 앞자리 정규화라 긴 유니코드 0 덧붙임은 거부될 수 있음 | `scripts/rint_iface_join.py:79` (`_INT_RE`) | ASCII 생산 덤프 범위 명시 + open 유지면 연기 가능 |
| `SELF-124` P3 | 요청서가 *"봉인 32 파일 무변경"* 을 범위 한정 없이 · 시험 수를 *"78/135 → 138/138"* (다른 두 시험 판) 로 적음 | `docs/reviews/codex_rint_join_rimpr_fix_recheck_request_20261020.md` 12 · 19 행 · 원장 RIMPR-01 · 02 evidence_tests 첫 줄 · 커밋 `3b9d51789` 메시지 (고칠 수 없음 = 기록만) | §7 권장 문장 · 현재 시험 138 을 옛 코드에 = 81/138 구분 |

## 2. 1저자가 정할 것

✅ 1저자 10-20 *"권고대로해"* — Q1 (가) · Q2 (가) · Q3 (가) · Q4 (가) · Q5 반영 · Q6 (나)

| Q | 결정 | 선택지 | 권고 |
|---|---|---|---|
| Q1 | `RIMPR-R01` 고침 방식 | (가) 머리 줄을 `ITEM:` 뒤 낱말로 토큰화해 구역 이름 (`TIMESTEP` · `NUMBER OF …` · `BOX BOUNDS` · `ATOMS` · `ENTRIES`) 을 **정확한 단어 경계**로 대조 → 표지 하나만 앞에서 제거 (슬라이스 · `removeprefix`) → 나머지 토큰은 기존 열 · 상자 플래그 검사에 그대로 (공백 · 탭 구분 · 쓰지 않는 진단 열 허용 그대로) — 예상 (시험 전): 경계 없음 · 붙여 쓴 반복 표지 (`ATOMSITEM:` · `BOUNDSITEM:` 꼴) = 모르는 절 (`frame_layout`) · 상자 표지 후첨 = 플래그 셋 아님 (`box_format`) · 행 표지 후첨 = 머리 열 수 ≠ 행 폭 (`row_width`) (나) 머리 줄 전체를 정규식 하나로 고정 — 열 이름 · 플래그 문법까지 새로 정의 | **(가)** — 판정문 최소 해결 그대로 · 바뀌는 곳 = 분류 · 표지 제거 두 자리뿐이고 열 · 상자 규칙은 그대로라 정상 `%g` 덤프 (real14 · case15 · gzip · CRLF · D19) 에 새 거짓 거부를 만들 길이 좁다 |
| Q2 | 시험 먼저 범위 | (가) 최소 반례 둘 (판정문 §3 문자열 그대로) + contact `ENTRIES` 대응 (경계 없음 · 반복 표지 · 행 표지 후첨) + 원자 쪽 반복 · 후첨 + 상자 경계 없음 · 반복 (Codex 독립 탐침 10 건 전부) + 정상 양성 그대로 (real14 · case15 · 접촉 0 행 · gzip · CRLF · 기존 빈 줄 규약 · D19 · 쓰지 않는 진단 열 · 공백 · 탭) → 고치기 전 판에서 새 반례 실패 확인 뒤 수정 (나) 최소 둘 + contact 대응만 | **(가)** — 판정문 요구 (두 사례 + contact 대응) 의 상위 집합 · 10 건은 이미 Codex 증거 (`docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/evidence/structure_results.json`) 에 입력 · 기대가 있어 옮기기만 하면 된다 |
| Q3 | `RIMPR-04` 지금 범위 | (가) 파생값 유한성 fail-closed — `:641–645` 의 거리 · 허용폭 (와 같은 부류 `:767` 반올림 폭 · `:799` 면적) 이 유한이 아니면 구조화 거부 (새 사유 코드 · 결과 0 건) + 1e160 반례 · 1e150 대조 상주 · 안정한 `hypot` 재작성 · 결과 유한성 전반 검토는 정량 채택 전 (나) 그대로 연기 (조건 넷 원장 기록 — 이미 적음) | **(가)** — 한 줄 꼴 fail-closed 로 알려진 false-PASS 를 막는 비용이 작고 조건 ③ (조인을 소비자 관문처럼 믿지 않음) 을 코드로 받친다 · 안정한 계산은 조건 ④ 대로 정량 채택 전 · 원장은 open 유지 (조건 ①) |
| Q4 | `RIMPR-03` | (가) 지금 — `_INT_RE` 의 `\d` → `[0-9]` (전각 · 아라비아-인도 숫자 = `int_token` 거부 · 반례 상주) (나) 연기 — *"ASCII 생산 덤프 지원"* 범위 명시 · open 유지 | **(가) 지금** — 한 글자 변경 · Q1 과 같은 파일 · 같은 시험 묶음 · 생산 덤프 (ASCII `%g`) 무영향 · 유니코드 0 덧붙임 문제도 같이 사라진다 |
| Q5 | 문서 정정 (`SELF-124`) | 요청서 12 행 → 판정문 §7 권장 문장 (*"이번 Rint 수정 두 커밋은 봉인 32 개를 변경하지 않았다. 대조 핀 이후의 다른 트랙 변경까지 포함한 전체 스냅샷의 동일성은 별도다."*) (⛔ 정정 10-20 `SELF-125` B: 원문은 "봉인 32개를" — 붙여 쓴다) · 19 행 → *"78/135 (시험 작성 중간 시점 · 135 개) → 138/138 · 현재 시험 138 을 옛 코드에 = 81/138"* · 원문은 지우지 않고 정정 표지 · 원장 첫 줄 = 이력 (verification_note 의 구분으로 충분) | **그대로 반영** — 다음 커밋에서 `SELF-124` claimed_fixed |
| Q6 | Codex 재확인 시점 | (가) 단독 짧은 재확인 (Q1 · Q3 · Q4 수정 diff + 탐침 재실행) (나) Rint ② 설계 리뷰 요청 (`docs/reviews/rint_carbon_additive_plan_20261020.md` Q12 = 구현 전 한 회차) 에 절을 나눠 함께 | **(나) 함께** — 셋 다 P3 · ①′ 정량 채택 HOLD 를 바꾸지 않고, S2 가 같은 조인 · 관문 위에 서므로 ② 구현 전에 고친 조인을 같은 회차에서 보는 편이 맞다 (② 요청이 늦어지면 (가) 로) |

## 3. 순서 (비준 뒤)

1. 시험 먼저 (고치기 전 실패 확인) — Q2 의 반례 (`RIMPR-R01` 10 건 · Q3 1e160 · Q4 전각) 를 `scripts/test_rint_g2_join.py` 에 · 정상 양성 묶음 그대로 · 고치기 전 판의 실패 수를 기록 (판 · 집합을 같이 적는다 — `SELF-124` 교훈).
2. 수정 (Q1 · Q3 · Q4) — 기존 시험 138 + `test_rint_g2_am_iface.py` 136 · `test_rint_g2_rrm.py` 55 · t4 · t43 · t2 · 두 selftest 그대로 통과 · iface 끔 무영향.
3. 문서 (Q5) — 요청서 정정 표지 · 원장 `RIMPR-R01` · `RIMPR-03` · `RIMPR-04` (Q3 가 (가) 여도 open 유지 — 조건 ①) · `SELF-124` claimed_fixed.
4. Codex (Q6) — 수정 diff + 이번 묶음 탐침 재실행 요청 (`docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/probes/structure_probe.py` ·
   `docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/probes/structure_minimal_replay.py` · `docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/probes/numeric_review.py` ·
   `docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/probes/numeric_overflow_replay.py` — 고친 뒤 기대: 헤더 반례 10 = 거부 · Q3 (가) 면 1e160 = 거부 · Q4 (가) 면 전각 정수 = 거부 · 그 밖 판정 그대로).

### 결과 (10-20 · 작업 트리 · `9845d526c` 바로 위 두 커밋 · push 안 함)

- **시험 먼저 `12d894c09`** (`scripts/test_rint_g2_join.py` 만 · 새 검사 68 = J12 26 · J12P 9 · J13 8 · J14 25): 고치기 전 코드 (`9845d526c` 판 `scripts/rint_iface_join.py`) 에 **152/206** — 실패 54 = 새 반례 전부 (J12 26 · J13 6 · J14 22) · 옛 138 + 새 양성 14 (J12P 9 · J13 ② 1e150 대조 2 · J14 ASCII 3) 통과.
- **수정 `a2cfd0365`** (`scripts/rint_iface_join.py` · 요청서 정정 표지 Q5): 같은 시험 **206/206**.  사유 = 경계 없음 · 붙여 쓴 반복 표지 → `frame_layout` (새 칸 `header_boundary` · 반복 표지는 + `row_width` / `box_format`) · 행 표지 후첨 → `row_width` · 상자 표지 후첨 → `box_format` · 파생값 넘침 → 새 코드 `derived_nonfinite` (G-frame f6 · G-geo `delta_bound_um` · `dem_am_am.area_um2`) · 전각 · 아라비아-인도 숫자 → `int_token`.  `JOIN_VERSION` v4.
- 회귀 (수정 뒤 · 이 컨테이너 Linux · Python 3.11.15 · NumPy 2.4.6 · SciPy 1.17.1):

| 시험 | 결과 |
|---|---|
| `scripts/test_rint_g2_join.py` | 206/206 (고치기 전 152/206) |
| `scripts/test_rint_g2_am_iface.py` | 136/136 |
| `scripts/test_rint_g2_rrm.py` | 55/55 |
| `scripts/test_rint_t4_census.py` | 8/8 |
| `scripts/test_rint_t43_order.py` | 6/6 |
| `scripts/test_rint_t2_dev.py` | 23/23 |
| `scripts/step3_sigma.py --selftest` · `--selftest-rint` | PASS · PASS |
| `scripts/rint_t41_census.py --selftest` | PASS |

- real14 = PASS · 457 / 457 / 457 · 인증 AM–AM 660 · case15 = PASS · 104 / 104 / 104 · 119 (AM–AM 밖 음수 면적 2 행 기록 그대로) — 수정 전 모듈과 입자 · atom id 사상 · `dem_am_am` 배열 바이트 같음 · `delta_bound_um` 같음 · 바뀐 것 = 기록의 새 칸 · 판 · 규칙 문구뿐 (`fp_join` 이 바뀐다 · 고정해 대조하는 곳 없음).  iface 끔 경로 무영향 (`scripts/step3_sigma.py` 무변경 · 조인 모듈은 그 경로에 없다) · 웹앱 화면 없음 · 봉인 32 · S3 수치 모듈 6 밖.
- 원장: `RIMPR-R01` · `RIMPR-03` · `SELF-124` → claimed_fixed (`a2cfd0365`) · `RIMPR-04` = open 유지 (부분 수정 note · 연기 조건 ①).
- ⬜ Codex 재확인 = Rint ② 설계 리뷰 회차에 절을 나눠 (Q6 (나)) — 위 4 의 탐침 재실행 + 수정 diff (`git diff 9845d526c a2cfd0365 -- scripts/rint_iface_join.py scripts/test_rint_g2_join.py`).

### PB1 같은 부류 보강 결과 (10-20 · 1저자 *"다 권고대로 해"* · 내부 사전 리뷰가 찾은 다섯 · 작업 트리 · `d1768cf0c` 바로 위 두 커밋 · push 안 함)

- **시험 먼저 `af8d1d501`** (`scripts/test_rint_g2_join.py` 만 · 새 묶음 J15 표지 경계 16 · J16 덤프 어휘 13 · J17 scaffold 실수 열 5 (+ 주석 줄 U+2014 양성) · J18 scaffold step 선언 5 (+ 양성 · 대조) · J15P 정상 양성 18 + J13 ⑤ 허용폭만 넘침 · J13 머리 출력 문구 정정): 고치기 전 모듈 (v4 = `a2cfd0365` 판) 에 **231/309** — 실패 78 = 새 반례 39 × (입구 REJECT · 소비자 차단) · 옛 206 · J13 ⑤ (v4 도 거부 = 변이 시험 틈 메움) · 새 양성 · 대조 23 통과.
- **수정 `263c9502b`** (`scripts/rint_iface_join.py` 만): 같은 시험 **309/309** · 표지 경계 = 줄 끝 · 공백 · 탭만 (`header_boundary`) · 덤프 글자 어휘 관문 (`frame_layout` · `atom_lexical` · `contact_lexical`) · scaffold 실수 열 ASCII 고정소수 + 주석 아닌 줄 어휘 (`numeric_format` · `scaffold_grammar` · `scaffold_lexical`) · scaffold 머리줄 step 선언 = 옛 문법으로 찾고 선언 전체 ASCII · int64 일 때만 값 (`int_token` · `scaffold_step` · `int()` 없음) · `JOIN_VERSION` v5 · 리포 `docs/data` 의 scaffold 41 파일 (2,042,453 행) = 고정소수 아닌 토큰 0 · 어휘 0 (생산 `%.6f`).
- 회귀 (이 판 · 이 컨테이너 Linux): 옛 시험 138 판 (`2b9efa253`) 을 고친 모듈에 138/138 · 위 표의 나머지 일곱 그대로 (am_iface 136/136 · rrm 55/55 · t4 8/8 · t43 6/6 · t2 23/23 · step3 두 selftest PASS · t41 selftest PASS) · real14 · case15 = 고치기 전 (v4) 과 입자 · atom id 사상 · `dem_am_am` 배열 여섯 · `delta_bound_um` 바이트 같음 · g_geo · g_frame 같음 · 어휘 · scaffold 형식 위반 0 · 바뀐 것 = 판 · 새 기록 칸 (`entrance.lexical` · `format.scaffold_bad`) · `fp_join` · 웹앱 화면 없음 · 봉인 확인 = `scripts/rint_iface_join.py` ∉ CODE_FILES 32 · NUMERIC_MODULES 6.
- Codex 탐침 넷 (위 4 의 리포 사본 · 경로 상수만 · 대조 = 같은 증거 폴더의 리뷰 핀 기록): 구조 144 = 뜻밖 통과 · 거부 0 · 리뷰 핀 대비 다름 14 = 헤더 반례 10 거부 (v4 에서 고침) + step 값 VT · FF 4 (여전히 거부 · 어휘 사유 하나 더) · 최소 재생 = 탐침 그대로는 첫 사례에서 정량 관문 ValueError (거부) · 관문을 감싼 같은 논리 = 둘 다 REJECT → `join_gate_failed` → 관문 거부 · 수치 113 = 리뷰 핀 대비 다름 16 = 1e160 계열 6 · 전각 정수 1 (v4 에서 고침) + 이미 거부된 9 에 사유 하나 더 (scaffold 지수 꼴 `1e306` 8 · 원자 x 전각 1) · 넘침 재생 3 = v4 와 같음 · v4 판 대비 판정 뒤집힘 0.
- 원장: `RIMPR-R01` · `RIMPR-03` note = 같은 부류 보강 · claimed_fixed `263c9502b` · `RIMPR-04` = open 유지 (J13 ⑤ · 남은 한정 목록 note) · 우리 기록 문장 정정 11 곳 (A–K) = `SELF-125` (`SELF-124` note 에 A · B · D · E 처리).
- ⬜ Codex 재확인 = Rint ② 설계 리뷰 회차 Part B (`docs/reviews/codex_rint_carbon_additive_design_request_20261020.md` · 리뷰 핀 = push 뒤 메인 · 발송 = 1저자).
