# Codex 짧은 재확인 요청 — 10-15 재확인 (코드 핀 `dcb97f1ed`) 의 남은 둘: RIMPR-01 (P2) · RIMPR-02 (P3) 수정 (2026-10-20 · 결과 0 건 · 발송 = 1저자)

> **한 줄**: Codex 재확인 (10-15 · 판정문 `docs/reviews/codex_review_rint_g2_impl_fix_recheck_20261015.md`) 이 남긴 RIMPR-01 (§2) · RIMPR-02 (§3) 를 판정문의 최소 해결대로 고쳤다 (시험 먼저).
> 둘이 닫히는지 · 최소 해결보다 넓힌 같은 부류 보강이 정상 입력을 깨지 않는지 · 새 결함이 있는지 짧게 판정해 달라.
> 1저자 10-20 *"Rint 관련해서 계속 gate 굴려봐 codex 리뷰 받고 · 이게 가장 급하게 진행되어야되는 부분"* (LHS 보다 먼저).
> **리뷰 핀** = 이 요청서를 담은 본 가지 커밋 (SHA 는 발송 때 1저자가 적는다) · **기준** = `dcb97f1ed` (지난 리뷰 핀) · 수정 커밋 = `3b9d51789`.

## 0. 대상 · 지위

- 코드 diff = `git diff dcb97f1ed <리뷰 핀> -- scripts/rint_iface_join.py scripts/test_rint_g2_join.py`.
- `scripts/step3_sigma.py` · 봉인 32 파일 무변경 — 조인은 진단 관문이라 생산 σ 경로에 들어가지 않는다.  ①′ 정량 채택 · 생산 HOLD 그대로.
- 새 시뮬레이션 · WSL · 재봉인 없음.

## 1. 판정문 최소 해결 ↔ 수정

| 원장 | 수정 (`3b9d51789`) | 시험 (고치기 전 → 뒤) |
|---|---|---|
| `RIMPR-01` (§2 — 데이터 블록에서 열 수가 다른 행이 조용히 빠짐 · 중복 필수 열은 첫 열만 · step/count 줄 뒤 토큰 무시) | 입구 e6 전수 소비: 행 절 (ITEM: ATOMS · ENTRIES) 의 비어 있지 않은 **모든** 행을 세고 열 수 ≠ 머리 열 수 = `row_width` · 소비하는 필수 열 이름 정확히 한 번 = `header_duplicate` · TIMESTEP · NUMBER OF 절은 몸통 **전체**가 한 정수 토큰 = `int_token` · 거부는 관문 계산 전 → 계획이 `join_gate_failed` 를 받고 정량 관문이 멈춘다 | `scripts/test_rint_g2_join.py` 78/135 → 138/138 (새 반례 57 = J10 37 · J11 20 · 옛 73 그대로 · 판정문 반례 24 열 접촉 행 · 7 열 원자 행 · `radius` 중복 · `100 0.9` · `1 garbage` + 짧은 행 둘) |
| `RIMPR-02` (§3 — Decimal 유한 ↔ float64 무한) | e1 유한 = **실제로 쓰는 float64 값** 기준 (±1e309 고정소수 · 지수 = `nonfinite_value`) · scaffold µm 변환값 (×1000) 도 유한 · int64 밖 정수 토큰 = `int_token` (OverflowError 대신) | 같은 파일 |

- 정상 입력 그대로: real_14 입자 457/457 · AM–AM 면적 660 인증 · case15 104/104 · 119 · D19 선언 재사용 PASS (계획 · 정량 관문까지) · 폭 정상 중복 행 = 같은 코드로 REJECT.
- 빈 줄 처리는 옛 판과 같게 묶었다 (고정 시험 3 — 옛 판에서도 통과) · `JOIN_VERSION` = `g_geo_g_frame_v3` · 입구 요약에 새 칸.
- 그 밖 회귀: `test_rint_t4_census.py` 8/8 · `test_rint_t43_order.py` 6/6 · `check_method_discipline.py` 오류 0 · 커밋 게이트 통과.

## 2. 최소 해결보다 넓힌 것 (같은 부류 · 1저자 비준 대기)

판정문 §2 의 뿌리 ("검사 전에 파서가 버리는 줄 · 열 · 토큰") 와 같은 길을 같이 막았다 — 각각 고치기 전 판에서 **통과**하던 변이다.

- 마지막 프레임의 모든 줄을 아는 절 넷 (TIMESTEP · NUMBER OF · BOX BOUNDS · 행) 에 한 번씩 배정 — 모르는 `ITEM:` 절 · 같은 절 두 번 · 첫 프레임 앞 비어 있지 않은 줄 · TIMESTEP · NUMBER OF 머리 줄의 뒤 토큰 = `frame_layout`.
- 상자 경계 줄 정확히 셋 (넷째 줄 = `box_format`) · step 값 다음 둘째 줄 · step 줄 안의 세로 탭 (줄 나눔으로 두 줄이 됨) = `int_token`.
- step · count 도 int64 범위 (2^63 이 통과하던 것) · 반경 10^306 구 하나 (µm 변환 = inf) = `nonfinite_value`.

## 3. 질문

| Q | 내용 |
|---|---|
| Q1 | RIMPR-01 · 02 가 판정문 §2 · §3 최소 해결로 닫히는가 |
| Q2 | §2 의 같은 부류 보강이 생산 `%g` 덤프 (real_14 · case15 · 0 열 · 끝 빈 줄 · gzip) 를 거짓 거부하지 않는가 · 넓힌 범위에 새 fail-open 이 있는가 |
| Q3 | 판정문 Q7 권고 (일반 관문의 막 행 `rface` 유한 · 비음수 · r = 0 보존) — `step3_sigma.iface_require_quantitative` 의 행 지문 검사 뒤 5–8 줄 + 시험 3–4 (NaN · 음수 · +inf 막 = 거부 · 등록 r = 0 · RRM 계획 = 통과).  승인 범위 밖이라 이번 묶음에 **없다** (1저자 결정 대기) — 넣는다면 그 자리가 맞는가 |
| Q4 | 남은 P3 둘 (원장 `RIMPR-03` · `RIMPR-04`): 정수 정규식 `\d` 가 전각 숫자 `１` 을 받음 · 아주 큰 유한 입력 (좌표 ~1e160) 이 입구 뒤 관문 산술에서 넘침 (`delta_bound_um` = inf) — 다음 묶음으로 미뤄도 되는가 |

## 4. 한정

- 이 컨테이너 · 정상 침대 두 개 (real_14 · case15) 결과다.
- `docs/data/rint_t41_census_20261013/census.json` 은 옛 `fp_join` 을 담고 있다 (그 값과 비교하는 곳 없음 · 다시 돌리면 값이 바뀐다).
- 수정은 작업 트리 에이전트가 만든 두 커밋 (시험 먼저 → 수정) 을 본 가지에 한 커밋으로 합쳐 옮긴 것이다 (내용 같음 · 고치기 전 숫자 78/135 는 시험만 넣은 상태에서 잰 값).
