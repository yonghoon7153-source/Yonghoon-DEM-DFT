# A8 실행본 확정안 — 독립 정적 검토

2026-09-24. **판정: 아래 조건을 포함한 제한 오프라인 배치 준비는 진행 권고. 현재 배치 승인을 대신하지 않으며 B 실행은 NO-GO/미승인이다.**

새 폴더로 분리하고 Java 두 경로·target·계약을 함께 고정하는 방향은 타당하다. 기존 A8 N6/N7 수용은 유지한다. 같은 389개 시험이나 COMSOL 정책 진단을 다시 요구할 이유는 이번 자료에서 찾지 못했다.

다만 새 단계의 완료 판정과 TTY 사전조건은 그대로 복사한 코드만으로 모두 집행되지 않는다. 아래 C1/C2를 명시하고 C3의 봉인 순서를 지켜야 한다. 이는 새 실행본의 native 실패를 재현했다는 보고가 아니라, 계획과 기존 집행 코드의 정적 대조 결과다. 새 배치 코드가 아직 없으므로 구현 통과로 판정하지 않는다.

## 1. 수신 확인

| 항목 | 직접 확인 |
|---|---|
| ZIP | COMSOL63_A8_EXECUTION_PLAN_20260924.zip |
| 크기 | 54,175 bytes |
| SHA-256 | `696de7adf371d2d3a02bafee2a9d942765b3cead7198f3fd679ca357445e4783` |
| manifest | 2,048 bytes / `3de5aab84441441e2c919e853bad82a35e99f3d23c4012508d0d15fe81edaf96` |
| 구성 | 11 payload + manifest = 12 entries |
| 검사 | 정확 집합·개별 크기/SHA·CRC·중복/정규화/대소문자 충돌·경로/유형 모두 통과 |

이번 메시지에는 생성 ZIP의 사전 raw SHA가 따로 없었다. 위 값은 수신 파일의 직접 측정이다. 내부 manifest 통과만으로 별도 생성본과 raw ZIP 동일성까지 주장하지 않는다.

A8 코드 166개에 대한 보내는 측 식별은 이전에 수신한 실제 166개 파일과 모두 일치했다. 불변 복사 목록 11개의 크기/SHA도 직접 대조했다. 네 phase의 예정 argv/cwd는 새 RUN에서 독립적으로 구성한 값과 일치했다. 검토자는 받은 Python/Java를 import하거나 실행하지 않았다.

선택 224개 before/after 기록은 경로 중복 없이 내부적으로 모두 일치한다. 그러나 원격 PC의 현재 224개를 직접 검증한 것은 아니다. 현재 prefs 원문·MPH·실행파일의 현지 바이트는 이 작은 ZIP에 없으며, 보내는 측 관측과 이전 자료의 비교 범위를 구분한다.

## 2. 수용 가능한 설계

### 경로와 불변 코드

- 새 source `api_recovery_B_A8R1`, run `saved_solution_A8R1_b006`, RUN `runtime/b006`은 서로 일관된다.
- 승인 파일은 source/approvals에 있고 RUN 밖이다. 내부 batch_authorized.json과 permission_token.txt는 RUN 안에 별도로 배치된다.
- 기존 Java 16행의 RUN/OUT만 바꾸고 역치환 전체 바이트를 비교하는 방안은 수치 본문 불변 확인에 적합하다.
- A8 path_binding.py의 독립 target SHA와 도출 규칙을 재사용하며, 예시 argv 두 벌의 상호 일치만으로 판정하지 않는다.

### 준비 플래그와 실행 승인

기존 path_binding.py:81은 approved=false와 B_path_ready=false를 요구한다. launcher.py:130–141은 별도 승인 파일의 approved=true·manifest SHA·run/예산·필수 명시 승인을 검사하고, 계약 B_path_ready=true도 요구한다.

