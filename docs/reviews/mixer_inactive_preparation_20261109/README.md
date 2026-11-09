# first8 현재 소스의 비활성 사본 — 2026-11-09

**비활성 복사본 준비·한정 합성 검증 완료, 외부 확인 대기, 전체 HOLD.** 운영 봉인·기존 launch 73파일·원 계획 자산 40파일·실행 정책은 변경하지 않았다. 연구 결과 0건이며 실제 자료·호스트·Slurm·MPI·시뮬레이터 접근은 없다.

1저자는 팔당 NP20, 초기 E0 1팔, 자격 확인과 별도 wave 승인 뒤 최대 2팔, E0→검토→N0→검토→B1 U/C→B2 U/C→B3 U/C 정책과 새 복사본의 비활성 준비를 채택했다. 질문·응답 원문과 이후 HOLD 경계는 `author_policy_record.json`에 보존했다. 이 기록은 기계 승인 파일이 아니며, 실제 자원 관측·후속 wave·운영 재봉인·실행 GO를 발급하지 않는다. 이전 준비표의 미비준 상태는 작성 당시 기록으로 남는다.

## 출처와 바뀐 범위

| 역할 | 고정 핀 |
|---|---|
| 이번 부모 B·메타 생성·검증 소스 | `e48e5fa0498ab7ee8fd84163d9af024d07cbb135` |
| 원 덱·STL·메타 생성 출처와 기존 운영 초안 봉인 | `527e244e4ebd6f0cb04c6cfb2ff5f3a52fb01996` |
| 이전 수용 비활성 후보 | `4eb6c593ec5384ed8e51079f5ec7196b1eeae80f` |
| 그 후보의 검증 소스 | `69b6bec7ac20343dd884f8d5fa63e8bf45e7df97` |
| 원 launch 비교 기준 | `e6000405b7625acf8c2c0a393571b116479e0e97` |

`source_inventory.json`의 제한된 12의존은 믹서 스크립트 9개와 STL 3개다. 별도 MGS 검토의 12개 스크립트 묶음과 다르다. 원 봉인 대비 현재 생성기·readback 2개, 이전 후보 검증 소스 대비 생성기 1개가 다르다. launch 73파일은 원 비교 핀 대비 MLAR의 `submit_one.py.txt` 1개가 다르다. 이 누적 변경은 기존 한정 판정의 반입 결과이며 이번 작업에서 고친 것이 아니다.

현재 스냅샷 86파일은 12의존·launch73·기존 준비 시험1로 구성된다. 각 파일의 Git blob 신원과 SHA256을 대조했다. 과거 12의존의 SHA256도 원 `source_seal.json` 및 이전 후보와 일치한다. 이 목록은 검토 스냅샷의 신원표이며 운영 source seal이 아니다. Rint 파일·시험·리뷰는 스냅샷이나 실행 대상에 포함하지 않았다.

## 먼저 재현한 실패와 새 사본

`deck_meta`는 생성기 원바이트 SHA를 기록한다. `validate_case`는 현재 생성기가 만든 메타 전체와 타입 엄격 비교한다. 현재 B에서 원 덱8·원 메타8을 그대로 확인한 최초 시험은 **1메서드 안의 8 subtest 전부 실패, errors0, rc1**이었다. 실패 이유는 모두 `metadata differs from the fixed case recipe`였다. 이 실패는 현재 소스와 옛 메타를 혼합한 경우의 재현이며, 이전 고정 핀의 수용 판정을 철회하거나 새 P를 계상하지 않는다.

새 `candidate/`에는 자산40과 결속 문서3만 있다. 덱8과 STL24는 원바이트 그대로 복사했다. 메타8은 기존 JSON의 `generator_sha256` 값 한 곳만 현재 생성기 SHA로 바꿨으며, 나머지 바이트와 타입·값은 보존했다. 현재 소스에서 다시 생성한 덱8과 메타8이 그 사본에 각각 바이트/타입 엄격 일치함을 확인했다. 원 메타를 현재 소스로 만들었다고 소급 표기하지 않는다.

