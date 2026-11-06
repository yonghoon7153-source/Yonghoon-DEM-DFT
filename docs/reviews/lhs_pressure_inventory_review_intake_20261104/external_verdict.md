# LHS 압력 로그 재고 명령 — 독립 반박 재검토 (2026-11-04)

**판정: 준비·검토 범위의 핵심 계약 수용. 새 P1/P2 반례 없음. P3 보강 2건. 전체 게이트 HOLD 유지.**

이 판정은 실제 ibb/WSL 재고 실행 허가, 압력 적격성, A/C 선택, 복사·전송, 압력 기록, 등록 변경, 단계 A 또는 배포 GO가 아니다. 원격 연구 호스트를 열거나 연구 로그를 읽지 않았다. 소스·원장·등록·Git 상태를 변경하지 않았다. 독립 합성 탐침과 리뷰 산출물만 별도 로컬 폴더에 만들었다.

## 1. 핀·바이트와 증거 신원

| 항목 | 독립 대조 |
|---|---|
| 가지 / 핀 | `codex/lhs-v13-1104` / `c8a55c8ae1021ec80634ee8c6533deeebc67ce61` |
| 수령 ZIP | `codex_lhs_pressure_inventory_20261104_c8a55c8ae102.zip`, 203,871 B |
| ZIP SHA256 | `f3fa59d7c244dccbf09cbea95c4cfac85466d1c420c76027dc06b8e207de06aa` — 사용자 제공값과 같음 |
| PIN / SNAPSHOT_MANIFEST | 핀 같음. 17개 파일의 크기·SHA256 전부 같음 |
| 원격 핀 대조 | 핀 지정 GitHub 목록의 17개 blob SHA1·크기와 ZIP에서 직접 계산한 Git blob 신원 전부 같음 |
| 포장 매니페스트 | PACKAGE_SHA256SUMS 68개 전부 같음. 자기 자신을 제외한 파일 누락 없음 |
| ZIP 경로 | 상위 경로 탈출·절대 경로·중복 이름·symlink 항목 없음 |
| 명령 SHA256 | `c989194dd204622d87fcaa435ec5e95aac5eb82904be0afaa4e2ff57ff1e718a` |
| 비교한 B7 코드 SHA256 | `34eb74142884489505590501840ccc6423a014a508989c82f135020146283ad3` |

근거: 증거 묶음의 `intake.json`, `remote_blob_listing.json`, `verification.json`, `verify_received.py`.
원격은 현재 가지 끝 대신 위 전체 SHA로 조회했다. Git fetch/checkout은 하지 않았다.

`source_provenance.json`의 scratch 정본 README 해시(`1de84226…`)는 현 핀 README(`2e375eea…`)와 다르다. 첨부 `DELIVERY_VALIDATION/initial-attempt/lhs/inventory-integration-before/` 안의 이전 README 바이트가 그 scratch 해시와 정확히 일치한다. 이를 현 핀 바이트 불일치로 오인하지 않았다. 명령·시험 해시는 scratch 기록과 현 핀에서 동일하다.

아래 `I:L`은 핀의 `docs/reviews/lhs_pressure_inventory_20261104/pressure_inventory.sh:L`, `R:L`은 같은 폴더 `README.md:L`을 뜻한다.
[고정 명령 원문](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/c8a55c8ae1021ec80634ee8c6533deeebc67ce61/docs/reviews/lhs_pressure_inventory_20261104/pressure_inventory.sh),
[고정 요청서](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/c8a55c8ae1021ec80634ee8c6533deeebc67ce61/docs/reviews/lhs_pressure_inventory_20261104/review_request.md).

## 2. 실제로 수행한 독립 검증과 한계

