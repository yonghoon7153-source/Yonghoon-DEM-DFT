# MLAR-01 경로 문자 경계 수정 후보 — 2026-11-09

**비활성 수정 후보 · 외부 재확인 대기 · 실제 연구 결과 0건 · 전체 HOLD.** 2026-11-08 MLA B 후보 독립 검토에서 남은 MLAR-01/P1의 지시문 경로 문자 경계만 다룬다. 실제 제출·MPI·DEM·현장 자격·값 열람·운영 재봉인·등록·배포를 수행하거나 승인하지 않는다. 이 후보의 정적/모의 통과가 외부 종결이나 실행 GO를 만들지 않는다.

## 신원과 원 판정

| 역할 | 핀 또는 기록 |
|---|---|
| 새 가지 바탕 B | `40d9658c07eb578d03dff7905b301da7efacf582` |
| 11-08 독립 검토 대상 B | `a2e0396241c4e4cddea3c8771872f9fdcc650ef7` |
| 원 준비 의존 봉인 | `527e244e4ebd6f0cb04c6cfb2ff5f3a52fb01996` |
| 이번 후보의 최종 검토 핀 | 전달 ZIP의 `PIN.txt` 및 `source_inventory.json`으로 식별 |
| 외부 판정 수령 신원 | `receipt.json` |

11-08 판정은 MLA-01 **부분/열림**, MLA-02·03 **각 원 결함의 아래 범위에서 종결 가능**, 정적 자산·문서 경계 한정 수용이다. MLAR-01은 MLA-01과 같은 제출 경계에 남은 경로 한 건이며 기존 P1과 더해 독립 P1 두 건으로 세지 않는다. 외부 원 증거 ZIP은 리포에 반입하지 않는다. 이 문서는 그 증거를 대체하거나 원장을 직접 닫는 기록이 아니다.

원 launch/recheck README의 MLA-01–03 외부 대기·OPEN 문구는 당시의 역사 기록으로 보존했다. 이번 `receipt.json`과 이 문서가 새 한정 판정을 구분해 적으며, 원 README의 당시 판정을 소급 수정하지 않는다.

## 최소 변경과 확인 범위

대상은 `../mixer_first8_launch_preparation_20261106/submit_one.py.txt`의 `canonical_runner` 경로 검사다. 원 함수는 일반 SPACE/LF만 거부하여 TAB·VT·FF가 출력 지시문에서 별도 옵션 토큰을 만들 수 있었다. 고정된 제출 argv와 환경 필터가 별도 script 옵션을 자동 삭제하는 것은 아니다. 원 CR 사례는 전체 제출 경로에서 이미 거부됐으므로 원 TAB·VT·FF와 같은 전체 우회로로 세지 않는다.

후보의 문자 정책은 기존 네 바인딩 `python`·`job_start`·`stdout`·`stderr`에서 `str.isspace()`가 참인 Unicode 공백, C0(`ord < 32`), DEL(`ord == 127`)을 runner 생성 전에 거부하는 것이다. 모든 C1 문자를 일괄 거부한다고 주장하지 않는다. `test_runner_paths.py`는 Windows 문법 어댑터를 적용하지 않은 canonical 함수(수정 전/후 각각)의 문자 경계와 사전에 준비된 TAB·VT·FF runner의 전체 제출 관문을 대조한다. 정상 경로의 바이트 보존·원 반례 및 추가 음성의 결과는 `source_inventory.json`, `evidence.json`과 이 합성 시험에서 확인한다. shell quoting만으로 Slurm 지시문 파서의 안전성을 주장하지 않는다. 기존 환경/자원 argv/할당 표지 방어는 유지하며 새 기능이나 실제 scheduler 실행을 추가하지 않는다.

수정 전 실패, 수정 후 정상/음성, 기존 환경·할당 회귀의 정확한 명령·Python 신원·rc·관측 단위는 `evidence.json`이 기록한다. `run_mock_checks.py`는 이번 후보용 합성 검사 하니스이며 새 작업 폴더에만 기록한다. 전체 제출/기존 회귀의 Windows leading-slash 문법 어댑터와 가짜 `statvfs` 용량은 시험 복사본에만 적용한다. 어댑터 없는 canonical 함수의 문자 검사와 그 어댑터 경로를 구분하며 실제 POSIX/Slurm 실행 증거로 쓰지 않는다. 로컬 모의의 관측/메서드/버전 반복을 합산해 연구 관측이나 현장 자격으로 보고하지 않는다. 준비용 `commands.txt`, 제출 초안과 sbatch 초안을 직접 실행하는 안내가 아니다.

