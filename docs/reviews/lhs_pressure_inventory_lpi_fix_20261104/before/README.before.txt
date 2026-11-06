# LHS 압력 로그 재고 준비본 — 값 출력·복사·전송 없음

`pressure_inventory.sh` 한 파일에 표준 라이브러리 Python을 넣었다. 리포·B7 모듈 import가 필요 없다. shell의 큰 heredoc 임시 파일을 피하려고 `python3 -I -B -c`로 실행한다. 입력 로그를 쓸 수 있는 open 옵션이나 파일 생성·전송·제출 명령은 없다. OS의 읽기 access-time 갱신은 별도로 제어하지 않는다.

검토 후 **1저자가 해당 기계에서** 파일로 실행한다. 여기서는 실행하지 않았다.

```sh
sh pressure_inventory.sh ibb
sh pressure_inventory.sh wsl
```

기계별 명령 하나만 선택한다. 출력은 JSON 하나, stderr는 비운다. 출력 저장·리다이렉션·로그 전송 명령은 제공하지 않는다. CLI에 임의 경로나 가드 해제 옵션은 없다.

| 모드 | 실제 신원 가드 | 고정 범위 |
|---|---|---|
| ibb | Linux, short hostname `ibb-master`, 실제 계정 `yonghoon`, real/effective UID 동일 | `/home/yonghoon/dem_test/lhs`: lhs00_000–099 + lhsx_001–064; `/home/yonghoon/lhs_supp_20261006`: lhss_001–020; 합계184 |
| wsl | Linux, 커널 release에 Microsoft, 실제 계정 `yonghoon71`, real/effective UID 동일 | `/home/yonghoon71/lhs_local`: lhs00_100–129; 합계30 |

ibb hostname은 이 세션의 기존 사용자 화면 `ibb-master`에 근거한다. `/home/yonghoon/...`가 정확히 `/lustre/home/yonghoon/...`로 풀리는 root 별칭만 허용한다. root를 연 뒤 case·logs 디렉터리와 최종 파일은 dir-fd + `O_NOFOLLOW`로 접근한다. symlink가 다른 곳을 가리키면 거부한다.

| 출력 | 뜻 |
|---|---|
| `logs.log.liggghts` | 두 모드의 필수 로그. 상태·바이트 수·아래 줄 수만 |
| `logs.log.txt` | WSL만의 추가 필수 로그. 두 파일은 따로 세며 동일 실행 사본인지 비교하지 않음 |
| `b7_matches` | B7 정규식과 `splitlines`에 일치한 줄 수. NaN·문자 토큰도 문법 일치면 센다. **압력 적격성/도달 판정이 아님** |
| `pressure_prefix_malformed` | `Current Pressure:`로 시작하지만 B7 전체 꼴에 안 맞는 줄 수 |
| `read_restart_echo_lines` / `reading_restart_message_lines` | 각각 시작 anchored 명령 echo / 메시지 줄 수. 합쳐서 재개 사건 수로 만들지 않음 |
| `logs_with_b7_matches` | 검사한 필수 로그 중 일치 줄이 한 줄 이상인 파일 수. 둘 이상이어도 재고 완료는 가능하며, B7의 다중 후보 거부를 해제하지 않음 |
| `case_out` / `root_out` | 각각 `case/logs/*.out`, `root/logs/output_<case>_*.out`의 정규 파일 수. 본문을 열지 않고 파일명도 출력하지 않음 |

`rc 0 / INVENTORY_COMPLETE`는 정해진 재고를 읽었다는 뜻이다. 빈 로그·0 일치 줄·문법에 맞는 NaN·중복 로컬 로그도 그 수를 보고할 수 있으며 실제 압력 절차로 넘어가라는 뜻이 아니다. `rc 2 / NOT_ESTABLISHED`는 신원·경로·읽기·변경·파일 종류 등의 제한으로 전체 재고가 성립하지 않았다는 뜻이다. 실패 파일의 부분 줄 수는 내보내지 않는다. 필수 root/case/log 누락은 rc2; 선택 `.out` 검색 디렉터리가 실제로 없는 경우는 `ABSENT / 0`으로 센다. `.out`은 파일 종류·개수만 세며 본문 읽기 가능성을 인증하지 않는다.

각 파일의 읽기 전·후 및 현재 이름의 dev/inode/mode/크기/mtime/ctime/소유자를 대조한다. 디렉터리도 연 구간에서 변경을 검사한다. 전체 184/30개를 원자적 스냅샷으로 잠그지는 않는다. 읽기가 끝난 뒤 수정된 파일이나 같은 재개 사건의 echo/message 중복을 추론하지 않는다. 파일512MiB 초과·물리 줄1Mi 문자 초과·읽은 문자 합512Mi 초과는 `LIMIT / rc2`로 거부한다 (읽는 동안 계속 붙는 파일도 무한히 따라가지 않음).