| 수행 | 결과 | 증명 범위 |
|---|---|---|
| 고정 파일 검증 | 17/17 원격 blob, 68/68 포장 항목 | 받은 바이트와 핀의 일치 |
| B7 실제 함수 대조 | 7,179개 독립 생성 입력에서 `b7_matches == B7.parse_log(text)['n']` | 줄 분리·정규식·디코딩 조건에서의 계수 동등성 |
| 별도 계약 탐침 | 214 고정 ID, 신원 조건 7개, 추가 합성 조합 300개 | 순수 함수·조건식 |
| 오류 주입 | 22/22 | 핀에서 추출한 실제 함수에 OS/IO 결과를 명시적으로 주입하여 거부·집계 분기 확인 |
| 출력 실패 주입 | 이중 JSON 반례 재현 | LPI-01. 실제 터미널 장애 재현은 아님 |
| 비정상 긴 줄 | 처리 시간 증가·5초 탐침 제한 초과 | LPI-02. 실제 로그에서 발생했다는 뜻 아님 |

환경은 Windows CPython 3.12.14다. 핀의 내장 Python 또는 함수·상수 AST를 변경 없이 추출했다. 파서 탐침은 메모리 스트림을, 경로 탐침은 명시적 OS/IO 대역을 사용했다. 계약 탐침은 Windows에 없는 pwd import를 대역으로 제공했다. 이는 **실제 POSIX 권한·O_NOFOLLOW·Lustre 동작을 인증한 시험이 아니다.**

네이티브 Git shell의 합성 시험 시도는 shell 자체 초기화에서 접근 오류로 막혔다. 대상 shell 명령이 실행된 것으로 세지 않았다. WSL로 우회하지 않았다. 첨부 구현 측 Python 3.11/3.8의 20/20 기록은 받은 증거로만 보존했고, 이번 독립 실행 수에 합산하지 않았다. 전체 게이트도 재실행하지 않았다.

## 3. 질문별 판정

### Q1 — 고정 범위·신원·root 별칭·하위 symlink

**준비 로직 수용. 실제 호스트의 파일 존재와 경로 신원은 미검증.**

- `I:180–187`: ibb는 lhs00_000–099 100개 + lhsx_001–064 64개 + lhss_001–020 20개 = **184개**. WSL은 lhs00_100–129 **30개**. 두 집합 합계 **214개**, ID 중복 없음.
- `I:23–25`의 root 세 개와 받은 거부 보고의 대상 구성이 일치한다. 원래 실행기·코호트 파일까지 반입된 묶음은 아니므로, 역사적 실제 실행 자리까지 독립 인증하지 않는다.
- `I:244–266`: 실제 UID/eUID·계정·커널·호스트 정보를 읽고, CLI에서 임의 root나 가드 해제를 받지 않는다. ibb의 사용자·short hostname·Linux·비 Microsoft 조건, WSL의 사용자·Linux·Microsoft release 조건이 문서와 같다.
- WSL 조건은 같은 계정명과 커널 조건을 만족하는 다른 WSL도 통과한다. 이는 문서에 적힌 **환경 조건 검사**이며 특정 기계의 암호학적 신원 증명이 아니다.
- `I:72–95`: 원 요청 경로 자체 또는 정확한 `/lustre` 접두 경로만 허용한다. resolved root는 각 구성요소를 디렉터리 fd와 NOFOLLOW로 연다. root 아래 case/logs/최종 파일은 symlink를 거부한다 (`I:51–69,119–177`).

**문구 경계:** 별칭 검사는 최종 requested/resolved 경로 쌍을 검사한다. 별칭을 만든 symlink가 반드시 `/home/yonghoon` 한 곳에 놓였다는 검사는 아니다. README의 “root 별칭 허용 + root 아래 거부” 계약에는 맞는다. 이를 “home부터 root까지 모든 중간 symlink 금지”로 확대해서 쓰면 안 된다. 현재 계약으로는 새 결함으로 세지 않는다.

근거: `contract_review/probe_result.json`의 fixed_plan/identity, `paths_review/exact_ast_results.txt` 01–04·08–10·20.

### Q2 — B7 일치 줄 수만 세는가·재개 사건으로 합치지 않는가

**수용. 파서 정의를 바꾸는 반례 없음.**

