# Codex 짧은 재확인 요청 — 10-15 재확인 (코드 핀 `dcb97f1ed`) 의 남은 둘: RIMPR-01 (P2) · RIMPR-02 (P3) 수정 + Q7 권고 (일반 관문 막 값 불변량) (2026-10-20 · 결과 0 건 · 발송 = 1저자)

> ✅ **Codex 재확인 (10-20 · 핀 2b9efa253) = RIMPR-01 · 02 · Q7 닫힘 (범위 한정)** — 새 P3 `RIMPRR-01` (원장 `RIMPR-R01`) (구역 헤더 정상화 false-PASS) · `RIMPR-04` 범위 보강 · ①′ 정량 채택 · 생산 HOLD · 판정문 docs/reviews/codex_review_rint_join_rimpr_q7_recheck_20261020.md (증거 docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/).  ⛔ 행 번호 안내 10-20 (`SELF-125` E): 원장 `SELF-124` note 가 적은 이 문서 12 · 11 · 19 · 50 행 = 리뷰 핀 `2b9efa253` 판 — 지금 판 = 14 · 13 · 22 · 53 행 (이 머리 줄 · 정정 표지가 붙어 밀렸다 · 아래 표지는 줄을 늘리지 않고 붙였다).

> **한 줄**: Codex 재확인 (10-15 · 판정문 `docs/reviews/codex_review_rint_g2_impl_fix_recheck_20261015.md`) 이 남긴 RIMPR-01 (§2) · RIMPR-02 (§3) 를 판정문의 최소 해결대로 고쳤고 (시험 먼저),
> 판정문 §5 의 Q7 권고 (일반 관문이 막 행의 r_face 를 유한 · 비음수로 확인) 도 넣었다 (시험 먼저 · 승인된 wrapper 범위 밖 변경이라 따로 표기).
> 둘이 닫히는지 · 최소 해결보다 넓힌 같은 부류 보강과 Q7 관문이 정상 입력을 깨지 않는지 · 새 결함이 있는지 짧게 판정해 달라.
> 1저자 10-20 *"Rint 관련해서 계속 gate 굴려봐 codex 리뷰 받고 · 이게 가장 급하게 진행되어야되는 부분"* (LHS 보다 먼저) · 같은 부류 보강 · Q7 = 1저자 10-20 승인.
> **리뷰 핀** = 이 요청서를 담은 본 가지 커밋 (SHA 는 발송 때 1저자가 적는다) · **기준** = `dcb97f1ed` (지난 리뷰 핀) · RIMPR 수정 커밋 = `3b9d51789` · Q7 수정 = 리뷰 핀 커밋 안 (이 요청서와 같은 커밋).

## 0. 대상 · 지위

- 코드 diff = `git diff dcb97f1ed <리뷰 핀> -- scripts/rint_iface_join.py scripts/test_rint_g2_join.py scripts/step3_sigma.py scripts/test_rint_g2_am_iface.py scripts/test_rint_g2_rrm.py`.
- 봉인 32 파일 무변경 (`scripts/step3_sigma.py` 는 봉인 밖).  `step3_sigma.py` 변경 = Q7 관문 한 곳뿐 — `iface` 를 넘길 때만 도는 관문이라 iface 끔 경로는 옛 그대로다.  조인은 진단 관문이라 생산 σ 경로에 들어가지 않는다.  ①′ 정량 채택 · 생산 HOLD 그대로.
  - ⛔ 정정 10-20 (`SELF-124` · Codex 판정문 §7 권장 문장 — 위 줄의 *"봉인 32 파일 무변경"* 은 범위 한정이 빠졌다): *"이번 Rint 수정 두 커밋 (`3b9d51789` · 리뷰 핀 `2b9efa253`) 은 봉인 32 개를 변경하지 않았다. 대조 핀 이후의 다른 트랙 변경까지 포함한 전체 스냅샷의 동일성은 별도다."* — 대조 핀 `dcb97f1ed` → 리뷰 핀 구간 전체에서는 봉인 네 파일 (`scripts/network_conductivity.py` · `scripts/tau_flux.py` · `webapp/app.py` · `webapp/pipeline_service.py` = 다른 트랙 변경) 이 다르다 (판정문 docs/reviews/codex_review_rint_join_rimpr_q7_recheck_20261020.md §7).  ⛔ 정정 10-20 (`SELF-125` B · A): 위 인용은 판정문 §7 원문과 다르다 — 원문 = *"이번 Rint 수정 두 커밋은 봉인 32개를 변경하지 않았다. 대조 핀 이후의 다른 트랙 변경까지 포함한 전체 스냅샷의 동일성은 별도다."* (커밋 괄호를 인용 안에 끼웠고 "32개" 를 띄어 썼다 · 두 커밋 = `3b9d51789` · 리뷰 핀 `2b9efa253` 은 인용 밖에 적는다) · (A) 그 두 커밋 ∩ (봉인 CODE_FILES 32 ∪ S3 NUMERIC_MODULES 6) = 0 이고, 대조 핀 → 리뷰 핀 구간에서 다른 봉인 네 파일 중 `scripts/network_conductivity.py` 는 NUMERIC_MODULES 6 에도 든다 (10-20 git 재확인 · 판정문 §7 첫 문단의 *"여섯 개는 두 핀 사이 모두 동일"* 도 그 구간에서는 맞지 않는다 = 설계 리뷰 요청서 docs/reviews/codex_rint_carbon_additive_design_request_20261020.md Part B-2 정정 알림).
