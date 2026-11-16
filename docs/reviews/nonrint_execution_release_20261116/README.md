# 비 Rint 실행 준비 전달 — 2026-11-16

| 트랙 | 계산 | 상태 | 숫자 | 다음 |
|---|---|---|---|---|
| DEM 우선 (수영) | S/F 형상 출력 · WSL CPU1 | 1 블록 준비 | 고정 커밋 시험 14/14 · 기존 9/9 | 1저자 실행 · 결과 묶음 수령 |
| DEM 우선 C 믹서 | 승인 A/B V2 위 E0 한 팔 · ibb NP20 | 2 발사 GO 대기 | 모의 19 통과 · 실제 링크 1 skip · B 283/283 보존 | 1저자가 블록에서 GO_E0_ONCE 입력 뒤 실행 |
| DEM 우선 A G2c′ | 남은 실패 경로·재큐 자격 | 3 기존 내용 판정 고정 | NP2=366288 · NP4=366290 | 새 계산·제출·N40000 재실행 0 |
| 공유 출력 문구 | 대기열 2–5 | 4 변경안만 | 대상 코드 변경 0 | Claude와 줄·시험·영향 확인 뒤 별도 수정 |

## 1. 바탕과 고정 핀

가지 `codex/suyoung-e0-release-1116`, 바탕 `f1b9d002fdd844d6b4be089b73322051e8b312df`.
1저자 11-16 동결 축소 뒤 수영 검토 로컬 바이트 두 개를 그대로 커밋했다. 이 두 파일은 이전 `docs/reviews/suyoung_shape_preparation_20261116/local_preparation_receipt.json`의 SHA256과 같다.

- 수영 실행 핀: `c759c4c7ab7abec2148e23fa231d004c1d4d0fec`.
- 믹서 발사 도구 최종 핀: `997aabe1b5a702e2f389007e3923018d778ce857`. 구현 `6c1144cde6b3671be55b85c626044020ae1f734d` 뒤 영수증의 등록 문서 참조 한 곳을 리포 전체 경로로 맞췄다.
- 믹서 승인 B의 역사 소스 핀: `8231f395cda98fed8dbbf5422ccda003b11a8da9`. 발사 도구 핀으로 바꿔 쓰지 않는다.
- 승인 A/B V2 반환 SHA256: `6f7f407479af6282b9c8d4e83afa86645d4fda1506b29801be2165dcc2965737`.

현재 문서 끝 커밋은 위 실행 핀을 바꾸지 않는다. Claude 반입은 cherry-pick -x로 하며 원격 고정 핀을 보존한다. 이미 반입한 `85ac45386`, `f1b9d002f`, `9aa6b7427`, `ad7c1f826`, `8231f395c`는 이번 목록에 다시 넣지 않는다.

## 2. 문서와 검사

- 수영: `docs/reviews/nonrint_execution_release_20261116/suyoung_release.md`.
- 믹서: `docs/reviews/nonrint_execution_release_20261116/mixer_release.md`.
- 변경 전 제안: `docs/reviews/nonrint_execution_release_20261116/post_attempt4_change_proposal.md`.
- 재현 범위·수치: `docs/reviews/nonrint_execution_release_20261116/verification_receipt.json`.
- 리포 밖 전달물의 신원만: `docs/reviews/nonrint_execution_release_20261116/artifact_binding.json`.

리포에는 실제 접속 정보·명령 블록 원문·원 결과 로그를 넣지 않는다. 블록 두 개와 각 고정 소스 tar는 1저자용 다운로드 ZIP, 코드·문서·패치는 Claude 인계 ZIP으로 따로 전달한다. 새 리포 문서 참조는 전체 경로로 썼다. Claude가 고친 기존 G2c′ 문서 및 내부 해시 목록은 이 가지에서 덮지 않는다.

## 3. 범위

현장 접속·계산·제출·새 운영 재봉인·원장 변경 **0**. 준비된 개발 계산을 물리 자격이나 논문 숫자로 채택하지 않는다. 믹서 E0 발사 GO는 별도이고 다음 팔로 자동 진행하지 않는다.

고정 가지 `codex/rint-rtr01-receipt-1113`는 push하지 않는다. kgy 작업 트리·저장본·계산, Rint 공유 소스와 Claude 전용 네 경로는 건드리지 않는다. 50kg 응력은 이미 Love–Weber이며 재작도하지 않는다. 후막은 계획 없음으로 제외한다.
