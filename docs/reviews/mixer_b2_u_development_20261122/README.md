# B2-U 개발 회전 한 팔 · 2026-11-22

| 트랙 | 계산 | 상태 | 수량·자원 | 다음 |
|---|---|---|---|---|
| 믹서 B2-U | 층상 충전 후 2회전 | 1저자 개발 GO · 현장 제출 전 | ibb 1노드, MPI 20, 48시간 상한, 234장 | 1저자 발사 → U 반환과 W9 대조 → C 별도 결정 |

## 계산 질문

같은 충전 시드 32452843과 같은 AM 상대 점착에서, 등록 덱의 SE–SE 기준 점착을 B1-U의 100배로 높이면 SE 군집과 공간 조성이 어떻게 달라지는가. 고정 덱의 Bo_SE는 B1-U 0.21244, B2-U 21.244다. 두 팔 모두 γ_AM/γ_SE = 0.1, γ_W/γ_SE = 0.00256이다. 상대비를 고정한 변화이므로 연동되는 쌍의 점착도 함께 변한다. B1-U 한 팔의 실제 소요는 25시간 7분 43초였다. B2-U의 실측 시간은 반환 때 기록한다.

## 제출과 회수

- 배포본의 `PASTE_B2_U.txt GO_B2_U_ONCE`를 1저자가 WSL에서 한 번 실행한다. 고정 소스 tar가 TXT와 같은 폴더에 있어야 한다. B1 캠페인은 읽기 전용으로 참조하고 B2-U는 새 디렉터리에서 시작한다.
- U 368139와 C 368316의 고정 포인터·해시 목록·완료 상태·종료 신원, 두 팔을 연결한 개발 판독, 승인 B 소스 283파일과 B2-U의 다섯 입력을 확인한다. U 하나에만 정책과 예약을 발행한다. 고정 제출기는 `sbatch --no-requeue`로 한 노드·20 CPU 한 잡을 요청한다.
- 대기·실행 중 CPU에 20을 더해 60 이내, 동시 first8 0, 저장 공간·inode·OST·QoS와 런타임 신원은 실제 제출 직전에 기존 관문에서 확인한다. 1저자가 승인한 표본 간격은 32,976 step, 저장 형식은 17자리다.
- 분리된 감시기가 종료 시점의 실행 환경을 수집한다. 연결 중단이나 응답 모호 시 같은 파일의 `STATUS`로 기존 제출을 조회한다. `RETURN`은 원 잡 결과를 회수한다. 결과는 U 보고 tar, 전체 tar, SHA256SUMS, return.json과 감시 로그다.
- 다음 팔 판단은 B2-U의 원 잡 COMPLETED 0:0, runner rc 0, 정확한 파일명 234개, 원 잡 반환 해시, W9 LIVE_TERMINAL_MATCH를 함께 대조한 뒤 1저자가 한다. 회수 전용으로만 찍힌 RECOVERY_ONLY는 종료 직후 측정의 결측으로 표시한다.

## 결속 근거

원 덱 계획은 `docs/reviews/mixer_first8_launch_preparation_20261106/`, 공통 제출·회수 규약은 `docs/reviews/mixer_b1_pair_20261120/README.md`, 직전 개발 판독은 `docs/reviews/mixer_b1_pair_return_20261122/README.md`와 `docs/reviews/mixer_b1_pair_return_20261122/readback.json`에 있다.

| 신원 | SHA256 |
|---|---|
| B 배포 매니페스트 | `088460cc6a71db4fcc0b6fd326fb89ae629767a2ded45846952640ca44ac0ee0` |
| B2-U 덱 | `b37974e5c0674947912e932c55517e9e84243293f29257183f8f70cc032f2fd7` |
| B2-U 메타데이터 | `7e7b3f13354aaf312d780f8b96094a432cc64fadd20c335b815ab871ff2602ec` |
| B1-U 반환 포인터 | `b055909e3ee4179245fc82dfaa94fd4bbe964e0f0175c3ccca10c058cd625591` |
| B1-C 반환 포인터 | `ccedefc61c1505ae2c36bb14e7f259ccca4c377eda5f0e0a4641f8418bff4c73` |
| B1 U/C 판독 pair.json | `6fb926e4a0fbe2b536acccb90cf10e440da2d064611cf0b0bc913a341d8f0f1a` |

1저자 GO 요청: B2-U 개발 1팔은 11-22 승인받았다. 실행 인자는 `GO_B2_U_ONCE`이다. B2-C는 U 반환 대조 뒤 1저자 결정 항목이다.