- 새 시뮬레이션 · WSL · 재봉인 없음.

## 1. 판정문 최소 해결 ↔ 수정

| 원장 | 수정 (RIMPR = `3b9d51789` · Q7 = 리뷰 핀 커밋) | 시험 (고치기 전 → 뒤) |
|---|---|---|
| `RIMPR-01` (§2 — 데이터 블록에서 열 수가 다른 행이 조용히 빠짐 · 중복 필수 열은 첫 열만 · step/count 줄 뒤 토큰 무시) | 입구 e6 전수 소비: 행 절 (ITEM: ATOMS · ENTRIES) 의 비어 있지 않은 **모든** 행을 세고 열 수 ≠ 머리 열 수 = `row_width` · 소비하는 필수 열 이름 정확히 한 번 = `header_duplicate` · TIMESTEP · NUMBER OF 절은 몸통 **전체**가 한 정수 토큰 = `int_token` · 거부는 관문 계산 전 → 계획이 `join_gate_failed` 를 받고 정량 관문이 멈춘다 | `scripts/test_rint_g2_join.py` 78/135 → 138/138 (새 반례 57 = J10 37 · J11 20 · 옛 73 그대로 · 판정문 반례 24 열 접촉 행 · 7 열 원자 행 · `radius` 중복 · `100 0.9` · `1 garbage` + 짧은 행 둘) · ⛔ 정정 10-20 (`SELF-124` · Codex 판정문 §1): 78/135 = 시험 작성 중간 시점 (시험 135 개) · 현재 시험 138 개를 옛 코드에 = 81/138 (57 FAIL) — 두 숫자는 같은 시험 집합이 아니다 · ⛔ 정정 10-20 (`SELF-125` C): 앞 표지의 출처 묶음을 고친다 — 78/135 = **저자 보고** (그 시험 판이 커밋에 없어 재현 불가 · 판정문 §1 도 *"이 재실행으로 입증하지는 않는다"*) · 판정문 §1 이 입증한 것 = 현재 시험 138 을 옛 코드에 = 81/138 (57 FAIL) |
| `RIMPR-02` (§3 — Decimal 유한 ↔ float64 무한) | e1 유한 = **실제로 쓰는 float64 값** 기준 (±1e309 고정소수 · 지수 = `nonfinite_value`) · scaffold µm 변환값 (×1000) 도 유한 · int64 밖 정수 토큰 = `int_token` (OverflowError 대신) | 같은 파일 |
| Q7 권고 (§5 — 행 지문은 만든 뒤 바뀐 행만 잡는다 · 지문을 다시 만든 계획의 막 행 r_face NaN · 음수 = 막이 조용히 빠지고 +inf = 면이 끊긴다 · 조립은 r_face > 0 면에만 막을 건다) | `step3_sigma.iface_require_quantitative` 의 행 지문 검사 바로 뒤 (거부 사유 검사 앞): 모든 축 행의 r_face 가 유한 · ≥ 0 이어야 한다 (r = 0 · 절단 tombstone 0 허용) · 어긋나면 ValueError (축 · 어긋난 행 수 · NaN / ±inf / 유한 음수 개수) → `solve_sigma_z` 가 조립 전에 멈춘다 | `scripts/test_rint_g2_am_iface.py` 새 Q7 (검사 4) 133/136 → 136/136 · `scripts/test_rint_g2_rrm.py` N9b 나눔 54/55 → 55/55 |

