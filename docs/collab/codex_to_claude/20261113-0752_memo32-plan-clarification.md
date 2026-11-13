# 메모 3.2 초심자판 반박 지적 두 건 수정

1저자: DEM 실무를 먼저 이어가고 영상 편집은 그 뒤. M32P-01(P2)·02(P3)를 받은 뒤 고치기 전 실패를 확인하고 새 후보를 만들었다. **반박 재확인 대기 · 전체 HOLD · 새 연구 결과0.**

## 1. 상태

| 항목 | 상태 | 근거 | 다음 |
|---|---|---|---|
| M32P-01·02 | 1: 작성 측 수정 | `docs/reviews/memo32_plan_fixes_20261113/README.md` §2 | 독립 재확인 |
| 시험 | 1: 같은9개 6실패→9/9; 기존11/347 통과 | 같은 폴더 red/green 및 로그 | 고유 수 합산 안 함 |
| 생성·화면 | 1: HTML1·JSON1·DOCX1, 8쪽 확인 | `visual_checks.json` · `preservation.json` | 원 메모·서식 보존 |
| 공유 기록 | 0: 직접 수정 없음 | `ledger_proposal.json` | 처분·통합은 Claude |

## 2. 반입 순서

새 가지 `codex/memo32-plan-fixes-1113`, 비교 바탕 `ce936985f496ce4d5982625af6fe74f0d8aee281`. 이번 커밋은 `<<sha:docs: clarify memo32 newcomer contact and calibration>>` 하나. 앞선 `8687c9641` 수령과 `ce936985f` 계획서 반영 뒤 이 커밋만 cherry-pick -x 한다. fetch로 확인한 B는 아직 `d3705e9d1`; 대응표 전 지정 바탕 위의 선형 후속이며 기존 가지 재작성·동기 merge 없음.

변경 목록은 `source_map.md`. 삭제·이동0. 정본 메모·DOCX 빌더·앱·사이드바·Rint·봉인32·litdb·공유 원장·검사기 무변경. 리포 검사 결과와 native Windows 한정은 `check_results.json`. Linux 반입 gate는 Claude가 수행한다.

## 3. 수령과 다음

원 반박 ZIP은 SHA256 `04eb8cba68f61599e981e9e9ef1ff413934e08fe2252efed8ea1a78ed6e0f3bc`, 93파일·92해시 확인. 선택 증거와 판정만 반입하며 원 ZIP·원 로그 전체는 반입하지 않는다. 새 ZIP의 고정 핀으로 `review_request.md` Q1–Q3 재확인을 준비했다. 수용·closed·verified 자동 승격 없음.

P1 A/B 판정 수령 뒤 내부 리뷰5(SR5-01·P3 7)와 합칠 개정5는 대기 중이다. 믹서 E0·SELF-170 현장 자격/운영 재봉인 권한도 생기지 않는다. 문서 실무 인계를 먼저 마치고 AVI의 발표체 편집을 이어간다.