따라서 새 최종 계약의 B_path_ready=true와 사용자 실행 승인 부재를 분리하는 방안 자체는 우회가 아니다. 단, contract.approved=false 또는 문서 usable=false가 launcher의 독립 실행 차단 장치인 것처럼 설명하면 안 된다. 실제 실행권은 별도 B 승인 파일과 검증 경로에 있다. D11에는 승인 없는 상태/false 승인/다른 run·manifest/정상 fixture 승인의 경계를 포함해 그 연결을 확인할 것을 권고한다. 실제 승인은 만들지 않는다.

### prefs 기준 변경

새 기준 `064d1900…`을 새 계약에만 넣고 실제 prefs나 옛 계약을 쓰지 않는 안은 구분이 명확하다. default_prefs_source.identity와 protected_files의 해당 항목을 함께 갱신해야 한다. 16개 security 값은 옛 계약과 정확히 같아야 하며 현지 재측정이 다르면 중지한다. 보안값 외 전체 prefs의 변화 원인을 확인했다는 의미는 아니다.

## 3. C1 — 새 단계의 16개 결과 집합을 별도로 집행할 것

근거: EXECUTION_PLAN_KO.md:37–38의 단계명은 `deployment_binding`이다. 기존 completion_contract.py:61–68은 report.status를 검사하지만 **시험 개수·ID·각 결과·실패 수 검사는 stage == synthetic일 때만** 적용하며, 그때의 개수는 389로 고정되어 있다.

따라서 같은 소비 함수를 호출한다는 사실만으로 새 단계의 D01–D16이 모두 실행됐다는 검증이 생기지 않는다. 새 driver가 그 역할을 맡아야 한다. 이는 N5/N6 시간·외부 종료 검사에 대한 반박이 아니라 새 단계로 연결할 때의 책임 분리다.

배치 구현 조건:

1. 봉인된 D01–D16의 정확 집합을 검사한다. 단순 count=16만 보지 말고 누락·중복·알 수 없는 ID·skip/미실행·일반 오류를 거부한다.
2. 각 ID의 계획된 양성 대조와 거부 이유/도달 단계가 충족돼야 한다. 기대 음성의 실제 거부와 시험 코드 자체 오류를 구분한다.
3. 이 집합 검사 결과 AND 기존 completion/report/external 소비 결과 AND 마지막 전달 경계가 모두 통과해야 준비 완료다.
4. D12 안에 빈 집합·하나 누락·중복 ID·실패 결과를 담은 해시 일관 자료와 온전 대조를 넣는다. 기존 completion_contract.py를 수정하거나 전체389 suite를 재실행할 필요는 없다.

이번에 그러한 자료를 실제 consumer에 주입하지 않았다. 위 판단은 해당 조건문의 정적 확인이며 새 driver의 실제 결함을 관측했다는 뜻은 아니다.

## 4. C2 — TTY는 아직 ‘Desktop 이전 코드 gate’가 아니다

근거: EXECUTION_PLAN_KO.md:91은 TTY 미제공이면 COMSOL 시작 전에 멈춘다고 한다. 그러나 기존 launcher.py:305에서 apply Desktop phase를 실행한 다음, 306행의 observe를 통해 timed_attest에 들어간다. `sys.stdin.isatty()` 거부는 118행에 있다. main의 승인 확인/execute 진입 전에 이 검사는 없다.

정적 호출 순서: main → verify_approval → Runner.execute → phase(apply) → observe → timed_attest → isatty.

따라서 다른 사전조건이 통과한 비TTY 실행에서는 **이 TTY 검사만으로 첫 Desktop 시작을 막을 수 없다.** 실제 비TTY 실행이나 Desktop 호출로 재현하지는 않았다.

다음 오프라인 배치에서 launcher 불변 조건을 깨며 고치라고 요구하지 않는다. 계획/B 문안을 다음처럼 명확히 해야 한다.