정식 수정 전 새 시험은 4메서드에서 failure 38·error 0·rc1이었다. `evidence.json`의 `candidate_submit_sha256`에 결속된 최종 LF 후보는 새 4/4와 기존 제출 10/10·작업시작 8/8·MLA 14/14가 각각 통과했다(rc0). 직접 문자 검사 40관측 중 원 함수가 놓친 32건을 포함해 후보는 40건 모두 거부했다. stdout/stderr의 TAB·VT·FF 전체 제출 6관측은 각각 fake sbatch 1회에서 0회로 바뀌고 정상 대조 두 건은 유지됐다. 중간 CRLF 후보의 통과 뒤 수정 파일만 LF로 정규화하여 같은 suite를 다시 확인했으며 두 기록을 보존한다. 이 반복이나 메서드와 그 안의 관측을 더하지 않는다. 이 모의검사 중 실제 외부 process/network 시도는 audit 기록 0건이며 실제 제출·MPI·연구 실행도 0건이다.

재현 입력은 **고정 Git blob 바이트 또는 전달 ZIP의 snapshot**을 사용한다. 정식 전후 검사와 별도로 준비 중단 두 건을 보존한다. 첫 건은 Windows worktree의 `core.autocrlf=true`로 40자산 일부의 바이트가 달라진 경우다. 다음 건은 archive 산출물의 자산 SHA 미일치이며 원인은 확정하지 않았다. 첫 건의 원 stderr는 별도 저장되지 않아 준비 경위 기록으로 남기며, 두 번째의 원 stderr는 보존했다. 두 건 모두 대상 시험 0건으로, 정책 회귀 실패나 통과로 세지 않는다. 정식 수정 전 검사는 원 ZIP의 준비 73파일을 scratch에 복사하고 바탕 B의 Git tree blob OID 73/73과 일치함을 확인한 snapshot을 사용했다. 원본은 수정하지 않으며 전후 후보 변경분을 구분한다. worktree나 실패한 archive 산출물이 그대로 봉인과 일치한다고 주장하지 않는다. 실제 사용한 snapshot 신원과 두 준비 오류/전후 결과는 `evidence.json` 및 `source_inventory.json`으로 대조한다.

### 안전 재현

전달 검토 ZIP을 새 검토용 복사 폴더에 풀고 그 추출 루트에서 아래 두 명령을 각각 사용한다. `snapshot`은 후보, `before`는 수정 전 제출 코드, `sealed_source`는 원 봉인의 12의존 바이트다. `replay-before`와 `replay-after`는 실행 전에 존재하지 않는 새 작업 폴더여야 하며 원본 ZIP·snapshot·기존 결과를 수정하거나 덮어쓰지 않는다. 하니스 내부 외부 호출은 대역이며 실제 제출 명령이 아니다.

수정 전 반례 재현의 기대 종료값은 **rc1**이다:

```text
python -I -B -X utf8 snapshot/docs/reviews/mixer_mlar01_path_recheck_20261109/run_mock_checks.py --repo snapshot --sealed-snapshot sealed_source --work replay-before --phase before --submit-source before/docs/reviews/mixer_first8_launch_preparation_20261106/submit_one.py.txt
```

수정 후 새 시험과 기존 회귀의 기대 종료값은 **rc0**이다:

```text
python -I -B -X utf8 snapshot/docs/reviews/mixer_mlar01_path_recheck_20261109/run_mock_checks.py --repo snapshot --sealed-snapshot sealed_source --work replay-after --phase after --existing
```

## 보존되는 MLA-02·03 판정과 운영 책임

**MLA-02의 종결 가능 범위는 같은 승인 설치·정책·저자 GO에 결속된 제출/예약 경계다.** 공유 admission 원장은 경쟁·상한·pending·실패/불명확/중단된 제출·동일 case 재시도를 차단하는 로컬 모의 근거를 갖는다. 실제 Lustre 원자성·강제 종료/전원 장애 내구성·scheduler 대조·수동 예약 해제는 인증하지 않는다.

**제출 실패·불명확·중단 상태는 공유 원장이 후속 팔을 차단한다. 성공적으로 제출된 뒤의 런 실패는 자동 전파하지 않으며 승인 운영자의 감시·STOP과 별도 회수/해제 절차가 필요하다.** 제출 원장은 `job_end`를 소비하지 않으므로, 이미 `SUBMITTED`인 런이 nonzero/TECH_HOLD가 되거나 start만 남아도 한도가 허용하면 다음 사전 승인 팔을 호출할 수 있다. 이 잔여 운영 책임을 자동 캠페인 HOLD 기능으로 표현하지 않는다.

