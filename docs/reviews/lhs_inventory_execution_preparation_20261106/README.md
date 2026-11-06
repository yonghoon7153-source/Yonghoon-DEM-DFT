# LHS 재고 실행 준비 — 2026-11-06

**준비·문서·로컬 합성 검사만. Rint② 우선, 전체 HOLD 유지.** 실제 ibb/WSL 접근·재고 실행·압력 값 접근·복사·전송·압력 기록 재작성·단계 A·제출은 하지 않았다. 현장 실행 GO는 이 준비 문서나 합성 PASS로 대신하지 않는다.

기준 main은 `18bb6a2e41ad58129657a68450f4c88157f3d5a6`, 이 가지의 이력 보존 통합 HEAD는 `5ee9cd5351c3d35a7c2c84c6701b820f9edb55d7`이다. 새 준비 파일을 포함하는 최종 검토 PIN은 상위 인계의 PIN 기록을 사용한다. 이 둘이나 그 PIN을 역사적 B7 발사 핀으로 바꾸어 쓰지 않는다.

## 원인과 종결 경계

| 구분 | 증명되는 사실 | 남은 사실 |
|---|---|---|
| OBS-AUDIT-01 / 원장 별칭 LPI-A01, P3 | 재고 명령의 조상 stat→open→fstat 사이 무관 sibling 생성·삭제가 디렉터리 size/mtime/ctime을 바꾸어 CHANGED/rc2를 낼 수 있다. 선택 로그에 쓰기가 없어도 가능하다. | 최초 test17 rc2의 실제 원인은 당시 root/case/errno 상세가 없어 확정 불가. 후속 PASS나 같은 형태의 합성 반례로 역사 원인을 고치거나 종결할 수 없다. |
| 압력 기록 214/214 REFUSED | 보존된 보고의164건 후보0,30건 판정 줄 있는 로그 둘,20건 `logs` 디렉터리 후보 열기 실패는 B7의 후보 부재/모호성 거부 경로와 일치한다. | 현재 원격 로그 유무·두 로컬 로그가 같은 실행인지·재개 사슬은 미관측. 압력 도달 여부나 값의 증거가 아니다. |

코드 근거: `docs/reviews/lhs_pressure_inventory_20261104/pressure_inventory.sh:46–60,79–95,194–205,233–238`의 metadata 비교와 rc 경로; 기존 `test_pressure_inventory.py:221–235`는 rc 단언이 쓰기 audit/전후 파일 단언보다 먼저다. 최초 실패를 “쓰기 검출”로 읽지 않는다. `scripts/lhs_pressure_record.py:117–153`은 덱 검사 뒤 판정 로그0개/둘 이상을137/139행에서 거부한다. 두 프로그램의 서로 다른 사건을 한 원인으로 묶지 않는다.

기존 외부 판정은 `docs/reviews/lhs_pressure_inventory_closure_20261104/external_verdict.txt:63–73`, 기존 결정적 재현은 같은 폴더 `_repro_ours_20261104/probe_obs_audit.py:14–26`, 214건 보고는 `docs/reviews/lhs_pressure_inventory_20261104/received/20261104-0233_lhs-pressure-refusal.md:24–39`다. 보고된 과거 화면 사실을 이번 직접 현장 관측으로 쓰지 않는다.164건 로그 전송 누락과30건 동일 실행 사본설은 그 보고에서도 추정이다.

조상 가드는 변경 입력을 보수적으로 거부하는 정당한 방어다. 가용성 비용은 증명되지만 압력 판독/정확성 결함이나 새 LPI-01 회귀는 증명되지 않았다. **명령·가드·정규식·출력 schema는 수정하지 않는다.** 자동 재시도·조상 비교 완화도 없다. LPI-01 출력 한정 종결, LPI-02 설명/반례 보존 한정 종결과 A01 열린 역사 조사는 별개다. 크기 상한은 시간 상한이 아니다. regex·디렉터리 열거·파일시스템 대기·전체 wall-clock 위험은 미해결이다. 새 합성 wrapper는 root/case 상태를 함께 남기는 진단만 추가한다.