`candidate_asset_manifest.json`은 원 자산 출처와 현재 메타·검증 소스를 분리한다. `candidate_bindings.json`은 8개 합성 결속이며 관측 입자·연구 결과가 아니다. `inactive_candidate.json`은 별도 schema, `validation_source_pin`, `execution_authorized=false`, `operational_activation=false`, HOLD를 사용한다. 운영 `source_pin`·허용 제출 목록은 없으며, 운영 봉인 자리로 복사하거나 이름을 바꾸지 않았다.

## 한정 검증

| 범위 | 결과 | 해석 |
|---|---|---|
| 원 메타와 현재 소스 혼합 | 8 subtest 실패·rc1 | 위 결속 차이의 최초 재현 |
| 새 사본 | 덱8·메타8·결속8·D2 짝3 PASS | 같은 소스의 생성 대조를 포함하며 독립 물리 검증이 아님 |
| 비활성 계약·자산·스냅샷 거부 탐침 | 33조건 전부 거부 | 계약16·옛 메타8·자산/결속6·스냅샷3; 실제 제출 시험이 아님 |
| 기존 준비 시험 | 변경 없는 14메서드 PASS·rc0 | 8케이스/3짝 등과 중첩되므로 합산하지 않음 |
| 생성 후 별도 읽기 검증 | 동일 43파일 묶음 PASS | build와 verify를 새 고유 시험으로 중복 계상하지 않음 |
| import 신원 내부 보완 | 합성 5메서드: 수정 전 4FAIL/오류0 → 수정 후 5PASS | 아래 캐시/추가 파일/링크 신호 경계; 외부 독립 판정이나 새 P 계상이 아님 |

검증기는 과학 모듈을 불러오기 전에 subprocess/socket audit 차단을 설치한다. 감사 이벤트 두 개만 합성 주입해 차단을 확인했으며 검증기 안에서 실제 Popen/socket을 호출하지 않았다. 추가 process/network 시도는 0이었다. 과학 모듈은 SHA/Git blob을 확인해 이미 읽어 둔 원소스 바이트를 전용 loader에서 compile하며 Python bytecode cache를 읽지 않는다. import 전후에는 스냅샷의 전체 파일·디렉터리 그래프를 86파일 명부와 대조해 추가 모듈·cache·예정 밖 디렉터리를 거부하고, 경로 조상의 symlink/reparse link도 거부한다. 생성은 입력 스냅샷·증거와 겹치지 않는 새 `candidate`에만, 증거 쓰기는 새 증거 폴더에만 허용한다. 시험14는 같은 제한 안에서 직접 불러왔다. 전체 게이트·MLAR/MGS 결함 시험·관측 파이프라인·실제 현장 시험은 반복하지 않았다.

내부 읽기 검토에서 최초 검증기의 `-B`/`dont_write_bytecode`는 기존 cache 읽기를 막지 않고, 명부 밖 파일도 거부하지 않는다는 점을 찾았다. 실제 연구 코드 대신 값 하나를 주는 합성 모듈과 예외 표식만 든 unchecked-hash pyc로 반례를 먼저 남겼다. 고정 `.py`가 그대로인데도 최초 loader에서 표식이 실행됐다. 새 5메서드는 정상 소스, 추가 모듈, cache 그래프, 전용 소스 loader, 조상 링크 신호를 확인한다. 조상 링크는 이식 가능한 mock 신호이며 실제 OS symlink/junction 자격 시험은 아니다. 최종 검증기로 옛 메타의 8실패·새 후보43파일/33거부·기존 준비14를 새 증거 폴더에서 재확인했다. 후보 자산·메타·계약 및 source inventory는 이 보완에서 바꾸지 않았다.