승인 운영자는 오류·비유한 값·입자 손실·승인된 시간/디스크/진행 한계 위반·진행 미확인 때 후속 파동 제출을 멈추고 TECH/HOLD와 이유·시각·accounting을 기록한다. 취소 권한이 있는 정확한 package job ID만 중단하며 사용자 전체 작업을 취소하지 않는다. 부분 입력/출력/체크포인트/영수증을 보존하고, 정지 상태의 완전한 목록과 새 수령 사본의 해시를 대조한다. 원자료 열람·회수 자체도 해당 실행 범위의 승인을 따라야 하며 이 문서가 새 권한을 주지 않는다.

예약은 제출 명령 종료 후에도 보존한다. 별도로 검토된 scheduler 대조·수동 해제 절차 없이 예약/잔존 lock 삭제·자동 해제·retry·resume·requeue·campaign reset을 하지 않는다. 복사한 별도 설치나 독립 정책으로 한도를 우회하지 않는다. NP·동시성 정책 전환과 예약 계승도 별도 검토 대상이다.

**MLA-03의 종결 가능 범위는 로컬 파일/모의 경로에서 기존 출력의 계산 전 거부·보존, 늦은 종료 영수증의 배타 생성 충돌 보존, 정상/nonzero/일반 spawn 예외의 흔적 보존이다.** native dangling symlink는 독립 검토 환경에서 실제 생성하지 못했으며 `lexists` 정적 대조를 POSIX runtime 증거로 쓰지 않는다. Lustre·전원 장애·일반 signal/crash 복구를 인증하지 않는다. KeyboardInterrupt는 start/streams만 남기고 end가 없을 수 있다. 이 흔적이나 없는 exit code를 정상 완료로 바꾸지 않는다. rc0의 `EXITED_REQUIRES_QUALIFICATION`도 물리 PASS가 아니다.

## 봉인과 승인 경계

원 40개 계획 자산과 12개 의존/source seal, job-start의 바이트는 `source_inventory.json`으로 대조한다. 원 준비 73개 중 제출 코드 한 파일만 달라지고 나머지 72개 blob은 같다. MLA-02/03 로직·옛18·D3 SOP·기타 생산 소스의 불변은 바탕 B 대비 기존 tracked 파일의 Git 차이가 이 제출 코드의 경로 조건과 주석뿐인 것으로 확인한다. 이는 현장 자격의 증명이 아니다. 12개 의존은 원 봉인 핀의 바이트를 **모의 fixture의 해시 대조에만** 사용한다. 최신 B·R01 소비자·새 seed 생성기를 원 봉인에 섞거나 운영 source seal로 교체하지 않는다. 수정 파일 및 새 후보 증거의 신원 결속과 실제 운영 묶음의 재봉인은 별개다.

다음은 그대로 남는다:

- 수정 후보의 MLAR-01 한정 독립 재확인과 Claude의 반입/원장 대응.
- 최종 운영 묶음·source pin·runner·실제 binary/MPI/interpreter·덱/STL·물리 배치 신원과 실제 scheduler/POSIX/공유 파일시스템 자격.
- 실제 100k 양성 경로·시간/디스크/쿼터/출력 예산·감시/중단/회수 기준과 필요한 MXD2R 범위 판정.
- 1저자의 NP·동시 팔·순서·wave·개별 case 범위 결정과 명시된 최종 묶음에 대한 별도 실행 GO.

`.example`과 GO 환경 토큰은 비활성이며 실제 승인 문서의 진위를 인증하지 않는다. `runner_reviewed` 같은 불리언이나 일치하는 해시도 미해결 사실·저자 권한을 대신하지 않는다. `QUALIFICATION_PILOT_GO`는 전체 HOLD 아래 E0 한 건의 검토된 자격 실험 허가이며 완료된 100k 자격을 선행 사실로 꾸미는 것이 아니다. `MAP_CASE_GO`에는 수용된 실제 자격이 추가로 필요하다. pilot 완료·rc0·관측기 OK만으로 후속 case나 MXD2R 종결을 승인하지 않는다. 제출은 승인된 관문을 통해야 하며 raw sbatch는 우회 수단이 아니다.

`review_request.md`는 이 최소 후보의 별도 반박 창 요청서다. 발송은 1저자가 맡으며 이 작업에서 외부 발송하지 않는다. 공유 기록은 별도 `ledger_proposal.json` 제안이며 직접 변경하지 않는다.