`I:17`의 정규식 문자열과 flags가 B7 `scripts/lhs_pressure_record.py:55`와 같다. `I:98–116`은 네 개 정수만 누적하며 압력·목표 토큰을 float로 바꾸지 않는다. B7의 `splitlines()`와 UTF-8 replacement/universal-newline 읽기 조건을 맞춰 7,179개를 대조했다. CR/LF/CRLF, 나머지 Unicode 줄 구분자, 잘못된 UTF-8, NUL/BOM, 비숫자·NaN·inf, 구분자에 붙은 토큰, 명령 echo와 주석을 포함했다.

독립 합성 입력 결과:
- 문법에 맞는 비숫자/NaN 줄 두 개 → `b7_matches=2`.
- `read_restart` echo 한 줄과 `Reading restart file` 메시지 한 줄 → 각 **1**, 재개 사건 **2회**로 합산하지 않음.
- 두 필수 로그에 같은 문법 줄이 있어도 파일별로 센다. 같은 실행의 복제본인지 판정하지 않는다.

따라서 이 명령의 rc0은 B7 압력 기록의 OK가 아니다. 재개 흔적 0도 재개 부재의 증명이 아니다. 해당 시작 문자열로 기록된 줄을 못 찾았다는 뜻이다.

근거: `parser_review/probe_parser.py`, `parser_review/probe_results.json`.

### Q3 — 값 비출력·무쓰기·외부 실행 없음

**핵심 수용. “오류 상황에도 항상 JSON 하나”라는 전칭은 LPI-01로 수정 필요.**

`I:33–43,234–238,258–280`의 출력은 고정 식별자·상태·정수 및 고정 B7 해시다. 입력 줄·압력/목표 캡처·exception 문자열·임의 파일명·동적 계정/호스트/경로를 출력에 넣지 않는다. 오류에 비공개 표지를 심은 독립 탐침에서도 표지가 출력되지 않았다.

파일 open 세 자리(`I:57,84,129`)는 모두 읽기용이다. `I:133`도 읽기 모드다. 생성·truncate·append·rename·remove 호출이 없다. 내장 Python은 외부 프로세스를 실행하지 않고 shell은 그 Python만 시작한다. SSH/SCP/tar/Git·제출 호출도 없다. `-I -B`로 리포 import와 바이트코드 쓰기를 피하고, shell의 대형 heredoc도 쓰지 않는다. README가 이미 밝힌 OS atime 갱신은 “직접 파일 쓰기 없음”과 구별한다.

다만 이것을 모든 OS/NSS/파일시스템의 부수 효과까지 없는 인증으로 확대하지 않는다. POSIX 전체 명령의 syscall audit는 이번 환경에서 재실행하지 않았다.

### Q4 — 오류 거부·rc0의 뜻·놓친 반례

**문서에 정의된 정상 런타임의 거부 로직 수용. 실행 환경 전체 인증은 미검토.**

독립 오류 주입에서 다음을 확인했다.
- 필수 로그 누락·PermissionError·symlink·FIFO/디렉터리 → 고정 오류 상태.
- stat→open 사이 inode/type 교체, 읽는 중 변경, 읽은 뒤 이름 교체/소멸 → 거부, 해당 파일의 부분 계수 폐기.
- 선택 .out 디렉터리의 진짜 부재 → ABSENT/0. 권한 오류는 ABSENT로 바꾸지 않음.
- 필수 파일 실패 또는 최종 root 변경 → 최상위 rc2/NOT_ESTABLISHED.

원천: `I:119–177,190–238`. 실패한 파일의 계수는 버리지만 성공한 다른 파일의 계수와 counted_cases는 rc2 응답 안에 남을 수 있다. 이것은 성공 판정이 아니다. **최상위 상태와 프로세스 종료 코드를 함께 읽어야 한다.**

rc0에서 빈 파일·0개 일치·NaN 문법 줄·로컬 중복 파일을 허용하는 것은 이 재고 계약에 맞다. .out은 종류·개수만 확인하며 본문 읽기 가능성·판정 줄 존재를 확인하지 않는다. 이 명령만으로 lhss .out 두 개 중 하나를 선택할 수 없다.