## 한 파일 WSL 실행 준비물

이 폴더의 `pressure_inventory.sh`는 기존 검토 명령의 **바이트 동일 사본**이다. SHA256:

```text
2305bd2194b29ac5439008906a17b1c673968a59fd52dcdde35b03ff4da20634
```

독립 검토가 수용한 최종 PIN/이 해시와 해당 기계의 재고만 실행한다는 1저자의 명시 GO가 있어야 아래 현장 단계로 간다. 새 토큰이나 승인 암호는 요구하지 않는다. 현재 이 파일의 로컬 존재는 실제 WSL 배치를 뜻하지 않는다. 다음 목적지는 준비 패키지의 지정 경로이며 현재 존재/배치 여부는 미확인이다:

```text
/home/yonghoon71/lhs_pressure_inventory_20261106.sh
```

검토된 파일을 이 경로에 배치하는 일도 실제 기계에서는 아직 하지 않았다. 파일이 없거나 다른 바이트이거나 기존 파일을 덮어야 하면 멈춘다. 데이터 폴더의 로그를 이 위치로 복사하지 않는다. 파일 자체는 표준 라이브러리 Python을 포함하며 리포/B7 import나 checkout 변경이 필요 없다. 실행 전 운영자가 위 SHA256, Python3 사용 가능 여부, 아래 신원·경로 조건을 확인한다. `python3 -I -B`는 PATH의 python3을 사용한다. 현재 WSL의 Python 실제 경로/버전은 이 준비에서 측정하지 않았다.

승인 후 실행할 **한 명령**은 아래다. 파일로 실행하며 heredoc·출력 리다이렉션·전송·제출 명령을 덧붙이지 않는다:

```sh
sh /home/yonghoon71/lhs_pressure_inventory_20261106.sh wsl
```

이 명령 직후 셸의 프로세스 종료코드도 확인해야 한다. JSON 안 rc만으로 대신하지 않는다. 이 문서는 stdout 저장이나 수집 업로드를 지시하지 않는다.

`RUN_AFTER_AUTHOR_GO.sh.txt`는 같은 실제 경로를 채운 사전 점검·실행·종료코드 확인 블록이다. 계정·파일 종류·명령 SHA·Python 사용 가능 여부를 먼저 검사하고 stdout은 재고 JSON에 남긴다. 현재는 검토 문서이며 실제 WSL에서 실행하지 않았다. 사전 해시 대조는 원자적 코드 로딩 보장이 아니므로 검토된 파일을 실행 중 변경하지 않는 운영 조건이 필요하다. 이 블록도 승인이나 자동 재시도를 만들지 않는다.

| 호스트 | 신원 조건 | 읽기 범위와 기대 |
|---|---|---|
| WSL | Linux, 실제 계정 yonghoon71, UID=eUID, kernel release에 microsoft. hostname 조건은 없다. | `/home/yonghoon71/lhs_local/lhs00_100`–`lhs00_129`,30건. 각 log.liggghts와 log.txt 필수. |
| ibb, 별도 실행 범위 | Linux, short hostname ibb-master, 실제 계정 yonghoon, UID=eUID, kernel release에 microsoft 없음. | `/home/yonghoon/dem_test/lhs`: lhs00_000–099+lhsx_001–064,164건; `/home/yonghoon/lhs_supp_20261006`: lhss_001–020,20건. 각 log.liggghts 필수. 합184건. |

WSL 실행은 **network194/214 재고가 아니다**.184건을 WSL에서 읽을 기존 명령/검증된 매핑이 없고, ibb의184건과 WSL의30건을 각각 해당 신원/경로에서 확인해야 전체214건의 다음 판단 자료가 된다. ibb 파일 배치와 실제 실행은 별도 승인·준비 범위로 남기며 이 WSL 파일 실행에 SSH/scp를 연결하지 않는다. 기존 명령에는 ibb 모드가 있지만 WSL에서 ibb로 바꾸면 신원 가드가 거부한다.