- 같은 실제 호출 경로에서 사용할 Windows TTY의 사전 확인은 아직 미완인 B 착수 전 운영 조건이다. 앱 터미널이 보인다는 사실이나 현재 검토 셸의 TTY 결과로 대신하지 않는다.
- launcher가 그 조건을 이미 선행 집행한다고 표현하지 않는다. 현지 사용자가 직접 입력할 수 있는 경로·확인 주체·증거를 B 승인 전에 확정해야 한다.
- 선행 코드 gate가 필요하면 그 최소 변경은 별도 변경 승인 대상이다. 이번 세 개 배치 도구에 새 native 실행 제어기를 끼워 넣거나 임의 transport로 우회하지 않는다.

TTY 확인이 미완이어도 경로 결속만의 B_path_ready는 별개로 표현할 수 있다. 그러나 B 실제 실행 가능/사용 가능으로 승격할 수는 없다.

## 5. C3 — 실제 raw 계약을 먼저 고정하고 view를 파생할 것

계획의 ‘한 필드만 false인 view’ 제한은 유지하되 구현 순서를 고정한다.

1. 별도 배치 승인 아래 최종 후보 raw 계약을 생성한다. contract.approved=false, B_path_ready=true는 준비 후보일 뿐 실제 승인 파일은 없다.
2. 이 raw 계약을 source seal에 넣는다. 그 바이트를 읽어 얻은 객체의 복사본에서 B_path_ready 한 필드만 false로 바꿔 검증한다. 삭제·기본값 채움·다른 불일치 정규화는 금지한다.
3. view 역변환의 구조/타입 비교와 원래 raw SHA를 모두 확인한다. view를 다시 JSON으로 직렬화한 해시가 원래 raw 바이트 해시라고 가정하지 않는다.
4. D10과 D11이 성공적으로 본 raw 계약·코드·target이 최종 CODE_MANIFEST에도 동일해야 한다. 시험 뒤 플래그나 계약을 다시 고치고 같은 시험이 그 바이트를 검증했다고 표현하지 않는다.
5. 실제 사용자 승인 파일은 만들지 않는다. 실패 자료에 후보 플래그가 있어도 준비 완료가 아니며, 완료/외부 반환 누락이면 비활성·미완 보고를 유지한다.

## 6. 다음 승인 범위와 제출물

위 C1/C3는 제안한 새 deployment_verify.py / deployment_package.py / test_deployment_binding.py 및 기존 D10–D12의 상세 조건으로 포함할 수 있다. ID는 16개로 유지할 수 있지만 각 하위 사례의 실제 실행 수도 공개하고, 이를 총 16개 assertion인 것처럼 표현하지 않는다. 최대2회/첫 완전 통과 후 중지/정적·구현·전달 및 전체 예산 조건을 유지한다. 추가 native 시험이나 기존389 재실행을 승인하지 않는다.

원래 11개 불변 파일·두 Java literal·TARGET_SHA 상수·새 계약/target/binding/봉인과 문서만 허용한다. 허용 범위 밖 수정이 필요하면 중지한다. b003 pending/원복·기존 failed·원본/MPH/ZIP/영수증은 보존한다.

배치 결과에서는 최소 diff, 정확 ID/하위 사례 결과, raw/view 대응, 봉인 시점, 최종 manifest와 시험된 코드의 동일성, 완료/외부 반환, 원본 보존을 확인한 뒤에만 별도 B 승인을 검토한다. native API/정책/실제 수치/정리/원복은 아직 미시험이다.

**현재 결론: 제한 배치 준비 계획 조건부 수용. 배치 실행은 사용자 별도 승인 필요. B/COMSOL 실행·장시간 운전은 계속 보류.**

이번 작업: 검토자 데이터 검증기 1회, 받은 코드 정적 읽기/AST 읽기만 수행. 대상 module import·suite/probe/F·배치·COMSOL/JVM·prefs/registry/ACL 변경은 0회. 상세 데이터는 VERIFICATION.json. 처음 광역 파일 목록에서 관계없는 과거 scratch의 접근 거부가 있었으며 우회하지 않고 관련 명시 경로만 사용했다.