이미 명시된 “전체 184/30개 원자적 스냅샷 아님, 각 파일 확인 종료 뒤 변경 미검출”은 새 결함으로 재등재하지 않는다. 읽기 크기 상한은 처리 시간 상한이 아니며, 이 추가 경계는 LPI-02에 기록한다.

## 4. 새 지적 — 준비 기능을 무너뜨리는 P1/P2와 구별

### LPI-01 · P3 — stdout 오류 뒤 두 번째 JSON을 출력하려 함

- 위치: `I:267–271`; 관련 문구 `R:12,35`.
- 반례: 첫 성공 JSON 본문 쓰기는 허용하고 이어지는 개행 쓰기만 OSError를 내는 합성 출력 객체를 사용했다. 실제 `main()`은 출력 오류를 계산 오류처럼 잡고 두 번째 JSON을 쓴다.
- 관측: 함수 반환값 **2**, `json.loads` 실패. 출력에는 `INVENTORY_COMPLETE/rc0` 객체 바로 뒤에 `NOT_ESTABLISHED/rc2/INVENTORY_ERROR` 객체가 붙었다. 계속 쓰기 불가능한 객체에서는 두 번째 print도 예외를 낸다.
- 무너지는 것: “어떤 오류에서도 JSON 하나를 내보낸다”는 출력 계약. **압력값 누출·실제 프로세스 rc0 오판·실제 호스트 장애를 보인 것은 아니다.** rc2와 전체 JSON을 검사하는 수신자는 거부한다. 이 건만으로 준비 기능을 HOLD로 돌릴 근거는 없다.
- 최소 처리: 계산/직렬화 예외와 출력 예외를 분리하고, 출력 시작 뒤 실패를 잡아 새 JSON을 재출력하지 않는다. 단일 JSON 보장은 stdout이 정상인 조건으로 한정한다. 읽는 쪽도 “프로세스 rc0 + 완전한 JSON 한 개 + 최상위 INVENTORY_COMPLETE/rc0”를 모두 요구한다. shell fallback과 flush 실패도 같은 출력 계약으로 검토한다. 원천 수정은 이번 리뷰에서 하지 않았다.
- 재현: `python -I -B contract_review/probe_contract.py`.
- 증거: `contract_review/probe_result.json`의 `stdout_failure_after_json_before_newline`, `persistent_stdout_failure_escapes_main`.

별도 정적 관찰: `I:279`는 해석기의 모든 rc2를 그대로 통과시킨다. 따라서 시작 자체가 rc2로 끝난 경우까지 RUNTIME_ERROR JSON으로 바꾼다는 README 문장은 코드보다 강하다. 지원 Python에서 그런 시작 실패를 실제 재현하지 않았으므로 독립된 신규 결함으로 세지 않는다. 문구를 정상 지원 런타임 조건으로 좁히면 충분하다.

### LPI-02 · P3 — 입력 길이 상한이 정규식 처리 시간의 상한은 아님

- 위치: `I:17,103–111`; 한정 대상 `R:33`.
- 합성 입력: `'Current Pressure: ' + 'xMPa(Target:' * n + 'X'`. 끝 괄호가 없고 길이는 허용 상한보다 작다.
- 실제 함수 측정: n=1,000, **12,019자 → 0.054679초**; n=3,000, **36,019자 → 0.500813초**. n=10,000, **120,019자**는 독립 탐침이 정한 **5초 제한**을 넘었다. 마지막 탐침의 자식 프로세스만 종료했다.
- 무너지는 것: 데이터 크기를 제한했으니 짧은 시간에 반드시 끝난다는 추가 추론. 코드·README는 명시적 시간 상한을 약속하지 않았고, B7 자체와 같은 정규식이므로 계수 불일치가 아니다. 실제 연구 로그에서 발생했다는 증거도 없다.
- 최소 처리: “읽기 크기 상한이며 시간 상한 아님”을 명시하고 반례를 보존한다. 추후 시간 제한이 요구될 때만 한계를 사전 고정한 오류 거부 또는 동등성이 검증된 계수 경로를 별도로 검토한다. 이번에 B7·압력 규칙을 바꿀 이유는 아니다.
- 재현: `python -I -B parser_review/probe_parser.py`. 이 탐침은 긴 입력을 자식 프로세스에서 5초로 제한한다.
- 증거: `parser_review/probe_results.json`의 `timing_synthetic_malformed`.

