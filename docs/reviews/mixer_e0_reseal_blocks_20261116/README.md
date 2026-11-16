# E0 재봉인 A/B — 1저자 WSL 실행용 준비

1저자 11-16: 재봉인 별도 승인을 이번 지시로 갈음. 실행은 1저자이며, pqwtv8 반입은 시도 4 DONE 뒤다. 이번 구현은 새 복사본의 A/B 생성·검산 도구이며 발사·배포·예약 변경을 하지 않는다.

정본 순서 = `docs/reviews/mixer_e0_pilot_registration_20261113/registration_candidate.md` §7-6·§18 Q-C′. 원 덱·STL 생성 핀은 보존하고 관측기와 SELF-170의 현재 신원을 묶는다. 옛 등록 문서의 “별도 승인 대기”를 다시 묻지 않는다.

## 1. 도구와 블록

`scripts/mixer_e0_reseal_bundle.py --source <고정 소스 사본> --output <새 폴더> --mode linux-checks`.
실제 붙여넣기 TXT와 고정 핀 source tar는 리포 밖 전달물이다. TXT는 WSL Python 3·NumPy/SciPy·bash·timeout을 확인하고, tar 해시/목록 대조 → 새 폴더 → 도구 실행 → rc·RECEIPT·로그·B 묶음 회수까지 한다. 자동 설치·자동 재시도는 없다. CPU 1개, 예상 수분(현장 미측정), 전체 시간 상한 30분·각 검사 상한 600초. SSH·Slurm·MPI·DEM 엔진을 호출하지 않는다. first8 시험의 fake scheduler는 합성 호출이다.

| 차례 | 처리 | 성공 근거 |
|---|---|---|
| A | 86파일 IN 목록 중 관측기 현재 신원만 바꿈; 원본/수용 이력 칸은 보존. 새 snapshot·candidate·증거 폴더 | build·verify rc0, old rc1/8 subcase 실패/오류0, 준비14 rc0 |
| B | F8 메타8·40자산 목록·자산 SHA 목록·소스 봉인12를 같은 새 사본에 적용 | validate_case 8, 원 E0 메타 거부, 40자산/40해시, 덱8·STL24 보존 |
| SELF-170 | 현재 wrapper와 동봉 소스의 추가 신원 목록; canary·전체 blind selftest | 각각 rc0·로그 보존. 역사12 봉인에 새 의존을 조용히 끼워 넣지 않음 |
| Linux 회귀 | 관측기43 및 기존 제출10·경계14·job-start8·준비전용1 | 실제 실행 로그·rc 수령. 수를 합산하지 않음 |
| 회수 | 원 source package 재대조, B integrity 재대조 | RECEIPT.status=AB_READY_FOR_AUTHOR_REVIEW + rc0; 불완전/실패는 완료 아님 |

B의 `source_seal.json.source_pin`은 전달 소스 핀이다. static_asset_manifest의 원 `source_pin`은 덱·STL 출처 그대로, `metadata_generation_source_pin`은 IN 후보의 기존 생성기 신원이다. 현행 전체 소스 pin과 혼동하지 않는다. A 기록은 **재봉인 전 검증 기록**이며 B에 IN 검증기를 다시 돌려 통과시킨다고 주장하지 않는다.

`e0_runtime_tool_identity.json`은 SELF-170 등 동봉 도구의 추가 해시 목록이다. 기존 제출기는 역사12 파일만 검사하므로, 후속 pilot 블록은 이 추가 목록도 발사 전에 확인하도록 연결해야 한다. 이 도구의 B 폴더를 기존 배포 폴더에 자동 복사하지 않는다. 본 도구는 Git 커밋·push를 실행하지 않는다; A/B는 별도 디렉터리·영수증 단계이고 실제 반입은 Claude의 커밋으로 한다.

## 2. 작성 측 확인

- 새 복사/신원 회귀 8/8. 예상 밖 의존 변경·파일 변조·추가 파일·기존/겹친 출력·덱 변경·SELF-170 drift 거부, 원 생성 핀과 8메타·32원자산 보존 확인.
- Windows 새 복사본 assemble: A build/verify·old 음성·준비14, B validate8/원 E0 메타 음성, 자산40·소스12 확인. 원 소스 불변. 개발 중 사본을 썼으므로 최종 전달 핀의 Linux 결과로 세지 않는다.
- Linux 전체 blind·제출/작업 시작 모의는 1저자 블록에서 수행할 항목이다. 현장·연구 결과 0. 운영 반입·자동 발사 권한을 만들지 않는다.

기준 12 의존에 들어 있지 않은 SELF-170의 신원을 12의 일부인 것처럼 기록하지 않았다. 추가 목록과 source package 전체 해시는 전달/사본 결속이며, 라이브러리·동시 변경·실제 호스트 자격을 대신하지 않는다. E0 한 팔 이후 N0·B 팔은 자동 승인되지 않는다.
