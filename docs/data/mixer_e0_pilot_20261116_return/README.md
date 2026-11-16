# E0 366423 수령 · 개발 자료 (2026-11-16 실행 / 11-17 KST 정리)

| 트랙 | 계산 | 상태 | 숫자 | 다음 |
|---|---|---|---|---|
| 믹서 E0 | 승인된 한 팔 366423 | 실행 끝 · 전체 회수 확인 · 관측 OK | NP20 · 03:53:26 · 100000 입자 · 1121 프레임 | 종료 직후 신원 영수증 부재 처분 + 1저자 자격 수용 판단 |
| 다음 회전 | PRECAL_N0 | 미실행 · 저장 정책 검토 | 기존 32976 step · 234 프레임 · 마지막 bin 100 프레임 | 기존 다음 wave 조건과 승인 |

## 1. 수령 신원과 범위

바탕 = `2da71fe5abbaa856beb87c39c2a49424e4c87bc7`. 새 Claude 기준은 `claude/stoic-knuth-NObVQ`가 이 커밋으로 fast-forward된 뒤의 본 세션이다. 대피 가지 `claude/sdcp-dem-manuscript-si-pqwtv8`는 여기서 정지한다. 현재 기록은 **개발 자료**이며 새 DEM 실행·제출·취소·재봉인 0이다.

| 수령물 | bytes | SHA256 |
|---|---:|---|
| e0_report.tar.gz | 210599 | 64c3de3752c49d41d83fa47ac58723a51f561736b4bcfe355f5bc1d79f722e20 |
| e0_full_result.tar.gz | 11152406005 | c9f4fb005a4a937cdefa17493cb9fca3729fb5410a4a7baaa22fe111cbe77a91 |
| 첫 미완료 report | 143346 | 711b080c22fdb2ff1d1f00cecea75fa86310147f7c5fdbe35b39536d0dd2fe89 |

실행 컨트롤러 핀 = `997aabe1b5a702e2f389007e3923018d778ce857`, 소스 SHA256 `56f2d5ea366e55c987417bc7fea0f777598fb807f21de1887ae4aeea8af2a943`. 승인 B = `8231f395cda98fed8dbbf5422ccda003b11a8da9`, A/B 반환 SHA256 `6f7f407479af6282b9c8d4e83afa86645d4fda1506b29801be2165dcc2965737`.

원 압축본을 스트림으로 읽어 전체 SHA256·gzip CRC·경로·중복·링크를 확인했다. 전체 1445 멤버 중 정규 파일 1440개, 이 중 런 파일 1138/1138은 회수 목록의 길이·SHA256과 같다. 소스 283/283은 승인 B manifest와 같다. report 정규 파일 42개 중 full과 공통인 33개는 바이트 동일이다. 서로 중첩하는 수를 합산하지 않는다. full은 보고서 최종화 전 생성되므로 final controller JSON 등 report 전용 멤버의 부재는 누락으로 세지 않는다.

첫 미완료 report도 원 해시와 같고, recovery 기록이 보존했다고 적은 evidence 34개가 전부 그 바이트와 같다. 원 반환본·덤프·restart·제어 파일 변경 0. 리포에는 원 로그와 원 압축본을 넣지 않고 이 요약, 상대 경로 목록, 파생 검산만 넣었다. 재현의 자세한 범위는 `docs/data/mixer_e0_pilot_20261116_return/receipt.json`과 `docs/data/mixer_e0_pilot_20261116_return/case_inventory.json`이다.

## 2. 등록 대조

기준 = `docs/reviews/mixer_e0_pilot_registration_20261113/registration_candidate.md` §7-3 C1–C7, §9 사후 S5, §12 W9. 기준을 결과에 맞추어 옮기지 않았다.

