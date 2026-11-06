# 실제 원 덱·include·재개 사슬 — 정적 신원 계획

현재 상태: **NOT_ESTABLISHED**. 이번 작업은 저장소 소스와 기존 정적 검토 문서만 읽었다. 실제 호스트/원 덱/include/체크포인트/로그에 접근하지 않았다. 파일 생성기 규약, 템플릿 경로 문헌, 과거 reader 성공은 실제 이번 코호트의 유효 입력 신원을 대신하지 않는다.

## 확인된 저장소 규약과 출처

| 출처 | 정적으로 읽은 범위 | 한계 |
|---|---|---|
| `scripts/lhs_ext_materialize.py` 8–44행 | 두 실제 호스트 템플릿의 경로·type/질량분율 규약 | 현재 원본 바이트·현장 존재 미확인 |
| 같은 파일 87–111행 | apply_ins_scale은 삽입 높이를 바꿈 | N·고체량·두께가 함께 변할 수 있음. 실제 실현 N 아님 |
| `scripts/press_units.py` 33–39행 | 필드별 목표압 변환 계수 | 실제 판힘 출력의 단위/스케일을 자동 인증하지 않음 |
| `scripts/lhs_pressure_record.py` 3–25행 | 목표 도달 로그 판정과 뒤 PHASE 4 구분 | 실제 PHASE 4 완료/평형/종점 압력 근거 아님 |
| 수용 N 초안 source_inventory.json | 한정된 원 덱 파일명/세 압축본 멤버 목록 검색 기록 | 이번 전 저장소 재검색·호스트 부재 증명이 아님 |

자료 요청 대상 경로(문헌 기록, **현재 존재 확인/복사 지시 아님**):

- ibb 3type 템플릿 `/home/yonghoon/dem_test/lhs/lhs00_000/input_lhs00_000.liggghts`
- ibb 2type 템플릿 `/home/yonghoon/dem_test/lhs/lhs00_110/input_lhs00_110.liggghts`
- WSL 2type 대안 `/home/yonghoon71/lhs_local/lhs00_110/input_lhs00_110.liggghts`

두 템플릿만으로 후보 214개의 실제 실행 덱을 인증하지 않는다. 각 후보의 **실제 실행 시점** 원 덱·의존 파일/재개 입력·명령 인자 매핑이 필요하다. 현재 파일은 실행 뒤 수정됐을 수도 있으므로 실행 시 봉인 해시/receipt와 별도 대조해야 한다. 없다면 현재 정적 바이트까지만 알고 실제 실행 신원은 미확정이다. synthetic `lhs00_777`이나 타 트랙 D0.7 입력으로 채우지 않는다.

## 값 열람 전에 고정할 명부

1. **진입 입력**: case/producer/run ID, 실제 절대 경로·별칭의 정규화, 파일 종류·bytes·SHA256, 실행 때 봉인된 해시와 현재 해시 구분. 실행 CLI의 -var/-in, 작업 경로, 실제로 참조하는 환경 변수의 이름/비밀이 아닌 입력 값·출처. 인증정보를 명부에 넣지 않는다.
2. **의존 폐쇄**: include/jump/read_data/mesh/property 입력·관련 변수 파일의 경로/bytes/SHA256, 순서와 부모→자식 edge, 조건 분기·반복·변수 치환. root 덱 hash만을 effective-deck hash라 하지 않는다. 정적으로 해결할 수 없는 데이터 의존 분기·누락 include·변수는 UNRESOLVED다. 덱을 실행/eval하거나 매크로를 임의 평가해 해결하지 않는다. 고정 바인딩과 순서 있는 파일/edge 명부의 직렬화 규칙을 정한 뒤에만 결속 해시를 부여한다.
3. **물리/프로토콜 키**: units·축소법·dt, type/재료/PSD와 분율 의미, fix ID/law/group/계수와 type별 scale, 동적 membership 규칙, 판면적·속도와 fix/unfix, 압축 종료 알고리즘, PHASE 4 예정 구간, timestep reset, 출력 필드/정밀도/간격. 실제 c_v/속도/면적/예정 길이는 현재 모두 null. 50kg의 수치를 복사하지 않는다.
4. **재개 DAG**: 각 체크포인트의 bytes/SHA256·producer 실행/입력·parent/child, 기록 step·PHASE·누적 시간, periodic restart 또는 command write_restart 종류, 소비자 입력·변경 fix/계수·binary/NP/MPI 신원 근거. 하나의 문자열 경로가 아니라 공유 조상/분기/사본을 보존한다. checkpoint hash는 상태 동일 바이트만, 소스 hash는 코드 동일 바이트만 증명한다. 재개 물리 연속성·접촉 이력 동일성·G2c/P1 인증은 주장하지 않는다.
5. **출력 결속**: 값 없이 수집 가능한 실행/segment 식별자·예정 출력 파일/프레임 규약·수확 설정과 원본 봉인 근거를 먼저 확보한다. 실제 완료/step/멤버십/압력은 이후 별도 승인된 원자료 확인으로 검증한다. 실제 로그 통째 열람이나 압력 출력 줄 읽기를 정적 입력 확인에 끼워 넣지 않는다.

후속의 실제 파일 반입/호스트 읽기는 1저자가 범위·담당·출처를 정한다. 이번 문서는 실행 명령·접속·복사·제출을 제공하거나 수행하지 않는다. **미확보는 규칙 미작성과 구분하지만, 완성된 사전등록/실행 자격으로 주장하지 않는다.**