원문·exception 문자열·임의 파일명·동적으로 얻은 사용자/호스트/경로는 출력하지 않는다. 출력 식별자는 고정 case ID·고정 로그 이름·enum·정수뿐이다. 오류는 고정 코드만 출력한다. 해석기 자체의 시작 실패는 shell이 `RUNTIME_ERROR / rc2`로 바꾼다.

## 합성 검증과 근거

`test_pressure_inventory.py`의 첫19개를 구현보다 먼저 작성했고 `tests_before.log`는 명령 파일 부재로 import 단계 실패 (**0개 실행**, 19개 실패라고 세지 않음)를 보존했다. 뒤에 성장 중인 스트림의 총 읽기 상한 시험을 먼저 더해 실패를 확인했다 (`total_bound_before.log`: 1개 실패) → 상한 구현. 내부 읽기 검토의 지적에 따라 권한 오류 시험을 유효 디렉터리 fd + 실제 주입 호출 단언으로 고쳤다. 검토자는 해당 수정 재확인 뒤 지정 범위의 추가 must-fix 없음을 보고했으며 독립 시험 실행·외부 GO는 하지 않았다.

최종 합성 시험은 **Python3.11.17 20/20** (`tests_after.log`)와 **실제 Python3.8.20 20/20** (`tests_after_py38.log`)이다. 범위·빈/잘못된 줄·중복·재개 구분·오류/파일명 비노출·symlink/FIFO·읽기 중 변경/교체·쓰기 audit·가드·shell 문법·읽기 상한을 검사한다. Python3.8의 실제 shell CLI도 cloud 신원에서 rc2·stderr 빈 출력으로 거부됨을 별도 확인했다 (`cli_py38_refusal.json`, `cli_py38_stderr.log`). 명령 파일 바이트는 이 확인 동안 바꾸지 않았다. 임시 디렉터리와 cloud의 잘못된 신원 거부만 검사했고, 실제 ibb/WSL의 권한·Lustre 동작은 미실행이다.

재현: `python3 -I -B test_pressure_inventory.py`. 실제 테스트 해석기·명령 SHA·B7 정규식 동일성·근거 파일 SHA는 `source_provenance.json`에 기록한다. 출처는 첨부 거부 보고, B7 압력 도구(해시 `34eb74142884489505590501840ccc6423a014a508989c82f135020146283ad3`), canonical `docs/data/lhs_network214_35f032737_20261030/s5_judgment/README.md` §11-3·§11-4다. 기존 원인 분석은 다시 수행하지 않았다. 개발·합성 시험은 scratch에서 했고, 이 폴더에는 그 명령·시험·증거를 반입했다. 등록 문서·B7 도구·공유 원장은 변경하지 않았다.

## 수령·결정·리뷰 경계

1저자는 11-04 이 창의 [LHS] Q1에 **재고 확인만 먼저 준비**를 선택했다. 현재 로그 유무·판정 줄 수·재개 흔적을 보고 다음 A/C를 고르는 준비이며, A의 로그 선택 규칙이나 C의 도구 개정을 비준한 것이 아니다. 실제 ibb/WSL 실행은 이 창에서 하지 않았다.

Claude 쪽지는 `received/20261104-0233_lhs-pressure-refusal.md`에 원문 그대로 보존했다 (16,104 B, SHA256 `6afe50b420bbd4ff0b4a02086de166ab25b430c85810046686a8af16de08ef3a`). 쪽지의 폴더 생성·복사·전송 초안은 실행하지 않는다. 원격 로그 현재 상태, 두 로컬 로그의 동일 실행 여부, 재개 사슬은 아직 미확인이다. 본 명령은 그 쪽지의 전송 블록을 구현한 것이 아니다.

내부 읽기 QA에서 오류 비노출 시험의 잘못된 fd를 고쳐 실제 PermissionError 경로가 호출됐음을 확인하도록 했다. 최종 코드·문서 읽기 대조에서 추가 필수 수정은 보고되지 않았다. 이는 외부 독립 실행·CLOSED·GO가 아니다. 별도 반박 리뷰 요청은 같은 폴더 `review_request.md`; 최종 리뷰 핀은 전달 ZIP의 `PIN.txt`다.

수령 Q1 기록 검토와 재고 명령 검토는 서로 다른 요청 단위다. 이 명령은 공용 게이트에 새 검사로 연결하지 않았으며, 합성 직접 시험 결과를 공용 검사 수에 합산하지 않는다. `source_provenance.json`의 scratch 실행 위치·해석기·소스 해시는 원래 시험 출처로 유지했다. 반입한 명령과 시험의 바이트는 그 최종 증거와 대조한다.
