# Codex 비준 뒤 준비 반입 대응표 — 2026-11-09 (Claude 서브 세션 · 가지 B)

1저자 11-09 전달 = Codex 실무 창 통합 인계 ZIP (codex_ratified_preparation_9241933b9836_claude_handoff_20261109.zip · 996,574 B · sha256 43517509… · 내부 해시 17/17 · 패치 4 = 원 커밋 patch-id 4/4 · LHS 스냅샷 4 = 핀 blob 4/4) · 원격 가지 셋의 끝 = 핀 (`codex/dem-gen2-1109` = `9241933b9836` · `codex/lhs-policy-1109` = `847d4952407a` · `codex/mixer-inactive-prep-1109` = `73e659273fd2`).
반입 기록이며 값 열람 · 현장 접근 · 운영 재봉인 · 실행 GO 가 아니다 — 전체 HOLD 그대로.

## 1. 대응표

| # | Codex 가지 | Codex 원 커밋 | B 커밋 | 내용 |
|---|---|---|---|---|
| 1 | codex/dem-gen2-1109 | `9241933b9836` | `27ed57b96` | DEM 세대 2 비활성 7 단계 생산기 후보 · 합성 guard · T5/T11 등록 초안 (추가 14 파일) |
| 2 | codex/lhs-policy-1109 | `56a08a7679b1` | `5a9b73d1f` | LHS 문서 정책 비준 원문 수령 (추가 1 파일) |
| 3 | codex/lhs-policy-1109 | `847d4952407a` | `095bf43f2` | LHS 사전 접근 동결안 초안 (추가 3 파일) |
| 4 | codex/mixer-inactive-prep-1109 | `73e659273fd2` | `1df1ba5a7` | 믹서 first8 현재 소스 · 메타 비활성 사본 (추가 61 파일) |

- 바탕 = B `8842ed2bd` 위 `cherry-pick -x` 4 (충돌 0 · LHS 둘 = 수령 → 동결안 순서). 네 커밋 = 추가만 79 파일 · B 의 `e48e5fa04` 뒤 변경 68 파일과 겹침 0 · Rint 경로 0 · 반입 커밋 patch-id = 원 커밋 = ZIP 패치 (4/4) · 각 반입 커밋 파일 = 원 커밋과 차이 0.
- 반박 창 검토 ZIP 둘 (발송 = 1저자): DEM 검토 ZIP (내부 해시 104/104 · 고정 파일 blob 17/17) · 믹서 검토 ZIP (내부 해시 184/184 · 고정 파일 61/61 · 의존 스냅샷 86/86 = B blob).
- Codex 쪽지 셋의 `<<sha:…>>` 자리 = 이 표 (쪽지 원바이트 보존 · 고쳐 쓰지 않음).

## 2. 우리 기계 재실행 (11-09 · 합성만 · 판정 아님)

| 대상 | 결과 | Codex 기록 |
|---|---|---|
| `scripts/test_make_dem_gen2_decks.py` · `scripts/test_dem_gen2_qualification.py` (Python 3.11 · `-I`) | 15/15 · 15/15 (rc 0) | 15 + 15 |
| 믹서 `verify_inactive.py --mode old` (의존 스냅샷 86) | rc 1 · 8 실패 (옛 메타 ↔ 현재 생성기 결속) | rc 1 |
| `--mode verify` | rc 0 · 사례 8 · 덱 재생성 8 바이트 같음 · STL 24 그대로 · 결속 8 · 후보 43 파일 · 실제 하위 프로세스 · 소켓 시도 0 | rc 0 |
| `--mode preparation-tests` | rc 0 | rc 0 (14) |
| `test_snapshot_provenance.py` | rc 0 · 5 메서드 | 5 PASS |

- 가지 B 빠른 점검 (반입 네 커밋 위): `scripts/check_doc_refs.py` · 원장 자기일관 · 자기검사 등재 · 방법론 규율 = 오류 0 · 철회값 스윕 = 누수 0. 전체 게이트 (178 단계 · 나눠 돌림) = 이 쪽지 커밋까지 한 묶음.
- 새 DEM 시험 둘 · 믹서 검증기는 지금 전체 게이트 목록 밖이다 (Codex 커밋 = 추가만 · `scripts/check_all.sh` 무변경) — 게이트에 넣을지는 반박 창 검토 뒤.

## 3. 상태 (Codex 쪽지 그대로 · 이 반입이 바꾼 것 없음)

- DEM = 비활성 생산기 후보. 실제 관측 → 단계 전이 · 완전한 경계 프레임 · P2 ULPR / 언로딩 · 자유 표면 연결 = 미구현 · 실제 T5 / T11 / T12 = NOT_RUN · physical_ready = false · DEMP-01 / 02 원장 상태 변경 없음 · 50 kg 0.7 / 1 µm 비교 = 세대 2 안 (같은 실제 정적 압력 · 하중 ↔ 면적 환산 미확인 · 300 MPa 와 동치라 쓰지 않음).
- LHS = 문서 정책 RATIFIED · 실제 동결 NOT_FROZEN (실제 신원 · 명부 · 정본 구간 · A/C · 접근 범위 · 값 GO = 별도 · null).
- 믹서 = 비활성 사본 (운영 봉인 · launch 73 · 원 자산 40 그대로) · 원장 제안 = `apply_now: false` (외부 한정 확인 뒤 Claude 적용) → 이번 반입에 원장 적용 없음.

## 4. 다음

- 반박 창 검토 ZIP 둘 발송 = 1저자 (DEM = 생산기 · 합성 guard · T5/T11 문안 한정 · 믹서 = 현재 소스 / 메타 사본 결속 · 비활성 경계 한정).
- 다음 새 가지 바탕 = `origin/claude/sdcp-dem-manuscript-si-pqwtv8` 최신 (이 쪽지 커밋 push 뒤).
- Rint 파일 (`scripts/rint_r_chain.py` · 그 시험 · Rint ② 리뷰 문서) = Claude 세션 몫 그대로 (회차 ⑤ 준비 중).
