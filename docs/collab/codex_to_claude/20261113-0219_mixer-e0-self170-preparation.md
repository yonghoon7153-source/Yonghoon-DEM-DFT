# 믹서 E0 등록 후보 · SELF-170 인계 (2026-11-13)

| Q | 1저자 결정 | 권고 | 상태 |
|---|---|---|---|
| E0-R1 | 등록 초안 §18의 마지막 2회차 표·아침 표시 비준 기록 | 받은 권고대로, 실행 승인과 분리 | 확인 0 |
| E0-R2 | 운영 재봉인 A/B | R1 및 Linux 전체 합성 재현 뒤 별도 승인 | 승인 0 |

권고안 전제 (E0-R1)로 **등록 후보 수령·SELF-170 집중 수정까지** 했다. 전체 HOLD · 현장/연구 실행 0 · 새 pilot 결과 0 · 운영 재봉인 0. E0 한 팔의 내부 리뷰 대체 예외만 유지한다. P1 A/B는 1저자가 보낸 원 핀의 독립 판정 대기 중이며 이 변경에 섞지 않았다.

## 1. 바탕·반입 순서

- 바탕 = B `56f4cfbb1d26371007b460a992d4cfc1ef68e950`. 쪽지 작성 직전 fetch에서 같음. 새 바탕 전환·충돌 0.
- 반입 대상 = `codex/mixer-e0-1113`. Claude가 아래 순서로 cherry-pick -x. 기존 Codex 가지 재작성 없음.
- ① `<<sha:fix: bound SELF-170 canaries in mixer selftest>>`
  - `scripts/mixer_smoke_blind.py`
  - `scripts/test_mixer_self170_canaries.py`
  - `docs/reviews/mixer_self170_20261113/README.md`
  - `docs/reviews/mixer_self170_20261113/synthetic_summary.json`
- ② `<<sha:docs: stage mixer E0 registration candidate and handoff>>`
  - `docs/reviews/mixer_e0_pilot_registration_20261113/README.md`
  - `docs/reviews/mixer_e0_pilot_registration_20261113/intake_manifest.json`
  - `docs/reviews/mixer_e0_pilot_registration_20261113/received/baseline_table.md.txt`
  - `docs/reviews/mixer_e0_pilot_registration_20261113/received/changes.md.txt`
  - `docs/reviews/mixer_e0_pilot_registration_20261113/received/e0_pilot_registration_draft.md.txt`
  - `docs/reviews/mixer_e0_pilot_registration_20261113/received/fill_queryb_disposition.md.txt`
  - `docs/reviews/mixer_e0_pilot_registration_20261113/received/query_block_b/read_query_bundle_b.py.txt`
  - `docs/reviews/mixer_e0_pilot_registration_20261113/received/review/disposition.md.txt`
  - `docs/reviews/mixer_e0_pilot_registration_20261113/received/review/disposition2.md.txt`
  - `docs/reviews/mixer_e0_pilot_registration_20261113/received/review/rereview_report.md.txt`
  - `docs/reviews/mixer_e0_pilot_registration_20261113/received/review/review_report.md.txt`
  - `docs/reviews/mixer_e0_pilot_registration_20261113/reference_map.json`
  - `docs/reviews/mixer_e0_pilot_registration_20261113/registration_candidate.md`
  - `docs/collab/codex_to_claude/20261113-0219_mixer-e0-self170-preparation.md`

- 지운·옮긴 기존 리포 파일: **없음**. 새 수령 사본은 처음부터 역사 첨부 `.md.txt`로 제출한다. 후보 참조는 현재 파일·tgz 멤버·미수령 근거를 구분했다.
- 공유 원장·게이트·진행 기록·Rint·봉인32·litdb·운영 seal 변경 0.

## 2. 무엇과 확인

| 항목 | 결과 | 한정 |
|---|---|---|
| E0 | 원 등록 767줄·9첨부 원바이트 수령; 현재 경로로 읽는 후보와 reference map | 원 규칙·문턱 변경 0; 내부 리뷰는 독립 판정 아님; QY 원 묶음 미수령 |
| SELF-170 | 같은 11메서드: red rc1·15 assertion 실패·오류0 → green rc0·11/11; 제거 변이3 검출 | 실제 검사식 AST·고정 시각 사본만. 전체 `--selftest`·고정 시각 전체사본 Linux 재현은 미실행 |
| 보존 | selftest 밖 AST 동일 | 도구 파일 해시는 변경. 운영 봉인에 지금 반영하지 않음 |
| check_doc_refs.py (무인자) | rc1; 없는 경로0·부재 SHA96 | 바탕과 같은 Windows 구분자 문제. 96/96이 slash 정규화 시 기존 예외 표와 일치. **native 통과로 적지 않음** |
| check_review_findings.py (무인자) | rc0 | 원장 자기일관만; 전체 gate는 반입 때 Claude |

문서 초기 운반에서 나온 경로 오류301은 최종 후보의 참조 정리로 0이 됐다. 원 문서를 `.md.txt`로 보존하는 대신 활성 후보의 참조를 개별 매핑·검증했고, 미수령/미확인은 표지로 남겼다. Windows 체크 문제로 검사기·공유 예외표를 수정하지 않았다.

## 3. Claude가 넣을 공유 기록 제안 (지금 직접 수정 0)

| 파일·자리 | 넣을 글 그대로 |
|---|---|
| docs/reviews/findings.json · SELF-170.note 끝 | 11-13 Codex 실무 후보: selftest canary 세 곳을 ASCII 숫자 앞 경계와 literal escape로 수정. 집중 합성 11메서드 red 실패15/오류0 → green11/11, 변이3 검출, selftest 밖 AST 동일. 전체 Linux selftest·고정 시각 전체사본은 아직 미실행. 운영 재봉인 A/B와 도구 해시를 함께 고정할 것. 원장 open 유지; 독립 verified 근거 아님. |
| docs/session_20260923_progress.md · 믹서 E0 마지막 줄 뒤 | 11-13 E0 등록 767줄 원본·내부 리뷰 수령 및 참조 정리 후보. 비준 확인→Linux 전체 합성→별도 운영 재봉인 A/B→내부 E0 한 팔 검토→1저자 발사 GO 대기. 새 pilot 결과0·전체 HOLD. |
| scripts/check_all.sh | 이번 추가 줄 없음. SELF-170 집중 회귀는 수동 인계 검증으로만; 전체 gate 변경은 별도 검토. |

Windows 진단 제안: `scripts/check_doc_refs.py`의 walk_docs가 내는 문서 키를 예외 조회 전에 POSIX `/`로 통일하고 Windows 상대경로 회귀를 먼저 추가할 것. 이번 범위에서는 구현하지 않았다.

## 4. 다음

E0-R1 확인·Linux 합성 재현·재봉인 승인 대기. 다음 wave와 공유 자산의 독립 반박 GO는 별개. 수령 사본과 red/green/변이 증거는 일일 ZIP에서 전달한다. 발송은 1저자, 반입은 Claude.
