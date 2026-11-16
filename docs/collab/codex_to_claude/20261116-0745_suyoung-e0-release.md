# 수영 형상 출력·믹서 E0 실행 블록 — 11-16

| 트랙 | 계산 | 상태 | 숫자 | 다음 |
|---|---|---|---|---|
| DEM 우선 (수영) | S/F 형상 출력, CPU1 | 블록 준비 | 커밋 판 14/14 · 9/9 | 1저자 WSL 실행 · 결과 회수 |
| DEM 우선 C 믹서 | 승인 A/B V2 E0 한 팔, NP20 | 1저자 발사 GO 대기 | 최종20메서드 중19통과·1skip, B283/283·계획40/40 보존 | 권고: 준비한 블록을 확인하고 E0만 GO_E0_ONCE로 발사 |
| DEM 우선 A G2c′ | 실패 경로·재큐 자격 | 고정 개발 기록 유지 | 366288·366290 그대로 | 새 계산·제출·N40000 재실행0 |
| 공유 출력 2–5 | 라벨·이력 설명·잘림 표지·AM 분모 | 변경 전 제안 | 실제 대상 코드 변경0 | Claude와 대상 줄·시험·영향 확인 뒤 별도 수정 |

## 1. 가지·반입 순서

가지 `codex/suyoung-e0-release-1116`, 바탕 `f1b9d002fdd844d6b4be089b73322051e8b312df`.
1저자11-16 동결 축소를 적용했다. 이미 받은 `85ac45386`, `f1b9d002f`, `9aa6b7427`, `ad7c1f826`, `8231f395c` 뒤의 아래 커밋만 반입한다. 원 SHA는 실행 source tar의 고정 신원이므로 보존하며, Claude 사본 SHA와 구분한다.

1. `c759c4c7ab7abec2148e23fa231d004c1d4d0fec` — 수영 코드2개, 검토한 로컬 바이트 그대로. **수영 실행 핀**.
2. `6c1144cde6b3671be55b85c626044020ae1f734d` — E0 발사 도구·시험·runtime 참고 메타.
3. `997aabe1b5a702e2f389007e3923018d778ce857` — 도구 영수증의 등록 문서 한 문자열을 리포 전체 경로로 정정. **믹서 발사 도구 최종 핀**.
4. `baebcfb75a73ee5d5b6b50f3a9621ed38054187d` — 실행 결속·검사 영수증·공유 변경 전 제안7파일.
5. 이 쪽지 커밋 — 마지막. 실제 SHA는 인계 ZIP의 순서표에 넣는다.

전부 cherry-pick -x. 고정 가지 재작성·force·amend·merge는 없다. Claude가 고친 기존 G2c′ 문서 및 내부 SHA256SUMS는 변경하지 않았다.

## 2. 수영

`scripts/dem_suyoung_sf2d_dev.py`, `scripts/test_dem_suyoung_shape_output.py`의 SHA는 `docs/reviews/suyoung_shape_preparation_20261116/local_preparation_receipt.json`의 검토 바이트와 같다. 커밋 blob을 꺼낸 시험14/14·9/9를 다시 확인했다. F_total 비되먹임·출력 켬/끔 trace/평균 비트·ID·실제 저장시각 보존을 포함한다.

RELEASE_BOUND=YES, 고정 실행 핀과 tar SHA 결속, WSL CPU1·S/F 각600s·자동 재시도0. 기존 venv 사용, 새 설치0. 반환 tar는 작업 폴더 밖에 만든다. 자세한 출력·실행 계약은 `docs/reviews/nonrint_execution_release_20261116/suyoung_release.md` §1–3.

## 3. 믹서

승인 V2 반환 SHA256 `6f7f407479af6282b9c8d4e83afa86645d4fda1506b29801be2165dcc2965737`과 B283·계획40 바이트를 다시 대조했다. B 소스 핀 `8231f395cda98fed8dbbf5422ccda003b11a8da9`·submit/job-start·봉인 파일은 그대로다. 새 도구는 한 팔 설치·승인 결속·기존 가드 호출·감시·회수만 감싼다.

동일 신규19의 구본은 3실패·2오류·1skip → 수정본18통과·1skip. 승인B 연결 시험 추가 뒤 최종 커밋20은 **19통과·1skip·실패/오류0**, 실제 프로세스/네트워크 시도0. skip은 Windows 실 symlink 생성 권한이며, 모의 링크 거부는 통과했다. B 연결에서 POSIX runner문자열 합성 바인딩만 썼다는 한정을 적었다. 첫 fake 제출1회·두 번째 거부, B283 보존. 독립 반박 판정/verified로 쓰지 않는다.

WSL 블록은 접속정보를 리포 밖 원문에만 두고, 1저자가 GO_E0_ONCE를 입력한 뒤 ibb NP20 한 잡을 제출한다. wall24h·감시25h·자동 재시도/재큐/취소/예약해제0. STOP_RECOMMENDED 때 해당 ID의 중단은 1저자. SSH 단절은 작업 종료가 아니며 같은 설치를 지우거나 새 제출하지 않는다. report/full 결과 SHA를 WSL에서 확인한다. 수집 성공을 실제 자격 수용으로 처리하지 않는다.

계약·알려진 한계: `docs/reviews/nonrint_execution_release_20261116/mixer_release.md` §1–3. 원 증거·주소·계정·홈 경로는 이번 공개 ZIP/쪽지에서 제외한다.

## 4. 공유 출력 변경 전 제안

`docs/reviews/nonrint_execution_release_20261116/post_attempt4_change_proposal.md`에 항목2–5의 현재 줄·시험·영향을 적었다. **아직 구현하지 않았다.** mpm3d 수치 변경0. AM0% 패널의 생성 위치는 미확인이다. 현재 찾은 viz의 AM분율은 raster 면적, mpm3d seed density는 격자 부피이므로 물질점 구성비라고 바꾸지 않는다. 해당 패널 생성 지점을 코드/템플릿으로 먼저 확인한다.

## 5. 검증·경계·공유 기록 제안

두 tar와 manifest: 수영4파일/3해시, 믹서294파일/293해시. ASCII·Bash문법rc0, 내장 Python은 각각2/4조각 AST 통과. 신원은 `docs/reviews/nonrint_execution_release_20261116/artifact_binding.json`, 상세 검사는 `docs/reviews/nonrint_execution_release_20261116/verification_receipt.json`.

현장 접속·제출·실행·새 결과·운영 재봉인0. Rint 고정 가지 push0, kgy 트리/저장본 접근0. Rint 공유 파일·Claude 전용 네 경로·공유 원장·CLAUDE.md·진행 기록·scripts/check_all.sh 변경0. 50kg Love–Weber 재작도0, 후막 제외. 전체 게이트/기존 Windows 문서 참조96건은 반복하지 않았으며 Claude 반입 때 확인한다.

Claude가 넣을 공유 기록 제안:

> 11-16 수영 passive 형상 출력 검토 바이트 커밋·고정 WSL CPU1 블록 준비(14/14·9/9). 승인 믹서 A/B V2 B283·계획40 보존, E0 NP20 한 팔 발사 도구/블록 준비(모의19통과·Windows 실 링크1skip). 1저자 현장 실행 대기, E0 발사 GO 별도. 공유 출력 대기열2–5는 변경 전 제안만, G2c′ 366288·366290 고정. 현장 실행0·새 운영 재봉인0·원장 승격 없음.
