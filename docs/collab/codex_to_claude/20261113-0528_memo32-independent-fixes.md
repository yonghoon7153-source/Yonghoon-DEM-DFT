# [DEM 우선 (수영)] 메모 3.2 판정 수령 · 수정 후보 인계

전체 HOLD. 연구 결과 0 · 생산 구현/실행/값 열람/봉인 0. M32R-01–06의 문서 수정 후보를 보낸다. 수정 후보의 독립 재확인 전이다.

| 사용자 결정 | 권고 | 현재 |
|---|---|---|
| Q1. M0 적합 수 | 기존 공통 규칙대로 적합 1 + 사전 고정 2; 3자유도 예외는 열지 않음 | 권고안 전제 (Q1); 맞출 변수/값/출처는 등록 전 미정 |

## 1. 반입

- 바탕 B: `d3705e9d11886e0a0cefe3cf6a961e7d42b6901c` (쪽지 직전 fetch에서 같음).
- 대상 가지: `codex/memo32-fixes-1113`.
- 순서: `<<sha:docs: address memo32 independent findings M32R-01-06>>` 한 커밋만 cherry-pick -x. 원 요청 가지를 다시 반입할 필요 없음.
- 지운/옮긴 파일: 없음. 기존 수정은 메모 하나, 나머지는 새 수령·처분·시험·요청·쪽지.

## 2. 상태와 근거

| 항목 | 상태 | 근거 | 다음 |
|---|---|---|---|
| 원 독립 판정 | 문서 부분 수용; 새 P1 1/P2 2/P3 3 | 원 요청 `1e823a34ce8459f7596c8c80e4874bc933220733`; `docs/reviews/memo32_fixes_20261113/received/verdict.md.txt` | 6건 수정 후보 재확인 |
| 기존 DRD | 8/13 문서 종결 가능; 5/13 부분 + SELF-161 부분 | 같은 폴더 README §1–2 | 원장 직접 수정 없음 |
| 수정 | cap 목표점 미확정; U6(c) 초과/누락 중단; 필수 상자 비교 완전성; O7/M0/LA25 정정 | 메모 §0, §3, §4, Q9, D-1–D-3; README §2 | 등록·숫자·실행 승인 별개 |
| 원 반례 | 원 소형 탐침4 rc0, JSON5 의미 일치 | `docs/reviews/memo32_fixes_20261113/review_replay.json` | 생산 함수 검증 아님 |
| 시험 먼저 | 최초14메서드/실패관측28/오류0 후 수정; 최종 동일 suite 전 실패메서드12/14·관측29·오류0 → 후14/14; 변이4/4 | `docs/reviews/memo32_fixes_20261113/contract_results.json` | 문서 수동 전사·증인 검사 한정 |
| 필수 저장소 점검 | doc refs rc1: 경로0·SHA96 (기존 Windows 예외96/96); findings 무인자 rc0. native PASS 아님 | `docs/reviews/memo32_fixes_20261113/check_results.json` | 전체 gate 두 조각은 반입 때 Claude |

## 3. 공유 기록에 넣을 제안

원장 제안만: `docs/reviews/memo32_fixes_20261113/ledger_proposal.json`. 원 판정의 8건은 문서 범위 종결 가능 근거를 보탬. M32R-01(P1), 02·03(P2), 04–06(P3)은 새 문서 수정 후보 claimed_fixed 제안이며 독립 종결/verified로 자동 올리지 않는다. 기존 DRD-01·08·10·11·12 및 SELF-161와 연결하고 같은 반례를 중복 계상하지 않는다.

CLAUDE.md 및 `docs/session_20260923_progress.md`의 [DEM 우선 (수영)] 메모 줄에 넣을 문장:
> 11-13 메모3.2 독립 판정 = 문서 부분 수용 (DRD13 중8 종결 가능; M32R-01 P1,02·03 P2,04–06 P3). Codex 수정 후보 수령: cap 목표점 미확정, U6(c) 중단, 필수 상자 비교 완전성 및 O7/M0/LA25 정정. 문서 합성14/14·변이4/4; 실제 자격0, 독립 재확인 전, 전체 HOLD. 근거 = docs/reviews/memo32_fixes_20261113/README.md.

계획서 웹앱·docx 확정 반영은 수정 후보 독립 판정 뒤다. 원 반박 수령 ZIP은 전체 반입하지 않고 선별 원바이트10개와 수령 해시를 넣었다. 외부 원 ZIP은 재확인 패키지에 그대로 동봉한다. P1 A/B 독립 판정 대기/내부5회차 초안, E0-R3 수령과 SELF-170은 별개이며 이번 판정으로 바뀌지 않는다. Rint·litdb 정본·봉인32·공유 파일 변경 없음.

## 4. 이 커밋의 파일 목록

- `docs/reviews/dem_redesign_direction_20261109/memo_v3_2.md`
- `docs/reviews/memo32_fixes_20261113/appendix_cap_revert_summary.txt`
- `docs/reviews/memo32_fixes_20261113/box_revert_summary.txt`
- `docs/reviews/memo32_fixes_20261113/cap_revert_summary.txt`
- `docs/reviews/memo32_fixes_20261113/check_contract.py`
- `docs/reviews/memo32_fixes_20261113/contract_results.json`
- `docs/reviews/memo32_fixes_20261113/dense_revert_summary.txt`
- `docs/reviews/memo32_fixes_20261113/edit_map.json`
- `docs/reviews/memo32_fixes_20261113/green_summary.txt`
- `docs/reviews/memo32_fixes_20261113/ledger_proposal.json`
- `docs/reviews/memo32_fixes_20261113/log_selection.json`
- `docs/reviews/memo32_fixes_20261113/PREATTACK.md`
- `docs/reviews/memo32_fixes_20261113/README.md`
- `docs/reviews/memo32_fixes_20261113/received/branch_probe.py.txt`
- `docs/reviews/memo32_fixes_20261113/received/branch_results.json`
- `docs/reviews/memo32_fixes_20261113/received/contact_probe.py.txt`
- `docs/reviews/memo32_fixes_20261113/received/contact_probe_results.json`
- `docs/reviews/memo32_fixes_20261113/received/convergence_results.json`
- `docs/reviews/memo32_fixes_20261113/received/findings.json`
- `docs/reviews/memo32_fixes_20261113/received/literature_reproduce.py.txt`
- `docs/reviews/memo32_fixes_20261113/received/literature_results.json`
- `docs/reviews/memo32_fixes_20261113/received/manifest.json`
- `docs/reviews/memo32_fixes_20261113/received/probe_convergence.py.txt`
- `docs/reviews/memo32_fixes_20261113/received/verdict.md.txt`
- `docs/reviews/memo32_fixes_20261113/red_summary.txt`
- `docs/reviews/memo32_fixes_20261113/review_replay.json`
- `docs/reviews/memo32_fixes_20261113/review_request.md`
- `docs/reviews/memo32_fixes_20261113/check_results.json`
- `docs/collab/codex_to_claude/20261113-0528_memo32-independent-fixes.md`
- `docs/reviews/memo32_fixes_20261113/received/.gitattributes`
