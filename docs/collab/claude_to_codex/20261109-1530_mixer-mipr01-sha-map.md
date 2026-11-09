# Codex 믹서 MIP-01 Windows namespace 잔여 (MIPR-01) 수정 후보 반입 대응표 — 2026-11-09 (Claude 서브 세션 · 가지 B)

1저자 11-09 전달 = Codex 실무 창 인계 ZIP (codex_mipr01_windows_path_fix_dcfd62262f10_claude_handoff_20261109.zip · sha256 34e49e8f… · 내부 해시 15/15 · 안의 재검토 ZIP = 1저자가 반박 창에 보낸 것과 같은 바이트 (sha256 c8e7dab4…)) · 원격 가지 `codex/mixer-windows-path-fix-1109` 끝 = `dcfd62262f10`.
반입 기록이며 실제 OS 링크 · 적대적 동시 변경 자격 · 운영 재봉인 · 현장 자격 · 실행 GO 가 아니다 — 전체 HOLD 그대로.

## 1. 대응표

| # | Codex 가지 | Codex 원 커밋 | B 커밋 | 처분 |
|---|---|---|---|---|
| 1 | codex/mixer-windows-path-fix-1109 (바탕 B `69d714d09`) | `be4388d0c1d3` (준비 사본 · 원 `73e659273fd2` 와 같은 내용) | — (건너뜀) | patch-id 22b82297… = B `1df1ba5a7` 와 같음 → 중복 적용 안 함 |
| 2 | 같은 가지 | `d310f741a636` (이전 고침 사본 · 원 `3ca47af5b0ac` 와 같은 내용) | — (건너뜀) | patch-id ec0b0ada… = B `f46c73f4c` 와 같음 → 중복 적용 안 함 |
| 3 | 같은 가지 | `dcfd62262f10` | `86bceb195` | 이번 반입 (`cherry-pick -x` · 충돌 0 · 바뀐 8 파일 (검증기 1 고침 · 문서 · 시험 7 추가) blob = 원 커밋 8/8 · patch-id 3efabcb2… = 원 커밋 = ZIP 패치 03) |

## 2. 독립 검토 수령 · 원장

- 반박 창 재확인 (리뷰 핀 `3ca47af5b0ac` = B `f46c73f4c` · 판정 ZIP sha256 6bcff75f…) = MIP-01 **부분 해결 · 열림** · 잔여 재현 MIPR-01 (같은 P2 · 별도 계상 안 함) · 새 P1 / P3 0.  원 ZIP = 외부 위치 문구 → 리포 밖 보존 · 리포 = `docs/reviews/mixer_windows_path_fix_20261109/intake_receipt.json` (신원 · 수령 바이트 감사).
- 원장 (이 쪽지와 같은 커밋): MIP-01 = claimed_fixed 유지 · sha `f46c73f4c` → `86bceb195` · 부분 해결 수령과 잔여 MIPR-01 을 메모로 · 독립 재확인 대기 · verified 아님 (고친 쪽 · 검토 쪽 모두 Codex 창) — Codex 원장 제안 (`docs/reviews/mixer_windows_path_fix_20261109/ledger_proposal.json`) 그대로.

## 3. 우리 기계 재실행 (11-09 · 리눅스 Python 3.11 · 합성만 · 판정 아님)

| 대상 | 결과 | Codex 기록 (Windows Python 3.12) |
|---|---|---|
| 기존 일반 경로 회귀 `docs/reviews/mixer_inactive_path_fix_20261109/test_evidence_boundary.py` (새 검증기 sha256 91a01359…) | 5/5 rc 0 | 5/5 rc 0 (CLI 41 회) |
| 검증기 `--mode old` · `verify` · `preparation-tests` | rc 1 (옛 메타 8 실패 = 기대) · 0 · 0 | 같음 |
| 출처 시험 `docs/reviews/mixer_inactive_preparation_20261109/test_snapshot_provenance.py` | 5/5 rc 0 | 5/5 |
| 새 Windows 전용 시험 `docs/reviews/mixer_windows_path_fix_20261109/test_windows_path_boundary.py` | 리눅스에서 실행 거부 (`requires Windows` · 설계) — 우리 쪽 재현 못 함 | 같은 시험 바이트 수정 전 subtest 실패 148 · rc 1 → 5/5 rc 0 |
| 후보 폴더 · 작업 트리 | 43 파일 그대로 · 변경 0 | 43 · 의존 86 보존 |

## 4. 다음

- 재검토 ZIP (MIPR-01 한정) = 1저자 11-09 반박 창 발송 끝 → 판정 수령 = 다음 인계 때.  Windows 쪽 확인이 더 필요하면 1저자가 그 기계에서 돌릴 명령을 Claude 가 준다 (1저자 11-09 제안).
- 다음 새 가지 바탕 = `origin/claude/sdcp-dem-manuscript-si-pqwtv8` 최신 (이 쪽지 커밋 push 뒤).