최초 Git archive 준비 4건은 누락 객체 보충 중 연결 실패로 중단됐다. 이후 오프라인 스냅샷 준비에서 파일 mode 범위를 바로잡았고, 한 과거 제출기 파일은 로컬 사본 대신 로컬 Git blob 원바이트로 읽었다. 이 준비 오류들에서는 과학 시험을 돌리지 않았다. 실패 도구 출력은 원 stderr 파일이 아니라 별도 전사 기록으로 구분했다. 최종 스냅샷의 모든 바이트는 고정 Git blob과 대조했고 archive 성공을 주장하지 않는다.

검증 JSON은 `evidence/`에 원바이트로 보존했다. 외부 경로가 포함될 수 있는 콘솔 원로그는 전달 ZIP의 별도 evidence 영역에 두며, 리포의 `evidence.json`에는 상대 식별자와 해시만 기록한다. 라이브 파일시스템의 적대적 동시 변경이나 모든 Python/OS를 인증하는 도구는 아니다.

## 안전한 재현 범위

검토 ZIP의 `snapshot/`은 위 86파일 고정 입력이다. `review/`를 이 폴더의 사본, `candidate/`를 그 안의 이미 생성된 사본이라고 할 때 다음은 비활성 합성 검사만 한다. 증거 경로는 각각 존재하지 않는 새 폴더여야 한다.

```text
python -I -B -X utf8 review/verify_inactive.py --mode old --snapshot snapshot --candidate review/candidate --evidence evidence/red
python -I -B -X utf8 review/verify_inactive.py --mode verify --snapshot snapshot --candidate review/candidate --evidence evidence/green
python -I -B -X utf8 review/verify_inactive.py --mode preparation-tests --snapshot snapshot --candidate review/candidate --evidence evidence/preparation14
python -I -B -X utf8 review/test_snapshot_provenance.py --verifier review/verify_inactive.py --work evidence/import-provenance-green
```

첫 명령의 기대 rc는 1(옛 메타 8실패), 나머지는 0이다. 마지막은 작은 무해한 캐시 표식 fixture만 만들며 과학 모듈을 import하지 않는다. 사본 자체를 다시 만들려면 `--mode build`와 별도의 존재하지 않는 `--candidate`를 쓴다. 기존 후보를 덮어쓰지 않는다. Git/네트워크 호출이나 운영 스크립트 실행은 검증기에 없다. 외부 로컬 시험 runner가 Python 검사 프로세스를 시작한 사실과 검증기 내부의 process/network 시도0을 구분한다. Python·NumPy 등의 설치 환경은 12의존 봉인 밖이며 실제 사용 Python 신원은 증거 JSON에 기록했다.

## 남는 조건

기존 드라이버는 자신 옆의 원 `source_seal.json`과 `static_asset_manifest.json`을 계속 읽는다. 경로·source_pin 동등성 검사를 정적으로 읽었고 드라이버는 import/호출하지 않았다. 따라서 이번 자료가 자동 채택되거나 운영 재봉인이 된 것은 아니다. 과거 69b6/e600 고정 verifier도 이번 B용 검사로 재사용하거나 수정하지 않았다.

새 후보의 외부 한정 확인, 최종 driver/runner/physical manifest 결속과 별도 운영 준비 범위, 실제 binary/MPI·호스트·공유 파일시스템·자원·시간/중단·디스크/회수 자격은 남는다. 100k 양성 파이프라인은 한정 E0 pilot에서 확보할 수 있는 실제 결과이며 이미 완료한 선행 사실로 채우지 않는다. Pilot GO와 이후 map/wave GO는 별개다. 제출 후 런 실패의 자동 HOLD 전파는 없으므로 승인 운영자의 감시·STOP과 검토된 예약 해제·정책 전환이 필요하다. 자동 해제·재시도·resume은 없다.

기존 LHS12·MLA/MLAR·MGS 한정 수용을 다시 열지 않는다. 짧은 `review_request.md`의 범위는 이번 현재 소스/새 메타 사본의 결속과 비활성 경계뿐이며 발송은 1저자다. 원장은 `ledger_proposal.json` 제안만 있고 직접 수정하지 않았다.