| 항목 | 상태 | 확인과 한정 |
|---|---|---|
| C1 | 1 = 기록 일치 | sacct COMPLETED · 0:0 · 20 CPU · 1 node |
| C2 | 1 | 제출·start·end·scheduler job 366423, claim/start/approval SHA 일치, runner rc0 |
| C3 | 1 | post 1121개, step 1000–1121000 / 1000; 모든 장의 머리 100000, 개행 100009, 마지막 행 12칸, 끝 개행. restart a.bin/b.bin/settled.bin 3개 모두 양수 |
| C4 | 1 | post+restart 25909227745 B < 29266573952 B; 항목 1140 < 1146 |
| C5 | 1 = 기록 범위 | 실행 출력 수정 시각 창 일치, 놓인 7파일의 제출 시각 조건 일치, 자산 5개 승인 B와 동일, claim/receipt 첫 report와 동일, 회수 watch의 크기 합 일치. 기록되지 않은 행위의 부재 인증은 아님 |
| C6 | 1 = 기록 범위 | loop ranks [20,20,20,20]; 배너 version/build/git는 기준표 §0-A와 일치; 관측기와 의존 9개 source seal 일치 |
| C7 | 1 | t0 x/y/z 유효숫자 7자리 이상 존재. 정확한 분포는 receipt의 C7 칸 |
| 사후 S5 | 1 = 진행 불명 해소 | 첫 프레임 +6.343 s, 프레임 수정 시각 최대 간격 20 s; 1800 s 초과 0. §9에 따라 감시 공백의 진행 불명은 회수 목록으로 풀림 |
| W9 | 2 = 부분 | 발사 전과 회수 시점의 binary/mpirun+30 libraries, 7꾸러미/1011파일 모두 일치. **종료 직후** 영수증은 없음. 회수 신원 확인은 종료 +9362.118 s이며 이를 즉시 T9로 소급하지 않음 |
| 자격 수용 / N0 GO | 0 = 없음 | 이 수령 기록은 1저자 수용이나 후속 발사를 대신하지 않음 |

첫 감시는 08:01:36Z–08:31:38Z 네 줄 뒤 Broken pipe로 끊겼다. 종료는 11:55:02.782Z, 회수 watch는 14:30:47Z 한 줄이다. 회수 폴더 이름 `runtime_T9`와 `runtime_post_matches=true`는 코드가 붙인 이름·필드이고, 실제 수집 시각 14:31:04.900Z를 우선한다. 감시 실패를 계산 실패로 바꾸지도, 끝까지 감시했다고 바꾸지도 않는다. scheduler 종료 뒤의 squeue ABSENT는 sacct 완료와 별개로 확인했다.

## 3. 관측과 물리 대조 한 줄

승인 B의 고정 관측기 `bb2f322987fa6eb2e49159e6cc1447f5264036fc9cd84b3f4d59a60ffbc63710`와 의존 8개를 그대로 사용했다. 전체 파일 무결성 검사 후, E0에 필요한 t0와 덱·메타·로그의 정확한 사본으로 관측했다. E0 관측은 t0 한 장이며 전체 1121장의 물리 관측은 아니다. Windows Python 3.12.14 / NumPy 2.5.5 / SciPy 1.17.1. 최초 두 준비 시도는 NumPy의 OS 조회(`cmd /c ver`)를 감사 hook이 막아 bootstrap TECH였고, 데이터 분석 전 실패다. 과학 라이브러리 초기화 뒤 hook을 건 최종 관측은 OK, 외부 프로세스·네트워크 시도 0. 고정 관측기·물리 계산 코드는 고치지 않았다.

- 원자 합 100000, AM_P/AM_S/SE = 136/693/99171 (계획 143/699/99158과 상별 차이는 그대로 기록).
- t0 = 1121000, 최종 계산 = 1121213. t0는 끝보다 213 step, 0.0000505449 s 앞의 등록 격자점이다.
- SE–SE 접촉쌍 168504, AM_P–SE 17449, AM_S–SE 19878; SE 군집 분율 0.9961581511, AM 하나 이상에 닿은 SE 분율 0.3431245021. 원시 분산과 기존 해상도 범위는 receipt에 보존했다. E0의 M과 회전 bin은 NOT_APPLICABLE이다.
- **물리·이전 기록 대조:** 3.89 h는 등록 E1의 3.4–4.9 h 안이다. 점착 계수 0에서도 정착한 입자의 순간 기하 접촉은 남으므로, 접촉 군집·접촉 부착 분율이 0이 아닌 것을 점착 발생이나 영구 응집으로 해석하지 않는다.

## 4. squeue 고침 · 다음

수집 때 1저자가 쓴 대리 파일은 특정 job/query/error에만 적용된 회수 수단이며 고정 소스가 교체된 것이 아니다. native 고침은 별도 `codex/mixer-squeue-purged-1116`의 `dd2c50741f43830ec83b232d0ec51b990d5beaab` → `f1a673fab45b50bedb71a1c8203d9c8ae75f6c97`. rc1+빈 stdout+등록된 정확한 진단일 때만 ABSENT, 종료는 여전히 sacct로 확인한다. 새 12/12, 기존 19 pass/1 skip는 앞 고침 검증 수이며 이번 수령에서 다시 실행하지 않았다. 기존 366423의 실행 파일·수집 TXT·author GO·해시는 그대로다.

다음 준비: 세션과 분리된 원격 감시, 종료 즉시 신원 영수증, 다음 회전의 시간/자원 계획 및 기존 W1–W10 처분. 원장·공유 기록은 Claude가 처리한다. 개발 계산 허용과 논문 수치·봉인 직전 검토를 구분하며 다음 wave를 자동으로 열지 않는다.