ibb root는 정해진 `/home/yonghoon/...`→`/lustre/home/yonghoon/...` 별칭만 허용한다. WSL의 root 별칭이나 임의 경로 대체는 허용하지 않는다. case/logs/최종 파일의 symlink와 비정규 파일 거부를 그대로 둔다. 실제 경로가 다르거나 필수 로그가 없으면 우회하지 말고 준비 불성립으로 남긴다.

## 기대 결과·중단 조건

수용에는 **프로세스 rc0 + 완전한 JSON 정확히 하나 + 최상위 INVENTORY_COMPLETE/rc0**가 모두 필요하다. WSL은 mode=wsl, expected_cases=30, counted_cases=30, 고정30 case 집합과 schema=lhs_pressure_inventory/v1이어야 한다. ibb 기대184는 WSL 결과로 채우지 않는다.

신원 불일치, root/case/필수 로그 누락, symlink/비정규 파일, 읽기 오류, 변경, LIMIT는 NOT_ESTABLISHED/rc2다. Python 시작 실패/신호/출력 장애는 JSON 없이 다른 비정상 rc일 수도 있다. JSON이 완전해 보여도 프로세스 rc가0이 아니면 중단한다. 오래 걸리거나 중단되면 완료로 추정하지 않는다. 시간 상한이 없는 현재 명령의 위험을 해소한 것으로 쓰지 않는다.

성공한 재고도 빈 로그, 판정 줄0, 문법에 맞는 NaN 토큰, 로컬 두 로그의 중복을 셀 수 있다. 압력 적격성·동일 실행·재개 사슬·단계 A GO가 아니다. 선택 `.out` 디렉터리 없음은 ABSENT/0일 수 있으며 본문은 열지 않는다. 값·원문·임의 파일명·동적 경로를 새 진단으로 출력하지 않는다. 전체 원자적 스냅샷이나 읽기 후 불변을 보장하지 않는다. OS atime 변경은 별도 제어하지 않는다.

기존 거부 TSV와 R/RS는 보존한다. 실제 WSL 과거 위치는 canonical `docs/data/lhs_network214_35f032737_20261030/s5_judgment/README.md:451`의 `/home/yonghoon71/net194_35f032737_1028/pressure` 및 `/home/yonghoon71/netsupp20_35f032737_1028/pressure`이며 이번에 접근하지 않았다. 이 재고 파일은 그 배치 폴더를 읽거나 쓰지 않는다. 압력 기록, A/C 선택, B7/등록 변경, 단계 A는 별도 결정이다. B7 `35f0327377a4213774010a090df4d224e50d29e1`과 canonical 해시/130+64+20 OK 관문을 우회하지 않는다.

## 로컬 검증·인계

`test_ancestor_diagnostics.py`는 새 임시 디렉터리의 빈 로그만 사용하는 합성 wrapper다. 기준 성공과 결정적 조상 변경 거부, 선택 로그 불변, 거부 시 root/case 사유 보존을 검사한다. 실제 CLI/신원/생산 ROOTS를 실행하지 않는다. 의도적으로 sibling을 쓰는 이 시험을 무쓰기 audit 시험으로 세지 않는다. 결과와 명령은 `evidence/`에 별도 보존한다. 기존 audit 시험과 최초 실패 기록은 고치지 않는다. 상세 판정/공유 원장/발송은 상위 인계가 소유한다.

실제 설치된 Python3.12.14와3.8.20에서 새 합성 시험 각1/1, rc0. `sh -n` rc0, 기존 명령과 `cmp` 동일. `replay_guard_mutation.py`는 새 임시 사본에서 조상 stat/open 비교 하나만 제거하며 Python3.12.14의 새 시험이 기대 rc2/관측rc0으로 실패한다: mutant rc1, runner rc0. 이 음성 대조1건을 정상 PASS로 더하지 않는다. 정확한 argv/로그는 `evidence/validation.json`. 기존 전체 suite·시간 반례를 새로 실행했다고 쓰지 않는다.