부수 경계: .out 디렉터리는 `os.listdir` 전체를 읽고 root/logs를 case마다 다시 검사한다 (`I:160,213`). 디렉터리 항목 수·전체 wall-clock·네트워크 파일시스템 대기 시간의 상한은 없다. 실제 대형 디렉터리나 정지를 관측하지 않았으므로 별도 고위험 지적으로 세지 않는다.

## 5. 기존 처리의 종결 가능 범위

| 기존 사항 | 이번 처분 | 닫히지 않는 것 |
|---|---|---|
| 명령·시험·핀 바이트 신원 | 대조 완료 | 실제 호스트에 놓일 파일의 신원 |
| 고정 184/30 계획, B7 일치 수, 재개 두 계수 분리 | 준비 로직 수용 | 실제 로그 재고·압력 도달·같은 실행 여부 |
| 잘못된 fd로 PermissionError 시험이 엉뚱한 자리에서 통과하던 문제 | 수정 방식 수용. `test_pressure_inventory.py:160–171`은 유효 fd를 먼저 만들고 해당 open 호출을 단언함. 독립 주입도 열기 거부 경로를 확인 | 원래 Linux 시험의 독립 실환경 재실행 |
| 성장 중인 스트림의 총 읽기 상한 | 코드와 독립 분기 검토상 수용. 파일/물리 줄/문자 합 상한 유지 | 시간 상한·Lustre 지연 상한 |
| Python 3.8 실행 증거 | 받은 최종 소스 해시와 연결됨. AST 호환도 대조 | 이번 창에서 실제 3.8/POSIX CLI를 돌렸다는 주장 |
| 최초 tests_before 실패 | **import 단계 0개 실행**이라는 기록을 유지 | 19개 개별 음성 대조가 구현 전 모두 실패했다는 주장 |
| 기존 압력 REFUSED 214건·로그 복제/재개 사슬·A/C | 열림/별도 | 본 명령 수용을 원인 종결로 쓰지 않음 |
| Q1 결과 기록, L214P-02/03, Rint E13d·믹서 게이트 실패, 배포 항목 | 미검토·기존 상태 유지 | 원장 CLOSED, 통합/실행/배포 GO |

이번 요청에는 이전 독립 압력 재고 finding ID별 종결표가 없다. 위 “수용”은 검토 대상 구현 경계에 대한 판단이다. 임의의 기존 ID를 새로 만들어 verified로 만들지 않았다. 원장은 수정하지 않았다.

## 6. 전체 게이트·다음 판단의 경계

첨부 `DELIVERY_VALIDATION/lhs-isolated-stopped/gate.log:118–120`에 E13d 실패와 50 PASS/1 FAIL이 있으며, 같은 폴더 `state.json`의 반환 코드는 143이다. 초기 믹서 로그에도 시간 제한 실패가 있다. 직접 20개 시험·이번 순수 함수 대조를 이 전체 게이트에 더해 PASS로 바꿀 수 없다. 첨부 게이트 실패의 원인 분석이나 재실행은 이번 범위가 아니다.

현재 결론은 다음과 같다.

1. **값을 출력하지 않는 고정 재고 계수 명령의 준비 방향은 수용한다.**
2. 출력 계약 문구와 오류 처리에는 LPI-01, 시간 상한의 해석에는 LPI-02가 남는다. 둘 다 P3이며 값 노출·핵심 집계 오류를 입증한 것은 아니다.
3. 실제 ibb/WSL 파일 존재·권한·Lustre·실제 stdout/CLI 동작은 미검증이다. 이 문서는 실제 실행을 승인하지 않는다.
4. 압력 판정·복사/전송·등록·단계 A·배포·원장 종결은 이번에 수행하거나 해제하지 않았다.

**전체 게이트: HOLD 유지.**

