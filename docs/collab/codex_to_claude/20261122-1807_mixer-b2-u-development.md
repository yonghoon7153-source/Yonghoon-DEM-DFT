# 믹서 B2-U 개발 1팔 · 발사 준비

| 트랙 | 계산 | 상태 | 숫자 | 다음 |
|---|---|---|---|---|
| 믹서 B2-U | 점착 단계 B2 · U 2회전 | 1저자 GO 수령 · WSL 블록 준비 | 1노드, MPI 20, 상한 48시간, 234장 | 1저자 1회 발사 · U 정상 반환 및 W9 확인 |

가지 `codex/mixer-b2-u-1122`는 B1 판독 끝 `616162d9567ead90b5d69b8715c59110e07dabbb`에서 시작한다. 발사 소스 핀은 `f9c8ee5a2cc590ceb70766d144e82ad571942535`이다. 1저자 반입 결정 뒤 이 핀 → 이 쪽지 커밋 순으로 cherry-pick -x 한다. 두 커밋의 SHA와 stable patch-id는 HANDOFF.md에 기록한다.

- 새 소스와 회귀는 `scripts/mixer_b2_u_ibb.py`, `scripts/test_mixer_b2_u_ibb.py`다. 원 승인 B 입력 283/283와 이전 컨트롤러 3개를 그대로 사용한다. 과거 B1의 U/C 원 영수증과 해시 목록을 읽었고, 로컬에 있는 원 보고/전체 tar 4개 모두 해당 목록과 일치했다.
- Linux 로컬 모의 시험은 B2 새 6실패 → 6/6, 앞 B1 쌍 7/7 및 수집 3/3이다. 완성 배포 tar와 원 B1 반환 두 개로 제출기를 호출해 U의 모의 제출 1개, 같은 승인 재사용 거부, C 호출 0개, 234장·종료 신원·반환 해시 2/2를 확인했다. 검증기 `docs/reviews/mixer_b2_u_development_20261122/check_release.py`는 소스 tar와 B1 U/C 원 반환 폴더를 인수로 받으며 외부 프로세스 실행과 네트워크 연결을 차단한다. 현장 접속·제출은 0회다.
- 운영자 ZIP의 SHA256은 `a6af12595aecee0bac966a6ba71373a47a746f63b5a771d5100fced79550f601`, 소스 tar는 `332148bd05db2718da30487352cc54523cb69b9abb92db43a5af44a8fa51df64`, TXT는 `b7896fc58bc36d5cacc078282f2cb75d2c3ff73678ce05938b44af88c8f61ea9`다. ZIP은 별도 전달한다.
- 실험 질문·고정 덱 신원·결정 경계는 `docs/reviews/mixer_b2_u_development_20261122/README.md`에 있다. 조회 모드 STATUS는 기존 잡을 한 번 읽고, RETURN은 기존 U 잡만 회수한다. B2_C_AUTHORIZED=False를 유지한다.

공유 기록 제안 — 11-22 B1 U/C 반환 뒤 1저자 B2-U 개발 1팔 GO. 고정 소스 f9c8ee5a2 · 2회전, NP20, 48시간 상한, 234장. 현장 실행 대기. B2-C는 U 정상 반환과 W9 확인 뒤 별도 결정.

1저자 GO 요청: B2-U 한 팔은 승인 완료. 1저자 실행 자리는 `bash PASTE_B2_U.txt GO_B2_U_ONCE`다.
