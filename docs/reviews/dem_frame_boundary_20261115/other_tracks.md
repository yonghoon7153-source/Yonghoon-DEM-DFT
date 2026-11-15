# 믹서·LHS — 다음 준비 경계

## 1. 믹서 증서와 기록의 순서

고정 후보 087ba5eb9a8d1d2c363d265bacfe064116361c80의 `scripts/mixer_smoke_blind.py` 네 함수만 읽었다. SHA·AST 위치는 `mixer_publication_map.json`. 소스 실행·연구 입력 읽기·증서 작성·예약 변경0이다.

| 선택 경로 | 순서 | 준비에서 구분할 것 |
|---|---|---|
| run_blind (143–208) | 원기록 O_EXCL 생성 → 직렬화·권한·해시 → 투영/누수 검사 → 증서 .tmp 쓰기 → replace → journal append·chmod → 반환 | 거부와 I/O 예외, 증서가 이미 바뀐 뒤 journal 실패를 각각 기록 |
| run_contract_cert (313–373) | reader/contact 처리 → E0면 completion → _vault → 투영/누수 검사 → 거부면 journal+rc2 / 정상면 증서 replace → journal → rc0 | E0와 회전 팔의 reader 경로를 동일하다고 가정하지 않음 |
| _vault (211–230) | mkdir/chmod → 시각 이름 → O_EXCL 충돌 재시도 → json.dump·newline → chmod·hash | O_EXCL은 기존 이름 덮어쓰기를 막는 단계. 이후 직렬화·권한·해시·내구성 성공 전체를 뜻하지 않음 |
| _blind_log (233–237) | append 열기 → 한 줄 쓰기 → chmod | 증서 replace와 하나의 원자적 묶음이라는 근거는 없음 |

이 표는 소스 순서의 관찰이며 재현된 신규 결함 판정이 아니다. 실제 POSIX 권한·파일시스템 원자성/내구성·다른 writer·공유 저장소·namespace·시계는 별도 자격이다. 이번 정적 검산에서 데이터를 생성하거나 fsync·프로세스 충돌 시험을 하지 않았다.

다음 SELF-170 사본 시험에 붙일 **미실행 계획**:

| ID | 주입 경계 | 기록할 최소 관찰 |
|---|---|---|
| MP01 | _vault에서 첫 이름 FileExistsError, 다음 이름 성공 / 전부 충돌 | 원본 해시·시도한 이름 수·생성 여부·최종 rc/예외. 전부 충돌을 성공으로 세지 않음 |
| MP02 | O_EXCL 성공 뒤 직렬화 또는 chmod/hash 실패 | 남은 원기록의 유무·부분 상태, 증서/journal의 전후 집합. 단순 파일 존재를 완료로 세지 않음 |
| MP03 | 증서 .tmp 쓰기 실패 / replace 실패 | 옛 증서·임시 파일·원기록의 상태를 따로 기록. 모든 실패가 같은 잔존 상태라고 단정하지 않음 |
| MP04 | replace 성공 뒤 journal append 또는 chmod 실패 | 새 증서와 실패 반환이 함께 있을 수 있음을 관찰. journal이 있다고만 해서 append·권한이 모두 완료됐다고 판단하지 않음 |
| MP05 | wrapper 원기록·증서·journal 정상 완료 | 내용·해시·권한과 정상 반환을 해당 시도에 결속. SELF-170 시계/자식 경로 기록은 기존 네 칸과 구분 |

고정 clock overlay는 wrapper 안 datetime 바인딩만 바꾼다. 시간 고정 통과를 파일 I/O·동시성 자격으로 전용하지 않는다. MP01–05는 기존 SELF-170 네 칸을 대체하거나 새 현장 명령을 승인하지 않는다. 운영 재봉인·E0·first8·host/wave·실행 GO는 그대로 HOLD.

## 2. LHS O1

실제 O1 출력은 아직 수령하지 않았다. 기존11키와 별도 실제 rc, 10개 수령 사례를 그대로 사용한다. `docs/reviews/nonrint_offline_casebooks_20261114/lhs_o1_receipt_plan.md`와 `docs/reviews/dem_priority_preparation_20261114/lhs_o1_intake_examples.md`의 다음 조건을 유지한다.

- 현재 덱의 별칭·종류·크기·SHA256·관측 시각만 O1 범위다. 현재 hash를 과거 실행 신원으로 대체하지 않는다.
- 명령 출력과 별도 rc가 함께 있어야 수령 판단한다. 결손/부분/불일치에서 성공값을 채우거나 자동 재시도하지 않는다.
- A→B→A 변경 및 비원자적 읽기 한계를 보존한다. 성공 수령도 역사 실행·원 로그·값 GO가 아니다.
- 명령 SHA256 `2026d61bb920599ca95870b62b8aee9ed3345f288da21ed4ff090a0064e0b8a3`와 양식은 보존했다. 새 parser·명령·빈 영수증을 만들지 않았다.

상태는 `execution_identity_status=NOT_ESTABLISHED`, 값 열람 GO 없음, 전체 HOLD. 새 비결과 자료가 없는 동안 Q2–Q4를 다시 묻거나 명부/정본/쌍을 확정하지 않는다.
