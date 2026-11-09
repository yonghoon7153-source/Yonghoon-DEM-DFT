# Codex DEM 세대 2 G2PREP-01–04 수정 후보 반입 대응표 — 2026-11-09 (Claude 서브 세션 · 가지 B)

1저자 11-09 전달 = Codex 실무 창 인계 ZIP (codex_dem_gen2_four_fixes_6adf932499cd_claude_handoff_20261109.zip · sha256 5c0fa9dd… · 내부 해시 12/12 · 안의 재검토 ZIP = 1저자가 반박 창에 보낸 것과 같음 (sha256 7504b3d9… · 내부 해시 104/104)) · 원격 가지 `codex/dem-gen2-fixes-1109` 끝 = `6adf932499cd`.
반입 기록이며 실제 T0 극성 · T5 / T11 / T12 자격 · 값 열람 · 운영 재봉인 · 실행 GO 가 아니다 — 전체 HOLD 그대로.

## 1. 대응표

| # | Codex 가지 | Codex 원 커밋 | B 커밋 | 처분 |
|---|---|---|---|---|
| 1 | codex/dem-gen2-fixes-1109 (바탕 B `69d714d09`) | `08fb8b178eae` (원 후보 `9241933b9836` 의 같은 내용 사본) | — (건너뜀) | B 에 이미 `27ed57b96` (= `9241933b9836` cherry-pick) · 원 후보 14 파일 blob = 사본 = B 14/14 · patch-id 같음 → 인계 지시대로 중복 적용 안 함 |
| 2 | 같은 가지 | `6adf932499cd` | `160b9ee10` | 이번 반입 (`cherry-pick -x` · 충돌 0 · 바뀐 10 파일 (소스 4 고침 · 문서 6 추가) blob = 원 커밋 10/10 · patch-id = 원 커밋 = ZIP 패치) |

## 2. 독립 검토 수령 · 원장

- 반박 창 판정 (리뷰 핀 `9241933b9836` · 판정 ZIP sha256 30eac8f7…) = 문서 · 미정값 · 비활성 경계 한정 수용 · 코드 보완 필요 (P1 0 · P2 둘 · P3 둘). 원 ZIP = 리포 밖 위치 문구 → 리포 밖 보존 · 리포 = `docs/reviews/dem_gen2_preparation_fixes_20261109/intake_receipt.json` (신원 · 수령 바이트 감사 PASS).
- 원장 (이 쪽지와 같은 커밋 · 원장 ID 형식 = 앞머리 다섯 자 이하 → `G2PR-NN` = Codex 표기 G2PREP-NN): G2PR-01 (P2 · 판 반력 극성) · G2PR-02 (P2 · 지연 큐 중 첫 창 진입 = 수렴) · G2PR-03 (P3 · 큰 반경비 교차 원판 상쇄) · G2PR-04 (P3 · 큰 절대좌표 관통 반올림) = claimed_fixed (`160b9ee10`) · 독립 재확인 대기 · verified 아님 (고친 쪽 · 검토 쪽 모두 Codex 창).

## 3. 우리 기계 재실행 (11-09 · 합성만 · 판정 아님)

| 대상 | 결과 | Codex 기록 |
|---|---|---|
| `scripts/test_make_dem_gen2_decks.py` (Python 3.11 · `-I`) | 18/18 (rc 0) | 18/18 (고치기 전 실패 11) |
| `scripts/test_dem_gen2_qualification.py` | 22/22 (rc 0) | 22/22 (고치기 전 실패 21 · subtest 관측 포함) |
| 소스 · 시험 넷 sha256 | `docs/reviews/dem_gen2_preparation_fixes_20261109/verification_summary.json` 과 같음 (4/4) | — |

## 4. 다음

- 재검토 ZIP (G2PREP-01–04 한정) = 1저자 11-09 반박 창 발송 끝 → 판정 수령 = 다음 인계 때 (원 판정문 신원 · 결과 함께).
- 실제 T0 극성 · 완결된 T5 / T11 / T12 · live observer · P2 ULPR · 경계 기록 = 미구현 · NOT_RUN 그대로.
- 다음 새 가지 바탕 = `origin/claude/sdcp-dem-manuscript-si-pqwtv8` 최신 (이 쪽지 커밋 push 뒤).
