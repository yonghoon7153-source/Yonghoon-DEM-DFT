# Codex 비 Rint 첫 연결 반입 대응표 — 2026-11-09 밤 (Claude 서브 세션 · 가지 B)

1저자 11-09 밤 전달 = Codex 실무 창 인계 (가지 `codex/nonrint-first-link-1109` · 끝 0f7ea5ea5d34 · 바탕 B e91bd1c94).  반입 기록이며 실행 · 값 열람 · 현장 접근 · 운영 재봉인 · 실행 GO 가 아니다 — 전체 HOLD 그대로.

## 1. 대응표

| # | Codex 원 커밋 | 처분 |
|---|---|---|
| 1 | 43eb8a28c (조건부 선행 1 · 승인 준비 양식 7) | **반입 안 함** — B 의 533ae324c 와 같은 내용 (그 커밋이 바꾼 7 파일 = B 끝과 diff 0) |
| 2 | b492a2062 (조건부 선행 2 · LHS Q1 선택지 3) | **반입 안 함** — B 의 dfadc452c 와 같은 내용 (3 파일 diff 0) |
| 3 | 708add516 (DEM 합성 관측 → 단계 진단 연결 · 소스 · 시험 · 요청 / 근거 5 파일) | `cherry-pick -x` (충돌 0) |
| 4 | 0f7ea5ea5 (공통 README · LHS O1 초안 · 믹서 메타 초안 · 고정 계획 빈틀 · 인계 쪽지 5 파일) | `cherry-pick -x` (충돌 0) |

- 인계 ZIP sha256 caeab985d2a2e73c93739d9366897e387459152716aa2e46d9e45830f9bd2f3b · 안쪽 SHA256SUMS 통과 · snapshot 10 파일 = 반입 뒤 B 의 blob 10/10 같음.
- DEM 반박 검토 ZIP sha256 fb5c392ecf997646dc7a250faaf55ae0778c72d568e935881f7da164fa7f94d3 (인계 쪽지 값과 같음) — 반박 창 발송 = 1저자 · 리포에는 넣지 않음 (쪽지대로).
- 시험 (Claude 컨테이너 · 반입 뒤 B): `scripts/test_dem_gen2_observation_bridge.py` 32/32 · `scripts/test_dem_gen2_qualification.py` 22/22.  ⚠ DEM 세대 2 시험 파일들은 전체 게이트 (`scripts/check_all.sh`) 단계에 들어 있지 않다 (앞선 반입들과 같음) — 게이트 통과가 이 시험 통과를 뜻하지 않는다 · 단계 추가는 별도 결정.

## 2. 1저자 결정 (11-09 밤) — 다음 준비에 반영할 것

- **DEM 세대 2 E_SE 보정 표적 = DEM 자신의 질량 기준 기공률 ε_sphere (진밀도 1.64) 10–13 %** (순수 SE 침대 · 300 MPa 가압 + 이완 끝) · ε_union 은 함께 기록만.  = 10-14 D9 의 "ε_union 표적" 개정 (MV-03 방향 · `docs/reviews/dem_protocol_gen2_plan_draft_20261014.md` D9 옆 표지).  1저자 *"권고대로 해야지 ㅇㅇ"*.
- 랩 표준 10–13 % (진밀도 1.64) = 외부 기준 · 출처 질문 닫음 (1저자 *"잔말말고 이걸로 하라고"*).
- 새 트랙 [DEM 우선 (수영)] (가압부터 탈압까지 한 모델 재설계) = Claude 세션 담당 · 이 창 범위 밖.
- DEM Q3 M1–M9 = 1저자 답 대기.

## 3. 다음 (Codex 실무 창)

- 새 가지 바탕 = `origin/claude/sdcp-dem-manuscript-si-pqwtv8` 최신 (이 쪽지 커밋 push 뒤).
- DEM 반박 판정 전에는 두 번째 연결로 넘어가지 않는다 (판정 = 1저자 전달).  위 E_SE 표적 정의는 문서 (선택표 · 등록 초안) 에만 반영.