- 정상 입력 그대로: real_14 입자 457/457 · AM–AM 면적 660 인증 · case15 104/104 · 119 · D19 선언 재사용 PASS (계획 · 정량 관문까지) · 폭 정상 중복 행 = 같은 코드로 REJECT.
- Q7 양성 대조: RRM r = 0 계획 (r_face 0 막 행 67 · 절단 tombstone 85) σ 0.0037299595666211234 · 정상 RRM 계획 σ 0.003334457143882423 (Codex 값 · 상대 1e−9) · CNC r = 0 계획 (막 행 0) = OFF 와 σ · φ 비트 같음 · 같은 꼴의 유한 양수 변이 (r_face × 2 · 지문 다시 만듦) = 관문 통과 · 풀이 (σ 가 OFF > 정상 > 변이 순).  음성 셋 (NaN · −r_face · +inf) = 관문 ValueError (`r_face` 표지) · 솔브 CG 호출 0.
- N9b 기록을 둘로 나눴다: (a) RRM 원장 검사가 맡는 우회 (cut 삭제 · 값이 유한해서 그대로 일반 관문 밖) σ 0.0040840140889134725 = 옛 기록 그대로 · (b) film r_face NaN 계획 = 이제 일반 솔버도 거부 — 막힌 우회 크기는 같은 조립의 등록 r = 0 계획으로 기록 (NaN · 0 둘 다 r_face > 0 이 아니라 조립 행렬이 같다 · 고치기 전 판에서 σ hex · φ 바이트 · n_dof · 잔차 같음 확인) σ 0.0037299595666211234 = Codex 의 NaN 값.
- 빈 줄 처리는 옛 판과 같게 묶었다 (고정 시험 3 — 옛 판에서도 통과) · `JOIN_VERSION` = `g_geo_g_frame_v3` · 입구 요약에 새 칸.
- 그 밖 회귀: `test_rint_t4_census.py` 8/8 · `test_rint_t43_order.py` 6/6 · `check_method_discipline.py` 오류 0 · 커밋 게이트 통과.

## 2. 최소 해결보다 넓힌 것 (같은 부류 · 1저자 비준 10-20)

판정문 §2 의 뿌리 ("검사 전에 파서가 버리는 줄 · 열 · 토큰") 와 같은 길을 같이 막았다 — 각각 고치기 전 판에서 **통과**하던 변이다.

- 마지막 프레임의 모든 줄을 아는 절 넷 (TIMESTEP · NUMBER OF · BOX BOUNDS · 행) 에 한 번씩 배정 — 모르는 `ITEM:` 절 · 같은 절 두 번 · 첫 프레임 앞 비어 있지 않은 줄 · TIMESTEP · NUMBER OF 머리 줄의 뒤 토큰 = `frame_layout`.
- 상자 경계 줄 정확히 셋 (넷째 줄 = `box_format`) · step 값 다음 둘째 줄 · step 줄 안의 세로 탭 (줄 나눔으로 두 줄이 됨) = `int_token`.
- step · count 도 int64 범위 (2^63 이 통과하던 것) · 반경 10^306 구 하나 (µm 변환 = inf) = `nonfinite_value`.

## 3. 질문

| Q | 내용 |
|---|---|
| Q1 | RIMPR-01 · 02 가 판정문 §2 · §3 최소 해결로 닫히는가 |
| Q2 | §2 의 같은 부류 보강이 생산 `%g` 덤프 (real_14 · case15 · 0 열 · 끝 빈 줄 · gzip) 를 거짓 거부하지 않는가 · 넓힌 범위에 새 fail-open 이 있는가 |
| Q3 | 판정문 Q7 권고를 이번 묶음에 넣었다 (§1 마지막 행 · 1저자 10-20 승인 · 승인된 wrapper 범위 밖 변경).  자리 (행 지문 검사 뒤 · 거부 사유 검사 앞) · 범위 (r = 0 · tombstone 보존 · iface 끔 무영향) 가 맞는가 · N9b 기록을 나눈 것 (cut 삭제 우회 = 유한 값이라 여전히 일반 관문 밖 = RRM 원장 검사 몫) 이 맞는가 |
| Q4 | 남은 P3 둘 (원장 `RIMPR-03` · `RIMPR-04`): 정수 정규식 `\d` 가 전각 숫자 `１` 을 받음 · 아주 큰 유한 입력 (좌표 ~1e160) 이 입구 뒤 관문 산술에서 넘침 (`delta_bound_um` = inf) — 다음 묶음으로 미뤄도 되는가 |

## 4. 한정

- 이 컨테이너 · 정상 침대 두 개 (real_14 · case15) 결과다.
- `docs/data/rint_t41_census_20261013/census.json` 은 옛 `fp_join` 을 담고 있다 (그 값과 비교하는 곳 없음 · 다시 돌리면 값이 바뀐다).
- 수정은 작업 트리 에이전트가 만든 두 커밋 (시험 먼저 → 수정) 을 본 가지에 한 커밋으로 합쳐 옮긴 것이다 (내용 같음 · 고치기 전 숫자 78/135 는 시험만 넣은 상태에서 잰 값).  ⛔ 정정 10-20 (`SELF-125` D): 이 78/135 에는 표지가 없었다 — §1 표의 정정 표지 (`SELF-124` · `SELF-125` C) 로 갈음한다 (78/135 = 저자 보고 · 재현 불가 · 현재 시험 138 을 옛 코드에 = 81/138).
- Q7 도 같은 방식이다 (에이전트의 시험 먼저 커밋 + 수정 → 본 가지 한 커밋).  고치기 전 숫자 (133/136 · 54/55) 는 시험만 넣은 상태를 새 빈 폴더에 풀어 다시 돌려 확인했다 (실패 = Q7 음성 셋 · N9b Q7 하나뿐).
